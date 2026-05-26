#!/usr/bin/env python3
"""Resolve visuals for a project JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "animations"))

from visual_library import prefetch_beat_visuals  # noqa: E402
from visual_resolver import resolve_project  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Resolve beat visuals from project JSON")
    parser.add_argument("project_json", type=Path)
    parser.add_argument("-o", "--output", type=Path, help="Write resolved JSON (default: in-place)")
    args = parser.parse_args()

    project = json.loads(args.project_json.read_text())
    resolved = resolve_project(project)
    for beat in resolved.get("beats", []):
        prefetch_beat_visuals(beat)

    out = args.output or args.project_json
    out.write_text(json.dumps(resolved, indent=2))
    print(f"Resolved {len(resolved.get('beats', []))} beat(s) → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
