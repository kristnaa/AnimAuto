# Changing


---

## AnimatedBoundary - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.changing.AnimatedBoundary.html

AnimatedBoundary¶

Qualified name: manim.animation.changing.AnimatedBoundary

class AnimatedBoundary(vmobject, colors=[ManimColor('#29ABCA'), ManimColor('#9CDCEB'), ManimColor('#236B8E'), ManimColor('#736357')], max_stroke_width=3, cycle_rate=0.5, back_and_forth=True, draw_rate_func=<function smooth>, fade_rate_func=<function smooth>, **kwargs)[source]¶
Bases: VGroup

Boundary of a VMobject with animated color change.

Examples

Example: AnimatedBoundaryExample ¶

from manim import *

class AnimatedBoundaryExample(Scene):
def construct(self):
text = Text("So shiny!")
boundary = AnimatedBoundary(text, colors=[RED, GREEN, BLUE],
cycle_rate=3)
self.add(text, boundary)
self.wait(2)

class AnimatedBoundaryExample(Scene):
def construct(self):
text = Text("So shiny!")
boundary = AnimatedBoundary(text, colors=[RED, GREEN, BLUE],
cycle_rate=3)
self.add(text, boundary)
self.wait(2)

Methods

full_family_become_partial

update_boundary_copies

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

vmobject (VMobject)

colors (Sequence[ParsableManimColor])

max_stroke_width (float)

cycle_rate (float)

back_and_forth (bool)

draw_rate_func (RateFunction)

fade_rate_func (RateFunction)

kwargs (Any)

_original__init__(vmobject, colors=[ManimColor('#29ABCA'), ManimColor('#9CDCEB'), ManimColor('#236B8E'), ManimColor('#736357')], max_stroke_width=3, cycle_rate=0.5, back_and_forth=True, draw_rate_func=<function smooth>, fade_rate_func=<function smooth>, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

vmobject (VMobject)

colors (Sequence[TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor')])

max_stroke_width (float)

cycle_rate (float)

back_and_forth (bool)

draw_rate_func (RateFunction)

fade_rate_func (RateFunction)

kwargs (Any)


---

## TracedPath - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.changing.TracedPath.html

TracedPath¶

Qualified name: manim.animation.changing.TracedPath

class TracedPath(traced_point_func, stroke_width=2, stroke_color=ManimColor('#FFFFFF'), dissipating_time=None, **kwargs)[source]¶
Bases: VMobject

Traces the path of a point returned by a function call.

Parameters:

traced_point_func (Callable) – The function to be traced.

stroke_width (float) – The width of the trace.

stroke_color (ParsableManimColor | None) – The color of the trace.

dissipating_time (float | None) – The time taken for the path to dissipate. Default set to None
which disables dissipation.

kwargs (Any)

Examples

Example: TracedPathExample ¶

from manim import *

class TracedPathExample(Scene):
def construct(self):
circ = Circle(color=RED).shift(4*LEFT)
dot = Dot(color=RED).move_to(circ.get_start())
rolling_circle = VGroup(circ, dot)
trace = TracedPath(circ.get_start)
rolling_circle.add_updater(lambda m: m.rotate(-0.3))
self.add(trace, rolling_circle)
self.play(rolling_circle.animate.shift(8*RIGHT), run_time=4, rate_func=linear)

class TracedPathExample(Scene):
def construct(self):
circ = Circle(color=RED).shift(4*LEFT)
dot = Dot(color=RED).move_to(circ.get_start())
rolling_circle = VGroup(circ, dot)
trace = TracedPath(circ.get_start)
rolling_circle.add_updater(lambda m: m.rotate(-0.3))
self.add(trace, rolling_circle)
self.play(rolling_circle.animate.shift(8*RIGHT), run_time=4, rate_func=linear)

Example: DissipatingPathExample ¶

from manim import *

class DissipatingPathExample(Scene):
def construct(self):
a = Dot(RIGHT * 2)
b = TracedPath(a.get_center, dissipating_time=0.5, stroke_opacity=[0, 1])
self.add(a, b)
self.play(a.animate(path_arc=PI / 4).shift(LEFT * 2))
self.play(a.animate(path_arc=-PI / 4).shift(LEFT * 2))
self.wait()

class DissipatingPathExample(Scene):
def construct(self):
a = Dot(RIGHT * 2)
b = TracedPath(a.get_center, dissipating_time=0.5, stroke_opacity=[0, 1])
self.add(a, b)
self.play(a.animate(path_arc=PI / 4).shift(LEFT * 2))
self.play(a.animate(path_arc=-PI / 4).shift(LEFT * 2))
self.wait()

Methods

update_path

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

_original__init__(traced_point_func, stroke_width=2, stroke_color=ManimColor('#FFFFFF'), dissipating_time=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

traced_point_func (Callable)

stroke_width (float)

stroke_color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | None)

dissipating_time (float | None)

kwargs (Any)

Return type:
None
