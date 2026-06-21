---
name: hermes-tweet
description: >
  Install, configure, and operate the upstream Hermes Tweet plugin for Hermes Agent.
  Use when the user wants Hermes Agent to work with X/Twitter through read-first
  exploration, account reads, trends, monitors, media, giveaways, or
  approval-gated posting actions. Not for generic post copywriting.
---

# Hermes Tweet

Hermes Tweet helps Claude Code users add the
[Xquik-dev/hermes-tweet](https://github.com/Xquik-dev/hermes-tweet) plugin to a
local Hermes Agent setup.

## Use When

- The user wants Hermes Agent access to X/Twitter workflows.
- The user asks to install or configure the Hermes Tweet plugin.
- The user needs read-first social research, account reads, trends, monitors,
  media, or giveaway workflows from Hermes Agent.
- The user explicitly approves action-capable X/Twitter operations.

## Do Not Use For

- Generic post writing without Hermes Agent setup.
- Bypassing the plugin action gate.
- Posting without explicit operator approval.

## Install

Run the install against the Hermes Agent virtual environment:

```bash
~/.hermes/hermes-agent/venv/bin/python -m pip install hermes-tweet
```

Register the plugin inside Hermes Agent:

```bash
hermes plugin add hermes-tweet
```

Set `XQUIK_API_KEY` in the environment used by Hermes Agent.

Enable write actions only when the operator explicitly approves them:

```bash
export HERMES_TWEET_ENABLE_ACTIONS=true
```

## Operating Pattern

1. Start with read-only tools: exploration, account reads, trends, monitors,
   media checks, or giveaway context.
2. Confirm the account, audience, and action before any write operation.
3. Require `HERMES_TWEET_ENABLE_ACTIONS=true` before action-capable tools.
4. Keep drafts and summaries inspectable before publishing.
5. Link back to the upstream plugin for current usage and release notes:
   https://github.com/Xquik-dev/hermes-tweet
