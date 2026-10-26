"""Offline, non-effectful verification of HIH 0.1.1 release-preparation inputs.

Never creates tags, GitHub releases, authorization or publication receipts.
Run: python ci/verify_hih_release.py --offline
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parents[1]
SUBJECT="a4f3544aafdfde0c8095fec7371cb776ea0b5703"
TAG="gcl-hih-00-v0.1.1"
DIR=Path("evidence/council/GCL-HIH-00")
PACKET=DIR/"RELEASE_PACKET-0.1.1.md"
NOTES=DIR/"RELEASE_NOTES-0.1.1.md"
MANIFEST=DIR/"RELEASE_MANIFEST-0.1.1.json"


def file_digest(data: bytes) -> tuple[str,str]:
    return (hashlib.sha1(b"blob "+str(len(data)).encode()+b"\0"+data).hexdigest(),
            hashlib.sha256(data).hexdigest())


def subject_blob(path: str) -> bytes:
    check=subprocess.run(["git", "show", f"{SUBJECT}:{path}"],
                         cwd=ROOT,stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,check=False)
    if check.returncode:
        raise AssertionError(f"exact protected subject missing: {path}")
    return check.stdout


def validate() -> dict:
    data=json.loads((ROOT/MANIFEST).read_text(encoding="utf-8"))
    packet=(ROOT/PACKET).read_text(encoding="utf-8")
    notes=(ROOT/NOTES).read_bytes()
    assert data["record_type"]=="GCL_HIH_RELEASE_CANDIDATE_MANIFEST/1"
    assert data["version"]=="0.1.1" and data["release_tag"]==TAG
    assert data["tag_target_protected_commit"]==SUBJECT
    assert data["publication_state"]=="PREPARED_NOT_AUTHORIZED_NOT_RELEASED"
    assert data["publication_authorization_required"] is True
    assert data["release_notes"]["path"]==str(NOTES)
    note_git,note_sha=file_digest(notes)
    assert (data["release_notes"]["git_blob_sha1"],
            data["release_notes"]["sha256"]) == (note_git,note_sha)
    assert len(data["source_artifacts"])>=7
    for path, expected in data["source_artifacts"].items():
        raw=subject_blob(path)
        blob,sha=file_digest(raw)
        assert blob==expected["git_blob_sha1"],path
        assert sha==expected["sha256"],path
        assert len(raw)==expected["size_bytes"],path
        local=(ROOT/path).read_bytes()
        if local != raw:
            # The admission-tree status was HOLD before publication.
            # A later protected receipt may promote only release status;
            # the signed admission and source artifact identities cannot drift.
            assert path=="status/GCL-HIH-00-current.json", "source drift: "+path
            receipt_path=ROOT/DIR/"RELEASE_RECEIPT-0.1.1.json"
            assert receipt_path.is_file(), "unreceipted status promotion"
            original=json.loads(raw)
            current=json.loads(local)
            receipt=json.loads(receipt_path.read_text())
            assert receipt["status"]=="PUBLISHED_AND_VERIFIED"
            assert receipt["release"]["immutable"] is True
            assert receipt["tag"]["verified_target_commit_sha1"]==SUBJECT
            assert receipt["release"]["tag"]==TAG
            assert receipt["notes"]["sha256"]==data["release_notes"]["sha256"]
            assert current["public_release"]["status"]=="PUBLISHED"
            assert current["public_release"]["formal_release_authorized"] is True
            assert current["public_release"]["publication_receipt"]==str(DIR/"RELEASE_RECEIPT-0.1.1.json")
            assert current["public_release"]["tag_target_protected_commit"]==SUBJECT
            assert current["claim_boundaries"]["public_release"] is True
            del original["public_release"]
            del current["public_release"]
            original["claim_boundaries"].pop("public_release")
            current["claim_boundaries"].pop("public_release")
            assert original==current, "non-release admission/status drift"
    status=json.loads(subject_blob("status/GCL-HIH-00-current.json"))
    admission=json.loads(subject_blob("admissions/GCL-HIH-00-0.1.1.json"))
    assert status["version"]=="0.1.1"
    assert status["public_release"]["status"]=="HOLD"
    assert status["public_release"]["formal_release_authorized"] is False
    assert admission["status"]=="admitted"
    assert admission["public_release"]["human_steward_exact_release_authorization_recorded"] is False
    for key in ("standard","disclosure_template"):
        name=admission["source"]["standard_path" if key=="standard" else "disclosure_template_path"]
        assert admission["source"]["standard_git_blob_sha1" if key=="standard" else "disclosure_template_git_blob_sha1"]==data["source_artifacts"][name]["git_blob_sha1"]
    assert "NOT AUTHORIZED" in packet and "NOT RELEASED" in packet
    assert "NOT CREATED" in packet and TAG in packet and SUBJECT in packet
    assert f"gcl-hih-00-v0.1.1" in notes.decode()
    assert data["release_notes"]["sha256"] in (ROOT/MANIFEST).read_text()
    # A historic 0.1.0 packet is deliberately not modified for this successor.
    original=(ROOT/DIR/"RELEASE_PACKET.md").read_text()
    assert "GCL-HIH-00 v0.1.0" in original
    assert "gcl-hih-00-v0.1.0" in original
    return {"record_type":"GCL_HIH_RELEASE_PREFLIGHT/1",
            "status":"PASS_PREPARATION_ONLY","version":"0.1.1",
            "target":SUBJECT,"tag":TAG,"source_files_verified":len(data["source_artifacts"]),
            "release_notes_sha256":note_sha,
            "external_release_authorized":False,
            "tag_created":False,
            "github_release_created":False}


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument("--offline",action="store_true",required=True)
    ap.parse_args()
    print(json.dumps(validate(),sort_keys=True,indent=2))


if __name__=="__main__":
    main()
