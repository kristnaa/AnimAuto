#!/usr/bin/env python3
"""Generate ASCII GRID LAYOUT blocks for beat scripts.

Examples:
  python generate_grid.py --list-layouts
  python generate_grid.py --example beat1
  python generate_grid.py --layout card_right_icon_left \\
    --label "Welcome to Python for AI" \\
    --left icon_python,icon_scream \\
    --card-size "5.6 × 5.0" \\
    --card-lines "Line 1|Line 2|punchline"
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

from grid_layouts import LAYOUTS, beat1_example, build_grid, render_ascii  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate beat GRID LAYOUT ASCII diagrams.")
    parser.add_argument("--list-layouts", action="store_true", help="Show layout preset IDs")
    parser.add_argument("--example", choices=["beat1"], help="Print a filled reference grid")
    parser.add_argument("--layout", choices=list(LAYOUTS.keys()), help="Layout preset ID")
    parser.add_argument("--label", default="Your Label Here", help="Yellow heading text")
    parser.add_argument("--left", default="", help="Comma-separated left icon IDs")
    parser.add_argument("--right", default="", help="Comma-separated right icon IDs")
    parser.add_argument("--card-side", choices=["left", "right"], default="right")
    parser.add_argument("--card-size", default="5.6 × 5.0", help='e.g. "5.6 × 5.0"')
    parser.add_argument("--card-lines", default="", help="Pipe-separated card text lines")
    parser.add_argument("--bg-lines", default="", help="Pipe-separated white-on-orange lines")
    parser.add_argument("--left-morph", default="", help="Left morph/animation ID")
    parser.add_argument("--right-morph", default="", help="Right morph/animation ID")
    parser.add_argument("--note", action="append", default=[], dest="notes", help="Extra grid note")
    args = parser.parse_args()

    if args.list_layouts:
        print("Available layout presets:\n")
        for lid, desc in LAYOUTS.items():
            print(f"  {lid:26}  {desc}")
        return 0

    if args.example == "beat1":
        print(render_ascii(beat1_example()))
        return 0

    if not args.layout:
        parser.print_help()
        print("\nTry: python generate_grid.py --example beat1")
        return 1

    left_icons = [s.strip() for s in args.left.split(",") if s.strip()]
    right_icons = [s.strip() for s in args.right.split(",") if s.strip()]
    card_lines = [s.strip() for s in args.card_lines.split("|") if s.strip()]
    bg_lines = [s.strip() for s in args.bg_lines.split("|") if s.strip()]

    grid = build_grid(
        args.layout,
        args.label,
        left_icon=left_icons[0] if len(left_icons) == 1 else "",
        right_icon=right_icons[0] if len(right_icons) == 1 else "",
        left_icons=left_icons if len(left_icons) != 1 else None,
        right_icons=right_icons if len(right_icons) != 1 else None,
        card_side=args.card_side,
        card_size=args.card_size,
        card_lines=card_lines or None,
        bg_lines=bg_lines or None,
        left_morph=args.left_morph,
        right_morph=args.right_morph,
        notes=args.notes,
    )
    print(render_ascii(grid))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
