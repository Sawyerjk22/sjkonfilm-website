# Unsplash & Pinterest -> Instagram Inbound Funnel Guide

This guide outlines how to maximize organic Instagram follower growth (`@sawyer.j.knox`) and portfolio traffic (`sjkonfilm.work`) from **Unsplash** and **Pinterest**.

---

## 1. Unsplash Strategy & Bio Optimization

Unsplash images get millions of impressions from designers, editors, writers, and bloggers. When creators re-use your photos or download them for moodboards, directing them to your Instagram profile turns views into active followers.

### Unsplash Account Profile Bio
```text
Portland-based 35mm & 120 film photographer.
Portfolio & prints: https://sjkonfilm.work
Instagram: @sawyer.j.knox
```

### Unsplash Photo Upload Checklist
1. **Filename**: Export WebP/JPEG assets using `scripts/process-staging.py` so EXIF/IPTC artist tags (`Sawyer Knox`) and copyright comments (`Instagram: @sawyer.j.knox | Portfolio: https://sjkonfilm.work`) are baked into the file headers.
2. **Photo Description Prompt**:
   - In Unsplash photo descriptions, include clean attribution guidelines:
     > *"Shot on 35mm film in Portland, OR by Sawyer Knox. Instagram: @sawyer.j.knox | Portfolio: sjkonfilm.work"*
3. **Location & Tags**: Always add location (`Portland, Oregon`) and technical tags (`35mm film`, `black and white`, `street photography`, `film grain`, `analog photography`).

---

## 2. Pinterest Strategy & Bulk Upload Workflow

Pinterest acts as a visual search engine where analog photography content receives long-tail traffic for years.

### A. Pinterest Profile Bio
```text
Sawyer Knox | 35mm & 120 Film Photography
Authentic street and travel film photography based in Portland, Oregon.
Instagram: @sawyer.j.knox | sjkonfilm.work
```

### B. Pinterest Board Structure
Maintain clean boards mapping to your website galleries:
- **35mm Street Photography**
- **Analog Landscapes & Scenes**
- **Color Film Photography**
- **Vertical Film Shots & Portraits**
- **Rolleiflex 120 Medium Format**
- **Featured Film Photography**

### C. Bulk Pin Upload Workflow (CSV)
1. Run `python scripts/export-pinterest-csv.py`.
2. This generates `pinterest_pins_part1.csv`, `pinterest_pins_part2.csv`, etc., containing up to 100 pins per CSV file formatted to Pinterest's exact bulk specifications.
3. Open **Pinterest Business -> Create -> Bulk Create Pins**.
4. Drag and drop the generated CSV file.
5. All Pins are published with:
   - Optimized Titles
   - Direct image URLs
   - Direct portfolio gallery destination links
   - Description formatted with Instagram credit (`Instagram: @sawyer.j.knox | Portfolio & prints: https://sjkonfilm.work`)

### D. Automated Pinterest RSS Feed Auto-Pinning
1. Ensure `rss.xml` is updated whenever new photos are added by running `python scripts/generate-rss.py`.
2. In Pinterest Settings -> **Claimed Accounts -> Auto-publish from RSS feed**, add your feed URL:
   `https://sjkonfilm.work/rss.xml`
3. Pinterest automatically converts every new gallery upload into a Pin linked to `sjkonfilm.work` with your Instagram handle in the caption.

---

## 3. Embedded Image Metadata Protection

All images processed through `scripts/process-staging.py` or backfilled via `scripts/inject-metadata.py` have the following IPTC/EXIF metadata embedded directly in the WebP/AVIF file headers:

- **Artist**: `Sawyer Knox`
- **Copyright**: `© Sawyer Knox (https://sjkonfilm.work)`
- **Comment**: `35mm/120 film photography by Sawyer Knox. Instagram: @sawyer.j.knox | Portfolio: https://sjkonfilm.work`

If an editor or blog downloads an image directly from your site or Unsplash, reverse image tools, metadata parsers, and EXIF viewers preserve credit back to **`@sawyer.j.knox`**.
