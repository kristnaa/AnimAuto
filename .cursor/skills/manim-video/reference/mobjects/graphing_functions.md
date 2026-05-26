# Graphing Functions


---

## FunctionGraph - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.graphing.functions.FunctionGraph.html

FunctionGraph¶

Qualified name: manim.mobject.graphing.functions.FunctionGraph

class FunctionGraph(function, x_range=None, color=ManimColor('#FFFF00'), **kwargs)[source]¶
Bases: ParametricFunction

A ParametricFunction that spans the length of the scene by default.

Examples

Example: ExampleFunctionGraph ¶

from manim import *

class ExampleFunctionGraph(Scene):
def construct(self):
cos_func = FunctionGraph(
lambda t: np.cos(t) + 0.5 * np.cos(7 * t) + (1 / 7) * np.cos(14 * t),
color=RED,
)

sin_func_1 = FunctionGraph(
lambda t: np.sin(t) + 0.5 * np.sin(7 * t) + (1 / 7) * np.sin(14 * t),
color=BLUE,
)

sin_func_2 = FunctionGraph(
lambda t: np.sin(t) + 0.5 * np.sin(7 * t) + (1 / 7) * np.sin(14 * t),
x_range=[-4, 4],
color=GREEN,
).move_to([0, 1, 0])

self.add(cos_func, sin_func_1, sin_func_2)

class ExampleFunctionGraph(Scene):
def construct(self):
cos_func = FunctionGraph(
lambda t: np.cos(t) + 0.5 * np.cos(7 * t) + (1 / 7) * np.cos(14 * t),
color=RED,
)

sin_func_1 = FunctionGraph(
lambda t: np.sin(t) + 0.5 * np.sin(7 * t) + (1 / 7) * np.sin(14 * t),
color=BLUE,
)

sin_func_2 = FunctionGraph(
lambda t: np.sin(t) + 0.5 * np.sin(7 * t) + (1 / 7) * np.sin(14 * t),
x_range=[-4, 4],
color=GREEN,
).move_to([0, 1, 0])

self.add(cos_func, sin_func_1, sin_func_2)

Methods

get_function

get_point_from_function

Attributes

always

Call a method on a mobject every frame.

animate

Used to animate the application of any method of self.

animation_overrides

color

depth

The depth of the mobject.

fill_color

If there are multiple colors (for gradient) this returns the first one

height

The height of the mobject.

n_points_per_curve

sheen_factor

stroke_color

width

The width of the mobject.

Parameters:

function (Callable[[float], Any])

x_range (tuple[float, float] | tuple[float, float, float] | None)

color (ParsableManimColor)

kwargs (Any)

_original__init__(function, x_range=None, color=ManimColor('#FFFF00'), **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

function (Callable[[float], Any])

x_range (tuple[float, float] | tuple[float, float, float] | None)

color (ParsableManimColor)

kwargs (Any)

Return type:
None


---

## ImplicitFunction - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.graphing.functions.ImplicitFunction.html

ImplicitFunction¶

Qualified name: manim.mobject.graphing.functions.ImplicitFunction

class ImplicitFunction(func, x_range=None, y_range=None, min_depth=5, max_quads=1500, use_smoothing=True, **kwargs)[source]¶
Bases: VMobject

An implicit function.

Parameters:

func (Callable[[float, float], float]) – The implicit function in the form f(x, y) = 0.

x_range (Sequence[float] | None) – The x min and max of the function.

y_range (Sequence[float] | None) – The y min and max of the function.

min_depth (int) – The minimum depth of the function to calculate.

max_quads (int) – The maximum number of quads to use.

use_smoothing (bool) – Whether or not to smoothen the curves.

kwargs (Any) – Additional parameters to pass into VMobject

Note

A small min_depth \(d\) means that some small details might
be ignored if they don’t cross an edge of one of the
\(4^d\) uniform quads.

The value of max_quads strongly corresponds to the
quality of the curve, but a higher number of quads
may take longer to render.

Examples

Example: ImplicitFunctionExample ¶

from manim import *

class ImplicitFunctionExample(Scene):
def construct(self):
graph = ImplicitFunction(
lambda x, y: x * y ** 2 - x ** 2 * y - 2,
color=YELLOW
)
self.add(NumberPlane(), graph)

class ImplicitFunctionExample(Scene):
def construct(self):
graph = ImplicitFunction(
lambda x, y: x * y ** 2 - x ** 2 * y - 2,
color=YELLOW
)
self.add(NumberPlane(), graph)

Methods

generate_points

Initializes points and therefore the shape.

init_points

Attributes

always

Call a method on a mobject every frame.

animate

Used to animate the application of any method of self.

animation_overrides

color

depth

The depth of the mobject.

fill_color

If there are multiple colors (for gradient) this returns the first one

height

The height of the mobject.

n_points_per_curve

sheen_factor

stroke_color

width

The width of the mobject.

_original__init__(func, x_range=None, y_range=None, min_depth=5, max_quads=1500, use_smoothing=True, **kwargs)¶
An implicit function.

Parameters:

func (Callable[[float, float], float]) – The implicit function in the form f(x, y) = 0.

x_range (Sequence[float] | None) – The x min and max of the function.

y_range (Sequence[float] | None) – The y min and max of the function.

min_depth (int) – The minimum depth of the function to calculate.

max_quads (int) – The maximum number of quads to use.

use_smoothing (bool) – Whether or not to smoothen the curves.

kwargs (Any) – Additional parameters to pass into VMobject

Note

A small min_depth \(d\) means that some small details might
be ignored if they don’t cross an edge of one of the
\(4^d\) uniform quads.

The value of max_quads strongly corresponds to the
quality of the curve, but a higher number of quads
may take longer to render.

Examples

Example: ImplicitFunctionExample ¶

from manim import *

class ImplicitFunctionExample(Scene):
def construct(self):
graph = ImplicitFunction(
lambda x, y: x * y ** 2 - x ** 2 * y - 2,
color=YELLOW
)
self.add(NumberPlane(), graph)

class ImplicitFunctionExample(Scene):
def construct(self):
graph = ImplicitFunction(
lambda x, y: x * y ** 2 - x ** 2 * y - 2,
color=YELLOW
)
self.add(NumberPlane(), graph)

generate_points()[source]¶
Initializes points and therefore the shape.

Gets called upon creation. This is an empty method that can be implemented by
subclasses.

Return type:
Self


---

## ParametricFunction - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.graphing.functions.ParametricFunction.html

ParametricFunction¶

Qualified name: manim.mobject.graphing.functions.ParametricFunction

class ParametricFunction(function, t_range=(0, 1), scaling=<manim.mobject.graphing.scale.LinearBase object>, dt=1e-08, discontinuities=None, use_smoothing=True, use_vectorized=False, **kwargs)[source]¶
Bases: VMobject

A parametric curve.

Parameters:

function (Callable[[float], Point3DLike]) – The function to be plotted in the form of (lambda t: (x(t), y(t), z(t)))

t_range (tuple[float, float] | tuple[float, float, float]) – Determines the length that the function spans in the form of (t_min, t_max, step=0.01). By default [0, 1]

scaling (_ScaleBase) – Scaling class applied to the points of the function. Default of LinearBase.

use_smoothing (bool) – Whether to interpolate between the points of the function after they have been created.
(Will have odd behaviour with a low number of points)

use_vectorized (bool) – Whether to pass in the generated t value array to the function as [t_0, t_1, ...].
Only use this if your function supports it. Output should be a numpy array
of shape [[x_0, x_1, ...], [y_0, y_1, ...], [z_0, z_1, ...]] but z can
also be 0 if the Axes is 2D

discontinuities (Iterable[float] | None) – Values of t at which the function experiences discontinuity.

dt (float) – The left and right tolerance for the discontinuities.

kwargs (Any)

Examples

Example: PlotParametricFunction ¶

from manim import *

class PlotParametricFunction(Scene):
def func(self, t):
return (np.sin(2 * t), np.sin(3 * t), 0)

def construct(self):
func = ParametricFunction(self.func, t_range = (0, TAU), fill_opacity=0).set_color(RED)
self.add(func.scale(3))

class PlotParametricFunction(Scene):
def func(self, t):
return (np.sin(2 * t), np.sin(3 * t), 0)

def construct(self):
func = ParametricFunction(self.func, t_range = (0, TAU), fill_opacity=0).set_color(RED)
self.add(func.scale(3))

Example: ThreeDParametricSpring ¶

from manim import *

class ThreeDParametricSpring(ThreeDScene):
def construct(self):
curve1 = ParametricFunction(
lambda u: (
1.2 * np.cos(u),
1.2 * np.sin(u),
u * 0.05
), color=RED, t_range = (-3*TAU, 5*TAU, 0.01)
).set_shade_in_3d(True)
axes = ThreeDAxes()
self.add(axes, curve1)
self.set_camera_orientation(phi=80 * DEGREES, theta=-60 * DEGREES)
self.wait()

class ThreeDParametricSpring(ThreeDScene):
def construct(self):
curve1 = ParametricFunction(
lambda u: (
1.2 * np.cos(u),
1.2 * np.sin(u),
u * 0.05
), color=RED, t_range = (-3*TAU, 5*TAU, 0.01)
).set_shade_in_3d(True)
axes = ThreeDAxes()
self.add(axes, curve1)
self.set_camera_orientation(phi=80 * DEGREES, theta=-60 * DEGREES)
self.wait()

Attention

If your function has discontinuities, you’ll have to specify the location
of the discontinuities manually. See the following example for guidance.

Example: DiscontinuousExample ¶

from manim import *

class DiscontinuousExample(Scene):
def construct(self):
ax1 = NumberPlane((-3, 3), (-4, 4))
ax2 = NumberPlane((-3, 3), (-4, 4))
VGroup(ax1, ax2).arrange()
discontinuous_function = lambda x: (x ** 2 - 2) / (x ** 2 - 4)
incorrect = ax1.plot(discontinuous_function, color=RED)
correct = ax2.plot(
discontinuous_function,
discontinuities=[-2, 2],  # discontinuous points
dt=0.1,  # left and right tolerance of discontinuity
color=GREEN,
)
self.add(ax1, ax2, incorrect, correct)

class DiscontinuousExample(Scene):
def construct(self):
ax1 = NumberPlane((-3, 3), (-4, 4))
ax2 = NumberPlane((-3, 3), (-4, 4))
VGroup(ax1, ax2).arrange()
discontinuous_function = lambda x: (x ** 2 - 2) / (x ** 2 - 4)
incorrect = ax1.plot(discontinuous_function, color=RED)
correct = ax2.plot(
discontinuous_function,
discontinuities=[-2, 2],  # discontinuous points
dt=0.1,  # left and right tolerance of discontinuity
color=GREEN,
)
self.add(ax1, ax2, incorrect, correct)

Methods

generate_points

Initializes points and therefore the shape.

get_function

get_point_from_function

init_points

Attributes

always

Call a method on a mobject every frame.

animate

Used to animate the application of any method of self.

animation_overrides

color

depth

The depth of the mobject.

fill_color

If there are multiple colors (for gradient) this returns the first one

height

The height of the mobject.

n_points_per_curve

sheen_factor

stroke_color

width

The width of the mobject.

_original__init__(function, t_range=(0, 1), scaling=<manim.mobject.graphing.scale.LinearBase object>, dt=1e-08, discontinuities=None, use_smoothing=True, use_vectorized=False, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

function (Callable[[float], Point3DLike])

t_range (tuple[float, float] | tuple[float, float, float])

scaling (_ScaleBase)

dt (float)

discontinuities (Iterable[float] | None)

use_smoothing (bool)

use_vectorized (bool)

kwargs (Any)

generate_points()[source]¶
Initializes points and therefore the shape.

Gets called upon creation. This is an empty method that can be implemented by
subclasses.

Return type:
Self


---

## functions - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.graphing.functions.html

functions¶

Mobjects representing function graphs.

Classes

FunctionGraph

A ParametricFunction that spans the length of the scene by default.

ImplicitFunction

An implicit function.

ParametricFunction

A parametric curve.
