#!/usr/bin/env python3
"""
RSS Curation Pipeline for OpenEd
Fetches feeds from 40+ sources, outputs for manual scoring.

Usage:
  python3 curate.py --no-score           # List items without AI scoring
  python3 curate.py --no-score --days 1.5  # Last 36 hours
  python3 curate.py --json               # Output as JSON for Claude to score
  python3 curate.py --output FILE        # Write to file (for cron)
"""

import argparse
import feedparser
import json
import os
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

SKILL_DIR = Path(__file__).parent
FEEDS_FILE = SKILL_DIR / "feeds.json"
SLACK_CHANNEL = "curation-inbox"  # Private channel

PROMPT_TEMPLATE = """Rate this article for OpenEd relevance (1-5):

SCORING:
5 = Highly relevant - families mixing approaches, kids thriving outside traditional school, practical parent help, state news for AR/IN/IA/KS/MN/MT/NV/OR/UT
4 = Good fit - homeschool/alt-ed content with fresh angle, neurodiversity, curriculum comparisons
3 = Maybe - general education news with possible OpenEd angle
2 = Weak - public school focused, no homeschool angle
1 = Skip - political only, clickbait, dogmatic single-method, trashes public schools

ARTICLE:
Title: {title}
Source: {source}
Summary: {summary}

Respond with ONLY valid JSON: {{"score": N, "reason": "brief explanation", "angle": "OpenEd angle if score >= 4, else null"}}"""


def load_feeds():
    """Load feeds from JSON file."""
    with open(FEEDS_FILE) as f:
        data = json.load(f)
    return data.get("homeschool", [])


def fetch_feeds(feeds, days=1):
    """Fetch recent items from all feeds."""
    cutoff = datetime.now() - timedelta(days=days)
    items = []

    for feed_info in feeds:
        try:
            feed = feedparser.parse(feed_info["url"])
            for entry in feed.entries[:10]:  # Max 10 per feed
                published = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    published = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    published = datetime(*entry.updated_parsed[:6])

                if published and published < cutoff:
                    continue

                # Clean HTML from summary
                summary = re.sub('<[^<]+?>', '', entry.get('summary', ''))[:300]

                items.append({
                    "title": entry.get("title", "No title"),
                    "url": entry.get("link", ""),
                    "summary": summary,
                    "source": feed_info["name"],
                    "tier": feed_info.get("tier", 3),
                    "published": published,
                })
        except Exception as e:
            print(f"  Error fetching {feed_info['name']}: {e}", file=sys.stderr)

    return items


def score_item(item):
    """Score a single item using Claude CLI."""
    prompt = PROMPT_TEMPLATE.format(
        title=item["title"],
        source=item["source"],
        summary=item["summary"][:200]
    )

    # Write to temp file to avoid shell escaping issues
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(prompt)
        prompt_file = f.name

    try:
        result = subprocess.run(
            f"cat '{prompt_file}' | claude -p -",
            shell=True, capture_output=True, text=True, timeout=45
        )
        output = result.stdout.strip()

        # Find JSON in output
        for line in output.split('\n'):
            line = line.strip()
            if line.startswith('{') and 'score' in line:
                data = json.loads(line)
                return data.get('score', 0), data.get('reason', ''), data.get('angle')

        return 0, 'No JSON in response', None
    except json.JSONDecodeError:
        return 0, 'Invalid JSON', None
    except subprocess.TimeoutExpired:
        return 0, 'Timeout', None
    except Exception as e:
        return 0, str(e)[:50], None
    finally:
        os.unlink(prompt_file)


def format_slack_message(items):
    """Format items for Slack - clean, minimal formatting."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    lines = [
        f"*Daily Curation - {date_str}*",
        f"{len(items)} items scored 4+",
        ""
    ]

    for item in items:
        # Hyperlinked title with source
        lines.append(f"• <{item['url']}|{item['title']}> ({item['source']})")
        # Summary + angle combined
        summary = item.get('summary', '')[:150]
        if item.get('angle'):
            lines.append(f"  {summary}")
            lines.append(f"  *OpenEd angle:* {item['angle']}")
        else:
            lines.append(f"  {summary}")
        lines.append("")

    return "\n".join(lines)


def post_to_slack(message):
    """Post to Slack using MCP (via Claude)."""
    # This is a placeholder - actual posting happens via Claude's Slack MCP
    print("\n[Would post to Slack #curation-inbox]")
    print("Use Claude's Slack MCP: mcp__slack__conversations_add_message")
    print(f"Channel: {SLACK_CHANNEL}")
    return message


def main():
    parser = argparse.ArgumentParser(description="RSS Curation for OpenEd")
    parser.add_argument("--test", action="store_true", help="Dry run, don't post to Slack")
    parser.add_argument("--slack", action="store_true", help="Post to Slack")
    parser.add_argument("--days", type=float, default=1, help="Days to look back (default: 1, use 1.5 for 36hrs)")
    parser.add_argument("--all", action="store_true", help="Show all items, not just score 4+")
    parser.add_argument("--no-score", action="store_true", help="Skip AI scoring, just list items")
    parser.add_argument("--json", action="store_true", help="Output as JSON for Claude to score")
    parser.add_argument("--output", type=str, help="Write output to file")
    args = parser.parse_args()

    # Determine output destination
    out = open(args.output, 'w') if args.output else sys.stdout

    def log(msg):
        if not args.json:
            print(msg, file=sys.stderr if args.output else sys.stdout)

    log(f"Loading feeds from {FEEDS_FILE}...")
    feeds = load_feeds()
    log(f"Found {len(feeds)} feeds")

    log(f"\nFetching items from last {args.days} day(s)...")
    items = fetch_feeds(feeds, days=args.days)
    log(f"Found {len(items)} items")

    if not items:
        log("No items to process")
        return

    # JSON output mode - for Claude to score
    if args.json:
        # Convert datetime to string for JSON serialization
        for item in items:
            if item.get('published'):
                item['published'] = item['published'].isoformat()
        print(json.dumps(items, indent=2), file=out)
        if args.output:
            out.close()
        return

    if args.no_score:
        print(f"\n=== ITEMS ({len(items)}) ===", file=out)
        for item in sorted(items, key=lambda x: (x['tier'], x['source'])):
            pub = item['published'].strftime('%m/%d') if item['published'] else '?'
            print(f"[{pub}] T{item['tier']} {item['source'][:20]:20} | {item['title'][:60]}", file=out)
            print(f"       {item['url']}", file=out)
            if item.get('summary'):
                summary = item['summary'][:100].replace('\n', ' ')
                print(f"       {summary}...", file=out)
            print(file=out)
        if args.output:
            out.close()
        return

    log("\nScoring with Claude CLI (may have errors)...")
    for i, item in enumerate(items):
        score, reason, angle = score_item(item)
        item['score'] = score
        item['reason'] = reason
        item['angle'] = angle
        log(f"  [{score}] {item['source'][:15]:15} | {item['title'][:45]}...")

    # Sort by score descending
    items.sort(key=lambda x: (-x['score'], x['tier']))

    # Filter
    if args.all:
        display_items = items
    else:
        display_items = [i for i in items if i['score'] >= 4]

    print(f"\n=== RESULTS ({len(display_items)} items) ===\n", file=out)

    for item in display_items:
        pub = item['published'].strftime('%m/%d') if item['published'] else '?'
        print(f"[Score {item['score']}] {item['source']} ({pub})", file=out)
        print(f"  {item['title']}", file=out)
        print(f"  Reason: {item['reason']}", file=out)
        if item.get('angle'):
            print(f"  Angle: {item['angle']}", file=out)
        print(f"  URL: {item['url']}", file=out)
        print(file=out)

    if args.output:
        out.close()

    if args.slack and display_items:
        message = format_slack_message(display_items)
        post_to_slack(message)
    elif args.test:
        log("[DRY RUN - use --slack to post]")


if __name__ == "__main__":
    main()
