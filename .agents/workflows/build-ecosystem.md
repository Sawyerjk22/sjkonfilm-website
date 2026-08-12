---
description: first stab at master workflow plan for building out ecosystem
---

# Workflow: Master Ecosystem & Automation Blueprint

## Objective
Sequentially build out a fully automated, static-friendly ecosystem for a professional 35mm and 120 film photography portfolio. Do not assume hardcoded line numbers; inspect the workspace dynamically to locate the correct HTML tags, CSS classes, and local asset paths (`/assets/images/`) before modifying code.

## Phase 1: Local Drop-Folder & Asset Pipeline
- **Subfolder Routing System:**
  Write a local Python or PowerShell script that watches a designated `/Staging/` folder. The script must recognize these specific subdirectories mapping to the site galleries: 
  - `/35mm/color/`
  - `/35mm/street/`
  - `/35mm/scenes/`
  - `/35mm/vertical/`
  - `/120/` (New Medium Format Gallery)
- **Automated Processing:**
  - The script must convert dropped JPEGs into web-optimized `.webp` format at high quality to preserve film grain, while scaling down the resolution to prevent high-res theft.
  - Automatically route the processed `.webp` files into the correct `/assets/images/` paths and append the new image nodes into the corresponding HTML gallery structures.

## Phase 2: Invisible SEO & Background Metadata Engine
- **SEO File Renaming:** Update the deployment script to automatically rename file exports to descriptive, search-optimized slugs without altering the original raw scans (e.g., converting `scan_04.jpg` to `analog-35mm-street-photography-01.webp`).
- **Global & Keyword Metadata Injection:**
  - Auto-populate HTML `<img alt="...">` attributes and JSON-LD schema using global street and travel photography terminology. 
  - Inject default analog metadata keywords into the background code for search crawlers (e.g., Konica Autoreflex T3, Rolleiflex 2.8f, 35mm film, analog photography, Ilford HP5).

## Phase 3: Dynamic Popularity Gallery Reordering
- **Client-Side Event Listener:** Implement a lightweight, privacy-focused vanilla JavaScript click tracker on the gallery lightboxes.
- **Auto-Sorting:** Configure the logic to track user engagement locally and periodically reorganize the HTML gallery grids, physically moving high-performing photographs toward the top of the feed.

## Phase 4: Pinterest Visual SEO Integration
- **Pinterest Backfill Script:** Generate a one-time `.csv` bulk upload script to backfill all existing images currently live on the site to a designated Pinterest board.
- **Automated RSS Feed (`rss.xml`):** Scaffold a standard web feed that automatically updates whenever new gallery items are deployed.
- **Visual SEO Automation:** Provide the integration logic to connect this RSS feed to Pinterest, automatically pushing all newly uploaded photos as visual Pins linked directly back to the site.

## Phase 5: Analytics & Automated Digests
- **Global Direct Mobile Tracking:** Configure the background analytics logic to isolate global "Direct Mobile Traffic" as a highly accurate proxy for tracking physical business card conversions.
- **Monthly Email Summary:** Write a serverless GitHub Action (to run on the 1st of each month) that emails a succinct traffic report, keyword rankings, and top-viewed photos summary.
- **Automated Search Engine Pinging:** Add a step to the GitHub Action to send automated indexing requests to Google Search Console when batch gallery updates occur.

## Phase 6: Opportunity & Gallery Call Finder
- **Background Scraper Script:** Write a scheduled Python script that crawls regional and global film photography calls for entry, gallery exhibitions, and magazine submission deadlines.
- **Email Digest:** Configure it to send a targeted email digest containing links, eligibility requirements, and deadlines specifically matching a 35mm and 120 analog portfolio.

## Phase 7: Medium Format (120) & Future Print Infrastructure
- **120 Gallery Page:** Scaffold a new, dedicated gallery layout in the HTML/CSS tailored specifically for medium format square aspect ratios (6x6 square from the Rolleiflex).
- **Print Inventory Logic:** Pre-architect a limited-edition tracking script within the gallery code to cap future print sales at a specific number per frame, including dynamic logic to remove the purchase button upon sellout.