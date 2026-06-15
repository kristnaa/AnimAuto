# Voice motion mode

Create **motion-graphics videos from narration** — no themes, beat templates, cards, or icons.

## Two-step flow

1. **New project** → choose **Voice motion** (or enable **Voice motion** in Chat)
2. **Upload audio** — MP3, WAV, M4A, etc. (max 25 MB)
3. **Generate storyboard** — Whisper transcribes with word timestamps → Director Agent splits **sentences** and designs one **page** per sentence (layout, headline, animations)
4. **Review** — edit headlines, swap layout templates (center title, flowchart, bullets, etc.)
5. **Approve & generate video** — deterministic Manim codegen from the storyboard → render → **ffmpeg muxes your voice** into `latest.mp4`

Use **Send** in Chat to generate the storyboard from audio, or click **Generate storyboard** in the panel.

## Visual style

- Black background (`#000000`)
- White `Text()` for narration lines
- Colorful Manim shapes (`Circle`, `Arrow`, `RoundedRectangle`, etc.)
- `TypeWithCursor` typing animations via `voice_motion_helpers`
- No Iconify icons, no white cards, no theme background

## Layout templates

| Layout | Use when |
|--------|----------|
| `center_title` | Hook, section header |
| `center_subtitle` | Single key line |
| `center_bullets` | List in one sentence |
| `flowchart_vertical` | Process steps top-to-bottom |
| `flowchart_horizontal` | Pipeline left-to-right |
| `compare_columns` | Before/after, vs |
| `diagram_labeled` | Concept + caption |
| `kinetic_keywords` | Emphasis word |
| `fade_transition` | Bridge between sections |

## Chat after codegen

Type edits in Chat — e.g. *"Add a blue circle when I say Python"* — the LLM updates `generated_scene.py`. Use the **Code** tab for manual tweaks.

## Requirements

- `OPENAI_API_KEY` — transcription (Whisper) + director + optional chat edits
- **ffmpeg** — mux narration into the final MP4 (`brew install ffmpeg` on macOS)

Check health: `GET /api/health` includes `ffmpeg_available`.

## API

| Endpoint | Purpose |
|----------|---------|
| `POST /api/projects` with `creation_mode: voice_motion` | Create voice project |
| `POST /api/projects/{id}/voice/upload` | Upload narration |
| `POST /api/projects/{id}/voice/storyboard` | Transcribe + director → `director_plan` |
| `GET /api/projects/{id}/voice/storyboard` | Sentences + pages for UI |
| `PATCH /api/projects/{id}/voice/storyboard` | Edit page layout/headline/order |
| `POST /api/projects/{id}/voice/storyboard/approve` | Approve storyboard |
| `POST /api/projects/{id}/voice/generate` | Compile scene (requires approved storyboard) |
| `GET /api/projects/{id}/voice` | Full voice_motion payload |
| `POST /api/projects/{id}/chat` | Edit motion scene (voice projects) |

## Project JSON

```json
{
  "creation_mode": "voice_motion",
  "voice_motion": {
    "audio_ref": "media/narration.mp3",
    "duration_sec": 42.5,
    "transcript": "Hello everyone…",
    "words": [{ "word": "Hello", "start": 0.12, "end": 0.38 }],
    "sentences": [{ "id": "s01", "text": "Hello everyone.", "start": 0, "end": 1.8 }],
    "director_plan": {
      "summary": "Intro to AI tools",
      "pages": [{
        "id": "p01",
        "sentence_id": "s01",
        "start": 0,
        "end": 1.8,
        "layout": "center_title",
        "headline": "Hello everyone"
      }]
    },
    "storyboard_status": "draft",
    "segments": [{ "start": 0, "end": 4.2, "text": "Hello everyone" }],
    "motion_plan": []
  },
  "beats": [],
  "code_customized": true
}
```

## Related

- [Studio UI](studio-ui)
- [Quick start](quick-start)
