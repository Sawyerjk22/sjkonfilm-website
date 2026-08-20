#!/usr/bin/env python3
import os
import subprocess

# OpenGraph card targets
OG_CONFIG = [
    {
        "output": os.path.join("assets", "images", "og-main.png"),
        "hero_img": os.path.join("assets", "images", "featured", "thumbs", "img_3461.webp"),
        "title": "SAWYER KNOX",
        "subtitle": "35mm & 120 Film Photography | Portland, OR"
    },
    {
        "output": os.path.join("assets", "images", "og-street.png"),
        "hero_img": os.path.join("assets", "images", "street", "thumbs", "img_0491a.webp"),
        "title": "STREET PHOTOGRAPHY",
        "subtitle": "35mm Black & White Street Portfolio | Sawyer Knox"
    },
    {
        "output": os.path.join("assets", "images", "og-scenes.png"),
        "hero_img": os.path.join("assets", "images", "scenes", "thumbs", "img_0538.webp"),
        "title": "ANALOG SCENES",
        "subtitle": "Landscape & Travel Film Photography | Sawyer Knox"
    },
    {
        "output": os.path.join("assets", "images", "og-color.png"),
        "hero_img": os.path.join("assets", "images", "color", "thumbs", "train123.webp"),
        "title": "COLOR FILM",
        "subtitle": "35mm Color Film Portfolio | Sawyer Knox"
    },
    {
        "output": os.path.join("assets", "images", "og-vertical.png"),
        "hero_img": os.path.join("assets", "images", "vertical", "thumbs", "img_2628.webp"),
        "title": "VERTICAL PORTRAITS",
        "subtitle": "Vertical 35mm Analog Frames | Sawyer Knox"
    }
]

def generate_og_card(cfg):
    out_path = cfg["output"]
    hero = cfg["hero_img"]
    title = cfg["title"]
    subtitle = cfg["subtitle"]

    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    if os.path.exists(hero):
        # Composite hero image resized inside 1200x630 dark canvas
        cmd = [
            "magick",
            "-size", "1200x630", "xc:#0e0d0c",
            "(", hero, "-resize", "800x550>", "-bordercolor", "#1a1918", "-border", "1", ")",
            "-gravity", "center", "-composite",
            "-font", "Georgia", "-fill", "#ffffff", "-pointsize", "42",
            "-gravity", "south", "-geometry", "+0+60",
            "-annotate", "+0+0", title,
            "-fill", "#a09d98", "-pointsize", "22",
            "-annotate", "+0-30", subtitle,
            out_path
        ]
    else:
        # Fallback text card
        cmd = [
            "magick",
            "-size", "1200x630", "xc:#0e0d0c",
            "-font", "Georgia", "-fill", "#ffffff", "-pointsize", "52",
            "-gravity", "center", "-annotate", "+0-20", title,
            "-fill", "#a09d98", "-pointsize", "24",
            "-annotate", "+0+40", subtitle,
            out_path
        ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Generated OG Preview Card -> {out_path}")
    except Exception as e:
        print(f"Failed to generate {out_path}: {e}")

def main():
    print("Generating 1200x630 OpenGraph Social Preview Cards...")
    for cfg in OG_CONFIG:
        generate_og_card(cfg)
    print("OpenGraph Card Generation Complete.")

if __name__ == "__main__":
    main()
