# Blackboard mind map (reference: blackboard-why-python.png)

**Topic example:** “Why Python?” — radial hub with branches on a **black chalkboard**.

## Blackboard aesthetic (mandatory)

- Background: **black**
- Chalk labels: **white**
- Branch arrows: **curved yellow** (not only straight)
- Keyword highlights: **blue** wash behind one word (e.g. “Demand” in “High in Demand”)
- Hub corner tag: **red** badge (“WHY”)
- Colorful **icons** beside each branch (from icon catalog)

## Use when

- **Why / reasons / benefits** overview → `mind_map_radial` with `mode: full` (up to 5 branches)
- Single topic sentence (“great for AI”, “huge community”) → `mode: single` (hub + one branch + icon)

## Composition

- **Central hub box** with topic name (e.g. “Python”) + optional tag
- **Curved arrows** radiating to branch nodes
- Each branch = **icon + 2–3 word label** + optional highlight
- Sub-branches (Automation, Web, Gaming, Data) as small labeled dots when relevant

## Icon mapping

| Topic | icon_id |
|-------|---------|
| Demand / growth | `bar_chart_up` |
| Power / simple | `rocket` or `code_simple` |
| Versatility | `swiss_knife` |
| Automation | `robot_arm` |
| Web | `globe` |
| Gaming | `gamepad` |
| Data science | `chart_lines` |
| Community | `crowd` |
| AI | `brain_gear` |

## Text rules

- Branch labels ≤3 words: “High Demand”, “Huge Community”, “AI”
- **Never** paste full narration
- Sub-labels ≤2 words each

## Layout + background

- Layout: `mind_map_radial`
- Background: `blackboard_clean`

## Do not

- White background
- Python snake logo — use text “Python” in hub only
- Paragraph text under icons
