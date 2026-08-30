from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import jsonschema

import ghos_control_plane as control


ROOT = Path(__file__).resolve().parents[1]
CONTROL_GLOB = ".ghos-control/*/ledger.json"


class ControlStoreError(ValueError):
    pass


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ControlStoreError(f"control record must be an object: {path}")
    return value


def validate_control_directory(directory: Path, *, repository_root: Path = ROOT) -> dict[str, Any]:
    schema = _load(repository_root / "schemas" / "ghos_control_plane.schema.json")
    catalog = _load(
        repository_root
        / "implementation"
        / "GCL-GHOS-CONTROL-PLANE-REMEDIATION-001"
        / "control-plane"
        / "transition-catalog.json"
    )
    admission = _load(directory / "admission.json")
    ledger = _load(directory / "ledger.json")
    store = _load(directory / "store.json")

    for record in (admission, ledger):
        jsonschema.validate(record, schema, cls=jsonschema.Draft202012Validator)
    if ledger["storage_status"] != "PROTECTED_CONTROL_REF":
        raise ControlStoreError("operational ledger is not on a protected control ref")
    if ledger["catalog_digest"] != control.catalog_digest(catalog):
        raise ControlStoreError("control ledger catalog digest drift")
    control.validate_event_sequence(ledger)
    first = ledger["events"][0]
    if first["event_type"] != "WORK_PACKAGE_ADMITTED":
        raise ControlStoreError("control ledger does not begin with admission")
    if first["payload"]["admission_digest"] != control.digest(admission):
        raise ControlStoreError("control ledger admission digest drift")
    if store.get("work_package") != ledger["work_package"]:
        raise ControlStoreError("control store work-package substitution")
    if not store.get("deletion_prohibited") or not store.get("non_fast_forward_prohibited"):
        raise ControlStoreError("control store lacks append-only ref protection")
    if store.get("claim_boundaries") != control.CLAIM_BOUNDARIES:
        raise ControlStoreError("control store widens authority")

    projection = _load(repository_root / "status" / "GCL-GHOS-00-current.json")
    authority = control.resolve_effective_authority(root=repository_root, projection=projection)
    state = control.reduce_ledger(ledger, catalog, authority, admission)
    jsonschema.validate(state, schema, cls=jsonschema.Draft202012Validator)
    return state


def validate(*, root: Path = ROOT) -> None:
    for ledger_path in sorted(root.glob(CONTROL_GLOB)):
        validate_control_directory(ledger_path.parent, repository_root=root)


if __name__ == "__main__":
    validate()
    print("protected GH-OS control stores validated")
