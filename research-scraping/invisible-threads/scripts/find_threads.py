"""
Find invisible threads across Cross & Plough essays.

Uses topic extraction + embedding + Louvain clustering.
Runs entirely locally (no GPU required).

Usage:
    python find_threads.py --input ../data/insights_*.json
"""

import json
import argparse
import numpy as np
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import Optional

# Optional: use Claude for topic extraction, or do simple keyword extraction
USE_LLM_FOR_TOPICS = False  # Set True if you want higher quality topic extraction


def extract_topics_simple(insights: list[dict]) -> list[dict]:
    """
    Simple topic extraction without LLM.
    Uses the insight text + category as the topic representation.
    """
    topics = []
    for i, ins in enumerate(insights):
        topic = {
            "idx": i,
            "insight_text": ins["insight_text"],
            "topic": ins.get("category", "other"),
            "claim": ins["insight_text"][:100],
            "category": ins.get("category", "other"),
        }
        topics.append(topic)
    return topics


def extract_topics_llm(insights: list[dict], api_key: str) -> list[dict]:
    """
    Extract topics using Claude API for higher quality clustering.
    """
    import anthropic

    client = anthropic.Anthropic(api_key=api_key)
    topics = []

    TOPIC_PROMPT = """Extract the core TOPIC and CLAIM from this insight about Catholic agrarianism/Distributism.

## Rules:
1. TOPIC should be the underlying concept (5-10 words)
2. CLAIM should be the actionable principle (one sentence)

## Insight:
{insight}

## Respond with JSON:
{{"topic": "...", "claim": "...", "category": "one of: industrialism, land, family, property, craft, liturgy, organic-farming, distributism, eugenics, totalitarianism, natural-law, peasantry, economics, spirituality, other"}}"""

    for i, ins in enumerate(insights):
        try:
            response = client.messages.create(
                model="claude-3-5-haiku-latest",
                max_tokens=200,
                messages=[{"role": "user", "content": TOPIC_PROMPT.format(insight=ins["insight_text"])}]
            )
            text = response.content[0].text

            # Parse JSON from response
            import re
            json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
            if json_match:
                result = json.loads(json_match.group())
            else:
                result = {"topic": ins["insight_text"][:50], "claim": ins["insight_text"][:100], "category": "other"}

        except Exception as e:
            result = {"topic": ins["insight_text"][:50], "claim": ins["insight_text"][:100], "category": "other"}

        result["idx"] = i
        result["insight_text"] = ins["insight_text"]
        topics.append(result)

        if (i + 1) % 10 == 0:
            print(f"  Topic extraction: {i+1}/{len(insights)}")

    return topics


def build_similarity_graph(embeddings: np.ndarray, threshold: float = 0.5):
    """Build similarity graph from embeddings."""
    import networkx as nx
    from sklearn.metrics.pairwise import cosine_similarity

    sim_matrix = cosine_similarity(embeddings)

    G = nx.Graph()
    G.add_nodes_from(range(len(embeddings)))

    edge_count = 0
    for i in range(len(embeddings)):
        for j in range(i + 1, len(embeddings)):
            if sim_matrix[i, j] >= threshold:
                G.add_edge(i, j, weight=sim_matrix[i, j])
                edge_count += 1

    return G, sim_matrix


def find_communities(G, min_size: int = 2, resolution: float = 1.0):
    """Find communities using Louvain algorithm."""
    try:
        import community as community_louvain
    except ImportError:
        print("Installing python-louvain...")
        import subprocess
        subprocess.check_call(["pip", "install", "python-louvain"])
        import community as community_louvain

    # Only consider nodes with edges
    nodes_with_edges = [n for n in G.nodes() if G.degree(n) > 0]
    if len(nodes_with_edges) < min_size:
        return []

    subgraph = G.subgraph(nodes_with_edges)
    partition = community_louvain.best_partition(subgraph, resolution=resolution, random_state=42)

    # Group by community
    communities = defaultdict(set)
    for node, comm_id in partition.items():
        communities[comm_id].add(node)

    # Filter by min_size
    valid = [c for c in communities.values() if len(c) >= min_size]
    return sorted(valid, key=len, reverse=True)


def main():
    parser = argparse.ArgumentParser(description="Find invisible threads")
    parser.add_argument("--input", required=True, help="Input JSON from extract_insights.py")
    parser.add_argument("--threshold", type=float, default=0.5, help="Similarity threshold")
    parser.add_argument("--min-size", type=int, default=2, help="Min insights per thread")
    parser.add_argument("--min-sources", type=int, default=2, help="Min different source issues")
    parser.add_argument("--resolution", type=float, default=1.0, help="Louvain resolution")
    parser.add_argument("--use-llm", action="store_true", help="Use LLM for topic extraction")
    args = parser.parse_args()

    print("Cross & Plough Thread Finder")
    print("=" * 40)

    # Load insights
    print(f"\nLoading insights from {args.input}...")
    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    insights = [r["insight"] for r in data["results"] if r.get("has_insight") and r.get("insight")]
    print(f"Loaded {len(insights)} insights")

    if len(insights) < 5:
        print("ERROR: Need at least 5 insights to find threads")
        return

    # === STEP 1: Extract topics ===
    print(f"\n{'=' * 40}")
    print("STEP 1: Extracting topics")
    print("=" * 40)

    if args.use_llm:
        import os
        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            print("WARNING: No API key, falling back to simple extraction")
            topics = extract_topics_simple(insights)
        else:
            topics = extract_topics_llm(insights, api_key)
    else:
        topics = extract_topics_simple(insights)

    print(f"Extracted {len(topics)} topics")

    # Sample
    print("\nSample topics:")
    for t in topics[:5]:
        print(f"  [{t.get('category', '?')}] {t.get('topic', t.get('claim', '')[:40])}")

    # === STEP 2: Embed topics ===
    print(f"\n{'=' * 40}")
    print("STEP 2: Embedding topics")
    print("=" * 40)

    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        print("Installing sentence-transformers...")
        import subprocess
        subprocess.check_call(["pip", "install", "sentence-transformers"])
        from sentence_transformers import SentenceTransformer

    model = SentenceTransformer("all-MiniLM-L6-v2")

    # Embed insight text (or topic+claim if LLM extracted)
    if args.use_llm:
        topic_texts = [f"{t.get('topic', '')} - {t.get('claim', '')}" for t in topics]
    else:
        topic_texts = [t["insight_text"] for t in topics]

    print(f"Embedding {len(topic_texts)} texts...")
    embeddings = model.encode(topic_texts, show_progress_bar=True)

    # === STEP 3: Build graph and find communities ===
    print(f"\n{'=' * 40}")
    print(f"STEP 3: Finding threads (threshold={args.threshold})")
    print("=" * 40)

    G, sim_matrix = build_similarity_graph(embeddings, threshold=args.threshold)

    nodes_with_edges = sum(1 for n in G.nodes() if G.degree(n) > 0)
    edges = G.number_of_edges()
    print(f"Graph: {len(topic_texts)} nodes, {edges} edges, {nodes_with_edges} connected")

    communities = find_communities(G, min_size=args.min_size, resolution=args.resolution)
    print(f"Found {len(communities)} communities with >= {args.min_size} insights")

    # === STEP 4: Filter by min_sources ===
    print(f"\n{'=' * 40}")
    print(f"STEP 4: Filtering by source diversity (>= {args.min_sources} sources)")
    print("=" * 40)

    threads = []
    skipped = 0

    for comm in communities:
        # Get insights in this community
        thread_insights = [insights[topics[idx]["idx"]] for idx in comm]
        thread_topics = [topics[idx] for idx in comm]

        # Count unique sources (different magazine issues)
        sources = list(set(ins.get("document_id", ins.get("source", "")) for ins in thread_insights))

        if len(sources) < args.min_sources:
            skipped += 1
            continue

        # Calculate coherence
        comm_list = list(comm)
        upper_tri = sim_matrix[np.ix_(comm_list, comm_list)][np.triu_indices(len(comm_list), k=1)]
        coherence = float(np.mean(upper_tri)) if len(upper_tri) > 0 else 1.0

        # Find dominant category
        categories = [t.get("category", "other") for t in thread_topics]
        dominant_cat = Counter(categories).most_common(1)[0][0]

        # Get years spanned
        years = sorted(set(ins.get("year", 0) for ins in thread_insights))

        threads.append({
            "thread_id": len(threads),
            "size": len(comm),
            "num_sources": len(sources),
            "years_spanned": years,
            "coherence": round(coherence, 3),
            "category": dominant_cat,
            "insights": thread_insights,
            "topics": thread_topics,
        })

    print(f"Valid threads: {len(threads)} (skipped {skipped} with < {args.min_sources} sources)")

    # Sort by source coverage
    threads.sort(key=lambda x: (x["num_sources"], x["size"]), reverse=True)

    # === Summary ===
    print(f"\n{'=' * 40}")
    print("RESULTS")
    print("=" * 40)

    total_in_threads = sum(t["size"] for t in threads)
    print(f"Threads found: {len(threads)}")
    print(f"Insights in threads: {total_in_threads}/{len(insights)} ({total_in_threads/len(insights)*100:.0f}%)")

    print(f"\nDiscovered Threads:")
    for t in threads:
        print(f"\n  Thread {t['thread_id']}: [{t['category']}] ({t['size']} insights, {t['num_sources']} sources, {t['years_spanned'][0]}-{t['years_spanned'][-1]})")
        print(f"    Sample insights:")
        for ins in t["insights"][:3]:
            print(f"      - \"{ins['insight_text'][:70]}...\"")

    # Save output
    output_dir = Path(args.input).parent
    output_file = output_dir / f"threads_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    output_data = {
        "metadata": {
            "timestamp": datetime.now().isoformat(),
            "input_file": args.input,
            "threshold": args.threshold,
            "min_size": args.min_size,
            "min_sources": args.min_sources,
            "total_insights": len(insights),
            "insights_in_threads": total_in_threads,
            "threads_found": len(threads),
        },
        "threads": threads,
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\nSaved to: {output_file}")


if __name__ == "__main__":
    main()
