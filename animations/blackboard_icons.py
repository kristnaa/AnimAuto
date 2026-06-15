"""Reusable blackboard icon catalog — SVG-first with procedural fallback."""

from __future__ import annotations

from manim import *

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

# Iconify refs — colorful icons keep their palette; mono icons tint to WHITE.
ICON_SVG_REFS: dict[str, str] = {
    "bar_chart_up": "lucide:bar-chart",
    "rocket": "lucide:rocket",
    "code_simple": "lucide:square-code",
    "swiss_knife": "tabler:tool",
    "robot_arm": "mdi:robot-industrial",
    "globe": "lucide:globe",
    "gamepad": "mdi:gamepad-variant",
    "chart_lines": "lucide:trending-up",
    "crowd": "mdi:account-group",
    "brain_gear": "lucide:brain",
    "document_py": "lucide:file-code",
    "gear_process": "mdi:cog",
    "cube_vm": "mdi:cube-outline",
    "pac_output": "game-icons:pacman",
}

ICON_SCALES: dict[str, float] = {
    "bar_chart_up": 0.42,
    "rocket": 0.45,
    "code_simple": 0.42,
    "swiss_knife": 0.44,
    "robot_arm": 0.44,
    "globe": 0.44,
    "gamepad": 0.44,
    "chart_lines": 0.42,
    "crowd": 0.44,
    "brain_gear": 0.44,
    "document_py": 0.44,
    "gear_process": 0.44,
    "cube_vm": 0.44,
    "pac_output": 0.38,
    "binary_strip": 1.0,
}

COLORFUL_ICONS = frozenset({"document_py", "pac_output", "rocket", "gamepad", "brain_gear"})


def _load_svg_icon(icon_id: str) -> Mobject | None:
    ref = ICON_SVG_REFS.get(icon_id)
    if not ref:
        return None
    try:
        from icon_library import load_icon

        scale = ICON_SCALES.get(icon_id, 0.42)
        tint = None if icon_id in COLORFUL_ICONS else WHITE
        mob = load_icon(ref, scale=scale, color=tint)
        return mob
    except Exception:
        return None


def icon_by_id(icon_id: str) -> VGroup:
    svg = _load_svg_icon(icon_id)
    if svg is not None:
        return VGroup(svg)
    builders = {
        "bar_chart_up": _icon_bar_chart_up,
        "rocket": _icon_rocket,
        "code_simple": _icon_code_simple,
        "swiss_knife": _icon_swiss_knife,
        "robot_arm": _icon_robot_arm,
        "globe": _icon_globe,
        "gamepad": _icon_gamepad,
        "chart_lines": _icon_chart_lines,
        "crowd": _icon_crowd,
        "brain_gear": _icon_brain_gear,
        "document_py": _icon_document_py,
        "gear_process": _icon_gear_process,
        "cube_vm": _icon_cube_vm,
        "binary_strip": _icon_binary_strip,
        "pac_output": _icon_pac_output,
    }
    fn = builders.get(icon_id, _icon_gear_process)
    return fn()


def hub_python_logo(*, scale: float = 0.38) -> Mobject:
    """Colorful Python mark for mind-map hub."""
    try:
        from icon_library import load_icon

        return load_icon("devicon:python", scale=scale, color=None)
    except Exception:
        return Text("Py", color=BLUE, font_size=20, weight=BOLD)


def _icon_bar_chart_up() -> VGroup:
    bars = VGroup(
        *[
            Rectangle(width=0.22, height=0.25 + i * 0.18, color=BLUE, fill_opacity=0.6, stroke_width=1)
            for i in range(4)
        ]
    ).arrange(RIGHT, buff=0.08, aligned_edge=DOWN)
    arrow = Arrow(bars.get_bottom() + LEFT * 0.1, bars.get_top() + RIGHT * 0.15, color=RED, stroke_width=2, buff=0.05)
    return VGroup(bars, arrow)


def _icon_rocket() -> VGroup:
    body = Triangle(color=RED, fill_opacity=0.7).scale(0.35).rotate(PI)
    flame = VGroup(
        Line(body.get_bottom(), body.get_bottom() + DOWN * 0.2 + LEFT * 0.08, color=ORANGE, stroke_width=2),
        Line(body.get_bottom(), body.get_bottom() + DOWN * 0.25, color=YELLOW, stroke_width=2),
        Line(body.get_bottom(), body.get_bottom() + DOWN * 0.2 + RIGHT * 0.08, color=ORANGE, stroke_width=2),
    )
    return VGroup(body, flame)


def _icon_code_simple() -> VGroup:
    small = RoundedRectangle(width=0.45, height=0.55, color=BLUE, fill_opacity=0.2)
    sl = VGroup(*[Line(small.get_left() + RIGHT * 0.1, small.get_right() + LEFT * 0.1, color=WHITE, stroke_width=1).shift(UP * (0.12 - i * 0.12)) for i in range(2)])
    sl.move_to(small.get_center())
    big = RoundedRectangle(width=0.55, height=0.85, color=GRAY, fill_opacity=0.15).shift(RIGHT * 0.55)
    bl = VGroup(*[Line(big.get_left() + RIGHT * 0.08, big.get_right() + LEFT * 0.08, color=WHITE, stroke_width=1).shift(UP * (0.2 - i * 0.1)) for i in range(4)])
    bl.move_to(big.get_center())
    return VGroup(small, sl, big, bl)


def _icon_swiss_knife() -> VGroup:
    body = RoundedRectangle(width=0.35, height=0.7, color=RED, fill_opacity=0.75, corner_radius=0.08)
    tools = VGroup(
        Line(body.get_top(), body.get_top() + UP * 0.25 + LEFT * 0.12, color=GRAY, stroke_width=3),
        Line(body.get_top(), body.get_top() + UP * 0.2, color=GRAY, stroke_width=3),
        Line(body.get_top(), body.get_top() + UP * 0.25 + RIGHT * 0.12, color=GRAY, stroke_width=3),
    )
    return VGroup(body, tools)


def _icon_robot_arm() -> VGroup:
    base = Rectangle(width=0.35, height=0.12, color=YELLOW, fill_opacity=0.5)
    arm = Line(base.get_top(), base.get_top() + UP * 0.35 + RIGHT * 0.25, color=WHITE, stroke_width=4)
    claw = VGroup(
        Line(arm.get_end(), arm.get_end() + UP * 0.12 + LEFT * 0.1, color=WHITE, stroke_width=3),
        Line(arm.get_end(), arm.get_end() + UP * 0.12 + RIGHT * 0.1, color=WHITE, stroke_width=3),
    )
    return VGroup(base, arm, claw)


def _icon_globe() -> VGroup:
    c = Circle(radius=0.35, color=BLUE, fill_opacity=0.25, stroke_width=2)
    meridians = VGroup(
        Ellipse(width=0.25, height=0.7, color=BLUE, stroke_width=1).move_to(c.get_center()),
        Line(c.get_top(), c.get_bottom(), color=BLUE, stroke_width=1),
        Line(c.get_left(), c.get_right(), color=BLUE, stroke_width=1),
    )
    return VGroup(c, meridians)


def _icon_gamepad() -> VGroup:
    pad = RoundedRectangle(width=0.75, height=0.4, color=WHITE, fill_opacity=0.15, corner_radius=0.12)
    dots = VGroup(
        Dot(pad.get_center() + LEFT * 0.15 + UP * 0.05, color=RED, radius=0.05),
        Dot(pad.get_center() + LEFT * 0.15 + DOWN * 0.05, color=BLUE, radius=0.05),
        Dot(pad.get_center() + RIGHT * 0.15, color=GREEN, radius=0.05),
    )
    return VGroup(pad, dots)


def _icon_chart_lines() -> VGroup:
    bars = VGroup(
        Rectangle(width=0.15, height=0.2, color=BLUE, fill_opacity=0.5),
        Rectangle(width=0.15, height=0.35, color=BLUE, fill_opacity=0.5),
        Rectangle(width=0.15, height=0.28, color=BLUE, fill_opacity=0.5),
    ).arrange(RIGHT, buff=0.06, aligned_edge=DOWN)
    line = VMobject(color=GREEN, stroke_width=2)
    line.set_points_as_corners([bars.get_left() + UP * 0.1, bars.get_center() + UP * 0.45, bars.get_right() + UP * 0.25])
    return VGroup(bars, line)


def _icon_crowd() -> VGroup:
    heads = VGroup(
        *[
            VGroup(
                Circle(radius=0.08, color=WHITE, fill_opacity=0.3, stroke_width=1),
                Line(ORIGIN, DOWN * 0.12, color=WHITE, stroke_width=2),
            ).shift(RIGHT * i * 0.22)
            for i in range(4)
        ]
    )
    return heads


def _icon_brain_gear() -> VGroup:
    head = Arc(radius=0.35, angle=PI, color=WHITE, stroke_width=2).rotate(-PI / 2)
    gear = Circle(radius=0.12, color=YELLOW, fill_opacity=0.5).shift(RIGHT * 0.05)
    nodes = VGroup(
        Dot(head.get_top() + UP * 0.05, color=BLUE, radius=0.04),
        Dot(head.get_end() + LEFT * 0.05, color=BLUE, radius=0.04),
    )
    return VGroup(head, gear, nodes)


def _icon_document_py() -> VGroup:
    doc = RoundedRectangle(width=0.5, height=0.65, color=WHITE, fill_opacity=0.12, stroke_width=2)
    squig = VGroup(*[Line(doc.get_left() + RIGHT * 0.08, doc.get_right() + LEFT * 0.08, color=WHITE, stroke_width=1).shift(UP * (0.15 - i * 0.1)) for i in range(3)])
    squig.move_to(doc.get_center())
    tag = Text("py", color=BLUE, font_size=14).move_to(doc.get_corner(DR) + UL * 0.12)
    return VGroup(doc, squig, tag)


def _icon_gear_process() -> VGroup:
    gear = Circle(radius=0.28, color=GRAY, fill_opacity=0.4, stroke_width=2)
    teeth = VGroup(
        *[Rectangle(width=0.08, height=0.12, color=GRAY, fill_opacity=0.5).move_to(gear.get_center() + 0.32 * np.array([np.cos(a), np.sin(a), 0])) for a in np.linspace(0, TAU, 8, endpoint=False)]
    )
    ring = Circle(radius=0.45, color=YELLOW, stroke_width=1.5).set_opacity(0.5)
    return VGroup(ring, gear, teeth)


def _icon_cube_vm() -> VGroup:
    outer = Square(side_length=0.55, color=TEAL, stroke_width=2)
    inner = Square(side_length=0.3, color=WHITE, stroke_width=1.5).move_to(outer.get_center())
    corners = VGroup(
        Line(outer.get_corner(DL), inner.get_corner(DL), color=TEAL, stroke_width=1),
        Line(outer.get_corner(DR), inner.get_corner(DR), color=TEAL, stroke_width=1),
    )
    return VGroup(outer, inner, corners)


def _icon_binary_strip() -> VGroup:
    from blackboard_sketch import chalk_text

    return VGroup(chalk_text("1011001", color=BLUE, font_size=18, weight=NORMAL, seed="binary"))


def _icon_pac_output() -> VGroup:
    wedge = Sector(radius=0.35, angle=PI / 1.5, color=YELLOW, fill_opacity=0.85).rotate(-PI / 4)
    dots = VGroup(
        Dot(wedge.get_right() + RIGHT * 0.2, color=BLUE, radius=0.06),
        Dot(wedge.get_right() + RIGHT * 0.35, color=BLUE, radius=0.06),
    )
    return VGroup(wedge, dots)


def icon_catalog_for_prompt() -> str:
    lines = ["Icon catalog (pick icon_id per stage/branch):"]
    hints = {
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
    for iid in ICON_IDS:
        lines.append(f"- {iid}: {hints.get(iid, '')}")
    return "\n".join(lines)
