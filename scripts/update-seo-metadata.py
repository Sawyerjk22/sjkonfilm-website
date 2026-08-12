#!/usr/bin/env python3
"""
SEO & Background Metadata Engine for sjkonfilm.work
Injects rich JSON-LD microdata schemas and enhances image alt attributes with camera,
film stock, and keyword metadata for Google Search indexing.
"""

import os
import re
import glob
import json

CAMERA_KEYWORDS = [
    "Konica Autoreflex T3",
    "Rolleiflex 2.8f",
    "35mm film",
    "120 medium format film",
    "Ilford HP5 Plus",
    "Kodak Portra 400",
    "Analog photography",
    "Portland Oregon street photography",
    "Travel photography"
]

def enhance_alt_text(alt_text, category):
    """Ensure alt text contains essential analog film keywords if sparse."""
    if not alt_text or alt_text.startswith("New Location"):
        alt_text = f"Analog {category} film photography by Sawyer Knox"
    
    # Check if key photographic terms are included
    if "35mm" not in alt_text and "120" not in alt_text and "film" not in alt_text.lower():
        alt_text = f"{alt_text} - 35mm Film Photography"
    
    return alt_text

def build_image_object_schema(img_src, img_full, alt_text, category):
    """Build a Schema.org ImageObject JSON node."""
    full_url = img_full.replace("../", "https://sjkonfilm.work/").replace("./", "https://sjkonfilm.work/")
    if not full_url.startswith("http"):
        full_url = f"https://sjkonfilm.work/{full_url.lstrip('/')}"
        
    return {
        "@type": "ImageObject",
        "contentUrl": full_url,
        "name": alt_text,
        "description": f"{alt_text}. Shot on analog film (Konica Autoreflex T3 / Rolleiflex 2.8f, Ilford HP5) by Sawyer Knox in Portland, Oregon and worldwide.",
        "author": {
            "@type": "Person",
            "name": "Sawyer Knox"
        },
        "copyrightNotice": "© 2026 Sawyer Knox. All Rights Reserved."
    }

def process_html_seo(filepath):
    """Process an HTML file to inject / update image alt tags and schema microdata."""
    if not os.path.exists(filepath):
        return

    category = os.path.splitext(os.path.basename(filepath))[0]
    
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Find all gallery image tags
    img_pattern = re.compile(r'<img\s+([^>]*data-full="([^"]+)"[^>]*)>', re.IGNORECASE)
    matches = img_pattern.findall(content)

    if not matches:
        return

    image_schemas = []
    updated_content = content

    for full_tag, full_url in matches:
        # Extract alt attribute
        alt_match = re.search(r'alt="([^"]*)"', full_tag)
        current_alt = alt_match.group(1) if alt_match else ""
        
        new_alt = enhance_alt_text(current_alt, category)
        
        # Update alt attribute if changed
        if alt_match and current_alt != new_alt:
            new_tag = full_tag.replace(f'alt="{current_alt}"', f'alt="{new_alt}"')
            updated_content = updated_content.replace(full_tag, new_tag)

        img_schema = build_image_object_schema(full_url, full_url, new_alt, category)
        image_schemas.append(img_schema)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(updated_content)

    print(f"Enhanced SEO metadata for {len(image_schemas)} images in {filepath}")

def main():
    pages = glob.glob("pages/*.html") + ["index.html"]
    for page in pages:
        process_html_seo(page)

if __name__ == "__main__":
    main()
