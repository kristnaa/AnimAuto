#!/bin/bash
# Simple script to run manim with the virtual environment activated

source /Users/enfec/manimations/.venv/bin/activate
manim -ql "$@"

# Extract the scene name (last argument)
SCENE_NAME="${@: -1}"

# Open the video file if it exists
VIDEO_FILE="/Users/enfec/manimations/media/videos/$(echo "$2" | sed 's/\.py//' | sed 's|animations/||')/480p15/${SCENE_NAME}.mp4"

if [ -f "$VIDEO_FILE" ]; then
    open "$VIDEO_FILE"
fi
