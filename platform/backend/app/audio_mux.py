"""Mux narration audio into rendered Manim MP4 via ffmpeg."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def mux_audio_video(video_path: Path, audio_path: Path, output_path: Path) -> Path:
    """Combine silent video with narration track; trim to shortest stream."""
    if not ffmpeg_available():
        raise RuntimeError(
            "ffmpeg is not installed. Install ffmpeg to mux voice into the final video."
        )
    if not video_path.is_file():
        raise FileNotFoundError(f"Video not found: {video_path}")
    if not audio_path.is_file():
        raise FileNotFoundError(f"Audio not found: {audio_path}")

    output_path = output_path.resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tmp:
        tmp_path = Path(tmp.name)

    try:
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(video_path),
            "-i",
            str(audio_path),
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(tmp_path),
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            tail = (proc.stderr or proc.stdout or "")[-2000:]
            raise RuntimeError(f"ffmpeg mux failed:\n{tail}")
        if output_path.exists():
            output_path.unlink()
        shutil.move(str(tmp_path), str(output_path))
        return output_path
    finally:
        if tmp_path.exists():
            tmp_path.unlink(missing_ok=True)
