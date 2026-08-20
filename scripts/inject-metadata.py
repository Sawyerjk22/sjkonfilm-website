#!/usr/bin/env python3
"""
Backfill EXIF/IPTC Metadata Script for sjkonfilm.work
Stamps all images in assets/images/ with artist, copyright, portfolio URL, and Instagram handle using ImageMagick.
"""

import os
import glob
import subprocess

META_FLAGS = [
    "-set", "artist", "Sawyer Knox",
    "-set", "copyright", "© Sawyer Knox (https://sjkonfilm.work)",
    "-set", "comment", "35mm/120 film photography by Sawyer Knox. Instagram: @sawyer.j.knox | Portfolio: https://sjkonfilm.work"
]

def backfill_metadata():
    image_paths = glob.glob("assets/images/**/*.*", recursive=True)
    valid_exts = (".webp", ".avif", ".jpg", ".png")
    
    target_files = [p for p in image_paths if p.lower().endswith(valid_exts)]
    print(f"Found {len(target_files)} image assets to process for metadata backfill.")
    
    success_count = 0
    for path in target_files:
        try:
            cmd = ["magick", path] + META_FLAGS + [path]
            subprocess.run(cmd, check=True)
            success_count += 1
        except Exception as e:
            print(f"Failed to process {path}: {e}")

    print(f"\nMetadata backfill complete. Successfully updated {success_count}/{len(target_files)} image files.")

if __name__ == "__main__":
    backfill_metadata()
