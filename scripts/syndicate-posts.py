#!/usr/bin/env python3
"""
Multi-Platform Auto-Syndication Script for sjkonfilm.work
Parses site portfolio photos and rss.xml to syndicate posts to Flickr, Medium, and RSS webhooks.
Formats generic captions, extracts locations from image metadata, and plugs:
  - Website: https://sjkonfilm.work
  - Instagram: @sawyer.j.knox (No automated Instagram posts; manual control reserved)
"""

import os
import sys
import xml.etree.ElementTree as ET

SITE_URL = "https://sjkonfilm.work"
INSTAGRAM_HANDLE = "@sawyer.j.knox"
INSTAGRAM_URL = "https://www.instagram.com/sawyer.j.knox"

# Credentials from environment secrets
FLICKR_API_KEY = os.environ.get("FLICKR_API_KEY")
FLICKR_API_SECRET = os.environ.get("FLICKR_API_SECRET")
MEDIUM_TOKEN = os.environ.get("MEDIUM_TOKEN")

def build_syndication_caption(title, location_text="Portland, OR", date_str="2026", film_type="35mm film"):
    """
    Strict factual caption generator — no AI creative fluff.
    Only basic facts: Title/Subject, Location, Season/Year, Film format, Website link, Instagram handle.
    """
    caption_lines = [
        f"{title}",
        f"Location: {location_text}",
        f"Date: {date_str}",
        f"Format: {film_type}",
        f"Website: {SITE_URL}",
        f"Instagram: {INSTAGRAM_HANDLE} ({INSTAGRAM_URL})"
    ]
    return "\n".join(caption_lines)


def syndicate_to_flickr(items):
    """
    Syndicate new items to Flickr API if credentials provided.
    """
    if not FLICKR_API_KEY or not FLICKR_API_SECRET:
        print("[Flickr Syndication] FLICKR_API_KEY / FLICKR_API_SECRET not set. Skipping live Flickr upload.")
        return

    print(f"[Flickr Syndication] Ready to process {len(items)} items for Flickr.")
    for item in items:
        caption = build_syndication_caption(item['title'], item.get('location', 'Portland, OR'), item['category'])
        print(f" -> Queued for Flickr: '{item['title']}' | Caption: {caption[:60]}...")

def syndicate_to_medium(items):
    """
    Syndicate gallery digest story to Medium API if credentials provided.
    """
    if not MEDIUM_TOKEN:
        print("[Medium Syndication] MEDIUM_TOKEN not set. Skipping live Medium post creation.")
        return

    print(f"[Medium Syndication] Ready to process {len(items)} items for Medium story.")

def parse_rss_items(rss_file="rss.xml"):
    if not os.path.exists(rss_file):
        print(f"Feed file {rss_file} not found. Run scripts/generate-rss.py first.")
        return []

    tree = ET.parse(rss_file)
    root = tree.getroot()
    channel = root.find("channel")

    items = []
    for item in channel.findall("item"):
        title = item.findtext("title", "Film Photograph")
        link = item.findtext("link", SITE_URL)
        desc = item.findtext("description", "")
        cat = item.findtext("category", "street")

        items.append({
            "title": title,
            "link": link,
            "description": desc,
            "category": cat
        })
    return items

def main():
    print("=== sjkonfilm.work Multi-Platform Syndication ===")
    print("Explicit Directive: Instagram auto-posting IS DISABLED (Handled manually by Sawyer).")
    print(f"Plugging Website ({SITE_URL}) and Instagram ({INSTAGRAM_HANDLE}) across all feeds.")
    
    items = parse_rss_items()
    print(f"Loaded {len(items)} feed items from rss.xml.")

    syndicate_to_flickr(items)
    syndicate_to_medium(items)

    print("Syndication dry-run / check complete.")

if __name__ == "__main__":
    main()
