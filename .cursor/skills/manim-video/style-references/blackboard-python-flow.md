# Blackboard explainer flow (reference: blackboard-python-flow.png)

**Topic example:** “How Python Works?” — left-to-right pipeline on a **black chalkboard** (not white).

## Blackboard aesthetic (mandatory)

- Scene background: **pure black** (`#000000`)
- Chalk text: **white**
- Arrows: **yellow**, preferably **dashed** between pipeline stages
- Highlights: semi-transparent **blue** pills behind one keyword
- Accent tags: **red** corner badges (e.g. “WHY”, “NEW”)
- **No white-filled boxes** — use dark fills with white chalk outlines only

## Use when

- Explaining **how something works**, toolchain, interpreter, pipeline
- Tutorial voice-over with **icons + short labels**

## Composition

- **Linear left → right** — use layout `pipeline_blackboard`
- Three stages typical: **Source → Process (nested) → Output**
- Middle stage wrapped in outer **chalk box** with nested sub-steps
- **Dashed yellow arrows** between stages
- Icons from catalog: `document_py`, `gear_process`, `cube_vm`, `pac_output`, `binary_strip`

## Text rules

- Labels only: “Source Code”, “Compiler”, “Output” (≤3 words)
- **No narration sentences** on screen
- Optional blue highlight on one word per label

## Layout + background

- Layout: `pipeline_blackboard`
- Background: `blackboard_clean`

## Do not

- White background or whiteboard look
- Brand logos (Python, VS Code) — use `document_py` generic icon
- Full transcript text
