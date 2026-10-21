# AGENTS.md

## Project & Persona Context
- **Identity:** Sawyer Knox, GPS Analyst at Deloitte and film photographer based in Portland, Oregon.
- **Project:** `sjkonfilm.work` - A professional 35mm and 120 film photography portfolio.
- **Aesthetic:** Authentic, gritty, minimalist, and organic. Focus heavily on black and white street and travel photography. 
- **Goal:** To maintain a lightning-fast, highly optimized web presence that ranks globally on Google Search and serves as a verified anchor for my digital identity and knowledge graph. Want to build this site out into whatever it needs to be to spread my footprint, brand, name, work, etc. I want this to be a hub for me and my work. It is a changing thing that we are building out one piece at a time but each piece should work with the others and my social media towards the goal of allowing me to take my finished product (photos) and as easily and automatically as possible, do everyhting remotely possible to get me fans, followers, and recognition. 

## Tech Stack & Hosting
- **Architecture:** Pure static site. 
- **Languages:** Strict vanilla HTML, CSS, and lightweight JavaScript only. 
- **Hosting:** Version-controlled via Git, pushed to a GitHub repository, and deployed via GitHub Pages.
- **Domain:** Custom domain (`sjkonfilm.work`) routed through Porkbun DNS.

## Strict Agent Constraints
1. **No Heavy Frameworks:** Do NOT introduce React, Next.js, Node.js, backend databases, or complex build tools. Keep the footprint minimal and local.
2. **SEO Priority:** All HTML changes must protect and enhance existing semantic tags, `<head>` metadata, and schema JSON-LD scripts tying the site to my LinkedIn and Instagram.
3. **Mobile and desktop compatibility:** Make sure the site looks good on both mobile and desktop. make sure changes to one never breaks the other. Optimize for both. 
4. **Asset Management:** All images are stored locally in `/assets/images/` using a 2-tier decoupled engine (`full/` for Lightbox modals, `thumbs/` for gallery grids). Standard aspect dimensions are `900x597` (horizontal) and `597x900` (vertical). Thumbnails use WebP with srcset (`400w` for mobile, `900w` for desktop). Automation tools are stored in `/scripts/`.
5. **Code Style:** Keep CSS classes semantic and clean. Do not leave orphaned code. Ensure cross-browser compatibility for basic styling.
6. **Agent Self-Maintenance & Context Integrity:** Any AI agent working on this codebase MUST keep `AGENTS.md` updated whenever new features, social accounts, workflows, scripts, or architectural changes are implemented. Whenever a milestone is reached, the agent MUST update `AGENTS.md` so future agent sessions maintain continuous, perfect context without redundant suggestions.
7. **Factual Captions Only (No AI Creativity):** All generated photo captions, metadata descriptions, and RSS/syndication text MUST be strictly factual—containing only basic facts: Photo Title/Subject, Location, Rough Date (Season & Year), Film Format (35mm / 120 film), Website link (`https://sjkonfilm.work`), and Instagram handle (`@sawyer.j.knox`). Do NOT add subjective descriptions, fluffy storytelling, or AI prose.
8. **No EXIF/Camera Overlays:** Do NOT suggest or add EXIF, film stock, camera gear, or technical badges to the lightbox viewer or gallery pages.
9. **No Geospatial / GPS Maps:** Do NOT suggest or add interactive GIS/GPS photo location maps.



## Site Architecture & Taxonomy Hierarchy
- **Categorization Model:** Exactly two top-level film formats: **35mm** and **120**.
  - **35mm:** Subdivided strictly into **Color** and **Black & White**. All previous street, scenes, and vertical categories have been unified directly into their respective B&W and Color collections (no separate street, scenes, or vertical categories).
  - **120:** Dedicated to 6×6 square medium format negatives (currently all Black & White; no color 120 exists yet).
- **Works Page (`works.html`):** Features "Selected Works" with two clean exhibition display cards:
  1. **35mm Film:** 3:2 landscape display image, curatorial description, simple text subcategories (`Black & White · Color`), and direct collection link.
  2. **120 Medium Format:** 1:1 square display image, curatorial description, simple text (`Black & White`), and direct collection link. *(Strict rule: Do NOT specify camera brand/model like Rolleiflex in public card titles/subtitles)*.
- **Minimalist Sub-Navigation:** No rounded bubble pills or active highlighting buttons anywhere. Under 35mm, subcategories are presented as quiet, elegant text links: `Black & White · Color`. No format switchers between 35 and 120 on gallery pages, and no status counts ("Showing X photographs").
- **Header Navigation:** Dropdown on hover over `Work` consists strictly of two direct items: `35mm` and `120`.

## Image Pipeline & Maintenance Workflow
When publishing new photographs:
1. **Drop into Staging:** Place exported full-size scans into their respective folder under `/Staging/` (e.g., `Staging/35mm/color/`, `Staging/35mm/street/`, `Staging/35mm/scenes/`, `Staging/35mm/vertical/`, or `Staging/120/`).
2. **Automated Staging Processing:** Run `python scripts/process-staging.py`. The script handles SEO slug renaming, metadata injection, WebP/AVIF generation (`full/` at max 1800px, `thumbs/` at 900w and 400w), appends the responsive `<img>` node directly to the target `pages/[category].html` gallery and syncs with `pages/35mm.html`, cleans up by deleting the staging file, and updates `rss.xml` for Pinterest syndication.
3. **Commit & Deploy:** Inspect the updated HTML, then commit and push to GitHub (`git push origin main`) for live deployment on GitHub Pages.

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
