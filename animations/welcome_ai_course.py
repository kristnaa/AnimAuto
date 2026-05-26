from manim import *
from manim.utils.rate_functions import smooth

class WelcomeAICourse(Scene):
    def construct(self):
        # Load PNG background image
        bg = ImageMobject("/Users/enfec/manimations/background/orange_theme_BG.png")
        bg.scale_to_fit_width(config.frame_width)
        bg.move_to(ORIGIN)
        
        # Add background first (will be behind everything)
        self.add(bg)
        
        # Create "Welcome to" text, center aligned
        welcome_to_text = Text(
            "Welcome to",
            font_size=60,
            color=WHITE,
            weight=BOLD
        )
        welcome_to_text.set_x(0)  # Center horizontally
        welcome_to_text.set_y(1.5)  # Position above
        
        # Create "Python for AI Course" text, center aligned
        course_text = Text(
            "Python for AI Course",
            font_size=72,
            color=WHITE,
            weight=BOLD
        )
        course_text.set_x(0)  # Center horizontally
        course_text.set_y(-0.5)  # Position below
        
        # Animate both texts writing - fast
        self.play(Write(welcome_to_text), run_time=0.8)
        self.play(Write(course_text), run_time=0.8)
        # Add Python logo below the course text
        logo = ImageMobject("/Users/enfec/manimations/background/python.png")
        logo.set_height(1.2)
        logo.next_to(course_text, DOWN, buff=0.5)
        self.play(FadeIn(logo), run_time=1.0)
        self.wait(1.5)
        
        # SMOOTH TRANSITION: Fade out first screen while keeping background
        # Second screen starts blank
        self.play(
            FadeOut(welcome_to_text),
            FadeOut(course_text),
            FadeOut(logo),
            run_time=0.6
        )
        
        # Second screen: Writing your first Python program
        # Create texts but don't add them yet - start blank
        topic_text = Text(
            "Writing your first",
            font_size=60,
            color=WHITE,
            weight=BOLD
        )
        topic_text.set_x(0)
        topic_text.set_y(1.5)
        
        program_text = Text(
            "Python Program",
            font_size=72,
            color=WHITE,
            weight=BOLD
        )
        program_text.set_x(0)
        program_text.set_y(0.2)
        
        hello_world_text = Text(
            'print("Hello World")',
            font_size=64,
            color=YELLOW,
            weight=BOLD
        )
        hello_world_text.set_x(0)
        hello_world_text.set_y(-1.5)
        
        # Second screen starts blank - add texts one by one
        self.play(Write(topic_text), run_time=0.8)
        self.play(Write(program_text), run_time=0.8)
        self.wait(0.8)
        
        # Animate Hello World code
        self.play(Write(hello_world_text), run_time=0.8)
        self.wait(3)
        
        # PROFESSIONAL LAYERED FADE: Multiple objects fade with timing
        self.play(
            FadeOut(topic_text),
            FadeOut(program_text),
            FadeOut(hello_world_text),
            run_time=1.0,
            rate_func=smooth
        )
        self.wait(0.5)
