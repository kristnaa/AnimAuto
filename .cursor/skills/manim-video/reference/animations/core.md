# Core


---

## animation - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.animation.html

animation¶

Animate mobjects.

Classes

Add

Add Mobjects to a scene, without animating them in any other way.

Animation

An animation.

Wait

A "no operation" animation.

Functions

override_animation(animation_class)[source]¶
Decorator used to mark methods as overrides for specific Animation types.

Should only be used to decorate methods of classes derived from Mobject.
Animation overrides get inherited to subclasses of the Mobject who defined
them. They don’t override subclasses of the Animation they override.

See also

add_animation_override()

Parameters:
animation_class (type[Animation]) – The animation to be overridden.

Returns:
The actual decorator. This marks the method as overriding an animation.

Return type:
Callable[[Callable], Callable]

Examples

Example: OverrideAnimationExample ¶

from manim import *

class MySquare(Square):
@override_animation(FadeIn)
def _fade_in_override(self, **kwargs):
return Create(self, **kwargs)

class OverrideAnimationExample(Scene):
def construct(self):
self.play(FadeIn(MySquare()))

class MySquare(Square):
@override_animation(FadeIn)
def _fade_in_override(self, **kwargs):
return Create(self, **kwargs)

class OverrideAnimationExample(Scene):
def construct(self):
self.play(FadeIn(MySquare()))

prepare_animation(anim)[source]¶
Returns either an unchanged animation, or the animation built
from a passed animation factory.

Examples

>>> from manim import Square, FadeIn
>>> s = Square()
>>> prepare_animation(FadeIn(s))
FadeIn(Square)

>>> prepare_animation(s.animate.scale(2).rotate(42))
_MethodAnimation(Square)

>>> prepare_animation(42)
Traceback (most recent call last):
...
TypeError: Object 42 cannot be converted to an animation

Parameters:
anim (Animation | _AnimationBuilder | _AnimationBuilder)

Return type:
Animation


---

## changing - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.changing.html

changing¶

Animation of a mobject boundary and tracing of points.

Classes

AnimatedBoundary

Boundary of a VMobject with animated color change.

TracedPath

Traces the path of a point returned by a function call.


---

## composition - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.composition.html

composition¶

Tools for displaying multiple animations at once.

Classes

AnimationGroup

Plays a group or series of Animation.

LaggedStart

Adjusts the timing of a series of Animation according to lag_ratio.

LaggedStartMap

Plays a series of Animation while mapping a function to submobjects.

Succession

Plays a series of animations in succession.


---

## creation - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.creation.html

creation¶

Animate the display or removal of a mobject from a scene.

Classes

AddTextLetterByLetter

Show a Text letter by letter on the scene.

AddTextWordByWord

Show a Text word by word on the scene.

Create

Incrementally show a VMobject.

DrawBorderThenFill

Draw the border first and then show the fill.

RemoveTextLetterByLetter

Remove a Text letter by letter from the scene.

ShowIncreasingSubsets

Show one submobject at a time, leaving all previous ones displayed on screen.

ShowPartial

Abstract class for Animations that show the VMobject partially.

ShowSubmobjectsOneByOne

Show one submobject at a time, removing all previously displayed ones from screen.

SpiralIn

Create the Mobject with sub-Mobjects flying in on spiral trajectories.

TypeWithCursor

Similar to AddTextLetterByLetter , but with an additional cursor mobject at the end.

Uncreate

Like Create but in reverse.

UntypeWithCursor

Similar to RemoveTextLetterByLetter , but with an additional cursor mobject at the end.

Unwrite

Simulate erasing by hand a Text or a VMobject.

Write

Simulate hand-writing a Text or hand-drawing a VMobject.


---

## fading - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.fading.html

fading¶

Fading in and out of view.

Example: Fading ¶

from manim import *

class Fading(Scene):
def construct(self):
tex_in = Tex("Fade", "In").scale(3)
tex_out = Tex("Fade", "Out").scale(3)
self.play(FadeIn(tex_in, shift=DOWN, scale=0.66))
self.play(ReplacementTransform(tex_in, tex_out))
self.play(FadeOut(tex_out, shift=DOWN * 2, scale=1.5))

class Fading(Scene):
def construct(self):
tex_in = Tex("Fade", "In").scale(3)
tex_out = Tex("Fade", "Out").scale(3)
self.play(FadeIn(tex_in, shift=DOWN, scale=0.66))
self.play(ReplacementTransform(tex_in, tex_out))
self.play(FadeOut(tex_out, shift=DOWN * 2, scale=1.5))

Classes

FadeIn

Fade in Mobject s.

FadeOut

Fade out Mobject s.


---

## growing - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.growing.html

growing¶

Animations that introduce mobjects to scene by growing them from points.

Example: Growing ¶

from manim import *

class Growing(Scene):
def construct(self):
square = Square()
circle = Circle()
triangle = Triangle()
arrow = Arrow(LEFT, RIGHT)
star = Star()

VGroup(square, circle, triangle).set_x(0).arrange(buff=1.5).set_y(2)
VGroup(arrow, star).move_to(DOWN).set_x(0).arrange(buff=1.5).set_y(-2)

self.play(GrowFromPoint(square, ORIGIN))
self.play(GrowFromCenter(circle))
self.play(GrowFromEdge(triangle, DOWN))
self.play(GrowArrow(arrow))
self.play(SpinInFromNothing(star))

class Growing(Scene):
def construct(self):
square = Square()
circle = Circle()
triangle = Triangle()
arrow = Arrow(LEFT, RIGHT)
star = Star()

VGroup(square, circle, triangle).set_x(0).arrange(buff=1.5).set_y(2)
VGroup(arrow, star).move_to(DOWN).set_x(0).arrange(buff=1.5).set_y(-2)

self.play(GrowFromPoint(square, ORIGIN))
self.play(GrowFromCenter(circle))
self.play(GrowFromEdge(triangle, DOWN))
self.play(GrowArrow(arrow))
self.play(SpinInFromNothing(star))

Classes

GrowArrow

Introduce an Arrow by growing it from its start toward its tip.

GrowFromCenter

Introduce an Mobject by growing it from its center.

GrowFromEdge

Introduce an Mobject by growing it from one of its bounding box edges.

GrowFromPoint

Introduce an Mobject by growing it from a point.

SpinInFromNothing

Introduce an Mobject spinning and growing it from its center.


---

## indication - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.indication.html

indication¶

Animations drawing attention to particular mobjects.

Examples

Example: Indications ¶

from manim import *

class Indications(Scene):
def construct(self):
indications = [ApplyWave,Circumscribe,Flash,FocusOn,Indicate,ShowPassingFlash,Wiggle]
names = [Tex(i.__name__).scale(3) for i in indications]

self.add(names[0])
for i in range(len(names)):
if indications[i] is Flash:
self.play(Flash(UP))
elif indications[i] is ShowPassingFlash:
self.play(ShowPassingFlash(Underline(names[i])))
else:
self.play(indications[i](names[i]))
self.play(AnimationGroup(
FadeOut(names[i], shift=UP*1.5),
FadeIn(names[(i+1)%len(names)], shift=UP*1.5),
))

class Indications(Scene):
def construct(self):
indications = [ApplyWave,Circumscribe,Flash,FocusOn,Indicate,ShowPassingFlash,Wiggle]
names = [Tex(i.__name__).scale(3) for i in indications]

self.add(names[0])
for i in range(len(names)):
if indications[i] is Flash:
self.play(Flash(UP))
elif indications[i] is ShowPassingFlash:
self.play(ShowPassingFlash(Underline(names[i])))
else:
self.play(indications[i](names[i]))
self.play(AnimationGroup(
FadeOut(names[i], shift=UP*1.5),
FadeIn(names[(i+1)%len(names)], shift=UP*1.5),
))

Classes

ApplyWave

Send a wave through the Mobject distorting it temporarily.

Blink

Blink the mobject.

Circumscribe

Draw a temporary line surrounding the mobject.

Flash

Send out lines in all directions.

FocusOn

Shrink a spotlight to a position.

Indicate

Indicate a Mobject by temporarily resizing and recoloring it.

ShowPassingFlash

Show only a sliver of the VMobject each frame.

ShowPassingFlashWithThinningStrokeWidth

Wiggle

Wiggle a Mobject.


---

## movement - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.movement.html

movement¶

Animations related to movement.

Classes

ComplexHomotopy

Complex Homotopy a function Cx[0, 1] to C

Homotopy

A Homotopy.

MoveAlongPath

Make one mobject move along the path of another mobject.

PhaseFlow

SmoothedVectorizedHomotopy


---

## numbers - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.numbers.html

numbers¶

Animations for changing numbers.

Classes

ChangeDecimalToValue

Animate a DecimalNumber to a target value using linear interpolation.

ChangingDecimal

Animate a DecimalNumber to values specified by a user-supplied function.


---

## rotation - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.rotation.html

rotation¶

Animations related to rotation.

Classes

Rotate

Animation that rotates a Mobject.

Rotating

Animation that rotates a Mobject.


---

## specialized - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.specialized.html

specialized¶

Classes

Broadcast

Broadcast a mobject starting from an initial_width, up to the actual size of the mobject.


---

## speedmodifier - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.speedmodifier.html

speedmodifier¶

Utilities for modifying the speed at which animations are played.

Classes

ChangeSpeed

Modifies the speed of passed animation.


---

## transform - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.html

transform¶

Animations transforming one mobject into another.

Classes

ApplyComplexFunction

ApplyFunction

ApplyMatrix

Applies a matrix transform to an mobject.

ApplyMethod

Animates a mobject by applying a method.

ApplyPointwiseFunction

Animation that applies a pointwise function to a mobject.

ApplyPointwiseFunctionToCenter

ClockwiseTransform

Transforms the points of a mobject along a clockwise oriented arc.

CounterclockwiseTransform

Transforms the points of a mobject along a counterclockwise oriented arc.

CyclicReplace

An animation moving mobjects cyclically.

FadeToColor

Animation that changes color of a mobject.

FadeTransform

Fades one mobject into another.

FadeTransformPieces

Fades submobjects of one mobject into submobjects of another one.

MoveToTarget

Transforms a mobject to the mobject stored in its target attribute.

ReplacementTransform

Replaces and morphs a mobject into a target mobject.

Restore

Transforms a mobject to its last saved state.

ScaleInPlace

Animation that scales a mobject by a certain factor.

ShrinkToCenter

Animation that makes a mobject shrink to center.

Swap

Transform

A Transform transforms a Mobject into a target Mobject.

TransformAnimations

TransformFromCopy

Preserves a copy of the original VMobject and transforms only it's copy to the target VMobject


---

## transform_matching_parts - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform_matching_parts.html

transform_matching_parts¶

Animations that try to transform Mobjects while keeping track of identical parts.

Classes

TransformMatchingAbstractBase

Abstract base class for transformations that keep track of matching parts.

TransformMatchingShapes

An animation trying to transform groups by matching the shape of their submobjects.

TransformMatchingTex

A transformation trying to transform rendered LaTeX strings.


---

## updaters - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.updaters.html

updaters¶

Animations and utility mobjects related to update functions.

Modules¶

mobject_update_utils

Utility functions for continuous animation of mobjects.

update

Animations that update mobjects.
