export const SAMPLE_BEAT_SCRIPT = `# Episode meta
CAMERA:      moving
STYLE_PACK:  course_clean
NAME:        Python Foundation Intro

### BEAT 1 — welcome_to_python

TYPE:       statement | joke punchline
DURATION:   ~6s
LAYOUT:     card_right_icon_left
CAMERA:     moving

─── TIMELINE ───
| 0.0   | LABEL             | anim_type, white cursor             |
| 0.3   | ui_card (empty)   | anim_grow_card @ right              |
| 0.7   | line 1–4          | anim_type                           |
| 3.5   | icon_python       | anim_fade_in @ left                 |
| 4.2   | punchline         | anim_type, card center              |
| 4.8   | "screaming"       | anim_word_red + anim_wiggle         |

─── CONTENT ───
LABEL:
Welcome to Python for AI

TEXT (card, black):
Today, we meet Python…
the programming language
that helps humans
talk to computers.
Without screaming too much.

─── ICONS ───
icon_python: Python programming language brand logo | color: #3776AB
icon_scream: screaming panicked emoji face | color: WHITE

─── CARD ───
SIDE: right | SIZE: 5.6 × 5.0

─── EMPHASIS ───
word: screaming | color: RED | animation: wiggle

─── CAMERA ───
cam_focus_right: after_line_2
cam_focus_left: after_icon
cam_focus_card: punchline
cam_restore: exit

HOLD: 1.2s

### BEAT 2 — what_is_python

TYPE:       question
DURATION:   ~5.5s
LAYOUT:     text_right_icon_left
CAMERA:     moving

─── CONTENT ───
LABEL:
Big Question

TEXT (white, on BG):
So first…
what exactly is Python?

─── ICONS ───
shape_question: large question mark help circle | color: WHITE | scale: 1.8

─── EMPHASIS ───
word: Python | color: YELLOW | animation: indicate

─── CAMERA ───
cam_focus_left: after_icon
cam_focus_right: after_line_1
cam_restore: exit

HOLD: 1.2s

### BEAT 3 — simple_answer

TYPE:       statement
DURATION:   ~7s
LAYOUT:     card_right_icon_left
CAMERA:     moving

─── CONTENT ───
LABEL:
Simple Answer

TEXT (card, black):
Python is a programming language.
We write instructions,
and the computer follows them.
Usually.

─── ICONS ───
icon_terminal: command line terminal icon | color: WHITE

─── EMPHASIS ───
word: programming language | color: YELLOW | animation: indicate
word: Usually | color: RED | animation: wiggle

─── CARD ───
SIDE: right | SIZE: 5.6 × 4.6

─── CAMERA ───
cam_focus_card: after_line_1
cam_focus_left: after_icon
cam_focus_card: punchline
cam_restore: exit

HOLD: 1.2s
`;
