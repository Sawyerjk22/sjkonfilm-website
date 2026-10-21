#!/usr/bin/env python3
import os
import re

def build_35mm_page():
    # Define sources with their subcategory and tone
    sources = [
        ("pages/street.html", "street", "bw"),
        ("pages/scenes.html", "scenes", "bw"),
        ("pages/color.html", "color", "color"),
        ("pages/vertical.html", "vertical", "mixed")
    ]
    
    collected_imgs = []
    seen_srcs = set()

    for html_file, subcat, default_tone in sources:
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
        print(f"{html_file}: extracted {len(raw_imgs)} images")

        for img_tag in raw_imgs:
            src_match = re.search(r'src=["\']([^"\']+)["\']', img_tag)
            src = src_match.group(1) if src_match else ""
            if src in seen_srcs:
                continue
            seen_srcs.add(src)

            # Determine tone
            tone = default_tone
            if subcat == "vertical":
                # Detect if it's color or bw based on filename or alt
                # If "Color" in alt or specific color files, mark color, else bw
                if "color" in img_tag.lower():
                    tone = "color"
                else:
                    tone = "bw"

            # Clean and enrich img tag
            clean_tag = img_tag.strip()
            # Remove any existing data-subcat or data-tone
            clean_tag = re.sub(r'\s*data-subcat=["\'][^"\']*["\']', '', clean_tag)
            clean_tag = re.sub(r'\s*data-tone=["\'][^"\']*["\']', '', clean_tag)
            
            # Insert data-subcat and data-tone right after <img
            enriched_tag = re.sub(r'^<img', f'<img data-subcat="{subcat}" data-tone="{tone}"', clean_tag)
            
            # Ensure loading="lazy" for all except first 4
            if len(collected_imgs) >= 4:
                enriched_tag = re.sub(r'\s*fetchpriority=["\'][^"\']*["\']', '', enriched_tag)
                if 'loading=' not in enriched_tag:
                    enriched_tag = enriched_tag[:-1] + ' loading="lazy">'

            collected_imgs.append(enriched_tag)

    print(f"Total unique 35mm images collected: {len(collected_imgs)}")

    # Template for 35mm.html
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <link rel="icon" href="/favicon.png" type="image/png">
  <link rel="apple-touch-icon" href="/favicon.png">

  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>35mm Film Photography | Sawyer Knox</title>
  <meta name="description" content="Explore authentic 35mm film photography by Sawyer Knox. Featuring candid street moments, travel scenes, and analog color archives.">
  <link rel="canonical" href="https://sjkonfilm.work/pages/35mm.html">

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;500&family=Playfair+Display:wght@500&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="../style.css?v=11">

  <!-- Open Graph / Social -->
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://sjkonfilm.work/pages/35mm.html">
  <meta property="og:title" content="35mm Film Photography | Sawyer Knox">
  <meta property="og:description" content="Authentic 35mm film photography portfolio: street, architectural scenes, and color archives.">
  <meta property="og:image" content="https://sjkonfilm.work/assets/images/og-main.png">

  <!-- Twitter Cards -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="35mm Film Photography | Sawyer Knox">
  <meta name="twitter:description" content="Authentic 35mm film photography portfolio: street, architectural scenes, and color archives.">
  <meta name="twitter:image" content="https://sjkonfilm.work/assets/images/og-main.png">

  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@graph": [
      {{
        "@type": "CollectionPage",
        "@id": "https://sjkonfilm.work/pages/35mm.html#webpage",
        "url": "https://sjkonfilm.work/pages/35mm.html",
        "name": "35mm Film Photography Archive | Sawyer Knox",
        "description": "Complete 35mm film photography collection by Sawyer Knox, featuring black and white street scenes, travel, and color archives.",
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
          <a href="../works.html" class="active">Work</a>
          <ul class="dropdown">
            <li><a href="../works.html">Overview</a></li>
            <li class="dropdown-divider"></li>
            <li><a href="35mm.html"><strong>35mm Film</strong></a></li>
            <li class="dropdown-sub"><a href="35mm.html?filter=bw">35mm Black & White</a></li>
            <li class="dropdown-sub"><a href="35mm.html?filter=color">35mm Color</a></li>
            <li class="dropdown-divider"></li>
            <li><a href="120.html"><strong>120 Medium Format</strong></a></li>
          </ul>
        </li>
        <li><a href="../about.html">About</a></li>
        <li><a href="../contact.html">Contact</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <!-- CATEGORY SUB-NAVIGATION & FILTER BAR -->
    <nav class="category-subnav" aria-label="Film Category Filters">
      <div class="format-switch">
        <a href="35mm.html" class="format-pill active" aria-current="page">35mm Film</a>
        <a href="120.html" class="format-pill">120 Medium Format</a>
      </div>

      <div class="filter-pills" id="filterPills" role="toolbar" aria-label="35mm Subcategories">
        <button class="filter-btn active" data-filter="all" aria-pressed="true">All 35mm</button>
        <button class="filter-btn" data-filter="bw" aria-pressed="false">Black & White</button>
        <button class="filter-btn" data-filter="color" aria-pressed="false">Color</button>
        <button class="filter-btn" data-filter="street" aria-pressed="false">Street</button>
        <button class="filter-btn" data-filter="scenes" aria-pressed="false">Scenes</button>
        <button class="filter-btn" data-filter="vertical" aria-pressed="false">Vertical</button>
      </div>
    </nav>

    <div class="gallery-status-bar" id="galleryStatusBar" aria-live="polite">
      Showing all {len(collected_imgs)} 35mm photographs
    </div>

    <section class="gallery" id="filmGallery">
      {chr(10).join("      " + img for img in collected_imgs)}
    </section>
  </main>

  <footer>
    <div class="footer-content">
      <p>© 2026 Sawyer Knox</p>
      <a href="https://www.instagram.com/sawyer.j.knox" target="_blank" rel="me noopener noreferrer">Instagram</a>
    </div>
  </footer>

  <script src="../Lightbox.js?v=11" defer></script>

  <!-- Client-Side Gallery Subcategory Filter Script -->
  <script>
    document.addEventListener("DOMContentLoaded", () => {{
      const filterBtns = document.querySelectorAll("#filterPills .filter-btn");
      const gallery = document.getElementById("filmGallery");
      const imgs = Array.from(gallery.querySelectorAll("img"));
      const statusBar = document.getElementById("galleryStatusBar");

      const applyFilter = (filterKey) => {{
        let visibleCount = 0;

        imgs.forEach((img) => {{
          const subcat = img.dataset.subcat || "";
          const tone = img.dataset.tone || "";

          let match = false;
          if (filterKey === "all") {{
            match = true;
          }} else if (filterKey === "bw") {{
            match = (tone === "bw");
          }} else if (filterKey === "color") {{
            match = (tone === "color");
          }} else if (filterKey === "street") {{
            match = (subcat === "street");
          }} else if (filterKey === "scenes") {{
            match = (subcat === "scenes");
          }} else if (filterKey === "vertical") {{
            match = (subcat === "vertical");
          }}

          if (match) {{
            img.classList.remove("is-filtered-out");
            visibleCount++;
          }} else {{
            img.classList.add("is-filtered-out");
          }}
        }});

        // Update Buttons
        filterBtns.forEach((btn) => {{
          const isActive = btn.dataset.filter === filterKey;
          btn.classList.toggle("active", isActive);
          btn.setAttribute("aria-pressed", isActive ? "true" : "false");
        }});

        // Update Status Bar
        const labels = {{
          all: "all " + visibleCount + " 35mm photographs",
          bw: visibleCount + " Black & White 35mm photographs",
          color: visibleCount + " Color 35mm photographs",
          street: visibleCount + " 35mm street photographs",
          scenes: visibleCount + " 35mm architectural & landscape scenes",
          vertical: visibleCount + " vertical 35mm frames"
        }};
        if (statusBar) {{
          statusBar.textContent = "Showing " + (labels[filterKey] || visibleCount + " photographs");
        }}

        // Update URL query param quietly
        const url = new URL(window.location);
        if (filterKey === "all") {{
          url.searchParams.delete("filter");
        }} else {{
          url.searchParams.set("filter", filterKey);
        }}
        window.history.replaceState({{}}, "", url);
      }};

      // Attach button clicks
      filterBtns.forEach((btn) => {{
        btn.addEventListener("click", () => {{
          applyFilter(btn.dataset.filter);
        }});
      }});

      // Read initial filter from URL params if present
      const params = new URLSearchParams(window.location.search);
      const initialFilter = params.get("filter") || "all";
      if (initialFilter && initialFilter !== "all") {{
        applyFilter(initialFilter);
      }}
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
    print("Successfully built pages/35mm.html!")

if __name__ == "__main__":
    build_35mm_page()
