#!/bin/bash
# Daily RSS curation wrapper script
SKILL_DIR="/Users/charliedeist/Desktop/New Root Docs/OpenEd Vault/.claude/skills/rss-curation"
OUTPUT_DIR="$SKILL_DIR/output"

mkdir -p "$OUTPUT_DIR"

# Run curation and save to dated file + latest.json
DATE=$(date +%Y-%m-%d)
python3 "$SKILL_DIR/curate.py" --json --days 1.5 > "$OUTPUT_DIR/$DATE.json" 2>"$OUTPUT_DIR/curation.log"
cp "$OUTPUT_DIR/$DATE.json" "$OUTPUT_DIR/latest.json"

echo "Curation complete: $OUTPUT_DIR/$DATE.json"
