---
name: hook-writer
description: Generate, diagnose, and refine video/content hooks using Kallaway's frameworks. Four modes — archetype (6 variants), snapback (3-line formula), power-word (6-bucket construction), and diagnose (4-mistake audit + rewrite). Every hook passes through the same quality gate. Use when writing hooks for YouTube videos, Reels, newsletters, blog posts, or any content that needs to grab attention in the first 2 seconds.
---

# Hook Writer

Generate and refine hooks for any content format. Based on Kallaway's hook frameworks (extracted from 66 chunks across 8 episodes analyzing 100+ viral videos).

## When to Use

- Writing a YouTube video hook or title
- Opening a newsletter, blog post, or social post
- Auditing an existing hook that isn't performing
- Generating multiple hook options to test
- Learning hook anatomy (power-word mode with annotations)

**Not for:** Full video scripts (use `video-script-writer`), thumbnails, SEO titles without a hook angle.

---

## Modes

### Mode 1: `archetype` — Generate 6 Variants

Given a topic, produce one hook per archetype. Each archetype has a distinct contrast mechanism.

**The 6 Archetypes:**

| Archetype | Contrast Mechanism | Pattern |
|-----------|-------------------|---------|
| **Fortune Teller** | Present vs. future | "X is going to change everything about Y" |
| **Experimenter** | Old method vs. new method | "I just tried X and here's what happened" |
| **Teacher** | Failing vs. winning | "Here's how to X (step-by-step)" |
| **Magician** | Visual stun + redirect | "Check this out..." + unexpected reveal |
| **Investigator** | Unknown vs. revealed | "Nobody is talking about X" / "The secret behind Y" |
| **Contrarian** | Conventional wisdom vs. your belief | "You're doing X wrong. Here's why." |

**Process:**
1. Parse the topic for its core subject, audience pain point, and available angle
2. For each archetype, generate a hook following its contrast mechanism
3. Score each hook's contrast strength (1-10) based on the distance between the viewer's assumed belief (A) and the alternative (B)
4. Recommend the archetype whose contrast best fits the topic and audience
5. Run all 6 through the quality gate

**Output:** 6 hook variants with contrast scores + recommendation of strongest fit.

---

### Mode 2: `snapback` — 3-Line Formula

The tightest hook structure. Three lines, three moves.

**The Formula:**

**Line 1 — Context Lean:** State the topic in as few words as possible for instant clarity. Add one lean-in: common ground, benefit, pain point, metaphor, or something mind-blowing. The viewer self-selects in or out after this line.

**Line 2 — Scroll Stop:** Begin with a contrasting word ("But," "However," "Yet"). This line stuns — stops forward momentum. Sets up the haymaker without delivering it.

**Line 3 — Contrarian Snapback:** Snap the viewer in the opposite direction. The bigger the shock, the bigger the snap. This opens the curiosity loop that the rest of the content must close.

**Contrast types:**
- **Stated:** Explicitly name both A and B ("Most people do X, but actually Y")
- **Implied:** State B only, let A be assumed ("This method is 8x more effective")

**Process:**
1. Write Line 1 (context lean)
2. Write Line 2 (scroll stop interjection)
3. Write Line 3 (contrarian snapback)
4. Run through the quality gate
5. If any check fails, auto-rewrite the offending line

**Output:** 3-line hook + full diagnostic results.

---

### Mode 3: `power-word` — 6-Bucket Construction

Build a hook by filling structural word-bucket slots. Produces an annotated hook that shows *why* each word is there. Best for learning and for hooks that need to be extremely tight (titles, thumbnails, Shorts).

**The 6 Buckets:**

| Bucket | Required? | What it does | Example |
|--------|-----------|-------------|---------|
| **Subject** | Yes | Who is this about? | "I", "you", "Tesla" |
| **Action** | Yes | What did/will they do? | "grew", "built", "discovered" |
| **Objective** | Yes | What's the end state? | "100K subscribers", "clear skin" |
| **Contrast** | Yes | What's the gap between A and B? | "zero to 100K", "without Accutane" |
| **Proof** | Optional | Why should I believe you? | "again", "after 10 years" |
| **Time** | Optional | How fast? | "in 30 days", "overnight" |

**Process:**
1. Fill Subject → Action → Objective → Contrast (4 required buckets)
2. Optionally add Proof and/or Time
3. Assemble into a natural sentence
4. Produce 3 variants: minimal (4 buckets), with proof, with proof + time
5. Generate a copywork template with [BLANKS] for reuse on future topics
6. Annotate every word's function
7. Run through quality gate

**Output:** Annotated hook + 3 variants + reusable copywork template.

---

### Mode 4: `diagnose` — 4-Mistake Audit + Rewrite

Takes an existing hook and audits it against the 4 failure modes. Diagnoses the problem, then rewrites to fix it.

**The 4 Mistakes:**

**1. Delay** — Topic doesn't appear in the first sentence. Every word before topic introduction = viewer decay.
- Fix: Move the topic to the very first clause.

**2. Confusion** — Jargon, passive voice, or ambiguous phrasing. If a sentence can be interpreted more than one way, it will be.
- Fix: Rewrite at 6th-grade reading level. Active voice. No undefined terms.

**3. Irrelevance** — "I/me" framing dominates. Pain point isn't agitated. Content feels "nice to have" not "need to have."
- Fix: Flip to "you/your" framing. Replace trend-reporting with pain-point-solving.

**4. Disinterest** — No clear A-vs-B contrast. Both A and B are obvious or expected. No curiosity loop.
- Fix: Increase the distance between A and B. Make B more shocking, specific, or counter-intuitive.

**Process:**
1. Run all 4 checks against the existing hook
2. Score each dimension (clarity, curiosity, relevance, comprehension) from 1-10
3. Flag specific mistakes with severity (minor/major/critical)
4. Rewrite the hook, fixing all flagged issues
5. Suggest visual alignment (3-5 word text overlay + key visual)
6. Run rewrite through quality gate to confirm it passes

**Output:** Diagnostic report + scores + rewritten hook + visual alignment suggestion.

---

## Quality Gate (Applied to ALL Modes)

Every hook produced by any mode must pass these checks before output:

| Check | Rule |
|-------|------|
| **Length** | 1-3 sentences max. Snapback mode: exactly 3 lines. Power-word: 1-2 sentences. |
| **Topic clarity** | Topic identifiable in the first sentence |
| **Contrast** | Clear A-to-B contrast present. Must be falsifiable (not a truism like "good to better") |
| **Reading level** | 6th grade max. No jargon or undefined terms |
| **You-framing** | "You/your" appears at least once (exception: Experimenter archetype uses "I" by design) |
| **No vague openers** | Never use "Wait till you see this" / "You're never going to believe this" / "This is insane" |
| **Contrast score** | Rate the A-B distance 1-10. Flag anything below 5. |

If a hook fails any check, rewrite before presenting.

---

## Examples

**Input:** Topic: "Most YouTube creators waste their first 5 seconds." Audience: aspiring YouTubers.

**Archetype mode (Contrarian):**
> "The first 5 seconds of your video are worthless. Not because they don't matter — because you're filling them with the wrong words."
> Contrast: 9/10 (conventional = "first 5 seconds are everything" vs. "you're using them wrong")

**Snapback mode:**
> "Every YouTube guru tells you the first 5 seconds decide everything. But the data shows something different. The creators getting 70% retention aren't hooking harder — they're hooking smarter."

**Power-word mode:**
> "You [subject] are wasting [action] your first 5 seconds [objective] on filler that kills retention [contrast]."
> Copywork template: [SUBJECT] are [ACTION] your [OBJECTIVE] on [CONTRAST].

**Diagnose mode (auditing a weak hook):**
> Original: "In this video, I'm going to share some tips about making better YouTube hooks."
> Diagnosis: Delay (4 filler words before topic), Irrelevance ("I'm going to share" = I-framing), Disinterest (no contrast — "some tips" creates zero curiosity)
> Rewrite: "Your hooks are losing viewers in the first 2 seconds. Here are 3 fixes that doubled my retention."

---

## Related Skills

- **video-script-writer** — Uses hook-writer for its intro, then handles body + outro
- **youtube-title-creator** — Title-specific optimization (overlaps with power-word mode)
- **video-caption-creation** — On-screen text hooks for short-form

---

*The hook is the highest-leverage moment in any piece of content. Everything after it is earned by the first 2 seconds.*
