import os
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()

BRAND_NAME = os.getenv("BRAND_NAME", "Tauhid Ads Lab")
BRAND_PHONE = os.getenv("BRAND_PHONE", "+8801624608468")
BRAND_WEBSITE = os.getenv("BRAND_WEBSITE", "tauhidadslab.com").replace("http://", "").replace("https://", "").strip("/")

# Palettes
FB_THEMES = [
    {
        "name": "Facebook High-Energy Blue & Gold",
        "primary": (30, 58, 138),      # Deep Navy Blue (#1E3A8A)
        "accent": (245, 158, 11),      # Golden Yellow (#F59E0B)
        "accent_light": (254, 243, 199),
        "bg": (248, 250, 252),
        "card_bg": (255, 255, 255),
        "text_dark": (15, 23, 42),
        "text_muted": (71, 85, 105),
        "white": (255, 255, 255)
    },
    {
        "name": "Facebook Vibrant Royal & Orange",
        "primary": (29, 78, 216),      # Royal Blue (#1D4ED8)
        "accent": (249, 115, 22),      # Orange (#F97316)
        "accent_light": (255, 237, 213),
        "bg": (255, 255, 255),
        "card_bg": (241, 245, 249),
        "text_dark": (17, 24, 39),
        "text_muted": (100, 116, 139),
        "white": (255, 255, 255)
    }
]

LI_THEMES = [
    {
        "name": "LinkedIn Executive Navy & Steel",
        "primary": (15, 23, 42),       # Dark Slate (#0F172A)
        "accent": (59, 130, 246),      # Corporate Blue (#3B82F6)
        "accent_light": (219, 234, 254),
        "bg": (255, 255, 255),
        "card_bg": (248, 250, 252),
        "text_dark": (15, 23, 42),
        "text_muted": (100, 116, 139),
        "white": (255, 255, 255)
    },
    {
        "name": "LinkedIn Deep Teal & Gold",
        "primary": (13, 71, 89),       # Deep Teal
        "accent": (245, 158, 11),      # Gold
        "accent_light": (254, 243, 199),
        "bg": (250, 250, 250),
        "card_bg": (255, 255, 255),
        "text_dark": (24, 24, 27),
        "text_muted": (82, 82, 91),
        "white": (255, 255, 255)
    }
]

def get_font(size, bold=False):
    font_candidates = []
    if os.name == 'nt':
        font_candidates.extend([
            "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf",
            "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf",
            "C:\\Windows\\Fonts\\impact.ttf" if bold else "C:\\Windows\\Fonts\\tahoma.ttf"
        ])
    font_candidates.extend([
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf" if bold else "/usr/share/fonts/truetype/freefont/FreeSans.ttf"
    ])
    for path in font_candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    try:
        return ImageFont.load_default()
    except Exception:
        return None

def create_facebook_graphic(post_data, output_path="fb_graphic.png"):
    """
    Facebook Design Style: Vibrant, High-Conversion Promotional Banner.
    Features bold curved wave, massive 2-tone title, checked bullet list,
    action button, website, and phone footer.
    """
    WIDTH, HEIGHT = 1080, 1080
    theme = random.choice(FB_THEMES)
    img = Image.new("RGB", (WIDTH, HEIGHT), color=theme["bg"])
    draw = ImageDraw.Draw(img)
    
    # 1. Top Wave
    draw.polygon([(0, 0), (WIDTH, 0), (WIDTH, 140), (0, 200)], fill=theme["primary"])
    draw.polygon([(WIDTH - 240, 0), (WIDTH, 0), (WIDTH, 170), (WIDTH - 160, 160)], fill=theme["accent"])
    
    # Top Branding & Website
    draw.text((60, 55), f"⚡ {BRAND_NAME.upper()}", fill=theme["white"], font=get_font(34, bold=True))
    draw.text((60, 105), f"🌐 {BRAND_WEBSITE} • {post_data.get('category', 'ADS STRATEGY')}", fill=theme["accent_light"], font=get_font(20, bold=True))
    
    # Decorative dots
    for r in range(4):
        for c in range(5):
            draw.ellipse([WIDTH - 180 + (c*18), 260 + (r*18), WIDTH - 176 + (c*18), 264 + (r*18)], fill=theme["accent"])
            
    # Headline
    h1 = post_data.get("graphic_title_line1", "WE HELP TO").upper()
    h2 = post_data.get("graphic_title_line2", "GROW YOUR BUSINESS").upper()
    draw.text((60, 240), h1, fill=theme["primary"], font=get_font(38, bold=True))
    
    wrapped_h2 = textwrap.fill(h2, width=18)
    draw.text((60, 295), wrapped_h2, fill=theme["accent"], font=get_font(64, bold=True), spacing=15)
    
    bbox = draw.textbbox((60, 295), wrapped_h2, font=get_font(64, bold=True), spacing=15)
    sub_y = bbox[3] + 25
    
    sub = post_data.get("graphic_subtitle", f"Visit {BRAND_WEBSITE} to scale your sales.")
    draw.text((60, sub_y), textwrap.fill(sub, width=42), fill=theme["text_muted"], font=get_font(26, bold=False), spacing=10)
    
    # Bullets card
    card_y = sub_y + 80
    card_h = 240
    draw.rounded_rectangle([60, card_y, WIDTH - 60, card_y + card_h], radius=24, fill=theme["card_bg"], outline=theme["accent"], width=2)
    
    bullets = post_data.get("bullet_points", ["Laser Targeted Ads", "Sales Funnels", "High-ROAS Creatives", "Full Tracking Setup"])
    for i, b in enumerate(bullets[:4]):
        row_y = card_y + 25 + (i * 50)
        draw.ellipse([85, row_y + 2, 115, row_y + 32], fill=theme["accent"])
        draw.text((93, row_y + 3), "✔", fill=theme["white"], font=get_font(22, bold=True))
        draw.text((130, row_y + 4), b, fill=theme["text_dark"], font=get_font(28, bold=True))
        
    # CTA button
    cta_y = card_y + card_h + 35
    draw.rounded_rectangle([60, cta_y, 440, cta_y + 65], radius=32, fill=theme["accent"])
    draw.text((95, cta_y + 16), f"🚀  {post_data.get('cta_text', 'BOOK FREE AUDIT')}", fill=theme["white"], font=get_font(26, bold=True))
    
    # Footer
    footer_y = HEIGHT - 100
    draw.rectangle([0, footer_y, WIDTH, HEIGHT], fill=theme["primary"])
    draw.text((60, footer_y + 32), BRAND_NAME.upper(), fill=theme["white"], font=get_font(28, bold=True))
    
    phone_text = f"📞 Call / WhatsApp: {BRAND_PHONE}"
    p_bbox = draw.textbbox((0, 0), phone_text, font=get_font(28, bold=True))
    draw.text((WIDTH - (p_bbox[2] - p_bbox[0]) - 60, footer_y + 32), phone_text, fill=theme["accent"], font=get_font(28, bold=True))
    
    img.save(output_path, "PNG", quality=95)
    print(f"[Image Engine] Facebook graphic generated: {output_path}")
    return output_path

def create_linkedin_graphic(post_data, output_path="li_graphic.png"):
    """
    LinkedIn Design Style: Clean Executive Infographic & Thought-Leadership Card.
    Structured, data-driven look with framework blocks, website, and authority styling.
    """
    WIDTH, HEIGHT = 1080, 1080
    theme = random.choice(LI_THEMES)
    img = Image.new("RGB", (WIDTH, HEIGHT), color=theme["card_bg"])
    draw = ImageDraw.Draw(img)
    
    margin = 40
    # Outer executive border
    draw.rectangle([margin, margin, WIDTH - margin, HEIGHT - margin], outline=theme["primary"], width=2)
    
    # Top Bar
    draw.rectangle([margin, margin, WIDTH - margin, 130], fill=theme["primary"])
    draw.text((70, 65), f"⚡ {BRAND_NAME.upper()}", fill=theme["white"], font=get_font(32, bold=True))
    draw.text((WIDTH - 360, 72), f"🌐 {BRAND_WEBSITE}", fill=theme["accent_light"], font=get_font(22, bold=True))
    
    # Category Tag
    draw.rounded_rectangle([70, 170, 380, 215], radius=8, fill=theme["accent_light"])
    draw.text((90, 182), post_data.get("category", "PERFORMANCE INSIGHT").upper(), fill=theme["primary"], font=get_font(18, bold=True))
    
    # Headline
    h1 = post_data.get("graphic_title_line1", "HOW TO SCALE").upper()
    h2 = post_data.get("graphic_title_line2", "REVENUE & LOWER CPA").upper()
    draw.text((70, 245), h1, fill=theme["text_muted"], font=get_font(36, bold=True))
    draw.text((70, 295), textwrap.fill(h2, width=22), fill=theme["primary"], font=get_font(52, bold=True), spacing=10)
    
    # Decorative rule
    draw.line([(70, 435), (250, 435)], fill=theme["accent"], width=5)
    
    # 4 Data / Framework Metric Cards
    card_y = 470
    card_w = (WIDTH - 140 - 24) // 2
    bullets = post_data.get("bullet_points", ["Creative Hook Testing", "Full Funnel Attribution", "Audience Segmentation", "Scaling Budget With ROAS"])
    
    for idx, b in enumerate(bullets[:4]):
        bx = 70 + (idx % 2) * (card_w + 24)
        by = card_y + (idx // 2) * 125
        draw.rounded_rectangle([bx, by, bx + card_w, by + 105], radius=14, fill=theme["white"], outline=theme["accent"], width=2)
        # Step number
        draw.rounded_rectangle([bx + 18, by + 18, bx + 65, by + 50], radius=8, fill=theme["accent_light"])
        draw.text((bx + 26, by + 24), f"0{idx+1}", fill=theme["primary"], font=get_font(18, bold=True))
        draw.text((bx + 80, by + 22), textwrap.fill(b, width=18), fill=theme["text_dark"], font=get_font(22, bold=True), spacing=4)
        
    # Strategy Callout Box
    box_y = 750
    draw.rounded_rectangle([70, box_y, WIDTH - 70, box_y + 130], radius=16, fill=theme["primary"])
    draw.text((100, box_y + 28), "LOOKING TO SCALE YOUR BUSINESS?", fill=theme["white"], font=get_font(26, bold=True))
    draw.text((100, box_y + 68), f"Book a 30-min strategy session or visit {BRAND_WEBSITE}", fill=theme["accent_light"], font=get_font(20, bold=False))
    
    # Footer Strip
    footer_y = HEIGHT - 110
    draw.rectangle([margin, footer_y, WIDTH - margin, HEIGHT - margin], fill=theme["accent"])
    draw.text((70, footer_y + 22), BRAND_NAME.upper(), fill=theme["white"], font=get_font(26, bold=True))
    draw.text((WIDTH - 460, footer_y + 22), f"Direct: {BRAND_PHONE}", fill=theme["white"], font=get_font(26, bold=True))
    
    img.save(output_path, "PNG", quality=95)
    print(f"[Image Engine] LinkedIn graphic generated: {output_path}")
    return output_path

if __name__ == "__main__":
    demo = {
        "category": "ADS AUDIT & STRATEGY",
        "graphic_title_line1": "WE HELP TO",
        "graphic_title_line2": "GROW YOUR BUSINESS",
        "graphic_subtitle": f"Visit {BRAND_WEBSITE} to scale your sales with data-driven ads.",
        "bullet_points": ["Laser Targeted Ads", "Conversion Funnels", "High-ROAS Creatives", "Full Tracking Setup"],
        "cta_text": "BOOK FREE AUDIT"
    }
    create_facebook_graphic(demo)
    create_linkedin_graphic(demo)
