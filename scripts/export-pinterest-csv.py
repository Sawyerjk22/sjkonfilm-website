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

            title = alt_text if alt_text and not alt_text.startswith("New Location") else f"{cat.title()} Film Photography"
            desc = f"{title}. Shot on analog 35mm / 120 film by Sawyer Knox in Portland, Oregon. Explore more film photography at sjkonfilm.work."

            items.append({
                "Title": title,
                "Media URL": media_url,
                "Destination Link": dest_link,
                "Description": desc,
                "Board Name": board_name
            })

    output_csv = "pinterest_pins.csv"
    fieldnames = ["Title", "Media URL", "Destination Link", "Description", "Board Name"]

    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(items)

    print(f"Exported {len(items)} pins to {output_csv}")

if __name__ == "__main__":
    export_pinterest_csv()
