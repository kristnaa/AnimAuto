# Geometry Arc


---

## AnnotationDot - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.AnnotationDot.html

AnnotationDot¶

Qualified name: manim.mobject.geometry.arc.AnnotationDot

class AnnotationDot(radius=0.10400000000000001, stroke_width=5, stroke_color=ManimColor('#FFFFFF'), fill_color=ManimColor('#58C4DD'), **kwargs)[source]¶
Bases: Dot

A dot with bigger radius and bold stroke to annotate scenes.

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

Parameters:

radius (float)

stroke_width (float)

stroke_color (ParsableManimColor)

fill_color (ParsableManimColor)

kwargs (Any)

_original__init__(radius=0.10400000000000001, stroke_width=5, stroke_color=ManimColor('#FFFFFF'), fill_color=ManimColor('#58C4DD'), **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

radius (float)

stroke_width (float)

stroke_color (ParsableManimColor)

fill_color (ParsableManimColor)

kwargs (Any)

Return type:
None


---

## AnnularSector - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.AnnularSector.html

AnnularSector¶

Qualified name: manim.mobject.geometry.arc.AnnularSector

class AnnularSector(inner_radius=1, outer_radius=2, angle=1.5707963267948966, start_angle=0, fill_opacity=1, stroke_width=0, color=ManimColor('#FFFFFF'), **kwargs)[source]¶
Bases: Arc

A sector of an annulus.

Parameters:

inner_radius (float) – The inside radius of the Annular Sector.

outer_radius (float) – The outside radius of the Annular Sector.

angle (float) – The clockwise angle of the Annular Sector.

start_angle (float) – The starting clockwise angle of the Annular Sector.

fill_opacity (float) – The opacity of the color filled in the Annular Sector.

stroke_width (float) – The stroke width of the Annular Sector.

color (ManimColor) – The color filled into the Annular Sector.

kwargs (Any)

Examples

Example: AnnularSectorExample ¶

from manim import *

class AnnularSectorExample(Scene):
def construct(self):
# Changes background color to clearly visualize changes in fill_opacity.
self.camera.background_color = WHITE

# The default parameter start_angle is 0, so the AnnularSector starts from the +x-axis.
s1 = AnnularSector(color=YELLOW).move_to(2 * UL)

# Different inner_radius and outer_radius than the default.
s2 = AnnularSector(inner_radius=1.5, outer_radius=2, angle=45 * DEGREES, color=RED).move_to(2 * UR)

# fill_opacity is typically a number > 0 and <= 1. If fill_opacity=0, the AnnularSector is transparent.
s3 = AnnularSector(inner_radius=1, outer_radius=1.5, angle=PI, fill_opacity=0.25, color=BLUE).move_to(2 * DL)

# With a negative value for the angle, the AnnularSector is drawn clockwise from the start value.
s4 = AnnularSector(inner_radius=1, outer_radius=1.5, angle=-3 * PI / 2, color=GREEN).move_to(2 * DR)

self.add(s1, s2, s3, s4)

class AnnularSectorExample(Scene):
def construct(self):
# Changes background color to clearly visualize changes in fill_opacity.
self.camera.background_color = WHITE

# The default parameter start_angle is 0, so the AnnularSector starts from the +x-axis.
s1 = AnnularSector(color=YELLOW).move_to(2 * UL)

# Different inner_radius and outer_radius than the default.
s2 = AnnularSector(inner_radius=1.5, outer_radius=2, angle=45 * DEGREES, color=RED).move_to(2 * UR)

# fill_opacity is typically a number > 0 and Methods

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

_original__init__(inner_radius=1, outer_radius=2, angle=1.5707963267948966, start_angle=0, fill_opacity=1, stroke_width=0, color=ManimColor('#FFFFFF'), **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

inner_radius (float)

outer_radius (float)

angle (float)

start_angle (float)

fill_opacity (float)

stroke_width (float)

color (ParsableManimColor)

kwargs (Any)

Return type:
None

generate_points()[source]¶
Initializes points and therefore the shape.

Gets called upon creation. This is an empty method that can be implemented by
subclasses.

Return type:
None


---

## Annulus - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.Annulus.html

Annulus¶

Qualified name: manim.mobject.geometry.arc.Annulus

class Annulus(inner_radius=1, outer_radius=2, fill_opacity=1, stroke_width=0, color=ManimColor('#FFFFFF'), mark_paths_closed=False, **kwargs)[source]¶
Bases: Circle

Region between two concentric Circles.

Parameters:

inner_radius (float) – The radius of the inner Circle.

outer_radius (float) – The radius of the outer Circle.

kwargs (Any) – Additional arguments to be passed to Annulus

fill_opacity (float)

stroke_width (float)

color (ParsableManimColor)

mark_paths_closed (bool)

Examples

Example: AnnulusExample ¶

from manim import *

class AnnulusExample(Scene):
def construct(self):
annulus_1 = Annulus(inner_radius=0.5, outer_radius=1).shift(UP)
annulus_2 = Annulus(inner_radius=0.3, outer_radius=0.6, color=RED).next_to(annulus_1, DOWN)
self.add(annulus_1, annulus_2)

class AnnulusExample(Scene):
def construct(self):
annulus_1 = Annulus(inner_radius=0.5, outer_radius=1).shift(UP)
annulus_2 = Annulus(inner_radius=0.3, outer_radius=0.6, color=RED).next_to(annulus_1, DOWN)
self.add(annulus_1, annulus_2)

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

_original__init__(inner_radius=1, outer_radius=2, fill_opacity=1, stroke_width=0, color=ManimColor('#FFFFFF'), mark_paths_closed=False, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

inner_radius (float)

outer_radius (float)

fill_opacity (float)

stroke_width (float)

color (ParsableManimColor)

mark_paths_closed (bool)

kwargs (Any)

Return type:
None

generate_points()[source]¶
Initializes points and therefore the shape.

Gets called upon creation. This is an empty method that can be implemented by
subclasses.

Return type:
None


---

## Arc - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.Arc.html

Arc¶

Qualified name: manim.mobject.geometry.arc.Arc

class Arc(radius=1.0, start_angle=0, angle=1.5707963267948966, num_components=9, arc_center=array([0., 0., 0.]), **kwargs)[source]¶
Bases: TipableVMobject

A circular arc.

Examples

A simple arc of angle Pi.

Example: ArcExample ¶

from manim import *

class ArcExample(Scene):
def construct(self):
self.add(Arc(angle=PI))

class ArcExample(Scene):
def construct(self):
self.add(Arc(angle=PI))

Methods

generate_points

Initializes points and therefore the shape.

get_arc_center

Looks at the normals to the first two anchors, and finds their intersection points

init_points

move_arc_center_to

stop_angle

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

radius (float | None)

start_angle (float)

angle (float)

num_components (int)

arc_center (Point3DLike)

kwargs (Any)

_original__init__(radius=1.0, start_angle=0, angle=1.5707963267948966, num_components=9, arc_center=array([0., 0., 0.]), **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

radius (float | None)

start_angle (float)

angle (float)

num_components (int)

arc_center (Point3DLike)

kwargs (Any)

generate_points()[source]¶
Initializes points and therefore the shape.

Gets called upon creation. This is an empty method that can be implemented by
subclasses.

Return type:
None

get_arc_center(warning=True)[source]¶
Looks at the normals to the first two
anchors, and finds their intersection points

Parameters:
warning (bool)

Return type:
Point3D


---

## ArcBetweenPoints - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.ArcBetweenPoints.html

ArcBetweenPoints¶

Qualified name: manim.mobject.geometry.arc.ArcBetweenPoints

class ArcBetweenPoints(start, end, angle=1.5707963267948966, radius=None, **kwargs)[source]¶
Bases: Arc

Inherits from Arc and additionally takes 2 points between which the arc is spanned.

Example

Example: ArcBetweenPointsExample ¶

from manim import *

class ArcBetweenPointsExample(Scene):
def construct(self):
circle = Circle(radius=2, stroke_color=GREY)
dot_1 = Dot(color=GREEN).move_to([2, 0, 0]).scale(0.5)
dot_1_text = Tex("(2,0)").scale(0.5).next_to(dot_1, RIGHT).set_color(BLUE)
dot_2 = Dot(color=GREEN).move_to([0, 2, 0]).scale(0.5)
dot_2_text = Tex("(0,2)").scale(0.5).next_to(dot_2, UP).set_color(BLUE)
arc= ArcBetweenPoints(start=2 * RIGHT, end=2 * UP, stroke_color=YELLOW)
self.add(circle, dot_1, dot_2, dot_1_text, dot_2_text)
self.play(Create(arc))

class ArcBetweenPointsExample(Scene):
def construct(self):
circle = Circle(radius=2, stroke_color=GREY)
dot_1 = Dot(color=GREEN).move_to([2, 0, 0]).scale(0.5)
dot_1_text = Tex("(2,0)").scale(0.5).next_to(dot_1, RIGHT).set_color(BLUE)
dot_2 = Dot(color=GREEN).move_to([0, 2, 0]).scale(0.5)
dot_2_text = Tex("(0,2)").scale(0.5).next_to(dot_2, UP).set_color(BLUE)
arc= ArcBetweenPoints(start=2 * RIGHT, end=2 * UP, stroke_color=YELLOW)
self.add(circle, dot_1, dot_2, dot_1_text, dot_2_text)
self.play(Create(arc))

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

Parameters:

start (Point3DLike)

end (Point3DLike)

angle (float)

radius (float | None)

kwargs (Any)

_original__init__(start, end, angle=1.5707963267948966, radius=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

start (Point3DLike)

end (Point3DLike)

angle (float)

radius (float | None)

kwargs (Any)

Return type:
None


---

## ArcPolygon - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.ArcPolygon.html

ArcPolygon¶

Qualified name: manim.mobject.geometry.arc.ArcPolygon

class ArcPolygon(*vertices, angle=0.7853981633974483, radius=None, arc_config=None, **kwargs)[source]¶
Bases: VMobject

A generalized polygon allowing for points to be connected with arcs.

This version tries to stick close to the way Polygon is used. Points
can be passed to it directly which are used to generate the according arcs
(using ArcBetweenPoints). An angle or radius can be passed to it to
use across all arcs, but to configure arcs individually an arc_config list
has to be passed with the syntax explained below.

Parameters:

vertices (Point3DLike) – A list of vertices, start and end points for the arc segments.

angle (float) – The angle used for constructing the arcs. If no other parameters
are set, this angle is used to construct all arcs.

radius (float | None) – The circle radius used to construct the arcs. If specified,
overrides the specified angle.

arc_config (list[dict] | None) – When passing a dict, its content will be passed as keyword
arguments to ArcBetweenPoints. Otherwise, a list
of dictionaries containing values that are passed as keyword
arguments for every individual arc can be passed.

kwargs (Any) – Further keyword arguments that are passed to the constructor of
VMobject.

arcs¶
The arcs created from the input parameters:

>>> from manim import ArcPolygon
>>> ap = ArcPolygon([0, 0, 0], [2, 0, 0], [0, 2, 0])
>>> ap.arcs
[ArcBetweenPoints, ArcBetweenPoints, ArcBetweenPoints]

Type:
list

Tip

Two instances of ArcPolygon can be transformed properly into one
another as well. Be advised that any arc initialized with angle=0
will actually be a straight line, so if a straight section should seamlessly
transform into an arced section or vice versa, initialize the straight section
with a negligible angle instead (such as angle=0.0001).

Note

There is an alternative version (ArcPolygonFromArcs) that is instantiated
with pre-defined arcs.

See also

ArcPolygonFromArcs

Examples

Example: SeveralArcPolygons ¶

from manim import *

class SeveralArcPolygons(Scene):
def construct(self):
a = [0, 0, 0]
b = [2, 0, 0]
c = [0, 2, 0]
ap1 = ArcPolygon(a, b, c, radius=2)
ap2 = ArcPolygon(a, b, c, angle=45*DEGREES)
ap3 = ArcPolygon(a, b, c, arc_config={'radius': 1.7, 'color': RED})
ap4 = ArcPolygon(a, b, c, color=RED, fill_opacity=1,
arc_config=[{'radius': 1.7, 'color': RED},
{'angle': 20*DEGREES, 'color': BLUE},
{'radius': 1}])
ap_group = VGroup(ap1, ap2, ap3, ap4).arrange()
self.play(*[Create(ap) for ap in [ap1, ap2, ap3, ap4]])
self.wait()

class SeveralArcPolygons(Scene):
def construct(self):
a = [0, 0, 0]
b = [2, 0, 0]
c = [0, 2, 0]
ap1 = ArcPolygon(a, b, c, radius=2)
ap2 = ArcPolygon(a, b, c, angle=45*DEGREES)
ap3 = ArcPolygon(a, b, c, arc_config={'radius': 1.7, 'color': RED})
ap4 = ArcPolygon(a, b, c, color=RED, fill_opacity=1,
arc_config=[{'radius': 1.7, 'color': RED},
{'angle': 20*DEGREES, 'color': BLUE},
{'radius': 1}])
ap_group = VGroup(ap1, ap2, ap3, ap4).arrange()
self.play(*[Create(ap) for ap in [ap1, ap2, ap3, ap4]])
self.wait()

For further examples see ArcPolygonFromArcs.

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

_original__init__(*vertices, angle=0.7853981633974483, radius=None, arc_config=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

vertices (Point3DLike)

angle (float)

radius (float | None)

arc_config (list[dict] | None)

kwargs (Any)

Return type:
None


---

## ArcPolygonFromArcs - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.ArcPolygonFromArcs.html

ArcPolygonFromArcs¶

Qualified name: manim.mobject.geometry.arc.ArcPolygonFromArcs

class ArcPolygonFromArcs(*arcs, **kwargs)[source]¶
Bases: VMobject

A generalized polygon allowing for points to be connected with arcs.

This version takes in pre-defined arcs to generate the arcpolygon and introduces
little new syntax. However unlike Polygon it can’t be created with points
directly.

For proper appearance the passed arcs should connect seamlessly:
[a,b][b,c][c,a]

If there are any gaps between the arcs, those will be filled in
with straight lines, which can be used deliberately for any straight
sections. Arcs can also be passed as straight lines such as an arc
initialized with angle=0.

Parameters:

arcs (Arc | ArcBetweenPoints) – These are the arcs from which the arcpolygon is assembled.

kwargs (Any) – Keyword arguments that are passed to the constructor of
VMobject. Affects how the ArcPolygon itself is drawn,
but doesn’t affect passed arcs.

arcs¶
The arcs used to initialize the ArcPolygonFromArcs:

>>> from manim import ArcPolygonFromArcs, Arc, ArcBetweenPoints
>>> ap = ArcPolygonFromArcs(Arc(), ArcBetweenPoints([1,0,0], [0,1,0]), Arc())
>>> ap.arcs
[Arc, ArcBetweenPoints, Arc]

Tip

Two instances of ArcPolygon can be transformed properly into
one another as well. Be advised that any arc initialized with angle=0
will actually be a straight line, so if a straight section should seamlessly
transform into an arced section or vice versa, initialize the straight
section with a negligible angle instead (such as angle=0.0001).

Note

There is an alternative version (ArcPolygon) that can be instantiated
with points.

See also

ArcPolygon

Examples

One example of an arcpolygon is the Reuleaux triangle.
Instead of 3 straight lines connecting the outer points,
a Reuleaux triangle has 3 arcs connecting those points,
making a shape with constant width.

Passed arcs are stored as submobjects in the arcpolygon.
This means that the arcs are changed along with the arcpolygon,
for example when it’s shifted, and these arcs can be manipulated
after the arcpolygon has been initialized.

Also both the arcs contained in an ArcPolygonFromArcs, as well as the
arcpolygon itself are drawn, which affects draw time in Create
for example. In most cases the arcs themselves don’t
need to be drawn, in which case they can be passed as invisible.

Example: ArcPolygonExample ¶

from manim import *

class ArcPolygonExample(Scene):
def construct(self):
arc_conf = {"stroke_width": 0}
poly_conf = {"stroke_width": 10, "stroke_color": BLUE,
"fill_opacity": 1, "color": PURPLE}
a = [-1, 0, 0]
b = [1, 0, 0]
c = [0, np.sqrt(3), 0]
arc0 = ArcBetweenPoints(a, b, radius=2, **arc_conf)
arc1 = ArcBetweenPoints(b, c, radius=2, **arc_conf)
arc2 = ArcBetweenPoints(c, a, radius=2, **arc_conf)
reuleaux_tri = ArcPolygonFromArcs(arc0, arc1, arc2, **poly_conf)
self.play(FadeIn(reuleaux_tri))
self.wait(2)

class ArcPolygonExample(Scene):
def construct(self):
arc_conf = {"stroke_width": 0}
poly_conf = {"stroke_width": 10, "stroke_color": BLUE,
"fill_opacity": 1, "color": PURPLE}
a = [-1, 0, 0]
b = [1, 0, 0]
c = [0, np.sqrt(3), 0]
arc0 = ArcBetweenPoints(a, b, radius=2, **arc_conf)
arc1 = ArcBetweenPoints(b, c, radius=2, **arc_conf)
arc2 = ArcBetweenPoints(c, a, radius=2, **arc_conf)
reuleaux_tri = ArcPolygonFromArcs(arc0, arc1, arc2, **poly_conf)
self.play(FadeIn(reuleaux_tri))
self.wait(2)

The arcpolygon itself can also be hidden so that instead only the contained
arcs are drawn. This can be used to easily debug arcs or to highlight them.

Example: ArcPolygonExample2 ¶

from manim import *

class ArcPolygonExample2(Scene):
def construct(self):
arc_conf = {"stroke_width": 3, "stroke_color": BLUE,
"fill_opacity": 0.5, "color": GREEN}
poly_conf = {"color": None}
a = [-1, 0, 0]
b = [1, 0, 0]
c = [0, np.sqrt(3), 0]
arc0 = ArcBetweenPoints(a, b, radius=2, **arc_conf)
arc1 = ArcBetweenPoints(b, c, radius=2, **arc_conf)
arc2 = ArcBetweenPoints(c, a, radius=2, stroke_color=RED)
reuleaux_tri = ArcPolygonFromArcs(arc0, arc1, arc2, **poly_conf)
self.play(FadeIn(reuleaux_tri))
self.wait(2)

class ArcPolygonExample2(Scene):
def construct(self):
arc_conf = {"stroke_width": 3, "stroke_color": BLUE,
"fill_opacity": 0.5, "color": GREEN}
poly_conf = {"color": None}
a = [-1, 0, 0]
b = [1, 0, 0]
c = [0, np.sqrt(3), 0]
arc0 = ArcBetweenPoints(a, b, radius=2, **arc_conf)
arc1 = ArcBetweenPoints(b, c, radius=2, **arc_conf)
arc2 = ArcBetweenPoints(c, a, radius=2, stroke_color=RED)
reuleaux_tri = ArcPolygonFromArcs(arc0, arc1, arc2, **poly_conf)
self.play(FadeIn(reuleaux_tri))
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

_original__init__(*arcs, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

arcs (Arc | ArcBetweenPoints)

kwargs (Any)

Return type:
None


---

## Circle - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.Circle.html

Circle¶

Qualified name: manim.mobject.geometry.arc.Circle

class Circle(radius=None, color=ManimColor('#FC6255'), **kwargs)[source]¶
Bases: Arc

A circle.

Parameters:

color (ManimColor) – The color of the shape.

kwargs (Any) – Additional arguments to be passed to Arc

radius (float | None)

Examples

Example: CircleExample ¶

from manim import *

class CircleExample(Scene):
def construct(self):
circle_1 = Circle(radius=1.0)
circle_2 = Circle(radius=1.5, color=GREEN)
circle_3 = Circle(radius=1.0, color=BLUE_B, fill_opacity=1)

circle_group = Group(circle_1, circle_2, circle_3).arrange(buff=1)
self.add(circle_group)

class CircleExample(Scene):
def construct(self):
circle_1 = Circle(radius=1.0)
circle_2 = Circle(radius=1.5, color=GREEN)
circle_3 = Circle(radius=1.0, color=BLUE_B, fill_opacity=1)

circle_group = Group(circle_1, circle_2, circle_3).arrange(buff=1)
self.add(circle_group)

Methods

from_three_points

Returns a circle passing through the specified three points.

point_at_angle

Returns the position of a point on the circle.

surround

Modifies a circle so that it surrounds a given mobject.

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

_original__init__(radius=None, color=ManimColor('#FC6255'), **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

radius (float | None)

color (ParsableManimColor)

kwargs (Any)

Return type:
None

static from_three_points(p1, p2, p3, **kwargs)[source]¶
Returns a circle passing through the specified
three points.

Example

Example: CircleFromPointsExample ¶

from manim import *

class CircleFromPointsExample(Scene):
def construct(self):
circle = Circle.from_three_points(LEFT, LEFT + UP, UP * 2, color=RED)
dots = VGroup(
Dot(LEFT),
Dot(LEFT + UP),
Dot(UP * 2),
)
self.add(NumberPlane(), circle, dots)

class CircleFromPointsExample(Scene):
def construct(self):
circle = Circle.from_three_points(LEFT, LEFT + UP, UP * 2, color=RED)
dots = VGroup(
Dot(LEFT),
Dot(LEFT + UP),
Dot(UP * 2),
)
self.add(NumberPlane(), circle, dots)

Parameters:

p1 (Point3DLike)

p2 (Point3DLike)

p3 (Point3DLike)

kwargs (Any)

Return type:
Circle

point_at_angle(angle)[source]¶
Returns the position of a point on the circle.

Parameters:
angle (float) – The angle of the point along the circle in radians.

Returns:
The location of the point along the circle’s circumference.

Return type:
numpy.ndarray

Examples

Example: PointAtAngleExample ¶

from manim import *

class PointAtAngleExample(Scene):
def construct(self):
circle = Circle(radius=2.0)
p1 = circle.point_at_angle(PI/2)
p2 = circle.point_at_angle(270*DEGREES)

s1 = Square(side_length=0.25).move_to(p1)
s2 = Square(side_length=0.25).move_to(p2)
self.add(circle, s1, s2)

class PointAtAngleExample(Scene):
def construct(self):
circle = Circle(radius=2.0)
p1 = circle.point_at_angle(PI/2)
p2 = circle.point_at_angle(270*DEGREES)

s1 = Square(side_length=0.25).move_to(p1)
s2 = Square(side_length=0.25).move_to(p2)
self.add(circle, s1, s2)

surround(mobject, dim_to_match=0, stretch=False, buffer_factor=1.2)[source]¶
Modifies a circle so that it surrounds a given mobject.

Parameters:

mobject (Mobject) – The mobject that the circle will be surrounding.

dim_to_match (int)

buffer_factor (float) – Scales the circle with respect to the mobject. A buffer_factor < 1 makes the circle smaller than the mobject.

stretch (bool) – Stretches the circle to fit more tightly around the mobject. Note: Does not work with Line

Return type:
Self

Examples

Example: CircleSurround ¶

from manim import *

class CircleSurround(Scene):
def construct(self):
triangle1 = Triangle()
circle1 = Circle().surround(triangle1)
group1 = Group(triangle1,circle1) # treat the two mobjects as one

line2 = Line()
circle2 = Circle().surround(line2, buffer_factor=2.0)
group2 = Group(line2,circle2)

# buffer_factor < 1, so the circle is smaller than the square
square3 = Square()
circle3 = Circle().surround(square3, buffer_factor=0.5)
group3 = Group(square3, circle3)

group = Group(group1, group2, group3).arrange(buff=1)
self.add(group)

class CircleSurround(Scene):
def construct(self):
triangle1 = Triangle()
circle1 = Circle().surround(triangle1)
group1 = Group(triangle1,circle1) # treat the two mobjects as one

line2 = Line()
circle2 = Circle().surround(line2, buffer_factor=2.0)
group2 = Group(line2,circle2)

# buffer_factor


---

## CubicBezier - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.CubicBezier.html

CubicBezier¶

Qualified name: manim.mobject.geometry.arc.CubicBezier

class CubicBezier(start_anchor, start_handle, end_handle, end_anchor, **kwargs)[source]¶
Bases: VMobject

A cubic Bézier curve.

Example

Example: BezierSplineExample ¶

from manim import *

class BezierSplineExample(Scene):
def construct(self):
p1 = np.array([-3, 1, 0])
p1b = p1 + [1, 0, 0]
d1 = Dot(point=p1).set_color(BLUE)
l1 = Line(p1, p1b)
p2 = np.array([3, -1, 0])
p2b = p2 - [1, 0, 0]
d2 = Dot(point=p2).set_color(RED)
l2 = Line(p2, p2b)
bezier = CubicBezier(p1b, p1b + 3 * RIGHT, p2b - 3 * RIGHT, p2b)
self.add(l1, d1, l2, d2, bezier)

class BezierSplineExample(Scene):
def construct(self):
p1 = np.array([-3, 1, 0])
p1b = p1 + [1, 0, 0]
d1 = Dot(point=p1).set_color(BLUE)
l1 = Line(p1, p1b)
p2 = np.array([3, -1, 0])
p2b = p2 - [1, 0, 0]
d2 = Dot(point=p2).set_color(RED)
l2 = Line(p2, p2b)
bezier = CubicBezier(p1b, p1b + 3 * RIGHT, p2b - 3 * RIGHT, p2b)
self.add(l1, d1, l2, d2, bezier)

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

Parameters:

start_anchor (Point3DLike)

start_handle (Point3DLike)

end_handle (Point3DLike)

end_anchor (Point3DLike)

kwargs (Any)

_original__init__(start_anchor, start_handle, end_handle, end_anchor, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

start_anchor (Point3DLike)

start_handle (Point3DLike)

end_handle (Point3DLike)

end_anchor (Point3DLike)

kwargs (Any)

Return type:
None


---

## CurvedArrow - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.CurvedArrow.html

CurvedArrow¶

Qualified name: manim.mobject.geometry.arc.CurvedArrow

class CurvedArrow(start_point, end_point, **kwargs)[source]¶
Bases: ArcBetweenPoints

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

Parameters:

start_point (Point3DLike)

end_point (Point3DLike)

kwargs (Any)

_original__init__(start_point, end_point, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

start_point (Point3DLike)

end_point (Point3DLike)

kwargs (Any)

Return type:
None


---

## CurvedDoubleArrow - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.CurvedDoubleArrow.html

CurvedDoubleArrow¶

Qualified name: manim.mobject.geometry.arc.CurvedDoubleArrow

class CurvedDoubleArrow(start_point, end_point, **kwargs)[source]¶
Bases: CurvedArrow

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

Parameters:

start_point (Point3DLike)

end_point (Point3DLike)

kwargs (Any)

_original__init__(start_point, end_point, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

start_point (Point3DLike)

end_point (Point3DLike)

kwargs (Any)

Return type:
None


---

## Dot - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.Dot.html

Dot¶

Qualified name: manim.mobject.geometry.arc.Dot

class Dot(point=array([0., 0., 0.]), radius=0.08, stroke_width=0, fill_opacity=1.0, color=ManimColor('#FFFFFF'), **kwargs)[source]¶
Bases: Circle

A circle with a very small radius.

Parameters:

point (Point3DLike) – The location of the dot.

radius (float) – The radius of the dot.

stroke_width (float) – The thickness of the outline of the dot.

fill_opacity (float) – The opacity of the dot’s fill_colour

color (ManimColor) – The color of the dot.

kwargs (Any) – Additional arguments to be passed to Circle

Examples

Example: DotExample ¶

from manim import *

class DotExample(Scene):
def construct(self):
dot1 = Dot(point=LEFT, radius=0.08)
dot2 = Dot(point=ORIGIN)
dot3 = Dot(point=RIGHT)
self.add(dot1,dot2,dot3)

class DotExample(Scene):
def construct(self):
dot1 = Dot(point=LEFT, radius=0.08)
dot2 = Dot(point=ORIGIN)
dot3 = Dot(point=RIGHT)
self.add(dot1,dot2,dot3)

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

_original__init__(point=array([0., 0., 0.]), radius=0.08, stroke_width=0, fill_opacity=1.0, color=ManimColor('#FFFFFF'), **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

point (Point3DLike)

radius (float)

stroke_width (float)

fill_opacity (float)

color (ParsableManimColor)

kwargs (Any)

Return type:
None


---

## Ellipse - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.Ellipse.html

Ellipse¶

Qualified name: manim.mobject.geometry.arc.Ellipse

class Ellipse(width=2, height=1, **kwargs)[source]¶
Bases: Circle

A circular shape; oval, circle.

Parameters:

width (float) – The horizontal width of the ellipse.

height (float) – The vertical height of the ellipse.

kwargs (Any) – Additional arguments to be passed to Circle.

Examples

Example: EllipseExample ¶

from manim import *

class EllipseExample(Scene):
def construct(self):
ellipse_1 = Ellipse(width=2.0, height=4.0, color=BLUE_B)
ellipse_2 = Ellipse(width=4.0, height=1.0, color=BLUE_D)
ellipse_group = Group(ellipse_1,ellipse_2).arrange(buff=1)
self.add(ellipse_group)

class EllipseExample(Scene):
def construct(self):
ellipse_1 = Ellipse(width=2.0, height=4.0, color=BLUE_B)
ellipse_2 = Ellipse(width=4.0, height=1.0, color=BLUE_D)
ellipse_group = Group(ellipse_1,ellipse_2).arrange(buff=1)
self.add(ellipse_group)

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

_original__init__(width=2, height=1, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

width (float)

height (float)

kwargs (Any)

Return type:
None


---

## LabeledDot - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.LabeledDot.html

LabeledDot¶

Qualified name: manim.mobject.geometry.arc.LabeledDot

class LabeledDot(label, radius=None, buff=0.1, **kwargs)[source]¶
Bases: Dot

A Dot containing a label in its center.

Parameters:

label (str | SingleStringMathTex | Text | Tex) – The label of the Dot. This is rendered as MathTex
by default (i.e., when passing a str), but other classes
representing rendered strings like Text or Tex
can be passed as well.

radius (float | None) – The radius of the Dot. If provided, the buff is ignored.
If None (the default), the radius is calculated based on the size
of the label and the buff.

buff (float)

kwargs (Any)

Examples

Example: SeveralLabeledDots ¶

from manim import *

class SeveralLabeledDots(Scene):
def construct(self):
sq = Square(fill_color=RED, fill_opacity=1)
self.add(sq)
dot1 = LabeledDot(Tex("42", color=RED))
dot2 = LabeledDot(MathTex("a", color=GREEN))
dot3 = LabeledDot(Text("ii", color=BLUE))
dot4 = LabeledDot("3")
dot1.next_to(sq, UL)
dot2.next_to(sq, UR)
dot3.next_to(sq, DL)
dot4.next_to(sq, DR)
self.add(dot1, dot2, dot3, dot4)

class SeveralLabeledDots(Scene):
def construct(self):
sq = Square(fill_color=RED, fill_opacity=1)
self.add(sq)
dot1 = LabeledDot(Tex("42", color=RED))
dot2 = LabeledDot(MathTex("a", color=GREEN))
dot3 = LabeledDot(Text("ii", color=BLUE))
dot4 = LabeledDot("3")
dot1.next_to(sq, UL)
dot2.next_to(sq, UR)
dot3.next_to(sq, DL)
dot4.next_to(sq, DR)
self.add(dot1, dot2, dot3, dot4)

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

_original__init__(label, radius=None, buff=0.1, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

label (str | SingleStringMathTex | Text | Tex)

radius (float | None)

buff (float)

kwargs (Any)

Return type:
None


---

## Sector - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.Sector.html

Sector¶

Qualified name: manim.mobject.geometry.arc.Sector

class Sector(radius=1, **kwargs)[source]¶
Bases: AnnularSector

A sector of a circle.

Examples

Example: ExampleSector ¶

from manim import *

class ExampleSector(Scene):
def construct(self):
sector = Sector(radius=2)
sector2 = Sector(radius=2.5, angle=60*DEGREES).move_to([-3, 0, 0])
sector.set_color(RED)
sector2.set_color(PINK)
self.add(sector, sector2)

class ExampleSector(Scene):
def construct(self):
sector = Sector(radius=2)
sector2 = Sector(radius=2.5, angle=60*DEGREES).move_to([-3, 0, 0])
sector.set_color(RED)
sector2.set_color(PINK)
self.add(sector, sector2)

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

Parameters:

radius (float)

kwargs (Any)

_original__init__(radius=1, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

radius (float)

kwargs (Any)

Return type:
None


---

## TangentialArc - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.TangentialArc.html

TangentialArc¶

Qualified name: manim.mobject.geometry.arc.TangentialArc

class TangentialArc(line1, line2, radius, corner=(1, 1), **kwargs)[source]¶
Bases: ArcBetweenPoints

Construct an arc that is tangent to two intersecting lines.
You can choose any of the 4 possible corner arcs via the corner tuple.
corner = (s1, s2) where each si is ±1 to control direction along each line.

Examples

Example: TangentialArcExample ¶

from manim import *

class TangentialArcExample(Scene):
def construct(self):
line1 = DashedLine(start=3 * LEFT, end=3 * RIGHT)
line1.rotate(angle=31 * DEGREES, about_point=ORIGIN)
line2 = DashedLine(start=3 * UP, end=3 * DOWN)
line2.rotate(angle=12 * DEGREES, about_point=ORIGIN)

arc = TangentialArc(line1, line2, radius=2.25, corner=(1, 1), color=TEAL)
self.add(arc, line1, line2)

class TangentialArcExample(Scene):
def construct(self):
line1 = DashedLine(start=3 * LEFT, end=3 * RIGHT)
line1.rotate(angle=31 * DEGREES, about_point=ORIGIN)
line2 = DashedLine(start=3 * UP, end=3 * DOWN)
line2.rotate(angle=12 * DEGREES, about_point=ORIGIN)

arc = TangentialArc(line1, line2, radius=2.25, corner=(1, 1), color=TEAL)
self.add(arc, line1, line2)

The following example shows all four possible corner configurations:

Example: TangentialArcCorners ¶

from manim import *

class TangentialArcCorners(Scene):
def construct(self):
# Create two intersecting lines
line1 = DashedLine(start=3 * LEFT, end=3 * RIGHT, color=GREY)
line2 = DashedLine(start=3 * UP, end=3 * DOWN, color=GREY)

# All four corner configurations with different colors
arc_pp = TangentialArc(line1, line2, radius=1.5, corner=(1, 1), color=RED)
arc_pn = TangentialArc(line1, line2, radius=1.5, corner=(1, -1), color=GREEN)
arc_np = TangentialArc(line1, line2, radius=1.5, corner=(-1, 1), color=BLUE)
arc_nn = TangentialArc(line1, line2, radius=1.5, corner=(-1, -1), color=YELLOW)

# Labels for each arc
label_pp = Text("(1,1)", font_size=24, color=RED).next_to(arc_pp, UR, buff=0.1)
label_pn = Text("(1,-1)", font_size=24, color=GREEN).next_to(arc_pn, DR, buff=0.1)
label_np = Text("(-1,1)", font_size=24, color=BLUE).next_to(arc_np, UL, buff=0.1)
label_nn = Text("(-1,-1)", font_size=24, color=YELLOW).next_to(arc_nn, DL, buff=0.1)

self.add(line1, line2, arc_pp, arc_pn, arc_np, arc_nn)
self.add(label_pp, label_pn, label_np, label_nn)

class TangentialArcCorners(Scene):
def construct(self):
# Create two intersecting lines
line1 = DashedLine(start=3 * LEFT, end=3 * RIGHT, color=GREY)
line2 = DashedLine(start=3 * UP, end=3 * DOWN, color=GREY)

# All four corner configurations with different colors
arc_pp = TangentialArc(line1, line2, radius=1.5, corner=(1, 1), color=RED)
arc_pn = TangentialArc(line1, line2, radius=1.5, corner=(1, -1), color=GREEN)
arc_np = TangentialArc(line1, line2, radius=1.5, corner=(-1, 1), color=BLUE)
arc_nn = TangentialArc(line1, line2, radius=1.5, corner=(-1, -1), color=YELLOW)

# Labels for each arc
label_pp = Text("(1,1)", font_size=24, color=RED).next_to(arc_pp, UR, buff=0.1)
label_pn = Text("(1,-1)", font_size=24, color=GREEN).next_to(arc_pn, DR, buff=0.1)
label_np = Text("(-1,1)", font_size=24, color=BLUE).next_to(arc_np, UL, buff=0.1)
label_nn = Text("(-1,-1)", font_size=24, color=YELLOW).next_to(arc_nn, DL, buff=0.1)

self.add(line1, line2, arc_pp, arc_pn, arc_np, arc_nn)
self.add(label_pp, label_pn, label_np, label_nn)

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

Parameters:

line1 (Line)

line2 (Line)

radius (float)

corner (Any)

kwargs (Any)

_original__init__(line1, line2, radius, corner=(1, 1), **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

line1 (Line)

line2 (Line)

radius (float)

corner (Any)

kwargs (Any)


---

## TipableVMobject - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.TipableVMobject.html

TipableVMobject¶

Qualified name: manim.mobject.geometry.arc.TipableVMobject

class TipableVMobject(tip_length=0.35, normal_vector=array([0., 0., 1.]), tip_style=None, **kwargs)[source]¶
Bases: VMobject

Meant for shared functionality between Arc and Line.
Functionality can be classified broadly into these groups:

Adding, Creating, Modifying tips

add_tip calls create_tip, before pushing the new tipinto the TipableVMobject’s list of submobjects

stylistic and positional configuration

Checking for tips

Boolean checks for whether the TipableVMobject has a tipand a starting tip

Getters

Straightforward accessors, returning information pertainingto the TipableVMobject instance’s tip(s), its length etc

Methods

add_tip

Adds a tip to the TipableVMobject instance, recognising that the endpoints might need to be switched if it's a 'starting tip' or not.

assign_tip_attr

create_tip

Stylises the tip, positions it spatially, and returns the newly instantiated tip to the caller.

get_default_tip_length

get_end

Returns the point, where the stroke that surrounds the Mobject ends.

get_first_handle

get_last_handle

get_length

get_start

Returns the point, where the stroke that surrounds the Mobject starts.

get_tip

Returns the TipableVMobject instance's (first) tip, otherwise throws an exception.

get_tips

Returns a VGroup (collection of VMobjects) containing the TipableVMObject instance's tips.

get_unpositioned_tip

Returns a tip that has been stylistically configured, but has not yet been given a position in space.

has_start_tip

has_tip

pop_tips

position_tip

reset_endpoints_based_on_tip

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

tip_length (float)

normal_vector (Vector3DLike)

tip_style (dict | None)

kwargs (Any)

_original__init__(tip_length=0.35, normal_vector=array([0., 0., 1.]), tip_style=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

tip_length (float)

normal_vector (Vector3DLike)

tip_style (dict | None)

kwargs (Any)

Return type:
None

add_tip(tip=None, tip_shape=None, tip_length=None, tip_width=None, at_start=False)[source]¶
Adds a tip to the TipableVMobject instance, recognising
that the endpoints might need to be switched if it’s
a ‘starting tip’ or not.

Parameters:

tip (tips.ArrowTip | None)

tip_shape (type[tips.ArrowTip] | None)

tip_length (float | None)

tip_width (float | None)

at_start (bool)

Return type:
Self

create_tip(tip_shape=None, tip_length=None, tip_width=None, at_start=False)[source]¶
Stylises the tip, positions it spatially, and returns
the newly instantiated tip to the caller.

Parameters:

tip_shape (type[tips.ArrowTip] | None)

tip_length (float | None)

tip_width (float | None)

at_start (bool)

Return type:
tips.ArrowTip

get_end()[source]¶
Returns the point, where the stroke that surrounds the Mobject ends.

Return type:
Point3D

get_start()[source]¶
Returns the point, where the stroke that surrounds the Mobject starts.

Return type:
Point3D

get_tip()[source]¶
Returns the TipableVMobject instance’s (first) tip,
otherwise throws an exception.

Return type:
VMobject

get_tips()[source]¶
Returns a VGroup (collection of VMobjects) containing
the TipableVMObject instance’s tips.

Return type:
VGroup

get_unpositioned_tip(tip_shape=None, tip_length=None, tip_width=None)[source]¶
Returns a tip that has been stylistically configured,
but has not yet been given a position in space.

Parameters:

tip_shape (type[tips.ArrowTip] | None)

tip_length (float | None)

tip_width (float | None)

Return type:
tips.ArrowTip | tips.ArrowTriangleFilledTip


---

## arc - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.geometry.arc.html

arc¶

Mobjects that are curved.

Examples

Example: UsefulAnnotations ¶

from manim import *

class UsefulAnnotations(Scene):
def construct(self):
m0 = Dot()
m1 = AnnotationDot()
m2 = LabeledDot("ii")
m3 = LabeledDot(MathTex(r"\alpha").set_color(ORANGE))
m4 = CurvedArrow(2*LEFT, 2*RIGHT, radius= -5)
m5 = CurvedArrow(2*LEFT, 2*RIGHT, radius= 8)
m6 = CurvedDoubleArrow(ORIGIN, 2*RIGHT)

self.add(m0, m1, m2, m3, m4, m5, m6)
for i, mobj in enumerate(self.mobjects):
mobj.shift(DOWN * (i-3))

class UsefulAnnotations(Scene):
def construct(self):
m0 = Dot()
m1 = AnnotationDot()
m2 = LabeledDot("ii")
m3 = LabeledDot(MathTex(r"\alpha").set_color(ORANGE))
m4 = CurvedArrow(2*LEFT, 2*RIGHT, radius= -5)
m5 = CurvedArrow(2*LEFT, 2*RIGHT, radius= 8)
m6 = CurvedDoubleArrow(ORIGIN, 2*RIGHT)

self.add(m0, m1, m2, m3, m4, m5, m6)
for i, mobj in enumerate(self.mobjects):
mobj.shift(DOWN * (i-3))

Classes

AnnotationDot

A dot with bigger radius and bold stroke to annotate scenes.

AnnularSector

A sector of an annulus.

Annulus

Region between two concentric Circles.

Arc

A circular arc.

ArcBetweenPoints

Inherits from Arc and additionally takes 2 points between which the arc is spanned.

ArcPolygon

A generalized polygon allowing for points to be connected with arcs.

ArcPolygonFromArcs

A generalized polygon allowing for points to be connected with arcs.

Circle

A circle.

CubicBezier

A cubic Bézier curve.

CurvedArrow

CurvedDoubleArrow

Dot

A circle with a very small radius.

Ellipse

A circular shape; oval, circle.

LabeledDot

A Dot containing a label in its center.

Sector

A sector of a circle.

TangentialArc

Construct an arc that is tangent to two intersecting lines.

TipableVMobject

Meant for shared functionality between Arc and Line.
