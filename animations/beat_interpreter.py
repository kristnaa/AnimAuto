"""Interpret JSON beat specs into Manim animations."""

from __future__ import annotations

import sys
from pathlib import Path

from manim import *

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "animations"))

from beat_helpers import BeatScene, MovingBeatScene  # noqa: E402
from icon_grid import layout_icons_in_panel  # noqa: E402
from icon_triggers import line_has_trigger, resolve_icon_reveal_mode  # noqa: E402
from visual_library import load_visual  # noqa: E402
from visual_resolver import resolve_beat_visuals  # noqa: E402

MANIM_ROOT = ROOT
BG_PATH = MANIM_ROOT / "background" / "orange_theme_BG.png"


def _apply_bg(scene):
    bg = ImageMobject(str(BG_PATH))
    bg.scale_to_fit_width(config.frame_width * (1.25 if isinstance(scene, MovingBeatScene) else 1.0))
    bg.move_to(ORIGIN)
    scene.add(bg)


def _normalize_text(text: str) -> str:
    return text.replace(" ", "")


def _word_in_text(text_mob, word: str) -> bool:
    text = text_mob.text if hasattr(text_mob, "text") else str(text_mob)
    return _normalize_text(word) in _normalize_text(text) or word in text


def _find_word(mob, word: str):
    text = mob.text
    compact_word = _normalize_text(word)
    start = text.find(compact_word)
    if start < 0:
        return mob
    return mob[start : start + len(compact_word)]


def _apply_word_color(text_mob, word: str, color) -> None:
    """Color an emphasized word (uses submobject slice — visible unlike set_color_by_t2c)."""
    if not _word_in_text(text_mob, word):
        return
    _find_word(text_mob, word).set_color(color)


def _camera_step(beat: dict, hook: str) -> dict | None:
    for step in beat.get("camera") or []:
        if step.get("hook") == hook:
            return step
    return None


def _run_camera(scene, beat: dict, hook: str, *, label, card=None, card_side="right", run_time=None):
    if not isinstance(scene, MovingBeatScene):
        return
    step = _camera_step(beat, hook)
    if not step:
        return
    action = step.get("action", "")
    rt = run_time or float(step.get("run_time", 0.9))
    if action == "cam_focus_left":
        scene.cam_focus_left(label, run_time=rt)
    elif action == "cam_focus_right":
        scene.cam_focus_right(label, run_time=rt)
    elif action == "cam_focus_card" and card is not None:
        scene.cam_focus_card(card, run_time=rt)
    elif action == "cam_restore":
        scene.cam_restore(run_time=rt)
    elif action == "cam_restore_fast":
        scene.cam_restore(run_time=0.5)


def _icon_side(layout: str) -> str:
    if "icon_right" in layout:
        return "right"
    if "icon_left" in layout:
        return "left"
    if "card_left" in layout:
        return "right"
    if "card_right" in layout:
        return "left"
    if "text_left" in layout:
        return "right"
    if "text_right" in layout:
        return "left"
    return "left"


def _card_side(layout: str, beat: dict) -> str:
    if beat.get("card_side"):
        return beat["card_side"]
    if "card_left" in layout:
        return "left"
    if "card_right" in layout:
        return "right"
    return "right"


def _bg_text_side(layout: str) -> str:
    if "text_right" in layout:
        return "right"
    if "text_left" in layout:
        return "left"
    return "right"


def _load_icon_panel(scene, beat: dict, label, icon_side: str, *, hide_for_sync: bool = False):
    """Load primary or multi-icon panel using invisible grid cells."""
    visuals = beat.get("visuals_resolved") or {}
    panel = scene.icon_panel_bounds(icon_side, label)
    grid_mode = beat.get("icon_grid")

    stack_specs = visuals.get("stack")
    if isinstance(stack_specs, list) and stack_specs:
        specs = stack_specs[:4]
        mobs = [load_visual(scene, spec) for spec in specs]
        group = layout_icons_in_panel(mobs, panel, mode=grid_mode)
        if hide_for_sync:
            for mob in mobs:
                mob.set_opacity(0)
            scene.add(*mobs)
            return group, mobs, specs
        return group, mobs, specs

    primary_spec = visuals.get("primary")
    swap_spec = visuals.get("swap")
    primary_mob = load_visual(scene, primary_spec) if primary_spec else None
    swap_mob = load_visual(scene, swap_spec) if swap_spec else None

    if primary_mob and swap_mob:
        layout_icons_in_panel([primary_mob], panel, mode="single")
        return primary_mob, [primary_mob, swap_mob], []

    if primary_mob:
        layout_icons_in_panel([primary_mob], panel, mode="single")
        return primary_mob, [primary_mob], []

    return None, [], []


def _build_trigger_map(stack_specs: list[dict], stack_mobs: list) -> tuple[dict[str, Mobject], list]:
    """Map trigger word → icon; return icons without triggers for batch reveal."""
    triggered: dict[str, Mobject] = {}
    untriggered: list = []
    for spec, mob in zip(stack_specs, stack_mobs):
        word = (spec.get("trigger") or "").strip().lower()
        if word:
            triggered[word] = mob
        else:
            untriggered.append(mob)
    return triggered, untriggered


def _ensure_full_frame_for_word_sync(scene, stack_count: int, reveal_mode: str) -> None:
    """Zoom out to full frame so card + icon grid are visible during word sync."""
    if reveal_mode != "on_word" or stack_count < 3:
        return
    if isinstance(scene, MovingBeatScene):
        scene.cam_restore(run_time=0.55)


def _cam_focus_icon(scene, label, icon_side: str, *, run_time: float = 0.9) -> None:
    if not isinstance(scene, MovingBeatScene):
        return
    if icon_side == "right":
        scene.cam_focus_right(label, run_time=run_time)
    else:
        scene.cam_focus_left(label, run_time=run_time)


def _beat_uses_camera(beat: dict, project_default: bool) -> bool:
    if "use_camera" in beat:
        return bool(beat["use_camera"])
    return project_default


def _begin_beat(scene: BeatScene, use_camera: bool) -> None:
    """Ensure each beat starts from a clean frame and default camera."""
    scene.sweep_foreground(run_time=0)
    if isinstance(scene, MovingBeatScene) and use_camera:
        frame = scene.camera.frame
        if (
            abs(frame.width - config.frame_width) > 0.05
            or abs(frame.height - config.frame_height) > 0.05
            or np.linalg.norm(frame.get_center()[:2]) > 0.05
        ):
            scene.cam_restore(run_time=0.35)


def run_beat_from_spec(scene: BeatScene, beat: dict, *, use_camera: bool = False) -> None:
    beat = resolve_beat_visuals(dict(beat))
    _begin_beat(scene, use_camera)
    layout = beat.get("layout", "card_right_icon_left")
    label_text = beat.get("label", "Beat")
    label = scene.top_label(label_text)
    cam_on = _beat_uses_camera(beat, use_camera)
    has_camera_spec = bool(beat.get("camera"))

    card = None
    card_lines_mobs = []
    bg_lines_mobs = None
    punchline_mob = None

    has_card = "card" in layout or beat.get("card_lines")
    card_side = _card_side(layout, beat)
    icon_side = _icon_side(layout)

    # Card layouts: treat bg_lines as card content when card_lines missing.
    card_lines = beat.get("card_lines")
    if has_card and not card_lines and beat.get("bg_lines"):
        card_lines = beat["bg_lines"]

    if has_card and card_lines:
        card = scene.empty_card(
            side=card_side,
            width=float(beat.get("card_width", 5.6)),
            height=float(beat.get("card_height", 5.0)),
            label=label,
        )
        all_lines = list(card_lines)
        if beat.get("punchline_line") and beat["punchline_line"] not in all_lines:
            all_lines.append(beat["punchline_line"])

        lines_group = scene.card_lines(*all_lines, max_width=card.width - 2 * 0.45)
        scene.place_card_content(lines_group, card)

        punchline = beat.get("punchline_line")
        if punchline and punchline in all_lines:
            pi = all_lines.index(punchline)
            card_lines_mobs = [lines_group[i] for i in range(len(all_lines)) if i != pi]
            punchline_mob = lines_group[pi]
        else:
            card_lines_mobs = list(lines_group)
            punchline_mob = None
    elif beat.get("bg_lines"):
        bg_lines_mobs = scene.bg_lines(*beat["bg_lines"])
        bg_lines_mobs.move_to(scene.panel_anchor(_bg_text_side(layout), label))

    stack_specs = (beat.get("visuals_resolved") or {}).get("stack") or []
    icon_reveal = resolve_icon_reveal_mode(beat, stack_specs)
    use_word_sync = icon_reveal == "on_word" and bool(stack_specs)
    has_icon_triggers = any(s.get("trigger") for s in stack_specs)

    icon_panel, icon_mobs, _ = _load_icon_panel(
        scene,
        beat,
        label,
        icon_side,
        hide_for_sync=use_word_sync and has_icon_triggers,
    )
    primary_mob = icon_mobs[0] if len(icon_mobs) == 1 else icon_panel
    swap_mob = icon_mobs[1] if len(icon_mobs) > 1 and not isinstance(icon_panel, VGroup) else None
    stack_mobs = icon_mobs if isinstance(icon_panel, VGroup) else []

    trigger_map: dict[str, Mobject] = {}
    untriggered_icons: list = []
    revealed_words: set[str] = set()
    if use_word_sync and has_icon_triggers and stack_mobs:
        trigger_map, untriggered_icons = _build_trigger_map(stack_specs, stack_mobs)
        _ensure_full_frame_for_word_sync(scene, len(stack_specs), icon_reveal)

    batch_icon_reveal = icon_panel and not (use_word_sync and has_icon_triggers)

    scene.type_text(label, time_per_char=0.045, cursor_color=YELLOW)

    primary_shown = False
    if batch_icon_reveal and bg_lines_mobs is not None:
        scene.play(FadeIn(icon_panel), run_time=0.4)
        primary_shown = True
        if has_camera_spec:
            _run_camera(scene, beat, "after_icon", label=label, card=card, card_side=card_side)
        elif cam_on:
            _cam_focus_icon(scene, label, icon_side)
        scene.wait(0.4)

    if card:
        scene.play(GrowFromCenter(card), run_time=0.4)

    trigger_words = list(trigger_map.keys())
    typed: list = []
    if card_lines_mobs:
        for i, line in enumerate(card_lines_mobs):
            if trigger_map and line_has_trigger(line.text, trigger_words):
                revealed_words = scene.type_line_with_icon_triggers(
                    line,
                    trigger_map,
                    time_per_char=0.05,
                    cursor_color=YELLOW,
                    revealed=revealed_words,
                )
            else:
                scene.type_text(line, time_per_char=0.05)
            typed.append(line)
            for em in beat.get("emphasis") or []:
                w = em.get("word")
                if w and _word_in_text(line, w):
                    part = _find_word(line, w)
                    if em.get("color") == "RED":
                        _apply_word_color(line, w, RED)
                    if em.get("animation") == "wiggle":
                        scene.play(Wiggle(part), run_time=0.6)
                    elif em.get("animation") == "indicate":
                        scene.play(Indicate(part, color=YELLOW), run_time=0.55)
            hook = f"after_line_{i + 1}"
            if has_camera_spec:
                _run_camera(scene, beat, hook, label=label, card=card, card_side=card_side)
            elif cam_on and i == 1 and isinstance(scene, MovingBeatScene):
                fn = scene.cam_focus_right if card_side == "right" else scene.cam_focus_left
                fn(label, run_time=0.9)

    if bg_lines_mobs is not None:
        for i, line in enumerate(bg_lines_mobs):
            if trigger_map and line_has_trigger(line.text, trigger_words):
                revealed_words = scene.type_line_with_icon_triggers(
                    line,
                    trigger_map,
                    time_per_char=0.05,
                    cursor_color=WHITE,
                    revealed=revealed_words,
                )
            else:
                scene.type_text(line, time_per_char=0.05)
            hook = f"after_line_{i + 1}"
            if has_camera_spec:
                _run_camera(scene, beat, hook, label=label, card=card, card_side=card_side)
            elif cam_on and i == 0 and isinstance(scene, MovingBeatScene):
                scene.cam_focus_right(label, run_time=0.9)
            if beat.get("emphasis"):
                for em in beat["emphasis"]:
                    w = em.get("word")
                    if w and _word_in_text(line, w):
                        if em.get("color") == "RED":
                            _apply_word_color(line, w, RED)
                        color = YELLOW if em.get("color") != "RED" else RED
                        anim = Indicate(_find_word(line, w), color=color)
                        scene.play(anim, run_time=0.55)

    if batch_icon_reveal and not primary_shown:
        scene.play(FadeIn(icon_panel), run_time=0.4)
        if has_camera_spec:
            _run_camera(scene, beat, "after_icon", label=label, card=card, card_side=card_side)
        elif cam_on:
            _cam_focus_icon(scene, label, icon_side)
    elif use_word_sync and has_icon_triggers:
        still_hidden = [
            m
            for m in (*untriggered_icons, *trigger_map.values())
            if (m.get_opacity() if m.get_opacity() is not None else 1.0) < 0.5
        ]
        if still_hidden:
            for mob in still_hidden:
                mob.set_opacity(1)
            scene.play(*[FadeIn(m, scale=1.02) for m in still_hidden], run_time=0.4)
        if has_camera_spec:
            _run_camera(scene, beat, "after_icon", label=label, card=card, card_side=card_side)
        elif cam_on and len(stack_specs) >= 3 and isinstance(scene, MovingBeatScene):
            scene.cam_restore(run_time=0.5)

    # Punchline sequence
    if punchline_mob and card:
        if typed:
            scene.play(*[FadeOut(m) for m in typed], run_time=0.4)
        scene.place_card_line(punchline_mob, card, centered=True)
        if primary_mob and swap_mob:
            scene.play(FadeOut(primary_mob), FadeIn(swap_mob), run_time=0.4)
        elif stack_mobs and swap_mob:
            scene.play(FadeOut(icon_panel), FadeIn(swap_mob), run_time=0.4)
        if has_camera_spec:
            _run_camera(scene, beat, "punchline", label=label, card=card, card_side=card_side)
        elif cam_on and isinstance(scene, MovingBeatScene):
            scene.cam_focus_card(card, run_time=0.9)
        scene.type_text(punchline_mob, time_per_char=0.05)
        for em in beat.get("emphasis") or []:
            word = em.get("word")
            if word and _word_in_text(punchline_mob, word):
                part = _find_word(punchline_mob, word)
                if em.get("color") == "RED":
                    _apply_word_color(punchline_mob, word, RED)
                if em.get("animation") == "wiggle":
                    extras = [Wiggle(part)]
                    if swap_mob:
                        extras.append(Wiggle(swap_mob))
                    scene.play(*extras, run_time=0.6)
                elif em.get("animation") == "indicate":
                    scene.play(Indicate(part, color=YELLOW), run_time=0.55)
    elif punchline_mob:
        scene.type_text(punchline_mob, time_per_char=0.05)

    scene.wait(float(beat.get("hold", 1.2)))

    if has_camera_spec:
        _run_camera(scene, beat, "exit", label=label, card=card, card_side=card_side)
    elif cam_on and isinstance(scene, MovingBeatScene):
        scene.cam_restore(run_time=0.7)

    # One unified fade: card, card text, icons, and detached emphasis slices together.
    scene.sweep_foreground(run_time=0.55)


def make_scene_class(project: dict, use_camera: bool = False):
    """Dynamically build a Manim Scene class from a project dict."""

    class GeneratedScene(MovingBeatScene if use_camera else BeatScene):
        def construct(self):
            _apply_bg(self)
            beats = project.get("beats", [])
            for i, beat in enumerate(beats):
                run_beat_from_spec(self, beat, use_camera=use_camera)
                if i < len(beats) - 1:
                    self.beat_transition()

    GeneratedScene.__name__ = project.get("scene_class", "GeneratedScene")
    return GeneratedScene
