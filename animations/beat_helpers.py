"""Shared layout, typing, and camera helpers for course beats."""

from __future__ import annotations

from manim import *
from manim.utils.rate_functions import smooth

BG_PATH = "/Users/enfec/manimations/background/orange_theme_BG.png"
LABEL_TOP_BUFF = 0.9
LABEL_CONTENT_GAP = 0.25
PANEL_FRAME_WIDTH = 7.5
CARD_PAD_X = 0.45
CARD_PAD_Y = 0.35


class BeatLayoutMixin:
    def setup_background(self, overscale: float = 1.0):
        bg = ImageMobject(BG_PATH)
        bg.scale_to_fit_width(config.frame_width * overscale)
        bg.move_to(ORIGIN)
        self.add(bg)

    def left_center(self):
        return LEFT * (config.frame_width / 4)

    def right_center(self):
        return RIGHT * (config.frame_width / 4)

    def top_label(self, text):
        lbl = Text(text, font_size=48, color=WHITE, weight=BOLD)
        lbl.to_edge(UP, buff=LABEL_TOP_BUFF)
        return lbl

    def content_center_y(self, label: Mobject) -> float:
        frame_bottom = -config.frame_height / 2
        content_top = label.get_bottom()[1] - LABEL_CONTENT_GAP
        return (content_top + frame_bottom) / 2

    def panel_anchor(self, side: str, label: Mobject) -> np.ndarray:
        x = self.right_center()[0] if side == "right" else self.left_center()[0]
        y = self.content_center_y(label)
        return np.array([x, y, 0.0])

    def on_card(self, text, font_size=28):
        return Text(text, font_size=font_size, color=BLACK, weight=BOLD)

    def card_lines(self, *lines, font_size=28, max_width=None):
        group = VGroup(*[self.on_card(line, font_size=font_size) for line in lines])
        if max_width is not None:
            for line in group:
                if line.width > max_width:
                    line.scale(max_width / line.width)
        group.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        return group

    def place_card_content(self, content: Mobject, card: Mobject, pad_x=CARD_PAD_X, pad_y=CARD_PAD_Y):
        """Fit text block inside card with inner padding."""
        max_w = card.width - 2 * pad_x
        max_h = card.height - 2 * pad_y

        if isinstance(content, VGroup):
            for mob in content:
                if mob.width > max_w:
                    mob.scale(max_w / mob.width)
            content.arrange(DOWN, buff=0.22, aligned_edge=LEFT)

        if content.width > max_w:
            content.scale(max_w / content.width)
        if content.height > max_h:
            content.scale(max_h / content.height)

        content.move_to(card.get_center())
        content.align_to(card.get_left() + RIGHT * pad_x, LEFT)
        return content

    def card_text_in(self, card: Mobject, *lines, font_size=28):
        """Build card lines sized and padded to stay inside the card."""
        max_w = card.width - 2 * CARD_PAD_X
        group = self.card_lines(*lines, font_size=font_size, max_width=max_w)
        return self.place_card_content(group, card)

    def place_card_line(self, line: Mobject, card: Mobject, *, centered=False):
        """Position a single line inside card with horizontal padding."""
        max_w = card.width - 2 * CARD_PAD_X
        if line.width > max_w:
            line.scale(max_w / line.width)
        line.align_to(card.get_left() + RIGHT * CARD_PAD_X, LEFT)
        if centered:
            line.move_to([line.get_center()[0], card.get_center()[1], 0])
        return line

    def on_bg(self, text, font_size=36):
        return Text(text, font_size=font_size, color=WHITE, weight=BOLD)

    def bg_lines(self, *lines, font_size=36):
        group = VGroup(*[self.on_bg(line, font_size=font_size) for line in lines])
        group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        return group

    def shape_question(self, radius=0.8):
        circle = Circle(radius=radius, color=WHITE, stroke_width=3)
        mark = Text("?", font_size=90, color=YELLOW, weight=BOLD)
        mark.move_to(circle.get_center())
        return VGroup(circle, mark)

    def empty_card(self, side="right", width=5.6, height=5.0, label=None):
        card = RoundedRectangle(
            width=width,
            height=height,
            corner_radius=0.22,
            fill_color=WHITE,
            fill_opacity=0.96,
            stroke_color=GREY_B,
            stroke_width=1.5,
        )
        if label is not None:
            card.move_to(self.panel_anchor(side, label))
        else:
            anchor = self.right_center() if side == "right" else self.left_center()
            card.move_to(anchor)
        return card

    def typing_cursor_for(self, text_mob, cursor_color=YELLOW):
        return Rectangle(
            width=0.06,
            height=max(0.3, text_mob.height * 1.05),
            fill_color=cursor_color,
            fill_opacity=1,
            stroke_width=0,
        )

    def type_text(self, text_mob, time_per_char=0.05, cursor_color=YELLOW):
        cursor = self.typing_cursor_for(text_mob, cursor_color=cursor_color)
        if len(text_mob) > 0:
            cursor.move_to(text_mob[0])
        else:
            cursor.move_to(text_mob.get_left())
        self.play(
            TypeWithCursor(text_mob, cursor, time_per_char=time_per_char, leave_cursor_on=False),
            run_time=max(0.4, len(text_mob.text) * time_per_char),
        )

    def fade_clear(self, *mobjects, run_time=0.55):
        on_scene = set(self.mobjects)
        targets: list[Mobject] = []
        seen: set[int] = set()
        for m in mobjects:
            if m is None or not isinstance(m, Mobject):
                continue
            for mob in m.get_family():
                mob_id = id(mob)
                if mob_id in seen:
                    continue
                if mob in on_scene:
                    targets.append(mob)
                    seen.add(mob_id)
        if targets:
            self.play(*[FadeOut(m) for m in targets], run_time=run_time, rate_func=smooth)
            remaining = [m for m in targets if m in self.mobjects]
            if remaining:
                self.remove(*remaining)

    def sweep_foreground(self, run_time=0.3):
        """Remove every mobject except the background (catches detached emphasis slices)."""
        if len(self.mobjects) <= 1:
            return
        strays = [m for m in list(self.mobjects)[1:] if m in self.mobjects]
        if not strays:
            return
        if run_time <= 0.01:
            self.remove(*strays)
            return
        self.play(*[FadeOut(m) for m in strays], run_time=run_time, rate_func=smooth)
        remaining = [m for m in strays if m in self.mobjects]
        if remaining:
            self.remove(*remaining)

    def beat_transition(self, run_time=0.8, hold=0.15):
        """Pause between beats — keeps orange background visible (no black flash)."""
        if hasattr(self, "cam_restore"):
            self.cam_restore(run_time=min(run_time, 0.5))
        if hold > 0:
            self.wait(hold)


class BeatScene(BeatLayoutMixin, Scene):
    def setup_background(self):
        super().setup_background(overscale=1.0)


class MovingBeatScene(BeatLayoutMixin, MovingCameraScene):
    """MovingCameraScene with beat layout + cam_* helpers."""

    def setup_background(self):
        super().setup_background(overscale=1.25)

    def cam_restore(self, run_time=0.8):
        self.play(
            self.camera.frame.animate.set(width=config.frame_width)
            .set(height=config.frame_height)
            .move_to(ORIGIN),
            run_time=run_time,
            rate_func=smooth,
        )

    def cam_focus_point(self, point, width=PANEL_FRAME_WIDTH, run_time=1.0):
        height = config.frame_height * (width / config.frame_width)
        self.play(
            self.camera.frame.animate.set(width=width).set(height=height).move_to(point),
            run_time=run_time,
            rate_func=smooth,
        )

    def cam_focus_left(self, label, run_time=1.0):
        self.cam_focus_point(self.panel_anchor("left", label), run_time=run_time)

    def cam_focus_right(self, label, run_time=1.0):
        self.cam_focus_point(self.panel_anchor("right", label), run_time=run_time)

    def cam_focus_card(self, card, run_time=1.0):
        self.play(self.camera.auto_zoom(card, margin=0.5), run_time=run_time, rate_func=smooth)

    def cam_focus_mobject(self, mob, margin=0.4, run_time=0.9):
        self.play(self.camera.auto_zoom(mob, margin=margin), run_time=run_time, rate_func=smooth)
