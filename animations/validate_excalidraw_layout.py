#!/usr/bin/env python3
"""Smoke-test Excalidraw layout across scene types (vectors, raster, mixed)."""

from __future__ import annotations

import sys
from pathlib import Path

from excalidraw_parser import extract_svg_raster_placements, prepare_svg_for_manim
from excalidraw_scene import UL, _fit_svg_group, _load_svg_group, _svg_vector_root


def _viewbox(svg_path: Path) -> tuple[float, float, float, float]:
    import xml.etree.ElementTree as ET

    from excalidraw_parser import parse_view_box

    root = ET.parse(svg_path).getroot()
    return parse_view_box(root)


def _placement_in_viewbox(
    x: float,
    y: float,
    w: float,
    h: float,
    vb: tuple[float, float, float, float],
    *,
    slack: float = 80.0,
) -> bool:
    vb_x, vb_y, vb_w, vb_h = vb
    return (
        x + w >= vb_x - slack
        and y + h >= vb_y - slack
        and x <= vb_x + vb_w + slack
        and y <= vb_y + vb_h + slack
    )


def validate_svg(svg_path: Path) -> list[str]:
    errors: list[str] = []
    if not svg_path.exists():
        return [f"missing file: {svg_path}"]

    vb = _viewbox(svg_path)
    prepared = prepare_svg_for_manim(svg_path)
    for placement in extract_svg_raster_placements(prepared):
        if not _placement_in_viewbox(placement.x, placement.y, placement.width, placement.height, vb):
            errors.append(
                f"placement unit {placement.unit_index} outside viewBox: "
                f"({placement.x:.0f},{placement.y:.0f}) {placement.width:.0f}x{placement.height:.0f}"
            )

    group = _load_svg_group(svg_path)
    _fit_svg_group(group)
    vb_x, vb_y, vb_w, vb_h = group.excal_view_box or vb
    page_w = group.width
    page_h = group.height

    if page_w <= 0 or page_h <= 0:
        errors.append("group has zero size after layout")

    svg = _svg_vector_root(group)
    if svg is not None and svg.width > 0.001:
        if abs(svg.width - page_w) > page_w * 0.05:
            errors.append(f"vector width {svg.width:.2f} != page width {page_w:.2f}")

    for icon in group.get_family():
        placement = getattr(icon, "excal_placement", None)
        if placement is None:
            continue
        if abs(placement.rotation) > 1e-3:
            continue
        ul = icon.get_corner(UL)
        nx = (placement.x - vb_x) / vb_w if vb_w > 0 else 0.5
        ny = (placement.y - vb_y) / vb_h if vb_h > 0 else 0.5
        expected_ul = (
            -page_w / 2 + nx * page_w,
            page_h / 2 - ny * page_h,
            0.0,
        )
        if abs(ul[0] - expected_ul[0]) > page_w * 0.08 or abs(ul[1] - expected_ul[1]) > page_h * 0.08:
            errors.append(
                f"icon unit {placement.unit_index} drifted: "
                f"UL ({ul[0]:.2f},{ul[1]:.2f}) expected ~({expected_ul[0]:.2f},{expected_ul[1]:.2f})"
            )

    return errors


def main(argv: list[str]) -> int:
    paths = [Path(p) for p in argv[1:]] or [
        Path("/Users/enfec/manimations-studio/projects/162522d6/media/opening-pt-1_1_.svg"),
        Path("/Users/enfec/manimations-studio/projects/162522d6/media/frame_6_.svg"),
        Path("/Users/enfec/manimations-studio/projects/2705decc/media/scene_3.1.svg"),
        Path("/Users/enfec/manimations/assets/excalidraw/test-excalidraw-export.svg"),
    ]
    failed = 0
    for path in paths:
        errors = validate_svg(path)
        if errors:
            failed += 1
            print(f"FAIL {path}")
            for err in errors:
                print(f"  - {err}")
        else:
            print(f"OK   {path}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
