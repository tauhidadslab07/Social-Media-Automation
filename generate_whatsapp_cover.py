import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_whatsapp_covers():
    # WhatsApp Business recommended size: 1200x675 (16:9 high resolution)
    WIDTH, HEIGHT = 1200, 675
    
    # Try finding modern fonts
    def get_font(size, bold=False):
        font_paths = [
            f"C:/Windows/Fonts/{'segoeuib.ttf' if bold else 'segoeui.ttf'}",
            f"C:/Windows/Fonts/{'arialbd.ttf' if bold else 'arial.ttf'}",
            f"C:/Windows/Fonts/{'tahoma.ttf' if not bold else 'tahomabd.ttf'}"
        ]
        for p in font_paths:
            if os.path.exists(p):
                try:
                    return ImageFont.truetype(p, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    # -------------------------------------------------------------
    # VARIATION 1: Midnight Luxury & Electric Cyan Glow (Agency Theme)
    # -------------------------------------------------------------
    img = Image.new("RGBA", (WIDTH, HEIGHT), (10, 15, 29, 255))
    draw = ImageDraw.Draw(img)

    # Ambient Background Gradient / Lighting
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    
    # Top-right electric cyan flare
    for r in range(400, 0, -20):
        alpha = int(45 * (1 - r / 400))
        glow_draw.ellipse([WIDTH - 300 - r, -100 - r, WIDTH - 300 + r, -100 + r], fill=(0, 210, 255, alpha))
        
    # Bottom-right royal blue / purple aura
    for r in range(500, 0, -25):
        alpha = int(35 * (1 - r / 500))
        glow_draw.ellipse([WIDTH - 150 - r, HEIGHT - 100 - r, WIDTH - 150 + r, HEIGHT - 100 + r], fill=(59, 130, 246, alpha))

    # Amber gold subtle spark
    for r in range(250, 0, -15):
        alpha = int(30 * (1 - r / 250))
        glow_draw.ellipse([450 - r, 120 - r, 450 + r, 120 + r], fill=(245, 158, 11, alpha))

    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # Decorative tech grid dots or subtle lines
    for x in range(350, WIDTH - 40, 50):
        for y in range(40, HEIGHT - 40, 50):
            draw.point((x, y), fill=(255, 255, 255, 18))

    # Left Profile Avatar Safe Zone Guide (Visual subtle indicator)
    # The profile picture sits around (60, 420) on mobile
    
    # BRAND PILL BADGE (Top Center/Right)
    badge_x, badge_y = 360, 55
    badge_w, badge_h = 320, 36
    draw.rounded_rectangle([badge_x, badge_y, badge_x + badge_w, badge_y + badge_h], radius=18, fill=(15, 23, 42, 220), outline=(0, 210, 255, 180), width=1)
    # Green pulse dot inside badge
    draw.ellipse([badge_x + 14, badge_y + 12, badge_x + 24, badge_y + 22], fill=(16, 185, 129, 255))
    draw.text((badge_x + 32, badge_y + 8), "PERFORMANCE MARKETING AGENCY", fill=(0, 210, 255, 255), font=get_font(13, bold=True))

    # MAIN HEADLINE: TAUHID ADS LAB
    headline_font = get_font(52, bold=True)
    draw.text((360, 105), "TAUHID ADS LAB", fill=(255, 255, 255, 255), font=headline_font)
    
    # Gold glowing underline
    draw.rounded_rectangle([360, 172, 580, 176], radius=2, fill=(245, 158, 11, 255))

    # SUBTITLE
    sub_font = get_font(23, bold=False)
    draw.text((360, 190), "We Help Brands Scale With High-ROAS Paid Ads", fill=(203, 213, 225, 255), font=sub_font)

    # 4 KEY SERVICE CARDS (2x2 Glassmorphic Pills)
    services = [
        (" Meta (FB & IG) Ads Scaling", 360, 245),
        (" Google & YouTube Ads Strategy", 760, 245),
        (" E-commerce Revenue Scaling", 360, 310),
        (" High-Converting Funnel & Leads", 760, 310),
    ]

    card_font = get_font(17, bold=True)
    for title, cx, cy in services:
        cw, ch = 370, 50
        # Glass card background
        draw.rounded_rectangle([cx, cy, cx + cw, cy + ch], radius=12, fill=(20, 30, 55, 200), outline=(51, 65, 85, 180), width=1)
        draw.text((cx + 16, cy + 14), title, fill=(241, 245, 249, 255), font=card_font)

    # STATS / TRUST BAR (Middle-Right)
    stat_y = 390
    draw.rounded_rectangle([360, stat_y, 1130, stat_y + 75], radius=16, fill=(15, 23, 42, 230), outline=(37, 99, 235, 140), width=1)

    # Stat 1
    draw.text((385, stat_y + 12), "5.0 ★ Rated", fill=(245, 158, 11, 255), font=get_font(21, bold=True))
    draw.text((385, stat_y + 40), "Client Satisfaction", fill=(148, 163, 184, 255), font=get_font(14, bold=False))

    draw.line([(570, stat_y + 15), (570, stat_y + 60)], fill=(51, 65, 85, 200), width=1)

    # Stat 2
    draw.text((605, stat_y + 12), "3X - 7X ROAS", fill=(0, 210, 255, 255), font=get_font(21, bold=True))
    draw.text((605, stat_y + 40), "Target Ad Performance", fill=(148, 163, 184, 255), font=get_font(14, bold=False))

    draw.line([(820, stat_y + 15), (820, stat_y + 60)], fill=(51, 65, 85, 200), width=1)

    # Stat 3
    draw.text((855, stat_y + 12), "100% Data-Driven", fill=(52, 211, 153, 255), font=get_font(21, bold=True))
    draw.text((855, stat_y + 40), "Transparent Analytics", fill=(148, 163, 184, 255), font=get_font(14, bold=False))

    # BOTTOM FOOTER BAR (Contact & Action)
    foot_y = 495
    # WhatsApp direct CTA button
    draw.rounded_rectangle([360, foot_y, 670, foot_y + 54], radius=27, fill=(37, 211, 102, 255)) # WhatsApp green
    draw.text((385, foot_y + 15), " Chat On WhatsApp: +880 1624 608468", fill=(10, 15, 29, 255), font=get_font(16, bold=True))

    # Website Pill
    draw.rounded_rectangle([700, foot_y, 970, foot_y + 54], radius=27, fill=(30, 41, 59, 240), outline=(59, 130, 246, 200), width=1)
    draw.text((725, foot_y + 16), "🌐 tauhidadslab.com", fill=(255, 255, 255, 255), font=get_font(16, bold=True))

    # Free consultation tag
    draw.text((365, foot_y + 75), "⚡ Book Free Strategy Call: calendly.com/tauhidadslab/30min", fill=(148, 163, 184, 255), font=get_font(15, bold=False))

    # Left side branding illustration (Modern 3D-styled chart badge)
    # Sits nicely above where the avatar circular cut is
    chart_box = [60, 80, 310, 330]
    draw.rounded_rectangle(chart_box, radius=20, fill=(15, 23, 42, 220), outline=(0, 210, 255, 100), width=1)
    
    # Growth graph illustration inside chart box
    draw.text((85, 105), "GROWTH TRAJECTORY", fill=(0, 210, 255, 255), font=get_font(12, bold=True))
    draw.text((85, 130), "+340%", fill=(16, 185, 129, 255), font=get_font(34, bold=True))
    draw.text((85, 175), "Average Client Revenue", fill=(148, 163, 184, 255), font=get_font(13, bold=False))
    
    # Glowing upward trendline
    points = [(85, 280), (130, 260), (175, 270), (220, 220), (265, 200), (290, 150)]
    draw.line(points, fill=(16, 185, 129, 255), width=4)
    for px, py in points:
        draw.ellipse([px - 5, py - 5, px + 5, py + 5], fill=(255, 255, 255, 255), outline=(16, 185, 129, 255), width=2)

    # Save Variation 1
    cover1_path = os.path.join(os.getcwd(), "whatsapp_business_cover_luxury.png")
    img.convert("RGB").save(cover1_path, "PNG", quality=98)
    print(f"Generated: {cover1_path}")

    # -------------------------------------------------------------
    # VARIATION 2: Clean High-Trust Corporate Edition (Bright / Minimal)
    # -------------------------------------------------------------
    img2 = Image.new("RGBA", (WIDTH, HEIGHT), (15, 23, 42, 255)) # Dark slate
    draw2 = ImageDraw.Draw(img2)

    # Gradient mesh background
    mesh = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    mesh_draw = ImageDraw.Draw(mesh)
    for r in range(450, 0, -20):
        alpha = int(40 * (1 - r / 450))
        mesh_draw.ellipse([WIDTH - 250 - r, 50 - r, WIDTH - 250 + r, 50 + r], fill=(37, 99, 235, alpha))
    for r in range(350, 0, -20):
        alpha = int(30 * (1 - r / 350))
        mesh_draw.ellipse([600 - r, HEIGHT - 50 - r, 600 + r, HEIGHT - 50 + r], fill=(16, 185, 129, alpha))
    img2 = Image.alpha_composite(img2, mesh)
    draw2 = ImageDraw.Draw(img2)

    # Tagline top
    draw2.text((360, 65), "CERTIFIED DIGITAL ADVERTISING PARTNER", fill=(56, 189, 248, 255), font=get_font(14, bold=True))

    # Huge bold title
    draw2.text((360, 100), "TAUHID ADS LAB", fill=(255, 255, 255, 255), font=get_font(56, bold=True))
    draw2.text((360, 175), "Maximize ROI & Dominate Your Market With Paid Ads", fill=(226, 232, 240, 255), font=get_font(23, bold=False))

    # Horizontal Service Badges
    service_list = [
        " Meta Ads (Facebook & Instagram)",
        " Google Search & Display Ads",
        " E-commerce ROAS Scaling",
        " Lead Generation & High-Ticket Funnels",
        " Conversion Rate Optimization (CRO)"
    ]

    sy = 230
    for s in service_list:
        draw2.text((360, sy), s, fill=(241, 245, 249, 255), font=get_font(18, bold=True))
        sy += 40

    # Large Action Card
    action_box = [360, 460, 1140, 560]
    draw2.rounded_rectangle(action_box, radius=18, fill=(30, 41, 59, 240), outline=(56, 189, 248, 160), width=2)
    
    # Phone
    draw2.text((390, 480), " Direct WhatsApp / Call:", fill=(148, 163, 184, 255), font=get_font(14, bold=False))
    draw2.text((390, 505), "+880 1624 608468", fill=(37, 211, 102, 255), font=get_font(26, bold=True))

    draw2.line([(680, 475), (680, 545)], fill=(71, 85, 105, 200), width=1)

    # Website
    draw2.text((710, 480), " Official Agency Portal:", fill=(148, 163, 184, 255), font=get_font(14, bold=False))
    draw2.text((710, 505), "tauhidadslab.com", fill=(56, 189, 248, 255), font=get_font(26, bold=True))

    draw2.line([(960, 475), (960, 545)], fill=(71, 85, 105, 200), width=1)

    # Free Consultation
    draw2.text((980, 480), " Strategy Session:", fill=(148, 163, 184, 255), font=get_font(14, bold=False))
    draw2.text((980, 508), "30-Min Free Audit", fill=(245, 158, 11, 255), font=get_font(20, bold=True))

    # Left Side Trust Card
    trust_box = [60, 80, 310, 310]
    draw2.rounded_rectangle(trust_box, radius=20, fill=(30, 41, 59, 220), outline=(56, 189, 248, 100), width=1)
    draw2.text((85, 110), "OUR PROMISE", fill=(56, 189, 248, 255), font=get_font(13, bold=True))
    draw2.text((85, 140), "Results First.", fill=(255, 255, 255, 255), font=get_font(26, bold=True))
    draw2.text((85, 180), "We don't just run ads.", fill=(203, 213, 225, 255), font=get_font(15, bold=False))
    draw2.text((85, 205), "We build profitable", fill=(203, 213, 225, 255), font=get_font(15, bold=False))
    draw2.text((85, 230), "customer acquisition", fill=(203, 213, 225, 255), font=get_font(15, bold=False))
    draw2.text((85, 255), "ecosystems.", fill=(245, 158, 11, 255), font=get_font(15, bold=True))

    cover2_path = os.path.join(os.getcwd(), "whatsapp_business_cover_corporate.png")
    img2.convert("RGB").save(cover2_path, "PNG", quality=98)
    print(f"Generated: {cover2_path}")

create_whatsapp_covers()
