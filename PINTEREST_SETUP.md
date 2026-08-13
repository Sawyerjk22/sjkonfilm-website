# Pinterest Visual SEO & Auto-Pin Integration Guide

This guide walks you through setting up a Pinterest Business account for **`sjkonfilm.work`**, verifying your domain, backfilling your existing portfolio via CSV, and enabling hands-free RSS auto-pinning for new uploads.

---

## Step 1: Create & Claim Pinterest Business Account

1. Go to [Pinterest Business Signup](https://www.pinterest.com/business/create/) and sign up using your professional email.
2. Set your Profile Name to **Sawyer Knox | Film Photography** and handle to `@sjkonfilm` or `@sawyer.j.knox`.
3. Go to **Settings > Claimed Accounts > Claim website**.
4. Select **Add HTML tag** and copy the verification tag (e.g. `<meta name="p:domain_verify" content="..." />`).
5. Paste the verification tag into the `<head>` of your `index.html` file.
6. Commit & push changes to GitHub Pages, then click **Verify** in Pinterest.

---

## Step 2: One-Time Bulk Backfill (315+ Existing Photos)

To immediately publish all existing images on your site to Pinterest:

1. Run the local export script:
   ```bash
   python scripts/export-pinterest-csv.py
   ```
*(Since Pinterest strictly limits bulk CSV uploads to 100 rows per file, this generates `pinterest_pins_part1.csv` through `part4.csv` [100, 100, 100, 15 pins]).*
2. In Pinterest Business Hub, click **Create > Create Pins in Bulk**.
3. Upload each CSV file (`part1.csv`, `part2.csv`, `part3.csv`, `part4.csv`) separately and click **Publish**.
4. *Note: If you previously uploaded the old 200-row files where Pinterest processed the first 100 of each file (uploading Part 1 & Part 3 equivalents), you only need to upload **`pinterest_pins_part2.csv`** and **`pinterest_pins_part4.csv`** to finish backfilling all 315 photos.*
5. Pinterest will parse and create pins with high-resolution image previews, descriptive titles, camera keywords, and direct links back to `https://sjkonfilm.work`.

---

## Step 3: Enable Automated RSS Auto-Pinning (Hands-Free)

Whenever you deploy new photos via Phase 1 staging script, `rss.xml` automatically updates.

To connect `rss.xml` to Pinterest:
1. Go to **Settings > Claimed Accounts > Auto-publish Pins from RSS feed**.
2. Click **Connect RSS feed**.
3. Paste your feed URL: `https://sjkonfilm.work/rss.xml`
4. Select your destination Pinterest board (e.g. *35mm & 120 Film Photography*).
5. Click **Save**.

> [!TIP]
> Pinterest will check your `rss.xml` feed every few hours and automatically publish newly added photos as high-ranking visual Pins linked directly to `sjkonfilm.work`.
