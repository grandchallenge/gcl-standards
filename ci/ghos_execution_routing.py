from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Mapping

import jsonschema
import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_ROOT = ".github/workflows"
REGISTRY_PATH = ".ghos-routing/workflows.json"
SCHEMA_PATH = "schemas/ghos_execution_routing.schema.json"
CLAIM_BOUNDARIES = {
    "constitutional": False, "merge": False, "certification": False,
    "production": False, "publication": False, "mathematical_claim": False,
    "claim_promotion": False, "commercial": False,
}
ADMITTED_CONTROLLERS = [{
    "controller_id": "GITHUB_ACTIONS",
    "executor_class": "PERSISTENT_CONTROLLER",
    "provider": "github",
    "durable_wake_mechanism": "repository-bound GitHub Actions event queue",
    "state_store": "GitHub Actions workflow run and job records bound to repository and commit SHA",
    "supported_features": ["AUTONOMOUS_WAKE", "EXTERNAL_REUSABLE_JOB", "EXTERNAL_WAIT",
        "NON_RECONCILABLE_MUTATION", "OPAQUE_EXECUTION", "SCHEDULED", "SECRET_CREDENTIAL",
        "UNATTENDED_DISPATCH", "WRITE_CAPABLE"],
}]


class RoutingError(ValueError):
    pass


def _load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RoutingError(f"routing record must be an object: {path}")
    return value


def _load_workflow(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RoutingError(f"workflow must be a mapping: {path}")
    return value


def workflow_paths(root: Path) -> list[str]:
    directory = root / WORKFLOW_ROOT
    return sorted(
        path.relative_to(root).as_posix()
        for pattern in ("*.yml", "*.yaml")
        for path in directory.glob(pattern)
        if path.is_file()
    )


def observed_features(workflow: Mapping[str, Any]) -> list[str]:
    # PyYAML 1.1 may decode the key `on` as True.
    triggers = workflow.get("on", workflow.get(True, {}))
    if isinstance(triggers, str):
        trigger_names = {triggers}
    elif isinstance(triggers, list):
        trigger_names = set(triggers)
    elif isinstance(triggers, Mapping):
        trigger_names = set(triggers)
    else:
        trigger_names = set()

    features: set[str] = set()
    if "schedule" in trigger_names:
        features.update({"SCHEDULED", "AUTONOMOUS_WAKE"})
    if trigger_names.intersection({"repository_dispatch", "workflow_run"}):
        features.update({"UNATTENDED_DISPATCH", "AUTONOMOUS_WAKE"})

    def write_capable(permissions: object) -> bool:
        return isinstance(permissions, str) and permissions == "write-all" or (
            isinstance(permissions, Mapping)
            and any(value == "write" for value in permissions.values())
        )

    if write_capable(workflow.get("permissions")):
        features.add("WRITE_CAPABLE")

    jobs = workflow.get("jobs", {})
    if not isinstance(jobs, Mapping):
        raise RoutingError("workflow jobs must be a mapping")
    for job in jobs.values():
        if not isinstance(job, Mapping):
            raise RoutingError("workflow job must be a mapping")
        if "uses" in job:
            features.add("EXTERNAL_REUSABLE_JOB")
        if write_capable(job.get("permissions")):
            features.add("WRITE_CAPABLE")
        text = json.dumps(job, sort_keys=True).lower()
        if '"uses":' in text:
            features.add("OPAQUE_EXECUTION")
        if '"run":' in text:
            features.add("OPAQUE_EXECUTION")
        if "${{ secrets." in text or "secrets[" in text or "github.token" in text:
            features.add("SECRET_CREDENTIAL")
        if any(token in text for token in ("gh run watch", "sleep ", "poll", "wait-for", "wait_for")):
            features.add("EXTERNAL_WAIT")
        if "ghos-non-reconcilable-mutation" in text:
            features.add("NON_RECONCILABLE_MUTATION")
        if any(token in text for token in ("gh pr merge", "git push", "git.exe push", "gh release create", "gh api", "-x post", "-x patch", "-x put", "-x delete")):
            features.add("WRITE_CAPABLE")
    return sorted(features)


def derive_topology(features: set[str]) -> str:
    if features.intersection({"AUTONOMOUS_WAKE", "NON_RECONCILABLE_MUTATION", "OPAQUE_EXECUTION", "SECRET_CREDENTIAL", "WRITE_CAPABLE"}):
        return "PERSISTENT_CONTROLLER_REQUIRED"
    if features.intersection({"EXTERNAL_REUSABLE_JOB", "EXTERNAL_WAIT", "UNATTENDED_DISPATCH"}):
        return "MULTI_SESSION_RESUMABLE"
    return "BOUNDED_ATOMIC"


def validate(*, root: Path = ROOT, expected_repository: str | None = None) -> None:
    schema = _load_json(root / SCHEMA_PATH)
    registry = _load_json(root / REGISTRY_PATH)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(registry, schema, cls=jsonschema.Draft202012Validator)
    if registry["claim_boundaries"] != CLAIM_BOUNDARIES:
        raise RoutingError("execution-routing registry widens authority")
    if registry["controllers"] != ADMITTED_CONTROLLERS:
        raise RoutingError("controller catalog is not the governed admitted-controller set")
    expected_repository = expected_repository or os.environ.get("GITHUB_REPOSITORY")
    if expected_repository and registry["repository"] != expected_repository:
        raise RoutingError("execution-routing repository identity mismatch")

    discovered = workflow_paths(root)
    entries = registry["workflows"]
    registered = [entry["path"] for entry in entries]
    if len(registered) != len(set(registered)):
        raise RoutingError("workflow routing registry contains duplicate paths")
    if registered != discovered:
        missing = sorted(set(discovered) - set(registered))
        stale = sorted(set(registered) - set(discovered))
        raise RoutingError(f"workflow routing coverage mismatch: missing={missing}, stale={stale}")

    by_path = {entry["path"]: entry for entry in entries}
    controllers = {item["controller_id"]: item for item in registry["controllers"]}
    if len(controllers) != len(registry["controllers"]):
        raise RoutingError("controller catalog contains duplicate identities")
    for relative in discovered:
        entry = by_path[relative]
        features = observed_features(_load_workflow(root / relative))
        if entry["observed_features"] != features:
            raise RoutingError(f"workflow feature declaration drift: {relative}")
        topology = derive_topology(set(features))
        if entry["topology"] != topology:
            raise RoutingError(f"workflow topology declaration drift: {relative}")

        controller_id = entry["controller_id"]
        if topology != "BOUNDED_ATOMIC":
            if controller_id not in controllers:
                raise RoutingError(f"persistent workflow lacks admitted controller: {relative}")
            unsupported = set(features) - set(controllers[controller_id]["supported_features"])
            if unsupported:
                raise RoutingError(f"controller capability mismatch for {relative}: {sorted(unsupported)}")
        elif controller_id is not None:
            raise RoutingError(f"bounded workflow cannot claim persistent controller: {relative}")


if __name__ == "__main__":
    validate()
    print("GH-OS universal execution routing is valid")
