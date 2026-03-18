---
name: yt-outlier
description: Find viral YouTube video patterns in any niche using outlier analysis. Scrapes recent videos, computes views-to-subscriber ratios, and surfaces title/format patterns that outperform channel averages. Use for content ideation, niche validation, or competitor research.
argument-hint: "[topic or keyword]"
---

# YouTube Outlier Finder

Identify what's working on YouTube right now for any topic. Inspired by VidIQ's outlier score — but with pattern analysis on top.

## Usage

```
/yt-outlier claude code skills
/yt-outlier sourdough bread baking
/yt-outlier "homeschool curriculum reviews" --window month
```

## Core Concept: The Outlier Score

**Outlier Score = Video Views / Channel Subscriber Count**

A video with 100K views on a 10K-sub channel (10x) is a much stronger signal than 100K views on a 1M-sub channel (0.1x). The outlier score reveals which *topics and title formats* are punching above their weight — regardless of channel size.

| Score | Meaning |
|-------|---------|
| < 1x | Underperforming (below channel average) |
| 1-2x | Normal performance |
| 2-5x | Above average — topic resonated |
| 5-10x | Strong outlier — title/topic hit a nerve |
| 10x+ | Viral breakout — study this title closely |

## Workflow

### Step 1: Scrape YouTube Search Results

**Primary method: yt-dlp (free, no API key, no rate limits)**

```bash
# Search and get video metadata as JSON
yt-dlp "ytsearch30:<USER_KEYWORD>" --flat-playlist --dump-json 2>/dev/null

# Get subscriber count for a specific channel (flat-playlist doesn't include subs)
yt-dlp "https://www.youtube.com/@ChannelHandle" --playlist-items 1 --dump-json 2>/dev/null
```

Parse the JSON for: `title`, `view_count`, `channel`, `upload_date`, `thumbnails[-1].url`, `webpage_url`.

**Note:** `--flat-playlist` is fast but returns 0 for `channel_follower_count`. For outlier scores, you need a separate lookup per unique channel. Batch the top ~10 channels, not all 30.

**Thumbnail URLs** come from the `thumbnails` array in yt-dlp JSON. Use the last entry (highest resolution). Download with curl for visual analysis.

**Fallback method: Apify YouTube scraper** (if available, but check monthly limit first)

```
Tool: mcp__apify__streamers-slash-youtube-scraper
Input:
  searchQueries: ["<USER_KEYWORD>"]
  maxResults: 50
  dateFilter: <WINDOW>  (default: "month", options: "week", "month", "year")
  sortingOrder: "relevance"
```

**Time window mapping:**
- "2 weeks" → use `dateFilter: "month"` then filter by date in analysis
- "1 month" → `dateFilter: "month"`
- "3 months" → `dateFilter: "year"` then filter by date in analysis

If the keyword is broad, run a second search with a more specific variant to capture the long tail. For example, if the user searches "claude code", also try "claude code tutorial" or "claude code skills".

### Step 2: Compute Outlier Scores

For each video returned, calculate:

```
outlier_score = video_views / channel_subscribers
```

Filter out:
- Videos with 0 subscriber count (data unavailable)
- Official brand channels (Anthropic, OpenAI, etc.) — they skew the data
- Non-English results (unless the user is targeting a specific language market)
- Videos clearly unrelated to the topic (noise from broad search)

Sort by outlier score descending.

### Step 3: Analyze Title Patterns

Categorize every title in the top 30 by format. Look for these patterns:

| Pattern | Example | Signal |
|---------|---------|--------|
| **Listicle** | "9 automations + 4 builds that work" | High outlier avg in test data |
| **Time constraint** | "in 18 minutes", "in 35 minutes" | Specificity = credibility |
| **Cost/FREE** | "FREE Forever", "Stop Paying $200/mo" | Strong for small channels |
| **Credibility hook** | "(Meta Staff Engineer Tips)" | Authority + curiosity |
| **Build result** | "I Built 5 Websites", "Trading Bot" | Concrete output > vague promise |
| **Superlative** | "INSANE", "DESTROYED" | Overused, low outlier avg |
| **Negative/contrarian** | "don't install", "has a big problem" | Works for big channels only |
| **Comparison** | "vs", "which is better" | Decision-stage viewers |
| **Tutorial/How-to** | "Full Guide", "Step-by-Step" | High volume, moderate outlier |
| **Dollar claim** | "$273/Day", "$450K Campaign" | Money = clicks (use carefully) |

Count how many of the top 30 titles fall into each pattern. Compute average outlier score per pattern.

### Step 4: Surface Insights

Generate the report with these sections:

#### 1. Top 15 Outliers Table

```
Score | Views    | Subs     | Title                                          | Channel
21.6x | 122,089 |    5,640 | I Built 5 Websites in 18 Minutes...            | Luke Carter
```

#### 2. Pattern Scorecard

```
Format                          | Count | Avg Outlier | Avg Views
Listicle (N ways/tips/cases)    |     4 |       9.3x |   131,834
Time constraint (N minutes)     |     6 |       6.9x |   192,334
```

Rank patterns by average outlier score, not count.

#### 3. Channel Size Breakdown

Group videos into Small (<50K subs), Mid (50K-500K), Big (500K+):
- Which tier is producing the most outliers?
- What patterns work at each tier?

#### 4. Thumbnail Analysis

Download thumbnails for the top 10 outliers and analyze visually using Claude's image reading:

```bash
# Download thumbnail
curl -s -o "channel-title-slug.jpg" "<THUMBNAIL_URL>"
```

Then read each image and categorize by pattern:

| Pattern | Description | When It Works |
|---------|-------------|--------------|
| **Face + Bold Text** | Close-up emotional face, 3-5 word overlay, color-blocked key word | Big channels, interview formats |
| **Minimal Face + Short Phrase** | Approachable person, simple text, soft background | Small/mid channels building trust |
| **Nature/Lifestyle Scene** | Calming environment, minimal text, aesthetic > personality | Breathwork, meditation, wellness |
| **Provocative/Edgy** | Warning labels, psychedelic overtones, shirtless intensity | Established brands, edgy niches |
| **Pure Illustration** | No face, text-only or animated, clean design | Utility content (follow-along exercises) |

Note: color palette, text placement, facial expression, and whether the thumbnail "matches" the target audience.

#### 5. Content Gap Analysis

Look for what's NOT being covered well:
- Topics mentioned but with weak titles/low production
- Angles that exist in 1-2 videos but not widely covered
- Audience questions visible in titles that nobody's answering well

#### 5. Title Ideas

Based on the top-performing patterns, generate 5-10 concrete title ideas for the user. Combine the winning patterns:
- Listicle + time constraint: "7 Claude Code Skills You Can Build in 20 Minutes"
- Credibility + build result: "I Automated My Entire Workflow (Here's the Setup)"
- Cost angle + specific: "Stop Paying for [Tool] — Claude Code Does It Free"

**Important:** Title ideas should reflect the USER'S channel size and niche, not just copy what big channels do. Negative hooks work at 500K+ subs but not for small channels. Listicles and time constraints work at every level.

### Step 5: Cross-Reference with Niche Scout (Optional)

If the user is also evaluating this topic for a book:

> "This topic also has strong KDP potential. Run `/niche-scout <keyword>` to check Amazon demand and BSR competition."

If the YouTube data shows high engagement but the topic is very competitive on Amazon, that's a signal to use YouTube as the distribution channel and monetize differently (course, affiliate, community).

## Interpreting Results

**Strong niche signals:**
- Multiple small channels (<50K) achieving 5x+ outlier scores
- Consistent demand across multiple title formats
- Viewers engaging with both tutorial AND opinion content (mature audience)

**Weak niche signals:**
- Only big channels (500K+) getting views (brand-driven, not topic-driven)
- All outliers are "reaction" or news content (no staying power)
- Low total video count (nobody's making content = might mean nobody's watching)

**Red flags:**
- All top videos are from one channel (not a niche, it's a creator)
- Outlier scores cluster at 1x or below (topic is saturated)
- Views are high but engagement (likes/comments) is very low (clickbait, not real interest)

## Tool Dependencies

- **Apify** — YouTube scraper via MCP (`streamers/youtube-scraper`), APIFY_TOKEN in env
- **Claude analysis** — Pattern recognition, categorization, title generation (no external tool needed)

## Related Skills

- **niche-scout** — Evaluate the same keyword on Amazon KDP (book potential)
- **deep-research** — For deeper competitive analysis on borderline niches
- **skill-extractor** — If video transcripts reveal skills worth building
