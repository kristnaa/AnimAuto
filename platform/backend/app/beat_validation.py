"""Pre-render validation for beat visuals and content."""

from __future__ import annotations

from typing import Any

from beat_pacing import duration_warnings, estimate_project_seconds
from statement_content import is_statement_full_card, normalize_statement_block, resolve_statement_mode


def validate_beats(beats: list[dict], *, pacing: str | None = None) -> dict[str, Any]:
    issues: list[dict] = []
    warnings: list[dict] = []

    for i, beat in enumerate(beats):
        label = beat.get("label") or f"Beat {i + 1}"
        beat_type = (beat.get("type") or "").lower()
        layout = beat.get("layout") or ""

        has_text = bool(
            beat.get("card_lines")
            or beat.get("bg_lines")
            or beat.get("list_lines")
            or beat.get("code_lines")
            or beat.get("left_lines")
            or beat.get("right_lines")
        )
        if not has_text and beat_type != "code_demo":
            warnings.append(
                {
                    "beat_index": i,
                    "label": label,
                    "code": "empty_content",
                    "message": "Beat has no text or code lines.",
                }
            )

        visuals = beat.get("visuals_resolved") or beat.get("visuals") or {}
        primary = visuals.get("primary") if isinstance(visuals, dict) else None
        stack = visuals.get("stack") if isinstance(visuals, dict) else None

        if beat_type not in ("code_demo", "compare") and layout != "dual_card":
            if is_statement_full_card(beat):
                block = normalize_statement_block(beat)
                mode = resolve_statement_mode(block)
                has_content = bool(block.get("text_lines")) or (
                    isinstance(block.get("image"), dict) and block["image"].get("ref")
                ) or (isinstance(block.get("video"), dict) and block["video"].get("ref"))
                if not has_content:
                    warnings.append(
                        {
                            "beat_index": i,
                            "label": label,
                            "code": "empty_statement",
                            "message": "Statement beat has no text, image, or video content.",
                        }
                    )
            elif not primary and not stack:
                if beat_type in ("statement", "question", "joke", "explain", "recap", "list"):
                    warnings.append(
                        {
                            "beat_index": i,
                            "label": label,
                            "code": "missing_visual",
                            "message": "No icon/visual resolved for this beat.",
                        }
                    )

        if isinstance(primary, dict):
            if not (primary.get("ref") or primary.get("concept") or primary.get("description")):
                issues.append(
                    {
                        "beat_index": i,
                        "label": label,
                        "code": "invalid_primary",
                        "message": "Primary visual is empty.",
                    }
                )

        if beat.get("bg_lines") and "text_" not in layout:
            warnings.append(
                {
                    "beat_index": i,
                    "label": label,
                    "code": "layout_mismatch",
                    "message": "bg_lines used but layout is not a text-on-background layout.",
                }
            )

        for key in ("card_lines", "bg_lines", "list_lines"):
            lines = beat.get(key)
            if isinstance(lines, list):
                for line in lines:
                    if len(str(line)) > 72:
                        warnings.append(
                            {
                                "beat_index": i,
                                "label": label,
                                "code": "long_line",
                                "message": (
                                    f"Line longer than 72 chars will be split at render "
                                    f"({len(str(line))} chars)."
                                ),
                            }
                        )
                        break

    estimated_seconds = estimate_project_seconds(beats, pacing)
    warnings.extend(duration_warnings(beats, pacing))

    return {
        "valid": len(issues) == 0,
        "issue_count": len(issues),
        "warning_count": len(warnings),
        "estimated_seconds": estimated_seconds,
        "estimated_label": f"~{estimated_seconds:.0f}s ({estimated_seconds / 60:.1f} min)",
        "issues": issues,
        "warnings": warnings,
    }
