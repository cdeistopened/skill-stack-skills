---
name: cover-creator
description: Generate print-ready KDP book covers from public domain art. Full pipeline: dimension calculation, museum art sourcing, gradient overlay design, typographic hierarchy, back cover layout with real praise quotes, iterative refinement, and Kindle cover export. Use when publishing any book through KDP — handles the complete cover creation workflow from art selection through print-ready PDF. Also use when the user mentions book covers, KDP covers, cover design, or needs to format cover art for Amazon publishing.
---

# Cover Creator

Generate print-ready KDP paperback covers programmatically. Input: cover art image + book metadata. Output: 300 DPI PDF wrap cover (front + spine + back) ready for KDP upload, plus a Kindle ebook cover.

The skill is the full workflow, not just the script. Art sourcing, design decisions, back cover content research, iterative refinement, and Kindle export are all part of the job.

## When to Use

- Publishing any book through Amazon KDP
- User mentions book covers, KDP covers, cover design
- Need to format cover art for Amazon publishing
- Building a series with consistent visual branding
- Turning public domain art into professional book covers

## What It Produces

1. **Print-ready PDF** at 300 DPI — full wrap (front + spine + back) with correct KDP dimensions
2. **PNG preview** for quick review
3. **Kindle ebook cover** — 1600x2560px, cropped from the print front cover
4. Front cover: title with typographic hierarchy, author name, over gradient-overlaid artwork
5. Spine: title + author (auto-scaled to fit spine width)
6. Back cover: description, praise quotes, categories, barcode zone

## Requirements

- Python 3 with Pillow (`pip3 install Pillow`)
- macOS system fonts: Bodoni 72 (regular, bold, smallcaps), Baskerville (regular, semibold, bold, italic) — all in `/System/Library/Fonts/Supplemental/`
- Cover art image at minimum 300 DPI at cover dimensions

---

## The Pipeline

```
Step 1: Calculate dimensions (word count → page count → spine width → canvas size)
Step 2: Source cover art (museum databases, public domain verification)
Step 3: Make design decisions (gravity, overlay, typography, colors)
Step 4: Write back cover content (description + real praise quotes)
Step 5: Generate and iterate (run script, study output, adjust, repeat 3-5x)
Step 6: Export Kindle cover (crop front cover to 1600x2560)
```

---

## Step 1: Calculate Dimensions

### Inputs

- **Word count** of the manuscript
- **Trim size**: 5x8, 5.5x8.5, or 6x9 (most common)
- **Paper color**: cream or white

### Word Count to Page Count

| Trim Size | Words Per Page | Formula |
|-----------|---------------|---------|
| 5 x 8 | 250 | `ceil(word_count / 250)`, round up to even |
| 5.5 x 8.5 | 260 | `ceil(word_count / 260)`, round up to even |
| 6 x 9 | 280 | `ceil(word_count / 280)`, round up to even |

Always round up to even — KDP requires even page counts.

### Spine Width

```
white paper:          page_count × 0.002252 inches/page
cream paper:          page_count × 0.0025   inches/page
standard color paper: page_count × 0.0032   inches/page
premium color paper:  page_count × 0.002252 inches/page
```

Full dimension reference with all 14 KDP trim sizes: `reference/kdp-dimensions.md`

Spine text only allowed if page count > 79.

### Full Cover Canvas

```
canvas_width  = 0.125" bleed + back_trim_w + spine_width + front_trim_w + 0.125" bleed
canvas_height = 0.125" bleed + trim_h + 0.125" bleed
```

### Safety Zones

- **Trim safety**: 0.25" from trim edges on all sides — keep ALL text inside this
- **Spine safety**: 0.0625" on each side of spine (Amazon requirement)

### Key Insight: Free Kindle Cover

5x8 trim ratio = 1:1.6 = exact Kindle cover ratio (1600x2560px). The print front cover crops almost perfectly to a Kindle ebook cover. Minor upscale from 1537x2475 to 1600x2560.

### Minimum Art Resolution by Trim Size

| Trim Size | Front Cover at 300 DPI | Minimum Source |
|-----------|----------------------|----------------|
| 5 x 8 | 1537 x 2475 | ~1600 x 2500 |
| 5.5 x 8.5 | 1687 x 2625 | ~1700 x 2650 |
| 6 x 9 | 1837 x 2775 | ~1850 x 2800 |

If the source image is smaller, it will look soft. Find a higher-res version or choose different art.

---

## Step 2: Source Cover Art

### Best Sources for Public Domain Art (Ranked by Reliability)

1. **Metropolitan Museum** (metmuseum.org) — CC0, excellent quality, API for downloads
   - URL pattern: `https://images.metmuseum.org/CRDImages/ep/original/FILENAME.jpg`
   - Use Wikimedia API to find exact filenames: `https://commons.wikimedia.org/w/api.php?action=query&titles=File:FILENAME&prop=imageinfo&iiprop=url&format=json`
2. **National Gallery of Art** (nga.gov) — Open Access
3. **Yale Center for British Art** — IIIF, thousands of Turner works
4. **Wikimedia Commons** — check license tags (PD-old, PD-Art, CC0)
5. **Google Art Project** versions on Wikimedia often have highest resolution (6000+ px)
6. **Rijksmuseum** (rijksmuseum.nl) — CC0, Dutch masters
7. **Art Institute of Chicago** (artic.edu) — CC0

### Public Domain Rules

| Condition | Status |
|-----------|--------|
| Artist died 70+ years ago | Public domain |
| Published before 1928 (US) | Public domain |
| Photo of 2D artwork (Bridgeman v. Corel) | No new copyright created |
| Museum photos from Met, Yale, NGA | Explicitly open access |

### Search Strategy

1. Extract 3-5 themes from the book
2. Match art era to text era when possible
3. **Portraits crop better than landscapes** for book covers
4. For landscape paintings: look for strong vertical energy (sky, clouds, architecture) that survives portrait cropping
5. Cross-reference Wikimedia for specific artists when museum search is limited
6. **Always crop the frame off museum photos** before using as cover art

### Rights Checklist

Before using any image:
- [ ] Artist died 70+ years ago (or work published pre-1928 US)
- [ ] Not a modern photograph of a 3D sculpture
- [ ] High-res available (minimum 300 DPI at cover dimensions)
- [ ] No modern watermarks or overlays
- [ ] If Wikimedia: license tag says PD-old, PD-Art, or CC0

---

## Step 3: Design Decisions

### Art Placement: The `art_gravity` Parameter

Controls which part of a landscape image to keep when cropping to portrait orientation.

- `0.0` = keep top (sky, clouds, architecture)
- `0.5` = center (split evenly)
- `1.0` = keep bottom (foreground, ground, water)

For paintings with dramatic skies, use **0.15-0.25**. For paintings with interesting foreground detail, use **0.6-0.8**.

### Overlay Strategy — The #1 Thing That Separates Good From Bad

**NEVER use a flat dark overlay.** It kills the painting's tonal range and makes the cover look like a dark rectangle with text.

**USE gradient overlays**: dark at top (for title readability), dark at bottom (for author name), clear in the middle (let the painting breathe).

| Parameter | Range | What It Controls |
|-----------|-------|-----------------|
| `overlay_top_alpha` | 90-120 | Darkness at top edge. Just enough to read white text on clouds. |
| `overlay_bottom_alpha` | 140-170 | Darkness at bottom edge. Darker — author name needs contrast against foreground. |
| `overlay_mid_clear` | 0.35-0.50 | Vertical position where overlay is most transparent. |

**The mid-clear zone should align with the painting's most interesting detail.** If the painting has a gorgeous sunset at 40% from top, set `overlay_mid_clear` to 0.40.

The script uses ease-in/ease-out curves for smooth transitions — the gradient is not linear.

### Title Typography: Per-Line Scaling

Multi-line titles with per-line scaling create typographic hierarchy. This is what makes a cover look designed rather than typed.

| Parameter | What It Does | Example |
|-----------|-------------|---------|
| `title_line_scale` | Scale factor per line (1.0 = base size) | `[0.55, 1.0, 0.45, 1.3]` |
| `title_leading` | Spacing between title lines | 1.2-1.4 |
| `title_size` | Base font size in points at 300 DPI | 100-150 |

**The anchor word** — usually the distinctive noun — should be the biggest. Articles and prepositions should be smallest.

Example for "THE CRUISE OF THE NONA":
```
title: "THE CRUISE\nOF THE NONA"
title_line_scale: [0.55, 1.0, 0.45, 1.3]
```
Result: "THE CRUISE" is medium, "OF THE" is small, "NONA" is largest.

### Text Alignment

- **Center-alignment**: safer, works for most compositions
- **Right-alignment**: works when the art has visual weight on the left
- **Left-alignment**: unusual for covers, rarely the right call

### Font Pairing

| Element | Font | Notes |
|---------|------|-------|
| Title | Bodoni Bold (`bodoni-bold`) | Classic, high contrast serif |
| Author | Bodoni Small Caps (`bodoni-sc`) | Matches title family |
| Back cover body | Baskerville (`baskerville`) | Readable, warm |
| Back cover quotes | Baskerville Bold (`baskerville-bold`) | Stands out from body |
| Spine title | Baskerville SemiBold (`baskerville-semibold`) | |
| Spine author | Baskerville (`baskerville`) | |

**Max 2 font families total.** Bodoni for front cover display, Baskerville for everything else.

### Color Palette (Dark/Classical Covers)

These are the proven defaults. Adjust only with reason.

| Element | RGB | Description |
|---------|-----|-------------|
| Title | `(255, 252, 240)` | Warm cream, not pure white |
| Author | `(255, 252, 240)` | Same warm cream |
| Spine title | `(220, 200, 160)` | Muted gold |
| Spine author | `(240, 230, 215)` | Light cream |
| Background | `(25, 22, 20)` | Near-black brown, not pure black |
| Spine | `(20, 18, 16)` | Slightly darker than background |
| Back cover body | `(230, 220, 205)` | Cream |
| Back cover quotes | `(220, 200, 160)` | Light gold |
| Praise header | `(210, 190, 145)` | Muted gold |
| Separator line | `(210, 190, 145)` | Muted gold |
| Categories | `(150, 145, 135)` | Light gray |

---

## Step 4: Back Cover Content

### Structure (Top to Bottom)

1. **Opening description** — 1-2 paragraphs, what the book is
2. **Highlights/themes paragraph** — what the reader gets
3. **"New edition" note** — for public domain reprints
4. **Separator line** — thin gold rule, inset from margins
5. **"PRAISE FOR [TITLE]" header** — regular weight, centered
6. **2-3 attributed quotes** — bold, larger than body, research real ones
7. **Categories** — bottom left (e.g., "Sailing / Travel Writing / Essays")
8. **Barcode zone** — bottom right, white 2"x1.2" rectangle

### Researching Real Praise Quotes

For public domain books: find actual praise. Do not fabricate quotes.

**Where to look:**
- Goodreads reviews (sort by most popular)
- Publisher pages (Loreto, Ignatius, TAN, Os Justi Press for Catholic books)
- Introductions and forewords to modern editions
- Contemporary reviews from the original publication era
- Literary journals and Catholic publications
- Other authors who referenced the work

**Format:**
```python
quotes: [
    ("\u201cThe quote text here.\u201d", "\u2014 Attribution Name"),
    ("\u201cAnother quote.\u201d", "\u2014 Source, Publication"),
]
```

Use curly quotes (unicode `\u201c` and `\u201d`) and em dash (`\u2014`) for attribution.

### Back Cover Text Sizing (at 300 DPI)

| Element | Config Key | Default | Range |
|---------|-----------|---------|-------|
| Body text | `back_body_size` | 38 | 36-46 |
| Key question | `back_question_size` | 40 | 38-48 |
| Quotes | `back_quote_size` | 40 | 38-48 |
| Attribution | `back_attrib_size` | 30 | 28-36 |
| Praise header | `praise_header_size` | 26 | 24-32 |
| Categories | `category_size` | 26 | 24-32 |

### Mirror Art Effect

The script can paste a faint, horizontally flipped version of the front art onto the back cover. Creates subtle visual continuity.

| Parameter | Default | What It Does |
|-----------|---------|-------------|
| `mirror_art_on_back` | `True` | Enable/disable mirrored art on back |
| `mirror_art_alpha` | `35` | Opacity (0-255). 25-45 range. Higher = more visible art, harder to read text. |

---

## Step 5: Generate and Iterate

### Running the Script

```bash
# Option 1: Edit CONFIG dict in the script, then run
python3 scripts/generate_cover.py

# Option 2: Pass a JSON config file
python3 scripts/generate_cover.py config.json

# Option 3: Override just the art path
python3 scripts/generate_cover.py --art /path/to/painting.jpg
python3 scripts/generate_cover.py /path/to/painting.jpg
```

Output: `cover.png` + `cover.pdf` in the script's directory (or `output_dir` if set).

### The Iteration Loop

This is where covers get good. Plan for 3-5 rounds minimum.

1. **Generate** — run the script
2. **Open PNG** — study at full resolution AND at thumbnail size
3. **Check these things:**
   - Title readability at thumbnail (shrink browser to ~120px wide)
   - Overlay transparency — is the painting breathing in the middle?
   - Spacing balance — title not too close to top, author not too close to bottom
   - Spine text legible (script auto-scales, but verify)
   - Back cover text not cramped or floating
   - Barcode zone clear of text
4. **Adjust config values** — see common fixes below
5. **Regenerate** — script runs in ~2 seconds

### Common Fixes

| Problem | Fix |
|---------|-----|
| Title hard to read | Increase `overlay_top_alpha` (try 110-130) |
| Title too small at thumbnail | Increase `title_size` (try 140-160) |
| Painting looks dead/dark | Reduce `overlay_top_alpha` and `overlay_bottom_alpha` by 20-30 |
| Dead space above title | Decrease `title_zone_top` (try 0.04-0.06) |
| Dead space below author | Decrease `author_zone_bottom` (try 0.04-0.06) |
| Overlay hides best part of painting | Move `overlay_mid_clear` to align with that detail |
| Author name lost in foreground | Increase `overlay_bottom_alpha` (try 160-180) |
| Spine text invisible | Script auto-scales, but check `spine_title` and `spine_author` strings are set |
| Back cover text cramped | Reduce `back_body_size` by 2-4pt, or cut a paragraph |
| Back cover text floating | Increase sizes, or add another praise quote |
| Art crops badly | Adjust `art_gravity` (lower = more sky, higher = more ground) |

---

## Step 6: Export Kindle Cover

Crop the front cover area from the full wrap to **1600x2560px** for Kindle.

For 5x8 trim, the front cover is 1537x2475px — nearly exact Kindle ratio. Slight upscale needed.

```python
# Crop front cover from wrap
from PIL import Image
wrap = Image.open("cover.png")
# Front cover starts at: BLEED + BACK_TRIM_W + SPINE_W
# Calculate these from the config
front_left = bleed_px + trim_w_px + spine_px
front_right = front_left + trim_w_px + bleed_px  # include right bleed
kindle = wrap.crop((front_left, 0, front_right, wrap.height))
kindle = kindle.resize((1600, 2560), Image.LANCZOS)
kindle.save("kindle-cover.jpg", quality=95)
```

---

## Full Config Reference

Every parameter the script accepts, with defaults and valid ranges.

### Book Metadata

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `title` | string | — | Front cover title. Use `\n` for line breaks. |
| `subtitle` | string | `""` | Optional subtitle below title. |
| `author_line_1` | string | — | Primary author line (usually full name). |
| `author_line_2` | string | `""` | Optional second author line (e.g., "With an Introduction by..."). |
| `spine_title` | string | — | Title for spine (often abbreviated). |
| `spine_author` | string | — | Author surname for spine. |

### Dimensions

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `trim_w` | float | — | Trim width in inches (5, 5.5, or 6). |
| `trim_h` | float | — | Trim height in inches (8, 8.5, or 9). |
| `page_count` | int | — | Total page count (must be even). |
| `paper` | string | `"cream"` | `"cream"` (0.0025"/page) or `"white"` (0.002252"/page). |

### Cover Art

| Key | Type | Default | Range | Description |
|-----|------|---------|-------|-------------|
| `art_path` | string | — | — | Path to cover art image file. |
| `art_gravity` | float | `0.3` | 0.0-1.0 | Crop anchor. 0.0=top (sky), 1.0=bottom (ground). |
| `overlay_top_alpha` | int | `160` | 0-255 | Darkness at top edge of gradient overlay. |
| `overlay_bottom_alpha` | int | `120` | 0-255 | Darkness at bottom edge of gradient overlay. |
| `overlay_mid_clear` | float | `0.45` | 0.0-1.0 | Vertical position where overlay is most transparent. |
| `mirror_art_on_back` | bool | `True` | — | Paste faint mirrored art on back cover. |
| `mirror_art_alpha` | int | `35` | 0-255 | Opacity of mirrored back art. 25-45 typical. |

### Front Cover Layout

| Key | Type | Default | Range | Description |
|-----|------|---------|-------|-------------|
| `front_align` | string | `"center"` | `"left"`, `"center"`, `"right"` | Text alignment on front cover. |
| `title_zone_top` | float | `0.08` | 0.0-0.3 | Fraction of safe area from top where title starts. |
| `author_zone_bottom` | float | `0.08` | 0.0-0.3 | Fraction of safe area from bottom where author sits. |
| `title_line_scale` | list[float] | `[1.0]` per line | — | Scale factor per title line. See typography section. |
| `title_leading` | float | `1.35` | 1.1-1.6 | Line spacing multiplier between title lines. |

### Font Sizes (at 300 DPI)

| Key | Default | Range | Element |
|-----|---------|-------|---------|
| `title_size` | `130` | 90-180 | Front cover title (base size before line scaling). |
| `subtitle_size` | `50` | 30-70 | Subtitle. |
| `author_size_1` | `60` | 40-80 | Primary author name. |
| `author_size_2` | `40` | 28-60 | Secondary author line. |
| `back_body_size` | `38` | 32-48 | Back cover description paragraphs. |
| `back_question_size` | `40` | 34-50 | Back cover key question. |
| `back_quote_size` | `40` | 34-50 | Praise quotes. |
| `back_attrib_size` | `30` | 24-38 | Quote attributions. |
| `praise_header_size` | `26` | 22-34 | "PRAISE FOR..." header. |
| `category_size` | `26` | 22-34 | Category line at bottom. |

### Font Families

| Key | Default | Options |
|-----|---------|---------|
| `title_font` | `"bodoni-bold"` | `bodoni`, `bodoni-bold`, `bodoni-italic`, `bodoni-sc`, `baskerville`, `baskerville-semibold`, `baskerville-italic`, `baskerville-bold` |
| `subtitle_font` | `"baskerville-italic"` | Same as above. |
| `author_font` | `"bodoni-sc"` | Same as above. |

### Colors (RGB Tuples)

| Key | Default | Description |
|-----|---------|-------------|
| `bg_color` | `(25, 22, 20)` | Canvas background (near-black brown). |
| `spine_color` | `(20, 18, 16)` | Spine strip color. |
| `title_color` | `(255, 250, 235)` | Front cover title. |
| `subtitle_color` | `(240, 230, 210)` | Front cover subtitle. |
| `author_color` | `(255, 250, 235)` | Front cover author name. |
| `spine_title_color` | `(220, 200, 160)` | Spine title text (muted gold). |
| `spine_author_color` | `(240, 230, 215)` | Spine author text. |
| `back_body_color` | `(230, 220, 205)` | Back cover body text (cream). |
| `back_question_color` | `(210, 190, 145)` | Back cover key question (gold). |
| `back_quote_color` | `(220, 200, 160)` | Praise quote text (light gold). |
| `back_attrib_color` | `(230, 220, 205)` | Quote attribution text. |
| `praise_header_color` | `(210, 190, 145)` | "PRAISE FOR..." header (gold). |
| `separator_color` | `(210, 190, 145)` | Separator rule (gold). |
| `category_color` | `(150, 145, 135)` | Category line (light gray). |

### Back Cover Content

| Key | Type | Description |
|-----|------|-------------|
| `back_paragraphs` | list[str] | Opening description paragraphs. |
| `back_question` | string | Optional bold centered question (empty to skip). |
| `back_body` | list[str] | Body paragraphs after the question. |
| `praise_header` | string | e.g., `"PRAISE FOR THE CRUISE OF THE NONA"` (empty to skip). |
| `quotes` | list[tuple] | `[("Quote text", "— Attribution"), ...]` |
| `categories` | string | e.g., `"Sailing / Travel Writing / Essays"` |

### Output

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `output_dir` | string | `""` | Output directory. Empty = same as script. |
| `output_name` | string | `"cover"` | Base filename (produces `{name}.png` + `{name}.pdf`). |

---

## Spine Rules

- **Under 80 pages**: No spine text. Script skips spine text automatically.
- **80-130 pages**: Title only, auto-scaled small.
- **130+ pages**: Title + author name.
- **US convention**: Text reads top-to-bottom (script rotates -90 degrees).
- **Spine safety**: 0.0625" padding on each side. The script enforces this.
- **Spine color**: Match the painting's dominant dark tone. Never use light colors — spine shows shelf wear.

---

## Series Branding

When publishing multiple books in a series:

- Same script/config template for all covers
- Shared color palette (same RGB values)
- Consistent layout (title position, font, alignment)
- Same spine treatment
- Vary only: artwork, title text, subtitle, accent color

The reader should recognize the series from across the room.

---

## Common Mistakes

1. **Flat overlay instead of gradient** — the single most common mistake. Kills the painting. Always use gradient.
2. **Pure white text on pure black background** — looks harsh. Use warm cream on near-black brown.
3. **Fabricated praise quotes** — for public domain books, real quotes exist. Research them.
4. **Ignoring thumbnail readability** — the cover must work at 120px wide on Amazon search results.
5. **Too many font families** — max 2. Bodoni + Baskerville is the proven pairing.
6. **Skipping iteration** — first generation is never the final. Budget 3-5 rounds minimum.
7. **Not cropping museum frames** — museum photos often include gilt frames. Crop to the painting.
8. **Wrong genre signal** — the art should match the book's era and subject matter.

---

## Integration

- **Input from**: `niche-scout` (category data), `listing-optimizer` (title/subtitle), Vellum or word processor (page count)
- **Output to**: KDP upload (PDF for print cover), Kindle upload (JPG for ebook cover)
- **Art sourcing reference**: `reference/art-sources.md` for museum collections + artist guide
- **Template verification**: Download KDP template from kdp.amazon.com/cover-calculator, overlay on PDF to confirm alignment

## Files

```
cover-creator/
├── SKILL.md                    ← This file
├── scripts/
│   └── generate_cover.py       ← Cover generation script (Pillow)
└── reference/
    ├── art-sources.md          ← Museum collections + artist guide
    └── kdp-dimensions.md       ← Complete KDP dimension formulas, all trim sizes, paper multipliers
```
