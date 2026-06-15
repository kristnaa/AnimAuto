"""Layout template catalog and default page structures for the voice director."""

from __future__ import annotations

import re
from typing import Any

LAYOUT_IDS = (
    "center_title",
    "center_bullets",
    "flowchart_vertical",
    "flowchart_horizontal",
    "compare_columns",
    "diagram_labeled",
    "kinetic_keywords",
    "visual_orbit",
    "pipeline_blackboard",
    "mind_map_radial",
    "fade_transition",
)

ICON_IDS = (
    "bar_chart_up",
    "rocket",
    "code_simple",
    "swiss_knife",
    "robot_arm",
    "globe",
    "gamepad",
    "chart_lines",
    "crowd",
    "brain_gear",
    "document_py",
    "gear_process",
    "cube_vm",
    "binary_strip",
    "pac_output",
)

BACKGROUND_STYLE_IDS = (
    "blackboard_clean",
    "radial_blue",
    "corner_warm",
    "grid_fade",
    "split_tone",
    "orbit_glow",
    "edge_frame",
)

MAX_HOOK_WORDS = 4
MAX_LABEL_WORDS = 3
MAX_BULLET_WORDS = 5

LAYOUT_DESCRIPTIONS: dict[str, str] = {
    "center_title": "Hook ONLY — 2–4 word title + visual badge (intro sentences)",
    "center_bullets": "Short bullet labels (≤5 words each) beside colored dots — lists, multi-point ideas",
    "flowchart_vertical": "Numbered boxes + arrows — NO narration caption, labels only",
    "flowchart_horizontal": "Left-to-right pipeline — labels only, no paragraph text",
    "compare_columns": "Two short labels + vs arrow — contrasts, before/after",
    "diagram_labeled": "Central shape + 1–3 word label INSIDE — optional 3-word caption max",
    "kinetic_keywords": "ONE emphasized keyword (1–2 words) + pulsing shape — no subtitle",
    "visual_orbit": "Hub diagram: center concept + 2–4 satellite nodes — minimal labels",
    "pipeline_blackboard": "Blackboard L→R pipeline with icons + dashed yellow arrows + nested process box",
    "mind_map_radial": "Radial hub + curved branches + icon per branch (full or single mode)",
    "fade_transition": "Visual bridge — 1–2 word hint OR pure motion (arrow pulse), no sentences",
}

BACKGROUND_DESCRIPTIONS: dict[str, str] = {
    "blackboard_clean": "Minimal chalk dust — default for blackboard pipeline/mind-map pages",
    "corner_warm": "Warm orange corner accents — energy, hooks, CTAs",
    "grid_fade": "Faint grid + teal wash — structure, lists, processes",
    "split_tone": "Diagonal purple/teal split — comparisons, transitions",
    "orbit_glow": "Scattered glow dots — concepts, orbit layouts",
    "edge_frame": "Minimal edge brackets — clean, keyword moments",
    "radial_blue": "Soft blue radial rings — tech, data, AI topics",
}


def layout_catalog_for_prompt() -> str:
    lines = [
        "Layouts (one per sentence). Narration stays in VO — screen shows visuals + short labels only:",
    ]
    for lid in LAYOUT_IDS:
        lines.append(f"- {lid}: {LAYOUT_DESCRIPTIONS[lid]}")
    lines.append("\nBackground styles (pick a DIFFERENT one per page when possible):")
    for bid in BACKGROUND_STYLE_IDS:
        lines.append(f"- {bid}: {BACKGROUND_DESCRIPTIONS[bid]}")
    return "\n".join(lines)


ICON_HINTS: dict[str, str] = {
    "bar_chart_up": "demand, growth",
    "rocket": "speed, power",
    "code_simple": "simplicity",
    "swiss_knife": "versatility",
    "robot_arm": "automation",
    "globe": "web",
    "gamepad": "gaming",
    "chart_lines": "data science",
    "crowd": "community",
    "brain_gear": "AI",
    "document_py": "source code",
    "gear_process": "compiler/process",
    "cube_vm": "virtual machine",
    "binary_strip": "bytecode",
    "pac_output": "output/result",
}


def icon_catalog_for_prompt() -> str:
    lines = ["Icon catalog (icon_id per pipeline stage or mind-map branch):"]
    for iid in ICON_IDS:
        lines.append(f"- {iid}: {ICON_HINTS.get(iid, '')}")
    return "\n".join(lines)


def clip_words(text: str, max_words: int) -> str:
    words = re.findall(r"\S+", (text or "").strip())
    if not words:
        return ""
    return " ".join(words[:max_words]).strip(".,!?;:")


def _extract_bullet_candidates(text: str) -> list[str]:
    parts = re.split(r",|\band\b|\bthen\b|\balso\b", text, flags=re.I)
    out = [clip_words(p.strip(" ."), MAX_BULLET_WORDS) for p in parts if p.strip(" .")]
    out = [x for x in out if x]
    if len(out) >= 2:
        return out[:4]
    words = text.split()
    if len(words) <= MAX_BULLET_WORDS:
        return [clip_words(text, MAX_BULLET_WORDS)]
    mid = len(words) // 2
    return [
        clip_words(" ".join(words[:mid]), MAX_BULLET_WORDS),
        clip_words(" ".join(words[mid:]), MAX_BULLET_WORDS),
    ]


def _flowchart_labels(text: str) -> list[str]:
    bullets = _extract_bullet_candidates(text)
    if len(bullets) >= 2:
        out = []
        for b in bullets[:4]:
            words = b.split()
            while words and words[0].lower() in ("first", "then", "next", "finally", "we", "you", "i"):
                words = words[1:]
            out.append(clip_words(" ".join(words) or b, MAX_LABEL_WORDS))
        return out
    words = [w for w in re.split(r"\s+", text.strip()) if w]
    if len(words) >= 4:
        chunk = max(1, len(words) // 3)
        return [
            clip_words(" ".join(words[:chunk]), MAX_LABEL_WORDS),
            clip_words(" ".join(words[chunk : chunk * 2]), MAX_LABEL_WORDS),
            clip_words(" ".join(words[chunk * 2 :]), MAX_LABEL_WORDS),
        ]
    return [clip_words(text, MAX_LABEL_WORDS) or "Step 1", "Step 2"]


def _hook_title(text: str) -> str:
    lower = text.lower()
    if any(k in lower for k in ("welcome", "hello", "intro", "hey")):
        return "Welcome"
    words = re.findall(r"\S+", text)
    return clip_words(" ".join(words[:MAX_HOOK_WORDS]), MAX_HOOK_WORDS) or "Start"


def _keyword_from(text: str) -> str:
    words = [w.strip(".,!?") for w in text.split() if w.strip(".,!?")]
    if not words:
        return "Focus"
    return clip_words(max(words, key=len), 2)


def _infer_icon(text: str) -> str:
    lower = text.lower()
    rules = [
        (("demand", "popular", "growth", "market"), "bar_chart_up"),
        (("fast", "power", "speed", "rocket", "simple"), "rocket"),
        (("simple", "easy", "readable"), "code_simple"),
        (("everywhere", "versatile", "toolkit", "swiss"), "swiss_knife"),
        (("automation", "automate", "robot"), "robot_arm"),
        (("web", "website", "internet"), "globe"),
        (("game", "gaming"), "gamepad"),
        (("data", "science", "analytics", "chart"), "chart_lines"),
        (("community", "people", "crowd"), "crowd"),
        (("ai", "machine learning", "neural", "brain"), "brain_gear"),
        (("source", "code", ".py", "script"), "document_py"),
        (("compiler", "compile", "interpret", "process", "virtual"), "gear_process"),
        (("bytecode", "binary", "vm"), "cube_vm"),
        (("output", "result", "run"), "pac_output"),
    ]
    for keys, icon in rules:
        if any(k in lower for k in keys):
            return icon
    return "gear_process"


def _default_pipeline_stages(text: str) -> list[dict[str, Any]]:
    labels = _flowchart_labels(text)
    if len(labels) >= 3:
        return [
            {"label": labels[0], "icon_id": "document_py"},
            {
                "label": clip_words(labels[1], MAX_LABEL_WORDS) or "Process",
                "icon_id": "gear_process",
                "nested": labels[1:3] if len(labels) > 2 else ["Compile", "Run"],
            },
            {"label": labels[-1], "icon_id": "pac_output"},
        ]
    return [
        {"label": "Source", "icon_id": "document_py"},
        {"label": "Process", "icon_id": "gear_process", "nested": ["Compile", "Bytecode", "VM"]},
        {"label": "Output", "icon_id": "pac_output"},
    ]


def _default_mind_map_branches(text: str, *, single: bool = False) -> list[dict[str, Any]]:
    labels = _extract_bullet_candidates(text)
    if single or len(labels) <= 1:
        lab = clip_words(labels[0] if labels else _keyword_from(text), MAX_LABEL_WORDS)
        highlight = lab.split()[-1] if lab.split() else None
        return [{"label": lab or "Topic", "icon_id": _infer_icon(text), "highlight": highlight}]
    branches = []
    for lab in labels[:5]:
        cw = clip_words(lab, MAX_LABEL_WORDS)
        branches.append(
            {
                "label": cw,
                "icon_id": _infer_icon(lab),
                "highlight": cw.split()[-1] if cw.split() else None,
            }
        )
    return branches


def _pick_layout(text: str, index: int) -> str:
    lower = text.lower()
    if any(k in lower for k in ("why ", "reasons", "benefits", "advantages")) and (
        index == 0 or "python" in lower or "topic" in lower
    ):
        return "mind_map_radial"
    if any(k in lower for k in ("how it works", "how ", "works", "interpreter", "compiler", "bytecode", "pipeline")):
        return "pipeline_blackboard"
    if index == 0 or any(k in lower for k in ("welcome", "hello", "intro", "today")):
        return "center_title"
    if any(k in lower for k in (" vs ", "versus", "compare", "before", "after", "unlike")):
        return "compare_columns"
    if any(k in lower for k in ("step", "first", "then", "next", "process", "flow")):
        return "flowchart_vertical"
    if any(k in lower for k in ("ai", "community", "demand", "automation", "web", "gaming", "data")):
        return "mind_map_radial"
    if text.count(",") >= 2 or " and " in lower:
        return "center_bullets"
    if any(k in lower for k in ("because", "means", "concept", "idea", "model", "system")):
        return "visual_orbit"
    if len(text.split()) <= 6:
        return "kinetic_keywords"
    return "center_bullets"


def _default_background(index: int, layout: str) -> str:
    if layout in ("pipeline_blackboard", "mind_map_radial"):
        return "blackboard_clean"
    layout_bias = {
        "center_title": "corner_warm",
        "flowchart_vertical": "grid_fade",
        "flowchart_horizontal": "grid_fade",
        "compare_columns": "split_tone",
        "diagram_labeled": "orbit_glow",
        "visual_orbit": "orbit_glow",
        "kinetic_keywords": "edge_frame",
        "fade_transition": "blackboard_clean",
    }
    return layout_bias.get(layout, BACKGROUND_STYLE_IDS[index % len(BACKGROUND_STYLE_IDS)])


def _sanitize_icon(icon_id: str | None) -> str:
    iid = str(icon_id or "gear_process")
    return iid if iid in ICON_IDS else _infer_icon(iid)


def _sanitize_stages(stages: list[Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for st in stages[:4]:
        if not isinstance(st, dict):
            continue
        nested = st.get("nested") or []
        out.append(
            {
                "label": clip_words(str(st.get("label") or "Step"), MAX_LABEL_WORDS),
                "icon_id": _sanitize_icon(st.get("icon_id")),
                "nested": [clip_words(str(n), MAX_LABEL_WORDS) for n in nested[:3]] if nested else [],
            }
        )
    return out


def _sanitize_branches(branches: list[Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for br in branches[:5]:
        if not isinstance(br, dict):
            continue
        subs = br.get("sub_labels") or []
        out.append(
            {
                "label": clip_words(str(br.get("label") or "Point"), MAX_LABEL_WORDS),
                "icon_id": _sanitize_icon(br.get("icon_id")),
                "highlight": clip_words(str(br.get("highlight") or ""), 1) or None,
                "sub_labels": [clip_words(str(s), MAX_LABEL_WORDS) for s in subs[:4]] if subs else [],
            }
        )
    return out


def enforce_visual_page(page: dict[str, Any], index: int = 0) -> dict[str, Any]:
    """Clamp on-screen text to short labels; keep full sentence_text for reference only."""
    layout = page.get("layout") or "center_bullets"
    sentence = str(page.get("sentence_text") or "")

    page["sentence_text"] = sentence
    page.pop("display_text", None)

    bg = str(page.get("background_style") or "")
    if bg not in BACKGROUND_STYLE_IDS:
        page["background_style"] = _default_background(index, layout)

    if layout == "center_title":
        page["headline"] = clip_words(str(page.get("headline") or _hook_title(sentence)), MAX_HOOK_WORDS)
    elif layout == "center_bullets":
        raw = page.get("bullets") or _extract_bullet_candidates(sentence)
        page["bullets"] = [clip_words(str(b), MAX_BULLET_WORDS) for b in raw if str(b).strip()][:4]
        page.pop("headline", None)
    elif layout.startswith("flowchart"):
        raw = page.get("flow_labels") or _flowchart_labels(sentence)
        page["flow_labels"] = [clip_words(str(x), MAX_LABEL_WORDS) for x in raw][:4]
        page.pop("headline", None)
    elif layout == "compare_columns":
        parts = _extract_bullet_candidates(sentence)
        page["left_label"] = clip_words(str(page.get("left_label") or (parts[0] if parts else "Before")), MAX_LABEL_WORDS)
        page["right_label"] = clip_words(
            str(page.get("right_label") or (parts[1] if len(parts) > 1 else "After")), MAX_LABEL_WORDS
        )
        page.pop("headline", None)
    elif layout == "diagram_labeled":
        page["shape_label"] = clip_words(str(page.get("shape_label") or _keyword_from(sentence)), MAX_LABEL_WORDS)
        cap = str(page.get("caption") or "")
        page["caption"] = clip_words(cap, MAX_LABEL_WORDS) if cap.strip() else ""
    elif layout == "visual_orbit":
        page["hub_label"] = clip_words(str(page.get("hub_label") or _keyword_from(sentence)), MAX_LABEL_WORDS)
        raw = page.get("orbit_labels") or _flowchart_labels(sentence)[:3]
        page["orbit_labels"] = [clip_words(str(x), MAX_LABEL_WORDS) for x in raw][:4]
    elif layout == "kinetic_keywords":
        page["keyword"] = clip_words(str(page.get("keyword") or _keyword_from(sentence)), 2)
        page.pop("headline", None)
    elif layout == "pipeline_blackboard":
        raw = page.get("stages") or _default_pipeline_stages(sentence)
        page["stages"] = _sanitize_stages(raw if isinstance(raw, list) else [])
        page["background_style"] = "blackboard_clean"
        page.pop("headline", None)
    elif layout == "mind_map_radial":
        lower = sentence.lower()
        mode = str(page.get("mode") or ("full" if any(k in lower for k in ("why", "reasons", "benefits")) else "single"))
        page["mode"] = mode if mode in ("full", "single") else "single"
        page["hub_label"] = clip_words(str(page.get("hub_label") or "Python"), MAX_LABEL_WORDS)
        if "why" in lower and not page.get("hub_tag"):
            page["hub_tag"] = "WHY"
        elif page.get("hub_tag"):
            page["hub_tag"] = clip_words(str(page["hub_tag"]), 1)
        else:
            page.pop("hub_tag", None)
        raw = page.get("branches") or _default_mind_map_branches(sentence, single=page["mode"] == "single")
        page["branches"] = _sanitize_branches(raw if isinstance(raw, list) else [])
        page["background_style"] = "blackboard_clean"
        page.pop("headline", None)
    else:  # fade_transition
        hint = str(page.get("headline") or page.get("hint") or "")
        page["hint"] = clip_words(hint, 2) if hint.strip() else ""

    page["text_mode"] = "visual"
    return page


def default_page_for_sentence(sentence: dict[str, Any], index: int) -> dict[str, Any]:
    text = str(sentence.get("text") or "")
    sid = sentence.get("id") or f"s{index + 1:02d}"
    start = float(sentence.get("start", 0))
    end = float(sentence.get("end", start + 1))
    layout = _pick_layout(text, index)

    page: dict[str, Any] = {
        "id": f"p{index + 1:02d}",
        "sentence_id": sid,
        "start": start,
        "end": end,
        "intent": layout,
        "layout": layout,
        "sentence_text": text,
        "background_style": _default_background(index, layout),
        "exit": "FadeOut_all",
    }

    if layout == "center_title":
        page["headline"] = _hook_title(text)
    elif layout == "center_bullets":
        page["bullets"] = _extract_bullet_candidates(text)
    elif layout.startswith("flowchart"):
        page["flow_labels"] = _flowchart_labels(text)
    elif layout == "compare_columns":
        parts = _extract_bullet_candidates(text)
        page["left_label"] = parts[0] if parts else "Before"
        page["right_label"] = parts[1] if len(parts) > 1 else "After"
    elif layout == "diagram_labeled":
        page["shape_label"] = _keyword_from(text)
        page["caption"] = ""
    elif layout == "visual_orbit":
        page["hub_label"] = _keyword_from(text)
        page["orbit_labels"] = _flowchart_labels(text)[:3]
    elif layout == "kinetic_keywords":
        page["keyword"] = _keyword_from(text)
    elif layout == "pipeline_blackboard":
        page["stages"] = _default_pipeline_stages(text)
    elif layout == "mind_map_radial":
        lower = text.lower()
        page["mode"] = "full" if any(k in lower for k in ("why", "reasons", "benefits")) else "single"
        page["hub_label"] = clip_words("Python" if "python" in lower else _keyword_from(text), MAX_LABEL_WORDS)
        if "why" in lower:
            page["hub_tag"] = "WHY"
        page["branches"] = _default_mind_map_branches(text, single=page["mode"] == "single")
    else:
        page["hint"] = clip_words(text, 2)

    return enforce_visual_page(page, index)


def normalize_page(page: dict[str, Any], sentence: dict[str, Any], index: int) -> dict[str, Any]:
    base = default_page_for_sentence(sentence, index)
    layout = str(page.get("layout") or base["layout"])
    if layout not in LAYOUT_IDS:
        layout = base["layout"]
    merged = {**base, **page}
    merged["layout"] = layout
    merged["sentence_text"] = str(sentence.get("text") or merged.get("sentence_text") or "")
    merged["start"] = float(sentence.get("start", merged.get("start", base["start"])))
    merged["end"] = float(sentence.get("end", merged.get("end", base["end"])))
    merged["id"] = str(page.get("id") or base["id"])
    merged["sentence_id"] = str(page.get("sentence_id") or sentence.get("id") or base["sentence_id"])
    merged.setdefault("exit", "FadeOut_all")
    return enforce_visual_page(merged, index)
