"""Re-export Excalidraw parser from animations package for FastAPI backend."""

from __future__ import annotations

import sys
from pathlib import Path

MANIM_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(MANIM_ROOT / "animations"))

from excalidraw_parser import (  # noqa: E402
    ExcalidrawPage,
    build_page_svg,
    detect_svg_pages,
    excalidraw_elements,
    load_scene_file,
    pages_from_excalidraw_file,
    pages_from_excalidraw_scene,
    parse_animation_sequence_phrases,
    scene_background,
    svg_canvas_background_color,
    svg_layer_paths,
)

__all__ = [
    "ExcalidrawPage",
    "build_page_svg",
    "detect_svg_pages",
    "excalidraw_elements",
    "load_scene_file",
    "pages_from_excalidraw_file",
    "pages_from_excalidraw_scene",
    "parse_animation_sequence_phrases",
    "scene_background",
    "svg_canvas_background_color",
    "svg_layer_paths",
]
