#!/usr/bin/env python3
import os
import glob
import subprocess

def convert_backlog():
    assets_dir = os.path.join("assets", "images")
    if not os.path.exists(assets_dir):
        print("Assets directory not found.")
        return

    pattern = os.path.join(assets_dir, "**", "*.webp")
    webp_files = glob.glob(pattern, recursive=True)

    print(f"Found {len(webp_files)} WebP file(s) across asset directories.")
    converted_count = 0

    for webp_path in webp_files:
        avif_path = os.path.splitext(webp_path)[0] + ".avif"
        if os.path.exists(avif_path):
            continue

        print(f"Converting -> {avif_path}")
        cmd = ["magick", webp_path, "-quality", "80", avif_path]
        try:
            subprocess.run(cmd, check=True)
            converted_count += 1
        except Exception as e:
            print(f"Error converting {webp_path}: {e}")

    print(f"\nAVIF Backlog Conversion Complete. Converted {converted_count} new file(s).")

if __name__ == "__main__":
    convert_backlog()
