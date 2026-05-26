# Three D Polyhedra


---

## ConvexHull3D - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.polyhedra.ConvexHull3D.html

ConvexHull3D¶

Qualified name: manim.mobject.three\_d.polyhedra.ConvexHull3D

class ConvexHull3D(*points, tolerance=1e-05, **kwargs)[source]¶
Bases: Polyhedron

A convex hull for a set of points

Parameters:

points (Point3D) – The points to consider.

tolerance (float) – The tolerance used for quickhull.

kwargs (Any) – Forwarded to the parent constructor.

Examples

Example: ConvexHull3DExample ¶

from manim import *

class ConvexHull3DExample(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
points = [
[ 1.93192757,  0.44134585, -1.52407061],
[-0.93302521,  1.23206983,  0.64117067],
[-0.44350918, -0.61043677,  0.21723705],
[-0.42640268, -1.05260843,  1.61266094],
[-1.84449637,  0.91238739, -1.85172623],
[ 1.72068132, -0.11880457,  0.51881751],
[ 0.41904805,  0.44938012, -1.86440686],
[ 0.83864666,  1.66653337,  1.88960123],
[ 0.22240514, -0.80986286,  1.34249326],
[-1.29585759,  1.01516189,  0.46187522],
[ 1.7776499,  -1.59550796, -1.70240747],
[ 0.80065226, -0.12530398,  1.70063977],
[ 1.28960948, -1.44158255,  1.39938582],
[-0.93538943,  1.33617705, -0.24852643],
[-1.54868271,  1.7444399,  -0.46170734]
]
hull = ConvexHull3D(
*points,
faces_config = {"stroke_opacity": 0},
graph_config = {
"vertex_type": Dot3D,
"edge_config": {
"stroke_color": BLUE,
"stroke_width": 2,
"stroke_opacity": 0.05,
}
}
)
dots = VGroup(*[Dot3D(point) for point in points])
self.add(hull)
self.add(dots)

class ConvexHull3DExample(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
points = [
[ 1.93192757,  0.44134585, -1.52407061],
[-0.93302521,  1.23206983,  0.64117067],
[-0.44350918, -0.61043677,  0.21723705],
[-0.42640268, -1.05260843,  1.61266094],
[-1.84449637,  0.91238739, -1.85172623],
[ 1.72068132, -0.11880457,  0.51881751],
[ 0.41904805,  0.44938012, -1.86440686],
[ 0.83864666,  1.66653337,  1.88960123],
[ 0.22240514, -0.80986286,  1.34249326],
[-1.29585759,  1.01516189,  0.46187522],
[ 1.7776499,  -1.59550796, -1.70240747],
[ 0.80065226, -0.12530398,  1.70063977],
[ 1.28960948, -1.44158255,  1.39938582],
[-0.93538943,  1.33617705, -0.24852643],
[-1.54868271,  1.7444399,  -0.46170734]
]
hull = ConvexHull3D(
*points,
faces_config = {"stroke_opacity": 0},
graph_config = {
"vertex_type": Dot3D,
"edge_config": {
"stroke_color": BLUE,
"stroke_width": 2,
"stroke_opacity": 0.05,
}
}
)
dots = VGroup(*[Dot3D(point) for point in points])
self.add(hull)
self.add(dots)

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

_original__init__(*points, tolerance=1e-05, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

points (Point3D)

tolerance (float)

kwargs (Any)


---

## Dodecahedron - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.polyhedra.Dodecahedron.html

Dodecahedron¶

Qualified name: manim.mobject.three\_d.polyhedra.Dodecahedron

class Dodecahedron(edge_length=1, **kwargs)[source]¶
Bases: Polyhedron

A dodecahedron, one of the five platonic solids. It has 12 faces, 30 edges and 20 vertices.

Parameters:

edge_length (float) – The length of an edge between any two vertices.

kwargs (Any)

Examples

Example: DodecahedronScene ¶

from manim import *

class DodecahedronScene(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
obj = Dodecahedron()
self.add(obj)

class DodecahedronScene(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
obj = Dodecahedron()
self.add(obj)

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

_original__init__(edge_length=1, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

edge_length (float)

kwargs (Any)


---

## Icosahedron - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.polyhedra.Icosahedron.html

Icosahedron¶

Qualified name: manim.mobject.three\_d.polyhedra.Icosahedron

class Icosahedron(edge_length=1, **kwargs)[source]¶
Bases: Polyhedron

An icosahedron, one of the five platonic solids. It has 20 faces, 30 edges and 12 vertices.

Parameters:

edge_length (float) – The length of an edge between any two vertices.

kwargs (Any)

Examples

Example: IcosahedronScene ¶

from manim import *

class IcosahedronScene(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
obj = Icosahedron()
self.add(obj)

class IcosahedronScene(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
obj = Icosahedron()
self.add(obj)

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

_original__init__(edge_length=1, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

edge_length (float)

kwargs (Any)


---

## Octahedron - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.polyhedra.Octahedron.html

Octahedron¶

Qualified name: manim.mobject.three\_d.polyhedra.Octahedron

class Octahedron(edge_length=1, **kwargs)[source]¶
Bases: Polyhedron

An octahedron, one of the five platonic solids. It has 8 faces, 12 edges and 6 vertices.

Parameters:

edge_length (float) – The length of an edge between any two vertices.

kwargs (Any)

Examples

Example: OctahedronScene ¶

from manim import *

class OctahedronScene(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
obj = Octahedron()
self.add(obj)

class OctahedronScene(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
obj = Octahedron()
self.add(obj)

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

_original__init__(edge_length=1, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

edge_length (float)

kwargs (Any)


---

## Polyhedron - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.polyhedra.Polyhedron.html

Polyhedron¶

Qualified name: manim.mobject.three\_d.polyhedra.Polyhedron

class Polyhedron(vertex_coords, faces_list, faces_config={}, graph_config={})[source]¶
Bases: VGroup

An abstract polyhedra class.

In this implementation, polyhedra are defined with a list of vertex coordinates in space, and a list
of faces. This implementation mirrors that of a standard polyhedral data format (OFF, object file format).

Parameters:

vertex_coords (Point3DLike_Array) – A list of coordinates of the corresponding vertices in the polyhedron. Each coordinate will correspond to
a vertex. The vertices are indexed with the usual indexing of Python.

faces_list (list[list[int]]) – A list of faces. Each face is a sublist containing the indices of the vertices that form the corners of that face.

faces_config (dict[str, str | int | float | bool]) – Configuration for the polygons representing the faces of the polyhedron.

graph_config (dict[str, Any]) – Configuration for the graph containing the vertices and edges of the polyhedron.

Examples

To understand how to create a custom polyhedra, let’s use the example of a rather simple one - a square pyramid.

Example: SquarePyramidScene ¶

from manim import *

class SquarePyramidScene(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
vertex_coords = [
[1, 1, 0],
[1, -1, 0],
[-1, -1, 0],
[-1, 1, 0],
[0, 0, 2]
]
faces_list = [
[0, 1, 4],
[1, 2, 4],
[2, 3, 4],
[3, 0, 4],
[0, 1, 2, 3]
]
pyramid = Polyhedron(vertex_coords, faces_list)
self.add(pyramid)

class SquarePyramidScene(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
vertex_coords = [
[1, 1, 0],
[1, -1, 0],
[-1, -1, 0],
[-1, 1, 0],
[0, 0, 2]
]
faces_list = [
[0, 1, 4],
[1, 2, 4],
[2, 3, 4],
[3, 0, 4],
[0, 1, 2, 3]
]
pyramid = Polyhedron(vertex_coords, faces_list)
self.add(pyramid)

In defining the polyhedron above, we first defined the coordinates of the vertices.
These are the corners of the square base, given as the first four coordinates in the vertex list,
and the apex, the last coordinate in the list.

Next, we define the faces of the polyhedron. The triangular surfaces of the pyramid are polygons
with two adjacent vertices in the base and the vertex at the apex as corners. We thus define these
surfaces in the first four elements of our face list. The last element defines the base of the pyramid.

The graph and faces of polyhedra can also be accessed and modified directly, after instantiation.
They are stored in the graph and faces attributes respectively.

Example: PolyhedronSubMobjects ¶

from manim import *

class PolyhedronSubMobjects(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
octahedron = Octahedron(edge_length = 3)
octahedron.graph[0].set_color(RED)
octahedron.faces[2].set_color(YELLOW)
self.add(octahedron)

class PolyhedronSubMobjects(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
octahedron = Octahedron(edge_length = 3)
octahedron.graph[0].set_color(RED)
octahedron.faces[2].set_color(YELLOW)
self.add(octahedron)

Methods

create_faces

Creates VGroup of faces from a list of face coordinates.

extract_face_coords

Extracts the coordinates of the vertices in the graph.

get_edges

Creates list of cyclic pairwise tuples.

update_faces

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

_original__init__(vertex_coords, faces_list, faces_config={}, graph_config={})¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

vertex_coords (Point3DLike_Array)

faces_list (list[list[int]])

faces_config (dict[str, str | int | float | bool])

graph_config (dict[str, Any])

create_faces(face_coords)[source]¶
Creates VGroup of faces from a list of face coordinates.

Parameters:
face_coords (Point3DLike_Array)

Return type:
VGroup

extract_face_coords()[source]¶
Extracts the coordinates of the vertices in the graph.
Used for updating faces.

Return type:
Point3DLike_Array

get_edges(faces_list)[source]¶
Creates list of cyclic pairwise tuples.

Parameters:
faces_list (list[list[int]])

Return type:
list[tuple[int, int]]


---

## Tetrahedron - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.polyhedra.Tetrahedron.html

Tetrahedron¶

Qualified name: manim.mobject.three\_d.polyhedra.Tetrahedron

class Tetrahedron(edge_length=1, **kwargs)[source]¶
Bases: Polyhedron

A tetrahedron, one of the five platonic solids. It has 4 faces, 6 edges, and 4 vertices.

Parameters:

edge_length (float) – The length of an edge between any two vertices.

kwargs (Any)

Examples

Example: TetrahedronScene ¶

from manim import *

class TetrahedronScene(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
obj = Tetrahedron()
self.add(obj)

class TetrahedronScene(ThreeDScene):
def construct(self):
self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES)
obj = Tetrahedron()
self.add(obj)

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

_original__init__(edge_length=1, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

edge_length (float)

kwargs (Any)


---

## polyhedra - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.three_d.polyhedra.html

polyhedra¶

General polyhedral class and platonic solids.

Classes

ConvexHull3D

A convex hull for a set of points

Dodecahedron

A dodecahedron, one of the five platonic solids.

Icosahedron

An icosahedron, one of the five platonic solids.

Octahedron

An octahedron, one of the five platonic solids.

Polyhedron

An abstract polyhedra class.

Tetrahedron

A tetrahedron, one of the five platonic solids.
