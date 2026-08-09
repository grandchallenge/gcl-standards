from __future__ import annotations

import copy
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "status_coherence", ROOT / "ci" / "status_coherence.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def canonical_evidence() -> dict[str, bytes]:
    return {
        "intellect_readme": b"`GI-AMEND-0001` is effective.\n",
        "intellect_status_page": b"`GI-AMEND-0001` is effective as constitutional version `1.1.0`.\n",
        "amendment": b"**Status:** Effective\n**GCL-GHOS status at activation:** Candidate; not yet admitted\n",
        "gcl_readme": b"`GCL-GHOS-00` is the admitted GitHub Constitutional Operating System.\n",
        "adr": b"**Status:** Accepted\n",
        "standard": b"**Status:** Admitted documentary successor; effective only when selected by a protected admission record\n",
        "admission": b'{"status":"admitted","next_gate":{"status":"complete"}}\n',
        "programme_adoption": b"status: active\n",
    }


def canonical_projection() -> dict[str, object]:
    admission_commit = "a" * 40
    return {
        "$schema": "../schemas/current_status_projection.schema.json",
        "schema_version": "1.0.0",
        "operation_id": "GCL-STATUS-COHERENCE-001",
        "constitutional": {
            "repository": "grandchallenge/INTELLECT",
            "schedule_path": "governance/constitutional_authority_schedule.json",
            "schedule_commit_sha": "b" * 40,
            "amendment": "GI-AMEND-0001",
            "amendment_status": "effective",
            "current_status_authority": "constitutional_status_only",
        },
        "lineage": {
            "predecessor_version": "0.1.0",
            "predecessor_admission": "admissions/GCL-GHOS-00-0.1.0.json",
            "successor_version": "0.1.1",
            "normative_body_sha256": "c9912acb0aacc186f93655e9e1b7938235954bb9466dcddf923cd601ed7bc2a3",
            "normative_body_unchanged": True,
        },
        "selected_admission": {
            "operation_id": "GCL-GHOS-00-0.1.1-ADMISSION-001",
            "path": "admissions/GCL-GHOS-00-0.1.1.json",
            "version": "0.1.1",
            "status": "admitted",
            "front_matter_status": "admitted",
            "commit_sha": admission_commit,
            "next_gate": {"operation": "MATH-PROGRAMME adoption", "status": "complete"},
        },
        "selected_programme_adoption": {
            "programme": "grandchallenge/MATH-PROGRAMME",
            "path": "programme-adoption/MATH-PROGRAMME.yaml",
            "standard_version": "0.1.1",
            "status": "active",
            "commit_sha": "c" * 40,
            "admission_commit_sha": admission_commit,
        },
        "descriptive_assertions": {
            "intellect_readme_amendment_status": "effective",
            "intellect_status_page_amendment_status": "effective",
            "amendment_gcl_status_scope": "candidate_at_activation",
            "gcl_readme_standard_status": "admitted",
            "adr_status": "accepted",
            "standard_front_matter_status": "admitted",
            "admission_adoption_gate_status": "complete",
            "programme_adoption_status": "active",
        },
        "descriptive_evidence": {
            key: {
                "repository": (
                    "grandchallenge/INTELLECT"
                    if key in {"intellect_readme", "intellect_status_page", "amendment"}
                    else "grandchallenge/gcl-standards"
                ),
                "path": f"evidence/{key}",
                "commit_sha": "d" * 40,
                "git_blob_sha1": MODULE.git_blob_sha1(content),
            }
            for key, content in canonical_evidence().items()
        },
        "claim_boundaries": {
            "constitutional_claim_authorized": False,
            "organization_wide_conformance_authorized": False,
            "mathematical_claim_authorized": False,
            "certification_claim_authorized": False,
            "production_claim_authorized": False,
            "novelty_claim_authorized": False,
            "deployment_claim_authorized": False,
            "commercial_claim_authorized": False,
        },
    }


def canonical_receipt() -> dict[str, object]:
    return {
        "$schema": "../schemas/coherence_receipt.schema.json",
        "schema_version": "1.0.0",
        "operation_id": "GCL-STATUS-COHERENCE-001",
        "status": "coherent",
        "contradictions": {
            "open_count": 0,
            "closed_ids": [
                "SC-01", "SC-02", "SC-03", "SC-04", "SC-05",
                "SC-06", "SC-07", "SC-08", "VAL-01",
            ],
        },
        "review_packet": {
            "campaign": "GCL-STATUS-COHERENCE-001",
            "packet_sha256": "a" * 64,
            "steward_authorization_url": "https://github.com/grandchallenge/.github/issues/1#issuecomment-1",
        },
        "reviewed_source_heads": {
            "intellect": "b" * 40,
            "gcl_standards": "c" * 40,
        },
        "protected_merges": {
            "gcl_integration": "d" * 40,
            "gcl_adoption": "e" * 40,
            "intellect_projection": "f" * 40,
            "github_profile": "1" * 40,
        },
        "current_status_projection": {
            "path": "status/GCL-GHOS-00-current.json",
            "git_blob_sha1": "2" * 40,
        },
        "claim_boundaries": {
            "constitutional_claim_authorized": False,
            "organization_wide_conformance_authorized": False,
            "mathematical_claim_authorized": False,
            "certification_claim_authorized": False,
            "production_claim_authorized": False,
            "novelty_claim_authorized": False,
            "deployment_claim_authorized": False,
            "commercial_claim_authorized": False,
        },
    }


class StatusCoherenceTests(unittest.TestCase):
    def test_canonical_projection_and_all_schemas_validate(self) -> None:
        MODULE.validate_schemas()
        MODULE.validate_projection(
            canonical_projection(), evidence_contents=canonical_evidence()
        )

    def test_self_report_cannot_substitute_for_exact_source_content(self) -> None:
        evidence = canonical_evidence()
        evidence["intellect_status_page"] = b"`GI-AMEND-0001` is proposed.\n"
        projection = canonical_projection()
        projection["descriptive_evidence"]["intellect_status_page"][
            "git_blob_sha1"
        ] = MODULE.git_blob_sha1(evidence["intellect_status_page"])
        with self.assertRaisesRegex(
            MODULE.StatusCoherenceError,
            "descriptive assertions do not match exact source blobs",
        ):
            MODULE.validate_projection(projection, evidence_contents=evidence)

    def test_descriptive_blob_identity_drift_is_rejected(self) -> None:
        evidence = canonical_evidence()
        evidence["adr"] += b"drift\n"
        with self.assertRaisesRegex(
            MODULE.StatusCoherenceError, "Git blob drift: adr"
        ):
            MODULE.validate_projection(
                canonical_projection(), evidence_contents=evidence
            )

    def test_exact_coherence_receipt_schema_is_closed_and_zero_conflict(self) -> None:
        schema = MODULE.load_json(ROOT / "schemas" / "coherence_receipt.schema.json")
        MODULE.jsonschema.validate(
            canonical_receipt(),
            schema,
            cls=MODULE.jsonschema.Draft202012Validator,
            format_checker=MODULE.jsonschema.FormatChecker(),
        )
        broken = canonical_receipt()
        broken["contradictions"]["open_count"] = 1
        with self.assertRaises(MODULE.jsonschema.ValidationError):
            MODULE.jsonschema.validate(broken, schema)

    def test_effective_amendment_with_proposed_page_is_rejected(self) -> None:
        broken = copy.deepcopy(canonical_projection())
        broken["descriptive_assertions"]["intellect_status_page_amendment_status"] = "proposed"
        with self.assertRaisesRegex(MODULE.StatusCoherenceError, "effective amendment"):
            MODULE.validate_projection(broken)

    def test_admitted_standard_with_candidate_front_matter_is_rejected(self) -> None:
        broken = copy.deepcopy(canonical_projection())
        broken["descriptive_assertions"]["standard_front_matter_status"] = "candidate"
        with self.assertRaisesRegex(MODULE.StatusCoherenceError, "candidate current front matter"):
            MODULE.validate_projection(broken)

    def test_active_adoption_with_not_started_gate_is_rejected(self) -> None:
        broken = copy.deepcopy(canonical_projection())
        broken["selected_admission"]["next_gate"]["status"] = "not_started"
        with self.assertRaisesRegex(MODULE.StatusCoherenceError, "not_started admission gate"):
            MODULE.validate_projection(broken)

    def test_historical_admission_cannot_be_selected_as_current(self) -> None:
        broken = copy.deepcopy(canonical_projection())
        broken["selected_admission"]["version"] = "0.1.0"
        with self.assertRaisesRegex(MODULE.StatusCoherenceError, "historical admission"):
            MODULE.validate_projection(broken)

    def test_successor_lineage_is_required(self) -> None:
        broken = copy.deepcopy(canonical_projection())
        broken.pop("lineage")
        with self.assertRaises(MODULE.jsonschema.ValidationError):
            MODULE.validate_projection(broken)

    def test_adoption_must_bind_selected_admission(self) -> None:
        broken = copy.deepcopy(canonical_projection())
        broken["selected_programme_adoption"]["admission_commit_sha"] = "d" * 40
        with self.assertRaisesRegex(MODULE.StatusCoherenceError, "does not bind"):
            MODULE.validate_projection(broken)

    def test_claim_authority_inflation_is_rejected(self) -> None:
        broken = copy.deepcopy(canonical_projection())
        broken["claim_boundaries"]["mathematical_claim_authorized"] = True
        with self.assertRaises(Exception):
            MODULE.validate_projection(broken)

    def test_receipt_requires_every_fixed_nonclaim_boundary(self) -> None:
        schema = MODULE.load_json(ROOT / "schemas" / "coherence_receipt.schema.json")
        broken = canonical_receipt()
        del broken["claim_boundaries"]["commercial_claim_authorized"]
        with self.assertRaises(MODULE.jsonschema.ValidationError):
            MODULE.jsonschema.validate(broken, schema)


if __name__ == "__main__":
    unittest.main()
