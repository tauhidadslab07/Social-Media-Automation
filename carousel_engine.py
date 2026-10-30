import os
import math
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from dotenv import load_dotenv

load_dotenv()

BRAND_NAME = os.getenv("BRAND_NAME", "Tauhid Ads Lab")
FOUNDER_NAME = "Md. Tauhidul Islam Bhuian"
BRAND_PHONE = os.getenv("BRAND_PHONE", "+8801624608468")
BRAND_WEBSITE = os.getenv("BRAND_WEBSITE", "tauhidadslab.com").replace("http://", "").replace("https://", "").strip("/")
BRAND_CALENDLY = os.getenv("BRAND_CALENDLY", "calendly.com/tauhidadslab/30min").replace("https://", "").replace("http://", "")

# ---------------------------------------------------------------------------
# BRAND PALETTE (Calibrated to tauhidadslab.com & Viral Emerald Carousel)
# ---------------------------------------------------------------------------
WIDTH = 1080
HEIGHT = 1350

COLORS = {
    "bg_base": (6, 9, 19),             # Midnight Obsidian
    "bg_teal": (8, 28, 24),            # Dark Forest Teal
    "flare_emerald": (34, 197, 94),    # Emerald Glow (#22C55E)
    "flare_cyan": (56, 189, 248),      # Electric Cyan (#38BDF8)
    "text_white": (255, 255, 255),
    "text_slate": (148, 163, 184),     # #94A3B8
    "text_muted": (100, 116, 139),
    "accent_emerald": (34, 197, 94),
    "accent_cyan": (56, 189, 248),
    "divider": (255, 255, 255, 42),
    "card_glass": (255, 255, 255, 18),
    "card_border": (255, 255, 255, 45),
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

def create_base_canvas():
    """
    Renders the signature 1080x1350 canvas:
    - Midnight obsidian to forest teal radial gradient
    - Soft emerald and cyan ambient flares
    """
    # 1. Base image with vertical gradient from teal to obsidian
    base = Image.new("RGBA", (WIDTH, HEIGHT), COLORS["bg_base"] + (255,))
    
    # Gradient overlay
    grad = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(grad)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(COLORS["bg_teal"][0] * (1 - ratio) + COLORS["bg_base"][0] * ratio)
        g = int(COLORS["bg_teal"][1] * (1 - ratio) + COLORS["bg_base"][1] * ratio)
        b = int(COLORS["bg_teal"][2] * (1 - ratio) + COLORS["bg_base"][2] * ratio)
        g_draw.line([(0, y), (WIDTH, y)], fill=(r, g, b, 255))
    
    base = Image.alpha_composite(base, grad)

    # 2. Top-Center Emerald Radial Flare
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    
    cx, cy = WIDTH // 2, 320
    fe = COLORS["flare_emerald"]
    for r in range(540, 0, -25):
        alpha = int(48 * (1 - (r / 540)))
        glow_draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(fe[0], fe[1], fe[2], alpha))

    # Bottom-Right Cyan Flare
    fc = COLORS["flare_cyan"]
    for r in range(450, 0, -30):
        alpha = int(25 * (1 - (r / 450)))
        glow_draw.ellipse([WIDTH + 50 - r, HEIGHT - 100 - r, WIDTH + 50 + r, HEIGHT - 100 + r], fill=(fc[0], fc[1], fc[2], alpha))

    base = Image.alpha_composite(base, glow)
    return base

def draw_header(draw, guide_text="Learn in 5 Slides ➔"):
    """Renders the top brand header, T logo icon, and horizontal divider."""
    hx, hy = 80, 70
    
    # Gradient T icon badge
    badge_size = 40
    draw.rounded_rectangle(
        [hx, hy, hx + badge_size, hy + badge_size],
        radius=10,
        fill=(14, 165, 233),
        outline=(56, 189, 248),
        width=1
    )
    t_font = get_font(20, bold=True)
    draw.text((hx + 13, hy + 8), "T", fill=(255, 255, 255), font=t_font)

    # Brand Title: TAUHID (White) ADS (Cyan) LAB (Emerald)
    tx = hx + badge_size + 14
    brand_font = get_font(24, bold=True)
    draw.text((tx, hy + 5), "TAUHID ", fill=(255, 255, 255), font=brand_font)
    w_t = draw.textbbox((0, 0), "TAUHID ", font=brand_font)[2]
    draw.text((tx + w_t, hy + 5), "ADS ", fill=(56, 189, 248), font=brand_font)
    w_a = draw.textbbox((0, 0), "ADS ", font=brand_font)[2]
    draw.text((tx + w_t + w_a, hy + 5), "LAB", fill=(34, 197, 94), font=brand_font)

    # Right Guide Text
    guide_font = get_font(22, bold=False)
    g_w = draw.textbbox((0, 0), guide_text, font=guide_font)[2]
    draw.text((WIDTH - 80 - g_w, hy + 7), guide_text, fill=(203, 213, 225), font=guide_font)

    # Horizontal Divider Line
    draw.line([(80, hy + 58), (WIDTH - 80, hy + 58)], fill=(255, 255, 255, 45), width=2)

def draw_footer_and_progress(draw, active_step=1, total_steps=5, all_active=False):
    """
    Renders the 5-segment progress bar and the bottom footer:
    - Founder Name on left
    - Agency website on right
    """
    # 1. Segmented Progress Bar
    bar_y = HEIGHT - 145
    bar_x = 80
    avail_w = WIDTH - 160
    gap = 12
    seg_w = (avail_w - (gap * (total_steps - 1))) / total_steps

    for i in range(total_steps):
        sx = bar_x + i * (seg_w + gap)
        if all_active:
            col = (34, 197, 94, 255)
        elif i + 1 == active_step:
            col = (255, 255, 255, 255)
        else:
            col = (255, 255, 255, 55)

        draw.rounded_rectangle([sx, bar_y, sx + seg_w, bar_y + 5], radius=3, fill=col)

    # 2. Bottom Footer
    footer_y = HEIGHT - 95
    f_font = get_font(24, bold=True)
    draw.text((80, footer_y), FOUNDER_NAME, fill=(203, 213, 225), font=f_font)

    web_text = BRAND_WEBSITE
    w_font = get_font(24, bold=True)
    w_w = draw.textbbox((0, 0), web_text, font=w_font)[2]
    draw.text((WIDTH - 80 - w_w, footer_y), web_text, fill=(56, 189, 248), font=w_font)

# ---------------------------------------------------------------------------
# SLIDE BUILDERS (1080x1350 Minimalist High-Contrast Carousel)
# ---------------------------------------------------------------------------

def render_cover_slide(title_text):
    """Renders Slide 1 (Cover Hook) with giant white typography and 5 arrows."""
    canvas = create_base_canvas()
    draw = ImageDraw.Draw(canvas)

    draw_header(draw, guide_text="Learn in 5 Slides ➔")

    # Center Headline
    title_font = get_font(74, bold=True)
    wrapped_title = textwrap.fill(title_text, width=22)
    
    # Calculate text positioning
    bbox = draw.textbbox((0, 0), wrapped_title, font=title_font)
    th = bbox[3] - bbox[1]
    ty = 480 - (th // 3)

    draw.text((80, ty), wrapped_title, fill=(255, 255, 255), font=title_font, spacing=16)

    # 5 Emerald Directional Arrows
    arrow_y = ty + th + 60
    arrow_font = get_font(44, bold=False)
    arrow_str = "➔   ➔   ➔   ➔   ➔"
    draw.text((80, arrow_y), arrow_str, fill=(34, 197, 94), font=arrow_font)

    draw_footer_and_progress(draw, active_step=1, total_steps=5)
    return canvas.convert("RGB")

def render_step_slide(step_num, title, description, total_steps=5):
    """Renders Steps 1 to 5 with giant number, directional arrows, and punchy body."""
    canvas = create_base_canvas()
    draw = ImageDraw.Draw(canvas)

    draw_header(draw, guide_text=f"Slide 0{step_num}")

    # Top Row: Big Number on Left, Two Arrows on Right
    num_y = 380
    num_font = get_font(125, bold=True)
    draw.text((80, num_y), f"{step_num}.", fill=(255, 255, 255), font=num_font)

    arrow_font = get_font(52, bold=False)
    draw.text((WIDTH - 200, num_y + 35), "➔  ➔", fill=(34, 197, 94), font=arrow_font)

    # Core Headline (Font size 58-62)
    h_y = num_y + 150
    h_font = get_font(58, bold=True)
    wrapped_title = textwrap.fill(title, width=26)
    draw.text((80, h_y), wrapped_title, fill=(255, 255, 255), font=h_font, spacing=12)

    t_bbox = draw.textbbox((0, 0), wrapped_title, font=h_font)
    t_height = t_bbox[3] - t_bbox[1]

    # Subtitle / Technical Explanation
    desc_y = h_y + t_height + 34
    desc_font = get_font(30, bold=False)
    wrapped_desc = textwrap.fill(description, width=44)
    draw.text((80, desc_y), wrapped_desc, fill=(148, 163, 184), font=desc_font, spacing=10)

    draw_footer_and_progress(draw, active_step=step_num, total_steps=total_steps)
    return canvas.convert("RGB")

def render_outro_slide(outro_title="Save this Blueprint", outro_sub=None):
    """Renders Slide 7 (Outro / Call-to-Action) with Bookmark icon and Emerald CTA."""
    canvas = create_base_canvas()
    draw = ImageDraw.Draw(canvas)

    draw_header(draw, guide_text="Action Step ➔")

    # Bookmark Icon Box
    bw, bh = 100, 100
    bx = (WIDTH - bw) // 2
    by = 380
    draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=26, fill=(255, 255, 255, 20), outline=(255, 255, 255, 45), width=2)
    
    # White Ribbon Bookmark Shape
    rx = bx + 34
    ry = by + 26
    rw, rh = 32, 48
    draw.polygon([
        (rx, ry),
        (rx + rw, ry),
        (rx + rw, ry + rh),
        (rx + (rw // 2), ry + rh - 12),
        (rx, ry + rh)
    ], fill=(255, 255, 255))

    # Headline
    o_font = get_font(72, bold=True)
    o_bbox = draw.textbbox((0, 0), outro_title, font=o_font)
    o_w = o_bbox[2] - o_bbox[0]
    draw.text(((WIDTH - o_w) // 2, by + bh + 45), outro_title, fill=(255, 255, 255), font=o_font)

    # Subhead
    if not outro_sub:
        outro_sub = "Reconcile your conversions 1:1 and eliminate tracking blindspots with Server-Side GTM."
    sub_font = get_font(28, bold=False)
    wrapped_sub = textwrap.fill(outro_sub, width=42)
    s_bbox = draw.textbbox((0, 0), wrapped_sub, font=sub_font)
    s_w = s_bbox[2] - s_bbox[0]
    draw.text(((WIDTH - s_w) // 2, by + bh + 145), wrapped_sub, fill=(148, 163, 184), font=sub_font, spacing=8, align="center")

    # Emerald CTA Button
    btn_w = 340
    btn_h = 72
    btn_x = (WIDTH - btn_w) // 2
    btn_y = by + bh + 260
    draw.rounded_rectangle([btn_x, btn_y, btn_x + btn_w, btn_y + btn_h], radius=36, fill=(34, 197, 94))
    
    btn_font = get_font(28, bold=True)
    btn_text = "Book Free Audit ➔"
    bw_box = draw.textbbox((0, 0), btn_text, font=btn_font)
    btn_tw = bw_box[2] - bw_box[0]
    draw.text((btn_x + (btn_w - btn_tw) // 2, btn_y + 20), btn_text, fill=(6, 9, 19), font=btn_font)

    # WhatsApp Direct Cue
    wa_font = get_font(24, bold=True)
    wa_text = f"💬 WhatsApp: {BRAND_PHONE}"
    wa_w = draw.textbbox((0, 0), wa_text, font=wa_font)[2]
    draw.text(((WIDTH - wa_w) // 2, btn_y + btn_h + 30), wa_text, fill=(56, 189, 248), font=wa_font)

    draw_footer_and_progress(draw, active_step=5, total_steps=5, all_active=True)
    return canvas.convert("RGB")

# ---------------------------------------------------------------------------
# PIPELINE GENERATORS
# ---------------------------------------------------------------------------

def build_shopify_ga4_carousel(output_dir="carousel_output"):
    """
    Builds the flagship Day 1 7-slide carousel:
    '5 Reasons Your Shopify & GA4 Sales Never Match'
    """
    os.makedirs(output_dir, exist_ok=True)
    slides = []

    # Slide 1: Cover
    s1 = render_cover_slide("5 Reasons Your Shopify & GA4 Sales Never Match")
    slides.append(s1)

    # Slide 2: Step 1
    s2 = render_step_slide(
        step_num=1,
        title="Thank-You Page Refreshes Trigger Duplicate Orders",
        description="Browser pixels fire every time a customer re-opens their order status page or tab, creating phantom purchases and artificially inflating reported ROAS."
    )
    slides.append(s2)

    # Slide 3: Step 2
    s3 = render_step_slide(
        step_num=2,
        title="Offsite Payment Gateways Skip Confirmation Page",
        description="PayPal, Klarna, and Apple Pay redirects often finalize transactions without returning customers to your thank-you page, losing 15-25% of purchase events."
    )
    slides.append(s3)

    # Slide 4: Step 3
    s4 = render_step_slide(
        step_num=3,
        title="Ad-Blockers & Brave Terminate Client Scripts",
        description="30%+ of buyers use privacy extensions that block google-analytics.com and connect.facebook.net before tracking scripts can even execute."
    )
    slides.append(s4)

    # Slide 5: Step 4
    s5 = render_step_slide(
        step_num=4,
        title="Server-Side GTM Moves Tracking to First-Party Cloud",
        description="Tracking events route securely through data.yourbrand.com, converting third-party requests into trusted first-party data immune to browser shields."
    )
    slides.append(s5)

    # Slide 6: Step 5
    s6 = render_step_slide(
        step_num=5,
        title="Unique Event ID Handshake Deduplicates 1:1",
        description="Every order is locked with a unique identifier so browser and server signals merge seamlessly, guaranteeing your analytics match bank deposits 1:1."
    )
    slides.append(s6)

    # Slide 7: Outro
    s7 = render_outro_slide(
        outro_title="Save this Blueprint",
        outro_sub="Reconcile your conversions 1:1 and eliminate tracking blindspots with Server-Side GTM."
    )
    slides.append(s7)

    # Save images
    image_paths = []
    for idx, slide in enumerate(slides):
        p = os.path.join(output_dir, f"slide_{idx + 1}.png")
        slide.save(p, "PNG", quality=98)
        image_paths.append(p)
        print(f"[Carousel Engine] Generated Slide {idx + 1}: {p}")

    # Compile PDF
    pdf_path = os.path.join(output_dir, "shopify_ga4_reconciliation.pdf")
    slides[0].save(
        pdf_path,
        "PDF",
        resolution=300.0,
        quality=100,
        save_all=True,
        append_images=slides[1:]
    )
    print(f"[Carousel Engine] Compiled 300 DPI PDF Carousel: {pdf_path}")
    return image_paths, pdf_path

def build_daily_carousel(day_cfg=None, output_dir="carousel_output"):
    """
    Builds a complete 7-slide Viral Emerald Carousel (1080x1350) for any day in the calendar.
    Strictly aligns with the minimalist 5-step framework learned from the high-converting swipeable guide.
    """
    os.makedirs(output_dir, exist_ok=True)
    if not day_cfg or day_cfg.get("day", 1) == 1:
        return build_shopify_ga4_carousel(output_dir)

    day_num = day_cfg.get("day", 2)
    bullets = day_cfg.get("bullet_points", [
        "First-Party Data Infrastructure",
        "Ad-Blocker & iOS Privacy Bypass",
        "1:1 Order Deduplication Handshake",
        "Higher ROAS & Lower CPA"
    ])

    # Slide 1: Cover
    cover_title = f"5 Ways {day_cfg.get('graphic_title_line1', 'Safari ITP')} & How to Fix It"
    if len(cover_title) > 55:
        cover_title = f"5 Ways to Fix {day_cfg.get('title', 'Server-Side Tracking')}"
    
    slides = []
    slides.append(render_cover_slide(cover_title))

    # Step 1
    s1_title = bullets[0] if len(bullets) > 0 else "Extend Cookie Lifetime to 1 Year"
    s1_desc = day_cfg.get("core_concept", "Restore first-party tracking persistence across all browser sessions.")
    slides.append(render_step_slide(1, s1_title, s1_desc))

    # Step 2
    s2_title = bullets[1] if len(bullets) > 1 else "First-Party DNS Subdomain Routing"
    s2_desc = "Route all telemetry through your own domain (data.yourbrand.com) to bypass ad blockers and third-party restrictions."
    slides.append(render_step_slide(2, s2_title, s2_desc))

    # Step 3
    s3_title = bullets[2] if len(bullets) > 2 else "Accurate 30-Day Multi-Touch Attribution"
    s3_desc = "Stop losing high-value buyers who take more than 7 days to convert. Capture every touchpoint cleanly."
    slides.append(render_step_slide(3, s3_title, s3_desc))

    # Step 4
    s4_title = bullets[3] if len(bullets) > 3 else "Server-Side Event Deduplication"
    s4_desc = "Feed Meta CAPI and Google Ads uncorrupted conversion signals with high Event Match Quality (8.5+)."
    slides.append(render_step_slide(4, s4_title, s4_desc))

    # Step 5
    s5_title = "1:1 Revenue Reconciliation"
    s5_desc = "Your ad platforms optimize for actual paying customers, lowering CPA and unlocking profitable scale."
    slides.append(render_step_slide(5, s5_title, s5_desc))

    # Slide 7: Outro
    slides.append(render_outro_slide(
        outro_title="Save this Blueprint",
        outro_sub=day_cfg.get("graphic_subtitle", "Reconcile your conversions 1:1 with Server-Side GTM.")
    ))

    # Save images in 1080x1350
    image_paths = []
    for idx, slide in enumerate(slides):
        p = os.path.join(output_dir, f"slide_{idx + 1}.png")
        slide.save(p, "PNG", quality=98)
        image_paths.append(p)
        print(f"[Carousel Engine] Generated Slide {idx + 1}: {p}")

    # Compile PDF
    pdf_path = os.path.join(output_dir, f"tracking_carousel_day_{day_num}.pdf")
    slides[0].save(
        pdf_path,
        "PDF",
        resolution=300.0,
        quality=100,
        save_all=True,
        append_images=slides[1:]
    )
    print(f"[Carousel Engine] Compiled 300 DPI LinkedIn PDF Carousel: {pdf_path}")
    return image_paths, pdf_path

if __name__ == "__main__":
    imgs, pdf = build_shopify_ga4_carousel()
    print(f"Total Slides: {len(imgs)}")
    print(f"PDF Carousel: {pdf}")
