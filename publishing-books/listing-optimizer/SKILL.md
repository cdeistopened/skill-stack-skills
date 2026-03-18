---
name: listing-optimizer
description: Write Amazon KDP book descriptions (HTML-formatted), select categories, fill backend keywords, and build author bios. Use when preparing a book for Amazon upload or optimizing an existing listing.
---

# Listing Optimizer

Write the complete Amazon listing package: description, categories, keywords, and author bio.

## What It Produces

1. **Book Description** — 5-part framework, output as Amazon-ready HTML
2. **Category Selections** — 3 picks, screened for ghosts and duplicates
3. **Backend Keywords** — 7 boxes filled using the hybrid strategy
4. **Author Bio** — 50-100 words, 5-key template

---

## Part 1: Book Description (5-Part Framework)

Source: Sean Dollwet, "Amazon KDP MISTAKES"

| Section | Purpose | Length |
|---------|---------|-------|
| **1. Hook/Headline** | Stop the scroll. Bold question or provocative statement. | 1-2 sentences |
| **2. Lead/Credibility** | Who wrote this and why it matters. | 2-3 sentences |
| **3. Bullet Points** | What's inside — features AND benefits, scannable. | 5-8 bullets |
| **4. Overcome Objections** | "Even if you've never..." / "Whether you're..." | 2-3 sentences |
| **5. Call to Action** | Ask for the sale. Direct and clear. | 1 sentence |

### Amazon HTML Reference

Amazon KDP descriptions support a **very limited** set of HTML tags. Use only these:

| Tag | Purpose | Example |
|-----|---------|---------|
| `<b>text</b>` | Bold | `<b>Stop buying boring books.</b>` |
| `<i>text</i>` | Italic | `<i>A Way of Salvation</i>` |
| `<br>` | Line break | End of sentence or between sections |
| `<p>text</p>` | Paragraph | Adds spacing below |
| `<h4>text</h4>` | Heading (largest allowed) | Section headers |
| `<h5>text</h5>` | Subheading | |
| `<h6>text</h6>` | Small heading | |
| `<ul><li>text</li></ul>` | Bullet list | Feature/benefit lists |
| `<ol><li>text</li></ol>` | Numbered list | Step-by-step |

**NOT supported:** `<h1>`-`<h3>`, `<img>`, `<a>` (links), `<div>`, `<span>`, CSS, colors, fonts, tables. Amazon will strip or reject unsupported tags.

**Character limit:** All characters count, including HTML tags. `<b>test</b>` = 11 characters.

### Description Template

```html
<h4><b>Are you searching for a life of deeper faith, closer family, and real community?</b></h4>

<p>Phil [Last Name] spent twenty years building what most people only dream about — a Catholic family homestead where prayer, farming, and community life come together as one. <i>Our Lady's Ranch</i> tells the story of how one family answered God's call to create something beautiful.</p>

<p><b>Inside you'll discover:</b></p>
<ul>
<li>How the Medjugorje messages inspired a practical way of daily living</li>
<li>The 4 types of Catholic Family Homesteads and which fits your family</li>
<li>A proven ownership structure that balances community with privacy</li>
<li>Why "hobby farming" beats commercial farming for family life</li>
<li>The 5 essential activities that build unbreakable family bonds</li>
<li>Practical steps to start your own homesteading journey — even from the city</li>
</ul>

<p>Whether you're a young family seeking alternatives to modern culture, empty nesters ready for a new chapter, or anyone drawn to intentional Catholic community — this book provides both the vision and the practical blueprint.</p>

<p><b>Scroll up and click "Buy Now" to begin your family's journey to peace.</b></p>
```

### Writing Rules

- **Lead with the reader's benefit**, not the author's story ("the autobiography trap")
- Every word is an algorithm signal — audit for unintended keyword associations
- Avoid health claims ("heal", "cure") — blocks Amazon Ads. Use "improve", "discover", "support"
- Study top-selling descriptions in your category and model their structure
- Bold main points, italicize key terms, use bullets — visual distinction matters

---

## Part 2: Category Selection (3 Picks)

Source: Dave Chesson, "INSANE Amazon Category Change" + "How to Choose Amazon Book Categories in 2023"

### The 2023+ System

- You select **exactly 3** Amazon categories (not BISAC codes)
- No contact form to request changes — your 3 picks are final
- Amazon reserves the right to override based on your keywords/metadata

### 5-Step Process

1. **Identify fitting categories** with realistic ranking potential. Check BSR of top books — categories where leaders sit at BSR 20K-80K offer the best path. Under 5K = heavy hitters.

2. **Use duplicates strategically.** 54% of KDP categories are duplicates. One pick that maps across multiple browse paths = maximum coverage from a single selection.

3. **Screen for ghost categories.** 27% are ghosts — they look real but lead to dead-end pages with no bestseller tag. Visit the actual Amazon page: if it lacks a category name and browsable tree in the sidebar, it's a ghost.

4. **Make your 3 selections** with full knowledge of the duplicate map and ghost list.

5. **Reinforce with keywords.** Dedicate 1-2 of your 7 keyword boxes to category-specific terms. Use additional boxes for terms from categories you didn't select — Amazon may add you automatically.

### 4 Misclassification Culprits

1. **Too-broad keywords** — "romance" instead of "New York hot steamy girl boss romance"
2. **Careless description language** — Amazon reads every word. A romance book mentioning "roll of the dice" got classified as gambling.
3. **Spammy marketing** — corrupts Amazon's understanding of your audience
4. **Unintended metadata overlaps** — author name or title containing common words that trigger wrong categories

---

## Part 3: Backend Keywords (7 Boxes)

Source: Kings of Kindle Ch 3, 121-author experiment

### How Amazon Keywords Work

- Amazon **recombines words automatically** — no need to repeat combinations
- More words per box **dilutes ranking** for each term
- Title/subtitle keywords rank **higher** than backend boxes
- Amazon reads: title, subtitle, 7 keyword boxes, description, categories, author name

### The Hybrid Strategy

Split your 7 boxes into two groups:

**Boxes 1-3 (or 1-4): Exact Target Phrases**
- Your most important search terms as complete phrases
- These are the terms you want to rank for directly
- Example: `catholic homesteading community` / `intentional catholic community` / `benedict option catholic`

**Boxes 4-7 (or 5-7): Broad Descriptive Fill**
- Individual words and modifiers that Amazon can recombine
- Category reinforcement terms (1-2 boxes dedicated to this)
- Related topic words that expand your reach
- Example: `faith family farming agrarian rural` / `medjugorje prayer rosary spirituality` / `homestead sustainable organic self sufficient`

### Keyword Rules

- **No commas** (Amazon treats commas as separators, wasting space)
- **No quotes** around phrases
- **No words already in your title/subtitle** (they already rank)
- **No brand names** (Kindle, Amazon, etc.)
- **No subjective claims** (best, amazing, #1)
- **No Amazon program names** (KDP Select, Prime, etc.)

### Research Process

1. **Amazon autocomplete** — Type your seed keyword, note suggestions. Use alphabet technique (keyword + a, keyword + b, etc.)
2. **Competitor titles** — Mine keywords from successful self-published titles in your niche
3. **DataForSEO** — Check search volume for candidate phrases
4. **Category terms** — Include words that reinforce your chosen categories

### Optimization Loop

After launch, use Amazon Ads search term reports to:
- Find converting search terms → promote to exact-phrase boxes
- Find non-converting terms → replace with new candidates
- Iterate monthly for first 3 months, then quarterly

---

## Part 4: Author Bio (5-Key Template)

Source: Zach Diamanti, "How to Write an Author Bio"

**Length:** 50-100 words. That's it.

| Key | Purpose | Example |
|-----|---------|---------|
| **1. Punchy opener** | Name your books/genre, set expectations | "Phil [Last Name] is an architect turned homesteader who spent twenty years building Catholic family communities in the California foothills." |
| **2. Expertise** | Non-fiction: credentials. Fiction: voice/personality. | "He founded Our Lady's Ranch in Grass Valley, California..." |
| **3. Credibility** | Awards, features — state simply, don't brag | "...where multiple families now live the homesteading vision he describes in this book." |
| **4. Personal touch** | Humanize — hobby, family, location | "Father of seven, he splits his time between prayer, farming, and architectural design." |
| **5. CTA** | Website, freebie, social handle | "Visit ourladysranch.com to learn more." |

**Tailor to the audience.** Same author, different books = different bios.

---

## Listing Mistakes Checklist

Before publishing, verify:

- [ ] Subtitle displays fully in search results (not truncated)
- [ ] Description uses 5-part framework (not 5 sad sentences)
- [ ] A+ Content has 3-5 modules (see `nano-banana-image-generator/references/aplus-content-guide.md`)
- [ ] No health claims blocking ads ("heal"/"cure" → "improve"/"discover")
- [ ] Description leads with reader benefit, not author biography
- [ ] Category selections verified as non-ghost (visited actual Amazon pages)
- [ ] Keywords don't duplicate title/subtitle words
- [ ] Author bio is 50-100 words with all 5 keys
- [ ] Title is instantly clear at thumbnail size

---

## Workflow

```
1. Read the manuscript (or summary)
2. Run /niche-scout to validate niche + get keyword data
3. Draft description using 5-part framework → output as HTML
4. Research categories using BSR data from niche-scout
5. Fill 7 keyword boxes using hybrid strategy
6. Write author bio using 5-key template
7. Generate A+ Content images (see nano-banana skill)
8. Review against Listing Mistakes Checklist
```
