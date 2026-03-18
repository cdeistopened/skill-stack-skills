#!/usr/bin/env bun
/**
 * Web Scrape — URLs → clean markdown
 *
 * Uses Defuddle (by kepano/Obsidian) for intelligent content extraction.
 * Defuddle scores DOM elements to find the real content, strips clutter,
 * and converts to markdown — replacing our old Turndown + regex approach.
 *
 * Usage:
 *   bun run web-scrape/scripts/scrape.ts --url <url> [--output dir]
 *   bun run web-scrape/scripts/scrape.ts --file urls.txt [--output dir]
 *   bun run web-scrape/scripts/scrape.ts --url <url> --summarize
 */

import { parseArgs } from "util";
import { readFileSync, writeFileSync } from "fs";
import { join } from "path";
import { scrapeUrl, type ScrapeResult } from "../../shared/scrape";
import { generateText, cleanOutput } from "../../shared/ai";
import { ensureOutputDir, slugify, frontmatter, fmtDate } from "../../shared/config";

// --- AI Summary ---

async function summarize(markdown: string, title: string, author: string): Promise<string> {
  const prompt = `Summarize this article in 3-5 bullet points, then provide 3-5 topic tags.

Title: ${title}
Author: ${author || "Unknown"}

Article content:
${markdown.substring(0, 15000)}

Format:
## Summary
- bullet 1
- bullet 2
...

**Topics:** tag1, tag2, tag3`;

  return cleanOutput(await generateText(prompt, { maxTokens: 2048, temperature: 0.2 }));
}

// --- Main ---

async function main() {
  const { values } = parseArgs({
    args: Bun.argv.slice(2),
    options: {
      url: { type: "string" },
      file: { type: "string" },
      output: { type: "string" },
      summarize: { type: "boolean", default: false },
    },
    strict: true,
  });

  if (!values.url && !values.file) {
    console.log(`Usage:
  bun run web-scrape/scripts/scrape.ts --url <url>
  bun run web-scrape/scripts/scrape.ts --file urls.txt

Options:
  --summarize  Add AI summary at the top
  --output     Output directory (default: output/scraped/)`);
    process.exit(1);
  }

  let urls: string[] = [];
  if (values.url) {
    urls = [values.url];
  } else if (values.file) {
    urls = readFileSync(values.file, "utf-8")
      .split("\n")
      .map((l) => l.trim())
      .filter((l) => l && !l.startsWith("#"));
    console.log(`Loaded ${urls.length} URLs from ${values.file}`);
  }

  const outDir = ensureOutputDir(values.output || "scraped");
  console.log(`\nScraping ${urls.length} URL(s)...\n`);

  for (const [i, url] of urls.entries()) {
    if (urls.length > 1) console.log(`[${i + 1}/${urls.length}]`);
    try {
      console.log(`  Fetching: ${url}`);
      const result = await scrapeUrl(url);
      console.log(`  ✓ ${result.title} (${result.wordCount} words)`);

      let content = result.markdown;
      if (values.summarize) {
        console.log(`  Summarizing...`);
        const summary = await summarize(result.markdown, result.title, result.author);
        content = summary + "\n\n---\n\n" + result.markdown;
      }

      const filename = `${slugify(result.title)}-${fmtDate(new Date())}.md`;
      const md = frontmatter({
        title: result.title,
        author: result.author || undefined,
        description: result.description || undefined,
        source: url,
        domain: result.domain,
        date: result.publishedDate || undefined,
        scraped: fmtDate(new Date()),
        words: result.wordCount,
        type: "web-scrape",
      }) + content;

      const outPath = join(outDir, filename);
      writeFileSync(outPath, md);
      console.log(`  → ${outPath}\n`);
    } catch (e: any) {
      console.error(`  ✗ ${url}: ${e.message}\n`);
    }
  }
  console.log("Done.");
}

main().catch((e) => {
  console.error("Fatal:", e.message);
  process.exit(1);
});
