"""Parse Excalidraw (.excalidraw) and SVG exports for Manim animation."""

from __future__ import annotations

import base64
import copy
import json
import re
import xml.etree.ElementTree as ET
import zlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont


def load_scene_file(path: Path) -> dict[str, Any]:
    """Load .excalidraw JSON or pass-through for SVG."""
    suffix = path.suffix.lower()
    if suffix == ".svg":
        return {"format": "svg", "path": str(path.resolve())}
    if suffix in (".excalidraw", ".json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("type") != "excalidraw":
            raise ValueError("JSON file is not Excalidraw format")
        return {"format": "excalidraw", "data": data, "path": str(path.resolve())}
    raise ValueError(f"Unsupported file type: {suffix} (use .svg or .excalidraw)")


def excalidraw_elements(data: dict[str, Any]) -> list[dict[str, Any]]:
    elements = data.get("elements") or []
    out: list[dict[str, Any]] = []
    for el in elements:
        if not isinstance(el, dict):
            continue
        if el.get("isDeleted"):
            continue
        if el.get("type") in ("selection", "embeddable"):
            continue
        out.append(el)

    def sort_key(el: dict[str, Any]) -> tuple:
        anim = el.get("customData", {}) or {}
        order = anim.get("animOrder")
        if order is None and str(el.get("name", "")).startswith("anim:"):
            try:
                order = int(str(el["name"]).split(":")[1])
            except (ValueError, IndexError):
                order = None
        return (
            order if order is not None else 10_000,
            float(el.get("index") or 0),
        )

    out.sort(key=sort_key)
    return out


def svg_layer_paths(svg_path: Path) -> list[Path]:
    """Split SVG into one mini-SVG per animatable layer (preserves draw order)."""
    text = svg_path.read_text(encoding="utf-8")
    try:
        root = ET.fromstring(text)
    except ET.ParseError as exc:
        raise ValueError(f"Invalid SVG: {exc}") from exc

    tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
    if tag != "svg":
        raise ValueError("Root element is not <svg>")

    layers: list[str] = []

    def is_drawable(elem: ET.Element) -> bool:
        local = elem.tag.split("}")[-1]
        return local in ("path", "line", "rect", "circle", "ellipse", "polyline", "polygon", "text", "g")

    children = list(root)
    drawable_children = [c for c in children if is_drawable(c)]
    if len(drawable_children) >= 2:
        for child in drawable_children:
            layers.append(_wrap_svg_fragment(root, child))
    else:
        for elem in root.iter():
            local = elem.tag.split("}")[-1]
            if local == "path":
                layers.append(_wrap_svg_fragment(root, elem))

    if not layers:
        layers.append(text)

    cache_dir = svg_path.parent / ".excalidraw_layers" / svg_path.stem
    cache_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for i, layer_svg in enumerate(layers):
        out = cache_dir / f"layer_{i:03d}.svg"
        out.write_text(layer_svg, encoding="utf-8")
        paths.append(out)
    return paths


def _wrap_svg_fragment(root: ET.Element, elem: ET.Element) -> str:
    view_box = root.get("viewBox") or f"0 0 {root.get('width', '800')} {root.get('height', '600')}"
    width = root.get("width", "800")
    height = root.get("height", "600")
    defs_parts: list[str] = []
    style_parts: list[str] = []
    for child in root:
        local = child.tag.split("}")[-1]
        if local == "defs":
            defs_parts.append(ET.tostring(child, encoding="unicode"))
        elif local == "style":
            style_parts.append(ET.tostring(child, encoding="unicode"))

    elem_s = ET.tostring(elem, encoding="unicode")
    bg = ""
    if root.get("style") and "background" in (root.get("style") or ""):
        bg = '<rect width="100%" height="100%" fill="#000000"/>'

    return (
        f'<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{view_box}" width="{width}" height="{height}">'
        f"{''.join(defs_parts)}{''.join(style_parts)}{bg}{elem_s}</svg>"
    )


def scene_background(scene_data: dict[str, Any]) -> str:
    if scene_data.get("format") == "excalidraw":
        app = (scene_data.get("data") or {}).get("appState") or {}
        return str(app.get("viewBackgroundColor") or "#ffffff")
    path = scene_data.get("path")
    if path:
        canvas = svg_canvas_background_color(Path(path))
        if canvas:
            return canvas
    return "#ffffff"


def svg_canvas_background_color(svg_path: Path) -> str | None:
    """Read full-canvas background fill from an Excalidraw SVG export."""
    try:
        root = ET.parse(svg_path).getroot()
    except ET.ParseError:
        return None

    _, _, vb_w, vb_h = parse_view_box(root)
    for elem in root:
        if _local_tag(elem) != "rect":
            continue
        fill = (elem.get("fill") or "").strip()
        if not fill:
            continue
        w_attr = elem.get("width", "")
        h_attr = elem.get("height", "")
        if w_attr in ("100%", str(int(vb_w)) if vb_w == int(vb_w) else str(vb_w)) and h_attr in (
            "100%",
            str(int(vb_h)) if vb_h == int(vb_h) else str(vb_h),
        ):
            return fill
        if _rect_covers_view_box(elem, vb_w, vb_h):
            return fill
    return None


def _rect_covers_view_box(elem: ET.Element, vb_w: float, vb_h: float) -> bool:
    try:
        w = float(str(elem.get("width", "0")).replace("%", ""))
        h = float(str(elem.get("height", "0")).replace("%", ""))
    except ValueError:
        return elem.get("width") == "100%" and elem.get("height") == "100%"
    return w >= vb_w * 0.95 and h >= vb_h * 0.95


def parse_view_box(root: ET.Element) -> tuple[float, float, float, float]:
    vb = root.get("viewBox") or ""
    parts = vb.split()
    if len(parts) >= 4:
        return float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3])
    try:
        w = float(str(root.get("width", "800")).replace("px", ""))
        h = float(str(root.get("height", "600")).replace("px", ""))
    except ValueError:
        w, h = 800.0, 600.0
    return 0.0, 0.0, w, h


def _local_tag(elem: ET.Element) -> str:
    return elem.tag.split("}")[-1] if "}" in elem.tag else elem.tag


def _parse_translate(transform: str) -> tuple[float, float]:
    if not transform:
        return 0.0, 0.0
    m = re.search(r"translate\(\s*([-\d.eE+]+)\s+([-\d.eE+]+)\s*\)", transform)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(r"translate\(\s*([-\d.eE+]+)\s*,\s*([-\d.eE+]+)\s*\)", transform)
    if m:
        return float(m.group(1)), float(m.group(2))
    return 0.0, 0.0


def _parent_chain(elem: ET.Element, parent_map: dict[ET.Element, ET.Element]) -> list[ET.Element]:
    chain: list[ET.Element] = []
    cur: ET.Element | None = elem
    while cur is not None:
        chain.append(cur)
        cur = parent_map.get(cur)
    return chain


def iter_svg_text_elements(svg_path: Path) -> list[dict[str, Any]]:
    """Extract <text> nodes from Excalidraw SVG (Manim SVGMobject skips these)."""
    try:
        root = ET.parse(svg_path).getroot()
    except ET.ParseError:
        return []

    parent_map: dict[ET.Element, ET.Element] = {child: parent for parent in root.iter() for child in parent}
    x0, y0, vb_w, vb_h = parse_view_box(root)
    items: list[dict[str, Any]] = []

    for idx, elem in enumerate(root.iter()):
        if _local_tag(elem) != "text":
            continue
        content = "".join(elem.itertext()).strip()
        if not content:
            continue
        tx, ty = float(elem.get("x", 0) or 0), float(elem.get("y", 0) or 0)
        for ancestor in _parent_chain(elem, parent_map)[1:]:
            ox, oy = _parse_translate(ancestor.get("transform") or "")
            tx += ox
            ty += oy
        fs_raw = str(elem.get("font-size") or "24").replace("px", "")
        try:
            font_size_px = float(fs_raw)
        except ValueError:
            font_size_px = 24.0
        fill = elem.get("fill") or "#ffffff"
        anchor = elem.get("text-anchor") or "start"
        font_family = elem.get("font-family") or ""
        font_weight = elem.get("font-weight") or "normal"
        items.append(
            {
                "order": idx,
                "text": content,
                "x": tx,
                "y": ty,
                "x0": x0,
                "y0": y0,
                "vb_w": vb_w,
                "vb_h": vb_h,
                "font_size_px": font_size_px,
                "fill": fill,
                "anchor": anchor,
                "font_family": font_family,
                "font_weight": font_weight,
            }
        )
    return items


_FONT_FACE_RE = re.compile(
    r"font-family:\s*([^;\"']+)[^;]*;\s*src:\s*url\(\s*data:font/"
    r"(woff2|woff|truetype|opentype);base64,([^)]+)\)",
    re.IGNORECASE,
)

_FONT_EXT = {
    "woff2": "woff2",
    "woff": "woff",
    "truetype": "ttf",
    "opentype": "otf",
}


def primary_font_family(font_family: str) -> str:
    """First family from a CSS font-family list."""
    if not font_family:
        return ""
    return font_family.split(",")[0].strip().strip("'\"")


def extract_svg_embedded_fonts(
    svg_path: Path,
    cache_dir: Path | None = None,
) -> dict[str, Path]:
    """Extract embedded @font-face blobs from Excalidraw SVG exports."""
    try:
        raw = svg_path.read_text(encoding="utf-8")
    except OSError:
        return {}

    cache_dir = cache_dir or (svg_path.parent / ".excalidraw_render" / "fonts")
    cache_dir.mkdir(parents=True, exist_ok=True)
    fonts: dict[str, Path] = {}

    for match in _FONT_FACE_RE.finditer(raw):
        name = match.group(1).strip().strip("'\"")
        fmt = match.group(2).lower()
        ext = _FONT_EXT.get(fmt, fmt)
        try:
            payload = base64.b64decode(match.group(3))
        except ValueError:
            continue
        safe = re.sub(r"[^\w.-]+", "_", name) or "embedded"
        dest = cache_dir / f"{safe}.{ext}"
        if not dest.exists() or dest.read_bytes() != payload:
            dest.write_bytes(payload)
        fonts[name] = dest
    return fonts


def resolve_text_font(
    font_family: str,
    embedded: dict[str, Path],
) -> tuple[str, Path | None]:
    """Pick an embedded font file matching the SVG text's font-family."""
    primary = primary_font_family(font_family)
    if primary and primary in embedded:
        return primary, embedded[primary]
    if primary:
        for name, path in embedded.items():
            if name.lower() == primary.lower():
                return name, path
    if embedded:
        name = next(iter(embedded))
        return name, embedded[name]
    return primary or "sans-serif", None


def prepare_svg_for_manim(
    svg_path: Path,
    animation_sequence: list[str] | None = None,
) -> Path:
    """Return an SVG ready for SVGMobject: text as paths, optional draw-order."""
    converted = convert_svg_text_to_paths(svg_path)
    if animation_sequence:
        converted = reorder_svg_by_sequence(converted, animation_sequence)
    return converted


@dataclass(frozen=True)
class ExcalidrawPage:
    """One Excalidraw frame/slide treated as a full-screen animation page."""

    page_id: str
    name: str
    x: float
    y: float
    width: float
    height: float

    @property
    def sort_key(self) -> tuple[float, float]:
        return (self.y, self.x)


def _decode_excalidraw_payload(data: dict[str, Any]) -> str:
    raw = data.get("encoded") or ""
    if isinstance(raw, str):
        blob = raw.encode("latin-1")
    else:
        blob = bytes(raw)
    if data.get("compressed"):
        return zlib.decompress(blob).decode("utf-8")
    return blob.decode("utf-8")


def decode_svg_embedded_scene(svg_path: Path) -> dict[str, Any] | None:
    """Decode embedded Excalidraw JSON from SVG metadata when present."""
    try:
        text = svg_path.read_text(encoding="utf-8")
    except OSError:
        return None
    if "payload-type:" not in text or "payload-start" not in text:
        return None
    match = re.search(
        r"<!--\s*payload-start\s*-->\s*(.*?)\s*<!--\s*payload-end\s*-->",
        text,
        re.S,
    )
    if not match:
        return None
    b64 = re.sub(r"\s+", "", match.group(1))
    version_match = re.search(r"payload-version:(\d+)", text)
    is_byte_string = version_match is None or version_match.group(1) != "1"
    try:
        decoded = base64.b64decode(b64)
        payload_text = decoded.decode("latin-1") if is_byte_string else decoded.decode("utf-8")
        wrapper = json.loads(payload_text)
    except (ValueError, json.JSONDecodeError):
        return None
    if isinstance(wrapper, dict) and wrapper.get("type") == "excalidraw":
        return wrapper
    if isinstance(wrapper, dict) and "encoded" in wrapper:
        try:
            payload_text = _decode_excalidraw_payload(wrapper)
        except zlib.error:
            return None
    else:
        return None
    try:
        scene = json.loads(payload_text)
    except json.JSONDecodeError:
        return None
    return scene if scene.get("type") == "excalidraw" else None


def pages_from_excalidraw_scene(scene: dict[str, Any]) -> list[ExcalidrawPage]:
    """Return frame/slide pages from embedded or .excalidraw scene data."""
    elements = scene.get("elements") or []
    frames: list[ExcalidrawPage] = []
    for el in elements:
        if not isinstance(el, dict) or el.get("isDeleted"):
            continue
        if el.get("type") not in ("frame", "magicframe"):
            continue
        frames.append(
            ExcalidrawPage(
                page_id=str(el.get("id") or ""),
                name=str(el.get("name") or "Page").strip() or "Page",
                x=float(el.get("x") or 0),
                y=float(el.get("y") or 0),
                width=float(el.get("width") or 0),
                height=float(el.get("height") or 0),
            )
        )
    frames = [p for p in frames if p.width > 10 and p.height > 10 and p.page_id]
    frames.sort(key=lambda p: p.sort_key)
    return frames


def _clip_path_frame_id(value: str | None) -> str | None:
    if not value:
        return None
    match = re.search(r"url\(#([^)]+)\)", value)
    if not match:
        return None
    frame_id = match.group(1)
    if frame_id.startswith("image-clipPath-"):
        return None
    return frame_id


def _clip_path_rect_bounds(clip_elem: ET.Element) -> tuple[float, float, float, float] | None:
    rect = next((child for child in clip_elem if _local_tag(child) == "rect"), None)
    if rect is None:
        return None
    tx, ty = _parse_translate(rect.get("transform") or "")
    try:
        w = float(str(rect.get("width") or "0"))
        h = float(str(rect.get("height") or "0"))
    except ValueError:
        return None
    if w < 10 or h < 10:
        return None
    return tx, ty, w, h


def _pages_from_svg_clip_paths(root: ET.Element) -> list[ExcalidrawPage]:
    pages: list[ExcalidrawPage] = []
    for elem in root.iter():
        if _local_tag(elem) != "clipPath":
            continue
        frame_id = elem.get("id") or ""
        if not frame_id or frame_id.startswith("image-clipPath-"):
            continue
        bounds = _clip_path_rect_bounds(elem)
        if bounds is None:
            continue
        x, y, w, h = bounds
        pages.append(
            ExcalidrawPage(
                page_id=frame_id,
                name=f"Page {len(pages) + 1}",
                x=x,
                y=y,
                width=w,
                height=h,
            )
        )
    pages.sort(key=lambda p: p.sort_key)
    return pages


def _element_page_id(elem: ET.Element, pages: list[ExcalidrawPage]) -> str | None:
    clip_id = _clip_path_frame_id(elem.get("clip-path"))
    if clip_id:
        return clip_id
    for child in elem.iter():
        if child is elem:
            continue
        clip_id = _clip_path_frame_id(child.get("clip-path"))
        if clip_id:
            return clip_id
    tx, ty = _parse_translate(elem.get("transform") or "")
    cx, cy = tx, ty
    for page in pages:
        if page.x <= cx <= page.x + page.width and page.y <= cy <= page.y + page.height:
            return page.page_id
    return None


def detect_svg_pages(svg_path: Path) -> list[ExcalidrawPage]:
    """Detect multiple Excalidraw frames/slides in an SVG export."""
    scene = decode_svg_embedded_scene(svg_path)
    if scene:
        pages = pages_from_excalidraw_scene(scene)
        if len(pages) > 1:
            return pages
    try:
        root = ET.parse(svg_path).getroot()
    except ET.ParseError:
        return []
    pages = _pages_from_svg_clip_paths(root)
    if len(pages) > 1:
        return pages
    return []


def build_page_svg(svg_path: Path, page: ExcalidrawPage, pages: list[ExcalidrawPage]) -> Path:
    """Build a single-page SVG cropped to one frame/slide."""
    root = ET.parse(svg_path).getroot()
    svg_ns = "http://www.w3.org/2000/svg"
    drawables = _drawable_root_children(root)
    page_elems: list[ET.Element] = []
    for elem in drawables:
        elem_page = _element_page_id(elem, pages)
        if elem_page == page.page_id:
            page_elems.append(copy.deepcopy(elem))

    if not page_elems:
        raise ValueError(f"No drawable content found for page {page.name!r}")

    new_root = ET.Element(f"{{{svg_ns}}}svg")
    new_root.set("xmlns", svg_ns)
    new_root.set("viewBox", f"0 0 {page.width} {page.height}")
    new_root.set("width", str(page.width))
    new_root.set("height", str(page.height))

    for child in root:
        if _local_tag(child) == "defs":
            new_root.append(copy.deepcopy(child))

    bg = ET.Element(f"{{{svg_ns}}}rect")
    bg.set("x", "0")
    bg.set("y", "0")
    bg.set("width", str(page.width))
    bg.set("height", str(page.height))
    canvas = svg_canvas_background_color(svg_path) or "#ffffff"
    bg.set("fill", canvas)
    new_root.append(bg)

    wrapper = ET.Element(f"{{{svg_ns}}}g")
    wrapper.set("transform", f"translate({-page.x} {-page.y})")
    for elem in page_elems:
        wrapper.append(elem)
    new_root.append(wrapper)

    render_dir = svg_path.parent / ".excalidraw_render" / "pages"
    render_dir.mkdir(parents=True, exist_ok=True)
    safe_id = re.sub(r"[^\w.-]+", "_", page.page_id)[:32]
    out = render_dir / f"{svg_path.stem}_page_{safe_id}.svg"
    out.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(new_root, encoding="unicode"),
        encoding="utf-8",
    )
    return out


def pages_from_excalidraw_file(path: Path) -> list[ExcalidrawPage]:
    """Detect pages in .excalidraw JSON."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("type") != "excalidraw":
        return []
    return pages_from_excalidraw_scene(data)


def parse_animation_sequence_phrases(note: str) -> list[str]:
    """Parse a natural-language note into ordered animation labels."""
    text = note.strip().lower()
    if not text:
        return []
    text = re.sub(
        r"^(?:ok(?:\s+so)?[, ]+|so[, ]+|please[, ]+|i want(?: it)? to(?: write| animate| show| draw)?[, ]+)+",
        "",
        text,
    )
    parts = re.split(r"\bthen\b", text)
    phrases: list[str] = []
    for part in parts:
        part = part.strip()
        part = re.sub(r"^(?:write|animate|show|draw)\s+", "", part)
        part = re.sub(r"\s+(?:first|next|last|finally)$", "", part)
        part = re.sub(r"\s+text$", "", part)
        part = part.strip(" ,.")
        if len(part) >= 2:
            phrases.append(part)
    return phrases


def _element_text_label(elem: ET.Element) -> str:
    label = (elem.get("data-excal-text") or "").strip().lower()
    if label:
        return label
    if _local_tag(elem) == "text":
        return "".join(elem.itertext()).strip().lower()
    for child in elem.iter():
        if child is elem:
            continue
        nested = (child.get("data-excal-text") or "").strip().lower()
        if nested:
            return nested
        if _local_tag(child) == "text":
            text = "".join(child.itertext()).strip().lower()
            if text:
                return text
    return ""


def _element_path_weight(elem: ET.Element) -> int:
    weight = 0
    tag = _local_tag(elem)
    if tag == "path":
        weight += max(len(elem.get("d") or ""), 1)
    for child in elem.iter():
        if child is elem:
            continue
        if _local_tag(child) == "path":
            weight += max(len(child.get("d") or ""), 1)
    return weight


def _phrase_match_score(phrase: str, label: str, *, is_path_unit: bool) -> float:
    phrase = phrase.strip().lower()
    label = label.strip().lower()
    if not phrase:
        return 0.0
    if "logo" in phrase and is_path_unit and not label:
        return 0.85
    if label:
        if phrase in label or label in phrase:
            return 1.0
        phrase_tokens = set(re.findall(r"[a-z0-9]+", phrase))
        label_tokens = set(re.findall(r"[a-z0-9]+", label))
        if phrase_tokens and label_tokens:
            overlap = len(phrase_tokens & label_tokens) / len(phrase_tokens)
            if overlap >= 0.5:
                return 0.6 + overlap * 0.35
    if not is_path_unit and not label:
        return 0.0
    if "python" in phrase and "logo" not in phrase and "ai" in phrase and "ai" in label:
        return 0.9
    return 0.0


def _drawable_root_children(root: ET.Element) -> list[ET.Element]:
    skip_tags = {"defs", "metadata", "style", "mask"}
    _, _, vb_w, vb_h = parse_view_box(root)
    drawables: list[ET.Element] = []
    for child in list(root):
        tag = _local_tag(child)
        if tag in skip_tags:
            continue
        if tag == "rect" and _rect_covers_view_box(child, vb_w, vb_h):
            continue
        drawables.append(child)
    return drawables


def normalize_animation_sequence(phrases: list[str] | None) -> list[str]:
    """Clean phrases from chat notes or generated scene code."""
    if not phrases:
        return []
    out: list[str] = []
    for raw in phrases:
        part = raw.strip().lower()
        part = re.sub(r"^(?:write|animate|show|draw)\s+", "", part)
        part = re.sub(r"\s+(?:first|next|last|finally|text)$", "", part)
        part = part.strip(" ,.")
        if len(part) >= 2:
            out.append(part)
    return out


def reorder_svg_by_sequence(svg_path: Path, phrases: list[str]) -> Path:
    """Reorder top-level SVG groups to match user animation sequence notes."""
    phrases = normalize_animation_sequence(phrases)
    if not phrases:
        return svg_path
    try:
        root = ET.parse(svg_path).getroot()
    except ET.ParseError:
        return svg_path

    drawables = _drawable_root_children(root)
    if len(drawables) < 2:
        return svg_path

    ordered: list[ET.Element] = []
    used: set[int] = set()

    for phrase in phrases:
        if "logo" in phrase.lower():
            for elem in drawables:
                eid = id(elem)
                if eid in used:
                    continue
                label = _element_text_label(elem)
                if label:
                    continue
                if _element_path_weight(elem) < 20:
                    continue
                ordered.append(elem)
                used.add(eid)
            continue

        best_elem: ET.Element | None = None
        best_score = 0.35
        for elem in drawables:
            eid = id(elem)
            if eid in used:
                continue
            label = _element_text_label(elem)
            score = _phrase_match_score(phrase, label, is_path_unit=not bool(label))
            if score > best_score:
                best_score = score
                best_elem = elem
        if best_elem is not None:
            ordered.append(best_elem)
            used.add(id(best_elem))

    for elem in drawables:
        if id(elem) not in used:
            ordered.append(elem)

    if ordered == drawables:
        return svg_path

    first_idx = next(i for i, child in enumerate(list(root)) if child in drawables)
    for elem in drawables:
        root.remove(elem)
    for offset, elem in enumerate(ordered):
        root.insert(first_idx + offset, elem)

    render_dir = svg_path.parent / ".excalidraw_render"
    render_dir.mkdir(parents=True, exist_ok=True)
    out = render_dir / f"{svg_path.stem}_ordered.svg"
    out.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode"),
        encoding="utf-8",
    )
    return out


def convert_svg_text_to_paths(svg_path: Path) -> Path:
    """Replace SVG <text> nodes with per-glyph <path> outlines using embedded fonts."""
    try:
        root = ET.parse(svg_path).getroot()
    except ET.ParseError:
        return svg_path

    parent_map: dict[ET.Element, ET.Element] = {child: parent for parent in root.iter() for child in parent}
    text_elems = [elem for elem in root.iter() if _local_tag(elem) == "text" and "".join(elem.itertext()).strip()]
    if not text_elems:
        return svg_path

    embedded = extract_svg_embedded_fonts(svg_path)
    font_cache: dict[Path, TTFont] = {}
    changed = False
    svg_ns = "http://www.w3.org/2000/svg"

    for elem in text_elems:
        content = "".join(elem.itertext()).strip()
        if not content:
            continue
        fs_raw = str(elem.get("font-size") or "24").replace("px", "")
        try:
            font_size_px = float(fs_raw)
        except ValueError:
            font_size_px = 24.0
        fill = elem.get("fill") or "#ffffff"
        anchor = elem.get("text-anchor") or "start"
        font_name, font_path = resolve_text_font(elem.get("font-family") or "", embedded)
        if font_path is None:
            continue
        if font_path not in font_cache:
            font_cache[font_path] = TTFont(font_path)
        font = font_cache[font_path]

        # Keep coordinates local — parent <g transform="..."> must stay intact.
        tx = float(elem.get("x", 0) or 0)
        ty = float(elem.get("y", 0) or 0)

        path_elems = _text_to_path_elements(
            content,
            font,
            anchor_x=tx,
            baseline_y=ty,
            font_size_px=font_size_px,
            fill=fill,
            anchor=anchor,
        )
        if not path_elems:
            continue

        parent = parent_map.get(elem)
        if parent is None:
            continue
        idx = list(parent).index(elem)
        parent.remove(elem)
        group = ET.Element(f"{{{svg_ns}}}g")
        group.set("data-excal-text", content[:48])
        for path_elem in path_elems:
            group.append(path_elem)
        parent.insert(idx, group)
        # Bubble label to outer transform wrapper so draw-order matching sees it.
        if (
            _local_tag(parent) == "g"
            and parent.get("transform")
            and len(list(parent)) == 1
            and not parent.get("data-excal-text")
        ):
            parent.set("data-excal-text", content[:48])
        changed = True

    if not changed:
        return svg_path

    render_dir = svg_path.parent / ".excalidraw_render"
    render_dir.mkdir(parents=True, exist_ok=True)
    out = render_dir / f"{svg_path.stem}_paths.svg"
    out.write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(root, encoding="unicode"),
        encoding="utf-8",
    )
    return out


def _text_to_path_elements(
    text: str,
    font: TTFont,
    *,
    anchor_x: float,
    baseline_y: float,
    font_size_px: float,
    fill: str,
    anchor: str,
) -> list[ET.Element]:
    """Layout text with Excalidraw's embedded subset font; one path per glyph."""
    glyph_set = font.getGlyphSet()
    cmap = font.getBestCmap() or {}
    hmtx = font["hmtx"]
    upem = float(font["head"].unitsPerEm or 1000)
    scale = font_size_px / upem

    advances: list[tuple[str, float]] = []
    for ch in text:
        gname = cmap.get(ord(ch))
        if not gname:
            default_adv = hmtx[".notdef"][0] * scale if ".notdef" in hmtx else 250 * scale
            advances.append(("", default_adv))
            continue
        advances.append((gname, hmtx[gname][0] * scale))

    total_width = sum(adv for _, adv in advances)
    if anchor == "middle":
        cursor_x = anchor_x - total_width / 2
    elif anchor == "end":
        cursor_x = anchor_x - total_width
    else:
        cursor_x = anchor_x

    svg_ns = "http://www.w3.org/2000/svg"
    paths: list[ET.Element] = []
    for gname, adv in advances:
        if not gname:
            cursor_x += adv
            continue
        pen = SVGPathPen(glyph_set)
        transform = TransformPen(
            pen,
            (scale, 0, 0, -scale, cursor_x, baseline_y),
        )
        glyph_set[gname].draw(transform)
        d = pen.getCommands()
        if not d:
            cursor_x += adv
            continue
        path_elem = ET.Element(f"{{{svg_ns}}}path")
        path_elem.set("d", d)
        path_elem.set("fill", fill)
        path_elem.set("stroke", "none")
        paths.append(path_elem)
        cursor_x += adv
    return paths
