### BEAT 1 — welcome_to_python

TYPE:       statement | joke punchline
DURATION:   ~6s
LAYOUT:     card_right_icon_left
EPISODE:    1 | BEAT: 1

─── GRID LAYOUT ───
See grid.txt (regenerate: python .cursor/skills/manim-video/scripts/generate_grid.py --example beat1)

─── TIMELINE ───
| t (s) | Element           | Action                              |
|-------|-------------------|-------------------------------------|
| 0.0   | LABEL             | anim_type, white cursor             |
| 0.3   | ui_card (empty)   | anim_grow_card @ panel_anchor right |
| 0.7   | line 1            | anim_type                           |
| 1.5   | line 2            | anim_type                           |
| 2.3   | line 3            | anim_type                           |
| 3.0   | line 4            | anim_type                           |
| 3.5   | icon_python       | anim_fade_in @ left content_y       |
| 4.0   | lines 1–4         | anim_fade_out                       |
| 4.0   | icon_python       | anim_fade_out                       |
| 4.0   | icon_scream       | anim_fade_in @ same anchor          |
| 4.2   | punchline         | anim_type, card center              |
| 4.8   | "screaming"       | anim_word_red + anim_wiggle         |
| 4.8   | icon_scream       | anim_wiggle                         |
| 5.4   | HOLD              | wait_med 1.2s                       |
| 6.0   | ALL               | anim_fade_all                       |

─── CONTENT ───
LABEL:
Welcome to Python for AI

TEXT (card, black):
Today, we meet Python…
the programming language
that helps humans
talk to computers.
Without screaming too much.

─── ICONS (icons.json) ───
icon_python: fa6-brands:python
icon_scream: twemoji:face-screaming-in-fear

─── CARD ───
SIDE: right | SIZE: 5.6 × 5.0 | POSITION: panel_anchor(right, label)

HOLD: 1.2s | EXIT: anim_fade_all
