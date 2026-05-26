from manim import *

class HelloWorld(Scene):
    def construct(self):
        # Create the text "Hello World"
        text = Text("Hello World", font_size=72)
        
        # Add the text to the scene
        self.add(text)
        
        # Animate the text appearing with a fade-in effect
        self.play(Write(text), run_time=2)
        
        # Wait for 2 seconds
        self.wait(2)
        
        # Animate the text disappearing with a fade-out effect
        self.play(FadeOut(text), run_time=2)
