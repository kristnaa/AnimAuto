"""Load Excalidraw SVG / .excalidraw files and animate draw-order reveal in Manim."""

from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

from manim import *
import numpy as np

from excalidraw_parser import (
    ExcalidrawPage,
    build_page_svg,
    detect_svg_pages,
    pages_from_excalidraw_file,
    prepare_svg_for_manim,
    svg_canvas_background_color,
)

# Excalidraw Y-down → Manim Y-up
_EXCAL_SCALE = 0.012


def animate_excalidraw_file(
    scene: Scene,
    file_path: str | Path,
    *,
    total_run_time: float = 6.0,
    hold_time: float = 1.0,
    fade_out: bool = True,
    animation_sequence: list[str] | None = None,
) -> None:
    """Main entry: load file and play draw-order animation."""
    path = Path(file_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"Drawing not found: {path}")

    suffix = path.suffix.lower()
    if suffix == ".svg":
        pages = detect_svg_pages(path)
        bg = _svg_background(path)
        if len(pages) > 1:
            _animate_svg_pages(
                scene,
                path,
                pages,
                bg=bg,
                total_run_time=total_run_time,
                hold_time=hold_time,
                fade_out=fade_out,
                animation_sequence=animation_sequence,
            )
            return
        group = _load_svg_group(path, animation_sequence=animation_sequence)
    elif suffix in (".excalidraw", ".json"):
        pages = pages_from_excalidraw_file(path)
        if len(pages) > 1:
            _animate_excalidraw_json_pages(
                scene,
                path,
                pages,
                total_run_time=total_run_time,
                hold_time=hold_time,
                fade_out=fade_out,
            )
            return
        group, bg = _load_excalidraw_group(path)
        scene.camera.background_color = bg
        _fit_to_frame(group)
        group.move_to(ORIGIN)
        _play_draw_layers(scene, group, total_run_time=total_run_time, hold_time=hold_time, fade_out=fade_out)
        return
    else:
        raise ValueError(f"Unsupported format: {suffix}")

    scene.camera.background_color = bg
    _fit_to_frame(group)
    group.move_to(ORIGIN)
    _play_draw_layers(scene, group, total_run_time=total_run_time, hold_time=hold_time, fade_out=fade_out)


def _play_draw_layers(
    scene: Scene,
    group: Mobject,
    *,
    total_run_time: float,
    hold_time: float,
    fade_out: bool,
) -> None:
    layers = _animation_layers(group)
    n = max(len(layers), 1)
    per = max(0.08, (total_run_time - hold_time) / n)

    for layer in layers:
        if isinstance(layer, VMobject) and layer.get_num_points() > 0:
            if float(layer.get_stroke_width() or 0) > 0:
                _ensure_visible_stroke(layer)
            scene.play(Create(layer), run_time=per)
        elif isinstance(layer, Mobject):
            scene.play(FadeIn(layer, shift=0.05 * UP), run_time=per * 0.85)

    scene.wait(hold_time)
    if fade_out:
        scene.play(FadeOut(group), run_time=0.3)


def _animate_svg_pages(
    scene: Scene,
    svg_path: Path,
    pages: list[ExcalidrawPage],
    *,
    bg: str,
    total_run_time: float,
    hold_time: float,
    fade_out: bool,
    animation_sequence: list[str] | None,
) -> None:
    scene.camera.background_color = bg
    n_pages = len(pages)
    transition = min(0.35, max(0.2, total_run_time * 0.05))
    page_hold = max(0.25, hold_time / n_pages)
    draw_budget = max(0.8, (total_run_time - page_hold * n_pages - transition * (n_pages - 1)) / n_pages)

    current: Mobject | None = None
    for index, page in enumerate(pages):
        page_svg = build_page_svg(svg_path, page, pages)
        group = _load_svg_group(page_svg, animation_sequence=animation_sequence)
        _fit_to_frame(group)
        group.move_to(ORIGIN)

        if current is not None:
            scene.play(FadeOut(current), run_time=transition)

        layers = _animation_layers(group)
        layer_count = max(len(layers), 1)
        per = max(0.08, draw_budget / layer_count)
        for layer in layers:
            if isinstance(layer, VMobject) and layer.get_num_points() > 0:
                if float(layer.get_stroke_width() or 0) > 0:
                    _ensure_visible_stroke(layer)
                scene.play(Create(layer), run_time=per)
            elif isinstance(layer, Mobject):
                scene.play(FadeIn(layer, shift=0.05 * UP), run_time=per * 0.85)

        scene.wait(page_hold)
        current = group

    if fade_out and current is not None:
        scene.play(FadeOut(current), run_time=0.3)


def _animate_excalidraw_json_pages(
    scene: Scene,
    path: Path,
    pages: list[ExcalidrawPage],
    *,
    total_run_time: float,
    hold_time: float,
    fade_out: bool,
) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    app = data.get("appState") or {}
    bg = str(app.get("viewBackgroundColor") or "#ffffff")
    scene.camera.background_color = bg

    elements = [el for el in (data.get("elements") or []) if isinstance(el, dict) and not el.get("isDeleted")]
    transition = min(0.35, max(0.2, total_run_time * 0.05))
    n_pages = len(pages)
    page_hold = max(0.25, hold_time / n_pages)
    draw_budget = max(0.8, (total_run_time - page_hold * n_pages - transition * (n_pages - 1)) / n_pages)

    current: Mobject | None = None
    for page in pages:
        page_elements = [
            el
            for el in elements
            if el.get("id") == page.page_id or el.get("frameId") == page.page_id
        ]
        if not page_elements:
            continue
        bounds = _elements_bounds(page_elements)
        parts: list[Mobject] = []
        for el in page_elements:
            mob = _element_to_mobject(el, bounds)
            if mob is not None:
                parts.append(mob)
        if not parts:
            continue
        group = VGroup(*parts)
        _fit_to_frame(group)
        group.move_to(ORIGIN)

        if current is not None:
            scene.play(FadeOut(current), run_time=transition)

        layer_count = max(len(parts), 1)
        per = max(0.08, draw_budget / layer_count)
        for mob in parts:
            if isinstance(mob, VMobject) and mob.get_num_points() > 0:
                if float(mob.get_stroke_width() or 0) > 0:
                    _ensure_visible_stroke(mob)
                scene.play(Create(mob), run_time=per)
            else:
                scene.play(FadeIn(mob, shift=0.05 * UP), run_time=per * 0.85)

        scene.wait(page_hold)
        current = group

    if fade_out and current is not None:
        scene.play(FadeOut(current), run_time=0.3)


def _fit_to_frame(group: Mobject, margin: float = 0.9) -> None:
    """Scale drawing to fill the Manim frame (scale up or down)."""
    fw = config.frame_width * margin
    fh = config.frame_height * margin
    if group.width > 0.001 and group.height > 0.001:
        group.scale(min(fw / group.width, fh / group.height))
    elif group.width > 0.001:
        group.scale(fw / group.width)
    elif group.height > 0.001:
        group.scale(fh / group.height)


def _ensure_visible_stroke(mob: VMobject, min_width: float = 2.0) -> None:
    for sm in mob.get_family():
        w = float(sm.get_stroke_width() or 0)
        if w > 0:
            sm.set_stroke(width=max(w, min_width))


def _animation_layers(group: VGroup) -> list[Mobject]:
    """Collect drawable strokes in document order from a loaded SVG tree."""
    root = group.submobjects[0] if len(group.submobjects) == 1 else group
    layers = _collect_stroke_layers(root, svg_root=root)
    if layers:
        return layers
    if len(group.submobjects) > 1:
        return [sm for sm in group.submobjects if not _is_background_fill(sm, root)]
    return [group]


def _collect_stroke_layers(
    mob: Mobject,
    acc: list[Mobject] | None = None,
    *,
    svg_root: Mobject | None = None,
) -> list[Mobject]:
    if acc is None:
        acc = []
    if svg_root is None:
        svg_root = mob
    if isinstance(mob, VMobject) and mob.get_num_points() > 1:
        child_strokes = [
            c
            for c in mob.submobjects
            if isinstance(c, VMobject)
            and c.get_num_points() > 1
            and not _is_background_fill(c, svg_root)
        ]
        if not child_strokes:
            if not _is_background_fill(mob, svg_root):
                acc.append(mob)
            return acc
    for child in mob.submobjects:
        _collect_stroke_layers(child, acc, svg_root=svg_root)
    return acc


def _is_background_fill(mob: Mobject, root: Mobject | None = None) -> bool:
    if not isinstance(mob, VMobject):
        return False
    fill = float(mob.get_fill_opacity() or 0)
    if fill < 0.75:
        return False
    if root is None:
        return False
    if root.width < 0.01 or root.height < 0.01:
        return False
    if mob.width >= root.width * 0.92 and mob.height >= root.height * 0.92:
        return True
    return False


def _load_svg_group(path: Path, animation_sequence: list[str] | None = None) -> VGroup:
    """Load entire SVG once — text is converted to paths for exact Excalidraw shapes."""
    cleaned = _strip_svg_background_rect(path)
    render_path = prepare_svg_for_manim(cleaned, animation_sequence=animation_sequence)
    svg = SVGMobject(str(render_path))
    _hide_background_submobjects(svg)
    return VGroup(svg)


def _strip_svg_background_rect(svg_path: Path) -> Path:
    """Remove full-canvas white/colored background rects from Excalidraw SVG exports."""
    text = svg_path.read_text(encoding="utf-8")
    try:
        root = ET.fromstring(text)
    except ET.ParseError:
        return svg_path

    view_box = root.get("viewBox") or ""
    vb_parts = view_box.split()
    vb_w = float(vb_parts[2]) if len(vb_parts) >= 4 else 800.0
    vb_h = float(vb_parts[3]) if len(vb_parts) >= 4 else 600.0

    removed = False
    for elem in list(root):
        local = elem.tag.split("}")[-1]
        if local != "rect":
            continue
        w_attr = elem.get("width", "")
        h_attr = elem.get("height", "")
        fill = (elem.get("fill") or "").lower()
        if w_attr in ("100%", str(vb_w)) and h_attr in ("100%", str(vb_h)):
            root.remove(elem)
            removed = True
        elif fill in ("#ffffff", "white", "#fff") and _rect_covers_canvas(elem, vb_w, vb_h):
            root.remove(elem)
            removed = True

    if not removed:
        return svg_path

    render_dir = svg_path.parent / ".excalidraw_render"
    render_dir.mkdir(parents=True, exist_ok=True)
    out = render_dir / f"{svg_path.stem}_nobg.svg"
    out.write_text(ET.tostring(root, encoding="unicode"), encoding="utf-8")
    return out


def _rect_covers_canvas(elem: ET.Element, vb_w: float, vb_h: float) -> bool:
    try:
        w = float(str(elem.get("width", "0")).replace("%", ""))
        h = float(str(elem.get("height", "0")).replace("%", ""))
    except ValueError:
        return elem.get("width") == "100%" and elem.get("height") == "100%"
    return w >= vb_w * 0.95 and h >= vb_h * 0.95


def _hide_background_submobjects(mob: Mobject) -> None:
    for sm in mob.get_family():
        if _is_background_fill(sm, mob):
            sm.set_opacity(0)
            sm.set_fill(opacity=0)


def _svg_background(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    if "viewBackgroundColor" in text:
        m = re.search(r'"viewBackgroundColor"\s*:\s*"([^"]+)"', text)
        if m:
            return m.group(1)
    canvas = svg_canvas_background_color(path)
    if canvas:
        return canvas
    # Excalidraw dark mode export
    if re.search(r'viewBackgroundColor["\']?\s*[:=]\s*["\']#1', text, re.I):
        return "#1e1e1e"
    return "#ffffff"


def _load_excalidraw_group(path: Path) -> tuple[VGroup, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    elements = _excalidraw_elements(data)
    app = data.get("appState") or {}
    bg = str(app.get("viewBackgroundColor") or "#ffffff")

    if not elements:
        raise ValueError("Excalidraw file has no drawable elements")

    bounds = _elements_bounds(elements)
    parts: list[Mobject] = []
    for el in elements:
        mob = _element_to_mobject(el, bounds)
        if mob is not None:
            parts.append(mob)
    return VGroup(*parts), bg


def _excalidraw_elements(data: dict[str, Any]) -> list[dict[str, Any]]:
    elements = data.get("elements") or []
    out = [el for el in elements if isinstance(el, dict) and not el.get("isDeleted")]
    out.sort(key=lambda e: (float(e.get("index") or 0),))
    return out


def _elements_bounds(elements: list[dict[str, Any]]) -> tuple[float, float, float, float]:
    xs: list[float] = []
    ys: list[float] = []
    for el in elements:
        x, y = float(el.get("x", 0)), float(el.get("y", 0))
        w = float(el.get("width") or 0)
        h = float(el.get("height") or 0)
        xs.extend([x, x + w])
        ys.extend([y, y + h])
        for pt in el.get("points") or []:
            if len(pt) >= 2:
                xs.append(x + float(pt[0]))
                ys.append(y + float(pt[1]))
    if not xs:
        return 0, 0, 800, 600
    return min(xs), min(ys), max(xs), max(ys)


def _map_point(x: float, y: float, bounds: tuple[float, float, float, float]) -> np.ndarray:
    x0, y0, x1, y1 = bounds
    cx = (x0 + x1) / 2
    cy = (y0 + y1) / 2
    mx = (x - cx) * _EXCAL_SCALE
    my = -(y - cy) * _EXCAL_SCALE
    return np.array([mx, my, 0.0])


def _stroke(el: dict[str, Any]) -> dict[str, Any]:
    return {
        "color": el.get("strokeColor") or WHITE,
        "width": max(1.5, float(el.get("strokeWidth") or 2)),
        "fill": el.get("backgroundColor") or el.get("fillStyle"),
        "opacity": float(el.get("opacity") or 100) / 100.0,
    }


def _element_to_mobject(el: dict[str, Any], bounds: tuple[float, float, float, float]) -> Mobject | None:
    etype = el.get("type")
    st = _stroke(el)
    x, y = float(el.get("x", 0)), float(el.get("y", 0))

    if etype == "rectangle":
        w, h = float(el.get("width") or 1), float(el.get("height") or 1)
        center = _map_point(x + w / 2, y + h / 2, bounds)
        rect = RoundedRectangle(
            width=max(w * _EXCAL_SCALE, 0.05),
            height=max(h * _EXCAL_SCALE, 0.05),
            corner_radius=float(el.get("roundness") or 0) * _EXCAL_SCALE * 8,
            color=st["color"],
            stroke_width=st["width"],
        )
        if st["fill"] and st["fill"] != "transparent":
            rect.set_fill(st["fill"], opacity=0.25)
        rect.move_to(center)
        return rect

    if etype == "ellipse":
        w, h = float(el.get("width") or 1), float(el.get("height") or 1)
        center = _map_point(x + w / 2, y + h / 2, bounds)
        ell = Ellipse(
            width=max(w * _EXCAL_SCALE, 0.05),
            height=max(h * _EXCAL_SCALE, 0.05),
            color=st["color"],
            stroke_width=st["width"],
        )
        ell.move_to(center)
        return ell

    if etype == "diamond":
        w, h = float(el.get("width") or 1), float(el.get("height") or 1)
        center = _map_point(x + w / 2, y + h / 2, bounds)
        d = Polygon(
            UP * h * _EXCAL_SCALE / 2,
            RIGHT * w * _EXCAL_SCALE / 2,
            DOWN * h * _EXCAL_SCALE / 2,
            LEFT * w * _EXCAL_SCALE / 2,
            color=st["color"],
            stroke_width=st["width"],
        )
        d.move_to(center)
        return d

    if etype in ("arrow", "line"):
        pts = el.get("points") or [[0, 0], [100, 0]]
        if len(pts) < 2:
            return None
        start = _map_point(x + float(pts[0][0]), y + float(pts[0][1]), bounds)
        end = _map_point(x + float(pts[-1][0]), y + float(pts[-1][1]), bounds)
        if etype == "arrow":
            return Arrow(
                start,
                end,
                color=st["color"],
                stroke_width=st["width"],
                buff=0,
                max_tip_length_to_length_ratio=0.15,
            )
        return Line(start, end, color=st["color"], stroke_width=st["width"])

    if etype == "freedraw":
        pts = el.get("points") or []
        if len(pts) < 2:
            return None
        coords = [_map_point(x + float(p[0]), y + float(p[1]), bounds) for p in pts if len(p) >= 2]
        vm = VMobject(color=st["color"], stroke_width=st["width"])
        vm.set_points_as_corners(coords)
        return vm

    if etype == "text":
        raw = str(el.get("text") or el.get("originalText") or "")
        if not raw.strip():
            return None
        fs = max(14, int(float(el.get("fontSize") or 20) * _EXCAL_SCALE * 28))
        pos = _map_point(x, y, bounds)
        t = Text(raw, font_size=fs, color=st["color"])
        t.move_to(pos)
        return t

    if etype == "image":
        return None

    return None
