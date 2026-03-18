---
name: wiki-extract-entities
description: Extract named entities from transcripts into a structured inventory with mention counts, co-occurrences, and sentiment.
---

# Wiki Extract Entities

Extract named entities from transcripts and build a cumulative inventory with mention counts, source episodes, co-occurrence tracking, and sentiment. Uses Gemini to identify entities in domain-specific categories defined in `wiki.yaml`.

## When to Use

After transcripts exist in `data/transcripts/`. Entity extraction can run independently of chunking -- it reads raw transcripts, not chunks. The entity inventory feeds into article topic selection, SEO briefs, and wiki navigation.

## Prerequisites

- `wiki.yaml` exists with `entities.categories` configured
- Transcripts in `data/transcripts/` (from `wiki-transcribe`)
- Python dependencies: `google-genai`, `pyyaml`

## Environment

| Variable | Required | Source |
|----------|----------|--------|
| `GEMINI_API_KEY` | Yes | `~/.zshrc` or `shared-backend/.env` |

## Usage

```bash
cd {wiki-dir}/pipeline

# Extract from 10 transcripts (default behavior)
python3 extract.py --limit 10

# Extract from all transcripts
python3 extract.py

# Re-extract (don't skip already-processed episodes)
python3 extract.py --no-skip
```

### CLI Arguments

| Flag | Default | Description |
|------|---------|-------------|
| `--limit` | None (all) | Max transcripts to process |
| `--no-skip` | false | Re-process episodes already in inventory |

## How It Works

1. **Load existing inventory**: If `data/entities/entity-inventory.json` exists, load it and track which episodes are already processed
2. **Collect transcripts**: Scan all `paths.transcript_dirs` from `wiki.yaml`
3. **Split for extraction**: Each transcript is split into ~4000-character chunks at `## ` header boundaries (not the same as semantic chunks)
4. **Build prompt**: For each chunk, build an extraction prompt with category definitions and host exclusion rules from `wiki.yaml`
5. **Call Gemini**: `gemini-3-flash-preview` with optional thinking mode
6. **Merge into inventory**: Each entity is added/updated in the running inventory with:
   - Mention count increment
   - Source episode tracking
   - Sentiment tallying (positive/negative/neutral)
   - Co-occurrence tracking (entities mentioned in the same chunk)
7. **Checkpoint**: Save inventory every 10 episodes
8. **Final save**: Write `entity-inventory.json` and `top-entities.json`

## Output

### `data/entities/entity-inventory.json`

Full inventory organized by category:

```json
{
  "people": {
    "Warren Buffett": {
      "mentions": 102,
      "sources": ["episode_id_1", "episode_id_2"],
      "co_occurs_with": {
        "Berkshire Hathaway": 45,
        "Charlie Munger": 38
      },
      "sentiment": {
        "positive": 80,
        "negative": 5,
        "neutral": 17
      }
    }
  },
  "companies": {
    "Berkshire Hathaway": {
      "mentions": 67,
      "sources": ["episode_id_1"],
      "co_occurs_with": {"Warren Buffett": 45},
      "sentiment": {"positive": 50, "negative": 2, "neutral": 15}
    }
  }
}
```

### `data/entities/top-entities.json`

Top 50 entities by mention count, flattened:

```json
[
  {
    "name": "Warren Buffett",
    "category": "people",
    "mentions": 102,
    "sources_count": 45,
    "sentiment": {"positive": 80, "negative": 5, "neutral": 17},
    "top_co_occurs": [["Berkshire Hathaway", 45], ["Charlie Munger", 38]]
  }
]
```

## wiki.yaml Config Reference

```yaml
entities:
  categories:
    people: "Founders, guests, investors, mentors, business personalities"
    companies: "Startups, businesses, brands, products mentioned"
    ideas: "Business ideas, opportunities, market trends, concepts"
    frameworks: "Mental models, business strategies, principles, systems"
    tactics: "Specific how-tos, methods, actionable techniques"
    numbers: "Revenue figures, valuations, deal sizes, growth metrics"
  context: |
    Optional extraction-specific context (falls back to top-level context)
  thinking_budget: 2048
hosts:
  - name: Sam Parr
    exclude_from_entities: true
  - name: Shaan Puri
    exclude_from_entities: true
```

| Field | Purpose |
|-------|---------|
| `categories` | Dict of category name to description. These are the valid labels for extracted entities. |
| `context` | Optional extraction-specific context. Falls back to top-level `context` if not set. |
| `thinking_budget` | Gemini thinking tokens for extraction (0 = disabled, 2048 = recommended) |
| `hosts[].exclude_from_entities` | When `true`, host names are excluded from extraction results |

### Designing Entity Categories

Categories should be domain-specific. Examples from existing wikis:

**Business podcast (MFM):** people, companies, ideas, frameworks, tactics, numbers

**Finance podcast (MoneyWise):** people, companies, portfolios, income_sources, expenses, net_worth, frameworks, tactics

**Health/science podcast:** people, compounds, mechanisms, studies, protocols, conditions

**Tech podcast:** people, companies, technologies, architectures, tools, metrics

## Gemini Configuration

| Setting | Value |
|---------|-------|
| Model | `gemini-3-flash-preview` |
| Max output tokens | 4,096 |
| Temperature | 0.1 |
| Thinking budget | From `wiki.yaml` (default: 2048) |
| Rate limiting | 0.5s sleep between chunks |

## Cost

- ~$0.01 per transcript
- A 600-episode corpus costs roughly $6 total
- Each transcript is split into multiple extraction chunks, but the prompt and response are small

## Quality Checks

After a run:

- [ ] **Category distribution**: All configured categories should have entities. Empty categories may indicate poor category design:
  ```bash
  python3 -c "
  import json
  inv = json.load(open('data/entities/entity-inventory.json'))
  for cat, entities in inv.items():
      print(f'{cat}: {len(entities)} entities')
  "
  ```

- [ ] **Host exclusion**: Verify hosts are NOT in the inventory (they should be excluded):
  ```bash
  python3 -c "
  import json
  inv = json.load(open('data/entities/entity-inventory.json'))
  for cat, entities in inv.items():
      for name in entities:
          if 'parr' in name.lower() or 'puri' in name.lower():
              print(f'WARNING: Host found: {name} in {cat}')
  "
  ```

- [ ] **Name normalization**: Check for duplicates (e.g., "Elon Musk" and "Musk" as separate entries). Some duplication is expected -- the inventory is additive.

- [ ] **Top entities make sense**: The top 10 by mention count should be recognizable, important entities from the show:
  ```bash
  python3 -c "
  import json
  top = json.load(open('data/entities/top-entities.json'))
  for e in top[:10]:
      print(f\"{e['name']} ({e['category']}): {e['mentions']} mentions\")
  "
  ```

- [ ] **Co-occurrence sanity**: Top co-occurrences should reflect real relationships (e.g., a founder co-occurs with their company)

- [ ] **Sentiment distribution**: Most entities should be neutral or positive. A heavily negative-skewed entity might indicate extraction errors.

## Shared Library Reference

| Module | Class/Function | Purpose |
|--------|----------------|---------|
| `wiki-projects/lib/entity_extractor.py` | `EntityExtractor` | Core extraction engine |
| `wiki-projects/lib/config.py` | `WikiConfig` | Config loader with entity category access |
| `wiki-projects/lib/gemini_client.py` | `create_client()` | API client |
| `wiki-projects/lib/utils.py` | `parse_frontmatter_regex()`, `extract_json_object()` | Utilities |

## Troubleshooting

**Inventory grows very large**: The MFM inventory reached 22,621 entities across 600+ episodes. This is normal for large corpora. The `top-entities.json` file provides a manageable subset.

**Many entities in wrong categories**: Review the category descriptions in `wiki.yaml`. Make them more specific and add negative examples if needed.

**Checkpointing**: The extractor saves every 10 episodes. If a run crashes, re-run with default flags and it will resume from where it left off (skipping processed episodes).

**Slow processing**: Entity extraction is sequential (not parallelized like chunking) because it maintains a running inventory. The 0.5s sleep between chunks prevents rate limiting. A 100-episode corpus takes roughly 30-45 minutes.
