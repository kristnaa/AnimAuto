# Vector Space Scene


---

## LinearTransformationScene - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.scene.vector_space_scene.LinearTransformationScene.html

LinearTransformationScene¶

Qualified name: manim.scene.vector\_space\_scene.LinearTransformationScene

class LinearTransformationScene(include_background_plane=True, include_foreground_plane=True, background_plane_kwargs=None, foreground_plane_kwargs=None, show_coordinates=False, show_basis_vectors=True, basis_vector_stroke_width=6, i_hat_color=ManimColor('#83C167'), j_hat_color=ManimColor('#FC6255'), leave_ghost_vectors=False, **kwargs)[source]¶
Bases: VectorScene

This scene contains special methods that make it
especially suitable for showing linear transformations.

Parameters:

include_background_plane (bool) – Whether or not to include the background plane in the scene.

include_foreground_plane (bool) – Whether or not to include the foreground plane in the scene.

background_plane_kwargs (dict[str, Any] | None) – Parameters to be passed to NumberPlane to adjust the background plane.

foreground_plane_kwargs (dict[str, Any] | None) – Parameters to be passed to NumberPlane to adjust the foreground plane.

show_coordinates (bool) – Whether or not to include the coordinates for the background plane.

show_basis_vectors (bool) – Whether to show the basis x_axis -> i_hat and y_axis -> j_hat vectors.

basis_vector_stroke_width (float) – The stroke_width of the basis vectors.

i_hat_color (ParsableManimColor) – The color of the i_hat vector.

j_hat_color (ParsableManimColor) – The color of the j_hat vector.

leave_ghost_vectors (bool) – Indicates the previous position of the basis vectors following a transformation.

kwargs (Any)

Examples

Example: LinearTransformationSceneExample ¶

from manim import *

class LinearTransformationSceneExample(LinearTransformationScene):
def __init__(self, **kwargs):
LinearTransformationScene.__init__(
self,
show_coordinates=True,
leave_ghost_vectors=True,
**kwargs
)

def construct(self):
matrix = [[1, 1], [0, 1]]
self.apply_matrix(matrix)
self.wait()

class LinearTransformationSceneExample(LinearTransformationScene):
def __init__(self, **kwargs):
LinearTransformationScene.__init__(
self,
show_coordinates=True,
leave_ghost_vectors=True,
**kwargs
)

def construct(self):
matrix = [[1, 1], [0, 1]]
self.apply_matrix(matrix)
self.wait()

Methods

add_background_mobject

Adds the mobjects to the special list self.background_mobjects.

add_foreground_mobject

Adds the mobjects to the special list self.foreground_mobjects.

add_moving_mobject

Adds the mobject to the special list self.moving_mobject, and adds a property to the mobject called mobject.target, which keeps track of what the mobject will move to or become etc.

add_special_mobjects

Adds mobjects to a separate list that can be tracked, if these mobjects have some extra importance.

add_title

Adds a title, after scaling it, adding a background rectangle, moving it to the top and adding it to foreground_mobjects adding it as a local variable of self.

add_transformable_label

Method for creating, and animating the addition of a transformable label for the vector.

add_transformable_mobject

Adds the mobjects to the special list self.transformable_mobjects.

add_unit_square

Adds a unit square to the scene via self.get_unit_square.

add_vector

Adds a vector to the scene, and puts it in the special list self.moving_vectors.

apply_function

Applies the given function to each of the mobjects in self.transformable_mobjects, and plays the animation showing this.

apply_inverse

This method applies the linear transformation represented by the inverse of the passed matrix to the number plane, and each vector/similar mobject on it.

apply_inverse_transpose

Applies the inverse of the transformation represented by the given transposed matrix to the number plane and each vector/similar mobject on it.

apply_matrix

Applies the transformation represented by the given matrix to the number plane, and each vector/similar mobject on it.

apply_nonlinear_transformation

Applies the non-linear transformation represented by the given function to the number plane and each vector/similar mobject on it.

apply_transposed_matrix

Applies the transformation represented by the given transposed matrix to the number plane, and each vector/similar mobject on it.

get_ghost_vectors

Returns all ghost vectors ever added to self.

get_matrix_transformation

Returns a function corresponding to the linear transformation represented by the matrix passed.

get_moving_mobject_movement

This method returns an animation that moves a mobject in "self.moving_mobjects"  to its corresponding .target value.

get_piece_movement

This method returns an animation that moves an arbitrary mobject in "pieces" to its corresponding .target value.

get_transformable_label_movement

This method returns an animation that moves all labels in "self.transformable_labels" to its corresponding .target .

get_transposed_matrix_transformation

Returns a function corresponding to the linear transformation represented by the transposed matrix passed.

get_unit_square

Returns a unit square for the current NumberPlane.

get_vector_movement

This method returns an animation that moves a mobject in "self.moving_vectors"  to its corresponding .target value.

setup

This is meant to be implemented by any scenes which are commonly subclassed, and have some common setup involved before the construct method is called.

update_default_configs

write_vector_coordinates

Returns a column matrix indicating the vector coordinates, after writing them to the screen, and adding them to the special list self.foreground_mobjects

Attributes

camera

time

The time since the start of the scene.

add_background_mobject(*mobjects)[source]¶
Adds the mobjects to the special list
self.background_mobjects.

Parameters:
*mobjects (Mobject) – The mobjects to add to the list.

Return type:
None

add_foreground_mobject(*mobjects)[source]¶
Adds the mobjects to the special list
self.foreground_mobjects.

Parameters:
*mobjects (Mobject) – The mobjects to add to the list

Return type:
None

add_moving_mobject(mobject, target_mobject=None)[source]¶
Adds the mobject to the special list
self.moving_mobject, and adds a property
to the mobject called mobject.target, which
keeps track of what the mobject will move to
or become etc.

Parameters:

mobject (Mobject) – The mobjects to add to the list

target_mobject (Mobject | None) – What the moving_mobject goes to, etc.

Return type:
None

add_special_mobjects(mob_list, *mobs_to_add)[source]¶
Adds mobjects to a separate list that can be tracked,
if these mobjects have some extra importance.

Parameters:

mob_list (list[Mobject]) – The special list to which you want to add
these mobjects.

*mobs_to_add (Mobject) – The mobjects to add.

Return type:
None

add_title(title, scale_factor=1.5, animate=False)[source]¶
Adds a title, after scaling it, adding a background rectangle,
moving it to the top and adding it to foreground_mobjects adding
it as a local variable of self. Returns the Scene.

Parameters:

title (str | MathTex | Tex) – What the title should be.

scale_factor (float) – How much the title should be scaled by.

animate (bool) – Whether or not to animate the addition.

Returns:
The scene with the title added to it.

Return type:
LinearTransformationScene

add_transformable_label(vector, label, transformation_name='L', new_label=None, **kwargs)[source]¶
Method for creating, and animating the addition of
a transformable label for the vector.

Parameters:

vector (Vector) – The vector for which the label must be added.

label (MathTex | str) – The MathTex/string of the label.

transformation_name (str | MathTex) – The name to give the transformation as a label.

new_label (str | MathTex | None) – What the label should display after a Linear Transformation

**kwargs (Any) – Any valid keyword argument of get_vector_label

Returns:
The MathTex of the label.

Return type:
MathTex

add_transformable_mobject(*mobjects)[source]¶
Adds the mobjects to the special list
self.transformable_mobjects.

Parameters:
*mobjects (Mobject) – The mobjects to add to the list.

Return type:
None

add_unit_square(animate=False, **kwargs)[source]¶
Adds a unit square to the scene via
self.get_unit_square.

Parameters:

animate (bool) – Whether or not to animate the addition
with DrawBorderThenFill.

**kwargs (Any) – Any valid keyword arguments of
self.get_unit_square()

Returns:
The unit square.

Return type:
Square

add_vector(vector, color=ManimColor('#FFFF00'), animate=False, **kwargs)[source]¶
Adds a vector to the scene, and puts it in the special
list self.moving_vectors.

Parameters:

vector (Arrow | list | tuple | ndarray) – It can be a pre-made graphical vector, or the
coordinates of one.

color (ParsableManimColor) – The string of the hex color of the vector.
This is only taken into consideration if
‘vector’ is not an Arrow. Defaults to YELLOW.

**kwargs (Any) – Any valid keyword argument of VectorScene.add_vector.

animate (bool)

**kwargs

Returns:
The arrow representing the vector.

Return type:
Arrow

apply_function(function, added_anims=[], **kwargs)[source]¶
Applies the given function to each of the mobjects in
self.transformable_mobjects, and plays the animation showing
this.

Parameters:

function (MappingFunction) – The function that affects each point
of each mobject in self.transformable_mobjects.

added_anims (list[Animation]) – Any other animations that need to be played
simultaneously with this.

**kwargs (Any) – Any valid keyword argument of a self.play() call.

Return type:
None

apply_inverse(matrix, **kwargs)[source]¶
This method applies the linear transformation
represented by the inverse of the passed matrix
to the number plane, and each vector/similar mobject on it.

Parameters:

matrix (ndarray | list | tuple) – The matrix whose inverse is to be applied.

**kwargs (Any) – Any valid keyword argument of self.apply_matrix()

Return type:
None

apply_inverse_transpose(t_matrix, **kwargs)[source]¶
Applies the inverse of the transformation represented
by the given transposed matrix to the number plane and each
vector/similar mobject on it.

Parameters:

t_matrix (ndarray | list | tuple) – The matrix.

**kwargs (Any) – Any valid keyword argument of self.apply_transposed_matrix()

Return type:
None

apply_matrix(matrix, **kwargs)[source]¶
Applies the transformation represented by the
given matrix to the number plane, and each vector/similar
mobject on it.

Parameters:

matrix (ndarray | list | tuple) – The matrix.

**kwargs (Any) – Any valid keyword argument of self.apply_transposed_matrix()

Return type:
None

apply_nonlinear_transformation(function, **kwargs)[source]¶
Applies the non-linear transformation represented
by the given function to the number plane and each
vector/similar mobject on it.

Parameters:

function (Callable[[ndarray], ndarray]) – The function.

**kwargs (Any) – Any valid keyword argument of self.apply_function()

Return type:
None

apply_transposed_matrix(transposed_matrix, **kwargs)[source]¶
Applies the transformation represented by the
given transposed matrix to the number plane,
and each vector/similar mobject on it.

Parameters:

transposed_matrix (ndarray | list | tuple) – The matrix.

**kwargs (Any) – Any valid keyword argument of self.apply_function()

Return type:
None

get_ghost_vectors()[source]¶
Returns all ghost vectors ever added to self. Each element is a VGroup of
two ghost vectors.

Return type:
VGroup

get_matrix_transformation(matrix)[source]¶
Returns a function corresponding to the linear
transformation represented by the matrix passed.

Parameters:
matrix (ndarray | list | tuple) – The matrix.

Return type:
Callable[[TypeAliasForwardRef(‘~manim.typing.Point3D’)], TypeAliasForwardRef(‘~manim.typing.Point3D’)]

get_moving_mobject_movement(func)[source]¶
This method returns an animation that moves a mobject
in “self.moving_mobjects”  to its corresponding .target value.
func is a function that determines where the .target goes.

Parameters:
func (MappingFunction) – The function that determines where the .target of
the moving mobject goes.

Returns:
The animation of the movement.

Return type:
Animation

get_piece_movement(pieces)[source]¶
This method returns an animation that moves an arbitrary
mobject in “pieces” to its corresponding .target value.
If self.leave_ghost_vectors is True, ghosts of the original
positions/mobjects are left on screen

Parameters:
pieces (Iterable[Mobject]) – The pieces for which the movement must be shown.

Returns:
The animation of the movement.

Return type:
Animation

get_transformable_label_movement()[source]¶
This method returns an animation that moves all labels
in “self.transformable_labels” to its corresponding .target .

Returns:
The animation of the movement.

Return type:
Animation

get_transposed_matrix_transformation(transposed_matrix)[source]¶
Returns a function corresponding to the linear
transformation represented by the transposed
matrix passed.

Parameters:
transposed_matrix (ndarray | list | tuple) – The matrix.

Return type:
Callable[[TypeAliasForwardRef(‘~manim.typing.Point3D’)], TypeAliasForwardRef(‘~manim.typing.Point3D’)]

get_unit_square(color=ManimColor('#FFFF00'), opacity=0.3, stroke_width=3)[source]¶
Returns a unit square for the current NumberPlane.

Parameters:

color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | Iterable[TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor')]) – The string of the hex color code of the color wanted.

opacity (float) – The opacity of the square

stroke_width (float) – The stroke_width in pixels of the border of the square

Return type:
Square

get_vector_movement(func)[source]¶
This method returns an animation that moves a mobject
in “self.moving_vectors”  to its corresponding .target value.
func is a function that determines where the .target goes.

Parameters:
func (MappingFunction) – The function that determines where the .target of
the moving mobject goes.

Returns:
The animation of the movement.

Return type:
Animation

setup()[source]¶
This is meant to be implemented by any scenes which
are commonly subclassed, and have some common setup
involved before the construct method is called.

Return type:
None

write_vector_coordinates(vector, **kwargs)[source]¶
Returns a column matrix indicating the vector coordinates,
after writing them to the screen, and adding them to the
special list self.foreground_mobjects

Parameters:

vector (Vector) – The arrow representing the vector.

**kwargs (Any) – Any valid keyword arguments of VectorScene.write_vector_coordinates

Returns:
The column matrix representing the vector.

Return type:
Matrix


---

## VectorScene - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.scene.vector_space_scene.VectorScene.html

VectorScene¶

Qualified name: manim.scene.vector\_space\_scene.VectorScene

class VectorScene(basis_vector_stroke_width=6.0, **kwargs)[source]¶
Bases: Scene

Methods

add_axes

Adds a pair of Axes to the Scene.

add_plane

Adds a NumberPlane object to the background.

add_vector

Returns the Vector after adding it to the Plane.

coords_to_vector

This method writes the vector as a column matrix (henceforth called the label), takes the values in it one by one, and form the corresponding lines that make up the x and y components of the vector.

get_basis_vector_labels

Returns naming labels for the basis vectors.

get_basis_vectors

Returns a VGroup of the Basis Vectors (1,0) and (0,1)

get_vector

Returns an arrow on the Plane given an input numerical vector.

get_vector_label

Returns naming labels for the passed vector.

label_vector

Shortcut method for creating, and animating the addition of a label for the vector.

lock_in_faded_grid

This method freezes the NumberPlane and Axes that were already in the background, and adds new, manipulatable ones to the foreground.

position_x_coordinate

position_y_coordinate

show_ghost_movement

This method plays an animation that partially shows the entire plane moving in the direction of a particular vector.

vector_to_coords

This method displays vector as a Vector() based vector, and then shows the corresponding lines that make up the x and y components of the vector.

write_vector_coordinates

Returns a column matrix indicating the vector coordinates, after writing them to the screen.

Attributes

camera

time

The time since the start of the scene.

Parameters:

basis_vector_stroke_width (float)

kwargs (Any)

add_axes(animate=False, color=ManimColor('#FFFFFF'))[source]¶
Adds a pair of Axes to the Scene.

Parameters:

animate (bool) – Whether or not to animate the addition of the axes through Create.

color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | Iterable[TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor')]) – The color of the axes. Defaults to WHITE.

Return type:
Axes

add_plane(animate=False, **kwargs)[source]¶
Adds a NumberPlane object to the background.

Parameters:

animate (bool) – Whether or not to animate the addition of the plane via Create.

**kwargs (Any) – Any valid keyword arguments accepted by NumberPlane.

Returns:
The NumberPlane object.

Return type:
NumberPlane

add_vector(vector, color=ManimColor('#FFFF00'), animate=True, **kwargs)[source]¶
Returns the Vector after adding it to the Plane.

Parameters:

vector (Arrow | TypeAliasForwardRef('~manim.typing.Vector3DLike')) – It can be a pre-made graphical vector, or the
coordinates of one.

color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | Iterable[TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor')]) – The string of the hex color of the vector.
This is only taken into consideration if
‘vector’ is not an Arrow. Defaults to YELLOW.

animate (bool) – Whether or not to animate the addition of the vector
by using GrowArrow

**kwargs (Any) – Any valid keyword argument of Arrow.
These are only considered if vector is not
an Arrow.

Returns:
The arrow representing the vector.

Return type:
Arrow

coords_to_vector(vector, coords_start=array([2., 2., 0.]), clean_up=True)[source]¶
This method writes the vector as a column matrix (henceforth called the label),
takes the values in it one by one, and form the corresponding
lines that make up the x and y components of the vector. Then, an
Vector() based vector is created between the lines on the Screen.

Parameters:

vector (Vector2DLike) – The vector to show.

coords_start (Point3DLike) – The starting point of the location of
the label of the vector that shows it
numerically.
Defaults to 2 * RIGHT + 2 * UP or (2,2)

clean_up (bool) – Whether or not to remove whatever
this method did after it’s done.

Return type:
None

get_basis_vector_labels(**kwargs)[source]¶
Returns naming labels for the basis vectors.

Parameters:
**kwargs (Any) –
Any valid keyword arguments of get_vector_label:vector,
label (str,MathTex)
at_tip (bool=False),
direction (str=”left”),
rotate (bool),
color (str),
label_scale_factor=VECTOR_LABEL_SCALE_FACTOR (int, float),

Return type:
VGroup

get_basis_vectors(i_hat_color=ManimColor('#83C167'), j_hat_color=ManimColor('#FC6255'))[source]¶
Returns a VGroup of the Basis Vectors (1,0) and (0,1)

Parameters:

i_hat_color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | Iterable[TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor')]) – The hex colour to use for the basis vector in the x direction

j_hat_color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | Iterable[TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor')]) – The hex colour to use for the basis vector in the y direction

Returns:
VGroup of the Vector Mobjects representing the basis vectors.

Return type:
VGroup

get_vector(numerical_vector, **kwargs)[source]¶
Returns an arrow on the Plane given an input numerical vector.

Parameters:

numerical_vector (Vector3DLike) – The Vector to plot.

**kwargs (Any) – Any valid keyword argument of Arrow.

Returns:
The Arrow representing the Vector.

Return type:
Arrow

get_vector_label(vector, label, at_tip=False, direction='left', rotate=False, color=None, label_scale_factor=0.8)[source]¶
Returns naming labels for the passed vector.

Parameters:

vector (Vector) – Vector Object for which to get the label.

at_tip (bool) – Whether or not to place the label at the tip of the vector.

direction (str) – If the label should be on the “left” or right of the vector.

rotate (bool) – Whether or not to rotate it to align it with the vector.

color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | None) – The color to give the label.

label_scale_factor (float) – How much to scale the label by.

label (MathTex | str)

Returns:
The MathTex of the label.

Return type:
MathTex

label_vector(vector, label, animate=True, **kwargs)[source]¶
Shortcut method for creating, and animating the addition of
a label for the vector.

Parameters:

vector (Vector) – The vector for which the label must be added.

label (MathTex | str) – The MathTex/string of the label.

animate (bool) – Whether or not to animate the labelling w/ Write

**kwargs (Any) – Any valid keyword argument of get_vector_label

Returns:
The MathTex of the label.

Return type:
MathTex

lock_in_faded_grid(dimness=0.7, axes_dimness=0.5)[source]¶
This method freezes the NumberPlane and Axes that were already
in the background, and adds new, manipulatable ones to the foreground.

Parameters:

dimness (float) – The required dimness of the NumberPlane

axes_dimness (float) – The required dimness of the Axes.

Return type:
None

show_ghost_movement(vector)[source]¶
This method plays an animation that partially shows the entire plane moving
in the direction of a particular vector. This is useful when you wish to
convey the idea of mentally moving the entire plane in a direction, without
actually moving the plane.

Parameters:
vector (Arrow | TypeAliasForwardRef('~manim.typing.Vector2DLike') | TypeAliasForwardRef('~manim.typing.Vector3DLike')) – The vector which indicates the direction of movement.

Return type:
None

vector_to_coords(vector, integer_labels=True, clean_up=True)[source]¶
This method displays vector as a Vector() based vector, and then shows
the corresponding lines that make up the x and y components of the vector.
Then, a column matrix (henceforth called the label) is created near the
head of the Vector.

Parameters:

vector (Vector3DLike) – The vector to show.

integer_labels (bool) – Whether or not to round the value displayed.
in the vector’s label to the nearest integer

clean_up (bool) – Whether or not to remove whatever
this method did after it’s done.

Return type:
tuple[Matrix, Line, Line]

write_vector_coordinates(vector, **kwargs)[source]¶
Returns a column matrix indicating the vector coordinates,
after writing them to the screen.

Parameters:

vector (Vector) – The arrow representing the vector.

**kwargs (Any) – Any valid keyword arguments of coordinate_label():

Returns:
The column matrix representing the vector.

Return type:
Matrix


---

## vector_space_scene - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.scene.vector_space_scene.html

vector_space_scene¶

A scene suitable for vector spaces.

Classes

LinearTransformationScene

This scene contains special methods that make it especially suitable for showing linear transformations.

VectorScene
