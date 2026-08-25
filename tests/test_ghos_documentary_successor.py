from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "ghos_documentary_successor", ROOT / "ci" / "ghos_documentary_successor.py"
)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class GhosDocumentarySuccessorTests(unittest.TestCase):
    def _fixture(
        self,
        *,
        historical_011: str | None = None,
        current: str | None = None,
        readme: str | None = None,
        admission: dict[str, object] | None = None,
    ):
        historical_010 = MODULE.HISTORICAL_STANDARD_010.read_text(encoding="utf-8")
        base_historical_011 = MODULE.HISTORICAL_STANDARD_011.read_text(encoding="utf-8")
        base_current = MODULE.CURRENT_STANDARD.read_text(encoding="utf-8")
        adr = MODULE.ADR.read_text(encoding="utf-8")
        base_readme = MODULE.README.read_text(encoding="utf-8")
        base_admission = json.loads(MODULE.ADMISSION_020.read_text(encoding="utf-8"))
        schema = MODULE.ADMISSION_SCHEMA.read_text(encoding="utf-8")

        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        (root / "standards" / "history").mkdir(parents=True)
        (root / "decisions").mkdir()
        (root / "admissions").mkdir()
        (root / "schemas").mkdir()
        (root / "standards" / "history" / "GCL-GHOS-00-0.1.0.md").write_text(
            historical_010, encoding="utf-8", newline="\n"
        )
        (root / "standards" / "history" / "GCL-GHOS-00-0.1.1.md").write_text(
            base_historical_011 if historical_011 is None else historical_011,
            encoding="utf-8",
            newline="\n",
        )
        (root / "standards" / "GCL-GHOS-00.md").write_text(
            base_current if current is None else current,
            encoding="utf-8",
            newline="\n",
        )
        (root / "decisions" / "ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md").write_text(
            adr, encoding="utf-8", newline="\n"
        )
        (root / "README.md").write_text(
            base_readme if readme is None else readme,
            encoding="utf-8",
            newline="\n",
        )
        (root / "admissions" / "GCL-GHOS-00-0.2.0.json").write_text(
            json.dumps(base_admission if admission is None else admission, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (root / "schemas" / "standard_normative_successor_admission.schema.json").write_text(
            schema, encoding="utf-8", newline="\n"
        )
        subprocess.run(
            ["git", "init", "--quiet"], cwd=root, check=True, capture_output=True
        )
        return temporary, root

    def test_exact_reviewed_source_admission_validates(self) -> None:
        MODULE.validate()

    def test_missing_execution_continuity_boundary_is_rejected(self) -> None:
        current = MODULE.CURRENT_STANDARD.read_text(encoding="utf-8").replace(
            "tooling failure does not by\nitself constitute an authority boundary.",
            "tooling failure may terminate execution.",
        )
        temporary, root = self._fixture(current=current)
        with temporary:
            with self.assertRaisesRegex(
                MODULE.DocumentarySuccessorError,
                "bounded-execution-continuity",
            ):
                MODULE.validate(root=root)

    def test_historical_011_identity_drift_is_rejected(self) -> None:
        historical_011 = MODULE.HISTORICAL_STANDARD_011.read_text(
            encoding="utf-8"
        ) + "\n"
        temporary, root = self._fixture(historical_011=historical_011)
        with temporary:
            with self.assertRaisesRegex(
                MODULE.DocumentarySuccessorError,
                "historical 0.1.1 Git blob identity drift",
            ):
                MODULE.validate(root=root)

    def test_reviewed_020_source_blob_drift_is_rejected(self) -> None:
        current = MODULE.CURRENT_STANDARD.read_text(encoding="utf-8") + "\n"
        temporary, root = self._fixture(current=current)
        with temporary:
            with self.assertRaisesRegex(
                MODULE.DocumentarySuccessorError,
                "reviewed 0.2.0 standard source blob drift",
            ):
                MODULE.validate(root=root)

    def test_referee_and_adversary_sessions_must_be_distinct(self) -> None:
        admission = json.loads(MODULE.ADMISSION_020.read_text(encoding="utf-8"))
        admission["review_staffing"]["referee"]["session_id"] = admission[
            "review_staffing"
        ]["adversary"]["session_id"]
        temporary, root = self._fixture(admission=admission)
        with temporary:
            with self.assertRaisesRegex(
                MODULE.DocumentarySuccessorError,
                "sessions must be distinct",
            ):
                MODULE.validate(root=root)

    def test_programme_adoption_cannot_be_prematurely_promoted(self) -> None:
        readme = MODULE.README.read_text(encoding="utf-8") + (
            "\nMATH-PROGRAMME actively adopts `0.2.0`.\n"
        )
        temporary, root = self._fixture(readme=readme)
        with temporary:
            with self.assertRaisesRegex(
                MODULE.DocumentarySuccessorError,
                "prematurely promotes 0.2.0",
            ):
                MODULE.validate(root=root)


if __name__ == "__main__":
    unittest.main()
