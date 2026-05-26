# Mapping Camera


---

## MappingCamera - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.camera.mapping_camera.MappingCamera.html

MappingCamera¶

Qualified name: manim.camera.mapping\_camera.MappingCamera

class MappingCamera(mapping_func=<function MappingCamera.<lambda>>, min_num_curves=50, allow_object_intrusion=False, **kwargs)[source]¶
Bases: Camera

Parameters:

mapping_func (callable) – Function to map 3D points to new 3D points (identity by default).

min_num_curves (int) – Minimum number of curves for VMobjects to avoid visual glitches.

allow_object_intrusion (bool) – If True, modifies original mobjects; else works on copies.

kwargs (dict) – Additional arguments passed to Camera base class.

Methods

capture_mobjects

Capture mobjects for rendering after applying the spatial mapping.

points_to_pixel_coords

Attributes

background_color

background_opacity

capture_mobjects(mobjects, **kwargs)[source]¶
Capture mobjects for rendering after applying the spatial mapping.

Copies mobjects unless intrusion is allowed, and ensures
vector objects have enough curves for smooth distortion.


---

## OldMultiCamera - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.camera.mapping_camera.OldMultiCamera.html

OldMultiCamera¶

Qualified name: manim.camera.mapping\_camera.OldMultiCamera

class OldMultiCamera(*cameras_with_start_positions, **kwargs)[source]¶
Bases: Camera

Parameters:
cameras_with_start_positions (tuple) – Tuples of (Camera, (start_y, start_x)) indicating camera and
its pixel offset on the final frame.

Methods

capture_mobjects

Capture mobjects by printing them on pixel_array.

init_background

Initialize the background.

set_background

Sets the background to the passed pixel_array after converting to valid RGB values.

set_pixel_array

Sets the pixel array of the camera to the passed pixel array.

Attributes

background_color

background_opacity

capture_mobjects(mobjects, **kwargs)[source]¶
Capture mobjects by printing them on pixel_array.

This is the essential function that converts the contents of a Scene
into an array, which is then converted to an image or video.

Parameters:

mobjects – Mobjects to capture.

kwargs – Keyword arguments to be passed to get_mobjects_to_display().

Notes

For a list of classes that can currently be rendered, see display_funcs().

init_background()[source]¶
Initialize the background.
If self.background_image is the path of an image
the image is set as background; else, the default
background color fills the background.

set_background(pixel_array, **kwargs)[source]¶
Sets the background to the passed pixel_array after converting
to valid RGB values.

Parameters:

pixel_array – The pixel array to set the background to.

convert_from_floats – Whether or not to convert floats values to proper RGB valid ones, by default False

set_pixel_array(pixel_array, **kwargs)[source]¶
Sets the pixel array of the camera to the passed pixel array.

Parameters:

pixel_array – The pixel array to convert and then set as the camera’s pixel array.

convert_from_floats – Whether or not to convert float values to proper RGB values, by default False


---

## SplitScreenCamera - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.camera.mapping_camera.SplitScreenCamera.html

SplitScreenCamera¶

Qualified name: manim.camera.mapping\_camera.SplitScreenCamera

class SplitScreenCamera(left_camera, right_camera, **kwargs)[source]¶
Bases: OldMultiCamera

Initializes a split screen camera setup with two side-by-side cameras.

Parameters:

left_camera (Camera)

right_camera (Camera)

kwargs (dict)

Methods

Attributes

background_color

background_opacity


---

## mapping_camera - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.camera.mapping_camera.html

mapping_camera¶

A camera module that supports spatial mapping between objects for distortion effects.

Classes

MappingCamera

OldMultiCamera

SplitScreenCamera

Initializes a split screen camera setup with two side-by-side cameras.
