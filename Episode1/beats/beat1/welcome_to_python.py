"""BEAT 1 — welcome_to_python"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "animations"))

from manim import *

from beat_helpers import BeatScene, MovingBeatScene
from icon_library import load_beat_icon

EPISODE = 1
BEAT = 1


def run_beat_01_welcome_to_python(scene: BeatScene, *, use_camera: bool = False) -> None:
    label = scene.top_label("Welcome to Python for AI")
    card = scene.empty_card(side="right", width=5.6, height=5.0, label=label)

    lines_group = scene.card_lines(
        "Today, we meet Python…",
        "the programming language",
        "that helps humans",
        "talk to computers.",
        "Without screaming too much.",
        max_width=card.width - 2 * 0.45,
    )
    scene.place_card_content(lines_group, card)
    lines = VGroup(*[lines_group[i] for i in range(4)])
    line5 = lines_group[4]

    left_anchor = scene.panel_anchor("left", label)
    python_logo = load_beat_icon(EPISODE, BEAT, "icon_python", scale=1.2, color=BLUE)
    python_logo.move_to(left_anchor)
    scream_face = load_beat_icon(EPISODE, BEAT, "icon_scream", scale=1.2, color=None)
    scream_face.move_to(left_anchor)

    scene.type_text(label, time_per_char=0.045, cursor_color=WHITE)
    scene.play(GrowFromCenter(card), run_time=0.4)

    scene.type_text(lines[0], time_per_char=0.06)
    scene.type_text(lines[1], time_per_char=0.05)

    if use_camera and isinstance(scene, MovingBeatScene):
        scene.cam_focus_right(label, run_time=1.0)

    scene.type_text(lines[2], time_per_char=0.05)
    scene.type_text(lines[3], time_per_char=0.05)

    scene.play(FadeIn(python_logo), run_time=0.4)

    if use_camera and isinstance(scene, MovingBeatScene):
        scene.cam_focus_left(label, run_time=1.0)

    scene.play(*[FadeOut(line) for line in lines], run_time=0.4)
    scene.place_card_line(line5, card, centered=True)
    scene.play(FadeOut(python_logo), FadeIn(scream_face), run_time=0.4)

    if use_camera and isinstance(scene, MovingBeatScene):
        scene.cam_focus_card(card, run_time=0.9)

    scene.type_text(line5, time_per_char=0.05)

    start = line5.text.find("screaming")
    screaming = line5[start : start + len("screaming")]
    screaming.set_color(RED)
    scene.play(Wiggle(screaming), Wiggle(scream_face), run_time=0.6)

    scene.wait(1.2)

    if use_camera and isinstance(scene, MovingBeatScene):
        scene.cam_restore(run_time=0.7)

    scene.fade_clear(label, card, scream_face, line5, run_time=0.55)


class WelcomeToPython(BeatScene):
    def construct(self):
        self.setup_background()
        run_beat_01_welcome_to_python(self)
