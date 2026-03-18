---
name: obsidian-markdown
description: >-
  Reference for Obsidian-specific markdown syntax beyond standard CommonMark — wikilinks,
  callouts, embeds, properties, dataview, and templater. Use when creating or editing
  files intended for the Obsidian vault.
---

# Obsidian Markdown Extensions

Reference for Obsidian-specific markdown syntax beyond standard CommonMark. Use when creating or editing files intended for the Obsidian vault.

---

## Properties (Frontmatter)

YAML block at file start, delimited by `---`. Obsidian reads these as typed properties.

```yaml
---
title: My Note
date: 2026-03-01
tags:
  - project/alpha
  - status/active
status: in_progress
aliases:
  - Alt Name
cssclasses:
  - wide-page
---
```

**Property types:** text, number, checkbox, date, datetime, list, tags
**Reserved properties:** `tags`, `aliases`, `cssclasses`

---

## Internal Links (Wikilinks)

```markdown
[[Note Name]]                    # Link to note
[[Note Name|Display Text]]       # Link with alias
[[Note Name#Heading]]            # Link to heading
[[Note Name#^block-id]]          # Link to block
[[Note Name#Heading|Display]]    # Heading link with alias
```

**Embeds** — prefix with `!` to render inline:
```markdown
![[Note Name]]                   # Embed entire note
![[Note Name#Heading]]           # Embed section
![[image.png]]                   # Embed image
![[image.png|300]]               # Embed image with width
![[audio.mp3]]                   # Embed audio player
![[video.mp4]]                   # Embed video player
![[document.pdf]]                # Embed PDF
![[document.pdf#page=3]]         # Embed specific PDF page
```

---

## Block References

Add a `^block-id` at the end of any block (paragraph, list item, etc.):

```markdown
This is a paragraph I want to reference. ^my-block

- List item with reference ^list-ref
```

Link to it: `[[Note Name#^my-block]]`
Embed it: `![[Note Name#^my-block]]`

Block IDs: lowercase letters, numbers, hyphens. Obsidian auto-generates 6-char hex IDs when you type `^` in the link autocomplete.

---

## Tags

```markdown
#tag                    # Simple tag
#nested/tag             # Nested tag (creates hierarchy)
#project/alpha          # Convention: category/value
```

Tags work in body text and in `tags:` frontmatter property. Nested tags create browsable hierarchies in the tag pane.

---

## Callouts

```markdown
> [!note] Optional Title
> Callout body content.

> [!warning]
> No title — uses type name as title.

> [!tip]- Foldable (collapsed by default)
> Content hidden until expanded.

> [!tip]+ Foldable (expanded by default)
> Content visible, can be collapsed.
```

**Built-in types:** note, abstract/summary/tldr, info, todo, tip/hint/important, success/check/done, question/help/faq, warning/caution/attention, failure/fail/missing, danger/error, bug, example, quote/cite

**Nesting:** Callouts can nest inside each other with additional `>` levels.

---

## Comments

```markdown
%%This text is invisible in reading view%%

%%
Multi-line comments
also work
%%
```

---

## Footnotes

```markdown
Here is a sentence with a footnote.[^1]

[^1]: This is the footnote content.

Inline footnote^[This is inline footnote content].
```

---

## Math (LaTeX)

```markdown
Inline: $E = mc^2$

Block:
$$
\sum_{i=1}^{n} x_i = x_1 + x_2 + \cdots + x_n
$$
```

---

## Tables (Standard + Extended)

```markdown
| Left | Center | Right |
|:-----|:------:|------:|
| a    |   b    |     c |
```

---

## Task Lists

```markdown
- [ ] Unchecked
- [x] Checked
- [/] In progress (community convention)
- [-] Cancelled (community convention)
```

---

## Highlights and Formatting

```markdown
==highlighted text==          # Yellow highlight
**bold** and *italic*         # Standard
~~strikethrough~~             # Standard
`inline code`                 # Standard
```

---

## Best Practices for This Vault

1. **Always use wikilinks** (`[[Note]]`) not markdown links for internal vault links
2. **Frontmatter on every file** — at minimum: `title`, `date`, `tags`
3. **Use nested tags** for categorization: `#status/active`, `#project/opened`, `#type/podcast`
4. **Block references** for granular linking — better than duplicating content
5. **Aliases** for notes with multiple names (e.g., person's full name + first name)
6. **Callouts** for important information, warnings, or collapsible sections
7. **Comments** (`%%...%%`) for Claude-only notes that shouldn't render in Obsidian
