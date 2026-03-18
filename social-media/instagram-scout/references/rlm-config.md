# RLM Scout Config — Dr. Richard Louis Miller

Reference for configuring instagram-scout for Dr. Miller's niche. Copy the JSON at the bottom to `RLM/scout-config.json`.

## Niche Definition

Dr. Miller sits at the intersection of **clinical psychology + aging well + mind mastery**. He's 87, has 65+ years of practice, and his core message is "you are the boss of your mind." His audience is mostly women 35-65 who found him on Instagram and want practical, warm, non-woo advice for anxiety, overthinking, and aging gracefully.

The competitive landscape has three layers:

### Tier 1: Direct Competitors (5-10 accounts)
These creators are in the same niche, target similar audiences, and post similar content formats. Study these closely — their top posts are the most directly adaptable.

**Why these accounts:**
- `drjoedispenza` — Meditation + neuroscience + mindset. Massive engagement, similar "mind over matter" philosophy. His viral Reels show what hooks work for the meditation/mindset crowd.
- `theholisticpsychologist` — Psychology self-healing. She proved the "therapist on Instagram" format at scale. Her talking-head + text overlay style is the template.
- `drchatterjee` — Holistic health, longevity. UK-based doctor with a warm, accessible voice. His carousel + Reel mix is what we're targeting.
- `mel_robbins` — Mindset, habits, motivation. Not a psychologist but dominates the "practical mental tools" space. Her hook writing is best-in-class.
- `drweil` — Integrative medicine, breathing. Elder statesman of holistic health. His audience overlaps heavily with Richard's.
- `richroll` — Aging, wellness, mindset. Podcast-first creator who turned Instagram into a growth engine. His audience is the male side of Richard's demo.
- `wimhof_official` — Breathwork, cold exposure. Different method but same "master your physiology" message. His Reels format translates well.
- `sadhguru` — Meditation, inner engineering. Massive but useful for studying what spiritual/mindfulness hooks resonate at scale.

### Tier 2: Mid-Tier Niche Accounts (30-40 accounts)
These are the 10K-500K range accounts where viral breakouts are detectable. When a mid-tier therapist's post gets 10x their usual engagement, the format or topic is resonating beyond their core audience — that's an early signal.

**Categories to cover:**
- **Therapists / Psychologists** (talking head, text overlay, "therapist tip" format)
- **Breathwork / Meditation** (technique demos, guided exercises)
- **Aging Well / Longevity** (health tips, mindset for older adults)
- **Mindset / Motivation** (quote cards, motivational Reels)
- **Anxiety / Stress** (coping tools, relatable content)

### Tier 3: TikTok Keywords
TikTok trends lead Instagram by 2-4 weeks. These keywords catch what's about to blow up:

- `anxiety tips psychologist` — Richard's bread and butter
- `breathing exercises calm` — Core technique
- `mindset over 50` / `aging well tips` / `mental health older adults` — His demographic
- `meditation for beginners` — Entry point content
- `psychology life hack` / `stress relief technique` — Snackable tools format
- `positive psychology` / `mind control technique` — His philosophical positioning

### Tier 4: Google Trends Terms
Monitor search interest for Richard's core topics. When a term spikes, it's time to post about it:

- Breathwork, meditation, anxiety, visualization — Core methods
- Longevity, aging well, mind body connection — His pillars
- Vagus nerve, somatic therapy, grounding techniques — Adjacent trending topics that Richard can speak to
- Box breathing, mood control — Specific techniques he teaches

## Account Selection Criteria

When updating the competitor/mid-tier lists, look for accounts that are:

1. **Talking head format** — Richard's content is him speaking to camera. Prioritize accounts that also do talking head, not graphic design or lifestyle photography.
2. **Psychology / wellness / aging niche** — Not fitness influencers, not life coaches with no credentials, not pure meditation apps.
3. **Engaged audience, not just followers** — A 50K account with 5% engagement rate is more useful than a 2M account with 0.1%.
4. **Text overlay on thumbnails** — This is the dominant format in the niche. The thumbnail text IS the hook.
5. **Regular posting cadence** — Accounts that post 3-7x/week have enough data to compute meaningful baselines.

## Config JSON

```json
{
  "project_name": "Dr. Miller - Mind Mastery",

  "creator": {
    "name": "Dr. Richard Louis Miller",
    "handle": "drrichardlouismiller",
    "bio": "87-year-old clinical psychologist with 65+ years of experience. Author, podcast host (Mind Body Health & Politics), creator of The Pause app and book.",
    "followers": "218K"
  },

  "voice": {
    "tone": "Warm, grandfatherly, encouraging",
    "style": "Direct but never preachy. Simple language for profound concepts. Stories from lived experience (Winnebago crash, grief, recovery). Optimistic without being naive.",
    "avoid": ["jargon", "condescension", "woo-woo language", "clinical detachment"]
  },

  "brand": {
    "method": "The P.O.P. Protocol (Pause \u2192 Order \u2192 Play)",
    "techniques": [
      "Golden Light visualization (core meditation/mood-setting)",
      "Abdominal breathing for calm",
      "Counting exercises for mental discipline",
      "Present-moment awareness",
      "Self-talk and positive affirmations"
    ],
    "core_message": "You are the boss of your mind. The mind is not the boss \u2014 it's a tool.",
    "pillars": [
      "Mind mastery & mood control",
      "Aging well & vitality",
      "Resilience stories",
      "Daily habits & routines",
      "Breathing & meditation"
    ],
    "hashtags": [
      "#mindmastery", "#thepause", "#moodcontrol",
      "#positivepsychology", "#agingwell", "#mentalhealth",
      "#breathwork", "#meditation", "#resilience",
      "#drrichardlouismiller"
    ]
  },

  "audience": {
    "age_range": "35-65",
    "interests": [
      "Anxiety and stress management",
      "Practical psychology (not woo-woo)",
      "Aging-well community",
      "Podcast listeners wanting actionable mental health tools"
    ],
    "description": "Mostly women 35-65 who found Richard on Instagram. Dealing with anxiety, stress, overthinking. Want practical, warm, credentialed advice from someone who's lived it."
  },

  "competitors": [
    "drjoedispenza",
    "theholisticpsychologist",
    "drchatterjee",
    "mel_robbins",
    "drweil",
    "richroll",
    "wimhof_official",
    "sadhguru",
    "drmarkwilliamson",
    "hubaboreanaz"
  ],

  "mid_tier_accounts": [
    "lisaoliveratherapy",
    "therapy_jeff",
    "dr.juliesmith",
    "silvykhoucasian",
    "nedratawwab",
    "mindfulmft",
    "justinlmft",
    "psychlogywithdrhillary",
    "breathwithmads",
    "breathing.app",
    "calm",
    "headspace",
    "the.breathing.class",
    "breathwork_daily",
    "itsmepranabreath",
    "drpeterattia",
    "drdavidsinclair",
    "foundmyfitness",
    "dr.gabriellelyon",
    "mark_hyman",
    "drperlmutter",
    "longevity.md",
    "themindsjournal",
    "the.mind.unleashed",
    "mindset_therapy",
    "notesfromyourtherapist",
    "anxietyhealer",
    "risingwoman_",
    "neuroscience_academy",
    "brainfacts_org",
    "doctormike",
    "drericberg",
    "drjasonfung",
    "anxiety_wellbeing",
    "calmclinicofficial",
    "anxietycoachesassociation"
  ],

  "tiktok_keywords": [
    "anxiety tips psychologist",
    "breathing exercises calm",
    "mindset over 50",
    "aging well tips",
    "mental health older adults",
    "meditation for beginners",
    "psychology life hack",
    "stress relief technique",
    "positive psychology",
    "mind control technique"
  ],

  "google_trends_terms": [
    "breathwork",
    "meditation for anxiety",
    "how to calm anxiety",
    "positive psychology",
    "aging well",
    "longevity tips",
    "mind body connection",
    "mental health over 50",
    "visualization meditation",
    "stress relief exercises",
    "mood control",
    "grounding techniques",
    "vagus nerve exercises",
    "box breathing",
    "somatic therapy"
  ]
}
```
