# Manim Camera Guide (Course Videos)

Manim CE **v0.20.1** — synthesized from official camera docs for this repo’s beat workflow.

**Official references:** [reference/cameras/](.) + [INDEX.md](../INDEX.md) (cameras section)

---

## Which camera / scene to use

| Use case | Scene class | Camera class | Best for our course? |
|----------|-------------|--------------|----------------------|
| Static split layout (current beats) | `BeatScene` → `Scene` | `Camera` | ✅ default |
| Pan, zoom, follow frame | `MovingCameraScene` | `MovingCamera` | ✅ **primary camera upgrade** |
| Magnifier / PiP inset | `ZoomedScene` | `MovingCamera` + zoomed sub-camera | ✅ code detail, one word |
| 3D orbit, depth | `ThreeDScene` | `ThreeDCamera` | ⚠️ rare — 3D demos only |
| Warp / fisheye space | custom `MappingCamera` | `MappingCamera` | ❌ avoid for tutorials |
| Two live camera feeds | `SplitScreenCamera` | `OldMultiCamera` | ❌ we layout panels manually |
| Multiple perspectives | `MultiCamera` | `MultiCamera` | ❌ advanced compositing |

**BackgroundColoredVMobjectDisplayer** — internal helper on `Camera` for rendering VMobjects over a background image. Not chosen directly in beat scripts; our orange PNG is a full-frame `ImageMobject`.

---

## MovingCamera (most important)

**Docs:** [MovingCamera](moving_camera.md) · [MovingCameraScene](../scenes/moving_camera_scene.md)

The camera has a **`frame`** mobject (usually invisible `ScreenRectangle`) that defines what region is visible. Animating the frame = camera move.

### Core properties

| Property | Meaning |
|----------|---------|
| `self.camera.frame` | Rectangle controlling viewport |
| `self.camera.frame_center` | Center of visible region |
| `self.camera.frame_width` / `frame_height` | Visible size in Manim units |
| `self.camera.auto_zoom(mobs, margin=0)` | Fit frame around mobjects (2D XY only) |

### Common patterns

```python
class MyBeat(MovingCameraScene):  # not plain Scene
    def construct(self):
        self.setup_background()
        card = ...

        # Pan right panel
        self.play(
            self.camera.frame.animate.move_to(RIGHT * 3.55),
            run_time=1.0,
        )

        # Zoom in on card
        self.play(
            self.camera.frame.animate.set(width=7).move_to(card),
            run_time=1.2,
        )

        # Auto-zoom (returns animation)
        self.play(self.camera.auto_zoom(card, margin=0.4))

        # Restore full frame
        self.play(
            self.camera.frame.animate.set(width=config.frame_width)
            .set(height=config.frame_height)
            .move_to(ORIGIN),
            run_time=1.0,
        )
```

**Note:** `auto_zoom` fails correctly only for **2D objects in the XY plane** (not after 3D camera rotation).

---

## ZoomedScene (inset magnifier)

**Docs:** [ZoomedScene](../scenes/zoomed_scene.md)

Picture-in-picture: main frame stays wide; a small display shows a zoomed sub-region.

```python
class CodeZoom(ZoomedScene):
    def construct(self):
        self.setup_background()
        code = Code(...)
        self.play(Write(code))
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        self.activate_zooming(animate=True)
        self.play(self.get_zoom_in_animation())
```

Use for: zooming into **code**, a **single word**, or a **small diagram** without losing full-scene context.

---

## ThreeDCamera

**Docs:** [ThreeDCamera](three_d_camera.md) · [ThreeDScene](../scenes/three_d_scene.md)

Spherical-style camera with **phi**, **theta**, **gamma**, **zoom**, **focal_distance**.

```python
class Spin3D(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        label = Text("Title")
        self.add_fixed_in_frame_mobjects(label)  # stays on screen while camera orbits
        self.play(self.camera.theta_tracker.animate.set_value(30 * DEGREES), run_time=3)
```

| Method | Effect |
|--------|--------|
| `set_theta` / `theta_tracker` | Orbit around Z axis |
| `set_phi` / `phi_tracker` | Tilt off Z axis |
| `set_gamma` | Roll |
| `set_zoom` | Dolly in/out |
| `add_fixed_in_frame_mobjects(mob)` | HUD / labels fixed on screen |
| `add_fixed_orientation_mobjects(mob)` | Always face camera (3D labels) |

---

## MappingCamera & SplitScreenCamera

**MappingCamera** — applies `mapping_func(point) → point` to warp all geometry (bulge, ripple). Low-level; rarely needed for AI course slides.

**SplitScreenCamera(left_camera, right_camera)** — renders two camera views side-by-side. Legacy; our beats already use **left/right panel layout** on one static camera instead.

---

## MultiCamera

**MultiCamera** extends `MovingCamera`; composites `ImageMobjectFromCamera` sub-feeds. Used for advanced multi-view compositing, not typical lesson beats.

---

## Integration with this repo

### Scene base classes

| Script value | Python base | When |
|--------------|---------------|------|
| `camera: none` | `BeatScene` (`Scene`) | Default — beats 1–2 so far |
| `camera: moving` | `MovingBeatScene` (`MovingCameraScene`) | Pan / zoom between panels |
| `camera: zoomed` | `ZoomedBeatScene` (`ZoomedScene`) | PiP code zoom |
| `camera: 3d` | `ThreeDBeatScene` (`ThreeDScene`) | 3D object demos |

*(Implement `MovingBeatScene` in `beat_helpers.py` when first camera beat ships — same helpers as `BeatScene`.)*

### Where camera goes in a beat script

```
─── CAMERA ───
SCENE BASE:   moving
RESTORE:      yes @ beat exit   ← return to full frame before fade_all

TIMELINE (camera rows):
| t   | cam_focus_right(card) | run_time 1.0 |
| t   | cam_restore           | run_time 0.8 |
```

Between joined beats (`episode1_beats_1_2.py`): call **`cam_restore`** before `beat_transition()` if a beat ended zoomed in.

### Panel focus targets (14.22 × 8.0 canvas)

| Target | `frame.move_to` | Typical zoom width |
|--------|-----------------|-------------------|
| Full scene | `ORIGIN` | `14.22` (config.frame_width) |
| Left panel | `LEFT * 3.55` | `7.5` |
| Right panel | `RIGHT * 3.55` | `7.5` |
| Single card | `card.get_center()` | `card.width + 1.2` |
| Label + content | `DOWN * 0.4` | `12.0` |

---

## FocusOn vs camera

`FocusOn(target)` is an **animation** (darkens edges, scales view feel) but is **not** the same as moving `camera.frame`. Use:

- **`FocusOn`** — quick emphasis pulse on one mobject (no scene class change)
- **`camera.frame.animate`** — persistent reframing for a section of the beat

---

## Links (official)

- [Camera](https://docs.manim.community/en/stable/reference/manim.camera.camera.Camera.html)
- [BackgroundColoredVMobjectDisplayer](https://docs.manim.community/en/stable/reference/manim.camera.camera.BackgroundColoredVMobjectDisplayer.html)
- [MovingCamera](https://docs.manim.community/en/stable/reference/manim.camera.moving_camera.MovingCamera.html)
- [MappingCamera](https://docs.manim.community/en/stable/reference/manim.camera.mapping_camera.MappingCamera.html)
- [SplitScreenCamera](https://docs.manim.community/en/stable/reference/manim.camera.mapping_camera.SplitScreenCamera.html)
- [MultiCamera](https://docs.manim.community/en/stable/reference/manim.camera.multi_camera.MultiCamera.html)
- [ThreeDCamera](https://docs.manim.community/en/stable/reference/manim.camera.three_d_camera.ThreeDCamera.html)
