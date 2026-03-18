# LLM Council

Query multiple LLMs, have them peer-review and rank each other's responses, then synthesize a final answer via a chairman model. Based on [karpathy/llm-council](https://github.com/karpathy/llm-council).

## Trigger

User invokes `/council` with a question or topic.

## How It Works

Three stages, all via OpenRouter API:

1. **Stage 1 — First Opinions**: GPT-5.1, Gemini 3 Pro, Claude Sonnet 4.5, and Grok 4 each answer the query independently (in parallel).
2. **Stage 2 — Peer Review**: Each model receives all anonymized responses and ranks them by quality. Rankings are aggregated.
3. **Stage 3 — Chairman Synthesis**: Gemini 3 Pro (chairman) reads all responses + all rankings and produces a single final answer representing the council's collective wisdom.

## Usage

Run the council script:

```bash
OPENROUTER_API_KEY="$OPENROUTER_API_KEY" uv run --with httpx python3 .claude/skills/llm-council/council.py "YOUR QUESTION HERE"
```

The script:
- Prints truncated Stage 1 responses (first 500 chars each)
- Prints parsed rankings from each model in Stage 2
- Prints the full chairman synthesis in Stage 3
- Saves the complete session to `.claude/skills/llm-council/last_session.json`

## Workflow

1. User asks `/council "question"`
2. Run the command above with the user's question
3. Wait for it to complete (~60-120s depending on model latency)
4. Present the **Stage 3 final answer** to the user
5. If the user wants to see individual model responses or rankings, read `last_session.json`

## Config

Edit `council.py` to change:
- `COUNCIL_MODELS` — which models sit on the council
- `CHAIRMAN_MODEL` — which model synthesizes the final answer
- Models use OpenRouter identifiers (e.g., `openai/gpt-5.1`)

## Requirements

- `OPENROUTER_API_KEY` in environment (set in `~/.zshrc`)
- `uv` installed (manages Python + dependencies)
- OpenRouter account with credits loaded
