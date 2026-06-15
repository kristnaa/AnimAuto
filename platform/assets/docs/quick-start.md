# Quick start

Get Manimations Studio running locally in a few minutes.

## Prerequisites

- Python 3.11+ with the repo Manim venv
- Node.js 18+
- OpenAI API key
- **ffmpeg** (required for **Voice motion** — mux narration into MP4). macOS: `brew install ffmpeg`

## Setup

1. **Environment**

```bash
cp platform/.env.example platform/.env
# Add OPENAI_API_KEY=sk-...
```

2. **Backend** (uses repo Manim for rendering)

```bash
chmod +x platform/start-backend.sh platform/start-frontend.sh platform/start.sh
./platform/start-backend.sh
```

3. **Frontend** (separate terminal)

```bash
./platform/start-frontend.sh
```

4. Open **http://127.0.0.1:5173**

Or run both: `./platform/start.sh`

## First project

**Beat studio (themed slides):**

1. On the **Projects hub**, click **New project** → **Beat studio**.
2. **Pick or create a theme** — background, typography, palette.
3. Describe your animation in **Chat**, or switch to **Beat script** and paste from the template.
4. Wait for preview render — progress shows **percentage + phase**.
5. Click **1080p60** when ready for HD export.

**Voice motion (narration → shapes):**

1. **New project** → **Voice motion** (no theme required).
2. In **Chat**, upload narration (MP3/WAV/M4A) and click **Send**.
3. Studio transcribes with Whisper, generates a Manim scene, renders, and **muxes your voice** into the preview.

See [Voice motion](voice-motion) for details.

## Two-phase flow

Studio separates **ingest** (fast) from **render** (slow):

| Phase | What happens | Endpoint |
|-------|--------------|----------|
| Ingest | Parse/save beats | `POST /chat`, `POST /script`, `PUT /beats` |
| Render | Manim preview (420p) | `POST /render` → poll `/render-status` (~400ms) |
| Export | 1080p60 | `POST /export` → poll `/export-status` |

After editing beats, use **Re-render** in the preview toolbar. Chat may show “Rendering…” while the follow-up render runs.

## Long scripts (avoid 4+ minute videos)

Full narration essays (like a 5-minute YouTube intro) must be split into **many short beats**, not one beat per paragraph.

| Guideline | Target |
|-----------|--------|
| Beats | 14–18 for a ~2 min episode |
| Card lines | Max **3** per beat, ~**55 characters** each |
| Hold | **0.9–1.2s** between beats |
| Pacing | Studio auto-switches to **dense** for long imports |

Check the header warning: **Est. runtime ~120s (2.0 min)** before rendering. If you see **4+ min**, open **Beats**, shorten lines, lower **Hold**, or split into two projects.

Preview render waits up to **30 minutes** for Manim; very long videos still take longer to encode.

## Example Chat prompts

- "Create a 3-beat intro: welcome to Python, what is Python?, simple answer with joke."
- "Create a code_demo beat showing a Python decorator."
- "Change beat 2 to use slide_from_right icon entrance and triple_top grid."
- "Make beat 1 continue into beat 2 without fading to black."

## Deployment

For VPS / DigitalOcean with Nginx + Docker, see `platform/DEPLOY-DIGITALOCEAN.md`. The frontend SPA serves `/docs` routes via `try_files … /index.html`.

## Related

- [Studio UI](studio-ui) — full interface tour
- [Beat script format](beat-script) — structured authoring
