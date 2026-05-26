# Movement


---

## ComplexHomotopy - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.movement.ComplexHomotopy.html

ComplexHomotopy¶

Qualified name: manim.animation.movement.ComplexHomotopy

class ComplexHomotopy(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Homotopy

Complex Homotopy a function Cx[0, 1] to C

Methods

Attributes

run_time

Parameters:

complex_homotopy (Callable[[complex, float], float])

mobject (Mobject)

kwargs (Any)

_original__init__(complex_homotopy, mobject, **kwargs)¶
Complex Homotopy a function Cx[0, 1] to C

Parameters:

complex_homotopy (Callable[[complex, float], float])

mobject (Mobject)

kwargs (Any)


---

## Homotopy - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.movement.Homotopy.html

Homotopy¶

Qualified name: manim.animation.movement.Homotopy

class Homotopy(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Animation

A Homotopy.

This is an animation transforming the points of a mobject according
to the specified transformation function. With the parameter \(t\)
moving from 0 to 1 throughout the animation and \((x, y, z)\)
describing the coordinates of the point of a mobject,
the function passed to the homotopy keyword argument should
transform the tuple \((x, y, z, t)\) to \((x', y', z')\),
the coordinates the original point is transformed to at time \(t\).

Parameters:

homotopy (Callable[[float, float, float, float], tuple[float, float, float]]) – A function mapping \((x, y, z, t)\) to \((x', y', z')\).

mobject (Mobject) – The mobject transformed under the given homotopy.

run_time (float) – The run time of the animation.

apply_function_kwargs (dict[str, Any] | None) – Keyword arguments propagated to Mobject.apply_function().

kwargs (Any) – Further keyword arguments passed to the parent class.

Examples

Example: HomotopyExample ¶

from manim import *

class HomotopyExample(Scene):
def construct(self):
square = Square()

def homotopy(x, y, z, t):
if t <= 0.25:
progress = t / 0.25
return (x, y + progress * 0.2 * np.sin(x), z)
else:
wave_progress = (t - 0.25) / 0.75
return (x, y + 0.2 * np.sin(x + 10 * wave_progress), z)

self.play(Homotopy(homotopy, square, rate_func= linear, run_time=2))

class HomotopyExample(Scene):
def construct(self):
square = Square()

def homotopy(x, y, z, t):
if t Methods

function_at_time_t

interpolate_submobject

Attributes

run_time

_original__init__(homotopy, mobject, run_time=3, apply_function_kwargs=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

homotopy (Callable[[float, float, float, float], tuple[float, float, float]])

mobject (Mobject)

run_time (float)

apply_function_kwargs (dict[str, Any] | None)

kwargs (Any)


---

## MoveAlongPath - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.movement.MoveAlongPath.html

MoveAlongPath¶

Qualified name: manim.animation.movement.MoveAlongPath

class MoveAlongPath(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Animation

Make one mobject move along the path of another mobject.

Example: MoveAlongPathExample ¶

from manim import *

class MoveAlongPathExample(Scene):
def construct(self):
d1 = Dot().set_color(ORANGE)
l1 = Line(LEFT, RIGHT)
l2 = VMobject()
self.add(d1, l1, l2)
l2.add_updater(lambda x: x.become(Line(LEFT, d1.get_center()).set_color(ORANGE)))
self.play(MoveAlongPath(d1, l1), rate_func=linear)

class MoveAlongPathExample(Scene):
def construct(self):
d1 = Dot().set_color(ORANGE)
l1 = Line(LEFT, RIGHT)
l2 = VMobject()
self.add(d1, l1, l2)
l2.add_updater(lambda x: x.become(Line(LEFT, d1.get_center()).set_color(ORANGE)))
self.play(MoveAlongPath(d1, l1), rate_func=linear)

Methods

interpolate_mobject

Interpolates the mobject of the Animation based on alpha value.

Attributes

run_time

Parameters:

mobject (Mobject)

path (VMobject)

suspend_mobject_updating (bool)

kwargs (Any)

_original__init__(mobject, path, suspend_mobject_updating=False, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

path (VMobject)

suspend_mobject_updating (bool)

kwargs (Any)

interpolate_mobject(alpha)[source]¶
Interpolates the mobject of the Animation based on alpha value.

Parameters:
alpha (float) – A float between 0 and 1 expressing the ratio to which the animation
is completed. For example, alpha-values of 0, 0.5, and 1 correspond
to the animation being completed 0%, 50%, and 100%, respectively.

Return type:
None


---

## PhaseFlow - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.movement.PhaseFlow.html

PhaseFlow¶

Qualified name: manim.animation.movement.PhaseFlow

class PhaseFlow(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Animation

Methods

interpolate_mobject

Interpolates the mobject of the Animation based on alpha value.

Attributes

run_time

Parameters:

function (Callable[[np.ndarray], np.ndarray])

mobject (Mobject)

virtual_time (float)

suspend_mobject_updating (bool)

rate_func (RateFunction)

kwargs (Any)

_original__init__(function, mobject, virtual_time=1, suspend_mobject_updating=False, rate_func=<function linear>, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

function (Callable[[np.ndarray], np.ndarray])

mobject (Mobject)

virtual_time (float)

suspend_mobject_updating (bool)

rate_func (RateFunction)

kwargs (Any)

interpolate_mobject(alpha)[source]¶
Interpolates the mobject of the Animation based on alpha value.

Parameters:
alpha (float) – A float between 0 and 1 expressing the ratio to which the animation
is completed. For example, alpha-values of 0, 0.5, and 1 correspond
to the animation being completed 0%, 50%, and 100%, respectively.

Return type:
None


---

## SmoothedVectorizedHomotopy - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.movement.SmoothedVectorizedHomotopy.html

SmoothedVectorizedHomotopy¶

Qualified name: manim.animation.movement.SmoothedVectorizedHomotopy

class SmoothedVectorizedHomotopy(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Homotopy

Methods

interpolate_submobject

Attributes

run_time

Parameters:

homotopy (Callable[[float, float, float, float], tuple[float, float, float]])

mobject (Mobject)

run_time (float)

apply_function_kwargs (dict[str, Any] | None)

kwargs (Any)

_original__init__(homotopy, mobject, run_time=3, apply_function_kwargs=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

homotopy (Callable[[float, float, float, float], tuple[float, float, float]])

mobject (Mobject)

run_time (float)

apply_function_kwargs (dict[str, Any] | None)

kwargs (Any)
