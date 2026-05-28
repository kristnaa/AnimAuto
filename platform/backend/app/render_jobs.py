"""Background Manim render jobs with on-disk status for polling."""

from __future__ import annotations

import json
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

_locks: dict[str, threading.Lock] = {}
_registry_lock = threading.Lock()


def _status_path(renders_dir: Path) -> Path:
    return renders_dir / ".render_status.json"


def _project_lock(project_id: str) -> threading.Lock:
    with _registry_lock:
        lock = _locks.get(project_id)
        if lock is None:
            lock = threading.Lock()
            _locks[project_id] = lock
        return lock


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_status(renders_dir: Path) -> dict:
    path = _status_path(renders_dir)
    if not path.exists():
        return {"status": "idle"}
    try:
        data = json.loads(path.read_text())
        if isinstance(data, dict):
            return data
    except (OSError, json.JSONDecodeError):
        pass
    return {"status": "idle"}


def write_status(renders_dir: Path, payload: dict) -> None:
    renders_dir.mkdir(parents=True, exist_ok=True)
    _status_path(renders_dir).write_text(json.dumps(payload, indent=2))


def start_preview_render(
    project_id: str,
    renders_dir: Path,
    render_fn: Callable[[], None],
) -> dict:
    """Run render_fn in a background thread; return current job status."""
    lock = _project_lock(project_id)
    if not lock.acquire(blocking=False):
        current = read_status(renders_dir)
        if current.get("status") == "rendering":
            return current
        lock.acquire()

    write_status(
        renders_dir,
        {"status": "rendering", "started_at": _now_iso(), "error": None},
    )

    def _run() -> None:
        try:
            render_fn()
            write_status(
                renders_dir,
                {"status": "done", "finished_at": _now_iso(), "error": None},
            )
        except Exception as exc:
            write_status(
                renders_dir,
                {
                    "status": "error",
                    "finished_at": _now_iso(),
                    "error": str(exc),
                },
            )
        finally:
            lock.release()

    threading.Thread(target=_run, daemon=True, name=f"render-{project_id}",).start()
    return read_status(renders_dir)
