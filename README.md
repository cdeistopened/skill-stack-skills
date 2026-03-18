# Skill Stack Skills

72 production-ready Claude Code skills organized by category. Each skill is a `SKILL.md` file (with optional `references/` directory) that can be dropped into any `.claude/skills/` folder.

## Categories

### podcast-youtube/ (14 skills)
| Skill | Description |
|-------|-------------|
| podcast-transcript-pipeline | Full production pipeline for raw transcripts to publication-ready text |
| transcript-polisher | Transform raw transcripts into polished documents maintaining authentic voice |
| cold-open-creator | Create 25-50 second cold opens that hook listeners before the episode begins |
| youtube-clip-extractor | Download YouTube videos, analyze transcripts for clip moments, extract with ffmpeg |
| youtube-title-creator | Generate titles and thumbnails achieving 6%+ click-through rates |
| yt-outlier | Identify what's working on YouTube right now for any topic |
| youtube-script-template | Write complete YouTube scripts for 10-12 minute videos |
| video-caption-creation | On-screen text generation — the #1 visual element in short-form video |
| podcast-production | Transform transcripts into editor handoff documents |
| podcast-blog-post-creator | Transform podcast episodes into SEO-optimized blog posts |
| youtube-scriptwriting | Transform ideas into retention-optimized scripts via checkpoint workflow |
| youtube-downloader | Download transcripts and captions from YouTube videos using yt-dlp |
| hook-writer | Generate and refine hooks for any content format |
| descript-api | Programmatic Descript project creation, media import, and Agent Underlord editing |

### writing-voice/ (11 skills)
| Skill | Description |
|-------|-------------|
| clear-writing | Human prose engine — clear writing that doesn't pad or perform |
| ghostwriter | Transform source material into authentic, human-written content |
| voice-dna | Extract a voice from writing samples and write in that voice reliably |
| voice-matching-wizard | Create a voice skill from any writing style's patterns and rhythms |
| anti-ai-writing | Eliminate AI patterns and apply proven writing fundamentals |
| gemini-writer | Leverage Gemini's 1M token context for large writing tasks |
| voice-pirate-wires | Authentic conversational writing for smart, serious-but-not-stuffy audiences |
| voice-analyzer | Transform writing samples into a codified, replicable voice style |
| writing-style | Kill the most common AI tells on sight |
| hook-and-headline-writing | Create hooks and headlines using systematic frameworks |
| narrative-snippets | Turn raw material into structured stories via universal narrative beats |

### video-production/ (7 skills)
| Skill | Description |
|-------|-------------|
| reel-builder | Create multi-scene animated reels from AI-generated images |
| text-on-broll | Composite bold on-screen text over AI-generated b-roll footage |
| remotion-video | Create programmatic videos using Remotion (React components to video) |
| video-generator | Generate videos using Google VEO 3.1 or OpenAI Sora |
| image-prompt-generator | Generate professional images using Gemini API |
| video-script-writer | End-to-end video scriptwriting from concept to camera-ready script |
| nano-banana-image-generator | Generate images using Gemini 3.1 Flash Image or Gemini 3 Pro Image |

### social-media/ (9 skills)
| Skill | Description |
|-------|-------------|
| text-content | Transform source content into platform-optimized social posts via framework fitting |
| instagram-scout | Recurring content intelligence tool turning competitor research into strategy |
| x-research | Agentic research over X/Twitter with iterative refinement |
| social-content-creation | Source material to high-performing social posts using framework fitting |
| content-repurposer | Transform source content into platform-optimized posts |
| dude-with-sign-writer | Bold, conversational one-liners that stop scrolling |
| meta-ads-creative | Research-driven Meta ad creative using the 6 Elements framework |
| voice-trung-phan | Trung Phan voice style (based on 880 tweets analysis) |
| article-titles | Write titles for published articles, deep dives, and blog posts |

### email-newsletter/ (1 skill)
| Skill | Description |
|-------|-------------|
| sales-copy-writer | Sales copy that sounds like the person selling, not a marketer |

### research-scraping/ (6 skills)
| Skill | Description |
|-------|-------------|
| deep-research | Delegate multi-source research to Gemini's Deep Research agent |
| local-markdown-search | Search local markdown collections with BM25, vector search, and LLM re-ranking |
| niche-scout | Evaluate keyword/topic profitability for KDP publishing |
| seomachine | Unified SEO data platform for keyword research and competitor analysis |
| last30days | Research any topic across Reddit, X, and the web — what people actually discuss |
| clifton-sellers-content-prompts | Seven prompts for serious founder-led content |

### publishing-books/ (4 skills)
| Skill | Description |
|-------|-------------|
| book-writer | Multi-phase book manuscript pipeline with orthogonality and voice consistency |
| book-quality-loop | Zero tolerance for AI tells in book writing |
| book-chapter-writer | Write premium book chapters from podcast transcripts using fractal structure |
| amazon-category-research | Find profitable Amazon book categories with low competition |

### business-strategy/ (3 skills)
| Skill | Description |
|-------|-------------|
| company-name-generator | Naming strategy using David Placek's Lexicon Branding methodology |
| brand-identity-wizard | Comprehensive brand identity documents for consistent voice and messaging |
| retardmax | Stop thinking, start doing — simplify ruthlessly |

### wiki-pipeline/ (5 skills)
| Skill | Description |
|-------|-------------|
| wiki-chunk | Split transcripts into semantic topic chunks using Gemini |
| wiki-extract-entities | Extract named entities and build cumulative inventory with mention counts |
| wiki-embed-qdrant | Create vector embeddings and upsert into Qdrant Cloud |
| wiki-index-qmd | Index chunks into QMD hybrid search (BM25 + vector + re-ranking) |
| wiki-write-articles | Generate wiki articles using two-agent research + writing workflow |

### plugin-meta/ (5 skills)
| Skill | Description |
|-------|-------------|
| plugin-builder | Turn a content archive into an installable Claude Code plugin |
| skill-creator | Create new skills and iteratively improve them |
| skill-extractor | Turn raw source material into a list of buildable Claude Code skills |
| archive-decomposer | Break a content archive into component skills and frameworks |
| autoresearch | Fix the 30% failure rate in skills with targeted research |

### infrastructure/ (7 skills)
| Skill | Description |
|-------|-------------|
| claude-setup-guide | Interactive onboarding from "I have Claude" to "Claude in my daily work" |
| obsidian-markdown | Obsidian-specific markdown syntax beyond standard CommonMark |
| obsidian-bases | Create .base files — Obsidian's built-in database views |
| obsidian-canvas | Create .canvas files — Obsidian's visual workspace format |
| notion-export | Convert local markdown files to Notion pages with rich text formatting |
| notion-import | Import Notion workspaces into Obsidian vault |
| markdown-to-gdoc | Create formatted Google Docs from markdown using pandoc and gws CLI |

## Usage

Copy any skill folder into your project's `.claude/skills/` directory. Claude Code will automatically discover and use it.

```bash
# Example: add the voice-dna skill
cp -r writing-voice/voice-dna /path/to/your/project/.claude/skills/
```
