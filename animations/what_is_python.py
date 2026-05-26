from manim import *
from manim.utils.rate_functions import smooth

BG_PATH = "/Users/enfec/manimations/background/orange_theme_BG.png"
LOGO_PATH = "/Users/enfec/manimations/background/python.png"


class WhatIsPython(Scene):
    def construct(self):
        bg = ImageMobject(BG_PATH)
        bg.scale_to_fit_width(config.frame_width)
        bg.move_to(ORIGIN)
        self.add(bg)

        self.play_welcome_intro()
        self.scene_what_is_python()
        self.scene_popular_language()
        self.scene_used_in()
        self.scene_fun_fact_one()
        self.scene_fun_fact_two()
        self.scene_not_the_snake()
        self.scene_joke()

    # ------------------------------------------------------------------ helpers
    def fade_clear(self, *mobjects, run_time=0.6):
        if mobjects:
            self.play(*[FadeOut(m) for m in mobjects], run_time=run_time, rate_func=smooth)

    def title_text(self, text, font_size=52, color=WHITE):
        return Text(text, font_size=font_size, color=color, weight=BOLD)

    def body_text(self, text, font_size=40, color=WHITE):
        return Text(text, font_size=font_size, color=color, weight=BOLD)

    def fun_fact_box(self, number, body, body_font_size=36):
        label = Text(f"Fun Fact #{number}", font_size=34, color=YELLOW, weight=BOLD)
        content = Text(body, font_size=body_font_size, color=WHITE, weight=BOLD)
        group = VGroup(label, content).arrange(DOWN, buff=0.35)
        box = SurroundingRectangle(group, color=YELLOW, stroke_width=2, buff=0.35)
        return VGroup(box, group)

    # ---------------------------------------------------------- welcome intro
    def play_welcome_intro(self):
        welcome_to_text = self.title_text("Welcome to", font_size=60)
        welcome_to_text.set_x(0).set_y(1.5)

        course_text = self.title_text("Python for AI Course", font_size=72)
        course_text.set_x(0).set_y(-0.5)

        logo = ImageMobject(LOGO_PATH)
        logo.set_height(1.2)
        logo.next_to(course_text, DOWN, buff=0.5)

        self.play(Write(welcome_to_text), run_time=0.8)
        self.play(Write(course_text), run_time=0.8)
        self.play(FadeIn(logo), run_time=1.0)
        self.wait(1.5)
        self.fade_clear(welcome_to_text, course_text, logo)

    # ---------------------------------------------- "what exactly is Python?"
    def scene_what_is_python(self):
        question = self.title_text("So first… what exactly is Python?", font_size=48)
        question.move_to(ORIGIN)

        python_highlight = SurroundingRectangle(
            question, color=YELLOW, buff=0.2, stroke_width=3
        )
        python_highlight.set_opacity(0)

        self.play(Write(question), run_time=1.2)
        self.play(Create(python_highlight), run_time=0.6)
        self.play(Indicate(question, color=YELLOW, scale_factor=1.05), run_time=0.8)
        self.wait(1.2)
        self.fade_clear(question, python_highlight)

    # ---------------------------------------- world's most popular language
    def scene_popular_language(self):
        statement = self.title_text(
            "Python is one of the world's\nmost popular programming languages.",
            font_size=44,
        )
        statement.move_to(ORIGIN)

        badge = RoundedRectangle(
            width=5.5, height=1.0, corner_radius=0.2, color=GREEN, fill_opacity=0.25
        )
        badge_label = Text("Top 3 Worldwide", font_size=28, color=GREEN, weight=BOLD)
        badge_group = VGroup(badge, badge_label)
        badge_label.move_to(badge.get_center())
        badge_group.next_to(statement, DOWN, buff=0.6)

        globe = Circle(radius=0.35, color=BLUE, fill_opacity=0.4)
        globe.next_to(statement, UP, buff=0.5)

        self.play(FadeIn(globe, scale=0.5), run_time=0.5)
        self.play(Write(statement), run_time=1.4)
        self.play(GrowFromCenter(badge_group), run_time=0.7)
        self.wait(1.5)
        self.fade_clear(statement, badge_group, globe)

    # ---------------------------------------------------------- "It's used in"
    def scene_used_in(self):
        header = self.title_text("It's used in:", font_size=52, color=YELLOW)
        header.to_edge(UP, buff=0.8)

        uses = [
            ("AI", YELLOW),
            ("websites", BLUE),
            ("games", GREEN),
            ("automation", TEAL),
            ("hacking", RED),
            ("data science", MAROON_A),
            ("robotics", PURPLE),
            ("machine learning", GOLD),
            ("space research", "#87CEEB"),
        ]

        pills = VGroup()
        for label, color in uses:
            pill = RoundedRectangle(
                width=2.8, height=0.65, corner_radius=0.15, color=color, fill_opacity=0.35
            )
            text = Text(label, font_size=26, color=WHITE, weight=BOLD)
            text.move_to(pill.get_center())
            pills.add(VGroup(pill, text))

        pills.arrange_in_grid(rows=3, cols=3, buff=(0.45, 0.35))
        pills.next_to(header, DOWN, buff=0.55)

        self.play(Write(header), run_time=0.8)
        self.play(
            LaggedStart(*[FadeIn(p, shift=UP * 0.3) for p in pills], lag_ratio=0.12),
            run_time=2.5,
        )
        self.play(Flash(pills[0], color=YELLOW, flash_radius=0.8), run_time=0.4)
        self.play(Flash(pills[8], color=YELLOW, flash_radius=0.8), run_time=0.4)
        self.wait(1.5)
        self.fade_clear(header, pills)

    # -------------------------------------------------------- fun fact #1
    def scene_fun_fact_one(self):
        fact = self.fun_fact_box(
            1,
            "NASA, Netflix, Google,\nand Instagram all use Python.",
            body_font_size=38,
        )
        fact.move_to(ORIGIN)

        companies = VGroup(
            self.body_text("NASA", font_size=30, color=YELLOW),
            self.body_text("Netflix", font_size=30, color=RED),
            self.body_text("Google", font_size=30, color=BLUE),
            self.body_text("Instagram", font_size=30, color="#E1306C"),
        )
        companies.arrange(RIGHT, buff=0.55)
        companies.next_to(fact, DOWN, buff=0.5)

        self.play(GrowFromCenter(fact), run_time=0.9)
        self.play(
            LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in companies], lag_ratio=0.15),
            run_time=1.2,
        )
        self.wait(1.8)
        self.fade_clear(fact, companies)

    # -------------------------------------------------------- fun fact #2
    def scene_fun_fact_two(self):
        fact = self.fun_fact_box(
            2,
            "Python was created by\nGuido van Rossum in 1991.",
            body_font_size=38,
        )
        fact.move_to(ORIGIN)

        year_circle = Circle(radius=0.55, color=YELLOW, fill_opacity=0.2)
        year_label = Text("1991", font_size=32, color=YELLOW, weight=BOLD)
        year_label.move_to(year_circle.get_center())
        year_group = VGroup(year_circle, year_label)
        year_group.next_to(fact, DOWN, buff=0.45)

        self.play(GrowFromCenter(fact), run_time=0.9)
        self.play(SpinInFromNothing(year_group), run_time=0.7)
        self.wait(1.8)
        self.fade_clear(fact, year_group)

    # ------------------------------------------- NOT named after the snake
    def scene_not_the_snake(self):
        also = self.body_text("Also…", font_size=44, color=YELLOW)
        also.to_edge(UP, buff=1.0)

        not_snake = self.title_text(
            "the language is NOT\nnamed after the snake.",
            font_size=42,
        )
        not_snake.next_to(also, DOWN, buff=0.55)

        snake_icon = Text("Snake", font_size=36, color=GREEN, weight=BOLD)
        snake_box = SurroundingRectangle(snake_icon, color=GREEN, buff=0.2)
        snake_group = VGroup(snake_box, snake_icon)
        snake_group.next_to(not_snake, LEFT, buff=0.6)

        cross = Cross(snake_group, stroke_color=RED, stroke_width=6)

        self.play(Write(also), run_time=0.6)
        self.play(Write(not_snake), run_time=1.0)
        self.play(FadeIn(snake_group, shift=RIGHT * 0.3), run_time=0.6)
        self.play(Create(cross), run_time=0.5)
        self.wait(1.5)

        monty = self.title_text(
            "It's actually named after a comedy show\ncalled Monty Python's Flying Circus.",
            font_size=36,
            color=YELLOW,
        )
        monty.next_to(not_snake, DOWN, buff=0.65)

        circus_arc = Arc(radius=1.1, angle=PI, color=GOLD).next_to(monty, DOWN, buff=0.15)
        circus = Text("Flying Circus", font_size=28, color=GOLD, weight=BOLD, slant=ITALIC)
        circus.move_to(circus_arc.get_center())

        self.play(FadeOut(snake_group, cross), run_time=0.4)
        self.play(FadeOut(not_snake), FadeIn(monty, shift=UP * 0.2), run_time=1.0, rate_func=smooth)
        self.play(Create(circus_arc), Write(circus), run_time=1.0)
        self.wait(1.5)
        self.fade_clear(also, monty, circus_arc, circus)

    # ---------------------------------------------------------------- joke
    def scene_joke(self):
        setup = self.body_text(
            "So if you were scared of snakes…\ngood news.",
            font_size=40,
        )
        setup.move_to(ORIGIN + UP * 0.8)

        punchline = self.title_text(
            "The only thing Python bites\nis your sleep schedule.",
            font_size=44,
            color=YELLOW,
        )
        punchline.next_to(setup, DOWN, buff=0.6)

        joke_box = SurroundingRectangle(
            VGroup(setup, punchline), color=GREEN, stroke_width=2, buff=0.4
        )

        moon = Circle(radius=0.25, color=GRAY, fill_opacity=0.6)
        moon.next_to(punchline, RIGHT, buff=0.5)

        self.play(Write(setup), run_time=1.0)
        self.wait(0.5)
        self.play(Create(joke_box), Write(punchline), FadeIn(moon), run_time=1.2)
        self.play(Wiggle(punchline), run_time=1.0)
        self.play(Indicate(punchline, color=YELLOW), run_time=0.8)
        self.wait(2.0)
        self.fade_clear(setup, punchline, joke_box, moon, run_time=1.0)
