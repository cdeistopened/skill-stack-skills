# Manuscript Search Skill

Search the Benedict Challenge manuscript with natural language queries.

---

## Usage

When user asks to search the manuscript (e.g., "What did I write about replacement habits?"), follow this workflow:

### Step 1: Extract Search Terms

From the query, identify:
- **Primary terms**: Key words/phrases to search (e.g., "replacement", "habits", "substitute")
- **Semantic expansions**: Related terms the user might have used (e.g., "swap", "instead of", "alternative")

### Step 2: Search All Sources

Search these locations in order of canonicity:

| Priority | Location | Content Type |
|----------|----------|--------------|
| 1 (Best prose) | `Book/Source Material/Tidbits/` | 113 Substack posts - polished writing |
| 2 (Working draft) | `Book/v3_new_draft/` | Current revision drafts |
| 3 (Structure ref) | `Book/Source Material/v1_original_draft/` | Original chapters - topic coverage |

Use Grep with:
```
pattern: term1|term2|term3
output_mode: content
-C: 2 (context lines)
-n: true (line numbers)
-i: true (case insensitive)
```

### Step 3: Return Results

Format results as:

```markdown
## Search Results: "[query]"

### From Tidbits (Canonical)
**[filename]** (line X)
> Matching passage with context...

### From v3_new_draft (Working)
**[filename]** (line X)
> Matching passage with context...

### From v1_original (Reference)
**[filename]** (line X)
> Matching passage with context...
```

### Step 4: Synthesize (Optional)

If user asks for synthesis or there are many results, use the `gemini-writer` skill to:
- Summarize what was written about the topic
- Note which sources have the best treatment
- Identify gaps or contradictions

---

## Example Queries

- "What did I write about replacement habits?"
- "Find mentions of the four types of monks"
- "Where do I discuss epiousios bread?"
- "What have I written about autophagy?"
- "Find all St. Benedict quotes"

---

## Search Paths (Absolute)

```
/Users/charliedeist/Desktop/New Root Docs/Personal/Benedict Challenge/Book/Source Material/Tidbits/
/Users/charliedeist/Desktop/New Root Docs/Personal/Benedict Challenge/Book/v3_new_draft/
/Users/charliedeist/Desktop/New Root Docs/Personal/Benedict Challenge/Book/Source Material/v1_original_draft/
```

---

## Notes

- Corpus: 239 markdown files, 3.1MB total
- All content fits easily in Gemini's 1M token context if synthesis needed
- Tidbits are MORE canonical than original chapters (user's polished Substack writing)
