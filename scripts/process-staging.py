#!/usr/bin/env python3
import os
import sys
import re
import glob
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

# Category Mapping to target HTML files and asset paths
CATEGORY_MAP = {
    "color": {
        "staging_dir": os.path.join("Staging", "35mm", "color"),
        "html_file": os.path.join("pages", "color.html"),
        "asset_dir": os.path.join("assets", "images", "color"),
        "html_prefix": "../assets",
        "default_alt": "Color 35mm Film Photography - Sawyer Knox",
        "default_dims": (900, 597)
    },
    "street": {
        "staging_dir": os.path.join("Staging", "35mm", "street"),
        "html_file": os.path.join("pages", "street.html"),
        "asset_dir": os.path.join("assets", "images", "street"),
        "html_prefix": "../assets",
        "default_alt": "Candid 35mm Street Photography - Sawyer Knox",
        "default_dims": (900, 597)
    },
    "scenes": {
        "staging_dir": os.path.join("Staging", "35mm", "scenes"),
        "html_file": os.path.join("pages", "scenes.html"),
        "asset_dir": os.path.join("assets", "images", "scenes"),
        "html_prefix": "../assets",
        "default_alt": "Analog Landscape and Scene Photography - Sawyer Knox",
        "default_dims": (900, 597)
    },
    "vertical": {
        "staging_dir": os.path.join("Staging", "35mm", "vertical"),
        "html_file": os.path.join("pages", "vertical.html"),
        "asset_dir": os.path.join("assets", "images", "vertical"),
        "html_prefix": "../assets",
        "default_alt": "Vertical 35mm Film Portrait - Sawyer Knox",
        "default_dims": (597, 900)
    },
    "120": {
        "staging_dir": os.path.join("Staging", "120"),
        "html_file": os.path.join("pages", "120.html"),
        "asset_dir": os.path.join("assets", "images", "120"),
        "html_prefix": "../assets",
        "default_alt": "Rolleiflex 120 Medium Format Film Photography - Sawyer Knox",
        "default_dims": (900, 900)
    }
}

def slugify(text):
    """Convert filename or text into clean SEO slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    text = text.strip('-')
    return text

def get_image_info(filepath):
    """Get dimensions (width, height) using ImageMagick identify."""
    try:
        cmd = ["magick", "identify", "-format", "%w %h", filepath]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        w, h = map(int, res.stdout.strip().split())
        return w, h
    except Exception as e:
        print(f"Warning: could not get dimensions for {filepath}: {e}")
        return 900, 597

def process_image(src_path, cat, cat_info, dry_run=False):
    """Process a single staged image file."""
    fname = os.path.basename(src_path)
    base_name, ext = os.path.splitext(fname)

    # Standardize slug name for SEO
    if base_name.lower().startswith("scan") or base_name.lower().startswith("img_"):
        slug_base = f"analog-{cat}-film-photography-{slugify(base_name)}"
    else:
        slug_base = slugify(base_name)

    slug_fname = f"{slug_base}.webp"

    full_dir = os.path.join(cat_info["asset_dir"], "full")
    thumbs_dir = os.path.join(cat_info["asset_dir"], "thumbs")

    os.makedirs(full_dir, exist_ok=True)
    os.makedirs(thumbs_dir, exist_ok=True)

    dest_full = os.path.join(full_dir, slug_fname)
    dest_thumb_900 = os.path.join(thumbs_dir, slug_fname)
    dest_thumb_400 = os.path.join(thumbs_dir, f"{slug_base}-400w.webp")

    print(f"\nProcessing [{cat}] {fname} -> {slug_fname}...")

    # Get input dimensions
    orig_w, orig_h = get_image_info(src_path)
    is_vertical = orig_h > orig_w
    is_square = abs(orig_w - orig_h) < 50

    if is_square:
        w_out, h_out = 900, 900
    elif is_vertical:
        w_out, h_out = 597, 900
    else:
        w_out, h_out = 900, 597

    if not dry_run:
        # 1. Convert to high-quality Full WebP (Max dimension 1800 for lightbox sharpness)
        subprocess.run(["magick", src_path, "-resize", "1800x1800>", "-quality", "88", dest_full], check=True)

        # 2. Convert to 900w Thumbnail WebP
        subprocess.run(["magick", src_path, "-resize", f"{w_out}x{h_out}", "-quality", "85", dest_thumb_900], check=True)

        # 3. Convert to 400w Mobile Thumbnail WebP
        w_400 = 400 if not is_vertical else int(400 * (597 / 900))
        h_400 = int(400 * (597 / 900)) if not is_vertical else 400
        if is_square:
            w_400, h_400 = 400, 400
        subprocess.run(["magick", src_path, "-resize", f"{w_400}x{h_400}", "-quality", "82", dest_thumb_400], check=True)

    prefix = cat_info["html_prefix"]
    img_src = f"{prefix}/images/{cat}/thumbs/{slug_fname}"
    img_srcset = f"{prefix}/images/{cat}/thumbs/{slug_base}-400w.webp 400w, {prefix}/images/{cat}/thumbs/{slug_fname} 900w"
    img_full = f"{prefix}/images/{cat}/full/{slug_fname}"

    alt_text = f"{cat_info['default_alt']} - {base_name.replace('-', ' ').title()}"

    html_tag = (
        f'      <img src="{img_src}" srcset="{img_srcset}" sizes="(max-width: 768px) 100vw, 33vw" '
        f'data-full="{img_full}" alt="{alt_text}" width="{w_out}" height="{h_out}" loading="lazy" decoding="async">'
    )

    # Insert into target HTML if exists
    html_file = cat_info["html_file"]
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        if slug_fname not in content:
            gallery_sec = '<section class="gallery">'
            if gallery_sec in content and not dry_run:
                updated_content = content.replace(gallery_sec, f"{gallery_sec}\n{html_tag}")
                with open(html_file, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                print(f"  [HTML Updated] Appended image node to {html_file}")
            else:
                print(f"  [Generated Tag] {html_tag}")
        else:
            print(f"  [Skipped] Image {slug_fname} already present in {html_file}")

    # Move raw source to Staging/processed/
    processed_dir = os.path.join("Staging", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    if not dry_run:
        dest_proc = os.path.join(processed_dir, fname)
        if os.path.exists(dest_proc):
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest_proc = os.path.join(processed_dir, f"{base_name}_{timestamp}{ext}")
        os.rename(src_path, dest_proc)
        print(f"  [Staging Cleaned] Moved raw file to {dest_proc}")

def main():
    parser = argparse.ArgumentParser(description="Process staged gallery images.")
    parser.add_argument("--dry-run", action="store_true", help="Perform dry run without writing files.")
    args = parser.parse_args()

    total_processed = 0
    for cat, info in CATEGORY_MAP.items():
        staged_dir = info["staging_dir"]
        if not os.path.exists(staged_dir):
            continue

        valid_exts = ("*.jpg", "*.jpeg", "*.webp", "*.png", "*.JPG", "*.JPEG", "*.WEBP", "*.PNG")
        files = []
        for ext in valid_exts:
            files.extend(glob.glob(os.path.join(staged_dir, ext)))

        for filepath in files:
            process_image(filepath, cat, info, dry_run=args.dry_run)
            total_processed += 1

    if total_processed == 0:
        print("No staged images found in Staging subdirectories.")
    else:
        print(f"\nSuccessfully processed {total_processed} staged image(s).")
        print("\n--- Triggering Post-Processing Automations ---")
        subprocess.run([sys.executable, "scripts/generate-rss.py"], check=False)
        subprocess.run([sys.executable, "scripts/syndicate-posts.py"], check=False)


if __name__ == "__main__":
    main()
