# Business Acquisition Evaluator

Walk a founder through buying a small business using frameworks from Sarah Moore, Brent Beshore, Andrew Wilkinson, and Codie Sanchez as discussed on My First Million.

## When to Use

The user wants to buy a business instead of starting one from scratch. They might say:
- "I want to buy a small business"
- "Help me evaluate this acquisition target"
- "How do I find businesses to buy?"
- "I have $X to deploy — what should I acquire?"

## Phase 1: Should You Buy Instead of Build?

From Shaan Puri and the "boring businesses" thesis across multiple episodes:

The MFM case for buying over building:
- Existing revenue, customers, and cash flow from day one
- Skip the 0-to-1 product-market fit grind
- Industry doesn't matter as much as you think — what matters is consistent profitability

> "Industry is overrated. What matters is that you find a business that is established and has been consistently profitable for a number of years. Everything else? Garbage." — Sarah Moore

Ask the user:
1. How much capital do you have to deploy? (This determines deal size.)
2. Do you want to operate it yourself or hire a CEO?
3. Are you comfortable with debt? (Most small acquisitions use leverage.)
4. What's your time horizon — build and hold, or buy-fix-sell?

## Phase 2: Sourcing — Finding Businesses to Buy

From Sarah Moore's zero-money-down acquisition process (`dF6zvTXimxY.md`):

**Step 1: Build a target database**
- Scrape a private company database (BizBuySell, BizQuest, or direct outreach)
- Filter by: geography (1.5-hour radius if you want to visit), revenue range ($1M-$20M sweet spot), years in operation (5+ years of profitability)
- Remove: anything over $100M revenue, professional services firms, franchises

**Step 2: Mass outreach**
- Guess email patterns (first.last@domain, first-initial.last@domain)
- Verify with Bulk Email Checker
- Template: "I'm looking for a business to buy, and yours seems to perfectly fit the bill — it's within this revenue range, it's been around for a really long time, it's been profitable for a number of years."
- Volume matters: Sarah contacted thousands. Expect low single-digit response rates.
- Counter-intuitive: angry replies are useful — "they filled out our survey without realizing it"

**Step 3: Qualification gate**
- On the first call, get to price range quickly
- If the seller thinks their business is worth 10x earnings, end the conversation
- You're looking for: consistently profitable for multiple years + willing to discuss a seller's note

**Source transcript:** `transcripts/dF6zvTXimxY.md`

## Phase 3: Valuation — What to Pay

From Sam, Shaan, and guests across multiple episodes:

**Small businesses (under $5M revenue):** Trade at 2-4x annual profit (SDE — Seller's Discretionary Earnings)

**The quick math:**
- Ask for 3 years of tax returns and P&L statements
- Calculate average annual profit (add back owner's salary, one-time expenses)
- Multiply by 2.5-3.5x for a fair offer
- Offer slightly high (closer to 4x) knowing there's room to negotiate down

**Red flags in the financials:**
- Revenue declining year over year
- Single customer concentration (>25% of revenue from one client)
- Owner is the entire sales operation (you're buying a job, not a business)
- Deferred maintenance or capex (the real cost is hidden)

**Sam's North Star math:** Can you express the acquisition as `Purchase Price / Annual Cash Flow = Payback Period`? If payback is under 3 years, it's attractive. Under 2 years, it's a great deal.

## Phase 4: Deal Structure

From Sarah Moore and multiple acquisition episodes:

**The zero-money-down structure:**
- 25% seller's note (the seller finances part of the deal — they get paid over time)
- 75% bank financing (SBA loans are designed for this)
- Key: find a bank that views the seller's note as equity (not all will)
- Expect 20+ bank rejections before finding one that works

**Why sellers accept this:** They get a higher total price, ongoing income, and tax advantages from spreading the payment over time.

**Alternative structures discussed on MFM:**
- Earnouts (avoid if possible — "47% earned less than expected")
- Revenue share (better for the buyer, worse for the seller)
- Equity rollover (seller keeps a stake — aligns incentives)

## Phase 5: People Diligence

From Brent Beshore (`3q1QvEkbbyk.md`):

> "The business we're in is predicting people's behavior. If all these businesses are predicated on the people who run them, the primary risks are going to be the people."

**The Beshore Method:**
1. **Personality type:** Immediately categorize using Myers-Briggs axes (I/E, S/N, T/F, J/P) to understand how they think and communicate
2. **Motivation pattern:** Layer in Enneagram for emotional drive
3. **The Jerk Test:** Eat with them. Travel with them. Observe them with wait staff, at the airport during a delay. "It is impossible to fake it when you're at the airport grinding through security."
4. **Reference checks:** Talk to employees, suppliers, customers — not just the references the seller provides

**Blake's "Teach Me Something" test** (from `3VLDuDZ6Qvo.md`):
> Ask the seller or key employees to teach you something about the business. Push back 2-3 times with "I don't understand, can you walk me through that?" — you'll immediately see who knows their stuff and who's bluffing.

## Phase 6: Post-Acquisition — Running What You Bought

From Andrew Wilkinson's Tiny Corp approach (`RzwS8iUHeQo.md`):

**If you want to operate:**
- Ask: "If I could change one thing, what would give the business the most leverage?" Usually it's something boring — pricing, operations, not product.
- Don't try to change everything at once. The business worked before you — respect what's there.

**If you want to delegate:**
- Readiness check: Is the business at $300K+ profit? Does it have product-market fit?
- Find the #2 at a similar business that's 2x your size
- Comp structure: lead with total comp ($300K = $150K base + $150K bonus), tie bonus to EBITDA, uncapped upside
- For equity: require them to write a check (not options) — Wilkinson will even loan them the money
- After hiring: send financials monthly. Annual in-person meeting. Leave them alone.

**Source transcript:** `transcripts/RzwS8iUHeQo.md`

## Phase 7: Search the Archive

Before finalizing any acquisition, search the transcripts for relevant episodes:

```
grep -ri "boring business" transcripts/    # 45 matches across 30 files
grep -ri "roll-up" transcripts/            # acquisition roll-up strategies
grep -ri "laundromat\|lawn care\|plumbing\|HVAC" transcripts/  # specific boring industries
```

The archive contains detailed case studies of specific acquisitions in dozens of industries. Search for your target industry — there's a good chance Sam, Shaan, or a guest has discussed it.

## Output

After walking through all phases, summarize:
1. **Buy vs. Build verdict** for this user's situation
2. **Target profile:** industry, geography, revenue range, deal size
3. **Outreach plan:** how many targets, what template
4. **Valuation range:** based on the financials
5. **Deal structure recommendation**
6. **Key diligence questions** specific to this deal
7. **Post-acquisition plan:** operate or delegate?
