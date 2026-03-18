---
name: wiki-embed-qdrant
description: Embed semantic chunks into Qdrant Cloud for the production RAG backend API.
---

# Wiki Embed Qdrant

Create vector embeddings from semantic chunks using the Gemini embedding API and upsert them into a Qdrant Cloud collection. This powers the production chatbot/RAG backend deployed on Railway.

## When to Use

After chunks exist in `data/chunks/` (from `wiki-chunk`). This step makes the wiki searchable via the shared backend API.

## Prerequisites

- Chunks exist in `data/chunks/` (JSON files from the chunking pipeline)
- Qdrant Cloud account with a cluster running
- Python dependencies: `qdrant-client`, `requests`, `python-dotenv`, `pyyaml`

## Environment

| Variable | Required | Source |
|----------|----------|--------|
| `GEMINI_API_KEY` | Yes | `~/.zshrc` or `shared-backend/.env` |
| `QDRANT_API_KEY` | Yes | `~/.zshrc` or `shared-backend/.env` |
| `QDRANT_CLOUD_URL` | Yes | `~/.zshrc` or `shared-backend/.env` |

All three variables must be set. The embed script loads from `shared-backend/.env` via `python-dotenv`.

## Usage

```bash
cd wiki-projects/shared-backend

# Embed chunks for a specific wiki
python3 embed_chunks.py --wiki {slug}

# Custom batch size (default: 20)
python3 embed_chunks.py --wiki {slug} --batch-size 50

# Resume from a specific offset (skip first N chunks)
python3 embed_chunks.py --wiki {slug} --start-from 500
```

### CLI Arguments

| Flag | Default | Description |
|------|---------|-------------|
| `--wiki` | Required | Wiki slug (must be in `WIKI_CONFIGS`) |
| `--batch-size` | 20 | Chunks per Qdrant upsert batch |
| `--start-from` | 0 | Skip first N chunks (for resuming) |

### Adding a New Wiki

Before running for a new wiki, add it to the `WIKI_CONFIGS` dict in `shared-backend/embed_chunks.py`:

```python
WIKI_CONFIGS = {
    # ... existing entries ...
    "{slug}": {
        "chunks_dir": Path(__file__).parent.parent / "{slug}-wiki/data/chunks",
        "collection": "{slug}_chunks",
    },
}
```

Also add the wiki to the backend API config in `shared-backend/main.py`:

```python
"{slug}": {
    "name": "{Wiki Name}",
    "collection": "{slug}_chunks",
    "backend": "qdrant_cloud",
    "prompt_context": "brief description of content domain",
    "source_label": "{Show Name}",
}
```

## How It Works

1. **Load chunks**: Read all JSON files from the wiki's chunks directory using the wiki-specific loader function
2. **Detect embedding dimension**: Embed one sample chunk to determine vector size (768 for Gemini embedding-001)
3. **Create collection**: If the Qdrant collection does not exist, create it with cosine distance
4. **Auto-resume**: If the collection already has points and `--start-from` is 0, automatically resume from the existing point count
5. **Batch process**: For each batch:
   - Truncate chunk text to 8000 characters for embedding
   - Call Gemini embedding API (`gemini-embedding-001`)
   - Create `PointStruct` with vector and metadata payload
   - Upsert batch to Qdrant
6. **Verify**: Print final vector count

## Embedding Details

| Setting | Value |
|---------|-------|
| Model | `gemini-embedding-001` |
| Vector dimensions | 768 |
| Distance metric | Cosine |
| Max text length | 8000 characters (truncated) |
| API method | REST (`generativelanguage.googleapis.com/v1beta`) |

### Payload Schema

Each point in Qdrant stores:

```json
{
  "id": 0,
  "vector": [0.123, -0.456, ...],
  "payload": {
    "text": "Full chunk content...",
    "episode_title": "Episode Title",
    "episode_date": "",
    "topic_title": "Topic Name",
    "topic_type": "framework",
    "url": "",
    "start_timestamp": "05:30"
  }
}
```

MFM and MoneyWise also include `key_entities` in the payload.

## Output

- Vectors in Qdrant Cloud collection `{slug}_chunks`
- Collection is immediately queryable via the RAG backend API

### Testing the Backend

After embedding, test via the shared backend:

```bash
# Check stats
curl https://api-production-4224.up.railway.app/stats/{slug}

# Test a query
curl -X POST https://api-production-4224.up.railway.app/chat \
  -H "Content-Type: application/json" \
  -H "X-User-Email: test@example.com" \
  -d '{"wiki":"{slug}","query":"test query here","limit":5}'
```

Daily limit is 20 queries per email.

## Cost

- **Embedding**: ~$0.001 per chunk (Gemini embedding API is very cheap)
- **Qdrant Cloud**: Free tier covers small collections; paid tier for larger wikis
- A 5,000-chunk wiki costs roughly $5 to embed

## Quality Checks

After embedding:

- [ ] **Vector count matches chunk count**: Compare Qdrant collection point count against total chunks:
  ```bash
  # Expected chunks
  python3 -c "
  import json, glob
  total = sum(json.load(open(f))['total_chunks'] for f in glob.glob('../{slug}-wiki/data/chunks/*.json'))
  print(f'Expected: {total}')
  "
  ```

- [ ] **Test RAG queries**: Run 3-5 test queries against the backend and verify results are relevant

- [ ] **Payload completeness**: Query a single point and verify all metadata fields are present:
  ```python
  from qdrant_client import QdrantClient
  client = QdrantClient(url=QDRANT_CLOUD_URL, api_key=QDRANT_API_KEY)
  points = client.scroll(collection_name="{slug}_chunks", limit=1)
  print(points[0][0].payload)
  ```

- [ ] **No empty vectors**: Spot-check that retrieved results have meaningful text content

## wiki.yaml Config Reference

The embed script does not read `wiki.yaml` directly. It uses the hardcoded `WIKI_CONFIGS` dict in `embed_chunks.py`. The convention is:
- Chunks dir: `{slug}-wiki/data/chunks`
- Collection name: `{slug}_chunks`

## Shared Library Reference

| File | Purpose |
|------|---------|
| `wiki-projects/shared-backend/embed_chunks.py` | Embedding and Qdrant upsert script |
| `wiki-projects/shared-backend/main.py` | RAG backend API (FastAPI on Railway) |
| `wiki-projects/shared-backend/.env` | API keys (GEMINI, QDRANT) |

## Troubleshooting

**"Collection not found" on query**: The collection was created but is empty. Check that the embedding step completed without errors.

**Auto-resume skips everything**: If the collection already has the right number of points, the script correctly skips. Use `--start-from 0` and delete/recreate the collection to force re-embedding.

**Gemini embedding API 429 (rate limit)**: Reduce batch size to 10 and add delays. The script does not have built-in rate limiting for embedding calls.

**Qdrant connection timeout**: Check `QDRANT_CLOUD_URL` format. It should be `https://xxxxxxxx.us-east4-0.gcp.cloud.qdrant.io:6333` (with port).

**Partial upload (interrupted)**: The auto-resume feature handles this. Re-run the same command and it will pick up from where it left off based on existing point count.

**Different chunk formats per wiki**: The embed script has wiki-specific loader functions (`load_mfm_chunks`, `load_huberman_chunks`, etc.) because chunk JSON schemas vary slightly between older and newer wikis. New wikis using the shared lib chunker follow the MFM/MoneyWise format.
