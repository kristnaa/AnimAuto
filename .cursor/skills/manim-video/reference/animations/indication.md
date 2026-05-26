# Indication


---

## ApplyWave - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.indication.ApplyWave.html

ApplyWave¶

Qualified name: manim.animation.indication.ApplyWave

class ApplyWave(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Homotopy

Send a wave through the Mobject distorting it temporarily.

Parameters:

mobject (Mobject) – The mobject to be distorted.

direction (Vector3DLike) – The direction in which the wave nudges points of the shape

amplitude (float) – The distance points of the shape get shifted

wave_func (RateFunction) – The function defining the shape of one wave flank.

time_width (float) – The length of the wave relative to the width of the mobject.

ripples (int) – The number of ripples of the wave

run_time (float) – The duration of the animation.

kwargs (Any)

Examples

Example: ApplyingWaves ¶

from manim import *

class ApplyingWaves(Scene):
def construct(self):
tex = Tex("WaveWaveWaveWaveWave").scale(2)
self.play(ApplyWave(tex))
self.play(ApplyWave(
tex,
direction=RIGHT,
time_width=0.5,
amplitude=0.3
))
self.play(ApplyWave(
tex,
rate_func=linear,
ripples=4
))

class ApplyingWaves(Scene):
def construct(self):
tex = Tex("WaveWaveWaveWaveWave").scale(2)
self.play(ApplyWave(tex))
self.play(ApplyWave(
tex,
direction=RIGHT,
time_width=0.5,
amplitude=0.3
))
self.play(ApplyWave(
tex,
rate_func=linear,
ripples=4
))

Methods

Attributes

run_time

_original__init__(mobject, direction=array([0., 1., 0.]), amplitude=0.2, wave_func=<function smooth>, time_width=1, ripples=1, run_time=2, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

direction (Vector3DLike)

amplitude (float)

wave_func (RateFunction)

time_width (float)

ripples (int)

run_time (float)

kwargs (Any)


---

## Blink - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.indication.Blink.html

Blink¶

Qualified name: manim.animation.indication.Blink

class Blink(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Succession

Blink the mobject.

Parameters:

mobject (Mobject) – The mobject to be blinked.

time_on (float) – The duration that the mobject is shown for one blink.

time_off (float) – The duration that the mobject is hidden for one blink.

blinks (int) – The number of blinks

hide_at_end (bool) – Whether to hide the mobject at the end of the animation.

kwargs (Any) – Additional arguments to be passed to the Succession constructor.

Examples

Example: BlinkingExample ¶

from manim import *

class BlinkingExample(Scene):
def construct(self):
text = Text("Blinking").scale(1.5)
self.add(text)
self.play(Blink(text, blinks=3))

class BlinkingExample(Scene):
def construct(self):
text = Text("Blinking").scale(1.5)
self.add(text)
self.play(Blink(text, blinks=3))

Methods

Attributes

run_time

_original__init__(mobject, time_on=0.5, time_off=0.5, blinks=1, hide_at_end=False, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

time_on (float)

time_off (float)

blinks (int)

hide_at_end (bool)

kwargs (Any)


---

## Circumscribe - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.indication.Circumscribe.html

Circumscribe¶

Qualified name: manim.animation.indication.Circumscribe

class Circumscribe(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Succession

Draw a temporary line surrounding the mobject.

Parameters:

mobject (Mobject) – The mobject to be circumscribed.

shape (type[Rectangle] | type[Circle]) – The shape with which to surround the given mobject. Should be either
Rectangle or Circle

fade_in (bool) – Whether to make the surrounding shape to fade in. It will be drawn otherwise.

fade_out (bool) – Whether to make the surrounding shape to fade out. It will be undrawn otherwise.

time_width (float) – The time_width of the drawing and undrawing. Gets ignored if either fade_in or fade_out is True.

buff (float) – The distance between the surrounding shape and the given mobject.

color (ParsableManimColor) – The color of the surrounding shape.

run_time (float) – The duration of the entire animation.

kwargs (Any) – Additional arguments to be passed to the Succession constructor

stroke_width (float)

Examples

Example: UsingCircumscribe ¶

from manim import *

class UsingCircumscribe(Scene):
def construct(self):
lbl = Tex(r"Circum-\\scribe").scale(2)
self.add(lbl)
self.play(Circumscribe(lbl))
self.play(Circumscribe(lbl, Circle))
self.play(Circumscribe(lbl, fade_out=True))
self.play(Circumscribe(lbl, time_width=2))
self.play(Circumscribe(lbl, Circle, True))

class UsingCircumscribe(Scene):
def construct(self):
lbl = Tex(r"Circum-\\scribe").scale(2)
self.add(lbl)
self.play(Circumscribe(lbl))
self.play(Circumscribe(lbl, Circle))
self.play(Circumscribe(lbl, fade_out=True))
self.play(Circumscribe(lbl, time_width=2))
self.play(Circumscribe(lbl, Circle, True))

Methods

Attributes

run_time

_original__init__(mobject, shape=<class 'manim.mobject.geometry.polygram.Rectangle'>, fade_in=False, fade_out=False, time_width=0.3, buff=0.1, color=ManimColor('#FFFF00'), run_time=1, stroke_width=4, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

shape (type[Rectangle] | type[Circle])

fade_in (bool)

fade_out (bool)

time_width (float)

buff (float)

color (ParsableManimColor)

run_time (float)

stroke_width (float)

kwargs (Any)


---

## Flash - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.indication.Flash.html

Flash¶

Qualified name: manim.animation.indication.Flash

class Flash(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: AnimationGroup

Send out lines in all directions.

Parameters:

point (Point3DLike | Mobject) – The center of the flash lines. If it is a Mobject its center will be used.

line_length (float) – The length of the flash lines.

num_lines (int) – The number of flash lines.

flash_radius (float) – The distance from point at which the flash lines start.

line_stroke_width (int) – The stroke width of the flash lines.

color (ParsableManimColor) – The color of the flash lines.

time_width (float) – The time width used for the flash lines. See ShowPassingFlash for more details.

run_time (float) – The duration of the animation.

kwargs (Any) – Additional arguments to be passed to the Succession constructor

Examples

Example: UsingFlash ¶

from manim import *

class UsingFlash(Scene):
def construct(self):
dot = Dot(color=PURE_YELLOW).shift(DOWN)
self.add(Tex("Flash the dot below:"), dot)
self.play(Flash(dot))
self.wait()

class UsingFlash(Scene):
def construct(self):
dot = Dot(color=PURE_YELLOW).shift(DOWN)
self.add(Tex("Flash the dot below:"), dot)
self.play(Flash(dot))
self.wait()

Example: FlashOnCircle ¶

from manim import *

class FlashOnCircle(Scene):
def construct(self):
radius = 2
circle = Circle(radius)
self.add(circle)
self.play(Flash(
circle, line_length=1,
num_lines=30, color=RED,
flash_radius=radius+SMALL_BUFF,
time_width=0.3, run_time=2,
rate_func = rush_from
))

class FlashOnCircle(Scene):
def construct(self):
radius = 2
circle = Circle(radius)
self.add(circle)
self.play(Flash(
circle, line_length=1,
num_lines=30, color=RED,
flash_radius=radius+SMALL_BUFF,
time_width=0.3, run_time=2,
rate_func = rush_from
))

Methods

create_line_anims

create_lines

Attributes

run_time

_original__init__(point, line_length=0.2, num_lines=12, flash_radius=0.1, line_stroke_width=3, color=ManimColor('#FFFF00'), time_width=1, run_time=1.0, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

point (TypeAliasForwardRef('~manim.typing.Point3DLike') | Mobject)

line_length (float)

num_lines (int)

flash_radius (float)

line_stroke_width (int)

color (ParsableManimColor)

time_width (float)

run_time (float)

kwargs (Any)


---

## FocusOn - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.indication.FocusOn.html

FocusOn¶

Qualified name: manim.animation.indication.FocusOn

class FocusOn(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Transform

Shrink a spotlight to a position.

Parameters:

focus_point (Point3DLike | Mobject) – The point at which to shrink the spotlight. If it is a Mobject its center will be used.

opacity (float) – The opacity of the spotlight.

color (ParsableManimColor) – The color of the spotlight.

run_time (float) – The duration of the animation.

kwargs (Any)

Examples

Example: UsingFocusOn ¶

from manim import *

class UsingFocusOn(Scene):
def construct(self):
dot = Dot(color=PURE_YELLOW).shift(DOWN)
self.add(Tex("Focusing on the dot below:"), dot)
self.play(FocusOn(dot))
self.wait()

class UsingFocusOn(Scene):
def construct(self):
dot = Dot(color=PURE_YELLOW).shift(DOWN)
self.add(Tex("Focusing on the dot below:"), dot)
self.play(FocusOn(dot))
self.wait()

Methods

create_target

Attributes

path_arc

path_func

run_time

_original__init__(focus_point, opacity=0.2, color=ManimColor('#888888'), run_time=2, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

focus_point (TypeAliasForwardRef('~manim.typing.Point3DLike') | Mobject)

opacity (float)

color (ParsableManimColor)

run_time (float)

kwargs (Any)


---

## Indicate - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.indication.Indicate.html

Indicate¶

Qualified name: manim.animation.indication.Indicate

class Indicate(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Transform

Indicate a Mobject by temporarily resizing and recoloring it.

Parameters:

mobject (Mobject) – The mobject to indicate.

scale_factor (float) – The factor by which the mobject will be temporally scaled

color (ParsableManimColor) – The color the mobject temporally takes.

rate_func (RateFunction) – The function defining the animation progress at every point in time.

kwargs (Any) – Additional arguments to be passed to the Succession constructor

Examples

Example: UsingIndicate ¶

from manim import *

class UsingIndicate(Scene):
def construct(self):
tex = Tex("Indicate").scale(3)
self.play(Indicate(tex))
self.wait()

class UsingIndicate(Scene):
def construct(self):
tex = Tex("Indicate").scale(3)
self.play(Indicate(tex))
self.wait()

Methods

create_target

Attributes

path_arc

path_func

run_time

_original__init__(mobject, scale_factor=1.2, color=ManimColor('#FFFF00'), rate_func=<function there_and_back>, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

scale_factor (float)

color (ParsableManimColor)

rate_func (RateFunction)

kwargs (Any)


---

## ShowPassingFlash - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.indication.ShowPassingFlash.html

ShowPassingFlash¶

Qualified name: manim.animation.indication.ShowPassingFlash

class ShowPassingFlash(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: ShowPartial

Show only a sliver of the VMobject each frame.

Parameters:

mobject (VMobject) – The mobject whose stroke is animated.

time_width (float) – The length of the sliver relative to the length of the stroke.

kwargs (Any)

Examples

Example: TimeWidthValues ¶

from manim import *

class TimeWidthValues(Scene):
def construct(self):
p = RegularPolygon(5, color=DARK_GRAY, stroke_width=6).scale(3)
lbl = VMobject()
self.add(p, lbl)
p = p.copy().set_color(BLUE)
for time_width in [0.2, 0.5, 1, 2]:
lbl.become(Tex(r"\texttt{time\_width={{%.1f}}}"%time_width))
self.play(ShowPassingFlash(
p.copy().set_color(BLUE),
run_time=2,
time_width=time_width
))

class TimeWidthValues(Scene):
def construct(self):
p = RegularPolygon(5, color=DARK_GRAY, stroke_width=6).scale(3)
lbl = VMobject()
self.add(p, lbl)
p = p.copy().set_color(BLUE)
for time_width in [0.2, 0.5, 1, 2]:
lbl.become(Tex(r"\texttt{time\_width={{%.1f}}}"%time_width))
self.play(ShowPassingFlash(
p.copy().set_color(BLUE),
run_time=2,
time_width=time_width
))

See also

Create

Methods

clean_up_from_scene

Clean up the Scene after finishing the animation.

Attributes

run_time

_original__init__(mobject, time_width=0.1, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (VMobject)

time_width (float)

kwargs (Any)

Return type:
None

clean_up_from_scene(scene)[source]¶
Clean up the Scene after finishing the animation.

This includes to remove() the Animation’s
Mobject if the animation is a remover.

Parameters:
scene (Scene) – The scene the animation should be cleaned up from.

Return type:
None


---

## ShowPassingFlashWithThinningStrokeWidth - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.indication.ShowPassingFlashWithThinningStrokeWidth.html

ShowPassingFlashWithThinningStrokeWidth¶

Qualified name: manim.animation.indication.ShowPassingFlashWithThinningStrokeWidth

class ShowPassingFlashWithThinningStrokeWidth(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: AnimationGroup

Methods

Attributes

run_time

Parameters:

vmobject (VMobject)

n_segments (int)

time_width (float)

remover (bool)

kwargs (Any)

_original__init__(vmobject, n_segments=10, time_width=0.1, remover=True, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

vmobject (VMobject)

n_segments (int)

time_width (float)

remover (bool)

kwargs (Any)


---

## Wiggle - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.indication.Wiggle.html

Wiggle¶

Qualified name: manim.animation.indication.Wiggle

class Wiggle(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Animation

Wiggle a Mobject.

Parameters:

mobject (Mobject) – The mobject to wiggle.

scale_value (float) – The factor by which the mobject will be temporarily scaled.

rotation_angle (float) – The wiggle angle.

n_wiggles (int) – The number of wiggles.

scale_about_point (Point3DLike | None) – The point about which the mobject gets scaled.

rotate_about_point (Point3DLike | None) – The point around which the mobject gets rotated.

run_time (float) – The duration of the animation

kwargs (Any)

Examples

Example: ApplyingWaves ¶

from manim import *

class ApplyingWaves(Scene):
def construct(self):
tex = Tex("Wiggle").scale(3)
self.play(Wiggle(tex))
self.wait()

class ApplyingWaves(Scene):
def construct(self):
tex = Tex("Wiggle").scale(3)
self.play(Wiggle(tex))
self.wait()

Methods

get_rotate_about_point

get_scale_about_point

interpolate_submobject

Attributes

run_time

_original__init__(mobject, scale_value=1.1, rotation_angle=0.06283185307179587, n_wiggles=6, scale_about_point=None, rotate_about_point=None, run_time=2, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

scale_value (float)

rotation_angle (float)

n_wiggles (int)

scale_about_point (TypeAliasForwardRef('~manim.typing.Point3DLike') | None)

rotate_about_point (TypeAliasForwardRef('~manim.typing.Point3DLike') | None)

run_time (float)

kwargs (Any)
