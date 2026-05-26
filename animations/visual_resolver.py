"""Semantic visual resolver — maps beat context to concrete visual specs."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
CATALOG_PATH = ROOT / "assets" / "visual_catalog.json"
STYLE_PACKS_DIR = ROOT / "assets" / "style_packs"

ROLE_DEFAULTS: dict[str, str] = {
    "subject": "sparkles",
    "question": "question",
    "tool": "terminal",
    "actor": "computer",
    "process": "code",
    "punchline": "failure",
    "brand": "python",
    "emphasis": "sparkles",
}

TYPE_RULES: dict[str, dict[str, Any]] = {
    "question": {"left_concept": "question", "left_role": "question"},
    "statement": {"left_role": "subject"},
    "joke": {"left_role": "subject", "swap_role": "punchline"},
    "joke punchline": {"left_role": "subject", "swap_role": "punchline"},
    "explain": {"left_role": "tool"},
}


def _as_dict(value: Any, default: dict | None = None) -> dict:
    """Coerce GPT/script output into a dict (lists often arrive where dicts are expected)."""
    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                return item
        return default or {}
    return default or {}


def _normalize_visuals(visuals: Any) -> dict:
    if visuals is None:
        return {}
    if isinstance(visuals, list):
        out: dict[str, dict] = {}
        if len(visuals) > 0:
            out["primary"] = _as_dict(visuals[0])
        if len(visuals) > 1:
            out["swap"] = _as_dict(visuals[1])
        return out
    if isinstance(visuals, dict):
        return {
            "primary": _as_dict(visuals.get("primary") or visuals.get("left")),
            "swap": _as_dict(visuals.get("swap") or visuals.get("left_swap"), default={}),
        }
    return {}


def _emphasis_trigger(beat: dict) -> str | None:
    emphasis = beat.get("emphasis")
    if not emphasis:
        return None
    if isinstance(emphasis, list):
        first = emphasis[0]
        if isinstance(first, dict):
            return first.get("word")
        if isinstance(first, str):
            return first
    return None


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text())


def load_catalog() -> dict[str, dict]:
    return _load_json(CATALOG_PATH)


def load_style_pack(pack_id: str = "course_clean") -> dict:
    path = STYLE_PACKS_DIR / f"{pack_id}.json"
    if not path.exists():
        path = STYLE_PACKS_DIR / "course_clean.json"
    return _load_json(path)


def _tokenize(text: str) -> set[str]:
    return {t.lower() for t in re.findall(r"[a-zA-Z']+", text.lower())}


def score_concept(concept_id: str, entry: dict, tokens: set[str], beat_type: str) -> float:
    score = 0.0
    tags = set(entry.get("tags", []))
    synonyms = set(entry.get("synonyms", []))
    if concept_id in tokens:
        score += 10
    score += len(tokens & synonyms) * 4
    score += len(tokens & tags) * 2
    if beat_type in tags:
        score += 5
    return score


def infer_concept_from_text(text: str, beat_type: str = "statement", role: str = "subject") -> str:
    catalog = load_catalog()
    tokens = _tokenize(text)
    best_id = ROLE_DEFAULTS.get(role, "sparkles")
    best_score = 0.0
    for concept_id, entry in catalog.items():
        s = score_concept(concept_id, entry, tokens, beat_type)
        if s > best_score:
            best_score = s
            best_id = concept_id
    return best_id if best_score > 0 else ROLE_DEFAULTS.get(role, "sparkles")


def _pick_candidate(entry: dict, style_pack: dict) -> dict:
    exclude = set(style_pack.get("exclude_style_packs", []))
    prefer_kinds = style_pack.get("prefer_kinds", ["procedural", "brand", "iconify"])
    candidates = entry.get("candidates", [])
    filtered = [
        c
        for c in candidates
        if c.get("style_pack") is None or c.get("style_pack") not in exclude
    ]
    if not filtered:
        filtered = candidates
    for kind in prefer_kinds:
        for c in filtered:
            if c.get("kind") == kind:
                return dict(c)
    return dict(filtered[0]) if filtered else {"kind": "iconify", "ref": "lucide:sparkles", "scale": 1.2}


ICONIFY_REF = re.compile(r"^[a-z0-9-]+:[a-z0-9-]+$")


def _infer_kind_from_ref(ref: str, icon_id: str = "") -> str:
    if ref.startswith("assets/") or ("/" in ref and ref.endswith(".svg")):
        return "brand"
    if ref == "shape_question":
        return "procedural"
    if ICONIFY_REF.match(ref):
        return "iconify"
    return "iconify"


def resolve_visual_slot(
    slot: dict,
    *,
    concept: str,
    role: str,
    style_pack_id: str,
) -> dict:
    """Use explicit script ref/color when provided; otherwise fall back to catalog."""
    style_pack = load_style_pack(style_pack_id)
    ref = (slot.get("ref") or "").strip()
    if ref:
        if ICONIFY_REF.match(ref):
            kind = "iconify"
        elif ref == "shape_question":
            kind = "procedural"
        else:
            kind = slot.get("kind") or _infer_kind_from_ref(ref, slot.get("icon_id", ""))
        color = slot.get("color")
        if color is None and kind == "iconify":
            color = style_pack.get("default_icon_color", "#FFFFFF")
        return {
            "concept": concept,
            "role": role,
            "kind": kind,
            "ref": ref,
            "scale": float(slot.get("scale", 1.2)),
            "color": color,
        }
    return resolve_concept(concept, style_pack_id=style_pack_id, role=role)


def resolve_concept(
    concept: str,
    *,
    style_pack_id: str = "course_clean",
    role: str = "subject",
) -> dict:
    catalog = load_catalog()
    style_pack = load_style_pack(style_pack_id)
    entry = catalog.get(concept) or catalog.get(ROLE_DEFAULTS.get(role, "sparkles"), {})
    candidate = _pick_candidate(entry, style_pack)
    color = candidate.get("color")
    if color is None and candidate.get("kind") == "iconify":
        color = style_pack.get("default_icon_color", "#FFFFFF")
    return {
        "concept": concept,
        "role": role,
        "kind": candidate.get("kind", "iconify"),
        "ref": candidate.get("ref", "lucide:sparkles"),
        "scale": candidate.get("scale", 1.2),
        "color": color,
    }


def resolve_beat_visuals(beat: dict, style_pack_id: str | None = None) -> dict:
    """Resolve all visuals for a beat dict. Mutates and returns beat with resolved visuals."""
    pack = style_pack_id or beat.get("style_pack", "course_clean")
    beat_type = beat.get("type", "statement").lower()
    rules = TYPE_RULES.get(beat_type, TYPE_RULES["statement"])

    all_text = " ".join(
        [
            beat.get("label", ""),
            " ".join(beat.get("card_lines", [])),
            " ".join(beat.get("bg_lines", [])),
            beat.get("punchline_line", ""),
        ]
    )

    visuals_in = _normalize_visuals(beat.get("visuals"))
    resolved: dict[str, dict] = {}

    # Primary left visual
    primary = visuals_in.get("primary") or {}
    concept = primary.get("concept")
    role = primary.get("role") or rules.get("left_role", "subject")
    if not concept:
        concept = rules.get("left_concept") or infer_concept_from_text(all_text, beat_type, role)
    resolved["primary"] = resolve_visual_slot(
        primary,
        concept=concept,
        role=role,
        style_pack_id=pack,
    )

    # Optional swap (punchline)
    swap = visuals_in.get("swap")
    if swap or rules.get("swap_role") or beat.get("punchline_line"):
        swap = swap or {}
        swap_role = swap.get("role") or rules.get("swap_role", "punchline")
        swap_concept = swap.get("concept") or infer_concept_from_text(
            beat.get("punchline_line", all_text), beat_type, swap_role
        )
        trigger = swap.get("trigger") or swap.get("trigger_word") or _emphasis_trigger(beat)
        resolved["swap"] = {
            **resolve_visual_slot(
                swap,
                concept=swap_concept,
                role=swap_role,
                style_pack_id=pack,
            ),
            "trigger": trigger,
        }

    beat = dict(beat)
    beat["visuals_resolved"] = resolved
    beat["style_pack"] = pack
    return beat


def resolve_project(project: dict) -> dict:
    """Resolve visuals for every beat in a project."""
    pack = project.get("style_pack", "course_clean")
    beats = [resolve_beat_visuals(b, pack) for b in project.get("beats", [])]
    out = dict(project)
    out["beats"] = beats
    return out


def build_icons_manifest(beat: dict) -> dict[str, str]:
    """Extract iconify refs needed for a beat into icons.json format."""
    if beat.get("icons"):
        return dict(beat["icons"])
    manifest: dict[str, str] = {}
    for slot, spec in (beat.get("visuals_resolved") or {}).items():
        if not isinstance(spec, dict) or spec.get("kind") != "iconify":
            continue
        concept = spec.get("concept", slot)
        icon_id = f"icon_{concept}"
        manifest[icon_id] = spec["ref"]
    return manifest
