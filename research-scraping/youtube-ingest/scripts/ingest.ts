#!/usr/bin/env bun
/**
 * YouTube Ingest — video/playlist/channel → Gemini transcription → markdown
 *
 * Usage:
 *   bun run youtube-ingest/scripts/ingest.ts --url <youtube-url> [--output dir]
 *   bun run youtube-ingest/scripts/ingest.ts --playlist <playlist-url> [--limit N]
 */

import { parseArgs } from "util";
import { writeFileSync } from "fs";
import { join } from "path";
import { generate, uploadFile, deleteFile, cleanOutput } from "../../shared/ai";
import { ensureOutputDir, slugify, frontmatter, fmtDate } from "../../shared/config";

// --- YouTube URL parsing ---

function extractVideoId(url: string): string | null {
  const patterns = [
    /(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})/,
    /youtube\.com\/v\/([a-zA-Z0-9_-]{11})/,
    /youtube\.com\/.*[?&]v=([a-zA-Z0-9_-]{11})/,
    /youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})/,
  ];
  for (const p of patterns) {
    const m = url.match(p);
    if (m?.[1]) return m[1];
  }
  return null;
}

function extractPlaylistId(url: string): string | null {
  const m = url.match(/[?&]list=([a-zA-Z0-9_-]+)/);
  return m?.[1] || null;
}

// --- Metadata ---

interface VideoMeta {
  title: string;
  author: string;
  authorUrl: string;
  thumbnail: string;
}

async function getVideoMeta(videoId: string): Promise<VideoMeta> {
  try {
    const oembedUrl = `https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v=${videoId}&format=json`;
    const res = await fetch(oembedUrl);
    if (!res.ok) return { title: "Unknown", author: "Unknown", authorUrl: "", thumbnail: "" };
    const data = (await res.json()) as any;
    return {
      title: data.title || "Unknown",
      author: data.author_name || "Unknown",
      authorUrl: data.author_url || "",
      thumbnail: data.thumbnail_url || "",
    };
  } catch {
    return { title: "Unknown", author: "Unknown", authorUrl: "", thumbnail: "" };
  }
}

// --- Playlist fetching (scrape approach) ---

async function getPlaylistVideoIds(playlistId: string): Promise<string[]> {
  // Use YouTube's playlist page and extract video IDs from the HTML
  const url = `https://www.youtube.com/playlist?list=${playlistId}`;
  const res = await fetch(url, {
    headers: { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)" },
  });
  if (!res.ok) throw new Error(`Playlist fetch failed: ${res.status}`);
  const html = await res.text();

  // Extract video IDs from ytInitialData
  const videoIds: string[] = [];
  const regex = /"videoId":"([a-zA-Z0-9_-]{11})"/g;
  let match;
  const seen = new Set<string>();
  while ((match = regex.exec(html)) !== null) {
    if (!seen.has(match[1])) {
      seen.add(match[1]);
      videoIds.push(match[1]);
    }
  }
  return videoIds;
}

// --- Transcription via Gemini ---

const TRANSCRIBE_PROMPT = (meta: VideoMeta) =>
  `You are a professional transcriptionist. Transcribe this audio completely and accurately.

Video: "${meta.title}"
Channel: ${meta.author}

## Output Format
1. **Summary:** 2-3 sentence summary
2. **Topics:** 3-5 topic tags, comma-separated
3. **Speakers:** List distinct speakers
4. Full transcript with ## section headers

## Rules
- Transcribe EVERYTHING verbatim
- Clean up filler words but preserve voice
- Use **Name:** labels when identifiable
- Mark ads/sponsors with [AD]
- Preserve technical terms exactly`;

async function transcribeVideo(videoId: string): Promise<{ transcript: string; meta: VideoMeta }> {
  const meta = await getVideoMeta(videoId);
  console.log(`  Title: ${meta.title}`);
  console.log(`  Channel: ${meta.author}`);

  // Download audio via yt-dlp (must be installed)
  console.log(`  Downloading audio via yt-dlp...`);
  const tmpFile = `/tmp/doodle-yt-${videoId}.m4a`;

  const proc = Bun.spawn(
    ["yt-dlp", "-f", "bestaudio[ext=m4a]/bestaudio", "-o", tmpFile, "--no-playlist", `https://www.youtube.com/watch?v=${videoId}`],
    { stdout: "pipe", stderr: "pipe" }
  );
  const exitCode = await proc.exited;
  if (exitCode !== 0) {
    const stderr = await new Response(proc.stderr).text();
    throw new Error(`yt-dlp failed (${exitCode}): ${stderr.substring(0, 200)}`);
  }

  const audioFile = Bun.file(tmpFile);
  const audioBytes = new Uint8Array(await audioFile.arrayBuffer());
  const sizeMB = (audioBytes.length / (1024 * 1024)).toFixed(1);
  console.log(`  Audio: ${sizeMB} MB`);

  const prompt = TRANSCRIBE_PROMPT(meta);
  const INLINE_LIMIT = 20 * 1024 * 1024;
  let transcript: string;

  if (audioBytes.length <= INLINE_LIMIT) {
    console.log(`  Transcribing (inline)...`);
    const base64 = Buffer.from(audioBytes).toString("base64");
    transcript = cleanOutput(
      await generate({
        parts: [
          { inlineData: { mimeType: "audio/mp4", data: base64 } },
          { text: prompt },
        ],
      })
    );
  } else {
    console.log(`  Uploading to Gemini...`);
    const uploaded = await uploadFile(audioBytes, "audio/mp4", meta.title);
    console.log(`  Transcribing (uploaded)...`);
    try {
      transcript = cleanOutput(
        await generate({
          parts: [
            { fileData: { mimeType: "audio/mp4", fileUri: uploaded.uri } },
            { text: prompt },
          ],
        })
      );
    } finally {
      await deleteFile(uploaded.name);
    }
  }

  // Clean up temp file
  try { await Bun.spawn(["rm", tmpFile]).exited; } catch {}

  return { transcript, meta };
}

// --- Main ---

async function main() {
  const { values } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      url: { type: "string" },
      playlist: { type: "string" },
      limit: { type: "string", default: "5" },
      output: { type: "string" },
      list: { type: "boolean", default: false },
    },
    strict: true,
  });

  if (!values.url && !values.playlist) {
    console.log(`Usage:
  bun run youtube-ingest/scripts/ingest.ts --url <youtube-url>
  bun run youtube-ingest/scripts/ingest.ts --playlist <playlist-url> [--limit N] [--list]

Requires yt-dlp installed: brew install yt-dlp`);
    process.exit(1);
  }

  // Single video mode
  if (values.url) {
    const videoId = extractVideoId(values.url);
    if (!videoId) {
      console.error("Could not extract video ID from URL");
      process.exit(1);
    }

    console.log(`\nProcessing video: ${videoId}`);
    const { transcript, meta } = await transcribeVideo(videoId);

    const outDir = ensureOutputDir(values.output || "youtube");
    const filename = `${slugify(meta.title)}-${videoId}.md`;
    const md = frontmatter({
      title: meta.title,
      channel: meta.author,
      videoId,
      source: `https://www.youtube.com/watch?v=${videoId}`,
      transcribed: fmtDate(new Date()),
      type: "youtube-transcript",
    }) + transcript;

    const outPath = join(outDir, filename);
    writeFileSync(outPath, md);
    console.log(`\n✓ Saved: ${outPath}`);
    return;
  }

  // Playlist mode
  const playlistId = extractPlaylistId(values.playlist!);
  if (!playlistId) {
    console.error("Could not extract playlist ID from URL");
    process.exit(1);
  }

  console.log(`\nFetching playlist: ${playlistId}`);
  const videoIds = await getPlaylistVideoIds(playlistId);
  const limit = parseInt(values.limit || "5", 10);
  console.log(`  Found ${videoIds.length} videos`);

  if (values.list) {
    for (const [i, vid] of videoIds.entries()) {
      const meta = await getVideoMeta(vid);
      console.log(`  ${i + 1}. ${meta.title} (${vid})`);
      if (i >= 29) {
        console.log(`  ... and ${videoIds.length - 30} more`);
        break;
      }
    }
    return;
  }

  const toProcess = videoIds.slice(0, limit);
  const outDir = ensureOutputDir(values.output || `youtube/playlist-${playlistId.substring(0, 12)}`);
  console.log(`Processing ${toProcess.length} of ${videoIds.length} videos\n`);

  for (const [i, vid] of toProcess.entries()) {
    console.log(`[${i + 1}/${toProcess.length}] ${vid}`);
    try {
      const { transcript, meta } = await transcribeVideo(vid);
      const filename = `${slugify(meta.title)}-${vid}.md`;
      const md = frontmatter({
        title: meta.title,
        channel: meta.author,
        videoId: vid,
        source: `https://www.youtube.com/watch?v=${vid}`,
        transcribed: fmtDate(new Date()),
        type: "youtube-transcript",
      }) + transcript;

      const outPath = join(outDir, filename);
      writeFileSync(outPath, md);
      console.log(`  ✓ Saved: ${outPath}\n`);
    } catch (e: any) {
      console.error(`  ✗ Failed: ${e.message}\n`);
    }
  }
  console.log("Done.");
}

main().catch((e) => {
  console.error("Fatal:", e.message);
  process.exit(1);
});
