from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path

import jsonschema
import yaml

from git_content import git_blob_sha1


ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "gcl_id_admission.schema.json"
ADMISSION = ROOT / "admissions" / "GCL-ID-00-0.1.0.json"
STANDARD = ROOT / "standards" / "GCL-ID-00.md"
STATUS = ROOT / "status" / "GCL-ID-00-current.json"
TEMPLATE = ROOT / "templates" / "identifiability_preflight.yaml"


class GCLIDError(ValueError):
    pass


def _load_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_yaml(path: Path) -> object:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def validate_admission_record(admission: Mapping[str, object]) -> None:
    schema = _load_json(SCHEMA)
    jsonschema.Draft202012Validator.check_schema(schema)
    jsonschema.validate(
        admission,
        schema,
        cls=jsonschema.Draft202012Validator,
        format_checker=jsonschema.FormatChecker(),
    )

    reviews = admission["source_reviews"]
    if not isinstance(reviews, Mapping):
        raise GCLIDError("source reviews must be structured")
    adversary = reviews["adversary"]
    referee = reviews["referee"]
    if not isinstance(adversary, Mapping) or not isinstance(referee, Mapping):
        raise GCLIDError("review bindings must be structured")
    if adversary["logical_pass_id"] == referee["logical_pass_id"]:
        raise GCLIDError("Adversary and Referee require distinct logical passes")
    if adversary["record_ref"] == referee["record_ref"]:
        raise GCLIDError("Adversary and Referee require distinct durable records")
    if adversary["candidate_head"] != referee["candidate_head"]:
        raise GCLIDError("review subject drift")
    if adversary["finding"] != "approved" or referee["finding"] != "approved":
        raise GCLIDError("both source reviews must approve the reviewed candidate")

    authority = admission["staffing_authority"]
    if not isinstance(authority, Mapping):
        raise GCLIDError("staffing authority must be structured")
    if authority["reserved_action_required"]:
        raise GCLIDError("GCL-ID-00 admission is not a reserved action")
    if authority["human_steward_gate"] != "not_applicable_under_GI_STEWARD_0003":
        raise GCLIDError("staffing authority drift")

    claims = admission["claim_boundaries"]
    if not isinstance(claims, Mapping) or any(bool(value) for value in claims.values()):
        raise GCLIDError("standards admission cannot manufacture downstream authority")


def validate_template_record(template: Mapping[str, object]) -> None:
    if template.get("standard") != "GCL-ID-00":
        raise GCLIDError("template standard identity drift")
    if template.get("standard_version") != "0.1.0":
        raise GCLIDError("template standard version drift")
    solver_gate = template.get("solver_gate")
    if not isinstance(solver_gate, Mapping) or solver_gate.get("may_claim_full_recovery") is not False:
        raise GCLIDError("template must fail closed on full-recovery claims")
    boundaries = template.get("claim_boundary")
    if not isinstance(boundaries, Mapping) or any(bool(value) for value in boundaries.values()):
        raise GCLIDError("template claim boundary must fail closed")


def validate_standard() -> None:
    text = STANDARD.read_text(encoding="utf-8")
    required = (
        "Before solving an inverse problem, characterize what the observation map has already transformed away.",
        "Absence of a known symmetry SHALL NOT be reported as proof of injectivity.",
        "A structural ambiguity SHALL NOT be treated as an optimization defect.",
        "MATHCERT retains sole certification authority",
        "\"Try a stronger solver\" is not, by itself, a response to a proved structural ambiguity.",
    )
    for token in required:
        if token not in text:
            raise GCLIDError(f"missing GCL-ID-00 boundary: {token}")

    forbidden = [
        (index, ord(character))
        for index, character in enumerate(text)
        if ord(character) < 32 and ord(character) not in (10, 13)
    ]
    if forbidden:
        raise GCLIDError(f"control characters in GCL-ID-00 source: {forbidden[:5]}")

    if git_blob_sha1(STANDARD, root=ROOT) != "4a7d5968bdbce38e6e462ed7c17a61ea6d5ca992":
        raise GCLIDError("reviewed GCL-ID-00 source blob drift")


def validate_status() -> None:
    status = _load_json(STATUS)
    if not isinstance(status, Mapping):
        raise GCLIDError("GCL-ID-00 status must be an object")
    if status.get("identifier") != "GCL-ID-00" or status.get("version") != "0.1.0":
        raise GCLIDError("GCL-ID-00 status identity drift")
    if status.get("status") != "admitted":
        raise GCLIDError("GCL-ID-00 status must be admitted after admission record integration")
    admission = status.get("admission")
    if not isinstance(admission, Mapping):
        raise GCLIDError("GCL-ID-00 status requires admission binding")
    if admission.get("record") != "admissions/GCL-ID-00-0.1.0.json":
        raise GCLIDError("GCL-ID-00 status admission record drift")
    programme = status.get("programme_adoption")
    if not isinstance(programme, Mapping) or programme.get("status") != "not_yet_adopted":
        raise GCLIDError("programme adoption must remain separate from standards admission")


def validate() -> None:
    admission = _load_json(ADMISSION)
    if not isinstance(admission, Mapping):
        raise GCLIDError("admission record must be an object")
    validate_admission_record(admission)
    validate_standard()
    validate_status()

    template = _load_yaml(TEMPLATE)
    if not isinstance(template, Mapping):
        raise GCLIDError("identifiability preflight template must be an object")
    validate_template_record(template)


if __name__ == "__main__":
    validate()
    print("GCL-ID-00 validation passed")
