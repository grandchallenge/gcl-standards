from __future__ import annotations

import subprocess
from pathlib import Path


class GitContentError(ValueError):
    pass


def _relative_path(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise GitContentError(f"path is outside repository root: {path}") from exc


def _git(root: Path, *arguments: str) -> bytes:
    try:
        completed = subprocess.run(
            ["git", "-C", str(root), *arguments],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise GitContentError(f"Git content lookup failed: {' '.join(arguments)}") from exc
    return completed.stdout


def git_blob_sha1(path: Path, *, root: Path) -> str:
    """Return the blob identity after Git's canonical clean filters."""

    relative = _relative_path(path, root)
    value = _git(root, "hash-object", f"--path={relative}", "--", relative)
    return value.decode("ascii").strip()


def canonical_git_bytes(path: Path, *, root: Path) -> bytes:
    """Return canonical blob bytes for a tracked or already-known Git blob."""

    identity = git_blob_sha1(path, root=root)
    return _git(root, "cat-file", "blob", identity)


def git_blob_sha1_at_commit(
    *, root: Path, commit: str, relative_path: str
) -> str:
    """Resolve an artifact identity from a named Git revision, not worktree bytes."""

    value = _git(root, "rev-parse", f"{commit}:{relative_path}")
    return value.decode("ascii").strip()


def git_text_at_commit(*, root: Path, commit: str, relative_path: str) -> str:
    return _git(root, "show", f"{commit}:{relative_path}").decode("utf-8")
