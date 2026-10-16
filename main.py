import os
import sys
from dotenv import load_dotenv

from content_engine import generate_dual_social_post
from image_engine import create_facebook_graphic, create_linkedin_graphic
from social_poster import (
    post_to_facebook,
    post_to_linkedin
)

load_dotenv()

def run_automation():
    print("=" * 70)
    print("🚀 Tauhid Ads Lab - Platform-Specific Dual Social Media Automation")
    print("🎯 Target Platforms: Facebook Page (Engaging) & LinkedIn (B2B Authority)")
    print("=" * 70)

    # 1. Generate Dual-Platform Content via AI
    print("\n[1/3] Generating Tailored Content for Facebook & LinkedIn...")
    post = generate_dual_social_post()
    
    fb_caption = f"{post.get('facebook_caption', '')}\n\n{post.get('facebook_hashtags', '')}".strip()
    li_caption = f"{post.get('linkedin_caption', '')}\n\n{post.get('linkedin_hashtags', '')}".strip()
    
    print("-> Facebook Caption ready (Orbit Media High-Engagement format)")
    print("-> LinkedIn Caption ready (Executive B2B Thought-Leadership format)")

    # 2. Design Platform-Specific Branded Graphics
    print("\n[2/3] Designing Tailored 1080x1080 Branded Graphics...")
    
    # Facebook Graphic: Vibrant, Promotional, High-Energy
    fb_image = "fb_graphic.png"
    create_facebook_graphic(post, output_path=fb_image)
    
    # LinkedIn Graphic: Clean, Executive Framework / Infographic Card
    li_image = "li_graphic.png"
    create_linkedin_graphic(post, output_path=li_image)

    # 3. Publish to Each Platform with its Own Dedicated Design & Copy
    print("\n[3/3] Publishing Tailored Posts to Channels...")
    results = {}
    
    # Publish to Facebook Page
    print("\n--- 🔵 Publishing to Facebook Page ---")
    results["Facebook Page"] = post_to_facebook(fb_image, fb_caption)
    
    # Publish to LinkedIn
    print("\n--- 💼 Publishing to LinkedIn ---")
    results["LinkedIn"] = post_to_linkedin(li_image, li_caption)

    # Summary Report
    print("\n" + "=" * 70)
    print("📊 Run Summary for Tauhid Ads Lab:")
    for platform, status in results.items():
        state = "✅ Successfully Published" if status else "⚠️ Skipped / Missing Credentials"
        print(f"  - {platform}: {state}")
    print("=" * 70)

if __name__ == "__main__":
    run_automation()
