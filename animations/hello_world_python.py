from manim import *

class HelloWorldToPython(MovingCameraScene):
    def construct(self):
        # Create "Hello World" text
        hello_world = Text("Hello World", font_size=60, color=BLUE)
        hello_world.move_to(ORIGIN)
        
        # Add title
        title = Text("Text Animation with Camera Shift", font_size=32, color=YELLOW)
        title.to_edge(UP, buff=0.5)
        
        self.add(title)
        
        # Animate "Hello World" appearing with Write animation
        self.play(Write(hello_world), run_time=2)
        self.wait(1)
        
        # Save camera state
        self.camera.frame.save_state()
        
        # Move "Hello World" to the left
        self.play(hello_world.animate.shift(LEFT * 3.5), run_time=1.5)
        self.wait(0.5)
        
        # Create "Python" text
        python_text = Text("Python", font_size=60, color=GREEN)
        python_text.move_to(RIGHT * 3.5)
        
        # Camera zooms in and focuses on the area where Python will appear
        self.play(self.camera.frame.animate.scale(0.9), run_time=0.8)
        self.wait(0.3)
        
        # Animate "Python" appearing
        self.play(Write(python_text), run_time=2)
        self.wait(1)
        
        # Camera pans to show both texts
        self.play(self.camera.frame.animate.scale(1.2).move_to(ORIGIN), run_time=1.5)
        self.wait(1)
        
        # Create connecting line
        line = Line(hello_world.get_right(), python_text.get_left(), color=YELLOW, stroke_width=3)
        self.play(Create(line), run_time=1)
        self.wait(1)
        
        # Add a plus sign in the middle
        plus_sign = Text("+", font_size=50, color=RED)
        plus_sign.move_to((hello_world.get_right() + python_text.get_left()) / 2)
        
        # Camera zooms in on the middle area
        self.play(
            self.camera.frame.animate.scale(0.8).move_to(plus_sign),
            run_time=1
        )
        self.wait(0.3)
        
        self.play(Write(plus_sign), run_time=1)
        self.wait(1)
        
        # Camera zooms back out to see everything
        self.play(self.camera.frame.animate.scale(1.25).move_to(ORIGIN), run_time=1.5)
        self.wait(1)
        
        # Restore camera to initial state
        self.play(Restore(self.camera.frame), run_time=1)
        self.wait(1)
        
        # Fade out all elements
        self.play(FadeOut(hello_world, python_text, line, plus_sign, title), run_time=1)
        self.wait(0.5)
