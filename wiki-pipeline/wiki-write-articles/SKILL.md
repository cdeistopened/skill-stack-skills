---
name: wiki-write-articles
description: Multi-agent article generation from wiki data. Research agent queries sources, writer agent produces articles in target voice.
---

# Wiki Write Articles

Generate wiki articles from corpus data using a two-agent workflow: a research agent that queries indexed chunks to gather evidence, and a writer agent that produces polished articles in a target voice with inline citations.

## When to Use

After at least one search index is available:
- QMD local index (from `wiki-index-qmd`), OR
- Qdrant Cloud embeddings (from `wiki-embed-qdrant`)

Also requires entity inventory (from `wiki-extract-entities`) for topic selection and cross-referencing.

## Prerequisites

- Search index: QMD collection or Qdrant embeddings populated
- Entity inventory at `data/entities/entity-inventory.json` and `data/entities/top-entities.json`
- Article topics selected (typically from top entities or SEO research)

## Environment

| Variable | Required | Source |
|----------|----------|--------|
| QMD CLI | If using QMD search | Installed via bun |
| `GEMINI_API_KEY` | If using Qdrant backend | `~/.zshrc` |
| `QDRANT_API_KEY` | If using Qdrant backend | `~/.zshrc` |
| `QDRANT_CLOUD_URL` | If using Qdrant backend | `~/.zshrc` |

Claude agents (research + writer) run within Claude Code sessions. No separate API keys needed for the agent layer.

## Workflow Overview

```
Topic Selection ──► Research Agent ──► research.json ──► Writer Agent ──► draft-{voice}.md
                         │                                    │
                         ▼                                    ▼
                   QMD/Qdrant search              Voice guidelines + citations
```

### Step 1: Topic Selection

Choose article topics from one or more sources:

**From entity inventory:**
```bash
# View top entities
python3 -c "
import json
top = json.load(open('data/entities/top-entities.json'))
for e in top[:20]:
    print(f\"{e['name']} ({e['category']}): {e['mentions']} mentions, {e['sources_count']} episodes\")
"
```

Good article candidates have:
- High mention count (discussed frequently)
- High source count (discussed across many episodes, not just one)
- Rich co-occurrence graph (connected to other entities)

**From SEO research:**
- Content briefs in `data/seo/` (if generated)
- Keyword research targeting search volume for the wiki's domain

**From editorial judgment:**
- Core concepts the show is known for
- Frequently asked questions from the audience
- Controversial or distinctive positions taken by hosts

### Step 2: Research Agent

The research agent gathers evidence for a specific topic by querying the search index.

**Research queries (3-5 per topic):**
1. Direct entity name search
2. Related concept search
3. Specific quote/advice search
4. Contrarian or nuanced angle search

**Using QMD:**
```bash
qmd search --collection {slug}-transcripts --query "Alex Hormozi business advice" --limit 10
qmd search --collection {slug}-transcripts --query "Hormozi $100M Offers framework" --limit 5
qmd search --collection {slug}-transcripts --query "Hormozi controversial opinion" --limit 5
```

**Using Qdrant backend:**
```bash
curl -X POST https://api-production-4224.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -H "X-User-Email: research@wiki.com" \
  -d '{"wiki":"{slug}","query":"Alex Hormozi business advice","limit":10}'
```

**Fallback (local chunk search):**
When API limits are exhausted, search chunk files directly:
```bash
grep -rl "Hormozi" data/chunks/ | head -10
```

**Research output:** Save as `docs/articles/{topic-slug}/research.json`:

```json
{
  "topic": "Alex Hormozi",
  "category": "people",
  "queries": [
    {"query": "Alex Hormozi business advice", "results": 10}
  ],
  "quotes": [
    {
      "text": "Direct quote from transcript...",
      "episode_id": "episode_slug",
      "episode_title": "Episode Title",
      "timestamp": "15:30",
      "speaker": "Sam"
    }
  ],
  "key_insights": [
    "Insight summary with episode reference"
  ],
  "episodes_referenced": ["ep1", "ep2", "ep3"],
  "related_entities": ["$100M Offers", "Gym Launch", "Acquisition.com"]
}
```

### Step 3: Writer Agent

The writer agent produces the article from the research file, following voice guidelines.

**Input:** `research.json` for the topic
**Output:** `draft-{voice}.md` (e.g., `draft-housel.md`)

### Voice Selection

Choose a voice style for the wiki. The voice should match the wiki's audience and tone.

**Proven voices from existing wikis:**

**Morgan Housel voice** (used for MFM Wiki):
- Calm, measured tone. Zero exclamation points.
- Lead with counterintuitive observation or striking anecdote
- Concrete numbers and specific examples throughout
- Paraphrase by default; only use direct quotes when "clip-worthy gold"
- Inline YouTube links with timestamps
- Wiki links using `[[Entity Name]]` for cross-references

**Other voice options to consider:**
- **Packy McCormick**: Energetic, pop-culture analogies, punchy subheads
- **Encyclopedia**: Neutral, factual, Wikipedia-style
- **Practitioner**: How-to focused, step-by-step, actionable

### Article Structure

```markdown
# {Entity/Topic Name}

Opening paragraph: counterintuitive hook or striking fact from the data.

## Background / Context

Who/what this is, why it matters in the show's universe.

## Key Themes

### Theme 1: [Specific Angle]

Content with inline citations: "direct quote" ([Episode Title, MM:SS](youtube_url&t=XXs)).

### Theme 2: [Another Angle]

More content with cross-references to [[Related Entity]].

## Notable Quotes

> "Exact quote from transcript" -- Speaker Name, [Episode Title](url)

## Episodes

| Episode | Date | Key Topics |
|---------|------|------------|
| Episode Title | YYYY-MM-DD | topic1, topic2 |

## See Also

- [[Related Entity 1]]
- [[Related Entity 2]]
```

### Step 4: Batch Processing

For producing multiple articles in a batch, use a manifest:

**`docs/articles/BATCH-MANIFEST.json`:**
```json
{
  "batch_id": "batch-2026-02-12",
  "status": "in_progress",
  "voice": "housel",
  "articles": [
    {"id": "alex-hormozi", "status": "draft_complete"},
    {"id": "boring-businesses", "status": "researching"},
    {"id": "network-effects", "status": "todo"}
  ]
}
```

Process each article sequentially:
1. Create `docs/articles/{topic-slug}/` directory
2. Run research queries, save `research.json`
3. Write draft, save `draft-{voice}.md`
4. Update manifest status

## Output

### Per Article

```
docs/articles/{topic-slug}/
├── research.json       # Gathered evidence with citations
└── draft-housel.md     # Article in target voice
```

### Batch

```
docs/articles/
├── BATCH-MANIFEST.json
├── alex-hormozi/
│   ├── research.json
│   └── draft-housel.md
├── boring-businesses/
│   ├── research.json
│   └── draft-housel.md
└── ...
```

## Quality Checks

### Research Quality

- [ ] **3+ queries per topic**: Each topic should have multiple search angles
- [ ] **5+ source episodes**: Articles grounded in a single episode are thin
- [ ] **Direct quotes captured**: At least 3-5 clip-worthy quotes with timestamps
- [ ] **Cross-references identified**: Related entities noted for wiki linking

### Article Quality

- [ ] **Factual accuracy**: Every claim should trace back to a source chunk. No hallucinated quotes, anecdotes, or statistics.
- [ ] **Voice consistency**: Read the article aloud. Does it match the target voice? (e.g., for Housel: no exclamation points, no listicles, calm tone)
- [ ] **Inline citations**: Quotes and specific claims have `[Episode Title, MM:SS]` links
- [ ] **Wiki links**: Related entities use `[[Entity Name]]` linking
- [ ] **No fabricated content**: Everything must come from the research.json or be clearly labeled as editorial context
- [ ] **Length**: Wiki articles should be 1,000-3,000 words. Shorter for minor entities, longer for major topics.
- [ ] **Episode table**: Includes a table of referenced episodes

### Common Failure Modes

- **Hallucinated quotes**: The writer agent invents quotes that sound plausible but are not in the research. Always cross-check direct quotes against `research.json`.
- **Wrong attribution**: Quote attributed to wrong speaker. Verify speaker labels from source chunks.
- **VIDEO_ID placeholders**: YouTube links need real video IDs. These may need a separate episode-to-YouTube mapping step.
- **Over-reliance on one episode**: Good articles draw from 5+ episodes. If research only found 1-2 episodes, the topic may not warrant a standalone article.

## Shared Library / Resource Reference

| Resource | Location | Purpose |
|----------|----------|---------|
| Entity inventory | `data/entities/top-entities.json` | Topic selection |
| Chunk files | `data/chunks/*.json` | Fallback local search |
| Shared backend | `wiki-projects/shared-backend/` | RAG API |
| MFM articles | `wiki-projects/mfm-wiki/docs/articles/` | Reference implementation (49 articles) |
| Batch manifest | `docs/articles/BATCH-MANIFEST.json` | Batch tracking |

## Troubleshooting

**RAG API returns no results**: Check that the Qdrant collection has vectors (`/stats/{slug}` endpoint). If empty, run `wiki-embed-qdrant` first.

**Daily query limit exhausted**: The backend has a 20-query daily limit per email. Use a different email or fall back to local chunk file search with `grep`.

**Articles feel generic**: Increase research depth. More queries with more specific angles produce more distinctive articles. Search for the entity's name plus specific subtopics, controversies, or frameworks.

**Missing YouTube URLs**: Create an episode-to-YouTube mapping file. This is a manual or semi-automated step that matches episode IDs/titles to YouTube video URLs.

**Batch consistency**: When writing 10+ articles in one session, the writer agent may drift from the voice guidelines. Re-read the voice spec every 5 articles and compare against the template article.
