---
name: plugin-builder
description: "Build a Claude Code plugin from a content archive (podcast transcripts, course material, book chapters). Produces interactive decision skills, tutor skills, framework articles, indexes, and a concierge router — the full 'Ask [Creator]' experience. Use when you have a transcript corpus and want to turn it into an installable plugin, when someone says 'build a plugin from these transcripts,' 'create an ask-[name] plugin,' or 'turn this archive into a coaching tool.' Also use when improving an existing plugin — adding skills, writing framework articles, or fixing index integrity."
---

# Plugin Builder

Turn a content archive into an installable Claude Code plugin. The plugin becomes an interactive coaching tool — users ask questions, get routed to the right skill or framework, and receive specific, source-cited guidance.

This skill covers the full pipeline from corpus to installable plugin. For the decomposition/discovery phase, it references the `archive-decomposer` (skill-extractor) skill. Everything after discovery — scaffolding, skill writing, article writing, index building, router wiring, quality checks — lives here.

## What a Plugin Contains

Every plugin produces the same artifact types. This pattern is proven across 5 builds (Lenny/303, KDP Kings/175, Scott Adams/389, Huberman/137, Zakery):

```
plugin/
├── .claude-plugin/
│   └── plugin.json              # Name, description, version, author
├── CLAUDE.md                    # End-user documentation (quick start, skill list, examples)
├── INSTALL.md                   # Installation guide
├── skills/
│   ├── ask-[creator]/SKILL.md   # Concierge router (1 per plugin)
│   ├── [decision-skill]/SKILL.md # 5-10 decision skills
│   └── [tutor-skill]/SKILL.md   # 2-4 tutor skills (NEVER skip these)
├── references/
│   ├── frameworks/              # 30-60 framework articles
│   ├── indexes/                 # 2-4 index files (by-topic + domain-specific)
│   └── decomposition-*.md       # Preserved decomposition files (source of truth)
└── transcripts/                 # Symlink to polished transcript directory
```

## The Five Phases

### Phase 1: Decompose (use archive-decomposer skill)

Read `.claude/skills/skill-extractor/SKILL.md` and follow its process. **Before building anything, run every framework through the 5-test skill-worthiness filter** (documented in both skill-extractor and archive-decomposer). Test 3 (source-specific knowledge) is the only hard gate — if an LLM already knows it, skip it. The other tests determine FORMAT: Decision Skill (all 5), Tutor Skill (1+3), Coaching Skill (3+partial), or Framework Article (3 only).

The key outputs:

1. **Domain decomposition files** — One per domain, ~40-60KB each. These are the most valuable intermediate artifact. ALWAYS save them to `plugin/references/decomposition-*.md`.

2. **Master Catalog** — Every framework scored I×S×T (Interactivity × Specificity × Transferability). This is the filter that determines what becomes a skill vs. article vs. nothing.

The number of domains depends on the archive. Patterns from completed builds:

| Archive | Domains |
|---------|---------|
| Lenny (product management) | Growth, Product, Metrics, Team, GTM |
| KDP Kings (self-publishing) | Research, Creation, Listing, Publishing, Pricing, Launch, Marketing |
| Huberman (health/science) | Sleep & Circadian, Exercise, Neurochemistry, Stress, Nutrition |

Run domain decomposers as parallel agents — one per domain. Each agent reads all transcripts relevant to its domain and extracts every protocol, framework, methodology, and specific number.

**Critical: Save the decomposition output.** Lenny's build ran the agents but didn't save the intermediate files. Huberman's did, and those 5 files (~50KB each) became the source of truth for everything downstream. Every framework article and skill references them.

### Phase 2: Scaffold

Create the directory structure and configuration files.

**plugin.json:**
```json
{
  "name": "ask-[creator]",
  "description": "[N] episodes of [Source] turned into an interactive [domain] coach. [X] skills, [Y]+ framework guides, and [N] searchable transcripts.",
  "version": "1.0.0",
  "author": {
    "name": "Creative Intelligence Agency"
  }
}
```

**CLAUDE.md** (end-user documentation):
- Quick Start section with 5-6 example questions
- Skill list organized by type (Decision / Tutor / Utility)
- "What's Inside" section (skills count, framework count, transcript count)
- Progressive disclosure explanation (ask → go deeper → go deepest)
- Domain-specific examples showing the specificity the plugin provides (see Huberman's dosage comparison table as the gold standard)
- Disclaimer appropriate to the domain

**INSTALL.md:**
- Prerequisites (Claude Code installed)
- Plugin installation steps
- First question to try
- Troubleshooting

**Symlink transcripts:**
```bash
ln -s ../data/[source]/polished plugin/transcripts
```

### Phase 3: Build Skills

Skills come from the Master Catalog. Tier 1 frameworks (I×S×T ≥ 50) become decision or tutor skills. The distinction:

#### Decision Skills (5-10 per plugin)

The user brings their situation, the skill diagnoses and prescribes.

**Pattern:** Consultation → Diagnosis → Prescription → Deliverable

**Structure (~150-300 lines):**
```markdown
---
name: [skill-name]
description: "[Pushy trigger description — what it does + when to use it + example phrases]"
---

# [Skill Name]

[One sentence: what you do for the user]

## The Consultation

### Step 1: [Understand/Audit/Assess]
Ask these diagnostic questions:
1. [Question about their situation]
2. [Question about their constraints]
3. [Question about their goals]

### Step 2: [Diagnose/Map/Evaluate]
Map their answers to the framework:
[Framework tables, decision trees, or scoring rubrics with specific numbers from the archive]

### Step 3: [Prescribe/Build/Design]
Based on diagnosis, build their specific protocol:
[Conditional prescriptions — "If X, then Y with Z dosage/timing/parameters"]

## Output
[Markdown template for the structured deliverable they receive]

## Source Transcripts
[Episode filenames]

## Disclaimer
[Domain-appropriate disclaimer]
```

**Gold standard examples:**
- `huberman-wiki/plugin/skills/morning-routine-designer/SKILL.md` — 6 protocols sequenced, edge case handling, timed output
- `lennys-wiki/plugin/skills/pmf-evaluator/SKILL.md` — Multi-step diagnostic, 5 framework layers, structured deliverable
- `kdp-kings-wiki/plugin/skills/niche-scout/SKILL.md` — Market-specific (BSR numbers, review thresholds)

#### Tutor Skills (2-4 per plugin, NEVER skip)

The user wants to learn, the skill teaches through guided exploration.

**Pattern:** Establish what they know → Teach concept → Ask them to apply → Teach next concept → Deliverable

**Structure (~150-250 lines):**
```markdown
---
name: [skill-name]
description: "[Trigger description — 'Teach me about X', 'How does X work', 'X workshop']"
---

# [Skill Name]

[One sentence: what you teach and how]

## Teaching Philosophy
Do not lecture. Ask questions, use analogies, let the user discover implications.

## Teaching Sequence

### 1. Establish What They Know
Ask: "[Opening question that surfaces their current mental model]"
Listen for: [Common misconception that becomes the entry point]

### 2. [Core Concept]
[Teach the concept with real quotes and analogies from the archive]
Ask: "[Question that makes them apply this to their own situation]"

### 3. [Next Concept Building on Previous]
[Build on what they just learned]
Ask: "[Deeper application question]"

[Continue for 6-10 steps]

## Deliverable
[Summary of what they learned + their specific application]
```

**Gold standard examples:**
- `lennys-wiki/plugin/skills/retention-workshop/SKILL.md` — Best in class. Teach → ask → teach → apply → deliverable.
- `huberman-wiki/plugin/skills/dopamine-masterclass/SKILL.md` — 10-step teaching sequence, wave pool analogy, personal application.

**Why tutors matter:** KDP Kings has zero tutor skills and it's the biggest gap. Tutors are the highest-engagement artifact because they're interactive learning. Every plugin needs at least 2-3.

#### Concierge Router (1 per plugin)

The dispatch layer that maps user intent to the right skill or framework search.

**Structure:**
```markdown
---
name: ask-[creator]
description: "Route any [domain] question to the right skill, protocol, or transcript search."
---

# Ask [Creator] — Concierge Router

## Routing Table
| User Intent | Route To | Type |
|-------------|----------|------|
| [Intent pattern] | `skill-name` | Decision/Tutor/Utility |
| Anything else | Search frameworks + transcripts | Direct |

## How to Route
1. Read the user's question
2. Match to the routing table
3. If match → read that skill's SKILL.md and follow it
4. If no match → search references/frameworks/ for relevant article
5. If still no match → search indexes, then read transcripts directly

## Framework Search
[List ALL actual framework filenames organized by domain. MUST match real files.]

## Response Style
[Domain-specific rules — lead with numbers, attribute to source, preserve hedging, etc.]
```

**Critical:** The framework search section must list ONLY filenames that actually exist in `references/frameworks/`. Phantom names are the most common bug across all three builds.

### Phase 4: Write Framework Articles

Tier 2 frameworks from the Master Catalog (I×S×T 25-49) become framework articles. These are dual-purpose: reference articles for human reading AND downloadable skill files for Claude.

**Structure (~80-120 lines):**
```markdown
---
name: "[Human-readable title]"
description: "[Trigger — when to surface this article]"
type: framework
domain: [domain-slug]
episodes:
  - [episode-filename-1.md]
  - [episode-filename-2.md]
source: [Creator name]
---

## When to Use
[1-2 paragraphs: specific situations that call for this framework]

## The Framework
[The actual methodology with real quotes, specific numbers, and source citations.
Every claim has an attributed quote. Every number has a source.]

## Example
[One concrete scenario showing the framework applied]

## Output
[What someone should be able to do after reading this]

> Source: [episode references]
```

**Gold standard examples:**
- `huberman-wiki/plugin/references/frameworks/physiological-sigh-protocol.md` — 82 lines, 4 real quotes from 4 episodes, step-by-step mechanism
- `huberman-wiki/plugin/references/frameworks/omega-3-epa-threshold.md` — Specific threshold (1000mg EPA), label-reading instructions, blood test guidance
- `lennys-wiki/plugin/references/frameworks/superhuman-pmf-engine.md` — The original gold standard

**Batch-by-source optimization:** Group articles by shared source episodes so each writing agent reads fewer transcripts. Works well when frameworks cluster by guest/episode (Lenny). Works less well when frameworks span dozens of episodes (Adams's persuasion filter = 16+ episodes). In that case, batch by domain instead.

**Quality gate for each article:**
- Does every claim have a source quote with episode attribution?
- Are specific numbers preserved (dosages, timings, temperatures, percentages)?
- Does the "When to Use" section describe a concrete situation, not a vague topic?
- Is the description field "pushy" enough to trigger when relevant?

### Phase 4.5: Enrichment Pass

Initial framework articles written from decomposition summaries are structurally correct but often lack real quotes. The enrichment pass goes back through decomposition reports and inserts direct quotes with episode citations.

**Why this is a separate phase:** Writing and enrichment have different failure modes. Writing agents need to produce structure and completeness. Enrichment agents need to find the best 3-5 quotes per article from the decomposition reports. Combining them overloads a single agent.

**Process:**
1. For each article missing real quotes, read the relevant decomposition report(s)
2. Find 3-5 direct quotes that support the article's key claims
3. Insert quotes with `> "quote" — Speaker, Episode Title` format
4. Verify every specific number in the article appears in a source quote

**Learned from Scott Adams build:** 14 of 36 articles were enriched in the first session; 22 still needed it. This phase can be parallelized — one agent per batch of 5-7 articles.

### Phase 4.75: Discovery Round

Both Scott Adams and Huberman decomposition reports surfaced frameworks NOT in the original plan. The persuasion report revealed "removing the reason," "audience of one," and "progression of awareness." The lifestyle report revealed "48-hour rule" and "one best evidence."

**Process:** After article writing, scan all decomposition reports for:
- Named frameworks that weren't in the Master Catalog
- Specific protocols with concrete parameters that deserve standalone articles
- Cross-domain patterns that emerge from reading multiple reports together

Create new framework articles for any discoveries that score well on the I×S×T rubric (or editorial judgment for smaller catalogs).

### Phase 4.9: Content Sensitivity Assessment

If the creator's content touches political, religious, health, or other sensitive domains, add framing to every skill and article:

- **Political content** (Scott Adams): "analytical, not advocacy" framing, present multiple perspectives, vocabulary table in router, track record includes wins AND losses
- **Health content** (Huberman): "informational, not medical advice" disclaimer, preserve hedging language from source, include safety warnings
- **Religious content**: Respect tradition, cite sources within the tradition, distinguish personal opinion from doctrine

This assessment should happen during Phase 2 (scaffolding) and inform every subsequent phase.

### Phase 5: Assemble

#### Build Indexes

Every plugin needs `references/indexes/by-topic.md` (universal). Additional indexes depend on the domain:

| Domain | Additional Indexes |
|--------|-------------------|
| Health/Science | by-supplement.md, by-protocol.md |
| Product Management | by-guest.md, by-company.md |
| Self-Publishing | by-stage.md, by-niche-type.md |
| General Business | by-industry.md, by-guest.md |

**Index format:**
```markdown
# [Index Name]

## [Category]

| [Entity] | Framework Articles | Key Episodes |
|----------|-------------------|--------------|
| [item] | `actual-framework-filename`, `another-one` | episode-id-1, episode-id-2 |
```

#### Wire the Router

Update the concierge router's framework search section with ALL actual framework filenames. Run the integrity check (see below).

#### Integrity Check (MANDATORY)

Run this validation before declaring the plugin complete:

```bash
# Extract all backtick-wrapped framework references from indexes and router
grep -oE '`[a-z0-9-]+(-[a-z0-9]+)+`' plugin/references/indexes/*.md plugin/skills/ask-*/SKILL.md | \
  sed 's/.*:`//;s/`$//' | sort -u > /tmp/referenced.txt

# List actual framework files
ls plugin/references/frameworks/ | sed 's/\.md$//' | sort -u > /tmp/existing.txt

# Check for mismatches
echo "=== Referenced but no file ===" && comm -23 /tmp/referenced.txt /tmp/existing.txt
echo "=== File exists but unreferenced ===" && comm -13 /tmp/referenced.txt /tmp/existing.txt
```

Both lists should be empty. If not:
- **Referenced but no file:** Either create the article or remove the reference
- **File exists but unreferenced:** Add it to the appropriate index and router section

#### Update plugin.json Description

Update the description with final counts:
```
"[N] episodes of [Source] turned into an interactive [domain] coach.
[X] decision and tutor skills, [Y] framework guides, and [N] searchable transcripts."
```

## Parallelization Strategy

The build benefits enormously from parallel agents. Here's what can run simultaneously:

**Phase 1:** All domain decomposer agents (one per domain) — fully parallel. **Critical batch size: 30-40 transcripts per agent, NOT 70-80.** Scott Adams build confirmed this — first attempt at 78 transcripts per agent hit context limits and 3 of 5 agents produced nothing. Second attempt at 35 transcripts per agent, all completed.

**Phase 3:** All decision skills can be written in parallel after decomposition completes. Tutor skills can also be parallel but should start after decision skills so the teaching content doesn't duplicate.

**Phase 4:** Framework article batches grouped by shared source episodes — each batch parallel.

**Phase 4.5:** Enrichment batches (5-7 articles per agent) — fully parallel.

**Phase 5:** Index building and router wiring — sequential (depends on knowing all framework filenames).

## Common Mistakes (Learned from 4 Builds)

1. **Phantom filenames in the router.** The router's framework search list gets written early and never updated. Both Huberman and Lenny had this. Always run the integrity check.

2. **Skipping tutor skills.** KDP Kings has zero tutors and it's the plugin's biggest gap. Budget at least 2-3 tutor skills per plugin. Tutor skills for controversial content (Scott Adams) require extra framing care.

3. **Not saving decomposition files.** These are the most valuable intermediate artifact. Lenny ran the agents but didn't save the output. Huberman did, and those 5 files (~50KB each) became the source of truth for everything downstream. Save to `plugin/references/decomposition-*.md`.

4. **Inconsistent specificity.** If the source material has specific numbers (dosages, BSR thresholds, percentages), the articles and skills MUST preserve them. "Consider X" is never acceptable when the source says "300mg of X, 30 minutes before Y."

5. **Skipping the enrichment pass.** Initial articles are structurally correct but lack real quotes. The enrichment pass is what turns a "good enough" article into something like the superhuman PMF engine. Scott Adams: 14/36 enriched, 22 still thin.

6. **Overloading decomposer agents.** 30-40 transcripts per agent is the sweet spot. At 70-80, agents hit context limits and produce nothing. Better to run more agents with smaller batches.

7. **Generic index types.** by-topic is universal, but every domain has an entity type that needs its own index. Health needs by-supplement. Product needs by-guest. Publishing needs by-stage. Discover these during decomposition, not hardcoded.

8. **Skipping the I×S×T scoring step.** Without scoring, you don't know what you missed. Lenny had 92 scored frameworks → 62 articles + 10 skills. KDP skipped scoring → 15 articles + 11 skills. However: for smaller catalogs (<40 frameworks), editorial judgment can substitute for formal scoring.

## Reference Builds

Read these for concrete examples of every artifact type:

| Plugin | Location | Skills | Frameworks | Strengths |
|--------|----------|--------|------------|-----------|
| Ask Lenny | `wiki-projects/lennys-wiki/plugin/` | 11 (5D+4T+1U+1R) | 62 | Master catalog, tutor skills, gold-standard superhuman PMF article |
| Ask KDP Kings | `wiki-projects/kdp-kings-wiki/plugin/` | 12 (10D+1U+1R) | 15 | Stage map routing, companion book, real BSR numbers |
| Ask Scott Adams | `wiki-projects/scott-adams-wiki/plugin/` | 12 (6D+4T+1U+1R) | 36 | Content sensitivity framing, decomposition reports preserved, 4 tutor skills for controversial content |
| Ask Huberman | `wiki-projects/huberman-wiki/plugin/` | 12 (6D+4T+1U+1R) | 56 | Strongest framework articles, 3 specialized indexes, decomposition preservation |
| Ask Zakery | `wiki-projects/how-to-think-wiki/plugin/` | 10 (6D+2T+1U+1R) | 16 | Critical thinking/logic, 2 reasoning indexes |

## Production Stats (for estimating new builds)

| Metric | Lenny | KDP Kings | Scott Adams | Huberman |
|--------|-------|-----------|-------------|----------|
| Source episodes | 303 | 175 (+book) | 389 polished | 137 |
| Decomposition agents | 5 | 0 (book chapters) | 5 (2 rounds) | 5 |
| Skills produced | 11 | 11 | 12 | 12 |
| Framework articles | 61 | 15 | 36 | 47 |
| Total plugin words | ~50K est | ~30K est | 64,673 | ~55K est |
| Approximate API cost | ~$15-20 | ~$8-10 | ~$25-30 | ~$15-20 |
