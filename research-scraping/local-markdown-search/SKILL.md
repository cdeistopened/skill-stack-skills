---
name: local-markdown-search
description: This skill enables searching across local markdown collections using QMD (Query Markup Documents). Use when indexing transcripts, notes, documentation, or knowledge bases for full-text, semantic, or combined search. Triggers on requests to "search my notes", "find in transcripts", "index markdown files", or "set up local search".
---

# Local Markdown Search

Search and query local markdown collections with BM25 full-text search, vector semantic search, and LLM re-ranking. Built on QMD (Query Markup Documents) for on-device, privacy-preserving search across transcripts, notes, wikis, and documentation.

## Purpose

- Index markdown files into searchable collections
- Perform keyword, semantic, or combined searches
- Retrieve full documents or snippets with context
- Support research workflows requiring source-grounded answers

## When to Use This Skill

- Setting up search for a new corpus of markdown files
- Querying transcripts, notes, or documentation
- Finding specific content across multiple files
- Building research briefs with source citations
- Creating searchable archives of knowledge bases

**Not for:** Web search, database queries, or non-markdown content.

---

## Setup

### Prerequisites

- Bun runtime installed
- QMD cloned and linked

### Installation

```bash
git clone https://github.com/tobi/qmd.git ~/qmd
cd ~/qmd
bun install
bun link  # Makes 'qmd' available globally
```

**Paths:**
- Index: `~/.cache/qmd/index.sqlite`
- Models: `~/.cache/qmd/models/` (~2GB, auto-downloaded on first use)

---

## Workflow

### Phase 1: Create Collections

**Goal:** Index markdown files into named, searchable collections.

#### Step 1: Add a Collection

```bash
qmd collection add /path/to/folder --name collection-name --mask "**/*.md"
```

**Parameters:**
- `--name`: Identifier for the collection (lowercase, hyphenated)
- `--mask`: Glob pattern for files to include

**Examples:**
```bash
qmd collection add ~/notes --name my-notes --mask "**/*.md"
qmd collection add ./transcripts --name podcasts --mask "**/polished/*.md"
qmd collection add . --name project --mask "**/*.{md,txt}"
```

#### Step 2: Verify Collections

```bash
qmd collection list   # Show all collections with stats
qmd status            # Index health and counts
```

### Phase 2: Search

**Goal:** Find relevant content across indexed collections.

#### Full-Text Search (BM25)

```bash
qmd search "keyword phrase" -n 10
qmd search "fasting cortisol" -c my-collection
```

#### Semantic Search (Vector)

Requires embeddings generated first:
```bash
qmd embed             # One-time setup (~2GB model download)
qmd vsearch "conceptual query about metabolism"
```

#### Combined Search with Reranking

```bash
qmd query "Why does this author oppose fasting?"
```

**Search Options:**
| Flag | Effect |
|------|--------|
| `-n <num>` | Number of results (default: 5) |
| `-c <name>` | Filter to specific collection |
| `--all` | Return all matches |
| `--min-score <num>` | Minimum similarity threshold |
| `--full` | Output full document content |
| `--files` | Output file paths only |
| `--json` | JSON output |

### Phase 3: Retrieve Documents

**Goal:** Get full content from search results.

#### Single Document

```bash
qmd get collection-name/path/to/file.md
qmd get collection-name/path/to/file.md -l 100  # First 100 lines
qmd get collection-name/path/to/file.md --from 50 -l 100  # Lines 50-150
```

#### Multiple Documents

```bash
qmd multi-get "**/*keyword*.md" -l 50
qmd multi-get "**/*.md" --max-bytes 10240
```

---

## Collection Management

```bash
qmd collection list              # List all with stats
qmd collection remove <name>     # Delete collection
qmd collection rename <old> <new>
qmd update                       # Re-index all collections
qmd update --pull                # Git pull then re-index
qmd cleanup                      # Remove orphaned data
```

---

## Context Annotations

Add metadata to improve search relevance:

```bash
qmd context add /path "Description of this folder's content"
qmd context list
qmd context rm /path
```

---

## MCP Server Integration

For AI agent integration:

```bash
qmd mcp    # Start MCP server
```

---

## Example: Research Workflow

```bash
# 1. Create collections
qmd collection add ~/wikis/ray-peat/transcripts --name rp-transcripts --mask "**/polished/*.md"
qmd collection add ~/wikis/ray-peat/newsletters --name rp-newsletters --mask "*.md"

# 2. Generate embeddings for semantic search
qmd embed

# 3. Search for topic
qmd search "fasting cortisol" -n 10 -c rp-transcripts
qmd vsearch "metabolic stress during starvation" -n 10

# 4. Get full documents from top results
qmd get rp-transcripts/jodellefit/polished/2019-06-01-cortisol.md --full

# 5. Multi-get for comprehensive research
qmd multi-get "**/*fasting*.md" -l 100 --md > research-sources.md
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Collection not found | Run `qmd collection list` to verify names |
| No results | Lower `--min-score` or check collection mask |
| Stale results | Run `qmd update` to re-index |
| Slow first search | Models downloading (~2GB one-time) |
| Vector search fails | Run `qmd embed` first |

---

## Related Skills

- **notebooklm** - Cloud-based search with Gemini (requires Google account)
- **research-assistant** - Research workflows using multiple tools

---

*QMD runs entirely on-device. No API keys required after initial model download. All data stays local.*
