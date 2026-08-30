from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from typing import Any, Mapping

import jsonschema
import yaml


CI_DIR = Path(__file__).resolve().parent
if str(CI_DIR) not in sys.path:
    sys.path.insert(0, str(CI_DIR))

from git_content import (  # noqa: E402
    git_blob_sha1,
    git_blob_sha1_at_commit,
    git_bytes_at_commit,
)


ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"
CURRENT_STATUS_PATH = ROOT / "status" / "GCL-GHOS-00-current.json"
COHERENCE_RECEIPT_PATH = (
    ROOT
    / "evidence"
    / "coherence-reviews"
    / "GCL-GHOS-ACTIVE-VERSION-RECONCILIATION-001.json"
)
REVIEW_RECEIPT_PATH = (
    ROOT
    / "evidence"
    / "coherence-reviews"
    / "GCL-STATUS-COHERENCE-001-b39b2f3fab12.json"
)


class StatusCoherenceError(ValueError):
    pass


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise StatusCoherenceError(f"record must be an object: {path}")
    return value


def projection_schema(*, root: Path = ROOT) -> dict[str, Any]:
    schema_dir = root / "schemas"
    schema = copy.deepcopy(load_json(schema_dir / "current_status_projection.schema.json"))
    schema["properties"]["lineage"] = load_json(
        schema_dir / "standard_successor_lineage.schema.json"
    )
    schema["properties"]["selected_admission"] = load_json(
        schema_dir / "current_admission_selection.schema.json"
    )
    schema["properties"]["selected_programme_adoption"] = load_json(
        schema_dir / "current_programme_adoption_selection.schema.json"
    )
    return schema


def _text(contents: Mapping[str, bytes], key: str) -> str:
    try:
        return contents[key].decode("utf-8")
    except (KeyError, UnicodeDecodeError) as exc:
        raise StatusCoherenceError(f"missing or invalid evidence content: {key}") from exc


def _resolve_evidence(
    evidence: Mapping[str, Any], repository_roots: Mapping[str, Path] | None
) -> dict[str, bytes]:
    if repository_roots is None:
        raise StatusCoherenceError("exact Git repository roots are required")
    contents: dict[str, bytes] = {}
    for key, source in evidence.items():
        repository = source["repository"]
        if repository not in repository_roots:
            raise StatusCoherenceError(f"unavailable evidence repository: {repository}")
        root = repository_roots[repository]
        try:
            identity = git_blob_sha1_at_commit(
                root=root,
                commit=source["commit_sha"],
                relative_path=source["path"],
            )
            content = git_bytes_at_commit(
                root=root,
                commit=source["commit_sha"],
                relative_path=source["path"],
            )
        except Exception as exc:
            raise StatusCoherenceError(
                f"cannot resolve exact Git evidence: {key}"
            ) from exc
        if identity != source["git_blob_sha1"]:
            raise StatusCoherenceError(f"descriptive evidence Git blob drift: {key}")
        contents[key] = content
    return contents


def _status_from_text(
    text: str,
    *,
    positive: str,
    negative_patterns: tuple[str, ...],
    status: str,
    key: str,
) -> str:
    if positive not in text:
        raise StatusCoherenceError(f"missing governed status assertion: {key}")
    if any(re.search(pattern, text, flags=re.IGNORECASE) for pattern in negative_patterns):
        raise StatusCoherenceError(f"contradictory governed status assertions: {key}")
    return status


def validate_descriptive_evidence(
    projection: dict[str, Any], repository_roots: Mapping[str, Path] | None
) -> None:
    evidence = projection["descriptive_evidence"]
    evidence_contents = _resolve_evidence(evidence, repository_roots)

    schedule = json.loads(_text(evidence_contents, "schedule"))
    amendment = _text(evidence_contents, "amendment")
    admission = json.loads(_text(evidence_contents, "admission"))
    adoption = yaml.safe_load(_text(evidence_contents, "programme_adoption"))
    if not all(isinstance(value, dict) for value in (schedule, admission, adoption)):
        raise StatusCoherenceError(
            "schedule, admission, and adoption evidence must be objects"
        )

    constitutional = projection["constitutional"]
    current_status_source = schedule.get("operating_standard", {}).get(
        "current_status_source", {}
    )
    schedule_values = {
        "status": schedule.get("status"),
        "amendment": schedule.get("amendment", {}).get("identifier"),
        "amendment_status": schedule.get("amendment", {}).get("status"),
        "effective_version": schedule.get("constitution", {}).get(
            "effective_version"
        ),
        "effective_at": schedule.get("activation", {}).get("effective_at"),
        "current_status_repository": current_status_source.get("repository"),
        "current_status_path": current_status_source.get("path"),
        "current_status_authority": current_status_source.get("authority"),
    }
    expected_schedule_values = {
        "status": "active",
        "amendment": constitutional["amendment"],
        "amendment_status": constitutional["amendment_status"],
        "effective_version": constitutional["effective_version"],
        "effective_at": constitutional["effective_at"],
        "current_status_repository": "grandchallenge/gcl-standards",
        "current_status_path": "status/GCL-GHOS-00-current.json",
        "current_status_authority": "subordinate_admission_and_adoption_projection",
    }
    if schedule_values != expected_schedule_values:
        raise StatusCoherenceError(
            "constitutional projection does not match exact activation schedule"
        )

    selected_admission = projection["selected_admission"]
    admitted_standard = admission.get("standard", {})
    actual_admission = {
        "operation_id": admission.get("operation_id"),
        "status": admission.get("status"),
        "identifier": admitted_standard.get("identifier"),
        "version": admitted_standard.get("version"),
        "next_gate_operation": admission.get("next_gate", {}).get("operation"),
        "next_gate_status": admission.get("next_gate", {}).get("status"),
    }
    expected_admission = {
        "operation_id": selected_admission["operation_id"],
        "status": selected_admission["status"],
        "identifier": "GCL-GHOS-00",
        "version": selected_admission["version"],
        "next_gate_operation": "MATH-PROGRAMME adoption",
        "next_gate_status": "not_started",
    }
    if actual_admission != expected_admission:
        raise StatusCoherenceError(
            "selected admission does not match exact admission record"
        )

    selected_adoption = projection["selected_programme_adoption"]
    admission_commit = adoption.get("standard_admission", {}).get("commit_sha")
    actual_adoption = {
        "programme": adoption.get("programme"),
        "status": adoption.get("status"),
        "standard_version": adoption.get("standard_version"),
        "admission_commit_sha": admission_commit,
    }
    expected_adoption = {
        "programme": selected_adoption["programme"],
        "status": selected_adoption["status"],
        "standard_version": selected_adoption["standard_version"],
        "admission_commit_sha": selected_adoption["admission_commit_sha"],
    }
    if actual_adoption != expected_adoption:
        raise StatusCoherenceError(
            "selected adoption does not match exact programme adoption record"
        )

    public_profile = _text(evidence_contents, "github_profile")
    required_profile_assertions = (
        r"`GI-AMEND-0001`(?::| is) effective",
        r"`GCL-GHOS-00` `0\.2\.0`.*(?:admitted|selected)",
        r"(?:`MATH-PROGRAMME` adoption: active|MATH-PROGRAMME actively adopts)",
        r"GitHub (?:remains\s+|is our\s+)?operational and evidentiary",
    )
    if not all(
        re.search(pattern, public_profile, flags=re.IGNORECASE)
        for pattern in required_profile_assertions
    ):
        raise StatusCoherenceError("public profile does not project exact current status")
    if re.search(
        r"GI-AMEND-0001.*proposed|GCL-GHOS-00.*candidate|adoption.*not_started",
        public_profile,
        flags=re.IGNORECASE,
    ):
        raise StatusCoherenceError("public profile contains contradictory status")

    derived = {
        "intellect_readme_amendment_status": _status_from_text(
            _text(evidence_contents, "intellect_readme"),
            positive="`GI-AMEND-0001` is effective",
            negative_patterns=(r"`GI-AMEND-0001` is proposed", r"GI-AMEND-0001.*proposed; not in force"),
            status="effective",
            key="intellect_readme",
        ),
        "intellect_status_page_amendment_status": _status_from_text(
            _text(evidence_contents, "intellect_status_page"),
            positive="`GI-AMEND-0001` is effective",
            negative_patterns=(r"`GI-AMEND-0001` is proposed", r"GI-AMEND-0001.*proposed; not in force"),
            status="effective",
            key="intellect_status_page",
        ),
        "amendment_gcl_status_scope": _status_from_text(
            amendment,
            positive="**GCL-GHOS status at activation:** Candidate; not yet admitted",
            negative_patterns=(r"\*\*GCL-GHOS status at activation:\*\* Admitted",),
            status="candidate_at_activation",
            key="amendment",
        ),
        "gcl_readme_standard_status": _status_from_text(
            _text(evidence_contents, "gcl_readme"),
            positive="is the admitted GitHub Constitutional",
            negative_patterns=(r"GCL-GHOS-00.* is (?:a |the )?candidate",),
            status="admitted",
            key="gcl_readme",
        ),
        "adr_status": _status_from_text(
            _text(evidence_contents, "adr"),
            positive="**Status:** Accepted",
            negative_patterns=(r"\*\*Status:\*\* (?:Proposed|Candidate)",),
            status="accepted",
            key="adr",
        ),
        "standard_front_matter_status": _status_from_text(
            _text(evidence_contents, "standard"),
            positive="**Status:** Candidate normative successor; no effect until protected successor admission and programme adoption",
            negative_patterns=(),
            status="historical_candidate_metadata",
            key="standard",
        ),
        "admission_adoption_gate_status": (
            "complete"
            if adoption.get("status") == "active"
            and admission_commit == selected_admission["admission_commit_sha"]
            else "not_started"
        ),
        "programme_adoption_status": adoption.get("status"),
        "github_profile_status": "effective_admitted_adopted",
    }
    if derived != projection["descriptive_assertions"]:
        raise StatusCoherenceError("descriptive assertions do not match exact source blobs")


def validate_projection(
    projection: dict[str, Any],
    *,
    root: Path = ROOT,
    repository_roots: Mapping[str, Path] | None = None,
) -> None:
    constitutional = projection.get("constitutional", {})
    assertions = projection.get("descriptive_assertions", {})
    admission = projection.get("selected_admission", {})
    adoption = projection.get("selected_programme_adoption", {})
    lineage = projection.get("lineage", {})

    if constitutional.get("amendment_status") == "effective" and (
        assertions.get("intellect_readme_amendment_status") == "proposed"
        or assertions.get("intellect_status_page_amendment_status") == "proposed"
    ):
        raise StatusCoherenceError(
            "effective amendment cannot have a proposed current status projection"
        )
    if admission.get("status") == "admitted" and (
        admission.get("front_matter_status") != "historical_candidate_metadata"
        or assertions.get("standard_front_matter_status") != "historical_candidate_metadata"
    ):
        raise StatusCoherenceError(
            "selected admission must classify immutable candidate-era front matter as historical metadata"
        )
    if adoption.get("status") == "active" and (
        assertions.get("admission_adoption_gate_status") == "not_started"
    ):
        raise StatusCoherenceError(
            "active programme adoption cannot have a not_started admission gate"
        )
    if admission.get("version") == lineage.get("predecessor_version"):
        raise StatusCoherenceError(
            "historical admission cannot be selected as current without successor lineage"
        )

    schema = projection_schema(root=root)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        projection,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )

    if adoption["admission_commit_sha"] != admission["admission_commit_sha"]:
        raise StatusCoherenceError("programme adoption does not bind selected admission")
    evidence = projection["descriptive_evidence"]
    intellect_commit = projection["constitutional"]["schedule_commit_sha"]
    admission_commit = admission["admission_commit_sha"]
    adoption_commit = adoption["commit_sha"]
    if any(evidence[key]["commit_sha"] != intellect_commit for key in (
        "schedule", "intellect_readme", "intellect_status_page", "amendment"
    )):
        raise StatusCoherenceError("INTELLECT evidence does not bind schedule commit")
    if any(evidence[key]["commit_sha"] != admission_commit for key in (
        "standard", "admission"
    )):
        raise StatusCoherenceError("admission evidence does not bind admission commit")
    if evidence["gcl_readme"]["commit_sha"] != evidence["adr"]["commit_sha"]:
        raise StatusCoherenceError("registry prose evidence does not bind one exact projection commit")
    if evidence["programme_adoption"]["commit_sha"] != adoption_commit:
        raise StatusCoherenceError("adoption evidence does not bind adoption commit")
    if (
        evidence["github_profile"]["commit_sha"]
        != projection["public_profile"]["commit_sha"]
    ):
        raise StatusCoherenceError("public-profile evidence does not bind profile commit")
    validate_descriptive_evidence(projection, repository_roots)
    if any(value is not False for value in projection["claim_boundaries"].values()):
        raise StatusCoherenceError("current-status projection widens prohibited authority")


def validate_coherence_receipt(
    receipt: dict[str, Any], projection: dict[str, Any], *, root: Path = ROOT
) -> None:
    schema = load_json(root / "schemas" / "active_version_reconciliation_receipt.schema.json")
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        receipt,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )

    projection_path = root / receipt["current_status_projection"]["path"]
    if git_blob_sha1(projection_path, root=root) != receipt[
        "current_status_projection"
    ]["git_blob_sha1"]:
        raise StatusCoherenceError("coherence receipt projection Git blob drift")

    expected_merges = {
        "gcl_integration": projection["selected_admission"]["admission_commit_sha"],
        "gcl_adoption": projection["selected_programme_adoption"]["commit_sha"],
        "intellect_projection": projection["constitutional"]["schedule_commit_sha"],
        "github_profile": projection["public_profile"]["commit_sha"],
    }
    if receipt["protected_merges"] != expected_merges:
        raise StatusCoherenceError("coherence receipt protected-merge binding drift")
    if receipt["claim_boundaries"] != projection["claim_boundaries"]:
        raise StatusCoherenceError("coherence receipt claim-boundary drift")
    expected_heads = {
        "intellect": projection["constitutional"]["schedule_commit_sha"],
        "gcl_standards": projection["descriptive_evidence"]["gcl_readme"]["commit_sha"],
    }
    if receipt["reviewed_source_heads"] != expected_heads:
        raise StatusCoherenceError("coherence receipt reviewed-source binding drift")
    packet_payload = {
        "current_status_projection": receipt["current_status_projection"],
        "protected_merges": receipt["protected_merges"],
        "reviewed_source_heads": receipt["reviewed_source_heads"],
    }
    expected_packet = hashlib.sha256(
        json.dumps(packet_payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()
    if receipt["review_packet"]["packet_sha256"] != expected_packet:
        raise StatusCoherenceError("coherence receipt packet binding drift")


def _run_git(*arguments: str, cwd: Path | None = None) -> None:
    try:
        subprocess.run(
            ["git", *arguments],
            cwd=cwd,
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise StatusCoherenceError(
            f"cannot fetch exact protected evidence: {' '.join(arguments)}"
        ) from exc


def _fetch_exact_repository(
    destination: Path, repository: str, commits: set[str]
) -> None:
    destination.mkdir(parents=True)
    _run_git("init", "--bare", "--quiet", cwd=destination)
    remote = f"https://github.com/{repository}.git"
    for commit in sorted(commits):
        _run_git(
            "fetch",
            "--quiet",
            "--no-tags",
            "--depth=1",
            remote,
            commit,
            cwd=destination,
        )


def validate_current_status(*, root: Path = ROOT) -> None:
    projection = load_json(root / "status" / "GCL-GHOS-00-current.json")
    receipt = load_json(
        root
        / "evidence"
        / "coherence-reviews"
        / "GCL-GHOS-ACTIVE-VERSION-RECONCILIATION-001.json"
    )
    commits_by_repository: dict[str, set[str]] = {}
    for source in projection["descriptive_evidence"].values():
        commits_by_repository.setdefault(source["repository"], set()).add(
            source["commit_sha"]
        )

    with tempfile.TemporaryDirectory(prefix="gcl-status-coherence-") as temporary:
        temporary_root = Path(temporary)
        repository_roots = {"grandchallenge/gcl-standards": root}
        for repository, commits in commits_by_repository.items():
            if repository == "grandchallenge/gcl-standards":
                continue
            destination = temporary_root / repository.split("/", maxsplit=1)[1]
            _fetch_exact_repository(destination, repository, commits)
            repository_roots[repository] = destination
        validate_projection(
            projection,
            root=root,
            repository_roots=repository_roots,
        )
    validate_coherence_receipt(receipt, projection, root=root)


def validate_schemas(*, root: Path = ROOT) -> None:
    for name in (
        "standard_successor_lineage.schema.json",
        "current_admission_selection.schema.json",
        "current_programme_adoption_selection.schema.json",
        "current_status_projection.schema.json",
        "coherence_receipt.schema.json",
        "active_version_reconciliation_receipt.schema.json",
    ):
        jsonschema.Draft202012Validator.check_schema(load_json(root / "schemas" / name))


if __name__ == "__main__":
    validate_schemas()
    validate_current_status()
    print("status coherence schemas and exact protected records validated")
