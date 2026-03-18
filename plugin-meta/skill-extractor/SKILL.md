---
name: skill-extractor
description: Extract actionable Claude Code skills from raw source material — transcripts, conversations, workflows, expertise dumps. This skill identifies repeatable, promptable workflows embedded in content and scores them by leverage. Use when processing a corpus (podcast transcripts, blog posts, course material) to discover what skills could be built from it.
---

# Skill Extractor

Turn raw source material into a list of buildable Claude Code skills. Not a knowledge base — skills are *workflows Claude can execute*, not facts Claude should know.

## The Core Distinction

**Skill** = a repeatable workflow with inputs, steps, and outputs that Claude executes inside a coding environment. Writing a YouTube script. Running an SEO audit. Drafting a newsletter. Creating ad copy.

**Not a skill** = static knowledge, reference material, domain expertise. How to raise meat birds. The history of fasting. Nutritional science. These become wiki articles, books, or reference docs — not skills.

**The test:** Can Claude *do* this thing, repeatedly, with different inputs, and produce a useful output? If yes → skill. If it's something Claude *knows* and references → not a skill.

---

## The 5-Test Skill-Worthiness Heuristic

The KDP Kings plugin is the gold standard — every skill has clear input → structured deliverable → source-specific knowledge. Score each candidate against these 5 tests. Test 3 (source knowledge) is the only hard requirement — if the LLM already knows it, don't bother. The other tests determine the FORMAT.

### Test 1: Concrete Input
Does the user bring something specific? A keyword, a manuscript, a publish date — not "I want advice about publishing."

### Test 2: Structured Deliverable
Does it produce a template output? A pricing card, launch timeline, niche report, listing package. The user walks away with an artifact, not a conversation.

### Test 3: Source-Specific Knowledge (REQUIRED)
Does it contain numbers, thresholds, or platform rules mined from the source that an LLM wouldn't know? Examples from KDP:
- BSR thresholds: <5,000 too competitive, 10K-30K sweet spot, <100K minimum viable
- The Dead Zone: $10.00-$19.98 earns LESS than $9.99 (royalty bracket math)
- 54% of KDP categories are duplicates, 27% are ghosts
- Health claims ("heal", "cure") block Amazon Ads entirely

### Test 4: Ordered Workflow
Are the steps ordered with dependencies? Pricing Step 2 (Dead Zone check) depends on Step 1 (royalty tier identification). Launch Phase 3 (99-cent period) depends on Phase 2 (free promo collecting reviews).

### Test 5: "Less Wrong" Decisions
At decision points, does the skill make better choices than a generic model? The listing-optimizer knows to check for ghost categories before selecting. The pricing-strategist knows the Countdown Deal loophole (preserves 70% royalty at $0.99).

---

## How the Tests Map to Content Types

A good plugin has a MIX of these. The 5 tests don't gate things out — they classify what to build:

| Passes | → Build as | Example |
|--------|-----------|---------|
| All 5 | **Decision Skill** (gold standard) | KDP niche-scout, pricing-strategist |
| 1 + 3 (input + source knowledge) | **Tutor Skill** (teach → apply → teach) | Huberman dopamine-masterclass, Lenny retention-workshop |
| 3 + some of 1/2 | **Lightweight Coaching Skill** (ask questions → apply framework → output) | Scott Adams reframe-engine, systems-designer |
| 3 only (source knowledge) | **Framework Article** (reference doc) | Named frameworks, mental models, specific protocols |
| None | **Skip** — generic content the LLM already knows | |

### Plugin composition target:
- 5-7 Decision Skills (the KDP-quality workflows)
- 2-4 Tutor Skills (interactive learning experiences)
- 1-3 Lightweight Coaching Skills (framework application)
- 15-60+ Framework Articles (reference docs, named frameworks, mental models)
- 1 Router/Concierge (dispatches to the right skill)

---

## Legacy Taxonomy (Still Useful for Discovery)

These 6 hallmarks help you FIND candidates. The 5-test filter above determines what you BUILD.

### 1. Repeated SOP / Workflow
Something done regularly as part of a content or business process.

### 2. Disposable One-Shot
Valuable but infrequent. Done once per project or client.

### 3. Specific Knowledge Applied as Process
Domain expertise distilled into a repeatable method.

### 4. Step-by-Step Process
A clear sequence where order matters.

### 5. Example-Driven
Skills where 3-5 concrete examples dramatically improve output quality.

### 6. Tool-Augmented
Skills that benefit from MCP servers, API calls, CLI tools, or other integrations.

---

## Available Tool Ecosystem

When evaluating whether a skill candidate is tool-augmented, consider what's currently available:

**MCP Servers (live in this workspace):**
- Slack (channels, messages, search)
- Google Drive (docs, sheets, slides, folders)
- Google Calendar (events, scheduling, freebusy)
- Apify (web scraping actors — YouTube, Twitter, any site)
- Notion (pages, databases, search)
- Video-audio (trim, convert, subtitles, overlays, concatenate)
- Context7 (library documentation lookup)

**CLI Tools:**
- ffmpeg (video/audio processing)
- yt-dlp (YouTube downloading)
- Whisper (transcription)
- qmd (local markdown search / RAG)
- gh (GitHub CLI)
- Bun/Node (JS execution)
- Python (scripting, data processing)

**APIs (via scripts):**
- DataForSEO (keyword research, SERP, rankings)
- Gemini (deep research, image generation, large-context writing)
- ElevenLabs (voice cloning)
- HubSpot (email marketing)
- Webflow (CMS publishing)

When a source mentions a workflow that *could* be automated with these tools but the creator does it manually, that's a high-value skill candidate.

---

## Extraction Workflow

### Phase 1: Ingest and Scan

**Input:** Raw source material — transcripts, blog posts, course outlines, conversation logs, wiki chunks.

Read the material. Identify skill candidates based on pattern recognition from existing skills in this workspace. For each candidate:

```markdown
### [Candidate Name]
- **What it does:** One sentence
- **Source:** Where in the material this was found
- **Hallmarks:** Which taxonomy items (1-6) it exhibits
- **Input → Output:** What goes in, what comes out
- **Frequency:** daily / weekly / per-project / one-time
```

### Phase 2: Score and Rank

| Dimension | Question | Score |
|-----------|----------|-------|
| **Leverage** | How much time/effort does this save per use? | 1-5 |
| **Frequency** | How often would this be used? | 1-5 |
| **Promptability** | How well can Claude execute this with a skill file? | 1-5 |

**Leverage × Frequency × Promptability = Extraction Priority**

High-priority (50+): build immediately. Medium (25-49): build when needed. Low (<25): note or discard.

### Phase 3: Spec the Winners

For each high-priority candidate, draft a skill spec for the skill-creator:

```markdown
## Skill Spec: [name]

**Purpose:** What this skill accomplishes
**Trigger:** What would the user say to invoke this?
**Not for:** What this skill should NOT be used for

**Input → Output**
**Workflow:** [numbered steps]
**Bundled Resources:** scripts, references, assets needed
**Tool Dependencies:** MCPs, APIs, CLI tools required
**Examples Needed:** What examples would make this work well?
**Source Attribution:** Where this was extracted from
```

### Phase 4: Present to User

1. Top 5 high-priority skills with full specs
2. Medium-priority as one-liners
3. Non-skill material routed elsewhere

Ask: "Which should I build first?"

---

## Routing Non-Skills

| Type | Destination |
|------|-------------|
| Domain knowledge / facts | Wiki article or reference doc |
| Opinion / philosophy | Blog post or book chapter |
| Personal story / anecdote | Narrative snippet for content |
| Tool recommendation | Relevant project's CLAUDE.md |
| Business strategy | Strategy doc or CIA-OFFER.md |

---

## Test Corpora

Already chunked and indexed in wiki-projects:
- **Kallaway** — 66 chunks, framework-dense → should yield many skills
- **Jenny Hoyos** — 60 chunks, short-form methodology → should yield skills
- **Colin & Samir** — 119 chunks, strategy + interviews → mixed

---

## Related Skills

- **skill-creator** — Takes a spec and builds the full skill. Extractor feeds into creator.
- **voice-analyzer** / **voice-wizard** — Specialized extractors for voice/style skills.
- **anti-ai-writing** — Example of a well-built skill.
- **book-chapter-writer** — Example of a complex multi-phase workflow skill.

---

*Extract the workflow, not the knowledge. If Claude can DO it repeatedly with different inputs, it's a skill. If Claude can only KNOW it, it's a reference doc.*
