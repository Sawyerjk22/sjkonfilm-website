#!/usr/bin/env python3
"""
Pinterest Bulk CSV Exporter for sjkonfilm.work
Parses site gallery images and exports a formatted CSV for Pinterest bulk pin upload.
"""

import os
import re
import csv
import glob

SITE_URL = "https://sjkonfilm.work"

BOARD_MAP = {
    "street": "35mm Street Photography",
    "scenes": "Analog Landscapes & Scenes",
    "color": "Color Film Photography",
    "vertical": "Vertical Film Shots & Portraits",
    "120": "Rolleiflex 120 Medium Format",
    "index": "Featured Film Photography"
}

def export_pinterest_csv():
    items = []
    seen = set()

    pages = glob.glob("pages/*.html") + ["index.html"]

    title_counts = {}

    for page_path in pages:
        cat = os.path.splitext(os.path.basename(page_path))[0]
        board_name = BOARD_MAP.get(cat, "Film Photography")
        dest_link = f"{SITE_URL}/{page_path.replace('\\', '/')}"

        with open(page_path, "r", encoding="utf-8") as f:
            content = f.read()

        img_pattern = re.compile(
            r'<img\s+[^>]*src="([^"]+)"[^>]*data-full="([^"]+)"[^>]*alt="([^"]*)"[^>]*>',
            re.IGNORECASE
        )

        for match in img_pattern.finditer(content):
            thumb_src, full_src, alt_text = match.groups()
            
            clean_full = full_src.replace("../", "").replace("./", "")
            media_url = f"{SITE_URL}/{clean_full.lstrip('/')}"

            if media_url in seen:
                continue
            seen.add(media_url)

            base_title = alt_text.strip() if alt_text and not alt_text.startswith("New Location") else f"{cat.title()} Film Photography"
            
            title_counts[base_title] = title_counts.get(base_title, 0) + 1
            if title_counts[base_title] > 1:
                title = f"{base_title} #{title_counts[base_title]}"
            else:
                title = base_title

            desc = f"{title}. Shot on analog 35mm / 120 film by Sawyer Knox in Portland, Oregon. Explore more film photography at sjkonfilm.work."

            items.append({
                "Title": title,
                "Media URL": media_url,
                "Destination Link": dest_link,
                "Description": desc,
                "Pinterest board": board_name
            })

    fieldnames = ["Title", "Media URL", "Destination Link", "Description", "Pinterest board"]
    max_chunk = 200

    if len(items) <= max_chunk:
        output_files = [("pinterest_pins.csv", items)]
    else:
        output_files = []
        for i in range(0, len(items), max_chunk):
            chunk_num = (i // max_chunk) + 1
            filename = f"pinterest_pins_part{chunk_num}.csv"
            output_files.append((filename, items[i:i + max_chunk]))
        # Also write the full set for reference
        output_files.append(("pinterest_pins_full.csv", items))

    for filename, chunk_items in output_files:
        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(chunk_items)
        print(f"Exported {len(chunk_items)} pins to {filename}")

if __name__ == "__main__":
    export_pinterest_csv()
