# Constants


---

## CapStyleType - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.constants.CapStyleType.html

CapStyleType¶

Qualified name: manim.constants.CapStyleType

class CapStyleType(*values)[source]¶
Bases: Enum

Collection of available cap styles.

See the example below for a visual illustration of the different
cap styles.

Examples

Example: CapStyleVariants ¶

from manim import *

class CapStyleVariants(Scene):
def construct(self):
arcs = VGroup(*[
Arc(
radius=1,
start_angle=0,
angle=TAU / 4,
stroke_width=20,
color=GREEN,
cap_style=cap_style,
)
for cap_style in CapStyleType
])
arcs.arrange(RIGHT, buff=1)
self.add(arcs)
for arc in arcs:
label = Text(arc.cap_style.name, font_size=24).next_to(arc, DOWN)
self.add(label)

class CapStyleVariants(Scene):
def construct(self):
arcs = VGroup(*[
Arc(
radius=1,
start_angle=0,
angle=TAU / 4,
stroke_width=20,
color=GREEN,
cap_style=cap_style,
)
for cap_style in CapStyleType
])
arcs.arrange(RIGHT, buff=1)
self.add(arcs)
for arc in arcs:
label = Text(arc.cap_style.name, font_size=24).next_to(arc, DOWN)
self.add(label)

Attributes

AUTO

ROUND

BUTT

SQUARE


---

## LineJointType - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.constants.LineJointType.html

LineJointType¶

Qualified name: manim.constants.LineJointType

class LineJointType(*values)[source]¶
Bases: Enum

Collection of available line joint types.

See the example below for a visual illustration of the different
joint types.

Examples

Example: LineJointVariants ¶

from manim import *

class LineJointVariants(Scene):
def construct(self):
mob = VMobject(stroke_width=20, color=GREEN).set_points_as_corners([
np.array([-2, 0, 0]),
np.array([0, 0, 0]),
np.array([-2, 1, 0]),
])
lines = VGroup(*[mob.copy() for _ in range(len(LineJointType))])
for line, joint_type in zip(lines, LineJointType):
line.joint_type = joint_type

lines.arrange(RIGHT, buff=1)
self.add(lines)
for line in lines:
label = Text(line.joint_type.name).next_to(line, DOWN)
self.add(label)

class LineJointVariants(Scene):
def construct(self):
mob = VMobject(stroke_width=20, color=GREEN).set_points_as_corners([
np.array([-2, 0, 0]),
np.array([0, 0, 0]),
np.array([-2, 1, 0]),
])
lines = VGroup(*[mob.copy() for _ in range(len(LineJointType))])
for line, joint_type in zip(lines, LineJointType):
line.joint_type = joint_type

lines.arrange(RIGHT, buff=1)
self.add(lines)
for line in lines:
label = Text(line.joint_type.name).next_to(line, DOWN)
self.add(label)

Attributes

AUTO

ROUND

BEVEL

MITER


---

## QualityDict - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.constants.QualityDict.html

QualityDict¶

Qualified name: manim.constants.QualityDict

class QualityDict[source]¶
Bases: TypedDict

Methods

Attributes

flag

pixel_height

pixel_width

frame_rate


---

## RendererType - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.constants.RendererType.html

RendererType¶

Qualified name: manim.constants.RendererType

class RendererType(*values)[source]¶
Bases: Enum

An enumeration of all renderer types that can be assigned to
the config.renderer attribute.

Manim’s configuration allows assigning string values to the renderer
setting, the values are then replaced by the corresponding enum object.
In other words, you can run:

config.renderer = "opengl"

and checking the renderer afterwards reveals that the attribute has
assumed the value:

<RendererType.OPENGL: 'opengl'>

Attributes

CAIRO

A renderer based on the cairo backend.

OPENGL

An OpenGL-based renderer.

CAIRO = 'cairo'¶
A renderer based on the cairo backend.

OPENGL = 'opengl'¶
An OpenGL-based renderer.


---

## constants - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.constants.html

constants¶

Constant definitions.

Module Attributes

ORIGIN

The center of the coordinate system.

UP

One unit step in the positive Y direction.

DOWN

One unit step in the negative Y direction.

RIGHT

One unit step in the positive X direction.

LEFT

One unit step in the negative X direction.

IN

One unit step in the negative Z direction.

OUT

One unit step in the positive Z direction.

UL

One step up plus one step left.

UR

One step up plus one step right.

DL

One step down plus one step left.

DR

One step down plus one step right.

Classes

CapStyleType

Collection of available cap styles.

LineJointType

Collection of available line joint types.

QualityDict

RendererType

An enumeration of all renderer types that can be assigned to the config.renderer attribute.
