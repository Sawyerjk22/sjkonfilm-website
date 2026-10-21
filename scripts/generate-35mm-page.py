#!/usr/bin/env python3
import os
import re

COLOR_VERTICALS = {
    "img_0830.webp",
    "img_3685.webp",
    "img_5824.webp",
    "img_7945 copy.webp",
    "img_5758.webp"
}

def build_35mm_page():
    sources = [
        ("pages/street.html", "bw"),
        ("pages/scenes.html", "bw"),
        ("pages/color.html", "color"),
        ("pages/vertical.html", "mixed")
    ]
    
    collected_imgs = []
    seen_srcs = set()
    color_vertical_tags = []

    for html_file, default_tone in sources:
        if not os.path.exists(html_file):
            print(f"File not found: {html_file}")
            continue
        with open(html_file, "r", encoding="utf-8") as f:
            content = f.read()

        gallery_match = re.search(r'<section class="gallery">(.*?)</section>', content, re.DOTALL)
        if not gallery_match:
            print(f"No gallery in {html_file}")
            continue

        raw_imgs = re.findall(r'<img\s+[^>]+>', gallery_match.group(1))

        for img_tag in raw_imgs:
            src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag)
            src = src_match.group(1) if src_match else ""
            if src in seen_srcs:
                continue
            seen_srcs.add(src)

            filename = os.path.basename(src).lower()

            if default_tone == "mixed":
                if filename in COLOR_VERTICALS:
                    tone = "color"
                    color_vertical_tags.append(img_tag)
                else:
                    tone = "bw"
            else:
                tone = default_tone

            clean_tag = img_tag.strip()
            clean_tag = re.sub(r'\s*data-subcat=["\'][^"\']*["\']', '', clean_tag)
            clean_tag = re.sub(r'\s*data-tone=["\'][^"\']*["\']', '', clean_tag)
            
            enriched_tag = re.sub(r'^<img', f'<img data-tone="{tone}"', clean_tag)

            if len(collected_imgs) >= 4:
                enriched_tag = re.sub(r'\s*fetchpriority=["\'][^"\']*["\']', '', enriched_tag)
                if 'loading=' not in enriched_tag:
                    enriched_tag = enriched_tag[:-1] + ' loading="lazy">'

            collected_imgs.append((tone, enriched_tag))

    bw_count = sum(1 for tone, _ in collected_imgs if tone == "bw")
    color_count = sum(1 for tone, _ in collected_imgs if tone == "color")
    print(f"Collected total {len(collected_imgs)} images: {bw_count} Black & White, {color_count} Color.")
    print(f"Added {len(color_vertical_tags)} vertical color images to Color.")

    # Generate pages/35mm.html
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <link rel="icon" href="/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="/favicon.png">

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>35mm Film Photography | Sawyer Knox</title>
  <meta name="description" content="35mm film photography by Sawyer Knox. Featuring authentic black and white and color analog archives.">
  <link rel="canonical" href="https://sjkonfilm.work/pages/35mm.html">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&family=Playfair+Display:wght@500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css?v=12">

  <!-- Open Graph / Social -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://sjkonfilm.work/pages/35mm.html">
  <meta property="og:title" content="35mm Film Photography | Sawyer Knox">
  <meta property="og:description" content="35mm film photography portfolio: authentic black and white and color archives.">
  <meta property="og:image" content="https://sjkonfilm.work/assets/images/og-main.png">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="35mm Film Photography | Sawyer Knox">
  <meta name="twitter:description" content="35mm film photography portfolio: authentic black and white and color archives.">
  <meta name="twitter:image" content="https://sjkonfilm.work/assets/images/og-main.png">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "CollectionPage",
        "@id": "https://sjkonfilm.work/pages/35mm.html#webpage",
        "url": "https://sjkonfilm.work/pages/35mm.html",
        "name": "35mm Film Photography | Sawyer Knox",
        "description": "35mm film photography collection by Sawyer Knox, featuring black and white and color archives.",
        "publisher": {{ "@id": "https://sjkonfilm.work/#person" }}
      }},
      {{
        "@type": "Person",
        "@id": "https://sjkonfilm.work/#person",
        "name": "Sawyer Knox",
        "jobTitle": "GPS Analyst",
        "worksFor": {{
          "@type": "Organization",
          "name": "Deloitte"
        }},
        "homeLocation": {{
          "@type": "Place",
          "name": "Portland, Oregon"
        }},
        "url": "https://sjkonfilm.work",
        "sameAs": [
          "https://www.instagram.com/sawyer.j.knox",
          "https://github.com/Sawyerjk22",
          "https://www.linkedin.com/in/sawyer-knox",
          "https://www.pinterest.com/sjkonfilm",
          "https://www.flickr.com/photos/sawyerknox",
          "https://unsplash.com/@sawyerknox",
          "https://medium.com/@sawyerknox"
        ]
      }}
    ]
  }}
  </script>
</head>

<body>
  <header>
    <h1 class="site-title">
      <a href="../index.html">Sawyer Knox</a>
    </h1>
    <nav>
      <ul class="nav-links">
        <li class="nav-item has-dropdown">
          <a href="../works.html">Work</a>
          <ul class="dropdown">
            <li><a href="35mm.html">35mm</a></li>
            <li><a href="120.html">120</a></li>
          </ul>
        </li>
        <li><a href="../about.html">About</a></li>
        <li><a href="../contact.html">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <!-- SIMPLE TEXT SUB-NAVIGATION (NO BUBBLES, NO HIGHLIGHTS) -->
    <nav class="subcat-text-nav" aria-label="35mm Subcategories">
      <button type="button" class="text-nav-btn" data-filter="bw">Black & White</button>
      <span class="nav-sep">·</span>
      <button type="button" class="text-nav-btn" data-filter="color">Color</button>
    </nav>

    <section class="gallery" id="filmGallery">
{chr(10).join("      " + tag for _, tag in collected_imgs)}
    </section>
  </main>

  <footer>
    <div class="footer-content">
      <p>© 2026 Sawyer Knox</p>
      <a href="https://www.instagram.com/sawyer.j.knox" target="_blank" rel="me noopener noreferrer">Instagram</a>
    </div>
  </footer>

  <script src="../Lightbox.js?v=11" defer></script>

  <!-- Clean Subcategory Toggle (No bubbles, no highlights) -->
  <script>
    document.addEventListener("DOMContentLoaded", () => {{
      const filterBtns = document.querySelectorAll(".subcat-text-nav .text-nav-btn");
      const gallery = document.getElementById("filmGallery");
      if (!gallery) return;
      const imgs = Array.from(gallery.querySelectorAll("img"));

      const applyFilter = (filterKey) => {{
        imgs.forEach((img) => {{
          const tone = img.dataset.tone || "bw";
          if (filterKey === "all") {{
            img.classList.remove("is-filtered-out");
          }} else if (tone === filterKey) {{
            img.classList.remove("is-filtered-out");
          }} else {{
            img.classList.add("is-filtered-out");
          }}
        }});

        const url = new URL(window.location);
        url.searchParams.set("filter", filterKey);
        window.history.replaceState({{}}, "", url);
      }};

      filterBtns.forEach((btn) => {{
        btn.addEventListener("click", () => {{
          applyFilter(btn.dataset.filter);
        }});
      }});

      const params = new URLSearchParams(window.location.search);
      const initialFilter = params.get("filter") || "bw";
      applyFilter(initialFilter);
    }});
  </script>

  <!-- Instagram Glass Badge -->
  <a href="https://instagram.com/sawyer.j.knox" class="glass-badge" target="_blank" rel="me noopener noreferrer" aria-label="Sawyer Knox Instagram">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <rect x="2" y="2" width="20" height="20" rx="5" ry="5"></rect>
      <path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"></path>
      <line x1="17.5" y1="6.5" x2="17.51" y2="6.5"></line>
    </svg>
  </a>
</body>
</html>
"""
    with open("pages/35mm.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Successfully rebuilt pages/35mm.html!")

if __name__ == "__main__":
    build_35mm_page()
