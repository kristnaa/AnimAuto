"""Voice director: transcript → sentences → page storyboard."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from app.voice_layouts import (
    ICON_IDS,
    LAYOUT_IDS,
    default_page_for_sentence,
    enforce_visual_page,
    icon_catalog_for_prompt,
    layout_catalog_for_prompt,
    normalize_page,
)

MANIM_ROOT = Path(__file__).resolve().parents[3]
VOICE_DIRECTOR_SKILL = MANIM_ROOT / ".cursor/skills/manim-video/voice-director.md"
STYLE_REFERENCES_DIR = MANIM_ROOT / ".cursor/skills/manim-video/style-references"
MAX_PAGES = 40
BATCH_SIZE = 6
MIN_SENTENCE_DURATION = 0.35


def load_style_reference_notes() -> str:
    """Load optional text notes alongside PNG/SVG screenshots in style-references/."""
    if not STYLE_REFERENCES_DIR.is_dir():
        return ""
    parts: list[str] = []
    for path in sorted(STYLE_REFERENCES_DIR.iterdir()):
        if path.name.upper() == "README.MD":
            continue
        if path.suffix.lower() in (".md", ".txt"):
            parts.append(f"### {path.name}\n{path.read_text(encoding='utf-8')[:2000]}")
        elif path.suffix.lower() in (".png", ".jpg", ".jpeg", ".webp", ".svg"):
            parts.append(f"- Reference image: `{path.name}` (place notes in a matching .md file)")
    if not parts:
        return ""
    header = ""
    if any(p.name.startswith("blackboard-") for p in STYLE_REFERENCES_DIR.iterdir() if p.suffix.lower() == ".md"):
        header = "**Active aesthetic: blackboard explainer** (black bg, chalk white text, yellow arrows, colored icons — NOT whiteboard).\n\n"
    return header + "## Style references (match mood/composition)\n" + "\n\n".join(parts)


def load_director_skill() -> str:
    skill = VOICE_DIRECTOR_SKILL.read_text(encoding="utf-8") if VOICE_DIRECTOR_SKILL.is_file() else layout_catalog_for_prompt()
    refs = load_style_reference_notes()
    return skill + ("\n\n" + refs if refs else "")


def _transcription_to_dict(transcription: Any) -> dict[str, Any]:
    if hasattr(transcription, "model_dump"):
        return transcription.model_dump()
    if isinstance(transcription, dict):
        return transcription
    return {"text": str(transcription), "segments": [], "words": []}


def _parse_words(data: dict[str, Any]) -> list[dict[str, Any]]:
    words: list[dict[str, Any]] = []
    for w in data.get("words") or []:
        if isinstance(w, dict):
            word = str(w.get("word", "")).strip()
            if not word:
                continue
            words.append(
                {
                    "word": word,
                    "start": round(float(w.get("start", 0)), 3),
                    "end": round(float(w.get("end", w.get("start", 0))), 3),
                }
            )
    return words


def transcribe_with_words(openai_client: Any, audio_path: Path) -> dict[str, Any]:
    with audio_path.open("rb") as handle:
        raw = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=handle,
            response_format="verbose_json",
            timestamp_granularities=["word", "segment"],
        )
    data = _transcription_to_dict(raw)
    words = _parse_words(data)
    segments: list[dict[str, Any]] = []
    for seg in data.get("segments") or []:
        if isinstance(seg, dict):
            text = str(seg.get("text", "")).strip()
            if text:
                segments.append(
                    {
                        "start": round(float(seg.get("start", 0)), 2),
                        "end": round(float(seg.get("end", 0)), 2),
                        "text": text,
                    }
                )
    duration = float(data.get("duration") or (segments[-1]["end"] if segments else 0))
    transcript = str(data.get("text") or " ".join(s["text"] for s in segments)).strip()
    sentences = split_sentences(transcript, words, segments)
    return {
        "transcript": transcript,
        "duration_sec": round(duration, 2),
        "words": words,
        "segments": segments,
        "sentences": sentences,
    }


def split_sentences(
    transcript: str,
    words: list[dict[str, Any]],
    segments: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    text = re.sub(r"\s+", " ", (transcript or "").strip())
    if not text:
        return []

    raw_parts = re.split(r"(?<=[.!?])\s+", text)
    parts = [p.strip() for p in raw_parts if p.strip()]
    if not parts:
        parts = [text]

    sentences: list[dict[str, Any]] = []
    word_idx = 0

    for i, part in enumerate(parts):
        part_words = re.findall(r"\S+", part)
        if not part_words:
            continue
        matched: list[dict[str, Any]] = []
        search_from = word_idx
        for pw in part_words:
            pw_clean = re.sub(r"[^\w']", "", pw.lower())
            found = False
            for j in range(search_from, len(words)):
                ww = re.sub(r"[^\w']", "", words[j]["word"].lower())
                if ww == pw_clean or ww.startswith(pw_clean) or pw_clean.startswith(ww):
                    matched.append(words[j])
                    search_from = j + 1
                    found = True
                    break
            if not found and search_from < len(words):
                matched.append(words[search_from])
                search_from += 1

        if matched:
            start = matched[0]["start"]
            end = matched[-1]["end"]
            word_idx = search_from
        elif segments:
            seg = segments[min(i, len(segments) - 1)]
            start = float(seg["start"])
            end = float(seg["end"])
        elif sentences:
            start = sentences[-1]["end"] + 0.05
            end = start + max(MIN_SENTENCE_DURATION, len(part.split()) * 0.28)
        else:
            start = 0.0
            end = max(MIN_SENTENCE_DURATION, len(part.split()) * 0.28)

        sentences.append(
            {
                "id": f"s{i + 1:02d}",
                "text": part if part[-1] in ".!?" else part + ".",
                "start": round(start, 2),
                "end": round(max(end, start + MIN_SENTENCE_DURATION), 2),
            }
        )

    return cap_sentences(sentences)


def _merge_sentence_pair(a: dict[str, Any], b: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "id": f"s{index + 1:02d}",
        "text": f"{a['text'].rstrip('.!?')} {b['text']}".strip(),
        "start": a["start"],
        "end": b["end"],
    }


def cap_sentences(sentences: list[dict[str, Any]], max_pages: int = MAX_PAGES) -> list[dict[str, Any]]:
    """Reduce sentence count to max_pages by merging adjacent sentences."""
    if len(sentences) <= max_pages:
        return sentences

    merged = list(sentences)
    while len(merged) > max_pages:
        prev_len = len(merged)
        reduced: list[dict[str, Any]] = []
        i = 0
        while i < len(merged):
            remaining_items = len(merged) - i
            remaining_slots = max_pages - len(reduced)
            if remaining_items <= remaining_slots:
                for j in range(i, len(merged)):
                    reduced.append({**merged[j], "id": f"s{len(reduced) + 1:02d}"})
                break

            a = merged[i]
            dur = a["end"] - a["start"]
            can_merge = i + 1 < len(merged)
            should_merge = can_merge and (
                dur < 2.0 or remaining_items > remaining_slots
            )
            if should_merge:
                reduced.append(_merge_sentence_pair(a, merged[i + 1], len(reduced)))
                i += 2
            else:
                reduced.append({**a, "id": f"s{len(reduced) + 1:02d}"})
                i += 1

        if len(reduced) >= prev_len:
            # Guaranteed progress: merge fixed-size buckets.
            bucket_size = max(2, (len(merged) + max_pages - 1) // max_pages)
            forced: list[dict[str, Any]] = []
            for start in range(0, len(merged), bucket_size):
                chunk = merged[start : start + bucket_size]
                if len(chunk) == 1:
                    forced.append({**chunk[0], "id": f"s{len(forced) + 1:02d}"})
                else:
                    acc = chunk[0]
                    for other in chunk[1:]:
                        acc = {
                            "text": f"{acc['text'].rstrip('.!?')} {other['text']}".strip(),
                            "start": acc["start"],
                            "end": other["end"],
                        }
                    forced.append({**acc, "id": f"s{len(forced) + 1:02d}"})
            reduced = forced

        merged = reduced

    return merged


def analyze_transcript(openai_client: Any, model: str, transcript: str, sentences: list[dict]) -> dict[str, Any]:
    payload = json.dumps({"transcript": transcript, "sentence_count": len(sentences)}, indent=2)
    response = openai_client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "Analyze narration for a motion-graphics video. Return JSON: "
                    '{"summary","topic","audience","pacing","visual_density":"low|medium|high"}'
                ),
            },
            {"role": "user", "content": payload},
        ],
        response_format={"type": "json_object"},
        temperature=0.3,
    )
    raw = response.choices[0].message.content or "{}"
    data = json.loads(raw)
    if not data.get("summary"):
        data["summary"] = transcript[:80] + ("…" if len(transcript) > 80 else "")
    return data


def design_pages(
    openai_client: Any,
    model: str,
    sentences: list[dict[str, Any]],
    analysis: dict[str, Any],
) -> list[dict[str, Any]]:
    skill = load_director_skill()
    catalog = layout_catalog_for_prompt() + "\n\n" + icon_catalog_for_prompt()
    pages: list[dict[str, Any]] = []

    for batch_start in range(0, len(sentences), BATCH_SIZE):
        batch = sentences[batch_start : batch_start + BATCH_SIZE]
        payload = json.dumps(
            {
                "analysis": analysis,
                "sentences": batch,
                "page_index_offset": batch_start,
            },
            indent=2,
        )
        response = openai_client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": skill + "\n\n" + catalog},
                {
                    "role": "user",
                    "content": (
                        "Design one VISUAL page per sentence. Narration is audio-only — "
                        "use short labels (see text limits), not full sentences. "
                        "Vary background_style each page.\n"
                        f"Layouts: {', '.join(LAYOUT_IDS)}.\n{payload}"
                    ),
                },
            ],
            response_format={"type": "json_object"},
            temperature=0.35,
        )
        raw = response.choices[0].message.content or "{}"
        data = json.loads(raw)
        batch_pages = data.get("pages") or []
        if not isinstance(batch_pages, list):
            batch_pages = []
        for j, sentence in enumerate(batch):
            idx = batch_start + j
            if j < len(batch_pages) and isinstance(batch_pages[j], dict):
                pages.append(normalize_page(batch_pages[j], sentence, idx))
            else:
                pages.append(default_page_for_sentence(sentence, idx))

    return pages


def align_pages_to_sentences(
    pages: list[dict[str, Any]], sentences: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Sync timing to sentences; keep visual labels from director (not full transcript)."""
    by_id = {s["id"]: s for s in sentences if isinstance(s, dict) and s.get("id")}
    for i, page in enumerate(pages):
        sid = page.get("sentence_id")
        sentence = by_id.get(sid) or (sentences[i] if i < len(sentences) else None)
        if not sentence:
            continue
        page["start"] = float(sentence.get("start", page.get("start", 0)))
        page["end"] = float(sentence.get("end", page.get("end", page["start"] + 1)))
        page["sentence_text"] = str(sentence.get("text") or page.get("sentence_text") or "")
        enforce_visual_page(page, i)
    return pages


def validate_director_plan(pages: list[dict[str, Any]], duration_sec: float) -> list[str]:
    issues: list[str] = []
    if not pages:
        issues.append("No pages in director plan")
        return issues
    if len(pages) > MAX_PAGES:
        issues.append(f"Too many pages ({len(pages)} > {MAX_PAGES})")
    prev_end = 0.0
    for p in pages:
        start = float(p.get("start", 0))
        end = float(p.get("end", start))
        if end <= start:
            issues.append(f"Page {p.get('id')} has invalid timing")
        if start < prev_end - 0.05:
            issues.append(f"Page {p.get('id')} overlaps previous")
        if p.get("layout") not in LAYOUT_IDS:
            issues.append(f"Page {p.get('id')} has unknown layout")
        prev_end = end
    if duration_sec and prev_end > duration_sec + 2.0:
        issues.append("Pages extend beyond audio duration")
    return issues


def run_storyboard_pipeline(
    openai_client: Any,
    model: str,
    audio_path: Path,
    *,
    existing_voice: dict[str, Any] | None = None,
    retranscribe: bool = False,
) -> dict[str, Any]:
    if existing_voice and existing_voice.get("sentences") and not retranscribe:
        transcript_data = {
            "transcript": existing_voice.get("transcript", ""),
            "duration_sec": existing_voice.get("duration_sec", 0),
            "words": existing_voice.get("words") or [],
            "segments": existing_voice.get("segments") or [],
            "sentences": existing_voice.get("sentences") or [],
        }
    else:
        transcript_data = transcribe_with_words(openai_client, audio_path)

    sentences = transcript_data["sentences"]
    analysis = analyze_transcript(openai_client, model, transcript_data["transcript"], sentences)
    pages = design_pages(openai_client, model, sentences, analysis)
    pages = align_pages_to_sentences(pages, sentences)
    plan = {"summary": analysis.get("summary", ""), "analysis": analysis, "pages": pages}
    warnings = validate_director_plan(pages, float(transcript_data.get("duration_sec") or 0))

    return {
        **transcript_data,
        "director_plan": plan,
        "storyboard_status": "draft",
        "storyboard_warnings": warnings,
    }
