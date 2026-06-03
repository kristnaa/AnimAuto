# Text → Manim Pipeline

Adapted from [rohitg00/manim-video-generator](https://github.com/rohitg00/manim-video-generator) — an NLU-driven generator that turns natural language into Manim CE code.

**Source repo:** https://github.com/rohitg00/manim-video-generator

Use this when the user pastes narration, beats, or a plain-language brief (not raw Python).

---

## How that repo works

```
User text → NLU Classifier → Scene Composer → Prompt Engine → Manim code → Render
```

| Stage | What it does |
|-------|----------------|
| **NLU** | Classifies intent (explain, process, compare, kinetic text, etc.) |
| **Scene Composer** | Builds a scene graph: acts, mobjects, animations, timing |
| **Prompt Engine** | 4 stages: plan → choreograph → generate code → validate/fix |
| **Render** | Runs `manim` CLI, returns MP4 |

We replicate this **manually in Cursor** using beats + conventions — no Node/OpenAI required.

---

## Intent → layout pattern (from NLU types)

| User intent | Layout / pattern |
|-------------|------------------|
| `EXPLAIN_CONCEPT` | CLEAR method: Context → Layers → Examples → Reinforce |
| `DEMONSTRATE_PROCESS` | Step boxes, arrows, progressive reveal |
| `TELL_STORY` | Hook → setup → rising action → climax → resolution |
| `COMPARE_CONTRAST` | Left/right split (50% each) |
| `TRANSFORM_OBJECT` | Left: animation (circle→square); right: card with text |
| `KINETIC_TEXT` | `TypeWithCursor` + `Blink`; no camera zoom |
| `CREATE_SCENE` | Follow user's beat script literally |
| Code demo / IDE window / "show code" | Studio **`code_demo`** beat — `LAYOUT: code_full_card`, `─── CODE ───` block |

For **AI course videos**, default intent is `DEMONSTRATE_PROCESS` + `KINETIC_TEXT`.

---

## CLEAR storytelling framework

From `visual-storyteller` skill:

- **C**ontext — establish topic (welcome beat)
- **L**ayers — add complexity gradually (definition → uses → code)
- **E**xamples — concrete instances (Hello World, company names)
- **A**nalogies — visual metaphors (potato, snake vs Monty Python)
- **R**einforce — recap + outro badge

Map beats to CLEAR when user doesn't specify structure.

---

## Progressive revelation rules

**Never dump everything at once.**

1. Show label (yellow, top edge)
2. `GrowFromCenter` white card (if structured content)
3. `TypeWithCursor` text line by line
4. `wait(HOLD)` for narration
5. Left-side visual (diagram, morph, icon) **after** or **with** first text line
6. `FadeOut` entire beat group before next beat

| Content | Reveal speed (`time_per_char`) | Wait after |
|---------|-------------------------------|------------|
| Short label | 0.06 | 0.5s |
| Body line | 0.04–0.05 | 1–2s |
| Code line | 0.07 | 2–4s |
| Key insight | 0.05 + `Indicate` | 2–3s |

---

## Scene graph (mental model before coding)

For each beat, define:

```yaml
beat_id: beat_03_definition
intent: EXPLAIN_CONCEPT
layout:
  left: circle_to_square morph
  right: white_card
  label: top yellow
text:
  - line 1
  - line 2
animations:
  - GrowFromCenter(card)
  - TypeWithCursor(each line)
  - ReplacementTransform(circle, square)
hold: 3
exit: fade_all
```

This mirrors `SceneGraph` / `Act` from the upstream repo.

---

## Project overrides (manimations repo)

These **override** generic manim-video-generator defaults:

| Upstream | This project |
|----------|--------------|
| `Write(text)` | `TypeWithCursor(text, yellow cursor)` |
| `MovingCameraScene` zoom | Plain `Scene`, **no camera** unless user asks |
| Center everything | **50/50 split**: left = visual, right = white card |
| 3blue1brown dark BG | `orange_theme_BG.png` always |
| Mixed text colors | Black on card, yellow labels only, white on orange BG |
| `AddTextLetterByLetter` | `TypeWithCursor` |

---

## Beat script → Python mapping

| Beat field | Code |
|------------|------|
| `LABEL` | `self.top_label(...)` |
| `CARD: yes, side right` | `self.white_card(content, side="right")` |
| `CARD: yes, side left` | `self.white_card(content, side="left")` |
| `CARD: no` | `self.bg_lines(...)` on orange BG |
| `TEXT` lines | `self.card_lines(...)` + `self.type_lines(...)` |
| `CODE` | `self.code_box(...)` + `TypeWithCursor` |
| `LIST` | `LaggedStart(FadeIn(...))` inside card |
| `ELEMENTS: circle→square` | `ReplacementTransform(circle, square)` on left |
| `HOLD: 3s` | `self.wait(3)` |
| `EXIT: fade_all` | `self.fade_clear(...)` |

---

## Explanation patterns (from visual-storyteller)

### What → Why → How
Beats 1–3: what is Python → why AI → how code works

### Problem → Solution
Beat 16: typo `pritn` (problem) vs correct `print` (solution)

### Build-up
Beat 14: Hello World → Data → Model → AI Project stack

### Comparison
Beat 16: WORKS vs DOES NOT WORK code boxes

---

## Upstream skills (reference only)

The GitHub repo ships skills installable via SkillKit:

- `visual-storyteller` — narratives, CLEAR, progressive reveal ← **most relevant**
- `animation-composer` — multi-act, transitions, layout validation
- `math-visualizer` — equations, graphs, proofs
- `motion-graphics` — kinetic typography, titles
- `shared/core-animations.py` — reusable entrance/exit/emphasis helpers

Full repo: https://github.com/rohitg00/manim-video-generator/tree/main/skills

---

## When user gives plain text (not beats)

1. Classify intent (see table above)
2. Split into beats (~1 idea each, 2–4 lines max)
3. Assign layout: card L/R, visual on opposite side
4. Add HOLD times (~2s default)
5. Write `animations/xxx.py` using helpers from `intro_python_hello_world.py`
6. Validate with `validate.sh`

---

## Example: one-line prompt → beats

**Input:** "Explain print() and show Hello World for beginners"

**Auto beats:**
1. LABEL: What is print? | CARD right | TEXT: print shows text on screen
2. LEFT: code box | CARD right | CODE: print("Hello, World!")
3. LEFT: output box | CARD right | TEXT: Run the file → see output
4. RECAP list | CARD right

Then implement with `TypeWithCursor`, orange BG, white cards.
