# Dual Exposure Photo-Grid Composite Tribute Poster

Conceptual tribute poster style combining a portrait silhouette with a photo mosaic grid of the subject's life and work. High-end, editorial, mixed-media aesthetic.

---

## Template Variables

Replace `[BRACKETS]` with subject-specific details.

---

## Instagram Version (1:1 Square)

```
Generate a dual exposure photo-grid composite tribute poster for [SUBJECT NAME]. Style: high-end conceptual tribute poster.

CENTRAL STRUCTURE (THE VESSEL):
The central focus is a large-scale, high-contrast black and white portrait silhouette of [SUBJECT NAME]. This main portrait acts as the container.

THE GRID FILL & TEXTURES (MIXED MEDIA):
The interior of the silhouette is populated by a dense "photo mosaic grid" of scenes from [SUBJECT]'s life and intellectual world — [LIST 6-8 SPECIFIC SCENES: e.g., lecture halls, handwritten manuscripts, specific locations, seminar rooms, stacks of books, crowds of students, relevant architecture, and landscapes].

CRITICAL TEXTURE INSTRUCTION: Do not just paste flat photos. Apply artistic textures to various grid cells to create a tactile, collage feel. Use effects like:
- Halftone Dots: Comic-book style raster patterns on some cells.
- Fabric/Embroidery: Subtle thread or canvas textures suggesting [RELEVANT TEXTILE: e.g., a clerical vestment, a wool sweater, classroom felt].
- Film Grain: Heavy noise on specific high-contrast documentary-style shots.

COLOR STRATEGY:
The base is Monochrome B&W. Use selective color overlays — muted earth tones ([LIST 3 COLORS: e.g., terracotta, olive, deep indigo]) — ONLY on specific grid cells to create a rhythm. These suggest [WHAT THE COLORS EVOKE: e.g., Mexico, the Church, and the printed page].

TYPOGRAPHY & BRANDING (STRICT MICRO-SCALING):
Do NOT include any text or typography on the image. No names, no labels, no captions.

COMPOSITION & BACKGROUND:
Background: Off-white or light grey with a visible high-quality paper or concrete texture. It should not be flat digital white.
Alignment: Center the figure perfectly. Maintain wide negative space around the object.
```

**Usage:**
```bash
export GEMINI_API_KEY=$(grep GEMINI_API_KEY .env | cut -d'=' -f2) && \
python ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" \
  "YOUR PROMPT HERE" \
  --input path/to/reference-photo.jpg \
  --model pro \
  --aspect 1:1 \
  --output "path/to/content/folder" \
  --name "subject-tribute"
```

---

## Thumbnail Version (16:9 Landscape)

```
Generate a dual exposure photo-grid composite tribute image for [SUBJECT NAME]. Style: high-end conceptual tribute, landscape format.

CENTRAL STRUCTURE (THE VESSEL):
A large-scale, high-contrast black and white portrait silhouette of [SUBJECT NAME], positioned slightly left of center to create visual tension in the wide format. The silhouette acts as the container for the mosaic grid.

THE GRID FILL & TEXTURES (MIXED MEDIA):
The interior of the silhouette is populated by a dense "photo mosaic grid" of scenes from [SUBJECT]'s life and intellectual world — [LIST 6-8 SPECIFIC SCENES].

CRITICAL TEXTURE INSTRUCTION: Do not just paste flat photos. Apply artistic textures to various grid cells to create a tactile, collage feel. Use effects like:
- Halftone Dots: Comic-book style raster patterns on some cells.
- Fabric/Embroidery: Subtle thread or canvas textures suggesting [RELEVANT TEXTILE].
- Film Grain: Heavy noise on specific high-contrast documentary-style shots.

COLOR STRATEGY:
The base is Monochrome B&W. Use selective color overlays — muted earth tones ([LIST 3 COLORS]) — ONLY on specific grid cells to create a rhythm.

TYPOGRAPHY & BRANDING:
Do NOT include any text or typography on the image. No names, no labels, no captions.

COMPOSITION & BACKGROUND:
Background: Off-white or light grey with a visible high-quality paper or concrete texture. It should not be flat digital white.
Alignment: Position the figure slightly left of center. Use the extra horizontal space for generous negative space on the right, creating a cinematic, editorial feel.
```

**Usage:**
```bash
export GEMINI_API_KEY=$(grep GEMINI_API_KEY .env | cut -d'=' -f2) && \
python ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" \
  "YOUR PROMPT HERE" \
  --input path/to/reference-photo.jpg \
  --model pro \
  --aspect 16:9 \
  --output "path/to/content/folder" \
  --name "subject-tribute-thumbnail"
```

---

## Examples

### Ivan Illich (Instagram 1:1)
- **Grid scenes:** Lecture halls, handwritten manuscripts, Mexican streetscapes of Cuernavaca, CIDOC seminar rooms, stacks of books, crowds of students, ecclesiastical architecture, Latin American landscapes
- **Textures:** Clerical vestment fabric, film grain on documentary shots
- **Colors:** Terracotta, olive, deep indigo (evoking Mexico, the Church, the printed page)

### John Taylor Gatto (Thumbnail 16:9)
- **Grid scenes:** NYC public school hallways, Wall Street Journal op-ed pages, classroom chalkboards, homeschool conference stages, taxi cabs, Madison Avenue offices, stacks of textbooks, state capitol buildings
- **Textures:** Chalk dust, newspaper halftone, worn classroom wood
- **Colors:** Slate blue, warm amber, brick red (evoking NYC schools, journalism, American institutions)

### Maria Montessori (Thumbnail 16:9)
- **Grid scenes:** Casa dei Bambini classroom, child-sized materials, Roman architecture, Indian landscapes, Amsterdam canals, children working with beads, medical instruments, handwritten letters
- **Textures:** Linen fabric, watercolor washes, aged paper
- **Colors:** Terracotta, sage green, warm gold (evoking Italy, natural materials, warmth)

---

## Key Learnings

1. **Always use a high-res reference photo** (1000px+ minimum, 1920px+ ideal) via the `--input` flag
2. **No text on the image** - typography renders unreliably; add text in post-production
3. **Photo era matters** - match the reference photo's age to the narrative context
4. **16:9 works better for thumbnails** - offset the silhouette slightly left of center for the landscape format
5. **Selective color overlays** should be thematic, not random - they tell a story about the subject's world
