# Voice motion style references

Drop **PNG, JPG, SVG, or WebP** screenshots here to guide the director's visual style.

## How it works

1. Add images (e.g. `blackboard-python-flow.png`)
2. Add a matching **`.md`** with the same base name describing blackboard rules, colors, and layout picks
3. Regenerate the **storyboard** — the director skill loads these notes automatically

## Active references

| Files | Style |
|-------|--------|
| `blackboard-python-flow.png` + `.md` | Blackboard L→R pipeline (“How X works”) |
| `blackboard-why-python.png` + `.md` | Blackboard radial mind map (“Why X”) |

Legacy alias: `whiteboard-python-flow.png` (same pipeline ref; render on **black** bg).

## Blackboard rules (both references)

- Black canvas, white chalk text, yellow arrows, blue highlights, red tags
- **Sketchy hand-drawn strokes** via `blackboard_sketch.py` (wobbly boxes, dashed arrows, chalk fonts)
- **SVG icons** from Iconify cache (`blackboard_icons.py`) — Pac-Man, rocket, brain, Python logo, etc.
- Narration in audio only — short labels + icons on screen
- Use layouts `pipeline_blackboard` and `mind_map_radial` with `blackboard_clean` background

## Limits

- References guide composition — Manim uses shape icons from `blackboard_icons.py`, not embedded PNGs in video
- For project-specific refs, upload to `projects/{id}/media/` and mention in Chat
