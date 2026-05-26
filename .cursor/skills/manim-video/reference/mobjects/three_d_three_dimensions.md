# Three D Three Dimensions


---

## Arrow3D - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.three_dimensions.Arrow3D.html

Arrow3D¶

Qualified name: manim.mobject.three\_d.three\_dimensions.Arrow3D

class Arrow3D(start=array([-1., 0., 0.]), end=array([1., 0., 0.]), thickness=0.02, height=0.3, base_radius=0.08, color=ManimColor('#FFFFFF'), resolution=24, **kwargs)[source]¶
Bases: Line3D

An arrow made out of a cylindrical line and a conical tip.

Parameters:

start (Point3DLike) – The start position of the arrow.

end (Point3DLike) – The end position of the arrow.

thickness (float) – The thickness of the arrow.

height (float) – The height of the conical tip.

base_radius (float) – The base radius of the conical tip.

color (ManimColor) – The color of the arrow.

resolution (int | tuple[int, int]) – The resolution of the arrow line.

kwargs (Any)

Examples

Example: ExampleArrow3D ¶

from manim import *

class ExampleArrow3D(ThreeDScene):
def construct(self):
axes = ThreeDAxes()
arrow = Arrow3D(
start=np.array([0, 0, 0]),
end=np.array([2, 2, 2]),
resolution=8
)
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
self.add(axes, arrow)

class ExampleArrow3D(ThreeDScene):
def construct(self):
axes = ThreeDAxes()
arrow = Arrow3D(
start=np.array([0, 0, 0]),
end=np.array([2, 2, 2]),
resolution=8
)
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
self.add(axes, arrow)

Methods

get_end

Returns the ending point of the Line3D.

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

_original__init__(start=array([-1., 0., 0.]), end=array([1., 0., 0.]), thickness=0.02, height=0.3, base_radius=0.08, color=ManimColor('#FFFFFF'), resolution=24, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

start (Point3DLike)

end (Point3DLike)

thickness (float)

height (float)

base_radius (float)

color (ParsableManimColor)

resolution (int | tuple[int, int])

kwargs (Any)

Return type:
None

get_end()[source]¶
Returns the ending point of the Line3D.

Returns:
end – Ending point of the Line3D.

Return type:
numpy.array


---

## Cone - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.three_dimensions.Cone.html

Cone¶

Qualified name: manim.mobject.three\_d.three\_dimensions.Cone

class Cone(base_radius=1, height=1, direction=array([0., 0., 1.]), show_base=False, v_range=(0, 6.283185307179586), u_min=0, checkerboard_colors=False, **kwargs)[source]¶
Bases: Surface

A circular cone.
Can be defined using 2 parameters: its height, and its base radius.
The polar angle, theta, can be calculated using arctan(base_radius /
height) The spherical radius, r, is calculated using the pythagorean
theorem.

Parameters:

base_radius (float) – The base radius from which the cone tapers.

height (float) – The height measured from the plane formed by the base_radius to
the apex of the cone.

direction (Vector3DLike) – The direction of the apex.

show_base (bool) – Whether to show the base plane or not.

v_range (tuple[float, float]) – The azimuthal angle to start and end at.

u_min (float) – The radius at the apex.

checkerboard_colors (list[ManimColor] | Literal[False]) – Show checkerboard grid texture on the cone.

kwargs (Any)

Examples

Example: ExampleCone ¶

from manim import *

class ExampleCone(ThreeDScene):
def construct(self):
axes = ThreeDAxes()
cone = Cone(direction=X_AXIS+Y_AXIS+2*Z_AXIS, resolution=8)
self.set_camera_orientation(phi=5*PI/11, theta=PI/9)
self.add(axes, cone)

class ExampleCone(ThreeDScene):
def construct(self):
axes = ThreeDAxes()
cone = Cone(direction=X_AXIS+Y_AXIS+2*Z_AXIS, resolution=8)
self.set_camera_orientation(phi=5*PI/11, theta=PI/9)
self.add(axes, cone)

Methods

func

Converts from spherical coordinates to cartesian.

get_direction

Returns the current direction of the apex of the Cone.

get_end

Returns the point, where the stroke that surrounds the Mobject ends.

get_start

Returns the point, where the stroke that surrounds the Mobject starts.

set_direction

Changes the direction of the apex of the Cone.

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

_original__init__(base_radius=1, height=1, direction=array([0., 0., 1.]), show_base=False, v_range=(0, 6.283185307179586), u_min=0, checkerboard_colors=False, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

base_radius (float)

height (float)

direction (Vector3DLike)

show_base (bool)

v_range (tuple[float, float])

u_min (float)

checkerboard_colors (Iterable[TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor')] | Literal[False])

kwargs (Any)

Return type:
None

func(u, v)[source]¶
Converts from spherical coordinates to cartesian.

Parameters:

u (float) – The radius.

v (float) – The azimuthal angle.

Returns:
Points defining the Cone.

Return type:
numpy.array

get_direction()[source]¶
Returns the current direction of the apex of the Cone.

Returns:
direction – The direction of the apex.

Return type:
numpy.array

get_end()[source]¶
Returns the point, where the stroke that surrounds the Mobject ends.

Return type:
Point3D

get_start()[source]¶
Returns the point, where the stroke that surrounds the Mobject starts.

Return type:
Point3D

set_direction(direction)[source]¶
Changes the direction of the apex of the Cone.

Parameters:
direction (Vector3DLike) – The direction of the apex.

Return type:
None


---

## Cube - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.three_dimensions.Cube.html

Cube¶

Qualified name: manim.mobject.three\_d.three\_dimensions.Cube

class Cube(side_length=2, fill_opacity=0.75, fill_color=ManimColor('#58C4DD'), stroke_width=0, **kwargs)[source]¶
Bases: VGroup

A three-dimensional cube.

Parameters:

side_length (float) – Length of each side of the Cube.

fill_opacity (float) – The opacity of the Cube, from 0 being fully transparent to 1 being
fully opaque. Defaults to 0.75.

fill_color (ParsableManimColor) – The color of the Cube.

stroke_width (float) – The width of the stroke surrounding each face of the Cube.

kwargs (Any)

Examples

Example: CubeExample ¶

from manim import *

class CubeExample(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)

axes = ThreeDAxes()
cube = Cube(side_length=3, fill_opacity=0.7, fill_color=BLUE)
self.add(cube)

class CubeExample(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)

axes = ThreeDAxes()
cube = Cube(side_length=3, fill_opacity=0.7, fill_color=BLUE)
self.add(cube)

Methods

generate_points

Creates the sides of the Cube.

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

_original__init__(side_length=2, fill_opacity=0.75, fill_color=ManimColor('#58C4DD'), stroke_width=0, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

side_length (float)

fill_opacity (float)

fill_color (ParsableManimColor)

stroke_width (float)

kwargs (Any)

Return type:
None

generate_points()[source]¶
Creates the sides of the Cube.

Return type:
None


---

## Cylinder - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.three_dimensions.Cylinder.html

Cylinder¶

Qualified name: manim.mobject.three\_d.three\_dimensions.Cylinder

class Cylinder(radius=1, height=2, direction=array([0., 0., 1.]), v_range=(0, 6.283185307179586), show_ends=True, resolution=(24, 24), **kwargs)[source]¶
Bases: Surface

A cylinder, defined by its height, radius and direction,

Parameters:

radius (float) – The radius of the cylinder.

height (float) – The height of the cylinder.

direction (Vector3DLike) – The direction of the central axis of the cylinder.

v_range (tuple[float, float]) – The height along the height axis (given by direction) to start and end on.

show_ends (bool) – Whether to show the end caps or not.

resolution (int | tuple[int, int]) – The number of samples taken of the Cylinder. A tuple can be used
to define different resolutions for u and v respectively.

kwargs (Any)

Examples

Example: ExampleCylinder ¶

from manim import *

class ExampleCylinder(ThreeDScene):
def construct(self):
axes = ThreeDAxes()
cylinder = Cylinder(radius=2, height=3)
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
self.add(axes, cylinder)

class ExampleCylinder(ThreeDScene):
def construct(self):
axes = ThreeDAxes()
cylinder = Cylinder(radius=2, height=3)
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
self.add(axes, cylinder)

Methods

add_bases

Adds the end caps of the cylinder.

func

Converts from cylindrical coordinates to cartesian.

get_direction

Returns the direction of the central axis of the Cylinder.

set_direction

Sets the direction of the central axis of the Cylinder.

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

_original__init__(radius=1, height=2, direction=array([0., 0., 1.]), v_range=(0, 6.283185307179586), show_ends=True, resolution=(24, 24), **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

radius (float)

height (float)

direction (Vector3DLike)

v_range (tuple[float, float])

show_ends (bool)

resolution (int | tuple[int, int])

kwargs (Any)

Return type:
None

add_bases()[source]¶
Adds the end caps of the cylinder.

Return type:
None

func(u, v)[source]¶
Converts from cylindrical coordinates to cartesian.

Parameters:

u (float) – The height.

v (float) – The azimuthal angle.

Returns:
Points defining the Cylinder.

Return type:
numpy.ndarray

get_direction()[source]¶
Returns the direction of the central axis of the Cylinder.

Returns:
direction – The direction of the central axis of the Cylinder.

Return type:
numpy.array

set_direction(direction)[source]¶
Sets the direction of the central axis of the Cylinder.

Parameters:
direction (numpy.array) – The direction of the central axis of the Cylinder.

Return type:
None


---

## Dot3D - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.three_dimensions.Dot3D.html

Dot3D¶

Qualified name: manim.mobject.three\_d.three\_dimensions.Dot3D

class Dot3D(point=array([0., 0., 0.]), radius=0.08, color=ManimColor('#FFFFFF'), resolution=(8, 8), **kwargs)[source]¶
Bases: Sphere

A spherical dot.

Parameters:

point (Point3D) – The location of the dot.

radius (float) – The radius of the dot.

color (ManimColor) – The color of the Dot3D.

resolution (int | tuple[int, int] | None) – The number of samples taken of the Dot3D. A tuple can be
used to define different resolutions for u and v respectively.

kwargs (Any)

Examples

Example: Dot3DExample ¶

from manim import *

class Dot3DExample(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)

axes = ThreeDAxes()
dot_1 = Dot3D(point=axes.coords_to_point(0, 0, 1), color=RED)
dot_2 = Dot3D(point=axes.coords_to_point(2, 0, 0), radius=0.1, color=BLUE)
dot_3 = Dot3D(point=[0, 0, 0], radius=0.1, color=ORANGE)
self.add(axes, dot_1, dot_2,dot_3)

class Dot3DExample(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75*DEGREES, theta=-45*DEGREES)

axes = ThreeDAxes()
dot_1 = Dot3D(point=axes.coords_to_point(0, 0, 1), color=RED)
dot_2 = Dot3D(point=axes.coords_to_point(2, 0, 0), radius=0.1, color=BLUE)
dot_3 = Dot3D(point=[0, 0, 0], radius=0.1, color=ORANGE)
self.add(axes, dot_1, dot_2,dot_3)

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

_original__init__(point=array([0., 0., 0.]), radius=0.08, color=ManimColor('#FFFFFF'), resolution=(8, 8), **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

point (Point3D)

radius (float)

color (ParsableManimColor)

resolution (int | tuple[int, int] | None)

kwargs (Any)

Return type:
None


---

## Line3D - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.three_dimensions.Line3D.html

Line3D¶

Qualified name: manim.mobject.three\_d.three\_dimensions.Line3D

class Line3D(start=array([-1., 0., 0.]), end=array([1., 0., 0.]), thickness=0.02, color=None, resolution=24, **kwargs)[source]¶
Bases: Cylinder

A cylindrical line, for use in ThreeDScene.

Parameters:

start (Point3DLike) – The start point of the line.

end (Point3DLike) – The end point of the line.

thickness (float) – The thickness of the line.

color (ManimColor) – The color of the line.

resolution (tuple[int, int]) – The resolution of the line.
By default this value is the number of points the line will sampled at.
If you want the line to also come out checkered, use a tuple.
For example, for a line made of 24 points with 4 checker points on each
cylinder, pass the tuple (4, 24).

kwargs (Any)

Examples

Example: ExampleLine3D ¶

from manim import *

class ExampleLine3D(ThreeDScene):
def construct(self):
axes = ThreeDAxes()
line = Line3D(start=np.array([0, 0, 0]), end=np.array([2, 2, 2]))
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
self.add(axes, line)

class ExampleLine3D(ThreeDScene):
def construct(self):
axes = ThreeDAxes()
line = Line3D(start=np.array([0, 0, 0]), end=np.array([2, 2, 2]))
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
self.add(axes, line)

Methods

get_end

Returns the ending point of the Line3D.

get_start

Returns the starting point of the Line3D.

parallel_to

Returns a line parallel to another line going through a given point.

perpendicular_to

Returns a line perpendicular to another line going through a given point.

pointify

Gets a point representing the center of the Mobjects.

set_start_and_end_attrs

Sets the start and end points of the line.

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

_original__init__(start=array([-1., 0., 0.]), end=array([1., 0., 0.]), thickness=0.02, color=None, resolution=24, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

start (Point3DLike)

end (Point3DLike)

thickness (float)

color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | None)

resolution (int | tuple[int, int])

kwargs (Any)

get_end()[source]¶
Returns the ending point of the Line3D.

Returns:
end – Ending point of the Line3D.

Return type:
numpy.array

get_start()[source]¶
Returns the starting point of the Line3D.

Returns:
start – Starting point of the Line3D.

Return type:
numpy.array

classmethod parallel_to(line, point=array([0., 0., 0.]), length=5, **kwargs)[source]¶
Returns a line parallel to another line going through
a given point.

Parameters:

line (Line3D) – The line to be parallel to.

point (Point3DLike) – The point to pass through.

length (float) – Length of the parallel line.

kwargs (Any) – Additional parameters to be passed to the class.

Returns:
Line parallel to line.

Return type:
Line3D

Examples

Example: ParallelLineExample ¶

from manim import *

class ParallelLineExample(ThreeDScene):
def construct(self):
self.set_camera_orientation(PI / 3, -PI / 4)
ax = ThreeDAxes((-5, 5), (-5, 5), (-5, 5), 10, 10, 10)
line1 = Line3D(RIGHT * 2, UP + OUT, color=RED)
line2 = Line3D.parallel_to(line1, color=YELLOW)
self.add(ax, line1, line2)

class ParallelLineExample(ThreeDScene):
def construct(self):
self.set_camera_orientation(PI / 3, -PI / 4)
ax = ThreeDAxes((-5, 5), (-5, 5), (-5, 5), 10, 10, 10)
line1 = Line3D(RIGHT * 2, UP + OUT, color=RED)
line2 = Line3D.parallel_to(line1, color=YELLOW)
self.add(ax, line1, line2)

classmethod perpendicular_to(line, point=array([0., 0., 0.]), length=5, **kwargs)[source]¶
Returns a line perpendicular to another line going through
a given point.

Parameters:

line (Line3D) – The line to be perpendicular to.

point (Point3DLike) – The point to pass through.

length (float) – Length of the perpendicular line.

kwargs (Any) – Additional parameters to be passed to the class.

Returns:
Line perpendicular to line.

Return type:
Line3D

Examples

Example: PerpLineExample ¶

from manim import *

class PerpLineExample(ThreeDScene):
def construct(self):
self.set_camera_orientation(PI / 3, -PI / 4)
ax = ThreeDAxes((-5, 5), (-5, 5), (-5, 5), 10, 10, 10)
line1 = Line3D(RIGHT * 2, UP + OUT, color=RED)
line2 = Line3D.perpendicular_to(line1, color=BLUE)
self.add(ax, line1, line2)

class PerpLineExample(ThreeDScene):
def construct(self):
self.set_camera_orientation(PI / 3, -PI / 4)
ax = ThreeDAxes((-5, 5), (-5, 5), (-5, 5), 10, 10, 10)
line1 = Line3D(RIGHT * 2, UP + OUT, color=RED)
line2 = Line3D.perpendicular_to(line1, color=BLUE)
self.add(ax, line1, line2)

pointify(mob_or_point, direction=None)[source]¶
Gets a point representing the center of the Mobjects.

Parameters:

mob_or_point (Mobject | TypeAliasForwardRef('~manim.typing.Point3DLike')) – Mobjects or point whose center should be returned.

direction (TypeAliasForwardRef('~manim.typing.Vector3DLike') | None) – If an edge of a Mobjects should be returned, the direction of the edge.

Returns:
Center of the Mobjects or point, or edge if direction is given.

Return type:
numpy.array

set_start_and_end_attrs(start, end, **kwargs)[source]¶
Sets the start and end points of the line.

If either start or end are Mobjects,
this gives their centers.

Parameters:

start (Point3DLike) – Starting point or Mobject.

end (Point3DLike) – Ending point or Mobject.

kwargs (Any)

Return type:
None


---

## Prism - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.three_dimensions.Prism.html

Prism¶

Qualified name: manim.mobject.three\_d.three\_dimensions.Prism

class Prism(dimensions=[3, 2, 1], **kwargs)[source]¶
Bases: Cube

A right rectangular prism (or rectangular cuboid).
Defined by the length of each side in [x, y, z] format.

Parameters:

dimensions (Vector3DLike) – Dimensions of the Prism in [x, y, z] format.

kwargs (Any)

Examples

Example: ExamplePrism ¶

from manim import *

class ExamplePrism(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=60 * DEGREES, theta=150 * DEGREES)
prismSmall = Prism(dimensions=[1, 2, 3]).rotate(PI / 2)
prismLarge = Prism(dimensions=[1.5, 3, 4.5]).move_to([2, 0, 0])
self.add(prismSmall, prismLarge)

class ExamplePrism(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=60 * DEGREES, theta=150 * DEGREES)
prismSmall = Prism(dimensions=[1, 2, 3]).rotate(PI / 2)
prismLarge = Prism(dimensions=[1.5, 3, 4.5]).move_to([2, 0, 0])
self.add(prismSmall, prismLarge)

Methods

generate_points

Creates the sides of the Prism.

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

_original__init__(dimensions=[3, 2, 1], **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

dimensions (Vector3DLike)

kwargs (Any)

Return type:
None

generate_points()[source]¶
Creates the sides of the Prism.

Return type:
None


---

## Sphere - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.three_dimensions.Sphere.html

Sphere¶

Qualified name: manim.mobject.three\_d.three\_dimensions.Sphere

class Sphere(center=array([0., 0., 0.]), radius=1, resolution=None, u_range=(0, 6.283185307179586), v_range=(0, 3.141592653589793), **kwargs)[source]¶
Bases: Surface

A three-dimensional sphere.

Parameters:

center (Point3DLike) – Center of the Sphere.

radius (float) – The radius of the Sphere.

resolution (int | Sequence[int] | None) – The number of samples taken of the Sphere. A tuple can be used
to define different resolutions for u and v respectively.

u_range (tuple[float, float]) – The range of the u variable: (u_min, u_max).

v_range (tuple[float, float]) – The range of the v variable: (v_min, v_max).

kwargs (Any)

Examples

Example: ExampleSphere ¶

from manim import *

class ExampleSphere(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=PI / 6, theta=PI / 6)
sphere1 = Sphere(
center=(3, 0, 0),
radius=1,
resolution=(20, 20),
u_range=[0.001, PI - 0.001],
v_range=[0, TAU]
)
sphere1.set_color(RED)
self.add(sphere1)
sphere2 = Sphere(center=(-1, -3, 0), radius=2, resolution=(18, 18))
sphere2.set_color(GREEN)
self.add(sphere2)
sphere3 = Sphere(center=(-1, 2, 0), radius=2, resolution=(16, 16))
sphere3.set_color(BLUE)
self.add(sphere3)

class ExampleSphere(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=PI / 6, theta=PI / 6)
sphere1 = Sphere(
center=(3, 0, 0),
radius=1,
resolution=(20, 20),
u_range=[0.001, PI - 0.001],
v_range=[0, TAU]
)
sphere1.set_color(RED)
self.add(sphere1)
sphere2 = Sphere(center=(-1, -3, 0), radius=2, resolution=(18, 18))
sphere2.set_color(GREEN)
self.add(sphere2)
sphere3 = Sphere(center=(-1, 2, 0), radius=2, resolution=(16, 16))
sphere3.set_color(BLUE)
self.add(sphere3)

Methods

func

The z values defining the Sphere being plotted.

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

_original__init__(center=array([0., 0., 0.]), radius=1, resolution=None, u_range=(0, 6.283185307179586), v_range=(0, 3.141592653589793), **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

center (Point3DLike)

radius (float)

resolution (int | Sequence[int] | None)

u_range (tuple[float, float])

v_range (tuple[float, float])

kwargs (Any)

Return type:
None

func(u, v)[source]¶
The z values defining the Sphere being plotted.

Returns:
The z values defining the Sphere.

Return type:
Point3D

Parameters:

u (float)

v (float)


---

## Surface - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.three_dimensions.Surface.html

Surface¶

Qualified name: manim.mobject.three\_d.three\_dimensions.Surface

class Surface(func, u_range=(0, 1), v_range=(0, 1), resolution=32, surface_piece_config={}, fill_color=ManimColor('#29ABCA'), fill_opacity=1.0, checkerboard_colors=[ManimColor('#29ABCA'), ManimColor('#236B8E')], stroke_color=ManimColor('#BBBBBB'), stroke_width=0.5, should_make_jagged=False, pre_function_handle_to_anchor_scale_factor=1e-05, **kwargs)[source]¶
Bases: VGroup

Creates a Parametric Surface using a checkerboard pattern.

Parameters:

func (Callable[[float, float], np.ndarray]) – The function defining the Surface.

u_range (tuple[float, float]) – The range of the u variable: (u_min, u_max).

v_range (tuple[float, float]) – The range of the v variable: (v_min, v_max).

resolution (int | Sequence[int]) – The number of samples taken of the Surface. A tuple can be
used to define different resolutions for u and v respectively.

fill_color (ParsableManimColor) – The color of the Surface. Ignored if checkerboard_colors
is set.

fill_opacity (float) – The opacity of the Surface, from 0 being fully transparent
to 1 being fully opaque. Defaults to 1.

checkerboard_colors (list[ManimColor] | Literal[False]) – ng individual faces alternating colors. Overrides fill_color.

stroke_color (ParsableManimColor) – Color of the stroke surrounding each face of Surface.

stroke_width (float) – Width of the stroke surrounding each face of Surface.
Defaults to 0.5.

should_make_jagged (bool) – Changes the anchor mode of the Bézier curves from smooth to jagged.
Defaults to False.

surface_piece_config (dict)

pre_function_handle_to_anchor_scale_factor (float)

kwargs (Any)

Examples

Example: ParaSurface ¶

from manim import *

class ParaSurface(ThreeDScene):
def func(self, u, v):
return np.array([np.cos(u) * np.cos(v), np.cos(u) * np.sin(v), u])

def construct(self):
axes = ThreeDAxes(x_range=[-4,4], x_length=8)
surface = Surface(
lambda u, v: axes.c2p(*self.func(u, v)),
u_range=[-PI, PI],
v_range=[0, TAU],
resolution=8,
)
self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
self.add(axes, surface)

class ParaSurface(ThreeDScene):
def func(self, u, v):
return np.array([np.cos(u) * np.cos(v), np.cos(u) * np.sin(v), u])

def construct(self):
axes = ThreeDAxes(x_range=[-4,4], x_length=8)
surface = Surface(
lambda u, v: axes.c2p(*self.func(u, v)),
u_range=[-PI, PI],
v_range=[0, TAU],
resolution=8,
)
self.set_camera_orientation(theta=70 * DEGREES, phi=75 * DEGREES)
self.add(axes, surface)

Methods

func

set_fill_by_checkerboard

Sets the fill_color of each face of Surface in an alternating pattern.

set_fill_by_value

Sets the color of each mobject of a parametric surface to a color relative to its axis-value.

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

_original__init__(func, u_range=(0, 1), v_range=(0, 1), resolution=32, surface_piece_config={}, fill_color=ManimColor('#29ABCA'), fill_opacity=1.0, checkerboard_colors=[ManimColor('#29ABCA'), ManimColor('#236B8E')], stroke_color=ManimColor('#BBBBBB'), stroke_width=0.5, should_make_jagged=False, pre_function_handle_to_anchor_scale_factor=1e-05, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

func (Callable[[float, float], ndarray])

u_range (tuple[float, float])

v_range (tuple[float, float])

resolution (int | Sequence[int])

surface_piece_config (dict)

fill_color (ParsableManimColor)

fill_opacity (float)

checkerboard_colors (Iterable[TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor')] | Literal[False])

stroke_color (ParsableManimColor)

stroke_width (float)

should_make_jagged (bool)

pre_function_handle_to_anchor_scale_factor (float)

kwargs (Any)

Return type:
None

set_fill_by_checkerboard(*colors, opacity=None)[source]¶
Sets the fill_color of each face of Surface in
an alternating pattern.

Parameters:

colors (ParsableManimColor) – List of colors for alternating pattern.

opacity (float | None) – The fill_opacity of Surface, from 0 being fully transparent
to 1 being fully opaque.

Returns:
The parametric surface with an alternating pattern.

Return type:
Surface

set_fill_by_value(axes, colorscale=None, axis=2, **kwargs)[source]¶
Sets the color of each mobject of a parametric surface to a color
relative to its axis-value.

Parameters:

axes (ThreeDAxes) – The axes for the parametric surface, which will be used to map
axis-values to colors.

colorscale (Iterable[ParsableManimColor] | Iterable[tuple[ParsableManimColor, float]] | None) – A list of colors, ordered from lower axis-values to higher axis-values.
If a list of tuples is passed containing colors paired with numbers,
then those numbers will be used as the pivots.

axis (int) – The chosen axis to use for the color mapping. (0 = x, 1 = y, 2 = z)

kwargs (Any)

Returns:
The parametric surface with a gradient applied by value. For chaining.

Return type:
Surface

Examples

Example: FillByValueExample ¶

from manim import *

class FillByValueExample(ThreeDScene):
def construct(self):
resolution_fa = 8
self.set_camera_orientation(phi=75 * DEGREES, theta=-160 * DEGREES)
axes = ThreeDAxes(x_range=(0, 5, 1), y_range=(0, 5, 1), z_range=(-1, 1, 0.5))
def param_surface(u, v):
x = u
y = v
z = np.sin(x) * np.cos(y)
return z
surface_plane = Surface(
lambda u, v: axes.c2p(u, v, param_surface(u, v)),
resolution=(resolution_fa, resolution_fa),
v_range=[0, 5],
u_range=[0, 5],
)
surface_plane.set_style(fill_opacity=1)
surface_plane.set_fill_by_value(axes=axes, colorscale=[(RED, -0.5), (YELLOW, 0), (GREEN, 0.5)], axis=2)
self.add(axes, surface_plane)

class FillByValueExample(ThreeDScene):
def construct(self):
resolution_fa = 8
self.set_camera_orientation(phi=75 * DEGREES, theta=-160 * DEGREES)
axes = ThreeDAxes(x_range=(0, 5, 1), y_range=(0, 5, 1), z_range=(-1, 1, 0.5))
def param_surface(u, v):
x = u
y = v
z = np.sin(x) * np.cos(y)
return z
surface_plane = Surface(
lambda u, v: axes.c2p(u, v, param_surface(u, v)),
resolution=(resolution_fa, resolution_fa),
v_range=[0, 5],
u_range=[0, 5],
)
surface_plane.set_style(fill_opacity=1)
surface_plane.set_fill_by_value(axes=axes, colorscale=[(RED, -0.5), (YELLOW, 0), (GREEN, 0.5)], axis=2)
self.add(axes, surface_plane)


---

## ThreeDVMobject - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.three_dimensions.ThreeDVMobject.html

ThreeDVMobject¶

Qualified name: manim.mobject.three\_d.three\_dimensions.ThreeDVMobject

class ThreeDVMobject(shade_in_3d=True, **kwargs)[source]¶
Bases: VMobject

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

u_index

v_index

u1

u2

v1

v2

Parameters:

shade_in_3d (bool)

kwargs (Any)

_original__init__(shade_in_3d=True, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

shade_in_3d (bool)

kwargs (Any)


---

## Torus - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.three_dimensions.Torus.html

Torus¶

Qualified name: manim.mobject.three\_d.three\_dimensions.Torus

class Torus(major_radius=3, minor_radius=1, u_range=(0, 6.283185307179586), v_range=(0, 6.283185307179586), resolution=None, **kwargs)[source]¶
Bases: Surface

A torus.

Parameters:

major_radius (float) – Distance from the center of the tube to the center of the torus.

minor_radius (float) – Radius of the tube.

u_range (tuple[float, float]) – The range of the u variable: (u_min, u_max).

v_range (tuple[float, float]) – The range of the v variable: (v_min, v_max).

resolution (int | tuple[int, int] | None) – The number of samples taken of the Torus. A tuple can be
used to define different resolutions for u and v respectively.

kwargs (Any)

Examples

Example: ExampleTorus ¶

from manim import *

class ExampleTorus(ThreeDScene):
def construct(self):
axes = ThreeDAxes()
torus = Torus()
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
self.add(axes, torus)

class ExampleTorus(ThreeDScene):
def construct(self):
axes = ThreeDAxes()
torus = Torus()
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
self.add(axes, torus)

Methods

func

The z values defining the Torus being plotted.

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

_original__init__(major_radius=3, minor_radius=1, u_range=(0, 6.283185307179586), v_range=(0, 6.283185307179586), resolution=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

major_radius (float)

minor_radius (float)

u_range (tuple[float, float])

v_range (tuple[float, float])

resolution (int | tuple[int, int] | None)

kwargs (Any)

Return type:
None

func(u, v)[source]¶
The z values defining the Torus being plotted.

Returns:
The z values defining the Torus.

Return type:
numpy.ndarray

Parameters:

u (float)

v (float)


---

## three_dimensions - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.three_dimensions.html

three_dimensions¶

Three-dimensional mobjects.

Classes

Arrow3D

An arrow made out of a cylindrical line and a conical tip.

Cone

A circular cone.

Cube

A three-dimensional cube.

Cylinder

A cylinder, defined by its height, radius and direction,

Dot3D

A spherical dot.

Line3D

A cylindrical line, for use in ThreeDScene.

Prism

A right rectangular prism (or rectangular cuboid).

Sphere

A three-dimensional sphere.

Surface

Creates a Parametric Surface using a checkerboard pattern.

ThreeDVMobject

Torus

A torus.
