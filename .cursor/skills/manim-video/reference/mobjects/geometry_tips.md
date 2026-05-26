# Geometry Tips


---

## ArrowCircleFilledTip - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.tips.ArrowCircleFilledTip.html

ArrowCircleFilledTip¶

Qualified name: manim.mobject.geometry.tips.ArrowCircleFilledTip

class ArrowCircleFilledTip(fill_opacity=1, stroke_width=0, **kwargs)[source]¶
Bases: ArrowCircleTip

Circular arrow tip with filled tip.

Methods

Attributes

always

Call a method on a mobject every frame.

animate

Used to animate the application of any method of self.

animation_overrides

base

The base point of the arrow tip.

color

depth

The depth of the mobject.

fill_color

If there are multiple colors (for gradient) this returns the first one

height

The height of the mobject.

length

The length of the arrow tip.

n_points_per_curve

sheen_factor

stroke_color

tip_angle

The angle of the arrow tip.

tip_point

The tip point of the arrow tip.

vector

The vector pointing from the base point to the tip point.

width

The width of the mobject.

Parameters:

fill_opacity (float)

stroke_width (float)

kwargs (Any)

_original__init__(fill_opacity=1, stroke_width=0, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

fill_opacity (float)

stroke_width (float)

kwargs (Any)

Return type:
None


---

## ArrowCircleTip - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.tips.ArrowCircleTip.html

ArrowCircleTip¶

Qualified name: manim.mobject.geometry.tips.ArrowCircleTip

class ArrowCircleTip(fill_opacity=0, stroke_width=3, length=0.35, start_angle=3.141592653589793, **kwargs)[source]¶
Bases: ArrowTip, Circle

Circular arrow tip.

Methods

Attributes

always

Call a method on a mobject every frame.

animate

Used to animate the application of any method of self.

animation_overrides

base

The base point of the arrow tip.

color

depth

The depth of the mobject.

fill_color

If there are multiple colors (for gradient) this returns the first one

height

The height of the mobject.

length

The length of the arrow tip.

n_points_per_curve

sheen_factor

stroke_color

tip_angle

The angle of the arrow tip.

tip_point

The tip point of the arrow tip.

vector

The vector pointing from the base point to the tip point.

width

The width of the mobject.

Parameters:

fill_opacity (float)

stroke_width (float)

length (float)

start_angle (float)

kwargs (Any)

_original__init__(fill_opacity=0, stroke_width=3, length=0.35, start_angle=3.141592653589793, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

fill_opacity (float)

stroke_width (float)

length (float)

start_angle (float)

kwargs (Any)

Return type:
None


---

## ArrowSquareFilledTip - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.tips.ArrowSquareFilledTip.html

ArrowSquareFilledTip¶

Qualified name: manim.mobject.geometry.tips.ArrowSquareFilledTip

class ArrowSquareFilledTip(fill_opacity=1, stroke_width=0, **kwargs)[source]¶
Bases: ArrowSquareTip

Square arrow tip with filled tip.

Methods

Attributes

always

Call a method on a mobject every frame.

animate

Used to animate the application of any method of self.

animation_overrides

base

The base point of the arrow tip.

color

depth

The depth of the mobject.

fill_color

If there are multiple colors (for gradient) this returns the first one

height

The height of the mobject.

length

The length of the arrow tip.

n_points_per_curve

sheen_factor

side_length

stroke_color

tip_angle

The angle of the arrow tip.

tip_point

The tip point of the arrow tip.

vector

The vector pointing from the base point to the tip point.

width

The width of the mobject.

Parameters:

fill_opacity (float)

stroke_width (float)

kwargs (Any)

_original__init__(fill_opacity=1, stroke_width=0, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

fill_opacity (float)

stroke_width (float)

kwargs (Any)

Return type:
None


---

## ArrowSquareTip - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.tips.ArrowSquareTip.html

ArrowSquareTip¶

Qualified name: manim.mobject.geometry.tips.ArrowSquareTip

class ArrowSquareTip(fill_opacity=0, stroke_width=3, length=0.35, start_angle=3.141592653589793, **kwargs)[source]¶
Bases: ArrowTip, Square

Square arrow tip.

Methods

Attributes

always

Call a method on a mobject every frame.

animate

Used to animate the application of any method of self.

animation_overrides

base

The base point of the arrow tip.

color

depth

The depth of the mobject.

fill_color

If there are multiple colors (for gradient) this returns the first one

height

The height of the mobject.

length

The length of the arrow tip.

n_points_per_curve

sheen_factor

side_length

stroke_color

tip_angle

The angle of the arrow tip.

tip_point

The tip point of the arrow tip.

vector

The vector pointing from the base point to the tip point.

width

The width of the mobject.

Parameters:

fill_opacity (float)

stroke_width (float)

length (float)

start_angle (float)

kwargs (Any)

_original__init__(fill_opacity=0, stroke_width=3, length=0.35, start_angle=3.141592653589793, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

fill_opacity (float)

stroke_width (float)

length (float)

start_angle (float)

kwargs (Any)

Return type:
None


---

## ArrowTip - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.tips.ArrowTip.html

ArrowTip¶

Qualified name: manim.mobject.geometry.tips.ArrowTip

class ArrowTip(*args, **kwargs)[source]¶
Bases: VMobject

Base class for arrow tips.

See also

ArrowTriangleTip
ArrowTriangleFilledTip
ArrowCircleTip
ArrowCircleFilledTip
ArrowSquareTip
ArrowSquareFilledTip
StealthTip

Examples

Cannot be used directly, only intended for inheritance:

>>> tip = ArrowTip()
Traceback (most recent call last):
...
NotImplementedError: Has to be implemented in inheriting subclasses.

Instead, use one of the pre-defined ones, or make
a custom one like this:

Example: CustomTipExample ¶

from manim import *

>>> from manim import RegularPolygon, Arrow
>>> class MyCustomArrowTip(ArrowTip, RegularPolygon):
...     def __init__(self, length=0.35, **kwargs):
...         RegularPolygon.__init__(self, n=5, **kwargs)
...         self.width = length
...         self.stretch_to_fit_height(length)
>>> arr = Arrow(
...     np.array([-2, -2, 0]), np.array([2, 2, 0]), tip_shape=MyCustomArrowTip
... )
>>> isinstance(arr.tip, RegularPolygon)
True
>>> from manim import Scene, Create
>>> class CustomTipExample(Scene):
...     def construct(self):
...         self.play(Create(arr))

>>> from manim import RegularPolygon, Arrow
>>> class MyCustomArrowTip(ArrowTip, RegularPolygon):
...     def __init__(self, length=0.35, **kwargs):
...         RegularPolygon.__init__(self, n=5, **kwargs)
...         self.width = length
...         self.stretch_to_fit_height(length)
>>> arr = Arrow(
...     np.array([-2, -2, 0]), np.array([2, 2, 0]), tip_shape=MyCustomArrowTip
... )
>>> isinstance(arr.tip, RegularPolygon)
True
>>> from manim import Scene, Create
>>> class CustomTipExample(Scene):
...     def construct(self):
...         self.play(Create(arr))

Using a class inherited from ArrowTip to get a non-filled
tip is a shorthand to manually specifying the arrow tip style as follows:

>>> arrow = Arrow(np.array([0, 0, 0]), np.array([1, 1, 0]),
...               tip_style={'fill_opacity': 0, 'stroke_width': 3})

The following example illustrates the usage of all of the predefined
arrow tips.

Example: ArrowTipsShowcase ¶

from manim import *

class ArrowTipsShowcase(Scene):
def construct(self):
tip_names = [
'Default (YELLOW)', 'ArrowTriangleTip', 'Default', 'ArrowSquareTip',
'ArrowSquareFilledTip', 'ArrowCircleTip', 'ArrowCircleFilledTip', 'StealthTip'
]

big_arrows = [
Arrow(start=[-4, 3.5, 0], end=[2, 3.5, 0], color=YELLOW),
Arrow(start=[-4, 2.5, 0], end=[2, 2.5, 0], tip_shape=ArrowTriangleTip),
Arrow(start=[-4, 1.5, 0], end=[2, 1.5, 0]),
Arrow(start=[-4, 0.5, 0], end=[2, 0.5, 0], tip_shape=ArrowSquareTip),

Arrow([-4, -0.5, 0], [2, -0.5, 0], tip_shape=ArrowSquareFilledTip),
Arrow([-4, -1.5, 0], [2, -1.5, 0], tip_shape=ArrowCircleTip),
Arrow([-4, -2.5, 0], [2, -2.5, 0], tip_shape=ArrowCircleFilledTip),
Arrow([-4, -3.5, 0], [2, -3.5, 0], tip_shape=StealthTip)
]

small_arrows = (
arrow.copy().scale(0.5, scale_tips=True).next_to(arrow, RIGHT) for arrow in big_arrows
)

labels = (
Text(tip_names[i], font='monospace', font_size=20, color=BLUE).next_to(big_arrows[i], LEFT) for i in range(len(big_arrows))
)

self.add(*big_arrows, *small_arrows, *labels)

class ArrowTipsShowcase(Scene):
def construct(self):
tip_names = [
'Default (YELLOW)', 'ArrowTriangleTip', 'Default', 'ArrowSquareTip',
'ArrowSquareFilledTip', 'ArrowCircleTip', 'ArrowCircleFilledTip', 'StealthTip'
]

big_arrows = [
Arrow(start=[-4, 3.5, 0], end=[2, 3.5, 0], color=YELLOW),
Arrow(start=[-4, 2.5, 0], end=[2, 2.5, 0], tip_shape=ArrowTriangleTip),
Arrow(start=[-4, 1.5, 0], end=[2, 1.5, 0]),
Arrow(start=[-4, 0.5, 0], end=[2, 0.5, 0], tip_shape=ArrowSquareTip),

Arrow([-4, -0.5, 0], [2, -0.5, 0], tip_shape=ArrowSquareFilledTip),
Arrow([-4, -1.5, 0], [2, -1.5, 0], tip_shape=ArrowCircleTip),
Arrow([-4, -2.5, 0], [2, -2.5, 0], tip_shape=ArrowCircleFilledTip),
Arrow([-4, -3.5, 0], [2, -3.5, 0], tip_shape=StealthTip)
]

small_arrows = (
arrow.copy().scale(0.5, scale_tips=True).next_to(arrow, RIGHT) for arrow in big_arrows
)

labels = (
Text(tip_names[i], font='monospace', font_size=20, color=BLUE).next_to(big_arrows[i], LEFT) for i in range(len(big_arrows))
)

self.add(*big_arrows, *small_arrows, *labels)

Methods

Attributes

always

Call a method on a mobject every frame.

animate

Used to animate the application of any method of self.

animation_overrides

base

The base point of the arrow tip.

color

depth

The depth of the mobject.

fill_color

If there are multiple colors (for gradient) this returns the first one

height

The height of the mobject.

length

The length of the arrow tip.

n_points_per_curve

sheen_factor

stroke_color

tip_angle

The angle of the arrow tip.

tip_point

The tip point of the arrow tip.

vector

The vector pointing from the base point to the tip point.

width

The width of the mobject.

Parameters:

args (Any)

kwargs (Any)

_original__init__(*args, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

args (Any)

kwargs (Any)

Return type:
None

property base: Point3D¶
The base point of the arrow tip.

This is the point connecting to the arrow line.

Examples

>>> from manim import Arrow
>>> arrow = Arrow(np.array([0, 0, 0]), np.array([2, 0, 0]), buff=0)
>>> arrow.tip.base.round(2) + 0.  # add 0. to avoid negative 0 in output
array([1.65, 0.  , 0.  ])

property length: float¶
The length of the arrow tip.

Examples

>>> from manim import Arrow
>>> arrow = Arrow(np.array([0, 0, 0]), np.array([1, 2, 0]))
>>> round(arrow.tip.length, 3)
0.35

property tip_angle: float¶
The angle of the arrow tip.

Examples

>>> from manim import Arrow
>>> arrow = Arrow(np.array([0, 0, 0]), np.array([1, 1, 0]), buff=0)
>>> bool(round(arrow.tip.tip_angle, 5) == round(PI/4, 5))
True

property tip_point: Point3D¶
The tip point of the arrow tip.

Examples

>>> from manim import Arrow
>>> arrow = Arrow(np.array([0, 0, 0]), np.array([2, 0, 0]), buff=0)
>>> arrow.tip.tip_point.round(2) + 0.
array([2., 0., 0.])

property vector: Vector3D¶
The vector pointing from the base point to the tip point.

Examples

>>> from manim import Arrow
>>> arrow = Arrow(np.array([0, 0, 0]), np.array([2, 2, 0]), buff=0)
>>> arrow.tip.vector.round(2) + 0.
array([0.25, 0.25, 0.  ])


---

## ArrowTriangleFilledTip - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.tips.ArrowTriangleFilledTip.html

ArrowTriangleFilledTip¶

Qualified name: manim.mobject.geometry.tips.ArrowTriangleFilledTip

class ArrowTriangleFilledTip(fill_opacity=1, stroke_width=0, **kwargs)[source]¶
Bases: ArrowTriangleTip

Triangular arrow tip with filled tip.

This is the default arrow tip shape.

Methods

Attributes

always

Call a method on a mobject every frame.

animate

Used to animate the application of any method of self.

animation_overrides

base

The base point of the arrow tip.

color

depth

The depth of the mobject.

fill_color

If there are multiple colors (for gradient) this returns the first one

height

The height of the mobject.

length

The length of the arrow tip.

n_points_per_curve

sheen_factor

stroke_color

tip_angle

The angle of the arrow tip.

tip_point

The tip point of the arrow tip.

vector

The vector pointing from the base point to the tip point.

width

The width of the mobject.

Parameters:

fill_opacity (float)

stroke_width (float)

kwargs (Any)

_original__init__(fill_opacity=1, stroke_width=0, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

fill_opacity (float)

stroke_width (float)

kwargs (Any)

Return type:
None


---

## ArrowTriangleTip - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.tips.ArrowTriangleTip.html

ArrowTriangleTip¶

Qualified name: manim.mobject.geometry.tips.ArrowTriangleTip

class ArrowTriangleTip(fill_opacity=0, stroke_width=3, length=0.35, width=0.35, start_angle=3.141592653589793, **kwargs)[source]¶
Bases: ArrowTip, Triangle

Triangular arrow tip.

Methods

Attributes

always

Call a method on a mobject every frame.

animate

Used to animate the application of any method of self.

animation_overrides

base

The base point of the arrow tip.

color

depth

The depth of the mobject.

fill_color

If there are multiple colors (for gradient) this returns the first one

height

The height of the mobject.

length

The length of the arrow tip.

n_points_per_curve

sheen_factor

stroke_color

tip_angle

The angle of the arrow tip.

tip_point

The tip point of the arrow tip.

vector

The vector pointing from the base point to the tip point.

width

The width of the mobject.

Parameters:

fill_opacity (float)

stroke_width (float)

length (float)

width (float)

start_angle (float)

kwargs (Any)

_original__init__(fill_opacity=0, stroke_width=3, length=0.35, width=0.35, start_angle=3.141592653589793, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

fill_opacity (float)

stroke_width (float)

length (float)

width (float)

start_angle (float)

kwargs (Any)

Return type:
None


---

## StealthTip - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.tips.StealthTip.html

StealthTip¶

Qualified name: manim.mobject.geometry.tips.StealthTip

class StealthTip(fill_opacity=1, stroke_width=3, length=0.175, start_angle=3.141592653589793, **kwargs)[source]¶
Bases: ArrowTip

‘Stealth’ fighter / kite arrow shape.

Naming is inspired by the corresponding
TikZ arrow shape.

Methods

Attributes

always

Call a method on a mobject every frame.

animate

Used to animate the application of any method of self.

animation_overrides

base

The base point of the arrow tip.

color

depth

The depth of the mobject.

fill_color

If there are multiple colors (for gradient) this returns the first one

height

The height of the mobject.

length

The length of the arrow tip.

n_points_per_curve

sheen_factor

stroke_color

tip_angle

The angle of the arrow tip.

tip_point

The tip point of the arrow tip.

vector

The vector pointing from the base point to the tip point.

width

The width of the mobject.

Parameters:

fill_opacity (float)

stroke_width (float)

length (float)

start_angle (float)

kwargs (Any)

_original__init__(fill_opacity=1, stroke_width=3, length=0.175, start_angle=3.141592653589793, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

fill_opacity (float)

stroke_width (float)

length (float)

start_angle (float)

kwargs (Any)

property length: float¶
The length of the arrow tip.

In this case, the length is computed as the height of
the triangle encompassing the stealth tip (otherwise,
the tip is scaled too large).


---

## tips - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.tips.html

tips¶

A collection of tip mobjects for use with TipableVMobject.

Classes

ArrowCircleFilledTip

Circular arrow tip with filled tip.

ArrowCircleTip

Circular arrow tip.

ArrowSquareFilledTip

Square arrow tip with filled tip.

ArrowSquareTip

Square arrow tip.

ArrowTip

Base class for arrow tips.

ArrowTriangleFilledTip

Triangular arrow tip with filled tip.

ArrowTriangleTip

Triangular arrow tip.

StealthTip

'Stealth' fighter / kite arrow shape.
