import os
import textwrap
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv

load_dotenv()

BRAND_NAME = os.getenv("BRAND_NAME", "Tauhid Ads Lab")
BRAND_PHONE = os.getenv("BRAND_PHONE", "+8801624608468")
BRAND_WEBSITE = os.getenv("BRAND_WEBSITE", "tauhidadslab.com").replace("http://", "").replace("https://", "").strip("/")
BRAND_CALENDLY = os.getenv("BRAND_CALENDLY", "calendly.com/tauhidadslab/30min").replace("https://", "").replace("http://", "")

# ---------------------------------------------------------------------------
# COLOR PALETTE: Minimalist Swiss Red & Black (Inspired by Template a1c44fef)
# ---------------------------------------------------------------------------
PALETTE = {
    "bg_base": (248, 248, 249),         # Pristine Swiss Off-White
    "bg_card": (255, 255, 255),         # Crisp Pure White
    "card_border": (226, 232, 240),     # Subtle Slate Border
    "text_black": (17, 17, 17),         # Pitch Black (Swiss Grotesk)
    "text_red": (200, 16, 46),          # Crimson Red Accent
    "text_charcoal": (71, 85, 105),     # Refined Subtitle
    "text_muted": (148, 163, 184),      # Micro Index & Cues
    "accent_green": (16, 185, 129),     # Emerald Status
    "accent_gold": (217, 119, 6),       # Warm Amber
    # Dark Mode Slide (Slide 4 Contrast)
    "dark_bg": (15, 18, 24),
    "dark_card": (24, 28, 38),
    "dark_border": (45, 55, 72)
}

def get_font(size, bold=False):
    """Locates modern UI fonts across Windows and Linux environments."""
    candidates = []
    if os.name == 'nt':
        candidates.extend([
            f"C:\\Windows\\Fonts\\{'segoeuib.ttf' if bold else 'segoeui.ttf'}",
            f"C:\\Windows\\Fonts\\{'arialbd.ttf' if bold else 'arial.ttf'}",
            f"C:\\Windows\\Fonts\\{'tahomabd.ttf' if bold else 'tahoma.ttf'}"
        ])
    candidates.extend([
        f"/usr/share/fonts/truetype/dejavu/{'DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf'}",
        f"/usr/share/fonts/truetype/freefont/{'FreeSansBold.ttf' if bold else 'FreeSans.ttf'}"
    ])
    for p in candidates:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    try:
        return ImageFont.load_default()
    except Exception:
        return None

def create_swiss_slide_base(width, height, slide_num, total_slides, is_dark=False):
    """
    Renders a pristine Minimalist Swiss canvas:
    - Off-white paper background (or contrast obsidian for dark slides)
    - Top center minimalist agency mark with crimson red dot
    - Top right slide index: '02/07'
    - Bottom left red accent dash
    - Bottom right subtle 'SWIPE ➔' cue
    """
    bg_color = PALETTE["dark_bg"] if is_dark else PALETTE["bg_base"]
    img = Image.new("RGBA", (width, height), bg_color + (255,))
    draw = ImageDraw.Draw(img)

    # 1. Top Center Minimalist Geometric Logo Mark
    center_x = width // 2
    logo_y = 50
    # Minimalist bracket / node icon
    logo_color = (255, 255, 255) if is_dark else PALETTE["text_black"]
    draw.polygon([
        (center_x - 14, logo_y),
        (center_x, logo_y - 12),
        (center_x + 14, logo_y),
        (center_x + 7, logo_y + 16),
        (center_x - 7, logo_y + 16)
    ], fill=logo_color)
    # Crimson red accent dot
    draw.ellipse([center_x + 10, logo_y - 14, center_x + 18, logo_y - 6], fill=PALETTE["text_red"])

    # 2. Top Right Slide Index (e.g. 02/07)
    index_text = f"{slide_num:02d}/{total_slides:02d}"
    index_color = (148, 163, 184) if is_dark else PALETTE["text_charcoal"]
    draw.text((width - 120, logo_y - 5), index_text, fill=index_color, font=get_font(20, bold=False))

    # 3. Bottom Accents
    bottom_y = height - 55
    # Red accent dash (Bottom Left)
    draw.rounded_rectangle([70, bottom_y, 110, bottom_y + 6], radius=3, fill=PALETTE["text_red"])

    # Bottom Right Cue
    if slide_num < total_slides:
        cue_color = (148, 163, 184) if is_dark else PALETTE["text_charcoal"]
        draw.text((width - 160, bottom_y - 8), "SWIPE ➔", fill=cue_color, font=get_font(18, bold=True))
    else:
        web_color = (0, 220, 255) if is_dark else PALETTE["text_red"]
        draw.text((width - 240, bottom_y - 8), f"🌐 {BRAND_WEBSITE}", fill=web_color, font=get_font(16, bold=True))

    return img

def render_swiss_step_slide(slide_num, total_slides, line1, line2, subhead, cards, is_dark=False, width=1080, height=1080):
    """
    Renders structured Minimalist Swiss slides with bold two-tone typography
    and clean floating white cards with generous breathing room.
    """
    img = create_swiss_slide_base(width, height, slide_num, total_slides, is_dark=is_dark)
    draw = ImageDraw.Draw(img)

    # 1. Dominant Swiss Headline
    y = 150
    h1_color = (255, 255, 255) if is_dark else PALETTE["text_black"]
    h2_color = PALETTE["text_red"]
    
    draw.text((70, y), line1.upper(), fill=h1_color, font=get_font(44, bold=True))
    y += 58
    draw.text((70, y), line2.upper(), fill=h2_color, font=get_font(48, bold=True))
    y += 68

    # 2. Refined Subhead
    sub_color = (203, 213, 225) if is_dark else PALETTE["text_charcoal"]
    draw.text((70, y), textwrap.fill(subhead, width=48), fill=sub_color, font=get_font(21, bold=False), spacing=6)
    y += 75

    # 3. Floating Content Cards
    card_bg = PALETTE["dark_card"] if is_dark else PALETTE["bg_card"]
    card_border = PALETTE["dark_border"] if is_dark else PALETTE["card_border"]
    title_color = (255, 255, 255) if is_dark else PALETTE["text_black"]
    desc_color = (148, 163, 184) if is_dark else PALETTE["text_charcoal"]

    card_h = 135
    gap = 22
    for i, c in enumerate(cards):
        cy = y + (i * (card_h + gap))
        
        # Crisp card with subtle shadow / border
        draw.rounded_rectangle(
            [70, cy, width - 70, cy + card_h],
            radius=16,
            fill=card_bg,
            outline=card_border,
            width=1
        )

        # Number Badge or Icon
        badge_bg = c.get("badge_bg", PALETTE["text_red"] if i == 0 else (30, 41, 59))
        draw.ellipse([95, cy + 26, 145, cy + 76], fill=badge_bg)
        draw.text((112, cy + 36), str(c.get("badge", i + 1)), fill=(255, 255, 255), font=get_font(22, bold=True))

        # Title & Description
        draw.text((170, cy + 24), c["title"], fill=title_color, font=get_font(22, bold=True))
        desc_wrapped = textwrap.fill(c["desc"], width=44)
        draw.text((170, cy + 62), desc_wrapped, fill=desc_color, font=get_font(17, bold=False), spacing=4)

    return img.convert("RGB")

def render_swiss_outro_slide(width=1080, height=1080):
    """Slide 7: Minimalist Swiss Outro & High-Converting CTA."""
    img = create_swiss_slide_base(width, height, 7, 7, is_dark=False)
    draw = ImageDraw.Draw(img)

    y = 150
    draw.text((70, y), "SCALE WITH CONFIDENCE.", fill=PALETTE["text_black"], font=get_font(44, bold=True))
    y += 58
    draw.text((70, y), "FIX YOUR TRACKING TODAY.", fill=PALETTE["text_red"], font=get_font(48, bold=True))
    y += 70

    sub = "Stop scaling on broken client-side data. Reconcile your analytics 1:1 with bank deposits."
    draw.text((70, y), textwrap.fill(sub, width=46), fill=PALETTE["text_charcoal"], font=get_font(21, bold=False), spacing=6)
    y += 85

    # Clean White Checklist Card
    card_h = 220
    draw.rounded_rectangle([70, y, width - 70, y + card_h], radius=18, fill=PALETTE["bg_card"], outline=PALETTE["card_border"], width=1)
    
    draw.text((105, y + 25), "🎯 THE TAUHID ADS LAB RECONCILIATION", fill=PALETTE["text_black"], font=get_font(20, bold=True))
    points = [
        "1:1 Reconciliation between Shopify & GA4 revenue.",
        "Zero duplicate orders from thank-you page reloads.",
        "Immune to Safari ITP 7-day wipes and ad-blockers.",
        "Server-Side GTM + Webhook deduplication architecture."
    ]
    py = y + 68
    for p in points:
        draw.text((105, py), f"✔ {p}", fill=PALETTE["text_charcoal"], font=get_font(18, bold=False))
        py += 36

    # Bottom Action Dock
    action_y = y + 250
    draw.rounded_rectangle([70, action_y, width - 70, action_y + 160], radius=18, fill=(17, 24, 39), outline=(30, 41, 59), width=1)
    draw.text((100, action_y + 22), "🚀 CLAIM YOUR FREE 30-MIN TRACKING AUDIT", fill=(255, 255, 255), font=get_font(22, bold=True))

    # WhatsApp Button
    draw.rounded_rectangle([100, action_y + 65, 520, action_y + 118], radius=24, fill=(37, 211, 102))
    draw.text((125, action_y + 80), f"💬 WhatsApp: {BRAND_PHONE}", fill=(10, 15, 29), font=get_font(18, bold=True))

    # Calendly Button
    draw.rounded_rectangle([545, action_y + 65, width - 100, action_y + 118], radius=24, fill=(30, 41, 59), outline=(71, 85, 105), width=1)
    draw.text((570, action_y + 80), "📅 Book Strategy Call", fill=(255, 255, 255), font=get_font(17, bold=True))

    draw.text((100, action_y + 132), f"🌐 {BRAND_WEBSITE} | Led by Md. Tauhidul Islam Bhuian", fill=(148, 163, 184), font=get_font(14, bold=False))

    return img.convert("RGB")

def build_shopify_ga4_carousel(output_dir="carousel_output"):
    """
    Builds the complete 7-slide Minimalist Swiss Carousel:
    - Slide 1: Ultra-crisp cover_slide.jpg (Minimalist Swiss Red & Black)
    - Slide 2: The 20% Revenue Gap (Off-white)
    - Slide 3: The 3 Hidden Attribution Killers (Off-white)
    - Slide 4: Server-Side GTM, Not Browser Pixels (Dark contrast slide)
    - Slide 5: Transaction ID Deduplication Handshake (Off-white)
    - Slide 6: 1:1 Revenue Reconciliation (Off-white)
    - Slide 7: Actionable Outro / Free Audit (Off-white)
    Compiles into PDF for LinkedIn & individual PNGs for Facebook!
    """
    os.makedirs(output_dir, exist_ok=True)
    slides = []

    # Slide 1: Master Cover Slide
    cover_path = os.path.join(os.path.dirname(__file__), "cover_slide.jpg")
    if os.path.exists(cover_path):
        s1 = Image.open(cover_path).convert("RGB")
    else:
        # Fallback render if cover image missing
        s1 = render_swiss_step_slide(1, 7, "Why Shopify & GA4", "Never Match.", "How a 20% tracking gap is quietly inflating your ad costs.", [])
    slides.append(s1)

    # Slide 2: The Discrepancy
    s2 = render_swiss_step_slide(
        slide_num=2,
        total_slides=7,
        line1="The 20% Revenue Gap",
        line2="Where Does It Go?",
        subhead="Most e-commerce stores scale ad spend on completely distorted data.",
        cards=[
            {
                "badge": "1",
                "badge_bg": PALETTE["text_red"],
                "title": "Shopify Backend vs GA4 Dashboard",
                "desc": "Your store records $52,400 in real orders. GA4 reports $38,900 (or $64,200 due to duplicate page reloads)."
            },
            {
                "badge": "2",
                "badge_bg": (30, 41, 59),
                "title": "Ad Algorithms Optimize on Fiction",
                "desc": "When purchase signals are missing or doubled, Google & Meta AI bid on the wrong audiences, inflating CPA."
            }
        ]
    )
    slides.append(s2)

    # Slide 3: The 3 Root Causes
    s3 = render_swiss_step_slide(
        slide_num=3,
        total_slides=7,
        line1="The 3 Silent",
        line2="Attribution Killers",
        subhead="Why traditional client-side pixels fail consistently on modern web stores.",
        cards=[
            {
                "badge": "01",
                "badge_bg": PALETTE["text_red"],
                "title": "Thank-You Page Refreshes",
                "desc": "Customers reload confirmation tabs to check delivery status, firing duplicate purchase conversions."
            },
            {
                "badge": "02",
                "badge_bg": (30, 41, 59),
                "title": "Offsite Payment Redirects",
                "desc": "Shoppers paying via PayPal, Klarna, or bank apps close the tab before returning to your thank-you page."
            },
            {
                "badge": "03",
                "badge_bg": (30, 41, 59),
                "title": "Ad Blockers & Safari ITP",
                "desc": "Over 25% of modern buyers run privacy shields that terminate client-side Google Tag Manager completely."
            }
        ]
    )
    slides.append(s3)

    # Slide 4: Contrast Dark Slide (Like Slide 4 in template a1c44)
    s4 = render_swiss_step_slide(
        slide_num=4,
        total_slides=7,
        line1="Server-Side GTM,",
        line2="Not Browser Pixels.",
        subhead="Moving conversion triggers from the fragile user browser to a private cloud server.",
        cards=[
            {
                "badge": "⚡",
                "badge_bg": PALETTE["text_red"],
                "title": "Direct Shopify Server Webhook",
                "desc": "The millisecond payment clears in Shopify, an encrypted webhook fires directly to your private sGTM server."
            },
            {
                "badge": "🛡️",
                "badge_bg": (37, 99, 235),
                "title": "100% Delivery Reliability",
                "desc": "It fires even if the buyer closes their browser, uses Brave, runs uBlock, or experiences connection drops."
            }
        ],
        is_dark=True
    )
    slides.append(s4)

    # Slide 5: Deduplication Handshake
    s5 = render_swiss_step_slide(
        slide_num=5,
        total_slides=7,
        line1="Transaction ID",
        line2="Deduplication Shield",
        subhead="Ensuring mathematical 1:1 precision between orders and analytics.",
        cards=[
            {
                "badge": "🔑",
                "badge_bg": PALETTE["text_red"],
                "title": "Single Truth Event ID",
                "desc": "Every order is locked with a unique Shopify order ID. GA4 strictly accepts the first payload and ignores duplicates."
            },
            {
                "badge": "📊",
                "badge_bg": (30, 41, 59),
                "title": "Zero Phantom Revenue",
                "desc": "Receipt refreshes and bookmarked confirmation URLs will never inflate your ROAS again."
            }
        ]
    )
    slides.append(s5)

    # Slide 6: The Outcome
    s6 = render_swiss_step_slide(
        slide_num=6,
        total_slides=7,
        line1="1:1 Revenue Match",
        line2="Scale With Confidence",
        subhead="What happens when your ad networks see 100% of your real cash.",
        cards=[
            {
                "badge": "📈",
                "badge_bg": PALETTE["text_red"],
                "title": "99%+ Match Accuracy",
                "desc": "Your GA4 e-commerce revenue reconciles 1:1 with your Stripe and bank deposit statements."
            },
            {
                "badge": "🎯",
                "badge_bg": (30, 41, 59),
                "title": "Lower Cost Per Acquisition",
                "desc": "Meta and Google AI bidding algorithms optimize for your actual high-margin paying customers."
            }
        ]
    )
    slides.append(s6)

    # Slide 7: Outro / CTA
    s7 = render_swiss_outro_slide()
    slides.append(s7)

    # Save individual slide images
    image_paths = []
    for idx, slide in enumerate(slides):
        p = os.path.join(output_dir, f"slide_{idx + 1}.png")
        slide.save(p, "PNG", quality=98)
        image_paths.append(p)
        print(f"[Carousel Engine] Generated Slide {idx + 1}: {p}")

    # Compile PDF for LinkedIn
    pdf_path = os.path.join(output_dir, "shopify_ga4_tracking_carousel.pdf")
    slides[0].save(
        pdf_path,
        "PDF",
        resolution=100.0,
        save_all=True,
        append_images=slides[1:]
    )
    print(f"[Carousel Engine] Compiled LinkedIn PDF Carousel: {pdf_path}")

    return image_paths, pdf_path

if __name__ == "__main__":
    imgs, pdf = build_shopify_ga4_carousel()
    print(f"Total Slides: {len(imgs)}")
    print(f"PDF Carousel: {pdf}")
