"""Statement beat — full-width card with optional text, image, and video."""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from manim import Mobject

StatementMode = Literal[
    "auto",
    "text",
    "image",
    "video",
    "text_image",
    "text_video",
    "text_image_video",
]

STATEMENT_MODES: tuple[str, ...] = (
    "auto",
    "text",
    "image",
    "video",
    "text_image",
    "text_video",
    "text_image_video",
)


def normalize_statement_block(beat: dict) -> dict:
    """Merge legacy card_lines and nested statement block into one shape."""
    raw = beat.get("statement")
    block: dict = dict(raw) if isinstance(raw, dict) else {}

    text_lines = block.get("text_lines")
    if not text_lines and beat.get("card_lines"):
        text_lines = list(beat["card_lines"])
    if isinstance(text_lines, list):
        block["text_lines"] = [str(x).strip() for x in text_lines if str(x).strip()]

    mode = block.get("mode") or "auto"
    if mode not in STATEMENT_MODES:
        mode = "auto"
    block["mode"] = mode

    for slot in ("image", "video"):
        spec = block.get(slot)
        if isinstance(spec, dict) and spec.get("ref"):
            block[slot] = {
                "ref": str(spec["ref"]),
                "kind": spec.get("kind") or "project",
                "loop": bool(spec.get("loop", True)),
                "muted": bool(spec.get("muted", True)),
            }
        elif slot in block:
            block.pop(slot, None)

    return block


def _has_text(block: dict) -> bool:
    return bool(block.get("text_lines"))


def _has_image(block: dict) -> bool:
    img = block.get("image")
    return isinstance(img, dict) and bool(img.get("ref"))


def _has_video(block: dict) -> bool:
    vid = block.get("video")
    return isinstance(vid, dict) and bool(vid.get("ref"))


def resolve_statement_mode(block: dict) -> str:
    mode = str(block.get("mode") or "auto")
    has_text = _has_text(block)
    has_image = _has_image(block)
    has_video = _has_video(block)

    if mode != "auto" and mode in STATEMENT_MODES:
        return mode

    parts: list[str] = []
    if has_text:
        parts.append("text")
    if has_image:
        parts.append("image")
    if has_video:
        parts.append("video")
    if not parts:
        return "text"
    return "_".join(parts)


def statement_flags(mode: str) -> tuple[bool, bool, bool]:
    """Return (show_text, show_image, show_video) for a resolved mode."""
    show_text = "text" in mode or mode in ("", "auto")
    show_image = "image" in mode
    show_video = "video" in mode
    if mode == "text":
        return True, False, False
    if mode == "image":
        return False, True, False
    if mode == "video":
        return False, False, True
    if mode == "text_image":
        return True, True, False
    if mode == "text_video":
        return True, False, True
    if mode == "text_image_video":
        return True, True, True
    return show_text, show_image, show_video


def is_statement_full_card(beat: dict) -> bool:
    layout = str(beat.get("layout") or "")
    if layout == "statement_full_card":
        return True
    if beat.get("type") == "statement" and isinstance(beat.get("statement"), dict):
        return True
    return False
