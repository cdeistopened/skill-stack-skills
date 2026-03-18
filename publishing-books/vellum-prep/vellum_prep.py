#!/usr/bin/env python3
"""
Vellum Prep: Clean markdown manuscripts for Vellum import.

Converts markdown → clean markdown → Word .docx
All programmatic - no AI tokens burned.

Usage:
    python3 vellum_prep.py manuscript.md [output.md]
"""

import re
import sys
import subprocess
from pathlib import Path


# =============================================================================
# Configuration - customize per book
# =============================================================================

# Patterns for running headers to remove (case-insensitive)
HEADER_PATTERNS = [
    r'^THE CRUISE OF THE "?NONA"?\s*$',
    r'^CRUISE OF THE "?NONA"?\s*$',
    # Add more patterns for other books:
    # r'^YOUR BOOK TITLE\s*$',
]

# Roman numeral to Arabic conversion
ROMAN_MAP = {
    'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
    'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10,
    'XI': 11, 'XII': 12, 'XIII': 13, 'XIV': 14, 'XV': 15,
    'XVI': 16, 'XVII': 17, 'XVIII': 18, 'XIX': 19, 'XX': 20,
    'XXI': 21, 'XXII': 22, 'XXIII': 23, 'XXIV': 24, 'XXV': 25,
}


# =============================================================================
# Core Functions
# =============================================================================

def remove_metadata_header(text: str) -> str:
    """Remove OCR metadata header (everything before first ---)."""
    match = re.search(r'^---\s*$', text, re.MULTILINE)
    if match:
        return text[match.end():].lstrip('\n')
    return text


def normalize_section_breaks(text: str) -> str:
    """Convert --- to *** for Vellum ornamental breaks."""
    return re.sub(r'^---\s*$', '***', text, flags=re.MULTILINE)


def remove_duplicate_headers(text: str, patterns: list = None) -> str:
    """Remove lines that are just repeated headers/titles."""
    if patterns is None:
        patterns = HEADER_PATTERNS

    lines = text.split('\n')
    cleaned = []
    for line in lines:
        is_header = any(
            re.match(p, line.strip(), re.IGNORECASE)
            for p in patterns
        )
        if not is_header:
            cleaned.append(line)

    return '\n'.join(cleaned)


def clean_artifacts(text: str, remove_images: bool = True) -> str:
    """Remove common OCR artifacts."""
    # Remove standalone page numbers
    text = re.sub(r'^\d{1,3}\s*$', '', text, flags=re.MULTILINE)

    # Remove standalone ellipses
    text = re.sub(r'^\.\.\.\s*$', '', text, flags=re.MULTILINE)

    # Fix hyphenated words split across lines
    text = re.sub(r'(\w)-\n(\w)', r'\1\2', text)

    # Collapse excessive blank lines
    text = re.sub(r'\n{4,}', '\n\n\n', text)

    # Remove [Image: ...] descriptions
    if remove_images:
        text = re.sub(r'\[Image:[^\]]*\]\n*', '', text)

    return text


def normalize_chapters(text: str) -> str:
    """
    Normalize chapter headings to Vellum format: # Chapter X: Title
    Converts Roman numerals to Arabic.
    """
    def replace_chapter(match):
        prefix = match.group(1) or ''  # ## or #
        numeral = match.group(2)  # Roman or Arabic
        title = match.group(3) or ''  # Title matches the rest of the line

        # Convert Roman to Arabic
        if numeral.upper() in ROMAN_MAP:
            num = ROMAN_MAP[numeral.upper()]
        else:
            try:
                num = int(numeral)
            except ValueError:
                num = numeral

        # Build new heading
        if title.strip():
            # Title case the title if it's ALL CAPS
            if title.isupper():
                title = title.title()
            return f'# Chapter {num}: {title.strip()}'
        else:
            return f'# Chapter {num}'

    # Match patterns like: ## CHAPTER I. THE HARBOR
    pattern = r'^(#{1,2}\s*)?CHAPTER\s+([IVXLC]+|\d+)\.?\s*[-:.]?\s*(.*)$'
    text = re.sub(pattern, replace_chapter, text, flags=re.MULTILINE | re.IGNORECASE)

    return text


def remove_publisher_frontmatter(text: str) -> str:
    """Remove publisher catalog and copyright boilerplate."""
    # Common patterns - customize as needed
    patterns = [
        # Publisher catalogs
        (r'### CONSTABLE\'S MISCELLANY.*?(?=# )', ''),
        # Copyright blocks
        (r'First Published.*?(?:TONBRIDGE|PRINTED IN).*?\n*\*\*\*\n*', ''),
    ]

    for pattern, replacement in patterns:
        text = re.sub(pattern, replacement, text, flags=re.DOTALL | re.IGNORECASE)

    return text


def format_titles(text: str) -> str:
    """Format title and author for Vellum."""
    # Convert ALL CAPS titles to Title Case
    def title_case_heading(match):
        hashes = match.group(1)
        title = match.group(2)
        if title.isupper() and len(title) > 3:
            title = title.title()
        return f'{hashes} {title}'

    text = re.sub(r'^(#{1,3})\s+([A-Z][A-Z\s]+)$', title_case_heading, text, flags=re.MULTILINE)

    return text


# =============================================================================
# Main Processing
# =============================================================================

def process_file(
    input_path: str,
    output_path: str = None,
    clean_for_vellum: bool = True,
    convert_to_docx: bool = True,
) -> dict:
    """
    Process a markdown file for Vellum.

    Args:
        input_path: Path to input markdown file
        output_path: Path for output (default: input_vellum.md)
        clean_for_vellum: Apply Vellum-specific formatting
        convert_to_docx: Also create .docx via pandoc

    Returns:
        dict with paths and stats
    """
    input_path = Path(input_path)
    if output_path is None:
        output_path = input_path.parent / f"{input_path.stem}_vellum.md"
    else:
        output_path = Path(output_path)

    print(f"Reading: {input_path.name}")
    text = input_path.read_text(encoding='utf-8')
    original_len = len(text)

    # Step 1: Remove OCR metadata header
    text = remove_metadata_header(text)
    print("  [1] Removed metadata header")

    # Step 2: Normalize section breaks
    text = normalize_section_breaks(text)
    print("  [2] Normalized section breaks (--- → ***)")

    # Step 3: Remove duplicate headers
    text = remove_duplicate_headers(text)
    print("  [3] Removed duplicate headers")

    # Step 4: Clean artifacts
    text = clean_artifacts(text, remove_images=True)
    print("  [4] Cleaned artifacts")

    if clean_for_vellum:
        # Step 5: Remove publisher front matter
        text = remove_publisher_frontmatter(text)
        print("  [5] Removed publisher front matter")

        # Step 6: Normalize chapters
        text = normalize_chapters(text)
        print("  [6] Normalized chapter headings")

        # Step 7: Format titles
        text = format_titles(text)
        print("  [7] Formatted titles")

    # Final cleanup
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = text.strip() + '\n'

    # Write markdown output
    output_path.write_text(text, encoding='utf-8')
    final_len = len(text)

    result = {
        'input': str(input_path),
        'markdown': str(output_path),
        'original_chars': original_len,
        'final_chars': final_len,
        'removed_chars': original_len - final_len,
    }

    print(f"\nOutput: {output_path.name}")
    print(f"  Original: {original_len:,} chars")
    print(f"  Final:    {final_len:,} chars")
    print(f"  Removed:  {original_len - final_len:,} chars")

    # Convert to .docx
    if convert_to_docx:
        docx_path = output_path.with_suffix('.docx')
        try:
            subprocess.run([
                'pandoc',
                str(output_path),
                '-o', str(docx_path),
                '--from', 'markdown',
                '--to', 'docx'
            ], check=True, capture_output=True)
            result['docx'] = str(docx_path)
            print(f"  Word:     {docx_path.name}")
        except FileNotFoundError:
            print("  [!] pandoc not found - skipping .docx conversion")
        except subprocess.CalledProcessError as e:
            print(f"  [!] pandoc error: {e.stderr.decode()}")

    return result


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Vellum Prep - Convert markdown to Vellum-ready Word documents")
        print()
        print("Usage: python3 vellum_prep.py <input.md> [output.md]")
        print()
        print("Options are configured in the script. Edit HEADER_PATTERNS")
        print("to customize which repeated headers to remove.")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None

    result = process_file(input_file, output_file)

    if 'docx' in result:
        print(f"\nReady for Vellum: {result['docx']}")
