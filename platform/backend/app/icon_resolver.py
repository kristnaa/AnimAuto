"""Resolve semantic icon descriptions to Iconify refs via GPT."""

from __future__ import annotations

import json
import re
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from app.openai_service import OpenAIService

ICONIFY_REF = re.compile(r"^[a-z0-9-]+:[a-z0-9-]+$")

ICON_RESOLVE_PROMPT = """You pick Iconify icons for Manim course videos (orange background, split-screen layout).

Return ONLY valid JSON:
{
  "resolved": {
    "0:primary": "prefix:name",
    "1:swap": "prefix:name"
  }
}

Keys are beat_index:slot where slot is "primary" or "swap".

Rules:
- Return only real Iconify refs in the form prefix:name (lowercase).
- Prefer lucide: for clean mono UI icons (terminal, laptop, code, help circle, sparkles).
- Prefer fa6-brands: or devicon: for brand logos (python, javascript, react).
- Prefer twemoji: or noto: for emoji — use full names like twemoji:face-screaming-in-fear (not screaming-face).
- Match each description semantically — do not return generic placeholders.
- One ref per requested key. Every key in the request must appear in resolved.
"""


def beats_need_icon_resolution(beats: list[dict]) -> bool:
    for beat in beats:
        for slot in (beat.get("visuals") or {}).values():
            if isinstance(slot, dict) and slot.get("description") and not slot.get("ref"):
                return True
    return False


def collect_icon_requests(beats: list[dict]) -> list[dict[str, Any]]:
    requests: list[dict[str, Any]] = []
    for beat_index, beat in enumerate(beats):
        visuals = beat.get("visuals") or {}
        for slot in ("primary", "swap"):
            spec = visuals.get(slot)
            if not isinstance(spec, dict) or spec.get("ref"):
                continue
            description = (spec.get("description") or "").strip()
            if not description:
                continue
            requests.append(
                {
                    "key": f"{beat_index}:{slot}",
                    "beat_index": beat_index,
                    "slot": slot,
                    "icon_id": spec.get("icon_id", slot),
                    "description": description,
                    "color": spec.get("color"),
                    "beat_label": beat.get("label", ""),
                    "beat_type": beat.get("type", ""),
                    "layout": beat.get("layout", ""),
                }
            )
    return requests


def apply_resolved_icons(beats: list[dict], resolved: dict[str, str]) -> list[dict]:
    out = [dict(b) for b in beats]
    for beat_index, beat in enumerate(out):
        visuals = dict(beat.get("visuals") or {})
        manifest = dict(beat.get("icons") or {})
        for slot in ("primary", "swap"):
            spec = visuals.get(slot)
            if not isinstance(spec, dict):
                continue
            key = f"{beat_index}:{slot}"
            ref = resolved.get(key)
            if not ref or not ICONIFY_REF.match(ref):
                continue
            spec = dict(spec)
            spec["ref"] = ref
            spec["kind"] = "iconify"
            spec.pop("description", None)
            icon_id = spec.get("icon_id") or f"icon_{slot}"
            manifest[icon_id] = ref
            visuals[slot] = spec
        if visuals:
            beat["visuals"] = visuals
        if manifest:
            beat["icons"] = manifest
    return out


def validate_icon_refs(beats: list[dict]) -> list[dict]:
    """Ensure every Iconify ref exists; search Iconify for alternatives on 404."""
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(root / "animations"))
    from icon_library import ensure_iconify_ref  # noqa: E402

    out: list[dict] = []
    for beat in beats:
        beat = dict(beat)
        visuals = dict(beat.get("visuals") or {})
        manifest = dict(beat.get("icons") or {})

        for slot in ("primary", "swap"):
            spec = visuals.get(slot)
            if not isinstance(spec, dict):
                continue
            ref = (spec.get("ref") or "").strip()
            if not ref or not ICONIFY_REF.match(ref):
                continue
            desc = (spec.get("description") or spec.get("icon_id") or "").replace("_", " ")
            fixed = ensure_iconify_ref(ref, desc)
            if fixed != ref:
                spec = dict(spec)
                spec["ref"] = fixed
                spec["kind"] = "iconify"
                icon_id = spec.get("icon_id")
                if icon_id:
                    manifest[icon_id] = fixed
                visuals[slot] = spec

        for icon_id, ref in list(manifest.items()):
            if not isinstance(ref, str) or not ICONIFY_REF.match(ref):
                continue
            desc = icon_id.replace("_", " ").replace("icon ", "").replace("shape ", "")
            manifest[icon_id] = ensure_iconify_ref(ref, desc)

        if visuals:
            beat["visuals"] = visuals
        if manifest:
            beat["icons"] = manifest
        out.append(beat)
    return out


def resolve_beat_icons(beats: list[dict], ai: OpenAIService) -> list[dict]:
    requests = collect_icon_requests(beats)
    if not requests:
        return validate_icon_refs(beats)
    resolved = ai.resolve_icon_descriptions(requests)
    beats = apply_resolved_icons(beats, resolved)
    return validate_icon_refs(beats)
