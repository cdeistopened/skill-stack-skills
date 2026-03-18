# Vellum Prep

Convert markdown manuscripts to Vellum-ready Word documents.

## When to Use

Use this skill when you have a markdown manuscript (from OCR, writing, or conversion) that needs to be formatted for import into Vellum book formatting software.

## What It Does

**Programmatic cleanup (no AI tokens):**
- Removes OCR metadata headers (processing timestamps, chunk markers, model info)
- Converts `---` to `***` (Vellum ornamental breaks)
- Removes duplicate running headers (e.g., repeated book title)
- Removes `[Image: ...]` placeholder descriptions (margin notes, decorations, back covers)
- Strips publisher front matter (catalogs, copyright boilerplate, pricing, paper notices)
- Strips publisher back matter (advertising sections, "By the Same Author", press notices for other books)
- Removes Contents/TOC tables (Vellum auto-generates)
- Normalizes chapter headings to `# Chapter X: Title` format
- Fixes OCR hyphenation artifacts (`defi- nition` → `definition`) via regex `(\w)- (\w)`
- Fixes bold all-caps drop caps (`**GOD** is` → `God is`, `IT is` → `It is`)
- Detects and removes duplicate content from OCR chunk boundary overlaps
- Cleans common artifacts (page numbers, ellipses)
- Converts to .docx via pandoc

**Editorial judgment (requires reading):**
- Evaluate front matter: what's essential for a modern reprint vs. dated (WWI paper shortages, original pricing, publication venue mentions)
- Evaluate back matter: keep charming period testimonials, cut advertising for other books
- Flag corrupted chunk boundaries where text is truncated or garbled (mark with `[text missing]`)
- Add review request page (tasteful, genre-appropriate, after last chapter)
- Add copyright/public domain notice page

## Usage

```bash
# From the manuscript directory:
python3 /path/to/vellum_prep.py manuscript.md

# Output: manuscript_vellum.md + manuscript.docx (if pandoc available)
```

Or invoke via Claude:
```
/vellum-prep manuscript.md
```

## Vellum Formatting Rules

| Markdown | Word Style | Vellum Element |
|----------|-----------|----------------|
| `# Chapter 1: Title` | Heading 1 | Chapter |
| `# Dedication` | Heading 1 | Dedication |
| `# Prologue` | Heading 1 | Prologue |
| `## Section` | Heading 2 | Level 1 Subhead |
| `***` | Centered asterisks | Ornamental Break |
| Single blank line | Blank paragraph | Scene Break |

## Configuration

Edit the script to customize:
- `header_patterns`: List of regex patterns for headers to remove
- `remove_images`: Whether to strip `[Image: ...]` tags
- `clean_for_vellum`: Apply Vellum-specific formatting

## Requirements

- Python 3.x
- pandoc (for .docx conversion)

## Handling Complex Manuscripts

For manuscripts with special requirements (Notion exports, external images, nested chapters), create a **book-specific preprocessing script**. See `Personal/Guide Abrege/prep_guide_abrege.py` for an example that handles:

### Notion Export Issues
- **Missing image folders**: Notion exports reference `FolderName/image.png` but don't always include the folder
- **Substack CDN images**: Can be downloaded with curl and remapped to local paths
- **Image mapping pattern**:
  ```python
  IMAGE_MAP = {
      "substack-uuid_dimensions.png": "images/01-descriptive-name.png",
  }
  ```

### Nested Chapter Headings
When a document has nested "CHAPTER I/II/III" within sections (e.g., each movement family has its own Chapter I, II, III):
- Keep top-level sections as `#` (Vellum chapters)
- Demote internal "CHAPTER X:" labels to `##` subheadings
- Strip the "CHAPTER X:" prefix, keep just the descriptive title

### Tables
- Multi-line cells in markdown tables **don't convert well** via pandoc - convert to numbered lists instead
- See `prep_guide_abrege.py` for regex pattern to match and replace specific tables

### Bold Labels as Headings
Instructional books often use `**FIRST TYPE:**` or `**Method A:**` as implicit subheadings. Convert these to actual headings (`####`) for proper Vellum hierarchy.

### Workflow for Complex Books
1. Run exploratory agent to analyze structure
2. Create book-specific prep script
3. Download/remap external images
4. Run prep script → intermediate `.md`
5. Run `pandoc` directly (not vellum_prep.py) to preserve images
6. Review in Vellum, fix Parts/special elements manually

## Public Domain Reprint Checklist

For reprints of out-of-copyright works:

1. **Copyright page**: "Original work by [Author] is in the public domain. This edition, including arrangement and typesetting, copyright [YEAR] [Publisher]. Cover design copyright [YEAR] [Publisher]."
2. **Review request page**: After final chapter, before appendices. Thank the reader, explain why reviews matter, clear CTA. Match the book's register (devotional ≠ business).
3. **Front matter triage**: Keep prefaces that frame the work theologically/historically. Cut paragraphs about paper shortages, original pricing, publication venues (e.g., "first appeared in the American Catholic Quarterly Review").
4. **Back matter triage**: Keep period testimonial letters (charming, historical). Cut "By the Same Author" advertising sections, press notices for other books, publisher catalogs.
5. **Contents table**: Always remove — Vellum generates its own.

## OCR Chunk Boundary Traps

When manuscripts come from chunked OCR (e.g., Gemini vision processing PDFs in 15-page chunks):

- **Truncated sentences**: Text cuts off mid-word at chunk end, next chunk starts mid-paragraph. Look for abrupt `...afteIs it not` type joins.
- **Duplicate content**: Same passage appears at end of one chunk and start of the next. The Newman development section appeared in both Ch II and Ch III — had to identify which chapter it properly belonged to and remove the duplicate.
- **Garbled text**: Chunk boundary corruption produces nonsense like `vouchsafed to themple in point` (should be "vouchsafed to them... example in point"). Flag with `[text missing]` if unrecoverable.
- **Orphaned sentences**: Random sentences that don't fit context, dragged from adjacent chunks. Remove after verifying they appear correctly elsewhere.

## Files

- `SKILL.md` - This file
- `vellum_prep.py` - Main conversion script (OCR cleanup focus)
