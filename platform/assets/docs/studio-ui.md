# Studio UI

Overview of every major surface in Manimations Studio.

## Projects hub

The landing screen when you open Studio.

| Action | Description |
|--------|-------------|
| **New project** | **Beat studio** (theme + beats) or **Voice motion** (narration → Manim shapes) |
| **Open** | Resume a saved project |
| **Rename / delete** | Manage projects from the hub card menu |
| **Deep link** | `?project={id}` opens a project directly |

Last opened project is stored in `localStorage` for quick resume.

## Header (top bar)

| Control | Description |
|---------|-------------|
| **Logo** | Manimations Studio branding |
| **Documentation** (book icon) | Opens `/docs` in a new tab — left of the project name |
| **Project name** | Current project title |
| **Theme dropdown** | Switch project theme *(beat studio only)* |
| **Voice motion badge** | Shown instead of theme picker on voice projects |
| **Projects** | Return to hub |
| **Revert** | Restore local version snapshots |

## Left panel tabs

### Chat

Plain-English prompts → AI updates beats **or** motion scene code → auto preview render.

- **Voice motion** toggle + **Upload audio** under the message box
- Shift+Enter for newline, Enter to send
- Voice projects: Send with audio uploads transcribes and generates; later messages edit the scene

See [Voice motion](voice-motion).

### Beat script

Paste structured beat scripts or JSON. Click **Generate from script** to parse and save.

- **View template** — starter script with all sections
- **Use AI author** — rough narration → full script (optional)
- Beat type picker with live layout preview

### Beats

Visual **beat timeline** editor with per-beat tabs:

| Tab | What you edit |
|-----|----------------|
| **Content** | Label, type, layout, hold, continue beat; **statement beats** also show card mode, text, image/video upload |
| **Icon** | Icon entrance + full-height icon picker |
| **Emphasis** | Highlight words — word, hex color swatch, animation (indicate / wiggle) |
| **Camera** | Per-beat moving camera toggle, camera steps (action, hook, duration), load type defaults |

**Beat script tab:** After picking **Statement**, use **Statement layout** chips (**Full card**, **Icon + card**, **Card + icon**, **Card only**) for live preview and template insert.

*(Beat script and Beats tabs are hidden for voice motion projects.)*

Timeline toolbar (icon-only): duplicate, delete, add beat. **Save beats** persists to the project and syncs the Beat script tab.

Timeline badges show emphasis count (`E2`), camera steps (`C3`), and `cam` when camera is enabled on a beat.

## Right panel

### Preview (420p / `-ql`)

- Video player for `latest.mp4`
- **Progress bar with percentage** — e.g. `23% — Animation 4 (50%)` during compile and Manim render
- **Cancel render** while preview is running
- **Re-render** after beat changes

Rendering is async: `POST /render` returns immediately; the UI polls `/render-status` every ~400ms.

### Export (1080p60)

- Background HD export with progress percentage and phase text
- Auto-download when complete

### Code

- Auto-generated Manim scene from beats
- Edit manually → **Apply & Re-render**
- **From beats** — regenerate code (discards manual edits)

## Validation

Before render, Studio may warn about missing icons or layout mismatches (`validate-beats`). Warnings appear in the header — fix in Beats tab or script.

## Related

- [Beat types](beat-types)
- [Beat script format](beat-script)
- [Cards & emphasis](cards-emphasis)
- [Camera](camera)
- [API reference](api-reference)
