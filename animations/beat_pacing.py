"""Beat pacing helpers — line splitting, hold defaults, duration estimates."""

from __future__ import annotations

import re
from typing import Any

MAX_LINE_CHARS = 58
MAX_CARD_LINES = 4
MAX_BG_LINES = 3
MAX_LIST_LINES = 5

PACING_PROFILES: dict[str, dict[str, float]] = {
    "dense": {
        "label_tpc": 0.038,
        "line_tpc": 0.038,
        "default_hold": 0.9,
        "max_hold": 1.2,
        "transition": 0.65,
        "icon_entrance": 0.35,
        "card_grow": 0.3,
    },
    "relaxed": {
        "label_tpc": 0.045,
        "line_tpc": 0.05,
        "default_hold": 1.2,
        "max_hold": 2.0,
        "transition": 0.8,
        "icon_entrance": 0.45,
        "card_grow": 0.4,
    },
}


def normalize_pacing_name(pacing: str | None) -> str:
    key = (pacing or "relaxed").strip().lower()
    return key if key in PACING_PROFILES else "relaxed"


def pacing_profile(pacing: str | None) -> dict[str, float]:
    return dict(PACING_PROFILES[normalize_pacing_name(pacing)])


def _split_sentence_chunk(text: str, max_chars: int) -> list[str]:
    text = re.sub(r"\s+", " ", str(text).strip())
    if not text:
        return []
    if len(text) <= max_chars:
        return [text]

    parts: list[str] = []
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        sentence = sentence.strip()
        if not sentence:
            continue
        if len(sentence) <= max_chars:
            parts.append(sentence)
            continue
        words = sentence.split()
        current: list[str] = []
        length = 0
        for word in words:
            extra = len(word) + (1 if current else 0)
            if current and length + extra > max_chars:
                parts.append(" ".join(current))
                current = [word]
                length = len(word)
            else:
                current.append(word)
                length += extra
        if current:
            parts.append(" ".join(current))
    return parts


def split_long_lines(lines: list[str] | None, *, max_chars: int = MAX_LINE_CHARS) -> list[str]:
    out: list[str] = []
    for line in lines or []:
        out.extend(_split_sentence_chunk(str(line), max_chars))
    return out


def _cap_lines(lines: list[str], limit: int) -> list[str]:
    if len(lines) <= limit:
        return lines
    trimmed = lines[: limit - 1]
    remainder = " ".join(lines[limit - 1 :])
    trimmed.append(remainder[:MAX_LINE_CHARS].rstrip())
    return trimmed


def normalize_beat_pacing(beat: dict, pacing: str | None = None) -> dict:
    """Split overly long lines and clamp hold for render-friendly pacing."""
    out = dict(beat)
    profile = pacing_profile(pacing)

    for key, limit in (
        ("card_lines", MAX_CARD_LINES),
        ("bg_lines", MAX_BG_LINES),
        ("list_lines", MAX_LIST_LINES),
    ):
        raw = out.get(key)
        if isinstance(raw, list) and raw:
            split = split_long_lines([str(x) for x in raw])
            out[key] = _cap_lines(split, limit)

    hold = out.get("hold")
    if hold is None:
        out["hold"] = profile["default_hold"]
    else:
        try:
            out["hold"] = min(float(hold), profile["max_hold"])
        except (TypeError, ValueError):
            out["hold"] = profile["default_hold"]

    return out


def normalize_beats_pacing(beats: list[dict], pacing: str | None = None) -> list[dict]:
    return [normalize_beat_pacing(b, pacing) for b in beats if isinstance(b, dict)]


def _line_fields(beat: dict) -> list[tuple[str, list[str]]]:
    fields: list[tuple[str, list[str]]] = []
    for key in ("card_lines", "bg_lines", "list_lines", "left_lines", "right_lines", "code_lines"):
        raw = beat.get(key)
        if isinstance(raw, list) and raw:
            fields.append((key, [str(x) for x in raw]))
    punch = beat.get("punchline_line")
    if punch:
        fields.append(("punchline_line", [str(punch)]))
    return fields


def estimate_beat_seconds(beat: dict, pacing: str | None = None) -> float:
    profile = pacing_profile(pacing)
    total = 0.0

    label = str(beat.get("label") or "")
    total += max(0.35, len(label) * profile["label_tpc"])
    total += profile["card_grow"]

    visuals = beat.get("visuals_resolved") or beat.get("visuals") or {}
    if isinstance(visuals, dict) and (visuals.get("primary") or visuals.get("stack")):
        total += profile["icon_entrance"] + 0.15

    for key, lines in _line_fields(beat):
        multiplier = profile["line_tpc"] if key != "code_lines" else 0.032
        for line in lines:
            total += max(0.25, len(line) * multiplier)
        if key == "list_lines":
            total += 0.25 * len(lines)

    beat_type = (beat.get("type") or "").lower()
    if beat_type == "joke":
        total += 0.5

    camera = beat.get("camera") or []
    if camera:
        total += 0.35 * len(camera)

    try:
        total += float(beat.get("hold", profile["default_hold"]))
    except (TypeError, ValueError):
        total += profile["default_hold"]

    total += profile["transition"]
    return round(total, 1)


def estimate_project_seconds(beats: list[dict], pacing: str | None = None) -> float:
    return round(sum(estimate_beat_seconds(b, pacing) for b in beats if isinstance(b, dict)), 1)


def duration_warnings(beats: list[dict], pacing: str | None = None) -> list[dict[str, Any]]:
    """Return warnings when a project is likely too long for preview."""
    seconds = estimate_project_seconds(beats, pacing)
    warnings: list[dict[str, Any]] = []
    if seconds > 150:
        warnings.append(
            {
                "code": "long_duration",
                "message": (
                    f"Estimated runtime ~{seconds:.0f}s ({seconds / 60:.1f} min). "
                    "Use dense pacing, shorter card lines, or split into multiple videos."
                ),
                "estimated_seconds": seconds,
            }
        )
    if len(beats) > 18:
        warnings.append(
            {
                "code": "many_beats",
                "message": f"{len(beats)} beats — consider splitting into 2 episodes (target 12–16 beats).",
                "beat_count": len(beats),
            }
        )
    return warnings
