"""HIH publication receipt coherence; immutable release is checked live separately."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/"evidence/council/GCL-HIH-00"


class HIHPublicReleaseReceiptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt=json.loads((BASE/"RELEASE_RECEIPT-0.1.1.json").read_text())
        cls.status=json.loads((ROOT/"status/GCL-HIH-00-current.json").read_text())
        cls.manifest=json.loads((BASE/"RELEASE_MANIFEST-0.1.1.json").read_text())

    def test_release_identity_and_exact_authorized_tag(self):
        r=self.receipt
        self.assertEqual(r["status"],"PUBLISHED_AND_VERIFIED")
        self.assertEqual(r["steward_authorization"]["decision"],"AUTHORIZE")
        self.assertEqual(r["release"]["release_id"],418941201)
        self.assertEqual(r["tag"]["git_ref"],"refs/tags/gcl-hih-00-v0.1.1")
        self.assertEqual(r["tag"]["verified_target_commit_sha1"],
                         "a4f3544aafdfde0c8095fec7371cb776ea0b5703")
        self.assertTrue(r["release"]["immutable"])
        self.assertFalse(r["release"]["draft"])
        self.assertFalse(r["release"]["prerelease"])
        self.assertEqual(r["release"]["author"],"fyremael")
        self.assertTrue(r["steward_authorization"]["relay_was_mechanical_transcription_not_independent_human_github_message"])
        self.assertFalse(r["steward_authorization"]["chat_identity_independently_verified_by_github"])

    def test_release_notes_and_preparation_evidence(self):
        r=self.receipt
        raw=(BASE/"RELEASE_NOTES-0.1.1.md").read_bytes()
        digest=hashlib.sha256(raw).hexdigest()
        self.assertEqual(r["notes"]["sha256"],digest)
        self.assertEqual(self.manifest["release_notes"]["sha256"],digest)
        self.assertEqual(r["packet"]["manifest_git_blob_sha1"],"ace63dc18ab8eb0b70b18c331f62f82bc718be21")
        self.assertTrue(r["notes"]["exact_byte_match_to_protected_notes"])

    def test_authoritative_current_status_and_nonadoption(self):
        p=self.status["public_release"]
        self.assertEqual(p["status"],"PUBLISHED")
        self.assertTrue(p["formal_release_authorized"])
        self.assertEqual(p["release_url"],self.receipt["release"]["url"])
        self.assertEqual(p["tag_target_protected_commit"],
                         self.receipt["tag"]["verified_target_commit_sha1"])
        self.assertEqual(p["publication_receipt"],"evidence/council/GCL-HIH-00/RELEASE_RECEIPT-0.1.1.json")
        self.assertTrue(self.status["claim_boundaries"]["public_release"])
        self.assertFalse(self.status["claim_boundaries"]["mandatory_org_policy"])
        self.assertEqual(self.status["programme_adoption"]["status"],"not_yet_adopted")

    def test_admission_and_old_packet_remain_historical(self):
        admitted=json.loads((ROOT/"admissions/GCL-HIH-00-0.1.1.json").read_text())
        self.assertEqual(admitted["public_release"]["status"],"HOLD_NOT_AUTHORIZED")
        old_packet=(BASE/"RELEASE_PACKET.md").read_text()
        self.assertIn("gcl-hih-00-v0.1.0",old_packet)
        self.assertNotIn("gcl-hih-00-v0.1.1",old_packet)
        self.assertEqual(self.receipt["tag"]["release_target_commitish_metadata"],"main")
        self.assertTrue(self.receipt["tag"]["target_commitish_is_not_tag_reference"])


if __name__=="__main__":
    unittest.main()
