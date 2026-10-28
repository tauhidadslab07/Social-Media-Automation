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
# COLOR PALETTE: Dark Luxury Tech (Midnight Obsidian, Electric Cyan, Gold Accent)
# ---------------------------------------------------------------------------
PALETTE = {
    "bg_base": (7, 10, 19),           # Midnight Obsidian
    "bg_secondary": (11, 16, 29),     # Slate Dark
    "accent_cyan": (0, 230, 255),     # Electric Cyan
    "accent_blue": (37, 99, 235),     # Royal Blue
    "accent_gold": (245, 158, 11),    # Amber Sun
    "accent_green": (16, 185, 129),   # Emerald Green
    "accent_red": (239, 68, 68),      # Alert Red
    "card_bg": (15, 23, 42, 230),     # Translucent Card
    "card_border": (0, 210, 255, 90),
    "text_white": (255, 255, 255),
    "text_muted": (148, 163, 184),
    "text_dark": (10, 15, 29)
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

def create_slide_base(width, height, slide_num, total_slides, category="E-COMMERCE TRACKING"):
    """Creates a unified 1080x1080 dark luxury slide canvas with ambient glow and brand header."""
    base = Image.new("RGBA", (width, height), PALETTE["bg_base"] + (255,))
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    # Ambient neon glows
    fp = PALETTE["accent_cyan"]
    for r in range(400, 0, -25):
        alpha = int(35 * (1 - (r / 400)))
        glow_draw.ellipse([width - 200 - r, -80 - r, width - 200 + r, -80 + r], fill=(fp[0], fp[1], fp[2], alpha))

    fs = PALETTE["accent_blue"]
    for r in range(350, 0, -25):
        alpha = int(25 * (1 - (r / 350)))
        glow_draw.ellipse([-60 - r, height - 120 - r, -60 + r, height - 120 + r], fill=(fs[0], fs[1], fs[2], alpha))

    composite = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(composite)

    # Dot grid texture
    for x in range(60, width - 40, 60):
        for y in range(80, height - 80, 60):
            draw.point((x, y), fill=(255, 255, 255, 18))

    # -------------------------------------------------------------
    # TOP HEADER: Brand Pill (Left) + Slide Number (Right)
    # -------------------------------------------------------------
    top_y = 50
    # Left Brand Pill
    pill_w, pill_h = 280, 42
    draw.rounded_rectangle(
        [50, top_y, 50 + pill_w, top_y + pill_h],
        radius=21,
        fill=(15, 23, 42, 230),
        outline=(0, 220, 255, 160),
        width=1
    )
    draw.ellipse([64, top_y + 15, 76, top_y + 27], fill=PALETTE["accent_green"])
    draw.text((86, top_y + 11), BRAND_NAME.upper(), fill=PALETTE["text_white"], font=get_font(16, bold=True))

    # Right: Slide Number Badge (e.g. 01 / 07)
    num_text = f"{slide_num:02d} / {total_slides:02d}"
    draw.rounded_rectangle(
        [width - 160, top_y, width - 50, top_y + pill_h],
        radius=21,
        fill=(30, 41, 59, 210),
        outline=(71, 85, 105, 180),
        width=1
    )
    draw.text((width - 142, top_y + 11), num_text, fill=PALETTE["accent_cyan"], font=get_font(16, bold=True))

    return composite

def render_cover_slide(width=1080, height=1080):
    """Slide 1: High-Impact Problem Hook Cover Slide."""
    img = create_slide_base(width, height, 1, 7, category="SHOPIFY & GA4 ATTRIBUTION")
    draw = ImageDraw.Draw(img)

    # Category capsule
    cat_y = 150
    draw.rounded_rectangle([50, cat_y, 350, cat_y + 36], radius=18, fill=(30, 41, 59, 230), outline=PALETTE["accent_gold"], width=1)
    draw.text((68, cat_y + 9), "● E-COMMERCE ATTRIBUTION", fill=PALETTE["accent_gold"], font=get_font(14, bold=True))

    # Massive Hook Headline
    y = 215
    draw.text((50, y), "WHY YOUR", fill=PALETTE["text_white"], font=get_font(48, bold=True))
    y += 65
    draw.text((50, y), "SHOPIFY REVENUE", fill=PALETTE["accent_cyan"], font=get_font(60, bold=True))
    y += 78
    draw.text((50, y), "& GA4 SALES NEVER MATCH", fill=PALETTE["text_white"], font=get_font(44, bold=True))
    y += 65

    # Subtitle
    sub = "And the 4-step server-side fix to reconcile your store's sales and bank deposits 1:1."
    draw.text((50, y), textwrap.fill(sub, width=44), fill=PALETTE["text_muted"], font=get_font(21, bold=False), spacing=6)

    # Hero Visual Card: The Mismatch Showcase
    card_y = 480
    card_h = 360
    draw.rounded_rectangle([50, card_y, width - 50, card_y + card_h], radius=22, fill=PALETTE["card_bg"], outline=(0, 220, 255, 90), width=1)

    # Left: Shopify Card
    draw.rounded_rectangle([80, card_y + 40, 500, card_y + card_h - 40], radius=16, fill=(11, 20, 36), outline=(16, 185, 129, 120), width=1)
    draw.text((110, card_y + 65), "🟢 SHOPIFY BACKEND", fill=PALETTE["accent_green"], font=get_font(18, bold=True))
    draw.text((110, card_y + 110), "$52,400.00", fill=PALETTE["text_white"], font=get_font(38, bold=True))
    draw.text((110, card_y + 175), "Real Verified Orders: 412", fill=PALETTE["text_muted"], font=get_font(17, bold=False))
    draw.text((110, card_y + 215), "Bank Deposits: 100% Cleared", fill=PALETTE["accent_green"], font=get_font(16, bold=True))

    # VS Divider
    draw.text((525, card_y + 150), "VS", fill=PALETTE["accent_gold"], font=get_font(24, bold=True))

    # Right: GA4 Card
    draw.rounded_rectangle([580, card_y + 40, width - 80, card_y + card_h - 40], radius=16, fill=(20, 15, 25), outline=(239, 68, 68, 120), width=1)
    draw.text((610, card_y + 65), "🔴 GA4 BROWSER PIXEL", fill=PALETTE["accent_red"], font=get_font(18, bold=True))
    draw.text((610, card_y + 110), "$38,900.00", fill=PALETTE["accent_red"], font=get_font(38, bold=True))
    draw.text((610, card_y + 175), "Reported Orders: 305", fill=PALETTE["text_muted"], font=get_font(17, bold=False))
    draw.text((610, card_y + 215), "Missing Revenue: -$13,500 (26%)", fill=PALETTE["accent_gold"], font=get_font(16, bold=True))

    # Bottom Swipe Prompt
    dock_y = height - 120
    draw.rounded_rectangle([50, dock_y, width - 50, dock_y + 70], radius=20, fill=(15, 23, 42, 240), outline=(59, 130, 246, 120), width=1)
    draw.text((80, dock_y + 24), "👉 SWIPE THROUGH TO SEE HOW WE FIX IT 1:1", fill=PALETTE["accent_cyan"], font=get_font(18, bold=True))
    draw.text((width - 150, dock_y + 24), "SWIPE ➡", fill=PALETTE["text_white"], font=get_font(18, bold=True))

    return img.convert("RGB")

def render_step_slide(slide_num, total_slides, step_tag, title_line1, title_line2, subhead, cards, width=1080, height=1080):
    """Renders structured educational slides with numbered points and high-contrast cards."""
    img = create_slide_base(width, height, slide_num, total_slides)
    draw = ImageDraw.Draw(img)

    # Step pill
    draw.rounded_rectangle([50, 140, 250, 174], radius=17, fill=(30, 41, 59, 230), outline=PALETTE["accent_cyan"], width=1)
    draw.text((68, 147), step_tag.upper(), fill=PALETTE["accent_cyan"], font=get_font(14, bold=True))

    # Headline
    y = 195
    draw.text((50, y), title_line1.upper(), fill=PALETTE["text_white"], font=get_font(42, bold=True))
    y += 56
    draw.text((50, y), title_line2.upper(), fill=PALETTE["accent_cyan"], font=get_font(46, bold=True))
    y += 65

    # Subhead
    draw.text((50, y), textwrap.fill(subhead, width=50), fill=PALETTE["text_muted"], font=get_font(19, bold=False), spacing=5)

    # Content Cards (1 to 3 cards)
    card_y = y + 70
    card_h = 140
    gap = 25

    for i, c in enumerate(cards):
        cy = card_y + (i * (card_h + gap))
        # Container box
        draw.rounded_rectangle([50, cy, width - 50, cy + card_h], radius=18, fill=PALETTE["card_bg"], outline=(51, 65, 85, 180), width=1)
        
        # Icon badge
        icon_bg = c.get("icon_color", PALETTE["accent_cyan"])
        draw.ellipse([75, cy + 28, 125, cy + 78], fill=icon_bg)
        draw.text((90, cy + 38), c.get("icon", "✔"), fill=(10, 15, 29), font=get_font(26, bold=True))

        # Title & Description
        draw.text((145, cy + 24), c["title"], fill=PALETTE["text_white"], font=get_font(21, bold=True))
        desc_wrapped = textwrap.fill(c["desc"], width=46)
        draw.text((145, cy + 62), desc_wrapped, fill=PALETTE["text_muted"], font=get_font(16, bold=False), spacing=4)

    # Bottom footer cue
    draw.text((50, height - 70), f"🌐 {BRAND_WEBSITE}", fill=PALETTE["accent_cyan"], font=get_font(16, bold=True))
    draw.text((width - 180, height - 70), "SWIPE FOR NEXT ➡", fill=PALETTE["text_muted"], font=get_font(15, bold=False))

    return img.convert("RGB")

def render_outro_slide(width=1080, height=1080):
    """Slide 7: High-Conversion Outro / CTA Slide."""
    img = create_slide_base(width, height, 7, 7)
    draw = ImageDraw.Draw(img)

    # Category capsule
    draw.rounded_rectangle([50, 140, 310, 174], radius=17, fill=(30, 41, 59, 230), outline=PALETTE["accent_green"], width=1)
    draw.text((68, 147), "● ACTIONABLE NEXT STEP", fill=PALETTE["accent_green"], font=get_font(14, bold=True))

    # Headline
    y = 195
    draw.text((50, y), "STOP GUESSING YOUR ROAS.", fill=PALETTE["text_white"], font=get_font(42, bold=True))
    y += 56
    draw.text((50, y), "SCALE ON 100% VERIFIED DATA.", fill=PALETTE["accent_cyan"], font=get_font(46, bold=True))
    y += 75

    # Promise Statement Card
    draw.rounded_rectangle([50, y, width - 50, y + 210], radius=20, fill=PALETTE["card_bg"], outline=(0, 220, 255, 120), width=1)
    draw.text((80, y + 25), "🎯 THE TAUHID ADS LAB PROMISE", fill=PALETTE["accent_gold"], font=get_font(20, bold=True))
    points = [
        "1:1 Reconciliation between Shopify & GA4 revenue.",
        "Zero duplicate purchases & zero ad-blocker dropouts.",
        "Smart Bidding algorithms train on actual bank cash.",
        "Full Server-Side GTM + Meta CAPI architecture."
    ]
    py = y + 65
    for p in points:
        draw.text((80, py), f"✔ {p}", fill=PALETTE["text_white"], font=get_font(17, bold=False))
        py += 34

    # Big CTA Action Block
    action_y = y + 245
    draw.rounded_rectangle([50, action_y, width - 50, action_y + 190], radius=22, fill=(15, 23, 42, 250), outline=PALETTE["accent_cyan"], width=2)
    draw.text((80, action_y + 24), "🚀 CLAIM YOUR FREE 30-MIN TRACKING AUDIT", fill=PALETTE["accent_cyan"], font=get_font(23, bold=True))

    # Buttons
    # WhatsApp Pill
    wa_w = 420
    draw.rounded_rectangle([80, action_y + 70, 80 + wa_w, action_y + 125], radius=27, fill=(37, 211, 102))
    draw.text((110, action_y + 86), f"💬 WhatsApp: {BRAND_PHONE}", fill=(10, 15, 29), font=get_font(19, bold=True))

    # Calendly Pill
    draw.rounded_rectangle([530, action_y + 70, width - 80, action_y + 125], radius=27, fill=(30, 41, 59, 230), outline=(71, 85, 105, 200), width=1)
    draw.text((555, action_y + 86), f"📅 {BRAND_CALENDLY}", fill=PALETTE["text_white"], font=get_font(17, bold=True))

    # Website footer
    draw.text((80, action_y + 148), f"🌐 Official Portal: {BRAND_WEBSITE} | Led by Md. Tauhidul Islam Bhuian", fill=PALETTE["text_muted"], font=get_font(15, bold=False))

    return img.convert("RGB")

def build_shopify_ga4_carousel(output_dir="carousel_output"):
    """
    Generates all 7 slides for 'Why Your Shopify Revenue and GA4 Sales Never Match',
    exports individual PNG slides for Facebook & Instagram Carousel,
    and compiles them into a pristine PDF document for LinkedIn Carousel!
    """
    os.makedirs(output_dir, exist_ok=True)
    slides = []

    # Slide 1: Cover
    cover_path = os.path.join(os.path.dirname(__file__), "cover_slide.jpg")
    if os.path.exists(cover_path):
        s1 = Image.open(cover_path).convert("RGB")
    else:
        s1 = render_cover_slide()
    slides.append(s1)

    # Slide 2: The Discrepancy
    s2 = render_step_slide(
        slide_num=2,
        total_slides=7,
        step_tag="01 / The Invisible Leak",
        title_line1="The 20% Revenue Gap",
        title_line2="In Modern E-Commerce",
        subhead="Most store owners scale ads based on completely distorted data.",
        cards=[
            {
                "icon": "❌",
                "icon_color": PALETTE["accent_red"],
                "title": "Shopify Backend vs GA4 Dashboard",
                "desc": "Your store records $52,400 in real orders. GA4 reports $38,900 (or $64,200 due to duplicate page refreshes)."
            },
            {
                "icon": "⚠️",
                "icon_color": PALETTE["accent_gold"],
                "title": "Ad Algorithms Optimize on Fiction",
                "desc": "When purchase signals are missing or inflated, Google Smart Bidding and Meta Advantage+ bid on the wrong audiences."
            }
        ]
    )
    slides.append(s2)

    # Slide 3: The 3 Root Causes
    s3 = render_step_slide(
        slide_num=3,
        total_slides=7,
        step_tag="02 / Root Causes",
        title_line1="The 3 Client-Side",
        title_line2="Tracking Killers",
        subhead="Why traditional browser pixels fail consistently on modern web stores.",
        cards=[
            {
                "icon": "1",
                "icon_color": PALETTE["accent_cyan"],
                "title": "Thank-You Page Refreshes",
                "desc": "Customers reload the confirmation tab to check tracking status, triggering duplicate purchase events."
            },
            {
                "icon": "2",
                "icon_color": PALETTE["accent_cyan"],
                "title": "Offsite Payment Redirects",
                "desc": "Shoppers paying via PayPal, Klarna, or bank apps close the tab before returning to your store."
            },
            {
                "icon": "3",
                "icon_color": PALETTE["accent_cyan"],
                "title": "Ad Blockers & Safari ITP",
                "desc": "Over 25% of modern buyers run privacy shields that block client-side Google Tag Manager completely."
            }
        ]
    )
    slides.append(s3)

    # Slide 4: The Architecture Fix
    s4 = render_step_slide(
        slide_num=4,
        total_slides=7,
        step_tag="03 / Architecture Fix",
        title_line1="Server-Side Webhooks",
        title_line2="Bypass Browser Flaws",
        subhead="Moving conversion triggers from the fragile user browser to the cloud.",
        cards=[
            {
                "icon": "⚡",
                "icon_color": PALETTE["accent_green"],
                "title": "Direct Shopify Server Webhook",
                "desc": "The moment payment clears in Shopify, an encrypted webhook fires directly to your private Server-Side GTM container."
            },
            {
                "icon": "🛡️",
                "icon_color": PALETTE["accent_green"],
                "title": "100% Delivery Reliability",
                "desc": "It fires even if the buyer closes their browser, uses Brave, runs uBlock, or experiences a sudden connection drop."
            }
        ]
    )
    slides.append(s4)

    # Slide 5: Transaction ID Deduplication
    s5 = render_step_slide(
        slide_num=5,
        total_slides=7,
        step_tag="04 / Data Integrity",
        title_line1="Unique Transaction ID",
        title_line2="Deduplication Shield",
        subhead="Ensuring mathematical 1:1 precision between orders and analytics.",
        cards=[
            {
                "icon": "🔑",
                "icon_color": PALETTE["accent_cyan"],
                "title": "Single Truth Event ID",
                "desc": "Every order is tagged with a unique Shopify order ID. GA4 strictly accepts the first payload and ignores duplicates."
            },
            {
                "icon": "📊",
                "icon_color": PALETTE["accent_cyan"],
                "title": "Zero Phantom Revenue",
                "desc": "Receipt refreshes and bookmarked confirmation URLs will never inflate your ROAS again."
            }
        ]
    )
    slides.append(s5)

    # Slide 6: The Transformation & ROI
    s6 = render_step_slide(
        slide_num=6,
        total_slides=7,
        step_tag="05 / The Outcome",
        title_line1="1:1 Revenue Match",
        title_line2="Scale With Confidence",
        subhead="What happens when your ad networks see 100% of your real cash.",
        cards=[
            {
                "icon": "📈",
                "icon_color": PALETTE["accent_green"],
                "title": "99%+ Match Accuracy",
                "desc": "Your GA4 e-commerce revenue reconciles 1:1 with your Stripe and bank deposit statements."
            },
            {
                "icon": "🎯",
                "icon_color": PALETTE["accent_green"],
                "title": "Lower Cost Per Acquisition",
                "desc": "Meta and Google AI bidding algorithms optimize for your actual high-margin paying customers."
            }
        ]
    )
    slides.append(s6)

    # Slide 7: Outro / CTA
    s7 = render_outro_slide()
    slides.append(s7)

    # Save individual slide images (for Facebook & Instagram Carousel)
    image_paths = []
    for idx, slide in enumerate(slides):
        p = os.path.join(output_dir, f"slide_{idx + 1}.png")
        slide.save(p, "PNG", quality=98)
        image_paths.append(p)
        print(f"[Carousel Engine] Generated Slide {idx + 1}: {p}")

    # Compile all slides into a high-res PDF Document for LinkedIn Carousel
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
