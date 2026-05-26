"""ASCII grid layout presets for beat scripts.

Used by generate_grid.py — also importable for agents.
"""

from __future__ import annotations

from dataclasses import dataclass, field

FRAME_W = 14.22
FRAME_H = 8.0
LEFT_X = -3.55
RIGHT_X = 3.55
LABEL_Y = "top (buff=0.9)"
CONTENT_NOTE = "panels centered below label, not full frame"


@dataclass
class GridSlot:
    kind: str  # icon | card | text | morph | empty
    name: str
    detail: str = ""
    position: str = ""


@dataclass
class BeatGrid:
    layout_id: str
    title: str
    label: str
    left: list[GridSlot] = field(default_factory=list)
    right: list[GridSlot] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


LAYOUTS: dict[str, str] = {
    "card_right_icon_left": "White card on RIGHT, icon/visual on LEFT (default)",
    "card_left_icon_right": "White card on LEFT, icon/visual on RIGHT",
    "card_right_only": "White card on RIGHT, left panel empty",
    "card_left_only": "White card on LEFT, right panel empty",
    "dual_card": "White card on BOTH sides",
    "dual_icon": "Icons/visuals on BOTH sides, no card",
    "text_right_icon_left": "No card — white text on RIGHT, icon on LEFT",
    "text_left_icon_right": "No card — white text on LEFT, icon on RIGHT",
    "icon_left_anim_right": "Icon LEFT, animation/morph RIGHT (no card)",
    "card_right_stack_left": "Card RIGHT, stacked icons LEFT",
}


def _slot_line(slot: GridSlot, panel: str) -> list[str]:
    x = LEFT_X if panel == "left" else RIGHT_X
    lines = [f"  [{slot.name}]"]
    if slot.kind == "card":
        lines.append(f"  @ ({x:+.2f}, content_y)  {slot.detail}")
    elif slot.kind == "icon":
        lines.append(f"  @ ({x:+.2f}, content_y)  {slot.detail}")
    elif slot.kind == "text":
        lines.append(f"  @ ({x:+.2f}, content_y)  white on orange")
        if slot.detail:
            for t in slot.detail.split("\n"):
                lines.append(f"    {t}")
    elif slot.kind == "morph":
        lines.append(f"  @ ({x:+.2f}, content_y)  {slot.detail}")
    elif slot.detail:
        lines.append(f"  {slot.detail}")
    return lines


def render_ascii(grid: BeatGrid, width: int = 61) -> str:
    """Render a beat grid diagram as ASCII."""
    sep = "├" + "─" * 22 + "┬" + "─" * (width - 24) + "┤"
    top = "┌" + "─" * width + "┐"
    bot = "└" + "─" * width + "┘"
    mid = "│"

    label_line = f'  LABEL: "{grid.label}"  @ {LABEL_Y}  YELLOW  anim_type (white cursor)'
    label_row = mid + label_line.ljust(width) + mid

    left_lines: list[str] = ["  LEFT PANEL", f"  x center: {LEFT_X:+.2f}"]
    right_lines: list[str] = ["  RIGHT PANEL", f"  x center: {RIGHT_X:+.2f}"]

    for slot in grid.left:
        left_lines.extend(_slot_line(slot, "left"))
    if not grid.left:
        left_lines.append("  (empty)")

    for slot in grid.right:
        right_lines.extend(_slot_line(slot, "right"))
    if not grid.right:
        right_lines.append("  (empty)")

    body_h = max(len(left_lines), len(right_lines))
    left_lines += [""] * (body_h - len(left_lines))
    right_lines += [""] * (body_h - len(right_lines))

    rows = [top, label_row, sep]
    for ll, rl in zip(left_lines, right_lines):
        row = mid + ll.ljust(22) + mid + rl.ljust(width - 24) + mid
        rows.append(row)
    rows.append(bot)

    header = f"─── GRID LAYOUT ({grid.layout_id}) ───"
    footer = [f"  Layout: {LAYOUTS.get(grid.layout_id, grid.layout_id)}"]
    footer.append(f"  Vertical: {CONTENT_NOTE}")
    for n in grid.notes:
        footer.append(f"  • {n}")

    return "\n".join([header, *rows, *footer])


def beat1_example() -> BeatGrid:
    return BeatGrid(
        layout_id="card_right_icon_left",
        title="welcome_to_python",
        label="Welcome to Python for AI",
        left=[
            GridSlot("icon", "icon_python", "size 1.2, color BLUE", f"({LEFT_X:+.2f}, content_y)"),
            GridSlot("icon", "icon_scream", "swap @ same anchor, t≈punchline", f"({LEFT_X:+.2f}, content_y)"),
        ],
        right=[
            GridSlot("card", "ui_card", "size 5.6 × 5.0, empty then type", f"({RIGHT_X:+.2f}, content_y)"),
            GridSlot("text", "card lines 1–4", "black, TypeWithCursor"),
            GridSlot("text", "punchline", "line 5 after lines 1–4 fade"),
        ],
        notes=[
            "Card grows EMPTY — text not inside GrowFromCenter",
            "Lines 1–4 fade before punchline",
            '"screaming" → RED + anim_wiggle; face wiggles too',
            "icon_python FadeOut → icon_scream FadeIn (same spot)",
        ],
    )


def build_grid(
    layout_id: str,
    label: str,
    *,
    left_icon: str = "",
    right_icon: str = "",
    left_icons: list[str] | None = None,
    right_icons: list[str] | None = None,
    card_side: str = "right",
    card_size: str = "5.6 × 5.0",
    card_lines: list[str] | None = None,
    bg_text_side: str = "",
    bg_lines: list[str] | None = None,
    left_morph: str = "",
    right_morph: str = "",
    notes: list[str] | None = None,
) -> BeatGrid:
    """Build a BeatGrid from high-level beat parameters."""
    left: list[GridSlot] = []
    right: list[GridSlot] = []

    def add_icons(side: str, names: list[str]) -> None:
        target = left if side == "left" else right
        for name in names:
            target.append(GridSlot("icon", name, "Iconify / beat icons/"))

    if left_icons:
        add_icons("left", left_icons)
    elif left_icon:
        add_icons("left", [left_icon])
    if left_morph:
        left.append(GridSlot("morph", left_morph, "ReplacementTransform / animation"))

    if right_icons:
        add_icons("right", right_icons)
    elif right_icon:
        add_icons("right", [right_icon])
    if right_morph:
        right.append(GridSlot("morph", right_morph, "ReplacementTransform / animation"))

    card_slot = GridSlot(
        "card",
        "ui_card",
        f"size {card_size}, side {card_side}",
        "",
    )
    text_slots = [GridSlot("text", f"line {i + 1}", line) for i, line in enumerate(card_lines or [])]

    if layout_id == "card_right_icon_left":
        if not left and left_icon:
            add_icons("left", [left_icon])
        right = [card_slot, *text_slots]
    elif layout_id == "card_left_icon_right":
        left = [card_slot, *text_slots]
        if not right and right_icon:
            add_icons("right", [right_icon])
    elif layout_id == "card_right_only":
        right = [card_slot, *text_slots]
    elif layout_id == "card_left_only":
        left = [card_slot, *text_slots]
    elif layout_id == "dual_card":
        left = [card_slot, *text_slots[: max(1, len(text_slots) // 2)]]
        right = [
            GridSlot("card", "ui_card", f"size {card_size}"),
            *text_slots[max(1, len(text_slots) // 2) :],
        ]
    elif layout_id == "dual_icon":
        add_icons("left", left_icons or ([left_icon] if left_icon else ["icon_a"]))
        add_icons("right", right_icons or ([right_icon] if right_icon else ["icon_b"]))
    elif layout_id == "text_right_icon_left":
        side = bg_text_side or "right"
        text_slot = GridSlot("text", "BG text", "\n".join(bg_lines or ["Line 1", "Line 2"]))
        if side == "right":
            right = [text_slot]
            if left_icon:
                add_icons("left", [left_icon])
        else:
            left = [text_slot]
            if right_icon:
                add_icons("right", [right_icon])
    elif layout_id == "text_left_icon_right":
        text_slot = GridSlot("text", "BG text", "\n".join(bg_lines or ["Line 1", "Line 2"]))
        left = [text_slot]
        if right_icon:
            add_icons("right", [right_icon])
    elif layout_id == "card_right_stack_left":
        right = [card_slot, *text_slots]
        for name in left_icons or ([left_icon] if left_icon else []):
            left.append(GridSlot("icon", name, "stacked vertical"))
    elif layout_id == "icon_left_anim_right":
        if left_icon:
            add_icons("left", [left_icon])
        right.append(GridSlot("morph", right_morph or "morph_*", "animation on orange BG"))
    else:
        raise KeyError(f"Unknown layout_id: {layout_id}. Choose from: {', '.join(LAYOUTS)}")

    return BeatGrid(
        layout_id=layout_id,
        title="",
        label=label,
        left=left,
        right=right,
        notes=notes or [],
    )
