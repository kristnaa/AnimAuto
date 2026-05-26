#!/usr/bin/env python3
"""Prefetch icons — global cache or per-beat Episode folders."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "animations"))

from icon_library import (  # noqa: E402
    list_aliases,
    prefetch,
    prefetch_all,
    read_beat_manifest,
    save_beat_icon,
    sync_beat_icons,
)


def main() -> int:
    parser = argparse.ArgumentParser(description="Prefetch Iconify icons.")
    parser.add_argument("icons", nargs="*", help="Icon refs or aliases")
    parser.add_argument("--all", action="store_true", help="Prefetch every global alias")
    parser.add_argument("--list", action="store_true", help="List global aliases")
    parser.add_argument("--force", action="store_true", help="Re-download even if cached")
    parser.add_argument("--episode", type=int, help="Episode number (e.g. 1)")
    parser.add_argument("--beat", type=int, help="Beat number (e.g. 1)")
    args = parser.parse_args()

    if args.list:
        for alias, ref in sorted(list_aliases().items()):
            print(f"{alias:20} → {ref}")
        return 0

    if args.episode is not None and args.beat is not None:
        paths = sync_beat_icons(args.episode, args.beat, force=args.force)
        dest = ROOT / f"Episode{args.episode}" / "beats" / f"beat{args.beat}" / "icons"
        print(f"Synced {len(paths)} beat icon(s) → {dest.relative_to(ROOT)}/")
        for p in paths:
            print(f"  {p.name}")
        return 0

    if args.all:
        paths = prefetch_all(force=args.force)
    elif args.icons:
        paths = prefetch(*args.icons, force=args.force)
    else:
        parser.print_help()
        return 1

    print(f"Cached {len(paths)} icon(s) under assets/icons/cache/")
    for p in paths:
        print(f"  {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
