# Svg Brace


---

## ArcBrace - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.svg.brace.ArcBrace.html

ArcBrace¶

Qualified name: manim.mobject.svg.brace.ArcBrace

class ArcBrace(arc=None, direction=array([1., 0., 0.]), **kwargs)[source]¶
Bases: Brace

Creates a Brace that wraps around an Arc.

The direction parameter allows the brace to be applied
from outside or inside the arc.

Warning

The ArcBrace is smaller for arcs with smaller radii.

Note

The ArcBrace is initially a vertical Brace defined by the
length of the Arc, but is scaled down to match the start and end
angles. An exponential function is then applied after it is shifted based on
the radius of the arc.

The scaling effect is not applied for arcs with radii smaller than 1 to prevent
over-scaling.

Parameters:

arc (Arc | None) – The Arc that wraps around the Brace mobject.

direction (Vector3DLike) – The direction from which the brace faces the arc.
LEFT for inside the arc, and RIGHT for the outside.

kwargs (Any)

Example

Example: ArcBraceExample ¶

from manim import *

class ArcBraceExample(Scene):
def construct(self):
arc_1 = Arc(radius=1.5,start_angle=0,angle=2*PI/3).set_color(RED)
brace_1 = ArcBrace(arc_1,LEFT)
group_1 = VGroup(arc_1,brace_1)

arc_2 = Arc(radius=3,start_angle=0,angle=5*PI/6).set_color(YELLOW)
brace_2 = ArcBrace(arc_2)
group_2 = VGroup(arc_2,brace_2)

arc_3 = Arc(radius=0.5,start_angle=-0,angle=PI).set_color(BLUE)
brace_3 = ArcBrace(arc_3)
group_3 = VGroup(arc_3,brace_3)

arc_4 = Arc(radius=0.2,start_angle=0,angle=3*PI/2).set_color(GREEN)
brace_4 = ArcBrace(arc_4)
group_4 = VGroup(arc_4,brace_4)

arc_group = VGroup(group_1, group_2, group_3, group_4).arrange_in_grid(buff=1.5)
self.add(arc_group.center())

class ArcBraceExample(Scene):
def construct(self):
arc_1 = Arc(radius=1.5,start_angle=0,angle=2*PI/3).set_color(RED)
brace_1 = ArcBrace(arc_1,LEFT)
group_1 = VGroup(arc_1,brace_1)

arc_2 = Arc(radius=3,start_angle=0,angle=5*PI/6).set_color(YELLOW)
brace_2 = ArcBrace(arc_2)
group_2 = VGroup(arc_2,brace_2)

arc_3 = Arc(radius=0.5,start_angle=-0,angle=PI).set_color(BLUE)
brace_3 = ArcBrace(arc_3)
group_3 = VGroup(arc_3,brace_3)

arc_4 = Arc(radius=0.2,start_angle=0,angle=3*PI/2).set_color(GREEN)
brace_4 = ArcBrace(arc_4)
group_4 = VGroup(arc_4,brace_4)

arc_group = VGroup(group_1, group_2, group_3, group_4).arrange_in_grid(buff=1.5)
self.add(arc_group.center())

References: Arc

Methods

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

_original__init__(arc=None, direction=array([1., 0., 0.]), **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

arc (Arc | None)

direction (Vector3DLike)

kwargs (Any)


---

## Brace - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.svg.brace.Brace.html

Brace¶

Qualified name: manim.mobject.svg.brace.Brace

class Brace(mobject, direction=array([0., -1., 0.]), buff=0.2, sharpness=2, stroke_width=0, fill_opacity=1.0, background_stroke_width=0, background_stroke_color=ManimColor('#000000'), **kwargs)[source]¶
Bases: VMobjectFromSVGPath

Takes a mobject and draws a brace adjacent to it.

Passing a direction vector determines the direction from which the
brace is drawn. By default it is drawn from below.

Parameters:

mobject (Mobject) – The mobject adjacent to which the brace is placed.

direction (Vector3DLike) – The direction from which the brace faces the mobject.

buff (float)

sharpness (float)

stroke_width (float)

fill_opacity (float)

background_stroke_width (float)

background_stroke_color (ParsableManimColor)

kwargs (Any)

See also

BraceBetweenPoints

Examples

Example: BraceExample ¶

from manim import *

class BraceExample(Scene):
def construct(self):
s = Square()
self.add(s)
for i in np.linspace(0.1,1.0,4):
br = Brace(s, sharpness=i)
t = Text(f"sharpness= {i}").next_to(br, RIGHT)
self.add(t)
self.add(br)
VGroup(*self.mobjects).arrange(DOWN, buff=0.2)

class BraceExample(Scene):
def construct(self):
s = Square()
self.add(s)
for i in np.linspace(0.1,1.0,4):
br = Brace(s, sharpness=i)
t = Text(f"sharpness= {i}").next_to(br, RIGHT)
self.add(t)
self.add(br)
VGroup(*self.mobjects).arrange(DOWN, buff=0.2)

Methods

get_direction

Returns the direction from the center to the brace tip.

get_tex

Places the tex at the brace tip.

get_text

Places the text at the brace tip.

get_tip

Returns the point at the brace tip.

put_at_tip

Puts the given mobject at the brace tip.

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

_original__init__(mobject, direction=array([0., -1., 0.]), buff=0.2, sharpness=2, stroke_width=0, fill_opacity=1.0, background_stroke_width=0, background_stroke_color=ManimColor('#000000'), **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

direction (Vector3DLike)

buff (float)

sharpness (float)

stroke_width (float)

fill_opacity (float)

background_stroke_width (float)

background_stroke_color (ParsableManimColor)

kwargs (Any)

get_direction()[source]¶
Returns the direction from the center to the brace tip.

Return type:
Vector3D

get_tex(*tex, **kwargs)[source]¶
Places the tex at the brace tip.

Parameters:

tex (str) – The tex to be placed at the brace tip.

kwargs (Any) – Any further keyword arguments are passed to put_at_tip() which
is used to position the tex at the brace tip.

Return type:
MathTex

get_text(*text, **kwargs)[source]¶
Places the text at the brace tip.

Parameters:

text (str) – The text to be placed at the brace tip.

kwargs (Any) – Any additional keyword arguments are passed to put_at_tip() which
is used to position the text at the brace tip.

Return type:
Tex

get_tip()[source]¶
Returns the point at the brace tip.

Return type:
Point3D

put_at_tip(mob, use_next_to=True, **kwargs)[source]¶
Puts the given mobject at the brace tip.

Parameters:

mob (Mobject) – The mobject to be placed at the tip.

use_next_to (bool) – If true, then next_to() is used to place the mobject at the
tip.

kwargs (Any) – Any additional keyword arguments are passed to next_to() which
is used to put the mobject next to the brace tip.

Return type:
Self


---

## BraceBetweenPoints - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.svg.brace.BraceBetweenPoints.html

BraceBetweenPoints¶

Qualified name: manim.mobject.svg.brace.BraceBetweenPoints

class BraceBetweenPoints(point_1, point_2, direction=array([0., 0., 0.]), **kwargs)[source]¶
Bases: Brace

Similar to Brace, but instead of taking a mobject it uses 2
points to place the brace.

A fitting direction for the brace is
computed, but it still can be manually overridden.
If the points go from left to right, the brace is drawn from below.
Swapping the points places the brace on the opposite side.

Parameters:

point_1 (Point3DLike) – The first point.

point_2 (Point3DLike) – The second point.

direction (Vector3DLike) – The direction from which the brace faces towards the points.

kwargs (Any)

Examples

Example: BraceBPExample ¶

from manim import *

class BraceBPExample(Scene):
def construct(self):
p1 = [0,0,0]
p2 = [1,2,0]
brace = BraceBetweenPoints(p1,p2)
self.play(Create(NumberPlane()))
self.play(Create(brace))
self.wait(2)

class BraceBPExample(Scene):
def construct(self):
p1 = [0,0,0]
p2 = [1,2,0]
brace = BraceBetweenPoints(p1,p2)
self.play(Create(NumberPlane()))
self.play(Create(brace))
self.wait(2)

Methods

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

_original__init__(point_1, point_2, direction=array([0., 0., 0.]), **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

point_1 (Point3DLike)

point_2 (Point3DLike)

direction (Vector3DLike)

kwargs (Any)


---

## BraceLabel - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.svg.brace.BraceLabel.html

BraceLabel¶

Qualified name: manim.mobject.svg.brace.BraceLabel

class BraceLabel(obj, text, brace_direction=array([ 0., -1., 0.]), label_constructor=<class 'manim.mobject.text.tex_mobject.MathTex'>, font_size=48, buff=0.2, brace_config=None, **kwargs)[source]¶
Bases: VMobject

Create a brace with a label attached.

Parameters:

obj (Mobject) – The mobject adjacent to which the brace is placed.

text (str) – The label text.

brace_direction (Vector3DLike) – The direction of the brace. By default DOWN.

label_constructor (type[SingleStringMathTex | Text]) – A class or function used to construct a mobject representing
the label. By default MathTex.

font_size (float) – The font size of the label, passed to the label_constructor.

buff (float) – The buffer between the mobject and the brace.

brace_config (dict[str, Any] | None) – Arguments to be passed to Brace.

kwargs (Any) – Additional arguments to be passed to VMobject.

Methods

change_brace_label

change_label

creation_anim

shift_brace

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

_original__init__(obj, text, brace_direction=array([ 0., -1., 0.]), label_constructor=<class 'manim.mobject.text.tex_mobject.MathTex'>, font_size=48, buff=0.2, brace_config=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

obj (Mobject)

text (str)

brace_direction (Vector3DLike)

label_constructor (type[SingleStringMathTex | Text])

font_size (float)

buff (float)

brace_config (dict[str, Any] | None)

kwargs (Any)


---

## BraceText - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.svg.brace.BraceText.html

BraceText¶

Qualified name: manim.mobject.svg.brace.BraceText

class BraceText(obj, text, label_constructor=<class 'manim.mobject.text.text_mobject.Text'>, **kwargs)[source]¶
Bases: BraceLabel

Create a brace with a text label attached.

Parameters:

obj (Mobject) – The mobject adjacent to which the brace is placed.

text (str) – The label text.

brace_direction – The direction of the brace. By default DOWN.

label_constructor (type[SingleStringMathTex | Text]) – A class or function used to construct a mobject representing
the label. By default Text.

font_size – The font size of the label, passed to the label_constructor.

buff – The buffer between the mobject and the brace.

brace_config – Arguments to be passed to Brace.

kwargs (Any) – Additional arguments to be passed to VMobject.

Examples

Example: BraceTextExample ¶

from manim import *

class BraceTextExample(Scene):
def construct(self):
s1 = Square().move_to(2*LEFT)
self.add(s1)
br1 = BraceText(s1, "Label")
self.add(br1)

s2 = Square().move_to(2*RIGHT)
self.add(s2)
br2 = BraceText(s2, "Label")

br2.change_label("new")
self.add(br2)
self.wait(0.1)

class BraceTextExample(Scene):
def construct(self):
s1 = Square().move_to(2*LEFT)
self.add(s1)
br1 = BraceText(s1, "Label")
self.add(br1)

s2 = Square().move_to(2*RIGHT)
self.add(s2)
br2 = BraceText(s2, "Label")

br2.change_label("new")
self.add(br2)
self.wait(0.1)

Methods

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

_original__init__(obj, text, label_constructor=<class 'manim.mobject.text.text_mobject.Text'>, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

obj (Mobject)

text (str)

label_constructor (type[SingleStringMathTex | Text])

kwargs (Any)


---

## brace - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.svg.brace.html

brace¶

Mobject representing curly braces.

Classes

ArcBrace

Creates a Brace that wraps around an Arc.

Brace

Takes a mobject and draws a brace adjacent to it.

BraceBetweenPoints

Similar to Brace, but instead of taking a mobject it uses 2 points to place the brace.

BraceLabel

Create a brace with a label attached.

BraceText

Create a brace with a text label attached.
