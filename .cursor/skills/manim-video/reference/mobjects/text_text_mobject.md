# Text Text Mobject


---

## MarkupText - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.text_mobject.MarkupText.html

MarkupText¶

Qualified name: manim.mobject.text.text\_mobject.MarkupText

class MarkupText(text, fill_opacity=1, stroke_width=0, color=None, font_size=48, line_spacing=-1, font='', slant='NORMAL', weight='NORMAL', justify=False, gradient=None, tab_width=4, height=None, width=None, should_center=True, disable_ligatures=False, warn_missing_font=True, **kwargs)[source]¶
Bases: SVGMobject

Display (non-LaTeX) text rendered using Pango.

Text objects behave like a VGroup-like iterable of all characters
in the given text. In particular, slicing is possible.

What is PangoMarkup?

PangoMarkup is a small markup language like html and it helps you avoid using
“range of characters” while coloring or styling a piece a Text. You can use
this language with MarkupText.

A simple example of a marked-up string might be:

<span foreground="blue" size="x-large">Blue text</span> is <i>cool</i>!"

and it can be used with MarkupText as

Example: MarkupExample ¶

from manim import *

class MarkupExample(Scene):
def construct(self):
text = MarkupText('<span foreground="blue" size="x-large">Blue text</span> is <i>cool</i>!"')
self.add(text)

class MarkupExample(Scene):
def construct(self):
text = MarkupText('Blue text is cool!"')
self.add(text)

A more elaborate example would be:

Example: MarkupElaborateExample ¶

from manim import *

class MarkupElaborateExample(Scene):
def construct(self):
text = MarkupText(
'<span foreground="purple">ا</span><span foreground="red">َ</span>'
'ل<span foreground="blue">ْ</span>ع<span foreground="red">َ</span>ر'
'<span foreground="red">َ</span>ب<span foreground="red">ِ</span>ي'
'<span foreground="green">ّ</span><span foreground="red">َ</span>ة'
'<span foreground="blue">ُ</span>'
)
self.add(text)

class MarkupElaborateExample(Scene):
def construct(self):
text = MarkupText(
'اَ'
'لْعَر'
'َبِي'
'َّة'
'ُ'
)
self.add(text)

PangoMarkup can also contain XML features such as numeric character
entities such as &#169; for © can be used too.

The most general markup tag is <span>, then there are some
convenience tags.

Here is a list of supported tags:

<b>bold</b>, <i>italic</i> and <b><i>bold+italic</i></b>

<u>underline</u> and <s>strike through</s>

<tt>typewriter font</tt>

<big>bigger font</big> and <small>smaller font</small>

<sup>superscript</sup> and <sub>subscript</sub>

<span underline="double" underline_color="green">double underline</span>

<span underline="error">error underline</span>

<span overline="single" overline_color="green">overline</span>

<span strikethrough="true" strikethrough_color="red">strikethrough</span>

<span font_family="sans">temporary change of font</span>

<span foreground="red">temporary change of color</span>

<span fgcolor="red">temporary change of color</span>

<gradient from="YELLOW" to="RED">temporary gradient</gradient>

For <span> markup, colors can be specified either as
hex triples like #aabbcc or as named CSS colors like
AliceBlue.
The <gradient> tag is handled by Manim rather than
Pango, and supports hex triplets or Manim constants like
RED or RED_A.
If you want to use Manim constants like RED_A together
with <span>, you will need to use Python’s f-String
syntax as follows:

MarkupText(f'<span foreground="{RED_A}">here you go</span>')

If your text contains ligatures, the MarkupText class may
incorrectly determine the first and last letter when creating the
gradient. This is due to the fact that fl are two separate characters,
but might be set as one single glyph - a ligature. If your language
does not depend on ligatures, consider setting disable_ligatures
to True. If you must use ligatures, the gradient tag supports an optional
attribute offset which can be used to compensate for that error.

For example:

<gradient from="RED" to="YELLOW" offset="1">example</gradient> to start the gradient one letter earlier

<gradient from="RED" to="YELLOW" offset=",1">example</gradient> to end the gradient one letter earlier

<gradient from="RED" to="YELLOW" offset="2,1">example</gradient> to start the gradient two letters earlier and end it one letter earlier

Specifying a second offset may be necessary if the text to be colored does
itself contain ligatures. The same can happen when using HTML entities for
special chars.

When using underline, overline or strikethrough together with
<gradient> tags, you will also need to use the offset, because
underlines are additional paths in the final SVGMobject.
Check out the following example.

Escaping of special characters: > should be written as &gt;
whereas < and & must be written as &lt; and
&amp;.

You can find more information about Pango markup formatting at the
corresponding documentation page:
Pango Markup.
Please be aware that not all features are supported by this class and that
the <gradient> tag mentioned above is not supported by Pango.

Parameters:

text (str) – The text that needs to be created as mobject.

fill_opacity (float) – The fill opacity, with 1 meaning opaque and 0 meaning transparent.

stroke_width (float) – Stroke width.

font_size (float) – Font size.

line_spacing (float) – Line spacing.

font (str) – Global font setting for the entire text. Local overrides are possible.

slant (str) – Global slant setting, e.g. NORMAL or ITALIC. Local overrides are possible.

weight (str) – Global weight setting, e.g. NORMAL or BOLD. Local overrides are possible.

gradient (Iterable[ParsableManimColor] | None) – Global gradient setting. Local overrides are possible.

warn_missing_font (bool) – If True (default), Manim will issue a warning if the font does not exist in the
(case-sensitive) list of fonts returned from manimpango.list_fonts().

color (ParsableManimColor | None)

justify (bool)

tab_width (int)

height (int | None)

width (int | None)

should_center (bool)

disable_ligatures (bool)

kwargs (Any)

Returns:
The text displayed in form of a VGroup-like mobject.

Return type:
MarkupText

Examples

Example: BasicMarkupExample ¶

from manim import *

class BasicMarkupExample(Scene):
def construct(self):
text1 = MarkupText("<b>foo</b> <i>bar</i> <b><i>foobar</i></b>")
text2 = MarkupText("<s>foo</s> <u>bar</u> <big>big</big> <small>small</small>")
text3 = MarkupText("H<sub>2</sub>O and H<sub>3</sub>O<sup>+</sup>")
text4 = MarkupText("type <tt>help</tt> for help")
text5 = MarkupText(
'<span underline="double">foo</span> <span underline="error">bar</span>'
)
group = VGroup(text1, text2, text3, text4, text5).arrange(DOWN)
self.add(group)

class BasicMarkupExample(Scene):
def construct(self):
text1 = MarkupText("foo bar foobar")
text2 = MarkupText("foo bar big small")
text3 = MarkupText("H2O and H3O+")
text4 = MarkupText("type help for help")
text5 = MarkupText(
'foo bar'
)
group = VGroup(text1, text2, text3, text4, text5).arrange(DOWN)
self.add(group)

Example: ColorExample ¶

from manim import *

class ColorExample(Scene):
def construct(self):
text1 = MarkupText(
f'all in red <span fgcolor="{YELLOW}">except this</span>', color=RED
)
text2 = MarkupText("nice gradient", gradient=(BLUE, GREEN))
text3 = MarkupText(
'nice <gradient from="RED" to="YELLOW">intermediate</gradient> gradient',
gradient=(BLUE, GREEN),
)
text4 = MarkupText(
'fl ligature <gradient from="RED" to="YELLOW">causing trouble</gradient> here'
)
text5 = MarkupText(
'fl ligature <gradient from="RED" to="YELLOW" offset="1">defeated</gradient> with offset'
)
text6 = MarkupText(
'fl ligature <gradient from="RED" to="YELLOW" offset="1">floating</gradient> inside'
)
text7 = MarkupText(
'fl ligature <gradient from="RED" to="YELLOW" offset="1,1">floating</gradient> inside'
)
group = VGroup(text1, text2, text3, text4, text5, text6, text7).arrange(DOWN)
self.add(group)

class ColorExample(Scene):
def construct(self):
text1 = MarkupText(
f'all in red except this', color=RED
)
text2 = MarkupText("nice gradient", gradient=(BLUE, GREEN))
text3 = MarkupText(
'nice intermediate gradient',
gradient=(BLUE, GREEN),
)
text4 = MarkupText(
'fl ligature causing trouble here'
)
text5 = MarkupText(
'fl ligature defeated with offset'
)
text6 = MarkupText(
'fl ligature floating inside'
)
text7 = MarkupText(
'fl ligature floating inside'
)
group = VGroup(text1, text2, text3, text4, text5, text6, text7).arrange(DOWN)
self.add(group)

Example: UnderlineExample ¶

from manim import *

class UnderlineExample(Scene):
def construct(self):
text1 = MarkupText(
'<span underline="double" underline_color="green">bla</span>'
)
text2 = MarkupText(
'<span underline="single" underline_color="green">xxx</span><gradient from="#ffff00" to="RED">aabb</gradient>y'
)
text3 = MarkupText(
'<span underline="single" underline_color="green">xxx</span><gradient from="#ffff00" to="RED" offset="-1">aabb</gradient>y'
)
text4 = MarkupText(
'<span underline="double" underline_color="green">xxx</span><gradient from="#ffff00" to="RED">aabb</gradient>y'
)
text5 = MarkupText(
'<span underline="double" underline_color="green">xxx</span><gradient from="#ffff00" to="RED" offset="-2">aabb</gradient>y'
)
group = VGroup(text1, text2, text3, text4, text5).arrange(DOWN)
self.add(group)

class UnderlineExample(Scene):
def construct(self):
text1 = MarkupText(
'bla'
)
text2 = MarkupText(
'xxxaabby'
)
text3 = MarkupText(
'xxxaabby'
)
text4 = MarkupText(
'xxxaabby'
)
text5 = MarkupText(
'xxxaabby'
)
group = VGroup(text1, text2, text3, text4, text5).arrange(DOWN)
self.add(group)

Example: FontExample ¶

from manim import *

class FontExample(Scene):
def construct(self):
text1 = MarkupText(
'all in sans <span font_family="serif">except this</span>', font="sans"
)
text2 = MarkupText(
'<span font_family="serif">mixing</span> <span font_family="sans">fonts</span> <span font_family="monospace">is ugly</span>'
)
text3 = MarkupText("special char > or &gt;")
text4 = MarkupText("special char &lt; and &amp;")
group = VGroup(text1, text2, text3, text4).arrange(DOWN)
self.add(group)

class FontExample(Scene):
def construct(self):
text1 = MarkupText(
'all in sans except this', font="sans"
)
text2 = MarkupText(
'mixing fonts is ugly'
)
text3 = MarkupText("special char > or >")
text4 = MarkupText("special char < and &")
group = VGroup(text1, text2, text3, text4).arrange(DOWN)
self.add(group)

Example: NewlineExample ¶

from manim import *

class NewlineExample(Scene):
def construct(self):
text = MarkupText('foooo<span foreground="red">oo\nbaa</span>aar')
self.add(text)

class NewlineExample(Scene):
def construct(self):
text = MarkupText('foooooo\nbaaaar')
self.add(text)

Example: NoLigaturesExample ¶

from manim import *

class NoLigaturesExample(Scene):
def construct(self):
text1 = MarkupText('fl<gradient from="RED" to="GREEN">oat</gradient>ing')
text2 = MarkupText('fl<gradient from="RED" to="GREEN">oat</gradient>ing', disable_ligatures=True)
group = VGroup(text1, text2).arrange(DOWN)
self.add(group)

class NoLigaturesExample(Scene):
def construct(self):
text1 = MarkupText('floating')
text2 = MarkupText('floating', disable_ligatures=True)
group = VGroup(text1, text2).arrange(DOWN)
self.add(group)

As MarkupText uses Pango to render text, rendering non-English
characters is easily possible:

Example: MultiLanguage ¶

from manim import *

class MultiLanguage(Scene):
def construct(self):
morning = MarkupText("வணக்கம்", font="sans-serif")
japanese = MarkupText(
'<span fgcolor="blue">日本</span>へようこそ'
)  # works as in ``Text``.
mess = MarkupText("Multi-Language", weight=BOLD)
russ = MarkupText("Здравствуйте मस नम म ", font="sans-serif")
hin = MarkupText("नमस्ते", font="sans-serif")
chinese = MarkupText("臂猿「黛比」帶著孩子", font="sans-serif")
group = VGroup(morning, japanese, mess, russ, hin, chinese).arrange(DOWN)
self.add(group)

class MultiLanguage(Scene):
def construct(self):
morning = MarkupText("வணக்கம்", font="sans-serif")
japanese = MarkupText(
'日本へようこそ'
)  # works as in ``Text``.
mess = MarkupText("Multi-Language", weight=BOLD)
russ = MarkupText("Здравствуйте मस नम म ", font="sans-serif")
hin = MarkupText("नमस्ते", font="sans-serif")
chinese = MarkupText("臂猿「黛比」帶著孩子", font="sans-serif")
group = VGroup(morning, japanese, mess, russ, hin, chinese).arrange(DOWN)
self.add(group)

You can justify the text by passing justify parameter.

Example: JustifyText ¶

from manim import *

class JustifyText(Scene):
def construct(self):
ipsum_text = (
"Lorem ipsum dolor sit amet, consectetur adipiscing elit."
"Praesent feugiat metus sit amet iaculis pulvinar. Nulla posuere "
"quam a ex aliquam, eleifend consectetur tellus viverra. Aliquam "
"fermentum interdum justo, nec rutrum elit pretium ac. Nam quis "
"leo pulvinar, dignissim est at, venenatis nisi."
)
justified_text = MarkupText(ipsum_text, justify=True).scale(0.4)
not_justified_text = MarkupText(ipsum_text, justify=False).scale(0.4)
just_title = Title("Justified")
njust_title = Title("Not Justified")
self.add(njust_title, not_justified_text)
self.play(
FadeOut(not_justified_text),
FadeIn(justified_text),
FadeOut(njust_title),
FadeIn(just_title),
)
self.wait(1)

class JustifyText(Scene):
def construct(self):
ipsum_text = (
"Lorem ipsum dolor sit amet, consectetur adipiscing elit."
"Praesent feugiat metus sit amet iaculis pulvinar. Nulla posuere "
"quam a ex aliquam, eleifend consectetur tellus viverra. Aliquam "
"fermentum interdum justo, nec rutrum elit pretium ac. Nam quis "
"leo pulvinar, dignissim est at, venenatis nisi."
)
justified_text = MarkupText(ipsum_text, justify=True).scale(0.4)
not_justified_text = MarkupText(ipsum_text, justify=False).scale(0.4)
just_title = Title("Justified")
njust_title = Title("Not Justified")
self.add(njust_title, not_justified_text)
self.play(
FadeOut(not_justified_text),
FadeIn(justified_text),
FadeOut(njust_title),
FadeIn(just_title),
)
self.wait(1)

Tests

Check that the creation of MarkupText works:

>>> MarkupText('The horse does not eat cucumber salad.')
MarkupText('The horse does not eat cucumber salad.')

Methods

font_list

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

hash_seed

A unique hash representing the result of the generated mobject points.

height

The height of the mobject.

n_points_per_curve

sheen_factor

stroke_color

width

The width of the mobject.

_count_real_chars(s)[source]¶
Counts characters that will be displayed.

This is needed for partial coloring or gradients, because space
counts to the text’s len, but has no corresponding character.

Parameters:
s (str)

Return type:
int

_extract_color_tags()[source]¶
Used to determine which parts (if any) of the string should be formatted
with a custom color.

Removes the <color> tag, as it is not part of Pango’s markup and would cause an error.

Note: Using the <color> tags is deprecated. As soon as the legacy syntax is gone, this function
will be removed.

Return type:
list[dict[str, Any]]

_extract_gradient_tags()[source]¶
Used to determine which parts (if any) of the string should be formatted
with a gradient.

Removes the <gradient> tag, as it is not part of Pango’s markup and would cause an error.

Return type:
list[dict[str, Any]]

_original__init__(text, fill_opacity=1, stroke_width=0, color=None, font_size=48, line_spacing=-1, font='', slant='NORMAL', weight='NORMAL', justify=False, gradient=None, tab_width=4, height=None, width=None, should_center=True, disable_ligatures=False, warn_missing_font=True, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

text (str)

fill_opacity (float)

stroke_width (float)

color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | None)

font_size (float)

line_spacing (float)

font (str)

slant (str)

weight (str)

justify (bool)

gradient (Iterable[TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor')] | None)

tab_width (int)

height (int | None)

width (int | None)

should_center (bool)

disable_ligatures (bool)

warn_missing_font (bool)

kwargs (Any)

_parse_color(col)[source]¶
Parse color given in <color> or <gradient> tags.

Parameters:
col (str)

Return type:
str

_text2hash(color)[source]¶
Generates sha256 hash for file name.

Parameters:
color (ParsableManimColor)

Return type:
str

_text2svg(color)[source]¶
Convert the text to SVG using Pango.

Parameters:
color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | None)

Return type:
str


---

## Paragraph - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.text_mobject.Paragraph.html

Paragraph¶

Qualified name: manim.mobject.text.text\_mobject.Paragraph

class Paragraph(*text, line_spacing=-1, alignment=None, **kwargs)[source]¶
Bases: VGroup

Display a paragraph of text.

For a given Paragraph par, the attribute par.chars is a
VGroup containing all the lines. In this context, every line is
constructed as a VGroup of characters contained in the line.

Parameters:

line_spacing (float) – Represents the spacing between lines. Defaults to -1, which means auto.

alignment (str | None) – Defines the alignment of paragraph. Defaults to None. Possible values are “left”, “right” or “center”.

text (str)

kwargs (Any)

Examples

Normal usage:

paragraph = Paragraph(
"this is a awesome",
"paragraph",
"With \nNewlines",
"\tWith Tabs",
"  With Spaces",
"With Alignments",
"center",
"left",
"right",
)

Remove unwanted invisible characters:

self.play(Transform(remove_invisible_chars(paragraph.chars[0:2]),
remove_invisible_chars(paragraph.chars[3][0:3]))

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

_change_alignment_for_a_line(alignment, line_no)[source]¶
Function to change one line’s alignment to a specific value.

Parameters:

alignment (str) – Defines the alignment of paragraph. Possible values are “left”, “right”, “center”.

line_no (int) – Defines the line number for which we want to set given alignment.

Return type:
None

_gen_chars(lines_str_list)[source]¶
Function to convert a list of plain strings to a VGroup of VGroups of chars.

Parameters:
lines_str_list (list) – List of plain text strings.

Returns:
The generated 2d-VGroup of chars.

Return type:
VGroup

_original__init__(*text, line_spacing=-1, alignment=None, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

text (str)

line_spacing (float)

alignment (str | None)

kwargs (Any)

_set_all_lines_alignments(alignment)[source]¶
Function to set all line’s alignment to a specific value.

Parameters:
alignment (str) – Defines the alignment of paragraph. Possible values are “left”, “right”, “center”.

Return type:
Paragraph

_set_all_lines_to_initial_positions()[source]¶
Set all lines to their initial positions.

Return type:
Paragraph

_set_line_alignment(alignment, line_no)[source]¶
Function to set one line’s alignment to a specific value.

Parameters:

alignment (str) – Defines the alignment of paragraph. Possible values are “left”, “right”, “center”.

line_no (int) – Defines the line number for which we want to set given alignment.

Return type:
Paragraph

_set_line_to_initial_position(line_no)[source]¶
Function to set one line to initial positions.

Parameters:
line_no (int) – Defines the line number for which we want to set given alignment.

Return type:
Paragraph


---

## Text - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.text_mobject.Text.html

Text¶

Qualified name: manim.mobject.text.text\_mobject.Text

class Text(text, fill_opacity=1.0, stroke_width=0, *, color=ManimColor('#FFFFFF'), font_size=48, line_spacing=-1, font='', slant='NORMAL', weight='NORMAL', t2c=None, t2f=None, t2g=None, t2s=None, t2w=None, gradient=None, tab_width=4, warn_missing_font=True, height=None, width=None, should_center=True, disable_ligatures=False, use_svg_cache=False, **kwargs)[source]¶
Bases: SVGMobject

Display (non-LaTeX) text rendered using Pango.

Text objects behave like a VGroup-like iterable of all characters
in the given text. In particular, slicing is possible.

Parameters:

text (str) – The text that needs to be created as a mobject.

font (str) – The font family to be used to render the text. This is either a system font or
one loaded with register_font(). Note that font family names may be different
across operating systems.

warn_missing_font (bool) – If True (default), Manim will issue a warning if the font does not exist in the
(case-sensitive) list of fonts returned from manimpango.list_fonts().

fill_opacity (float)

stroke_width (float)

color (ParsableManimColor | None)

font_size (float)

line_spacing (float)

slant (str)

weight (str)

t2c (dict[str, str] | None)

t2f (dict[str, str] | None)

t2g (dict[str, Iterable[ParsableManimColor]] | None)

t2s (dict[str, str] | None)

t2w (dict[str, str] | None)

gradient (Iterable[ParsableManimColor] | None)

tab_width (int)

height (float | None)

width (float | None)

should_center (bool)

disable_ligatures (bool)

use_svg_cache (bool)

kwargs (Any)

Returns:
The mobject-like VGroup.

Return type:
Text

Examples

Example: Example1Text ¶

from manim import *

class Example1Text(Scene):
def construct(self):
text = Text('Hello world').scale(3)
self.add(text)

class Example1Text(Scene):
def construct(self):
text = Text('Hello world').scale(3)
self.add(text)

Example: TextColorExample ¶

from manim import *

class TextColorExample(Scene):
def construct(self):
text1 = Text('Hello world', color=BLUE).scale(3)
text2 = Text('Hello world', gradient=(BLUE, GREEN)).scale(3).next_to(text1, DOWN)
self.add(text1, text2)

class TextColorExample(Scene):
def construct(self):
text1 = Text('Hello world', color=BLUE).scale(3)
text2 = Text('Hello world', gradient=(BLUE, GREEN)).scale(3).next_to(text1, DOWN)
self.add(text1, text2)

Example: TextItalicAndBoldExample ¶

from manim import *

class TextItalicAndBoldExample(Scene):
def construct(self):
text1 = Text("Hello world", slant=ITALIC)
text2 = Text("Hello world", t2s={'world':ITALIC})
text3 = Text("Hello world", weight=BOLD)
text4 = Text("Hello world", t2w={'world':BOLD})
text5 = Text("Hello world", t2c={'o':YELLOW}, disable_ligatures=True)
text6 = Text(
"Visit us at docs.manim.community",
t2c={"docs.manim.community": YELLOW},
disable_ligatures=True,
)
text6.scale(1.3).shift(DOWN)
self.add(text1, text2, text3, text4, text5 , text6)
Group(*self.mobjects).arrange(DOWN, buff=.8).set(height=config.frame_height-LARGE_BUFF)

class TextItalicAndBoldExample(Scene):
def construct(self):
text1 = Text("Hello world", slant=ITALIC)
text2 = Text("Hello world", t2s={'world':ITALIC})
text3 = Text("Hello world", weight=BOLD)
text4 = Text("Hello world", t2w={'world':BOLD})
text5 = Text("Hello world", t2c={'o':YELLOW}, disable_ligatures=True)
text6 = Text(
"Visit us at docs.manim.community",
t2c={"docs.manim.community": YELLOW},
disable_ligatures=True,
)
text6.scale(1.3).shift(DOWN)
self.add(text1, text2, text3, text4, text5 , text6)
Group(*self.mobjects).arrange(DOWN, buff=.8).set(height=config.frame_height-LARGE_BUFF)

Example: TextMoreCustomization ¶

from manim import *

class TextMoreCustomization(Scene):
def construct(self):
text1 = Text(
'Google',
t2c={'[:1]': '#3174f0', '[1:2]': '#e53125',
'[2:3]': '#fbb003', '[3:4]': '#3174f0',
'[4:5]': '#269a43', '[5:]': '#e53125'}, font_size=58).scale(3)
self.add(text1)

class TextMoreCustomization(Scene):
def construct(self):
text1 = Text(
'Google',
t2c={'[:1]': '#3174f0', '[1:2]': '#e53125',
'[2:3]': '#fbb003', '[3:4]': '#3174f0',
'[4:5]': '#269a43', '[5:]': '#e53125'}, font_size=58).scale(3)
self.add(text1)

As Text uses Pango to render text, rendering non-English
characters is easily possible:

Example: MultipleFonts ¶

from manim import *

class MultipleFonts(Scene):
def construct(self):
morning = Text("வணக்கம்", font="sans-serif")
japanese = Text(
"日本へようこそ", t2c={"日本": BLUE}
)  # works same as ``Text``.
mess = Text("Multi-Language", weight=BOLD)
russ = Text("Здравствуйте मस नम म ", font="sans-serif")
hin = Text("नमस्ते", font="sans-serif")
arb = Text(
"صباح الخير \n تشرفت بمقابلتك", font="sans-serif"
)  # don't mix RTL and LTR languages nothing shows up then ;-)
chinese = Text("臂猿「黛比」帶著孩子", font="sans-serif")
self.add(morning, japanese, mess, russ, hin, arb, chinese)
for i,mobj in enumerate(self.mobjects):
mobj.shift(DOWN*(i-3))

class MultipleFonts(Scene):
def construct(self):
morning = Text("வணக்கம்", font="sans-serif")
japanese = Text(
"日本へようこそ", t2c={"日本": BLUE}
)  # works same as ``Text``.
mess = Text("Multi-Language", weight=BOLD)
russ = Text("Здравствуйте मस नम म ", font="sans-serif")
hin = Text("नमस्ते", font="sans-serif")
arb = Text(
"صباح الخير \n تشرفت بمقابلتك", font="sans-serif"
)  # don't mix RTL and LTR languages nothing shows up then ;-)
chinese = Text("臂猿「黛比」帶著孩子", font="sans-serif")
self.add(morning, japanese, mess, russ, hin, arb, chinese)
for i,mobj in enumerate(self.mobjects):
mobj.shift(DOWN*(i-3))

Example: PangoRender ¶

from manim import *

class PangoRender(Scene):
def construct(self):
morning = Text("வணக்கம்", font="sans-serif")
self.play(Write(morning))
self.wait(2)

class PangoRender(Scene):
def construct(self):
morning = Text("வணக்கம்", font="sans-serif")
self.play(Write(morning))
self.wait(2)

Tests

Check that the creation of Text works:

>>> Text('The horse does not eat cucumber salad.')
Text('The horse does not eat cucumber salad.')

Methods

font_list

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

hash_seed

A unique hash representing the result of the generated mobject points.

height

The height of the mobject.

n_points_per_curve

sheen_factor

stroke_color

width

The width of the mobject.

_find_indexes(word, text)[source]¶
Finds the indexes of text in word.

Parameters:

word (str)

text (str)

Return type:
list[tuple[int, int]]

_original__init__(text, fill_opacity=1.0, stroke_width=0, color=None, font_size=48, line_spacing=-1, font='', slant='NORMAL', weight='NORMAL', t2c=None, t2f=None, t2g=None, t2s=None, t2w=None, gradient=None, tab_width=4, warn_missing_font=True, height=None, width=None, should_center=True, disable_ligatures=False, use_svg_cache=False, **kwargs)¶
Initialize self.  See help(type(self)) for accurate signature.

Parameters:

text (str)

fill_opacity (float)

stroke_width (float)

color (TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor') | None)

font_size (float)

line_spacing (float)

font (str)

slant (str)

weight (str)

t2c (dict[str, str] | None)

t2f (dict[str, str] | None)

t2g (dict[str, Iterable[TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor')]] | None)

t2s (dict[str, str] | None)

t2w (dict[str, str] | None)

gradient (Iterable[TypeAliasForwardRef('~manim.utils.color.core.ParsableManimColor')] | None)

tab_width (int)

warn_missing_font (bool)

height (float | None)

width (float | None)

should_center (bool)

disable_ligatures (bool)

use_svg_cache (bool)

kwargs (Any)

_text2hash(color)[source]¶
Generates sha256 hash for file name.

Parameters:
color (ParsableManimColor)

Return type:
str

_text2settings(color)[source]¶
Converts the texts and styles to a setting for parsing.

Parameters:
color (ParsableManimColor)

Return type:
list[TextSetting]

_text2svg(color)[source]¶
Convert the text to SVG using Pango.

Parameters:
color (ParsableManimColor)

Return type:
str

init_colors(propagate_colors=True)[source]¶
Initializes the colors.

Gets called upon creation. This is an empty method that can be implemented by
subclasses.

Parameters:
propagate_colors (bool)

Return type:
Self


---

## text_mobject - Manim Community v0.20.1

Source: https://docs.manim.community/en/stable/reference/manim.mobject.text.text_mobject.html

text_mobject¶

Mobjects used for displaying (non-LaTeX) text.

Note

Just as you can use Tex and MathTex (from the module tex_mobject)
to insert LaTeX to your videos, you can use Text to to add normal text.

Important

See the corresponding tutorial Text Without LaTeX, especially for information about fonts.

The simplest way to add text to your animations is to use the Text class. It uses the Pango library to render text.
With Pango, you are also able to render non-English alphabets like 你好 or  こんにちは or 안녕하세요 or مرحبا بالعالم.

Examples

Example: HelloWorld ¶

from manim import *

class HelloWorld(Scene):
def construct(self):
text = Text('Hello world').scale(3)
self.add(text)

class HelloWorld(Scene):
def construct(self):
text = Text('Hello world').scale(3)
self.add(text)

Example: TextAlignment ¶

from manim import *

class TextAlignment(Scene):
def construct(self):
title = Text("K-means clustering and Logistic Regression", color=WHITE)
title.scale(0.75)
self.add(title.to_edge(UP))

t1 = Text("1. Measuring").set_color(WHITE)

t2 = Text("2. Clustering").set_color(WHITE)

t3 = Text("3. Regression").set_color(WHITE)

t4 = Text("4. Prediction").set_color(WHITE)

x = VGroup(t1, t2, t3, t4).arrange(direction=DOWN, aligned_edge=LEFT).scale(0.7).next_to(ORIGIN,DR)
x.set_opacity(0.5)
x.submobjects[1].set_opacity(1)
self.add(x)

class TextAlignment(Scene):
def construct(self):
title = Text("K-means clustering and Logistic Regression", color=WHITE)
title.scale(0.75)
self.add(title.to_edge(UP))

t1 = Text("1. Measuring").set_color(WHITE)

t2 = Text("2. Clustering").set_color(WHITE)

t3 = Text("3. Regression").set_color(WHITE)

t4 = Text("4. Prediction").set_color(WHITE)

x = VGroup(t1, t2, t3, t4).arrange(direction=DOWN, aligned_edge=LEFT).scale(0.7).next_to(ORIGIN,DR)
x.set_opacity(0.5)
x.submobjects[1].set_opacity(1)
self.add(x)

Classes

MarkupText

Display (non-LaTeX) text rendered using Pango.

Paragraph

Display a paragraph of text.

Text

Display (non-LaTeX) text rendered using Pango.

Functions

register_font(font_file)[source]¶
Temporarily add a font file to Pango’s search path.

This searches for the font_file at various places. The order it searches it described below.

Absolute path.

In assets/fonts folder.

In font/ folder.

In the same directory.

Parameters:
font_file (str | Path) – The font file to add.

Return type:
Iterator[None]

Examples

Use with register_font(...) to add a font file to search
path.

with register_font("path/to/font_file.ttf"):
a = Text("Hello", font="Custom Font Name")

Raises:

FileNotFoundError: – If the font doesn’t exists.

AttributeError: – If this method is used on macOS.

.. important :: – This method is available for macOS for ManimPango>=v0.2.3. Using this
method with previous releases will raise an AttributeError on macOS.

Parameters:
font_file (str | Path)

Return type:
Iterator[None]

remove_invisible_chars(mobject)[source]¶
Function to remove unwanted invisible characters from some mobjects.

Parameters:
mobject (VMobject) – Any SVGMobject from which we want to remove unwanted invisible characters.

Returns:
The SVGMobject without unwanted invisible characters.

Return type:
SVGMobject
