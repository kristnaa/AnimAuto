"""Hand-drawn / chalk sketch styling for blackboard explainers."""

from __future__ import annotations

import hashlib
from typing import Iterable

from manim import *

CHALK_FONTS: tuple[str, ...] = (
    "Chalkboard SE",
    "Marker Felt",
    "Bradley Hand",
    "Comic Sans MS",
    "sans-serif",
)

SKETCH = {
    "enabled": True,
    "wobble": 0.014,
    "segments": 40,
    "ghost_opacity": 0.28,
    "stroke_width": 2.6,
}


def _rng(seed: str) -> np.random.RandomState:
    digest = hashlib.md5(seed.encode()).hexdigest()
    return np.random.RandomState(int(digest[:8], 16) % (2**31))


def chalk_text(
    text: str,
    *,
    color=WHITE,
    font_size: int = 22,
    weight=BOLD,
    seed: str | None = None,
) -> Text | VGroup:
    """Prefer casual chalk-like fonts when available."""
    mob: Text | None = None
    for font in CHALK_FONTS:
        try:
            mob = Text(text, font=font, color=color, font_size=font_size, weight=weight)
            break
        except Exception:
            continue
    if mob is None:
        mob = Text(text, color=color, font_size=font_size, weight=weight)
    if SKETCH["enabled"]:
        return sketch_mobject(mob, seed=seed or text)
    return mob


def _point_on_rounded_rect(t: float, width: float, height: float, radius: float) -> np.ndarray:
    """Parameterize perimeter of a rounded rectangle, t in [0, 1)."""
    w, h, r = width / 2, height / 2, min(radius, min(width, height) / 2 - 0.01)
    straight_x = max(width - 2 * r, 0.01)
    straight_y = max(height - 2 * r, 0.01)
    arc_len = PI * r / 2
    seg_lens = [straight_x, arc_len, straight_y, arc_len, straight_x, arc_len, straight_y, arc_len]
    total = sum(seg_lens)
    dist = (t % 1.0) * total
    x, y = w, h
    for idx, seg in enumerate(seg_lens):
        if dist > seg:
            dist -= seg
            continue
        u = dist / seg if seg > 0 else 0
        if idx == 0:
            return np.array([w - r - u * straight_x, h, 0])
        if idx == 1:
            ang = u * PI / 2
            return np.array([-(w - r) + r * np.cos(ang), (h - r) + r * np.sin(ang), 0])
        if idx == 2:
            return np.array([-(w - r), (h - r) - u * straight_y, 0])
        if idx == 3:
            ang = PI / 2 + u * PI / 2
            return np.array([-(w - r) + r * np.cos(ang), -(h - r) + r * np.sin(ang), 0])
        if idx == 4:
            return np.array([-(w - r) + u * straight_x, -(h - r), 0])
        if idx == 5:
            ang = PI + u * PI / 2
            return np.array([(w - r) + r * np.cos(ang), -(h - r) + r * np.sin(ang), 0])
        if idx == 6:
            return np.array([(w - r), -(h - r) + u * straight_y, 0])
        ang = 3 * PI / 2 + u * PI / 2
        return np.array([(w - r) + r * np.cos(ang), (h - r) + r * np.sin(ang), 0])
    return np.array([w, h, 0])


def sketch_rounded_rect(
    width: float,
    height: float,
    *,
    corner_radius: float = 0.12,
    color=WHITE,
    fill_color=BLACK,
    fill_opacity: float = 0.12,
    stroke_width: float | None = None,
    seed: str = "rect",
) -> VGroup:
    """Closed hand-drawn rounded rectangle."""
    rng = _rng(seed)
    amp = SKETCH["wobble"]
    n = SKETCH["segments"]
    pts: list[np.ndarray] = []
    for i in range(n):
        t = i / n
        p = _point_on_rounded_rect(t, width, height, corner_radius)
        jitter = amp * rng.randn(2)
        pts.append(p + np.array([jitter[0], jitter[1], 0]))
    pts.append(pts[0])
    sw = stroke_width if stroke_width is not None else SKETCH["stroke_width"]
    main = VMobject(color=color, stroke_width=sw)
    main.set_points_as_corners(pts)
    main.set_fill(fill_color, opacity=fill_opacity)
    ghost = main.copy().set_stroke(color, width=sw * 0.55, opacity=SKETCH["ghost_opacity"])
    ghost.shift(0.006 * UR)
    return VGroup(ghost, main)


def _wobble_polyline(points: Iterable[np.ndarray], seed: str, *, closed: bool = False) -> VMobject:
    rng = _rng(seed)
    amp = SKETCH["wobble"]
    arr = [np.array(p, dtype=float) for p in points]
    if closed and arr:
        arr.append(arr[0])
    dense: list[np.ndarray] = []
    for i in range(len(arr) - 1):
        a, b = arr[i], arr[i + 1]
        dense.append(a)
        for t in np.linspace(0, 1, 6, endpoint=False):
            p = a + t * (b - a)
            jitter = amp * rng.randn(2)
            dense.append(p + np.array([jitter[0], jitter[1], 0]))
    dense.append(arr[-1])
    mob = VMobject(stroke_width=SKETCH["stroke_width"])
    mob.set_points_as_corners(dense)
    return mob


def sketch_line(start: np.ndarray, end: np.ndarray, *, color=YELLOW, seed: str = "line") -> VGroup:
    main = _wobble_polyline([start, end], seed).set_stroke(color, width=SKETCH["stroke_width"])
    ghost = main.copy().set_stroke(color, width=SKETCH["stroke_width"] * 0.55, opacity=SKETCH["ghost_opacity"])
    ghost.shift(0.005 * UL)
    return VGroup(ghost, main)


def sketch_dashed_line(
    start: np.ndarray,
    end: np.ndarray,
    *,
    color=YELLOW,
    dash_length: float = 0.12,
    seed: str = "dash",
) -> VGroup:
    vec = end - start
    length = float(np.linalg.norm(vec))
    if length < 0.01:
        return VGroup()
    direction = vec / length
    n = max(2, int(length / dash_length))
    segs: list[Mobject] = []
    for i in range(n):
        if i % 2 == 0:
            a = start + direction * (i / n) * length
            b = start + direction * min((i + 1) / n, 1.0) * length
            segs.append(sketch_line(a, b, color=color, seed=f"{seed}-{i}"))
    return VGroup(*segs)


def sketch_curved_path(
    start: np.ndarray,
    end: np.ndarray,
    *,
    color=YELLOW,
    bulge: float = 0.5,
    seed: str = "curve",
) -> VGroup:
    mid = (start + end) / 2
    perp = np.array([-(end - start)[1], (end - start)[0], 0])
    if np.linalg.norm(perp) > 0.01:
        perp = perp / np.linalg.norm(perp) * bulge
    ctrl = mid + perp
    path = CubicBezier(start, start * 0.55 + ctrl * 0.45, end * 0.55 + ctrl * 0.45, end)
    pts = [path.point_from_proportion(t) for t in np.linspace(0, 1, 22)]
    main = _wobble_polyline(pts, seed).set_stroke(color, width=SKETCH["stroke_width"])
    ghost = main.copy().set_stroke(color, width=SKETCH["stroke_width"] * 0.55, opacity=SKETCH["ghost_opacity"])
    return VGroup(ghost, main)


def sketch_arrow_head(tip_at: np.ndarray, direction: np.ndarray, *, color=YELLOW, seed: str = "tip") -> VGroup:
    direction = direction / max(float(np.linalg.norm(direction)), 0.01)
    base = tip_at - direction * 0.22
    left = base + np.array([-direction[1], direction[0], 0]) * 0.09
    right = base - np.array([-direction[1], direction[0], 0]) * 0.09
    tri = _wobble_polyline([left, tip_at, right, left], seed, closed=True)
    tri.set_stroke(color, width=SKETCH["stroke_width"])
    tri.set_fill(color, opacity=0.85)
    return VGroup(tri)


def sketch_mobject(mob: Mobject, *, seed: str = "mob", amplitude: float | None = None) -> VGroup:
    """Double-stroke wobble wrapper for VMobjects (text, simple shapes)."""
    amp = amplitude if amplitude is not None else SKETCH["wobble"] * 0.65
    rng = _rng(seed)
    layers: list[Mobject] = []
    for sm in mob.get_family():
        if not isinstance(sm, VMobject) or sm.get_num_points() == 0:
            continue
        pts = sm.get_points().copy()
        noise = rng.randn(*pts.shape) * amp
        noise[:, 2] = 0
        wobbly = sm.copy()
        wobbly.set_points(pts + noise)
        stroke = sm.get_stroke_width() or 0
        fill_op = sm.get_fill_opacity() or 0
        color = sm.get_stroke_color() or sm.get_color()
        if fill_op > 0.01:
            wobbly.set_fill(sm.get_fill_color(), opacity=fill_op)
        if stroke > 0:
            wobbly.set_stroke(color, width=max(stroke, 1.5))
        ghost = wobbly.copy().set_stroke(color, width=max(stroke, 1.5) * 0.55, opacity=SKETCH["ghost_opacity"])
        ghost.shift(0.004 * DR)
        layers.extend([ghost, wobbly])
    if not layers:
        return VGroup(mob)
    return VGroup(*layers)


def sketch_highlight_pill(text: str, highlight_word: str | None, *, seed: str = "pill") -> VGroup:
    """Blue marker stroke under one word — sketch style."""
    if not highlight_word or highlight_word.lower() not in text.lower():
        return chalk_text(text, seed=seed)
    words = text.split()
    items: list[Mobject] = []
    for w in words:
        t = chalk_text(w, font_size=22, weight=NORMAL, seed=f"{seed}-{w}")
        if highlight_word.lower() in w.lower():
            pad = BackgroundRectangle(t, buff=0.08, corner_radius=0.06)
            pad.set_fill(BLUE, opacity=0.0)
            pad.set_stroke(BLUE, width=5, opacity=0.45)
            if SKETCH["enabled"]:
                pad = sketch_mobject(pad, seed=f"{seed}-pill")
            items.append(VGroup(pad, t))
        else:
            items.append(t)
    return VGroup(*items).arrange(RIGHT, buff=0.12)
