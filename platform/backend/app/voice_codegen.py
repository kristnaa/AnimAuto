"""Compile director storyboard pages into VoiceMotionScene Python."""

from __future__ import annotations

import json
from typing import Any

from app.voice_motion import SCENE_CLASS, sanitize_motion_scene

FADE_TIME = 0.35


def _esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _page_timing_wrapper(start: float, end: float, bg_style: str, body_lines: list[str]) -> list[str]:
    return [
        f"        target_start = {start:.3f}",
        f"        target_end = {end:.3f}",
        f"        gap = max(0, target_start - self.time)",
        f"        if gap > 0.01:",
        f"            self.wait(gap)",
        f'        decor = page_background("{_esc(bg_style)}")',
        f"        page_mobs = [decor]",
        f"        self.play(FadeIn(decor), run_time=0.2)",
        *body_lines,
        f"        fade_t = {FADE_TIME:.2f}",
        f"        remain = max(0.05, target_end - fade_t - self.time)",
        f"        self.wait(remain)",
        f"        fade_out_page(self, *page_mobs, run_time=fade_t)",
        f"        return page_mobs",
    ]


def compile_page_method(page: dict[str, Any], index: int) -> tuple[str, str]:
    name = f"_page_{index:02d}"
    layout = page.get("layout") or "center_bullets"
    start = float(page.get("start", 0))
    end = float(page.get("end", start + 1))
    bg = str(page.get("background_style") or "radial_blue")

    body: list[str] = []

    if layout == "center_title":
        hook = str(page.get("headline") or "Start")
        body = [
            f'        group = layout_center_title("{_esc(hook)}")',
            "        page_mobs.extend([group])",
            "        self.play(FadeIn(group[0]), run_time=0.25)",
            "        type_with_cursor(self, group[1], time_per_char=0.06)",
            "        self.play(Create(group[2]), FadeIn(group[3]), run_time=0.35)",
        ]
    elif layout == "center_bullets":
        bullets = page.get("bullets") or ["Point"]
        bl_json = json.dumps([str(b) for b in bullets[:4]])
        body = [
            f"        bullets = {bl_json}",
            "        group = layout_center_bullets(bullets)",
            "        page_mobs.extend([group])",
            "        self.play(FadeIn(group[0]), run_time=0.25)",
            "        self.play(LaggedStart(*[FadeIn(row) for row in group[1]], lag_ratio=0.2), run_time=0.75)",
        ]
    elif layout == "flowchart_vertical":
        labels = page.get("flow_labels") or ["Start", "End"]
        lb_json = json.dumps([str(x) for x in labels[:4]])
        body = [
            f"        labels = {lb_json}",
            "        chart = layout_flowchart_vertical(labels)",
            "        page_mobs.extend([chart])",
            "        self.play(LaggedStart(*[Create(m) for m in chart], lag_ratio=0.18), run_time=1.0)",
        ]
    elif layout == "flowchart_horizontal":
        labels = page.get("flow_labels") or ["A", "B"]
        lb_json = json.dumps([str(x) for x in labels[:4]])
        body = [
            f"        labels = {lb_json}",
            "        chart = layout_flowchart_horizontal(labels)",
            "        page_mobs.extend([chart])",
            "        self.play(LaggedStart(*[FadeIn(m) for m in chart], lag_ratio=0.15), run_time=0.9)",
        ]
    elif layout == "compare_columns":
        left = str(page.get("left_label") or "Before")
        right = str(page.get("right_label") or "After")
        body = [
            f'        group = layout_compare_columns("{_esc(left)}", "{_esc(right)}")',
            "        page_mobs.extend([group])",
            "        self.play(FadeIn(group[0]), FadeIn(group[1]), run_time=0.35)",
            "        self.play(GrowArrow(group[2]), run_time=0.35)",
            "        self.play(FadeIn(group[3]), run_time=0.35)",
        ]
    elif layout == "diagram_labeled":
        shape = str(page.get("shape_label") or "Core")
        cap = str(page.get("caption") or "")
        body = [
            f'        group = layout_diagram_labeled("{_esc(shape)}", "{_esc(cap)}")',
            "        page_mobs.extend([group])",
            "        self.play(FadeIn(group[0]), FadeIn(group[1]), run_time=0.3)",
            "        self.play(Create(group[2]), FadeIn(group[3]), run_time=0.35)",
            "        self.play(FadeIn(group[4]), run_time=0.3)",
            "        if len(group) > 5:",
            "            self.play(FadeIn(group[5]), run_time=0.25)",
        ]
    elif layout == "visual_orbit":
        hub = str(page.get("hub_label") or "Core")
        orbit = page.get("orbit_labels") or ["A", "B"]
        ob_json = json.dumps([str(x) for x in orbit[:4]])
        body = [
            f'        group = layout_visual_orbit("{_esc(hub)}", {ob_json})',
            "        page_mobs.extend([group])",
            "        self.play(Create(group[0]), FadeIn(group[1]), run_time=0.35)",
            "        self.play(FadeIn(group[2]), run_time=0.25)",
            "        self.play(LaggedStart(*[FadeIn(n) for n in group[3:]], lag_ratio=0.15), run_time=0.75)",
        ]
    elif layout == "kinetic_keywords":
        kw = str(page.get("keyword") or "Focus")
        body = [
            f'        mob = layout_kinetic_keyword("{_esc(kw)}")',
            "        page_mobs.append(mob)",
            "        self.play(FadeIn(mob[0]), run_time=0.25)",
            "        self.play(FadeIn(mob[1]), FadeIn(mob[2], scale=0.7), run_time=0.4)",
            "        self.play(Indicate(mob[2], color=YELLOW), run_time=0.35)",
        ]
    elif layout == "pipeline_blackboard":
        stages = page.get("stages") or []
        st_json = json.dumps(stages)
        bg = "blackboard_clean"
        body = [
            f"        stages = {st_json}",
            "        chart = layout_pipeline_blackboard(stages)",
            "        page_mobs.extend([chart])",
            "        draw_sketchy(self, chart, run_time=1.2)",
        ]
    elif layout == "mind_map_radial":
        hub = str(page.get("hub_label") or "Python")
        branches = page.get("branches") or []
        br_json = json.dumps(branches)
        mode = str(page.get("mode") or "single")
        tag = page.get("hub_tag")
        bg = "blackboard_clean"
        if tag:
            body = [
                f'        chart = layout_mind_map_radial("{_esc(hub)}", {br_json}, hub_tag="{_esc(str(tag))}", mode="{_esc(mode)}")',
                "        page_mobs.extend([chart])",
                "        draw_sketchy(self, chart, run_time=1.2)",
            ]
        else:
            body = [
                f'        chart = layout_mind_map_radial("{_esc(hub)}", {br_json}, mode="{_esc(mode)}")',
                "        page_mobs.extend([chart])",
                "        draw_sketchy(self, chart, run_time=1.2)",
            ]
    else:  # fade_transition
        hint = str(page.get("hint") or page.get("headline") or "")
        body = [
            f'        mob = layout_fade_transition("{_esc(hint)}")',
            "        page_mobs.append(mob)",
            "        self.play(FadeIn(mob), GrowArrow(mob[0]), run_time=0.45)",
            "        self.play(Indicate(mob[1], scale_factor=1.2), run_time=0.35)",
        ]

    lines = [
        f"    def {name}(self):",
        f'        # page {index + 1}: {start:.1f}–{end:.1f}s | {layout} | bg={bg}',
        *_page_timing_wrapper(start, end, bg, body),
    ]
    return name, "\n".join(lines)


def compile_scene_from_plan(director_plan: dict[str, Any]) -> str:
    pages = director_plan.get("pages") or []
    if not pages:
        raise ValueError("Director plan has no pages")

    methods: list[str] = []
    calls: list[str] = []
    for i, page in enumerate(pages):
        method_name, source = compile_page_method(page, i)
        methods.append(source)
        calls.append(f"        self.{method_name}()")

    methods_block = "\n\n".join(methods)
    code = f'''"""Voice motion scene — generated by Manimations Studio director."""

from manim import *
from blackboard_elements import draw_sketchy, layout_mind_map_radial, layout_pipeline_blackboard
from voice_motion_helpers import (
    fade_out_page,
    layout_center_bullets,
    layout_center_title,
    layout_compare_columns,
    layout_diagram_labeled,
    layout_fade_transition,
    layout_flowchart_horizontal,
    layout_flowchart_vertical,
    layout_kinetic_keyword,
    layout_visual_orbit,
    page_background,
    type_with_cursor,
)


class {SCENE_CLASS}(Scene):
{methods_block}

    def construct(self):
        self.camera.background_color = BLACK
{chr(10).join(calls)}
'''
    return sanitize_motion_scene(code)


def compile_and_validate(director_plan: dict[str, Any]) -> str:
    return compile_scene_from_plan(director_plan)
