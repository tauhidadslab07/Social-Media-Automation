import os
import sys
from dotenv import load_dotenv

load_dotenv()

from carousel_engine import build_shopify_ga4_carousel
from social_poster import (
    post_carousel_to_facebook,
    post_carousel_to_instagram,
    post_document_to_linkedin
)

BRAND_NAME = os.getenv("BRAND_NAME", "Tauhid Ads Lab")
BRAND_PHONE = os.getenv("BRAND_PHONE", "+8801624608468")
BRAND_WEBSITE = os.getenv("BRAND_WEBSITE", "http://tauhidadslab.com/")
BRAND_CALENDLY = os.getenv("BRAND_CALENDLY", "https://calendly.com/tauhidadslab/30min")

SHORT_CAPTION = f"""If your Shopify dashboard and GA4 revenue don't match, your ad platforms are optimizing on fiction. 🚨

Most e-commerce store owners think their ad campaigns are failing, when in reality their client-side tracking is leaking:
👉 Thank-you page refreshes trigger duplicate purchases and inflate your reported ROAS.
👉 Offsite payment redirects (PayPal, Klarna, Apple Pay) fail to return to your confirmation page.
👉 Ad-blockers and Safari ITP hide 25%+ of completed checkouts from your analytics.

When Meta and Google receive distorted conversion signals, their AI bids on the wrong prospects and your Cost Per Acquisition (CPA) skyrockets.

Swipe through this 7-slide blueprint to see how we fix it 1:1 using Server-Side GTM (sGTM) and Webhook deduplication. ➡

🎯 Ready to reconcile your revenue 1:1?
📅 Book a Free 30-Min Audit: {BRAND_CALENDLY}
🌐 Agency Case Studies: {BRAND_WEBSITE}
💬 WhatsApp / Direct Line: {BRAND_PHONE}

#Shopify #GA4 #ServerSideTracking #EcommerceTracking #MetaCAPI #TauhidAdsLab"""

def run_carousel_publish():
    print("=" * 70)
    print("🚀 Tauhid Ads Lab - Multi-Channel Carousel Publishing Engine")
    print("🎯 Topic: Why Your Shopify Revenue and GA4 Sales Never Match")
    print("=" * 70)

    # 1. Generate 7-Slide Deck and Compiled PDF Document
    print("\n[1/3] Generating 7-Slide Carousel Graphics & Compiled PDF...")
    image_paths, pdf_path = build_shopify_ga4_carousel()
    print(f"-> Generated {len(image_paths)} individual slide images for Facebook & Instagram")
    print(f"-> Generated PDF Document Carousel for LinkedIn: {pdf_path}")

    # 2. Publish to Channels
    print("\n[2/3] Publishing to Channels...")
    results = {}

    # Facebook Page Carousel
    print("\n--- 🔵 Publishing Multi-Image Carousel to Facebook Page ---")
    results["Facebook Page Carousel"] = post_carousel_to_facebook(image_paths, SHORT_CAPTION)

    # Instagram Carousel
    enable_ig = os.getenv("ENABLE_INSTAGRAM", "True").lower() in ("true", "1", "yes")
    if enable_ig:
        print("\n--- 📸 Publishing Swipeable Carousel to Instagram (@tauhidadslab) ---")
        results["Instagram Carousel"] = post_carousel_to_instagram(image_paths, SHORT_CAPTION)

    # LinkedIn Document Carousel (PDF)
    print("\n--- 💼 Publishing Document Carousel (PDF) to LinkedIn ---")
    results["LinkedIn PDF Carousel"] = post_document_to_linkedin(
        pdf_path,
        SHORT_CAPTION,
        title="Why Your Shopify Revenue & GA4 Sales Never Match"
    )

    # 3. Summary
    print("\n" + "=" * 70)
    print("📊 Carousel Publishing Summary:")
    for platform, status in results.items():
        state = "✅ Successfully Published" if status else "⚠️ Skipped / Check Credentials"
        print(f"  - {platform}: {state}")
    print("=" * 70)

if __name__ == "__main__":
    run_carousel_publish()
