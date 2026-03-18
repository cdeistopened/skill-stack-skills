#!/usr/bin/env python3
"""
Kill the Newsletter - Automated Feed Creation

Usage:
  python3 ktn_create.py "HSLDA Newsletter"
  python3 ktn_create.py "Withyweather" "Coach Meg Thomas"
"""

import sys
import json
import re
from playwright.sync_api import sync_playwright


def create_ktn_feed(title: str) -> dict:
    """Create a Kill the Newsletter feed and return the email + feed URL."""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Go to KTN
        page.goto("https://kill-the-newsletter.com/")

        # Fill the title field
        page.fill('input[name="title"]', title)

        # Submit the form
        page.click('button[type="submit"]')

        # Wait for redirect to feed page
        page.wait_for_url(re.compile(r"/feeds/[a-z0-9]+"), timeout=10000)

        # Extract the feed ID from URL
        feed_url = page.url
        feed_id = feed_url.split("/feeds/")[1].rstrip("/")

        # Get the email and feed URL from the page
        email = f"{feed_id}@kill-the-newsletter.com"
        atom_url = f"https://kill-the-newsletter.com/feeds/{feed_id}.xml"

        browser.close()

        return {
            "title": title,
            "feed_id": feed_id,
            "email": email,
            "atom_url": atom_url,
        }


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 ktn_create.py 'Newsletter Title' ['Another Title' ...]")
        sys.exit(1)

    titles = sys.argv[1:]
    results = []

    for title in titles:
        print(f"Creating KTN feed for: {title}...")
        try:
            result = create_ktn_feed(title)
            results.append(result)
            print(f"  ✅ Email: {result['email']}")
            print(f"  ✅ Feed:  {result['atom_url']}")
            print()
        except Exception as e:
            print(f"  ❌ Error: {e}")
            print()

    if results:
        print("\n=== SUMMARY ===")
        print("Add these to feeds.json:\n")
        for r in results:
            print(f'{{"name": "{r["title"]}", "url": "{r["atom_url"]}", "tier": 3}},')

        print("\n\nSubscribe to newsletters with these emails:")
        for r in results:
            print(f"  {r['title']}: {r['email']}")


if __name__ == "__main__":
    main()
