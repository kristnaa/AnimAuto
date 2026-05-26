# Fading


---

## FadeIn - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.fading.FadeIn.html

FadeIn¶

Qualified name: manim.animation.fading.FadeIn

class FadeIn(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: _Fade

Fade in Mobject s.

Parameters:

mobjects (Mobject) – The mobjects to be faded in.

shift – The vector by which the mobject shifts while being faded in.

target_position – The position from which the mobject starts while being faded in. In case
another mobject is given as target position, its center is used.

scale – The factor by which the mobject is scaled initially before being rescaling to
its original size while being faded in.

kwargs (Any)

Examples

Example: FadeInExample ¶

from manim import *

class FadeInExample(Scene):
def construct(self):
dot = Dot(UP * 2 + LEFT)
self.add(dot)
tex = Tex(
"FadeIn with ", "shift ", r" or target\_position", " and scale"
).scale(1)
animations = [
FadeIn(tex[0]),
FadeIn(tex[1], shift=DOWN),
FadeIn(tex[2], target_position=dot),
FadeIn(tex[3], scale=1.5),
]
self.play(AnimationGroup(*animations, lag_ratio=0.5))

class FadeInExample(Scene):
def construct(self):
dot = Dot(UP * 2 + LEFT)
self.add(dot)
tex = Tex(
"FadeIn with ", "shift ", r" or target\_position", " and scale"
).scale(1)
animations = [
FadeIn(tex[0]),
FadeIn(tex[1], shift=DOWN),
FadeIn(tex[2], target_position=dot),
FadeIn(tex[3], scale=1.5),
]
self.play(AnimationGroup(*animations, lag_ratio=0.5))

Methods

create_starting_mobject

create_target

Attributes

path_arc

path_func

run_time

_original__init__(*mobjects, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobjects (Mobject)

kwargs (Any)

Return type:
None


---

## FadeOut - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.fading.FadeOut.html

FadeOut¶

Qualified name: manim.animation.fading.FadeOut

class FadeOut(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: _Fade

Fade out Mobject s.

Parameters:

mobjects (Mobject) – The mobjects to be faded out.

shift – The vector by which the mobject shifts while being faded out.

target_position – The position to which the mobject moves while being faded out. In case another
mobject is given as target position, its center is used.

scale – The factor by which the mobject is scaled while being faded out.

kwargs (Any)

Examples

Example: FadeInExample ¶

from manim import *

class FadeInExample(Scene):
def construct(self):
dot = Dot(UP * 2 + LEFT)
self.add(dot)
tex = Tex(
"FadeOut with ", "shift ", r" or target\_position", " and scale"
).scale(1)
animations = [
FadeOut(tex[0]),
FadeOut(tex[1], shift=DOWN),
FadeOut(tex[2], target_position=dot),
FadeOut(tex[3], scale=0.5),
]
self.play(AnimationGroup(*animations, lag_ratio=0.5))

class FadeInExample(Scene):
def construct(self):
dot = Dot(UP * 2 + LEFT)
self.add(dot)
tex = Tex(
"FadeOut with ", "shift ", r" or target\_position", " and scale"
).scale(1)
animations = [
FadeOut(tex[0]),
FadeOut(tex[1], shift=DOWN),
FadeOut(tex[2], target_position=dot),
FadeOut(tex[3], scale=0.5),
]
self.play(AnimationGroup(*animations, lag_ratio=0.5))

Methods

clean_up_from_scene

Clean up the Scene after finishing the animation.

create_target

Attributes

path_arc

path_func

run_time

_original__init__(*mobjects, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobjects (Mobject)

kwargs (Any)

Return type:
None

clean_up_from_scene(scene)[source]¶
Clean up the Scene after finishing the animation.

This includes to remove() the Animation’s
Mobject if the animation is a remover.

Parameters:
scene (Scene) – The scene the animation should be cleaned up from.

Return type:
None
