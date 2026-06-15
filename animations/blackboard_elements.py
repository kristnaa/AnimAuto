"""Blackboard/chalk visual primitives for voice-motion explainer layouts."""

from __future__ import annotations

from manim import *

from blackboard_sketch import (
    SKETCH,
    chalk_text,
    sketch_curved_path,
    sketch_dashed_line,
    sketch_arrow_head,
    sketch_highlight_pill,
    sketch_rounded_rect,
)

BLACKBOARD = {
    "bg": BLACK,
    "chalk": WHITE,
    "arrow": YELLOW,
    "highlight": BLUE,
    "accent": RED,
    "fill_opacity": 0.15,
}


def page_background_blackboard_clean() -> VGroup:
    """Minimal chalk dust — does not compete with diagrams."""
    dust = VGroup(
        *[
            Dot(
                point=[2.8 * np.cos(a), 1.6 * np.sin(a), 0],
                radius=0.025,
                color=WHITE,
            ).set_opacity(0.08 + (i % 3) * 0.03)
            for i, a in enumerate(np.linspace(0, TAU, 14, endpoint=False))
        ]
    )
    return dust


def chalk_box(
    label: str,
    *,
    tag: str | None = None,
    width: float = 2.4,
    height: float = 1.0,
    with_python_logo: bool = False,
) -> VGroup:
    box = sketch_rounded_rect(
        width,
        height,
        fill_opacity=BLACKBOARD["fill_opacity"],
        seed=f"box-{label}",
    )
    parts: list[Mobject] = [box]
    if with_python_logo and "python" in label.lower():
        from blackboard_icons import hub_python_logo

        logo = hub_python_logo(scale=0.34)
        txt = chalk_text(label, font_size=24, seed=f"hub-{label}")
        row = VGroup(logo, txt).arrange(RIGHT, buff=0.12)
        row.move_to(box.get_center())
        parts.append(row)
    else:
        txt = chalk_text(label, font_size=24, seed=f"hub-{label}")
        txt.move_to(box.get_center())
        parts.append(txt)
    if tag:
        tag_mob = chalk_text(tag.upper(), font_size=14, seed=f"tag-{tag}")
        tag_bg = Polygon(
            box.get_corner(UR) + LEFT * 0.02 + DOWN * 0.02,
            box.get_corner(UR) + LEFT * 0.57 + DOWN * 0.02,
            box.get_corner(UR) + LEFT * 0.57 + DOWN * 0.4,
            box.get_corner(UR) + DOWN * 0.4,
            color=BLACKBOARD["accent"],
            fill_opacity=1,
            stroke_width=0,
        )
        tag_mob.move_to(tag_bg.get_center())
        parts.extend([tag_bg, tag_mob])
    return VGroup(*parts)


def highlight_pill(text: str, highlight_word: str | None = None) -> VGroup:
    return sketch_highlight_pill(text, highlight_word, seed=f"pill-{text}")


def curved_arrow_between(start: np.ndarray, end: np.ndarray, *, color=YELLOW) -> Mobject:
    curve = sketch_curved_path(start, end, color=color, seed=f"curve-{start}-{end}")
    direction = end - start
    tip = sketch_arrow_head(end, direction, color=color, seed=f"tip-{end}")
    return VGroup(curve, tip)


def dashed_arrow_between(start: np.ndarray, end: np.ndarray, *, color=YELLOW) -> VGroup:
    line = sketch_dashed_line(start, end, color=color, seed=f"dash-{start}-{end}")
    direction = end - start
    tip = sketch_arrow_head(end, direction, color=color, seed=f"dtip-{end}")
    return VGroup(line, tip)


def branch_node(label: str, icon: Mobject, *, highlight: str | None = None) -> VGroup:
    lbl = highlight_pill(label, highlight)
    lbl.scale(0.9)
    icon.scale(0.85)
    icon.next_to(lbl, UP, buff=0.2)
    return VGroup(icon, lbl)


def layout_pipeline_blackboard(stages: list[dict], *, title: str | None = None) -> VGroup:
    """Horizontal pipeline: icon + label stages with optional nested box."""
    parts_top: list[Mobject] = []
    if title:
        parts_top.append(highlight_pill(title, title.split()[0] if title.split() else None).scale(1.15))
        parts_top[-1].to_edge(UP, buff=0.55)

    stage_groups: list[VGroup] = []
    binary_between: str | None = None
    for st in stages:
        label = str(st.get("label") or "Step")
        icon_id = st.get("icon_id")
        from blackboard_icons import icon_by_id

        icon = icon_by_id(str(icon_id) if icon_id else "gear_process")
        node = branch_node(label, icon)
        nested = st.get("nested") or []
        if nested:
            inner_items: list[Mobject] = []
            nested_icons = st.get("nested_icons") or []
            for idx, n in enumerate(nested[:3]):
                n_icon = icon_by_id(str(nested_icons[idx])) if idx < len(nested_icons) else None
                t = chalk_text(str(n)[:12], font_size=16, weight=NORMAL, seed=f"nest-{n}")
                if n_icon:
                    n_icon.scale(0.55)
                    n_icon.next_to(t, UP, buff=0.08)
                    inner_items.append(VGroup(n_icon, t))
                else:
                    inner_items.append(t)
            inner = VGroup(*inner_items).arrange(RIGHT, buff=0.35)
            wrapper = sketch_rounded_rect(
                max(3.4, inner.width + 0.6),
                max(1.8, inner.height + 0.55),
                seed=f"wrap-{label}",
                fill_opacity=0.08,
            )
            inner.move_to(wrapper.get_center())
            outer_label = chalk_text(label, font_size=18, seed=f"outer-{label}").next_to(wrapper, UP, buff=0.12)
            stage_groups.append(VGroup(outer_label, wrapper, inner))
        else:
            stage_groups.append(node)
        if st.get("binary_strip"):
            binary_between = str(st["binary_strip"])

    row_parts: list[Mobject] = []
    for i, sg in enumerate(stage_groups):
        row_parts.append(sg)
        if i < len(stage_groups) - 1:
            a = stage_groups[i].get_right()
            b = stage_groups[i + 1].get_left()
            arrow_grp = dashed_arrow_between(a, b)
            if binary_between and i == len(stage_groups) - 2:
                from blackboard_icons import icon_by_id

                bin_mob = icon_by_id("binary_strip").scale(0.85)
                bin_mob.move_to((a + b) / 2 + UP * 0.35)
                arrow_grp = VGroup(arrow_grp, bin_mob)
            row_parts.append(arrow_grp)
    diagram = VGroup(*row_parts).arrange(RIGHT, buff=0.55).move_to(ORIGIN)
    if parts_top:
        diagram.next_to(parts_top[0], DOWN, buff=0.45)
        return VGroup(*parts_top, diagram)
    return diagram


def layout_mind_map_radial(
    hub_label: str,
    branches: list[dict],
    *,
    hub_tag: str | None = None,
    mode: str = "full",
    title: str | None = None,
) -> VGroup:
    from blackboard_icons import icon_by_id

    header: Mobject | None = None
    if title:
        header = highlight_pill(title, title.split()[-1] if title.split() else None).scale(1.2)
        header.to_edge(UP, buff=0.5)

    hub = chalk_box(
        hub_label,
        tag=hub_tag,
        width=2.8,
        height=1.05,
        with_python_logo="python" in hub_label.lower(),
    )
    if mode == "single" and branches:
        br = branches[0]
        icon = icon_by_id(str(br.get("icon_id") or "brain_gear"))
        node = branch_node(str(br.get("label") or "Topic"), icon, highlight=br.get("highlight"))
        node.next_to(hub, RIGHT, buff=1.2)
        link = curved_arrow_between(hub.get_right(), node.get_left())
        subs = _sub_branch_group(br.get("sub_labels") or [], br.get("sub_icons") or [])
        body = VGroup(hub, link, node, subs) if len(subs) > 0 else VGroup(hub, link, node)
        body.move_to(ORIGIN)
        if header:
            body.next_to(header, DOWN, buff=0.4)
            return VGroup(header, body)
        return body

    branch_mobs: list[VGroup] = []
    n = min(5, max(1, len(branches)))
    angle_offsets = [2.4, 1.0, 0.15, -1.0, -2.4][:n]
    radius = 2.65
    for i, br in enumerate(branches[:5]):
        angle = angle_offsets[i] if i < len(angle_offsets) else PI / 2 + i * TAU / n
        pos = hub.get_center() + radius * np.array([np.cos(angle), np.sin(angle), 0])
        icon = icon_by_id(str(br.get("icon_id") or "brain_gear"))
        hl = br.get("highlight")
        if not hl and br.get("label"):
            words = str(br["label"]).split()
            hl = words[-1] if words else None
        node = branch_node(str(br.get("label") or "Point"), icon, highlight=hl)
        node.move_to(pos)
        hub_edge = hub.get_center() + 0.35 * (pos - hub.get_center()) / max(np.linalg.norm(pos - hub.get_center()), 0.01)
        link = curved_arrow_between(hub_edge, node.get_center())
        group = VGroup(link, node)
        subs = br.get("sub_labels") or []
        if subs:
            sub_icons = br.get("sub_icons") or []
            sub_grp = _sub_branch_group(subs, sub_icons, horizontal=True)
            sub_grp.next_to(node, RIGHT, buff=0.35)
            sub_links = VGroup(
                *[
                    curved_arrow_between(node.get_right(), sub_grp[j].get_left(), color=YELLOW).scale(0.85)
                    for j in range(min(len(sub_grp), 4))
                ]
            )
            group = VGroup(group, sub_links, sub_grp)
        branch_mobs.append(group)
    body = VGroup(hub, *branch_mobs).move_to(ORIGIN)
    if header:
        body.next_to(header, DOWN, buff=0.35)
        return VGroup(header, body)
    return body


def _sub_branch_group(sub_labels: list, sub_icons: list | None = None, *, horizontal: bool = False) -> VGroup:
    if not sub_labels:
        return VGroup()
    items = []
    sub_icons = sub_icons or []
    from blackboard_icons import icon_by_id

    for idx, s in enumerate(sub_labels[:4]):
        t = chalk_text(str(s)[:10], font_size=15, weight=NORMAL, seed=f"sub-{s}")
        parts: list[Mobject] = []
        if idx < len(sub_icons):
            ic = icon_by_id(str(sub_icons[idx])).scale(0.6)
            ic.next_to(t, UP, buff=0.06)
            parts.extend([ic, t])
        else:
            dot = Dot(color=YELLOW, radius=0.05).next_to(t, LEFT, buff=0.1)
            parts.extend([dot, t])
        items.append(VGroup(*parts))
    if horizontal:
        return VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
    return VGroup(*items).arrange(DOWN, aligned_edge=LEFT, buff=0.15)


def draw_sketchy(scene, mob: Mobject, *, run_time: float = 1.4) -> None:
    """Hand-drawn reveal — Create on strokes, FadeIn on SVG icons."""
    strokes = [m for m in mob.get_family() if isinstance(m, VMobject) and m.get_stroke_width() and m.get_stroke_width() > 0]
    fills = [m for m in mob.get_family() if m not in strokes]
    if strokes:
        scene.play(*[Create(s) for s in strokes[:24]], run_time=run_time)
    if fills:
        scene.play(FadeIn(VGroup(*fills[:40]), shift=0.02 * UP), run_time=run_time * 0.45)
