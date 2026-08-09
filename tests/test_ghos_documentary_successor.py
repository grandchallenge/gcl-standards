from __future__ import annotations

import importlib.util
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
    def test_exact_documentary_successor_validates(self) -> None:
        MODULE.validate()

    def test_normative_body_change_is_rejected(self) -> None:
        historical = MODULE.HISTORICAL_STANDARD.read_text(encoding="utf-8")
        current = MODULE.CURRENT_STANDARD.read_text(encoding="utf-8")
        adr = MODULE.ADR.read_text(encoding="utf-8")
        readme = MODULE.README.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "standards" / "history").mkdir(parents=True)
            (root / "decisions").mkdir()
            (root / "README.md").write_text(readme, encoding="utf-8", newline="\n")
            (root / "standards" / "history" / "GCL-GHOS-00-0.1.0.md").write_text(
                historical, encoding="utf-8", newline="\n"
            )
            (root / "standards" / "GCL-GHOS-00.md").write_text(
                current.replace(
                    "It is a subordinate operating standard, not a constitution.",
                    "It is the constitution.",
                ),
                encoding="utf-8",
                newline="\n",
            )
            (root / "decisions" / "ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md").write_text(
                adr, encoding="utf-8", newline="\n"
            )
            subprocess.run(
                ["git", "init", "--quiet"], cwd=root, check=True, capture_output=True
            )
            with self.assertRaisesRegex(
                MODULE.DocumentarySuccessorError,
                "normative body differs",
            ):
                MODULE.validate(root=root)

    def test_stale_prospective_adr_status_is_rejected(self) -> None:
        historical = MODULE.HISTORICAL_STANDARD.read_text(encoding="utf-8")
        current = MODULE.CURRENT_STANDARD.read_text(encoding="utf-8")
        adr = MODULE.ADR.read_text(encoding="utf-8")
        readme = MODULE.README.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "standards" / "history").mkdir(parents=True)
            (root / "decisions").mkdir()
            (root / "README.md").write_text(readme, encoding="utf-8", newline="\n")
            (root / "standards" / "history" / "GCL-GHOS-00-0.1.0.md").write_text(
                historical, encoding="utf-8", newline="\n"
            )
            (root / "standards" / "GCL-GHOS-00.md").write_text(
                current, encoding="utf-8", newline="\n"
            )
            (root / "decisions" / "ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md").write_text(
                adr.replace(
                    "ADR-0001 was accepted through the protected `0.1.0` admission lineage",
                    "This ADR becomes accepted only after:",
                ),
                encoding="utf-8",
                newline="\n",
            )
            subprocess.run(
                ["git", "init", "--quiet"], cwd=root, check=True, capture_output=True
            )
            with self.assertRaisesRegex(
                MODULE.DocumentarySuccessorError,
                "stale prospective status",
            ):
                MODULE.validate(root=root)

    def test_stale_prospective_readme_status_is_rejected(self) -> None:
        historical = MODULE.HISTORICAL_STANDARD.read_text(encoding="utf-8")
        current = MODULE.CURRENT_STANDARD.read_text(encoding="utf-8")
        adr = MODULE.ADR.read_text(encoding="utf-8")
        readme = MODULE.README.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "standards" / "history").mkdir(parents=True)
            (root / "decisions").mkdir()
            (root / "standards" / "history" / "GCL-GHOS-00-0.1.0.md").write_text(
                historical, encoding="utf-8", newline="\n"
            )
            (root / "standards" / "GCL-GHOS-00.md").write_text(
                current, encoding="utf-8", newline="\n"
            )
            (root / "decisions" / "ADR-0001_GITHUB_CONSTITUTIONAL_OPERATING_SYSTEM.md").write_text(
                adr, encoding="utf-8", newline="\n"
            )
            (root / "README.md").write_text(
                readme.replace(
                    "selected status is\nresolved from its protected admission record",
                    "prepared for exact-packet review; it becomes selected only through admission",
                ),
                encoding="utf-8",
                newline="\n",
            )
            subprocess.run(
                ["git", "init", "--quiet"], cwd=root, check=True, capture_output=True
            )
            with self.assertRaisesRegex(
                MODULE.DocumentarySuccessorError,
                "README current-status projection is not time-stable",
            ):
                MODULE.validate(root=root)


if __name__ == "__main__":
    unittest.main()
