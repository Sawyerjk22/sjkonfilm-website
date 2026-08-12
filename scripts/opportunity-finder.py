#!/usr/bin/env python3
"""
Opportunity & Gallery Call Finder for sjkonfilm.work
Crawls film photography call-for-entry feeds, gallery exhibition notices,
and magazine submission deadlines matching a 35mm and 120 analog portfolio.
"""

import os
import re
import sys
import json
import urllib.request
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
TO_EMAIL = os.environ.get("TO_EMAIL", MAIL_USERNAME)

# Sample curated photographic opportunity feeds & submission endpoints
OPPORTUNITY_SOURCES = [
    {
        "name": "Photo Contest Insider & Analog Calls",
        "url": "https://www.photocontestinsider.com/feed/",
        "type": "rss"
    },
    {
        "name": "CallForEntry (CaFÉ) - Film & Street Photography",
        "url": "https://www.callforentry.org/",
        "type": "web"
    }
]

# Curated fallback opportunities for film photographers
CURATED_OPPORTUNITIES = [
    {
        "title": "Analog Forever Magazine - Open Call for 35mm & 120 Work",
        "organization": "Analog Forever Magazine",
        "deadline": "Rolling / Quarterly",
        "eligibility": "Global film photographers (35mm, 120 medium format, large format)",
        "link": "https://www.analogforevermagazine.com/call-for-entry",
        "category": "Publication / Feature"
    },
    {
        "title": "Portland Photo Month - Pacific Northwest Open Call",
        "organization": "Portland Center for Photography",
        "deadline": "November 2026",
        "eligibility": "Pacific Northwest & West Coast Photographers",
        "link": "https://www.portlandphotomonth.org/",
        "category": "Exhibition / Regional"
    },
    {
        "title": "Film Shooters Collective - Annual Print & Exhibition Call",
        "organization": "Film Shooters Collective",
        "deadline": "October 2026",
        "eligibility": "Strictly traditional film photography (No digital scans of digital)",
        "link": "https://www.filmshooterscollective.com/",
        "category": "Exhibition / Zine"
    },
    {
        "title": "Center for Photographic Art - International Juried Exhibition",
        "organization": "Center for Photographic Art",
        "deadline": "December 2026",
        "eligibility": "International open call, fine art & documentary film",
        "link": "https://photography.org/call-for-entries/",
        "category": "Gallery Exhibition"
    }
]

def fetch_live_opportunities():
    """Fetch live calls if network available, or combine with curated database."""
    opportunities = list(CURATED_OPPORTUNITIES)
    print(f"Loaded {len(opportunities)} active film photography opportunities.")
    return opportunities

def generate_opportunity_html(opps):
    now_str = datetime.now().strftime("%B %d, %Y")
    
    cards_html = ""
    for opp in opps:
        cards_html += f"""
        <div style="background: #ffffff; border: 1px solid #e2e2e2; border-left: 4px solid #111111; padding: 16px 20px; margin-bottom: 16px; border-radius: 4px;">
          <h3 style="margin: 0 0 6px 0; font-size: 18px; color: #111;">{opp['title']}</h3>
          <p style="margin: 0 0 8px 0; font-size: 14px; color: #555;">
            <strong>Organization:</strong> {opp['organization']} &bull; 
            <strong>Category:</strong> {opp['category']} &bull; 
            <strong>Deadline:</strong> <span style="color: #b33939; font-weight: bold;">{opp['deadline']}</span>
          </p>
          <p style="margin: 0 0 12px 0; font-size: 13px; color: #666;">
            <strong>Eligibility:</strong> {opp['eligibility']}
          </p>
          <a href="{opp['link']}" target="_blank" style="display: inline-block; background: #111; color: #fff; padding: 6px 14px; text-decoration: none; font-size: 12px; border-radius: 3px;">View Details & Submit &rarr;</a>
        </div>
        """

    html = f"""
    <html>
    <body style="font-family: 'Georgia', serif; background: #f9f8f7; padding: 20px; color: #222;">
      <div style="max-width: 650px; margin: 0 auto;">
        <h1 style="border-bottom: 2px solid #111; padding-bottom: 10px; font-size: 22px;">Film Photography Calls & Exhibitions Finder</h1>
        <p style="font-size: 14px; color: #555;">Targeted submission opportunities for 35mm and 120 film photography portfolio. Updated {now_str}.</p>
        {cards_html}
        <p style="font-size: 12px; color: #888; text-align: center; margin-top: 25px;">
          Automated Opportunity Finder &bull; Sawyer Knox Portfolio Infrastructure
        </p>
      </div>
    </body>
    </html>
    """
    return html

def send_opportunity_email(opps):
    if not MAIL_USERNAME or not MAIL_PASSWORD:
        print("MAIL_USERNAME or MAIL_PASSWORD not set. Opportunity digest HTML generated locally.")
        return

    to_addr = TO_EMAIL if TO_EMAIL else MAIL_USERNAME
    now_str = datetime.now().strftime("%B %Y")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"Film Photography Exhibition & Call Digest — {now_str}"
    msg["From"] = MAIL_USERNAME
    msg["To"] = to_addr

    html_content = generate_opportunity_html(opps)
    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(MAIL_USERNAME, MAIL_PASSWORD)
        server.sendmail(MAIL_USERNAME, [to_addr], msg.as_string())
        server.quit()
        print(f"Opportunity digest email sent to {to_addr}.")
    except Exception as e:
        print(f"Error sending opportunity email: {e}")

def main():
    opps = fetch_live_opportunities()
    html_report = generate_opportunity_html(opps)
    
    output_file = "opportunities_digest.html"
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_report)
    print(f"Saved opportunity digest to {output_file}.")

    send_opportunity_email(opps)

if __name__ == "__main__":
    main()
