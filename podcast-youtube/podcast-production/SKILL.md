---
name: podcast-production
description: Produce podcast episodes from Notion transcript to a single editor handoff document. Three phases with two human decision points.
---

# Podcast Production Skill (v2)

Transform a podcast transcript into a single **EDITOR_HANDOFF.md** - the one document your video editor needs. Three phases, two human checkpoints, converging on one deliverable.

**Previous version:** `SKILL_v1_archive.md` (4-checkpoint system, retired Feb 2026)

---

## The Pipeline

```
PHASE 1: SETUP (automated, no LLM needed for import)
  Step 0:   Import from Notion → SOURCE.md
  Step 0.5: Guest social research → GUEST_SOCIAL_RESEARCH.md
  Step 1:   SEO keyword research → SEO_Keywords.md
  Step 1.5: YT outlier research (2-3 niche queries) → YT_Outlier_Report.md
            Include direct YouTube search URLs for the top 3-5 most relevant outlier videos so the user can study thumbnails.

PHASE 2: AUDIT + HUMAN REVIEW
  Step 2:   Audit (angles, clips, cold opens, blog format assessment)
            → Checkpoint_1_Audit.md
  ────────── HUMAN CHECKPOINT: Select angle + approve clips ──────────
  Step 2.5: Deep-dive top outlier (reverse-engineer #1 title)
  Step 3:   Title + thumbnail variations (YouTube title + blog title)
            → Title_Options_By_Angle.md
            Note: YouTube supports A/B testing 3 title+thumbnail combos
  ────────── HUMAN CHECKPOINT: Select title + thumbnail ──────────

PHASE 3: HANDOFF ASSEMBLY (converges to one document)
  Step 4:   On-screen hook generation (3-4 per clip, * on recommended)
  Step 5:   Final clip markup (3 short + 2 long, edit-ready)
  Step 6:   Cold open assembly (2-3 options from selected clips)
  Step 7:   YouTube description + chapters (single code block, includes blog + transcript links)
  Step 8:   Narrative snippets extraction → blog post draft
  Step 9:   Social tagging strategy + platform post drafts
  Step 10:  Blog thumbnail + infographic generation (nano-banana-image-generator)
            → deliverable markdown files + images in guest folder
```

---

## Folder Structure

```
Studio/Podcast Studio/
├── PODCAST_SOP.md                  # Master SOP for Charlie + Chavilah
├── [Guest-Name]/                   # ONE folder per guest — everything lives here
│   ├── [guest-slug]-editor-handoff.md      # Deliverable: clips, hooks, cold open
│   ├── [guest-slug]-youtube-and-transcript.md  # Deliverable: YT description, chapters
│   ├── [guest-slug]-blog-and-social.md     # Deliverable: blog post, social drafts
│   ├── [guest-slug]-podcast-thumbnail-gen.jpg  # Generated image
│   ├── [guest-slug]-infographic-gen.jpg        # Generated image
│   └── prep/                       # Working files (research, drafts, checkpoints)
│       ├── SOURCE.md               # Raw transcript
│       ├── GUEST_SOCIAL_RESEARCH.md
│       ├── SEO_Keywords.md
│       ├── Checkpoint_1_Audit.md
│       └── Checkpoint_1_Selections.md
```

**One folder per guest.** Deliverables live at the root of the guest folder. Working files live in `prep/`. No separate handoff-packages directory.

**File naming rule (NEVER break):** Every deliverable file must include the guest slug in the filename. Never use generic names like `editor-handoff.md` or `blog-and-social.md` - these create duplicates across guest folders and are meaningless out of context. Use `math-academy-editor-handoff.md`, `amar-kumar-blog-and-social.md`, etc.

---

## Phase 1: Setup

### Step 0: Import from Notion

```bash
python3 /Users/charliedeist/Desktop/New\ Root\ Docs/.claude/scripts/notion_import.py <page_id> --title -o "Studio/Podcast Studio/[Guest-Name]/prep/SOURCE.md"
```

No LLM tokens. Direct Notion API to markdown. Creates the folder structure automatically.

To find page IDs for recorded episodes, query the Podcast Master Calendar Notion database (`d60323d3-8162-4cd0-9e1c-1fea5aad3801`) filtering for `Status = Recorded`.

### Step 0.5: Guest Social Research

Run a web search sub-agent to find:
- All personal + company handles (LinkedIn, X, IG, TikTok, YouTube)
- Which platform is their strongest (by engagement, not follower count)
- What kind of content they typically post/share
- Mutual connections with OpenEd
- Collaboration history (have they shared our content before?)

Output: `GUEST_SOCIAL_RESEARCH.md`

This informs clip selection (which platforms matter?) and social strategy (tagging, reshare potential).

### Step 1: SEO Keyword Research

Use DataForSEO to research 5-7 keywords related to the guest's topic. Focus on:
- Guest name + company (branded volume)
- Core topic terms (e.g., "microschool", "how to start a microschool")
- Related high-intent queries

Output: `SEO_Keywords.md` - consolidated summary, not individual briefs.

This informs title selection and blog post direction. YouTube title and blog title should be DIFFERENT:
- **YouTube title** = CTR optimized (curiosity, emotion, pattern interrupt)
- **Blog title** = SEO optimized (target keyword in title, search intent match)

---

## Phase 2: Audit + Human Review

### Step 2: Audit

Send to an Opus sub-agent with the full SOURCE.md. The audit produces:

1. **Angles** (3-5 distinct marketing angles, each with a 1-sentence pitch)
2. **Short clips** (5-8 candidates, 35-60 sec each — this is the ideal range)
   - Verbatim quotes with timestamps
   - Expand clips to include surrounding context; mark cuttable portions with ~~strikethrough~~ so the editor has options to trim
   - Category: Counterintuitive / Memorable / Relatable / Practical / Emotional
3. **Long clips** (3-4 candidates, 10-18 min each — must stand alone as independent YouTube content)
   - Narrative arc summary
   - Opening hook verbatim
4. **Cold open candidates** (2-3 montage arrangements using [SWOOSH] transitions)
5. **Blog format assessment** - Is this a "day-in-the-life" candidate or standard blog?
6. **Recording issues** - Technical artifacts the editor needs to handle (see below)
7. **Timestamp index** - Full chapter-by-chapter breakdown

**CRITICAL RULES:**
- All quotes VERBATIM. Never paraphrase.
- Mine the ENTIRE transcript, not just the first half.
- Bold over safe. Surprising, contrarian moments beat obvious observations.
- Target 5-8 clips in the audit (mine broadly), user will whittle to final picks with reasoning.

**Recording Issues (Step 6):**

Scan the full transcript for technical artifacts that require editor attention. These are NOT content issues (rambling, tangents) — they're production problems invisible to the content audit:

- **Pause/restart requests** - "Do you need to pause?", "Let me start that over", "Can we cut that?"
- **Recording glitches** - References to audio cutting out, screen freezing, "Can you hear me?"
- **Retakes** - Speaker explicitly redoing a section ("Let me say that again")
- **Room sound / environment** - Dogs barking, doorbells, construction mentioned in transcript
- **Platform artifacts** - Riverside/Zoom reconnection, "You froze for a second"

Format: timestamp + brief description. These go directly into the Editor Handoff so the editor can jump to those moments.

Output: `Checkpoint_1_Audit.md`

**Sub-agent prompt template:**
```
You are auditing a podcast transcript for content production.

Episode: [Guest Name]
Working directory: [path to prep/]

Read SOURCE.md (the full transcript).

Produce Checkpoint_1_Audit.md with:
- 3-5 angles (1-sentence pitch each)
- 5-8 short clip candidates (30-90 sec, verbatim with timestamps)
- 3-4 long clip candidates (10-18 min standalone, narrative arc + opening hook verbatim)
- 2-3 cold open montage arrangements
- Day-in-the-life assessment (yes/no with reasoning)
- Recording issues (pauses, retakes, glitches, room sound — NOT content tangents)
- Full timestamp index

Rules: ALL quotes verbatim. Mine the entire transcript. Bold over safe.
```

### HUMAN CHECKPOINT 1

Present the audit summary with **specific recommendations** — don't just present a menu. Claude should always recommend:
- **Primary angle** (recommended pick with 1-sentence case for it; list alternatives briefly)
- **Clips** (recommend 1-2 short + 0-2 long from the candidates, with reasoning for each selection and why others were cut)
- **Cold open** (recommend a specific arrangement, not just a list of options)
- **Blog format** (standard or day-in-the-life, with reasoning)

The user confirms or adjusts. The goal is to reduce decision load, not present every option equally.

### Step 3: Title + Thumbnail Variations

After angle selection, generate titles using the `youtube-title-creator` skill:
- 3-4 titles per angle using the 119 Creator Hooks frameworks (fewer, more opinionated picks)
- Each title includes: framework reference, psychological principles, thumbnail text suggestion
- Organize by angle so user can see which direction has the strongest title
- **Recommend a single best title** with reasoning. The goal is to go in with conviction on one title rather than A/B testing titles — YouTube needs ~200+ views to declare a winner, and splitting that across title variants delays the signal.

**YT Outlier integration:** Title recommendations should combine the `youtube-title-creator` frameworks with the YT outlier data from Step 1.5. The outlier report reveals which title patterns actually convert in the niche (question hooks, identity reframes, etc.) and which underperform (how-to, listicles). Use that data to weight framework selections — prioritize frameworks that match winning patterns in the outlier set.

**VERIFICATION RULE:** Any specific claim in a title (numbers, named concepts, frameworks) must cite the transcript moment that supports it. Never let a framework template inject a claim that isn't in the source.

**Retain 3-4 title options per angle** so the associate/editor can weigh in, but always lead with a strong recommendation.

**Thumbnail strategy: always fill all 3 A/B test slots.** YouTube gives you 3 thumbnail+title combo slots. Since we're being opinionated on the title (one winner), use all 3 slots for **complementary thumbnail variations** — same title, 3 different visual approaches. This maximizes what YouTube can learn from the test.

For each of the 3 thumbnail concepts, provide:
- Visual description (what the thumbnail image shows)
- On-screen text (2-4 words, COMPLEMENTARY to title - never repeats it. Title and thumbnail should carry different dimensions of the content. If title = personal story, thumbnail = shock/specificity. If title = practical, thumbnail = emotional. They work together like a headline and subhead, not like a headline said twice.)
- Why this variation tests something different (e.g., face vs. text-heavy vs. conceptual)

Output: `Title_Options_By_Angle.md`

### HUMAN CHECKPOINT 2

User selects:
- **YouTube title** (CTR optimized — one title, be opinionated. All 3 A/B slots share this title.)
- **Blog title** (SEO optimized, different from YouTube)
- **3 thumbnail variations** (different visual approaches to A/B test against the same title)

---

## Phase 3: Handoff Assembly

Everything converges into **3 markdown deliverables** in the guest's root folder.

### Output: 3 Notion Subpages

**Deliverable 1: Editor Handoff** (`[guest-slug]-editor-handoff.md`)
```markdown
# Editor Handoff: [Guest Name], [Company]

## Episode Info
- Guest, host, duration
- YouTube title (selected — one title, be opinionated)
- Blog title (selected, SEO optimized)
- Thumbnail variations (3 — use all YouTube A/B slots for visual variety, not title variety)

## Cold Opens
- 2-3 options, each 25-35 seconds
- Verbatim with ~~strikethrough~~ for cuts, *italics* for smoothing
- [SWOOSH] between unrelated moments
- Source timestamps for each segment

## Short Clips (1-2, max 3)
For each clip:
- Timestamp range
- On-screen hook options (3-4, * next to recommended)
- Full verbatim transcript with edit markup
- Caption (universal for FB, TikTok, IG, LinkedIn)
- X variant

## Long Clips (0-2 standalone, 10-18 min each)
For each clip:
- Timestamp range
- Narrative arc (setup → tension → payoff)
- On-screen hook options (3, * next to recommended)
- Opening hook verbatim
- Caption + X variant

## Recording Issues
- [HH:MM:SS] Brief description of issue (e.g., "Guest asks to restart answer")

## Edit Markup Key
```

**Deliverable 2: YouTube + Polished Transcript** (`[guest-slug]-youtube-and-transcript.md`)
```markdown
# YouTube + Polished Transcript: [Guest Name]

## YouTube Title
[Selected title]

## Thumbnail Variations (3 — all A/B tested against same title)
1. [Visual approach A] — on-screen text: "[Text]"
2. [Visual approach B] — on-screen text: "[Text]"
3. [Visual approach C] — on-screen text: "[Text]"

## YouTube Description
(Single code block - copy-paste ready. Includes:)
- Episode summary (2-3 sentences)
- Blog link: "Read the full blog post: opened.co/blog/[slug]" (ABOVE timestamps)
- Guest bio + social handles + resources
- OpenEd links
- Chapters (at the bottom)
- NO "In this episode you'll learn" bullet section
- NO transcript anchor link

## Blog Slug
[slug] → Full URL: https://opened.co/blog/[slug]

## Polished Transcript
(Generated from SOURCE.md. Section headers match chapter breakdown.
Appended to blog post under #transcript anchor.)
```

**Deliverable 3: Blog Post + Social** (`[guest-slug]-blog-and-social.md`)
```markdown
# Blog Post + Social: [Guest Name]

## SEO Metadata
- Blog title (SEO optimized), target keyword, search volume, blog slug

## Blog Post
- Full blog post draft (~1,200 words)
- Internal backlinks to relevant OpenEd content
- Guest handles + URLs in About section at bottom

## Social Tagging Strategy
- Guest handles per platform (table format)
- Platform priority ranking with reasoning

## Platform-Specific Post Drafts
For each platform, 1-2 ready-to-post drafts:
- **LinkedIn** (2 posts: episode announcement + mid-week angle)
- **X/Twitter** (2 posts: announcement + quote/stat hook)
- **Instagram** (2 posts: carousel concept + quote card)
- **Facebook** (1 post: full episode share)

## Distribution Timing
- Week 1: Launch day (all platforms) + staggered follow-ups
- Week 2: Evergreen angles (repurposed quotes, stats)
- Ongoing: Guest reshare coordination
```

### Step 8: Blog Post (Narrative Snippets Method)

Before writing the blog post, extract narrative beats from the transcript:

1. **Scan for story seeds** - transitions, contrast markers, failure admissions, turning points
2. **Extract 3-5 narrative arcs** using the 6-beat structure:
   - SETUP → DISASTER → FAILED APPROACH → INSIGHT → RESOLUTION → REFLECTION
3. **Pick one arc as the spine** of the blog post
4. **Weave other arcs** as supporting threads

The blog post should read like a great New Yorker profile at blog scale - observational, unhurried, letting scenes and quotes do the work. Voice: Ela (warm, curious, conversational) elevated by narrative craft.

**Blog post sub-agent reads:** SOURCE.md + GUEST_SOCIAL_RESEARCH.md + blog direction from subpage 3
**Blog post sub-agent uses:** `narrative-snippets` → `podcast-blog-post-creator` → `ghostwriter`
**Output:** ~1,200 word draft with SEO headers, 3-5 verbatim quotes, YouTube embed placeholder

**Integration requirements:**
- Include guest handles and URLs from GUEST_SOCIAL_RESEARCH.md (bio links, company URL)
- Scan published OpenEd content for internal backlinking opportunities (link to relevant articles, guides, and other podcast episodes)
- About section at bottom must include guest social handles with links

### Blog Slug Convention

Generate the slug during Phase 3 so it can be embedded in the YouTube description before publishing.

**Pattern:** `opened.co/blog/[seo-keyword-slug]`
**YouTube description must include:**
- `Read the full blog post: https://opened.co/blog/[slug]` (placed ABOVE timestamps)

### Step 10: Blog Thumbnail + Infographic

Generate visual assets using the `nano-banana-image-generator` skill. Save all images in the **guest folder** alongside the markdown deliverables.

**Required assets:**
1. **Blog thumbnail** (16:9, watercolor-line style) - conceptual illustration for the blog post header and Webflow CMS
2. **Infographic** (16:9, watercolor-line with Vox-style hierarchy) - data visualization or concept map for social sharing

**Optional assets (if the episode warrants them):**
- Quote card (1:1, opened-editorial style) - for Instagram/LinkedIn
- Instagram carousel intro slide (4:5, watercolor-line)

**Workflow:**
```bash
# Blog thumbnail
python3 ".claude/skills/nano-banana-image-generator/scripts/generate_image.py" \
  "prompt" --model pro --aspect 16:9 \
  --seo-name "[guest-slug]-podcast-thumbnail" \
  --context "[Blog title]" \
  --output "Studio/Podcast Studio/[Guest-Name]/"

# Optimize for Webflow
python3 ".claude/skills/nano-banana-image-generator/scripts/image_optimizer.py" \
  "Studio/Podcast Studio/[Guest-Name]/[file].jpg" \
  --use thumbnail
```

**Style selection guide:**
- **watercolor-line** (DEFAULT) - Warm, editorial, works for narrative/emotional episodes
- **opened-editorial** - Conceptual wit, better for data-driven or contrarian episodes
- **minimalist-ink** - High contrast, good for "bold statement" thumbnails

**Concept brainstorm:** Before generating, brainstorm 4-6 visual concepts with the user. Avoid generic education cliches (no lightbulbs, no raised hands, no stacks of books). Favor metaphor over literal depiction.

**Infographic principles:**
- Visual hierarchy does the work, not text
- Labels only, no explanatory paragraphs
- Icons should be hand-drawn style (not emoji)
- Clear left-to-right or top-to-bottom flow
- Pull key stats from the transcript (the guest's own data is most compelling)

### Notion Export

Push each subpage using:
```bash
python3 .claude/scripts/notion_markdown.py [file] --parent-id [episode-page-id] --title "[Subpage Title]"
```

Never use `--update` on the master episode page (it overwrites). Always create subpages.

### On-Screen Hook Standards

On-screen text is the #1 visual element. It does the PRIMARY work of stopping a scroll.

**Requirements per clip:**
- 3-4 hook options per clip
- Star (*) next to recommended pick
- No category labels, no rationale - just the options

**Hook categories:**
- **Polarizing** - Takes a side. "Schools trap families?"
- **Counter-Intuitive** - Surprises. "The school choice argument nobody makes"
- **Direct Challenge** - Confronts viewer. "Your kid's teacher hates their job"
- **Curiosity Gap** - Opens a loop. "55% want to quit"

**Complementarity principle:** On-screen text should ADD context that makes the audio land harder, not just label the clip. The gap between what you read and what you hear creates curiosity.

**"First 3 words" test:** The first 3 words someone reads do 80% of the work. Front-load the punch.

**Length variety (REQUIRED):** Every set of 3-4 hook options must span at least 2 length categories:
- **Punchy** (2-4 words): "Schools trap families?"
- **Statement** (5-8 words): "The school choice argument nobody makes"
- **Narrative** (9-15 words): "There's a cost every morning when a five-year-old walks in and knows"
- **Full quote** (15+ words): "If your strategy for keeping families is making sure they can't leave, you've lost"

If all hooks are the same length, redo them. The editor needs options that work at different scroll speeds.

### Descript Underlord Integration (Automated Clip Creation)

When clips and hooks are finalized, auto-generate Descript Underlord prompts to create social clips without opening the app. Uses the **descript-api** skill (`OpenEd Vault/.claude/skills/descript-api/SKILL.md`).

**Workflow:**
1. From clip markup, take the starred (*) hook option as the composition name
2. Build Underlord prompt: `Create a vertical 9:16 Instagram Reel, under 60 seconds. Extract the section where [SPEAKER] talks about [TOPIC]. Name the composition "[HOOK TEXT]". Apply the [LAYOUT] layout. Add classic karaoke-style captions. Apply Studio Sound.`
3. Send via `POST /jobs/agent` with the episode's `project_id`
4. Poll until complete, review at `project_url`

**Key:** The composition name IS the on-screen text when using layout packs (e.g. "yellow text title"). So the hook you write becomes the text viewers see.

**Known project IDs:** Listed in `descript-api` skill. To find new ones, check share URLs in `Published Content/Podcasts/*.md` and hit `/published_projects/{slug}`.

### Edit Markup Convention

```
~~strikethrough~~ = cut this (editor removes)
*italics* = minor smoothing edit (change spoken word)
[SWOOSH] = visual transition between unrelated segments
[AMAR] = speaker label
```

---

## Key Principles

1. **Verbatim only.** All quoted transcript exactly as spoken. Cut and rearrange, never paraphrase.
2. **Three subpages.** Everything flows into 3 Notion subpages: Editor Handoff, YouTube + Transcript, Blog + Social.
3. **Mine the whole transcript.** The strongest moment might be at minute 48.
4. **Bold over safe.** Contrarian > obvious. Tension > comfort.
5. **Clips: quality over quantity.** Short: 1-2 best (3 maximum), always with a recommended pick and reasoning. Long: 1-2 standalone clips (10-18 min) only if warranted — these must work as independent YouTube content, not just extended segments. Always recommend specific selections with reasoning for why each was chosen and why others were cut.
6. **Same caption everywhere.** One caption per clip for FB/TikTok/IG/LinkedIn. Optional X variant.
7. **Title + thumbnail are a pair.** Be opinionated on one title (don't split A/B test across titles). Use all 3 YouTube A/B slots for complementary thumbnail variations instead. Thumbnail complements title, never repeats it.
8. **YouTube title != blog title.** YouTube = CTR. Blog = SEO.
9. **On-screen hooks are the #1 priority.** 3-5 variations per clip, not afterthoughts.
10. **Guest research informs everything.** Know their platforms before selecting clips.

---

## Skill Dependencies

| Step | Skills Used |
|------|-------------|
| Step 0 | `notion_import.py` (script, not skill) |
| Step 1 | `seo-research` / DataForSEO |
| Step 3 | `youtube-title-creator` (119 frameworks) |
| Step 4 | `video-caption-creation` (hook categories, Triple Word Score) |
| Step 6 | `cold-open-creator` (optional reference) |
| Step 8 | `narrative-snippets` (extract beats) → `podcast-blog-post-creator` → `ghostwriter` (voice) |
| Step 8 alt | `day-in-the-life` (if applicable) |
| Step 10 | `nano-banana-image-generator` (thumbnail + infographic) |
| Quality | `quality-loop` (for blog post draft) |

---

## Common Mistakes

- Fabricating claims in titles (e.g., "6 Levels of Teaching" when transcript has no such framework)
- Single on-screen hook per clip instead of 3-5 options
- Generating platform-specific captions (same caption everywhere, X variant only)
- Thumbnail text that repeats the title
- Ignoring guest's social presence until the end
- SEO research after title selection instead of before
- Cold opens before clip selection (cold opens are assembled FROM clips)
- 25+ snippet inventory when 5-8 targeted clips is better
- **Fragmenting clips that belong together.** Prefer 2 great clips over 5 mediocre ones. If consecutive transcript segments form one teaching arc (e.g., principle → examples → metaphor), keep them as a single long-form clip (10-18 min), not 3 separate 45-sec clips. Long clips should be standalone YouTube content — a complete idea someone would watch independently. The audit mines broadly (5-8 candidates); the human whittles to final selections with edit markup.
- **Skipping YT outlier research.** Always run `/yt-outlier` on 2-3 niche queries BEFORE the title step. The outlier data reveals which title patterns actually convert (question hooks, identity reframes, etc.) and which underperform (how-to, listicles in parenting). Study the #1 outlier deeply — reverse-engineer title anatomy, thumbnail, search intent, and credential usage. Then model your title on the winning structure.
- **Ignoring lead magnet opportunities.** During social strategy, search the OpenEd archive for existing content related to the episode topic. If 3+ pieces exist, propose bundling them into a lead magnet (PDF playbook, Notion template) with a HubSpot landing page. The lead magnet link goes in the YouTube description topline and social CTAs.

---

## Notion Locations

| Resource | ID | Notes |
|----------|----|-------|
| Podcast Master Calendar DB | `d60323d3-8162-4cd0-9e1c-1fea5aad3801` | Filter `Status = Recorded` for ready episodes |
| Each episode page | Contains: Guest Info toggle, Relevant Context toggle, Rough Transcript toggle | |
| Notion export script | `.claude/scripts/notion_markdown.py` | `--parent-id` creates subpage, `--update` replaces content |
| Notion import script | `.claude/scripts/notion_import.py` | Pulls page to local markdown |

**Subpage push pattern:**
```bash
# Create 3 subpages under the episode's Notion page
# Files use [guest-slug] prefix (e.g., math-academy-, amar-kumar-)
python3 .claude/scripts/notion_markdown.py [Guest-Name]/[guest-slug]-editor-handoff.md \
  --parent-id [episode-page-id] --title "Editor Handoff"
python3 .claude/scripts/notion_markdown.py [Guest-Name]/[guest-slug]-youtube-and-transcript.md \
  --parent-id [episode-page-id] --title "YouTube + Polished Transcript"
python3 .claude/scripts/notion_markdown.py [Guest-Name]/[guest-slug]-blog-and-social.md \
  --parent-id [episode-page-id] --title "Blog Post + Social"
```

---

## Internal Backlinking (Step 8)

When drafting the blog post, scan for internal link opportunities:

1. **Search published content** - `Master_Content_Index.md` (`.claude/references/`) lists 400+ articles by tag
2. **Search podcast episodes** - Other published episodes in `Studio/Podcast Studio/`
3. **Search SEO content** - `Studio/SEO Content Production/` for topic overlaps
4. **Natural placement** - Links should feel like helpful context, not SEO stuffing. 3-5 internal links per blog post is the sweet spot.

**Link format:** `[anchor text](https://opened.co/blog/[slug])` - use descriptive anchors, not "click here."

---

## Next Priorities (Skill Improvements Backlog)

- [ ] Build `youtube_autocomplete.py` using DataForSEO for YouTube search suggestions
- [ ] Research exemplar podcast YouTube/IG channels for on-screen hook reference library
- [ ] Improve `video-caption-creation` skill with complementarity principle + real education creator examples
- [ ] Build dedicated title+thumbnail sub-agent with better variation examples from Creator Hooks
- [ ] Nearbound email templates (solo guest vs. guest-with-team, auto-populate links)
- [ ] Clip performance tracking (which hooks/captions drive engagement, feed back into hook library)
- [x] Descript Underlord integration (auto-generate Underlord prompts from clip markup) — see `descript-api` skill
- [ ] Polished transcript auto-generation as sub-agent (currently manual step)
- [ ] YouTube Shorts optimization (vertical crop guidance in editor handoff)
- [x] Add internal linking step (integrated into Step 8 blog post sub-agent)
- [x] Platform-specific social post drafts (integrated into Subpage 3 template)
- [x] Hook length variety requirement (integrated into On-Screen Hook Standards)
- [x] Blog thumbnail + infographic generation (Step 10)

---

## References

- `references/checkpoint-1-template.md` - Detailed audit template
- `references/checkpoint-2-example.md` - Cold open + clip example (Claire Honeycutt)
- `references/checkpoint-3-example.md` - YouTube strategy example
- `references/checkpoint-4-example.md` - Polished transcript + blog example
- `references/day-in-the-life-format.md` - Day-in-the-life blog template
- `SKILL_v1_archive.md` - Previous 4-checkpoint system
- `Studio/Podcast Studio/PODCAST_SOP.md` - Master SOP for Charlie + Chavilah

---

## Production Calendar (Feb 2026)

| Episode | Guest | Publish | Sprint Status | Handoff Package |
|---------|-------|---------|---------------|-----------------|
| Mason Ember | Mason Ember | Feb 5 | PUBLISHED | `Studio/Podcast Studio/Mason Ember/` |
| Claire Honeycutt R2 | Claire Honeycutt | Feb 12 | Sprint DONE | `Claire-Honeycutt-Round-2/` |
| Amar Kumar | Amar Kumar | Feb 19 | Sprint DONE | `Amar-Kumar/` |
| Bria Bloom | Bria Bloom | Feb 26 | Needs full sprint | — |

---

*Rewritten Feb 6, 2026. v2 after Amar Kumar + Claire Honeycutt sessions.*
