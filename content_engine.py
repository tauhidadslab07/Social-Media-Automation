import os
import re
import json
import random
import requests
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BRAND_NAME = os.getenv("BRAND_NAME", "Tauhid Ads Lab")
BRAND_PHONE = os.getenv("BRAND_PHONE", "+8801624608468")
BRAND_WEBSITE = os.getenv("BRAND_WEBSITE", "http://tauhidadslab.com/")
BRAND_CALENDLY = os.getenv("BRAND_CALENDLY", "https://calendly.com/tauhidadslab/30min")

# ============================================================================
# DEDICATED PILLARS: 100% SEPARATED GOOGLE ADS vs CONVERSION TRACKING
# ============================================================================

PILLARS = [
    {
        "id": "GOOGLE_ADS",
        "badge": "GOOGLE ADS SPECIALIST",
        "cta": "BOOK FREE ADS AUDIT",
        "niche_focus": "Local Business Google Ads, Search Ads, Call-Only Campaigns, High-Intent Keywords",
        "graphic_default_title1": "LOCAL GOOGLE ADS",
        "graphic_default_title2": "GET HIGH-VALUE CLIENTS",
        "graphic_default_sub": "Target ready-to-buy customers searching on Google right now.",
        "graphic_default_bullets": [
            "Top #1 Position on Google Search",
            "High-Intent Inbound Phone Calls",
            "Zero Wasted Negative Keywords",
            "Transparent ROAS & Lead Reporting"
        ],
        "topics": [
            "Why Local Businesses (Dentists, Lawyers, Clinics, Home Services) Get 5x Better Leads on Google Search vs Social Media",
            "How Google Call-Only Ads Drive Direct Phone Inquiries Without Needing a Complex Website",
            "Negative Keywords: How Stopping Junk Clicks Saves 35% of Your Google Ad Spend Every Month",
            "Dominating 'Near Me' Searches in Your City: The Google Local Campaign Blueprint",
            "Quality Score Secrets: How to Pay 40% Less Cost-Per-Click Than Your Local Competitors on Google",
            "Maximizing Inbound Patient & Client Bookings with Google Search & Performance Max Campaigns"
        ]
    },
    {
        "id": "CONVERSION_TRACKING",
        "badge": "SERVER-SIDE TRACKING & GA4",
        "cta": "FIX YOUR TRACKING TODAY",
        "niche_focus": "Server-Side Tracking, Google Tag Manager (GTM), GA4, Meta Conversions API (CAPI), Enhanced Conversions",
        "graphic_default_title1": "FIX BROKEN TRACKING",
        "graphic_default_title2": "GTM, GA4 & META CAPI",
        "graphic_default_sub": "Stop data loss from iOS updates. Feed ad algorithms with 100% accurate data.",
        "graphic_default_bullets": [
            "Server-Side GTM & Cloud Container",
            "Meta CAPI 9+/10 Event Match Quality",
            "GA4 E-Commerce & Lead Events",
            "Google Ads Enhanced Conversions"
        ],
        "topics": [
            "Why Browser-Only Pixels Lose 40%+ of Ad Conversions (And How Server-Side GTM Recovers Them)",
            "How iOS 14.5+ Blinds Ad Algorithms: Meta Conversions API (CAPI) and Stape.io First-Party Tracking",
            "Google Analytics 4 (GA4) Custom E-commerce & Lead Event Tracking for 100% True ROAS Attribution",
            "Enhanced Conversions in Google Ads: The Single Setting That Recovers Lost Sales and Drops CPA",
            "Event Deduplication: How to Prevent Double-Counting Conversions in Pixel & CAPI",
            "Full Tracking Audit Checklist: Fixing Broken Pixels Across Shopify, WordPress, WooCommerce, and Web Apps"
        ]
    }
]

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

def get_active_topics():
    topics_file = os.path.join(os.path.dirname(__file__), "topics.json")
    if os.path.exists(topics_file):
        try:
            with open(topics_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data
        except Exception:
            pass
    return None

def generate_dual_social_post():
    """
    Generates high-converting, 100% ENGLISH social media posts strictly separated into:
    - 100% PURE GOOGLE ADS FOR LOCAL BUSINESS
    or
    - 100% PURE CONVERSION TRACKING & ANALYTICS (GTM, GA4, CAPI)
    """
    custom_data = get_active_topics()
    selected_pillar = random.choice(PILLARS)
    
    if custom_data:
        if selected_pillar["id"] == "GOOGLE_ADS" and custom_data.get("google_ads_topics"):
            selected_topic = random.choice(custom_data["google_ads_topics"])
        elif selected_pillar["id"] == "CONVERSION_TRACKING" and custom_data.get("tracking_topics"):
            selected_topic = random.choice(custom_data["tracking_topics"])
        else:
            selected_topic = random.choice(selected_pillar["topics"])
    else:
        selected_topic = random.choice(selected_pillar["topics"])
    
    if not GEMINI_API_KEY:
        print("[Content Engine] No GEMINI_API_KEY found, using curated fallback.")
        return get_dual_fallback(selected_pillar, selected_topic)

    models_to_try = ["gemini-3.5-flash", "gemini-3-flash-preview", "gemini-flash-latest"]
    
    if selected_pillar["id"] == "GOOGLE_ADS":
        strict_instruction = f"""
STRICT NICHE MANDATE: This post must be 100% STRICTLY ABOUT GOOGLE ADS FOR LOCAL BUSINESSES (Doctors, Dentists, Lawyers, Clinics, Home Services, Real Estate, Local Stores).
- Do NOT talk about Facebook or Instagram ads.
- Focus purely on Google Search Ads, Call-Only Campaigns, High-Intent Keywords, Negative Keywords, Quality Score, and capturing ready-to-buy local searchers.
- Tone: High-authority, practical, showing local business owners how to stop burning cash on useless clicks and start getting inbound phone calls and booked appointments.
"""
    else:
        strict_instruction = f"""
STRICT NICHE MANDATE: This post must be 100% STRICTLY ABOUT ADVANCED CONVERSION TRACKING & WEB ANALYTICS (GTM, GA4, Server-Side Tracking, Meta Conversions API / CAPI, Enhanced Conversions across all niches: Shopify, WordPress, WooCommerce, Lead Gen).
- Do NOT give generic marketing fluff. Focus on accurate data attribution, fixing tracking leaks, iOS 14+ data loss, Event Match Quality (EMQ), and server container setup.
- Tone: Highly technical yet accessible, expert data architect, demonstrating that running ads with broken tracking is like pouring water into a leaky bucket.
"""

    prompt = f"""
You are the Chief Growth Strategist & Technical Lead at '{BRAND_NAME}', an elite performance marketing and tracking agency.
Agency Contact Details:
- Website: {BRAND_WEBSITE}
- Free 30-Min Strategy Call (Calendly): {BRAND_CALENDLY}
- Phone / WhatsApp: {BRAND_PHONE}

{strict_instruction}

Topic for today's post: {selected_topic}.

CRITICAL REQUIREMENTS:
1. LANGUAGE: 100% ENGLISH ONLY. Flawless, punchy, persuasive American/International English.
2. BOLDING: Use **double asterisks** around critical headlines, key stats, bullet point titles, and call-to-actions so our system converts them to TRUE BOLD on Facebook and LinkedIn.
3. MANDATORY LINKS in both posts:
   - Free 30-Min Consultation: {BRAND_CALENDLY}
   - Website: {BRAND_WEBSITE}
   - Phone / WhatsApp: {BRAND_PHONE}

Platform Guidelines:
1. FACEBOOK VERSION:
- Follow Orbit Media's 'Anatomy of the Perfect Post':
  - **Hook**: First line must be a powerful headline with numbers/benefits in **bold**.
  - **Secondary Headline**: Expand curiosity.
  - **Line Breaks**: Clean double spacing between paragraphs.
  - **Quote**: Memorable quote in quotation marks ("...").
  - **Bullet Points**: Actionable takeaways with emojis (✔, 🚀, 💡, 📞, 🎯) and **bold titles**.
  - **Call to Action**: Direct invite to book a free 30-min audit or message on WhatsApp.

2. LINKEDIN VERSION:
- High-level B2B Thought-Leadership:
  - Professional, data-driven, analytical tone for Founders, CEOs, Clinic Owners, and Marketing Directors.
  - Focus on Cost-Per-Acquisition, High-Intent Search, Attribution Quality, and ROAS.
  - Bold key insights and metrics.
  - Professional CTA to schedule on Calendly, visit the website, or contact directly.

The response MUST be valid JSON with the following exact keys:
{{
  "category": "{selected_pillar['badge']}",
  "graphic_title_line1": "{selected_pillar['graphic_default_title1']}",
  "graphic_title_line2": "{selected_pillar['graphic_default_title2']}",
  "graphic_subtitle": "{selected_pillar['graphic_default_sub']}",
  "bullet_points": ["4 punchy, high-impact bullet points related strictly to {selected_pillar['id']}"],
  "cta_text": "{selected_pillar['cta']}",
  "facebook_caption": "Complete formatted 100% English Facebook post using **bold** markers...",
  "facebook_hashtags": "#TauhidAdsLab #{selected_pillar['id'].replace('_', '')} #GoogleAds #LocalBusiness #Tracking",
  "linkedin_caption": "Complete formatted 100% English LinkedIn post using **bold** markers...",
  "linkedin_hashtags": "#PerformanceMarketing #{selected_pillar['id'].replace('_', '')} #WebAnalytics #TauhidAdsLab"
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

    print("[Content Engine] All Gemini model endpoints busy/failed. Using curated fallback.")
    return get_dual_fallback(selected_pillar, selected_topic)

def get_dual_fallback(pillar=None, topic=None):
    """Provides curated 100% English fallback with true Unicode bolding for each specific pillar."""
    pillar = pillar or PILLARS[0]
    topic = topic or pillar["topics"][0]
    
    if pillar["id"] == "GOOGLE_ADS":
        fb_raw = f"""**Stop Wasting Budget on Casual Scrollers: Why Local Businesses Win on Google Search! 🎯**

If you run a local service business (clinic, dental practice, law firm, real estate, or home services), social media ads often flood your inbox with casual questions like 'Price please?'. 

Google Search is fundamentally different: when someone types **'Emergency Dentist Near Me'** or **'Best Commercial Real Estate Agent'**, they already have their credit card in hand and are ready to hire.

❝**People scroll social media to kill time. People search on Google to solve an urgent problem immediately.**❞

Here are **3 Google Ads pillars** that get local businesses high-paying clients:
✔ **High-Intent Search Campaigns:** Bid strictly on high-commercial-intent search queries instead of broad informational keywords.
✔ **Negative Keyword Fortress:** Exclude words like 'free', 'cheap', 'jobs', and 'course' to save 30%+ of your daily ad spend from junk clicks.
✔ **Direct Call-Only Ads:** Connect high-intent searchers directly to your office front desk with a single tap on their smartphone.

Ready to dominate local search results and get consistent, high-paying clients?
**{BRAND_NAME} is offering a FREE 30-Minute Google Ads Local Audit!** 🚀

📅 **Book Your Free Strategy Call:**
👉 {BRAND_CALENDLY}

🌐 **Explore Our Agency Website:**
👉 {BRAND_WEBSITE}

📞 **Direct Call / WhatsApp:** {BRAND_PHONE}"""

        li_raw = f"""**For local businesses and high-ticket service providers, intent always beats interruption. 📈**

At **{BRAND_NAME}**, when we analyze underperforming advertising budgets for local practices, law firms, and service agencies, the primary mistake is over-allocating capital to social media interruption ads while ignoring **high-intent Google Search volume**.

When a prospective client searches for a solution on Google, they are already at the bottom of the decision funnel. Capturing this demand requires three non-negotiables:

1. **Granular Exact & Phrase Match Architecture:** Isolating top-tier buyer keywords with dedicated landing pages.
2. **Aggressive Negative Keyword Management:** Eliminating low-intent, informational queries to preserve ad budget.
3. **Quality Score Optimization:** Aligning ad copy with landing page relevance to achieve top ad rank at a 40% lower Cost-Per-Click (CPC).

💡 **Want an objective, data-backed audit of your local Google Ads campaigns?**
Book a direct 30-minute performance review with our senior growth team:

📅 **Schedule Your Session:** {BRAND_CALENDLY}
🌐 **Case Studies & Services:** {BRAND_WEBSITE}
📞 **Direct Contact / WhatsApp:** {BRAND_PHONE}"""

    else: # CONVERSION_TRACKING
        fb_raw = f"""**Running Ads Without Server-Side Tracking Is Like Pouring Water Into a Leaky Bucket! 📊**

Are your Facebook or Google Ads reporting 20 conversions, but your actual bank account or CRM only shows 5? Or did your Cost-Per-Acquisition suddenly double after recent iOS updates?

You don't have a traffic problem. **You have an attribution and data-tracking leak.**

❝**Ad algorithms can only optimize for the data they can see. If your tracking is blind, your ad budget is blind.**❞

Here is how modern **Server-Side Tracking** fixes your ad performance:
✔ **Google Tag Manager (GTM) Server Container:** Bypasses ad-blockers and Safari ITP restrictions by routing data through your own custom first-party subdomain.
✔ **Meta Conversions API (CAPI) with 9+/10 EMQ:** Feeds Meta's AI with hashed user data for laser-accurate retargeting and deduplication.
✔ **Google Ads Enhanced Conversions:** Recovers up to 20% of lost conversion data directly into Google Analytics 4 (GA4).
✔ **Zero Double-Counting:** Clean event deduplication ensures your ad platforms never report false numbers.

Ready to plug your tracking leaks and feed ad algorithms with 100% accurate data?
**{BRAND_NAME} is offering a FREE Full-Stack Tracking & Pixel Audit!** 🚀

📅 **Book Your Free Strategy Call:**
👉 {BRAND_CALENDLY}

🌐 **Explore Our Agency Website:**
👉 {BRAND_WEBSITE}

📞 **Direct Call / WhatsApp:** {BRAND_PHONE}"""

        li_raw = f"""**The single biggest factor separating high-ROAS advertisers from failing campaigns is Data Quality. 📉**

Since the rollout of privacy restrictions, browser-based client-side cookies lose up to **35% to 45% of critical conversion data**. When ad network algorithms lack complete conversion signals, your Cost-Per-Acquisition (CPA) spikes inevitably.

At **{BRAND_NAME}**, we implement enterprise-grade **Server-Side Tracking Architecture** across all e-commerce and lead generation ecosystems:

1. **Server-Side GTM via First-Party Subdomain:** Eliminates 3rd-party cookie dependency and resists browser ad-blockers.
2. **Meta Conversions API (CAPI) Integration:** Achieving an Event Match Quality (EMQ) score of 9.0+ with reliable event deduplication.
3. **Google Analytics 4 (GA4) & Enhanced Conversions:** Full-funnel event attribution from initial touchpoint to final purchase.

Stop feeding your ad algorithms degraded data. Build a rock-solid, privacy-compliant tracking foundation.

💡 **Want a full technical audit of your GTM, GA4, and CAPI setup?**
Book a direct 30-minute tracking review with our technical architects:

📅 **Schedule Your Session:** {BRAND_CALENDLY}
🌐 **Case Studies & Services:** {BRAND_WEBSITE}
📞 **Direct Contact / WhatsApp:** {BRAND_PHONE}"""

    return {
        "category": pillar["badge"],
        "graphic_title_line1": pillar["graphic_default_title1"],
        "graphic_title_line2": pillar["graphic_default_title2"],
        "graphic_subtitle": pillar["graphic_default_sub"],
        "bullet_points": pillar["graphic_default_bullets"],
        "cta_text": pillar["cta"],
        "facebook_caption": format_markdown_bold(fb_raw),
        "facebook_hashtags": f"#TauhidAdsLab #{pillar['id'].replace('_', '')} #GoogleAds #LocalBusiness #Tracking",
        "linkedin_caption": format_markdown_bold(li_raw),
        "linkedin_hashtags": f"#PerformanceMarketing #{pillar['id'].replace('_', '')} #WebAnalytics #TauhidAdsLab"
    }

if __name__ == "__main__":
    res = generate_dual_social_post()
    print("CATEGORY:", res["category"])
    print("--- FACEBOOK POST ---")
    print(res["facebook_caption"])
    print("\n--- LINKEDIN POST ---")
    print(res["linkedin_caption"])
