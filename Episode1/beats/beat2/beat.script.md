### BEAT 2 — what_is_python

TYPE:       question
DURATION:   ~5.5s
LAYOUT:     text_right_icon_left
EPISODE:    1 | BEAT: 2

─── GRID LAYOUT ───
See grid.txt

─── TIMELINE ───
| t (s) | Element           | Action                              |
|-------|-------------------|-------------------------------------|
| 0.0   | LABEL             | anim_type, white cursor             |
| 0.3   | shape_question    | anim_fade_in @ left content_y       |
| 0.8   | "So first…"       | anim_type @ right content_y         |
| 1.8   | pause             | wait_short 0.4s                     |
| 2.2   | "what exactly..." | anim_type                           |
| 3.3   | "Python"          | anim_indicate (YELLOW)              |
| 3.8   | HOLD              | wait_med 1.5s                       |
| 5.5   | ALL               | anim_fade_all                       |

─── CONTENT ───
LABEL:
Big Question

TEXT (white, on BG, right panel):
So first…
what exactly is Python?

─── ELEMENTS ───
shape_question @ left panel_anchor
  circle: WHITE stroke | "?" : YELLOW | height: 1.6

CARD: no

HOLD: 1.5s | EXIT: anim_fade_all

─── IMPLEMENTATION ───
File: Episode1/beats/beat2/what_is_python.py
Class: WhatIsPython(BeatScene)
