# Line Art / Scanned Illustration Cleanup

Clean scanned line art, woodcuts, and black-and-white illustrations from magazine or book pages. Produces high-contrast black-on-white images suitable for print reproduction.

## When to Use

- Cleaning illustrations extracted from scanned PDFs or magazines
- Removing scan artifacts (yellowing, grey spots, foxing, bleed-through)
- Isolating an illustration from surrounding text on a page
- Preparing historical woodcuts or line art for modern publication

## Two-Step Workflow

### Step 1: PIL Crop (Isolate the Illustration)

Extract the page from the PDF at 300 DPI using pymupdf, then crop to just the illustration area using PIL. This is critical — sending a full page with surrounding text to Gemini causes reinterpretation rather than cleanup.

```python
import fitz  # pymupdf
from PIL import Image

# Extract page at 300 DPI
doc = fitz.open("source.pdf")
page = doc[page_number - 1]  # 0-indexed
mat = fitz.Matrix(300/72, 300/72)
pix = page.get_pixmap(matrix=mat)
pix.save("page_raw.jpg")

# Crop to illustration area
img = Image.open("page_raw.jpg")
w, h = img.size

# For two-page spread scans:
# Right side illustration: left=50%, top=5%, right=95%, bottom=70%
# Left side illustration: left=5%, top=5%, right=50%, bottom=70%
# Adjust percentages per page — view first, then crop

crop_box = (int(w * 0.50), int(h * 0.05), int(w * 0.95), int(h * 0.70))
cropped = img.crop(crop_box)
cropped.save("illustration_crop.jpg", quality=95)
```

**Key rule:** Always VIEW the extracted page first, then specify crop coordinates. Illustration positions vary per page.

### Step 2: Gemini Cleanup

Use the nano-banana image generator with `--input` flag (rework mode) to clean the cropped illustration.

```bash
source ~/.zshrc && python3 generate_image.py \
  --input illustration_crop.jpg \
  --prompt "CLEANUP PROMPT HERE" \
  --model pro \
  --aspect square
```

### Gemini Cleanup Prompt Template

```
Clean up this scanned line art illustration for print publication.

PRESERVE with absolute fidelity:
- All original line work exactly as drawn
- All text, captions, and lettering that are part of the illustration design
- The artist's original style, line weight, and composition
- All fine details in the drawing

REMOVE:
- Yellowed or grey background — make pure white
- Scan artifacts: spots, specks, dust marks
- Page bleed-through from the reverse side
- Any surrounding text that is NOT part of the illustration

DO NOT:
- Redraw, simplify, or reinterpret any part of the illustration
- Change line weights or add new lines
- Smooth out intentional texture or artistic marks
- Add shading, gradients, or grey tones that weren't in the original
- Crop the illustration differently

Output: High-contrast black line art on pure white background.
```

### Variations

**For illustrations with captions/titles (keep text):**
Add to prompt: "Keep all text/captions that appear to be part of the illustration design (titles, labels, speech bubbles, credits)."

**For illustrations extracted from colored pages:**
Add to prompt: "The original was printed on tinted paper. Convert all background areas to pure white while preserving black line work."

**For very damaged scans (heavy foxing/staining):**
Add to prompt: "This scan has significant damage. Focus on recovering the black line work — err on the side of preserving too much rather than losing fine details."

## Quality Checklist

After cleanup, verify:
- [ ] Background is pure white (no grey cast)
- [ ] All original lines are preserved (compare with scan)
- [ ] No new lines or details added by Gemini
- [ ] Text/captions legible and undistorted
- [ ] No scan artifacts remaining
- [ ] File is JPEG (Gemini outputs JPEG data even with .png extension — verify with `file` command)

## File Organization

```
Illustrations/
├── extracted/     ← Raw page extractions from PDFs (300 DPI)
├── cropped/       ← PIL crops of individual illustrations
└── cleaned/       ← Gemini-cleaned final versions
```

## Known Issues

- **Gemini may reinterpret:** If the crop includes too much surrounding text, Gemini will try to "improve" the illustration rather than clean it. Solution: tighter crop in Step 1.
- **JPEG/PNG mismatch:** Gemini saves as .png but the data is JPEG. Always verify with `file` command and rename to .jpg if needed.
- **Metadata sidecar bug:** `generate_image.py` line 262 throws an error on `image.size` but the image saves successfully. Ignore the exit code.
