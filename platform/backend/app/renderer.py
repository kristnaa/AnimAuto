"""Manim render subprocess."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

MANIM_ROOT = Path(__file__).resolve().parents[3]
MANIM_PYTHON = MANIM_ROOT / ".venv" / "bin" / "python"


def detect_scene_class_from_file(scene_file: Path) -> str:
    try:
        source = scene_file.read_text()
    except OSError:
        return "GeneratedScene"
    match = re.search(
        r"class\s+(\w+)\s*\(\s*(?:MovingCameraScene|BeatScene|MovingBeatScene|Scene)",
        source,
    )
    return match.group(1) if match else "GeneratedScene"


def render_scene(
    scene_file: Path,
    scene_class: str = "GeneratedScene",
    quality: str = "-ql",
    output_mp4: Path | None = None,
) -> Path:
    scene_file = scene_file.resolve()
    if scene_class == "GeneratedScene":
        scene_class = detect_scene_class_from_file(scene_file)

    if output_mp4:
        output_mp4 = output_mp4.resolve()
        output_mp4.parent.mkdir(parents=True, exist_ok=True)
        if output_mp4.exists():
            output_mp4.unlink()

    python = str(MANIM_PYTHON) if MANIM_PYTHON.exists() else sys.executable
    cmd = [
        python,
        "-m",
        "manim",
        "render",
        "--flush_cache",
        quality,
        str(scene_file),
        scene_class,
    ]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(MANIM_ROOT / "animations") + os.pathsep + env.get("PYTHONPATH", "")

    result = subprocess.run(
        cmd,
        cwd=str(MANIM_ROOT),
        env=env,
        capture_output=True,
        text=True,
        timeout=900 if quality == "-qh" else 300,
    )
    if result.returncode != 0:
        raise RuntimeError(f"Manim render failed:\n{result.stderr[-3000:]}")

    # Find latest mp4 under media/videos for this scene
    media = MANIM_ROOT / "media" / "videos"
    candidates = sorted(
        media.rglob(f"{scene_class}.mp4"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not candidates:
        raise FileNotFoundError("Rendered MP4 not found")

    mp4 = candidates[0]
    if output_mp4:
        shutil.copy2(mp4, output_mp4)
        return output_mp4
    return mp4
