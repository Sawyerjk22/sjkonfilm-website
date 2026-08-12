#!/usr/bin/env python3
"""
RSS 2.0 & Media RSS Feed Generator for sjkonfilm.work
Scans all gallery images and builds rss.xml for RSS readers and Pinterest Auto-Pinning.
"""

import os
import re
import glob
from datetime import datetime, timezone
from xml.sax.saxutils import escape

SITE_URL = "https://sjkonfilm.work"
SITE_TITLE = "Sawyer Knox | 35mm & 120 Film Photography"
SITE_DESC = "Authentic, gritty 35mm and 120 film photography portfolio by Sawyer Knox. Portland, Oregon."

def extract_gallery_items():
    """Extract image metadata across all gallery pages."""
    items = []
    seen = set()

    pages = glob.glob("pages/*.html") + ["index.html"]
    for page_path in pages:
        cat = os.path.splitext(os.path.basename(page_path))[0]
        page_url = f"{SITE_URL}/{page_path.replace('\\', '/')}"

        with open(page_path, "r", encoding="utf-8") as f:
            content = f.read()

        img_pattern = re.compile(
            r'<img\s+[^>]*src="([^"]+)"[^>]*data-full="([^"]+)"[^>]*alt="([^"]*)"[^>]*>',
            re.IGNORECASE
        )

        for match in img_pattern.finditer(content):
            thumb_src, full_src, alt_text = match.groups()
            
            # Normalize full image URL
            clean_full = full_src.replace("../", "").replace("./", "")
            img_url = f"{SITE_URL}/{clean_full.lstrip('/')}"

            if img_url in seen:
                continue
            seen.add(img_url)

            # Build item title and description
            title = alt_text if alt_text and not alt_text.startswith("New Location") else f"Film Photograph - {cat.title()}"
            desc = f"{alt_text}. Captured on 35mm / 120 film by Sawyer Knox in Portland, Oregon and worldwide."

            items.append({
                "title": title,
                "link": page_url,
                "guid": img_url,
                "image_url": img_url,
                "description": desc,
                "category": cat
            })

    return items

def generate_rss_xml(items):
    """Generate RSS 2.0 XML string with Media RSS namespace."""
    now_rfc822 = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0" xmlns:media="http://search.yahoo.com/mrss/" xmlns:atom="http://www.w3.org/2005/Atom">',
        '  <channel>',
        f'    <title>{escape(SITE_TITLE)}</title>',
        f'    <link>{SITE_URL}</link>',
        f'    <description>{escape(SITE_DESC)}</description>',
        '    <language>en-us</language>',
        f'    <lastBuildDate>{now_rfc822}</lastBuildDate>',
        f'    <atom:link href="{SITE_URL}/rss.xml" rel="self" type="application/rss+xml" />',
    ]

    for item in items:
        xml_lines.extend([
            '    <item>',
            f'      <title>{escape(item["title"])}</title>',
            f'      <link>{escape(item["link"])}</link>',
            f'      <guid isPermaLink="true">{escape(item["guid"])}</guid>',
            f'      <pubDate>{now_rfc822}</pubDate>',
            f'      <description>{escape(item["description"])}</description>',
            f'      <category>{escape(item["category"])}</category>',
            f'      <media:content url="{escape(item["image_url"])}" medium="image" type="image/webp" />',
            '    </item>'
        ])

    xml_lines.extend([
        '  </channel>',
        '</rss>'
    ])

    return "\n".join(xml_lines)

def main():
    items = extract_gallery_items()
    rss_xml = generate_rss_xml(items)

    output_path = "rss.xml"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rss_xml)

    print(f"Generated {output_path} with {len(items)} image feed items.")

if __name__ == "__main__":
    main()
