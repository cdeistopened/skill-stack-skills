---
name: book-quality-loop
description: 5-judge quality gate for book chapters. Blocks publication until Human Detector, Accuracy, Voice, Redundancy, and Reader judges all pass. Adapted from OpenEd quality-loop for book production.
---

# Book Quality Loop

5-judge quality gate for book chapters. Every chapter must pass ALL blocking judges before the pipeline advances to the next chapter.

## Judges

### Judge 1: Human Detector (BLOCKING)

Zero tolerance for AI tells.

**Hard blocks — auto-reject if ANY found:**
- [ ] Correlative constructions ("X isn't just Y - it's Z", "It's not about X, it's about Y")
- [ ] Dramatic contrast reveals ("Not X. Y." as fragment pattern)
- [ ] Banned words: delve, comprehensive, crucial, leverage, landscape, navigate, foster, facilitate, realm, paradigm, embark, journey, tapestry, myriad, multifaceted, seamless, cutting-edge, transformative, pivotal, profound
- [ ] Banned phrases: "The best part?", "Here's the thing", "Let that sink in", "Now more than ever", "In today's fast-paced"
- [ ] Staccato patterns: "No X. No Y. Just Z."
- [ ] Triple adjective stacks: "Bold, beautiful, brilliant"
- [ ] Hedge stacks: might, could, perhaps, possibly (more than 1 per chapter)
- [ ] Throat-clearing openers: "Before we dive in...", "In order to understand..."
- [ ] Manufactured urgency: "Here's the part that should keep you up at night"
- [ ] Post-quote explanation (summarizing what was just quoted)
- [ ] Scaffolding sentences ("Before you understand X, you need to know Y")

**VERDICT:** PASS only if zero AI tells found.

---

### Judge 2: Accuracy Checker (BLOCKING)

Every factual claim must trace to source material.

- [ ] All stories match source blocks (names, dates, details)
- [ ] All statistics cite their source
- [ ] All quotes are verbatim from source material
- [ ] No claims presented as fact that aren't in the blocks
- [ ] No hallucinated anecdotes or studies
- [ ] Timeline events in correct order

**VERDICT:** PASS only if all facts verified against provided blocks.

---

### Judge 3: Voice Judge (BLOCKING)

Does this sound like the author, not like an AI writing about the author?

**Check against voice card:**
- [ ] Signature phrases used naturally (not forced)
- [ ] Sentence rhythm matches voice card samples
- [ ] Tone appropriate for subject matter
- [ ] First-person perspective consistent
- [ ] Conversational register (not academic, not clinical)
- [ ] Author's actual vocabulary (not elevated/literary unless that's the voice)

**The test:** If you removed the byline, would a reader who knows the author recognize the voice?

**VERDICT:** PASS only if voice is authentic.

---

### Judge 4: Redundancy Judge (BLOCKING)

Nothing repeated from prior chapters.

- [ ] No story told in full that was told in full in a prior chapter
- [ ] No framework explained that was already explained
- [ ] No quote used that was already used (exact or near-duplicate)
- [ ] No statistic cited that was already cited with the same context
- [ ] References to prior chapters use callbacks ("as we saw..."), not retelling
- [ ] Catchphrases appear no more than 2x total across manuscript

**VERDICT:** PASS only if zero redundancy found.

---

### Judge 5: Reader Advocate (BLOCKING)

Is this chapter worth reading?

- [ ] Hook creates genuine curiosity (not generic)
- [ ] Structure follows Lisec 5-part or equivalent (story → point → step → action → resolution)
- [ ] Each section earns its place (no padding)
- [ ] Specific examples and sensory details (not abstractions)
- [ ] Reader knows what to DO after reading (action item)
- [ ] Ending bridges naturally to next chapter
- [ ] Word count within target range
- [ ] Pacing varies (not monotone energy throughout)

**VERDICT:** PASS only if engaging throughout.

---

## Process

```
DRAFT CHAPTER
    ↓
JUDGE 1: Human Detector ──→ FAIL → Fix AI tells → Re-run Judge 1
    ↓ PASS
JUDGE 2: Accuracy ──→ FAIL → Fix facts → Re-run Judge 2
    ↓ PASS
JUDGE 3: Voice ──→ FAIL → Rewrite for voice → Re-run Judge 3
    ↓ PASS
JUDGE 4: Redundancy ──→ FAIL → Cut redundancy → Re-run Judge 4
    ↓ PASS
JUDGE 5: Reader ──→ FAIL → Improve engagement → Re-run Judge 5
    ↓ PASS
ADVANCE TO NEXT CHAPTER
```

## Output Format

After running all judges, produce a verdict card:

```markdown
## Quality Verdict: Chapter N — [Title]

| Judge | Verdict | Issues |
|-------|---------|--------|
| Human Detector | PASS/FAIL | [specific issues] |
| Accuracy | PASS/FAIL | [specific issues] |
| Voice | PASS/FAIL | [specific issues] |
| Redundancy | PASS/FAIL | [specific issues] |
| Reader | PASS/FAIL | [specific issues] |

**Overall: PASS / BLOCKED**
**Blocking issues:** [list]
```
