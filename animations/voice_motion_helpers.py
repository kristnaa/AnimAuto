"""Lightweight Manim helpers for voice-motion scenes (no BeatScene / icons)."""

from __future__ import annotations

from manim import *

# ---------------------------------------------------------------------------
# Text wrapping (no ellipsis truncation)
# ---------------------------------------------------------------------------

DEFAULT_MAX_CHARS = 40


def split_text_lines(text: str, max_chars: int = DEFAULT_MAX_CHARS) -> list[str]:
    clean = " ".join((text or "").split())
    if not clean:
        return [""]
    words = clean.split()
    lines: list[str] = []
    current: list[str] = []
    length = 0
    for word in words:
        extra = len(word) + (1 if current else 0)
        if current and length + extra > max_chars:
            lines.append(" ".join(current))
            current = [word]
            length = len(word)
        else:
            current.append(word)
            length += extra
    if current:
        lines.append(" ".join(current))
    return lines


def layout_wrapped_text(
    text: str,
    *,
    font_size: int = 32,
    color=WHITE,
    max_chars: int = DEFAULT_MAX_CHARS,
    line_buff: float = 0.24,
) -> VGroup:
    lines = split_text_lines(text, max_chars)
    items = [Text(line, font_size=font_size, color=color) for line in lines]
    group = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=line_buff)
    group.move_to(ORIGIN)
    return group


def layout_wrapped_in_box(
    text: str,
    *,
    font_size: int = 24,
    box_color=BLUE,
    max_chars: int = 22,
    min_width: float = 2.8,
) -> VGroup:
    body = layout_wrapped_text(text, font_size=font_size, max_chars=max_chars, line_buff=0.16)
    pad_w, pad_h = 0.45, 0.28
    box = RoundedRectangle(
        corner_radius=0.14,
        width=max(min_width, body.width + pad_w * 2),
        height=max(0.85, body.height + pad_h * 2),
        color=box_color,
        fill_opacity=0.22,
        stroke_width=2,
    )
    body.move_to(box.get_center())
    return VGroup(box, body)


# ---------------------------------------------------------------------------
# Page backgrounds — vary per scene
# ---------------------------------------------------------------------------

BACKGROUND_BUILDERS = (
    "radial_blue",
    "corner_warm",
    "grid_fade",
    "split_tone",
    "orbit_glow",
    "edge_frame",
)


def page_background(style: str = "radial_blue") -> VGroup:
    if style == "corner_warm":
        return VGroup(
            RoundedRectangle(width=13, height=7.2, corner_radius=0.2, color=ORANGE, stroke_width=0)
            .set_fill(ORANGE, opacity=0.07)
            .to_corner(DL, buff=0),
            Line(UL * 2.8 + LEFT * 5.5, UL * 2.8 + RIGHT * 0.5, color=ORANGE, stroke_width=4, stroke_opacity=0.55),
            Line(DR * 2.8 + RIGHT * 5.5, DR * 2.8 + LEFT * 0.5, color=YELLOW, stroke_width=3, stroke_opacity=0.45),
        )
    if style == "grid_fade":
        grid = VGroup(
            *[
                Line(LEFT * 6 + UP * y, RIGHT * 6 + UP * y, color=TEAL, stroke_width=1, stroke_opacity=0.12)
                for y in range(-3, 4)
            ],
            *[
                Line(LEFT * x + UP * 3.5, LEFT * x + DOWN * 3.5, color=TEAL, stroke_width=1, stroke_opacity=0.12)
                for x in range(-6, 7, 2)
            ],
        )
        wash = Rectangle(width=14, height=8, color=TEAL, stroke_width=0).set_fill(TEAL, opacity=0.04)
        return VGroup(wash, grid)
    if style == "split_tone":
        left = Polygon(UL * 4 + LEFT * 7, DL * 4 + LEFT * 7, ORIGIN + DOWN * 4, color=PURPLE, stroke_width=0)
        left.set_fill(PURPLE, opacity=0.12)
        right = Polygon(UR * 4 + RIGHT * 7, DR * 4 + RIGHT * 7, ORIGIN + DOWN * 4, color=TEAL, stroke_width=0)
        right.set_fill(TEAL, opacity=0.1)
        return VGroup(left, right)
    if style == "orbit_glow":
        dots = VGroup(
            *[
                Dot(point=[1.8 * np.cos(a), 1.8 * np.sin(a), 0], color=YELLOW if i % 2 else PURPLE, radius=0.06)
                for i, a in enumerate(np.linspace(0, TAU, 8, endpoint=False))
            ]
        )
        ring = Circle(radius=2.5, color=PURPLE, stroke_opacity=0.25, stroke_width=2).set_fill(PURPLE, opacity=0.05)
        return VGroup(ring, dots)
    if style == "edge_frame":
        frame = VGroup(
            Line(UL * 3 + LEFT * 2, UL * 3 + RIGHT * 2, color=WHITE, stroke_opacity=0.35, stroke_width=2),
            Line(DL * 3 + LEFT * 2, DL * 3 + RIGHT * 2, color=WHITE, stroke_opacity=0.35, stroke_width=2),
            Line(UL * 3 + LEFT * 3.5, DL * 3 + LEFT * 3.5, color=BLUE, stroke_opacity=0.4, stroke_width=2),
            Line(UR * 3 + RIGHT * 3.5, DR * 3 + RIGHT * 3.5, color=BLUE, stroke_opacity=0.4, stroke_width=2),
        )
        return frame
    if style == "blackboard_clean":
        from blackboard_elements import page_background_blackboard_clean

        return page_background_blackboard_clean()
    # radial_blue (default)
    ring = Circle(radius=3.4, color=BLUE, stroke_width=2, stroke_opacity=0.3).set_fill(BLUE, opacity=0.06)
    ring2 = Circle(radius=2.2, color=TEAL, stroke_width=1.5, stroke_opacity=0.22).set_fill(TEAL, opacity=0.05)
    return VGroup(ring2, ring)


def page_accent_backdrop(accent=BLUE, accent2=TEAL) -> VGroup:
    """Legacy — prefer page_background(style)."""
    return page_background("radial_blue")


def side_bars_for(mob: Mobject, color=BLUE) -> VGroup:
    left = Line(LEFT * 0.35, RIGHT * 0.35, color=color, stroke_width=4).next_to(mob, LEFT, buff=0.25)
    right = left.copy().next_to(mob, RIGHT, buff=0.25)
    return VGroup(left, right)


# ---------------------------------------------------------------------------
# Typing animations
# ---------------------------------------------------------------------------

def typing_cursor_for(text_mob: Mobject, cursor_color=YELLOW) -> Rectangle:
    return Rectangle(
        width=0.06,
        height=max(0.3, text_mob.height * 1.05),
        fill_color=cursor_color,
        fill_opacity=1,
        stroke_width=0,
    )


def type_with_cursor(scene, text_mob, *, time_per_char: float = 0.05, cursor_color=YELLOW) -> None:
    cursor = typing_cursor_for(text_mob, cursor_color=cursor_color)
    if len(text_mob) > 0:
        cursor.move_to(text_mob[0])
    else:
        cursor.move_to(text_mob.get_left())
    text_len = len(getattr(text_mob, "text", "") or "")
    scene.play(
        TypeWithCursor(text_mob, cursor, time_per_char=time_per_char, leave_cursor_on=False),
        run_time=max(0.35, text_len * time_per_char),
    )


def type_wrapped_with_cursor(
    scene,
    wrapped: VGroup,
    *,
    time_per_char: float = 0.04,
    cursor_color=YELLOW,
) -> None:
    for line_mob in wrapped:
        type_with_cursor(scene, line_mob, time_per_char=time_per_char, cursor_color=cursor_color)


def fade_out_page(scene, *mobjects, run_time: float = 0.4) -> None:
    group = VGroup(*[m for m in mobjects if m is not None])
    if len(group) > 0:
        scene.play(FadeOut(group), run_time=run_time)


# ---------------------------------------------------------------------------
# Layout builders
# ---------------------------------------------------------------------------

def layout_center_title(text: str, font_size: int = 52) -> VGroup:
    """Short hook title only (2–4 words)."""
    title = Text(text, color=WHITE, font_size=font_size, weight=BOLD)
    underline = Line(LEFT * 2.2, RIGHT * 2.2, color=YELLOW, stroke_width=4)
    underline.next_to(title, DOWN, buff=0.18)
    badge = RoundedRectangle(
        width=max(3.5, title.width + 0.8),
        height=max(1.0, title.height + 0.5),
        corner_radius=0.14,
        color=ORANGE,
        fill_opacity=0.18,
        stroke_width=2,
    )
    badge.move_to(title.get_center())
    accent = side_bars_for(title, color=BLUE)
    group = VGroup(badge, title, underline, accent)
    group.move_to(ORIGIN)
    return group


def layout_center_bullets(lines: list[str], font_size: int = 30) -> VGroup:
    items: list[VGroup] = []
    colors = [BLUE, TEAL, GREEN, YELLOW]
    for i, line in enumerate(lines):
        if not line.strip():
            continue
        label = Text(line.strip(), font_size=font_size, color=WHITE)
        dot = Dot(color=colors[i % len(colors)], radius=0.09)
        row = VGroup(dot, label).arrange(RIGHT, buff=0.25, aligned_edge=DOWN)
        items.append(row)
    group = VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.42)
    panel = RoundedRectangle(
        width=max(5.5, group.width + 0.8),
        height=max(1.4, group.height + 0.55),
        corner_radius=0.14,
        color=BLUE,
        fill_opacity=0.12,
        stroke_width=2,
        stroke_opacity=0.55,
    )
    panel.move_to(group.get_center())
    return VGroup(panel, group).move_to(ORIGIN)


def layout_flowchart_vertical(labels: list[str], *, color=BLUE) -> VGroup:
    nodes: list[VGroup] = []
    step_colors = [BLUE, TEAL, GREEN, PURPLE]
    for i, label in enumerate(labels):
        c = step_colors[i % len(step_colors)]
        node = layout_wrapped_in_box(label, font_size=22, box_color=c, max_chars=20, min_width=3.0)
        badge = Text(str(i + 1), font_size=18, color=BLACK, weight=BOLD)
        badge.move_to(node[0].get_corner(UL) + DR * 0.22)
        badge_bg = Circle(radius=0.18, color=YELLOW, fill_opacity=1).move_to(badge.get_center())
        nodes.append(VGroup(node, badge_bg, badge))
    group = VGroup(*nodes).arrange(DOWN, buff=0.5)
    arrows: list[Arrow] = []
    for i in range(len(nodes) - 1):
        arrows.append(
            Arrow(
                nodes[i].get_bottom(),
                nodes[i + 1].get_top(),
                buff=0.1,
                color=YELLOW,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.18,
            )
        )
    parts: list[Mobject] = []
    for i, node in enumerate(nodes):
        parts.append(node)
        if i < len(arrows):
            parts.append(arrows[i])
    out = VGroup(*parts)
    out.move_to(ORIGIN)
    return out


def layout_flowchart_horizontal(labels: list[str], *, color=TEAL) -> VGroup:
    nodes: list[VGroup] = []
    step_colors = [TEAL, BLUE, GREEN, ORANGE]
    for i, label in enumerate(labels):
        c = step_colors[i % len(step_colors)]
        node = layout_wrapped_in_box(label, font_size=20, box_color=c, max_chars=14, min_width=2.2)
        nodes.append(node)
    group = VGroup(*nodes).arrange(RIGHT, buff=0.42)
    arrows: list[Arrow] = []
    for i in range(len(nodes) - 1):
        arrows.append(
            Arrow(
                nodes[i].get_right(),
                nodes[i + 1].get_left(),
                buff=0.08,
                color=YELLOW,
                stroke_width=3,
            )
        )
    parts: list[Mobject] = []
    for i, node in enumerate(nodes):
        parts.append(node)
        if i < len(arrows):
            parts.append(arrows[i])
    out = VGroup(*parts)
    out.move_to(ORIGIN)
    return out


def layout_diagram_labeled(shape_label: str, caption: str = "") -> VGroup:
    shape = Circle(radius=1.15, color=PURPLE, fill_opacity=0.28, stroke_width=3)
    glow = Circle(radius=1.38, color=PURPLE, stroke_width=1, stroke_opacity=0.35, fill_opacity=0.06)
    inner = Text(shape_label, color=WHITE, font_size=28, weight=BOLD)
    inner.move_to(shape.get_center())
    spokes = VGroup(
        Line(shape.get_center(), shape.get_center() + UP * 1.55, color=BLUE, stroke_opacity=0.55, stroke_width=2),
        Line(shape.get_center(), shape.get_center() + DL * 1.35, color=TEAL, stroke_opacity=0.55, stroke_width=2),
        Line(shape.get_center(), shape.get_center() + DR * 1.35, color=GREEN, stroke_opacity=0.55, stroke_width=2),
    )
    satellites = VGroup(
        Square(side_length=0.45, color=YELLOW, fill_opacity=0.7).move_to(shape.get_center() + UP * 1.55),
        Square(side_length=0.45, color=TEAL, fill_opacity=0.7).move_to(shape.get_center() + DL * 1.35),
        Square(side_length=0.45, color=GREEN, fill_opacity=0.7).move_to(shape.get_center() + DR * 1.35),
    )
    parts: list[Mobject] = [glow, spokes, satellites, shape, inner]
    if caption.strip():
        cap = Text(caption, color=WHITE, font_size=24)
        cap.next_to(shape, DOWN, buff=0.35)
        parts.append(cap)
    group = VGroup(*parts)
    group.move_to(ORIGIN)
    return group


def layout_visual_orbit(hub_label: str, orbit_labels: list[str]) -> VGroup:
    hub = Circle(radius=0.95, color=BLUE, fill_opacity=0.35, stroke_width=3)
    hub_text = Text(hub_label, color=WHITE, font_size=24, weight=BOLD).move_to(hub.get_center())
    orbit_ring = Circle(radius=2.2, color=TEAL, stroke_opacity=0.35, stroke_width=2)
    nodes: list[VGroup] = []
    n = max(1, len(orbit_labels))
    for i, label in enumerate(orbit_labels[:4]):
        angle = i * TAU / n
        pos = orbit_ring.point_at_angle(angle)
        box = RoundedRectangle(width=1.8, height=0.65, corner_radius=0.1, color=YELLOW, fill_opacity=0.2)
        box.move_to(pos)
        txt = Text(label, font_size=18, color=WHITE).move_to(box.get_center())
        link = Line(hub.get_center(), box.get_center(), color=WHITE, stroke_opacity=0.35, stroke_width=1.5)
        nodes.append(VGroup(link, box, txt))
    return VGroup(orbit_ring, hub, hub_text, *nodes).move_to(ORIGIN)


def layout_kinetic_keyword(word: str) -> VGroup:
    ring = Circle(radius=1.5, color=YELLOW, stroke_width=2, stroke_opacity=0.45).set_fill(YELLOW, opacity=0.08)
    mob = Text(word, color=YELLOW, font_size=72, weight=BOLD)
    mob.move_to(ORIGIN)
    sparks = VGroup(
        *[
            Line(ORIGIN, 0.35 * (np.cos(a) * RIGHT + np.sin(a) * UP), color=ORANGE, stroke_width=2, stroke_opacity=0.6)
            for a in np.linspace(0, TAU, 6, endpoint=False)
        ]
    )
    return VGroup(ring, sparks, mob).move_to(ORIGIN)


def layout_fade_transition(hint: str = "") -> VGroup:
    arrow = Arrow(LEFT * 2.2, RIGHT * 2.2, color=BLUE, stroke_width=4, buff=0.1)
    pulse = Circle(radius=0.35, color=TEAL, fill_opacity=0.35).move_to(ORIGIN)
    parts: list[Mobject] = [arrow, pulse]
    if hint.strip():
        label = Text(hint, color=WHITE, font_size=28, weight=BOLD).next_to(arrow, UP, buff=0.35)
        parts.append(label)
    return VGroup(*parts).move_to(ORIGIN)


def layout_compare_columns(left: str, right: str) -> VGroup:
    left_box = layout_wrapped_in_box(left, font_size=24, box_color=BLUE, max_chars=12, min_width=2.4)
    right_box = layout_wrapped_in_box(right, font_size=24, box_color=GREEN, max_chars=12, min_width=2.4)
    left_box.shift(LEFT * 3.0)
    right_box.shift(RIGHT * 3.0)
    arrow = Arrow(
        left_box.get_right(),
        right_box.get_left(),
        buff=0.15,
        color=YELLOW,
        stroke_width=3,
    )
    vs = Text("vs", font_size=28, color=WHITE, weight=BOLD).move_to(ORIGIN)
    return VGroup(left_box, vs, arrow, right_box).move_to(ORIGIN)

