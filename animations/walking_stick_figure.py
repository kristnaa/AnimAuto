from manim import *

class WalkingStickFigure(Scene):
    def construct(self):
        # Create a stick figure
        def create_stick_figure(x_offset=0):
            """Create a stick figure at a given x position"""
            # Head
            head = Circle(radius=0.3, color=WHITE, fill_opacity=0)
            head.move_to([x_offset, 1.5, 0])
            
            # Body
            body = Line([x_offset, 1.2, 0], [x_offset, 0.6, 0], color=WHITE, stroke_width=2)
            
            # Left arm
            left_arm = Line([x_offset, 1.0, 0], [x_offset - 0.4, 0.8, 0], color=WHITE, stroke_width=2)
            
            # Right arm
            right_arm = Line([x_offset, 1.0, 0], [x_offset + 0.4, 0.8, 0], color=WHITE, stroke_width=2)
            
            # Left leg
            left_leg = Line([x_offset, 0.6, 0], [x_offset - 0.3, 0, 0], color=WHITE, stroke_width=2)
            
            # Right leg
            right_leg = Line([x_offset, 0.6, 0], [x_offset + 0.3, 0, 0], color=WHITE, stroke_width=2)
            
            return VGroup(head, body, left_arm, right_arm, left_leg, right_leg)
        
        def create_walking_stick_figure(x_offset=0, leg_angle=0):
            """Create a stick figure in walking pose"""
            # Head
            head = Circle(radius=0.3, color=WHITE, fill_opacity=0)
            head.move_to([x_offset, 1.5, 0])
            
            # Body
            body = Line([x_offset, 1.2, 0], [x_offset, 0.6, 0], color=WHITE, stroke_width=2)
            
            # Swinging arms (opposite to legs)
            if leg_angle > 0:  # Right leg forward
                left_arm = Line([x_offset, 1.0, 0], [x_offset - 0.3, 0.85, 0], color=WHITE, stroke_width=2)
                right_arm = Line([x_offset, 1.0, 0], [x_offset + 0.3, 0.75, 0], color=WHITE, stroke_width=2)
                
                # Left leg forward
                left_leg = Line([x_offset, 0.6, 0], [x_offset - 0.25, -0.05, 0], color=WHITE, stroke_width=2)
                # Right leg back
                right_leg = Line([x_offset, 0.6, 0], [x_offset + 0.35, 0.05, 0], color=WHITE, stroke_width=2)
            else:  # Left leg forward
                left_arm = Line([x_offset, 1.0, 0], [x_offset - 0.3, 0.75, 0], color=WHITE, stroke_width=2)
                right_arm = Line([x_offset, 1.0, 0], [x_offset + 0.3, 0.85, 0], color=WHITE, stroke_width=2)
                
                # Right leg forward
                right_leg = Line([x_offset, 0.6, 0], [x_offset + 0.25, -0.05, 0], color=WHITE, stroke_width=2)
                # Left leg back
                left_leg = Line([x_offset, 0.6, 0], [x_offset - 0.35, 0.05, 0], color=WHITE, stroke_width=2)
            
            return VGroup(head, body, left_arm, right_arm, left_leg, right_leg)
        
        # Create the stick figure
        stick_figure = create_walking_stick_figure(x_offset=-3)
        self.add(stick_figure)
        
        # Animate walking by moving the figure and changing poses
        for i in range(4):
            # Create walking pose
            new_figure = create_walking_stick_figure(x_offset=-3 + i * 1.5, leg_angle=i % 2)
            self.play(
                Transform(stick_figure, new_figure),
                run_time=0.6
            )
        
        # Wait a moment
        self.wait(1)
        
        # Final pose
        final_figure = create_stick_figure(x_offset=1.5)
        self.play(Transform(stick_figure, final_figure), run_time=0.5)
        
        self.wait(2)
