# Animation


---

## Add - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.animation.Add.html

Add¶

Qualified name: manim.animation.animation.Add

class Add(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Animation

Add Mobjects to a scene, without animating them in any other way. This
is similar to the Scene.add() method, but Add is an
animation which can be grouped into other animations.

Parameters:

mobjects (Mobject) – One Mobject or more to add to a scene.

run_time (float) – The duration of the animation after adding the mobjects. Defaults
to 0, which means this is an instant animation without extra wait time
after adding them.

**kwargs (Any) – Additional arguments to pass to the parent Animation class.

Examples

Example: DefaultAddScene ¶

from manim import *

class DefaultAddScene(Scene):
def construct(self):
text_1 = Text("I was added with Add!")
text_2 = Text("Me too!")
text_3 = Text("And me!")
texts = VGroup(text_1, text_2, text_3).arrange(DOWN)
rect = SurroundingRectangle(texts, buff=0.5)

self.play(
Create(rect, run_time=3.0),
Succession(
Wait(1.0),
# You can Add a Mobject in the middle of an animation...
Add(text_1),
Wait(1.0),
# ...or multiple Mobjects at once!
Add(text_2, text_3),
),
)
self.wait()

class DefaultAddScene(Scene):
def construct(self):
text_1 = Text("I was added with Add!")
text_2 = Text("Me too!")
text_3 = Text("And me!")
texts = VGroup(text_1, text_2, text_3).arrange(DOWN)
rect = SurroundingRectangle(texts, buff=0.5)

self.play(
Create(rect, run_time=3.0),
Succession(
Wait(1.0),
# You can Add a Mobject in the middle of an animation...
Add(text_1),
Wait(1.0),
# ...or multiple Mobjects at once!
Add(text_2, text_3),
),
)
self.wait()

Example: AddWithRunTimeScene ¶

from manim import *

class AddWithRunTimeScene(Scene):
def construct(self):
# A 5x5 grid of circles
circles = VGroup(
*[Circle(radius=0.5) for _ in range(25)]
).arrange_in_grid(5, 5)

self.play(
Succession(
# Add a run_time of 0.2 to wait for 0.2 seconds after
# adding the circle, instead of using Wait(0.2) after Add!
*[Add(circle, run_time=0.2) for circle in circles],
rate_func=smooth,
)
)
self.wait()

class AddWithRunTimeScene(Scene):
def construct(self):
# A 5x5 grid of circles
circles = VGroup(
*[Circle(radius=0.5) for _ in range(25)]
).arrange_in_grid(5, 5)

self.play(
Succession(
# Add a run_time of 0.2 to wait for 0.2 seconds after
# adding the circle, instead of using Wait(0.2) after Add!
*[Add(circle, run_time=0.2) for circle in circles],
rate_func=smooth,
)
)
self.wait()

Methods

begin

Begin the animation.

clean_up_from_scene

Clean up the Scene after finishing the animation.

finish

Finish the animation.

interpolate

Set the animation progress.

update_mobjects

Updates things like starting_mobject, and (for Transforms) target_mobject.

Attributes

run_time

_original__init__(*mobjects, run_time=0.0, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobjects (Mobject)

run_time (float)

kwargs (Any)

Return type:
None

begin()[source]¶
Begin the animation.

This method is called right as an animation is being played. As much
initialization as possible, especially any mobject copying, should live in this
method.

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

finish()[source]¶
Finish the animation.

This method gets called when the animation is over.

Return type:
None

interpolate(alpha)[source]¶
Set the animation progress.

This method gets called for every frame during an animation.

Parameters:
alpha (float) – The relative time to set the animation to, 0 meaning the start, 1 meaning
the end.

Return type:
None

update_mobjects(dt)[source]¶
Updates things like starting_mobject, and (for
Transforms) target_mobject.  Note, since typically
(always?) self.mobject will have its updating
suspended during the animation, this will do
nothing to self.mobject.

Parameters:
dt (float)

Return type:
None


---

## Animation - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.animation.Animation.html

Animation¶

Qualified name: manim.animation.animation.Animation

class Animation(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: object

An animation.

Animations have a fixed time span.

Parameters:

mobject – The mobject to be animated. This is not required for all types of animations.

lag_ratio – Defines the delay after which the animation is applied to submobjects. This lag
is relative to the duration of the animation.

This does not influence the total
runtime of the animation. Instead the runtime of individual animations is
adjusted so that the complete animation has the defined run time.

run_time – The duration of the animation in seconds.

rate_func – The function defining the animation progress based on the relative runtime (see  rate_functions) .

For example rate_func(0.5) is the proportion of the animation that is done
after half of the animations run time.

reverse_rate_function – Reverses the rate function of the animation. Setting reverse_rate_function
does not have any effect on remover or introducer. These need to be
set explicitly if an introducer-animation should be turned into a remover one
and vice versa.

name – The name of the animation. This gets displayed while rendering the animation.
Defaults to <class-name>(<Mobject-name>).

remover – Whether the given mobject should be removed from the scene after this animation.

suspend_mobject_updating – Whether updaters of the mobject should be suspended during the animation.

Return type:
Self

Note

In the current implementation of this class, the specified rate function is applied
within Animation.interpolate_mobject() call as part of the call to
Animation.interpolate_submobject(). For subclasses of Animation
that are implemented by overriding interpolate_mobject(), the rate function
has to be applied manually (e.g., by passing self.rate_func(alpha) instead
of just alpha).

Examples

Example: LagRatios ¶

from manim import *

class LagRatios(Scene):
def construct(self):
ratios = [0, 0.1, 0.5, 1, 2]  # demonstrated lag_ratios

# Create dot groups
group = VGroup(*[Dot() for _ in range(4)]).arrange_submobjects()
groups = VGroup(*[group.copy() for _ in ratios]).arrange_submobjects(buff=1)
self.add(groups)

# Label groups
self.add(Text("lag_ratio = ", font_size=36).next_to(groups, UP, buff=1.5))
for group, ratio in zip(groups, ratios):
self.add(Text(str(ratio), font_size=36).next_to(group, UP))

#Animate groups with different lag_ratios
self.play(AnimationGroup(*[
group.animate(lag_ratio=ratio, run_time=1.5).shift(DOWN * 2)
for group, ratio in zip(groups, ratios)
]))

# lag_ratio also works recursively on nested submobjects:
self.play(groups.animate(run_time=1, lag_ratio=0.1).shift(UP * 2))

class LagRatios(Scene):
def construct(self):
ratios = [0, 0.1, 0.5, 1, 2]  # demonstrated lag_ratios

# Create dot groups
group = VGroup(*[Dot() for _ in range(4)]).arrange_submobjects()
groups = VGroup(*[group.copy() for _ in ratios]).arrange_submobjects(buff=1)
self.add(groups)

# Label groups
self.add(Text("lag_ratio = ", font_size=36).next_to(groups, UP, buff=1.5))
for group, ratio in zip(groups, ratios):
self.add(Text(str(ratio), font_size=36).next_to(group, UP))

#Animate groups with different lag_ratios
self.play(AnimationGroup(*[
group.animate(lag_ratio=ratio, run_time=1.5).shift(DOWN * 2)
for group, ratio in zip(groups, ratios)
]))

# lag_ratio also works recursively on nested submobjects:
self.play(groups.animate(run_time=1, lag_ratio=0.1).shift(UP * 2))

Methods

begin

Begin the animation.

clean_up_from_scene

Clean up the Scene after finishing the animation.

copy

Create a copy of the animation.

create_starting_mobject

finish

Finish the animation.

get_all_families_zipped

get_all_mobjects

Get all mobjects involved in the animation.

get_all_mobjects_to_update

Get all mobjects to be updated during the animation.

get_rate_func

Get the rate function of the animation.

get_run_time

Get the run time of the animation.

get_sub_alpha

Get the animation progress of any submobjects subanimation.

interpolate

Set the animation progress.

interpolate_mobject

Interpolates the mobject of the Animation based on alpha value.

interpolate_submobject

is_introducer

Test if the animation is an introducer.

is_remover

Test if the animation is a remover.

set_default

Sets the default values of keyword arguments.

set_name

Set the name of the animation.

set_rate_func

Set the rate function of the animation.

set_run_time

Set the run time of the animation.

update_mobjects

Updates things like starting_mobject, and (for Transforms) target_mobject.

Attributes

run_time

_original__init__(mobject, lag_ratio=0.0, run_time=1.0, rate_func=<function smooth>, reverse_rate_function=False, name=None, remover=False, suspend_mobject_updating=True, introducer=False, *, _on_finish=<function Animation.<lambda>>, use_override=True)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

mobject (Mobject | OpenGLMobject | None)

lag_ratio (float)

run_time (float)

rate_func (Callable[[float], float])

reverse_rate_function (bool)

name (str)

remover (bool)

suspend_mobject_updating (bool)

introducer (bool)

_on_finish (Callable[[], None])

use_override (bool)

Return type:
None

_setup_scene(scene)[source]¶
Setup up the Scene before starting the animation.

This includes to add() the Animation’s
Mobject if the animation is an introducer.

Parameters:
scene (Scene) – The scene the animation should be cleaned up from.

Return type:
None

begin()[source]¶
Begin the animation.

This method is called right as an animation is being played. As much
initialization as possible, especially any mobject copying, should live in this
method.

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

copy()[source]¶
Create a copy of the animation.

Returns:
A copy of self

Return type:
Animation

finish()[source]¶
Finish the animation.

This method gets called when the animation is over.

Return type:
None

get_all_mobjects()[source]¶
Get all mobjects involved in the animation.

Ordering must match the ordering of arguments to interpolate_submobject

Returns:
The sequence of mobjects.

Return type:
Sequence[Mobject]

get_all_mobjects_to_update()[source]¶
Get all mobjects to be updated during the animation.

Returns:
The list of mobjects to be updated during the animation.

Return type:
List[Mobject]

get_rate_func()[source]¶
Get the rate function of the animation.

Returns:
The rate function of the animation.

Return type:
Callable[[float], float]

get_run_time()[source]¶
Get the run time of the animation.

Returns:
The time the animation takes in seconds.

Return type:
float

get_sub_alpha(alpha, index, num_submobjects)[source]¶
Get the animation progress of any submobjects subanimation.

Parameters:

alpha (float) – The overall animation progress

index (int) – The index of the subanimation.

num_submobjects (int) – The total count of subanimations.

Returns:
The progress of the subanimation.

Return type:
float

interpolate(alpha)[source]¶
Set the animation progress.

This method gets called for every frame during an animation.

Parameters:
alpha (float) – The relative time to set the animation to, 0 meaning the start, 1 meaning
the end.

Return type:
None

interpolate_mobject(alpha)[source]¶
Interpolates the mobject of the Animation based on alpha value.

Parameters:
alpha (float) – A float between 0 and 1 expressing the ratio to which the animation
is completed. For example, alpha-values of 0, 0.5, and 1 correspond
to the animation being completed 0%, 50%, and 100%, respectively.

Return type:
None

is_introducer()[source]¶
Test if the animation is an introducer.

Returns:
True if the animation is an introducer, False otherwise.

Return type:
bool

is_remover()[source]¶
Test if the animation is a remover.

Returns:
True if the animation is a remover, False otherwise.

Return type:
bool

classmethod set_default(**kwargs)[source]¶
Sets the default values of keyword arguments.

If this method is called without any additional keyword
arguments, the original default values of the initialization
method of this class are restored.

Parameters:
kwargs – Passing any keyword argument will update the default
values of the keyword arguments of the initialization
function of this class.

Return type:
None

Examples

Example: ChangeDefaultAnimation ¶

from manim import *

class ChangeDefaultAnimation(Scene):
def construct(self):
Rotate.set_default(run_time=2, rate_func=rate_functions.linear)
Indicate.set_default(color=None)

S = Square(color=BLUE, fill_color=BLUE, fill_opacity=0.25)
self.add(S)
self.play(Rotate(S, PI))
self.play(Indicate(S))

Rotate.set_default()
Indicate.set_default()

class ChangeDefaultAnimation(Scene):
def construct(self):
Rotate.set_default(run_time=2, rate_func=rate_functions.linear)
Indicate.set_default(color=None)

S = Square(color=BLUE, fill_color=BLUE, fill_opacity=0.25)
self.add(S)
self.play(Rotate(S, PI))
self.play(Indicate(S))

Rotate.set_default()
Indicate.set_default()

set_name(name)[source]¶
Set the name of the animation.

Parameters:
name (str) – The new name of the animation.

Returns:
self

Return type:
Animation

set_rate_func(rate_func)[source]¶
Set the rate function of the animation.

Parameters:
rate_func (Callable[[float], float]) – The new function defining the animation progress based on the
relative runtime (see rate_functions).

Returns:
self

Return type:
Animation

set_run_time(run_time)[source]¶
Set the run time of the animation.

Parameters:

run_time (float) – The new time the animation should take in seconds.

note:: (..) – The run_time of an animation should not be changed while it is already
running.

Returns:
self

Return type:
Animation

update_mobjects(dt)[source]¶
Updates things like starting_mobject, and (for
Transforms) target_mobject.  Note, since typically
(always?) self.mobject will have its updating
suspended during the animation, this will do
nothing to self.mobject.

Parameters:
dt (float)

Return type:
None


---

## Wait - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.animation.animation.Wait.html

Wait¶

Qualified name: manim.animation.animation.Wait

class Wait(mobject=None, *args, use_override=True, **kwargs)[source]¶
Bases: Animation

A “no operation” animation.

Parameters:

run_time (float) – The amount of time that should pass.

stop_condition (Callable[[], bool] | None) – A function without positional arguments that evaluates to a boolean.
The function is evaluated after every new frame has been rendered.
Playing the animation stops after the return value is truthy, or
after the specified run_time has passed.

frozen_frame (bool | None) – Controls whether or not the wait animation is static, i.e., corresponds
to a frozen frame. If False is passed, the render loop still
progresses through the animation as usual and (among other things)
continues to call updater functions. If None (the default value),
the Scene.play() call tries to determine whether the Wait call
can be static or not itself via Scene.should_mobjects_update().

kwargs – Keyword arguments to be passed to the parent class, Animation.

rate_func (Callable[[float], float])

Methods

begin

Begin the animation.

clean_up_from_scene

Clean up the Scene after finishing the animation.

finish

Finish the animation.

interpolate

Set the animation progress.

update_mobjects

Updates things like starting_mobject, and (for Transforms) target_mobject.

Attributes

run_time

_original__init__(run_time=1, stop_condition=None, frozen_frame=None, rate_func=<function linear>, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

run_time (float)

stop_condition (Callable[[], bool] | None)

frozen_frame (bool | None)

rate_func (Callable[[float], float])

begin()[source]¶
Begin the animation.

This method is called right as an animation is being played. As much
initialization as possible, especially any mobject copying, should live in this
method.

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

finish()[source]¶
Finish the animation.

This method gets called when the animation is over.

Return type:
None

interpolate(alpha)[source]¶
Set the animation progress.

This method gets called for every frame during an animation.

Parameters:
alpha (float) – The relative time to set the animation to, 0 meaning the start, 1 meaning
the end.

Return type:
None

update_mobjects(dt)[source]¶
Updates things like starting_mobject, and (for
Transforms) target_mobject.  Note, since typically
(always?) self.mobject will have its updating
suspended during the animation, this will do
nothing to self.mobject.

Parameters:
dt (float)

Return type:
None
