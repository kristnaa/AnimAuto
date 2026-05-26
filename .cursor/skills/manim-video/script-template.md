# Animation Script Template

Copy, fill in, and paste when requesting a new Manim video.

**Source of truth:** `platform/assets/beat-script-template.md` (Studio) · `Episode{N}/beats/beat*/` (hand-authored Manim) · `animations/beat_helpers.py` · this file.

---

## Manimations Studio (Beat script tab)

In **Manimations Studio**, paste beats into the Beat script tab and click **Generate**.

**Icons — describe + color only (GPT picks Iconify):**

```markdown
─── ICONS ───
icon_python: Python programming language brand logo | color: #3776AB
icon_scream: screaming panicked emoji face | color: WHITE
shape_question: large question mark help circle | color: WHITE | scale: 1.8
```

- **1st icon** → primary (left panel). **2nd icon** → swap (punchline joke).
- GPT resolves descriptions to Iconify refs at Generate time.
- **Advanced:** paste explicit refs (`fa6-brands:python`) if you already know them.
- Template file: `platform/assets/beat-script-template.md`

---

## Episode beats (hand-authored Manim)

For `Episode{N}/beats/beat{M}/` Python scenes, sync icons via `icons.json` + `fetch_icons.py` (see below).

---

## META

| Field | Your value |
|-------|------------|
| **Episode** | e.g. `Episode1` |
| **Beat folder** | e.g. `Episode1/beats/beat1/` |
| **Scene file** | e.g. `welcome_to_python.py` |
| **Scene class** | e.g. `WelcomeToPython` |
| **Base scene** | `BeatScene` / `camera_none` (see [CAMERA](#camera-system)) |
| **Render** | preview `-ql` / final `-qh` |
| **Target duration** | optional, e.g. ~6s per beat |

### Repo layout (per beat)

```
Episode1/beats/beat1/
  icons.json              # {"icon_python": "fa6-brands:python", ...}
  icons/                  # synced SVGs from Iconify
    icon_python.svg
    icon_scream.svg
  welcome_to_python.py    # Scene class
```

```bash
# Sync beat icons
python .cursor/skills/manim-video/scripts/fetch_icons.py --episode 1 --beat 1

# Generate ASCII grid diagram
python .cursor/skills/manim-video/scripts/generate_grid.py --example beat1
python .cursor/skills/manim-video/scripts/generate_grid.py --list-layouts

# Render
manim -ql Episode1/beats/beat1/welcome_to_python.py WelcomeToPython
```

---

## CANVAS REFERENCE (Manim CE 16:9)

Origin **(0, 0) = screen center.** Frame **14.22 × 8.0**.

```
    ┌─────────────────────────────────────────────────────────────┐
    │  HEADING ZONE  — label @ to_edge(UP, buff=0.9)  YELLOW      │
    ├──────────────────────┬──────────────────────────────────────┤
    │  LEFT PANEL          │  RIGHT PANEL                         │
    │  x center: -3.55     │  x center: +3.55                     │
    │                      │                                      │
    │  icons / morphs /    │  white card  OR  white text on       │
    │  animations          │  orange (no card)                    │
    │                      │                                      │
    │  ▲ content_y         │  ▲ content_y                         │
    │  (centered in area   │  (centered in area BELOW heading,   │
    │   BELOW heading)     │   NOT full frame height)             │
    └──────────────────────┴──────────────────────────────────────┘
```

| Constant | Value | Notes |
|----------|-------|-------|
| `frame_width` | **14.22** | Full canvas width |
| `frame_height` | **8.0** | Full canvas height |
| `left_panel_center` | **(-3.55, content_y)** | Left 50% anchor |
| `right_panel_center` | **(+3.55, content_y)** | Right 50% anchor |
| `LABEL_TOP_BUFF` | **0.9** | Top margin (2× old 0.45) |
| `LABEL_CONTENT_GAP` | **0.25** | Gap below label before content |
| `side_margin` | **0.55** | Gap from panel edge to card |

### Vertical centering rule (important)

Panels are **not** centered on the full frame. They center in the **remaining height below the heading**:

```
content_top    = label.bottom - LABEL_CONTENT_GAP
content_bottom = -frame_height / 2
content_y      = (content_top + content_bottom) / 2
```

Example: if total height = 100 and heading zone = 20 → center card/icons in the bottom **80**.

### Default card sizes

| Preset | width × height | Use when |
|--------|----------------|----------|
| `card_sm` | 5.0 × 2.8 | 1–2 short lines |
| `card_md` | 5.6 × 3.8 | 3–5 lines |
| `card_lg` | 5.6 × 5.0 | 5 lines + punchline (beat 1 style) |
| `card_xl` | 5.6 × 5.2 | long code + text |

Card: white, `corner_radius=0.22`, text **black**, left-aligned.  
**Grow empty card first** — never `GrowFromCenter(card + text)` (text would appear instantly).

---

## LAYOUT PRESETS (grid patterns)

Pick one per beat. Generate ASCII diagram with `generate_grid.py`.

| Layout ID | Pattern |
|-----------|---------|
| `card_right_icon_left` | **Default** — card right, icon/visual left |
| `card_left_icon_right` | Card left, icon/visual right |
| `card_right_only` | Card right, left empty |
| `card_left_only` | Card left, right empty |
| `dual_card` | White card on **both** sides |
| `dual_icon` | Icons/visuals both sides, no card |
| `text_right_icon_left` | No card — white text right, icon left |
| `text_left_icon_right` | No card — white text left, icon right |
| `icon_left_anim_right` | Icon left, morph/animation right |
| `card_right_stack_left` | Card right, **stacked** icons left |

```bash
# Examples
python .cursor/skills/manim-video/scripts/generate_grid.py --example beat1

python .cursor/skills/manim-video/scripts/generate_grid.py \
  --layout text_right_icon_left \
  --label "Big Question" \
  --left shape_question \
  --bg-lines "So first…|what exactly is Python?"

python .cursor/skills/manim-video/scripts/generate_grid.py \
  --layout card_left_icon_right \
  --label "Recap" \
  --right icon_rocket \
  --card-side left \
  --card-lines "Line 1|Line 2|Line 3"
```

---

## GLOBAL STYLE

```
Background:     background/orange_theme_BG.png  (full frame)
Card:           white, rounded, black text, left-aligned
Labels:         YELLOW, top (buff=0.9), TypeWithCursor + WHITE cursor
Text on BG:     WHITE (when no card)
Text on card:   BLACK, TypeWithCursor + YELLOW cursor
Accent text:    RED allowed for emphasis words (e.g. joke punchline)
Icon colors:    WHITE default on orange; brand colors OK (e.g. BLUE python)
Camera:         none  ← later phase
Font label:     32
Font card body: 28
Font BG text:   34
```

### Text animation rules

| Element | Animation | Cursor |
|---------|-----------|--------|
| Label (yellow) | `anim_type` | WHITE |
| Card lines (black) | `anim_type` | YELLOW |
| BG text (white) | `anim_type` | YELLOW |
| Code | `anim_type_slow` | YELLOW + optional blink |

**Never pre-add text to scene before `TypeWithCursor`.**  
**Never bundle text inside `GrowFromCenter(card)`.**

---

## ICON / ELEMENT LIBRARY

### Studio beat script (recommended)

In the **ICONS** section, write **what you want + color** — no Iconify lookup required:

```
─── ICONS ───
icon_id: plain English description | color: WHITE | scale: 1.2
```

| Part | Example |
|------|---------|
| icon_id | `icon_python`, `icon_terminal`, `shape_question` |
| description | `Python programming language brand logo` |
| color | `WHITE`, `BLUE`, `#3776AB` |
| scale | optional, default 1.2 |

**Slot order:** 1st → primary (left). 2nd → swap (punchline).

**Examples**

```
icon_python: Python programming language brand logo | color: #3776AB
icon_scream: screaming panicked emoji face | color: WHITE
icon_terminal: command line terminal icon | color: WHITE
shape_question: large question mark help circle | color: WHITE | scale: 1.8
```

GPT resolves to Iconify at Generate. Icons cache under `assets/icons/cache/`.

### Episode folder (hand-authored Python)

**Loader:** `load_beat_icon(episode, beat, icon_id, scale=1.2, color=WHITE)`

Icons live in `Episode{N}/beats/beat{M}/icons/` (manifest in `icons.json`).  
Browse Iconify: https://icon-sets.iconify.design/

#### Beat 1 icons (reference)

| ID | Iconify ref | Color |
|----|-------------|-------|
| `icon_python` | `fa6-brands:python` | `#3776AB` |
| `icon_scream` | `twemoji:face-screaming-in-fear` | WHITE |

#### Global aliases (any beat)

| ID | Iconify ref | Use |
|----|-------------|-----|
| `icon_laptop` | `lucide:laptop` | Computer |
| `icon_editor` | `lucide:square-code` | IDE |
| `icon_file` | `lucide:file` | New file |
| `icon_rocket` | `lucide:rocket` | Launch |
| `icon_heart` | `lucide:heart` | Joke |
| `icon_sparkles` | `lucide:sparkles` | Celebration |
| `shape_question` | `lucide:circle-help` | Big question |

Register beat icons in `icons.json`, then `fetch_icons.py --episode N --beat M`.

---

## ANIMATION LIBRARY

| ID | Manim | Use for |
|----|-------|---------|
| `anim_type` | `TypeWithCursor` | **Default** all text |
| `anim_grow_card` | `GrowFromCenter` | Empty card only |
| `anim_fade_in` | `FadeIn` | Icons |
| `anim_fade_out` | `FadeOut` | Single element / card lines |
| `anim_swap_icon` | `FadeOut(a), FadeIn(b)` | Same anchor swap |
| `anim_wiggle` | `Wiggle` | Joke word + matching icon |
| `anim_word_red` | `text[idx].set_color(RED)` | Emphasis before wiggle |
| `anim_fade_all` | `FadeOut` group | End of beat |
| `anim_transform` | `ReplacementTransform` | Morphs |
| `anim_lagged_in` | `LaggedStart(FadeIn)` | Lists |

| Timing | Meaning |
|--------|---------|
| `wait_short` | 0.4s |
| `wait_med` | 1.2s |
| `hold` | **You set** — narration pause before exit |

---

## BEAT TEMPLATE (full)

One beat = one block. **Always include GRID + TIMELINE.**

```
### BEAT N — short_name

TYPE:       question | statement | list | joke | code_demo | recap | outro
DURATION:   ~Xs
LAYOUT:     card_right_icon_left   ← preset ID (see above)
EPISODE:    1
BEAT:       N
CAMERA:     none | moving | zoomed | 3d   ← default: none

─── GRID LAYOUT ───
(paste output from: python generate_grid.py --layout ... --label "...")

─── TIMELINE ───
| t (s) | Element              | Action                    | Disappears |
|-------|----------------------|---------------------------|------------|
| 0.0   | LABEL                | anim_type (white cursor)  | exit       |
| 0.3   | ui_card (empty)      | anim_grow_card            | exit       |
| 0.7   | TEXT line 1          | anim_type                 | t=X or fade|
| …     | …                    | …                         | …          |
| X.X   | icon_a (left)        | anim_fade_in              | swap/exit  |
| X.X   | card lines 1–N       | anim_fade_out             | —          |
| X.X   | icon_a → icon_b      | anim_swap_icon            | exit       |
| X.X   | punchline            | anim_type                 | exit       |
| X.X   | "word" + icon        | anim_word_red + anim_wiggle | —        |
| X.X   | HOLD                 | wait_med                  | —          |
| X.X   | ALL                  | anim_fade_all             | —          |

─── CONTENT ───
LABEL:
Your Yellow Label

TEXT (card, black):
Line one
Line two
Punchline line

─── ICONS ───
icon_python: Python programming language brand logo | color: #3776AB
icon_scream: screaming panicked emoji face | color: WHITE

─── CARD ───
CARD:        yes
SIDE:        right | left
SIZE:        card_lg (5.6 × 5.0)
POSITION:    panel_anchor(side, label)  ← below heading
APPEAR:      t=0.3, empty, anim_grow_card

─── SWAPS / SEQUENCES (optional) ───
- icon_python @ left content_y → fades out @ punchline
- icon_scream @ same anchor → fades in

HOLD: 1.2s
EXIT: anim_fade_all
```

---

## FILLED EXAMPLE — BEAT 1 (Episode 1)

```
### BEAT 1 — welcome_to_python

TYPE:       statement | joke punchline
DURATION:   ~6s
LAYOUT:     card_right_icon_left
EPISODE:    1 | BEAT: 1

─── GRID LAYOUT ───
┌─────────────────────────────────────────────────────────────┐
│  LABEL: "Welcome to Python for AI"  @ top buff=0.9  YELLOW  │
├──────────────────────┬──────────────────────────────────────┤
│  LEFT PANEL          │  RIGHT PANEL                         │
│  center (-3.55, y*)  │  center (+3.55, y*)                  │
│                      │                                      │
│  [icon_python]       │  [ui_card 5.6×5.0]                   │
│  BLUE, scale 1.2     │  empty → type lines                  │
│  → swaps to:         │                                      │
│  [icon_scream]       │  TEXT (black):                       │
│  same anchor         │  Today, we meet Python…              │
│                      │  the programming language            │
│                      │  that helps humans                   │
│                      │  talk to computers.  ← fade before   │
│                      │  Without screaming too much.         │
└──────────────────────┴──────────────────────────────────────┘
  * y = content_y (centered below heading, not frame center)

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

─── ICONS ───
icon_python: Python programming language brand logo | color: #3776AB
icon_scream: screaming panicked emoji face | color: WHITE

─── EMPHASIS ───
word: screaming | color: RED | animation: wiggle

─── CARD ───
SIDE: right | SIZE: 5.6 × 5.0

HOLD: 1.2s

─── IMPLEMENTATION ───
File: Episode1/beats/beat1/welcome_to_python.py
Class: WelcomeToPython(BeatScene)
```

Regenerate grid: `python .cursor/skills/manim-video/scripts/generate_grid.py --example beat1`

---

## BEAT TEMPLATE (compact)

```
### BEAT 3 — definition

LAYOUT: card_right_icon_left | HOLD: 3s | EXIT: fade_all
EPISODE: 1 | BEAT: 3

GRID:  python generate_grid.py --layout card_right_icon_left --label "..." --left morph_circle_square --card-lines "a|b|c"

TIMELINE:
  0.0  LABEL              → anim_type (white cursor)
  0.4  empty card (right)  → anim_grow_card
  0.7  line 1              → anim_type
  2.0  morph (left)        → anim_transform
  4.0  HOLD 3s
  5.0  ALL                 → anim_fade_all
```

---

## QUICK RULES

1. **One beat = one idea.** Max ~5–6 card lines; punchline can replace earlier lines.
2. **Always GRID + TIMELINE** — use `generate_grid.py` for the diagram.
3. **Layout preset ID** on every beat (`card_right_icon_left`, etc.).
4. **Episode folder** — scene + `icons.json` + `icons/` per beat.
5. **Empty card first**, then `anim_type` each line separately.
6. **Label animates** — `anim_type` with white cursor, not `FadeIn`.
7. **Panel vertical center** — below heading (`panel_anchor`), not frame center.
8. **Icon swaps** — `FadeOut` + `FadeIn` at same `panel_anchor`.
9. **Emphasis** — red word + wiggle (+ icon wiggle if paired).
10. **Icons (Studio)** — describe + color in ICONS section; GPT picks Iconify. **Icons (Episode)** — `icons.json` + `fetch_icons.py`.
11. **Camera:** optional — see [CAMERA](#camera-system) below; default `none`.

---

## CAMERA SYSTEM

**Full guide:** [reference/cameras/COURSE_GUIDE.md](reference/cameras/COURSE_GUIDE.md)  
**Raw API docs:** [reference/cameras/](reference/cameras/) (Manim CE v0.20.1)

### Scene base (pick one per scene file)

| Script ID | Python base | Camera class | Use when |
|-----------|-------------|--------------|----------|
| `camera_none` | `BeatScene` | `Camera` | **Default** — static frame (beats 1–2) |
| `camera_moving` | `MovingCameraScene` | `MovingCamera` | Pan / zoom / follow panels |
| `camera_zoomed` | `ZoomedScene` | `MovingCamera` + inset | PiP magnifier on code/detail |
| `camera_3d` | `ThreeDScene` | `ThreeDCamera` | 3D objects, orbit shots |

### Camera animation library (beat timeline IDs)

Use in **TIMELINE** like any other animation. All `cam_*` rows assume **`MovingCameraScene`** unless noted.

#### Pan (move frame center)

| ID | Manim | Target | Typical run_time |
|----|-------|--------|------------------|
| `cam_pan_left` | `camera.frame.animate.move_to(LEFT*3.55)` | Left panel | 0.8–1.2s |
| `cam_pan_right` | `camera.frame.animate.move_to(RIGHT*3.55)` | Right panel | 0.8–1.2s |
| `cam_pan_up` | `camera.frame.animate.shift(UP*1.5)` | Heading zone | 0.6s |
| `cam_pan_down` | `camera.frame.animate.shift(DOWN*1.5)` | Lower content | 0.6s |
| `cam_pan_to` | `camera.frame.animate.move_to(point)` | Custom `(x,y)` | 0.8–1.2s |

#### Zoom (change frame size)

| ID | Manim | Effect | Typical run_time |
|----|-------|--------|------------------|
| `cam_zoom_in` | `frame.animate.set(width=W).move_to(target)` | Tighter on target | 1.0–1.4s |
| `cam_zoom_out` | `frame.animate.set(width=14.22).move_to(ORIGIN)` | Wider view | 1.0s |
| `cam_auto_zoom` | `camera.auto_zoom(mobs, margin=0.4)` | Fit around mobject(s) | 1.0s |
| `cam_focus_left` | pan left + `width≈7.5` | Left panel fill | 1.0s |
| `cam_focus_right` | pan right + `width≈7.5` | Right panel fill | 1.0s |
| `cam_focus_card` | `auto_zoom(ui_card, margin=0.5)` | Single white card | 1.0s |
| `cam_focus_mobject` | `auto_zoom(icon, margin=0.3)` | One icon / shape | 0.8s |

#### Restore & transitions

| ID | Manim | Use when |
|----|-------|----------|
| `cam_restore` | `frame.animate.set(width=14.22).set(height=8.0).move_to(ORIGIN)` | End of beat / before next beat |
| `cam_restore_fast` | same, `run_time=0.5` | Quick reset between beats |

**Rule:** If a beat uses any zoom/pan, add **`cam_restore`** before `anim_fade_all` or before `beat_transition`.

#### ZoomedScene (inset PiP) — `camera_zoomed` base only

| ID | Manim | Use when |
|----|-------|----------|
| `cam_inset_activate` | `activate_zooming(animate=True)` | Enable magnifier |
| `cam_inset_zoom_in` | `get_zoom_in_animation(run_time=2)` | Zoom into target region |
| `cam_inset_pop_out` | `get_zoomed_display_pop_out_animation()` | Show PiP box |

#### ThreeDScene — `camera_3d` base only

| ID | Manim | Effect |
|----|-------|--------|
| `cam_3d_set` | `set_camera_orientation(phi=…, theta=…)` | Initial 3D angle |
| `cam_3d_orbit_theta` | `theta_tracker.animate.set_value(...)` | Spin around Z |
| `cam_3d_orbit_phi` | `phi_tracker.animate.set_value(...)` | Tilt up/down |
| `cam_3d_zoom` | `set_zoom(z)` / `zoom_tracker` | Dolly |
| `cam_3d_fixed_label` | `add_fixed_in_frame_mobjects(label)` | Label stays on screen during orbit |

#### Not recommended for course beats

| ID | Class | Why skip |
|----|-------|----------|
| `cam_split_screen` | `SplitScreenCamera` | We already split with left/right panels |
| `cam_warp` | `MappingCamera` | Distorts text — bad for readability |
| `cam_multi` | `MultiCamera` | Advanced compositing only |

#### Pseudo-camera (Scene stays `camera_none`)

| ID | Manim | Note |
|----|-------|------|
| `anim_focus_on` | `FocusOn(mob)` | Quick pulse — **not** a real frame move |

---

### Camera block in beat template

Add to any beat that uses camera:

```
─── CAMERA ───
SCENE BASE:   camera_none | camera_moving | camera_zoomed | camera_3d
RESTORE:      yes @ beat exit (required if any cam_zoom/pan used)

TIMELINE (camera rows — optional):
| t (s) | Camera              | Action           | run_time |
|-------|---------------------|------------------|----------|
| 2.5   | cam_focus_right     | card typing done | 1.0      |
| 4.0   | cam_restore         | before punchline | 0.8      |
| 5.5   | cam_restore         | beat exit        | 0.5      |
```

### Example — focus right panel during question (beat 2 style)

```
LAYOUT: text_right_icon_left
SCENE BASE: camera_moving

TIMELINE:
  0.0  LABEL                    → anim_type
  0.3  shape_question           → anim_fade_in
  0.8  "So first…"             → anim_type
  1.6  cam_focus_right          → run_time 1.0   # frame slides to question text
  2.2  "what exactly is Python?" → anim_type
  3.3  "Python"                 → anim_indicate
  3.8  cam_restore              → run_time 0.8
  4.0  HOLD 1.5s
  5.5  ALL                      → anim_fade_all
```

### Joined episodes (beats 1 + 2)

```
beat 1 … cam_restore (if zoomed) → beat_transition → beat 2 …
```

`beat_transition` = fade through black (already in `beat_helpers.py`). Always **`cam_restore`** before transition if the previous beat moved the frame.

---

## MINIMAL ONE-LINER (agent expands)

```
Episode1/beat2 | LAYOUT: text_right_icon_left | hold 2.5s

BEAT 2 [question]:
  LABEL: Big Question
  LEFT: shape_question
  RIGHT: white text — So first… / what exactly is Python?
  TIMELINE: 0 type label, 0.4 fade question, 0.8 type L1, 2.0 type L2, 6.0 fade_all
```

---

## CAMERA QUICK PICK

| I want to… | Use |
|------------|-----|
| Keep static layout (now) | `camera_none` |
| Push into left/right panel | `cam_focus_left` / `cam_focus_right` |
| Zoom one card | `cam_focus_card` |
| Zoom one icon | `cam_focus_mobject` |
| Fit arbitrary group | `cam_auto_zoom` |
| Reset before next beat | `cam_restore` |
| Magnify code in corner | `camera_zoomed` + `cam_inset_*` |
| Orbit a 3D shape | `camera_3d` + `cam_3d_orbit_*` |
| Quick flash on one thing | `anim_focus_on` (no camera change) |
