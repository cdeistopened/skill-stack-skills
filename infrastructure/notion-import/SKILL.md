---
name: notion-import
description: >-
  Import Notion workspaces into Obsidian vaults and process results into usable structure.
  Covers API export setup, landscape mapping, routing decisions, and cleanup.
  Use when migrating content from Notion or processing a Notion export.
---

# Notion Import Skill

Guide for importing Notion workspaces into an Obsidian vault and processing the results into a usable structure.

---

## Phase 1: Export from Notion

### Method: API Import (Recommended)

**Why API over ZIP:** API import preserves Notion Databases as Obsidian `.base` files. ZIP/HTML import loses all database structure — you get flat markdown only.

### Setup Steps

1. **Create Notion Integration Token**
   - Go to [Notion Integrations](https://www.notion.so/my-integrations)
   - New integration → name it (e.g., "Personal Export")
   - Choose the workspace to export
   - Save → copy the `ntn_...` token
   - In the **Access** tab → Edit access → add all pages/databases you want

2. **Run Obsidian Importer**
   - Settings → Community Plugins → install/enable **Importer**
   - Open Importer (Cmd+P → "Importer" or ribbon icon)
   - File format: **Notion (API)**
   - Paste API token
   - Click **Load** to pull page/database list
   - Select what to import
   - **Set output folder to a staging directory** (e.g., `Project/notion-import/`) — never import directly into your working folders
   - Click Import, wait

### What You Get

- **Regular pages** → `.md` files with `notion-id` in frontmatter
- **Database items** → `.md` files with frontmatter containing all database properties + `base: "[[DatabaseName.base]]"` link
- **Databases** → `.base` files (Obsidian's native database format) with filters, properties, and view definitions
- **Folder structure** → mirrors Notion's page hierarchy (parent pages become folders)

### Known Limitations (API Import)

- Only the **primary view** per database is imported (alternate views lost)
- **Linked data sources** not imported (Notion API limitation)
- `People` functions (`name()`, `email()`) not available
- `Text` functions (`style()`, `unstyle()`) not available
- **Rate limits** make large workspaces slow — 1500 files can take 10-30+ minutes
- Emoji-prefixed page names become emoji-prefixed folder names (e.g., `📦 Archive/`)

### Frontmatter Structure (Database Items)

```yaml
---
notion-id: 1d0be9d0-0a42-808f-9795-d946fcdc690a
base: "[[DatabaseName.base]]"
Property Name: value
Another Property: value
Sub-item: []
Parent item:
  - notion-id-of-parent
---
```

### .base File Structure

```
# Database Name

filters:
  and:
    - note["base"] == link("DatabaseName.base")
properties:
  file.name:
    displayName: Name
  Property1:
    displayName: Property 1
views:
  - type: table
    name: Table View
    order:
      - file.name
      - Property1
```

---

## Phase 2: Landscape Mapping

After import completes, you need to understand what you have before routing anything.

### Step 1: Census

Run a structural census to understand the shape of the import:

```bash
# Total file count
find "path/to/notion-import/" -type f | wc -l

# File types breakdown
find "path/to/notion-import/" -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn

# Database (.base) files — these are the structured data
find "path/to/notion-import/" -name "*.base"

# Top-level folder structure (Notion's page hierarchy)
ls -la "path/to/notion-import/"

# Deepest nesting
find "path/to/notion-import/" -type f | awk -F/ '{print NF-1}' | sort -rn | head -5
```

### Step 2: Database Inventory

Each `.base` file represents a Notion database. Read each one to understand:
- What properties/columns it has
- How many items belong to it (grep for files with `base: "[[ThatDatabase.base]]"`)
- Whether it maps to an existing system (content calendar, task tracker, etc.)

### Step 3: Content Categorization

Map top-level folders to their destination:
- **Archive/junk** → delete or quarantine
- **Active projects** → merge with existing project folders
- **Reference material** → route to appropriate project
- **Databases worth keeping** → preserve `.base` files and their items together

---

## Phase 3: Processing & Routing

### Approach Options

**Option A: Manual audit (small imports, <100 files)**
Read through folders, move things where they belong.

**Option B: Agent team (large imports, 500+ files)**
Use subagents to parallelize the landscape mapping:
- Agent 1: Census + database inventory
- Agent 2: Read frontmatter of all database items, categorize by base
- Agent 3: Read top-level pages, summarize content
- Coordinator: builds routing map from agent findings

**Option C: QMD indexing (very large imports, searchable archive)**
Index all imported markdown into QMD for full-text + semantic search. Good when you need to query across the import rather than just route it.

### Routing Decisions

For each top-level folder/database, decide:
1. **Merge** — content maps to an existing project folder → move files there
2. **Keep** — valuable standalone content → rename/reorganize in place
3. **Archive** — old but might be useful → move to an archive folder
4. **Delete** — junk, duplicates, empty pages → remove

### Edge Cases & Gotchas

<!-- This section will be populated as we discover issues during the actual import -->

- **Emoji folder names**: Notion uses emoji prefixes heavily. These work in Obsidian but can cause issues with CLI tools and scripts.
- **"Untitled" databases**: Notion allows unnamed databases — these import as `Untitled/Untitled.base`, making identification harder. Check the properties and items to understand what they are.
- **Notion AI summaries in frontmatter**: If Notion AI was used, database items may have an `AI summary` property — this can actually be useful for quick triage.
- **Parent-child references by notion-id**: Parent/sub-item relations use raw Notion IDs, not wikilinks. These may need conversion if you want Obsidian graph connections.
- **Duplicate content**: Pages that appear in multiple Notion databases may import multiple times.

---

## Phase 4: Cleanup & Integration

### After Routing

- Delete the staging `notion-import/` folder once everything is routed
- Update project CLAUDE.md files if new content was added
- Create task files for any follow-up work discovered during audit
- If databases were preserved as `.base` files, verify they work in Obsidian's Base view

### Repeat for Additional Workspaces

Each Notion workspace needs its own integration token. Import one at a time to keep things manageable. The second import benefits from lessons learned on the first.

---

## Session Log

### Import 1: Creative Intelligence Agency (Personal Notion)
- **Date**: 2026-02-28
- **Token**: Created, all pages shared
- **Target folder**: `Creative Intelligence Agency/Notion/`
- **File count**: ~1500 expected
- **Status**: Import in progress
- **Observations**:
  - First files to land: `Podcast Name for Guests/`, `📦 Archive/`, loose pages
  - Archive contains old Ray Peat book drafts (Bioenergetic Tiger, PUFA chapter, etc.) — likely maps to existing `wiki-projects/` content
  - `.base` file found for an unnamed database with AI summary, Sub-item, Parent item columns
  - Database items include `notion-id` in frontmatter — good for dedup
  - Emoji prefixed folders confirmed (📦 Archive)
