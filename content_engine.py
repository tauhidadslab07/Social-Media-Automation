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
NICHE_TOPIC = os.getenv("NICHE_TOPIC", "Facebook Ads, Google Ads, E-commerce Scaling, Local Business Growth, High-ROAS Strategy")

POST_THEMES = [
    {
        "type": "GROWTH_STRATEGY",
        "description": "How to scale ad campaigns profitably, lower CPA, and 3x conversion rate.",
        "badge": "ADS STRATEGY",
        "cta": "BOOK FREE AUDIT"
    },
    {
        "type": "COMMON_MISTAKE",
        "description": "Costly mistakes business owners make with paid ads (boosting blindly, lack of retargeting, broken tracking).",
        "badge": "ADS MISTAKE TO AVOID",
        "cta": "FIX YOUR ADS TODAY"
    },
    {
        "type": "DATA_AND_FUNNEL",
        "description": "Conversion funnel mechanics, Pixel & CAPI tracking, creative testing frameworks.",
        "badge": "FUNNEL & DATA",
        "cta": "SCALE YOUR SALES"
    },
    {
        "type": "AGENCY_CASE_INSIGHT",
        "description": "How data-driven ad testing transforms a struggling business into a high-profit market leader.",
        "badge": "AGENCY CASE STUDY",
        "cta": "BOOK A CONSULTATION"
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
        # Uppercase A-Z -> Mathematical Sans-Serif Bold A-Z
        if 65 <= code <= 90:
            result.append(chr(code - 65 + 0x1D5D4))
        # Lowercase a-z -> Mathematical Sans-Serif Bold a-z
        elif 97 <= code <= 122:
            result.append(chr(code - 97 + 0x1D5EE))
        # Digits 0-9 -> Mathematical Sans-Serif Bold 0-9
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
    
    # Replace **word** or *word*
    formatted = re.sub(r'\*\*(.+?)\*\*', replacer, text)
    return formatted

def generate_dual_social_post():
    """
    Generates high-converting, 100% ENGLISH social media posts for Facebook and LinkedIn.
    Uses bolding on hooks, key insights, and CTAs.
    """
    selected_theme = random.choice(POST_THEMES)
    
    if not GEMINI_API_KEY:
        print("[Content Engine] No GEMINI_API_KEY found, using curated 100% English fallback.")
        return get_dual_fallback(selected_theme)

    # Models in order of preference
    models_to_try = ["gemini-3.5-flash", "gemini-3-flash-preview", "gemini-flash-latest"]
    
    prompt = f"""
You are the Chief Copywriter and Head of Growth for '{BRAND_NAME}', an elite performance advertising agency.
Agency Contact Details:
- Website: {BRAND_WEBSITE}
- Free 30-Min Strategy Call (Calendly): {BRAND_CALENDLY}
- Phone / WhatsApp: {BRAND_PHONE}
Niche: {NICHE_TOPIC}.
Topic for today's post: {selected_theme['description']}.

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
  - **Bullet Points**: Actionable takeaways with emojis (✔, 🚀, 💡) and **bold titles**.
  - **Call to Action**: Urgent invitation to book a free 30-min audit or call.

2. LINKEDIN VERSION:
- High-level B2B Thought-Leadership:
  - Professional, data-driven, analytical tone for Founders, CEOs, and Marketing Directors.
  - Focus on ROAS, CPA, conversion funnels, and Customer Acquisition Cost.
  - Bold key insights and metrics.
  - Professional CTA to schedule on Calendly, visit the website, or contact directly.

The response MUST be valid JSON with the following exact keys:
{{
  "category": "{selected_theme['badge']}",
  "graphic_title_line1": "WE HELP TO",
  "graphic_title_line2": "GROW YOUR BUSINESS",
  "graphic_subtitle": "Data-driven advertising strategies to scale your sales.",
  "bullet_points": ["Laser Targeted Ads", "Conversion Funnels", "High-ROAS Creatives", "Full Tracking Setup"],
  "cta_text": "{selected_theme['cta']}",
  "facebook_caption": "Complete formatted 100% English Facebook post using **bold** markers...",
  "facebook_hashtags": "#TauhidAdsLab #FacebookAds #LocalBusiness #EcommerceGrowth #PaidTraffic",
  "linkedin_caption": "Complete formatted 100% English LinkedIn post using **bold** markers...",
  "linkedin_hashtags": "#PerformanceMarketing #GrowthMarketing #B2B #DigitalAdvertising #TauhidAdsLab"
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
    return get_dual_fallback(selected_theme)

def get_dual_fallback(theme=None):
    """Provides curated 100% English fallback with true Unicode bolding."""
    theme = theme or POST_THEMES[0]
    
    fb_raw = f"""**Stop Wasting Your Ad Budget: 3 Secrets to 3X Your Sales! 📈**

Are you running ads daily but struggling to see consistent, predictable sales? Most local businesses and e-commerce stores fail because they simply hit 'Boost Post' with zero funnel architecture.

❝**Ad budget isn't the real bottleneck. Your audience targeting and conversion funnel are.**❞

Fix these **3 critical pillars** in your advertising today:
✔ **Hyper-Target Local Buyers:** Stop targeting broad demographics. Focus on high-intent in-market shoppers.
✔ **Ditch the Boost Button:** Use Ads Manager to build customized multi-stage retargeting campaigns.
✔ **Hook-Rate Optimization:** Test 3 new creative hooks every week to eliminate ad fatigue.

Ready to turn your ad spend into predictable, profitable revenue?
**{BRAND_NAME} is offering a FREE 30-Minute Ad Strategy & Audit Session!** 🚀

📅 **Book Your Free Consultation Call:**
👉 {BRAND_CALENDLY}

🌐 **Explore Our Agency Website:**
👉 {BRAND_WEBSITE}

📞 **Direct Call / WhatsApp:** {BRAND_PHONE}"""

    li_raw = f"""**Most brands don't have a traffic problem. They have a conversion & data-tracking problem. 📊**

In performance marketing, running paid media without a validated funnel is simply burning capital. When our team at **{BRAND_NAME}** audits underperforming ad accounts, **85% of budget waste** stems from three critical areas:

1. **Lack of Full-Funnel Architecture:** Over-indexing on cold top-of-funnel traffic with zero structured retargeting.
2. **Creative Fatigue:** Not rotating dynamic angles, hooks, and proof points on a weekly basis.
3. **Attribution Blindness:** Missing Conversions API (CAPI) and custom event parameter tracking.

If your objective is sustainable, profitable scaling, prioritize **lowering Customer Acquisition Cost (CAC)** while **maximizing Customer Lifetime Value (LTV)**.

💡 **Want an objective, data-backed audit of your current ad campaigns?**
Book a direct 30-minute performance review with our senior growth team:

📅 **Schedule Your Session:** {BRAND_CALENDLY}
🌐 **Case Studies & Services:** {BRAND_WEBSITE}
📞 **Direct Contact / WhatsApp:** {BRAND_PHONE}"""

    return {
        "category": theme["badge"],
        "graphic_title_line1": "WE HELP TO",
        "graphic_title_line2": "GROW YOUR BUSINESS",
        "graphic_subtitle": f"Visit {BRAND_WEBSITE} to scale your sales with data-driven ads.",
        "bullet_points": [
            "Laser Targeted Audience Setup",
            "High-Converting Ad Creatives & Copy",
            "Full Funnel Retargeting Strategy",
            "Proven High-ROAS Campaign Scaling"
        ],
        "cta_text": theme["cta"],
        "facebook_caption": format_markdown_bold(fb_raw),
        "facebook_hashtags": "#TauhidAdsLab #FacebookAds #LocalBusinessGrowth #EcommerceMarketing #PaidTraffic",
        "linkedin_caption": format_markdown_bold(li_raw),
        "linkedin_hashtags": "#PerformanceMarketing #GrowthMarketing #DigitalStrategy #B2B #PaidAds #TauhidAdsLab"
    }

if __name__ == "__main__":
    res = generate_dual_social_post()
    print("--- FACEBOOK POST ---")
    print(res["facebook_caption"])
    print("\n--- LINKEDIN POST ---")
    print(res["linkedin_caption"])
