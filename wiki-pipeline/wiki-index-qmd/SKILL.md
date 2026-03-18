---
name: wiki-index-qmd
description: Index semantic chunks into QMD (local hybrid search) for article research and RAG queries.
---

# Wiki Index QMD

Index semantic chunks into QMD, a local hybrid search engine that combines BM25 keyword search, vector similarity, and reranking. QMD collections are used by the article writing agents to research topics before drafting.

## When to Use

After chunks exist in `data/chunks/` (from `wiki-chunk`). QMD indexing is an alternative or complement to Qdrant Cloud embedding. Use QMD for local research and development; use Qdrant for the production RAG API.

## Prerequisites

- Chunks exist in `data/chunks/` (JSON files from the chunking pipeline)
- QMD CLI installed (bun-based)
- QMD server running locally

## Environment

| Variable | Required | Source |
|----------|----------|--------|
| QMD CLI | Yes | Installed via bun |
| No API keys needed | -- | QMD runs locally |

## Usage

### Step 1: Create Collection

```bash
qmd create-collection {slug}-transcripts
```

This creates an empty collection ready to accept documents.

### Step 2: Index Chunks

```bash
qmd index --collection {slug}-transcripts --input data/chunks/ --format wiki-chunks
```

The `wiki-chunks` format tells QMD to:
- Read each JSON file in the input directory
- Extract the `chunks[]` array from each file
- Index each chunk as a separate document with metadata fields:
  - `episode_id`
  - `episode_title`
  - `topic_title`
  - `topic_type`
  - `key_entities`
  - `timestamp_start`
  - `timestamp_end`

### Step 3: Verify

```bash
# Check collection stats
qmd stats {slug}-transcripts

# Test a search query
qmd search --collection {slug}-transcripts --query "business idea for SaaS" --limit 5
```

### Re-indexing

To re-index after adding new chunks:

```bash
# Delete and recreate
qmd delete-collection {slug}-transcripts
qmd create-collection {slug}-transcripts
qmd index --collection {slug}-transcripts --input data/chunks/ --format wiki-chunks
```

Or index only new files:

```bash
# Index a specific file
qmd index --collection {slug}-transcripts --input data/chunks/new_episode.json --format wiki-chunks
```

## How QMD Search Works

QMD provides hybrid search combining three signals:

1. **BM25 (keyword)**: Traditional full-text search. Good for exact name matches, specific terms.
2. **Vector (semantic)**: Embedding-based similarity. Good for conceptual queries that don't match exact words.
3. **Reranker**: Cross-encoder reranking of top results for precision.

The article writing agents use QMD queries like:
```
qmd search --collection mfm-transcripts --query "Alex Hormozi business advice" --limit 10
```

Results include the chunk content, metadata, and relevance scores.

## Output

After indexing, the QMD collection contains:

| Field | Source |
|-------|--------|
| Document text | `chunks[].content` |
| episode_id | `chunks[].episode_id` |
| episode_title | `chunks[].episode_title` |
| topic_title | `chunks[].topic_title` |
| topic_type | `chunks[].topic_type` |
| key_entities | `chunks[].key_entities` |
| timestamp_start | `chunks[].timestamp_start` |

## wiki.yaml Config Reference

QMD indexing does not read `wiki.yaml` directly -- it works from the chunk JSON files. The `slug` from `wiki.yaml` is used as the collection name convention: `{slug}-transcripts`.

## Quality Checks

After indexing:

- [ ] **Document count**: `qmd stats {slug}-transcripts` should show a document count close to the total chunk count across all JSON files
  ```bash
  python3 -c "
  import json, glob
  total = sum(json.load(open(f))['total_chunks'] for f in glob.glob('data/chunks/*.json'))
  print(f'Expected chunks: {total}')
  "
  ```

- [ ] **Search relevance**: Test 3-5 queries about known topics and verify results make sense:
  ```bash
  qmd search --collection {slug}-transcripts --query "specific known topic" --limit 3
  ```

- [ ] **Entity search**: Search for a top entity by name and confirm results include episodes where that entity appears

- [ ] **No empty documents**: Spot-check that retrieved documents have meaningful content (not empty or truncated)

## Relationship to Other Steps

```
Transcripts ──► Chunks ──► QMD Index ──► Article Research Agent
                       └──► Qdrant Embeddings ──► Production RAG API
```

QMD and Qdrant serve different purposes:
- **QMD**: Local development, article writing research, iterative queries
- **Qdrant**: Production chatbot backend, API access

Both can be populated from the same chunk files.

## Troubleshooting

**QMD not found**: Install QMD via bun. Check that the `qmd` binary is on your PATH.

**Indexing fails on large collections**: Index in batches by pointing to individual chunk files rather than the entire directory.

**Search returns irrelevant results**: Check that chunks are properly segmented. Poor chunking quality upstream leads to poor search quality downstream.

**Collection already exists**: Use `qmd delete-collection` then recreate, or use the `--upsert` flag if available.
