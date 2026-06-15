"""Static demo matching the Why Python + How Python Works reference screenshots."""

from manim import *
from blackboard_elements import (
    draw_sketchy,
    layout_mind_map_radial,
    layout_pipeline_blackboard,
    page_background_blackboard_clean,
)


class WhyPythonReference(Scene):
    """Radial mind map like blackboard-why-python.png."""

    def construct(self):
        self.camera.background_color = BLACK
        self.add(page_background_blackboard_clean())
        chart = layout_mind_map_radial(
            "Python",
            [
                {"label": "High Demand", "icon_id": "bar_chart_up", "highlight": "Demand"},
                {"label": "Power Simple", "icon_id": "rocket", "highlight": "Simple"},
                {
                    "label": "Everywhere",
                    "icon_id": "swiss_knife",
                    "highlight": "Everywhere",
                    "sub_labels": ["Automation", "Web", "Gaming", "Data"],
                    "sub_icons": ["robot_arm", "globe", "gamepad", "chart_lines"],
                },
                {"label": "Community", "icon_id": "crowd", "highlight": "Community"},
                {"label": "AI", "icon_id": "brain_gear", "highlight": "AI"},
            ],
            hub_tag="WHY",
            mode="full",
            title="Why Python",
        )
        draw_sketchy(self, chart, run_time=1.8)
        self.wait(2)


class HowPythonWorksReference(Scene):
    """Pipeline like blackboard-python-flow.png."""

    def construct(self):
        self.camera.background_color = BLACK
        self.add(page_background_blackboard_clean())
        chart = layout_pipeline_blackboard(
            [
                {"label": "Source", "icon_id": "document_py"},
                {
                    "label": "Interpreter",
                    "icon_id": "gear_process",
                    "nested": ["Compiler", "Bytecode", "VM"],
                    "nested_icons": ["gear_process", "document_py", "cube_vm"],
                },
                {"label": "Output", "icon_id": "pac_output", "binary_strip": "1011001"},
            ],
            title="How Python Works",
        )
        draw_sketchy(self, chart, run_time=1.8)
        self.wait(2)
