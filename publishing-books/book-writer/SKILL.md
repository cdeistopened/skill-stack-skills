---
name: book-writer
description: Sequential book production pipeline using Claude sub-agents. Enforces orthogonality (no repeated stories/ideas across chapters), quality gates, and voice consistency. Replaces gemini-writer for book projects. Use when drafting or rewriting book manuscripts.
---

# Book Writer — Sequential Production Pipeline

Produces book manuscripts through a multi-phase pipeline that enforces orthogonality, quality, and voice consistency. Each chapter is drafted sequentially with full awareness of all prior chapters, preventing redundancy.

## When to Use

- Drafting a new book from outline + source material
- Rewriting an existing manuscript with quality enforcement
- Any multi-chapter project requiring cross-chapter coordination

## Architecture

```
PHASE 0: STRUCTURAL PLAN (single agent, full context)
    ├── Content audit — what material exists, what's strong
    ├── Orthogonality map — each idea lives in ONE chapter only
    ├── Hook catalog — unique angle per chapter
    ├── Threading map — recurring motifs: intro → reference → resolve
    └── Chapter-by-chapter execution notes

PHASE 1: CHAPTER BRIEFS (single agent)
    ├── Self-contained brief per chapter (~8-12K tokens each)
    ├── Includes: assigned blocks, forbidden blocks, voice card, anti-AI card
    └── Hook approved before drafting begins

PHASE 2: SEQUENTIAL DRAFTING (sub-agents, one at a time)
    ├── Each agent sees: brief + ALL previously-written chapters
    ├── Accumulating context prevents redundancy
    ├── Quality loop runs after each chapter (blocking)
    └── Failed chapters get rewritten before pipeline advances

PHASE 3: ASSEMBLY REVIEW (single agent, full manuscript)
    ├── Read all chapters sequentially
    ├── Bridge document (chapter-to-chapter transitions)
    ├── Redundancy report (anything that slipped through)
    └── Voice consistency check
```

## Phase 0: Structural Plan

The most important phase. This is where orthogonality is designed, not enforced after the fact.

### Required Inputs
- Book outline with chapter descriptions
- All source material (blocks, transcripts, quotes, research)
- Voice guide or voice card
- Anti-AI rules

### Structural Plan Contents

**1. Content Inventory**
For each piece of source material, decide:
- Which chapter OWNS it (told in full, PRIMARY)
- Which chapters may REFERENCE it (one-sentence callback, max 2)
- Which chapters it's FORBIDDEN from (must not appear even in passing)

**2. Orthogonality Matrix**
Table showing every story, framework, quote, and evidence block mapped to exactly one chapter. The one-primary rule: if a story appears in full in Ch 4, it cannot appear in full in any other chapter.

**3. Hook Catalog**
Each chapter gets a structurally different hook approach:
- Personal anecdote opening
- Startling statistic
- Counterintuitive claim
- Scene-setting (time, place, sensory detail)
- Question that creates tension
- Quote that challenges assumptions

Track which approach is used per chapter — no two adjacent chapters should use the same hook type.

**4. Threading Map**
For recurring motifs that span multiple chapters:
- Chapter where INTRODUCED (full treatment)
- Chapters where REFERENCED (brief callback: "as we saw in Chapter N...")
- Chapter where RESOLVED (payoff)

**5. Chapter Execution Notes**
For each chapter, specific instructions:
- Word target
- Tone/energy (opening energy vs. closing energy)
- What the reader should FEEL at the end
- Bridge to next chapter (last paragraph sets up the next)
- Specific blocks to use and how

## Phase 1: Chapter Briefs

Each brief is a self-contained document that gives a sub-agent everything it needs:

```markdown
# Brief: Chapter N — [Title]

## Position
- Previous chapter ends with: [last paragraph summary]
- Next chapter opens with: [first paragraph summary]

## Goal
[1-2 sentences: what this chapter accomplishes]

## Word Target
[X,XXX - X,XXX words]

## Hook
[Approved hook with opening line]

## PRIMARY Blocks (use in full)
[Full text of assigned blocks]

## REFERENCE ONLY (one-sentence callback)
[Block ID — one-line summary, chapter where told in full]

## FORBIDDEN (do not mention)
[Block IDs that belong to other chapters]

## Voice Card
[Condensed voice rules]

## Anti-AI Card
[Kill list + patterns to avoid]

## Structure
Use the Lisec 5-part pattern:
1. Story Part I (hook, end on tension)
2. The Point (why this matters to the reader)
3. The Step (the methodology/technique/insight)
4. The Action (something to do TODAY)
5. Story Part II (resolution, transformation)
```

## Phase 2: Sequential Drafting

**Critical**: Chapters are drafted ONE AT A TIME, in order. Each sub-agent receives:
1. Its chapter brief
2. ALL previously-written chapters (accumulating context)
3. The structural plan

The prompt to each sub-agent includes:

```
You are writing Chapter N of [Book Title].

CRITICAL RULES:
- Follow your brief exactly
- Do NOT repeat any idea, story, quote, or anecdote from the
  previously-written chapters below
- If you need to reference something from a prior chapter,
  use a brief callback ("as we explored in Chapter N...")
- Use ONLY the blocks assigned to you in the brief
- Do NOT use any FORBIDDEN blocks
- Match the voice card exactly
- Zero tolerance for AI tells (see Anti-AI card)
- Output the complete chapter as markdown
```

### Quality Gate (After Each Chapter)

Run the book-quality-loop (5 judges) before advancing:
1. **Human Detector** — Zero AI tells
2. **Accuracy Checker** — All claims sourced from blocks
3. **Voice Judge** — Matches voice card
4. **Redundancy Judge** — Nothing repeated from prior chapters
5. **Reader Advocate** — Engaging, proper structure

If ANY blocking judge fails → rewrite and re-check before moving to next chapter.

## Phase 3: Assembly Review

Single agent reads the full manuscript sequentially:
- Bridge quality (do chapters flow into each other?)
- Redundancy report (did anything slip through?)
- Voice consistency (does chapter 10 sound like chapter 1?)
- Fact-check (do all citations match source material?)
- Word count per chapter
- Overall pacing assessment

## Running the Pipeline

### Option A: Manual (recommended for first book)

```bash
# Phase 0 — you run this in conversation with Claude
# Share outline + source material, ask for structural plan

# Phase 1 — generate briefs from the plan
# One brief per chapter, saved to briefs/

# Phase 2 — sequential drafting
# Launch one sub-agent per chapter, share accumulating context
# Run quality loop after each

# Phase 3 — assembly review
# Share full manuscript, ask for review
```

### Option B: Script (for subsequent books)

```bash
python3 .claude/skills/book-writer/scripts/book-writer.py \
  --outline outline.md \
  --sources blocks/ \
  --voice voice-card.md \
  --anti-ai anti-ai-card.md \
  --output chapters/ \
  --sequential
```

## Lessons from Big and Fat (What NOT to Do)

1. **Never draft chapters in parallel** — sub-agents with isolated briefs produce redundant content
2. **Never skip the structural plan** — orthogonality must be designed, not fixed after
3. **Never dump the full corpus into a brief** — extract blocks first, give only relevant blocks
4. **Never skip the quality gate** — every chapter must pass before the next one starts
5. **Never use a voice card without samples** — include 3-5 paragraphs of the author's BEST writing
6. **Never tell the same story twice** — the one-primary rule is sacred
