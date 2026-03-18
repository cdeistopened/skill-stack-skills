# RSS Curation Skill - Handoff

**Date:** 2026-02-04
**Status:** Full pipeline operational (fetch → triage → scrape → output)

---

## Daily Pipeline

```
1. FETCH     python3 agents/rss_curation.py --no-slack
             Auto-calculates hours since last run (no --hours needed).
             Only fetches content published AFTER the last scrape.
2. TRIAGE    python3 Projects/RSS-Curation/serve_dashboard.py  →  localhost:8000
             Star keepers in browser → Save
3. SCRAPE    python3 agents/scrape_starred.py --clear-queue
             Scrapes starred articles to staging/day-YYYY-MM-DD/
             Bulk-skips everything else. Queue is clean.
4. OUTPUT    Read staging folder → Draft "Top 5" X article + thread
             (or route to newsletter, social, etc.)
```

**IMPORTANT:** Never re-fetch old items. The script uses `lastRun` from tracking.json
to automatically scope each fetch. No `--hours` flag needed unless overriding manually.

### Quick Start

Say: **"Let's do RSS curation"**

Or run manually:
```bash
cd "OpenEd Vault"
python3 agents/rss_curation.py --no-slack          # auto since last run
python3 Projects/RSS-Curation/serve_dashboard.py &
open http://localhost:8000
# ... star items, save ...
python3 agents/scrape_starred.py --clear-queue
```

---

## Files

| File | Location | Purpose |
|------|----------|---------|
| `rss_curation.py` | `agents/` | **Step 1:** Fetch 58 feeds, score, dedupe, update tracking.json |
| `serve_dashboard.py` | `Projects/RSS-Curation/` | **Step 2:** Local triage dashboard at localhost:8000 |
| `scrape_starred.py` | `agents/` | **Step 3:** Scrape starred items to markdown, clear queue |
| `tracking.json` | `Projects/RSS-Curation/` | Persistent state - all items, stars, rejects |
| `manifest.json` | `staging/day-YYYY-MM-DD/` | Index of scraped articles for that day |
| `feeds.json` | `.claude/skills/rss-curation/` | 58 feeds by tier |
| `scoring-prompt.md` | `.claude/skills/rss-curation/` | Scoring criteria + NO_KEYWORDS |

---

## Dashboard

**URL:** http://localhost:8000 (warm sand/Notion theme)

**Actions:**
- ★ Star items you want to use
- ✗ Skip (with optional reason for prompt improvement)
- ✓ Used (when already used elsewhere)
- 💾 Save (IMPORTANT: must click Save before closing browser)
- 🗑 Clear Done (removes processed items, keeps reject reasons)

**Known issue:** No auto-save. If you close without clicking Save, stars/skips are lost. Stars saved mid-session survive because they trigger individual saves.

**Filter by:** status, score, source

---

## Scraper Details

`agents/scrape_starred.py` handles:
- **Regular articles:** trafilatura extraction (best-in-class article extraction)
- **Reddit threads:** JSON API - gets post + top 10 comments with scores
- **Substacks:** trafilatura works well on these
- **Paywalled/JS-rendered:** Returns error message, must visit manually

**Output:** `Projects/RSS-Curation/staging/day-YYYY-MM-DD/`
- One markdown file per starred item with YAML frontmatter
- `manifest.json` listing all scraped items

**Flags:**
- `--clear-queue` - Bulk-skip all non-starred new items
- `--date=YYYY-MM-DD` - Custom date folder

**After scraping:**
- Starred items marked as `published` in tracking.json
- Stars cleared (items are now in staging)
- Non-starred items marked as `rejected` (if --clear-queue)

---

## Scoring

**Keyword-based scoring in `rss_curation.py`:**
- DEFINITELY: 2+ keyword hits or high-value source boost
- PROBABLY: 1 keyword hit (also the default)
- NO: Any NO_KEYWORD match

**High-value sources (auto-boosted):** Lenore Skenazy, Peter Gray, Let Grow, Kerry McDonald, r/homeschool, r/unschool, Pam Barnhill, 1000 Hours Outside, Jon Haidt, After Babel

**NO_KEYWORDS:** Policy/political (ESA, voucher, legislation, trump, biden), public school focus (district, superintendent, school board), local news (snow day, school closure), off-topic (oral health, child care, college admission)

---

## Feed Sources (58 active)

**Tier 1 (thought leaders):** Michael B. Horn, Kerry McDonald, Claire Honeycutt, Peter Gray, After Babel, Let Grow, Corey DeAngelis, Lenore Skenazy
**Tier 1 (core homeschool):** Pam Barnhill, Simple Homeschool, Brave Writer, 1000 Hours Outside
**Tier 2 (community):** The Homeschool Mom, Hip Homeschool Moms, Homeschool Hideout, Fearless Homeschool, Homeschool Boss, A Gentle Feast, Hybrid Homeschool Project, Raising Lifelong Learners
**Tier 2 (classical/CM):** Classical Conversations, CiRCE, Simply Charlotte Mason, Memoria Press
**Tier 2 (research):** NHERI, Alliance for Self-Directed Education, Peter Gray (Psych Today), Sudbury Valley
**Tier 2 (news):** The 74, EdSurge, Getting Smart, EdWeek, Chalkbeat
**Tier 2 (microschools):** Acton Academy, KaiPod, VELA, Outschool
**Tier 2 (gold mines):** r/homeschool, r/unschool
**Tier 3 (policy):** Education Next, Reason Ed, Cato Ed, EdChoice, Rick Hess, CRPE, Pioneer, School Choice Week
**Tier 4 (substacks):** Ed3 World, Austin Scholar, Jay Wamstead, Hannah Frankman, Rebel Educator
**Tier 5 (podcasts):** Future of Ed, Homeschool Solutions, Read-Aloud Revival, Brave Learner

---

## Prompt Improvement Queue

When you have 5+ reject reasons, update `scoring-prompt.md` and `NO_KEYWORDS` in `rss_curation.py`.

**Current reject reasons on file:**
1. "Philadelphia school safety officers..." → "off topic" → Add: bulletproof, safety officer, school police
2. "Numbering Our Homeschool Days: Biblical Perspective..." → "religious/devotional" → ADDED to NO_KEYWORDS
3. "LA/SF Teachers Unions OK Strikes..." → "union/labor politics" → ADDED to NO_KEYWORDS

---

## Output Formats (downstream of scraping)

Once articles are in staging, route to:

| Format | Description | Status |
|--------|-------------|--------|
| X "Top 5" article | Daily thread tagging authors/orgs | Planned |
| Newsletter segments | Feed into opened-daily-newsletter-writer | Available |
| Social posts | Route through content-repurposer | Available |
| Slack digest | Post curated list to #market-daily | Available |

---

## Pending Improvements

- [ ] Auto-save in dashboard (save on every action, not manual click)
- [ ] launchd automation for daily 7am fetch
- [ ] Handle lookup sub-agents for X thread tagging
- [ ] After 5+ reject reasons, update scoring-prompt.md
- [ ] Better scraping for JS-rendered sites (Raising Lifelong Learners, The 74)

---

*Last updated: 2026-02-05*
