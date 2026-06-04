"""Invisible grid layouts for multi-icon beat panels (1–4 icons).

Percentages refer to the icon panel region (half-frame below the label),
not the full Manim frame. No visible grid lines are drawn.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

import numpy as np

if TYPE_CHECKING:
    from manim import Group, Mobject, VGroup

IconGridMode = Literal[
    "auto",
    "single",
    "horizontal",
    "vertical",
    "triple_top",
    "triple_bottom",
    "quad",
]

# Fraction of each cell reserved as inner padding around the icon.
CELL_PAD = 0.10

# (x, y, width, height) as fractions of panel — origin at bottom-left of panel.
CellSpec = tuple[float, float, float, float]


def _manim():
    from manim import Group, VMobject, VGroup

    return Group, VMobject, VGroup


def _icon_container(*mobs: "Mobject"):
    """VGroup for SVG icons; Group when rasters (ImageMobject) are included."""
    Group, VMobject, VGroup = _manim()
    if mobs and all(isinstance(m, VMobject) for m in mobs):
        return VGroup(*mobs)
    return Group(*mobs)


def panel_from_anchor(
    center: np.ndarray,
    *,
    panel_width: float,
    panel_height: float,
) -> dict[str, float | np.ndarray]:
    return {
        "center": center,
        "width": panel_width,
        "height": panel_height,
        "left": center[0] - panel_width / 2,
        "bottom": center[1] - panel_height / 2,
    }


def _cell_center(panel: dict, spec: CellSpec) -> tuple[np.ndarray, float, float]:
    x_frac, y_frac, w_frac, h_frac = spec
    width = float(panel["width"])
    height = float(panel["height"])
    left = float(panel["left"])
    bottom = float(panel["bottom"])

    cell_w = width * w_frac
    cell_h = height * h_frac
    cell_left = left + width * x_frac
    cell_bottom = bottom + height * y_frac
    center = np.array(
        [cell_left + cell_w / 2, cell_bottom + cell_h / 2, 0.0],
    )
    return center, cell_w, cell_h


def _fit_in_cell(mob: "Mobject", center: np.ndarray, cell_w: float, cell_h: float) -> None:
    inner_w = cell_w * (1 - 2 * CELL_PAD)
    inner_h = cell_h * (1 - 2 * CELL_PAD)
    mob.move_to(center)
    if mob.width > 0 and mob.width > inner_w:
        mob.scale(inner_w / mob.width)
    if mob.height > 0 and mob.height > inner_h:
        mob.scale(inner_h / mob.height)
    mob.move_to(center)


def _cells_for_count(count: int, mode: IconGridMode) -> list[CellSpec]:
    if count <= 0:
        return []
    if count == 1 or mode == "single":
        return [(0.0, 0.0, 1.0, 1.0)]

    if count == 2:
        if mode in ("vertical",):
            return [(0.0, 0.5, 1.0, 0.5), (0.0, 0.0, 1.0, 0.5)]
        # default / horizontal / auto
        return [(0.0, 0.0, 0.5, 1.0), (0.5, 0.0, 0.5, 1.0)]

    if count == 3:
        if mode == "triple_bottom":
            return [
                (0.0, 0.5, 1.0, 0.5),
                (0.0, 0.0, 0.5, 0.5),
                (0.5, 0.0, 0.5, 0.5),
            ]
        # default / triple_top / auto
        return [
            (0.0, 0.5, 0.5, 0.5),
            (0.5, 0.5, 0.5, 0.5),
            (0.0, 0.0, 1.0, 0.5),
        ]

    # 4+ → 2×2 (extras beyond 4 are ignored by caller)
    return [
        (0.0, 0.5, 0.5, 0.5),
        (0.5, 0.5, 0.5, 0.5),
        (0.0, 0.0, 0.5, 0.5),
        (0.5, 0.0, 0.5, 0.5),
    ]


def resolve_grid_mode(count: int, mode: IconGridMode | str | None) -> IconGridMode:
    raw = (mode or "auto").lower().replace("-", "_")
    if raw in (
        "single",
        "horizontal",
        "vertical",
        "triple_top",
        "triple_bottom",
        "quad",
    ):
        return raw  # type: ignore[return-value]
    if count == 1:
        return "single"
    if count == 2:
        return "horizontal"
    if count == 3:
        return "triple_top"
    return "quad"


def layout_icons_in_panel(
    mobs: list["Mobject"],
    panel: dict,
    *,
    mode: IconGridMode | str | None = "auto",
    max_icons: int = 4,
) -> "VGroup":
    """Place up to ``max_icons`` mobjects in an invisible grid inside ``panel``."""
    VGroup = _manim()
    icons = list(mobs[:max_icons])
    if not icons:
        return VGroup()

    grid_mode = resolve_grid_mode(len(icons), mode)  # type: ignore[arg-type]
    cells = _cells_for_count(len(icons), grid_mode)

    placed: list = []
    for mob, spec in zip(icons, cells):
        center, cell_w, cell_h = _cell_center(panel, spec)
        _fit_in_cell(mob, center, cell_w, cell_h)
        placed.append(mob)

    return _icon_container(*placed)
