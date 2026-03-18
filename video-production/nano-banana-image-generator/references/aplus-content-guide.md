# Amazon KDP A+ Content — Image Reference

## What A+ Content Is

Enhanced product page content for Amazon books. Adds visual modules below the book description. Proven to increase conversion ~5%. Available to all KDP authors through the KDP dashboard.

## Rules

- Max **5 modules** per detail page
- Company Logo module: max 1 per page
- **JPG or PNG only** (RGB, not CMYK)
- Max **2 MB per image** file
- Min 72 DPI (save source at 300 DPI, export at 2x web dimensions)
- Images must be **different** from product gallery images
- **No text that becomes unreadable on mobile** — Amazon auto-resizes
- No pricing, discounts, promotional language, or "buy now"
- No customer reviews or time-sensitive claims
- No competitor comparisons or external links
- No guarantees, refund policies, or shipping details
- Max 4 quotes (from well-known publications/public figures only)
- Awards must be within 2 years with documentation

## Module Specs

All dimensions below are **2x retina** (what you should generate/export at). Amazon minimums are half these values.

### Full-Width Modules

| Module | Generate At | Aspect | Best For |
|--------|-----------|--------|----------|
| **Image Header with Text** | 1940 x 600 | ~3.2:1 | Hero image, main value proposition |
| **Image & Dark Text Overlay** | 1940 x 600 | ~3.2:1 | Atmospheric scene with text overlay |
| **Image & Light Text Overlay** | 1940 x 600 | ~3.2:1 | Same but light background variant |
| **Company Logo** | 1200 x 360 | ~3.3:1 | Brand/imprint logo (max 1 per page) |

### Multi-Column Modules

| Module | Per-Image Size | Aspect | Best For |
|--------|---------------|--------|----------|
| **Three Images & Text** | 600 x 600 | 1:1 | Three key themes/chapters/features |
| **Four Images & Text** | 440 x 440 | 1:1 | Four selling points, compact |
| **Four Image/Text Quadrant** | 270 x 270 | 1:1 | Quick visual grid |

### Single Image Modules

| Module | Image Size | Aspect | Best For |
|--------|-----------|--------|----------|
| **Single Left/Right Image** | 600 x 600 | 1:1 | Feature highlight + text block |
| **Single Image & Highlights** | 600 x 600 | 1:1 | Image + bullet points |
| **Single Image & Sidebar** | 600 x 800 | 3:4 | Tall image + narrow sidebar text |
| **Single Image & Specs** | 600 x 600 | 1:1 | Image + specification table |

### Comparison & Text-Only

| Module | Image Size | Notes |
|--------|-----------|-------|
| **Comparison Chart** | 300 x 600 per product | Compare your other books by ASIN |
| **Product Description Text** | N/A | Text only |
| **Standard Text** | N/A | Text only |
| **Technical Specifications** | N/A | Table format, text only |

## Recommended Layout for Books

For a nonfiction book like OLR, a strong 5-module layout:

1. **Image Header** (1940x600) — Hero shot: ranch landscape, community life, or thematic scene
2. **Three Images & Text** (3x 600x600) — Three pillars: Spiritual Life / Sustainable Farm / Ecclesial Community
3. **Single Left Image** (600x600) — Author photo or community photo + author credibility text
4. **Single Right Image** (600x600) — Interior page preview or map of the property
5. **Comparison Chart** — Other books in the series or related titles

## Generation Workflow

```bash
# 1. Generate hero banner
python3 generate_image.py \
  "Panoramic view of rolling green hills with a small chapel..." \
  --model flash --aspect 16:9 \
  --seo-name "olr-aplus-hero" \
  --output "./aplus-images/"

# 2. Optimize to A+ banner dimensions
python3 image_optimizer.py \
  "./aplus-images/olr-aplus-hero-gen.jpg" \
  --use aplus-banner

# 3. Generate three-column images (1:1)
python3 generate_image.py \
  "Watercolor of a family praying together..." \
  --model flash --aspect 1:1 \
  --seo-name "olr-aplus-spiritual" \
  --output "./aplus-images/"

python3 image_optimizer.py \
  "./aplus-images/olr-aplus-spiritual-gen.jpg" \
  --use aplus-three-col
```

## Style Notes for Book A+ Content

- **Don't use generic stock photography feel** — use the same visual style as the book cover for brand cohesion
- **Interior page previews** are high-converting for nonfiction — screenshot actual typeset pages
- **Keep text in images minimal** — Amazon's text-in-image rules are strict and mobile crushes readability
- **Show the lifestyle, not just the product** — for a homesteading book, show the life, not just the book
