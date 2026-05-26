# Beat Script Template — Manimations Studio

Use this file in the **Beat script** tab. Studio parses every section and renders the video.

---

## How to use

1. Click **View template** or **Download** in the Beat script tab.
2. Copy the **STARTER SCRIPT** block below (from episode meta through your beats).
3. Paste into the Beat script editor.
4. Fill in placeholders — one `### BEAT` block per idea (~5–8 seconds each).
5. **Icons:** describe what you want + color — GPT picks the Iconify icon when you click **Generate**.
6. Click **Generate**. Use **Use AI author** only for rough narration → full script.

**Rules**

- Episode meta goes at the **top** (once).
- Every beat needs: TYPE, LAYOUT, CONTENT, ICONS, HOLD.
- Card beats: add CARD section + TEXT (card, black).
- Question beats: use `text_right_icon_left` + TEXT (white, on BG) — no card.
- Joke beats: setup lines in TEXT, last line as punchline; second icon = swap; EMPHASIS wiggle on punchline word.
- Camera beats: set `CAMERA: moving` (meta + beat) and add CAMERA hooks; always end with `cam_restore: exit`.
- Icons: first line = primary (left), second line = swap (punchline). You write **what** + **color** — not Iconify refs.

---

## STARTER SCRIPT — copy from here ↓

```
CAMERA:      moving          # none | moving
STYLE_PACK:  course_clean    # course_clean | playful
NAME:        Your Episode Title


### BEAT 1 — short_slug_name

TYPE:       statement          # statement | question | joke punchline | explain | recap
DURATION:   ~6s
LAYOUT:     card_right_icon_left
CAMERA:     moving             # moving | none

─── TIMELINE ───
| t (s) | Element           | Action                              |
|-------|-------------------|-------------------------------------|
| 0.0   | LABEL             | anim_type, white cursor             |
| 0.3   | ui_card (empty)   | anim_grow_card @ right              |
| 0.7   | line 1            | anim_type                           |
| 1.5   | line 2            | anim_type                           |
| 2.5   | icon_primary      | anim_fade_in @ left                 |
| 4.0   | HOLD              | wait_med 1.2s                       |
| 5.0   | ALL               | anim_fade_all                       |

─── CONTENT ───
LABEL:
Your Yellow Heading Here

TEXT (card, black):
First line of card text
Second line of card text
Optional third line

─── ICONS ───
icon_primary: sparkles celebration icon | color: WHITE
# icon_swap: screaming panicked emoji face | color: WHITE   # optional 2nd icon for punchline

─── CARD ───
SIDE: right | SIZE: 5.6 × 5.0

─── EMPHASIS ───
word: keyword | color: YELLOW | animation: indicate

─── CAMERA ───
cam_focus_right: after_line_1
cam_focus_left: after_icon
cam_restore: exit

HOLD: 1.2s
EXIT: anim_fade_all


### BEAT 2 — another_beat_slug

TYPE:       question
DURATION:   ~5s
LAYOUT:     text_right_icon_left
CAMERA:     moving

─── TIMELINE ───
| t (s) | Element           | Action                              |
|-------|-------------------|-------------------------------------|
| 0.0   | LABEL             | anim_type                           |
| 0.3   | shape_question    | anim_fade_in @ left                 |
| 0.8   | line 1            | anim_type @ right                   |
| 2.0   | line 2            | anim_type                           |
| 3.0   | HOLD              | wait_med 1.2s                       |

─── CONTENT ───
LABEL:
Your Question Label

TEXT (white, on BG):
First question line
Second question line?

─── ICONS ───
shape_question: large question mark help circle | color: WHITE | scale: 1.8

─── EMPHASIS ───
word: keyword | color: YELLOW | animation: indicate

─── CAMERA ───
cam_focus_left: after_icon
cam_focus_right: after_line_1
cam_restore: exit

HOLD: 1.2s
EXIT: anim_fade_all
```

---

## ICONS section — describe + color (GPT picks the icon)

Each line: `icon_id: what you want | color: COLOR | scale: 1.2`

| Part | Meaning |
|------|---------|
| **icon_id** | Local name (`icon_python`, `icon_terminal`, `shape_question`) |
| **description** | Plain English — GPT searches Iconify for the best match |
| **color** | `WHITE`, `BLUE`, `RED`, `YELLOW`, or hex `#3776AB` |
| **scale** | Optional size (default 1.2) |

**Slot order:** 1st icon → primary (left panel). 2nd icon → swap (punchline joke).

**Examples (you write these — no Iconify lookup needed)**

```
icon_python: Python programming language logo | color: #3776AB
icon_scream: screaming panicked emoji face | color: WHITE
icon_terminal: command line terminal | color: WHITE
shape_question: question mark help circle | color: WHITE | scale: 1.8
```

**Advanced:** if you already know the Iconify ref, you can paste it directly:

```
icon_python: fa6-brands:python | color: #3776AB
```

Icons download from Iconify at render time after GPT resolves your description.

---

## LAYOUT presets

| Layout ID | When to use |
|-----------|-------------|
| `card_right_icon_left` | **Default** — white card right, icon left |
| `card_left_icon_right` | Card left, icon right |
| `text_right_icon_left` | Questions — white text on orange, no card |
| `text_left_icon_right` | White text left, icon right |
| `card_right_only` | Card only, no icon |
| `dual_card` | Cards both sides |

---

## TYPE guide

| TYPE | Pattern |
|------|---------|
| `statement` | Card + icon, normal reveal |
| `question` | `text_right_icon_left`, no card |
| `joke punchline` | Setup lines + separate punchline; icon swap + wiggle |
| `explain` | Card + tool icon (terminal, code) |
| `recap` | Summary card, optional list |

---

## ANIMATION IDs (timeline)

| ID | Use |
|----|-----|
| `anim_type` | TypeWithCursor (all text) |
| `anim_grow_card` | GrowFromCenter empty card |
| `anim_fade_in` / `anim_fade_out` | Icons / elements |
| `anim_swap_icon` | FadeOut + FadeIn same anchor |
| `anim_word_red` + `anim_wiggle` | Joke emphasis |
| `anim_indicate` | Highlight word (YELLOW) |
| `anim_fade_all` | End of beat |

---

## CAMERA IDs (when CAMERA: moving)

| ID | Hook |
|----|------|
| `cam_focus_left` | `after_icon` |
| `cam_focus_right` | `after_line_1`, `after_line_2`, … |
| `cam_focus_card` | `punchline` |
| `cam_restore` | **`exit`** (required every beat) |

---

## CARD sizes

| SIZE | Use |
|------|-----|
| 5.6 × 5.0 | 4–5 lines + punchline |
| 5.6 × 4.6 | 3–4 lines |
| 5.6 × 3.8 | 2–3 short lines |
| 5.0 × 2.8 | 1–2 lines |

---

## FILLED EXAMPLES (reference)

### BEAT 1 — welcome_to_python (joke + icon swap)

```
### BEAT 1 — welcome_to_python

TYPE:       statement | joke punchline
DURATION:   ~6s
LAYOUT:     card_right_icon_left
CAMERA:     moving

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
```

### BEAT 2 — what_is_python (question, no card)

```
### BEAT 2 — what_is_python

TYPE:       question
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
```

### BEAT 3 — simple_answer (statement + indicate)

```
### BEAT 3 — simple_answer

TYPE:       statement
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
cam_restore: exit

HOLD: 1.2s
```

---

## Fields checklist (per beat)

| Section | Required? | Notes |
|---------|-----------|-------|
| `### BEAT N — slug` | Yes | Unique slug per beat |
| TYPE | Yes | statement, question, joke punchline |
| LAYOUT | Yes | See layout table |
| CONTENT / LABEL | Yes | Yellow top heading |
| CONTENT / TEXT | Yes | card or white-on-BG |
| ICONS | Yes | Description + color (GPT picks Iconify) |
| CARD | If card layout | SIDE + SIZE |
| EMPHASIS | If highlight word | word, color, animation |
| CAMERA | If moving | hooks + cam_restore exit |
| HOLD | Yes | Pause before exit (e.g. 1.2s) |

---

## JSON alternative (advanced)

```json
{
  "name": "Python Foundation Intro",
  "style_pack": "course_clean",
  "use_camera": true,
  "beats": [
    {
      "label": "Welcome to Python for AI",
      "type": "joke punchline",
      "layout": "card_right_icon_left",
      "card_lines": ["Today, we meet Python…", "the programming language", "that helps humans", "talk to computers."],
      "punchline_line": "Without screaming too much.",
      "visuals": {
        "primary": {"concept": "python", "description": "Python programming language brand logo", "color": "#3776AB"},
        "swap": {"concept": "frustration", "description": "screaming panicked emoji face", "trigger": "screaming", "color": "WHITE"}
      },
      "emphasis": [{"word": "screaming", "color": "RED", "animation": "wiggle"}],
      "hold": 1.2
    }
  ]
}
```

Visual concepts (catalog fallback if GPT unavailable): python, question, terminal, computer, code, ai, frustration, failure, success, sparkles
