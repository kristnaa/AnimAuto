"""BEAT 3 — simple_answer"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "animations"))

from manim import *

from beat_helpers import BeatScene, MovingBeatScene
from icon_library import load_beat_icon

EPISODE = 1
BEAT = 3


def _blink_cursor(scene: BeatScene, cursor: Mobject, times: int = 3) -> None:
    for _ in range(times):
        scene.play(FadeOut(cursor), run_time=0.1)
        scene.play(FadeIn(cursor), run_time=0.1)


def run_beat_03_simple_answer(scene: BeatScene, *, use_camera: bool = False) -> None:
    label = scene.top_label("Simple Answer")
    card = scene.empty_card(side="right", width=5.6, height=4.6, label=label)

    lines = scene.card_text_in(
        card,
        "Python is a programming language.",
        "We write instructions,",
        "and the computer follows them.",
        "Usually.",
    )

    left_anchor = scene.panel_anchor("left", label)
    laptop = load_beat_icon(EPISODE, BEAT, "icon_laptop", scale=1.2, color=WHITE)
    cursor = scene.typing_cursor_for(scene.on_card("A"))
    left_stack = VGroup(laptop, cursor).arrange(DOWN, buff=0.4)
    left_stack.move_to(left_anchor)

    scene.type_text(label, time_per_char=0.045, cursor_color=WHITE)
    scene.play(GrowFromCenter(card), run_time=0.4)

    scene.type_text(lines[0], time_per_char=0.05)

    if use_camera and isinstance(scene, MovingBeatScene):
        scene.cam_focus_card(card, run_time=0.9)

    line1 = lines[0]
    pl_start = line1.text.find("programming language")
    pl_word = line1[pl_start : pl_start + len("programming language")]
    scene.play(Indicate(pl_word, color=YELLOW), run_time=0.55)

    scene.type_text(lines[1], time_per_char=0.05)
    scene.type_text(lines[2], time_per_char=0.05)

    scene.play(FadeIn(laptop), run_time=0.35)

    if use_camera and isinstance(scene, MovingBeatScene):
        scene.cam_focus_left(label, run_time=0.9)

    scene.play(FadeIn(cursor), run_time=0.2)
    _blink_cursor(scene, cursor, times=3)

    if use_camera and isinstance(scene, MovingBeatScene):
        scene.cam_focus_card(card, run_time=0.9)

    scene.type_text(lines[3], time_per_char=0.06)
    scene.play(Wiggle(lines[3]), Wiggle(laptop), run_time=0.6)

    scene.wait(1.2)

    if use_camera and isinstance(scene, MovingBeatScene):
        scene.cam_restore(run_time=0.7)

    scene.fade_clear(label, card, laptop, cursor, *lines, run_time=0.55)


class SimpleAnswer(BeatScene):
    def construct(self):
        self.setup_background()
        run_beat_03_simple_answer(self)
