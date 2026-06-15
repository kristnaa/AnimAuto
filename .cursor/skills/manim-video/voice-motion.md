# Voice motion — Manim scene generation

Generate **standalone Manim CE scenes** for voice-driven motion graphics. No beat JSON, no cards, no icons, no themes.

**Director path:** Storyboard pages are compiled deterministically from layout templates (`center_title`, `flowchart_vertical`, etc.) using `voice_motion_helpers`. Prefer `TypeWithCursor` via `type_with_cursor()` over bare `Write` for narration text.

## Visual style (mandatory)

- Background: `self.camera.background_color = BLACK` (or `#000000`)
- Primary text: `Text(..., color=WHITE)` — use `Text`, not `MathTex`, unless the narration mentions an equation
- Accent shapes: Manim constants `BLUE`, `YELLOW`, `GREEN`, `RED`, `PURPLE`, `ORANGE`, `TEAL`, `PINK`
- Max 1–2 accent colors per segment
- No `BeatScene`, no `icon_library`, no `ImageMobject` from URLs, no card helpers

## Scene class

```python
from manim import *

class VoiceMotionScene(Scene):
    def construct(self):
        self.camera.background_color = BLACK
        # segment blocks with self.play / self.wait aligned to timestamps
```

## Timing rules

Each narration segment has `start` and `end` seconds from Whisper. For segment `[start, end]`:

1. Sum of `run_time` on all `self.play(...)` calls + all `self.wait(...)` in that block must equal `(end - start)` within ±0.15s
2. Use `# segment 0: 0.0–4.2s` comments above each block
3. Prefer `Write` or `FadeIn` for text; `Create` or `DrawBorderThenFill` for shapes
4. End each segment with `self.wait(...)` if animations finish early

## Allowed Manim toolkit

### Text
- `Text`, `Paragraph`, `MarkupText`
- Animations: `Write`, `FadeIn`, `FadeOut`, `Unwrite`

### 2D shapes
- `Circle`, `Square`, `Rectangle`, `RoundedRectangle`, `Polygon`, `RegularPolygon`
- `Line`, `Arrow`, `Dot`, `Arc`, `Annulus`, `Star`
- `Create`, `DrawBorderThenFill`, `GrowFromCenter`, `Circumscribe`, `Indicate`, `Flash`

### Motion
- `mobject.animate.shift()`, `.scale()`, `.rotate()`, `.set_color()`
- `Transform`, `ReplacementTransform`, `MoveAlongPath`
- `AnimationGroup`, `LaggedStart`, `Succession`

### Layout
- `.to_edge(UP/DOWN/LEFT/RIGHT)`, `.next_to()`, `.arrange(DOWN, buff=0.4)`, `VGroup`

### Graphs (when narration mentions data)
- `Axes`, `NumberPlane`, `axes.plot(...)`, `BarChart`

### 3D (sparingly)
- `ThreeDScene` only if plan says 3D; use `Sphere`, `Cube`, `set_camera_orientation`

## Segment → visual mapping

For each segment, pick visuals that **illustrate** the spoken words:

| Narration cue | Visual approach |
|---------------|-----------------|
| Introduction / title | Large centered `Text`, optional accent underline |
| List of items | `VGroup` of lines fading in with `LaggedStart` |
| Contrast / vs | Two shapes left/right, different colors |
| Growth / increase | Bar chart or arrow scaling up |
| Process / steps | Numbered circles + connecting arrows |
| Emphasis word | `Indicate` or color pulse on key text |

## Output format

Return **only** valid Python source. One file, one `VoiceMotionScene` class, complete `construct()` method.

## Forbidden

- `from beat_helpers import ...`
- `from icon_library import ...`
- `IconMobject`, external SVG/image loads
- `MathTex` unless equation is explicitly narrated
- `self.add_sound` (audio is muxed post-render)
