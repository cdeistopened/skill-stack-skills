# Invisible Threads Skill

Discovers non-obvious thematic connections ("invisible threads") across a corpus of essays, articles, or transcripts.

Adapted from [invisible-threads](https://github.com/baboonzero/invisible-threads).

## When to Use

- Editing an anthology and want to find thematic connections
- Analyzing a body of work for recurring ideas
- Finding quotes that support a theme across multiple sources
- Writing editorial commentary that weaves sources together

## Quick Start

```bash
# 1. Prepare your corpus as markdown files in a source directory

# 2. Chunk the corpus into a database
python chunk_corpus.py --source /path/to/markdown/files --output corpus.db

# 3. Extract insights using Gemini
python extract_insights.py --db corpus.db --backend gemini

# 4. Find threads
python find_threads.py --input data/insights_*.json

# 5. Review threads_*.json for editorial use
```

## Adapting for Your Project

The key file to modify is the **extraction prompt** in `extract_insights.py`.

### Default Prompt Categories
The default is set up for Catholic agrarian content (Cross & Plough):
- industrialism, land, family, property, craft, liturgy
- organic-farming, distributism, eugenics, totalitarianism
- natural-law, peasantry, economics, spirituality

### For Other Projects
Change the EXTRACTION_PROMPT in `extract_insights.py`:

1. **Context section**: Describe what the corpus is
2. **Examples section**: Give 3 examples of genuine insights from this domain
3. **Categories**: List 10-15 thematic categories relevant to your content

See `references/prompt-templates.md` for examples.

## Output

### insights_*.json
Each insight includes:
- `insight_text`: The extracted quote/idea
- `category`: Thematic category
- `novelty_score`: 1-10 how surprising
- `specificity_score`: 1-10 how quotable
- `source`: Which document it came from
- `raw_chunk`: Original context

### threads_*.json
Each thread includes:
- `thread_id`: Identifier
- `category`: Dominant theme
- `size`: Number of connected insights
- `num_sources`: How many different documents
- `years_spanned`: Timeline (if applicable)
- `insights`: All insights in this thread

## Editorial Applications

1. **Reorganize structure** around discovered threads
2. **Write headnotes** referencing how themes recur
3. **Add footnotes** pointing to related pieces
4. **Find unused quotes** that connect to themes
5. **Write bridge paragraphs** between sections

## Scripts

| Script | Purpose |
|--------|---------|
| `chunk_corpus.py` | Split markdown files into database |
| `extract_insights.py` | Extract insights using LLM (Gemini/Claude/Ollama) |
| `find_threads.py` | Cluster insights into thematic threads |

## Requirements

```
google-generativeai>=0.3.0  # For Gemini
sentence-transformers>=2.2.0
networkx>=3.0
python-louvain>=0.16
scikit-learn>=1.0
```

## Cost

| Backend | ~1000 chunks | Speed |
|---------|--------------|-------|
| Gemini Flash | Free tier | Fast |
| Gemini Pro | ~$1-2 | Fast |
| Claude Haiku | ~$0.50 | Fast |
| Ollama | Free | Slow |
