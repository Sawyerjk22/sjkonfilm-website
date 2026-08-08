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

## Image Pipeline & Maintenance Workflow
When publishing new photographs:
1. **Source Assets:** Place full-size WebP/JPEG images into `/assets/images/[category]/full/`.
2. **Standardize & Resize:** Run ImageMagick powershell scripts in `/scripts/` (`standardize-webp.ps1` and `resize-imagemagick.ps1`) to convert to WebP and generate `900w` + `400w` thumbnails.
3. **HTML Generation & Optimization:** Run `generate-code.ps1` to produce HTML image tags, paste tags into the corresponding `pages/[category].html` gallery, and run `update-gallery-html.ps1` to enforce lazy loading and dimensions.