#!/usr/bin/env python3
"""
Automated Search Engine Pinging & Indexing Request Tool for sjkonfilm.work
Sends indexing requests to IndexNow (Bing, Yandex, Seznam) and Google Search Console.
"""

import os
import sys
import json
import urllib.request
import urllib.parse

SITE_URL = "https://sjkonfilm.work"
INDEXNOW_KEY = os.environ.get("INDEXNOW_KEY", "sjkonfilm_indexnow_key_2026")

SITEMAP_URLS = [
    f"{SITE_URL}/",
    f"{SITE_URL}/works.html",
    f"{SITE_URL}/about.html",
    f"{SITE_URL}/contact.html",
    f"{SITE_URL}/pages/street.html",
    f"{SITE_URL}/pages/scenes.html",
    f"{SITE_URL}/pages/color.html",
    f"{SITE_URL}/pages/vertical.html",
    f"{SITE_URL}/pages/120.html"
]

def ping_google_sitemap():
    """Ping Google with sitemap update."""
    sitemap_url = f"{SITE_URL}/sitemap.xml"
    ping_url = f"https://www.google.com/ping?sitemap={urllib.parse.quote(sitemap_url)}"
    try:
        req = urllib.request.Request(ping_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            print(f"Pinged Google Sitemap ({resp.status})")
    except Exception as e:
        print(f"Google sitemap ping note: {e}")

def ping_indexnow():
    """Send IndexNow notification for instant search engine indexing."""
    endpoint = "https://api.indexnow.org/indexnow"
    payload = {
        "host": "sjkonfilm.work",
        "key": INDEXNOW_KEY,
        "keyLocation": f"{SITE_URL}/{INDEXNOW_KEY}.txt",
        "urlList": SITEMAP_URLS
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        endpoint,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"}
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"IndexNow API response code: {resp.status}")
    except Exception as e:
        print(f"IndexNow API submission: {e}")

def main():
    print("Sending search engine indexing pings...")
    ping_google_sitemap()
    ping_indexnow()
    print("Search engine ping completed.")

if __name__ == "__main__":
    main()
