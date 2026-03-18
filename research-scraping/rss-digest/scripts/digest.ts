#!/usr/bin/env bun
/**
 * RSS Digest — fetch feeds → filter → AI summarize → markdown digest
 *
 * Usage:
 *   bun run rss-digest/scripts/digest.ts --feeds feeds.json [--hours 24] [--output dir]
 *   bun run rss-digest/scripts/digest.ts --opml feeds.opml [--hours 24]
 *   bun run rss-digest/scripts/digest.ts --url <feed-url> [--limit 10]
 *
 * feeds.json format:
 *   { "feeds": ["https://example.com/feed", ...], "lastRun": "2026-02-18T00:00:00Z" }
 */

import { parseArgs } from "util";
import { XMLParser } from "fast-xml-parser";
import { readFileSync, writeFileSync } from "fs";
import { join } from "path";
import { generateText, cleanOutput } from "../../shared/ai";
import { ensureOutputDir, frontmatter, fmtDate } from "../../shared/config";
import { fetchArticles, matchesKeywords, type FeedArticle } from "../../shared/rss";

// --- Types ---

interface FeedsConfig {
  feeds: string[];
  lastRun?: string;
  keywords?: string[];
  noKeywords?: string[];
}

// --- OPML parsing ---

function parseOPML(opmlPath: string): string[] {
  const xml = readFileSync(opmlPath, "utf-8");
  const parser = new XMLParser({ ignoreAttributes: false, attributeNamePrefix: "@_" });
  const doc = parser.parse(xml);
  const feeds: string[] = [];

  function walk(node: any) {
    if (!node) return;
    const items = Array.isArray(node) ? node : [node];
    for (const item of items) {
      if (item["@_xmlUrl"]) feeds.push(item["@_xmlUrl"]);
      if (item.outline) walk(item.outline);
    }
  }

  walk(doc.opml?.body?.outline);
  return feeds;
}

// --- AI Digest ---

async function generateDigest(articles: FeedArticle[]): Promise<string> {
  if (articles.length === 0) return "*No new articles found.*";

  const articleList = articles
    .map(
      (a, i) =>
        `${i + 1}. **${a.title}** (${a.feed})\n   ${a.snippet}\n   URL: ${a.url}`
    )
    .join("\n\n");

  const prompt = `You are a research assistant creating a daily digest of RSS feed articles.

Here are ${articles.length} articles from today's feeds:

${articleList}

Create a well-organized digest with:
1. A 2-3 sentence **Executive Summary** of the top themes
2. Group articles by topic theme (not by source)
3. For each article: one-sentence summary with [link](url)
4. End with a **Worth Reading** section highlighting the 2-3 most important pieces

Format as clean markdown. Be concise — this is a scanning document, not a deep read.`;

  return cleanOutput(await generateText(prompt, { maxTokens: 8192, temperature: 0.3 }));
}

// --- Main ---

async function main() {
  const { values } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      feeds: { type: "string" },
      opml: { type: "string" },
      url: { type: "string" },
      hours: { type: "string" },
      limit: { type: "string", default: "50" },
      output: { type: "string" },
      raw: { type: "boolean", default: false },
    },
    strict: true,
  });

  if (!values.feeds && !values.opml && !values.url) {
    console.log(`Usage:
  bun run rss-digest/scripts/digest.ts --feeds feeds.json [--hours 24]
  bun run rss-digest/scripts/digest.ts --opml feeds.opml [--hours 24]
  bun run rss-digest/scripts/digest.ts --url <feed-url> [--limit 10]

Options:
  --feeds   Path to feeds.json config
  --opml    Path to OPML file
  --url     Single feed URL
  --hours   Only include articles from last N hours (auto-calculated from lastRun if --feeds)
  --limit   Max articles per feed (default: 50)
  --raw     Output raw article list instead of AI digest
  --output  Output directory`);
    process.exit(1);
  }

  let feedUrls: string[] = [];
  let sinceDate: Date | undefined;
  let config: FeedsConfig | undefined;

  // Load feeds
  if (values.feeds) {
    const raw = readFileSync(values.feeds, "utf-8");
    config = JSON.parse(raw) as FeedsConfig;
    feedUrls = config.feeds;
    // Auto-calculate since from lastRun
    if (config.lastRun && !values.hours) {
      sinceDate = new Date(config.lastRun);
      const hoursAgo = ((Date.now() - sinceDate.getTime()) / 3600000).toFixed(1);
      console.log(`Incremental: fetching since ${config.lastRun} (${hoursAgo}h ago)`);
    }
  } else if (values.opml) {
    feedUrls = parseOPML(values.opml);
    console.log(`Loaded ${feedUrls.length} feeds from OPML`);
  } else if (values.url) {
    feedUrls = [values.url];
  }

  if (values.hours) {
    const hoursAgo = parseFloat(values.hours);
    sinceDate = new Date(Date.now() - hoursAgo * 3600000);
    console.log(`Filtering: last ${hoursAgo} hours`);
  }

  // Fetch all feeds
  console.log(`\nFetching ${feedUrls.length} feeds...`);
  const allArticles: FeedArticle[] = [];

  for (const url of feedUrls) {
    const articles = await fetchArticles(url, sinceDate);
    if (articles.length > 0) {
      console.log(`  ✓ ${articles[0].feed}: ${articles.length} articles`);
      // Apply keyword filter
      const filtered = articles.filter((a) =>
        matchesKeywords(a, config?.keywords, config?.noKeywords)
      );
      allArticles.push(...filtered);
    }
  }

  const limit = parseInt(values.limit || "50", 10);
  // Sort by date, newest first
  allArticles.sort((a, b) => {
    try { return new Date(b.pubDate).getTime() - new Date(a.pubDate).getTime(); } catch { return 0; }
  });
  const articles = allArticles.slice(0, limit);

  console.log(`\n${articles.length} articles after filtering (of ${allArticles.length} total)\n`);

  if (articles.length === 0) {
    console.log("No new articles. Exiting.");
    // Update lastRun
    if (values.feeds && config) {
      config.lastRun = new Date().toISOString();
      writeFileSync(values.feeds, JSON.stringify(config, null, 2));
    }
    return;
  }

  // Generate output
  const outDir = ensureOutputDir(values.output || "digests");
  const today = fmtDate(new Date());

  if (values.raw) {
    // Raw article list
    const lines = articles.map(
      (a) => `- **${a.title}** (${a.feed}) — ${a.snippet}\n  ${a.url}`
    );
    const md = frontmatter({
      title: `RSS Digest ${today}`,
      articles: articles.length,
      feeds: feedUrls.length,
      generated: fmtDate(new Date()),
      type: "rss-digest",
    }) + lines.join("\n\n");

    const outPath = join(outDir, `digest-raw-${today}.md`);
    writeFileSync(outPath, md);
    console.log(`✓ Raw digest saved: ${outPath}`);
  } else {
    // AI-summarized digest
    console.log("Generating AI digest...");
    const digest = await generateDigest(articles);

    const md = frontmatter({
      title: `RSS Digest ${today}`,
      articles: articles.length,
      feeds: feedUrls.length,
      generated: fmtDate(new Date()),
      type: "rss-digest",
    }) + digest;

    const outPath = join(outDir, `digest-${today}.md`);
    writeFileSync(outPath, md);
    console.log(`✓ AI digest saved: ${outPath}`);
  }

  // Update lastRun
  if (values.feeds && config) {
    config.lastRun = new Date().toISOString();
    writeFileSync(values.feeds, JSON.stringify(config, null, 2));
    console.log(`Updated lastRun in ${values.feeds}`);
  }
}

main().catch((e) => {
  console.error("Fatal:", e.message);
  process.exit(1);
});
