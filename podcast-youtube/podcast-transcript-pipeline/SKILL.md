---
name: podcast-transcript-pipeline
description: "Full podcast transcript production pipeline — raw transcript to publication-ready text. 7 phases: mechanical cleanup, clip titling, polish pass, quote extraction, internal linking, episode titling, and clip selection for social. Produces transcripts at Naval podcast quality standards. Use when editing podcast transcripts, polishing interviews, preparing episodes for publishing, extracting clips for social, or building a repeatable production workflow for any podcast."
---

# Podcast Transcript Pipeline

Full production pipeline for turning raw podcast transcripts into publication-ready text. Built from the workflow that produces the Naval Ravikant podcast — adapted so any podcast can reach that standard.

The pipeline has 7 phases. Run them in order. Each phase has a defined input, output, and quality bar. Skip phases you don't need, but don't reorder them.

---

## Before You Start

You need three things:

1. **A raw transcript.** Exported from Descript, Whisper, or any transcription tool. Speaker labels help but aren't required.
2. **A proper noun list.** Names, products, companies, and technical terms that appear in this podcast. The pipeline uses this to catch mistranscriptions.
3. **A voice/style reference** (optional). If the host has a distinctive voice that should be preserved, note any stylistic preferences — do they use contractions? Sentence fragments? Specific catchphrases?

---

## Phase 1: Mechanical Cleanup

**Input:** Raw transcript
**Output:** Clean draft with clip/chapter boundaries
**Philosophy:** "Trim the fat, keep the flavor." More is gained through subtraction than addition. You are editing a transcript that must match audio. You cannot insert new words — only delete filler, adjust punctuation, and add paragraph breaks.

### Colloquialism Corrections

Always change informal contractions to their written form:

| Raw | Clean |
|-----|-------|
| gonna | going to |
| wanna | want to |
| 'cause / cause | because |
| kinda | kind of |
| gotta | got to / have to |
| lemme | let me |
| outta | out of |
| coulda / shoulda / woulda | could have / should have / would have |

Keep natural contractions (don't, can't, it's, that's, we're). Keep "And" or "But" at sentence start if it's the speaker's style. Keep intentional repetition for rhetorical effect.

### Filler Word Removal

**Remove without exception:**
- um, uh, ah — every instance
- "you know" — when meaningless filler (keep when genuinely asking)
- "I mean" — when empty qualifier
- "like" — when pure filler (keep for similes)
- "sort of" / "kind of" — when hedging, not when describing degree
- "right?" — when verbal tic, not when genuinely asking
- "so" / "well" — at sentence start when just launch words
- Exact repetitions: "the, the" → "the"
- False starts: "It's not a, and makes it" → "It makes it"
- Meta-conversation: about recording setup, "we can delete this," technical logistics

**Judgment calls:**
- "I think" — keep when genuinely qualifying; remove when verbal padding
- "basically" — keep once per passage if signaling simplification; remove excess
- "literally" / "obviously" / "actually" — keep when emphatic or contrasting; remove when tic

### Punctuation Standards

- **Em dashes:** No spaces before or after—like this. Use for asides, interruptions, clarifications.
- **Quotes:** Curly "quotes" and 'apostrophes' always. No straight quotes.
- **Commas:** Oxford comma always. After conjunctions separating independent clauses.
- **Proper nouns:** Capitalize correctly. Check against your proper noun list.
- **Numbers:** Spell out one through nine; numerals for 10+.
- **Titles:** Italicize book/movie/show titles.

### Paragraph Breaks

Create breaks at:
- Major topic shifts
- Before examples or stories
- After key conclusions (give them breathing room)
- When switching abstract ↔ concrete
- Before the speaker's "payoff" line
- When a new speaker enters

### Mistranscription Checks

Cross-reference every proper noun against your provided list. Common AI transcription errors:
- Technical terms mangled into similar-sounding words
- Names of people, companies, and products misspelled
- Domain-specific jargon replaced with common words

**Mark overdub suggestions** (where audio should be re-recorded or annotated) with: `[OVERDUB: current text → suggested text]`. Limit to 5-6 per full episode maximum.

### Output

Produce both:
1. **Working draft** with ~~strikethrough~~ for deletions and **[BOLD]** for overdub suggestions
2. **Clean version** — smooth, production-ready text

---

## Phase 2: Clip/Chapter Title Generation

**Input:** Cleaned transcript from Phase 1
**Output:** 2-3 title options per clip/chapter

### Title Style Rules

- **Title Case:** Capitalize all words except prepositions (of, at, in, the, and, to, for, but, or, nor)
- **Length:** 4-10 words (median ~6). Shorter is better.
- **No terminal punctuation.** No colons or subtitles.
- **Declarative or imperative** — not advisory ("Do X" not "You should do X")
- **Must work as a standalone maxim** — someone reading just the title should get the core idea

### Process

1. Read the full clip/chapter
2. Identify the anchor sentence — the single most quotable line
3. Check for the speaker's exact words first — can the title be a direct quote?
4. If no clean direct quote: compress the key idea into the speaker's vocabulary
5. Test standalone clarity: cover the transcript, read only the title. Does it communicate?
6. Test uniqueness: does this title distinguish this clip from every other?

### Anti-Patterns
- "How to..." titles (too advisory)
- Question titles (unless genuinely interrogative)
- Clickbait superlatives ("The Most Important Thing About...")
- Subtitle format ("Topic: A New Paradigm")
- Titles longer than 12 words
- Titles requiring context to understand
- Titles using words the speaker didn't say

---

## Phase 3: Polish Pass

**Input:** Transcript from Phase 1 with titles from Phase 2
**Output:** Diff document listing issues with line references

This is NOT editorial work. Word choice, tightening, restructuring, and creative judgment are the editor's domain. This phase catches objective, verifiable issues.

### Checklist

1. **Proper nouns** — verify every instance against canonical spelling. If a name appears multiple times, all instances must match.
2. **Capitalization** — Title Case for section headers. After colons: lowercase unless proper noun or complete sentence. No random mid-sentence capitalization.
3. **Paragraph breaks** — check for orphaned sentences, paragraphs covering two distinct topics, powerful lines buried at the end of long paragraphs.
4. **Formatting** — all book/movie titles italicized, em dashes properly formatted, curly quotes throughout, no unnecessary markdown escapes.
5. **Garbled sentences** — flag anything that doesn't parse on the page. Missing words, subject-verb disagreement that changes meaning, grammar breakdowns. Do NOT flag deliberate fragments used for emphasis.

### Output Format

```markdown
# Polish Pass Diff

## Issues Found

### 1. [Category] — [Brief Description]
**Line N:**
> ...context showing the ~~problem~~ **fix**...
[Explanation]

## Items Verified (No Issues)
- [Category]: [brief note]

## Summary
| # | Issue | Severity | Action |
|---|-------|----------|--------|
| 1 | Description | High/Medium/Low | Fix / Optional |
```

**Severity:** High = factually wrong or embarrassing. Medium = standard copyediting. Low = stylistic preference.

---

## Phase 4: Quote Extraction

**Input:** Polished transcript
**Output:** 3-5 tweetable quotes per clip/chapter

### What Makes a Good Quote

A short statement (under 280 characters) that:
- Packs a high density of ideas
- Provides enough context to stand alone
- Is the kind of insight people wish they'd thought of themselves
- Respects the reader's time

### Extraction Process

1. **Read the full clip.** Understand the arc.
2. **Identify candidate lines.** Look for: declarative thesis statements, contrast patterns ("X, not Y"), paradoxes, compressed wisdom, lines that would stop scrolling.
3. **Extract or compress.**
   - **Direct extraction:** The speaker said something already tweet-ready. Use their exact words, minor trimming only.
   - **Compression:** The idea spans 2-3 sentences. Compress into one, staying within the speaker's vocabulary.
4. **Categorize.** Assign a topic tag relevant to the podcast's domain.
5. **Add source references.** Line number or timestamp for verification.

### Output Format

```markdown
## Clip N: [Title]

**Tweet 1** (Category)
"The quote goes here."
*Source: line 45*

**Title** (Category)
"A shorter version suitable as an episode title."
*Source: line 78*
```

### Anti-Patterns
- Don't fabricate — every quote must trace to something actually said
- Don't moralize — keep the speaker's descriptive style
- Don't flatten — preserve edge and provocation
- Don't over-extract — 3-5 per clip, quality over quantity

---

## Phase 5: Internal Linking

**Input:** Final polished transcript + link reference document
**Output:** Enriched transcript with inline markdown links + changelog

### Link Hierarchy (Strict Priority)

1. **Related episodes** by the same host — link to previous episodes on the same topic
2. **Supporting social posts** — tweets, threads, or posts that elaborate on ideas mentioned
3. **People (living)** — link to active personal/professional site or primary social profile
4. **People (deceased)** — link to most authoritative resource (biography, foundation, Wikipedia)
5. **Books and works** — link to Amazon or public-domain/publisher full-text

### Rules
- First mention only — don't re-link the same target
- Don't over-link — link when it adds navigational value
- Verify URLs — dead links are worse than no links
- Don't change transcript text — links are additive only
- Respect the hierarchy — a related episode always takes priority over an external link

---

## Phase 6: Episode Titling

**Input:** All clip titles + full transcript
**Output:** 8-12 episode title candidates, ranked

### The PAH! Test

1. Would the host say this at a dinner party? If it sounds like a blog headline, it fails.
2. Does it make you curious?
3. Is it tweetable? "New episode: [TITLE]" — does that get shared?
4. Does it transcend the specific topic?
5. Is it surprising? If it's the obvious title, it's probably wrong.

### Rules
- 1-5 words ideal, 6-8 acceptable, 9+ almost never
- No "Host on X" or "Host and Guest discuss X" — never meta
- Pull from the speaker's actual words
- The title should exist somewhere in the transcript, or be a tight compression

---

## Phase 7: Clip Selection for Social

**Input:** Polished transcript with timestamps
**Output:** Clip sheet with selection guides for each clip

### Selection Criteria

- **Length:** 2:30 to 4:30 (sweet spot ~3:00-3:30)
- **Speaker:** Predominantly the host. Include a guest setup line only if essential to the argument.
- **Boundaries:** Contiguous audio only — no internal cuts.
- **Start:** Begin at the core argument. Drop setup, throat-clearing, warm-up sentences.
- **End:** Stop on a payoff line — the last punchy sentence before a topic shift or weaker restatement.
- **Content:** Thesis over examples. One idea per clip. Favor universal over specific.

### Output Format

```markdown
## Clip N: [Title]

**Source chapter:** [Chapter Title]
**Timestamps:** [Start] → [End]
**Duration:** ~[N] seconds

### Selection Guide
> Start after: "[words just before clip]"
> First words: "[first 5-8 words]"
> Last words: "[last 5-8 words]"
> Stop before: "[words just after clip]"

### Caption
[Title]. "[Opening quote ~200-250 chars]"

### Transcript
[Full text of the clip]
```

### Posting Strategy
1. Lead with the most provocative or timely clip
2. Space 4-6 days apart
3. Alternate philosophical and practical
4. Save the warmest clip for last
5. Total: 5-8 clips per episode

---

## Quality Bar

**Imagine this transcript as a chapter in a published book sitting in an airport bookstore.** Every proper noun spelled correctly, every title italicized, every paragraph break intentional. That's the bar.

### Final Checklist
- [ ] All colloquialisms fixed
- [ ] All filler words removed
- [ ] Punctuation consistent throughout
- [ ] No straight quotes remaining
- [ ] Em dashes properly formatted
- [ ] Paragraph breaks enhance readability
- [ ] Speaker's natural voice preserved
- [ ] No mistranscriptions
- [ ] Speaker names properly attributed
