---
name: voice-dna
description: Extract a writer's voice from their archive, produce a reusable voice fingerprint, then write in that voice with calibration. Two modes — EXTRACT (analyze samples → produce fingerprint) and WRITE (use fingerprint → produce content). For any writing task involving Charlie's voice, skip to the Charlie Deist Fingerprint section. For extracting anyone's voice, start at Phase 1.
priority: root
always_invoke: true
---

# Voice DNA

Two jobs: **extract** a voice from writing samples, and **write** in that voice reliably.

When the rules and the samples conflict, **the samples win.**

---

## Phase 1: EXTRACT — Build a Voice Fingerprint

Give me 5-15 pieces of someone's best writing. I'll analyze them across 7 dimensions and produce a `voice-dna.md` artifact that any future session can load.

### What to feed me

- **Minimum:** 5 pieces, 500+ words each
- **Ideal:** 10-15 pieces across different formats (essays, newsletters, social, emails)
- **Best signal:** Pieces the writer is proudest of — where they sound most like themselves
- **Bad signal:** Ghostwritten content, heavily edited committee docs, SEO filler

### The 7 Dimensions I Extract

#### 1. Sentence Rhythm (the strongest signal)

Not average sentence length — the **pattern** of alternation. This is what readers feel but can't name.

**What I measure:**
- Long/medium/short ratio (e.g., 60/25/15)
- Where short sentences land (after long builds? as openers? as closers?)
- Dominant punctuation signature (em dashes, semicolons, parentheticals, ellipses)
- Fragment frequency and placement

**Example extraction — Charlie Deist:**
> Ratio: 60% long clause-heavy (15-30+ words), 25% medium, 15% short declaratives
> Signature: Em dashes constantly — for asides, appositives, tonal pivots
> Fragments: Rare drum hits, never the baseline. Used for emphasis after long passages.
> Paragraphs: 2-5 sentences, allowed to run long when building momentum

**Example extraction — Dan Koe:**
> Ratio: 40% short (under 8 words), 35% medium, 25% long
> Signature: Line breaks as punctuation. One-sentence paragraphs are the norm.
> Fragments: Frequent. Often isolated on their own line.
> Paragraphs: 1-2 sentences. Rarely more than 3.

**Why this matters:** An AI asked to "write casually" defaults to medium-length sentences with occasional fragments. That sounds like every AI. Rhythm is identity.

#### 2. Structural Patterns

How does the writer build a piece? Where does the thesis appear? How do they open, transition, close?

**What I measure:**
- **Opener type:** In-motion scene? Question? Anecdote? Thesis statement? Contradiction?
- **Argument shape:** Narrative-first (story → point)? Thesis-first (claim → evidence)? Spiral (circling back)?
- **Transition style:** Invisible (no transition words)? Conversational ("But here's the thing")? Section breaks?
- **Closer type:** Call to action? Open question? Return to opening image? Quiet landing?

**Example — Charlie Deist opens by arriving in motion:**
> "With emotionless tears streaming down my face — stymied as I was by the inescapable reality that I was an addict — I decided to mix up my routine that day."

> "About 10 years ago, I got the idea to get my captain's license and start some kind of sailing business on San Francisco Bay."

He never opens with a thesis. The reader discovers the point through the story.

**Example — typical AI opener (kill this):**
> "In today's fast-paced world, finding your authentic voice has never been more important."

Nobody writes like that. Every AI does.

#### 3. Vocabulary Fingerprint

Not what words they use — what words they **overuse**, what they **never** use, and what **surprises**.

**What I measure:**
- Signature words that recur across pieces (physical verbs? Latin roots? slang?)
- Words conspicuously absent (corporate speak? hedging words? superlatives?)
- Register shifts — where do they go formal? Where do they go casual?
- Metaphor family — do they draw from nature? Sports? War? Cooking? Sailing?

**Example — Charlie Deist:**
> Physical verbs for abstract processes: "sanded down" not "improved," "bolted on" not "added"
> Metaphor family: Sailing, homesteading, marching, classical references
> Never uses: leverage, utilize, landscape, comprehensive, robust, game-changer
> Register shift: Classical references treated as living conversation partners, then punctured with self-deprecation

**Example — Dan Koe:**
> Metaphor family: Consciousness, evolution, self-creation
> Signature: "Most people" as a recurring frame for contrast
> Never uses: Hedging qualifiers ("perhaps," "it could be argued")

#### 4. Tone Markers

The emotional register and how it shifts within a piece.

**What I measure:**
- **Default register:** Authoritative? Conversational? Confessional? Academic?
- **Humor type:** Self-deprecating? Deadpan? Absurdist? Observational? None?
- **Vulnerability pattern:** Where do they get honest? How do they signal it?
- **Confidence level:** Do they hedge? Commit? Qualify then commit?

**Example — Charlie Deist:**
> Default: Conspiratorial peer with earned authority
> Humor: Self-deprecating, parenthetical, structurally surprising. Never tells jokes. Humor from juxtaposition — the lofty and the mundane.
> Vulnerability signal: "I should be honest:" / confessional turns preceded by self-aware throat-clearing
> Confidence: Admits failures constantly (cancelled marches, addiction, parenting struggles) but has done the things he writes about. The admission IS the authority.

**The confessional turn — a specific device:**
> "Suffice it to say, my mood hasn't matched the often lofty tone I employ when writing about subjects like the JFK 50 Miler — the Presidential Fitness Challenge *par excellence*, on which our nation's vitality supposedly depends! (See? there I go again with the loftiness.)"

He names his own tendency, undercuts it, then continues. This is a Charlie signature. An AI would never do this unprompted.

#### 5. Anti-Patterns (What the writing is NOT)

Often more diagnostic than positive patterns. What the writer avoids tells you what kind of writer they are.

**What I measure:**
- Constructions they never use
- Tones they never strike
- Structural moves they avoid
- What would feel "off" to their regular readers

**Example — Charlie Deist:**
> Never: Listicle structure, numbered "5 ways to..." framing
> Never: Performative emotional narration ("This hit me hard" / "I was shook")
> Never: Cable news dramatic fragments ("No fluff. No filler. Just results.")
> Never: Thesis-first academic structure
> Never: Corporate self-help language or fake urgency

#### 6. Reference World

The cultural, intellectual, and experiential universe the writer draws from. This is what makes voice three-dimensional.

**What I measure:**
- Who do they cite? (Authors, thinkers, friends, family, nobody?)
- What domains do they reference? (History, sports, theology, pop culture, personal experience?)
- How do they cite? (Formal attribution? Casual name-drop? Embedded allusion?)
- Are references decorative or structural? (Do they add to the argument or just signal erudition?)

**Example — Charlie Deist:**
> References: JFK, Yeats, Carl Schmitt, Camille Paglia, St. Paul, Wendell Berry — treated as living conversation partners, not museum pieces
> Domains: American history, theology, sailing, farming, classical philosophy, counterculture
> Style: Casual integration — "to borrow a term from Camille Paglia" — not footnoted, not showy
> Function: Always structural. Every intellectual reference tethered to something physical — a mile marker, a cow, a burn pile.

#### 7. Micro-Phrases (The Fingerprint Within the Fingerprint)

Every writer has verbal tics — tiny recurring phrases that are unconscious but unmistakable to regular readers.

**What I measure:**
- Transition phrases they repeat
- Sentence starters they favor
- Parenthetical fillers
- How they signal a shift in direction

**Example — Charlie Deist:**
> "More on this in a minute" — his pacing/teaser
> "I should be honest:" — confessional transition
> "And yet for all functional purposes" — rhetorical concession
> "Okay, Keith." — casual dismissiveness of bad arguments
> "(See? there I go again...)" — self-awareness aside
> "(whatever that meant)" — deflating his own past seriousness

---

### Extraction Prompt (copy-paste for any writer)

Run this after loading the writing samples:

```
Analyze these writing samples across 7 dimensions. For each dimension, provide:
1. The pattern you observe (with specific measurements where possible)
2. One direct quote from the samples that exemplifies it
3. One sentence describing what this writer would NEVER do

Dimensions:
1. Sentence Rhythm — long/medium/short ratio, dominant punctuation, fragment frequency
2. Structural Patterns — opener type, argument shape, transition style, closer type
3. Vocabulary Fingerprint — overused words, absent words, metaphor family, register shifts
4. Tone Markers — default register, humor type, vulnerability pattern, confidence level
5. Anti-Patterns — constructions never used, tones never struck, structural moves avoided
6. Reference World — who they cite, how they cite, decorative vs. structural
7. Micro-Phrases — recurring verbal tics, transition phrases, parenthetical fillers

Then produce a voice-dna.md artifact that another AI session could load to write in this voice. Include 2-3 of the strongest original samples as ground truth.
```

---

## Phase 2: CALIBRATE — Test and Refine

After extraction, write 3 test paragraphs on different topics. The writer rates each 1-5 and marks specific failures:

| Tag | Meaning | Action |
|-----|---------|--------|
| `WRONG` | This isn't how I'd say this at all | Rewrite the rule that produced it |
| `OVERSTATED` | I do this sometimes, but you're overdoing it | Dial back the frequency |
| `MISSING` | Something I always do is absent here | Add a new rule or micro-phrase |
| `NEEDS_NUANCE` | Close but the tone is slightly off | Add a contextual qualifier |
| `TOO_FORMAL` | This is stiff — I'm more casual here | Adjust register for this context |
| `LLM_ISM` | This sounds like AI, not me | Add to the anti-pattern list |

Run 2-3 calibration rounds. Each round should cut the error rate in half. After round 3, the fingerprint is usually stable.

**Expected progression:**
- Round 1: "This is maybe 60% me" — the big structural patterns are right, the texture is wrong
- Round 2: "Getting close, maybe 80%" — rhythm and tone are landing, micro-phrases need work
- Round 3: "I'd publish this with light edits" — 90%+ match, remaining issues are preference, not pattern

---

## The Tells: Why Banning Words Isn't Enough (And What Actually Works)

### The Detection Hierarchy

Detectors don't primarily detect words. They detect **statistics**. Banning "delve" and "leverage" is like cleaning up the crime scene without changing the criminal's DNA. Here's what actually moves the detection score, ranked by impact:

| Rank | Signal | What It Is | Impact |
|------|--------|-----------|--------|
| **1** | **Burstiness** | Sentence length variance across the document. AI clusters at 14-22 words. Humans have fat tails (3-word punches next to 45-word periods). | Highest — the #1 statistical signal. |
| **2** | **Perplexity** | How predictable is each word given its context? AI picks high-probability tokens. Replacing "delve" with "examine" just swaps one probable word for another. | High — requires genuinely unexpected word choices, not safe synonyms. |
| **3** | **Specificity density** | Named people, real dates, actual numbers, place names. Each is a low-frequency token that raises entropy. "A major company" vs. "Stripe in 2021." | High — directly raises token entropy. |
| **4** | **Document structure** | Five-paragraph essay pattern (intro → thesis → body → conclusion that restates). AI defaults to this template. | Medium-high — requires changing argument shape, not words. |
| **5** | **Epistemic markers** | Genuine first-person uncertainty ("I don't know," "I've changed my mind"). NOT performative hedging ("it's worth noting"). AI underproduces real uncertainty. | Medium — detectors distinguish real hedging from performance. |
| **6** | **Register shifts** | Moving from formal → casual → raw within one piece. AI maintains one register throughout. The variance itself is a signal. | Medium |
| **7** | **Transition frequency** | "Furthermore," "moreover," "additionally" appear 3-5x more in AI than human text. Measurable and statistically significant. | Medium |
| **8** | **Word bans** | Removing known AI vocabulary. Necessary but lowest individual impact. | Low by itself — cosmetic without the above. |

**The key insight:** You can ban every word on the list and still score as AI if the burstiness is flat, the perplexity is low, and the structure follows the template. The ban list is the final polish, not the primary intervention.

### Why Synonym Swapping Fails (The Mechanism)

Consider this AI sentence:
> "This represents a pivotal moment in the evolution of how organizations think about culture."

Replace every flagged word:
> "This is a key moment in the development of how organizations think about culture."

Both sentences have the same sentence length, structure, register, specificity (zero), and perplexity (every word is the statistically likely next token). The ban list changed the paint. The building is identical.

**What actually fixes it:**
> "When Stripe rewrote their culture doc in 2021, three VPs quit within a month. That's the moment I started paying attention."

Different burstiness (two sentences: 15 words, 10 words). Higher perplexity (Stripe, 2021, three VPs, quit). Specific detail. Register shift (analytical → personal). Genuine epistemic grounding (the writer was there). No word from any ban list appeared in the original — and yet the rewrite is undetectably human while the original screams AI.

### The 8 Interventions (Do These In Order)

After generating a draft, apply these fixes from highest impact to lowest:

**1. Break the burstiness.** Find sentence clusters in the 14-22 word range. Split some into 3-5 word declaratives. Merge others into 35+ word periodic sentences. Target: no more than 40% of sentences in any 8-word range band.

**2. Inject specificity.** Every abstraction resolves into a named thing. "Studies show" → "A 2019 Yale study of 400 students." "Recently" → "Last March." "A major company" → "Stripe." Each proper noun raises entropy.

**3. Add genuine uncertainty.** Not "it's important to note" (performative). "I genuinely don't understand why X." "I've changed my mind on this." "I may be wrong." These are the epistemic markers that human writing produces and AI underproduces.

**4. Break the template.** If it's intro → thesis → body → conclusion, change the shape. Delay the thesis. Start mid-story. End with a question. Return to the opening image. Anything but the five-paragraph default.

**5. Shift register.** At least one moment per piece where the tone changes. A formal argument interrupted by a casual aside. A technical explanation followed by a blunt personal reaction.

**6. Delete transitions without replacement.** Don't replace "furthermore" with "also" — delete the whole signpost. Real writing connects through momentum, not narration. If two paragraphs need a transition word to connect, the problem is the paragraphs.

**7. Introduce self-contradiction.** One moment where the text revises itself. "Actually, I understated that." "Wait — that's not quite right." AI never changes its mind mid-text. Humans do it constantly.

**8. Clean up the vocabulary.** NOW do the word bans. At this point they're the final polish on text that's already structurally human.

---

### The 30 Patterns (Organized by What Catches Them)

What follows is still useful — these are the observable patterns that editors, readers, and detectors flag. But know that patterns 1-4 are the **least impactful** to fix in isolation. The structural interventions above matter more.

### Surface Tells (Human Readers Catch These First)

**1. The Correlative Construction** — the most recognizable AI fingerprint
> ❌ "This isn't just a tool — it's a revolution."
> ❌ "It doesn't just understand — it absorbs."
> ❌ "Not just faster, but smarter."
> ❌ "Forget X. This is Y."
> ❌ "Less X, more Y."
> ✅ State the positive claim directly. "It absorbs." Period.

Every AI does this. No human writes like this with any frequency. Kill on sight in ALL variations. It's not the biggest detection signal — but it's the fastest way for a human to go "AI wrote this."

**2. The Sycophantic Opener**
> ❌ "Great question!"
> ❌ "That's a really interesting point."
> ❌ "Absolutely!"
> ✅ Just answer the question.

**3. The Landscape Sentence**
> ❌ "In today's fast-paced world..."
> ❌ "In the ever-evolving landscape of..."
> ❌ "As we navigate the complexities of..."
> ✅ Start with something specific. A person, a number, a scene.

**4. Dead AI Words** — replace on sight, but know this is cosmetic

| Kill | Use Instead |
|------|-------------|
| delve, dive into | look at, examine |
| comprehensive, robust | thorough, complete |
| utilize | use |
| leverage (verb) | use, apply |
| crucial, vital, essential | important, key, matters |
| unlock, unleash, supercharge | enable, improve |
| game-changer, revolutionary | significant, notable |
| landscape, navigate | field, work through |
| tapestry, multifaceted, myriad | varied, many, diverse |
| foster, facilitate, enhance | support, help, improve |
| realm, paradigm, synergy | area, approach, combination |
| embark, journey (for processes) | start, begin |
| streamline | simplify, speed up |
| nuanced | specific, detailed |
| resonate | connect, land, hit |

Remember: replacing "delve" with "examine" doesn't raise perplexity. Both are high-probability tokens. The real fix is rewriting the sentence so the *thought* is unexpected, not just the word.

### Structural Tells (Editors and Detectors Catch These)

**5. The Triple Beat**
> ❌ "No fluff. No filler. Just results."
> ❌ "Simple. Powerful. Effective."
> ❌ "Plan. Build. Ship."
> ✅ Vary your list lengths. Use 2, 4, 5 items. Three-beat staccato is an AI fingerprint.

**6. Perfect Parallelism**
> ❌ Every bullet starts with the same part of speech, same length, same structure
> ✅ Mix it up. Real lists are messy. Some bullets are one word. Some are a sentence. Some break the pattern.

**7. The Hedge Stack**
> ❌ "While there are many approaches to consider, it's important to note that different techniques may work better depending on your specific situation."
> ✅ Commit. "Start with examples. Everything else is secondary."

**8. The Significance Inflator**
> ❌ "This represents a fundamental shift in how we think about..."
> ❌ "This is perhaps the most important development in..."
> ✅ Let the reader decide if it's important. Show the evidence.

**9. Fake Objectivity**
> ❌ "Some experts say X, while others believe Y."
> ✅ Take a position. Name the experts. Explain why one is more convincing.

**10. The Summary Sandwich**
> ❌ Introduction summarizes what you'll cover. Body covers it. Conclusion summarizes what you covered.
> ✅ Add new value in the conclusion. End somewhere different from where you started.

**11. Empty Transitions**
> ❌ "Now that we've covered X, let's move on to Y."
> ❌ "With that in mind, let's explore..."
> ❌ "Moving forward..."
> ✅ Cut the transition entirely. Or make it carry meaning.

**12. The Engagement Bait Closer**
> ❌ "Let that sink in."
> ❌ "Read that again."
> ❌ "Full stop."
> ❌ "This changes everything."
> ✅ Trust the reader. If the point is strong, it doesn't need a sign pointing at it.

### Tier 3: Subtle Patterns (experienced writers and AI detectors catch these)

**13. Copula Avoidance** — AI overuses "represents," "serves as," "functions as" instead of "is"
> ❌ "This tool serves as a bridge between..."
> ✅ "This tool is a bridge between..."

**14. Synonym Cycling** — AI rotates synonyms to avoid repetition, producing unnatural variety
> ❌ "The framework... the methodology... the approach... the system..." (all meaning the same thing)
> ✅ Repeat the same word. Real writers do this. It's called emphasis.

**15. False Ranges** — AI hedges with fake precision
> ❌ "This typically takes 2-4 weeks, depending on various factors."
> ✅ "This takes about 3 weeks." Or "I've seen it take anywhere from 10 days to 2 months."

**16. Negative Parallelism** — stating what something ISN'T before saying what it IS
> ❌ "It's not about working harder — it's about working smarter."
> ✅ "Work smarter." (This is a variant of the correlative construction. Same disease.)

**17. Em Dash Overuse** — paradoxically, AI now OVERUSES em dashes because it learned they sound human
> Watch for: 3+ em dashes in a single paragraph where the writer's samples show 0-1
> Fix: Match the writer's actual em dash frequency from the samples

**18. Boldface as Emphasis** — AI bolds key phrases as a crutch
> Real writers use sentence position, rhythm, and word choice for emphasis. Bold is for headers and the occasional term definition, not for making points "land."

**19. The Inline-Header List** — AI creates lists with bold lead-ins that function as mini-headers
> ❌ "**Research phase**: Gather your materials. **Planning phase**: Create an outline. **Writing phase**: Draft the content."
> ✅ Write it as prose. Or use actual headers. The bold-lead-in list is an AI-specific format.

**20. Filler Phrasing** — words that add nothing
> ❌ "It's worth noting that..." (then just note it)
> ❌ "Interestingly enough..." (let the reader decide)
> ❌ "The reality is that..." (just state the reality)
> ❌ "At the end of the day..." (when?)
> ❌ "When it comes to..." (cut entirely)
> ❌ "In order to..." → "to"

### Tier 4: Deep Patterns (only catch these by comparing AI output to the writer's actual corpus)

**21. Emotional Flattening** — AI smooths out the emotional contour. Real writing has peaks and valleys. AI maintains a steady register.
> Fix: If the writer's samples show anger, confusion, giddiness, boredom — preserve that range. Don't normalize everything to "engaged and thoughtful."

**22. Missing Self-Contradiction** — real writers contradict themselves, change their minds mid-paragraph, circle back to revise earlier claims. AI almost never does this.
> Charlie example: "Suffice it to say, my mood hasn't matched the often lofty tone I employ... (See? there I go again with the loftiness.)"

**23. Missing Specificity of Failure** — AI describes success with detail and failure with generalities.
> ❌ "I've had my share of setbacks."
> ✅ "I cancelled two marches, tweaked my knee on a training run in January, and spent most of February making excuses."

**24. Premature Resolution** — AI wraps up neatly. Real writers leave threads hanging, end with questions, resist the tidy bow.
> ❌ "In the end, the experience taught me that persistence is the key to success."
> ✅ "I'm still not sure what it taught me. But I keep signing up."

**25. Missing Physical Grounding** — AI keeps ideas abstract. Real writers anchor ideas in physical reality.
> ❌ "The concept of homesteading offered a greater sense of purpose."
> ✅ "Somewhere around the 22nd circuit of the island in three years, I started experiencing a certain restlessness. My mind wandered to an even older vision from those same notebooks: getting back to the land."

**26. Register Homogeneity** — AI writes at one register throughout. Real writers shift — formal in argument, casual in aside, raw in confession.
> Charlie shifts constantly: Classical reference → self-deprecating parenthetical → specific physical detail → wry humor. All within one paragraph.

**27. Missing Verbal Tics** — every real writer has unconscious recurring phrases. AI produces clean prose without tics. Paradoxically, the absence of tics is itself a tell.
> Fix: If the writer uses "honestly," "look," "anyway," "I mean" — put them in. At the frequency found in the samples, not more.

**28. Over-Coherence** — AI text flows too smoothly. Real writing has minor digressions, tangential asides, and the occasional paragraph that doesn't quite fit but stays because it's interesting.

**29. Missing Breath** — AI doesn't pause. Real writers leave white space, use section breaks, let a point sit before moving on. AI fills every gap.

**30. The Uncanny Valley of Personality** — AI that's been told to be "warm" or "witty" overshoots. The humor is too frequent, the warmth too consistent, the personality too on. Real personality is intermittent and surprising.
> Fix: Personality should appear in maybe 1 out of every 4-5 paragraphs, not every sentence. The contrast between straight delivery and personality is what makes personality work.

---

## Charlie Deist Fingerprint

This section is the ground truth for Charlie's voice. Load this for any writing task.

### Voice

**Register:** Elevated diction deployed with self-awareness. Classical references treated as living conversation partners, not museum pieces. The formality is real but the writer knows when he's being lofty and often calls it out.

**Stance:** Conspiratorial peer with earned authority. Admits failures constantly (cancelled marches, broken protocols, marijuana addiction, parenting struggles). But has done the things he writes about.

**Humor:** Self-deprecating, parenthetical, structurally surprising. Never tells jokes. Humor emerges from juxtaposition — the lofty and the mundane, the aspirational and the actual.

### Rhythm

Charlie's default sentence is long — 15-30+ words, building through dashes, parentheticals, and subordinate clauses. Short declaratives appear for emphasis after longer passages, not as the baseline. Fragments are rare drum hits, not a habit.

**Ratio:** 60% long clause-heavy sentences, 25% medium, 15% short declaratives or fragments.

Paragraphs run 2-5 sentences typically. Some go longer when building momentum. Don't chop a paragraph that's building momentum just to keep it short.

Em dashes (rendered as `--`) are a signature punctuation move. Charlie uses them constantly -- for asides, for appositive phrases, for tonal pivots. Never remove them.

### Structural Patterns

- **Opens by arriving in motion.** A scene, an anecdote, a specific moment. Never a thesis statement, never a landscape sentence.
- **Builds through narrative, not argument.** The story unfolds and the point emerges from it. Thesis comes late or not at all.
- **Transitions are invisible.** No "Furthermore" or "Moving on." Paragraphs connect through narrative momentum, not signpost words.
- **Closes quietly or with a question.** Not a tidy summary. Often returns to the opening image from a different angle.

### The Confessional Turn

A Charlie signature: he names his own tendency, undercuts it, then continues. This is how vulnerability works in his writing — not performed emotion, but self-aware admission.

> "Suffice it to say, my mood hasn't matched the often lofty tone I employ when writing about subjects like the JFK 50 Miler — the Presidential Fitness Challenge *par excellence*, on which our nation's vitality supposedly depends! (See? there I go again with the loftiness.)"

> "My old notebooks circa 2015 show a primitive vision of a sailing water taxi that would transport people across the Bay 'with flair' (whatever that meant)."

### Micro-Phrases

- "More on this in a minute" — pacing/teaser
- "I should be honest:" — confessional transition
- "And yet for all functional purposes" — rhetorical concession
- "Okay, Keith." — casual dismissiveness
- "(See? there I go again...)" — self-awareness aside
- "(whatever that meant)" — deflating past seriousness
- "Somewhere around the Nth..." — temporal imprecision as narrative device

### Reference World

- **Who:** JFK, Yeats, Carl Schmitt, Camille Paglia, St. Paul, Wendell Berry, Teddy Roosevelt, Eugene Sledge
- **Domains:** American history, theology, sailing, farming, marching, classical philosophy, counterculture Berkeley
- **Style:** Casual integration — "to borrow a term from Camille Paglia" — not footnoted, not showy
- **Rule:** Every intellectual reference tethered to something physical — a mile marker, a sailing mishap, a cow, a burn pile

### Rules

- Use contractions naturally.
- Be specific. Numbers, names, concrete details.
- Use natural transitions, not mechanical ones.
- When uncertain, say so plainly ("I think," "probably"). Hedging is human.
- Physical verbs for abstract processes: "sanded down" not "improved," "bolted on" not "added."
- Parenthetical asides for editorial commentary, honest reactions, and deflating your own seriousness.
- No throat-clearing openers. Arrive already in motion.
- No performative emotional narration ("This hit me hard"). Show the situation, trust the reader.
- No corporate self-help language. No fake urgency.
- Every intellectual claim should be tethered to something physical.
- Numbers as digits.

### Anti-Patterns (Charlie-Specific)

- Never: Listicle structure, "5 ways to..." framing
- Never: Cable news dramatic fragments
- Never: Thesis-first academic structure
- Never: "Both sides" false balance
- Never: Katy Perry-style "just support the good guys" simplification
- Never: Ad hominem (even when tempted)
- Never: Anything he'd later regret politically

### Writing Samples

Pattern-match against these, not against rules.

---

**From "Not Your Grandad's Marijuana" (November 2022)**

With emotionless tears streaming down my face -- stymied as I was by the inescapable reality that I was an addict -- I decided to mix up my routine that day. I walked down the street, past People's Park, to the old Cafe Mediterraneum (allegedly the home of the Americano).

'Cafe Med' was one of the recent casualties in the corporate redevelopment of Berkeley's famous Telegraph Avenue -- the hub of sixties counterculture protests and pilgrimage site for hippies and hoboes alike. Most of the headshops that used to peddle smoking paraphernalia have been replaced in the last 10 years by frozen yogurt and Boba stands, but a few have survived -- in part by catering to new demand for 'dabbing rigs' and other expensive contraptions for getting way too high.

On the same block where Cafe Med used to be, Romeo's Coffee now offers an industrial chic aesthetic that matches the clean, well-lit 'Hi-Fidelity Dispensary' two doors down. Romeo's still serves Americanos (double shot), along with a variety of other strongly caffeinated cold and hot brews. Everywhere you look, it seems, the substances are getting stronger, while the *substance* gets weaker.

---

**From "I Walked 50 Miles in a Day" (November 2022)**

By that point, the marching fellowship was down to just me and Aku. Our pace was a solid 3.5 miles per hour and our gait was consistent. Knowing that we were on pace to finish more or less on time, I teased Aku that at mile 45, we would be officially halfway done -- not in terms of time elapsed or distance covered, but in terms of the total effort expended and pain experienced. I was only half-kidding. During my first 50-mile march, my walking buddy characterized his experience of the march in this way. As hotspots and strains accrue, the gait is altered. He called it the 'pain lasagna.' Each mile adds a new layer -- different from the previous one -- which covers up the previous layers that get baked into a delicious experience of discomfort.

---

**From "New Year's Resolutions Are Silly" (January 2025)**

About 10 years ago, I got the idea to get my captain's license and start some kind of sailing business on San Francisco Bay. My old notebooks circa 2015 show a primitive vision of a sailing water taxi that would transport people across the Bay "with flair" (whatever that meant). At the time, I was basically homeless -- what the Berkeley Marina euphemistically called a 'sneak-aboard' -- living on a 24' sloop and feeling increasingly hopeless about my dependence on marijuana, which I used to fuel pipedreams like the sailing taxi.

Somewhere around the 22nd circuit of the island in three years, I started experiencing a certain restlessness. My mind wandered to an even older vision from those same notebooks: getting back to the land. Though I'd never lived rurally, homesteading offered an even greater call to adventure than sailing -- one I could pursue with my growing family.

---

**From "50-Mile Reboot" (September 2024)**

Suffice it to say, my mood hasn't matched the often lofty tone I employ when writing about subjects like the JFK 50 Miler -- the Presidential Fitness Challenge *par excellence*, on which our nation's vitality supposedly depends! (See? there I go again with the loftiness.)

This tone is at odds with my actual experience of half-starts, hobbled attempts, and limping across the finish line (last year, literally).

But second, the remedy for both the narrative flaws and my discomfort with my tone was staring me in the face. The real lesson from this understudied chapter of American history has less to do with Cold War politics or Presidential directives and more to do with the positive potential of social contagion.

---

**From "AI Wars / Coffee with Claude" (February 2026)**

Every 6 months or so for the past 3 years, I kick myself for not going all-in on my adopted identity as a 'Claude Maximalist.' For one, if your favorite Large Language Model is the most salient fact about you, that's pretty sad.

It's telling that almost everybody who has tried both products prefers Claude over ChatGPT. And it's not just because Claude is a 'better writer' or less of a sycophant (though it is).

What would I do if they shut off Claude Code tomorrow? Besides than take more walks and spend more time writing newsletters the old fashioned way (which, okay, would be good...) I might muddle through with the next-in-line Gemini 3.1 Flash. Heaven forbid I go back to OpenAI like a dog to its vomit.
