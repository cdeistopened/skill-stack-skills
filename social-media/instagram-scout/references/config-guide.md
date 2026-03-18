# Scout Config Guide

Every project needs a `scout-config.json` in its working directory. This file parameterizes all creator-specific content.

## Full Schema

```json
{
  "project_name": "Dr. Miller - Mind Mastery",

  "creator": {
    "name": "Dr. Richard Louis Miller",
    "handle": "drrichardlouismiller",
    "bio": "85-year-old clinical psychologist with 65+ years of experience. Author, podcast host, creator of The Pause app and book.",
    "followers": "218K"
  },

  "voice": {
    "tone": "Warm, grandfatherly, encouraging",
    "style": "Direct but never preachy. Simple language for profound concepts. Stories from lived experience.",
    "avoid": ["jargon", "condescension", "woo-woo language"]
  },

  "brand": {
    "method": "The P.O.P. Protocol (Pause → Order → Play)",
    "techniques": [
      "Golden Light visualization",
      "Abdominal breathing",
      "Counting exercises",
      "Present-moment awareness"
    ],
    "core_message": "You are the boss of your mind. The mind is not the boss — it's a tool.",
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
      "#breathwork", "#meditation", "#resilience"
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
    "description": "Adults dealing with anxiety, stress, overthinking who want practical, science-backed tools from a warm authority figure"
  },

  "competitors": [
    "drjoedispenza",
    "drmarkwilliamson",
    "drweil",
    "richroll",
    "hubaboreanaz",
    "mel_robbins",
    "theholisticpsychologist",
    "drchatterjee",
    "wimhof_official",
    "sadhguru"
  ],

  "mid_tier_accounts": [
    "the.holistic.psychologist",
    "lisaoliveratherapy",
    "therapy_jeff",
    "dr.juliesmith",
    "silvykhoucasian",
    "nedratawwab",
    "mindfulmft",
    "justinlmft",
    "breathwithmads",
    "breathing.app",
    "calm",
    "headspace",
    "the.breathing.class",
    "drpeterattia",
    "drdavidsinclair",
    "foundmyfitness",
    "dr.gabriellelyon",
    "mark_hyman",
    "drperlmutter",
    "themindsjournal",
    "the.mind.unleashed",
    "mindset_therapy",
    "notesfromyourtherapist",
    "anxietyhealer",
    "risingwoman_",
    "neuroscience_academy",
    "doctormike",
    "drericberg",
    "drjasonfung",
    "anxiety_wellbeing",
    "calmclinicofficial"
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

## Field Descriptions

### `creator`
The person whose content you're creating. Their name, Instagram handle, short bio, and follower count. Used in AI analysis prompts so Gemini understands the adaptation target.

### `voice`
How the creator communicates. `tone` is the overall feel. `style` is specific writing patterns. `avoid` lists things that would feel off-brand. This shapes the creative briefs.

### `brand`
The creator's signature method/framework, specific techniques they teach, their core message, content pillars (the 3-5 topics they own), and standard hashtags. The analysis prompts reference these so briefs adapt trending formats to the creator's actual IP.

### `audience`
Who the content is for. Age range, interests, and a natural-language description. This keeps the AI from generating content that's technically on-topic but wrong for the demographic.

### `competitors`
5-15 Instagram accounts to study directly. These are the "who to copy from" list — established creators in the same niche. Profile scraping (`scrape.ts --profiles`) pulls their recent posts.

### `mid_tier_accounts`
20-40+ accounts in the 10K-500K follower range. These are where viral breakouts happen — they're small enough that a single post can massively outperform their baseline, which signals a trending format or topic. The trend scout's viral ratio engine scrapes all of these.

### `tiktok_keywords`
8-12 search phrases for TikTok trend detection. These should be specific to the niche. TikTok trends lead Instagram by 2-4 weeks, so this is the early warning system.

### `google_trends_terms`
10-20 search terms to monitor in Google Trends (US, 90-day window). When a term's recent interest exceeds its 90-day average by 1.5x+, it's flagged as spiking — ideal timing for content.

## Minimal Config

If you just need the profile scraper (not trend scout), you can use a minimal config:

```json
{
  "project_name": "Quick Scrape",
  "creator": {
    "name": "My Creator",
    "handle": "myhandle",
    "bio": "Brief description",
    "followers": "50K"
  },
  "voice": {
    "tone": "Friendly and authoritative",
    "style": "Clear, practical, no jargon"
  },
  "brand": {
    "pillars": ["Topic 1", "Topic 2", "Topic 3"],
    "hashtags": ["#tag1", "#tag2"]
  },
  "audience": {
    "description": "Adults interested in topic X"
  },
  "competitors": ["account1", "account2", "account3"]
}
```

Fields not in the config will be handled gracefully (empty arrays, generic prompts).
