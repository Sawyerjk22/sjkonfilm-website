# AGENTS.md

## Project & Persona Context
- **Identity:** Sawyer Knox, GPS Analyst at Deloitte and film photographer based in Portland, Oregon.
- **Project:** `sjkonfilm.work` - A professional 35mm and 120 film photography portfolio.
- **Aesthetic:** Authentic, gritty, minimalist, and organic. Focus heavily on black and white street and travel photography, with warm analog color tones and 6x6 medium format frames.
- **Goal:** To maintain a lightning-fast, highly optimized web presence that ranks globally on Google Search and serves as a verified anchor for Sawyer's digital identity and knowledge graph. The site serves as the central hub of an automated ecosystem, allowing Sawyer to take finished photos and effortlessly distribute them to social platforms, search engines, and directories to grow recognition, fans, and followers.

## Tech Stack & Hosting
- **Architecture:** Pure static site. Zero heavy frameworks, zero runtime dependencies.
- **Languages:** Strict vanilla HTML5, CSS3, and lightweight vanilla JavaScript only (for Lightbox and gallery filtering).
- **Hosting:** Version-controlled via Git, pushed to GitHub repository (`Sawyerjk22/sjkonfilm-website`), and deployed via GitHub Pages.
- **Domain:** Custom domain (`sjkonfilm.work`) routed through Porkbun DNS.

## Strict Agent Constraints
1. **No Heavy Frameworks:** Do NOT introduce React, Next.js, Vue, Node.js, backend databases, or complex build bundlers (Webpack, Vite, Tailwind). Keep the codebase static, lightweight, and local.
2. **SEO Priority:** All HTML changes must preserve and enhance semantic tags, `<head>` metadata, Open Graph cards, Twitter cards, and Schema.org JSON-LD scripts tying the site to Sawyer's LinkedIn, Instagram, and other verified entities.
3. **Mobile & Desktop Compatibility:** Optimize both mobile and desktop views with equal rigor. Changes made for one must never compromise or break the other. Test responsive behaviors across viewport widths.
4. **Asset Management:** All gallery images reside in `/assets/images/` using a 2-tier decoupled architecture:
   - `full/` for Lightbox modals (max 1800px on longest dimension).
   - `thumbs/` for gallery grids with responsive `srcset` (`400w` mobile thumbnail and standard `900w` thumbnail). Standard aspect ratios are `900x597` (landscape), `597x900` (portrait/vertical), and `900x900` (120 medium format square).
5. **Code Style:** Keep CSS classes semantic and clean. Do not leave orphaned code. Ensure cross-browser compatibility.
6. **Agent Self-Maintenance & Context Integrity:** Any AI agent working on this codebase MUST keep `AGENTS.md` and `GEMINI.md` updated whenever new features, workflows, scripts, social accounts, or architectural changes occur. Whenever a milestone is reached, update this document so future agent sessions maintain continuous, perfect context without redundant suggestions.
7. **Factual Captions Only (No AI Creativity):** All generated photo captions, metadata descriptions, and RSS/syndication text MUST remain strictly factual—containing only: Photo Title/Subject, Location, Season & Year, Film Format (35mm / 120 film), Website link (`https://sjkonfilm.work`), and Instagram handle (`@sawyer.j.knox`). Never add subjective descriptions, fluffy storytelling, or AI prose.
8. **No EXIF/Camera Overlays:** Do NOT suggest or add EXIF, film stock, camera gear, or technical badges to the lightbox viewer or gallery pages.
9. **No Geospatial / GPS Maps:** Do NOT suggest or add interactive GIS/GPS photo location maps.

## Site Architecture & Taxonomy Hierarchy (Current State)
- **Categorization Model:** Exactly two top-level film formats: **35mm** and **120**.
  - **35mm (`pages/35mm.html`):** The primary unified hub for all 35mm work. Features an instant client-side filter toggle for **Black & White** (`data-tone="bw"`) and **Color** (`data-tone="color"`). All street, scenes, and vertical categories have been unified into this central 35mm collection.
  - **120 (`pages/120.html`):** Dedicated to 6×6 square medium format negatives (currently all Black & White; no color 120 exists yet).
- **Works Page (`works.html`):** Features "Selected Works" with two clean, minimalist gallery display cards:
  1. **35mm:** 3:2 landscape display image, clean title `35mm`, and straightforward format subtitle (`Black & White · Color`). No marketing copy, format badges, or CTA arrows.
  2. **120:** 1:1 square display image (`2026-r05-120-1.webp`), clean title `Medium Format`, and straightforward format subtitle (`Black & White`). *(Strict rule: Do NOT specify camera brand/model like Rolleiflex in public card titles/subtitles)*.
- **Minimalist Sub-Navigation:** Under 35mm, subcategories are presented as quiet, understated text links (`Black & White · Color`) styled noticeably smaller than the main header navigation (`Work`, `About`, `Contact`). No rounded bubble pills or active highlighting buttons anywhere. No format switchers between 35 and 120 on gallery pages, and no status counts ("Showing X photographs").
- **Header Navigation:** Dropdown on hover over `Work` consists strictly of two direct items: `35mm` and `120`.
- **Legacy Subpages:** `pages/color.html`, `pages/street.html`, `pages/scenes.html`, and `pages/vertical.html` remain intact as valid landing pages and SEO anchors.

## Image Pipeline & Maintenance Workflow
When publishing new photographs:
1. **Drop into Staging:** Export full-size scans into the designated folder under `/Staging/`:
   - `Staging/35mm/bw/` -> 35mm Black & White
   - `Staging/35mm/color/` -> 35mm Color
   - `Staging/120/` -> 120 Medium Format (6x6 square)
   *(Legacy staging folders `Staging/35mm/street/`, `Staging/35mm/scenes/`, `Staging/35mm/vertical/` also route directly to `pages/35mm.html`)*.
2. **Automated Staging Processing:** Run:
   ```bash
   python3 scripts/process-staging.py
   ```
   The script handles SEO slug renaming, IPTC/EXIF artist & copyright metadata injection, WebP/AVIF generation (`full/` max 1800px, `thumbs/` at 900w and 400w), appends the responsive `<img>` node into the target HTML gallery (`pages/35mm.html` or `pages/120.html`), cleans up processed staging files, and updates `rss.xml` for Pinterest syndication.
3. **Commit & Deploy:** Inspect the updated HTML, then commit and push to GitHub (`git push origin main`) for live deployment on GitHub Pages.

## Automation & Scripting Ecosystem
- **`scripts/publish.py` ( & `git push` / `publish` Shell Trigger):** Master one-step automation. Simply drop scans into `Staging/` and run `git push` (or `publish` / `python3 scripts/publish.py`). Automatically executes `process-staging.py`, updates `rss.xml`, `sitemap.xml`, and `pinterest_pins_*.csv`, commits all generated assets and HTML, pushes to `origin main`, and pings IndexNow.
- **`scripts/curate.py` ( & `curate` Shell Trigger):** Local visual portfolio curation web UI (`http://localhost:8080/curate`). Allows Sawyer to visually browse all photos by category/orientation (`35mm B&W Horizontal`, `35mm B&W Vertical`, `35mm Color Horizontal`, `35mm Color Vertical`, `120 Medium Format`), click any photos to mark for removal, automatically strip their HTML nodes across `pages/35mm.html`, `pages/120.html`, and legacy subpages, safely archive removed `.webp`/`.avif` files into `Staging/processed/archived/`, regenerate `rss.xml`/`sitemap.xml`/Pinterest CSVs, and push live to GitHub with one button click.
- **`scripts/process-staging.py`:** Core asset pipeline using ImageMagick (`magick`) to resize, compress, inject IPTC/EXIF metadata, generate clean factual Season + Year captions (e.g. `Late Summer 2026 - 35mm Film Photography`—no locations or manual renaming required), save metadata-stamped high-res `.jpg` copies + `captions.txt` into `Staging/processed/unsplash-ready/` for Unsplash/Instagram, and insert HTML tags (automatically placing 35mm horizontal photos at the top and vertical photos at the bottom of `pages/35mm.html`).
- **`scripts/generate-rss.py`:** Parses gallery HTML, builds `rss.xml` with deep-linked Lightbox URLs (`#photo-slug`) and Media RSS tags for Pinterest auto-pinning, and regenerates `sitemap.xml` with full Google Image Sitemap (`<image:image>`) tags across all 333 gallery image nodes.
- **`scripts/export-pinterest-csv.py`:** Exports gallery images with deep-linked `#photo-slug` destination URLs into Pinterest-compliant bulk CSV upload files (`pinterest_pins_part1.csv` through `part3.csv`).
- **`scripts/generate-og-cards.py`:** Generates 1200×630 Open Graph preview cards (`og-main.png`, `og-120.png`, `og-street.png`, etc.).
- **`scripts/syndicate-posts.py`:** Multi-platform syndication to Flickr and Medium. *(Instagram auto-posting is strictly disabled; manual only)*.
- **`scripts/opportunity-finder.py`:** Crawls open calls for entry, zines, and gallery exhibition deadlines for analog photography.
- **`scripts/send-monthly-digest.py`:** Generates and emails a monthly ecosystem summary to Sawyer via SMTP.
- **`scripts/ping-search-engines.py`:** Pings IndexNow (`sjkonfilm-indexnow-key-2026.txt`) and Google Sitemap endpoints after batch updates.
- **`.github/workflows/auto-publish.yml`:** Automated GitHub Action triggered on every `push` to `main` to process any staged scans, sync `rss.xml` and Google Image `sitemap.xml`, and ping IndexNow + syndication endpoints.
- **`.github/workflows/monthly-digest.yml`:** Automated GitHub Action running on the 1st of every month to execute search engine pings, monthly digest email, and the opportunity finder.

## Active Digital Entity & Social Network Matrix (Completed & Interlinked)
- **Primary Domain:** `https://sjkonfilm.work` (Indexed, Schema JSON-LD `sameAs` array fully configured, `rel="me"` IndieWeb tags added).
- **Instagram:** `@sawyer.j.knox` — Public profile, display name explicitly set to `Sawyer Knox`, bio linked to `sjkonfilm.work`. *(Note: Instagram posting is handled 100% manually by Sawyer; auto-posting is strictly disabled).*
- **GitHub:** `Sawyerjk22` (Display Name: `Sawyer Knox`) — Location set to Portland, OR; Secrets (`MAIL_USERNAME`, `MAIL_PASSWORD`, `TO_EMAIL`) active for automated monthly digests and opportunity finder emails.
- **Pinterest:** `sjkonfilm` (Display Name: `Sawyer Knox | Film Photography`) — Claimed domain `sjkonfilm.work`, RSS auto-pinning active via `https://sjkonfilm.work/rss.xml`.
- **Flickr:** `flickr.com/photos/sawyerknox` (Display Name: `Sawyer Knox`) — Custom vanity URL active, website link & bio configured, RSS/API syndication configured in `scripts/syndicate-posts.py`.
- **Unsplash:** `@sawyerknox` (Display Name: `Sawyer Knox`) — Creator profile active with uploaded photos, linked to `sjkonfilm.work` & IG.
- **Medium:** `@sawyerknox` (Display Name: `Sawyer Knox`) — Profile active, bio and introduction article published, RSS auto-import & API syndication configured in `scripts/syndicate-posts.py`.
- **LinkedIn:** `in/sawyer-knox` — Linked in Schema.org and profile matrix.
- **Google Search Console:** `sjkonfilm.work` verified, re-indexing requested, `sitemap.xml` submitted with updated `<lastmod>` dates.

*Rule for AI Agents:* Do NOT suggest creating GitHub, Pinterest, Flickr, Unsplash, Medium, or Instagram accounts for Sawyer Knox, as they are fully set up, active, and interlinked in the website's Schema JSON-LD and `rel="me"` identity matrix. Instagram posting is strictly manual.

## MacBook / macOS Environment & Setup Instructions
When working on macOS:
1. **Repository Location:** The repository is permanently located at `/Users/sawyerknox/Photography/03_Website_sjkonfilm`:
   ```bash
   cd /Users/sawyerknox/Photography/03_Website_sjkonfilm
   ```
2. **Homebrew & ImageMagick (Required for Staging Pipeline):**
   The staging script `process-staging.py` calls `magick` to resize and compress photos. Installed at `/opt/homebrew/bin/magick` via Homebrew:
   ```bash
   brew install imagemagick
   ```
3. **Python 3:**
   macOS includes Python 3 by default (`python3`). All Python scripts use the standard library (`os`, `sys`, `re`, `glob`, `subprocess`, `urllib`, `smtplib`, `xml`) and are compatible with macOS Python 3.9+. Verify with:
   ```bash
   python3 --version
   ```
4. **Local Development Server:**
   To preview the site locally on macOS with live image rendering:
   ```bash
   python3 -m http.server 8000
   ```
   Then open `http://localhost:8000` in the browser, or use Antigravity's built-in preview.
5. **Running Automation Scripts:**
   Always use `python3`:
   ```bash
   python3 scripts/process-staging.py
   python3 scripts/generate-rss.py
   python3 scripts/syndicate-posts.py
   ```
6. **No PowerShell Needed:**
   The repository contains legacy `.ps1` scripts from Windows development; on macOS, always use the equivalent Python scripts (`process-staging.py`, `generate-rss.py`, etc.).

## Where We Left Off (Current Project Milestone)
- **MacBook Setup & First 120 + 35mm Batch:** Cloned repository to `/Users/sawyerknox/Photography/03_Website_sjkonfilm`, installed Homebrew, ImageMagick (`magick`), and GitHub CLI (`gh`), fixed `scripts/process-staging.py` (square detection for high-res 6×6 scans + `bw` category asset paths and `<section id="filmGallery">` regex), fixed Python 3.9 f-string compatibility in `generate-rss.py` / `export-pinterest-csv.py`, added IndexNow verification key file (`sjkonfilm-indexnow-key-2026.txt`), added the floating Instagram `.glass-badge` to `pages/120.html` plus RSS auto-discovery `<link>` tags across gallery pages, and published 15 new 120 medium format photographs (`pages/120.html`) and 8 new 35mm B&W photographs (`pages/35mm.html`).
- **Recent Completion:** Completed "Rehaul 4" which finalized the site simplification. Navigation dropdown now cleanly features `35mm` and `120`. `works.html` displays the two minimalist format cards. `pages/35mm.html` serves as the unified gallery with instant B&W/Color client-side filtering.
- **Pinterest Backfill:** 315+ photos backfilled across CSV parts 1–4. `rss.xml` auto-pinning enabled (now 298 feed items).
- **Staging Pipeline:** Staging directory tree preserved with `.gitkeep` files across all categories.
- **Active / Open Working Documents:**
  - `pages/35mm.html` (primary 35mm collection)
  - `pages/120.html` (6×6 medium format collection, now populated with 15 scans)
  - `pages/color.html` & `pages/street.html` (legacy subpages maintained for backwards compatibility)
  - `UNSPLASH_PINTEREST_FUNNEL.md` (active inbound strategy)
  - `scripts/syndicate-posts.py` (syndication hub)
- **Immediate Next Steps on MacBook:**
  1. Continue adding new 35mm film rolls by dropping scans into `Staging/35mm/bw/` or `Staging/35mm/color/` (or `Staging/120/`) and running `python3 scripts/process-staging.py`.
  2. Commit and push processed updates (`git push origin main`) to deploy live on GitHub Pages.