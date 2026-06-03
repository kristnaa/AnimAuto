"""Load and normalize Studio themes for Manim scenes."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

MANIM_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_BG_PATH = str(MANIM_ROOT / "background" / "orange_theme_BG.png")

DEFAULT_THEME: dict[str, Any] = {
    "id": "builtin_orange",
    "style_pack": "course_clean",
    "background": {"kind": "image", "path": DEFAULT_BG_PATH, "loop": True},
    "typography": {
        "heading": {
            "font": "Inter",
            "font_size": 48,
            "color": "#FFFFFF",
            "weight": "BOLD",
            "cursor": "#FFFFFF",
        },
        "subheading": {
            "font": "Inter",
            "font_size": 36,
            "color": "#FFFFFF",
            "weight": "BOLD",
            "cursor": "#FFEB3B",
        },
        "paragraph": {
            "font": "Inter",
            "font_size": 28,
            "color": "#000000",
            "weight": "BOLD",
            "cursor": "#FFEB3B",
        },
        "code": {
            "font": "Courier New",
            "font_size": 22,
            "color": "#abb2bf",
            "weight": "NORMAL",
            "cursor": None,
        },
    },
    "palette": {
        "card_fill": "#FFFFFF",
        "card_stroke": "#888888",
        "accent": "#FFEB3B",
        "emphasis_red": "#FC6255",
        "label_color": "#FFEB3B",
        "code_bg": "#282c34",
        "code_bg_deep": "#21252b",
        "code_border": "#3e4451",
        "code_text": "#abb2bf",
        "code_keyword": "#c678dd",
        "code_func": "#e06c75",
        "code_string": "#98c379",
        "code_number": "#d19a66",
        "code_cursor": "#528bff",
        "code_highlight": "#528bff",
        "code_error_highlight": "#e06c75",
        "code_run_green": "#98c379",
        "code_run_green_dark": "#6e9455",
    },
}


def normalize_theme(theme: dict[str, Any] | None) -> dict[str, Any]:
    if not theme:
        return json.loads(json.dumps(DEFAULT_THEME))
    merged = json.loads(json.dumps(DEFAULT_THEME))
    merged.update({k: v for k, v in theme.items() if k in ("id", "style_pack")})
    if theme.get("background"):
        merged["background"] = {**merged["background"], **theme["background"]}
    if theme.get("typography"):
        for role, spec in theme["typography"].items():
            merged["typography"].setdefault(role, {})
            merged["typography"][role].update(spec)
    if theme.get("palette"):
        merged["palette"] = {**merged["palette"], **theme["palette"]}
    return merged


def theme_from_json(raw: str | dict[str, Any]) -> dict[str, Any]:
    if isinstance(raw, str):
        return normalize_theme(json.loads(raw))
    return normalize_theme(raw)


def resolve_manim_color(value: str):
    """Map hex or Manim color name to a Manim color."""
    from manim import ManimColor

    if value.startswith("#"):
        return ManimColor(value)
    name = value.upper()
    import manim as mn

    if hasattr(mn, name):
        return getattr(mn, name)
    return ManimColor(value)
