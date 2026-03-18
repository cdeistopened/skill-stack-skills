"""
Extract insights from a corpus using LLM.

Supports multiple backends:
- Gemini (recommended - free tier, fast)
- Claude API
- Ollama (local)

Usage:
    # With Gemini (default)
    export GEMINI_API_KEY=your_key
    python extract_insights.py --db corpus.db --backend gemini

    # With Claude
    export ANTHROPIC_API_KEY=your_key
    python extract_insights.py --db corpus.db --backend claude
"""

import sqlite3
import json
import argparse
import re
import time
from pathlib import Path
from datetime import datetime
from typing import Optional

# ============================================================================
# EXTRACTION PROMPT - MODIFY THIS FOR YOUR PROJECT
# ============================================================================

EXTRACTION_PROMPT = """You are an insight extractor analyzing essays from *The Cross & The Plough* (1936-1946), a Catholic agrarian magazine advocating Distributism and land reform.

Your job is to identify genuinely insightful passages — ideas that challenge industrial modernity, reveal forgotten wisdom about land/family/craft, or articulate Catholic social principles in memorable ways.

## What IS an insight (high bar):

An insight must be SPECIFIC + NON-OBVIOUS + MEMORABLE.

EXAMPLES OF GENUINE INSIGHTS:
- "The mechanisation of life is the Beelzebub of our demons, but nowhere is it suggested how he is to be destroyed" — Names the core problem with striking imagery
- "Communism did not spring full-armed from Hell. It arose by way of reaction against the Hell of Industrial Capitalism" — Counterintuitive framing that challenges partisan thinking
- "The peasant owning his land, the fisherman owning his boat, though obliged to work hard, are nevertheless masters of themselves and of their time" — Crystallizes the Distributist vision

## What is NOT an insight:

NOT INSIGHTS — too generic:
- "We should return to the land" — Everyone in this magazine says this
- "Industrialism is bad" — Too obvious for this audience
- "Property is important" — Needs specific articulation

NOT INSIGHTS — just facts or descriptions:
- "The magazine was published quarterly" — Biographical, not insight
- "Fr. McNabb wore boots" — Anecdote without principle

## Calibration:

Ask: "Would a modern reader interested in Distributism/agrarianism find this passage quotable, memorable, or paradigm-shifting?"
- Already obvious to anyone reading this magazine? → NO_INSIGHT
- A striking articulation of a deeper truth? → INSIGHT

## Instructions:

If the excerpt contains a genuine insight, respond with EXACTLY this format:

INSIGHT: [The core claim in 1-2 sentences. Must stand alone without context.]
NOVELTY: [1-10] How surprising or counter-cultural is this? (7+ = challenges modern assumptions)
SPECIFICITY: [1-10] How concrete and quotable? (7+ = memorable phrasing)
CATEGORY: [One of: industrialism, land, family, property, craft, liturgy, organic-farming, distributism, eugenics, totalitarianism, natural-law, peasantry, enclosure, urbanization, economics, spirituality, education, other]
CONTEXT: [Brief note on why this matters - what modern assumption does it challenge?]

If NO genuine insight exists, respond ONLY with:
NO_INSIGHT

## Excerpt from {source}:
{chunk_text}"""


# ============================================================================
# LLM BACKENDS
# ============================================================================

def get_gemini_response(prompt: str, api_key: str, model: str = "gemini-2.0-flash") -> str:
    """Call Gemini API."""
    import google.generativeai as genai

    genai.configure(api_key=api_key)
    model_instance = genai.GenerativeModel(model)

    response = model_instance.generate_content(
        prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,
            max_output_tokens=500,
        )
    )
    return response.text


def get_claude_response(prompt: str, api_key: str) -> str:
    """Call Claude API (Haiku for cost efficiency)."""
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    message = client.messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text


def get_ollama_response(prompt: str, model: str = "qwen2.5:7b") -> str:
    """Call local Ollama instance."""
    import requests

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    return response.json()["response"]


# ============================================================================
# PARSING
# ============================================================================

def parse_response(response_text: str, chunk: dict) -> dict:
    """Parse LLM response into structured result."""
    result = {
        "chunk_id": chunk["id"],
        "document_id": chunk["document_id"],
        "source": chunk["title"],
        "year": chunk.get("year", 0),
        "has_insight": False,
        "insight": None,
        "raw_response": response_text,
    }

    if "NO_INSIGHT" in response_text.upper():
        return result

    try:
        insight_text = ""
        novelty = 5
        specificity = 5
        category = "other"
        context = ""

        for line in response_text.split("\n"):
            line = line.strip()
            if line.upper().startswith("INSIGHT:"):
                insight_text = line[8:].strip()
            elif line.upper().startswith("NOVELTY:"):
                match = re.search(r'(\d+)', line)
                if match:
                    novelty = int(match.group(1))
            elif line.upper().startswith("SPECIFICITY:"):
                match = re.search(r'(\d+)', line)
                if match:
                    specificity = int(match.group(1))
            elif line.upper().startswith("CATEGORY:"):
                category = line[9:].strip().lower().replace(" ", "-")
            elif line.upper().startswith("CONTEXT:"):
                context = line[8:].strip()

        # Filter template copies and low-quality
        is_template = "[The core claim" in insight_text or len(insight_text) < 20

        if insight_text and not is_template:
            result["has_insight"] = True
            result["insight"] = {
                "chunk_id": chunk["id"],
                "document_id": chunk["document_id"],
                "source": chunk["title"],
                "year": chunk.get("year", 0),
                "insight_text": insight_text,
                "novelty_score": novelty,
                "specificity_score": specificity,
                "category": category,
                "context": context,
                "raw_chunk": chunk["content"],
            }

    except Exception as e:
        result["error"] = str(e)

    return result


# ============================================================================
# MAIN
# ============================================================================

def load_chunks(db_path: Path, limit: int = 0) -> list[dict]:
    """Load chunks from database."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    query = """
        SELECT c.id, c.document_id, c.content, c.chunk_index,
               d.title, d.year, d.filename
        FROM chunks c
        JOIN documents d ON c.document_id = d.id
        ORDER BY d.year, c.chunk_index
    """

    if limit > 0:
        query += f" LIMIT {limit}"

    cursor.execute(query)
    chunks = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return chunks


def main():
    parser = argparse.ArgumentParser(description="Extract insights from corpus")
    parser.add_argument("--db", required=True, help="SQLite database path")
    parser.add_argument("--backend", choices=["gemini", "claude", "ollama"], default="gemini")
    parser.add_argument("--limit", type=int, default=0, help="Limit chunks (0=all)")
    parser.add_argument("--dry-run", action="store_true", help="Show prompts only")
    parser.add_argument("--batch-size", type=int, default=10, help="Save every N chunks")
    parser.add_argument("--output-dir", default="data", help="Output directory")
    args = parser.parse_args()

    print("Invisible Threads - Insight Extractor")
    print("=" * 50)

    # Load chunks
    db_path = Path(args.db)
    print(f"\nLoading chunks from {db_path}...")
    chunks = load_chunks(db_path, args.limit)
    print(f"Loaded {len(chunks)} chunks")

    if args.dry_run:
        print("\n--- DRY RUN: Sample prompt ---")
        sample = chunks[0] if chunks else {"content": "Sample", "title": "Test"}
        prompt = EXTRACTION_PROMPT.format(
            source=sample.get("title", "Unknown"),
            chunk_text=sample.get("content", "")[:500]
        )
        print(prompt[:2000] + "...")
        return

    # Setup backend
    import os

    if args.backend == "gemini":
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("ERROR: Set GEMINI_API_KEY environment variable")
            return

        # Import and test
        try:
            import google.generativeai as genai
        except ImportError:
            print("Installing google-generativeai...")
            import subprocess
            subprocess.check_call(["pip", "install", "google-generativeai"])
            import google.generativeai as genai

        get_response = lambda p: get_gemini_response(p, api_key)
        print("Using Gemini API (gemini-2.0-flash)")

    elif args.backend == "claude":
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("ERROR: Set ANTHROPIC_API_KEY environment variable")
            return
        get_response = lambda p: get_claude_response(p, api_key)
        print("Using Claude API (Haiku)")

    else:
        get_response = get_ollama_response
        print("Using Ollama (local)")

    # Create output directory
    output_dir = Path(args.output_dir)
    output_dir.mkdir(exist_ok=True)
    output_file = output_dir / f"insights_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    # Process chunks
    results = []
    insights_found = 0
    errors = 0
    start_time = time.time()

    for i, chunk in enumerate(chunks):
        prompt = EXTRACTION_PROMPT.format(
            source=chunk["title"],
            chunk_text=chunk["content"]
        )

        try:
            response = get_response(prompt)
            result = parse_response(response, chunk)
            results.append(result)

            if result["has_insight"]:
                insights_found += 1
                ins = result["insight"]
                print(f"  [{i+1}/{len(chunks)}] ✓ INSIGHT [{ins['category']}]: {ins['insight_text'][:50]}...")
            else:
                print(f"  [{i+1}/{len(chunks)}] - no insight")

        except Exception as e:
            errors += 1
            print(f"  [{i+1}/{len(chunks)}] ✗ ERROR: {e}")
            results.append({"chunk_id": chunk["id"], "error": str(e), "has_insight": False})

        # Save progress
        if (i + 1) % args.batch_size == 0:
            elapsed = time.time() - start_time
            rate = (i + 1) / elapsed
            eta = (len(chunks) - i - 1) / rate if rate > 0 else 0

            print(f"\n  --- Progress: {i+1}/{len(chunks)} | {insights_found} insights | {rate:.1f} chunks/sec | ETA: {eta/60:.1f}min ---\n")

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump({
                    "metadata": {
                        "timestamp": datetime.now().isoformat(),
                        "backend": args.backend,
                        "chunks_processed": len(results),
                        "insights_found": insights_found,
                        "in_progress": True,
                    },
                    "results": results
                }, f, indent=2, ensure_ascii=False)

        # Rate limiting (Gemini has generous limits but be polite)
        time.sleep(0.05)

    # Final save
    elapsed = time.time() - start_time

    final_data = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "backend": args.backend,
            "database": str(db_path),
            "chunks_processed": len(results),
            "insights_found": insights_found,
            "errors": errors,
            "extraction_rate": f"{insights_found/len(results)*100:.1f}%" if results else "0%",
            "elapsed_seconds": round(elapsed, 1),
        },
        "results": results
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(final_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'=' * 50}")
    print("EXTRACTION COMPLETE")
    print(f"{'=' * 50}")
    print(f"Chunks processed: {len(results)}")
    print(f"Insights found: {insights_found} ({insights_found/len(results)*100:.1f}%)")
    print(f"Errors: {errors}")
    print(f"Time: {elapsed:.1f}s ({elapsed/60:.1f} min)")
    print(f"Output: {output_file}")


if __name__ == "__main__":
    main()
