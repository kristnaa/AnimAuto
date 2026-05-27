"""Word-triggered icon reveal helpers."""

from __future__ import annotations

import re


def split_line_by_triggers(text: str, triggers: list[str]) -> list[tuple[str, str | None]]:
    """Split *text* into segments; trigger segments carry the matched word (lowered)."""
    if not text or not triggers:
        return [(text, None)]

    unique = sorted({t.strip().lower() for t in triggers if t.strip()}, key=len, reverse=True)
    if not unique:
        return [(text, None)]

    pattern = "|".join(re.escape(t) for t in unique)
    parts: list[tuple[str, str | None]] = []
    pos = 0
    for match in re.finditer(rf"(?i)\b(?:{pattern})\b", text):
        if match.start() > pos:
            parts.append((text[pos : match.start()], None))
        parts.append((match.group(0), match.group(0).lower()))
        pos = match.end()
    if pos < len(text):
        parts.append((text[pos:], None))
    return parts if parts else [(text, None)]


def line_has_trigger(text: str, triggers: list[str]) -> bool:
    lowered = text.lower()
    for word in triggers:
        w = word.strip().lower()
        if w and re.search(rf"(?i)\b{re.escape(w)}\b", lowered):
            return True
    return False


def resolve_icon_reveal_mode(beat: dict, stack_specs: list[dict]) -> str:
    """Return ``together`` or ``on_word``."""
    mode = (beat.get("icon_reveal") or "auto").lower().replace("-", "_").replace(" ", "_")
    has_triggers = any(s.get("trigger") for s in stack_specs)
    if mode in ("together", "batch", "all"):
        return "together"
    if mode in ("on_word", "word", "sync", "trigger"):
        return "on_word"
    # auto — sync when any icon declares a trigger word
    return "on_word" if has_triggers else "together"
