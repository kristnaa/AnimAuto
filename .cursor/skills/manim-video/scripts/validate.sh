#!/bin/bash
# Quick-render a Manim scene for validation (low quality, no auto-open).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../../../.." && pwd)"
source "$ROOT/.venv/bin/activate"

if [ "$#" -lt 2 ]; then
  echo "Usage: validate.sh <scene_file.py> <SceneClassName> [manim flags...]"
  echo "Example: validate.sh animations/welcome_ai_course.py WelcomeAICourse"
  exit 1
fi

SCENE_FILE="$1"
SCENE_NAME="$2"
shift 2

manim -ql "$@" "$ROOT/$SCENE_FILE" "$SCENE_NAME"

SCRIPT_BASE="$(basename "$SCENE_FILE" .py)"
VIDEO="$ROOT/media/videos/$SCRIPT_BASE/480p15/${SCENE_NAME}.mp4"

if [ -f "$VIDEO" ]; then
  echo "OK: $VIDEO"
else
  echo "Render finished but video not found at expected path: $VIDEO"
  exit 1
fi
