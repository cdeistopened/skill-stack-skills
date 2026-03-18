---
name: cover-brief
description: Generate a cover design brief with art research, genre signals, palette, typography, and trim/spine specs. Use when preparing a book for KDP and need cover direction — whether for a designer, Canva, or AI image generation.
---

# Cover Brief Generator

Generate a complete cover design brief from manuscript + niche data. Includes public domain art research, genre-appropriate palette, typography, trim/spine calculations, and comp cover analysis.

## When to Use

- Starting a new book and need cover direction
- Briefing a designer (Fiverr, Miblart, Reedsy, 99designs)
- Self-designing in Canva/BookBrush and need specs
- Researching public domain art for a reprint/compilation

## What It Produces

1. **Trim & Spine Specs** — dimensions, spine width from page count, bleed, template download link
2. **Genre Signal Analysis** — what covers in your category look like and what readers expect
3. **Art Research** — 10-15 public domain paintings/images with source links, rights status, crop notes
4. **Palette & Typography** — color scheme, font recommendations, hierarchy
5. **Comp Cover Gallery** — 5-8 successful covers in your category to study
6. **Design Brief Document** — ready to hand to a designer or use as self-design guide
7. **Thumbnail Test Criteria** — will it read at 120x180 pixels?

---

## Step 1: Trim & Spine Specs

### Standard KDP Trim Sizes

| Name | Size | Best For |
|------|------|----------|
| Mass market | 4.25" x 6.875" | Fiction, devotionals |
| **Pocket** | **5" x 8"** | Short nonfiction, spiritual reading, reprints |
| Trade | 5.5" x 8.5" | Most nonfiction |
| US Trade | 6" x 9" | Business, self-help, longer works |
| Large | 7" x 10" | Textbooks, workbooks |

### Spine Width Calculation

```
Spine width = page count x paper multiplier

Paper multipliers:
  White paper:  0.002252"  per page
  Cream paper:  0.0025"    per page
```

Example: 200-page book on cream paper = 200 x 0.0025 = 0.500" spine

**Books under 100 pages:** No spine text allowed by KDP. Use a solid color or minimal design element.

### KDP Cover Template

Download from: https://kdp.amazon.com/en_US/cover-templates
- Enter trim size, page count, paper color
- Downloads a PDF template with bleed marks, spine boundaries, barcode placement

---

## Step 2: Genre Signal Analysis

**Critical rule:** Genre fit > artistic quality. A beautiful cover that signals the wrong genre will kill sales.

### Process

1. Go to the Amazon bestseller list for your target category
2. Screenshot the top 20 covers
3. Identify the patterns:
   - **Dominant colors** (religious = gold/burgundy/navy, self-help = bright/white, thriller = dark/red)
   - **Typography style** (serif = traditional/literary, sans-serif = modern/business)
   - **Image treatment** (photographic, illustrated, abstract, text-only)
   - **Layout** (centered, asymmetric, full-bleed image)
4. Your cover must MATCH these patterns while standing out within them

### 8 Cover Mistakes That Kill Sales (from Kings of Kindle Ch 6)

1. Wrong genre signal — romance cover on a business book
2. Too many fonts — max 2 font families
3. Unreadable at thumbnail — title must pop at 120x180px
4. Cluttered composition — one focal point, not five
5. Stock photo cliches — avoid the obvious Shutterstock picks everyone uses
6. Bad color contrast — title disappears into background
7. DIY look — screams amateur, signals low-quality content
8. No series branding — books in a series should look like siblings ("Pringles Principle": same designer, shared palette, consistent layout)

---

## Step 3: Art Research (Public Domain Focus)

For reprints, compilations, and classical/religious books, public domain art is ideal: free, beautiful, high-resolution, and genre-appropriate.

### Public Domain Rules

| Condition | Status |
|-----------|--------|
| Artist died 70+ years ago (most countries) | Public domain |
| Published before 1928 (US) | Public domain |
| Photo of a 2D artwork (US — Bridgeman v. Corel) | No new copyright |
| Museum restricts downloads but art is PD | Legal to use, may violate museum ToS |

**Safe sources for high-res PD art:**

| Source | Quality | Notes |
|--------|---------|-------|
| **Wikimedia Commons** | Variable (some excellent) | Always check license tag |
| **Metropolitan Museum Open Access** | Excellent | CC0, download button on qualifying works |
| **National Gallery of Art (DC)** | Excellent | Open Access program, high-res TIFF |
| **Rijksmuseum** | Excellent | Rijksstudio, CC0 |
| **Art Institute of Chicago** | Excellent | CC0 on qualifying works |
| **Rawpixel PD collection** | Good | Curated, already cleaned up |
| **Google Arts & Culture** | Variable | Good for discovery, download from museum site |
| **Library of Congress** | Excellent | Prints & Photographs division |

### Art Research Process

1. **Identify themes** from the manuscript (contemplation, light/dark, sacred spaces, saints)
2. **Search by theme** on Wikimedia Commons, Met, NGA
3. **Search by referenced figures** — if the book mentions St. Bernard, Teresa of Avila, etc., find classical depictions
4. **Search by period** — match the book's era (medieval manuscript illuminations for medieval texts, Baroque for Counter-Reformation, etc.)
5. **Evaluate each candidate:**
   - Public domain status confirmed?
   - High-res available (minimum 300 DPI at cover size)?
   - Crops well to book dimensions?
   - Mood match? (contemplative, serious, luminous — not saccharine or kitschy)
   - Passes the thumbnail test?
6. **Present 10-15 options** with links, artist/date, rights status, and notes on why each fits

### Art Categories by Book Type

| Book Genre | Art Direction |
|------------|---------------|
| Catholic mysticism/theology | Renaissance/Baroque religious art, monastery scenes, contemplative saints, gold leaf illuminations |
| Catholic devotional | Sacred Heart, Marian art, gentle pastorals, warm tones |
| Church history | Historical scenes, manuscript illuminations, portraits of popes/saints/doctors |
| Philosophy/apologetics | Classical architecture, symbolic still life, text-heavy minimalist |
| Biblical studies | Old Master biblical scenes, archaeological imagery |
| Prayer/contemplative | Landscapes, monastic interiors, candlelight, soft focus |
| Lives of saints | Portraits, hagiographic scenes, attribute symbolism |

---

## Step 4: Palette & Typography

### Palette Generation

Start from the dominant colors of your chosen artwork, then build a 4-color scheme:

1. **Primary** — background or dominant field (from artwork)
2. **Secondary** — title text color (must contrast with primary)
3. **Accent** — subtitle, author name, decorative elements
4. **Neutral** — spine, back cover base

**Catholic/religious palette families:**
- **TAN Books**: Cream + burgundy + gold
- **Ignatius Press**: Navy + gold + white
- **Sophia Institute**: Forest green + cream + gold
- **EWTN/Ascension**: Royal blue + white + gold

### Typography

| Element | Recommendation |
|---------|---------------|
| **Title** | Serif for traditional/literary (Garamond, Caslon, Minion, Cormorant). Sans-serif for modern/practical (Montserrat, Lato). |
| **Subtitle** | Same family as title, lighter weight or smaller size |
| **Author name** | Same family, small caps or regular weight |
| **Max fonts** | 2 families absolute maximum |
| **Hierarchy** | Title 3-4x larger than author name. Subtitle between. |

---

## Step 5: Design Brief Document

Output a markdown document with all of the above, structured for handoff:

```markdown
# Cover Design Brief: [Book Title]

## Specs
- Trim: [size]
- Spine: [width]" ([page count] pages, [paper color] paper)
- Template: [KDP template download link or note]

## Genre Context
[2-3 sentences on what covers in this category look like]

## Art Direction
[Mood, tone, era, specific imagery direction]

### Artwork Options
1. [Title] by [Artist] ([Year]) — [link] — [why it fits]
2. ...

## Palette
- Primary: [hex/description]
- Secondary: [hex/description]
- Accent: [hex/description]

## Typography
- Title: [font recommendation]
- Subtitle/Author: [font recommendation]

## Comp Covers
[5-8 Amazon links or cover images to study]

## Thumbnail Test
[Specific criteria for this book]

## Series Branding Notes
[If part of a series, how to maintain visual consistency]
```

---

## Workflow

```
1. Get manuscript + niche data (from listing-optimizer or niche-scout output)
2. Calculate trim/spine specs from page count
3. Analyze top 20 covers in target category
4. Research public domain art (10-15 candidates)
5. Generate palette from chosen artwork
6. Recommend typography
7. Compile design brief document
8. Run thumbnail test on mockup
```

## Integration

- **Input from:** `niche-scout` (category data), `listing-optimizer` (title/subtitle), Vellum (page count)
- **Output to:** Designer (Fiverr/Miblart brief), Canva (self-design), or future Canva MCP automation
- **Series connection:** When doing multiple books, reference the first book's brief for "Pringles Principle" consistency
