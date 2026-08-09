from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("git_content", ROOT / "ci" / "git_content.py")
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class GitContentTests(unittest.TestCase):
    def test_lf_and_crlf_have_the_same_canonical_git_identity(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "--quiet"], cwd=root, check=True)
            subprocess.run(
                ["git", "config", "core.autocrlf", "true"], cwd=root, check=True
            )
            (root / ".gitattributes").write_text("*.txt text\n", encoding="utf-8")
            (root / "lf.txt").write_bytes(b"alpha\nbeta\n")
            (root / "crlf.txt").write_bytes(b"alpha\r\nbeta\r\n")
            self.assertEqual(
                MODULE.git_blob_sha1(root / "lf.txt", root=root),
                MODULE.git_blob_sha1(root / "crlf.txt", root=root),
            )

    def test_historical_standard_matches_admitted_git_blob(self) -> None:
        historical = ROOT / "standards" / "history" / "GCL-GHOS-00-0.1.0.md"
        self.assertEqual(
            MODULE.git_blob_sha1(historical, root=ROOT),
            "b93c57f1fb27bf2a017a4b90719290342424f6d5",
        )


if __name__ == "__main__":
    unittest.main()
