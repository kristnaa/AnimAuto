# Growing


---

## GrowArrow - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.growing.GrowArrow.html

GrowArrow¶

Qualified name: manim.animation.growing.GrowArrow

class GrowArrow(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: GrowFromPoint

Introduce an Arrow by growing it from its start toward its tip.

Parameters:

arrow (Arrow) – The arrow to be introduced.

point_color (ParsableManimColor | None) – Initial color of the arrow before growing to its full size. Leave empty to match arrow’s color.

kwargs (Any)

Examples

Example: GrowArrowExample ¶

from manim import *

class GrowArrowExample(Scene):
def construct(self):
arrows = [Arrow(2 * LEFT, 2 * RIGHT), Arrow(2 * DR, 2 * UL)]
VGroup(*arrows).set_x(0).arrange(buff=2)
self.play(GrowArrow(arrows[0]))
self.play(GrowArrow(arrows[1], point_color=RED))

class GrowArrowExample(Scene):
def construct(self):
arrows = [Arrow(2 * LEFT, 2 * RIGHT), Arrow(2 * DR, 2 * UL)]
VGroup(*arrows).set_x(0).arrange(buff=2)
self.play(GrowArrow(arrows[0]))
self.play(GrowArrow(arrows[1], point_color=RED))

Methods

create_starting_mobject

Attributes

path_arc

path_func

run_time

_original__init__(arrow, point_color=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

arrow (Arrow)

point_color (ParsableManimColor | None)

kwargs (Any)


---

## GrowFromCenter - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.growing.GrowFromCenter.html

GrowFromCenter¶

Qualified name: manim.animation.growing.GrowFromCenter

class GrowFromCenter(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: GrowFromPoint

Introduce an Mobject by growing it from its center.

Parameters:

mobject (Mobject) – The mobjects to be introduced.

point_color (ParsableManimColor | None) – Initial color of the mobject before growing to its full size. Leave empty to match mobject’s color.

kwargs (Any)

Examples

Example: GrowFromCenterExample ¶

from manim import *

class GrowFromCenterExample(Scene):
def construct(self):
squares = [Square() for _ in range(2)]
VGroup(*squares).set_x(0).arrange(buff=2)
self.play(GrowFromCenter(squares[0]))
self.play(GrowFromCenter(squares[1], point_color=RED))

class GrowFromCenterExample(Scene):
def construct(self):
squares = [Square() for _ in range(2)]
VGroup(*squares).set_x(0).arrange(buff=2)
self.play(GrowFromCenter(squares[0]))
self.play(GrowFromCenter(squares[1], point_color=RED))

Methods

Attributes

path_arc

path_func

run_time

_original__init__(mobject, point_color=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

point_color (ParsableManimColor | None)

kwargs (Any)


---

## GrowFromEdge - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.growing.GrowFromEdge.html

GrowFromEdge¶

Qualified name: manim.animation.growing.GrowFromEdge

class GrowFromEdge(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: GrowFromPoint

Introduce an Mobject by growing it from one of its bounding box edges.

Parameters:

mobject (Mobject) – The mobjects to be introduced.

edge (Vector3DLike) – The direction to seek bounding box edge of mobject.

point_color (ParsableManimColor | None) – Initial color of the mobject before growing to its full size. Leave empty to match mobject’s color.

kwargs (Any)

Examples

Example: GrowFromEdgeExample ¶

from manim import *

class GrowFromEdgeExample(Scene):
def construct(self):
squares = [Square() for _ in range(4)]
VGroup(*squares).set_x(0).arrange(buff=1)
self.play(GrowFromEdge(squares[0], DOWN))
self.play(GrowFromEdge(squares[1], RIGHT))
self.play(GrowFromEdge(squares[2], UR))
self.play(GrowFromEdge(squares[3], UP, point_color=RED))

class GrowFromEdgeExample(Scene):
def construct(self):
squares = [Square() for _ in range(4)]
VGroup(*squares).set_x(0).arrange(buff=1)
self.play(GrowFromEdge(squares[0], DOWN))
self.play(GrowFromEdge(squares[1], RIGHT))
self.play(GrowFromEdge(squares[2], UR))
self.play(GrowFromEdge(squares[3], UP, point_color=RED))

Methods

Attributes

path_arc

path_func

run_time

_original__init__(mobject, edge, point_color=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

edge (Vector3DLike)

point_color (ParsableManimColor | None)

kwargs (Any)


---

## GrowFromPoint - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.growing.GrowFromPoint.html

GrowFromPoint¶

Qualified name: manim.animation.growing.GrowFromPoint

class GrowFromPoint(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Transform

Introduce an Mobject by growing it from a point.

Parameters:

mobject (Mobject) – The mobjects to be introduced.

point (Point3DLike) – The point from which the mobject grows.

point_color (ParsableManimColor | None) – Initial color of the mobject before growing to its full size. Leave empty to match mobject’s color.

kwargs (Any)

Examples

Example: GrowFromPointExample ¶

from manim import *

class GrowFromPointExample(Scene):
def construct(self):
dot = Dot(3 * UR, color=GREEN)
squares = [Square() for _ in range(4)]
VGroup(*squares).set_x(0).arrange(buff=1)
self.add(dot)
self.play(GrowFromPoint(squares[0], ORIGIN))
self.play(GrowFromPoint(squares[1], [-2, 2, 0]))
self.play(GrowFromPoint(squares[2], [3, -2, 0], RED))
self.play(GrowFromPoint(squares[3], dot, dot.get_color()))

class GrowFromPointExample(Scene):
def construct(self):
dot = Dot(3 * UR, color=GREEN)
squares = [Square() for _ in range(4)]
VGroup(*squares).set_x(0).arrange(buff=1)
self.add(dot)
self.play(GrowFromPoint(squares[0], ORIGIN))
self.play(GrowFromPoint(squares[1], [-2, 2, 0]))
self.play(GrowFromPoint(squares[2], [3, -2, 0], RED))
self.play(GrowFromPoint(squares[3], dot, dot.get_color()))

Methods

create_starting_mobject

create_target

Attributes

path_arc

path_func

run_time

_original__init__(mobject, point, point_color=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

point (Point3DLike)

point_color (ParsableManimColor | None)

kwargs (Any)


---

## SpinInFromNothing - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.growing.SpinInFromNothing.html

SpinInFromNothing¶

Qualified name: manim.animation.growing.SpinInFromNothing

class SpinInFromNothing(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: GrowFromCenter

Introduce an Mobject spinning and growing it from its center.

Parameters:

mobject (Mobject) – The mobjects to be introduced.

angle (float) – The amount of spinning before mobject reaches its full size. E.g. 2*PI means
that the object will do one full spin before being fully introduced.

point_color (ParsableManimColor | None) – Initial color of the mobject before growing to its full size. Leave empty to match mobject’s color.

kwargs (Any)

Examples

Example: SpinInFromNothingExample ¶

from manim import *

class SpinInFromNothingExample(Scene):
def construct(self):
squares = [Square() for _ in range(3)]
VGroup(*squares).set_x(0).arrange(buff=2)
self.play(SpinInFromNothing(squares[0]))
self.play(SpinInFromNothing(squares[1], angle=2 * PI))
self.play(SpinInFromNothing(squares[2], point_color=RED))

class SpinInFromNothingExample(Scene):
def construct(self):
squares = [Square() for _ in range(3)]
VGroup(*squares).set_x(0).arrange(buff=2)
self.play(SpinInFromNothing(squares[0]))
self.play(SpinInFromNothing(squares[1], angle=2 * PI))
self.play(SpinInFromNothing(squares[2], point_color=RED))

Methods

Attributes

path_arc

path_func

run_time

_original__init__(mobject, angle=1.5707963267948966, point_color=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

angle (float)

point_color (ParsableManimColor | None)

kwargs (Any)
