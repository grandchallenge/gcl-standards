from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
from typing import Any

import jsonschema

import ghos_control_plane as control


ROOT = Path(__file__).resolve().parents[1]
CONTROL_GLOB = ".ghos-control/*/ledger.json"
CONTROL_ID = "GCL-GHOS-CONTROL-PLANE-REMEDIATION-001"
CONTROL_DIRECTORY = f".ghos-control/{CONTROL_ID}"
CONTROL_REF = "refs/heads/control/GCL-GHOS-CONTROL-PLANE-REMEDIATION-002"
CONTROL_RULESET_ID = 21856524


class ControlStoreError(ValueError):
    pass


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ControlStoreError(f"control record must be an object: {path}")
    return value


def validate_control_directory(directory: Path, *, repository_root: Path = ROOT) -> dict[str, Any]:
    schema = _load(repository_root / "schemas" / "ghos_control_plane.schema.json")
    catalog = _load(
        repository_root
        / "implementation"
        / "GCL-GHOS-CONTROL-PLANE-REMEDIATION-001"
        / "control-plane"
        / "transition-catalog.json"
    )
    admission = _load(directory / "admission.json")
    ledger = _load(directory / "ledger.json")
    store = _load(directory / "store.json")

    for record in (admission, ledger):
        jsonschema.validate(record, schema, cls=jsonschema.Draft202012Validator)
    if ledger["storage_status"] != "PROTECTED_CONTROL_REF":
        raise ControlStoreError("operational ledger is not on a protected control ref")
    if ledger["catalog_digest"] != control.catalog_digest(catalog):
        raise ControlStoreError("control ledger catalog digest drift")
    control.validate_event_sequence(ledger)
    first = ledger["events"][0]
    if first["event_type"] != "WORK_PACKAGE_ADMITTED":
        raise ControlStoreError("control ledger does not begin with admission")
    if first["payload"]["admission_digest"] != control.digest(admission):
        raise ControlStoreError("control ledger admission digest drift")
    if store.get("work_package") != ledger["work_package"]:
        raise ControlStoreError("control store work-package substitution")
    expected_store = {
        "repository": "grandchallenge/gcl-standards",
        "ref": CONTROL_REF,
        "ruleset_id": CONTROL_RULESET_ID,
        "ruleset_url": f"https://github.com/grandchallenge/gcl-standards/rules/{CONTROL_RULESET_ID}",
    }
    if any(store.get(key) != value for key, value in expected_store.items()):
        raise ControlStoreError("control store repository/ref/ruleset substitution")
    if not store.get("deletion_prohibited") or not store.get("non_fast_forward_prohibited"):
        raise ControlStoreError("control store lacks append-only ref protection")
    if store.get("claim_boundaries") != control.CLAIM_BOUNDARIES:
        raise ControlStoreError("control store widens authority")

    projection = _load(repository_root / "status" / "GCL-GHOS-00-current.json")
    authority = control.resolve_effective_authority(root=repository_root, projection=projection)
    state = control.reduce_ledger(ledger, catalog, authority, admission)
    jsonschema.validate(state, schema, cls=jsonschema.Draft202012Validator)
    return state


def validate_append_prefix(
    directory: Path,
    *,
    base_admission: dict[str, Any],
    base_ledger: dict[str, Any],
    base_store: dict[str, Any],
) -> None:
    admission = _load(directory / "admission.json")
    ledger = _load(directory / "ledger.json")
    store = _load(directory / "store.json")
    if admission != base_admission or store != base_store:
        raise ControlStoreError("control admission/store identity changed after initialization")
    immutable_keys = set(base_ledger) - {"events", "ledger_head_digest"}
    if any(ledger.get(key) != base_ledger.get(key) for key in immutable_keys):
        raise ControlStoreError("control ledger identity changed")
    prior_events = base_ledger["events"]
    if len(ledger["events"]) <= len(prior_events):
        raise ControlStoreError("control update must append at least one event")
    if ledger["events"][: len(prior_events)] != prior_events:
        raise ControlStoreError("control update rewrites prior event history")


def _git_json(root: Path, revision: str, relative: str) -> dict[str, Any]:
    try:
        contents = subprocess.check_output(
            ["git", "show", f"{revision}:{relative}"], cwd=root
        )
        value = json.loads(contents)
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError) as exc:
        raise ControlStoreError(f"cannot resolve exact base control record: {relative}") from exc
    if not isinstance(value, dict):
        raise ControlStoreError(f"base control record is not an object: {relative}")
    return value


def validate(*, root: Path = ROOT) -> None:
    ledger_paths = sorted(root.glob(CONTROL_GLOB))
    target_ref = os.environ.get("GHOS_CONTROL_TARGET_REF")
    base_sha = os.environ.get("GHOS_CONTROL_BASE_SHA")
    if target_ref == CONTROL_REF:
        expected = root / CONTROL_DIRECTORY / "ledger.json"
        if ledger_paths != [expected]:
            raise ControlStoreError("protected control update deleted, renamed, or duplicated the ledger")
        if not base_sha:
            raise ControlStoreError("protected control update lacks exact base SHA")
        directory = expected.parent
        validate_append_prefix(
            directory,
            base_admission=_git_json(root, base_sha, f"{CONTROL_DIRECTORY}/admission.json"),
            base_ledger=_git_json(root, base_sha, f"{CONTROL_DIRECTORY}/ledger.json"),
            base_store=_git_json(root, base_sha, f"{CONTROL_DIRECTORY}/store.json"),
        )
    for ledger_path in ledger_paths:
        validate_control_directory(ledger_path.parent, repository_root=root)


if __name__ == "__main__":
    validate()
    print("protected GH-OS control stores validated")
