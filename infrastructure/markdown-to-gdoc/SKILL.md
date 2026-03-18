# Markdown to Google Doc

Create formatted Google Docs from markdown files using pandoc and the gws CLI.

## When to Use

When you need to push a markdown file to Google Drive as a properly formatted Google Doc — for team review, client sharing, or collaboration.

## Prerequisites

- `pandoc` installed (`brew install pandoc`)
- `gws` CLI authenticated (see memory for gws setup)
- For cdeist@opened.co: use `gws-opened` (shell function in ~/.zshrc)
- For chdeist@gmail.com: use `gws` (default profile)

## Pipeline

```
Markdown → pandoc → .docx → Drive upload → files.copy (converts to Google Doc) → cleanup
```

### Why This Pipeline

- Google Docs API `documents.create` only creates blank docs — you'd need hundreds of `batchUpdate` requests for formatting
- Google Drive API doesn't support direct markdown upload
- pandoc markdown → docx preserves headings, bold, italic, links, lists, and tables
- `files.copy` with `mimeType: application/vnd.google-apps.document` triggers Google's native docx-to-Doc conversion

## Steps

### 1. Convert Markdown to DOCX

```bash
pandoc "input.md" \
  -f markdown-auto_identifiers \
  -t docx \
  --reference-doc="path/to/reference.docx" \
  -o /tmp/output.docx
```

**Key flags:**
- `-f markdown-auto_identifiers` — disables automatic header IDs, which prevents bookmark anchors on every heading in the output
- `--reference-doc` — optional, applies custom fonts/styles from a template docx (e.g., Arial instead of Calibri)

### 2. Upload DOCX to Drive

```bash
UPLOAD=$(gws-opened drive files create \
  --json '{"name":"temp-upload.docx","parents":["FOLDER_ID"]}' \
  --upload /tmp/output.docx)
TEMP_ID=$(echo "$UPLOAD" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
```

### 3. Copy with Conversion

```bash
COPY=$(gws-opened drive files copy \
  --params "{\"fileId\":\"$TEMP_ID\"}" \
  --json "{\"name\":\"Document Title\",\"mimeType\":\"application/vnd.google-apps.document\",\"parents\":[\"FOLDER_ID\"]}")
DOC_ID=$(echo "$COPY" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
echo "https://docs.google.com/document/d/$DOC_ID/edit"
```

The `mimeType: application/vnd.google-apps.document` in the copy request is what triggers the conversion. Without it, you get a raw .docx file in Drive.

### 4. Clean Up

```bash
gws-opened drive files delete --params "{\"fileId\":\"$TEMP_ID\"}" > /dev/null
```

## Batch Script

For multiple files in the same folder:

```bash
FOLDER_ID="your-folder-id"
REF_DOC="path/to/pandoc-reference.docx"  # optional

for MD_FILE in file1.md file2.md file3.md; do
  NAME=$(head -1 "$MD_FILE" | sed 's/^# //')  # Extract title from H1
  LOWER=$(basename "$MD_FILE" .md)
  DOCX="/tmp/${LOWER}.docx"

  # Convert
  pandoc "$MD_FILE" -f markdown-auto_identifiers -t docx --reference-doc="$REF_DOC" -o "$DOCX"

  # Upload temp
  TEMP_ID=$(gws-opened drive files create \
    --json "{\"name\":\"${LOWER}-temp.docx\",\"parents\":[\"$FOLDER_ID\"]}" \
    --upload "$DOCX" | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

  # Convert to Google Doc
  DOC_ID=$(gws-opened drive files copy \
    --params "{\"fileId\":\"$TEMP_ID\"}" \
    --json "{\"name\":\"$NAME\",\"mimeType\":\"application/vnd.google-apps.document\",\"parents\":[\"$FOLDER_ID\"]}" \
    | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")

  echo "$NAME: https://docs.google.com/document/d/$DOC_ID/edit"

  # Cleanup
  gws-opened drive files delete --params "{\"fileId\":\"$TEMP_ID\"}" > /dev/null
  rm "$DOCX"
done
```

## What Converts Well

- Headings (H1-H4) → Google Doc heading styles
- **Bold** and *italic* → preserved
- [Links](url) → clickable hyperlinks
- Bullet lists and numbered lists → native Google Doc lists
- Tables → Google Doc tables
- Blockquotes → indented paragraphs
- Code blocks → monospace font

## What Doesn't Convert

- `<details>`/`<summary>` HTML toggles → rendered as plain text (Google Docs has no native accordion)
- HTML comments (`<!-- -->`) → stripped by pandoc
- Markdown tables with complex formatting → may lose alignment
- Images referenced by URL → not embedded (would need separate upload)

## Gotchas

- **gws-opened is a shell function**, not a binary. You cannot call it from Python's `subprocess` — run it via Bash tool directly.
- **Bookmark anchors on headings**: pandoc adds automatic header identifiers that become bookmark icons in Google Docs. Fix: `-f markdown-auto_identifiers` removes them.
- **File lands in root**: If you omit `parents` in the JSON metadata, the file goes to the Drive root. Always specify the target folder ID.
- **Untitled docs**: If the `files.create` upload doesn't include a name in the JSON body, it creates "Untitled". The name goes in `--json`, not `--params`.

## Reference Docs

State pages reference doc (Arial fonts): `OpenEd Vault/Studio/SEO Content Production/State Pages/pandoc-reference.docx`

## Known Folder IDs

| Folder | ID | Account |
|--------|-------|---------|
| State Pages review folder | `1qmNKScfHridH0x6LXoGC7kEZuZkB5qOU` | cdeist@opened.co |
