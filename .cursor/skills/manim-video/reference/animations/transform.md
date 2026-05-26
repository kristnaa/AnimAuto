# Transform


---

## ApplyComplexFunction - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.ApplyComplexFunction.html

ApplyComplexFunction¶

Qualified name: manim.animation.transform.ApplyComplexFunction

class ApplyComplexFunction(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: ApplyMethod

Methods

Attributes

path_arc

path_func

run_time

Parameters:

function (types.MethodType)

mobject (Mobject)

_original__init__(function, mobject, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

function (MethodType)

mobject (Mobject)

Return type:
None


---

## ApplyFunction - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.ApplyFunction.html

ApplyFunction¶

Qualified name: manim.animation.transform.ApplyFunction

class ApplyFunction(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Transform

Methods

create_target

Attributes

path_arc

path_func

run_time

Parameters:

function (types.MethodType)

mobject (Mobject)

_original__init__(function, mobject, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

function (MethodType)

mobject (Mobject)

Return type:
None


---

## ApplyMatrix - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.ApplyMatrix.html

ApplyMatrix¶

Qualified name: manim.animation.transform.ApplyMatrix

class ApplyMatrix(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: ApplyPointwiseFunction

Applies a matrix transform to an mobject.

Parameters:

matrix (np.ndarray) – The transformation matrix.

mobject (Mobject) – The Mobject.

about_point (np.ndarray) – The origin point for the transform. Defaults to ORIGIN.

kwargs – Further keyword arguments that are passed to ApplyPointwiseFunction.

Examples

Example: ApplyMatrixExample ¶

from manim import *

class ApplyMatrixExample(Scene):
def construct(self):
matrix = [[1, 1], [0, 2/3]]
self.play(ApplyMatrix(matrix, Text("Hello World!")), ApplyMatrix(matrix, NumberPlane()))

class ApplyMatrixExample(Scene):
def construct(self):
matrix = [[1, 1], [0, 2/3]]
self.play(ApplyMatrix(matrix, Text("Hello World!")), ApplyMatrix(matrix, NumberPlane()))

Methods

initialize_matrix

Attributes

path_arc

path_func

run_time

_original__init__(matrix, mobject, about_point=array([0., 0., 0.]), **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

matrix (ndarray)

mobject (Mobject)

about_point (ndarray)

Return type:
None


---

## ApplyMethod - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.ApplyMethod.html

ApplyMethod¶

Qualified name: manim.animation.transform.ApplyMethod

class ApplyMethod(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Transform

Animates a mobject by applying a method.

Note that only the method needs to be passed to this animation,
it is not required to pass the corresponding mobject. Furthermore,
this animation class only works if the method returns the modified
mobject.

Parameters:

method (Callable) – The method that will be applied in the animation.

args – Any positional arguments to be passed when applying the method.

kwargs – Any keyword arguments passed to Transform.

Methods

check_validity_of_input

create_target

Attributes

path_arc

path_func

run_time

_original__init__(method, *args, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:
method (Callable)

Return type:
None


---

## ApplyPointwiseFunction - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.ApplyPointwiseFunction.html

ApplyPointwiseFunction¶

Qualified name: manim.animation.transform.ApplyPointwiseFunction

class ApplyPointwiseFunction(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: ApplyMethod

Animation that applies a pointwise function to a mobject.

Examples

Example: WarpSquare ¶

from manim import *

class WarpSquare(Scene):
def construct(self):
square = Square()
self.play(
ApplyPointwiseFunction(
lambda point: complex_to_R3(np.exp(R3_to_complex(point))), square
)
)
self.wait()

class WarpSquare(Scene):
def construct(self):
square = Square()
self.play(
ApplyPointwiseFunction(
lambda point: complex_to_R3(np.exp(R3_to_complex(point))), square
)
)
self.wait()

Methods

Attributes

path_arc

path_func

run_time

Parameters:

function (types.MethodType)

mobject (Mobject)

run_time (float)

_original__init__(function, mobject, run_time=3.0, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

function (MethodType)

mobject (Mobject)

run_time (float)

Return type:
None


---

## ApplyPointwiseFunctionToCenter - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.ApplyPointwiseFunctionToCenter.html

ApplyPointwiseFunctionToCenter¶

Qualified name: manim.animation.transform.ApplyPointwiseFunctionToCenter

class ApplyPointwiseFunctionToCenter(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: ApplyPointwiseFunction

Methods

begin

Begin the animation.

Attributes

path_arc

path_func

run_time

Parameters:

function (types.MethodType)

mobject (Mobject)

_original__init__(function, mobject, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

function (MethodType)

mobject (Mobject)

Return type:
None

begin()[source]¶
Begin the animation.

This method is called right as an animation is being played. As much
initialization as possible, especially any mobject copying, should live in this
method.

Return type:
None


---

## ClockwiseTransform - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.ClockwiseTransform.html

ClockwiseTransform¶

Qualified name: manim.animation.transform.ClockwiseTransform

class ClockwiseTransform(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Transform

Transforms the points of a mobject along a clockwise oriented arc.

See also

Transform, CounterclockwiseTransform

Examples

Example: ClockwiseExample ¶

from manim import *

class ClockwiseExample(Scene):
def construct(self):
dl, dr = Dot(), Dot()
sl, sr = Square(), Square()

VGroup(dl, sl).arrange(DOWN).shift(2*LEFT)
VGroup(dr, sr).arrange(DOWN).shift(2*RIGHT)

self.add(dl, dr)
self.wait()
self.play(
ClockwiseTransform(dl, sl),
Transform(dr, sr)
)
self.wait()

class ClockwiseExample(Scene):
def construct(self):
dl, dr = Dot(), Dot()
sl, sr = Square(), Square()

VGroup(dl, sl).arrange(DOWN).shift(2*LEFT)
VGroup(dr, sr).arrange(DOWN).shift(2*RIGHT)

self.add(dl, dr)
self.wait()
self.play(
ClockwiseTransform(dl, sl),
Transform(dr, sr)
)
self.wait()

Methods

Attributes

path_arc

path_func

run_time

Parameters:

mobject (Mobject)

target_mobject (Mobject)

path_arc (float)

_original__init__(mobject, target_mobject, path_arc=-3.141592653589793, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

target_mobject (Mobject)

path_arc (float)

Return type:
None


---

## CounterclockwiseTransform - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.CounterclockwiseTransform.html

CounterclockwiseTransform¶

Qualified name: manim.animation.transform.CounterclockwiseTransform

class CounterclockwiseTransform(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Transform

Transforms the points of a mobject along a counterclockwise oriented arc.

See also

Transform, ClockwiseTransform

Examples

Example: CounterclockwiseTransform_vs_Transform ¶

from manim import *

class CounterclockwiseTransform_vs_Transform(Scene):
def construct(self):
# set up the numbers
c_transform = VGroup(DecimalNumber(number=3.141, num_decimal_places=3), DecimalNumber(number=1.618, num_decimal_places=3))
text_1 = Text("CounterclockwiseTransform", color=RED)
c_transform.add(text_1)

transform = VGroup(DecimalNumber(number=1.618, num_decimal_places=3), DecimalNumber(number=3.141, num_decimal_places=3))
text_2 = Text("Transform", color=BLUE)
transform.add(text_2)

ints = VGroup(c_transform, transform)
texts = VGroup(text_1, text_2).scale(0.75)
c_transform.arrange(direction=UP, buff=1)
transform.arrange(direction=UP, buff=1)

ints.arrange(buff=2)
self.add(ints, texts)

# The mobs move in clockwise direction for ClockwiseTransform()
self.play(CounterclockwiseTransform(c_transform[0], c_transform[1]))

# The mobs move straight up for Transform()
self.play(Transform(transform[0], transform[1]))

class CounterclockwiseTransform_vs_Transform(Scene):
def construct(self):
# set up the numbers
c_transform = VGroup(DecimalNumber(number=3.141, num_decimal_places=3), DecimalNumber(number=1.618, num_decimal_places=3))
text_1 = Text("CounterclockwiseTransform", color=RED)
c_transform.add(text_1)

transform = VGroup(DecimalNumber(number=1.618, num_decimal_places=3), DecimalNumber(number=3.141, num_decimal_places=3))
text_2 = Text("Transform", color=BLUE)
transform.add(text_2)

ints = VGroup(c_transform, transform)
texts = VGroup(text_1, text_2).scale(0.75)
c_transform.arrange(direction=UP, buff=1)
transform.arrange(direction=UP, buff=1)

ints.arrange(buff=2)
self.add(ints, texts)

# The mobs move in clockwise direction for ClockwiseTransform()
self.play(CounterclockwiseTransform(c_transform[0], c_transform[1]))

# The mobs move straight up for Transform()
self.play(Transform(transform[0], transform[1]))

Methods

Attributes

path_arc

path_func

run_time

Parameters:

mobject (Mobject)

target_mobject (Mobject)

path_arc (float)

_original__init__(mobject, target_mobject, path_arc=3.141592653589793, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

target_mobject (Mobject)

path_arc (float)

Return type:
None


---

## CyclicReplace - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.CyclicReplace.html

CyclicReplace¶

Qualified name: manim.animation.transform.CyclicReplace

class CyclicReplace(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Transform

An animation moving mobjects cyclically.

In particular, this means: the first mobject takes the place
of the second mobject, the second one takes the place of
the third mobject, and so on. The last mobject takes the
place of the first one.

Parameters:

mobjects (Mobject) – List of mobjects to be transformed.

path_arc (float) – The angle of the arc (in radians) that the mobjects will follow to reach
their target.

kwargs – Further keyword arguments that are passed to Transform.

Examples

Example: CyclicReplaceExample ¶

from manim import *

class CyclicReplaceExample(Scene):
def construct(self):
group = VGroup(Square(), Circle(), Triangle(), Star())
group.arrange(RIGHT)
self.add(group)

for _ in range(4):
self.play(CyclicReplace(*group))

class CyclicReplaceExample(Scene):
def construct(self):
group = VGroup(Square(), Circle(), Triangle(), Star())
group.arrange(RIGHT)
self.add(group)

for _ in range(4):
self.play(CyclicReplace(*group))

Methods

create_target

Attributes

path_arc

path_func

run_time

_original__init__(*mobjects, path_arc=1.5707963267948966, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobjects (Mobject)

path_arc (float)

Return type:
None


---

## FadeToColor - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.FadeToColor.html

FadeToColor¶

Qualified name: manim.animation.transform.FadeToColor

class FadeToColor(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: ApplyMethod

Animation that changes color of a mobject.

Examples

Example: FadeToColorExample ¶

from manim import *

class FadeToColorExample(Scene):
def construct(self):
self.play(FadeToColor(Text("Hello World!"), color=RED))

class FadeToColorExample(Scene):
def construct(self):
self.play(FadeToColor(Text("Hello World!"), color=RED))

Methods

Attributes

path_arc

path_func

run_time

Parameters:

mobject (Mobject)

color (str)

_original__init__(mobject, color, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

color (str)

Return type:
None


---

## FadeTransform - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.FadeTransform.html

FadeTransform¶

Qualified name: manim.animation.transform.FadeTransform

class FadeTransform(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Transform

Fades one mobject into another.

Parameters:

mobject – The starting Mobject.

target_mobject – The target Mobject.

stretch – Controls whether the target Mobject is stretched during
the animation. Default: True.

dim_to_match – If the target mobject is not stretched automatically, this allows
to adjust the initial scale of the target Mobject while
it is shifted in. Setting this to 0, 1, and 2, respectively,
matches the length of the target with the length of the starting
Mobject in x, y, and z direction, respectively.

kwargs – Further keyword arguments are passed to the parent class.

Examples

Example: DifferentFadeTransforms ¶

from manim import *

class DifferentFadeTransforms(Scene):
def construct(self):
starts = [Rectangle(width=4, height=1) for _ in range(3)]
VGroup(*starts).arrange(DOWN, buff=1).shift(3*LEFT)
targets = [Circle(fill_opacity=1).scale(0.25) for _ in range(3)]
VGroup(*targets).arrange(DOWN, buff=1).shift(3*RIGHT)

self.play(*[FadeIn(s) for s in starts])
self.play(
FadeTransform(starts[0], targets[0], stretch=True),
FadeTransform(starts[1], targets[1], stretch=False, dim_to_match=0),
FadeTransform(starts[2], targets[2], stretch=False, dim_to_match=1)
)

self.play(*[FadeOut(mobj) for mobj in self.mobjects])

class DifferentFadeTransforms(Scene):
def construct(self):
starts = [Rectangle(width=4, height=1) for _ in range(3)]
VGroup(*starts).arrange(DOWN, buff=1).shift(3*LEFT)
targets = [Circle(fill_opacity=1).scale(0.25) for _ in range(3)]
VGroup(*targets).arrange(DOWN, buff=1).shift(3*RIGHT)

self.play(*[FadeIn(s) for s in starts])
self.play(
FadeTransform(starts[0], targets[0], stretch=True),
FadeTransform(starts[1], targets[1], stretch=False, dim_to_match=0),
FadeTransform(starts[2], targets[2], stretch=False, dim_to_match=1)
)

self.play(*[FadeOut(mobj) for mobj in self.mobjects])

Methods

begin

Initial setup for the animation.

clean_up_from_scene

Clean up the Scene after finishing the animation.

get_all_families_zipped

get_all_mobjects

Get all mobjects involved in the animation.

ghost_to

Replaces the source by the target and sets the opacity to 0.

Attributes

path_arc

path_func

run_time

_original__init__(mobject, target_mobject, stretch=True, dim_to_match=1, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

begin()[source]¶
Initial setup for the animation.

The mobject to which this animation is bound is a group consisting of
both the starting and the ending mobject. At the start, the ending
mobject replaces the starting mobject (and is completely faded). In the
end, it is set to be the other way around.

clean_up_from_scene(scene)[source]¶
Clean up the Scene after finishing the animation.

This includes to remove() the Animation’s
Mobject if the animation is a remover.

Parameters:
scene – The scene the animation should be cleaned up from.

get_all_mobjects()[source]¶
Get all mobjects involved in the animation.

Ordering must match the ordering of arguments to interpolate_submobject

Returns:
The sequence of mobjects.

Return type:
Sequence[Mobject]

ghost_to(source, target)[source]¶
Replaces the source by the target and sets the opacity to 0.

If the provided target has no points, and thus a location of [0, 0, 0]
the source will simply fade out where it currently is.


---

## FadeTransformPieces - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.FadeTransformPieces.html

FadeTransformPieces¶

Qualified name: manim.animation.transform.FadeTransformPieces

class FadeTransformPieces(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: FadeTransform

Fades submobjects of one mobject into submobjects of another one.

See also

FadeTransform

Examples

Example: FadeTransformSubmobjects ¶

from manim import *

class FadeTransformSubmobjects(Scene):
def construct(self):
src = VGroup(Square(), Circle().shift(LEFT + UP))
src.shift(3*LEFT + 2*UP)
src_copy = src.copy().shift(4*DOWN)

target = VGroup(Circle(), Triangle().shift(RIGHT + DOWN))
target.shift(3*RIGHT + 2*UP)
target_copy = target.copy().shift(4*DOWN)

self.play(FadeIn(src), FadeIn(src_copy))
self.play(
FadeTransform(src, target),
FadeTransformPieces(src_copy, target_copy)
)
self.play(*[FadeOut(mobj) for mobj in self.mobjects])

class FadeTransformSubmobjects(Scene):
def construct(self):
src = VGroup(Square(), Circle().shift(LEFT + UP))
src.shift(3*LEFT + 2*UP)
src_copy = src.copy().shift(4*DOWN)

target = VGroup(Circle(), Triangle().shift(RIGHT + DOWN))
target.shift(3*RIGHT + 2*UP)
target_copy = target.copy().shift(4*DOWN)

self.play(FadeIn(src), FadeIn(src_copy))
self.play(
FadeTransform(src, target),
FadeTransformPieces(src_copy, target_copy)
)
self.play(*[FadeOut(mobj) for mobj in self.mobjects])

Methods

begin

Initial setup for the animation.

ghost_to

Replaces the source submobjects by the target submobjects and sets the opacity to 0.

Attributes

path_arc

path_func

run_time

_original__init__(mobject, target_mobject, stretch=True, dim_to_match=1, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

begin()[source]¶
Initial setup for the animation.

The mobject to which this animation is bound is a group consisting of
both the starting and the ending mobject. At the start, the ending
mobject replaces the starting mobject (and is completely faded). In the
end, it is set to be the other way around.

ghost_to(source, target)[source]¶
Replaces the source submobjects by the target submobjects and sets
the opacity to 0.


---

## MoveToTarget - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.MoveToTarget.html

MoveToTarget¶

Qualified name: manim.animation.transform.MoveToTarget

class MoveToTarget(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Transform

Transforms a mobject to the mobject stored in its target attribute.

After calling the generate_target() method, the target
attribute of the mobject is populated with a copy of it. After modifying the attribute,
playing the MoveToTarget animation transforms the original mobject
into the modified one stored in the target attribute.

Examples

Example: MoveToTargetExample ¶

from manim import *

class MoveToTargetExample(Scene):
def construct(self):
c = Circle()

c.generate_target()
c.target.set_fill(color=GREEN, opacity=0.5)
c.target.shift(2*RIGHT + UP).scale(0.5)

self.add(c)
self.play(MoveToTarget(c))

class MoveToTargetExample(Scene):
def construct(self):
c = Circle()

c.generate_target()
c.target.set_fill(color=GREEN, opacity=0.5)
c.target.shift(2*RIGHT + UP).scale(0.5)

self.add(c)
self.play(MoveToTarget(c))

Methods

check_validity_of_input

Attributes

path_arc

path_func

run_time

Parameters:
mobject (Mobject)

_original__init__(mobject, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:
mobject (Mobject)

Return type:
None


---

## ReplacementTransform - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.ReplacementTransform.html

ReplacementTransform¶

Qualified name: manim.animation.transform.ReplacementTransform

class ReplacementTransform(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Transform

Replaces and morphs a mobject into a target mobject.

Parameters:

mobject (Mobject) – The starting Mobject.

target_mobject (Mobject) – The target Mobject.

kwargs – Further keyword arguments that are passed to Transform.

Examples

Example: ReplacementTransformOrTransform ¶

from manim import *

class ReplacementTransformOrTransform(Scene):
def construct(self):
# set up the numbers
r_transform = VGroup(*[Integer(i) for i in range(1,4)])
text_1 = Text("ReplacementTransform", color=RED)
r_transform.add(text_1)

transform = VGroup(*[Integer(i) for i in range(4,7)])
text_2 = Text("Transform", color=BLUE)
transform.add(text_2)

ints = VGroup(r_transform, transform)
texts = VGroup(text_1, text_2).scale(0.75)
r_transform.arrange(direction=UP, buff=1)
transform.arrange(direction=UP, buff=1)

ints.arrange(buff=2)
self.add(ints, texts)

# The mobs replace each other and none are left behind
self.play(ReplacementTransform(r_transform[0], r_transform[1]))
self.play(ReplacementTransform(r_transform[1], r_transform[2]))

# The mobs linger after the Transform()
self.play(Transform(transform[0], transform[1]))
self.play(Transform(transform[1], transform[2]))
self.wait()

class ReplacementTransformOrTransform(Scene):
def construct(self):
# set up the numbers
r_transform = VGroup(*[Integer(i) for i in range(1,4)])
text_1 = Text("ReplacementTransform", color=RED)
r_transform.add(text_1)

transform = VGroup(*[Integer(i) for i in range(4,7)])
text_2 = Text("Transform", color=BLUE)
transform.add(text_2)

ints = VGroup(r_transform, transform)
texts = VGroup(text_1, text_2).scale(0.75)
r_transform.arrange(direction=UP, buff=1)
transform.arrange(direction=UP, buff=1)

ints.arrange(buff=2)
self.add(ints, texts)

# The mobs replace each other and none are left behind
self.play(ReplacementTransform(r_transform[0], r_transform[1]))
self.play(ReplacementTransform(r_transform[1], r_transform[2]))

# The mobs linger after the Transform()
self.play(Transform(transform[0], transform[1]))
self.play(Transform(transform[1], transform[2]))
self.wait()

Methods

Attributes

path_arc

path_func

run_time

_original__init__(mobject, target_mobject, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

target_mobject (Mobject)

Return type:
None


---

## Restore - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.Restore.html

Restore¶

Qualified name: manim.animation.transform.Restore

class Restore(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: ApplyMethod

Transforms a mobject to its last saved state.

To save the state of a mobject, use the save_state() method.

Examples

Example: RestoreExample ¶

from manim import *

class RestoreExample(Scene):
def construct(self):
s = Square()
s.save_state()
self.play(FadeIn(s))
self.play(s.animate.set_color(PURPLE).set_opacity(0.5).shift(2*LEFT).scale(3))
self.play(s.animate.shift(5*DOWN).rotate(PI/4))
self.wait()
self.play(Restore(s), run_time=2)

class RestoreExample(Scene):
def construct(self):
s = Square()
s.save_state()
self.play(FadeIn(s))
self.play(s.animate.set_color(PURPLE).set_opacity(0.5).shift(2*LEFT).scale(3))
self.play(s.animate.shift(5*DOWN).rotate(PI/4))
self.wait()
self.play(Restore(s), run_time=2)

Methods

Attributes

path_arc

path_func

run_time

Parameters:
mobject (Mobject)

_original__init__(mobject, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:
mobject (Mobject)

Return type:
None


---

## ScaleInPlace - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.ScaleInPlace.html

ScaleInPlace¶

Qualified name: manim.animation.transform.ScaleInPlace

class ScaleInPlace(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: ApplyMethod

Animation that scales a mobject by a certain factor.

Examples

Example: ScaleInPlaceExample ¶

from manim import *

class ScaleInPlaceExample(Scene):
def construct(self):
self.play(ScaleInPlace(Text("Hello World!"), 2))

class ScaleInPlaceExample(Scene):
def construct(self):
self.play(ScaleInPlace(Text("Hello World!"), 2))

Methods

Attributes

path_arc

path_func

run_time

Parameters:

mobject (Mobject)

scale_factor (float)

_original__init__(mobject, scale_factor, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

scale_factor (float)

Return type:
None


---

## ShrinkToCenter - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.ShrinkToCenter.html

ShrinkToCenter¶

Qualified name: manim.animation.transform.ShrinkToCenter

class ShrinkToCenter(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: ScaleInPlace

Animation that makes a mobject shrink to center.

Examples

Example: ShrinkToCenterExample ¶

from manim import *

class ShrinkToCenterExample(Scene):
def construct(self):
self.play(ShrinkToCenter(Text("Hello World!")))

class ShrinkToCenterExample(Scene):
def construct(self):
self.play(ShrinkToCenter(Text("Hello World!")))

Methods

Attributes

path_arc

path_func

run_time

Parameters:
mobject (Mobject)

_original__init__(mobject, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:
mobject (Mobject)

Return type:
None


---

## Swap - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.Swap.html

Swap¶

Qualified name: manim.animation.transform.Swap

class Swap(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: CyclicReplace

Methods

Attributes

path_arc

path_func

run_time

Parameters:

mobjects (Mobject)

path_arc (float)

_original__init__(*mobjects, path_arc=1.5707963267948966, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobjects (Mobject)

path_arc (float)

Return type:
None


---

## Transform - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.Transform.html

Transform¶

Qualified name: manim.animation.transform.Transform

class Transform(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Animation

A Transform transforms a Mobject into a target Mobject.

Parameters:

mobject (Mobject | None) – The Mobject to be transformed. It will be mutated to become the target_mobject.

target_mobject (Mobject | None) – The target of the transformation.

path_func (Callable | None) – A function defining the path that the points of the mobject are being moved
along until they match the points of the target_mobject, see utils.paths.

path_arc (float) – The arc angle (in radians) that the points of mobject will follow to reach
the points of the target if using a circular path arc, see path_arc_centers.
See also manim.utils.paths.path_along_arc().

path_arc_axis (np.ndarray) – The axis to rotate along if using a circular path arc, see path_arc_centers.

path_arc_centers (Point3DLike | Point3DLike_Array | None) – The center of the circular arcs along which the points of mobject are
moved by the transformation.

If this is set and path_func is not set, then a path_along_circles path will be generated
using the path_arc parameters and stored in path_func. If path_func is set, this and the
other path_arc fields are set as attributes, but a path_func is not generated from it.

replace_mobject_with_target_in_scene (bool) – Controls which mobject is replaced when the transformation is complete.

If set to True, mobject will be removed from the scene and target_mobject will
replace it. Otherwise, target_mobject is never added and mobject just takes its shape.

Examples

Example: TransformPathArc ¶

from manim import *

class TransformPathArc(Scene):
def construct(self):
def make_arc_path(start, end, arc_angle):
points = []
p_fn = path_along_arc(arc_angle)
# alpha animates between 0.0 and 1.0, where 0.0
# is the beginning of the animation and 1.0 is the end.
for alpha in range(0, 11):
points.append(p_fn(start, end, alpha / 10.0))
path = VMobject(stroke_color=YELLOW)
path.set_points_smoothly(points)
return path

left = Circle(stroke_color=BLUE_E, fill_opacity=1.0, radius=0.5).move_to(LEFT * 2)
colors = [TEAL_A, TEAL_B, TEAL_C, TEAL_D, TEAL_E, GREEN_A]
# Positive angles move counter-clockwise, negative angles move clockwise.
examples = [-90, 0, 30, 90, 180, 270]
anims = []
for idx, angle in enumerate(examples):
left_c = left.copy().shift((3 - idx) * UP)
left_c.fill_color = colors[idx]
right_c = left_c.copy().shift(4 * RIGHT)
path_arc = make_arc_path(left_c.get_center(), right_c.get_center(),
arc_angle=angle * DEGREES)
desc = Text('%d°' % examples[idx]).next_to(left_c, LEFT)
# Make the circles in front of the text in front of the arcs.
self.add(
path_arc.set_z_index(1),
desc.set_z_index(2),
left_c.set_z_index(3),
)
anims.append(Transform(left_c, right_c, path_arc=angle * DEGREES))

self.play(*anims, run_time=2)
self.wait()

class TransformPathArc(Scene):
def construct(self):
def make_arc_path(start, end, arc_angle):
points = []
p_fn = path_along_arc(arc_angle)
# alpha animates between 0.0 and 1.0, where 0.0
# is the beginning of the animation and 1.0 is the end.
for alpha in range(0, 11):
points.append(p_fn(start, end, alpha / 10.0))
path = VMobject(stroke_color=YELLOW)
path.set_points_smoothly(points)
return path

left = Circle(stroke_color=BLUE_E, fill_opacity=1.0, radius=0.5).move_to(LEFT * 2)
colors = [TEAL_A, TEAL_B, TEAL_C, TEAL_D, TEAL_E, GREEN_A]
# Positive angles move counter-clockwise, negative angles move clockwise.
examples = [-90, 0, 30, 90, 180, 270]
anims = []
for idx, angle in enumerate(examples):
left_c = left.copy().shift((3 - idx) * UP)
left_c.fill_color = colors[idx]
right_c = left_c.copy().shift(4 * RIGHT)
path_arc = make_arc_path(left_c.get_center(), right_c.get_center(),
arc_angle=angle * DEGREES)
desc = Text('%d°' % examples[idx]).next_to(left_c, LEFT)
# Make the circles in front of the text in front of the arcs.
self.add(
path_arc.set_z_index(1),
desc.set_z_index(2),
left_c.set_z_index(3),
)
anims.append(Transform(left_c, right_c, path_arc=angle * DEGREES))

self.play(*anims, run_time=2)
self.wait()

See also

ReplacementTransform, interpolate(), align_data()

Methods

begin

Begin the animation.

clean_up_from_scene

Clean up the Scene after finishing the animation.

create_target

get_all_families_zipped

get_all_mobjects

Get all mobjects involved in the animation.

interpolate_submobject

Attributes

path_arc

path_func

run_time

_original__init__(mobject, target_mobject=None, path_func=None, path_arc=0, path_arc_axis=array([0., 0., 1.]), path_arc_centers=None, replace_mobject_with_target_in_scene=False, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject | None)

target_mobject (Mobject | None)

path_func (Callable | None)

path_arc (float)

path_arc_axis (ndarray)

path_arc_centers (TypeAliasForwardRef('~manim.typing.Point3DLike') | TypeAliasForwardRef('~manim.typing.Point3DLike_Array') | None)

replace_mobject_with_target_in_scene (bool)

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

get_all_mobjects()[source]¶
Get all mobjects involved in the animation.

Ordering must match the ordering of arguments to interpolate_submobject

Returns:
The sequence of mobjects.

Return type:
Sequence[Mobject]


---

## TransformAnimations - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.TransformAnimations.html

TransformAnimations¶

Qualified name: manim.animation.transform.TransformAnimations

class TransformAnimations(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Transform

Methods

interpolate

Set the animation progress.

Attributes

path_arc

path_func

run_time

Parameters:

start_anim (Animation)

end_anim (Animation)

rate_func (Callable)

_original__init__(start_anim, end_anim, rate_func=<function squish_rate_func.<locals>.result>, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

start_anim (Animation)

end_anim (Animation)

rate_func (Callable)

Return type:
None

interpolate(alpha)[source]¶
Set the animation progress.

This method gets called for every frame during an animation.

Parameters:
alpha (float) – The relative time to set the animation to, 0 meaning the start, 1 meaning
the end.

Return type:
None


---

## TransformFromCopy - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform.TransformFromCopy.html

TransformFromCopy¶

Qualified name: manim.animation.transform.TransformFromCopy

class TransformFromCopy(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Transform

Preserves a copy of the original VMobject and transforms only it’s copy to the target VMobject

Methods

interpolate

Set the animation progress.

Attributes

path_arc

path_func

run_time

Parameters:

mobject (Mobject)

target_mobject (Mobject)

_original__init__(mobject, target_mobject, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

target_mobject (Mobject)

Return type:
None

interpolate(alpha)[source]¶
Set the animation progress.

This method gets called for every frame during an animation.

Parameters:
alpha (float) – The relative time to set the animation to, 0 meaning the start, 1 meaning
the end.

Return type:
None
