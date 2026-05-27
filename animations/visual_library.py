"""Unified visual loader — procedural, brand, and iconify assets."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import TYPE_CHECKING

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "animations"))

from icon_library import fetch_iconify_svg  # noqa: E402

if TYPE_CHECKING:
    from manim import Mobject


def _manim():
    from manim import Mobject, SVGMobject, WHITE

    return Mobject, SVGMobject, WHITE


def _resolve_color(color: str | None):
    if color is None:
        return None
    from manim import BLUE, GREEN, ORANGE, PURPLE, RED, WHITE, YELLOW

    named = {
        "WHITE": WHITE,
        "BLUE": BLUE,
        "RED": RED,
        "YELLOW": YELLOW,
        "GREEN": GREEN,
        "ORANGE": ORANGE,
        "PURPLE": PURPLE,
    }
    if isinstance(color, str) and color.upper() in named:
        return named[color.upper()]
    return color


def _svg_mob(path: Path, scale: float, color: str | None) -> "Mobject":
    _, SVGMobject, _ = _manim()
    mob = SVGMobject(str(path))
    resolved = _resolve_color(color)
    if resolved is not None:
        mob.set_color(resolved)
    mob.scale(scale)
    return mob


def load_procedural(scene, ref: str, scale: float = 1.0) -> "Mobject":
    if ref == "shape_question":
        return scene.shape_question(radius=0.8 * scale)
    raise KeyError(f"Unknown procedural visual: {ref}")


def load_brand(ref: str, scale: float = 1.0) -> "Mobject":
    path = ROOT / ref if not ref.startswith("/") else Path(ref)
    if not path.exists():
        raise FileNotFoundError(f"Brand asset not found: {path}")
    return _svg_mob(path, scale, color=None)


def load_iconify(ref: str, scale: float = 1.0, color: str | None = None) -> "Mobject":
    _, _, WHITE = _manim()
    if color is None:
        color = WHITE
    prefix, name = ref.split(":", 1)
    svg_path = fetch_iconify_svg(prefix, name)
    return _svg_mob(svg_path, scale, color)


def load_visual(scene, spec: dict) -> "Mobject":
    """Load a resolved visual spec into a Manim mobject."""
    _, _, WHITE = _manim()
    kind = spec.get("kind", "iconify")
    ref = spec.get("ref", "lucide:sparkles")
    scale = float(spec.get("scale", 1.2))
    color = spec.get("color")
    if color is None and kind == "iconify":
        color = WHITE
    elif color == "WHITE":
        color = WHITE

    if kind == "procedural":
        return load_procedural(scene, ref, scale)
    if kind == "brand":
        return load_brand(ref, scale)
    return load_iconify(ref, scale, color)


def prefetch_beat_visuals(beat: dict) -> list[Path]:
    """Download/cache all iconify assets for a beat."""
    saved: list[Path] = []
    resolved = beat.get("visuals_resolved") or {}
    slots: list = []
    stack = resolved.get("stack")
    if isinstance(stack, list):
        slots.extend(stack)
    for slot_name in ("primary", "swap"):
        spec = resolved.get(slot_name)
        if isinstance(spec, dict):
            slots.append(spec)
    for spec in slots:
        if not isinstance(spec, dict) or spec.get("kind") != "iconify":
            continue
        ref = spec.get("ref", "")
        if ":" not in ref:
            continue
        prefix, name = ref.split(":", 1)
        desc = spec.get("description") or spec.get("concept") or "icon"
        saved.append(fetch_iconify_svg(prefix, name, description=str(desc)))
    return saved
