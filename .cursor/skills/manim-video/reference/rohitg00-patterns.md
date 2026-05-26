# Patterns from manim-video-generator

Condensed from https://github.com/rohitg00/manim-video-generator (MIT).

## Text typing (prefer TypeWithCursor in this project)

Upstream `core-animations.py` uses `AddTextLetterByLetter`. **This repo uses:**

```python
cursor = Rectangle(width=0.06, height=0.35, fill_color=YELLOW, fill_opacity=1, stroke_width=0)
cursor.move_to(text[0])
self.play(TypeWithCursor(text, cursor, time_per_char=0.05, leave_cursor_on=True))
self.play(Blink(cursor, blinks=2))
```

## Entrance animations

| Function | Effect |
|----------|--------|
| `GrowFromCenter(mob)` | White card appear |
| `FadeIn(mob, shift=UP*0.15)` | List item |
| `LaggedStart(*anims, lag_ratio=0.12)` | Staggered list |
| `Create(shape)` | Diagram lines |
| `ReplacementTransform(a, b)` | Circle → square |

## Emphasis

| Function | When |
|----------|------|
| `Indicate(mob, color=YELLOW)` | Key word |
| `Wiggle(mob)` | Joke punchline |
| `SurroundingRectangle(mob, color=YELLOW)` | Highlight |
| `Cross(mob)` | "Not this" (use black stroke in this project) |

## Exit / transition

| Function | When |
|----------|------|
| `FadeOut(VGroup(...))` | End of beat |
| `ReplacementTransform(old, new)` | Code change challenge |
| Fade to black overlay | Final outro |

## Split-screen layout (comparison)

```python
# Left 50%: visual / animation
left_content.move_to(LEFT * frame_width / 4)

# Right 50%: white card
card.move_to(RIGHT * frame_width / 4)
```

Alternate card side on beats 6, 14, 16 for variety.

## Process walkthrough

```python
for step in steps:
    self.play(GrowFromCenter(card))
    self.type_lines(*step.text)
    self.play(FadeIn(step.visual))
    self.wait(step.hold)
    self.fade_clear(card, step.visual)
```

## Pacing table (visual-storyteller)

| Content | Animation | Wait |
|---------|-----------|------|
| New concept | slow type 0.05 | 2–3s |
| Process step | type 0.04 | 1–2s |
| Transition | FadeOut 0.55s | 0.3s |
| Final reveal | type + Indicate | 3s |

## Anti-patterns (avoid)

```python
# BAD: all at once
self.add(a, b, c, d)

# BAD: animate without adding
self.play(mob.animate.shift(RIGHT))  # mob never added

# BAD: camera zoom every beat (this project)
self.camera.frame.animate.scale(0.8)

# BAD: random colors on same card
Text("...", color=RED), Text("...", color=BLUE)
```

## NLU intent quick pick

| Keywords in user text | Intent |
|-----------------------|--------|
| explain, what is, why | EXPLAIN_CONCEPT |
| step 1, how to, tutorial | DEMONSTRATE_PROCESS |
| compare, vs, difference | COMPARE_CONTRAST |
| morph, transform, change to | TRANSFORM_OBJECT |
| type, write, code | KINETIC_TEXT |
| story, joke, fun fact | TELL_STORY |
