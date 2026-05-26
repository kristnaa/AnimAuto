# Text Tex Mobject


---

## BulletedList - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.tex_mobject.BulletedList.html

BulletedList¶

Qualified name: manim.mobject.text.tex\_mobject.BulletedList

class BulletedList(*items, buff=0.5, dot_scale_factor=2, tex_environment=None, **kwargs)[source]¶
Bases: Tex

A bulleted list.

Examples

Example: BulletedListExample ¶

from manim import *

class BulletedListExample(Scene):
def construct(self):
blist = BulletedList("Item 1", "Item 2", "Item 3", height=2, width=2)
blist.set_color_by_tex("Item 1", RED)
blist.set_color_by_tex("Item 2", GREEN)
blist.set_color_by_tex("Item 3", BLUE)
self.add(blist)

class BulletedListExample(Scene):
def construct(self):
blist = BulletedList("Item 1", "Item 2", "Item 3", height=2, width=2)
blist.set_color_by_tex("Item 1", RED)
blist.set_color_by_tex("Item 2", GREEN)
blist.set_color_by_tex("Item 3", BLUE)
self.add(blist)

Methods

fade_all_but

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

hash_seed

A unique hash representing the result of the generated mobject points.

height

The height of the mobject.

n_points_per_curve

sheen_factor

stroke_color

width

The width of the mobject.

Parameters:

items (str)

buff (float)

dot_scale_factor (float)

tex_environment (str | None)

kwargs (Any)

_original__init__(*items, buff=0.5, dot_scale_factor=2, tex_environment=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

items (str)

buff (float)

dot_scale_factor (float)

tex_environment (str | None)

kwargs (Any)


---

## MathTex - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.tex_mobject.MathTex.html

MathTex¶

Qualified name: manim.mobject.text.tex\_mobject.MathTex

class MathTex(*tex_strings, arg_separator=' ', substrings_to_isolate=None, tex_to_color_map=None, tex_environment='align*', **kwargs)[source]¶
Bases: SingleStringMathTex

A string compiled with LaTeX in math mode.

Examples

Example: Formula ¶

from manim import *

class Formula(Scene):
def construct(self):
t = MathTex(r"\int_a^b f'(x) dx = f(b)- f(a)")
self.add(t)

class Formula(Scene):
def construct(self):
t = MathTex(r"\int_a^b f'(x) dx = f(b)- f(a)")
self.add(t)

Notes

Double-brace notation {{ ... }} can be used to split a single
string argument into multiple submobjects without having to pass
separate strings:

MathTex(r"{{ a^2 }} + {{ b^2 }} = {{ c^2 }}")

Each {{ ... }} group and every piece of text between groups
becomes its own submobject, which is useful for
TransformMatchingTex animations.

For {{ to be recognised as a group opener it must appear either
at the very start of the string or be immediately preceded by a
whitespace character.  {{ that follows non-whitespace — such as
in \frac{{{n}}}{k} or a^{{2}} — is left untouched, so
ordinary nested-brace LaTeX is not accidentally split.  To prevent
an unintentional split, insert a space between the two braces:
{{ ... }} → { { ... } }.

Tests

Check that creating a MathTex works:

>>> MathTex('a^2 + b^2 = c^2')
MathTex('a^2 + b^2 = c^2')

Check that double brace group splitting works correctly:

>>> t1 = MathTex('{{ a }} + {{ b }} = {{ c }}')
>>> len(t1.submobjects)
5
>>> t2 = MathTex(r"\frac{1}{a+b\sqrt{2}}")
>>> len(t2.submobjects)
1

Methods

get_part_by_tex

index_of_part

set_color_by_tex

set_color_by_tex_to_color_map

set_opacity_by_tex

Sets the opacity of the tex specified.

sort_alphabetically

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

hash_seed

A unique hash representing the result of the generated mobject points.

height

The height of the mobject.

n_points_per_curve

sheen_factor

stroke_color

width

The width of the mobject.

Parameters:

tex_strings (str)

arg_separator (str)

substrings_to_isolate (Iterable[str] | None)

tex_to_color_map (dict[str, ParsableManimColor] | None)

tex_environment (str | None)

kwargs (Any)

_break_up_by_substrings()[source]¶
Reorganize existing submobjects one layer
deeper based on the structure of tex_strings (as a list
of tex_strings)

Return type:
Self

property _main_matches: list[tuple[str, str]]¶
Return only the main tex_string matches.

_original__init__(*tex_strings, arg_separator=' ', substrings_to_isolate=None, tex_to_color_map=None, tex_environment='align*', **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

tex_strings (str)

arg_separator (str)

substrings_to_isolate (Iterable[str] | None)

tex_to_color_map (dict[str, TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor')] | None)

tex_environment (str | None)

kwargs (Any)

static _split_double_braces(tex_string)[source]¶
Split tex_string on Manim’s {{ ... }} double-brace notation.

Rules that avoid false positives on ordinary LaTeX source:

{{ is only treated as a group opener when it appears at the very
start of the string or is immediately preceded by a whitespace
character.  Naturally-occurring {{ in LaTeX is usually preceded
by non-whitespace (e.g. \frac{{{n}}}{k} or a^{{2}}), so
the whitespace guard eliminates the most common false positives
without any brace-depth bookkeeping on the outer string.

Inside an open group the depth of real LaTeX braces is tracked.
}} only closes the Manim group when the inner depth is zero,
so {{ a^{b^{c}} }} is handled correctly.

Escape sequences are consumed as two-character units in priority
order: \\ first (escaped backslash), then \{ / \}
(escaped braces).  This ensures e.g. \\}} is read as an
escaped backslash followed by a real }} rather than as
\ + \} + lone }.

Parameters:
tex_string (str)

Return type:
list[str]

property _substring_matches: list[tuple[str, str]]¶
Return only the ‘ss’ (substring_to_isolate) matches.

set_opacity_by_tex(tex, opacity=0.5, remaining_opacity=None, **kwargs)[source]¶
Sets the opacity of the tex specified. If ‘remaining_opacity’ is specified,
then the remaining tex will be set to that opacity.

Parameters:

tex (str) – The tex to set the opacity of.

opacity (float) – Default 0.5. The opacity to set the tex to

remaining_opacity (float | None) – Default None. The opacity to set the remaining tex to.
If None, then the remaining tex will not be changed

kwargs (Any)

Return type:
Self


---

## MathTexPart - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.tex_mobject.MathTexPart.html

MathTexPart¶

Qualified name: manim.mobject.text.tex\_mobject.MathTexPart

class MathTexPart(fill_color=None, fill_opacity=0.0, stroke_color=None, stroke_opacity=1.0, stroke_width=4, background_stroke_color=ManimColor('#000000'), background_stroke_opacity=1.0, background_stroke_width=0, sheen_factor=0.0, joint_type=None, sheen_direction=array([-1., 1., 0.]), close_new_points=False, pre_function_handle_to_anchor_scale_factor=0.01, make_smooth_after_applying_functions=False, background_image=None, shade_in_3d=False, tolerance_for_point_equality=1e-06, n_points_per_cubic_curve=4, cap_style=CapStyleType.AUTO, **kwargs)[source]¶
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

tex_string

Parameters:

fill_color (ParsableManimColor | None)

fill_opacity (float)

stroke_color (ParsableManimColor | None)

stroke_opacity (float)

stroke_width (float)

background_stroke_color (ParsableManimColor | None)

background_stroke_opacity (float)

background_stroke_width (float)

sheen_factor (float)

joint_type (LineJointType | None)

sheen_direction (Vector3DLike)

close_new_points (bool)

pre_function_handle_to_anchor_scale_factor (float)

make_smooth_after_applying_functions (bool)

background_image (Image | str | None)

shade_in_3d (bool)

tolerance_for_point_equality (float)

n_points_per_cubic_curve (int)

cap_style (CapStyleType)

kwargs (Any)

_original__init__(fill_color=None, fill_opacity=0.0, stroke_color=None, stroke_opacity=1.0, stroke_width=4, background_stroke_color=ManimColor('#000000'), background_stroke_opacity=1.0, background_stroke_width=0, sheen_factor=0.0, joint_type=None, sheen_direction=array([-1., 1., 0.]), close_new_points=False, pre_function_handle_to_anchor_scale_factor=0.01, make_smooth_after_applying_functions=False, background_image=None, shade_in_3d=False, tolerance_for_point_equality=1e-06, n_points_per_cubic_curve=4, cap_style=CapStyleType.AUTO, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

fill_color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | None)

fill_opacity (float)

stroke_color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | None)

stroke_opacity (float)

stroke_width (float)

background_stroke_color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | None)

background_stroke_opacity (float)

background_stroke_width (float)

sheen_factor (float)

joint_type (LineJointType | None)

sheen_direction (Vector3DLike)

close_new_points (bool)

pre_function_handle_to_anchor_scale_factor (float)

make_smooth_after_applying_functions (bool)

background_image (Image | str | None)

shade_in_3d (bool)

tolerance_for_point_equality (float)

n_points_per_cubic_curve (int)

cap_style (CapStyleType)

kwargs (Any)


---

## SingleStringMathTex - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.tex_mobject.SingleStringMathTex.html

SingleStringMathTex¶

Qualified name: manim.mobject.text.tex\_mobject.SingleStringMathTex

class SingleStringMathTex(tex_string, stroke_width=0, should_center=True, height=None, organize_left_to_right=False, tex_environment='align*', tex_template=None, font_size=48, color=None, **kwargs)[source]¶
Bases: SVGMobject

Elementary building block for rendering text with LaTeX.

Tests

Check that creating a SingleStringMathTex object works:

>>> SingleStringMathTex('Test')
SingleStringMathTex('Test')

Methods

get_tex_string

init_colors

Initializes the colors.

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

hash_seed

A unique hash representing the result of the generated mobject points.

height

The height of the mobject.

n_points_per_curve

sheen_factor

stroke_color

width

The width of the mobject.

Parameters:

tex_string (str)

stroke_width (float)

should_center (bool)

height (float | None)

organize_left_to_right (bool)

tex_environment (str | None)

tex_template (TexTemplate | None)

font_size (float)

color (ParsableManimColor | None)

kwargs (Any)

_original__init__(tex_string, stroke_width=0, should_center=True, height=None, organize_left_to_right=False, tex_environment='align*', tex_template=None, font_size=48, color=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

tex_string (str)

stroke_width (float)

should_center (bool)

height (float | None)

organize_left_to_right (bool)

tex_environment (str | None)

tex_template (TexTemplate | None)

font_size (float)

color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | None)

kwargs (Any)

_remove_stray_braces(tex)[source]¶
Makes MathTex resilient to unmatched braces.

This is important when the braces in the TeX code are spread over
multiple arguments as in, e.g., MathTex(r"e^{i", r"\tau} = 1").

Parameters:
tex (str)

Return type:
str

property font_size: float¶
The font size of the tex mobject.

init_colors(propagate_colors=True)[source]¶
Initializes the colors.

Gets called upon creation. This is an empty method that can be implemented by
subclasses.

Parameters:
propagate_colors (bool)

Return type:
Self


---

## Tex - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.tex_mobject.Tex.html

Tex¶

Qualified name: manim.mobject.text.tex\_mobject.Tex

class Tex(*tex_strings, arg_separator='', tex_environment='center', **kwargs)[source]¶
Bases: MathTex

A string compiled with LaTeX in normal mode.

The color can be set using
the color argument. Any parts of the tex_string that are colored by the
TeX commands \color or \textcolor will retain their original color.

Tests

Check whether writing a LaTeX string works:

>>> Tex('The horse does not eat cucumber salad.')
Tex('The horse does not eat cucumber salad.')

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

font_size

The font size of the tex mobject.

hash_seed

A unique hash representing the result of the generated mobject points.

height

The height of the mobject.

n_points_per_curve

sheen_factor

stroke_color

width

The width of the mobject.

Parameters:

tex_strings (str)

arg_separator (str)

tex_environment (str | None)

kwargs (Any)

_original__init__(*tex_strings, arg_separator='', tex_environment='center', **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

tex_strings (str)

arg_separator (str)

tex_environment (str | None)

kwargs (Any)


---

## Title - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.tex_mobject.Title.html

Title¶

Qualified name: manim.mobject.text.tex\_mobject.Title

class Title(*text_parts, include_underline=True, match_underline_width_to_text=False, underline_buff=0.25, **kwargs)[source]¶
Bases: Tex

A mobject representing an underlined title.

Examples

Example: TitleExample ¶

from manim import *

import manim

class TitleExample(Scene):
def construct(self):
banner = ManimBanner()
title = Title(f"Manim version {manim.__version__}")
self.add(banner, title)

import manim

class TitleExample(Scene):
def construct(self):
banner = ManimBanner()
title = Title(f"Manim version {manim.__version__}")
self.add(banner, title)

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

font_size

The font size of the tex mobject.

hash_seed

A unique hash representing the result of the generated mobject points.

height

The height of the mobject.

n_points_per_curve

sheen_factor

stroke_color

width

The width of the mobject.

Parameters:

text_parts (str)

include_underline (bool)

match_underline_width_to_text (bool)

underline_buff (float)

kwargs (Any)

_original__init__(*text_parts, include_underline=True, match_underline_width_to_text=False, underline_buff=0.25, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

text_parts (str)

include_underline (bool)

match_underline_width_to_text (bool)

underline_buff (float)

kwargs (Any)


---

## tex_mobject - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.tex_mobject.html

tex_mobject¶

Mobjects representing text rendered using LaTeX.

Important

See the corresponding tutorial Text With LaTeX

Note

Just as you can use Text (from the module text_mobject) to add text to your videos, you can use Tex and MathTex to insert LaTeX.

Classes

BulletedList

A bulleted list.

MathTex

A string compiled with LaTeX in math mode.

MathTexPart

SingleStringMathTex

Elementary building block for rendering text with LaTeX.

Tex

A string compiled with LaTeX in normal mode.

Title

A mobject representing an underlined title.
