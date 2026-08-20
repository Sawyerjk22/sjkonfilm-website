#!/usr/bin/env python3
"""
Dynamic Popularity Gallery Reordering Engine for sjkonfilm.work
Pulls global engagement metrics (GA4 Data API or local metrics file)
and physically re-sorts static HTML gallery DOM nodes by popularity.
"""

import os
import re
import glob
import json
import argparse
from pathlib import Path

# Optional Google Analytics Data API import
try:
    from google.analytics.data_v1beta import BetaAnalyticsDataClient  # type: ignore
    from google.analytics.data_v1beta.types import RunReportRequest, Metric, Dimension  # type: ignore
    GA_AVAILABLE = True
except ImportError:
    GA_AVAILABLE = False

METRICS_FILE = "popularity_metrics.json"

def fetch_ga4_metrics(property_id):
    """Fetch image view events from GA4 Data API if credentials exist."""
    if not GA_AVAILABLE or not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        print("GA4 API client or credentials not configured. Using local popularity_metrics.json.")
        return load_local_metrics()

    client = BetaAnalyticsDataClient()
    request = RunReportRequest(
        property=f"properties/{property_id}",
        dimensions=[Dimension(name="pagePath"), Dimension(name="customEvent:image_id")],
        metrics=[Metric(name="eventCount")],
    )
    
    metrics = {}
    try:
        response = client.run_report(request)
        for row in response.rows:
            image_id = row.dimension_values[1].value
            count = int(row.metric_values[0].value)
            if image_id:
                metrics[image_id] = metrics.get(image_id, 0) + count
        print(f"Fetched GA4 popularity metrics for {len(metrics)} photos.")
        save_metrics(metrics)
        return metrics
    except Exception as e:
        print(f"Error fetching GA4 metrics: {e}. Falling back to local metrics.")
        return load_local_metrics()

def load_local_metrics():
    """Load cached popularity metrics from JSON file."""
    if os.path.exists(METRICS_FILE):
        with open(METRICS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_metrics(metrics):
    """Cache popularity metrics locally."""
    with open(METRICS_FILE, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

def extract_image_id(img_tag):
    """Extract unique image identifier or filename from data-full/src."""
    match = re.search(r'data-full="([^"]+)"', img_tag)
    if match:
        return os.path.basename(match.group(1))
    src_match = re.search(r'src="([^"]+)"', img_tag)
    if src_match:
        return os.path.basename(src_match.group(1))
    return img_tag

def reorder_gallery_html(filepath, metrics):
    """Re-sort <img> tags inside <section class="gallery"> by view count."""
    if not os.path.exists(filepath):
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    sec_match = re.search(r'(<section class="gallery">)(.*?)(</section>)', content, re.DOTALL)
    if not sec_match:
        return

    opening_tag, inner_html, closing_tag = sec_match.groups()
    
    # Extract all <img> tags
    img_tags = re.findall(r'<img\s+[^>]+>', inner_html)
    if not img_tags:
        return

    # Sort img_tags based on metrics score (higher score first)
    def sort_key(img_tag):
        img_id = extract_image_id(img_tag)
        return metrics.get(img_id, 0)

    # Sort descending by score, maintaining relative order for ties
    sorted_img_tags = sorted(img_tags, key=sort_key, reverse=True)

    # Reconstruct inner gallery HTML
    new_inner_html = "\n      " + "\n      ".join(sorted_img_tags) + "\n    "
    new_content = content.replace(f"{opening_tag}{inner_html}{closing_tag}", f"{opening_tag}{new_inner_html}{closing_tag}")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"Reordered {len(sorted_img_tags)} gallery photos in {filepath} based on popularity.")

def main():
    parser = argparse.ArgumentParser(description="Reorder static HTML gallery images by popularity.")
    parser.add_argument("--property-id", help="Google Analytics 4 Property ID")
    parser.add_argument("--mock-data", action="store_true", help="Generate sample metrics for demonstration.")
    args = parser.parse_args()

    metrics = {}
    if args.property_id:
        metrics = fetch_ga4_metrics(args.property_id)
    else:
        metrics = load_local_metrics()

    if args.mock_data or not metrics:
        print("Using or updating sample popularity metrics...")
        # Fill empty metrics if needed
        all_imgs = glob.glob("assets/images/*/thumbs/*.webp")
        for i, img_path in enumerate(all_imgs):
            fname = os.path.basename(img_path)
            if "-400w" not in fname and fname not in metrics:
                metrics[fname] = max(0, 100 - i * 2)
        save_metrics(metrics)

    pages = glob.glob("pages/*.html")
    for page in pages:
        reorder_gallery_html(page, metrics)

if __name__ == "__main__":
    main()
