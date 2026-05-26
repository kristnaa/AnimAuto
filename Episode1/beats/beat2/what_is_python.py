"""BEAT 2 — what_is_python"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "animations"))

from manim import *

from beat_helpers import BeatScene, MovingBeatScene
from icon_library import load_beat_icon

EPISODE = 1
BEAT = 2


def run_beat_02_what_is_python(scene: BeatScene, *, use_camera: bool = False) -> None:
    label = scene.top_label("Big Question")

    question = load_beat_icon(EPISODE, BEAT, "shape_question", scale=1.4, color=WHITE)
    question.move_to(scene.panel_anchor("left", label))

    right_text = scene.bg_lines("So first…", "what exactly is Python?", font_size=36)
    right_text.move_to(scene.panel_anchor("right", label))

    scene.type_text(label, time_per_char=0.045, cursor_color=WHITE)
    scene.play(FadeIn(question), run_time=0.4)

    scene.type_text(right_text[0], time_per_char=0.06)

    if use_camera and isinstance(scene, MovingBeatScene):
        scene.cam_focus_left(label, run_time=0.9)

    scene.wait(0.4)

    if use_camera and isinstance(scene, MovingBeatScene):
        scene.cam_focus_right(label, run_time=1.0)

    scene.type_text(right_text[1], time_per_char=0.05)

    line2 = right_text[1]
    start = line2.text.find("Python")
    python_word = line2[start : start + len("Python")]
    scene.play(Indicate(python_word, color=YELLOW), run_time=0.55)

    scene.wait(1.2)

    if use_camera and isinstance(scene, MovingBeatScene):
        scene.cam_restore(run_time=0.7)

    scene.fade_clear(label, question, right_text, run_time=0.55)


class WhatIsPython(BeatScene):
    def construct(self):
        self.setup_background()
        run_beat_02_what_is_python(self)
