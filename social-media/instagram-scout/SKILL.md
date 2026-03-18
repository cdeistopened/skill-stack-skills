---
name: instagram-scout
description: >
  Instagram competitive intelligence and content strategy tool. Scrapes competitor profiles via Apify,
  detects trending content across Instagram/TikTok/Google Trends, analyzes viral posts with Gemini AI,
  and generates creative briefs adapted to any creator's voice and brand. Use this skill whenever
  the user mentions Instagram content strategy, competitor analysis, social media trend scouting,
  content calendar planning, viral post analysis, creative briefs, or wants to understand what's
  performing well on Instagram in a niche — even if they don't explicitly say "instagram-scout."
---

# Instagram Scout

A recurring content intelligence tool that turns competitor research into actionable content strategy for any creator. Run it weekly or biweekly to stay on top of what's working — trends move fast.

## When to Run

This is **not a one-time audit** — it's a recurring intelligence pipeline. The cadence depends on how actively the creator is posting:

| Cadence | What to run | When |
|---------|-------------|------|
| **Weekly** | Profile Scraper (`--profiles --analyze --brief`) | Content planning day — generates next week's ideas |
| **Biweekly** | Full Trend Scout (`--analyze`) | Deeper scan — catches emerging formats and cross-platform signals |
| **Ad hoc** | Single profile or hashtag scrape | When you see a competitor post blow up and want to understand why |
| **First run** | Everything — full trend scout + competitor profiles | Initial landscape scan when onboarding a new client |

The output directory is date-stamped (`output/YYYY-MM-DD-*/`), so you build a natural archive of what was trending when. Over time this becomes a dataset of niche trend history.

## What It Does

1. **Profile Scraper** — Scrape competitor Instagram profiles, rank posts by engagement, AI-analyze the top performers, generate creative briefs in the creator's voice
2. **Trend Scout** — 4 concurrent engines: IG viral ratio detection (40+ accounts), TikTok leading indicators (2-4 week advance signal), Google Trends matching, Gemini Vision video analysis
3. **Web UI** — Interactive dashboard for browsing/bookmarking posts, running AI analysis, and generating briefs (SQLite-backed)

## Requirements

- **Runtime**: [Bun](https://bun.sh) (TypeScript runtime)
- **Environment variables**: `APIFY_TOKEN` (required), `GEMINI_API_KEY` (required for AI analysis/briefs)
- **Apify actors used**: `apify~instagram-scraper`, `apify~instagram-reel-scraper`, `clockworks~free-tiktok-scraper`, `emastra~google-trends-scraper`

## Setup for a New Project

Every project needs a `scout-config.json` file in its working directory. This config drives all the creator-specific content — competitor lists, keywords, brand voice, audience targeting.

### Step 1: Create the config

Read `references/config-guide.md` for the full schema and an example. The essential sections:

```json
{
  "project_name": "Creator Name - Niche",
  "creator": { "name": "...", "handle": "...", "bio": "...", "followers": "..." },
  "voice": { "tone": "...", "style": "...", "avoid": [] },
  "brand": { "method": "...", "techniques": [], "core_message": "...", "pillars": [], "hashtags": [] },
  "audience": { "age_range": "...", "interests": [], "description": "..." },
  "competitors": ["handle1", "handle2"],
  "mid_tier_accounts": ["handle1", "handle2"],
  "tiktok_keywords": ["keyword1", "keyword2"],
  "google_trends_terms": ["term1", "term2"]
}
```

- `competitors` — 5-15 accounts in the same niche (the "who to study" list for profile scraping)
- `mid_tier_accounts` — 20-40+ mid-tier accounts (10K-500K followers) for viral ratio detection. Include therapists, practitioners, educators in adjacent niches.
- `tiktok_keywords` — 8-12 search phrases that match the creator's niche. TikTok trends lead Instagram by 2-4 weeks.
- `google_trends_terms` — 10-20 search terms to monitor for interest spikes.

### Step 2: Install dependencies

```bash
cd <skill-path>/scripts
bun install  # (no external deps — just bun built-ins)
```

## Usage

All scripts are in `scripts/` within this skill directory. They read `scout-config.json` from the current working directory (or pass `--config=path/to/config.json`).

### Profile Scraper

```bash
# Scrape all competitors defined in config
bun run <skill-path>/scripts/scrape.ts --profiles

# Scrape one specific profile
bun run <skill-path>/scripts/scrape.ts --profile=drjoedispenza

# Scrape + AI analysis of top 10 posts
bun run <skill-path>/scripts/scrape.ts --profiles --analyze

# Full pipeline: scrape + analyze + generate creative brief
bun run <skill-path>/scripts/scrape.ts --profiles --analyze --brief

# Search by hashtag
bun run <skill-path>/scripts/scrape.ts --hashtag=breathwork --analyze --brief

# Control posts per profile (default: 12)
bun run <skill-path>/scripts/scrape.ts --profiles --limit=20
```

**Output**: Creates `output/YYYY-MM-DD-{label}/` with:
- `00-overview.md` — Ranked engagement table + top 15 captions
- `01-{username}.md` through `10-{username}.md` — Individual post AI analysis
- `creative-brief.md` — 7 content ideas adapted to the creator's voice

### Trend Scout

```bash
# Run all 4 engines
bun run <skill-path>/scripts/trend-scout.ts

# Run specific engines
bun run <skill-path>/scripts/trend-scout.ts --ig-only
bun run <skill-path>/scripts/trend-scout.ts --tiktok-only
bun run <skill-path>/scripts/trend-scout.ts --trends-only

# Add AI synthesis (combines all signals into action plan)
bun run <skill-path>/scripts/trend-scout.ts --analyze
```

**Output**: Creates `output/YYYY-MM-DD-trend-scout/` with:
- `00-full-report.md` — Combined report
- `01-instagram-viral-ratio.md` — Posts outperforming their account baseline (>2x = viral)
- `02-tiktok-leading-indicators.md` — Trending TikTok content (early signal)
- `03-google-trends.md` — Spiking/rising/declining search terms
- `04-video-analysis.md` — Gemini Vision breakdown of top viral Reels (transcript, hooks, format)
- `05-synthesis-action-plan.md` — AI-generated weekly content calendar + opportunities

### Web UI

```bash
bun run <skill-path>/scripts/server.ts
# Opens at http://localhost:8003
```

Interactive dashboard for real-time research: search hashtags, browse posts, bookmark favorites, run AI analysis, generate briefs. SQLite-backed with caching.

## How the Engines Work

### Viral Ratio Detection
A post's likes divided by its creator's average likes. A ratio of 5x means the post got 5 times more engagement than usual — signaling the *format or topic* resonates beyond the core audience. The skill scrapes 12 recent posts from each mid-tier account, computes baselines, and flags posts >2x as breakouts.

### TikTok Leading Indicators
TikTok trends hit Instagram 2-4 weeks later. The skill searches 8-12 niche keywords on TikTok, collects top videos, and surfaces formats/hooks/hashtags gaining traction. This is the early warning system.

### Google Trends Matching
Monitors 10-20 search terms for interest spikes over 90 days. Terms showing >1.5x growth are flagged as "SPIKING" — ideal timing for content. Terms at >1.2x are "rising."

### Video Analysis (Gemini Vision)
Downloads top viral Reels, sends to Gemini 2.0 Flash for: word-for-word transcript, hook analysis (first 3 sec), format classification, visual techniques, content structure, and replication notes.

## Interpreting Results

When presenting results to the user, focus on:
1. **Viral ratio breakouts** — Which posts dramatically outperformed? What format/topic caused it?
2. **Cross-platform signals** — Is the same theme trending on TikTok AND spiking in Google Trends? That's a strong signal.
3. **Actionable adaptation** — Don't just report what's trending. Show how to adapt it to the creator's voice, method, and audience.
4. **Timing** — Google Trends shows what people are searching NOW. TikTok shows what they'll search in 2-4 weeks. Instagram viral ratios show what's working TODAY.

## Client-Specific References

Pre-built configs for existing clients:
- **Dr. Richard Louis Miller** — `references/rlm-config.md` — Full config with rationale for every account choice, niche mapping, and ready-to-use JSON. Focused on talking-head psychologist/wellness accounts.

When onboarding a new client, use the RLM config as a template and adjust the accounts/keywords for the new niche.

## Data Limitations & Future Enhancements

**What Apify gives us:** Caption text, engagement counts, post type, hashtags, latest comments, display URL (thumbnail image), and video URLs for Reels.

**What we can't easily get:**
- On-screen text from thumbnails (the hook text overlaid on images/video covers)
- Audio transcripts from Reels (unless we download the video and send to Gemini Vision, which Engine 4 does for viral posts)

**Thumbnail text extraction (planned):** For talking-head accounts, the thumbnail text overlay IS the hook — it's often more important than the caption. A lightweight enhancement would grab the `displayUrl` (post thumbnail) and send it to Gemini for OCR/text extraction. This would let us analyze hook text patterns at scale without downloading full videos. Not yet implemented but straightforward to add as a post-processing step on the overview report.

**Practical implication:** When selecting accounts for the config, prioritize talking-head creators who use text overlays — the caption + comment data is most useful for these formats. Lifestyle photography or graphic design accounts yield less actionable data from text-only analysis.

## Cost Awareness

Each Apify actor run consumes credits. Approximate costs:
- Profile scrape (12 posts): ~$0.01-0.02 per profile
- Full competitor scrape (10 profiles): ~$0.10-0.20
- Trend scout (all engines): ~$0.50-1.00
- Gemini analysis: included with API key (Flash model is cheap)

Warn the user before running large scrapes (40+ accounts in trend scout).
