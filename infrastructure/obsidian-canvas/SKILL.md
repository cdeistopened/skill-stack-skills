---
name: obsidian-canvas
description: >-
  Reference for creating Obsidian .canvas files — the visual workspace format for spatial layouts,
  relationship maps, content planning boards, and architecture diagrams. Use when building
  any visual or spatial document in Obsidian.
---

# Obsidian Canvas

Reference for creating `.canvas` files — Obsidian's visual workspace format. Use for spatial layouts, relationship maps, content planning boards, and visual architecture diagrams.

---

## File Format

A `.canvas` file is JSON with two arrays: `nodes` and `edges`.

```json
{
  "nodes": [],
  "edges": []
}
```

---

## Node Types

### Text Node
Inline markdown content rendered on the canvas.

```json
{
  "id": "a1b2c3d4e5f6g7h8",
  "type": "text",
  "x": 0,
  "y": 0,
  "width": 400,
  "height": 200,
  "text": "# Heading\n\nMarkdown content here.\n\n- Bullet points\n- **Bold text**",
  "color": "1"
}
```

### File Node
Embeds a vault file on the canvas.

```json
{
  "id": "b2c3d4e5f6g7h8i9",
  "type": "file",
  "x": 500,
  "y": 0,
  "width": 400,
  "height": 400,
  "file": "OpenEd Vault/tasks/some-task.md",
  "subpath": "#Context"
}
```

- `file` — path relative to vault root
- `subpath` — optional heading or block to embed (e.g., `#Heading` or `#^block-id`)

### Link Node
Embeds a web page.

```json
{
  "id": "c3d4e5f6g7h8i9j0",
  "type": "link",
  "x": 1000,
  "y": 0,
  "width": 400,
  "height": 300,
  "url": "https://example.com"
}
```

### Group Node
Visual container that groups other nodes.

```json
{
  "id": "d4e5f6g7h8i9j0k1",
  "type": "group",
  "x": -50,
  "y": -50,
  "width": 950,
  "height": 500,
  "label": "Phase 1: Research",
  "color": "2",
  "background": "path/to/image.png",
  "backgroundStyle": "cover"
}
```

- `backgroundStyle` — `cover`, `ratio`, or `repeat`

---

## Edges (Connections)

```json
{
  "id": "e5f6g7h8i9j0k1l2",
  "fromNode": "a1b2c3d4e5f6g7h8",
  "toNode": "b2c3d4e5f6g7h8i9",
  "fromSide": "right",
  "toSide": "left",
  "fromEnd": "none",
  "toEnd": "arrow",
  "color": "3",
  "label": "feeds into"
}
```

- `fromSide` / `toSide` — `top`, `right`, `bottom`, `left`
- `fromEnd` / `toEnd` — `none` or `arrow`
- `label` — text displayed on the edge (optional)

---

## IDs

All IDs are 16-character hex strings. Generate with:
```javascript
// In a script
crypto.randomUUID().replace(/-/g, '').slice(0, 16)
```

Or for Claude: generate 16 random hex chars (0-9, a-f).

---

## Colors

Both nodes and edges accept a `color` property:

| Value | Color |
|-------|-------|
| `"0"` | Default (no color) |
| `"1"` | Red |
| `"2"` | Orange |
| `"3"` | Yellow |
| `"4"` | Green |
| `"5"` | Cyan |
| `"6"` | Purple |

Custom hex colors also work: `"#FF5733"`

---

## Positioning

- `x`, `y` — top-left corner of the node (can be negative)
- `width`, `height` — size in pixels
- Canvas is infinite in all directions
- Obsidian's default grid snaps to ~20px intervals
- Convention: arrange left-to-right or top-to-bottom for flow

**Layout tips:**
- Standard node: 400w × 200-300h
- Small card: 250w × 150h
- Wide overview: 600w × 400h
- Vertical spacing: 50-100px between nodes
- Horizontal spacing: 100-150px between columns

---

## Complete Example: Content Pipeline Canvas

```json
{
  "nodes": [
    {
      "id": "a1b2c3d4e5f6g7h8",
      "type": "text",
      "x": 0,
      "y": 0,
      "width": 300,
      "height": 150,
      "text": "# Source Content\n\nPodcast episodes, interviews, research",
      "color": "1"
    },
    {
      "id": "b2c3d4e5f6g7h8i9",
      "type": "text",
      "x": 450,
      "y": -100,
      "width": 300,
      "height": 120,
      "text": "## Newsletter\nDaily (Mon-Thu) + Weekly (Fri)",
      "color": "4"
    },
    {
      "id": "c3d4e5f6g7h8i9j0",
      "type": "text",
      "x": 450,
      "y": 50,
      "width": 300,
      "height": 120,
      "text": "## Social Posts\nLinkedIn, X, Instagram",
      "color": "5"
    },
    {
      "id": "d4e5f6g7h8i9j0k1",
      "type": "text",
      "x": 450,
      "y": 200,
      "width": 300,
      "height": 120,
      "text": "## Blog / SEO\nLong-form articles",
      "color": "6"
    },
    {
      "id": "e5f6g7h8i9j0k1l2",
      "type": "group",
      "x": -50,
      "y": -150,
      "width": 850,
      "height": 520,
      "label": "Hub-and-Spoke Pipeline"
    }
  ],
  "edges": [
    {
      "id": "f6g7h8i9j0k1l2m3",
      "fromNode": "a1b2c3d4e5f6g7h8",
      "toNode": "b2c3d4e5f6g7h8i9",
      "fromSide": "right",
      "toSide": "left",
      "toEnd": "arrow"
    },
    {
      "id": "g7h8i9j0k1l2m3n4",
      "fromNode": "a1b2c3d4e5f6g7h8",
      "toNode": "c3d4e5f6g7h8i9j0",
      "fromSide": "right",
      "toSide": "left",
      "toEnd": "arrow"
    },
    {
      "id": "h8i9j0k1l2m3n4o5",
      "fromNode": "a1b2c3d4e5f6g7h8",
      "toNode": "d4e5f6g7h8i9j0k1",
      "fromSide": "right",
      "toSide": "left",
      "toEnd": "arrow"
    }
  ]
}
```

---

## Tips for This Vault

1. **Use file nodes** to embed task files, project docs, or MOC notes directly on canvases
2. **Groups** for project phases, content pipelines, or team areas
3. **Color-code by area**: Red = urgent, Green = OpenEd, Purple = CIA, Cyan = Personal
4. **Edges with labels** document relationships ("blocks", "feeds into", "depends on")
5. **Canvas files can live anywhere** — consider `views/` folder alongside `.base` files
