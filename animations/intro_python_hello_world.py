from manim import *
from manim.utils.rate_functions import smooth

BG_PATH = "/Users/enfec/manimations/background/orange_theme_BG.png"
SIDE_MARGIN = 0.55


class IntroPythonHelloWorld(Scene):
    def construct(self):
        self.setup_background()
        self.beat_01_course_welcome()
        self.beat_02_what_is_python()
        self.beat_03_simple_definition()
        self.beat_04_why_python_for_ai()
        self.beat_05_real_world_use()
        self.beat_06_tiny_truth()
        self.beat_07_not_the_snake()
        self.beat_08_today_mission()
        self.beat_09_open_editor()
        self.beat_10_create_file()
        self.beat_11_write_first_code()
        self.beat_12_explain_print()
        self.beat_13_run_the_code()
        self.beat_14_ai_connection()
        self.beat_15_student_challenge()
        self.beat_16_beginner_mistake()
        self.beat_17_recap()
        self.beat_18_ending()

    # ---------------------------------------------------------------- layout
    def setup_background(self):
        bg = ImageMobject(BG_PATH)
        bg.scale_to_fit_width(config.frame_width)
        bg.move_to(ORIGIN)
        self.add(bg)
        self.bg = bg

    def left_center(self):
        return LEFT * (config.frame_width / 4)

    def right_center(self):
        return RIGHT * (config.frame_width / 4)

    def card_width(self):
        return config.frame_width / 2 - SIDE_MARGIN * 2

    def top_label(self, text):
        lbl = Text(text, font_size=32, color=YELLOW, weight=BOLD)
        lbl.to_edge(UP, buff=0.45)
        return lbl

    def label(self, text, font_size=30):
        return Text(text, font_size=font_size, color=YELLOW, weight=BOLD)

    def on_card(self, text, font_size=30):
        return Text(text, font_size=font_size, color=BLACK, weight=BOLD)

    def on_bg(self, text, font_size=34):
        return Text(text, font_size=font_size, color=WHITE, weight=BOLD)

    def card_lines(self, *lines, font_size=28, left_align=True):
        group = VGroup(*[self.on_card(line, font_size=font_size) for line in lines])
        if left_align:
            group.arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        else:
            group.arrange(DOWN, buff=0.22, center=True)
        return group

    def bg_lines(self, *lines, font_size=34):
        group = VGroup(*[self.on_bg(line, font_size=font_size) for line in lines])
        group.arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        return group

    def white_card(self, content, side="right", height=None):
        width = self.card_width()
        if height is None:
            height = max(2.8, content.height + 0.9)
        card = RoundedRectangle(
            width=max(width, content.width + 0.8),
            height=max(2.8, height),
            corner_radius=0.22,
            fill_color=WHITE,
            fill_opacity=0.96,
            stroke_color=GREY_B,
            stroke_width=1.5,
        )
        anchor = self.right_center() if side == "right" else self.left_center()
        card.move_to(anchor)
        content.move_to(card.get_center())
        return VGroup(card, content), card

    def place_left(self, mob):
        mob.move_to(self.left_center())
        return mob

    def place_right(self, mob):
        mob.move_to(self.right_center())
        return mob

    def fade_clear(self, *mobjects, run_time=0.55):
        mobs = [m for m in mobjects if m is not None]
        if mobs:
            self.play(*[FadeOut(m) for m in mobs], run_time=run_time, rate_func=smooth)

    def fade_to_black(self, *mobjects, run_time=1.0):
        overlay = Rectangle(
            width=config.frame_width + 2,
            height=config.frame_height + 2,
            fill_color=BLACK,
            fill_opacity=0,
            stroke_width=0,
        ).move_to(ORIGIN)
        self.add(overlay)
        self.play(
            *[FadeOut(m) for m in mobjects if m is not None],
            overlay.animate.set_fill(opacity=1),
            run_time=run_time,
            rate_func=smooth,
        )

    # ------------------------------------------------------------- components
    def mini_pill(self, text):
        pill = RoundedRectangle(
            width=1.9, height=0.48, corner_radius=0.1,
            fill_color=GREY_E, fill_opacity=1, stroke_color=BLACK, stroke_width=1,
        )
        t = self.on_card(text, font_size=20)
        t.move_to(pill.get_center())
        return VGroup(pill, t)

    def code_box(self, code, font_size=24):
        text = Text(code, font="Courier New", font_size=font_size, color=BLACK, weight=BOLD)
        box = SurroundingRectangle(text, color=BLACK, buff=0.2, stroke_width=2)
        return VGroup(box, text), text, box

    def output_box(self, text_str):
        text = self.on_card(text_str, font_size=24)
        box = RoundedRectangle(
            width=text.width + 0.65, height=text.height + 0.4,
            corner_radius=0.1, fill_color=GREY_E, fill_opacity=1,
            stroke_color=BLACK, stroke_width=1.5,
        )
        text.move_to(box.get_center())
        return VGroup(box, text), text

    def yellow_check(self):
        return Text("✓", font_size=24, color=YELLOW, weight=BOLD)

    def blink_mobject(self, mob, times=2):
        for _ in range(times):
            self.play(mob.animate.set_opacity(0), run_time=0.1)
            self.play(mob.animate.set_opacity(1), run_time=0.1)

    def typing_cursor_for(self, text_mob):
        return Rectangle(
            width=0.06,
            height=max(0.3, text_mob.height * 1.05),
            fill_color=YELLOW,
            fill_opacity=1,
            stroke_width=0,
        )

    def type_text(self, text_mob, time_per_char=0.05, leave_cursor_on=False, blink=0):
        cursor = self.typing_cursor_for(text_mob)
        if len(text_mob) > 0:
            cursor.move_to(text_mob[0])
        else:
            cursor.move_to(text_mob.get_left())
        self.play(
            TypeWithCursor(
                text_mob,
                cursor,
                time_per_char=time_per_char,
                leave_cursor_on=leave_cursor_on or blink > 0,
            )
        )
        if blink > 0:
            self.play(Blink(cursor, blinks=blink))
        return cursor

    def type_lines(self, *lines, time_per_char=0.05):
        for line in lines:
            self.type_text(line, time_per_char=time_per_char)

    def sparkle_dots(self, center, count=6, radius=0.9):
        return VGroup(*[
            Dot(center + radius * np.array([np.cos(i * TAU / count), np.sin(i * TAU / count), 0]),
                radius=0.05, color=YELLOW)
            for i in range(count)
        ])

    def drawn_laptop(self):
        base = RoundedRectangle(width=1.2, height=0.8, corner_radius=0.08, color=WHITE, stroke_width=2)
        screen = RoundedRectangle(width=0.95, height=0.55, corner_radius=0.05, color=WHITE, stroke_width=2)
        screen.move_to(base.get_center() + UP * 0.04)
        return VGroup(base, screen)

    def drawn_editor(self):
        window = RoundedRectangle(width=3.5, height=1.9, corner_radius=0.1, color=BLACK, stroke_width=2)
        bar = Rectangle(width=3.5, height=0.28, fill_color=GREY_B, fill_opacity=1, stroke_width=0).align_to(window, UP)
        dots = VGroup(*[
            Dot(bar.get_left() + RIGHT * (0.28 + i * 0.2) + DOWN * 0.03, radius=0.045, color=BLACK)
            for i in range(3)
        ])
        cursor = Rectangle(width=0.06, height=0.28, fill_color=YELLOW, fill_opacity=1, stroke_width=0)
        cursor.move_to(window.get_center() + LEFT * 0.9)
        return VGroup(window, bar, dots, cursor), cursor

    def drawn_potato(self):
        body = Ellipse(width=0.95, height=0.7, color=BLACK, fill_color=GREY_B, fill_opacity=0.35, stroke_width=2)
        glasses = RoundedRectangle(width=0.6, height=0.16, corner_radius=0.04, color=BLACK, stroke_width=2)
        glasses.move_to(body.get_center() + UP * 0.08)
        return VGroup(body, glasses)

    def drawn_sleeping_snake(self):
        snake = ArcBetweenPoints(LEFT * 0.65, RIGHT * 0.65, angle=-PI / 2, color=WHITE, stroke_width=4)
        zzz = self.on_bg("z z z", font_size=16).next_to(snake, UP, buff=0.06)
        return VGroup(snake, zzz)

    def drawn_rocket(self):
        body = Polygon(UP * 0.4, LEFT * 0.18 + DOWN * 0.28, RIGHT * 0.18 + DOWN * 0.28,
                       color=WHITE, fill_color=GREY_E, fill_opacity=0.5, stroke_width=2)
        window = Circle(radius=0.07, color=WHITE, fill_color=GREY_B, fill_opacity=1, stroke_width=1.5)
        window.move_to(body.get_center() + UP * 0.05)
        return VGroup(body, window)

    def drawn_heart(self):
        return VGroup(
            Arc(radius=0.12, angle=PI, color=WHITE, stroke_width=2).shift(LEFT * 0.06 + DOWN * 0.03),
            Arc(radius=0.12, angle=PI, color=WHITE, stroke_width=2).shift(RIGHT * 0.06 + DOWN * 0.03),
        )

    def shape_morph_left(self):
        circle = Circle(radius=0.85, color=WHITE, stroke_width=3, fill_color=BLUE_E, fill_opacity=0.2)
        square = Square(side_length=1.45, color=WHITE, stroke_width=3, fill_color=YELLOW_E, fill_opacity=0.2)
        square.move_to(circle.get_center())
        return circle, square

    # ================================================================ beats
    def beat_01_course_welcome(self):
        label = self.top_label("Welcome to Python for AI")
        left = VGroup(
            self.drawn_laptop().scale(1.05),
            self.on_bg("Python", font_size=28),
            self.sparkle_dots(self.left_center() + UP * 0.2),
        ).arrange(DOWN, buff=0.3)
        self.place_left(left)

        card_content = self.card_lines(
            "Today, we meet Python…",
            "the language that helps humans",
            "talk to computers",
            "without crying too much.",
            font_size=28,
        )
        card, _ = self.white_card(card_content, side="right", height=3.8)

        self.play(FadeIn(label), FadeIn(left), run_time=0.6)
        self.play(GrowFromCenter(card), run_time=0.6)
        self.type_lines(*card_content, time_per_char=0.05)
        self.play(Wiggle(card_content[-1]), run_time=0.6)
        self.wait(2)
        self.fade_clear(label, left, card)

    def beat_02_what_is_python(self):
        label = self.top_label("Big Question")

        left = VGroup(
            Circle(radius=1.0, color=YELLOW, stroke_width=3),
            Text("?", font_size=110, color=YELLOW, weight=BOLD),
        )
        self.place_left(left)

        # No card — short question reads better as white text on orange BG (right half)
        right_text = self.bg_lines("So first…", "what exactly is Python?", font_size=36)
        self.place_right(right_text)

        self.play(FadeIn(label), FadeIn(left), run_time=0.6)
        self.type_text(right_text[0], time_per_char=0.06)
        self.wait(0.4)
        self.type_text(right_text[1], time_per_char=0.05)
        self.play(Indicate(right_text[1], color=YELLOW), run_time=0.55)
        self.wait(2.5)
        self.fade_clear(label, left, right_text)

    def beat_03_simple_definition(self):
        label = self.top_label("Simple Answer")

        circle, square = self.shape_morph_left()
        self.place_left(circle)

        card_content = self.card_lines(
            "Python is a programming language.",
            "That means we write instructions,",
            "and the computer follows them.",
            "Usually.",
            font_size=26,
        )
        card, _ = self.white_card(card_content, side="right", height=3.8)

        self.play(FadeIn(label), GrowFromCenter(card), Create(circle), run_time=0.7)
        self.type_lines(*card_content[:3], time_per_char=0.05)
        self.play(ReplacementTransform(circle, square), run_time=0.9)
        self.type_text(card_content[3], time_per_char=0.06)
        self.play(Wiggle(card_content[3]), run_time=0.7)
        self.wait(3)
        self.fade_clear(label, square, card)

    def beat_04_why_python_for_ai(self):
        label = self.top_label("Why Python for AI?")

        pills = VGroup(self.mini_pill("Data"), self.mini_pill("Math"), self.mini_pill("Code")).arrange(RIGHT, buff=0.2)
        ai = self.mini_pill("AI")
        ai.next_to(pills, DOWN, buff=0.45)
        arrows = VGroup(*[
            Arrow(p.get_bottom(), ai.get_top() + UP * 0.03, buff=0.05, color=WHITE, stroke_width=2,
                  max_tip_length_to_length_ratio=0.18)
            for p in pills
        ])
        left = VGroup(pills, arrows, ai).arrange(DOWN, buff=0.25)
        self.place_left(left)

        card_content = self.card_lines(
            "AI needs three things:",
            "data, math, and code.",
            "Python helps us connect all three.",
            font_size=26,
        )
        card, _ = self.white_card(card_content, side="right", height=3.2)

        self.play(FadeIn(label), GrowFromCenter(card), run_time=0.6)
        self.type_text(card_content[0], time_per_char=0.05)
        self.play(LaggedStart(*[FadeIn(p, shift=UP * 0.1) for p in pills], lag_ratio=0.15), run_time=0.8)
        self.play(Create(arrows), FadeIn(ai), run_time=0.7)
        self.type_text(card_content[1], time_per_char=0.05)
        self.type_text(card_content[2], time_per_char=0.05)
        self.play(Indicate(card_content[2], color=YELLOW), run_time=0.7)
        self.wait(3)
        self.fade_clear(label, left, card)

    def beat_05_real_world_use(self):
        label = self.top_label("Python Shows Up Everywhere")

        shapes = VGroup(Circle(radius=0.25, color=WHITE, stroke_width=2),
                        Square(side_length=0.45, color=WHITE, stroke_width=2),
                        RegularPolygon(6, radius=0.25, color=WHITE, stroke_width=2))
        names = self.bg_lines("AI", "Web", "Robots", font_size=22)
        left = VGroup(*[VGroup(s, n).arrange(RIGHT, buff=0.15) for s, n in zip(shapes, names)])
        left.arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        self.place_left(left)

        items = ["AI chatbots", "recommendation systems", "data analysis",
                 "automation", "websites", "robots"]
        rows = VGroup(*[
            VGroup(self.yellow_check(), self.on_card(it, font_size=21)).arrange(RIGHT, buff=0.1)
            for it in items
        ]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        subtitle = self.on_card("Used in real projects,\nnot just classrooms.", font_size=22)
        card_content = VGroup(subtitle, rows).arrange(DOWN, buff=0.28, aligned_edge=LEFT)
        card, _ = self.white_card(card_content, side="right", height=4.6)

        self.play(FadeIn(label), FadeIn(left), GrowFromCenter(card), run_time=0.7)
        self.type_text(subtitle, time_per_char=0.05)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.12) for r in rows], lag_ratio=0.1), run_time=1.6)
        self.wait(3)
        self.fade_clear(label, left, card)

    def beat_06_tiny_truth(self):
        label = self.top_label("Tiny Python Truth")

        # Card on LEFT for variety; potato animation on RIGHT
        card_content = self.card_lines(
            "Python was designed to be readable.",
            "Your code should look less like",
            "alien language…",
            "and more like instructions",
            "for a very obedient potato.",
            font_size=24,
        )
        card, _ = self.white_card(card_content, side="left", height=4.2)

        potato = self.drawn_potato().scale(1.05)
        bubble = RoundedRectangle(width=2.3, height=0.5, corner_radius=0.1, color=WHITE, stroke_width=2)
        bubble_text = Text("I await your command.", font_size=15, color=BLACK)
        bubble_text.move_to(bubble.get_center())
        right = VGroup(VGroup(bubble, bubble_text), potato).arrange(DOWN, buff=0.12)
        self.place_right(right)

        self.play(FadeIn(label), GrowFromCenter(card), run_time=0.6)
        self.type_lines(*card_content[:3], time_per_char=0.04)
        self.wait(0.3)
        self.type_lines(*card_content[3:], time_per_char=0.04)
        self.play(FadeIn(right), run_time=0.6)
        self.wait(2.5)
        self.fade_clear(label, card, right)

    def beat_07_not_the_snake(self):
        label = self.top_label("Important Snake News")

        snake_word = self.on_bg("snake", font_size=26)
        snake_box = SurroundingRectangle(snake_word, color=WHITE, buff=0.12, stroke_width=1.5)
        cross = Cross(VGroup(snake_box, snake_word), stroke_color=WHITE, stroke_width=4)
        sleeping = self.drawn_sleeping_snake()
        left = VGroup(VGroup(snake_box, snake_word), cross, sleeping).arrange(DOWN, buff=0.3)
        self.place_left(left)

        card_content = self.card_lines(
            "Python the language",
            "is NOT named after the snake.",
            "So relax.",
            "No reptiles will jump out",
            "when you write code.",
            "Probably.",
            font_size=24,
        )
        card, _ = self.white_card(card_content, side="right", height=4.4)

        self.play(FadeIn(label), GrowFromCenter(card), run_time=0.6)
        self.type_lines(*card_content, time_per_char=0.04)
        self.play(FadeIn(left), Create(cross), run_time=0.55)
        self.play(Wiggle(card_content[-1]), run_time=0.6)
        self.wait(3)
        self.fade_clear(label, left, card)

    def beat_08_today_mission(self):
        label = self.top_label("Today's Mission")

        mini = RoundedRectangle(width=2.2, height=0.9, corner_radius=0.1, color=WHITE, stroke_width=2)
        mini_text = self.bg_lines("Project 01", "Hello World", font_size=22, )
        mini_text.move_to(mini.get_center())
        arrow = Arrow(UP * 0.35, DOWN * 0.35, color=YELLOW, stroke_width=3)
        left = VGroup(VGroup(mini, mini_text), arrow).arrange(DOWN, buff=0.35)
        self.place_left(left)

        card_content = self.card_lines(
            "You will write your first Python project.",
            "It will be small.",
            "It will be powerful.",
            "It will say hello.",
            "Very dramatic.",
            font_size=24,
        )
        card, _ = self.white_card(card_content, side="right", height=4.2)

        self.play(FadeIn(label), FadeIn(left), GrowFromCenter(card), run_time=0.7)
        self.type_lines(*card_content, time_per_char=0.04)
        self.play(Indicate(mini_text[1], color=YELLOW), run_time=0.55)
        self.wait(2)
        self.fade_clear(label, left, card)

    def beat_09_open_editor(self):
        label = self.top_label("Step 1")

        editor, cursor = self.drawn_editor()
        self.place_left(editor.scale(0.9))

        card_content = self.card_lines(
            "Open your code editor",
            "or course coding playground.",
            "No installation today.",
            "We are here to write code,",
            "not fight software demons.",
            font_size=24,
        )
        card, _ = self.white_card(card_content, side="right", height=4.0)

        self.play(FadeIn(label), FadeIn(editor), GrowFromCenter(card), run_time=0.7)
        self.type_lines(*card_content, time_per_char=0.04)
        self.blink_mobject(cursor, times=2)
        self.wait(2.5)
        self.fade_clear(label, editor, card)

    def beat_10_create_file(self):
        label = self.top_label("Step 2")

        file_icon = RoundedRectangle(width=0.75, height=0.85, corner_radius=0.07, color=WHITE, stroke_width=2)
        fname = self.on_bg("first_project.py", font_size=24)
        fname_box = SurroundingRectangle(fname, color=WHITE, buff=0.14, stroke_width=2)
        left = VGroup(file_icon, VGroup(fname_box, fname)).arrange(DOWN, buff=0.22)
        self.place_left(left)

        card_content = self.card_lines(
            "Create a new file named:",
            "first_project.py",
            "This is your first Python project file.",
            "Please treat it with respect.",
            "It is only one line old.",
            font_size=24,
        )
        card, _ = self.white_card(card_content, side="right", height=4.2)

        self.play(FadeIn(label), FadeIn(left), GrowFromCenter(card), run_time=0.7)
        self.type_text(card_content[0], time_per_char=0.05)
        self.play(Indicate(card_content[1], color=YELLOW), run_time=0.55)
        self.type_lines(*card_content[2:], time_per_char=0.04)
        self.wait(2.5)
        self.fade_clear(label, left, card)

    def beat_11_write_first_code(self):
        label = self.top_label("Step 3")

        code_group, code_text, code_border = self.code_box('print("Hello, World!")')
        self.place_left(code_group)

        card_content = self.card_lines("Type this exact line:", font_size=28)
        card, _ = self.white_card(card_content, side="right", height=2.4)

        self.play(FadeIn(label), GrowFromCenter(card), run_time=0.6)
        self.type_text(card_content[0], time_per_char=0.05)
        self.play(Create(code_border), run_time=0.45)
        self.type_text(code_text, time_per_char=0.07, leave_cursor_on=True, blink=3)
        self.wait(4)

        self.b11_label = label
        self.b11_left = code_group
        self.b11_card = card

    def beat_12_explain_print(self):
        label = self.top_label("What Did We Just Write?")

        code_group, _, _ = self.code_box('print("Hello, World!")')
        output, output_text = self.output_box("Hello, World!")
        arrow = Arrow(code_group.get_bottom(), output.get_top(), buff=0.08, color=WHITE, stroke_width=2)
        left = VGroup(code_group, arrow, output).arrange(DOWN, buff=0.18)
        self.place_left(left)

        card_content = self.card_lines(
            "print means: show this on the screen.",
            "This code tells Python:",
            '"Please display Hello, World!"',
            "Very polite. Very professional.",
            font_size=24,
        )
        card, _ = self.white_card(card_content, side="right", height=3.5)

        self.fade_clear(self.b11_label, self.b11_left, self.b11_card, run_time=0.45)
        self.play(FadeIn(label), FadeIn(left), GrowFromCenter(card), run_time=0.65)
        self.type_lines(*card_content, time_per_char=0.04)
        self.type_text(output_text, time_per_char=0.05)
        self.wait(3)
        self.fade_clear(label, left, card)

    def beat_13_run_the_code(self):
        label = self.top_label("Step 4")

        output, output_text = self.output_box("Hello, World!")
        laptop = self.drawn_laptop().scale(0.85)
        left = VGroup(laptop, output).arrange(DOWN, buff=0.3)
        self.place_left(left)

        card_content = self.card_lines(
            "Now run the file.",
            "Python reads your line…",
            "then prints: Hello, World!",
            "Congratulations.",
            "You have officially bossed",
            "a computer around.",
            font_size=24,
        )
        card, _ = self.white_card(card_content, side="right", height=4.5)

        self.play(FadeIn(label), FadeIn(laptop), GrowFromCenter(card), run_time=0.7)
        self.type_lines(*card_content[:3], time_per_char=0.04)
        self.play(FadeIn(output), run_time=0.4)
        self.type_text(output_text, time_per_char=0.05)
        self.type_lines(*card_content[3:], time_per_char=0.04)
        self.wait(3)
        self.fade_clear(label, left, card)

    def beat_14_ai_connection(self):
        label = self.top_label("AI Connection")

        card_content = self.card_lines(
            "This tiny line is the beginning.",
            "Later, Python will help us read data,",
            "train models, make predictions,",
            "and build AI projects.",
            "Every big AI journey starts",
            "with one small print.",
            font_size=22,
        )
        card, _ = self.white_card(card_content, side="left", height=4.5)

        stack = VGroup(*[self.mini_pill(item) for item in ["Hello World", "Data", "Model", "AI Project"]])
        stack[0].add(SurroundingRectangle(stack[0], color=YELLOW, buff=0.07, stroke_width=2))
        arrows = VGroup(*[
            Arrow(stack[i].get_bottom(), stack[i + 1].get_top(), buff=0.05, color=WHITE, stroke_width=2,
                  max_tip_length_to_length_ratio=0.15)
            for i in range(len(stack) - 1)
        ])
        right = VGroup()
        for i, s in enumerate(stack):
            right.add(s)
            if i < len(arrows):
                right.add(arrows[i])
        right.arrange(DOWN, buff=0.1)
        self.place_right(right)

        self.play(FadeIn(label), GrowFromCenter(card), run_time=0.65)
        self.type_text(card_content[0], time_per_char=0.05)
        self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.08) for s in stack], lag_ratio=0.16), run_time=0.9)
        self.type_lines(*card_content[1:], time_per_char=0.04)
        self.play(Indicate(stack[0], color=YELLOW), run_time=0.55)
        self.wait(3)
        self.fade_clear(label, card, right)

    def beat_15_student_challenge(self):
        label = self.top_label("Mini Challenge")

        code, _, _ = self.code_box('print("Hello, future AI engineer!")', font_size=17)
        output, output_text = self.output_box("Hello, future AI engineer!")
        heart = self.drawn_heart()
        left = VGroup(code, output, heart).arrange(DOWN, buff=0.25)
        self.place_left(left)

        card_content = self.card_lines(
            "Change your code to say:",
            "Then run it again.",
            "If your computer can say nice things…",
            "that is already emotional support.",
            font_size=24,
        )
        card, _ = self.white_card(card_content, side="right", height=3.8)

        self.play(FadeIn(label), GrowFromCenter(card), run_time=0.65)
        self.type_text(card_content[0], time_per_char=0.05)
        self.play(FadeIn(code), run_time=0.4)
        self.type_lines(*card_content[1:], time_per_char=0.04)
        self.play(FadeIn(output), FadeIn(heart), run_time=0.4)
        self.type_text(output_text, time_per_char=0.05)
        self.play(Wiggle(card_content[-1]), run_time=0.65)
        self.wait(3.5)
        self.fade_clear(label, left, card)

    def beat_16_beginner_mistake(self):
        label = self.top_label("Beginner Warning")

        card_content = self.card_lines(
            "Python cares about spelling.",
            "The computer is powerful…",
            "not forgiving.",
            font_size=26,
        )
        card, _ = self.white_card(card_content, side="left", height=2.8)

        good, _, _ = self.code_box('print("Hello, World!")', font_size=18)
        bad, _, _ = self.code_box('pritn("Hello, World!")', font_size=18)
        right = VGroup(
            VGroup(self.label("WORKS", font_size=18), good).arrange(DOWN, buff=0.1),
            VGroup(self.label("DOES NOT WORK", font_size=18), bad).arrange(DOWN, buff=0.1),
        ).arrange(DOWN, buff=0.3)
        self.place_right(right)

        self.play(FadeIn(label), GrowFromCenter(card), FadeIn(right), run_time=0.7)
        self.type_text(card_content[0], time_per_char=0.05)
        self.play(Wiggle(bad), run_time=0.55)
        self.type_lines(*card_content[1:], time_per_char=0.04)
        self.wait(3)
        self.fade_clear(label, card, right)

    def beat_17_recap(self):
        label = self.top_label("Quick Recap")

        circle, square = self.shape_morph_left()
        self.place_left(circle)

        items = [
            "Python is a programming language.",
            "It is very useful for AI.",
            "print shows text on the screen.",
            "Your first project says Hello, World!",
        ]
        rows = VGroup(*[
            VGroup(self.yellow_check(), self.on_card(it, font_size=20)).arrange(RIGHT, buff=0.08)
            for it in items
        ]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        card, _ = self.white_card(rows, side="right", height=3.8)

        self.play(FadeIn(label), Create(circle), GrowFromCenter(card), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.1) for r in rows], lag_ratio=0.14), run_time=1.2)
        self.play(ReplacementTransform(circle, square), run_time=0.8)
        self.play(Indicate(rows[-1], color=YELLOW), run_time=0.55)
        self.wait(3)
        self.fade_clear(label, square, card)

    def beat_18_ending(self):
        label = self.top_label("Project Complete")

        rocket = self.drawn_rocket()
        badge = RoundedRectangle(width=3.4, height=0.55, corner_radius=0.1, color=WHITE, stroke_width=2)
        badge_text = self.on_bg("Python Project 01 Complete", font_size=20)
        badge_text.move_to(badge.get_center())
        left = VGroup(rocket, VGroup(badge, badge_text)).arrange(DOWN, buff=0.35)
        self.place_left(left)

        card_content = self.card_lines(
            "You just wrote your first Python program.",
            "It did not build a robot army… yet.",
            "But it did prove one thing:",
            "you can give instructions to a computer.",
            "And that is where AI begins.",
            font_size=24,
        )
        card, _ = self.white_card(card_content, side="right", height=4.2)

        self.play(FadeIn(label), FadeIn(left), GrowFromCenter(card), run_time=0.7)
        self.type_lines(*card_content, time_per_char=0.04)
        self.play(GrowFromCenter(badge), run_time=0.45)
        self.wait(3)
        self.fade_to_black(label, left, card, self.bg)
