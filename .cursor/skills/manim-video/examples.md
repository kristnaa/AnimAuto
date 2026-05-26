# Project examples

Working scenes in this repo. Match their style when creating new animations.

## welcome_ai_course.py — `WelcomeAICourse`

**Type:** Course intro, two-screen sequence, background image.

Patterns:
- Full-screen PNG background via `ImageMobject` + `scale_to_fit_width(config.frame_width)`
- Stacked centered titles with manual `set_x` / `set_y`
- Python logo with `FadeIn` below course title
- Screen transition: `FadeOut` all foreground mobjects, keep background
- Second screen: topic lines + yellow code string
- Layered fade with `rate_func=smooth`

## hello_world_python.py — `HelloWorldToPython`

**Type:** `MovingCameraScene`, camera zoom/pan, connecting elements.

Patterns:
- `self.camera.frame.save_state()` / `Restore(self.camera.frame)`
- `self.camera.frame.animate.scale(...).move_to(...)`
- Side-by-side layout with `shift(LEFT/RIGHT * 3.5)`
- `Line` between mobjects, `Text` as connector symbol

## decorator_code_typing.py — `DecoratorCodeTyping`

**Type:** Code walkthrough with camera focus and callout boxes.

Patterns:
- Multi-line code as single `Text` with `\n`, `font="Courier New"`, `line_spacing=1.4`
- `SurroundingRectangle` around code and callouts
- Camera zoom into region before revealing detail
- Side callouts with `to_edge(RIGHT)` + `shift(UP/DOWN)`
- Long code reveal: `Write(code_text, run_time=10)`

## hello_world.py — `HelloWorld`

**Type:** Minimal `Scene`, single text fade.

Patterns:
- Basic `Write` + `FadeOut` lifecycle

## When to pick which base class

| Need | Base class |
|------|------------|
| Static camera, slides | `Scene` |
| Zoom, pan, focus | `MovingCameraScene` |
| 3D objects | `ThreeDScene` |

## Example request → scene mapping

| User asks for | Start from |
|---------------|------------|
| Course/module intro | `welcome_ai_course.py` |
| Explain Python code | `decorator_code_typing.py` |
| Compare two concepts side by side | `hello_world_python.py` |
| Simple demo | `hello_world.py` |
