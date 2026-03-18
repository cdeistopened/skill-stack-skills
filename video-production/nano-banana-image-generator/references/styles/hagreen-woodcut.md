# Philip Hagreen Woodcut / Catholic Distributist Illustration

Black-and-white satirical woodcut illustrations in the style of Philip Hagreen (1890-1988), artist of the Guild of St. Joseph and St. Dominic at Ditchling, Sussex. Hagreen illustrated the *Cross and the Plough* magazine (1936-1946) for the Catholic Land Movement, producing editorial woodcuts that combined social commentary with Catholic visual tradition.

## When to Use

- Illustrations for the Cross & Plough anthology ("The Last Chance")
- Catholic social teaching or distributist content
- Anti-industrial or agrarian themes
- Satirical commentary on capitalism, industrialism, or modernity
- Religious imagery in a devotional line-art tradition
- Any content connected to CLM Publishing projects

## Reference Image

**Composite of 4 cleaned Hagreen originals:**
`Cross & Plough/Anthology/Illustrations/cleaned/hagreen-style-reference-composite.jpg`

Always submit this composite as `--input` reference when generating in this style. The examples do the heavy lifting — keep prompts simple and let the visual reference guide the style.

## Visual Characteristics

**Line quality:**
- Bold, confident outlines with uniform weight — NOT scratchy or sketchy
- Clean, unbroken contour lines defining forms
- Minimal interior detail — bodies and objects are mostly outline with selective fills
- Solid black fills for clothing, hair, and shadow areas (not crosshatching)
- Flat, graphic quality — closer to linocut than pen-and-ink

**Figures:**
- Stylized, slightly rounded human forms — NOT realistic proportions
- Large heads, shortened bodies, simplified hands
- Figures often anthropomorphized animals (toads, pigs) or allegorical types (top-hat capitalist, laboring worker)
- Clothing rendered with bold black/white contrast — solid black suits, striped trousers
- Faces simplified to a few expressive lines

**Composition:**
- Single-scene satirical tableaux — one clear image, one clear point
- Figures dominate the frame with minimal or no background
- Strong horizontal or pyramidal arrangements
- Caption/title integrated below the illustration in letterpress typography
- Often includes a biblical or literary quote as part of the composition

**Themes & Motifs:**
- Industrial critique: machinery devouring nature, workers in harness, mechanical idols
- Biblical allegory: golden calves, Exodus references, Nativity scenes
- Distributist symbols: land, bread, family, craft, the Holy Family's workshop
- Animals as political metaphors: toads (gluttony), pigs (industry), calves (idolatry)

**What it is NOT:**
- NOT crosshatched or stippled (Hagreen uses solid fills, not texture)
- NOT sketchy or rough (lines are clean and deliberate)
- NOT photorealistic or anatomically precise
- NOT cluttered — compositions are spare and readable
- NOT colored — pure black on white only

## Technical Direction

```
STYLE: 1930s Catholic distributist woodcut illustration in the style of Philip Hagreen. Bold black outlines on white. Flat, graphic quality — solid black fills for clothing and shadows, no crosshatching or stippling. Clean linocut-like contours. Stylized, slightly rounded figures with simplified features.

RENDERING: Pure black ink on white paper. No gray tones, no gradients. Forms defined by bold unbroken contour lines. Shadows and dark areas are solid black fills. White areas are completely clean.

MOOD: Satirical but dignified. The humor is cerebral — visual metaphor and biblical allusion, not caricature. The overall feeling is of a serious magazine with a wry editorial eye.
```

## Example Prompt Structure

```
[Submit hagreen-style-reference-composite.jpg as --input]

Generate a new illustration in EXACTLY the style shown in this reference image — bold black outlines, flat solid fills, stylized rounded figures, clean white background. This is the Philip Hagreen woodcut style from 1930s Catholic magazines.

SUBJECT: [What to illustrate]

CAPTION: [Optional — text to appear below the illustration in serif letterpress style]

The illustration should look like it belongs alongside the four examples in the reference. Same line weight, same level of stylization, same graphic simplicity.
```

## Source Material

- Original magazine: *The Cross and the Plough* (1936-1946), organ of the Catholic Land Association of England and Wales
- Artist: Philip Hagreen (1890-1988), Guild of St. Joseph and St. Dominic, Ditchling
- Cleaned originals: `Cross & Plough/Anthology/Illustrations/cleaned/`
- Raw page scans: `Cross & Plough/Anthology/Illustrations/`
- PDFs: `Cross & Plough/Sources/PDFs/`

## Cleaning Scanned Originals

See `references/styles/line-art-cleanup.md` for the full two-step workflow:
1. PIL crop to isolate illustration from page scan
2. Gemini cleanup (whiten background, remove artifacts, preserve line work)

Batch crop script: `Cross & Plough/Anthology/Illustrations/crop_batch.py`

## Extracted Illustrations Catalog

### Cleaned Originals (8)
| Name | File | Source | Essay |
|---|---|---|---|
| Toad Eating the Cow | `hagreen-toad-cleaned_*` | Issue 35, p5 | "Industrialism at the Bar of Science" |
| As Aaron Said (Golden Calf) | `hagreen-golden-calf-cleaned_*` | Issue 39, p5 | Industrial idolatry / Part I |
| Madonna & Child | `madonna-hail-mary-cleaned_*` | Issue 45, p5 | "Towards Nazareth" / Prologue |
| Equal Opportunity For All | `hagreen-equal-opportunity-cleaned_*` | Issue 56, p6 | "Markets and Martyrs" (Rope) |
| Genesis Grape Vine Border | `genesis-grape-vine-cleaned_*` | Issue 40, p5 | Part II frontispiece |
| Standard of Living | `standard-of-living-cleaned_*` | Issue 46, p6 | Part I (Beveridge) |
| Saint with PAX Book | `saint-pax-book-cleaned_*` | Issue 37, p7 | Prologue / Epilogue |
| INDUSTRY Pig | `industry-pig-cleaned_*` | Issue 36, p5 | Part I motif |

### Novel Generations (6, Hagreen style via Gemini)
| Name | File | Essay |
|---|---|---|
| Towards Nazareth | `towards-nazareth-holy-family_*` | "Towards Nazareth" |
| Jesus the Carpenter | `jesus-the-carpenter_*` | "Jesus the Carpenter" |
| The Laxton Community | `laxton-community_*` | "The Laxton Community" |
| Behold a Great Priest | `mcnabb-great-priest_*` | "Behold a Great Priest" |
| The Birmingham Scheme | `birmingham-scheme_*` | "Prelude to Action" |
| Fragmentation of Knowledge | `fragmentation-knowledge_*` | "Fragmentation of Knowledge" |

### Batch 2 — Cleaned (10)
| Name | File | Source | Essay |
|---|---|---|---|
| Our Primary Industry | `our-primary-industry-cleaned.jpg` | Issue 34, p5 | Part I / imports (artist: Powys Evans) |
| Bureaucracy and Big Business | `bureaucracy-big-business-cleaned.jpg` | Issue 41, p4 | Part I / Beveridge |
| Goose That Laid Golden Eggs | `goose-golden-eggs-cleaned.jpg` | Issue 42, p4 | Part I / wartime |
| Satan & Co. | `satan-and-company-cleaned.jpg` | Issue 45, p3 | Part I / blackmail |
| Prayer for Fruits of Earth | `prayer-sun-moon-wheat-cleaned.jpg` | Issue 47, p7 | Interlude |
| Vocation in Work | `vocation-in-work-cleaned.jpg` | Issue 48, p4 | Part II / dignity |
| Social Security / Industrial Slavery | `social-security-industrial-slavery-cleaned.jpg` | Issue 50, p4 | Part I / Beveridge |
| Caesar's Master (Madonna) | `caesars-master-madonna-cleaned.jpg` | Issue 54, p5 | Part IV / Kenrick |
| Trying to Make Ends Meet | `trying-to-make-ends-meet-cleaned.jpg` | Issue 55, p5 | Part II / Kenrick |
| The Official Attitude | `official-attitude-cleaned.jpg` | Issue 57, p5 | Part I / critique |

### Batch 3 — Cleaned (4)
| Name | File | Source | Essay |
|---|---|---|---|
| Wings Over Home Land | `wings-over-homeland-cleaned.jpg` | Issue 37, p9 | Part I (John Hagreen) |
| Saints Peter and Paul | `saints-peter-paul-cleaned.jpg` | Issue 38, p4 | Prologue/Epilogue |
| Industrialism/Security | `industrialism-security-cleaned.jpg` | Issue 47, p3 | Part I |
| Centrifugal Force | `centrifugal-force-cleaned.jpg` | Issue 49, p7 | Part I |
