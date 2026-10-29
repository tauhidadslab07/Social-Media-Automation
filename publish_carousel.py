import os
import sys
from dotenv import load_dotenv

load_dotenv()

from content_engine import get_current_day_config
from carousel_engine import build_daily_carousel, build_shopify_ga4_carousel
from social_poster import (
    post_carousel_to_facebook,
    post_carousel_to_instagram,
    post_carousel_to_linkedin,
    post_document_to_linkedin
)

BRAND_NAME = os.getenv("BRAND_NAME", "Tauhid Ads Lab")
BRAND_PHONE = os.getenv("BRAND_PHONE", "+8801624608468")
BRAND_WEBSITE = os.getenv("BRAND_WEBSITE", "http://tauhidadslab.com/")
BRAND_CALENDLY = os.getenv("BRAND_CALENDLY", "https://calendly.com/tauhidadslab/30min")

def build_carousel_caption(day_cfg):
    """
    Constructs high-converting, contrarian copy tailored to the day's carousel topic.
    """
    if not day_cfg or day_cfg.get("day", 1) == 1:
        return f"""If your Shopify dashboard and GA4 revenue don't match, your ad platforms are optimizing on fiction. 🚨

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

    title = day_cfg.get("title", "Server-Side Tracking Architecture")
    core_concept = day_cfg.get("core_concept", "Why client-side pixels fail to capture modern multi-device journeys.")
    bullets = day_cfg.get("bullet_points", [
        "100% First-Party Data Pipeline",
        "Ad-Blocker & Safari ITP Immune",
        "Unique Event ID Deduplication",
        "Lower Ad CPA & Predictable Scaling"
    ])
    bullet_text = "\n".join([f"👉 {b}" for b in bullets])

    return f"""Stop letting client-side pixel drops destroy your ad performance. 🚨

Topic: {title}

Here is what most performance marketers don't realize:
{core_concept}

Why this directly hits your bottom line:
{bullet_text}

When you move tracking to a private Server-Side GTM container, your ad algorithms receive clean, unadulterated conversion signals.

Swipe through this 7-slide blueprint to see the exact technical architecture. ➡

🎯 Ready to future-proof your tracking stack?
📅 Book a Free 30-Min Audit: {BRAND_CALENDLY}
🌐 Agency Case Studies: {BRAND_WEBSITE}
💬 WhatsApp / Direct Line: {BRAND_PHONE}

#ServerSideTracking #MetaCAPI #GoogleAds #GA4 #Attribution #TauhidAdsLab"""

def run_carousel_publish():
    print("=" * 70)
    print("🚀 Tauhid Ads Lab - Multi-Channel Carousel Publishing Engine")
    print("=" * 70)

    # 1. Determine active day config
    day_cfg = get_current_day_config()
    day_num = day_cfg.get("day", 1) if day_cfg else 1
    topic_title = day_cfg.get("title", "Why Your Shopify Revenue and GA4 Sales Never Match") if day_cfg else "Why Your Shopify Revenue and GA4 Sales Never Match"
    
    print(f"🎯 Active Topic (Day {day_num}): {topic_title}")

    # 2. Generate 7-Slide Deck and Compiled PDF Document
    print("\n[1/3] Generating 7-Slide Minimalist Swiss Deck & Compiled PDF...")
    image_paths, pdf_path = build_daily_carousel(day_cfg)
    print(f"-> Generated {len(image_paths)} individual slide images for Facebook & Instagram")
    print(f"-> Generated PDF Document Carousel for LinkedIn: {pdf_path}")

    caption = build_carousel_caption(day_cfg)

    # 3. Publish to Channels
    print("\n[2/3] Publishing to Channels...")
    results = {}

    # Facebook Page Carousel
    print("\n--- 🔵 Publishing Multi-Image Carousel to Facebook Page ---")
    results["Facebook Page Carousel"] = post_carousel_to_facebook(image_paths, caption)

    # Instagram Carousel
    enable_ig = os.getenv("ENABLE_INSTAGRAM", "True").lower() in ("true", "1", "yes")
    if enable_ig:
        print("\n--- 📸 Publishing Swipeable Carousel to Instagram (@tauhidadslab) ---")
        results["Instagram Carousel"] = post_carousel_to_instagram(image_paths, caption)

    # LinkedIn Carousel Post (Multi-Image Carousel)
    print("\n--- 💼 Publishing Swipeable Multi-Image Carousel to LinkedIn ---")
    results["LinkedIn Carousel"] = post_carousel_to_linkedin(image_paths, caption)

    # 4. Summary
    print("\n" + "=" * 70)
    print("📊 Carousel Publishing Summary:")
    for platform, status in results.items():
        state = "✅ Successfully Published" if status else "⚠️ Skipped / Check Credentials"
        print(f"  - {platform}: {state}")
    print("=" * 70)

if __name__ == "__main__":
    run_carousel_publish()
