# Transform Matching Parts


---

## TransformMatchingAbstractBase - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform_matching_parts.TransformMatchingAbstractBase.html

TransformMatchingAbstractBase¶

Qualified name: manim.animation.transform\_matching\_parts.TransformMatchingAbstractBase

class TransformMatchingAbstractBase(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: AnimationGroup

Abstract base class for transformations that keep track of matching parts.

Subclasses have to implement the two static methods
get_mobject_parts() and
get_mobject_key().

Basically, this transformation first maps all submobjects returned
by the get_mobject_parts method to certain keys by applying the
get_mobject_key method. Then, submobjects with matching keys
are transformed into each other.

Parameters:

mobject (Mobject) – The starting Mobject.

target_mobject (Mobject) – The target Mobject.

transform_mismatches (bool) – Controls whether submobjects without a matching key are transformed
into each other by using Transform. Default: False.

fade_transform_mismatches (bool) – Controls whether submobjects without a matching key are transformed
into each other by using FadeTransform. Default: False.

key_map (dict | None) – Optional. A dictionary mapping keys belonging to some of the starting mobject’s
submobjects (i.e., the return values of the get_mobject_key method)
to some keys belonging to the target mobject’s submobjects that should
be transformed although the keys don’t match.

kwargs – All further keyword arguments are passed to the submobject transformations.

Note

If neither transform_mismatches nor fade_transform_mismatches
are set to True, submobjects without matching keys in the starting
mobject are faded out in the direction of the unmatched submobjects in
the target mobject, and unmatched submobjects in the target mobject
are faded in from the direction of the unmatched submobjects in the
start mobject.

Methods

clean_up_from_scene

Clean up the Scene after finishing the animation.

get_mobject_key

get_mobject_parts

get_shape_map

Attributes

run_time

_original__init__(mobject, target_mobject, transform_mismatches=False, fade_transform_mismatches=False, key_map=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

target_mobject (Mobject)

transform_mismatches (bool)

fade_transform_mismatches (bool)

key_map (dict | None)

clean_up_from_scene(scene)[source]¶
Clean up the Scene after finishing the animation.

This includes to remove() the Animation’s
Mobject if the animation is a remover.

Parameters:
scene (Scene) – The scene the animation should be cleaned up from.

Return type:
None


---

## TransformMatchingShapes - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform_matching_parts.TransformMatchingShapes.html

TransformMatchingShapes¶

Qualified name: manim.animation.transform\_matching\_parts.TransformMatchingShapes

class TransformMatchingShapes(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: TransformMatchingAbstractBase

An animation trying to transform groups by matching the shape
of their submobjects.

Two submobjects match if the hash of their point coordinates after
normalization (i.e., after translation to the origin, fixing the submobject
height at 1 unit, and rounding the coordinates to three decimal places)
matches.

See also

TransformMatchingAbstractBase

Examples

Example: Anagram ¶

from manim import *

class Anagram(Scene):
def construct(self):
src = Text("the morse code")
tar = Text("here come dots")
self.play(Write(src))
self.wait(0.5)
self.play(TransformMatchingShapes(src, tar, path_arc=PI/2))
self.wait(0.5)

class Anagram(Scene):
def construct(self):
src = Text("the morse code")
tar = Text("here come dots")
self.play(Write(src))
self.wait(0.5)
self.play(TransformMatchingShapes(src, tar, path_arc=PI/2))
self.wait(0.5)

Methods

get_mobject_key

get_mobject_parts

Attributes

run_time

Parameters:

mobject (Mobject)

target_mobject (Mobject)

transform_mismatches (bool)

fade_transform_mismatches (bool)

key_map (dict | None)

_original__init__(mobject, target_mobject, transform_mismatches=False, fade_transform_mismatches=False, key_map=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

target_mobject (Mobject)

transform_mismatches (bool)

fade_transform_mismatches (bool)

key_map (dict | None)


---

## TransformMatchingTex - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.transform_matching_parts.TransformMatchingTex.html

TransformMatchingTex¶

Qualified name: manim.animation.transform\_matching\_parts.TransformMatchingTex

class TransformMatchingTex(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: TransformMatchingAbstractBase

A transformation trying to transform rendered LaTeX strings.

Two submobjects match if their tex_string matches.

See also

TransformMatchingAbstractBase

Examples

Example: MatchingEquationParts ¶

from manim import *

class MatchingEquationParts(Scene):
def construct(self):
variables = VGroup(MathTex("a"), MathTex("b"), MathTex("c")).arrange_submobjects().shift(UP)

eq1 = MathTex("{{x}}^2", "+", "{{y}}^2", "=", "{{z}}^2")
eq2 = MathTex("{{a}}^2", "+", "{{b}}^2", "=", "{{c}}^2")
eq3 = MathTex("{{a}}^2", "=", "{{c}}^2", "-", "{{b}}^2")

self.add(eq1)
self.wait(0.5)
self.play(TransformMatchingTex(Group(eq1, variables), eq2))
self.wait(0.5)
self.play(TransformMatchingTex(eq2, eq3))
self.wait(0.5)

class MatchingEquationParts(Scene):
def construct(self):
variables = VGroup(MathTex("a"), MathTex("b"), MathTex("c")).arrange_submobjects().shift(UP)

eq1 = MathTex("{{x}}^2", "+", "{{y}}^2", "=", "{{z}}^2")
eq2 = MathTex("{{a}}^2", "+", "{{b}}^2", "=", "{{c}}^2")
eq3 = MathTex("{{a}}^2", "=", "{{c}}^2", "-", "{{b}}^2")

self.add(eq1)
self.wait(0.5)
self.play(TransformMatchingTex(Group(eq1, variables), eq2))
self.wait(0.5)
self.play(TransformMatchingTex(eq2, eq3))
self.wait(0.5)

Methods

get_mobject_key

get_mobject_parts

Attributes

run_time

Parameters:

mobject (Mobject)

target_mobject (Mobject)

transform_mismatches (bool)

fade_transform_mismatches (bool)

key_map (dict | None)

_original__init__(mobject, target_mobject, transform_mismatches=False, fade_transform_mismatches=False, key_map=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject)

target_mobject (Mobject)

transform_mismatches (bool)

fade_transform_mismatches (bool)

key_map (dict | None)
