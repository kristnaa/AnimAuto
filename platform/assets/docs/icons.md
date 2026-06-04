# Icons

How to specify icons in beat scripts, the Beats editor, and JSON.

## ICONS section (beat script)

Each line:

```
icon_id: description or fa6-brands:ref | color: WHITE | scale: 1.2 | trigger: word
```

| Part | Meaning |
|------|---------|
| **icon_id** | Local name (`icon_python`, `shape_question`) |
| **description** | Plain English — GPT searches Iconify |
| **color** | `WHITE`, `#3776AB`, hex, or **`ORIGINAL`** for full-color brand/emoji icons |
| **scale** | Optional (default 1.2) |
| **trigger** | Optional — word in TEXT that reveals this icon |

## Slot order

| Icons listed | Behavior |
|--------------|----------|
| 1 | Single icon — fills icon panel |
| 2 (joke) | 1st = primary, 2nd = swap at punchline |
| 2–4 (multi) | Grid in icon panel; optional word-sync |

## Examples

Describe + color (GPT picks Iconify):

```
icon_python: Python programming language logo | color: #3776AB
icon_scream: screaming panicked emoji face | color: WHITE
shape_question: large question mark help circle | color: WHITE | scale: 1.8
```

Explicit Iconify refs:

```
icon_python: fa6-brands:python | color: #3776AB
icon_mobile: fe:mobile | color: WHITE | trigger: mobile
```

Icons download from Iconify at render time. Cached under `assets/icons/cache/`.

## Color: mono vs full-color

| Icon type | Examples | Color in editor / script |
|-----------|----------|---------------------------|
| **Mono stroke** | Lucide, MDI outline | `WHITE`, hex, or named colors — tints the outline |
| **Brand / emoji** | `devicon:python`, `fa6-brands:*`, Twemoji | **`ORIGINAL`** — keeps logo colors |

Many brand SVGs (e.g. `devicon:python`) use **SVG gradients**. Manim cannot render gradients directly, so the renderer **flattens** them to solid fills before load (cached as `*.flat.svg` next to the source). Use **ORIGINAL** in the Icon tab or `"color": "ORIGINAL"` in JSON — do not expect a white tint on colorful logos.

```json
"visuals": {
  "primary": {
    "concept": "python",
    "color": "ORIGINAL",
    "ref": "devicon:python",
    "kind": "iconify"
  }
}
```

For a single-color Python outline, pick a Lucide/mono icon instead of a brand set.

## Uploaded icons (SVG / PNG)

In the **Icon** tab, use the upload button in the search row:

| Format | Stored as | Render path |
|--------|-----------|-------------|
| **PNG / JPG** | `projects/{id}/icons/…` | `ImageMobject` |
| **SVG** | same folder | `SVGMobject` (gradients flattened when needed) |

Uploaded files are **project-scoped** (`kind: "project"`, ref like `icons/my-logo.png`). PNG uploads work in single-icon beats and in **multi-icon grids** (the grid uses Manim `Group` when rasters are present).

**Tip:** PNG is safest for photos and complex artwork; SVG is best for simple vector logos.

## Beats editor — Icon tab

1. Select a beat in the timeline
2. Open the **Icon** tab (full-height picker)
3. Search catalog concepts or Iconify (`python`, `terminal`, …)
4. **Upload** PNG/JPG/SVG for a project-only icon (stored under the project `icons/` folder)
5. Click the **color swatch** for full hex picker (saturation, hue, RGB)
   - Lucide/mono icons: white outline + your tint
   - Colorful icons (emoji, brands): use **ORIGINAL** — keeps logo colors (gradients auto-flattened at render)

## Visual catalog

- File: `assets/visual_catalog.json`
- API: `GET /api/visual-catalog`
- Search: `GET /api/icons/search?q=python`

## Validation

`validate-beats` warns if icons fail to resolve before render. Fix in Beats tab or paste explicit refs.

## Related

- [Icon grid](icon-grid)
- [Icon reveal](icon-reveal)
- [Icon entrances](icon-entrances)
- [Studio UI](studio-ui)
