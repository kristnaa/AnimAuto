"""Load beat JSON embedded in generated scene files."""

from __future__ import annotations

import json
import re


def load_beat_json(raw: str) -> dict:
    """Parse beat JSON; strips trailing commas (common after manual code edits)."""
    cleaned = re.sub(r",(\s*[}\]])", r"\1", raw)
    return json.loads(cleaned)
