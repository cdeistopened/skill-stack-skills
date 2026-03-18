#!/usr/bin/env python3
"""
LLM Council CLI - Query multiple LLMs, have them rank each other, synthesize a final answer.
Based on https://github.com/karpathy/llm-council

Usage: uv run --with httpx council.py "Your question here"
"""

import asyncio
import json
import os
import re
import sys
import time
from collections import defaultdict

import httpx

# --- Config ---

OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "")
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

COUNCIL_MODELS = [
    "openai/gpt-5.2",
    "google/gemini-3-pro-preview",
    "anthropic/claude-opus-4.6",
    "x-ai/grok-4",
]

CHAIRMAN_MODEL = "anthropic/claude-opus-4.6"

# Short display names
MODEL_NAMES = {
    "openai/gpt-5.2": "GPT-5.2",
    "openai/gpt-5.1": "GPT-5.1",
    "google/gemini-3-pro-preview": "Gemini 3 Pro",
    "anthropic/claude-opus-4.6": "Claude Opus 4.6",
    "anthropic/claude-sonnet-4.5": "Claude Sonnet 4.5",
    "x-ai/grok-4": "Grok 4",
    "google/gemini-2.5-flash": "Gemini 2.5 Flash",
}


def short_name(model: str) -> str:
    return MODEL_NAMES.get(model, model.split("/")[-1])


# --- API ---

async def query_model(client: httpx.AsyncClient, model: str, messages: list, timeout: float = 120.0) -> dict | None:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {"model": model, "messages": messages}
    try:
        response = await client.post(OPENROUTER_API_URL, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        return {"content": data["choices"][0]["message"].get("content", "")}
    except Exception as e:
        print(f"  [ERROR] {short_name(model)}: {e}", file=sys.stderr)
        return None


async def query_models_parallel(client: httpx.AsyncClient, models: list, messages: list) -> dict:
    tasks = [query_model(client, model, messages) for model in models]
    responses = await asyncio.gather(*tasks)
    return {model: resp for model, resp in zip(models, responses)}


# --- Stages ---

async def stage1(client: httpx.AsyncClient, query: str) -> list:
    print("\n" + "=" * 70)
    print("STAGE 1: Collecting individual responses")
    print("=" * 70)
    t0 = time.time()

    messages = [{"role": "user", "content": query}]
    responses = await query_models_parallel(client, COUNCIL_MODELS, messages)

    results = []
    for model, resp in responses.items():
        if resp is not None:
            results.append({"model": model, "response": resp["content"]})
            print(f"\n--- {short_name(model)} ---")
            print(resp["content"][:500] + ("..." if len(resp["content"]) > 500 else ""))

    print(f"\n[Stage 1 complete: {len(results)}/{len(COUNCIL_MODELS)} models responded in {time.time()-t0:.1f}s]")
    return results


async def stage2(client: httpx.AsyncClient, query: str, stage1_results: list) -> tuple:
    print("\n" + "=" * 70)
    print("STAGE 2: Peer review & ranking")
    print("=" * 70)
    t0 = time.time()

    labels = [chr(65 + i) for i in range(len(stage1_results))]
    label_to_model = {f"Response {l}": r["model"] for l, r in zip(labels, stage1_results)}

    responses_text = "\n\n".join(
        f"Response {l}:\n{r['response']}" for l, r in zip(labels, stage1_results)
    )

    ranking_prompt = f"""You are evaluating different responses to the following question:

Question: {query}

Here are the responses from different models (anonymized):

{responses_text}

Your task:
1. First, evaluate each response individually. For each response, explain what it does well and what it does poorly.
2. Then, at the very end of your response, provide a final ranking.

IMPORTANT: Your final ranking MUST be formatted EXACTLY as follows:
- Start with the line "FINAL RANKING:" (all caps, with colon)
- Then list the responses from best to worst as a numbered list
- Each line should be: number, period, space, then ONLY the response label (e.g., "1. Response A")

Now provide your evaluation and ranking:"""

    messages = [{"role": "user", "content": ranking_prompt}]
    responses = await query_models_parallel(client, COUNCIL_MODELS, messages)

    results = []
    for model, resp in responses.items():
        if resp is not None:
            text = resp["content"]
            parsed = parse_ranking(text)
            results.append({"model": model, "ranking": text, "parsed_ranking": parsed})
            print(f"\n--- {short_name(model)}'s ranking ---")
            if parsed:
                for i, label in enumerate(parsed, 1):
                    real_model = label_to_model.get(label, "?")
                    print(f"  {i}. {short_name(real_model)}")
            else:
                print("  [Could not parse ranking]")

    # Aggregate
    agg = aggregate_rankings(results, label_to_model)
    if agg:
        print(f"\n--- Aggregate ranking ---")
        for item in agg:
            print(f"  {short_name(item['model'])}: avg rank {item['average_rank']}")

    print(f"\n[Stage 2 complete in {time.time()-t0:.1f}s]")
    return results, label_to_model


async def stage3(client: httpx.AsyncClient, query: str, stage1_results: list, stage2_results: list) -> dict:
    print("\n" + "=" * 70)
    print("STAGE 3: Chairman synthesis")
    print("=" * 70)
    t0 = time.time()

    s1_text = "\n\n".join(
        f"Model: {short_name(r['model'])}\nResponse: {r['response']}" for r in stage1_results
    )
    s2_text = "\n\n".join(
        f"Model: {short_name(r['model'])}\nRanking: {r['ranking']}" for r in stage2_results
    )

    chairman_prompt = f"""You are the Chairman of an LLM Council. Multiple AI models have provided responses to a user's question, and then ranked each other's responses.

Original Question: {query}

STAGE 1 - Individual Responses:
{s1_text}

STAGE 2 - Peer Rankings:
{s2_text}

Your task as Chairman is to synthesize all of this information into a single, comprehensive, accurate answer to the user's original question. Consider:
- The individual responses and their insights
- The peer rankings and what they reveal about response quality
- Any patterns of agreement or disagreement

Provide a clear, well-reasoned final answer that represents the council's collective wisdom:"""

    messages = [{"role": "user", "content": chairman_prompt}]
    resp = await query_model(client, CHAIRMAN_MODEL, messages)

    if resp is None:
        result = {"model": CHAIRMAN_MODEL, "response": "Error: Chairman failed to respond."}
    else:
        result = {"model": CHAIRMAN_MODEL, "response": resp["content"]}

    print(f"\n--- {short_name(CHAIRMAN_MODEL)} (Chairman) ---")
    print(result["response"])
    print(f"\n[Stage 3 complete in {time.time()-t0:.1f}s]")
    return result


# --- Helpers ---

def parse_ranking(text: str) -> list:
    if "FINAL RANKING:" in text:
        section = text.split("FINAL RANKING:")[1]
        matches = re.findall(r'\d+\.\s*Response [A-Z]', section)
        if matches:
            return [re.search(r'Response [A-Z]', m).group() for m in matches]
    return re.findall(r'Response [A-Z]', text)


def aggregate_rankings(stage2_results: list, label_to_model: dict) -> list:
    positions = defaultdict(list)
    for r in stage2_results:
        parsed = parse_ranking(r["ranking"])
        for pos, label in enumerate(parsed, 1):
            if label in label_to_model:
                positions[label_to_model[label]].append(pos)
    agg = []
    for model, pos_list in positions.items():
        agg.append({"model": model, "average_rank": round(sum(pos_list) / len(pos_list), 2)})
    agg.sort(key=lambda x: x["average_rank"])
    return agg


# --- Main ---

async def run_council(query: str):
    if not OPENROUTER_API_KEY:
        print("ERROR: OPENROUTER_API_KEY not set. Add it to ~/.zshrc or environment.", file=sys.stderr)
        sys.exit(1)

    print(f"\nQUERY: {query}")
    print(f"COUNCIL: {', '.join(short_name(m) for m in COUNCIL_MODELS)}")
    print(f"CHAIRMAN: {short_name(CHAIRMAN_MODEL)}")

    t_total = time.time()

    async with httpx.AsyncClient() as client:
        s1 = await stage1(client, query)
        if not s1:
            print("\nAll models failed. Check your OpenRouter credits and API key.", file=sys.stderr)
            sys.exit(1)
        s2, label_map = await stage2(client, query, s1)
        s3 = await stage3(client, query, s1, s2)

    print("\n" + "=" * 70)
    print(f"COUNCIL SESSION COMPLETE ({time.time()-t_total:.1f}s total)")
    print("=" * 70)

    # Save session to JSON
    output = {
        "query": query,
        "council": COUNCIL_MODELS,
        "chairman": CHAIRMAN_MODEL,
        "stage1": s1,
        "stage2": [{"model": r["model"], "parsed_ranking": r["parsed_ranking"]} for r in s2],
        "aggregate": aggregate_rankings(s2, label_map),
        "final_answer": s3["response"],
    }
    out_path = os.path.join(os.path.dirname(__file__), "last_session.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSession saved to {out_path}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: council.py \"Your question here\"", file=sys.stderr)
        sys.exit(1)
    asyncio.run(run_council(" ".join(sys.argv[1:])))
