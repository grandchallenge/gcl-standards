"""Prevent status corrections from altering the admitted HIH acknowledgments."""
from pathlib import Path
from hashlib import sha1

ROOT = Path(__file__).resolve().parents[1]

def blob(path: str) -> str:
    raw = (ROOT / path).read_bytes()
    return sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()

def test_admitted_predecessor_exact_blobs():
    assert blob("standards/history/GCL-HIH-00-0.1.0.md") == "7f381080b7dd98a7f922274a9693bbc7ead0f40c"
    assert blob("templates/history/AI_PARTICIPATION_DISCLOSURE-0.1.0.md") == "4b5577a396214e3090e969808bf601ab035413de"

def test_full_short_and_accountable_author_text_unchanged():
    before = (ROOT/"standards/history/GCL-HIH-00-0.1.0.md").read_text()
    after = (ROOT/"standards/GCL-HIH-00.md").read_text()
    first="### Acknowledgment of Human Intellectual Heritage and AI Contributions"
    end="## 4."
    old=before[before.index(first):before.index(end)]
    new=after[after.index(first):after.index(end)]
    assert old.replace("## 3. Short acknowledgment (candidate publication text)", "## 3. Short acknowledgment") == new

def test_disclosure_fields_unchanged():
    old=(ROOT/"templates/history/AI_PARTICIPATION_DISCLOSURE-0.1.0.md").read_text()
    new=(ROOT/"templates/AI_PARTICIPATION_DISCLOSURE.md").read_text()
    a="## Disclosure of AI Participation"
    b="## Scope note"
    assert old.split(a,1)[1].split(b,1)[0] == new.split(a,1)[1].split(b,1)[0]

def test_no_stale_current_candidate_labels():
    standard=(ROOT/"standards/GCL-HIH-00.md").read_text()
    template=(ROOT/"templates/AI_PARTICIPATION_DISCLOSURE.md").read_text()
    assert "**Version:** 0.1.1" in standard and "**Version:** 0.1.1" in template
    assert "CANDIDATE FOR COUNCIL REVIEW" not in standard
    assert "proposal only" not in standard.lower()
    assert "DRAFT; NOT ADMITTED" not in template
    assert "status/GCL-HIH-00-current.json" in standard and "status/GCL-HIH-00-current.json" in template
    assert "public release" in standard.lower() and "programme" in template.lower()

def test_successor_admission_is_exact_and_release_stays_held():
    import json
    admission=json.loads((ROOT/"admissions/GCL-HIH-00-0.1.1.json").read_text())
    status=json.loads((ROOT/"status/GCL-HIH-00-current.json").read_text())
    assert admission["version"]==status["version"]=="0.1.1"
    assert admission["source"]["standard_git_blob_sha1"]==blob("standards/GCL-HIH-00.md")
    assert admission["source"]["disclosure_template_git_blob_sha1"]==blob("templates/AI_PARTICIPATION_DISCLOSURE.md")
    assert admission["predecessor"]["historical_standard_git_blob_sha1"]==blob("standards/history/GCL-HIH-00-0.1.0.md")
    assert admission["predecessor"]["historical_disclosure_git_blob_sha1"]==blob("templates/history/AI_PARTICIPATION_DISCLOSURE-0.1.0.md")
    assert admission["effective_condition"]=="protected_merge_of_this_exact_admission_record"
    assert status["public_release"]["status"]=="PUBLISHED"
    assert admission["public_release"]["human_steward_exact_release_authorization_recorded"] is False  # historical admission snapshot
    assert status["programme_adoption"]["status"]=="not_yet_adopted"
    assert "gcl-hih-00-v0.1.1" not in (ROOT/"evidence/council/GCL-HIH-00/RELEASE_PACKET.md").read_text()
