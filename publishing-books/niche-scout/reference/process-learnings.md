# Niche Scout — Process Learnings

## API Reliability (as of 2026-03-04)

### DataForSEO (Keyword Volume) — RELIABLE
- Direct REST API, returns in <3 seconds
- Supports `--bulk` mode for 10 keywords at once ($0.011 per call)
- Related keywords via separate endpoint ($0.02 per call)
- Amazon-specific search volume (not Google)
- **Credentials:** `~/.zshrc` (DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD)

### Apify Amazon Scraper (BSR) — FIXED (was timeout bug)
- Actor: `curious_coder~amazon-scraper`
- **Root cause of "failures":** Poll timeout was 5 min (30x10s) but runs take 6-10 min. Every "failed" run actually SUCCEEDED on Apify's side — our script just stopped waiting.
- **Fix applied:** Changed `range(30)` to `range(60)` in bsr-scraper.py (10 min timeout)
- **Actual success rate:** 100% of recent runs succeeded on Apify dashboard
- **Typical run times:** Search pass 4-10 min, detail pass 0.5-1 min
- **Cost:** ~$0.10-0.18 per run
- **Still true:** Running sequentially (one at a time) is more reliable than parallel

## Strategies That Work

1. **Run BSR scrapes sequentially, not parallel.** One at a time.
2. **Do keyword volume sweep FIRST** (cheap, fast). Only BSR-check the top 2-3 survivors.
3. **Start with the most obscure keyword.** Apify is more likely to succeed on low-competition terms.
4. **If a BSR scrape times out, wait 5-10 min before retrying.** Amazon rate limits cool down.

## Known Keyword Traps

- **"exit strategy"** — volume is sci-fi (Murderbot Diaries), not business
- **"myopia" (37K)** — volume is glasses shoppers, not book buyers
- **"succession" (39K)** — TV show viewers, not business owners
- **High volume ≠ book demand.** Always check if related keywords are book-intent (guide, workbook, how to) vs product-intent (glasses, cards, decor)

## Niche Viability Patterns (from 8 BSR runs)

- **Founder/wealth keywords** don't sell books on Amazon. Audience uses advisors + peer networks.
- **Self-help/mental health keywords** have massive volume but the top is dominated by perennial bestsellers.
- **Niche within a niche** is the play: not "anxiety" (87K) but "anxiety workbook for teens" type specificity.

## BSR Data Source Research (2026-03-04)

### Current: Apify `curious_coder~amazon-scraper` — UNRELIABLE
- Headless browser scraping, Amazon blocks ~70% of runs
- $0.50-1.00 per successful run (compute costs)
- No fix possible — Amazon's anti-bot detection is too aggressive for cloud browser pools

### Recommended Replacement: Keepa API
- **Python library:** `pip install keepa` (GitHub: akaszynski/keepa)
- **Pricing:** €49/mo minimum for API access (20 tokens/min = ~1,200 lookups/hr)
- **Key methods:**
  - `product_finder()` — search by title, category, sales rank range → returns ASINs
  - `query()` — full product data: BSR history (`SALES` field), reviews, price, publisher
  - `best_sellers_query()` — category bestseller lists
- **BSR data:** YES — returns full sales rank history, not just current BSR
- **Keyword search:** No direct keyword search, but `product_finder(titleSearch=...)` works
- **Reliability:** Direct API (not scraping), 99%+ uptime
- **Setup:** Get API key from keepa.com, subscribe to API plan

### Alternative: Bright Data Amazon Scraper
- **Success rate:** 99.98% in benchmarks
- **Data richness:** 686 fields (highest of all scrapers)
- **Speed:** ~66 seconds per request (slow but reliable)
- **Pricing:** Usage-based, ~$500/mo minimum for serious use
- **Best for:** Enterprise-scale scraping, overkill for niche research

### Alternative: Titans Quick View Chrome Extension
- **Free** Chrome extension for KDP publishers
- Shows BSR, avg price, reviews, niche score on Amazon search results
- **Excel export** of ASINs, titles, authors — could be scraped programmatically
- No API, but the extension's data could be captured via browser automation
- Good for manual spot-checks, not for batch automation

### Alternative: BookBeam
- All-in-one KDP tool with BSR tracking, keyword research, niche finder
- Chrome extension + web dashboard
- No API — web-only
- $19-49/mo estimated

### Alternative: Publisher Rocket ($199 one-time)
- Desktop app, most popular among KDP publishers
- Keyword volume, BSR, competition analysis, AMS ad keywords
- No API — manual use only
- Best for: Charlie doing manual research before committing to a niche

### Not Recommended
- **Amazon PA-API (PA-API 5.0):** Requires Associates account with 3 qualifying sales in 180 days. Returns BSR but keyword search is limited. Too much friction for our use case.
- **ScraperAPI / Oxylabs / Zyte:** General scraping proxies. Would need to build the Amazon parsing layer ourselves. Overkill.

## Recommended Architecture (v2)

1. **Step 1: Keyword Volume** — DataForSEO (keep as-is, works perfectly)
2. **Step 2: BSR Analysis** — Replace Apify with Keepa API
   - Use `product_finder(titleSearch="keyword", salesRankRange=[0, 200000])` to find ASINs
   - Use `query(asins)` to get BSR, publisher, reviews for top 10
   - Build scoring on top of same Dollwet benchmarks
3. **Step 3: Niche Matrix Scanner** — Batch combine Steps 1+2 across keyword combos

## Future Improvements

- [ ] Integrate Keepa API as BSR replacement (needs €49/mo subscription)
- [ ] Build the niche matrix scanner (batch test keyword combinations from a corpus)
- [ ] Add Google Trends integration for seasonality check
- [ ] Publisher Rocket for manual validation of top candidates
