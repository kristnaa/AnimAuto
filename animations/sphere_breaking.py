from manim import *
import numpy as np

class SphereBreaking(Scene):
    def construct(self):
        # Create ground
        ground = Line(LEFT * 6, RIGHT * 6, color=GREY, stroke_width=4)
        ground.shift(DOWN * 3)
        
        # Add ground
        self.add(ground)
        
        # Create a large sphere
        sphere = Sphere(
            center=np.array([0, 2, 0]),
            radius=0.5,
            color=BLUE,
            resolution=(20, 20)
        )
        
        self.add(sphere)
        
        # Add title
        title = Text("Sphere Breaking Animation", font_size=36, color=YELLOW)
        title.to_edge(UP, buff=0.3)
        self.add(title)
        
        # Animate sphere falling
        fall_animation = sphere.animate.shift(DOWN * 5)
        self.play(fall_animation, run_time=2)
        
        # Create impact effect (dust particles)
        dust_particles = VGroup()
        for i in range(8):
            angle = i * PI / 4
            particle = Dot(radius=0.08, color=GREY)
            particle.move_to(np.array([0.5 * np.cos(angle), -3, 0.5 * np.sin(angle)]))
            dust_particles.add(particle)
        
        # Animate dust particles spreading out
        self.play(
            *[dust.animate.shift(np.array([
                0.3 * np.cos(i * PI / 4), 
                0.2, 
                0.3 * np.sin(i * PI / 4)
            ])) for i, dust in enumerate(dust_particles)],
            run_time=0.5
        )
        
        self.wait(0.3)
        
        # Remove original sphere
        self.remove(sphere)
        
        # Create left hemisphere
        left_half = Sphere(
            center=np.array([-0.3, -3, 0]),
            radius=0.5,
            color=BLUE,
            resolution=(20, 20)
        )
        
        # Create right hemisphere
        right_half = Sphere(
            center=np.array([0.3, -3, 0]),
            radius=0.5,
            color=BLUE,
            resolution=(20, 20)
        )
        
        # Add the two halves
        self.add(left_half, right_half)
        
        # Animate the two halves moving apart
        self.play(
            left_half.animate.shift(LEFT * 0.5 + UP * 0.3),
            right_half.animate.shift(RIGHT * 0.5 + UP * 0.3),
            run_time=1
        )
        
        self.wait(0.5)
        
        # Animate the two halves falling and rotating
        self.play(
            left_half.animate.shift(DOWN * 1).rotate(PI / 4),
            right_half.animate.shift(DOWN * 1).rotate(-PI / 4),
            run_time=1.5
        )
        
        # Fade dust particles
        self.play(FadeOut(dust_particles), run_time=0.5)
        
        self.wait(1)
        
        # Fade everything out
        self.play(FadeOut(title, left_half, right_half, ground), run_time=1)
