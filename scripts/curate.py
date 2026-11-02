#!/usr/bin/env python3
"""
Visual Gallery Curation & Cleanup Tool for sjkonfilm.work
Starts a local interactive web UI at http://localhost:8080/curate
where Sawyer can visually click photos to remove them from the site,
edit captions, and push the cleaned-up gallery live with one click.
"""

import os
import re
import sys
import json
import glob
import shutil
import socket
import webbrowser
import subprocess
from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ARCHIVE_DIR = os.path.join(REPO_ROOT, "Staging", "processed", "archived")

GALLERY_FILES = [
    os.path.join("pages", "35mm.html"),
    os.path.join("pages", "color.html"),
    os.path.join("pages", "120.html"),
]

def parse_all_photos():
    """Parse all gallery photos from pages/35mm.html and pages/120.html."""
    photos = []
    seen = set()

    for rel_page in [os.path.join("pages", "35mm.html"), os.path.join("pages", "120.html")]:
        full_page = os.path.join(REPO_ROOT, rel_page)
        if not os.path.exists(full_page):
            continue
        with open(full_page, "r", encoding="utf-8") as f:
            content = f.read()

        sec_match = re.search(r'<section class="gallery[^"]*"[^>]*>(.*?)</section>', content, re.DOTALL)
        if not sec_match:
            continue
        inner = sec_match.group(1)

        for m in re.finditer(r'<img\s+[^>]+>', inner, re.DOTALL):
            tag = m.group(0)
            src_m = re.search(r'src="([^"]+)"', tag)
            full_m = re.search(r'data-full="([^"]+)"', tag)
            alt_m = re.search(r'alt="([^"]*)"', tag)
            tone_m = re.search(r'data-tone="([^"]+)"', tag)
            w_m = re.search(r'width="(\d+)"', tag)
            h_m = re.search(r'height="(\d+)"', tag)

            if not src_m:
                continue
            thumb_rel = src_m.group(1).replace("../", "").lstrip("/")
            full_rel = (full_m.group(1) if full_m else src_m.group(1)).replace("../", "").lstrip("/")

            if full_rel in seen:
                continue
            seen.add(full_rel)

            w = int(w_m.group(1)) if w_m else 900
            h = int(h_m.group(1)) if h_m else 597
            alt_raw = alt_m.group(1) if alt_m else ""
            clean_caption = re.sub(
                r'\s*-\s*(?:35mm|120)?(?:\s*Black\s*&\s*White|\s*Color|\s*Medium\s*Format)?\s*Film Photography.*',
                '',
                alt_raw,
                flags=re.IGNORECASE
            ).strip()

            if "120.html" in rel_page:
                fmt = "120"
                tone = "bw"
                orient = "square"
            else:
                fmt = "35mm"
                tone = tone_m.group(1) if tone_m else "bw"
                orient = "vertical" if h > w else "horizontal"

            photos.append({
                "id": full_rel,
                "filename": os.path.basename(full_rel),
                "thumb_url": "/" + thumb_rel,
                "full_url": "/" + full_rel,
                "alt": alt_raw,
                "caption": clean_caption,
                "format": fmt,
                "tone": tone,
                "orientation": orient,
                "width": w,
                "height": h,
                "page": rel_page
            })
    return photos

def archive_asset_variants(full_rel):
    """Move full and thumb WebP/AVIF variants to Staging/processed/archived/."""
    os.makedirs(ARCHIVE_DIR, exist_ok=True)
    # full_rel e.g. assets/images/street/full/000017060001.webp
    parts = full_rel.split("/")
    if len(parts) < 4:
        return 0
    cat_dir = "/".join(parts[:-2]) # assets/images/street
    fname = parts[-1]
    slug, _ = os.path.splitext(fname)

    candidates = [
        os.path.join(cat_dir, "full", f"{slug}.webp"),
        os.path.join(cat_dir, "full", f"{slug}.avif"),
        os.path.join(cat_dir, "thumbs", f"{slug}.webp"),
        os.path.join(cat_dir, "thumbs", f"{slug}.avif"),
        os.path.join(cat_dir, "thumbs", f"{slug}-400w.webp"),
        os.path.join(cat_dir, "thumbs", f"{slug}-400w.avif"),
    ]
    moved = 0
    for rel_c in candidates:
        abs_c = os.path.join(REPO_ROOT, rel_c)
        if os.path.exists(abs_c):
            dest_sub = os.path.join(ARCHIVE_DIR, rel_c)
            os.makedirs(os.path.dirname(dest_sub), exist_ok=True)
            shutil.move(abs_c, dest_sub)
            moved += 1
    return moved

def remove_photos_from_site(id_list):
    """Remove selected photo IDs (full_rel paths) from all gallery HTML files and archive assets."""
    target_set = set(id_list)
    removed_tags = 0

    for rel_page in GALLERY_FILES:
        abs_page = os.path.join(REPO_ROOT, rel_page)
        if not os.path.exists(abs_page):
            continue
        with open(abs_page, "r", encoding="utf-8") as f:
            content = f.read()

        def replace_img(match):
            nonlocal removed_tags
            tag = match.group(0)
            full_m = re.search(r'data-full="([^"]+)"', tag)
            src_m = re.search(r'src="([^"]+)"', tag)
            ref = (full_m.group(1) if full_m else (src_m.group(1) if src_m else "")).replace("../", "").lstrip("/")
            if ref in target_set:
                removed_tags += 1
                return ""
            return tag

        updated = re.sub(r'[ \t]*<img\s+[^>]+>\r?\n?', replace_img, content, flags=re.DOTALL)
        if updated != content:
            with open(abs_page, "w", encoding="utf-8") as f:
                f.write(updated)

    archived_files = 0
    for full_rel in target_set:
        archived_files += archive_asset_variants(full_rel)

    # Sync RSS & Sitemap & Pinterest CSVs
    subprocess.run([sys.executable, os.path.join(REPO_ROOT, "scripts", "generate-rss.py")], cwd=REPO_ROOT, check=False)
    subprocess.run([sys.executable, os.path.join(REPO_ROOT, "scripts", "export-pinterest-csv.py")], cwd=REPO_ROOT, check=False)

    return {
        "removed_photos": len(target_set),
        "removed_html_nodes": removed_tags,
        "archived_files": archived_files
    }

CURATE_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Curate Portfolio | Sawyer Knox</title>
  <style>
    :root {
      --bg: #f7f6f2;
      --card: #ffffff;
      --text: #181818;
      --muted: #6e6d68;
      --border: #e2e0d8;
      --danger: #c0392b;
      --danger-bg: rgba(192, 57, 43, 0.14);
      --accent: #111111;
    }
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Georgia, sans-serif;
      background: var(--bg);
      color: var(--text);
    }
    header {
      position: sticky;
      top: 0;
      z-index: 100;
      background: rgba(247, 246, 242, 0.96);
      backdrop-filter: blur(10px);
      border-bottom: 1px solid var(--border);
      padding: 14px 24px;
    }
    .top-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      max-width: 1440px;
      margin: 0 auto;
    }
    .brand {
      display: flex;
      align-items: baseline;
      gap: 12px;
    }
    .brand h1 {
      margin: 0;
      font-family: Georgia, serif;
      font-weight: 500;
      font-size: 1.35rem;
    }
    .brand span {
      font-size: 0.85rem;
      color: var(--muted);
    }
    .actions {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    button {
      border: 1px solid var(--border);
      background: var(--card);
      color: var(--text);
      padding: 8px 14px;
      border-radius: 5px;
      font-size: 0.85rem;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    button:hover:not(:disabled) {
      border-color: #888;
    }
    button:disabled {
      opacity: 0.45;
      cursor: not-allowed;
    }
    .btn-danger {
      background: var(--danger);
      color: #fff;
      border-color: var(--danger);
      font-weight: 600;
    }
    .btn-danger:hover:not(:disabled) {
      background: #a5281b;
      border-color: #a5281b;
    }
    .btn-primary {
      background: var(--accent);
      color: #fff;
      border-color: var(--accent);
      font-weight: 500;
    }
    .btn-primary:hover:not(:disabled) {
      background: #333;
    }
    .tabs-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      max-width: 1440px;
      margin: 12px auto 0;
      padding-top: 10px;
      border-top: 1px solid var(--border);
    }
    .tabs {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }
    .tab {
      padding: 6px 12px;
      border-radius: 999px;
      font-size: 0.8rem;
      background: transparent;
      border: 1px solid transparent;
      color: var(--muted);
    }
    .tab.active {
      background: var(--accent);
      color: #fff;
    }
    .search-box {
      padding: 6px 12px;
      border: 1px solid var(--border);
      border-radius: 5px;
      font-size: 0.85rem;
      min-width: 220px;
      background: #fff;
    }
    .status-banner {
      max-width: 1440px;
      margin: 14px auto 0;
      padding: 10px 16px;
      border-radius: 6px;
      background: #e8f5e9;
      color: #1b5e20;
      font-size: 0.88rem;
      display: none;
    }
    main {
      max-width: 1440px;
      margin: 20px auto 60px;
      padding: 0 24px;
    }
    .grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
      gap: 18px;
    }
    .card {
      background: var(--card);
      border: 2px solid transparent;
      border-radius: 6px;
      overflow: hidden;
      box-shadow: 0 2px 8px rgba(0,0,0,0.05);
      cursor: pointer;
      position: relative;
      transition: transform 0.12s ease, border-color 0.12s ease;
      user-select: none;
    }
    .card:hover {
      transform: translateY(-2px);
    }
    .card.selected {
      border-color: var(--danger);
      background: var(--danger-bg);
    }
    .thumb-wrap {
      position: relative;
      width: 100%;
      aspect-ratio: 3 / 2;
      background: #eceae4;
      overflow: hidden;
    }
    .card[data-orient="vertical"] .thumb-wrap {
      aspect-ratio: 2 / 3;
    }
    .card[data-orient="square"] .thumb-wrap {
      aspect-ratio: 1 / 1;
    }
    .thumb-wrap img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      display: block;
      transition: opacity 0.15s ease, filter 0.15s ease;
    }
    .card.selected .thumb-wrap img {
      opacity: 0.45;
      filter: grayscale(60%);
    }
    .remove-badge {
      position: absolute;
      top: 10px;
      left: 10px;
      background: var(--danger);
      color: #fff;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.06em;
      padding: 4px 8px;
      border-radius: 4px;
      display: none;
    }
    .card.selected .remove-badge {
      display: inline-block;
    }
    .zoom-btn {
      position: absolute;
      top: 8px;
      right: 8px;
      background: rgba(0,0,0,0.6);
      color: #fff;
      border: none;
      border-radius: 4px;
      padding: 4px 8px;
      font-size: 0.75rem;
      opacity: 0;
      transition: opacity 0.15s ease;
    }
    .card:hover .zoom-btn {
      opacity: 1;
    }
    .meta {
      padding: 10px 12px;
      font-size: 0.8rem;
    }
    .meta-title {
      font-weight: 600;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
      margin-bottom: 4px;
    }
    .meta-sub {
      color: var(--muted);
      font-size: 0.74rem;
      display: flex;
      justify-content: space-between;
    }
    .modal {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.88);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 999;
      padding: 24px;
    }
    .modal.open { display: flex; }
    .modal img {
      max-width: 92vw;
      max-height: 88vh;
      object-fit: contain;
    }
  </style>
</head>
<body>
  <header>
    <div class="top-row">
      <div class="brand">
        <h1>Sawyer Knox — Visual Portfolio Curator</h1>
        <span id="total-summary">Loading photos...</span>
      </div>
      <div class="actions">
        <button id="btn-clear" disabled>Clear Selection</button>
        <button id="btn-remove" class="btn-danger" disabled>Remove Selected (0)</button>
        <button id="btn-publish" class="btn-primary">Push Changes Live to Website</button>
      </div>
    </div>
    <div class="tabs-row">
      <div class="tabs" id="tabs">
        <button class="tab active" data-filter="all">All</button>
        <button class="tab" data-filter="35mm-bw-horizontal">35mm B&W Horizontal</button>
        <button class="tab" data-filter="35mm-bw-vertical">35mm B&W Vertical</button>
        <button class="tab" data-filter="35mm-color-horizontal">35mm Color Horizontal</button>
        <button class="tab" data-filter="35mm-color-vertical">35mm Color Vertical</button>
        <button class="tab" data-filter="120">120 Medium Format</button>
      </div>
      <input type="search" id="search" class="search-box" placeholder="Search caption or filename...">
    </div>
    <div id="banner" class="status-banner"></div>
  </header>

  <main>
    <div id="grid" class="grid"></div>
  </main>

  <div id="modal" class="modal" onclick="this.classList.remove('open')">
    <img id="modal-img" src="" alt="">
  </div>

  <script>
    let allPhotos = [];
    let selected = new Set();
    let currentFilter = "all";
    let lastClickedIndex = null;

    const grid = document.getElementById("grid");
    const btnClear = document.getElementById("btn-clear");
    const btnRemove = document.getElementById("btn-remove");
    const btnPublish = document.getElementById("btn-publish");
    const totalSummary = document.getElementById("total-summary");
    const banner = document.getElementById("banner");
    const searchInput = document.getElementById("search");

    function showBanner(msg, isError = false) {
      banner.textContent = msg;
      banner.style.display = "block";
      banner.style.background = isError ? "#fdecea" : "#e8f5e9";
      banner.style.color = isError ? "#b71c1c" : "#1b5e20";
    }

    function matchesFilter(p) {
      const q = searchInput.value.trim().toLowerCase();
      if (q && !p.caption.toLowerCase().includes(q) && !p.filename.toLowerCase().includes(q)) {
        return false;
      }
      if (currentFilter === "all") return true;
      if (currentFilter === "120") return p.format === "120";
      const [fmt, tone, orient] = currentFilter.split("-");
      return p.format === fmt && p.tone === tone && p.orientation === orient;
    }

    function updateButtons() {
      const count = selected.size;
      btnClear.disabled = count === 0;
      btnRemove.disabled = count === 0;
      btnRemove.textContent = `Remove Selected (${count})`;
      totalSummary.textContent = `${allPhotos.length} total photos on site · Click any photo to mark for removal (Shift+Click for range)`;
    }

    function updateTabCounts() {
      const counts = {
        "all": allPhotos.length,
        "35mm-bw-horizontal": allPhotos.filter(p => p.format === "35mm" && p.tone === "bw" && p.orientation === "horizontal").length,
        "35mm-bw-vertical": allPhotos.filter(p => p.format === "35mm" && p.tone === "bw" && p.orientation === "vertical").length,
        "35mm-color-horizontal": allPhotos.filter(p => p.format === "35mm" && p.tone === "color" && p.orientation === "horizontal").length,
        "35mm-color-vertical": allPhotos.filter(p => p.format === "35mm" && p.tone === "color" && p.orientation === "vertical").length,
        "120": allPhotos.filter(p => p.format === "120").length,
      };
      document.querySelectorAll(".tab").forEach(btn => {
        const key = btn.dataset.filter;
        const base = btn.dataset.label || btn.textContent;
        btn.dataset.label = base;
        btn.textContent = `${base} (${counts[key] || 0})`;
      });
    }

    function renderGrid() {
      const visible = allPhotos.filter(matchesFilter);
      grid.innerHTML = "";
      visible.forEach((p, idx) => {
        const card = document.createElement("div");
        card.className = "card" + (selected.has(p.id) ? " selected" : "");
        card.dataset.orient = p.orientation;
        card.innerHTML = `
          <div class="thumb-wrap">
            <img src="${p.thumb_url}" loading="lazy" alt="">
            <span class="remove-badge">MARKED TO REMOVE</span>
            <button class="zoom-btn" title="View Full Size">Zoom</button>
          </div>
          <div class="meta">
            <div class="meta-title" title="${p.caption || p.filename}">${p.caption || "Untitled"}</div>
            <div class="meta-sub">
              <span>${p.filename}</span>
              <span>${p.format.toUpperCase()} · ${p.tone.toUpperCase()}</span>
            </div>
          </div>
        `;
        card.querySelector(".zoom-btn").addEventListener("click", (e) => {
          e.stopPropagation();
          document.getElementById("modal-img").src = p.full_url;
          document.getElementById("modal").classList.add("open");
        });
        card.addEventListener("click", (e) => {
          if (e.shiftKey && lastClickedIndex !== null) {
            const start = Math.min(lastClickedIndex, idx);
            const end = Math.max(lastClickedIndex, idx);
            const shouldSelect = !selected.has(p.id);
            for (let i = start; i <= end; i++) {
              if (shouldSelect) selected.add(visible[i].id);
              else selected.delete(visible[i].id);
            }
          } else {
            if (selected.has(p.id)) selected.delete(p.id);
            else selected.add(p.id);
            lastClickedIndex = idx;
          }
          renderGrid();
          updateButtons();
        });
        grid.appendChild(card);
      });
      updateButtons();
    }

    async function loadPhotos() {
      const res = await fetch("/api/photos");
      allPhotos = await res.json();
      updateTabCounts();
      renderGrid();
    }

    document.querySelectorAll(".tab").forEach(btn => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".tab").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        currentFilter = btn.dataset.filter;
        lastClickedIndex = null;
        renderGrid();
      });
    });

    searchInput.addEventListener("input", renderGrid);

    btnClear.addEventListener("click", () => {
      selected.clear();
      renderGrid();
    });

    btnRemove.addEventListener("click", async () => {
      const count = selected.size;
      if (!count) return;
      if (!confirm(`Remove ${count} selected photo(s) from the website? (Files will be safely moved to Staging/processed/archived/)`)) {
        return;
      }
      btnRemove.disabled = true;
      btnRemove.textContent = "Removing...";
      try {
        const res = await fetch("/api/remove", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ ids: Array.from(selected) })
        });
        const data = await res.json();
        selected.clear();
        await loadPhotos();
        showBanner(`Removed ${data.removed_photos} photo(s) from HTML & archived ${data.archived_files} image files. Click "Push Changes Live to Website" when ready!`);
      } catch (err) {
        showBanner("Error removing photos: " + err, true);
      }
    });

    btnPublish.addEventListener("click", async () => {
      btnPublish.disabled = true;
      btnPublish.textContent = "Pushing Live to GitHub...";
      try {
        const res = await fetch("/api/publish", { method: "POST" });
        const data = await res.json();
        if (data.ok) {
          showBanner("Pushed live to https://sjkonfilm.work! GitHub Pages and IndexNow updated.");
        } else {
          showBanner("Publish error: " + data.error, true);
        }
      } catch (err) {
        showBanner("Publish request failed: " + err, true);
      } finally {
        btnPublish.disabled = false;
        btnPublish.textContent = "Push Changes Live to Website";
      }
    });

    loadPhotos();
  </script>
</body>
</html>
"""

class CurateRequestHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=REPO_ROOT, **kwargs)

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path in ("/curate", "/curate/"):
            body = CURATE_HTML.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if parsed.path == "/api/photos":
            data = json.dumps(parse_all_photos()).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        return super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/remove":
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length).decode("utf-8")
            payload = json.loads(raw)
            result = remove_photos_from_site(payload.get("ids", []))
            out = json.dumps(result).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(out)))
            self.end_headers()
            self.wfile.write(out)
            return
        if parsed.path == "/api/publish":
            try:
                subprocess.run([sys.executable, os.path.join(REPO_ROOT, "scripts", "publish.py")], cwd=REPO_ROOT, check=True)
                out = json.dumps({"ok": True}).encode("utf-8")
            except Exception as e:
                out = json.dumps({"ok": False, "error": str(e)}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(out)))
            self.end_headers()
            self.wfile.write(out)
            return
        self.send_error(404)

def find_open_port(start_port=8080):
    for port in range(start_port, start_port + 20):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
    return start_port

def main():
    os.chdir(REPO_ROOT)
    port = find_open_port(8080)
    url = f"http://localhost:{port}/curate"
    server = HTTPServer(("127.0.0.1", port), CurateRequestHandler)
    print(f"Visual Portfolio Curator running at: {url}")
    print("Press Ctrl+C to stop.")
    if "--no-open" not in sys.argv:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped Visual Portfolio Curator.")

if __name__ == "__main__":
    main()
