---
name: archive-decomposer
description: Decompose a content archive (podcast transcripts, course material, interview corpus) into buildable Claude Code skills. The key insight — the highest-value skills are interactive decision-making frameworks that a user applies to their own situation, NOT production tools that process the archive itself. Use when you have a large transcript corpus and want to find every teachable methodology embedded in it.
---

# Archive Decomposer

Break a content archive into its component skills — the repeatable decision-making frameworks, step-by-step processes, and operational methodologies that are embedded in conversations but never extracted into standalone tools.

## The Core Insight (Learned the Hard Way)

There are TWO categories of skills you can extract from a content archive. Most people only see the first. The second is where the real value lives.

### Category 1: Production Skills (Lower Value)

Skills where Claude processes the archive itself — content repurposing, search, mining, summarization.

Examples: "Find clip-worthy moments", "Turn a segment into a Twitter thread", "Generate show notes from a transcript"

These are useful but they're commodities. Any AI can summarize. The archive is the input being processed.

### Category 2: Decision-Making Skills (Higher Value)

Skills where the archive's *methodology* becomes an interactive coaching tool. A founder sits down with Claude and says "I'm thinking about X" — Claude walks them through a framework that a guest or host *actually taught* on the show, pulling from the source transcripts as evidence.

Examples:
- "I have a business idea — vet it" → Claude runs the idea through Imad's Thiel test, Hormozi's Value Equation, Sam's unit economics math, and Shaan's North Star formula
- "I want to buy a small business" → Claude walks through Sarah Moore's 7-step acquisition process with Beshore's people diligence and Wilkinson's delegation framework
- "I got an offer to buy my company" → Claude coaches the negotiation using Sam and Shaan's own exit mistakes and rules

**Why Category 2 is more valuable:**
- The archive becomes a KNOWLEDGE BASE for coaching, not a thing being processed
- Users can't get this from ChatGPT — it requires the specific methodology from specific episodes
- It's the reason someone would clone the repo and open it in Claude Code
- Each skill is a differentiated product, not a generic AI feature

### The Test

Before scoring any skill candidate, ask: **"Is this Claude processing the archive, or is this Claude coaching the user using wisdom FROM the archive?"**

If processing → Category 1 (still valid, but lower priority)
If coaching → Category 2 (build these first)

---

## What to Look For

### Signal 1: Named Frameworks

A guest or host gives a methodology a NAME or presents it as a numbered system.

**Search patterns:**
```
grep -ri "framework\|mental model\|equation\|formula" transcripts/
grep -ri "step one\|step 1\|first step\|three steps\|five steps" transcripts/
grep -ri "playbook\|blueprint\|system\|method" transcripts/
grep -ri "rule of\|rules for\|the key is\|the secret is" transcripts/
```

**What makes it a skill:** The framework has defined inputs (user's situation), clear steps (a sequence to follow), and actionable output (a decision, plan, or assessment).

**Example from MFM:** Hormozi's Value Equation — `Value = (Dream Outcome × Perceived Likelihood) / (Time Delay × Effort)` — is a named framework with 4 inputs that produces a score. Directly skillable.

### Signal 2: Step-by-Step Processes

Someone walks through HOW they did something in a specific, ordered sequence. Not "here's what I think about X" but "here's exactly what I did, in order."

**Search patterns:**
```
grep -ri "here's how\|here's what I do\|what I did was" transcripts/
grep -ri "first.*then.*finally\|step by step" transcripts/
grep -ri "the process\|my process\|our process" transcripts/
```

**What makes it a skill:** The steps are transferable — another founder could follow the same sequence with different inputs and get a useful result.

### Signal 3: Cautionary Frameworks (What NOT to Do)

Explicit admissions of error that contain extractable rules.

**Search patterns:**
```
grep -ri "I was wrong\|my mistake was\|what I got wrong" transcripts/
grep -ri "don't.*never\|avoid\|the worst thing" transcripts/
grep -ri "I wish I had\|if I could do it over\|looking back" transcripts/
grep -ri "regret\|learned the hard way" transcripts/
```

**What makes it a skill:** The mistake + lesson becomes a checklist item or decision rule.

### Signal 4: Decision Heuristics

Simple rules of thumb that compress complex decisions into actionable tests.

**Search patterns:**
```
grep -ri "rule of thumb\|heuristic\|my test is\|I always" transcripts/
grep -ri "if.*then\|whenever I\|the way I decide" transcripts/
grep -ri "no-brainer\|the trick\|shortcut" transcripts/
```

### Signal 5: Interactive Exercises

Moments where a host or guest describes something they do WITH another person — a conversation structure, a worksheet, a diagnostic.

**Search patterns:**
```
grep -ri "I ask them\|I would ask\|the question I ask" transcripts/
grep -ri "sit down and\|walk through\|we mapped out" transcripts/
grep -ri "exercise\|worksheet\|scorecard\|audit" transcripts/
```

### Signal 6: Guest Expertise Operationalized

A guest who is a genuine expert in a domain lays out their methodology in enough detail that it's repeatable.

---

## The 5-Test Filter (Score Before Building)

Before scoring I×S×T, run every framework candidate through the 5-test skill-worthiness filter. This determines what FORMAT to build, not whether to build at all.

### The 5 Tests (KDP Kings = Gold Standard)

| Test | What it measures | Example |
|------|-----------------|---------|
| **1. Concrete Input** | Does the user bring something specific? | A keyword, a manuscript, a business idea |
| **2. Structured Deliverable** | Does it produce a template output? | Pricing card, niche report, launch timeline |
| **3. Source-Specific Knowledge** (REQUIRED) | Does it contain specifics an LLM wouldn't know? | BSR thresholds, Dead Zone math, ghost categories |
| **4. Ordered Workflow** | Are steps ordered with dependencies? | Step 2 depends on Step 1's output |
| **5. Less-Wrong Decisions** | Does it make better choices than generic LLM? | Countdown Deal loophole, category validation |

### How Tests Map to Build Type

| Passes | → Build as | Example |
|--------|-----------|---------|
| All 5 | **Decision Skill** (gold standard) | KDP niche-scout, pricing-strategist |
| 1 + 3 (input + source knowledge) | **Tutor Skill** (teach → apply → teach) | Huberman dopamine-masterclass, Lenny retention-workshop |
| 3 + some of 1/2 | **Lightweight Coaching Skill** (questions → framework → output) | Scott Adams reframe-engine, systems-designer |
| 3 only (source knowledge) | **Framework Article** (reference doc) | Named frameworks, mental models, specific protocols |
| None | **Skip** — generic content the LLM already knows | |

**Test 3 is the only hard gate.** If the LLM already knows it, don't build anything. Everything else determines format.

---

## I×S×T Scoring (After 5-Test Classification)

For candidates that pass Test 3, score to determine build priority:

| Dimension | Question | Score |
|-----------|----------|-------|
| **Interactivity** | Can Claude run this as a back-and-forth coaching session? | 1-5 |
| **Specificity** | Are there concrete steps, numbers, templates, or rules — not just general advice? | 1-5 |
| **Transferability** | Does this work for different users with different inputs? | 1-5 |
| **Source Density** | How many episodes/guests contribute methodology to this skill? | 1-5 |

**Interactivity × Specificity × Transferability = Build Priority**

Source Density is a bonus multiplier: if 3+ episodes contribute frameworks to the same skill, it's a composite skill — higher value, more defensible.

**Build Priority 50+:** Build immediately — these are the flagship skills.
**Build Priority 25-49:** Build when the archive is published.
**Below 25:** Probably a reference doc, not a skill.

---

## Decomposition Workflow

### Phase 1: Signal Survey (Automated)

Run all the grep patterns across the full transcript archive. Don't read individual transcripts yet — just collect counts and identify which files light up across multiple signal types.

**Output:** A heat map of transcripts ranked by signal density. The top 20-30 transcripts are your primary sources.

### Phase 2: Deep Read (Targeted)

Read the top signal-dense transcripts in full. For each, extract:

```markdown
### [Framework/Process Name]
- **Speaker:** Who taught this
- **Episode:** filename + title
- **Type:** Named framework / Step-by-step / Cautionary / Heuristic / Exercise / Expert method
- **The methodology:** Summarize the actual steps or rules
- **Inputs required:** What does the user need to bring?
- **Output produced:** What does the user walk away with?
- **Composable with:** Other frameworks from other episodes that address the same domain
```

### Phase 3: Compose Skills

The best skills are composites — they stack 2-5 frameworks from different episodes into one coherent workflow. This is where the archive's value becomes greater than any single episode.

### Phase 4: Write the Skill File

Each skill file should contain:
1. **When to Use** — trigger phrases
2. **The framework, in order** — each step with the source quote and transcript reference
3. **Interactive prompts** — what to ask the user at each stage
4. **Archive search commands** — grep patterns to find additional relevant episodes
5. **Output template** — what the user gets at the end

### Phase 5: Update the CLAUDE.md

Add each skill to the repo's CLAUDE.md with:
- One-line description
- Source guests
- Example trigger phrases

---

## Category 1 Skills (Production — Build Second)

These are still valid, just lower priority. When building them, the approach is different: you need EXAMPLES of the creator's actual output, not just the methodology.

| Skill Type | What's Needed |
|-----------|--------------|
| Clip finder | Examples of clips that performed well + what made them clip-worthy |
| Thread writer | Actual threads from the host as style templates |
| Show notes generator | The show's actual format as a template |
| Content repurposer | Examples of how segments became social posts |

The key: Category 1 skills are built from OUTPUT EXAMPLES. Category 2 skills are built from INPUT METHODOLOGY. Different source material, different extraction approach.

---

## Proven Results

Skills already built from MFM using this methodology:

| Skill | Composite Sources | Category |
|-------|------------------|----------|
| idea-vetter | 5 episodes (Imad, Hormozi, Sam, Shaan, Brett Adcock) | Decision-making |
| acquisition-evaluator | 4 episodes (Sarah Moore, Beshore, Wilkinson, Codie Sanchez) | Decision-making |
| exit-coach | 3 episodes (Sam, Shaan, Wilkinson) | Decision-making |
| pricing-optimizer | 3 episodes (Patrick Campbell, Sam, Shaan) | Decision-making |
| cold-outreach | 3 episodes (Sam, Sarah Moore, Shaan) | Decision-making |
| hiring-framework | 4 episodes (Hormozi, Wilkinson, Beshore, Blake) | Decision-making |

---

*Decompose the methodology, not the content. The archive is the knowledge base, not the product. The skills are the product.*
