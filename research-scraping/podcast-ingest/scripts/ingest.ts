#!/usr/bin/env bun
/**
 * Podcast Ingest — RSS feed URL → episode list → Gemini transcription → polished markdown
 *
 * Usage:
 *   bun run podcast-ingest/scripts/ingest.ts --feed <rss-url> [--limit N] [--output dir]
 *   bun run podcast-ingest/scripts/ingest.ts --audio <audio-url> --title "Episode Title" [--output dir]
 */

import { parseArgs } from "util";
import { XMLParser } from "fast-xml-parser";
import { writeFileSync } from "fs";
import { join } from "path";
import { generate, uploadFile, deleteFile, cleanOutput } from "../../shared/ai";
import { ensureOutputDir, slugify, frontmatter, fmtDate } from "../../shared/config";

// --- Types ---

interface Episode {
  title: string;
  audioUrl: string;
  pubDate: string;
  duration?: string;
  description?: string;
  author?: string;
  link?: string;
}

interface FeedInfo {
  title: string;
  author?: string;
  description?: string;
  episodes: Episode[];
}

// --- RSS Parsing ---

async function fetchFeed(feedUrl: string): Promise<FeedInfo> {
  console.log(`Fetching feed: ${feedUrl}`);
  const res = await fetch(feedUrl, {
    headers: { "User-Agent": "DoodleSkills/1.0" },
    signal: AbortSignal.timeout(15000),
  });
  if (!res.ok) throw new Error(`Feed fetch failed: ${res.status}`);
  const xml = await res.text();

  const parser = new XMLParser({
    ignoreAttributes: false,
    attributeNamePrefix: "@_",
  });
  const doc = parser.parse(xml);

  // Handle RSS 2.0
  const channel = doc.rss?.channel;
  if (!channel) throw new Error("Not a valid RSS feed (no <channel> found)");

  const feedTitle = channel.title || "Unknown Podcast";
  const feedAuthor = channel["itunes:author"] || channel.managingEditor || "";
  const feedDesc = channel.description || "";

  const rawItems = Array.isArray(channel.item) ? channel.item : channel.item ? [channel.item] : [];

  const episodes: Episode[] = rawItems
    .map((item: any) => {
      const enclosure = item.enclosure;
      let audioUrl = "";
      if (enclosure) {
        audioUrl = enclosure["@_url"] || "";
      }
      if (!audioUrl) {
        const media = item["media:content"];
        if (media) audioUrl = media["@_url"] || "";
      }
      if (!audioUrl) return null;

      return {
        title: item.title || "Untitled",
        audioUrl,
        pubDate: item.pubDate || "",
        duration: item["itunes:duration"] || "",
        description: (item["itunes:summary"] || item.description || "").substring(0, 500),
        author: item["itunes:author"] || feedAuthor,
        link: item.link || "",
      } as Episode;
    })
    .filter(Boolean) as Episode[];

  console.log(`  Found ${episodes.length} episodes with audio`);
  return { title: feedTitle, author: feedAuthor, description: feedDesc, episodes };
}

// --- Transcription ---

const TRANSCRIBE_PROMPT = (meta: {
  title: string;
  feedName?: string;
  author?: string;
  description?: string;
}) => `You are a professional transcriptionist. Transcribe this audio completely and accurately.

Episode: "${meta.title}"
${meta.feedName ? `Podcast: "${meta.feedName}"` : ""}
${meta.author ? `Host/Author: ${meta.author}` : ""}
${meta.description ? `Description: ${meta.description}` : ""}

## Output Format

1. **Summary:** 2-3 sentence summary
2. **Topics:** 3-5 topic tags, comma-separated
3. **Speakers:** List distinct speakers (be conservative — only clearly different voices)
4. Full transcript with ## section headers when topics change

## Rules
- Transcribe EVERYTHING verbatim — do not summarize or skip
- Clean up filler words (um, uh) but preserve speaker voice
- Use **Name:** labels when speakers are identifiable
- Mark ads/sponsors with [AD]
- Preserve technical terms and names exactly as spoken`;

const INLINE_SIZE_LIMIT = 20 * 1024 * 1024; // 20MB

async function transcribeEpisode(
  audioUrl: string,
  meta: { title: string; feedName?: string; author?: string; description?: string }
): Promise<string> {
  console.log(`  Downloading audio...`);
  const audioRes = await fetch(audioUrl, {
    headers: { "User-Agent": "DoodleSkills/1.0" },
    redirect: "follow",
  });
  if (!audioRes.ok) throw new Error(`Audio download failed: ${audioRes.status}`);
  const audioBuffer = await audioRes.arrayBuffer();
  const audioBytes = new Uint8Array(audioBuffer);
  const mimeType = audioRes.headers.get("content-type") || "audio/mpeg";
  const sizeMB = (audioBytes.length / (1024 * 1024)).toFixed(1);
  console.log(`  Downloaded: ${sizeMB} MB (${mimeType})`);

  const prompt = TRANSCRIBE_PROMPT(meta);

  if (audioBytes.length <= INLINE_SIZE_LIMIT) {
    // Inline base64
    console.log(`  Transcribing (inline)...`);
    const base64 = Buffer.from(audioBytes).toString("base64");
    return cleanOutput(
      await generate({
        parts: [
          { inlineData: { mimeType, data: base64 } },
          { text: prompt },
        ],
      })
    );
  } else {
    // Upload via Files API
    console.log(`  Uploading to Gemini Files API...`);
    const file = await uploadFile(audioBytes, mimeType, meta.title);
    console.log(`  Transcribing (uploaded file)...`);
    try {
      return cleanOutput(
        await generate({
          parts: [
            { fileData: { mimeType, fileUri: file.uri } },
            { text: prompt },
          ],
        })
      );
    } finally {
      await deleteFile(file.name);
    }
  }
}

// --- Main ---

async function main() {
  const { values } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      feed: { type: "string" },
      audio: { type: "string" },
      title: { type: "string" },
      limit: { type: "string", default: "1" },
      output: { type: "string" },
      list: { type: "boolean", default: false },
    },
    strict: true,
  });

  if (!values.feed && !values.audio) {
    console.log(`Usage:
  bun run podcast-ingest/scripts/ingest.ts --feed <rss-url> [--limit N] [--list]
  bun run podcast-ingest/scripts/ingest.ts --audio <audio-url> --title "Episode Title"

Options:
  --feed    RSS feed URL (lists and transcribes episodes)
  --audio   Direct audio URL (transcribe a single file)
  --title   Episode title (used with --audio)
  --limit   Number of episodes to transcribe (default: 1)
  --list    List episodes without transcribing
  --output  Output directory (default: output/podcasts/)`);
    process.exit(1);
  }

  // Single audio URL mode
  if (values.audio) {
    const title = values.title || "untitled-episode";
    const outDir = ensureOutputDir(values.output || "podcasts");
    console.log(`\nTranscribing: ${title}`);
    const transcript = await transcribeEpisode(values.audio, { title });
    const filename = `${slugify(title)}-${fmtDate(new Date())}.md`;
    const md = frontmatter({
      title,
      source: values.audio,
      transcribed: fmtDate(new Date()),
      type: "podcast-transcript",
    }) + transcript;

    const outPath = join(outDir, filename);
    writeFileSync(outPath, md);
    console.log(`\n✓ Saved: ${outPath}`);
    return;
  }

  // Feed mode
  const feed = await fetchFeed(values.feed!);
  const limit = parseInt(values.limit || "1", 10);

  if (values.list) {
    console.log(`\n${feed.title} (${feed.episodes.length} episodes)\n`);
    for (const [i, ep] of feed.episodes.entries()) {
      const date = ep.pubDate ? fmtDate(ep.pubDate) : "no date";
      console.log(`  ${i + 1}. [${date}] ${ep.title}`);
      if (i >= 29) {
        console.log(`  ... and ${feed.episodes.length - 30} more`);
        break;
      }
    }
    return;
  }

  const outDir = ensureOutputDir(values.output || `podcasts/${slugify(feed.title)}`);
  const toProcess = feed.episodes.slice(0, limit);
  console.log(`\nProcessing ${toProcess.length} of ${feed.episodes.length} episodes from "${feed.title}"\n`);

  for (const [i, ep] of toProcess.entries()) {
    console.log(`[${i + 1}/${toProcess.length}] ${ep.title}`);
    try {
      const transcript = await transcribeEpisode(ep.audioUrl, {
        title: ep.title,
        feedName: feed.title,
        author: ep.author,
        description: ep.description,
      });

      const filename = `${slugify(ep.title)}-${fmtDate(ep.pubDate || new Date())}.md`;
      const md = frontmatter({
        title: ep.title,
        podcast: feed.title,
        author: ep.author,
        date: ep.pubDate ? fmtDate(ep.pubDate) : undefined,
        duration: ep.duration,
        source: ep.audioUrl,
        link: ep.link,
        transcribed: fmtDate(new Date()),
        type: "podcast-transcript",
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
