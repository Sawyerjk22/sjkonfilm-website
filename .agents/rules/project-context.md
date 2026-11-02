# Project Rules & Persona Directives

## Identity & Core Intent
- **Photographer:** Sawyer Knox (GPS Analyst at Deloitte & film photographer in Portland, Oregon).
- **Domain:** `https://sjkonfilm.work`
- **Instagram:** `@sawyer.j.knox` (Manual posting only; never automate Instagram).
- **Core Aesthetic:** Authentic, gritty, minimalist, organic 35mm and 120 analog film photography.

## Technical & Architectural Mandates
1. **Zero Frameworks:** Strict vanilla HTML5, CSS3, and minimal vanilla JavaScript. No React, Next.js, Node.js, Vite, or Tailwind.
2. **SEO & Metadata:** Preserve all `<head>` metadata, Open Graph cards, schema JSON-LD with verified social identities (`sameAs`), and semantic tags.
3. **Dual Optimization:** Mobile and desktop must look clean, balanced, and responsive.
4. **Asset Pipeline:** Images reside in `/assets/images/` (`full/` for Lightboxes max 1800px, `thumbs/` at 900w and 400w with srcset).
5. **No AI Fluff in Captions:** Captions, alt text, and syndication snippets must contain ONLY factual data: Subject/Title, Location, Date (Season & Year), Film format, Website link, and Instagram handle.
6. **No EXIF UI Badges or GPS Maps:** Never render camera specs or location map embeds in the visitor-facing UI.

## Current Site Hierarchy
- **Top-level formats:** `35mm` (`pages/35mm.html`) and `120` (`pages/120.html`).
- **35mm Collection:** Unified in `pages/35mm.html` with instant subcategory toggle for Black & White and Color.
- **120 Collection:** Dedicated to 6x6 medium format square negatives in `pages/120.html`.
- **Works Page (`works.html`):** Two minimalist cards (35mm and 120).

## Staging & Deployment Workflow (macOS / Linux / Windows)
1. Drop raw scans into `Staging/35mm/bw/`, `Staging/35mm/color/`, or `Staging/120/`.
2. Run: `python3 scripts/process-staging.py` (requires ImageMagick: `brew install imagemagick`).
3. Commit & push: `git push origin main` (deploys automatically via GitHub Pages).
