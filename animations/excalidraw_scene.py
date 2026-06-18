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
    SvgImagePlacement,
    _apply_svg_transform,
    _element_bbox_center,
    _element_has_raster_image,
    _element_path_weight,
    _element_text_label,
    _element_text_label_display,
    _element_unit_colors,
    _nearest_text_label,
    animation_unit_elements,
    build_page_svg,
    convert_svg_text_to_paths,
    describe_animation_units,
    detect_svg_pages,
    extract_svg_raster_placements,
    _is_excalidraw_frame_title,
    pages_from_excalidraw_file,
    parse_view_box,
    prepare_svg_for_manim,
    resolve_page_unit_order,
    strip_embedded_image_uses,
    svg_canvas_background_color,
    unit_path_layer_count,
)

# Excalidraw Y-down → Manim Y-up
_EXCAL_SCALE = 0.012


def _is_embedded_icon(mob: Mobject) -> bool:
    return isinstance(mob, ImageMobject) or bool(getattr(mob, "excal_is_svg_icon", False))


def _is_icon_wrapper(mob: Mobject) -> bool:
    return (
        isinstance(mob, Group)
        and len(mob.submobjects) == 1
        and _is_embedded_icon(mob.submobjects[0])
    )


def _resolve_icon_path(file_path: Path) -> Path:
    """Normalize cached icon paths (legacy .svgxml → .svg)."""
    if file_path.suffix.lower() == ".svgxml" and file_path.is_file():
        svg_path = file_path.with_suffix(".svg")
        if not svg_path.exists() or svg_path.read_bytes() != file_path.read_bytes():
            svg_path.write_bytes(file_path.read_bytes())
        return svg_path
    return file_path


def _load_embedded_icon(file_path: Path) -> Mobject:
    """Load an Excalidraw embedded PNG/JPEG/SVG icon."""
    path = _resolve_icon_path(file_path)
    if path.suffix.lower() == ".svg":
        icon = SVGMobject(str(path))
        icon.excal_is_svg_icon = True
        return icon
    return ImageMobject(str(path))


def _raster_content_bbox(image_path: Path) -> tuple[int, int, int, int] | None:
    """Pixel bounds of visible raster content, excluding solid margins."""
    path = _resolve_icon_path(image_path)
    if path.suffix.lower() == ".svg":
        return None
    try:
        from PIL import Image
    except ImportError:
        return None
    try:
        img = Image.open(path)
    except OSError:
        return None

    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        return img.convert("RGBA").getbbox()

    rgb = img.convert("RGB")
    width, height = rgb.size
    pixels = rgb.load()
    min_x, min_y, max_x, max_y = width, height, -1, -1
    for y in range(height):
        for x in range(width):
            red, green, blue = pixels[x, y]
            if red < 250 or green < 250 or blue < 250:
                min_x = min(min_x, x)
                min_y = min(min_y, y)
                max_x = max(max_x, x)
                max_y = max(max_y, y)
    if max_x < 0:
        return None
    return (min_x, min_y, max_x + 1, max_y + 1)


def _trim_icon_placement(
    placement: SvgImagePlacement,
    bbox: tuple[int, int, int, int],
    image_size: tuple[int, int],
) -> SvgImagePlacement:
    """Map a pixel crop back into SVG page coordinates."""
    bx0, by0, bx1, by1 = bbox
    image_w, image_h = image_size
    if image_w <= 0 or image_h <= 0:
        return placement
    if bx0 <= 0 and by0 <= 0 and bx1 >= image_w and by1 >= image_h:
        return placement
    return SvgImagePlacement(
        file_path=placement.file_path,
        x=placement.x + placement.width * bx0 / image_w,
        y=placement.y + placement.height * by0 / image_h,
        width=placement.width * (bx1 - bx0) / image_w,
        height=placement.height * (by1 - by0) / image_h,
        order=placement.order,
        unit_index=placement.unit_index,
    )


def _load_trimmed_raster_icon(
    placement: SvgImagePlacement,
) -> tuple[Mobject, SvgImagePlacement]:
    """Load a raster icon cropped to visible content with matching page placement."""
    path = _resolve_icon_path(placement.file_path)
    if path.suffix.lower() == ".svg":
        return _load_embedded_icon(path), placement

    try:
        from PIL import Image
    except ImportError:
        return _load_embedded_icon(path), placement

    try:
        image = Image.open(path)
    except OSError:
        return _load_embedded_icon(path), placement

    image_size = image.size
    bbox = _raster_content_bbox(path)
    if bbox is None:
        return ImageMobject(str(path)), placement

    trimmed = _trim_icon_placement(placement, bbox, image_size)
    cropped = image.crop(bbox)
    if cropped.mode not in ("RGBA", "RGB"):
        cropped = cropped.convert("RGBA" if "A" in cropped.getbands() else "RGB")
    return ImageMobject(np.array(cropped)), trimmed


def animate_excalidraw_file(
    scene: Scene,
    file_path: str | Path,
    *,
    total_run_time: float = 6.0,
    hold_time: float = 1.0,
    fade_out: bool = True,
    animation_sequence: list[str] | None = None,
    page_sequences: dict[int, list[int]] | None = None,
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
                page_sequences=page_sequences,
            )
            return
        group = _load_svg_group(
            path,
            animation_sequence=animation_sequence,
            unit_order=_resolve_unit_order(0, path, animation_sequence, page_sequences),
        )
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
    _fit_svg_group(group)
    group.move_to(ORIGIN)
    _play_draw_layers(scene, group, total_run_time=total_run_time, hold_time=hold_time, fade_out=fade_out)


def _play_animation_layer(
    scene: Scene,
    layer: Mobject,
    *,
    run_time: float,
    svg_root: Mobject | None = None,
) -> None:
    if _is_embedded_icon(layer) or _is_icon_wrapper(layer):
        icon = layer.submobjects[0] if _is_icon_wrapper(layer) else layer
        icon.set_opacity(1)
        layer.set_opacity(1)
        # Above sketch strokes (z=1); labels sit to the right and rarely overlap icons.
        layer.set_z_index(10)
        if layer not in scene.mobjects:
            scene.add(layer)
        return
    elif isinstance(layer, VMobject) and layer.get_num_points() > 0:
        layer.set_z_index(1)
        has_stroke = float(layer.get_stroke_opacity() or 0) > 0.05 and float(layer.get_stroke_width() or 0) > 0
        has_fill = float(layer.get_fill_opacity() or 0) > 0.05
        if has_stroke:
            _ensure_visible_stroke(layer)
        if has_fill and not has_stroke and _is_solid_panel_fill(layer, svg_root):
            layer.set_opacity(1)
            if layer not in scene.mobjects:
                scene.add(layer)
            return
        if has_stroke and not has_fill:
            scene.play(FadeIn(layer), run_time=run_time * 0.85)
        else:
            scene.play(Create(layer), run_time=run_time)
    elif isinstance(layer, VGroup) and layer.submobjects:
        layer.set_z_index(1)
        strokes = [
            sm
            for sm in layer.submobjects
            if isinstance(sm, VMobject) and sm.get_num_points() > 0
        ]
        if strokes:
            for sm in strokes:
                if float(sm.get_stroke_opacity() or 0) > 0.05:
                    _ensure_visible_stroke(sm)
            scene.play(
                AnimationGroup(*[FadeIn(sm) for sm in strokes], lag_ratio=0),
                run_time=run_time * 0.85,
            )
        else:
            scene.play(FadeIn(layer, shift=0.05 * UP), run_time=run_time * 0.85)
    elif isinstance(layer, Mobject):
        scene.play(FadeIn(layer, shift=0.05 * UP), run_time=run_time * 0.85)


def _svg_vector_root(group: Mobject) -> Mobject | None:
    for sm in group.submobjects:
        if _is_embedded_icon(sm):
            continue
        return sm.submobjects[0] if len(sm.submobjects) == 1 else sm
    return None


def _play_draw_layers(
    scene: Scene,
    group: Mobject,
    *,
    total_run_time: float,
    hold_time: float,
    fade_out: bool,
) -> None:
    _add_panel_backgrounds(scene, group)
    layers = _animation_layers(group)
    svg_root = _svg_vector_root(group)
    animated = [layer for layer in layers if not _is_embedded_icon(layer) and not _is_icon_wrapper(layer)]
    n = max(len(animated), 1)
    per = max(0.08, (total_run_time - hold_time) / n)

    for layer in layers:
        _play_animation_layer(scene, layer, run_time=per, svg_root=svg_root)

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
    page_sequences: dict[int, list[int]] | None = None,
) -> None:
    scene.camera.background_color = bg
    n_pages = len(pages)
    transition = min(0.35, max(0.2, total_run_time * 0.05))
    page_hold = max(0.25, hold_time / n_pages)
    draw_budget = max(0.8, (total_run_time - page_hold * n_pages - transition * (n_pages - 1)) / n_pages)

    current: Mobject | None = None
    for index, page in enumerate(pages):
        page_svg = build_page_svg(svg_path, page, pages)
        unit_order = _resolve_unit_order(index, page_svg, animation_sequence, page_sequences)
        group = _load_svg_group(
            page_svg,
            animation_sequence=animation_sequence if not unit_order else None,
            unit_order=unit_order,
        )
        _fit_svg_group(group)
        group.move_to(ORIGIN)
        if current is not None:
            scene.play(FadeOut(current), run_time=transition)

        _add_panel_backgrounds(scene, group)
        layers = _animation_layers(group)
        svg_root = _svg_vector_root(group)
        animated = [layer for layer in layers if not _is_embedded_icon(layer) and not _is_icon_wrapper(layer)]
        layer_count = max(len(animated), 1)
        per = max(0.08, draw_budget / layer_count)
        for layer in layers:
            _play_animation_layer(scene, layer, run_time=per, svg_root=svg_root)

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


def _fit_svg_group(group: Group, margin: float = 0.9) -> None:
    """Fit vectors and icons together so they share one scale transform."""
    if _svg_has_drawable_vectors(_svg_vector_root(group)):
        _fit_to_frame(group, margin)
        _align_raster_icons_to_manim_text(group)
        return

    images = [sm for sm in group.get_family() if _is_embedded_icon(sm)]
    if images:
        _position_raster_images_viewbox(group, images, margin)
        return

    _fit_to_frame(group, margin)


def _local_tag(elem: ET.Element) -> str:
    tag = elem.tag
    return tag.split("}")[-1] if "}" in tag else tag


_SVG_NUM_RE = re.compile(r"[-+]?(?:\d*\.\d+|\d+)(?:[eE][-+]?\d+)?")


def _svg_path_page_points(
    elem: ET.Element,
    parent_map: dict[ET.Element, ET.Element],
) -> list[tuple[float, float]]:
    """Sample one SVG path's coordinates in flattened page space."""
    nums = [float(n) for n in _SVG_NUM_RE.findall(elem.get("d") or "")]
    if len(nums) < 2:
        return []

    transforms: list[str] = []
    cur = parent_map.get(elem)
    while cur is not None and _local_tag(cur) != "svg":
        transform = cur.get("transform")
        if transform:
            transforms.append(transform)
        cur = parent_map.get(cur)

    points: list[tuple[float, float]] = []
    for index in range(0, len(nums) - 1, 2):
        x, y = nums[index], nums[index + 1]
        for transform in reversed(transforms):
            x, y = _apply_svg_transform(x, y, transform)
        points.append((x, y))
    return points


def _svg_path_manim_map(group: Group, root: ET.Element) -> dict[int, VMobject]:
    """Map SVG path document order to Manim path submobjects."""
    svg = _svg_vector_root(group)
    if svg is None:
        return {}

    root_mob = svg.submobjects[0] if len(svg.submobjects) == 1 else svg
    svg_paths = [elem for elem in root.iter() if _local_tag(elem) == "path"]
    manim_paths = [
        sm
        for sm in root_mob.submobjects
        if isinstance(sm, VMobject) and sm.get_num_points() > 0
    ]
    if len(svg_paths) != len(manim_paths):
        return {}

    return {index: manim_paths[index] for index in range(len(svg_paths))}


def _text_label_ink_bounds(
    root: ET.Element,
    path_map: dict[int, VMobject],
) -> list[dict[str, float | str]]:
    """Collect SVG and Manim left edges for each converted text label."""
    parent_map: dict[ET.Element, ET.Element] = {
        child: parent for parent in root.iter() for child in parent
    }
    svg_paths = [elem for elem in root.iter() if _local_tag(elem) == "path"]
    entries: list[dict[str, float | str]] = []

    for group in root.iter():
        label = group.get("data-excal-text")
        if not label:
            continue
        path_children = [child for child in group if _local_tag(child) == "path"]
        if not path_children:
            continue

        ink_min_x = float("inf")
        ink_min_y = float("inf")
        ink_max_x = float("-inf")
        ink_max_y = float("-inf")
        manim_left = float("inf")
        manim_center_y_sum = 0.0
        manim_center_y_count = 0

        for path_elem in path_children:
            points = _svg_path_page_points(path_elem, parent_map)
            if not points:
                continue
            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            ink_min_x = min(ink_min_x, min(xs))
            ink_max_x = max(ink_max_x, max(xs))
            ink_min_y = min(ink_min_y, min(ys))
            ink_max_y = max(ink_max_y, max(ys))

            try:
                manim_path = path_map[svg_paths.index(path_elem)]
            except (ValueError, KeyError):
                continue
            manim_left = min(manim_left, float(manim_path.get_left()[0]))
            manim_center_y_sum += float(manim_path.get_center()[1])
            manim_center_y_count += 1

        if ink_min_x == float("inf") or manim_left == float("inf") or manim_center_y_count <= 0:
            continue

        entries.append(
            {
                "label": label,
                "ink_min_x": ink_min_x,
                "ink_min_y": ink_min_y,
                "ink_max_x": ink_max_x,
                "ink_max_y": ink_max_y,
                "center_y": (ink_min_y + ink_max_y) / 2,
                "manim_left": manim_left,
                "manim_center_y": manim_center_y_sum / manim_center_y_count,
            }
        )
    return entries


def _svg_text_label_entries(root: ET.Element) -> list[dict[str, float | str]]:
    """SVG-space label bounds for pairing icons with text units."""
    parent_map: dict[ET.Element, ET.Element] = {
        child: parent for parent in root.iter() for child in parent
    }
    entries: list[dict[str, float | str]] = []
    for group in root.iter():
        label = group.get("data-excal-text")
        if not label:
            continue
        path_children = [child for child in group if _local_tag(child) == "path"]
        if not path_children:
            continue

        ink_min_x = float("inf")
        ink_min_y = float("inf")
        ink_max_x = float("-inf")
        ink_max_y = float("-inf")
        for path_elem in path_children:
            points = _svg_path_page_points(path_elem, parent_map)
            if not points:
                continue
            xs = [point[0] for point in points]
            ys = [point[1] for point in points]
            ink_min_x = min(ink_min_x, min(xs))
            ink_max_x = max(ink_max_x, max(xs))
            ink_min_y = min(ink_min_y, min(ys))
            ink_max_y = max(ink_max_y, max(ys))

        if ink_min_x == float("inf"):
            continue

        entries.append(
            {
                "label": label,
                "ink_min_x": ink_min_x,
                "ink_min_y": ink_min_y,
                "ink_max_x": ink_max_x,
                "ink_max_y": ink_max_y,
                "center_y": (ink_min_y + ink_max_y) / 2,
            }
        )
    return entries


def _text_unit_for_icon(
    placement: Any,
    render_path: Path,
    units: list[ET.Element],
) -> int | None:
    try:
        root = ET.parse(render_path).getroot()
    except ET.ParseError:
        return None

    text_entry = _text_label_for_icon(placement, _svg_text_label_entries(root))
    if text_entry is None:
        return None

    label = str(text_entry["label"])
    for unit_index, unit in enumerate(units):
        for elem in unit.iter():
            if elem.get("data-excal-text") == label:
                return unit_index
    return None


def _collect_icon_wrappers(group: Mobject) -> dict[int, Mobject]:
    wrappers: dict[int, Mobject] = {}
    for submob in group.submobjects:
        if not _is_icon_wrapper(submob):
            continue
        icon = submob.submobjects[0]
        unit_index = getattr(icon, "excal_unit_index", None)
        if unit_index is None:
            continue
        wrappers[int(unit_index)] = submob
    return wrappers


def _text_label_for_icon(
    placement: Any,
    text_entries: list[dict[str, float | str]],
) -> dict[str, float | str] | None:
    """Match one raster icon to the label sitting to its right in the same row."""
    icon_top = placement.y
    icon_bottom = placement.y + placement.height
    icon_center_y = placement.y + placement.height / 2
    icon_right = placement.x + placement.width

    best: dict[str, float | str] | None = None
    best_score = float("inf")
    for entry in text_entries:
        if float(entry["ink_max_y"]) < icon_top or float(entry["ink_min_y"]) > icon_bottom:
            continue

        gap_svg = float(entry["ink_min_x"]) - icon_right
        if gap_svg < -8 or gap_svg > 120:
            continue

        dy = abs(float(entry["center_y"]) - icon_center_y)
        score = dy * 4 + abs(gap_svg)
        if score < best_score:
            best_score = score
            best = entry
    return best


def _align_raster_icons_to_manim_text(group: Group) -> None:
    """Preserve SVG icon→text gaps using Manim-rendered text ink positions."""
    render_path = getattr(group, "excal_render_path", None)
    vb = getattr(group, "excal_view_box", None)
    svg = _svg_vector_root(group)
    if render_path is None or vb is None or svg is None:
        return

    try:
        root = ET.parse(render_path).getroot()
    except ET.ParseError:
        return

    vb_x, vb_y, vb_w, vb_h = vb
    if vb_w <= 0 or svg.width <= 0:
        return

    path_map = _svg_path_manim_map(group, root)
    if not path_map:
        return

    text_entries = _text_label_ink_bounds(root, path_map)
    if not text_entries:
        return

    for submob in group.submobjects:
        if not isinstance(submob, Group) or len(submob.submobjects) != 1:
            continue
        icon = submob.submobjects[0]
        if not _is_embedded_icon(icon):
            continue

        placement = getattr(icon, "excal_placement", None)
        if placement is None:
            continue

        text_entry = _text_label_for_icon(placement, text_entries)
        if text_entry is None:
            continue

        gap_svg = float(text_entry["ink_min_x"]) - (placement.x + placement.width)
        if gap_svg < -40:
            continue

        gap_manim = gap_svg / vb_w * svg.width
        target_right = float(text_entry["manim_left"]) - gap_manim
        shift_x = target_right - submob.get_right()[0]
        if abs(shift_x) > 1e-4:
            submob.shift(RIGHT * shift_x)

        # SVGMobject text and viewBox icon placement use opposite Y conventions;
        # snap icon center to the rendered text center instead of preserving SVG Y gap.
        target_center_y = float(text_entry["manim_center_y"])
        shift_y = target_center_y - submob.get_center()[1]
        if abs(shift_y) > 1e-4:
            submob.shift(UP * shift_y)


def _attach_raster_icons(
    svg: Mobject,
    render_path: Path,
    vb: tuple[float, float, float, float],
) -> list[Mobject]:
    """Build icon layers at flat SVG page coordinates (viewBox scaled)."""
    placements = extract_svg_raster_placements(render_path)
    if not placements:
        return []

    vb_x, vb_y, vb_w, vb_h = vb
    if vb_w <= 0 or vb_h <= 0:
        return []

    attached: list[Mobject] = []
    for placement in placements:
        try:
            img, placement = _load_trimmed_raster_icon(placement)
        except OSError:
            continue
        if placement.width <= 0 or placement.height <= 0:
            continue

        img.excal_placement = placement
        img.excal_unit_index = placement.unit_index
        img.set_opacity(0)

        _stretch_mobject_to_rect(
            img,
            placement.width / vb_w * svg.width,
            placement.height / vb_h * svg.height,
        )
        top_left = _viewbox_point_to_manim(svg, placement.x, placement.y, vb_x, vb_y, vb_w, vb_h)
        img.move_to(top_left, aligned_edge=UL)
        attached.append(Group(img))
    return attached


def _svg_has_drawable_vectors(svg: Mobject | None) -> bool:
    if svg is None:
        return False
    for mob in svg.get_family():
        if isinstance(mob, VMobject) and mob.get_num_points() > 0:
            return True
    return False


def _viewbox_page_size(vb_w: float, vb_h: float, margin: float) -> tuple[float, float]:
    """Map an SVG viewBox aspect ratio onto the Manim frame."""
    fw = config.frame_width * margin
    fh = config.frame_height * margin
    if vb_w <= 0 or vb_h <= 0:
        return fw, fh
    if vb_w / vb_h >= fw / fh:
        return fw, fw * vb_h / vb_w
    return fh * vb_w / vb_h, fh


def _viewbox_scales(
    vb_w: float,
    vb_h: float,
    *,
    width: float,
    height: float,
) -> tuple[float, float]:
    if vb_w <= 0 or vb_h <= 0:
        return 1.0, 1.0
    return width / vb_w, height / vb_h


def _viewbox_point_to_manim(
    svg: Mobject,
    x: float,
    y: float,
    vb_x: float,
    vb_y: float,
    vb_w: float,
    vb_h: float,
) -> np.ndarray:
    """Map one SVG viewBox point onto a fitted SVGMobject."""
    nx = (x - vb_x) / vb_w
    ny = (y - vb_y) / vb_h
    origin = svg.get_corner(UL)
    return origin + RIGHT * (nx * svg.width) + DOWN * (ny * svg.height)


def _stretch_mobject_to_rect(img: Mobject, target_w: float, target_h: float) -> None:
    """Match an icon to the exact SVG placement width/height after viewBox scaling."""
    if target_w <= 0 or target_h <= 0:
        return
    img.stretch_to_fit_width(max(target_w, 0.01))
    img.stretch_to_fit_height(max(target_h, 0.01))


def _position_raster_images_viewbox(
    group: Group,
    images: list[Mobject],
    margin: float,
) -> None:
    """Place raster images on image-only pages using the SVG viewBox."""
    vb = getattr(group, "excal_view_box", None)
    if vb is None:
        render_path = getattr(group, "excal_render_path", None)
        if render_path is not None:
            try:
                vb = parse_view_box(ET.parse(render_path).getroot())
                group.excal_view_box = vb
            except ET.ParseError:
                vb = None
    if vb is None:
        vb = (0.0, 0.0, 800.0, 450.0)
    vb_x, vb_y, vb_w, vb_h = vb
    page_w, page_h = _viewbox_page_size(vb_w, vb_h, margin)
    scale_x, scale_y = _viewbox_scales(vb_w, vb_h, width=page_w, height=page_h)
    page_origin = UP * (page_h / 2) + LEFT * (page_w / 2)
    for img in images:
        placement = getattr(img, "excal_placement", None)
        if placement is None:
            continue
        _stretch_mobject_to_rect(
            img,
            placement.width * scale_x,
            placement.height * scale_y,
        )
        nx = (placement.x - vb_x) / vb_w
        ny = (placement.y - vb_y) / vb_h
        top_left = page_origin + RIGHT * (nx * page_w) + DOWN * (ny * page_h)
        img.move_to(top_left, aligned_edge=UL)


def _collect_embedded_icons(group: Mobject) -> dict[int, Mobject]:
    icons: dict[int, Mobject] = {}
    for sm in group.get_family():
        if not _is_embedded_icon(sm):
            continue
        unit_index = getattr(sm, "excal_unit_index", None)
        if unit_index is None:
            continue
        icons[int(unit_index)] = sm
    return icons


def _ensure_visible_stroke(mob: VMobject, min_width: float = 2.0) -> None:
    for sm in mob.get_family():
        w = float(sm.get_stroke_width() or 0)
        if w > 0:
            sm.set_stroke(width=max(w, min_width))


def _unit_stroke_layer(strokes: list[Mobject]) -> Mobject:
    """One animation step per Excalidraw unit (not per path)."""
    if not strokes:
        return VGroup()
    if len(strokes) == 1:
        return strokes[0]
    return VGroup(*strokes)


def _resolve_draw_order(unit_order: list[int] | None, unit_count: int) -> list[int]:
    """Normalize saved draw-order indices without mutating the SVG."""
    if unit_count <= 0:
        return []
    default = list(range(unit_count))
    if not unit_order:
        return default
    seen: set[int] = set()
    ordered: list[int] = []
    for raw in unit_order:
        idx = int(raw)
        if idx in seen or idx < 0 or idx >= unit_count:
            continue
        ordered.append(idx)
        seen.add(idx)
    for idx in default:
        if idx not in seen:
            ordered.append(idx)
    return ordered


def _is_vector_logo_duplicate(unit: ET.Element) -> bool:
    """True for hand-drawn black logo traces, not cell boxes or colored decorations."""
    fill, stroke = _element_unit_colors(unit)
    fill_key = (fill or "").strip().lower()
    stroke_key = (stroke or "").strip().lower()
    path_weight = _element_path_weight(unit)

    if fill_key in ("#000000", "#000", "black") and path_weight > 500:
        return True

    if not fill_key and stroke_key in ("#000000", "#000", "black") and path_weight < 500:
        return True

    return False


def _unit_has_image_mask(unit: ET.Element) -> bool:
    return any(_local_tag(elem) == "mask" for elem in unit.iter())


def _should_shadow_logo_trace(
    unit: ET.Element,
    *,
    near_label: str | None,
    protected_labels: set[str],
    unit_label: str = "",
    has_raster_icons: bool = False,
) -> bool:
    """Hide Excalidraw image-mask slash traces when a raster icon replaces them."""
    if _element_has_raster_image(unit) or _element_text_label(unit):
        return False

    if not _is_vector_logo_duplicate(unit):
        return False

    label_lower = unit_label.lower()

    if near_label in protected_labels:
        return True

    if near_label and near_label.lower() in (
        "data",
        "science",
        "ai",
        "apps",
        "python",
        "not the only",
        "language...",
    ):
        if near_label not in protected_labels:
            return False

    if label_lower and any(
        token in label_lower
        for token in ("(data)", "(ai)", "(python)", "not the only")
    ):
        if near_label not in protected_labels:
            return False

    if _unit_has_image_mask(unit):
        if near_label is not None:
            return False
        if not has_raster_icons:
            return False
        if not label_lower:
            return True
        if ("illustration #" in label_lower or "icon #" in label_lower) and not any(
            token in label_lower for token in ("(data)", "(ai)", "(python)")
        ):
            return True
        return False

    fill, _ = _element_unit_colors(unit)
    fill_key = (fill or "").strip().lower()
    if fill_key in ("#000000", "#000", "black") and _element_path_weight(unit) > 500:
        if near_label in protected_labels:
            return True
        if near_label is None and ("illustration #" in label_lower or "icon #" in label_lower):
            return not any(token in label_lower for token in ("(data)", "(ai)", "(python)"))

    return False


def _shadowed_vector_logo_units(
    render_path: Path,
    units: list[ET.Element],
    raster_paired_text_units: set[int],
    *,
    source_svg_path: Path | None = None,
) -> set[int]:
    """Hand-drawn vector logo traces hidden when a raster icon covers the same label."""
    try:
        root = ET.parse(render_path).getroot()
    except ET.ParseError:
        return set()

    parent_map: dict[ET.Element, ET.Element] = {
        child: parent for parent in root.iter() for child in parent
    }
    vb = parse_view_box(root)
    _, _, vb_w, vb_h = vb

    protected_labels: set[str] = set()
    for idx in raster_paired_text_units:
        if idx < 0 or idx >= len(units):
            continue
        label = _element_text_label_display(units[idx]).strip()
        if label:
            protected_labels.add(label)

    text_units: list[tuple[str, tuple[float, float] | None]] = []
    for unit in units:
        if not _element_text_label(unit):
            continue
        label = _element_text_label_display(unit).strip()
        text_units.append(
            (label, _element_bbox_center(unit, parent_map))
        )

    has_raster_icons = bool(extract_svg_raster_placements(render_path))

    unit_labels: dict[int, str] = {}
    if source_svg_path is not None:
        for info in describe_animation_units(source_svg_path):
            unit_labels[info.index] = info.label

    shadowed: set[int] = set()
    for idx, unit in enumerate(units):
        label = unit_labels.get(idx, "") or _element_text_label_display(unit)
        if _is_excalidraw_frame_title(unit, label, parent_map, view_box=vb):
            shadowed.add(idx)
            continue
        if _element_has_raster_image(unit) or _element_text_label(unit):
            continue
        if _element_path_weight(unit) <= 0:
            continue
        center = _element_bbox_center(unit, parent_map)
        near = _nearest_text_label(
            center,
            text_units,
            max_dist=max(vb_w, vb_h) * 0.35,
        )
        if _should_shadow_logo_trace(
            unit,
            near_label=near,
            protected_labels=protected_labels,
            unit_label=unit_labels.get(idx, ""),
            has_raster_icons=has_raster_icons,
        ):
            shadowed.add(idx)
    return shadowed


def _animation_layers(group: Mobject) -> list[Mobject]:
    """Collect drawable strokes and raster images in draw-order."""
    render_path = getattr(group, "excal_render_path", None)
    unit_order = getattr(group, "excal_unit_order", None)
    vector_roots = [sm for sm in group.submobjects if not _is_icon_wrapper(sm)]
    icon_wrappers = _collect_icon_wrappers(group)

    all_strokes: list[Mobject] = []
    for svg_root in vector_roots:
        root = svg_root.submobjects[0] if len(svg_root.submobjects) == 1 else svg_root
        found = _collect_stroke_layers(root, svg_root=root)
        if found:
            all_strokes.extend(found)
        elif len(svg_root.submobjects) > 1:
            all_strokes.extend(
                [sm for sm in svg_root.submobjects if not _is_background_fill(sm, root)]
            )

    if render_path is not None and (icon_wrappers or animation_unit_elements(render_path)):
        units = animation_unit_elements(render_path)
        if units:
            layers: list[Mobject] = []
            offset = 0
            stroke_ranges: list[tuple[int, int]] = []
            for unit in units:
                count = unit_path_layer_count(unit)
                start = offset
                if count > 0 and offset < len(all_strokes):
                    offset = min(offset + count, len(all_strokes))
                stroke_ranges.append((start, offset))

            icon_before_text: dict[int, Mobject] = {}
            orphan_icons: dict[int, Mobject] = {}
            for icon_unit, wrapper in icon_wrappers.items():
                icon = wrapper.submobjects[0]
                placement = getattr(icon, "excal_placement", None)
                text_unit = (
                    _text_unit_for_icon(placement, render_path, units)
                    if placement is not None
                    else None
                )
                if text_unit is not None:
                    icon_before_text[text_unit] = wrapper
                else:
                    orphan_icons[icon_unit] = wrapper

            shadowed_vectors = _shadowed_vector_logo_units(
                render_path,
                units,
                set(icon_before_text.keys()),
                source_svg_path=getattr(group, "excal_source_path", None),
            )

            draw_order = _resolve_draw_order(unit_order, len(units))
            for unit_index in draw_order:
                if unit_index in icon_before_text:
                    layers.append(icon_before_text[unit_index])
                if unit_index in orphan_icons:
                    layers.append(orphan_icons[unit_index])
                if unit_index in shadowed_vectors:
                    continue
                start, end = stroke_ranges[unit_index]
                if start < end:
                    layers.append(_unit_stroke_layer(all_strokes[start:end]))

            if offset < len(all_strokes):
                tail = all_strokes[offset:]
                shadowed_stroke_indices: set[int] = set()
                cursor = 0
                for unit_index, unit in enumerate(units):
                    count = unit_path_layer_count(unit)
                    if unit_index in shadowed_vectors:
                        shadowed_stroke_indices.update(range(cursor, cursor + count))
                    cursor += count
                for stroke_index, stroke in enumerate(tail, start=offset):
                    if stroke_index in shadowed_stroke_indices:
                        continue
                    if stroke not in layers:
                        layers.append(stroke)
            for wrapper in icon_wrappers.values():
                if wrapper not in layers:
                    layers.append(wrapper)
            if layers:
                return layers

    if not all_strokes and vector_roots:
        all_strokes = list(vector_roots)
    layers = list(all_strokes)
    for wrapper in sorted(icon_wrappers.values(), key=lambda mob: getattr(mob.submobjects[0], "excal_unit_index", 0)):
        if wrapper not in layers:
            layers.append(wrapper)
    if layers:
        return layers
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
            and not _is_frame_outline(c, svg_root)
            and not _is_cell_background(c, svg_root)
        ]
        if not child_strokes:
            if (
                not _is_background_fill(mob, svg_root)
                and not _is_frame_outline(mob, svg_root)
                and not _is_cell_background(mob, svg_root)
            ):
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


def _is_frame_outline(mob: Mobject, root: Mobject | None = None) -> bool:
    """Skip hollow full-frame rectangles (Excalidraw slide borders)."""
    if not isinstance(mob, VMobject):
        return False
    if float(mob.get_fill_opacity() or 0) > 0.08:
        return False
    if float(mob.get_stroke_opacity() or 0) < 0.05:
        return False
    if root is None or root.width < 0.01 or root.height < 0.01:
        return False
    return mob.width >= root.width * 0.88 and mob.height >= root.height * 0.88


def _fill_rgb(mob: VMobject) -> tuple[float, float, float] | None:
    try:
        rgb = mob.get_fill_color()
        return float(rgb[0]), float(rgb[1]), float(rgb[2])
    except (TypeError, IndexError, AttributeError):
        return None


def _is_solid_panel_fill(mob: VMobject, root: Mobject | None = None) -> bool:
    """Large saturated fill-only shapes (note cards), not text glyph paths."""
    if float(mob.get_fill_opacity() or 0) < 0.35:
        return False
    if float(mob.get_stroke_opacity() or 0) > 0.05 and float(mob.get_stroke_width() or 0) > 0:
        return False
    if root is not None and root.width > 0.01 and root.height > 0.01:
        if mob.width < root.width * 0.08 or mob.height < root.height * 0.08:
            return False
    rgb = _fill_rgb(mob)
    if rgb is None:
        return False
    if max(rgb) > 0.97 and min(rgb) > 0.94:
        return False
    return (max(rgb) - min(rgb)) > 0.12


def _is_neutral_light_panel_fill(mob: VMobject) -> bool:
    """Pale gray grid/card panels (not white, not vivid note-card colors)."""
    rgb = _fill_rgb(mob)
    if rgb is None:
        return False
    mx, mn = max(rgb), min(rgb)
    if mx > 0.97 and mn > 0.94:
        return False
    return (mx - mn) < 0.08 and mx > 0.85


def _is_cell_background(mob: Mobject, root: Mobject | None = None) -> bool:
    """Light neutral panel fills — show immediately behind icons/text."""
    if not isinstance(mob, VMobject):
        return False
    if float(mob.get_fill_opacity() or 0) < 0.35:
        return False
    if not _is_neutral_light_panel_fill(mob):
        return False
    if root is None or root.width < 0.01 or root.height < 0.01:
        return False
    if mob.width >= root.width * 0.88 and mob.height >= root.height * 0.88:
        return False
    return mob.width >= root.width * 0.12 and mob.height >= root.height * 0.08


def _add_panel_backgrounds(scene: Scene, group: Mobject) -> None:
    """Add light grid panels to the scene before stroke animation begins."""
    for svg_root in group.submobjects:
        if _is_embedded_icon(svg_root):
            continue
        root = svg_root.submobjects[0] if len(svg_root.submobjects) == 1 else svg_root
        for mob in root.get_family():
            if _is_cell_background(mob, root):
                mob.set_opacity(1)
                if mob not in scene.mobjects:
                    scene.add(mob)


def _resolve_unit_order(
    page_index: int,
    page_svg: Path,
    animation_sequence: list[str] | None,
    page_sequences: dict[int, list[int]] | None,
) -> list[int] | None:
    converted = convert_svg_text_to_paths(page_svg)
    unit_count = len(animation_unit_elements(converted))
    if unit_count < 2:
        return None
    has_saved = bool(
        page_sequences
        and (page_index in page_sequences or str(page_index) in page_sequences)
    )
    if not has_saved and not animation_sequence:
        return None
    order = resolve_page_unit_order(
        page_index,
        unit_count,
        page_sequences=page_sequences,
        animation_sequence=animation_sequence,
        page_svg=converted,
    )
    if has_saved:
        return order
    default = list(range(unit_count))
    if order != default:
        return order
    return None


def _load_svg_group(
    path: Path,
    animation_sequence: list[str] | None = None,
    unit_order: list[int] | None = None,
) -> Group:
    """Load SVG vectors plus embedded raster images from Excalidraw exports."""
    cleaned = _strip_svg_background_rect(path)
    render_path = prepare_svg_for_manim(
        cleaned,
        animation_sequence=animation_sequence,
        unit_order=unit_order,
    )
    mobject_path = strip_embedded_image_uses(render_path)
    svg = SVGMobject(str(mobject_path))
    _hide_background_submobjects(svg)

    try:
        root = ET.parse(render_path).getroot()
    except ET.ParseError:
        root = None
    vb = parse_view_box(root) if root is not None else (0.0, 0.0, max(svg.width, 1.0), max(svg.height, 1.0))

    icons = _attach_raster_icons(svg, render_path, vb)
    group = Group(svg, *icons)
    group.excal_render_path = render_path
    group.excal_source_path = path
    group.excal_view_box = vb
    group.excal_unit_order = unit_order
    return group


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
