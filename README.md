# sjkonfilm.work

The official digital portfolio and photography archive of **Sawyer Knox**—a Deloitte GPS Analyst and analog film photographer based in Portland, Oregon.

- **Live Site:** [https://sjkonfilm.work](https://sjkonfilm.work)
- **Instagram:** [@sawyer.j.knox](https://www.instagram.com/sawyer.j.knox)
- **Film Formats:** 35mm and 120 (6×6 square medium format)

---

## Architecture & Tech Stack

- **Static Architecture:** Pure vanilla HTML5, CSS3, and lightweight vanilla JavaScript. Zero frameworks, zero dependencies, lightning-fast Core Web Vitals.
- **Hosting & CI/CD:** Hosted via GitHub Pages, custom domain routed through Porkbun DNS.
- **Decoupled Asset Engine:** Responsive WebP and AVIF images organized into `/assets/images/` with dual-tier storage (`full/` for modals, `thumbs/` for responsive gallery grids with `400w` and `900w` `srcset`).
- **Automated Social & Search Ecosystem:**
  - Automated RSS feed (`rss.xml`) connected to Pinterest auto-pinning.
  - Automated monthly ecosystem health digest & call finder via GitHub Actions (`.github/workflows/monthly-digest.yml`).
  - Search engine pings (Google Sitemap & IndexNow).
  - Rich Schema.org JSON-LD entity graph linking LinkedIn, Instagram, and verified creator profiles.

---

## Repository Structure

```text
├── index.html                 # Hero home landing page
├── works.html                 # Selected Works (35mm and 120 collection cards)
├── about.html                 # Biography, artist statement, and gear overview
├── contact.html               # Inquiries & licensing contact form
├── Lightbox.js                # Vanilla JS image modal viewer & touch swipe
├── style.css                  # Unified minimalist stylesheet & typography
│
├── pages/                     # Gallery pages
│   ├── 35mm.html              # Unified 35mm hub (Black & White + Color toggle)
│   ├── 120.html               # 120 Medium Format 6x6 square gallery
│   ├── color.html             # Legacy subpage / SEO anchor
│   ├── street.html            # Legacy subpage / SEO anchor
│   ├── scenes.html            # Legacy subpage / SEO anchor
│   └── vertical.html          # Legacy subpage / SEO anchor
│
├── assets/                    # Static assets
│   ├── icons/                 # Social and UI icons
│   └── images/                # Optimized WebP and AVIF images
│       ├── 120/               # (full / thumbs)
│       ├── color/             # (full / thumbs)
│       ├── street/            # (full / thumbs)
│       ├── scenes/            # (full / thumbs)
│       └── vertical/          # (full / thumbs)
│
├── Staging/                   # Drop folders for new photo scans
│   ├── 35mm/bw/               # Drop new 35mm B&W scans here
│   ├── 35mm/color/            # Drop new 35mm color scans here
│   └── 120/                   # Drop new 120 square scans here
│
├── scripts/                   # Automation & deployment tools (Python 3)
│   ├── process-staging.py     # Main image processing & HTML injection pipeline
│   ├── generate-rss.py        # RSS 2.0 / Media RSS feed generator for Pinterest
│   ├── export-pinterest-csv.py# Pinterest bulk CSV backfill exporter
│   ├── syndicate-posts.py     # Multi-platform post syndication (Flickr, Medium)
│   ├── opportunity-finder.py  # Film photography calls for entry scraper
│   ├── send-monthly-digest.py # Monthly email summary reporter
│   └── ping-search-engines.py # Google & IndexNow ping tool
│
├── .agents/                   # Antigravity agent configuration & workflows
│   ├── rules/                 # Workspace rules (project-context.md)
│   └── workflows/             # Slash command and step-by-step workflows
│
├── AGENTS.md                  # Comprehensive AI context, guidelines, and history
└── GEMINI.md                  # Synced Antigravity workspace instructions
```

---

## macOS Quickstart

### 1. Clone the Repository
```bash
git clone https://github.com/Sawyerjk22/sjkonfilm-website.git
cd sjkonfilm-website
```

### 2. Install ImageMagick (Homebrew)
The staging image pipeline (`scripts/process-staging.py`) requires ImageMagick to resize scans and embed IPTC/EXIF metadata:
```bash
brew install imagemagick
```

### 3. Local Development
Preview the site locally:
```bash
python3 -m http.server 8000
```
Then navigate to `http://localhost:8000` in your browser.

---

## Publishing New Photographs

1. **Drop scans** into the designated staging folder:
   - `Staging/35mm/bw/`
   - `Staging/35mm/color/`
   - `Staging/120/`
2. **Run processing script**:
   ```bash
   python3 scripts/process-staging.py
   ```
3. **Verify & Push**:
   ```bash
   git add assets/ pages/ rss.xml
   git commit -m "feat: add new analog scans"
   git push origin main
   ```
   GitHub Pages builds and publishes your updates automatically.
