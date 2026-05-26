# Text Numbers


---

## DecimalNumber - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.numbers.DecimalNumber.html

DecimalNumber¶

Qualified name: manim.mobject.text.numbers.DecimalNumber

class DecimalNumber(number=0, num_decimal_places=2, mob_class=<class 'manim.mobject.text.tex_mobject.MathTex'>, include_sign=False, group_with_commas=True, digit_buff_per_font_unit=0.001, show_ellipsis=False, unit=None, unit_buff_per_font_unit=0, include_background_rectangle=False, edge_to_fix=array([-1., 0., 0.]), font_size=48, stroke_width=0, fill_opacity=1.0, **kwargs)[source]¶
Bases: VMobject

An mobject representing a decimal number.

Parameters:

number (float) – The numeric value to be displayed. It can later be modified using set_value().

num_decimal_places (int) – The number of decimal places after the decimal separator. Values are automatically rounded.

mob_class (type[SingleStringMathTex]) – The class for rendering digits and units, by default MathTex.

include_sign (bool) – Set to True to include a sign for positive numbers and zero.

group_with_commas (bool) – When True thousands groups are separated by commas for readability.

digit_buff_per_font_unit (float) – Additional spacing between digits. Scales with font size.

show_ellipsis (bool) – When a number has been truncated by rounding, indicate with an ellipsis (...).

unit (str | None) – A unit string which can be placed to the right of the numerical values.

unit_buff_per_font_unit (float) – An additional spacing between the numerical values and the unit. A value
of unit_buff_per_font_unit=0.003 gives a decent spacing. Scales with font size.

include_background_rectangle (bool) – Adds a background rectangle to increase contrast on busy scenes.

edge_to_fix (Vector3DLike) – Assuring right- or left-alignment of the full object.

font_size (float) – Size of the font.

stroke_width (float)

fill_opacity (float)

kwargs (Any)

Examples

Example: MovingSquareWithUpdaters ¶

from manim import *

class MovingSquareWithUpdaters(Scene):
def construct(self):
decimal = DecimalNumber(
0,
show_ellipsis=True,
num_decimal_places=3,
include_sign=True,
unit=r"\text{M-Units}",
unit_buff_per_font_unit=0.003
)
square = Square().to_edge(UP)

decimal.add_updater(lambda d: d.next_to(square, RIGHT))
decimal.add_updater(lambda d: d.set_value(square.get_center()[1]))
self.add(square, decimal)
self.play(
square.animate.to_edge(DOWN),
rate_func=there_and_back,
run_time=5,
)
self.wait()

class MovingSquareWithUpdaters(Scene):
def construct(self):
decimal = DecimalNumber(
0,
show_ellipsis=True,
num_decimal_places=3,
include_sign=True,
unit=r"\text{M-Units}",
unit_buff_per_font_unit=0.003
)
square = Square().to_edge(UP)

decimal.add_updater(lambda d: d.next_to(square, RIGHT))
decimal.add_updater(lambda d: d.set_value(square.get_center()[1]))
self.add(square, decimal)
self.play(
square.animate.to_edge(DOWN),
rate_func=there_and_back,
run_time=5,
)
self.wait()

Methods

get_value

increment_value

set_value

Set the value of the DecimalNumber to a new number.

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

font_size

The font size of the tex mobject.

height

The height of the mobject.

n_points_per_curve

sheen_factor

stroke_color

width

The width of the mobject.

_get_formatter(**kwargs)[source]¶
Configuration is based first off instance attributes,
but overwritten by any kew word argument.  Relevant
key words:
- include_sign
- group_with_commas
- num_decimal_places
- field_name (e.g. 0 or 0.real)

Parameters:
kwargs (Any)

Return type:
str

_original__init__(number=0, num_decimal_places=2, mob_class=<class 'manim.mobject.text.tex_mobject.MathTex'>, include_sign=False, group_with_commas=True, digit_buff_per_font_unit=0.001, show_ellipsis=False, unit=None, unit_buff_per_font_unit=0, include_background_rectangle=False, edge_to_fix=array([-1., 0., 0.]), font_size=48, stroke_width=0, fill_opacity=1.0, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

number (float)

num_decimal_places (int)

mob_class (type[SingleStringMathTex])

include_sign (bool)

group_with_commas (bool)

digit_buff_per_font_unit (float)

show_ellipsis (bool)

unit (str | None)

unit_buff_per_font_unit (float)

include_background_rectangle (bool)

edge_to_fix (Vector3DLike)

font_size (float)

stroke_width (float)

fill_opacity (float)

kwargs (Any)

property font_size: float¶
The font size of the tex mobject.

set_value(number)[source]¶
Set the value of the DecimalNumber to a new number.

Parameters:
number (float) – The value that will overwrite the current number of the DecimalNumber.

Return type:
Self


---

## Integer - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.numbers.Integer.html

Integer¶

Qualified name: manim.mobject.text.numbers.Integer

class Integer(number=0, num_decimal_places=0, **kwargs)[source]¶
Bases: DecimalNumber

A class for displaying Integers.

Examples

Example: IntegerExample ¶

from manim import *

class IntegerExample(Scene):
def construct(self):
self.add(Integer(number=2.5).set_color(ORANGE).scale(2.5).set_x(-0.5).set_y(0.8))
self.add(Integer(number=3.14159, show_ellipsis=True).set_x(3).set_y(3.3).scale(3.14159))
self.add(Integer(number=42).set_x(2.5).set_y(-2.3).set_color_by_gradient(BLUE, TEAL).scale(1.7))
self.add(Integer(number=6.28).set_x(-1.5).set_y(-2).set_color(YELLOW).scale(1.4))

class IntegerExample(Scene):
def construct(self):
self.add(Integer(number=2.5).set_color(ORANGE).scale(2.5).set_x(-0.5).set_y(0.8))
self.add(Integer(number=3.14159, show_ellipsis=True).set_x(3).set_y(3.3).scale(3.14159))
self.add(Integer(number=42).set_x(2.5).set_y(-2.3).set_color_by_gradient(BLUE, TEAL).scale(1.7))
self.add(Integer(number=6.28).set_x(-1.5).set_y(-2).set_color(YELLOW).scale(1.4))

Methods

get_value

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

font_size

The font size of the tex mobject.

height

The height of the mobject.

n_points_per_curve

sheen_factor

stroke_color

width

The width of the mobject.

Parameters:

number (float)

num_decimal_places (int)

kwargs (Any)

_original__init__(number=0, num_decimal_places=0, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

number (float)

num_decimal_places (int)

kwargs (Any)

Return type:
None


---

## Variable - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.numbers.Variable.html

Variable¶

Qualified name: manim.mobject.text.numbers.Variable

class Variable(var, label, var_type=<class 'manim.mobject.text.numbers.DecimalNumber'>, num_decimal_places=2, **kwargs)[source]¶
Bases: VMobject

A class for displaying text that shows “label = value” with
the value continuously updated from a ValueTracker.

Parameters:

var (float) – The initial value you need to keep track of and display.

label (str | Tex | MathTex | Text | SingleStringMathTex) – The label for your variable. Raw strings are convertex to MathTex objects.

var_type (type[DecimalNumber | Integer]) – The class used for displaying the number. Defaults to DecimalNumber.

num_decimal_places (int) – The number of decimal places to display in your variable. Defaults to 2.
If var_type is an Integer, this parameter is ignored.

kwargs (Any) – Other arguments to be passed to ~.Mobject.

label¶
The label for your variable, for example x = ....

Type:
Union[str, Tex, MathTex, Text, SingleStringMathTex]

tracker¶
Useful in updating the value of your variable on-screen.

Type:
ValueTracker

value¶
The tex for the value of your variable.

Type:
Union[DecimalNumber, Integer]

Examples

Normal usage:

# DecimalNumber type
var = 0.5
on_screen_var = Variable(var, Text("var"), num_decimal_places=3)
# Integer type
int_var = 0
on_screen_int_var = Variable(int_var, Text("int_var"), var_type=Integer)
# Using math mode for the label
on_screen_int_var = Variable(int_var, "{a}_{i}", var_type=Integer)

Example: VariablesWithValueTracker ¶

from manim import *

class VariablesWithValueTracker(Scene):
def construct(self):
var = 0.5
on_screen_var = Variable(var, Text("var"), num_decimal_places=3)

# You can also change the colours for the label and value
on_screen_var.label.set_color(RED)
on_screen_var.value.set_color(GREEN)

self.play(Write(on_screen_var))
# The above line will just display the variable with
# its initial value on the screen. If you also wish to
# update it, you can do so by accessing the `tracker` attribute
self.wait()
var_tracker = on_screen_var.tracker
var = 10.5
self.play(var_tracker.animate.set_value(var))
self.wait()

int_var = 0
on_screen_int_var = Variable(
int_var, Text("int_var"), var_type=Integer
).next_to(on_screen_var, DOWN)
on_screen_int_var.label.set_color(RED)
on_screen_int_var.value.set_color(GREEN)

self.play(Write(on_screen_int_var))
self.wait()
var_tracker = on_screen_int_var.tracker
var = 10.5
self.play(var_tracker.animate.set_value(var))
self.wait()

# If you wish to have a somewhat more complicated label for your
# variable with subscripts, superscripts, etc. the default class
# for the label is MathTex
subscript_label_var = 10
on_screen_subscript_var = Variable(subscript_label_var, "{a}_{i}").next_to(
on_screen_int_var, DOWN
)
self.play(Write(on_screen_subscript_var))
self.wait()

class VariablesWithValueTracker(Scene):
def construct(self):
var = 0.5
on_screen_var = Variable(var, Text("var"), num_decimal_places=3)

# You can also change the colours for the label and value
on_screen_var.label.set_color(RED)
on_screen_var.value.set_color(GREEN)

self.play(Write(on_screen_var))
# The above line will just display the variable with
# its initial value on the screen. If you also wish to
# update it, you can do so by accessing the `tracker` attribute
self.wait()
var_tracker = on_screen_var.tracker
var = 10.5
self.play(var_tracker.animate.set_value(var))
self.wait()

int_var = 0
on_screen_int_var = Variable(
int_var, Text("int_var"), var_type=Integer
).next_to(on_screen_var, DOWN)
on_screen_int_var.label.set_color(RED)
on_screen_int_var.value.set_color(GREEN)

self.play(Write(on_screen_int_var))
self.wait()
var_tracker = on_screen_int_var.tracker
var = 10.5
self.play(var_tracker.animate.set_value(var))
self.wait()

# If you wish to have a somewhat more complicated label for your
# variable with subscripts, superscripts, etc. the default class
# for the label is MathTex
subscript_label_var = 10
on_screen_subscript_var = Variable(subscript_label_var, "{a}_{i}").next_to(
on_screen_int_var, DOWN
)
self.play(Write(on_screen_subscript_var))
self.wait()

Example: VariableExample ¶

from manim import *

class VariableExample(Scene):
def construct(self):
start = 2.0

x_var = Variable(start, 'x', num_decimal_places=3)
sqr_var = Variable(start**2, 'x^2', num_decimal_places=3)
Group(x_var, sqr_var).arrange(DOWN)

sqr_var.add_updater(lambda v: v.tracker.set_value(x_var.tracker.get_value()**2))

self.add(x_var, sqr_var)
self.play(x_var.tracker.animate.set_value(5), run_time=2, rate_func=linear)
self.wait(0.1)

class VariableExample(Scene):
def construct(self):
start = 2.0

x_var = Variable(start, 'x', num_decimal_places=3)
sqr_var = Variable(start**2, 'x^2', num_decimal_places=3)
Group(x_var, sqr_var).arrange(DOWN)

sqr_var.add_updater(lambda v: v.tracker.set_value(x_var.tracker.get_value()**2))

self.add(x_var, sqr_var)
self.play(x_var.tracker.animate.set_value(5), run_time=2, rate_func=linear)
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

_original__init__(var, label, var_type=<class 'manim.mobject.text.numbers.DecimalNumber'>, num_decimal_places=2, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

var (float)

label (str | Tex | MathTex | Text | SingleStringMathTex)

var_type (type[DecimalNumber | Integer])

num_decimal_places (int)

kwargs (Any)


---

## numbers - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.numbers.html

numbers¶

Mobjects representing numbers.

Classes

DecimalNumber

An mobject representing a decimal number.

Integer

A class for displaying Integers.

Variable

A class for displaying text that shows "label = value" with the value continuously updated from a ValueTracker.
