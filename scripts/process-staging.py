#!/usr/bin/env python3
import os
import sys
import re
import glob
import subprocess
import argparse
from datetime import datetime
from pathlib import Path

# Category Mapping to target HTML files and asset paths
CATEGORY_MAP = {
    "bw": {
        "staging_dir": os.path.join("Staging", "35mm", "bw"),
        "html_file": os.path.join("pages", "35mm.html"),
        "asset_dir": os.path.join("assets", "images", "street"),
        "html_prefix": "../assets",
        "format_label": "35mm Film Photography",
        "default_dims": (900, 597)
    },
    "color": {
        "staging_dir": os.path.join("Staging", "35mm", "color"),
        "html_file": os.path.join("pages", "color.html"),
        "asset_dir": os.path.join("assets", "images", "color"),
        "html_prefix": "../assets",
        "format_label": "35mm Film Photography",
        "default_dims": (900, 597)
    },
    "120": {
        "staging_dir": os.path.join("Staging", "120"),
        "html_file": os.path.join("pages", "120.html"),
        "asset_dir": os.path.join("assets", "images", "120"),
        "html_prefix": "../assets",
        "format_label": "120 Medium Format Film Photography",
        "default_dims": (900, 900)
    },
    "street": {
        "staging_dir": os.path.join("Staging", "35mm", "street"),
        "html_file": os.path.join("pages", "35mm.html"),
        "asset_dir": os.path.join("assets", "images", "street"),
        "html_prefix": "../assets",
        "format_label": "35mm Film Photography",
        "default_dims": (900, 597)
    },
    "scenes": {
        "staging_dir": os.path.join("Staging", "35mm", "scenes"),
        "html_file": os.path.join("pages", "35mm.html"),
        "asset_dir": os.path.join("assets", "images", "scenes"),
        "html_prefix": "../assets",
        "format_label": "35mm Film Photography",
        "default_dims": (900, 597)
    },
    "vertical": {
        "staging_dir": os.path.join("Staging", "35mm", "vertical"),
        "html_file": os.path.join("pages", "35mm.html"),
        "asset_dir": os.path.join("assets", "images", "vertical"),
        "html_prefix": "../assets",
        "format_label": "35mm Film Photography",
        "default_dims": (597, 900)
    }
}

def get_auto_season_year():
    """Return a clean factual Season + Year string based on current date."""
    now = datetime.now()
    m = now.month
    y = now.year
    if m in (3, 4, 5):
        season = "Spring"
    elif m in (6, 7):
        season = "Summer"
    elif m == 8:
        season = "Late Summer"
    elif m in (9, 10, 11):
        season = "Autumn"
    else:
        season = "Winter"
    return f"{season} {y}"

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

def process_image(src_path, cat, cat_info, date_override=None, dry_run=False):
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
    unsplash_dir = os.path.join("Staging", "processed", "unsplash-ready")

    os.makedirs(full_dir, exist_ok=True)
    os.makedirs(thumbs_dir, exist_ok=True)
    os.makedirs(unsplash_dir, exist_ok=True)

    dest_full = os.path.join(full_dir, slug_fname)
    dest_thumb_900 = os.path.join(thumbs_dir, slug_fname)
    dest_thumb_400 = os.path.join(thumbs_dir, f"{slug_base}-400w.webp")
    dest_unsplash_jpg = os.path.join(unsplash_dir, f"{slug_base}.jpg")

    print(f"\nProcessing [{cat}] {fname} -> {slug_fname}...")

    # Get input dimensions
    orig_w, orig_h = get_image_info(src_path)
    is_vertical = orig_h > orig_w
    is_square = (cat == "120") or (abs(orig_w - orig_h) < 50) or (abs(orig_w - orig_h) / max(orig_w, orig_h, 1) < 0.08)

    if is_square:
        w_out, h_out = 900, 900
    elif is_vertical:
        w_out, h_out = 597, 900
    else:
        w_out, h_out = 900, 597

    dest_full_avif = os.path.join(full_dir, f"{slug_base}.avif")
    dest_thumb_900_avif = os.path.join(thumbs_dir, f"{slug_base}.avif")
    dest_thumb_400_avif = os.path.join(thumbs_dir, f"{slug_base}-400w.avif")

    # Determine clean factual date label (from --date, subfolder name, or auto season/year)
    parent_folder = os.path.basename(os.path.dirname(src_path))
    staged_root_name = os.path.basename(cat_info["staging_dir"])
    if date_override:
        date_label = date_override.strip()
    elif parent_folder and parent_folder != staged_root_name:
        date_label = parent_folder.strip()
    else:
        date_label = get_auto_season_year()

    format_label = cat_info["format_label"]
    alt_text = f"{date_label} - {format_label}"

    if not dry_run:
        meta_flags = [
            "-set", "artist", "Sawyer Knox",
            "-set", "copyright", "© Sawyer Knox (https://sjkonfilm.work)",
            "-set", "comment", f"{alt_text} by Sawyer Knox. Instagram: @sawyer.j.knox | Portfolio: https://sjkonfilm.work"
        ]

        # 1. Convert to high-quality Full WebP & AVIF
        subprocess.run(["magick", src_path] + meta_flags + ["-resize", "1800x1800>", "-quality", "88", dest_full], check=True)
        subprocess.run(["magick", src_path] + meta_flags + ["-resize", "1800x1800>", "-quality", "82", dest_full_avif], check=True)

        # 2. Convert to 900w Thumbnail WebP & AVIF
        subprocess.run(["magick", src_path] + meta_flags + ["-resize", f"{w_out}x{h_out}", "-quality", "85", dest_thumb_900], check=True)
        subprocess.run(["magick", src_path] + meta_flags + ["-resize", f"{w_out}x{h_out}", "-quality", "78", dest_thumb_900_avif], check=True)

        # 3. Convert to 400w Mobile Thumbnail WebP & AVIF
        w_400 = 400 if not is_vertical else int(400 * (597 / 900))
        h_400 = int(400 * (597 / 900)) if not is_vertical else 400
        if is_square:
            w_400, h_400 = 400, 400
        subprocess.run(["magick", src_path] + meta_flags + ["-resize", f"{w_400}x{h_400}", "-quality", "82", dest_thumb_400], check=True)
        subprocess.run(["magick", src_path] + meta_flags + ["-resize", f"{w_400}x{h_400}", "-quality", "75", dest_thumb_400_avif], check=True)

        # 4. Save EXIF/IPTC-stamped high-res JPEG into Staging/processed/unsplash-ready/ for Unsplash & IG
        subprocess.run(["magick", src_path] + meta_flags + ["-quality", "95", dest_unsplash_jpg], check=True)
        captions_file = os.path.join(unsplash_dir, "captions.txt")
        film_tag = "120 medium format film" if cat == "120" else "35mm film"
        with open(captions_file, "a", encoding="utf-8") as cf:
            cf.write(
                f"{slug_base}.jpg\n"
                f"  Caption: Shot on {film_tag} ({date_label}) by Sawyer Knox. Instagram: @sawyer.j.knox | Portfolio: https://sjkonfilm.work\n"
                f"  Tags: {film_tag}, analog photography, film photography, film grain, black and white, sawyer knox\n\n"
            )
        print(f"  [Unsplash/IG Ready] Saved metadata-stamped JPEG -> {dest_unsplash_jpg}")

    prefix = cat_info["html_prefix"]
    asset_sub = os.path.basename(cat_info["asset_dir"])
    img_src = f"{prefix}/images/{asset_sub}/thumbs/{slug_fname}"
    img_srcset = f"{prefix}/images/{asset_sub}/thumbs/{slug_base}-400w.webp 400w, {prefix}/images/{asset_sub}/thumbs/{slug_fname} 900w"
    img_full = f"{prefix}/images/{asset_sub}/full/{slug_fname}"

    tone_attr = ""
    if cat in ("bw", "street", "scenes", "vertical"):
        tone_attr = 'data-tone="bw" '
    elif cat == "color":
        tone_attr = 'data-tone="color" '

    html_tag = (
        f'      <img {tone_attr}src="{img_src}" srcset="{img_srcset}" sizes="(max-width: 768px) 100vw, 33vw" '
        f'data-full="{img_full}" alt="{alt_text}" width="{w_out}" height="{h_out}" loading="lazy" decoding="async">'
    )

    # Insert into target HTML if exists (horizontal at top, vertical in bottom vertical section)
    def insert_gallery_node(html_content, node_tag, vertical_flag):
        if vertical_flag:
            first_vert = re.search(r'(\n[ \t]*<img\b[^>]*\bwidth="597"\s+height="900"[^>]*>)', html_content)
            if first_vert:
                target_vert = first_vert.group(1)
                return html_content.replace(target_vert, f"\n{node_tag}{target_vert}", 1)
            sec_close = re.search(r'(\n[ \t]*</section>)', html_content)
            if sec_close:
                target_close = sec_close.group(1)
                return html_content.replace(target_close, f"\n{node_tag}{target_close}", 1)
        gallery_match = re.search(r'(<section class="gallery[^"]*"[^>]*>)', html_content)
        if gallery_match:
            target_open = gallery_match.group(1)
            return html_content.replace(target_open, f"{target_open}\n{node_tag}", 1)
        return html_content

    html_file = cat_info["html_file"]
    if os.path.exists(html_file):
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        if slug_fname not in content:
            if not dry_run:
                updated_content = insert_gallery_node(content, html_tag, is_vertical and cat != "120")
                with open(html_file, "w", encoding="utf-8") as f:
                    f.write(updated_content)
                pos_note = "vertical bottom section" if (is_vertical and cat != "120") else "horizontal top section"
                print(f"  [HTML Updated] Appended image node to {html_file} ({pos_note})")
            else:
                print(f"  [Generated Tag] {html_tag}")
        else:
            print(f"  [Skipped] Image {slug_fname} already present in {html_file}")

    # If this is a 35mm category whose primary html_file wasn't pages/35mm.html (e.g. color), also append to pages/35mm.html
    if cat in ("color", "street", "scenes", "vertical"):
        hub_35mm = os.path.join("pages", "35mm.html")
        if os.path.exists(hub_35mm) and not dry_run:
            with open(hub_35mm, "r", encoding="utf-8") as f:
                hub_content = f.read()
            if slug_fname not in hub_content:
                tone = "color" if cat == "color" else "bw"
                hub_tag = (
                    f'      <img data-subcat="{cat}" data-tone="{tone}" src="{img_src}" srcset="{img_srcset}" '
                    f'sizes="(max-width: 768px) 100vw, 33vw" data-full="{img_full}" alt="{alt_text}" '
                    f'width="{w_out}" height="{h_out}" loading="lazy" decoding="async">'
                )
                updated_hub = insert_gallery_node(hub_content, hub_tag, is_vertical)
                with open(hub_35mm, "w", encoding="utf-8") as f:
                    f.write(updated_hub)
                print(f"  [Hub Updated] Appended image node to {hub_35mm}")

    # Delete staging file after processing
    if not dry_run:
        try:
            os.remove(src_path)
            print(f"  [Staging Cleaned] Deleted staging file: {src_path}")
        except OSError as e:
            print(f"  [Warning] Could not delete staging file {src_path}: {e}")
    else:
        print(f"  [Dry Run] Would delete staging file: {src_path}")

def main():
    parser = argparse.ArgumentParser(description="Process staged gallery images.")
    parser.add_argument("--dry-run", action="store_true", help="Perform dry run without writing files.")
    parser.add_argument("--date", type=str, default=None, help="Optional factual date label (e.g. 'Late Summer 2026').")
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
            files.extend(glob.glob(os.path.join(staged_dir, "*", ext)))

        for filepath in sorted(set(files)):
            process_image(filepath, cat, info, date_override=args.date, dry_run=args.dry_run)
            total_processed += 1

    if total_processed == 0:
        print("No staged images found in Staging subdirectories.")
    else:
        print(f"\nSuccessfully processed {total_processed} staged image(s).")
        print("\n--- Triggering Post-Processing Automations ---")
        subprocess.run([sys.executable, "scripts/generate-rss.py"], check=False)
        subprocess.run([sys.executable, "scripts/export-pinterest-csv.py"], check=False)
        subprocess.run([sys.executable, "scripts/syndicate-posts.py"], check=False)


if __name__ == "__main__":
    main()
