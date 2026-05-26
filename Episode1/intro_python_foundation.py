"""Episode 1 — intro_python_foundation (beats 1–3, camera + transitions)."""

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "animations"))

from beat_helpers import MovingBeatScene


def _load_runner(beat_dir: str, module_file: str, func_name: str):
    path = ROOT / "Episode1" / "beats" / beat_dir / module_file
    spec = importlib.util.spec_from_file_location(f"{beat_dir}_{module_file}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return getattr(module, func_name)


run_beat_01 = _load_runner("beat1", "welcome_to_python.py", "run_beat_01_welcome_to_python")
run_beat_02 = _load_runner("beat2", "what_is_python.py", "run_beat_02_what_is_python")
run_beat_03 = _load_runner("beat3", "simple_answer.py", "run_beat_03_simple_answer")


class IntroPythonFoundation(MovingBeatScene):
    def construct(self):
        self.setup_background()
        run_beat_01(self, use_camera=True)
        self.beat_transition(run_time=0.8, hold=0.25)
        run_beat_02(self, use_camera=True)
        self.beat_transition(run_time=0.8, hold=0.25)
        run_beat_03(self, use_camera=True)
        self.cam_restore(run_time=0.5)
