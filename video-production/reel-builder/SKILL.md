---
name: reel-builder
description: Build animated reels from AI-generated images using Fal.ai. Multi-scene pipeline — generate style-consistent stills (Kontext Max + flux), animate with Kling start/end frame interpolation for smooth scene-to-scene transitions, assemble with ffmpeg. Use when creating Instagram Reels, TikToks, Shorts, or any multi-shot animated content from scratch.
---

# Reel Builder

Create multi-scene animated reels from AI-generated images. Generates style-consistent stills, animates them with scene-to-scene transitions, and assembles a final video.

## Pipeline

```
Storyboard → Anchor Image → Style-Consistent Scenes → CHECKPOINT
  → Kling Start/End Frame Animation → CHECKPOINT → Assemble Reel → Add Text Overlays
```

## Prerequisites

- `FAL_KEY` set in environment (`~/.zshrc` and `OpenEd Vault/.env`)
- `ffmpeg` installed (`brew install ffmpeg`)
- `pip install requests`

## API Endpoints Used

| Step | Fal.ai Endpoint | Cost | Purpose |
|------|----------------|------|---------|
| Anchor image | `fal-ai/flux/schnell` | ~$0.01 | First scene, establishes style |
| Consistent scenes | `fal-ai/flux-pro/kontext/max` | $0.08/img | Same character in new scenes |
| Fallback (big scene change) | `fal-ai/flux-general` | ~$0.075/MP | Style reference when Kontext times out |
| Animation | `fal-ai/kling-video/v3/pro/image-to-video` | ~$0.56/5s | Start+end frame interpolation |

## Critical Learnings (from March 2026 testing)

### Aspect Ratio
- **DO NOT use `nano-banana-pro`** for custom aspect ratios — it always outputs 1024x1024 square regardless of `image_size` param.
- **USE `flux/schnell`** with explicit pixel dimensions: `"image_size": {"width": 768, "height": 1344}` for 9:16.
- If the input image is square, Kling outputs square video. The input image MUST be the correct aspect ratio.

### Dimension Reference
| Aspect | Width | Height |
|--------|-------|--------|
| 9:16 (Reels) | 768 | 1344 |
| 16:9 (YouTube) | 1344 | 768 |
| 1:1 (Feed) | 1024 | 1024 |

### Style Consistency
- **Kontext Max** (`flux-pro/kontext/max`) is the best tool for character consistency. Give it the anchor image + describe the new scene. It preserves character design, color palette, and art style.
- Kontext may **timeout on scenes very different from the anchor** (e.g., indoor anchor → outdoor meadow). If it returns null, fall back to **flux-general** with `reference_image_url` parameter.
- **flux-general** with `reference_strength: 0.7` is the fallback — style-consistent but slightly less character-locked.

### Scene-to-Scene Animation (the key technique)
- Instead of animating each image independently, use **Kling's start + end frame interpolation**.
- Pass `start_image_url` (Scene N) and `end_image_url` (Scene N+1) with a motion prompt describing the transition.
- This creates smooth morphs between scenes — no hard cuts needed.
- The motion prompt describes what CHANGES between the two frames, not the frames themselves.

### Assembly
- Kling may output slightly different dimensions per clip (e.g., 1088x1904 vs 1116x1852). Always **normalize to 1080x1920** with ffmpeg before concatenation:
  ```bash
  ffmpeg -y -i clip.mp4 -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -pix_fmt yuv420p clip_norm.mp4
  ```

## Workflow (Step by Step)

### Step 1: Storyboard

Define scenes as a table — each needs an image prompt and a transition prompt:

| Scene | Image Prompt | Transition to Next |
|-------|-------------|-------------------|
| 1 | Mama fox sleeping on couch, watercolor... | Kit tiptoes in with a drawing... |
| 2 | Kit showing mama a crayon drawing... | Scene shifts outdoors, kit runs into meadow... |
| 3 | Kit playing in meadow with dandelion... | Camera pushes in to kit's face... |
| 4 | Close-up kit with curious eyes... | Kit turns and runs to mama, they embrace... |
| 5 | Mama and kit in warm embrace... | (end) |

### Step 2: Generate Anchor Image

Use `flux/schnell` with explicit dimensions. The anchor establishes the style bible for all subsequent scenes.

```bash
curl -s -X POST "https://fal.run/fal-ai/flux/schnell" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "...", "image_size": {"width": 768, "height": 1344}}'
```

**Review the anchor carefully** — every subsequent image inherits its style.

### Step 3: Generate Remaining Scenes (Kontext Max)

Feed the anchor image URL to Kontext Max for each scene:

```bash
curl -s -X POST "https://fal.run/fal-ai/flux-pro/kontext/max" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Same fox character and art style. [new scene description]. No text.",
    "image_url": "ANCHOR_URL",
    "image_size": {"width": 768, "height": 1344},
    "output_format": "png"
  }'
```

If Kontext times out (usually for very different compositions), fall back to flux-general:

```bash
curl -s -X POST "https://fal.run/fal-ai/flux-general" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "[scene description]. Same art style...",
    "reference_image_url": "ANCHOR_URL",
    "reference_strength": 0.7,
    "image_size": {"width": 768, "height": 1344}
  }'
```

**CHECKPOINT:** Review all images. Regenerate any that don't match.

### Step 4: Animate with Kling (Start + End Frame)

Submit transition clips to the Kling queue. Each clip morphs from one scene to the next:

```bash
curl -s -X POST "https://queue.fal.run/fal-ai/kling-video/v3/pro/image-to-video" \
  -H "Authorization: Key $FAL_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "TRANSITION DESCRIPTION",
    "start_image_url": "SCENE_N_URL",
    "end_image_url": "SCENE_N+1_URL",
    "duration": "5",
    "aspect_ratio": "9:16",
    "generate_audio": false
  }'
```

Poll status at: `GET https://queue.fal.run/fal-ai/kling-video/requests/{request_id}/status`
(Accept both 200 and 202 status codes while polling.)

Get result at: `GET https://queue.fal.run/fal-ai/kling-video/requests/{request_id}`

**Timing:** ~2-3 minutes per clip. Submit all clips simultaneously to parallelize.

**CHECKPOINT:** Review each clip.

### Step 5: Assemble

Normalize dimensions, concatenate, output final reel:

```bash
# Normalize each clip to 1080x1920
for f in clip*.mp4; do
  ffmpeg -y -i "$f" -vf "scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -pix_fmt yuv420p "${f%.mp4}_norm.mp4"
done

# Concatenate
printf "file '%s'\n" *_norm.mp4 > concat.txt
ffmpeg -y -f concat -safe 0 -i concat.txt -c:v libx264 -pix_fmt yuv420p final_reel.mp4
```

### Step 6: Text Overlays (separate step)

Text is added AFTER animation — never bake text into the images or Kling prompts (it gets distorted). Options:
- **CapCut / InShot** — manual, fastest for one-offs
- **ffmpeg drawtext** — scripted, good for batch
- **Remotion** — programmatic, see `text-on-broll` skill

## Costs

| Reel Type | Images | Clips | Total |
|-----------|--------|-------|-------|
| 3-scene (2 transitions) | ~$0.25 | ~$1.12 | **~$1.40** |
| 5-scene (4 transitions) | ~$0.40 | ~$2.24 | **~$2.65** |
| 8-scene (7 transitions) | ~$0.65 | ~$3.92 | **~$4.60** |

## Prompt Tips

### For image generation
- Describe a single composed frame — think photography, not video
- Be explicit about style: "watercolor and ink," "editorial photography," "nursery print aesthetic"
- Always end with "No text anywhere" — models sometimes add random text
- Include "Vertical composition" for 9:16

### For Kontext (character consistency)
- Start prompts with "Same fox character and art style" (or whatever your subject is)
- Reference specific visual elements: "same watercolor and ink technique, same muted earth tones"
- The more different the new scene is from the anchor, the more likely Kontext times out

### For Kling transitions
- Describe the CHANGE between frames, not the frames themselves
- Keep to 1-2 actions per 5-second clip
- Include ambient motion: "wildflowers sway," "light shifts," "breeze ruffles fur"
- Don't include text descriptions — text in AI video always looks bad

## Related Skills

- **video-generator** — Single-shot video generation (VEO, Sora, Kling). Has the `generate_video.py` script with Kling provider support.
- **nano-banana-image-generator** — Standalone image generation (Gemini). Good for square images only.
- **video-caption-creation** — Add text overlays after assembly
- **text-on-broll** — Remotion-based text overlay on video

## Prompt Engineering Reference

See `video-generator/references/ai-video-prompt-engineering-guide.md` for comprehensive prompting guide (camera language, lighting, motion, audio, 14 sections from 7 sources).
