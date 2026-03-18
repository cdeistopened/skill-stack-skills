# KDP Cover Dimensions Reference

Complete dimension formulas and constants for Amazon KDP print and ebook covers.

## Paper Multipliers (Spine Width Per Page)

| Paper Type | Multiplier (inches/page) |
|-----------|-------------------------|
| White | 0.002252 |
| Cream | 0.0025 |
| Standard color | 0.0032 |
| Premium color | 0.002252 |

## Cover Formulas

```
spine_width  = page_count × paper_multiplier
full_width   = 0.125 + back_trim_w + spine_width + front_trim_w + 0.125
full_height  = 0.125 + trim_h + 0.125
```

### Safety Zones

| Zone | Dimension | Notes |
|------|-----------|-------|
| Bleed | 0.125" all sides | Content must extend to bleed edge |
| Text safety | 0.25" from trim edges | ALL text must be inside this |
| Spine safety | 0.0625" each side | Amazon hard requirement |
| Spine text | Only if pages > 79 | KDP rejects spine text on thin books |

## All KDP Trim Sizes

| Size (inches) | Common Name / Use |
|---------------|-------------------|
| 5 x 8 | Pocket — short nonfiction, spiritual reading |
| 5.06 x 7.81 | Digest |
| 5.25 x 8 | |
| 5.5 x 8.5 | Trade — most nonfiction |
| 6 x 9 | US Trade — business, self-help |
| 6.14 x 9.21 | Royal |
| 6.69 x 9.61 | Crown Quarto |
| 7 x 10 | Large — textbooks, workbooks |
| 7.44 x 9.69 | |
| 7.5 x 9.25 | |
| 8 x 10 | |
| 8.25 x 6 | Landscape |
| 8.25 x 8.25 | Square |
| 8.5 x 11 | Letter — manuals, cookbooks |

## Words Per Page by Trim Size

| Trim Size | Words/Page | Notes |
|-----------|-----------|-------|
| 5 x 8 | 250 | Standard for pocket books |
| 5.5 x 8.5 | 260 | Standard for trade |
| 6 x 9 | 280 | Standard for US trade |

Formula: `page_count = ceil(word_count / words_per_page)`, rounded up to even.

## Minimum Art Resolution (300 DPI)

| Trim Size | Front Cover Pixels | Full Wrap Width (example: 200pg cream) |
|-----------|-------------------|---------------------------------------|
| 5 x 8 | 1537 x 2475 | ~3450 x 2475 |
| 5.5 x 8.5 | 1687 x 2625 | ~3750 x 2625 |
| 6 x 9 | 1837 x 2775 | ~4050 x 2775 |

## Kindle Ebook Cover

| Property | Value |
|----------|-------|
| Recommended size | 1600 x 2560 px |
| Aspect ratio | 1:1.6 |
| Minimum size | 625 x 1000 px |
| Format | JPEG or TIFF, RGB color |
| Max file size | 50 MB |

**Key insight:** 5x8 trim ratio = 1:1.6 = exact Kindle ratio. The print front cover (1537x2475) upscales to 1600x2560 with minimal distortion. Free ebook cover from the print cover.

## KDP Template Verification

Download the official template from: **kdp.amazon.com/cover-calculator**

Enter: binding type, interior type, paper color, trim size, page count. Returns a PNG with pink safety zones, barcode placement, and spine guides. Overlay on your generated PDF to verify alignment before upload.
