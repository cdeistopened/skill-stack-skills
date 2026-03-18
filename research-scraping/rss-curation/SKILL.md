# RSS Daily Curation

Fetch and score 64 education/homeschool RSS feeds, post curated items to Slack.

## Invocation

Say: "Run RSS curation" or "Curate RSS feeds"

## What It Does

1. Run `python3 agents/rss_curation.py --no-slack`
2. Read the daily output file
3. Post DEFINITELY items to Slack #market-daily via MCP

## Scoring Criteria

### DEFINITELY (Post to Slack)
- Mixed approach families
- Kids thriving outside school
- Practical parent help (curriculum, routines, printers)
- Relatable parent moments
- Neurodiversity focus
- Free-range / independence themes
- Reddit discussions (gold mine)

### NO (Skip)
- School choice policy / ESA news
- Political content
- Public school focused

## High-Value Sources
Lenore Skenazy, Peter Gray, Let Grow, Kerry McDonald, Jon Haidt, r/homeschool, r/unschool, Pam Barnhill, 1000 Hours Outside

## Output Files

| File | Purpose |
|------|---------|
| `Projects/RSS-Curation/daily/YYYY-MM-DD.md` | Scored curation |
| `agents/rss_curation.py` | Fetch + score script |

## Ed the Horse Voice (for X posts)

- **Values**: "Normalize [thing]."
- **Observation**: "[Thing] happened. [Dry comment]."
- **Question**: "Why do we [accepted norm]?"
- **Contrarian**: "[Opposite of expected]. Think about it."

---

*Last updated: 2026-01-29*
