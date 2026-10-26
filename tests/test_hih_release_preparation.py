"""Adversarial HIH release preparation tests; no publication or tag mutations."""
from pathlib import Path
from unittest.mock import patch
import importlib.util
import json
import unittest

ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location(
    "hih_release_preflight", ROOT/"ci/verify_hih_release.py")
MOD=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


class HIHReleasePreparationTests(unittest.TestCase):
    def test_exact_protected_source_and_notes(self):
        receipt=MOD.validate()
        self.assertEqual(receipt["status"],"PASS_PREPARATION_ONLY")
        self.assertEqual(receipt["source_files_verified"],7)
        self.assertFalse(receipt["external_release_authorized"])
        self.assertFalse(receipt["tag_created"])
        self.assertFalse(receipt["github_release_created"])

    def test_source_content_substitution_rejected(self):
        genuine=MOD.subject_blob
        def wrong(path):
            if path=="standards/GCL-HIH-00.md":
                return b"altered published text"
            return genuine(path)
        with patch.object(MOD,"subject_blob",side_effect=wrong):
            with self.assertRaises(AssertionError):
                MOD.validate()

    def test_release_notes_drift_rejected(self):
        original=MOD.NOTES
        with patch.object(MOD,"NOTES",ROOT/"README.md"):
            with self.assertRaises(AssertionError):
                MOD.validate()
        self.assertEqual(MOD.NOTES,original)

    def test_version_and_authority_not_promoted(self):
        status=json.loads((ROOT/"status/GCL-HIH-00-current.json").read_text())
        manifest=json.loads((ROOT/MOD.MANIFEST).read_text())
        packet=(ROOT/MOD.PACKET).read_text()
        self.assertEqual(status["public_release"]["status"],"PUBLISHED")
        self.assertTrue(status["public_release"]["formal_release_authorized"])
        # The signed tag tree is an immutable pre-publication snapshot.
        historic=json.loads(MOD.subject_blob("status/GCL-HIH-00-current.json"))
        self.assertEqual(historic["public_release"]["status"],"HOLD")
        self.assertFalse(historic["public_release"]["formal_release_authorized"])
        self.assertEqual(manifest["publication_state"],"PREPARED_NOT_AUTHORIZED_NOT_RELEASED")
        self.assertIn("NOT AUTHORIZED",packet)
        self.assertIn("NOT RELEASED",packet)
        self.assertIn("AUTHORIZE",packet)
        self.assertIn("Human Steward",packet)
        self.assertIn("gcl-hih-00-v0.1.1",packet)

    def test_original_010_packet_unchanged(self):
        original=(ROOT/"evidence/council/GCL-HIH-00/RELEASE_PACKET.md").read_text()
        self.assertIn("GCL-HIH-00 v0.1.0",original)
        self.assertIn("gcl-hih-00-v0.1.0",original)
        self.assertNotIn("gcl-hih-00-v0.1.1",original)


if __name__=="__main__":
    unittest.main()
