---
name: wiki-chunk
description: Semantically chunk transcripts into topic-based JSON segments for search and RAG retrieval.
---

# Wiki Chunk

Split transcripts into semantic topic chunks using Gemini. Each chunk is a self-contained topic segment tagged with a topic type, key entities, and timestamps. Output is structured JSON ready for embedding and search.

## When to Use

After transcripts exist in `data/transcripts/`. Chunking is required before embedding (Qdrant) or indexing (QMD) steps.

## Prerequisites

- `wiki.yaml` exists with `chunking` section configured
- Transcripts in `data/transcripts/` (from `wiki-transcribe`)
- Python dependencies: `google-genai`, `pyyaml`

## Environment

| Variable | Required | Source |
|----------|----------|--------|
| `GEMINI_API_KEY` | Yes | `~/.zshrc` or `shared-backend/.env` |

## Usage

```bash
cd {wiki-dir}/pipeline

# Chunk 5 transcripts (default)
python3 chunk.py --limit 5 --workers 4

# Chunk all untranscribed
python3 chunk.py --limit 0

# Re-chunk everything (overwrite existing)
python3 chunk.py --no-skip --limit 0

# Single-threaded (for debugging)
python3 chunk.py --limit 1 --workers 1
```

### CLI Arguments

| Flag | Default | Description |
|------|---------|-------------|
| `--limit` | 5 | Max transcripts to process (0 = all) |
| `--workers` | 4 | Concurrent Gemini API calls |
| `--no-skip` | false | Re-chunk files that already have output |

## How It Works

1. **Collect transcripts**: Scans all directories listed in `wiki.yaml` `paths.transcript_dirs` for `.md` files
2. **Skip existing**: If a chunk JSON already exists for an episode ID, skip it (unless `--no-skip`)
3. **Parse frontmatter**: Extract title from YAML frontmatter
4. **Filter**: Skip transcripts under 100 words, truncate over 500K characters
5. **Build prompt**: Inject show context, topic types, speaker rules, and entity examples from `wiki.yaml`
6. **Call Gemini**: `gemini-3-flash-preview` with thinking mode (budget from `wiki.yaml`)
7. **Parse JSON**: Extract chunk array from response, clean markdown code fences
8. **Enrich**: Add `episode_id` and `episode_title` to each chunk
9. **Save**: Write JSON to `data/chunks/{episode_id}.json`

Processing is parallelized with a ThreadPoolExecutor. The `--workers` flag controls concurrency.

## Output Format

Each chunk file is `data/chunks/{episode_id}.json`:

```json
{
  "episode_id": "the_file_stem",
  "episode_title": "Episode Title from Frontmatter",
  "total_chunks": 12,
  "original_word_count": 8500,
  "chunks": [
    {
      "chunk_index": 0,
      "topic_title": "Descriptive Topic Name",
      "topic_type": "business_idea",
      "content": "Full text with **Speaker:** labels preserved...",
      "word_count": 650,
      "key_entities": ["Person Name", "Company Name", "concept"],
      "timestamp_start": "00:00",
      "timestamp_end": "05:30",
      "episode_id": "the_file_stem",
      "episode_title": "Episode Title"
    }
  ]
}
```

### Chunk Fields

| Field | Type | Description |
|-------|------|-------------|
| `chunk_index` | int | Sequential index within episode |
| `topic_title` | string | Descriptive, searchable title for the topic |
| `topic_type` | string | One of the types from `wiki.yaml` |
| `content` | string | Full transcript text for this chunk |
| `word_count` | int | Approximate word count |
| `key_entities` | string[] | 3-7 entities mentioned in the chunk |
| `timestamp_start` | string | Start time (MM:SS or HH:MM:SS) |
| `timestamp_end` | string | End time |

## wiki.yaml Config Reference

```yaml
chunking:
  topic_types:
    - business_idea
    - founder_story
    - framework
    - tactic
    - case_study
    - qa
    - intro
    - sponsor
    - tangent
  context: |
    Show description for chunking prompt context.
  rules:
    - "Pay special attention to financial figures"
  entity_examples: '"Person Name", "Company Name", "concept mentioned"'
  thinking_budget: 4096
paths:
  transcript_dirs: ["data/transcripts"]
```

| Field | Purpose |
|-------|---------|
| `topic_types` | Valid labels for chunk classification |
| `context` | Injected into the chunking prompt for domain awareness |
| `rules` | Extra rules appended to the prompt (numbered 9+) |
| `entity_examples` | Example entities for the JSON schema in the prompt |
| `thinking_budget` | Gemini thinking tokens (0 = disabled, 4096 = recommended) |

## Gemini Configuration

| Setting | Value |
|---------|-------|
| Model | `gemini-3-flash-preview` |
| Max output tokens | 65,536 |
| Temperature | 0.2 |
| Thinking budget | From `wiki.yaml` (default: 4096) |

## Cost

- ~$0.02 per transcript (Gemini 3 Flash)
- A 600-episode corpus costs roughly $12 total
- Thinking mode adds marginal cost but improves chunk boundary quality

## Quality Checks

After a batch run:

- [ ] **Chunk count per episode**: Should be 5-15 chunks. Check outliers:
  ```bash
  for f in data/chunks/*.json; do echo "$(python3 -c "import json; print(json.load(open('$f'))['total_chunks'])"): $f"; done | sort -n
  ```

- [ ] **No tiny chunks**: Chunks under 200 words may indicate poor segmentation. Spot-check any with `word_count < 200`

- [ ] **No monster chunks**: Chunks over 2000 words should be rare. They may indicate the model failed to find natural break points

- [ ] **Topic type distribution**: Check that `intro` and `sponsor` chunks are minimal:
  ```bash
  python3 -c "
  import json, glob, collections
  types = collections.Counter()
  for f in glob.glob('data/chunks/*.json'):
      for c in json.load(open(f))['chunks']:
          types[c['topic_type']] += 1
  for t, n in types.most_common(): print(f'{t}: {n}')
  "
  ```

- [ ] **Speaker labels preserved**: Open 2-3 chunk files and verify `**Name:**` labels are in the content

- [ ] **Entity quality**: Key entities should be meaningful names, not generic terms

- [ ] **JSON validity**: All files should parse without errors

## Shared Library Reference

| Module | Class/Function | Purpose |
|--------|----------------|---------|
| `wiki-projects/lib/chunker.py` | `SemanticChunker` | Core chunking engine |
| `wiki-projects/lib/config.py` | `WikiConfig` | Config loader |
| `wiki-projects/lib/gemini_client.py` | `create_client()` | API client |
| `wiki-projects/lib/utils.py` | `parse_frontmatter()`, `clean_json_response()` | Utilities |

## Troubleshooting

**JSON parse errors**: Gemini occasionally returns invalid JSON. The `clean_json_response()` function strips markdown code fences, but deeply malformed JSON will fail. Re-run and the transcript will be retried.

**Empty chunks array**: Usually means the transcript is too short or garbled. Check the source transcript quality.

**All chunks tagged as one type**: The topic types in `wiki.yaml` may not match the content well. Review and adjust topic types for better domain fit.

**Rate limiting**: With 4 workers, you may hit Gemini rate limits on large batches. Reduce `--workers 2` or add delays. The shared lib handles this gracefully with error logging.
