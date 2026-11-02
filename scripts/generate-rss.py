#!/usr/bin/env python3
"""
RSS 2.0, Media RSS Feed & Google Image Sitemap Generator for sjkonfilm.work
Scans all gallery images, builds rss.xml with unique titles, <enclosure>, <media:content>,
and ?photo=slug deep-linked Lightbox URLs for Pinterest Auto-Pinning,
and updates sitemap.xml with full Google Image Sitemap (<image:image>) entries.
"""

import os
import re
import glob
from datetime import datetime, timezone, timedelta
from xml.sax.saxutils import escape

SITE_URL = "https://sjkonfilm.work"
SITE_TITLE = "Sawyer Knox | 35mm & 120 Film Photography"
SITE_DESC = "Authentic, gritty 35mm and 120 film photography portfolio by Sawyer Knox. Portland, Oregon."

def get_slug_from_path(path_str):
    base = os.path.basename(path_str)
    slug = re.sub(r'\.(webp|avif|jpe?g|png)$', '', base, flags=re.IGNORECASE)
    slug = re.sub(r'-400w$', '', slug, flags=re.IGNORECASE)
    return slug

def extract_gallery_items():
    """Extract image metadata across all gallery pages."""
    items = []
    seen = set()
    page_images = {}
    title_counts = {}

    pages = sorted(glob.glob("pages/*.html")) + ["index.html"]
    for page_path in pages:
        cat = os.path.splitext(os.path.basename(page_path))[0]
        normalized_page = page_path.replace("\\", "/")
        page_url = f"{SITE_URL}/{normalized_page}"
        if normalized_page == "index.html":
            page_url = f"{SITE_URL}/"

        with open(page_path, "r", encoding="utf-8") as f:
            content = f.read()

        if "http-equiv=\"refresh\"" in content.lower():
            continue

        img_pattern = re.compile(
            r'<img\s+[^>]*src="([^"]+)"[^>]*data-full="([^"]+)"[^>]*alt="([^"]*)"[^>]*>',
            re.IGNORECASE
        )

        page_images.setdefault(page_url, [])

        for match in img_pattern.finditer(content):
            thumb_src, full_src, alt_text = match.groups()
            
            # Normalize full image URL
            clean_full = full_src.replace("../", "").replace("./", "").lstrip("/")
            img_url = f"{SITE_URL}/{clean_full}"
            slug = get_slug_from_path(clean_full)

            # Build item title and description (Strict facts only)
            base_title = alt_text.strip() if alt_text and not alt_text.startswith("New Location") else f"Film Photograph - {cat.title()}"
            if "Sawyer Knox" not in base_title:
                base_title = f"{base_title} - Sawyer Knox"

            film_label = "120 medium format film" if cat == "120" else "35mm film"
            desc = f"{base_title}. Shot on analog {film_label} by Sawyer Knox. Instagram: @sawyer.j.knox | Portfolio & prints: {SITE_URL}"

            page_images[page_url].append({
                "title": base_title,
                "caption": desc,
                "image_url": img_url
            })

            if img_url in seen:
                continue
            seen.add(img_url)

            # Deduplicate titles with #2, #3, etc. for Pinterest RSS compliance
            title_counts[base_title] = title_counts.get(base_title, 0) + 1
            if title_counts[base_title] > 1:
                unique_title = f"{base_title} #{title_counts[base_title]}"
            else:
                unique_title = base_title

            deep_link = f"{page_url}?photo={slug}" if slug and normalized_page != "index.html" else page_url
            file_size = os.path.getsize(clean_full) if os.path.exists(clean_full) else 0

            items.append({
                "title": unique_title,
                "link": deep_link,
                "guid": img_url,
                "image_url": img_url,
                "file_size": file_size,
                "description": desc,
                "category": cat
            })

    return items, page_images

def generate_rss_xml(items):
    """Generate RSS 2.0 XML string with Media RSS namespace and <enclosure> tags."""
    now_dt = datetime.now(timezone.utc)
    now_rfc822 = now_dt.strftime("%a, %d %b %Y %H:%M:%S +0000")

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

    for idx, item in enumerate(items):
        item_dt = (now_dt - timedelta(seconds=idx)).strftime("%a, %d %b %Y %H:%M:%S +0000")
        xml_lines.extend([
            '    <item>',
            f'      <title>{escape(item["title"])}</title>',
            f'      <link>{escape(item["link"])}</link>',
            f'      <guid isPermaLink="true">{escape(item["guid"])}</guid>',
            f'      <pubDate>{item_dt}</pubDate>',
            f'      <description>{escape(item["description"])}</description>',
            f'      <category>{escape(item["category"])}</category>',
            f'      <enclosure url="{escape(item["image_url"])}" length="{item["file_size"]}" type="image/webp" />',
            f'      <media:content url="{escape(item["image_url"])}" medium="image" type="image/webp" />',
            '    </item>'
        ])

    xml_lines.extend([
        '  </channel>',
        '</rss>'
    ])

    return "\n".join(xml_lines)

def generate_image_sitemap_xml(page_images):
    """Generate sitemap.xml with Google Image Sitemap (<image:image>) tags."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    core_pages = [
        f"{SITE_URL}/",
        f"{SITE_URL}/works.html",
        f"{SITE_URL}/about.html",
        f"{SITE_URL}/contact.html",
        f"{SITE_URL}/pages/35mm.html",
        f"{SITE_URL}/pages/color.html",
        f"{SITE_URL}/pages/120.html",
    ]

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'
    ]

    for url in core_pages:
        lines.append('  <url>')
        lines.append(f'    <loc>{escape(url)}</loc>')
        lines.append(f'    <lastmod>{today}</lastmod>')
        imgs = page_images.get(url, [])
        for img in imgs:
            lines.extend([
                '    <image:image>',
                f'      <image:loc>{escape(img["image_url"])}</image:loc>',
                f'      <image:title>{escape(img["title"])}</image:title>',
                f'      <image:caption>{escape(img["caption"])}</image:caption>',
                '    </image:image>'
            ])
        lines.append('  </url>')

    lines.append('</urlset>')
    return "\n".join(lines) + "\n"

def main():
    items, page_images = extract_gallery_items()
    rss_xml = generate_rss_xml(items)

    output_path = "rss.xml"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(rss_xml)
    print(f"Generated {output_path} with {len(items)} deep-linked image feed items.")

    sitemap_xml = generate_image_sitemap_xml(page_images)
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(sitemap_xml)
    total_sitemap_imgs = sum(len(v) for v in page_images.values())
    print(f"Generated sitemap.xml with {total_sitemap_imgs} Google Image Sitemap entries.")

if __name__ == "__main__":
    main()
