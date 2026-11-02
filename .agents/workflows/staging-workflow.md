---
description: Step-by-step workflow for processing and publishing new 35mm and 120 film rolls
---

# Workflow: Film Drop & Staging Pipeline

## Objective
Process newly scanned analog film frames into web-optimized, responsive WebP/AVIF images with embedded metadata, auto-inject into site gallery HTML, update Pinterest RSS feeds, and deploy to GitHub Pages.

## Step 1: Drop Raw Scans into Staging Subfolder
Export your high-resolution film scans (TIFF, PNG, or JPEG) directly into the appropriate staging folder:
- **35mm Black & White:** `Staging/35mm/bw/`
- **35mm Color:** `Staging/35mm/color/`
- **120 Medium Format (6x6 Square):** `Staging/120/`

*(Legacy folders `Staging/35mm/street/`, `Staging/35mm/scenes/`, `Staging/35mm/vertical/` also route directly to `pages/35mm.html`)*.

## Step 2: Run the Staging Pipeline
Execute the processing script:
```bash
python3 scripts/process-staging.py
```
*(Tip: Add `--dry-run` to preview filenames and generated HTML tags before writing files).*

What the script automatically executes:
1. Generates clean, search-friendly slugs (e.g. `analog-color-film-photography-img-0820.webp`).
2. Injects copyright, artist (`Sawyer Knox`), and website/Instagram links directly into IPTC/EXIF headers.
3. Compresses and generates:
   - Full lightbox asset (max 1800px) in `assets/images/<cat>/full/`
   - Desktop thumbnail (900w) in `assets/images/<cat>/thumbs/`
   - Mobile thumbnail (400w) in `assets/images/<cat>/thumbs/`
4. Appends responsive `<img>` elements with `srcset` and `sizes` attributes into the corresponding gallery (`pages/35mm.html` or `pages/120.html`).
5. Updates `rss.xml` with Media RSS enclosures for Pinterest auto-pinning.
6. Cleans up processed scans from the `Staging/` folder.

## Step 3: Verify Locally
Check the updated gallery locally:
```bash
python3 -m http.server 8000
```
Open `http://localhost:8000/pages/35mm.html` or `http://localhost:8000/pages/120.html` to confirm images and lightbox functionality.

## Step 4: Commit & Deploy
Commit the newly generated images and updated HTML/RSS files:
```bash
git add assets/ pages/ rss.xml
git commit -m "feat(gallery): add new film scans"
git push origin main
```
GitHub Pages will automatically build and deploy within 1–2 minutes.
Search engine ping and Pinterest auto-pinning will detect the updated `rss.xml` automatically.
