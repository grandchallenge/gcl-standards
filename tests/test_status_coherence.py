from __future__ import annotations

import copy
import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "status_coherence", ROOT / "ci" / "status_coherence.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def canonical_evidence(admission_commit: str = "0" * 40) -> dict[str, bytes]:
    return {
        "schedule": (
            b'{"status":"active","constitution":{"effective_version":"1.1.0"},'
            b'"amendment":{"identifier":"GI-AMEND-0001","status":"effective"},'
            b'"operating_standard":{"current_status_source":{"repository":"grandchallenge/gcl-standards",'
            b'"path":"status/GCL-GHOS-00-current.json","authority":"subordinate_admission_and_adoption_projection"}},'
            b'"activation":{"effective_at":"2026-08-03T10:00:00Z"}}\n'
        ),
        "intellect_readme": b"`GI-AMEND-0001` is effective.\n",
        "intellect_status_page": b"`GI-AMEND-0001` is effective as constitutional version `1.1.0`.\n",
        "amendment": b"**Status:** Effective\n**GCL-GHOS status at activation:** Candidate; not yet admitted\n",
        "gcl_readme": b"`GCL-GHOS-00` is the admitted GitHub Constitutional Operating System.\n",
        "adr": b"**Status:** Accepted\n",
        "standard": b"**Version:** 0.2.0\n**Status:** Candidate normative successor; no effect until protected successor admission and programme adoption\n",
        "admission": (
            b'{"operation_id":"GCL-GHOS-00-0.2.0-ADMISSION-001",'
            b'"status":"admitted","standard":{"identifier":"GCL-GHOS-00",'
            b'"version":"0.2.0"},"next_gate":{"operation":"MATH-PROGRAMME adoption",'
            b'"status":"not_started"}}\n'
        ),
        "programme_adoption": (
            "programme: grandchallenge/MATH-PROGRAMME\n"
            "status: active\n"
            "standard_version: 0.2.0\n"
            "standard_admission:\n"
            f"  commit_sha: {admission_commit}\n"
        ).encode("utf-8"),
        "github_profile": (
            b"`GI-AMEND-0001`: effective\n"
            b"`GCL-GHOS-00` `0.2.0`: admitted and selected\n"
            b"`MATH-PROGRAMME` adoption: active\n"
            b"GitHub remains operational and evidentiary only.\n"
        ),
    }


EVIDENCE_COORDINATES = {
    "schedule": (
        "grandchallenge/INTELLECT",
        "governance/constitutional_authority_schedule.json",
    ),
    "intellect_readme": ("grandchallenge/INTELLECT", "README.md"),
    "intellect_status_page": ("grandchallenge/INTELLECT", "docs/STATUS.md"),
    "amendment": (
        "grandchallenge/INTELLECT",
        "AMENDMENTS/0001-commentary-and-gcl-ghos.md",
    ),
    "gcl_readme": ("grandchallenge/gcl-standards", "README.md"),
    "adr": (
        "grandchallenge/gcl-standards",
        "decisions/ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md",
    ),
    "standard": ("grandchallenge/gcl-standards", "standards/GCL-GHOS-00.md"),
    "admission": (
        "grandchallenge/gcl-standards",
        "admissions/GCL-GHOS-00-0.2.0.json",
    ),
    "programme_adoption": (
        "grandchallenge/gcl-standards",
        "programme-adoption/MATH-PROGRAMME.yaml",
    ),
    "github_profile": ("grandchallenge/.github", "profile/README.md"),
}


def build_evidence_repositories(
    root: Path,
) -> tuple[dict[str, Path], dict[str, dict[str, str]]]:
    contents = canonical_evidence()
    repository_roots = {
        "grandchallenge/INTELLECT": root / "INTELLECT",
        "grandchallenge/gcl-standards": root / "gcl-standards",
        "grandchallenge/.github": root / ".github",
    }
    key_commits: dict[str, str] = {}
    for repository, repository_root in repository_roots.items():
        repository_root.mkdir(parents=True)
        subprocess.run(["git", "init", "--quiet"], cwd=repository_root, check=True)
        subprocess.run(
            ["git", "config", "user.email", "coherence@example.invalid"],
            cwd=repository_root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Coherence Test"],
            cwd=repository_root,
            check=True,
        )
        for key, (item_repository, path) in EVIDENCE_COORDINATES.items():
            if item_repository != repository or key == "programme_adoption":
                continue
            target = repository_root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(contents[key])
        subprocess.run(["git", "add", "."], cwd=repository_root, check=True)
        subprocess.run(
            ["git", "commit", "--quiet", "-m", "exact evidence"],
            cwd=repository_root,
            check=True,
        )
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repository_root, check=True,
            capture_output=True, text=True,
        ).stdout.strip()
        for key, (item_repository, _) in EVIDENCE_COORDINATES.items():
            if item_repository == repository and key != "programme_adoption":
                key_commits[key] = commit

        if repository == "grandchallenge/gcl-standards":
            adoption_path = EVIDENCE_COORDINATES["programme_adoption"][1]
            target = repository_root / adoption_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(canonical_evidence(commit)["programme_adoption"])
            subprocess.run(
                ["git", "add", adoption_path], cwd=repository_root, check=True
            )
            subprocess.run(
                ["git", "commit", "--quiet", "-m", "exact adoption"],
                cwd=repository_root,
                check=True,
            )
            key_commits["programme_adoption"] = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=repository_root, check=True,
                capture_output=True, text=True,
            ).stdout.strip()

    evidence_refs: dict[str, dict[str, str]] = {}
    for key, (repository, path) in EVIDENCE_COORDINATES.items():
        repository_root = repository_roots[repository]
        commit = key_commits[key]
        blob = subprocess.run(
            ["git", "rev-parse", f"{commit}:{path}"],
            cwd=repository_root,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        evidence_refs[key] = {
            "repository": repository,
            "path": path,
            "commit_sha": commit,
            "git_blob_sha1": blob,
        }
    return repository_roots, evidence_refs


def canonical_projection(
    evidence_refs: dict[str, dict[str, str]],
) -> dict[str, object]:
    intellect_commit = evidence_refs["amendment"]["commit_sha"]
    admission_commit = evidence_refs["admission"]["commit_sha"]
    adoption_commit = evidence_refs["programme_adoption"]["commit_sha"]
    return {
        "$schema": "../schemas/current_status_projection.schema.json",
        "schema_version": "1.0.0",
        "operation_id": "GCL-STATUS-COHERENCE-001",
        "constitutional": {
            "repository": "grandchallenge/INTELLECT",
            "schedule_path": "governance/constitutional_authority_schedule.json",
            "schedule_commit_sha": intellect_commit,
            "effective_version": "1.1.0",
            "effective_at": "2026-08-03T10:00:00Z",
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
            "operation_id": "GCL-GHOS-00-0.2.0-ADMISSION-001",
            "path": "admissions/GCL-GHOS-00-0.2.0.json",
            "version": "0.2.0",
            "status": "admitted",
            "front_matter_status": "historical_candidate_metadata",
            "admission_commit_sha": admission_commit,
        },
        "selected_programme_adoption": {
            "programme": "grandchallenge/MATH-PROGRAMME",
            "path": "programme-adoption/MATH-PROGRAMME.yaml",
            "standard_version": "0.2.0",
            "status": "active",
            "commit_sha": adoption_commit,
            "admission_commit_sha": admission_commit,
        },
        "public_profile": {
            "repository": "grandchallenge/.github",
            "path": "profile/README.md",
            "commit_sha": evidence_refs["github_profile"]["commit_sha"],
        },
        "descriptive_assertions": {
            "intellect_readme_amendment_status": "effective",
            "intellect_status_page_amendment_status": "effective",
            "amendment_gcl_status_scope": "candidate_at_activation",
            "gcl_readme_standard_status": "admitted",
            "adr_status": "accepted",
            "standard_front_matter_status": "historical_candidate_metadata",
            "admission_adoption_gate_status": "complete",
            "programme_adoption_status": "active",
            "github_profile_status": "effective_admitted_adopted",
        },
        "descriptive_evidence": copy.deepcopy(evidence_refs),
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
        "operation_id": "GCL-GHOS-ACTIVE-VERSION-RECONCILIATION-001",
        "status": "candidate_awaiting_protected_readback",
        "contradictions": {
            "open_count": 0,
            "closed_ids": [
                "SC-01", "SC-02", "SC-03", "SC-04", "SC-05",
                "SC-06", "SC-07", "SC-08", "VAL-01",
            ],
        },
        "review_packet": {
            "campaign": "GCL-GHOS-ACTIVE-VERSION-RECONCILIATION-001",
            "packet_sha256": "a" * 64,
            "governing_issue_disposition_url": "https://github.com/grandchallenge/.github/issues/1#issuecomment-1",
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
        "reconciliation_merge": None,
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
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.repository_roots, self.evidence_refs = build_evidence_repositories(
            Path(self.temporary.name)
        )
        self.projection = canonical_projection(self.evidence_refs)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def validate(self, projection: dict[str, object] | None = None) -> None:
        MODULE.validate_projection(
            projection or copy.deepcopy(self.projection),
            repository_roots=self.repository_roots,
        )

    def replace_and_commit(self, key: str, content: bytes) -> dict[str, object]:
        repository, path = EVIDENCE_COORDINATES[key]
        repository_root = self.repository_roots[repository]
        (repository_root / path).write_bytes(content)
        subprocess.run(["git", "add", path], cwd=repository_root, check=True)
        subprocess.run(
            ["git", "commit", "--quiet", "-m", f"mutate {key}"],
            cwd=repository_root,
            check=True,
        )
        projection = copy.deepcopy(self.projection)
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=repository_root, check=True,
            capture_output=True, text=True,
        ).stdout.strip()

        def bind(evidence_key: str, revision: str) -> None:
            item_path = EVIDENCE_COORDINATES[evidence_key][1]
            blob = subprocess.run(
                ["git", "rev-parse", f"{revision}:{item_path}"],
                cwd=repository_root, check=True, capture_output=True, text=True,
            ).stdout.strip()
            projection["descriptive_evidence"][evidence_key]["commit_sha"] = revision
            projection["descriptive_evidence"][evidence_key]["git_blob_sha1"] = blob

        if repository == "grandchallenge/INTELLECT":
            for evidence_key in (
                "schedule", "intellect_readme", "intellect_status_page", "amendment"
            ):
                bind(evidence_key, commit)
            projection["constitutional"]["schedule_commit_sha"] = commit
        elif repository == "grandchallenge/.github":
            bind("github_profile", commit)
            projection["public_profile"]["commit_sha"] = commit
        elif key == "programme_adoption":
            bind("programme_adoption", commit)
            projection["selected_programme_adoption"]["commit_sha"] = commit
        else:
            for evidence_key in ("gcl_readme", "adr", "standard", "admission"):
                bind(evidence_key, commit)
            projection["selected_admission"]["admission_commit_sha"] = commit
            projection["selected_programme_adoption"]["admission_commit_sha"] = commit
            adoption_path = EVIDENCE_COORDINATES["programme_adoption"][1]
            (repository_root / adoption_path).write_bytes(
                canonical_evidence(commit)["programme_adoption"]
            )
            subprocess.run(
                ["git", "add", adoption_path], cwd=repository_root, check=True
            )
            subprocess.run(
                ["git", "commit", "--quiet", "-m", "rebind adoption"],
                cwd=repository_root,
                check=True,
            )
            adoption_commit = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=repository_root, check=True,
                capture_output=True, text=True,
            ).stdout.strip()
            bind("programme_adoption", adoption_commit)
            projection["selected_programme_adoption"]["commit_sha"] = adoption_commit
        return projection

    def test_canonical_projection_and_all_schemas_validate(self) -> None:
        MODULE.validate_schemas()
        self.validate()

    def test_pending_admission_a_then_active_adoption_b_is_coherent(self) -> None:
        admission_commit = self.projection["selected_admission"]["admission_commit_sha"]
        adoption_commit = self.projection["selected_programme_adoption"]["commit_sha"]
        self.assertNotEqual(admission_commit, adoption_commit)
        evidence_contents = MODULE._resolve_evidence(
            self.projection["descriptive_evidence"], self.repository_roots
        )
        self.assertIn(b'"status":"not_started"', evidence_contents["admission"])
        self.assertEqual(
            self.projection["selected_programme_adoption"]["admission_commit_sha"],
            admission_commit,
        )
        self.assertEqual(
            self.projection["descriptive_assertions"]["admission_adoption_gate_status"],
            "complete",
        )
        self.validate()

    def test_self_report_cannot_substitute_for_exact_source_content(self) -> None:
        projection = self.replace_and_commit(
            "intellect_status_page", b"`GI-AMEND-0001` is proposed.\n"
        )
        with self.assertRaisesRegex(
            MODULE.StatusCoherenceError,
            "missing governed status assertion: intellect_status_page",
        ):
            self.validate(projection)

    def test_effective_and_proposed_in_same_blob_is_rejected(self) -> None:
        projection = self.replace_and_commit(
            "intellect_status_page",
            b"`GI-AMEND-0001` is effective.\n`GI-AMEND-0001` is proposed.\n",
        )
        with self.assertRaisesRegex(
            MODULE.StatusCoherenceError,
            "contradictory governed status assertions: intellect_status_page",
        ):
            self.validate(projection)

    def test_standard_without_exact_historical_front_matter_is_rejected(self) -> None:
        projection = self.replace_and_commit(
            "standard",
            b"**Status:** Admitted documentary successor\n**Status:** Candidate\n",
        )
        with self.assertRaisesRegex(
            MODULE.StatusCoherenceError,
            "missing governed status assertion: standard",
        ):
            self.validate(projection)

    def test_exact_schedule_must_match_constitutional_projection(self) -> None:
        projection = self.replace_and_commit(
            "schedule",
            canonical_evidence()["schedule"].replace(
                b'"status":"active"', b'"status":"proposed"'
            ),
        )
        with self.assertRaisesRegex(
            MODULE.StatusCoherenceError, "does not match exact activation schedule"
        ):
            self.validate(projection)

    def test_exact_admission_identity_must_match_selection(self) -> None:
        projection = self.replace_and_commit(
            "admission",
            (
                b'{"operation_id":"WRONG","status":"proposed",'
                b'"standard":{"identifier":"GCL-GHOS-00","version":"9.9.9"},'
                b'"next_gate":{"operation":"MATH-PROGRAMME adoption",'
                b'"status":"not_started"}}\n'
            ),
        )
        with self.assertRaisesRegex(
            MODULE.StatusCoherenceError, "does not match exact admission record"
        ):
            self.validate(projection)

    def test_exact_adoption_target_must_match_selection(self) -> None:
        projection = self.replace_and_commit(
            "programme_adoption",
            (
                "programme: grandchallenge/MATH-PROGRAMME\n"
                "status: active\n"
                "standard_version: 9.9.9\n"
                "standard_admission:\n"
                f"  commit_sha: {'0' * 40}\n"
            ).encode("utf-8"),
        )
        with self.assertRaisesRegex(
            MODULE.StatusCoherenceError,
            "does not match exact programme adoption record",
        ):
            self.validate(projection)

    def test_stale_public_profile_is_rejected(self) -> None:
        projection = self.replace_and_commit(
            "github_profile",
            b"`GI-AMEND-0001`: proposed\n`GCL-GHOS-00`: candidate\n",
        )
        with self.assertRaisesRegex(
            MODULE.StatusCoherenceError, "public profile does not project"
        ):
            self.validate(projection)

    def test_descriptive_blob_identity_drift_is_rejected(self) -> None:
        broken = copy.deepcopy(self.projection)
        broken["descriptive_evidence"]["adr"]["git_blob_sha1"] = (
            broken["descriptive_evidence"]["standard"]["git_blob_sha1"]
        )
        with self.assertRaisesRegex(
            MODULE.StatusCoherenceError, "Git blob drift: adr"
        ):
            self.validate(broken)

    def test_invented_repository_or_path_is_rejected(self) -> None:
        for field, value in (
            ("repository", "grandchallenge/UNRELATED"),
            ("path", "invented/not-at-commit.md"),
        ):
            with self.subTest(field=field):
                broken = copy.deepcopy(self.projection)
                broken["descriptive_evidence"]["adr"][field] = value
                with self.assertRaises(MODULE.jsonschema.ValidationError):
                    self.validate(broken)

    def test_unresolvable_declared_commit_is_rejected(self) -> None:
        broken = copy.deepcopy(self.projection)
        invented = "e" * 40
        for key in ("gcl_readme", "adr", "standard", "admission"):
            broken["descriptive_evidence"][key]["commit_sha"] = invented
        broken["selected_admission"]["admission_commit_sha"] = invented
        broken["selected_programme_adoption"]["admission_commit_sha"] = invented
        with self.assertRaisesRegex(
            MODULE.StatusCoherenceError, "cannot resolve exact Git evidence"
        ):
            self.validate(broken)

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
        broken = copy.deepcopy(self.projection)
        broken["descriptive_assertions"]["intellect_status_page_amendment_status"] = "proposed"
        with self.assertRaisesRegex(MODULE.StatusCoherenceError, "effective amendment"):
            MODULE.validate_projection(broken)

    def test_admitted_standard_with_candidate_front_matter_is_rejected(self) -> None:
        broken = copy.deepcopy(self.projection)
        broken["descriptive_assertions"]["standard_front_matter_status"] = "candidate"
        with self.assertRaisesRegex(MODULE.StatusCoherenceError, "historical metadata"):
            MODULE.validate_projection(broken)

    def test_active_adoption_with_not_started_gate_is_rejected(self) -> None:
        broken = copy.deepcopy(self.projection)
        broken["descriptive_assertions"]["admission_adoption_gate_status"] = "not_started"
        with self.assertRaisesRegex(MODULE.StatusCoherenceError, "not_started admission gate"):
            MODULE.validate_projection(broken)

    def test_historical_admission_cannot_be_selected_as_current(self) -> None:
        broken = copy.deepcopy(self.projection)
        broken["selected_admission"]["version"] = "0.1.0"
        with self.assertRaisesRegex(MODULE.StatusCoherenceError, "historical admission"):
            MODULE.validate_projection(broken)

    def test_successor_lineage_is_required(self) -> None:
        broken = copy.deepcopy(self.projection)
        broken.pop("lineage")
        with self.assertRaises(MODULE.jsonschema.ValidationError):
            MODULE.validate_projection(broken)

    def test_adoption_must_bind_selected_admission(self) -> None:
        broken = copy.deepcopy(self.projection)
        broken["selected_programme_adoption"]["admission_commit_sha"] = "d" * 40
        with self.assertRaisesRegex(MODULE.StatusCoherenceError, "does not bind"):
            MODULE.validate_projection(broken)

    def test_claim_authority_inflation_is_rejected(self) -> None:
        broken = copy.deepcopy(self.projection)
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
