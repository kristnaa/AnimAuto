"""Load manim-video skill files for OpenAI system prompts."""

from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

MANIM_ROOT = Path(__file__).resolve().parents[3]
SKILL_DIR = MANIM_ROOT / ".cursor" / "skills" / "manim-video"
STUDIO_TEMPLATE = MANIM_ROOT / "platform" / "assets" / "beat-script-template.md"
VISUAL_CATALOG = MANIM_ROOT / "assets" / "visual_catalog.json"


def _read(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text()


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        return re.sub(r"^---\n.*?\n---\n", "", text, count=1, flags=re.S)
    return text


@lru_cache(maxsize=1)
def load_visual_concepts() -> tuple[str, ...]:
    if not VISUAL_CATALOG.exists():
        return (
            "python",
            "question",
            "terminal",
            "computer",
            "code",
            "ai",
            "frustration",
            "failure",
            "success",
            "sparkles",
        )
    catalog = json.loads(VISUAL_CATALOG.read_text())
    return tuple(sorted(catalog.keys()))


@lru_cache(maxsize=1)
def load_skill_bundle() -> str:
    """Concatenate the authoring docs we train Cursor agents on."""
    parts: list[str] = []

    skill_md = _strip_frontmatter(_read(SKILL_DIR / "SKILL.md"))
    if skill_md.strip():
        parts.append("# Manim Video Skill (overview)\n\n" + skill_md.strip())

    studio = _read(STUDIO_TEMPLATE).strip()
    if studio:
        parts.append("# Beat Script Template (Studio source of truth)\n\n" + studio)

    conventions = _read(SKILL_DIR / "conventions.md").strip()
    if conventions:
        parts.append("# Project Conventions\n\n" + conventions)

    text_to_manim = _read(SKILL_DIR / "text-to-manim.md").strip()
    if text_to_manim:
        parts.append("# Text → Manim Pipeline\n\n" + text_to_manim)

    concepts = ", ".join(load_visual_concepts())
    parts.append(
        "# Visual concept IDs (use in visuals.primary/swap.concept)\n\n"
        + concepts
        + "\n\nPick semantically from narration. For jokes use swap + emphasis trigger."
    )

    return "\n\n---\n\n".join(parts)


CHAT_OUTPUT_SCHEMA = """Return ONLY valid JSON (no markdown fences):
{
  "message": "Brief friendly reply",
  "project": {
    "name": "Episode title",
    "style_pack": "course_clean" | "playful",
    "use_camera": true,
    "beats": [
      {
        "label": "Short yellow heading (one line only)",
        "type": "statement" | "question" | "joke punchline" | "explain" | "recap" | "code_demo" | "list" | "compare",
        "layout": "card_right_icon_left" | "card_left_icon_right" | "text_right_icon_left" | "text_left_icon_right" | "code_full_card" | "dual_card",
        "use_camera": true,
        "card_lines": ["for statement/joke/explain — NOT for code_demo"],
        "punchline_line": "optional joke last line",
        "bg_lines": ["for text_right_icon_left questions"],
        "list_lines": ["checklist item one", "item two"],
        "left_lines": ["compare left card"],
        "right_lines": ["compare right card"],
        "code_language": "python",
        "code_lines": ["def add(a, b):", "    return a + b", "print(add(2, 3))"],
        "code_result": "success" | "error",
        "code_output": "5",
        "code_error_line": 2,
        "code_error_message": "NameError: ...",
        "card_width": 5.6,
        "card_height": 5.0,
        "hold": 1.5,
        "visuals": {
          "primary": {"concept": "python", "role": "subject", "description": "...", "color": "WHITE"}
        },
        "emphasis": [{"word": "word", "color": "RED", "animation": "wiggle"}],
        "camera": [
          {"hook": "after_run|after_line_1|after_line_2|after_code|after_output|after_icon|punchline|exit", "action": "cam_focus_card|cam_focus_left|cam_focus_right|cam_restore", "run_time": 0.9}
        ]
      }
    ]
  }
}

For code_demo beats you MUST set:
- type: "code_demo"
- layout: "code_full_card"
- code_lines: array of source lines (strings with proper Python syntax)
- code_result: "success" or "error"
- code_output: expected stdout on success
- code_error_line + code_error_message: only when code_result is "error"
- Do NOT use card_lines for code — only code_lines
- visuals optional (empty {} is fine for code_demo)"""


SCRIPT_OUTPUT_SCHEMA = """Return ONLY valid JSON (no markdown fences). Prefer script_markdown:

{
  "name": "Episode title",
  "theme_id": "builtin_orange",
  "style_pack": "course_clean",
  "use_camera": true,
  "script_markdown": "### BEAT 1 — slug\\nTYPE: statement\\n..."
}

script_markdown MUST be a complete beat script using:
- Episode meta: CAMERA, THEME, STYLE_PACK, NAME at top
- ### BEAT N — slug headers
- TYPE, LAYOUT, CAMERA, DURATION per beat
- ─── TIMELINE ─── table (anim_type, anim_grow_card, cam_* hooks)
- ─── CONTENT ─── with LABEL, TEXT (card) or TEXT (white, on BG)
- ─── CODE ─── for code_demo beats: language, result (success|error), output, error_line (1-based, for error beats), error/error_message (traceback text), lines (indented code). No real execution — LLM or user authors output and which line fails.
- LIST (card, checks): for checklist beats
- TEXT (left card) / TEXT (right card): for compare beats
- ─── ICONS ─── with icon_id: plain English description | color: WHITE|#hex [| scale: 1.2]
- GPT resolves descriptions to Iconify refs at Generate time — do NOT require prefix:name in scripts unless user provides them.
- ─── CARD ─── SIDE and SIZE when using a card
- ─── EMPHASIS ─── word | color | animation
- ─── CAMERA ─── cam_*: hook lines when CAMERA is moving
- HOLD and EXIT per beat

Alternative (only if user pasted JSON): return the same fields with a "beats" array instead of script_markdown. visuals must be objects, not arrays."""


def build_chat_system_prompt() -> str:
    return f"""You are Manimations Studio — expert beat-script author for Manim CE course videos.

You turn narration into structured beats that render through our beat interpreter.
Follow the authoring knowledge below exactly — same rules as our Cursor manim-video skill.

## Authoring knowledge

{load_skill_bundle()}

## Output format

{CHAT_OUTPUT_SCHEMA}

## Critical rules
- Split narration into ~1-idea beats (~5–8s each). Use CLEAR storytelling when structure is unclear.
- **When user asks to write/run/show code, use a function, code demo, or Python snippet → type MUST be code_demo, layout code_full_card, with code_lines + code_output + code_result. Never put code in card_lines.**
- card_right_icon_left: statements with white card on right, icon/visual on left.
- text_right_icon_left: questions — no card, white text on orange right half.
- joke punchline: card_lines = setup lines; punchline_line = final line; swap visual + RED wiggle emphasis on trigger word.
- code_demo: dark code window, run button, line-by-line highlight, then output panel. Author realistic code_output (e.g. add(2,3) → "5").
- list: list_lines + optional icon; cam_focus_card hooks.
- compare: dual_card with left_lines and right_lines.
- use_camera: true + camera[] when episode uses moving camera; always cam_restore on hook "exit".
- visuals.primary and visuals.swap must be objects — never arrays. code_demo may omit visuals.
- emphasis entries must be objects {{"word", "color", "animation"}}.
- label must be ONE short line (never include LIST/CODE sections in label).
- If user asks to tweak, change only what they asked; preserve other beats.
- Do NOT include theme_id in project — visual theme is chosen by the user in the UI, not via chat.
"""


def build_script_system_prompt() -> str:
    return f"""You are Manimations Studio beat script compiler.

Convert the user's input (narration, rough notes, partial script, or JSON) into a **complete, render-ready beat script**.
Match the same quality as our hand-authored Episode beats.

## Authoring knowledge

{load_skill_bundle()}

## Output format

{SCRIPT_OUTPUT_SCHEMA}

## Critical rules
- Output script_markdown unless input is already valid JSON with a beats array.
- Every beat needs TIMELINE, CONTENT, ICONS, EMPHASIS (when needed), CAMERA hooks (if moving), HOLD.
- ICONS: describe what you want in plain English + color. Example: `icon_python: Python logo | color: #3776AB`
- Studio uses GPT to pick Iconify icons automatically when you Generate.
- Joke beats: fade out setup lines + primary icon, swap icon, type punchline centered, wiggle emphasis word.
- Questions: LAYOUT text_right_icon_left, bg_lines not card_lines.
- Do not omit cam_restore: exit on camera beats.
"""


def _as_dict(value: Any, default: dict | None = None) -> dict:
    if isinstance(value, dict):
        return value
    if isinstance(value, list):
        for item in value:
            if isinstance(item, dict):
                return item
        return default or {}
    return default or {}


def normalize_beat(beat: dict) -> dict:
    """Coerce GPT beat JSON into shapes the resolver/interpreter expect."""
    out = dict(beat)
    visuals = beat.get("visuals")
    if visuals is not None:
        if isinstance(visuals, list):
            normalized: dict[str, Any] = {}
            if visuals:
                normalized["primary"] = _as_dict(visuals[0])
            if len(visuals) > 1:
                normalized["swap"] = _as_dict(visuals[1])
            out["visuals"] = normalized
        elif isinstance(visuals, dict):
            primary = _as_dict(visuals.get("primary") or visuals.get("left"))
            swap = _as_dict(visuals.get("swap") or visuals.get("left_swap"), default={})
            out["visuals"] = {"primary": primary}
            if swap:
                out["visuals"]["swap"] = swap

    emphasis = beat.get("emphasis")
    if isinstance(emphasis, list):
        fixed: list[dict] = []
        for item in emphasis:
            if isinstance(item, dict):
                fixed.append(item)
            elif isinstance(item, str):
                fixed.append({"word": item, "color": "YELLOW", "animation": "indicate"})
        out["emphasis"] = fixed

    camera = beat.get("camera")
    if isinstance(camera, list):
        out["camera"] = [_as_dict(step) for step in camera if _as_dict(step)]

    # Coerce code_lines from a single string if model returned wrong shape
    code_lines = out.get("code_lines")
    try:
        from beat_helpers import normalize_code_lines  # noqa: WPS433
    except ImportError:
        def normalize_code_lines(lines):  # type: ignore[misc]
            if not lines:
                return []
            return [str(ln).expandtabs(4).rstrip() for ln in lines]

    if isinstance(code_lines, str):
        out["code_lines"] = normalize_code_lines(code_lines.splitlines())
    elif isinstance(code_lines, list):
        out["code_lines"] = normalize_code_lines(code_lines)

    if out.get("type") == "code_demo" or out.get("code_lines"):
        try:
            from beat_helpers import sanitize_code_demo_beat  # noqa: WPS433

            out = sanitize_code_demo_beat(out)
        except ImportError:
            pass

    try:
        from beat_types import apply_type_defaults, normalize_beat_type  # noqa: WPS433

        out["type"] = normalize_beat_type(out.get("type"))
        if out.get("code_lines") and out["type"] not in ("code_demo",):
            out["type"] = "code_demo"
        out = apply_type_defaults(out)
    except ImportError:
        pass

    return out


def normalize_project(data: dict) -> dict:
    out = dict(data)
    if "beats" in out and isinstance(out["beats"], list):
        out["beats"] = [normalize_beat(b) for b in out["beats"] if isinstance(b, dict)]
    return out
