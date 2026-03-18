---
name: youtube-clip-extractor
description: Extract clips from YouTube videos — download full-resolution video, identify compelling moments from transcripts, cut clips with ffmpeg (lossless, with editorial padding), and generate platform-optimized on-screen text and captions. Use when the user says "cut clips", "extract clips", "pull clips from this video", "find the best moments", "clip this interview", or has a YouTube URL they want to turn into short-form content. Also use when re-cutting or adding clips to an existing set, or when someone has a transcript and wants to identify clip-worthy moments even without a video yet.
---

# YouTube Clip Extractor

## Overview

Download YouTube videos at full resolution, analyze transcripts for compelling clip moments, extract clips using ffmpeg (lossless by default, with padding for editorial trimming), and generate platform-ready on-screen text and captions.

## When to Use This Skill

- You have a YouTube URL and want to extract the best clips
- You want automated clip identification based on hook/coda criteria
- You need clips cut and ready for Descript or other editors
- You want on-screen text hooks and platform-specific captions for each clip
- You have a transcript (from any source) and want to identify clip-worthy moments
- You need to add more clips to an existing set from a previous session

**Do NOT use for:**
- Full podcast production workflow (use `podcast-production` skill instead)
- Text-only social posts (use `social-content-creation` skill)

---

## Prerequisites

### Required Tools (install via Homebrew)

```bash
brew install yt-dlp ffmpeg
```

### File Location

Output directory is **project-relative**. Ask the user where clips should go, or use this default structure within the relevant project:

```
{project}/studio/clips/{video_id}/
├── full_video.mp4              # Full video (full resolution, H.264)
├── clip_01_{name}.mp4          # Individual clips (lossless cuts)
├── clip_02_{name}.mp4
└── clip-captions-and-hooks.md  # Captions & hooks for all clips
```

If no project context exists, fall back to `Content/YouTube Transcripts/clips/{video_id}/`.

---

## The 4-Phase Workflow

### Phase 1: Download Video & Transcript

**Goal:** Get full-resolution video and subtitles from YouTube URL

#### Step 1: Download at Full Resolution (H.264)

Always download the highest quality H.264 stream for Descript compatibility:

```bash
# Full resolution H.264 (default — always use this)
yt-dlp -f "bestvideo[vcodec^=avc]+bestaudio[ext=m4a]/best[vcodec^=avc]" \
  --merge-output-format mp4 \
  -o "{output_dir}/full_video.mp4" \
  "YOUTUBE_URL"
```

Verify resolution after download:
```bash
ffprobe -v quiet -print_format json -show_streams full_video.mp4 2>&1 | \
  python3 -c "import sys,json; d=json.load(sys.stdin); v=[s for s in d['streams'] if s['codec_type']=='video'][0]; print(f\"{v['width']}x{v['height']} {v['codec_name']}\")"
```

If H.264 is unavailable at the desired resolution, download best available then re-encode:
```bash
yt-dlp -f "bestvideo+bestaudio" --merge-output-format mp4 \
  -o "{output_dir}/full_video_temp.mp4" "YOUTUBE_URL"

ffmpeg -i "full_video_temp.mp4" -c:v libx264 -preset fast -crf 18 \
  -c:a aac -b:a 128k "full_video.mp4"
```

#### Step 2: Download Subtitles (if available)

```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download \
  -o "{output_dir}/full_video.%(ext)s" \
  "YOUTUBE_URL"
```

**Important:** Many YouTube videos have NO auto-generated or manual captions. If this fails, check with `--list-subs`. When no captions exist, use the **"Bring Your Own Transcript"** path — any existing transcript (polished, raw, or from another transcription tool) can be used for Phase 2 clip identification. You do NOT need a VTT file to identify clips.

#### Phase 1 Output:
- `full_video.mp4` — Full video at highest available H.264 resolution
- `full_video.en.vtt` — Timestamped subtitles (if available)
- OR: user-provided transcript from any source

---

### Phase 2: Analyze Transcript for Clips

**Goal:** Identify 5-8 compelling clip moments with strong hooks and codas

#### Clip Selection Criteria

**A good clip has:**

1. **Strong Hook (First 3 Seconds)**
   - Polarizing statement ("Your kid's addiction is actually genius")
   - Counter-intuitive reveal ("My son's first job sucked. Perfect.")
   - Direct challenge ("Never give up on the weird kid")
   - Curiosity gap ("Then everything changed...")

2. **Complete Arc (30-90 seconds)**
   - Clear beginning, middle, end
   - Not just a "good quote" — a complete thought
   - Setup → Tension → Resolution OR Setup → Tension → Cliffhanger

3. **Stakes**
   - Why does this matter?
   - Who cares?
   - What's at risk?

4. **Strong Coda/Ending**
   - Insight or surprising conclusion
   - Cuts right before the answer (cliffhanger)
   - Quotable final line

#### Scan Transcript For:

**Inflection Points:**
- "Then everything changed..."
- "I realized..."
- "That's when I knew..."
- "The moment I..."

**Vulnerability Moments:**
- Personal stakes, failures, struggles
- "I was terrified..."
- "I almost gave up..."
- "Nobody believed..."

**Contradiction Moments:**
- "We thought X but actually..."
- "Everyone says... but the truth is..."
- "The opposite happened..."

**Surprising Insights:**
- Research, data, unexpected findings
- Counter-intuitive conclusions
- "What we found was..."

**Character in Action:**
- Showing, not telling
- Doing, not describing
- Specific moments, not abstractions

#### Quality Tests (Pass 4/5):

- [ ] **Stranger Test:** Would someone with zero context care?
- [ ] **Itch Test:** Creates need to know more?
- [ ] **Stakes Test:** Clear why it matters?
- [ ] **Tease Test:** Hints without giving away?
- [ ] **Emotion Test:** Feel something in first 5 seconds?

#### Phase 2 Output Format:

Create analysis document with clip recommendations:

```markdown
# {Video Title} - Clip Analysis

## Video Details
- **URL:** [YouTube URL]
- **Duration:** [Total length]
- **Speaker(s):** [Names]
- **Topic:** [Primary subject]

---

## Recommended Clips

### CLIP 1: "{Descriptive Name}"
**Timestamp:** `MM:SS - MM:SS` (XX seconds)
**Hook:** [First line or opening moment]
**Arc:** [Setup → Middle → Ending summary]
**Coda:** [How it ends / final line]

**Key Quotes:**
- "[Verbatim quote 1]"
- "[Verbatim quote 2]"
- "[Verbatim quote 3]"

**Quality Tests:** Stranger ✅ | Itch ✅ | Stakes ✅ | Tease ✅ | Emotion ✅
**Why It Works:** [1-2 sentence rationale]
**Priority:** HIGH / MEDIUM / LOW

---

### CLIP 2: "{Descriptive Name}"
[Repeat structure...]

---

## Summary Table

| # | Clip Name | Timestamp | Length | Hook | Coda | Priority |
|---|-----------|-----------|--------|------|------|----------|
| 1 | [Name] | MM:SS-MM:SS | XXs | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | HIGH |
| 2 | [Name] | MM:SS-MM:SS | XXs | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | HIGH |
| 3 | [Name] | MM:SS-MM:SS | XXs | ⭐⭐⭐ | ⭐⭐⭐⭐ | MEDIUM |
```

---

### Phase 3: Cut Clips with FFmpeg

**Goal:** Extract approved clips as separate video files with editorial padding

#### Default: Lossless Cutting with Padding

Always add ~10 seconds of padding on each side of the target timestamp. This gives editorial room to find the perfect in/out points in Descript or any editor. The padding is cheap (a few extra MB) and prevents the need to re-download and re-cut.

**Lossless stream copy (DEFAULT — always use this):**
```bash
ffmpeg -y -ss START_WITH_PADDING -i "full_video.mp4" \
  -t DURATION_WITH_PADDING -c copy \
  "clip_01_{name}.mp4"
```

This is instant (no re-encoding), preserves full source quality, and produces Descript-compatible H.264 output. The only tradeoff is that the actual start frame may snap to the nearest keyframe — but with 10s of padding, this is irrelevant since you're trimming in the editor anyway.

**Example with padding calculation:**
```
Target clip: 41:37 – 44:00 (2:23)
With padding: 41:27 – 44:10 (2:43)
→ -ss 41:27 -t 163
```

**Only re-encode if** you need frame-precise cuts with no padding (rare):
```bash
ffmpeg -y -ss MM:SS -i "full_video.mp4" -t DURATION \
  -c:v libx264 -preset fast -crf 18 -c:a aac -b:a 128k \
  "clip_01_{name}.mp4"
```

#### Batch Cutting Example

```bash
# All clips from one interview, lossless with ~10s padding each side
ffmpeg -y -ss 07:08 -i "full_video.mp4" -t 152 -c copy "clip_01_tiny_increments.mp4"
ffmpeg -y -ss 19:37 -i "full_video.mp4" -t 153 -c copy "clip_02_origin_story.mp4"
ffmpeg -y -ss 41:27 -i "full_video.mp4" -t 163 -c copy "clip_03_winnebago.mp4"
ffmpeg -y -ss 57:36 -i "full_video.mp4" -t 124 -c copy "clip_04_theyre_scared.mp4"
```

#### Phase 3 Output:
- Individual MP4 files for each clip (full resolution, lossless)
- Each clip has ~10s padding on both sides for editorial trimming
- All files in project clips directory

---

### Phase 4: Generate On-Screen Text & Captions

**Goal:** Create platform-optimized hooks and captions for each clip

**This phase uses the `video-caption-creation` skill methodology.**

#### For Each Clip, Generate:

**1. On-Screen Text Hook (3-5 options)**

The text that appears in the first 3 seconds of the video. Must be:
- 2-4 words maximum (mobile readable)
- Stops the scroll
- Passes McDonald's Test (accessible language)
- Complements (not duplicates) audio

**Hook Categories:**
- **Polarizing:** "Your kid's [negative] is actually genius"
- **Counter-Intuitive:** "My son's first job sucked. Perfect."
- **Direct Challenge:** "Never give up on the weird kid"
- **Curiosity Gap:** "Then everything changed..."

**2. Platform-Specific Captions**

| Platform | On-Screen Text | Caption Style | Hashtags |
|----------|---------------|---------------|----------|
| Instagram | Same | Short, emoji OK, accessible | 5-10 |
| TikTok | Same | Short, emoji OK, accessible | 3-5 |
| YouTube Shorts | Same | Short, minimal emoji | 3-5 + #Shorts |
| Facebook | Same | Slightly longer, conversational, NO external links | 0-2 |

**Facebook Difference:** Caption can be longer and more conversational. NO hashtags or external links (kills reach).

**3. Algorithm Optimization**

Per the Triple Word Score system:
- **Audio:** Topic words spoken in first 10 seconds
- **On-Screen Text:** Reinforces (not competes with) audio
- **Caption:** Topic-relevant keywords in first sentence
- **Hashtags:** Broad → Mid → Specific → Niche (10-12 total)

#### Phase 4 Output Format:

Create file: `clips/{video_id}/{video_id}_CLIP_PACKAGE.md`

```markdown
# {Video Title} - Clip Package

## Source Video
- **URL:** [YouTube URL]
- **Title:** [Video title]
- **Duration:** [Total length]
- **Downloaded File:** `{video_id}.mp4`

---

## Context

[2-3 sentences explaining the backstory needed to understand the clip. Who is the speaker? What's their situation? What happened before/after the moments in the clip? This context ensures on-screen text and captions are coherent with the actual story.]

---

## Editing Instructions

**SEQUENCE (Rearranged from original - NOT linear):**

| Order | Timestamp | Speaker | Line |
|-------|-----------|---------|------|
| 1 | MM:SS-MM:SS | [Name] | "[Verbatim quote]" |
| 2 | MM:SS-MM:SS | [Name] | "[Verbatim quote]" |
| 3 | MM:SS-MM:SS | [Name] | "[Verbatim quote]" |

**OPTIONAL EXTENSION:**

| Order | Timestamp | Speaker | Line |
|-------|-----------|---------|------|
| 4 | MM:SS-MM:SS | [Name] | "[Verbatim quote]" |

---

## On-Screen Text Hook Options

1. **[Hook text]** - [Category]
2. **[Hook text]** - [Category]
3. **[Hook text]** - [Category]
4. **[Hook text]** - [Category]
5. **[Hook text]** - [Category]
6. **[Hook text]** - [Category]
7. **[Hook text]** - [Category]
8. **[Hook text]** - [Category]
9. **[Hook text]** - [Category]
10. **[Hook text]** - [Category]

---

## Platform Captions

### TikTok / Instagram Reels / YouTube Shorts
[Caption text]

[Hashtags: 3-5]

---

### Facebook
[Longer caption, conversational, NO hashtags]

---

### LinkedIn
[Professional tone caption]

[Hashtags: 3-5]
```

#### On-Screen Text Hook Categories

- **Story Setup** - Provides context that makes the clip make sense (e.g., "Homeschooler tries public school")
- **Polarizing** - Bold statement that divides opinion (e.g., "Most schools are awful")
- **Contrast** - Juxtaposition that creates tension (e.g., "First in class. Zero joy.")
- **Curiosity Gap** - Teases without revealing (e.g., "#1 out of 1,200 students")
- **Story Tease** - Hints at narrative arc (e.g., "She went back to homeschool after this")
- **Pattern Interrupt** - Subverts expectations (e.g., "This isn't anti-public school")

#### Context-Caption Coherence

**Critical:** On-screen text and captions must be coherent with the actual story in the transcript. Before writing hooks:

1. Understand the full context (who, what, when, why)
2. Identify what viewers need to know for the clip to make sense
3. Choose hooks that accurately represent the story
4. Avoid hooks that would confuse viewers when they hear the audio

**Example:** If the clip shows someone criticizing public school, but they were actually a homeschooler who tried public school once, hooks like "Homeschooler tries public school" or "She tried public school for one year" provide necessary context that makes the story coherent.

---

## Complete Workflow Example

```bash
# PHASE 1: Download full resolution video + attempt captions
OUTDIR="Creative Intelligence Agency/RLM/studio/clips/YnQbloQgZEY"
mkdir -p "$OUTDIR"

yt-dlp -f "bestvideo[vcodec^=avc]+bestaudio[ext=m4a]/best[vcodec^=avc]" \
  --merge-output-format mp4 \
  -o "$OUTDIR/full_video.mp4" \
  "https://www.youtube.com/watch?v=YnQbloQgZEY"

# Try captions (may not exist — that's OK)
yt-dlp --write-auto-sub --sub-lang en --skip-download \
  -o "$OUTDIR/full_video.%(ext)s" \
  "https://www.youtube.com/watch?v=YnQbloQgZEY"

# PHASE 2: Analyze transcript for clips
# Use VTT if available, OR any existing transcript (polished, raw, etc.)
# Output: clip analysis doc with timestamps, hooks, codas, quality tests

# PHASE 3: Cut clips (lossless, with ~10s padding)
ffmpeg -y -ss 07:08 -i "$OUTDIR/full_video.mp4" -t 152 -c copy "$OUTDIR/clip_01_tiny_increments.mp4"
ffmpeg -y -ss 41:27 -i "$OUTDIR/full_video.mp4" -t 163 -c copy "$OUTDIR/clip_02_winnebago.mp4"
ffmpeg -y -ss 57:36 -i "$OUTDIR/full_video.mp4" -t 124 -c copy "$OUTDIR/clip_03_theyre_scared.mp4"

# PHASE 4: Generate clip-captions-and-hooks.md with on-screen text + platform captions
```

---

## Related Skills

This skill integrates with:

| Skill | When to Use | What It Provides |
|-------|-------------|------------------|
| **video-caption-creation** | Phase 4 | On-screen text hook categories, Triple Word Score system, platform caption guidelines |
| **youtube-downloader** | Phase 1 (alternative) | Detailed yt-dlp installation checks, error handling, transcript-only workflow |
| **text-content** | After clips ready | Framework fitting for text posts about clips |
| **podcast-production** | Full episode workflow | Complete 4-checkpoint production system |

### Skill Cross-References

**From video-caption-creation:**
- Hook categories (Polarizing, Counter-Intuitive, Direct Challenge, Curiosity Gap)
- Triple Word Score system (Audio + On-Screen + Caption + Hashtags)
- Platform-specific hashtag counts
- McDonald's Test for accessibility

**From text-content:**
- Platform voice guidelines (LinkedIn vs Facebook vs Instagram)
- Framework fitting method
- 360+ templates in references/

---

## Common Mistakes to Avoid

### Download Issues
- ❌ Downloading AV1 codec (Descript can't import)
- ❌ Not re-encoding to H.264 when needed
- ❌ Assuming captions exist — many videos have NO auto-generated or manual captions. Always have a fallback (existing transcript, Whisper, manual transcription)
- ❌ Downloading at lower resolution when full resolution is available

### Clip Selection Issues
- ❌ Choosing "good quotes" instead of complete arcs
- ❌ Clips too long (>90 seconds) or too short (<30 seconds)
- ❌ No clear hook in first 3 seconds
- ❌ Giving away the punchline in the hook

### Cutting Issues
- ❌ Cutting without padding — always add ~10s each side for editorial trimming
- ❌ Re-encoding when `-c copy` (lossless) would work — only re-encode for frame-precise cuts without padding
- ❌ Starting mid-sentence
- ❌ Ending before natural conclusion

### Caption Issues
- ❌ On-screen text too long (>4 words)
- ❌ Same caption for Facebook as other platforms
- ❌ External links in Facebook caption
- ❌ Hashtags in Facebook caption

---

## Quality Checklist

Before delivering clips:

**Video Files:**
- [ ] All clips are H.264 encoded
- [ ] Each clip is 30-90 seconds
- [ ] Audio and video are synced
- [ ] Clean start/end points (no mid-word cuts)

**Clip Selection:**
- [ ] Each clip passes 4/5 quality tests
- [ ] Strong hook in first 3 seconds
- [ ] Complete arc (not just a quote)
- [ ] Clear stakes (why it matters)

**Captions & Hooks:**
- [ ] 3-5 on-screen text options per clip
- [ ] On-screen text is 2-4 words max
- [ ] Platform-specific captions created
- [ ] Facebook caption is different (longer, no hashtags)
- [ ] Hashtag strategy spans broad to niche

---

## Version History

- **v2.0** (2026-03-13): Major update from RLM/Jock Putney clip session
  - Default to full-resolution download (highest H.264 available)
  - Default to lossless cutting (`-c copy`) instead of re-encoding
  - Built-in ~10s editorial padding on all clips
  - "Bring Your Own Transcript" path when YouTube has no captions
  - Project-relative output directories instead of hardcoded path
  - Expanded description for better skill triggering
  - Support for non-linear workflow (analysis and cutting across sessions)

- **v1.1** (2025-12-20): Streamlined output format
  - Removed "Target Length" and "Concept" sections from output
  - Removed "Why This Edit Works" section
  - Added "Context" section for backstory coherence
  - Simplified on-screen text hooks to numbered list with categories only
  - Added "Story Setup" hook category for context-providing hooks
  - Added "Context-Caption Coherence" guidance
  - Updated output template to match streamlined format

- **v1.0** (2025-12-02): Initial skill creation
  - 4-phase workflow: Download → Analyze → Cut → Caption
  - Integration with video-caption-creation skill
  - H.264 encoding for Descript compatibility
  - Platform-specific caption guidelines
  - Quality tests from podcast-production skill
