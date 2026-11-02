#!/usr/bin/env python3
"""
One-Step Automated Publisher for sjkonfilm.work
Processes any scans in Staging/, updates galleries, RSS feed, Google Image Sitemap,
and Pinterest CSVs, commits changes if needed, pushes to GitHub, and pings IndexNow.
"""

import os
import sys
import glob
import subprocess
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def has_staged_scans():
    exts = ("*.jpg", "*.jpeg", "*.webp", "*.png", "*.JPG", "*.JPEG", "*.WEBP", "*.PNG")
    found = []
    for root, dirs, _ in os.walk(os.path.join(REPO_ROOT, "Staging")):
        if "processed" in root.split(os.sep):
            continue
        for ext in exts:
            found.extend(glob.glob(os.path.join(root, ext)))
    return found

def main():
    os.chdir(REPO_ROOT)
    env = os.environ.copy()
    if "/opt/homebrew/bin" not in env.get("PATH", ""):
        env["PATH"] = f"/opt/homebrew/bin:{env.get('PATH', '')}"

    staged_files = has_staged_scans()
    if staged_files:
        print(f"Found {len(staged_files)} scan(s) in Staging/. Running automated pipeline...")
        subprocess.run([sys.executable, "scripts/process-staging.py"] + sys.argv[1:], env=env, check=True)
    else:
        subprocess.run([sys.executable, "scripts/generate-rss.py"], env=env, check=True)
        subprocess.run([sys.executable, "scripts/export-pinterest-csv.py"], env=env, check=True)

    # Check if there are changes to commit
    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True).stdout.strip()
    if status:
        subprocess.run([
            "git", "add",
            "assets/images/", "pages/", "index.html", "works.html",
            "about.html", "contact.html", "style.css", "Lightbox.js",
            "rss.xml", "sitemap.xml", "AGENTS.md", "GEMINI.md", "scripts/"
        ], check=False)
        staged_diff = subprocess.run(["git", "diff", "--cached", "--quiet"])
        if staged_diff.returncode != 0:
            now_str = datetime.now().strftime("%Y-%m-%d")
            msg = f"feat(gallery): auto-publish staged film scans and update feeds ({now_str})"
            subprocess.run(["git", "commit", "-m", msg], check=True)

    print("Pushing to GitHub (origin main)...")
    subprocess.run(["git", "push", "origin", "main"], env=env, check=True)

    print("Pinging search engines (IndexNow)...")
    subprocess.run([sys.executable, "scripts/ping-search-engines.py"], env=env, check=False)
    print("\nAll done! Live deployment, RSS auto-pinning, and search engine indexing triggered.")

if __name__ == "__main__":
    main()
