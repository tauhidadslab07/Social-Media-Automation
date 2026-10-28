import os
import re
import json
import random
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BRAND_NAME = os.getenv("BRAND_NAME", "Tauhid Ads Lab")
BRAND_PHONE = os.getenv("BRAND_PHONE", "+8801624608468")
BRAND_WEBSITE = os.getenv("BRAND_WEBSITE", "http://tauhidadslab.com/")
BRAND_CALENDLY = os.getenv("BRAND_CALENDLY", "https://calendly.com/tauhidadslab/30min")

def to_unicode_bold(text):
    """
    Converts standard alphanumeric characters into real Unicode Bold Sans-Serif
    so they render as TRUE BOLD text on Facebook and LinkedIn feeds!
    """
    result = []
    for char in text:
        code = ord(char)
        if 65 <= code <= 90:
            result.append(chr(code - 65 + 0x1D5D4))
        elif 97 <= code <= 122:
            result.append(chr(code - 97 + 0x1D5EE))
        elif 48 <= code <= 57:
            result.append(chr(code - 48 + 0x1D7EC))
        else:
            result.append(char)
    return "".join(result)

def format_markdown_bold(text):
    """
    Finds all **bold text** in markdown and converts it to true Unicode bold
    for social media feeds.
    """
    def replacer(match):
        inner_text = match.group(1)
        return to_unicode_bold(inner_text)
    return re.sub(r'\*\*(.+?)\*\*', replacer, text)

def get_current_day_config():
    """
    Loads topics.json and determines the active day (1 to 10).
    Checks TOPIC_DAY env var first, otherwise computes from 2026-10-23 in BST (UTC+6).
    """
    topics_file = os.path.join(os.path.dirname(__file__), "topics.json")
    if not os.path.exists(topics_file):
        return None

    try:
        with open(topics_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"[Content Engine] Error reading topics.json: {e}")
        return None

    days = data.get("days", [])
    if not days:
        return None

    # Check override from env var
    env_day = os.getenv("TOPIC_DAY")
    if env_day and env_day.isdigit():
        target_day = int(env_day)
        for d in days:
            if d.get("day") == target_day:
                return d

    # Calculate from start_date in BST (Bangladesh Time = UTC+6)
    try:
        start_str = data.get("start_date", "2026-10-23")
        start_date = datetime.strptime(start_str, "%Y-%m-%d").date()
        bst_now = datetime.now(timezone.utc) + timedelta(hours=6)
        current_date = bst_now.date()
        diff = (current_date - start_date).days
        day_num = (diff % len(days)) + 1
        for d in days:
            if d.get("day") == day_num:
                return d
    except Exception as e:
        print(f"[Content Engine] Date calculation fallback: {e}")

    return days[0]

def generate_dual_social_post():
    """
    Generates high-converting, 100% ENGLISH social media posts strictly matching
    the curated 10-day calendar (Google Ads vs Conversion Tracking).
    """
    day_cfg = get_current_day_config()
    if not day_cfg:
        # Emergency fallback config
        day_cfg = {
            "day": 1,
            "pillar": "SERVER_SIDE_TRACKING",
            "title": "Why Browser Pixels Miss 30% of Your Real Conversions",
            "badge": "SERVER-SIDE · BASICS",
            "core_concept": "Browser pixels losing conversions due to ad blockers, Safari ITP, and third-party cookie restrictions.",
            "target_audience": "E-Commerce Founders, DTC Brands & Marketing Agencies",
            "goal": "Educate on invisible data loss and position Server-Side Tracking as the essential solution.",
            "graphic_title_line1": "BROWSER PIXELS ARE DEAD",
            "graphic_title_line2": "SWITCH TO SERVER-SIDE",
            "graphic_subtitle": "Recover 25-35% of lost conversions blocked by browser shields.",
            "bullet_points": [
                "Ad-Blocker Immune Tracking",
                "Bypass iOS 14.5+ Shielding",
                "First-Party Server Routing",
                "Recover Hidden Purchases"
            ],
            "cta_text": "UPGRADE TO SGTM"
        }

    pillar = day_cfg.get("pillar", "GOOGLE_ADS")
    
    if not GEMINI_API_KEY:
        print("[Content Engine] No GEMINI_API_KEY found, using curated fallback for Day", day_cfg.get("day", 1))
        return get_day_fallback(day_cfg)

    models_to_try = ["gemini-3.5-flash", "gemini-3-flash-preview", "gemini-flash-latest"]
    
    if pillar == "GOOGLE_ADS":
        strict_instruction = f"""
STRICT NICHE MANDATE: This post must be 100% STRICTLY ABOUT GOOGLE ADS FOR LOCAL BUSINESSES (Doctors, Dentists, Lawyers, Clinics, Home Services, Real Estate, Local Stores).
- Do NOT talk about Facebook or Instagram ads as a good option. Contrast Facebook boosting (interruption, tire-kickers) with Google Search Ads (urgent high-intent buyers ready with credit cards).
- Focus on: {day_cfg.get('core_concept')}.
- Tone: High-authority, practical, showing local business owners how to stop burning cash on useless clicks and start getting inbound phone calls and booked appointments.
"""
    else:
        strict_instruction = f"""
STRICT NICHE MANDATE: This post must be 100% STRICTLY ABOUT ADVANCED CONVERSION TRACKING & WEB ANALYTICS (GTM, GA4, Server-Side Tracking, Meta Conversions API / CAPI, Enhanced Conversions across all niches: Shopify, WordPress, WooCommerce, Lead Gen).
- Focus on: {day_cfg.get('core_concept')}.
- Tone: Highly technical yet accessible, expert data architect, demonstrating that running ads with broken tracking is like pouring water into a leaky bucket.
"""

    prompt = f"""
You are the Chief Growth Strategist & Technical Lead at '{BRAND_NAME}', an elite performance marketing and tracking agency led by Md. Tauhidul Islam Bhuian.
Agency Contact Details:
- Website: {BRAND_WEBSITE}
- Free 30-Min Strategy Call (Calendly): {BRAND_CALENDLY}
- Phone / WhatsApp: {BRAND_PHONE}

TODAY IS DAY {day_cfg.get('day')} OF OUR 30-DAY CAMPAIGN.
STAGE: {day_cfg.get('badge')}
TOPIC TITLE: "{day_cfg.get('title')}"
TARGET AUDIENCE: {day_cfg.get('target_audience')}
CORE GOAL: {day_cfg.get('goal')}

{strict_instruction}

CRITICAL COPYWRITING ARCHITECTURE:
1. LANGUAGE: 100% ENGLISH ONLY. Flawless, punchy, persuasive American/International English.
2. HOOK: First sentence must be a bold, scroll-stopping contrarian hook in **bold**.
3. REAL BOTTLENECK: Explain clearly why common methods fail and burn budget.
4. ACTIONABLE FRAMEWORK: Break down the solution into 2 to 3 bullet points with emojis (✔, 🚀, 💡, 📞, 🎯) and **bold titles**.
5. THE AHA MOMENT: Contrast interruption vs intent (e.g. scrolling sofa vs urgent emergency search / paying customers vs cheap form-fills).
6. ENGAGEMENT QUESTION: End with a direct question to Founders, Local Business Owners, or Agency Heads.
7. CALL TO ACTION & LINKS:
   - Free 30-Min Consultation: {BRAND_CALENDLY}
   - Website: {BRAND_WEBSITE}
   - Phone / WhatsApp: {BRAND_PHONE}
8. BOLDING: Use **double asterisks** around critical headlines and bullet points so our system converts them to TRUE BOLD on Facebook and LinkedIn.

The response MUST be valid JSON with the following exact keys:
{{
  "category": "{day_cfg.get('badge')}",
  "graphic_title_line1": "{day_cfg.get('graphic_title_line1')}",
  "graphic_title_line2": "{day_cfg.get('graphic_title_line2')}",
  "graphic_subtitle": "{day_cfg.get('graphic_subtitle')}",
  "bullet_points": {json.dumps(day_cfg.get('bullet_points', []))},
  "cta_text": "{day_cfg.get('cta_text', 'BOOK FREE AUDIT')}",
  "facebook_caption": "Complete formatted 100% English Facebook post using **bold** markers...",
  "facebook_hashtags": "#TauhidAdsLab #GoogleAds #LocalBusiness #Tracking #Day{day_cfg.get('day')}",
  "linkedin_caption": "Complete formatted 100% English LinkedIn post using **bold** markers...",
  "linkedin_hashtags": "#PerformanceMarketing #GoogleAds #LocalSEO #TauhidAdsLab #Day{day_cfg.get('day')}"
}}

Output ONLY valid raw JSON without markdown code fences or backticks.
"""

    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={GEMINI_API_KEY}"
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            if response.status_code == 200:
                data = response.json()
                raw_text = data['candidates'][0]['content']['parts'][0]['text'].strip()
                if raw_text.startswith("```"):
                    raw_text = raw_text.strip("`")
                    if raw_text.startswith("json"):
                        raw_text = raw_text[4:].strip()
                post_data = json.loads(raw_text)
                post_data["facebook_caption"] = format_markdown_bold(post_data.get("facebook_caption", ""))
                post_data["linkedin_caption"] = format_markdown_bold(post_data.get("linkedin_caption", ""))
                return post_data
        except Exception as e:
            continue

    print(f"[Content Engine] Gemini busy. Using curated fallback for Day {day_cfg.get('day', 1)}.")
    return get_day_fallback(day_cfg)

def get_day_fallback(day_cfg):
    """Provides curated 100% English fallback tailored to the specific day."""
    day_num = day_cfg.get("day", 1)
    
    # Specific master fallback for Day 1
    if day_num == 1:
        fb_raw = f"""**Why Your Browser Pixels Are Missing 30% of Real Conversions! 🚨**

If you run an e-commerce brand or lead gen business, relying solely on standard browser pixels (Meta Pixel, Google Tag) is costing you 20% to 35% of your recorded sales.

Here is the invisible breakdown happening right now:
👉 **Ad Blockers:** Over 30% of desktop and mobile users run uBlock, Brave, or AdGuard, which block `connect.facebook.net` and `google-analytics.com` scripts completely.
👉 **Apple Safari ITP:** iOS and Mac Safari cap JavaScript cookies to 7 days or 24 hours, wiping out your 30-day attribution and making retargeting audiences disappear.
👉 **Network Timeouts & Script Dropping:** Heavy page loads cause browser tracking scripts to fail before checkout fires.

When Meta and Google algorithms miss 30% of your conversions, their AI starts guessing—bidding on the wrong prospects and driving your Cost Per Acquisition (CPA) through the roof.

**The Solution? Server-Side Tracking (sGTM & Conversions API)**
At **{BRAND_NAME}**, we move tracking out of the vulnerable browser into a private, first-party cloud server:

✔ **Immune to Ad Blockers:** Events are routed through your own custom domain (`data.yourbrand.com`), bypassing browser blacklists completely.
✔ **First-Party Cookie Armor:** Extends cookie lifetime up to 1-2 years, restoring pristine multi-touch attribution and deep retargeting pools.
✔ **Flawless AI Bidding:** Feeds 100% complete purchase signals to Meta Advantage+ and Google Smart Bidding, accelerating the learning phase and slashing CPA.

Stop leaving your revenue attribution to the mercy of browser privacy settings.

---

👇 **E-Commerce & Agency Founders:** Have you noticed a discrepancy between your Shopify/Stripe sales and what your ad dashboards report?

⚡ Ready to recover your lost conversions?
**{BRAND_NAME} is offering a FREE 30-Minute Server-Side Tracking Audit:**
📅 **Book Your Strategy Call:** {BRAND_CALENDLY}
🌐 **Official Agency Portal:** {BRAND_WEBSITE}
📞 **Direct Line / WhatsApp:** {BRAND_PHONE}"""

        li_raw = f"""**In 2026, browser-based tracking pixels are technically obsolete. 📈**

At **{BRAND_NAME}**, when we audit underperforming ad accounts spending $10k to $100k/month, the root cause is rarely the ad creative—it is **signal degradation**.

Standard client-side pixels are losing 25% to 35% of conversion events due to three compounding technical barriers:
1. **Aggressive Client-Side Filtering:** Privacy browsers (Brave, Safari) and DNS blockers terminate ad network scripts before they ever execute.
2. **Safari Intelligent Tracking Prevention (ITP):** Capping client-side cookies to 7 days, blinding your multi-touch attribution models.
3. **Algorithm Misalignment:** When Meta and Google bidding engines receive incomplete data, their smart bidding models optimize for cheap tire-kickers rather than high-LTV buyers.

**The Modern Solution: Server-Side Google Tag Manager (sGTM) + Meta CAPI.**

By routing all event telemetry through a first-party cloud container hosted on your own subdomain:
- You own the data pipeline.
- You bypass client-side blockers.
- You achieve 8.5+ Event Match Quality (EMQ) on Meta.
- You supply AI bidding algorithms with 100% verified conversion telemetry.

When your ad networks see 100% of your revenue, your blended acquisition cost drops predictably.

💡 **Want an objective, technical audit of your tracking and attribution architecture?**
Schedule a direct 30-minute review with our engineering team:

📅 **Schedule Your Session:** {BRAND_CALENDLY}
🌐 **Case Studies & Services:** {BRAND_WEBSITE}
📞 **Direct Contact / WhatsApp:** {BRAND_PHONE}"""

    else:
        # Generic structured fallback for other days
        fb_raw = f"""**{day_cfg.get('title')} 📊**

Are you running paid ads without a validated, data-driven framework? Most businesses waste 30%+ of their ad capital because they treat advertising and tracking as separate silos.

At **{BRAND_NAME}**, we focus on one single metric: **Profitable, Predictable Revenue Growth**.

Key Pillars:
✔ **{day_cfg.get('bullet_points', ['Laser Targeted Campaigns'])[0]}**
✔ **{day_cfg.get('bullet_points', ['Conversion Funnel Optimization'])[1] if len(day_cfg.get('bullet_points', [])) > 1 else 'Conversion Funnels'}**
✔ **{day_cfg.get('bullet_points', ['Accurate Attribution Tracking'])[2] if len(day_cfg.get('bullet_points', [])) > 2 else 'Full Tracking'}**

Stop treating ads like an afterthought. It is the engine that powers modern client acquisition.

📅 **Book Your Free 30-Minute Consultation:** {BRAND_CALENDLY}
🌐 **Agency Website:** {BRAND_WEBSITE}
📞 **Direct Call / WhatsApp:** {BRAND_PHONE}"""

        li_raw = f"""**{day_cfg.get('title')} 📈**

In performance marketing and digital acquisition, data integrity separates market leaders from failing campaigns.

At **{BRAND_NAME}**, we architect full-funnel systems that combine high-intent Google Ads with enterprise-grade Server-Side Tracking.

Core Insights:
1. **Strategic Targeting:** Eliminating waste before scaling ad spend.
2. **Server-Side Data Routing:** Ensuring 100% accurate conversion attribution.
3. **Closed-Won Revenue Focus:** Optimizing ad networks for paying customers, not empty form-fills.

💡 **Want an objective audit of your advertising or tracking architecture?**
📅 **Schedule Your Session:** {BRAND_CALENDLY}
🌐 **Case Studies & Services:** {BRAND_WEBSITE}
📞 **Direct Contact / WhatsApp:** {BRAND_PHONE}"""

    return {
        "day": day_num,
        "category": day_cfg.get("badge", "GOOGLE ADS"),
        "graphic_title_line1": day_cfg.get("graphic_title_line1", "LOCAL GOOGLE ADS"),
        "graphic_title_line2": day_cfg.get("graphic_title_line2", "GET HIGH-VALUE CLIENTS"),
        "graphic_subtitle": day_cfg.get("graphic_subtitle", f"Visit {BRAND_WEBSITE} to scale your business."),
        "bullet_points": day_cfg.get("bullet_points", [
            "Top #1 Position on Google",
            "High-Intent Inbound Phone Calls",
            "Zero Wasted Negative Keywords",
            "Transparent ROAS Reporting"
        ]),
        "cta_text": day_cfg.get("cta_text", "BOOK FREE AUDIT"),
        "facebook_caption": format_markdown_bold(fb_raw),
        "facebook_hashtags": f"#TauhidAdsLab #GoogleAds #LocalBusiness #Tracking #Day{day_num}",
        "linkedin_caption": format_markdown_bold(li_raw),
        "linkedin_hashtags": f"#PerformanceMarketing #GoogleAds #LocalSEO #TauhidAdsLab #Day{day_num}"
    }

if __name__ == "__main__":
    res = generate_dual_social_post()
    print("CATEGORY:", res["category"])
    print("--- FACEBOOK POST ---")
    print(res["facebook_caption"])
    print("\n--- LINKEDIN POST ---")
    print(res["linkedin_caption"])
