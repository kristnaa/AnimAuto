# Statement beat

The **statement** beat is a yellow **label** plus one **full-width card** below it (margins preserved). Everything you show the viewer lives **inside that card** — not in a separate icon panel.

## Layout

```
LAYOUT: statement_full_card
```

```
┌─────────────────────────────────────────┐
│  LABEL (yellow, top)                    │
├─────────────────────────────────────────┤
│ ┌─────────────────────────────────────┐ │
│ │  Full-width white card              │ │
│ │  (text / image / video / combo)     │ │
│ └─────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

## Content modes

| Mode | What's inside the card |
|------|-------------------------|
| `text` | Typed black lines only |
| `image` | Uploaded image only |
| `video` | Looping video clip only |
| `text_image` | Lines on top, image below |
| `text_video` | Lines on top, video below |
| `text_image_video` | All three stacked |
| `auto` | Detect from what you filled in |

## Beats editor

1. Set beat **Type** to **Statement**
2. Stay on the **Content** tab — the **Statement card** section appears below label/type/layout
3. Pick **Card content mode**
4. Add **text**, **upload image**, and/or **upload video**

In the **Beat script** tab, pick **Statement** then choose a **Statement layout** sub-option: **Full card**, **Icon + card**, **Card + icon**, or **Card only**. Each updates the live preview and the inserted template block.

The **Icon** tab stays available (e.g. legacy side-icon layouts). For new statement beats, put media in the card — not the side panel.

## JSON

```json
{
  "label": "The news is scary",
  "type": "statement",
  "layout": "statement_full_card",
  "hold": 1.2,
  "statement": {
    "mode": "text_image",
    "text_lines": [
      "More than 80,000 layoffs in 2026",
      "Over one lakh in 2025"
    ],
    "image": {
      "ref": "media/layoffs-chart.png",
      "kind": "project"
    },
    "video": {
      "ref": "media/news-montage.mp4",
      "kind": "project",
      "loop": true,
      "muted": true
    }
  }
}
```

## Beat script

```
TYPE:       statement
LAYOUT:     statement_full_card

─── CONTENT ───
LABEL:
The news is scary

TEXT (card, black):
  More than 80,000 layoffs in 2026
  Over one lakh in 2025

─── STATEMENT ───
MODE: text_image
IMAGE: media/layoffs-chart.png
VIDEO: media/news-montage.mp4

HOLD: 1.2
```

## Media uploads

| Endpoint | Purpose |
|----------|---------|
| `POST /api/projects/{id}/media/upload` | PNG, JPG, WEBP, GIF, SVG, MP4, WEBM, MOV (max 25 MB) |
| `GET /api/projects/{id}/media/{filename}` | Preview / render serve |

Files are stored under `projects/{id}/media/` and referenced as `media/filename.ext`.

## Render behaviour

1. Yellow label types with cursor
2. White card grows (`GrowFromCenter`)
3. Card lines type one by one (if text mode)
4. Image / video fade in (if present)
5. Hold, then fade to next beat

Videos loop silently inside the card during the hold.

## Legacy statement (icon + half card)

Older projects may still use `card_right_icon_left` with a side icon. Those beats use the **Icon** tab and `run_panel_beat`. New statement beats should use `statement_full_card`.

## Related

- [Beat types](beat-types)
- [Cards & emphasis](cards-emphasis)
- [Studio UI](studio-ui)
