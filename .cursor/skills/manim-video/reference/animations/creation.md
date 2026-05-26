# Creation


---

## AddTextLetterByLetter - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.AddTextLetterByLetter.html

AddTextLetterByLetter¶

Qualified name: manim.animation.creation.AddTextLetterByLetter

class AddTextLetterByLetter(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: ShowIncreasingSubsets

Show a Text letter by letter on the scene.

Parameters:

time_per_char (float) – Frequency of appearance of the letters.

tip:: (..) – This is currently only possible for class:~.Text and not for class:~.MathTex

text (Text)

suspend_mobject_updating (bool)

int_func (Callable[[np.ndarray], np.ndarray])

rate_func (Callable[[float], float])

run_time (float | None)

Methods

Attributes

run_time

_original__init__(text, suspend_mobject_updating=False, int_func=<ufunc 'ceil'>, rate_func=<function linear>, time_per_char=0.1, run_time=None, reverse_rate_function=False, introducer=True, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

text (Text)

suspend_mobject_updating (bool)

int_func (Callable[[np.ndarray], np.ndarray])

rate_func (Callable[[float], float])

time_per_char (float)

run_time (float | None)

Return type:
None


---

## AddTextWordByWord - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.AddTextWordByWord.html

AddTextWordByWord¶

Qualified name: manim.animation.creation.AddTextWordByWord

class AddTextWordByWord(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Succession

Show a Text word by word on the scene. Note: currently broken.

Methods

Attributes

run_time

Parameters:

text_mobject (Text)

run_time (float)

time_per_char (float)

_original__init__(text_mobject, run_time=None, time_per_char=0.06, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

text_mobject (Text)

run_time (float)

time_per_char (float)

Return type:
None


---

## Create - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.Create.html

Create¶

Qualified name: manim.animation.creation.Create

class Create(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: ShowPartial

Incrementally show a VMobject.

Parameters:

mobject (VMobject | OpenGLVMobject | OpenGLSurface) – The VMobject to animate.

lag_ratio (float)

introducer (bool)

Raises:
TypeError – If mobject is not an instance of VMobject.

Examples

Example: CreateScene ¶

from manim import *

class CreateScene(Scene):
def construct(self):
self.play(Create(Square()))

class CreateScene(Scene):
def construct(self):
self.play(Create(Square()))

See also

ShowPassingFlash

Methods

Attributes

run_time

_original__init__(mobject, lag_ratio=1.0, introducer=True, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (VMobject | OpenGLVMobject | OpenGLSurface)

lag_ratio (float)

introducer (bool)

Return type:
None


---

## DrawBorderThenFill - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.DrawBorderThenFill.html

DrawBorderThenFill¶

Qualified name: manim.animation.creation.DrawBorderThenFill

class DrawBorderThenFill(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Animation

Draw the border first and then show the fill.

Examples

Example: ShowDrawBorderThenFill ¶

from manim import *

class ShowDrawBorderThenFill(Scene):
def construct(self):
self.play(DrawBorderThenFill(Square(fill_opacity=1, fill_color=ORANGE)))

class ShowDrawBorderThenFill(Scene):
def construct(self):
self.play(DrawBorderThenFill(Square(fill_opacity=1, fill_color=ORANGE)))

Methods

begin

Begin the animation.

get_all_mobjects

Get all mobjects involved in the animation.

get_outline

get_stroke_color

interpolate_submobject

Attributes

run_time

Parameters:

vmobject (VMobject | OpenGLVMobject)

run_time (float)

rate_func (Callable[[float], float])

stroke_width (float)

stroke_color (str)

introducer (bool)

_original__init__(vmobject, run_time=2, rate_func=<function double_smooth>, stroke_width=2, stroke_color=None, introducer=True, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

vmobject (VMobject | OpenGLVMobject)

run_time (float)

rate_func (Callable[[float], float])

stroke_width (float)

stroke_color (str)

introducer (bool)

Return type:
None

begin()[source]¶
Begin the animation.

This method is called right as an animation is being played. As much
initialization as possible, especially any mobject copying, should live in this
method.

Return type:
None

get_all_mobjects()[source]¶
Get all mobjects involved in the animation.

Ordering must match the ordering of arguments to interpolate_submobject

Returns:
The sequence of mobjects.

Return type:
Sequence[Mobject]


---

## RemoveTextLetterByLetter - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.RemoveTextLetterByLetter.html

RemoveTextLetterByLetter¶

Qualified name: manim.animation.creation.RemoveTextLetterByLetter

class RemoveTextLetterByLetter(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: AddTextLetterByLetter

Remove a Text letter by letter from the scene.

Parameters:

time_per_char (float) – Frequency of appearance of the letters.

tip:: (..) – This is currently only possible for class:~.Text and not for class:~.MathTex

text (Text)

suspend_mobject_updating (bool)

int_func (Callable[[np.ndarray], np.ndarray])

rate_func (Callable[[float], float])

run_time (float | None)

Methods

Attributes

run_time

_original__init__(text, suspend_mobject_updating=False, int_func=<ufunc 'ceil'>, rate_func=<function linear>, time_per_char=0.1, run_time=None, reverse_rate_function=True, introducer=False, remover=True, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

text (Text)

suspend_mobject_updating (bool)

int_func (Callable[[np.ndarray], np.ndarray])

rate_func (Callable[[float], float])

time_per_char (float)

run_time (float | None)

Return type:
None


---

## ShowIncreasingSubsets - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.ShowIncreasingSubsets.html

ShowIncreasingSubsets¶

Qualified name: manim.animation.creation.ShowIncreasingSubsets

class ShowIncreasingSubsets(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Animation

Show one submobject at a time, leaving all previous ones displayed on screen.

Examples

Example: ShowIncreasingSubsetsScene ¶

from manim import *

class ShowIncreasingSubsetsScene(Scene):
def construct(self):
p = VGroup(Dot(), Square(), Triangle())
self.add(p)
self.play(ShowIncreasingSubsets(p))
self.wait()

class ShowIncreasingSubsetsScene(Scene):
def construct(self):
p = VGroup(Dot(), Square(), Triangle())
self.add(p)
self.play(ShowIncreasingSubsets(p))
self.wait()

Methods

interpolate_mobject

Interpolates the mobject of the Animation based on alpha value.

update_submobject_list

Attributes

run_time

Parameters:

group (Mobject)

suspend_mobject_updating (bool)

int_func (Callable[[np.ndarray], np.ndarray])

_original__init__(group, suspend_mobject_updating=False, int_func=<ufunc 'floor'>, reverse_rate_function=False, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

group (Mobject)

suspend_mobject_updating (bool)

int_func (Callable[[ndarray], ndarray])

Return type:
None

interpolate_mobject(alpha)[source]¶
Interpolates the mobject of the Animation based on alpha value.

Parameters:
alpha (float) – A float between 0 and 1 expressing the ratio to which the animation
is completed. For example, alpha-values of 0, 0.5, and 1 correspond
to the animation being completed 0%, 50%, and 100%, respectively.

Return type:
None


---

## ShowPartial - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.ShowPartial.html

ShowPartial¶

Qualified name: manim.animation.creation.ShowPartial

class ShowPartial(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Animation

Abstract class for Animations that show the VMobject partially.

Raises:
TypeError – If mobject is not an instance of VMobject.

Parameters:
mobject (VMobject | OpenGLVMobject | OpenGLSurface | None)

See also

Create, ShowPassingFlash

Methods

interpolate_submobject

Attributes

run_time

_original__init__(mobject, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:
mobject (VMobject | OpenGLVMobject | OpenGLSurface | None)


---

## ShowSubmobjectsOneByOne - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.ShowSubmobjectsOneByOne.html

ShowSubmobjectsOneByOne¶

Qualified name: manim.animation.creation.ShowSubmobjectsOneByOne

class ShowSubmobjectsOneByOne(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: ShowIncreasingSubsets

Show one submobject at a time, removing all previously displayed ones from screen.

Methods

update_submobject_list

Attributes

run_time

Parameters:

group (Iterable[Mobject])

int_func (Callable[[np.ndarray], np.ndarray])

_original__init__(group, int_func=<ufunc 'ceil'>, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

group (Iterable[Mobject])

int_func (Callable[[ndarray], ndarray])

Return type:
None


---

## SpiralIn - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.SpiralIn.html

SpiralIn¶

Qualified name: manim.animation.creation.SpiralIn

class SpiralIn(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Animation

Create the Mobject with sub-Mobjects flying in on spiral trajectories.

Parameters:

shapes (Mobject) – The Mobject on which to be operated.

scale_factor (float) – The factor used for scaling the effect.

fade_in_fraction – Fractional duration of initial fade-in of sub-Mobjects as they fly inward.

Examples

Example: SpiralInExample ¶

from manim import *

class SpiralInExample(Scene):
def construct(self):
pi = MathTex(r"\pi").scale(7)
pi.shift(2.25 * LEFT + 1.5 * UP)
circle = Circle(color=GREEN_C, fill_opacity=1).shift(LEFT)
square = Square(color=BLUE_D, fill_opacity=1).shift(UP)
shapes = VGroup(pi, circle, square)
self.play(SpiralIn(shapes))

class SpiralInExample(Scene):
def construct(self):
pi = MathTex(r"\pi").scale(7)
pi.shift(2.25 * LEFT + 1.5 * UP)
circle = Circle(color=GREEN_C, fill_opacity=1).shift(LEFT)
square = Square(color=BLUE_D, fill_opacity=1).shift(UP)
shapes = VGroup(pi, circle, square)
self.play(SpiralIn(shapes))

Methods

interpolate_mobject

Interpolates the mobject of the Animation based on alpha value.

Attributes

run_time

_original__init__(shapes, scale_factor=8, fade_in_fraction=0.3, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

shapes (Mobject)

scale_factor (float)

Return type:
None

interpolate_mobject(alpha)[source]¶
Interpolates the mobject of the Animation based on alpha value.

Parameters:
alpha (float) – A float between 0 and 1 expressing the ratio to which the animation
is completed. For example, alpha-values of 0, 0.5, and 1 correspond
to the animation being completed 0%, 50%, and 100%, respectively.

Return type:
None


---

## TypeWithCursor - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.TypeWithCursor.html

TypeWithCursor¶

Qualified name: manim.animation.creation.TypeWithCursor

class TypeWithCursor(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: AddTextLetterByLetter

Similar to AddTextLetterByLetter , but with an additional cursor mobject at the end.

Parameters:

time_per_char (float) – Frequency of appearance of the letters.

cursor (Mobject) – Mobject shown after the last added letter.

buff (float) – Controls how far away the cursor is to the right of the last added letter.

keep_cursor_y (bool) – If True, the cursor’s y-coordinate is set to the center of the Text and remains the same throughout the animation. Otherwise, it is set to the center of the last added letter.

leave_cursor_on (bool) – Whether to show the cursor after the animation.

tip:: (..) – This is currently only possible for class:~.Text and not for class:~.MathTex.

text (Text)

Examples

Example: InsertingTextExample ¶

from manim import *

class InsertingTextExample(Scene):
def construct(self):
text = Text("Inserting", color=PURPLE).scale(1.5).to_edge(LEFT)
cursor = Rectangle(
color = GREY_A,
fill_color = GREY_A,
fill_opacity = 1.0,
height = 1.1,
width = 0.5,
).move_to(text[0]) # Position the cursor

self.play(TypeWithCursor(text, cursor))
self.play(Blink(cursor, blinks=2))

class InsertingTextExample(Scene):
def construct(self):
text = Text("Inserting", color=PURPLE).scale(1.5).to_edge(LEFT)
cursor = Rectangle(
color = GREY_A,
fill_color = GREY_A,
fill_opacity = 1.0,
height = 1.1,
width = 0.5,
).move_to(text[0]) # Position the cursor

self.play(TypeWithCursor(text, cursor))
self.play(Blink(cursor, blinks=2))

References: Blink

Methods

begin

Begin the animation.

clean_up_from_scene

Clean up the Scene after finishing the animation.

finish

Finish the animation.

update_submobject_list

Attributes

run_time

_original__init__(text, cursor, buff=0.1, keep_cursor_y=True, leave_cursor_on=True, time_per_char=0.1, reverse_rate_function=False, introducer=True, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

text (Text)

cursor (Mobject)

buff (float)

keep_cursor_y (bool)

leave_cursor_on (bool)

time_per_char (float)

Return type:
None

begin()[source]¶
Begin the animation.

This method is called right as an animation is being played. As much
initialization as possible, especially any mobject copying, should live in this
method.

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

finish()[source]¶
Finish the animation.

This method gets called when the animation is over.

Return type:
None


---

## Uncreate - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.Uncreate.html

Uncreate¶

Qualified name: manim.animation.creation.Uncreate

class Uncreate(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Create

Like Create but in reverse.

Examples

Example: ShowUncreate ¶

from manim import *

class ShowUncreate(Scene):
def construct(self):
self.play(Uncreate(Square()))

class ShowUncreate(Scene):
def construct(self):
self.play(Uncreate(Square()))

See also

Create

Methods

Attributes

run_time

Parameters:

mobject (VMobject | OpenGLVMobject)

reverse_rate_function (bool)

remover (bool)

_original__init__(mobject, reverse_rate_function=True, remover=True, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (VMobject | OpenGLVMobject)

reverse_rate_function (bool)

remover (bool)

Return type:
None


---

## UntypeWithCursor - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.UntypeWithCursor.html

UntypeWithCursor¶

Qualified name: manim.animation.creation.UntypeWithCursor

class UntypeWithCursor(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: TypeWithCursor

Similar to RemoveTextLetterByLetter , but with an additional cursor mobject at the end.

Parameters:

time_per_char (float) – Frequency of appearance of the letters.

cursor (VMobject | None) – Mobject shown after the last added letter.

buff – Controls how far away the cursor is to the right of the last added letter.

keep_cursor_y – If True, the cursor’s y-coordinate is set to the center of the Text and remains the same throughout the animation. Otherwise, it is set to the center of the last added letter.

leave_cursor_on – Whether to show the cursor after the animation.

tip:: (..) – This is currently only possible for class:~.Text and not for class:~.MathTex.

text (Text)

Examples

Example: DeletingTextExample ¶

from manim import *

class DeletingTextExample(Scene):
def construct(self):
text = Text("Deleting", color=PURPLE).scale(1.5).to_edge(LEFT)
cursor = Rectangle(
color = GREY_A,
fill_color = GREY_A,
fill_opacity = 1.0,
height = 1.1,
width = 0.5,
).move_to(text[0]) # Position the cursor

self.play(UntypeWithCursor(text, cursor))
self.play(Blink(cursor, blinks=2))

class DeletingTextExample(Scene):
def construct(self):
text = Text("Deleting", color=PURPLE).scale(1.5).to_edge(LEFT)
cursor = Rectangle(
color = GREY_A,
fill_color = GREY_A,
fill_opacity = 1.0,
height = 1.1,
width = 0.5,
).move_to(text[0]) # Position the cursor

self.play(UntypeWithCursor(text, cursor))
self.play(Blink(cursor, blinks=2))

References: Blink

Methods

Attributes

run_time

_original__init__(text, cursor=None, time_per_char=0.1, reverse_rate_function=True, introducer=False, remover=True, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

text (Text)

cursor (VMobject | None)

time_per_char (float)

Return type:
None


---

## Unwrite - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.Unwrite.html

Unwrite¶

Qualified name: manim.animation.creation.Unwrite

class Unwrite(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Write

Simulate erasing by hand a Text or a VMobject.

Parameters:

reverse (bool) – Set True to have the animation start erasing from the last submobject first.

vmobject (VMobject)

rate_func (Callable[[float], float])

Examples

Example: UnwriteReverseTrue ¶

from manim import *

class UnwriteReverseTrue(Scene):
def construct(self):
text = Tex("Alice and Bob").scale(3)
self.add(text)
self.play(Unwrite(text))

class UnwriteReverseTrue(Scene):
def construct(self):
text = Tex("Alice and Bob").scale(3)
self.add(text)
self.play(Unwrite(text))

Example: UnwriteReverseFalse ¶

from manim import *

class UnwriteReverseFalse(Scene):
def construct(self):
text = Tex("Alice and Bob").scale(3)
self.add(text)
self.play(Unwrite(text, reverse=False))

class UnwriteReverseFalse(Scene):
def construct(self):
text = Tex("Alice and Bob").scale(3)
self.add(text)
self.play(Unwrite(text, reverse=False))

Methods

Attributes

run_time

_original__init__(vmobject, rate_func=<function linear>, reverse=True, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

vmobject (VMobject)

rate_func (Callable[[float], float])

reverse (bool)

Return type:
None


---

## Write - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.Write.html

Write¶

Qualified name: manim.animation.creation.Write

class Write(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: DrawBorderThenFill

Simulate hand-writing a Text or hand-drawing a VMobject.

Examples

Example: ShowWrite ¶

from manim import *

class ShowWrite(Scene):
def construct(self):
self.play(Write(Text("Hello", font_size=144)))

class ShowWrite(Scene):
def construct(self):
self.play(Write(Text("Hello", font_size=144)))

Example: ShowWriteReversed ¶

from manim import *

class ShowWriteReversed(Scene):
def construct(self):
self.play(Write(Text("Hello", font_size=144), reverse=True, remover=False))

class ShowWriteReversed(Scene):
def construct(self):
self.play(Write(Text("Hello", font_size=144), reverse=True, remover=False))

Tests

Check that creating empty Write animations works:

>>> from manim import Write, Text
>>> Write(Text(''))
Write(Text(''))

Methods

begin

Begin the animation.

finish

Finish the animation.

reverse_submobjects

Attributes

run_time

Parameters:

vmobject (VMobject | OpenGLVMobject)

rate_func (Callable[[float], float])

reverse (bool)

_original__init__(vmobject, rate_func=<function linear>, reverse=False, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

vmobject (VMobject | OpenGLVMobject)

rate_func (Callable[[float], float])

reverse (bool)

Return type:
None

begin()[source]¶
Begin the animation.

This method is called right as an animation is being played. As much
initialization as possible, especially any mobject copying, should live in this
method.

Return type:
None

finish()[source]¶
Finish the animation.

This method gets called when the animation is over.

Return type:
None
