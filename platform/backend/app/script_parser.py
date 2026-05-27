"""Parse beat.script.md-style text or JSON into project beats."""

from __future__ import annotations

import json
import re
from typing import Any

CAMERA_ACTIONS = {
    "cam_focus_left",
    "cam_focus_right",
    "cam_focus_card",
    "cam_focus_mobject",
    "cam_restore",
    "cam_restore_fast",
    "cam_pan_left",
    "cam_pan_right",
}

ICONIFY_REF = re.compile(r"^[a-z0-9-]+:[a-z0-9-]+$")

CONCEPT_ALIASES: dict[str, str] = {
    "scream": "frustration",
}


def _parse_icon_line(line: str) -> tuple[str, str, dict[str, Any]] | None:
    line = line.strip().lstrip("-").strip()
    if not line or line.startswith("|") or line.startswith("#") or ":" not in line:
        return None

    icon_id, rest = line.split(":", 1)
    icon_id = icon_id.strip()
    extras: dict[str, str] = {}
    ref_part = rest.strip()
    if "|" in ref_part:
        chunks = [chunk.strip() for chunk in ref_part.split("|")]
        ref_part = chunks[0]
        for chunk in chunks[1:]:
            if ":" in chunk:
                key, value = chunk.split(":", 1)
                extras[key.strip().lower()] = value.strip()

    ref = ref_part.strip()
    if not icon_id or not ref:
        return None

    meta: dict[str, Any] = {}
    if ICONIFY_REF.match(ref):
        meta["ref"] = ref
    else:
        meta["description"] = ref
    if extras.get("color"):
        meta["color"] = extras["color"]
    if extras.get("scale"):
        meta["scale"] = float(extras["scale"])
    if extras.get("trigger"):
        meta["trigger"] = extras["trigger"]
    return icon_id, ref, meta


def _concept_from_icon_id(icon_id: str) -> str:
    concept = icon_id.removeprefix("icon_").removeprefix("shape_")
    if "question" in icon_id:
        concept = "question"
    return CONCEPT_ALIASES.get(concept, concept)


HOOK_ALIASES = {
    "after_line_1": "after_line_1",
    "after_line_2": "after_line_2",
    "after_line_3": "after_line_3",
    "after_icon": "after_icon",
    "after_primary_icon": "after_icon",
    "punchline": "punchline",
    "before_punchline": "punchline",
    "exit": "exit",
    "beat_exit": "exit",
}


def _strip(s: str) -> str:
    return s.strip()


def _parse_meta_header(text: str) -> dict[str, Any]:
    """Parse episode-level fields before first ### BEAT."""
    meta: dict[str, Any] = {}
    pre = text.split("### BEAT")[0] if "### BEAT" in text else text[:800]

    cam = re.search(r"^CAMERA:\s*(.+)$", pre, re.M | re.I)
    if cam:
        val = _strip(cam.group(1)).lower()
        meta["use_camera"] = val in ("moving", "yes", "true", "on")

    style = re.search(r"^STYLE_PACK:\s*(.+)$", pre, re.M | re.I)
    if style:
        meta["style_pack"] = _strip(style.group(1))

    name = re.search(r"^NAME:\s*(.+)$", pre, re.M | re.I)
    if name:
        meta["name"] = _strip(name.group(1))

    return meta


def _parse_card_section(block: str, beat: dict) -> None:
    card_m = re.search(r"─── CARD ───\s*\n(.+?)(?=\n───|\nHOLD|\Z)", block, re.S | re.I)
    if not card_m:
        return
    section = card_m.group(1)
    side = re.search(r"SIDE:\s*(left|right)", section, re.I)
    if side:
        beat["card_side"] = side.group(1).lower()
    size = re.search(r"SIZE:\s*([\d.]+)\s*[×x]\s*([\d.]+)", section, re.I)
    if size:
        beat["card_width"] = float(size.group(1))
        beat["card_height"] = float(size.group(2))


def _parse_emphasis_section(block: str, beat: dict) -> None:
    em_m = re.search(r"─── EMPHASIS ───\s*\n(.+?)(?=\n───|\nHOLD|\Z)", block, re.S | re.I)
    if not em_m:
        return
    emphasis: list[dict] = []
    for line in em_m.group(1).splitlines():
        line = line.strip().lstrip("-").strip()
        if not line or line.startswith("|"):
            continue
        parts = {}
        for chunk in line.split("|"):
            chunk = chunk.strip()
            if ":" in chunk:
                k, v = chunk.split(":", 1)
                parts[k.strip().lower()] = v.strip()
        if parts.get("word"):
            emphasis.append(
                {
                    "word": parts["word"],
                    "color": parts.get("color", "YELLOW").upper(),
                    "animation": parts.get("animation", "indicate"),
                }
            )
    if emphasis:
        beat["emphasis"] = emphasis


def _parse_camera_section(block: str, beat: dict) -> None:
    cam_m = re.search(r"─── CAMERA ───\s*\n(.+?)(?=\n───|\nHOLD|\Z)", block, re.S | re.I)
    steps: list[dict] = []
    if cam_m:
        for line in cam_m.group(1).splitlines():
            line = line.strip()
            if not line or line.startswith("|"):
                continue
            if ":" in line:
                action, hook = line.split(":", 1)
                action = action.strip()
                hook = hook.strip().lower().replace(" ", "_")
                if action in CAMERA_ACTIONS:
                    steps.append(
                        {
                            "action": action,
                            "hook": HOOK_ALIASES.get(hook, hook),
                            "run_time": 0.9,
                        }
                    )

    # Also parse cam_* from timeline table
    tl = re.search(r"─── TIMELINE ───\s*\n(.+?)(?=\n───|\Z)", block, re.S | re.I)
    if tl:
        for line in tl.group(1).splitlines():
            if "cam_" not in line:
                continue
            for action in CAMERA_ACTIONS:
                if action in line:
                    steps.append({"action": action, "hook": "timeline", "run_time": 0.9})

    if steps:
        beat["camera"] = steps


def _parse_beat_block(block: str) -> dict[str, Any]:
    beat: dict[str, Any] = {
        "hold": 1.2,
        "card_width": 5.6,
        "card_height": 5.0,
    }

    title = re.search(r"^###\s*BEAT\s*\d+\s*[—–-]\s*(.+)$", block, re.M | re.I)
    if title:
        beat["_slug"] = _strip(title.group(1))

    for key, field in [
        (r"^TYPE:\s*(.+)$", "type"),
        (r"^LAYOUT:\s*(.+)$", "layout"),
        (r"^ICON GRID:\s*(.+)$", "icon_grid"),
        (r"^ICON REVEAL:\s*(.+)$", "icon_reveal"),
        (r"^DURATION:\s*(.+)$", "duration"),
        (r"^HOLD:\s*([\d.]+)", "hold"),
        (r"^CAMERA:\s*(.+)$", "camera_mode"),
    ]:
        m = re.search(key, block, re.M | re.I)
        if m:
            val = _strip(m.group(1))
            if field == "hold":
                beat[field] = float(re.sub(r"[^\d.]", "", val) or "1.2")
            elif field == "camera_mode":
                beat["use_camera"] = val.lower() in ("moving", "yes", "true", "on")
            elif field == "type":
                beat[field] = val.strip()
            else:
                beat[field] = val

    label_m = re.search(
        r"(?:─── CONTENT ───\s*\n)?LABEL:\s*\n(.+?)(?=\n(?:TEXT|BG TEXT|───|\Z))",
        block,
        re.S | re.I,
    )
    if not label_m:
        label_m = re.search(
            r"LABEL:\s*\n(.+?)(?=\n(?:TEXT|BG TEXT|───|\Z))",
            block,
            re.S | re.I,
        )
    if label_m:
        beat["label"] = _strip(label_m.group(1))

    card_m = re.search(
        r"TEXT\s*\(card[^)]*\):\s*\n(.+?)(?=\n(?:───|BG TEXT|ICONS|CARD|HOLD|\Z))",
        block,
        re.S | re.I,
    )
    if card_m:
        lines = [_strip(l) for l in card_m.group(1).splitlines() if _strip(l)]
        if lines:
            type_lower = beat.get("type", "").lower()
            is_punchline = "punchline" in type_lower or "joke" in type_lower
            if is_punchline and len(lines) > 1:
                beat["card_lines"] = lines[:-1]
                beat["punchline_line"] = lines[-1]
            else:
                beat["card_lines"] = lines

    bg_m = re.search(
        r"TEXT\s*\(white[^)]*\):\s*\n(.+?)(?=\n(?:───|ICONS|HOLD|\Z))",
        block,
        re.S | re.I,
    )
    if not bg_m:
        bg_m = re.search(
            r"BG TEXT:\s*\n(.+?)(?=\n(?:───|ICONS|HOLD|\Z))",
            block,
            re.S | re.I,
        )
    if bg_m:
        beat["bg_lines"] = [_strip(l) for l in bg_m.group(1).splitlines() if _strip(l)]

    icons_m = re.search(r"─── ICONS.*?───\s*\n(.+?)(?=\n───|\nHOLD|\Z)", block, re.S | re.I)
    visuals: dict[str, Any] = {}
    if icons_m:
        manifest: dict[str, str] = {}
        slots: list[dict[str, Any]] = []
        for line in icons_m.group(1).splitlines():
            parsed = _parse_icon_line(line)
            if not parsed:
                continue
            icon_id, ref, meta = parsed
            concept = _concept_from_icon_id(icon_id)
            slot: dict[str, Any] = {
                "concept": concept,
                "icon_id": icon_id,
                **meta,
            }
            if meta.get("ref"):
                manifest[icon_id] = meta["ref"]
            if ref == "shape_question" and not meta.get("ref"):
                slot["kind"] = "procedural"
            slots.append(slot)

        if manifest:
            beat["icons"] = manifest

        if slots:
            layout = beat.get("layout", "")
            if len(slots) >= 3 or "stack" in layout:
                visuals["stack"] = [{**slot, "role": "subject"} for slot in slots[:4]]
            else:
                visuals["primary"] = {**slots[0], "role": "subject"}
                if len(slots) > 1:
                    visuals["swap"] = {**slots[1], "role": "punchline"}

    if visuals:
        beat["visuals"] = visuals

    _parse_card_section(block, beat)
    _parse_emphasis_section(block, beat)
    _parse_camera_section(block, beat)

    # Timeline table emphasis (legacy)
    wiggle_m = re.search(r'"([^"]+)"\s*\|\s*anim_word_red\s*\+\s*anim_wiggle', block, re.I)
    if wiggle_m:
        word = wiggle_m.group(1)
        existing = {e.get("word") for e in beat.get("emphasis") or [] if isinstance(e, dict)}
        if word not in existing:
            beat.setdefault("emphasis", []).append(
                {"word": word, "color": "RED", "animation": "wiggle"}
            )
        if visuals.get("swap"):
            visuals["swap"]["trigger"] = word

    indicate_m = re.search(r'"(\w+)"\s*\|\s*anim_indicate', block, re.I)
    if indicate_m:
        beat.setdefault("emphasis", []).append(
            {"word": indicate_m.group(1), "color": "YELLOW", "animation": "indicate"}
        )

    # Link emphasis trigger to swap visual
    for em in beat.get("emphasis") or []:
        if not isinstance(em, dict):
            continue
        if em.get("animation") == "wiggle" and visuals.get("swap") and not visuals["swap"].get("trigger"):
            visuals["swap"]["trigger"] = em["word"]

    if not beat.get("layout"):
        beat["layout"] = (
            "text_right_icon_left" if beat.get("bg_lines") else "card_right_icon_left"
        )
    if not beat.get("type"):
        beat["type"] = "statement"
    if not beat.get("label"):
        beat["label"] = beat.get("_slug", "Beat").replace("_", " ").title()

    beat.pop("_slug", None)
    return beat


def parse_script(text: str) -> dict[str, Any]:
    """Parse script text into partial project dict with beats list."""
    text = text.strip()
    if not text:
        raise ValueError("Script is empty")

    meta = _parse_meta_header(text)

    # Full project JSON
    if text.startswith("{"):
        data = json.loads(text)
        if "beats" in data:
            return {
                "name": data.get("name", "Script Import"),
                "style_pack": data.get("style_pack", "course_clean"),
                "use_camera": data.get("use_camera", False),
                "beats": data["beats"],
            }

    # JSON beats array only
    if text.startswith("["):
        return {"beats": json.loads(text), **meta}

    blocks = re.split(r"(?=^###\s*BEAT\s)", text, flags=re.M | re.I)
    beats = []
    for block in blocks:
        block = block.strip()
        if not block or not re.match(r"^###\s*BEAT", block, re.I):
            continue
        beat = _parse_beat_block(block)
        if beat.get("label") or beat.get("card_lines") or beat.get("bg_lines"):
            beats.append(beat)

    if not beats:
        raise ValueError(
            "Could not parse beats. Use ### BEAT headers or JSON with a beats array."
        )

    # Episode camera: meta flag OR any beat requests camera
    use_camera = meta.get("use_camera", False) or any(b.get("use_camera") for b in beats)

    name_m = re.search(r"^#\s+(.+)$", text, re.M)
    return {
        "name": meta.get("name") or (name_m.group(1).strip() if name_m else "Script Import"),
        "style_pack": meta.get("style_pack", "course_clean"),
        "use_camera": use_camera,
        "beats": beats,
    }
