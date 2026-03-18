---
name: obsidian-bases
description: >-
  Reference for creating Obsidian .base files — built-in database views that query vault files
  by frontmatter properties. Use when creating task dashboards, content indexes, filtered views,
  or any structured data display in Obsidian.
---

# Obsidian Bases

Reference for creating `.base` files — Obsidian's built-in database views that query vault files by frontmatter properties. Use for task dashboards, content indexes, and filtered views.

**Requires:** Bases core plugin enabled.

---

## File Format

A `.base` file is YAML. Place anywhere in the vault. Five top-level keys:

```yaml
filters:      # Scope and filter which files appear
formulas:     # Named computed properties
properties:   # Display config for each column
summaries:    # Aggregation formulas
views:        # Array of view definitions
```

**There is no `source:` key.** Bases always queries the entire vault. Use filters to scope to folders.

---

## Filters

Filters are YAML lists of **string expressions**. Logical grouping uses `and:`, `or:`, `not:` as keys.

### Folder Scoping
```yaml
filters:
  and:
    - 'file.inFolder("tasks")'           # Includes subfolders
    - 'file.folder == "tasks"'            # Exact folder only (no subfolders)
```

### Property Filters
```yaml
filters:
  and:
    - 'file.inFolder("tasks")'
    - 'status != "done"'
    - 'status != "later"'
    - 'priority == "critical"'
```

### Date Filters
```yaml
filters:
  and:
    - 'due < today()'                     # Overdue
    - 'due <= now() + "7d"'               # Due within 7 days
```

### Compound Filters
```yaml
filters:
  or:
    - and:
        - 'due == today()'
        - 'status != "done"'
    - 'status == "in_progress"'
```

### Other Filter Functions
- `file.hasTag("tag-name")` — files with a specific tag
- `file.hasLink("Note Name")` — files linking to a note
- `file.extension == "md"` — by file extension

**Operators:** `==`, `!=`, `<`, `<=`, `>`, `>=`, `contains()`, `startsWith()`, `endsWith()`

**Date functions:** `today()`, `now()`, `dateModify(date, "7 days")`

**Date arithmetic:** `now() + "7d"`, `today() - "30d"`

---

## Properties

Define which columns to display. Use **named keys** matching frontmatter fields.

```yaml
properties:
  file.name:
    displayName: Task
  status:
    displayName: Status
  priority:
    displayName: Priority
  due:
    displayName: Due Date
  assignee:
    displayName: Owner
  project:
    displayName: Project
```

**Built-in properties** (always available):
- `file.name` — filename without extension
- `file.path` — full path
- `file.created` — creation date
- `file.modified` — last modified date
- `file.size` — file size
- `file.folder` — parent folder

**Formula properties** use the `formula.` prefix:
```yaml
  formula.days_left:
    displayName: Days Left
```

---

## Formulas

Named computed columns defined at the top level.

```yaml
formulas:
  days_left: 'dateDiff(due, today(), "days")'
  urgency: |
    if(due == null, null,
      if(due < now(), "OVERDUE",
        if(due < now() + "7d", "THIS WEEK", "LATER")))
  display: 'file.name + " (" + status + ")"'
```

**Formula functions:**
- `now()` — current datetime
- `today()` — current date (no time)
- `dateDiff(date1, date2, unit)` — difference between dates ("days", "hours", etc.)
- `dateModify(date, duration)` — add duration to date
- `if(condition, then, else)` — conditional
- `contains(text, search)` — text search
- `format(value)` — convert to string
- `relative(date)` — human-readable relative time ("in 3 days", "2 days ago")
- `min()`, `max()`, `round()` — math
- Text: `+` (concat), `lower()`, `upper()`

**Reference properties directly by name** (not `prop("name")`):
- Correct: `due < now()`
- Wrong: `prop("due") < now()`

---

## Views

Array of view definitions. Multiple views create tabs.

### Table
```yaml
views:
  - type: table
    name: All Tasks
    order:
      - priority
      - due
      - file.name
```

### Cards (Kanban)
```yaml
views:
  - type: cards
    name: Kanban Board
    groupBy:
      property: status
      direction: ASC
    order:
      - priority
      - due
```

### Multiple Views
```yaml
views:
  - type: table
    name: Table View
    order:
      - due
  - type: cards
    name: Kanban
    groupBy:
      property: status
```

---

## Summaries

Aggregation for columns (shown at bottom).

```yaml
summaries:
  status: countBy
  effort: sum
  due: earliest
```

**Types:** `count`, `countBy`, `countEmpty`, `countNotEmpty`, `sum`, `average`, `min`, `max`, `range`, `earliest`, `latest`

---

## Complete Example: Task Dashboard

```yaml
filters:
  and:
    - 'file.inFolder("tasks")'
    - 'status != "done"'
    - 'status != "later"'

formulas:
  urgency: |
    if(due == null, 0,
      if(due < now(), "OVERDUE",
        if(due < now() + "7d", "THIS WEEK", "LATER")))

properties:
  file.name:
    displayName: Task
  status:
    displayName: Status
  priority:
    displayName: Priority
  assignee:
    displayName: Owner
  due:
    displayName: Due
  project:
    displayName: Project
  formula.urgency:
    displayName: Urgency

summaries:
  status: countBy
  due: earliest

views:
  - type: table
    name: Active Tasks
    order:
      - priority
      - due
  - type: cards
    name: Kanban
    groupBy:
      property: status
```

---

## Tips

1. **No `source:` key exists** — always use `filters:` with `file.inFolder()` to scope
2. **Properties use named keys**, not numbered ("0", "1") or arrays
3. **Formula references are bare names** (`due`, `status`), not `prop("due")`
4. **Views is always plural** (`views:` not `view:`) and an array
5. **Cards with `groupBy: status`** replicates a kanban board
6. **Date arithmetic** uses string durations: `now() + "7d"`, `today() - "30d"`
