from manim import *

class DecoratorCodeTyping(MovingCameraScene):
    def construct(self):
        # Add a title first
        title = Text("Python Decorator Pattern", font_size=40, color=YELLOW, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title), run_time=1.5)
        self.wait(0.5)
        
        # Create the code as text
        code_text = Text(
            "# Simple decorator\n\n"
            "def greet_decorator(func):\n"
            "    def wrapper():\n"
            "        print(\"Hello\")\n"
            "        func()\n"
            "        print(\"Goodbye\")\n"
            "    return wrapper\n\n"
            "@greet_decorator\n"
            "def say_name():\n"
            "    print(\"I am Divyanshu\")\n\n"
            "say_name()",
            font_size=18,
            font="Courier New",
            color=WHITE,
            line_spacing=1.4,
        )
        
        code_text.move_to(ORIGIN).shift(DOWN * 0.5)
        
        # Create a box around the code area
        code_box = SurroundingRectangle(code_text, color=BLUE, stroke_width=2, buff=0.3)
        
        # Show the box first
        self.play(Create(code_box), run_time=1)
        self.wait(0.3)
        
        # Zoom in on the code box
        self.play(self.camera.frame.animate.scale(0.8).move_to(code_text), run_time=1)
        self.wait(0.3)
        
        # Animate code appearing with typing effect inside the box
        self.play(Write(code_text), run_time=10)
        
        self.wait(1)
        
        # Zoom back out to normal
        self.play(self.camera.frame.animate.scale(1.25).move_to(ORIGIN), run_time=1.5)
        self.wait(0.5)
        
        # Create explanation boxes
        decorator_explanation = Text("@greet_decorator\napplies wrapper\nto function", font_size=14, color=YELLOW)
        decorator_explanation.to_edge(RIGHT, buff=0.5)
        decorator_explanation.shift(UP * 1.5)
        
        # Zoom and pan to decorator explanation
        self.play(self.camera.frame.animate.scale(0.7).move_to(decorator_explanation), run_time=1)
        self.wait(0.2)
        
        self.play(Create(SurroundingRectangle(decorator_explanation, color=YELLOW, stroke_width=2)), 
                  Write(decorator_explanation), run_time=1.5)
        self.wait(1)
        
        # Zoom back out
        self.play(self.camera.frame.animate.scale(1.43).move_to(ORIGIN), run_time=1)
        self.wait(0.5)
        
        # Output box
        output_text = Text("Output:\nHello\nI am Divyanshu\nGoodbye", font_size=14, color=GREEN)
        output_text.to_edge(RIGHT, buff=0.5)
        output_text.shift(DOWN * 1.5)
        
        # Zoom and pan to output
        self.play(self.camera.frame.animate.scale(0.7).move_to(output_text), run_time=1)
        self.wait(0.2)
        
        self.play(Create(SurroundingRectangle(output_text, color=GREEN, stroke_width=2)), 
                  Write(output_text), run_time=1.5)
        self.wait(2)
        
        # Final zoom out to see everything
        self.play(self.camera.frame.animate.scale(1.43).move_to(ORIGIN), run_time=1.5)
        self.wait(1)
        
        # Fade everything out
        self.play(FadeOut(VGroup(code_text, code_box, title, decorator_explanation, output_text)), run_time=1)
