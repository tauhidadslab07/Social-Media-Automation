import os
import random
import textwrap
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from dotenv import load_dotenv

load_dotenv()

BRAND_NAME = os.getenv("BRAND_NAME", "Tauhid Ads Lab")
BRAND_PHONE = os.getenv("BRAND_PHONE", "+8801624608468")
BRAND_WEBSITE = os.getenv("BRAND_WEBSITE", "tauhidadslab.com").replace("http://", "").replace("https://", "").strip("/")
BRAND_CALENDLY = os.getenv("BRAND_CALENDLY", "calendly.com/tauhidadslab/30min").replace("https://", "").replace("http://", "")

# ---------------------------------------------------------------------------
# 2026 APEX TECH & DARK LUXURY PALETTES (Scroll-Stopping High Contrast)
# ---------------------------------------------------------------------------
THEMES = [
    {
        "name": "Obsidian Cyber Cyan",
        "bg_base": (7, 10, 19),         # Deep Obsidian
        "flare_primary": (0, 220, 255),  # Electric Cyan
        "flare_secondary": (37, 99, 235), # Royal Blue
        "accent": (0, 240, 255),        # Neon Cyan
        "accent_warm": (245, 158, 11),   # Golden Amber
        "card_bg": (15, 23, 42, 225),    # Frosted Slate
        "card_border": (0, 210, 255, 90),
        "text_white": (255, 255, 255),
        "text_muted": (148, 163, 184),
        "success_green": (16, 185, 129),
        "alert_red": (239, 68, 68)
    },
    {
        "name": "Midnight Emerald & Gold",
        "bg_base": (6, 13, 20),         # Dark Teal Obsidian
        "flare_primary": (16, 185, 129), # Emerald Green
        "flare_secondary": (6, 182, 212),# Cyan
        "accent": (52, 211, 153),       # Neon Emerald
        "accent_warm": (251, 191, 36),   # Sun Gold
        "card_bg": (12, 28, 38, 230),
        "card_border": (16, 185, 129, 90),
        "text_white": (255, 255, 255),
        "text_muted": (156, 163, 175),
        "success_green": (16, 185, 129),
        "alert_red": (244, 63, 94)
    },
    {
        "name": "Deep Royal & Sunset Amber",
        "bg_base": (8, 9, 21),          # Midnight Indigo
        "flare_primary": (99, 102, 241), # Electric Indigo
        "flare_secondary": (245, 158, 11),# Amber
        "accent": (129, 140, 248),      # Periwinkle
        "accent_warm": (245, 158, 11),   # Golden Amber
        "card_bg": (17, 24, 39, 230),
        "card_border": (129, 140, 248, 90),
        "text_white": (255, 255, 255),
        "text_muted": (156, 163, 175),
        "success_green": (16, 185, 129),
        "alert_red": (239, 68, 68)
    }
]

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

def create_ambient_background(width, height, theme):
    """Renders a multi-layer dark mode canvas with glowing radial light flares."""
    base = Image.new("RGBA", (width, height), theme["bg_base"] + (255,))
    glow = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    # 1. Top-Right Neon Flare
    fp = theme["flare_primary"]
    for r in range(480, 0, -20):
        alpha = int(45 * (1 - (r / 480)))
        glow_draw.ellipse([width - 250 - r, -100 - r, width - 250 + r, -100 + r], fill=(fp[0], fp[1], fp[2], alpha))

    # 2. Bottom-Left Ambient Flare
    fs = theme["flare_secondary"]
    for r in range(420, 0, -25):
        alpha = int(35 * (1 - (r / 420)))
        glow_draw.ellipse([-80 - r, height - 150 - r, -80 + r, height - 150 + r], fill=(fs[0], fs[1], fs[2], alpha))

    # 3. Subtle Warm Accent Center Flare
    aw = theme["accent_warm"]
    for r in range(260, 0, -20):
        alpha = int(22 * (1 - (r / 260)))
        glow_draw.ellipse([540 - r, 380 - r, 540 + r, 380 + r], fill=(aw[0], aw[1], aw[2], alpha))

    composite = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(composite)

    # Subtle tech dot grid for depth
    for x in range(60, width - 40, 60):
        for y in range(80, height - 60, 60):
            draw.point((x, y), fill=(255, 255, 255, 22))

    return composite

def render_master_banner(post_data, output_path, is_linkedin=False):
    """
    Renders an ultra-modern, attention-grabbing 1080x1080 social media creative.
    Features:
    - Dark mode luxury background with ambient neon flares
    - Floating brand pill with green live dot
    - Giant scroll-stopping typographic hook
    - Old Way ❌ vs New Way ✅ visual comparison card
    - Live metric trust strip (ROAS, Inbound Calls, 5.0 Rating)
    - High-conversion bottom action dock (WhatsApp, Website, Free Audit)
    """
    WIDTH, HEIGHT = 1080, 1080
    theme = THEMES[1] if is_linkedin else random.choice(THEMES)
    
    img = create_ambient_background(WIDTH, HEIGHT, theme)
    draw = ImageDraw.Draw(img)

    # =========================================================================
    # 1. TOP BRAND HEADER (Y: 55)
    # =========================================================================
    # Left: Brand Badge Pill
    badge_x, badge_y = 60, 55
    badge_w, badge_h = 320, 44
    draw.rounded_rectangle(
        [badge_x, badge_y, badge_x + badge_w, badge_y + badge_h],
        radius=22,
        fill=(15, 23, 42, 220),
        outline=theme["accent"],
        width=1
    )
    # Pulsing Live Green Dot
    draw.ellipse([badge_x + 16, badge_y + 16, badge_x + 28, badge_y + 28], fill=theme["success_green"])
    draw.text((badge_x + 38, badge_y + 11), BRAND_NAME.upper(), fill=theme["text_white"], font=get_font(18, bold=True))

    # Right: Website Pill
    web_text = f"🌐 {BRAND_WEBSITE}"
    w_font = get_font(18, bold=True)
    w_bbox = draw.textbbox((0, 0), web_text, font=w_font)
    w_w = (w_bbox[2] - w_bbox[0]) + 36
    draw.rounded_rectangle(
        [WIDTH - 60 - w_w, badge_y, WIDTH - 60, badge_y + badge_h],
        radius=22,
        fill=(15, 23, 42, 200),
        outline=(71, 85, 105, 160),
        width=1
    )
    draw.text((WIDTH - 60 - w_w + 18, badge_y + 11), web_text, fill=theme["accent"], font=w_font)

    # =========================================================================
    # 2. TOPIC CATEGORY CAPSULE (Y: 130)
    # =========================================================================
    category = post_data.get("category", "GOOGLE ADS SPECIALIST").upper()
    cat_text = f"● {category}"
    cat_font = get_font(15, bold=True)
    cat_bbox = draw.textbbox((0, 0), cat_text, font=cat_font)
    cat_w = (cat_bbox[2] - cat_bbox[0]) + 30
    draw.rounded_rectangle(
        [60, 130, 60 + cat_w, 130 + 34],
        radius=17,
        fill=(30, 41, 59, 210),
        outline=theme["accent_warm"],
        width=1
    )
    draw.text((75, 137), cat_text, fill=theme["accent_warm"], font=cat_font)

    # =========================================================================
    # 3. GIANT SCROLL-STOPPING HEADLINE (Y: 185)
    # =========================================================================
    h1 = post_data.get("graphic_title_line1", "STOP BOOSTING POSTS").upper().strip(".")
    h2 = post_data.get("graphic_title_line2", "CAPTURE ACTIVE BUYERS").upper().strip(".")

    # Line 1: Bold White
    h1_font = get_font(46, bold=True)
    draw.text((60, 185), h1, fill=theme["text_white"], font=h1_font)

    # Line 2: Glowing Neon Accent (Large, Punchy)
    h2_font = get_font(56, bold=True)
    wrapped_h2 = textwrap.fill(h2, width=22)
    draw.text((60, 245), wrapped_h2, fill=theme["accent"], font=h2_font, spacing=10)

    # Calculate where Line 2 ends
    h2_bbox = draw.textbbox((60, 245), wrapped_h2, font=h2_font, spacing=10)
    sub_y = h2_bbox[3] + 16

    # Subtitle
    sub = post_data.get("graphic_subtitle", "Target ready-to-buy customers searching on Google right now.")
    sub_wrapped = textwrap.fill(sub, width=54)
    draw.text((60, sub_y), sub_wrapped, fill=theme["text_muted"], font=get_font(21, bold=False), spacing=6)

    sub_bbox = draw.textbbox((60, sub_y), sub_wrapped, font=get_font(21, bold=False), spacing=6)
    content_y = sub_bbox[3] + 28

    # =========================================================================
    # 4. HERO CENTERPIECE: 4-POINT APEX GRID OR COMPARISON CARD (Y: content_y)
    # =========================================================================
    bullets = post_data.get("bullet_points", [
        "Top #1 Position on Google Search",
        "High-Intent Inbound Phone Calls",
        "Negative Keywords Save 35%+ Budget",
        "Full Server-Side Tracking Setup"
    ])

    # 4-card 2x2 grid layout (clean, ultra-modern app cards)
    card_w = 460
    card_h = 100
    gap_x = 40
    gap_y = 20

    coords = [
        (60, content_y),
        (60 + card_w + gap_x, content_y),
        (60, content_y + card_h + gap_y),
        (60 + card_w + gap_x, content_y + card_h + gap_y)
    ]

    bullet_font = get_font(19, bold=True)
    for i, (cx, cy) in enumerate(coords[:4]):
        b_text = bullets[i] if i < len(bullets) else "Verified Growth Blueprint"
        # Translucent glass card
        draw.rounded_rectangle(
            [cx, cy, cx + card_w, cy + card_h],
            radius=16,
            fill=theme["card_bg"],
            outline=(51, 65, 85, 180),
            width=1
        )
        # Glowing checkmark circle
        icon_bg = theme["success_green"] if i % 2 == 0 else theme["accent"]
        draw.ellipse([cx + 18, cy + 22, cx + 54, cy + 58], fill=icon_bg)
        draw.text((cx + 28, cy + 24), "✔", fill=(7, 10, 19), font=get_font(22, bold=True))

        # Bullet Text wrapped nicely
        wrapped_b = textwrap.fill(b_text, width=28)
        draw.text((cx + 68, cy + 26), wrapped_b, fill=theme["text_white"], font=bullet_font, spacing=4)

    grid_bottom = content_y + (card_h * 2) + gap_y

    # =========================================================================
    # 5. LIVE METRIC TRUST STRIP (Y: ~770)
    # =========================================================================
    stat_y = grid_bottom + 25
    stat_h = 70
    draw.rounded_rectangle(
        [60, stat_y, WIDTH - 60, stat_y + stat_h],
        radius=16,
        fill=(15, 23, 42, 230),
        outline=theme["accent"],
        width=1
    )

    # Stat 1: 5.0 Rating
    draw.text((85, stat_y + 12), "⭐ 5.0 RATED", fill=theme["accent_warm"], font=get_font(17, bold=True))
    draw.text((85, stat_y + 38), "Top Agency Trust", fill=theme["text_muted"], font=get_font(13, bold=False))

    draw.line([(340, stat_y + 15), (340, stat_y + 55)], fill=(51, 65, 85, 220), width=1)

    # Stat 2: High-Intent Calls
    draw.text((375, stat_y + 12), "📞 INBOUND CALLS", fill=theme["accent"], font=get_font(17, bold=True))
    draw.text((375, stat_y + 38), "Ready-To-Buy Clients", fill=theme["text_muted"], font=get_font(13, bold=False))

    draw.line([(680, stat_y + 15), (680, stat_y + 55)], fill=(51, 65, 85, 220), width=1)

    # Stat 3: 0% Wasted Spend
    draw.text((715, stat_y + 12), "⚡ ZERO WASTED SPEND", fill=theme["success_green"], font=get_font(17, bold=True))
    draw.text((715, stat_y + 38), "Negative Keywords + GTM", fill=theme["text_muted"], font=get_font(13, bold=False))

    # =========================================================================
    # 6. HIGH-CONVERSION BOTTOM ACTION DOCK (Y: ~880)
    # =========================================================================
    dock_y = stat_y + stat_h + 24
    dock_h = 96
    draw.rounded_rectangle(
        [60, dock_y, WIDTH - 60, dock_y + dock_h],
        radius=20,
        fill=(10, 15, 30, 240),
        outline=(71, 85, 105, 200),
        width=1
    )

    # WhatsApp Button
    wa_w = 420
    draw.rounded_rectangle(
        [80, dock_y + 20, 80 + wa_w, dock_y + dock_h - 20],
        radius=26,
        fill=(37, 211, 102), # Official WhatsApp Green
    )
    draw.text((105, dock_y + 36), f"💬 WhatsApp: {BRAND_PHONE}", fill=(10, 15, 29), font=get_font(18, bold=True))

    # Right CTA: Book Strategy Session
    cta_text = post_data.get("cta_text", "BOOK FREE AUDIT").upper()
    cta_btn_text = f"🚀 {cta_text}"
    draw.text((540, dock_y + 26), cta_btn_text, fill=theme["accent"], font=get_font(20, bold=True))
    draw.text((540, dock_y + 54), f"📅 {BRAND_CALENDLY}", fill=theme["text_muted"], font=get_font(14, bold=False))

    # Save finalized image
    final_img = img.convert("RGB")
    final_img.save(output_path, "PNG", quality=98)
    print(f"[Image Engine 2026] Generated: {output_path}")
    return output_path

def render_template_poster(post_data, output_path, is_linkedin=False):
    """
    Renders an attention-grabbing social media graphic using the curated reference poster
    templates uploaded by the user in the 'templates/' directory.
    
    1. Selects the template based on post_data['day'] (1 to 31 rotation).
    2. Resizes/crops to 1080x1080 while preserving focal composition.
    3. Replaces old agency logo with official 'Tauhid Ads Lab' badge and website pill.
    4. Overlays custom high-contrast headline, category badge, and subtitle.
    5. Replaces bottom footer with Tauhid Ads Lab WhatsApp (+8801624608468) and Calendly booking CTA.
    6. Falls back to render_master_banner if no template is found or on error.
    """
    templates_dir = os.path.join(os.path.dirname(__file__), "templates")
    template_files = []
    if os.path.exists(templates_dir):
        template_files = sorted([
            f for f in os.listdir(templates_dir)
            if f.lower().endswith(('.jpg', '.jpeg', '.png'))
        ])

    if not template_files:
        print("[Image Engine] No templates found in templates/. Falling back to master banner.")
        return render_master_banner(post_data, output_path, is_linkedin=is_linkedin)

    # Determine day number (1-based)
    day = post_data.get("day", 1)
    try:
        day_idx = (int(day) - 1) % len(template_files)
    except Exception:
        day_idx = 0

    chosen_template = os.path.join(templates_dir, template_files[day_idx])
    print(f"[Image Engine] Using Reference Template #{day_idx + 1} ({template_files[day_idx]}) for Day {day}")

    try:
        with Image.open(chosen_template) as raw_img:
            base = raw_img.convert("RGBA")
            WIDTH, HEIGHT = 2160, 2160

            # Resize preserving aspect ratio, center crop, and apply anti-aliasing sharpen
            orig_w, orig_h = base.size
            scale = max(WIDTH / orig_w, HEIGHT / orig_h)
            new_w, new_h = int(orig_w * scale), int(orig_h * scale)
            resized = base.resize((new_w, new_h), Image.Resampling.LANCZOS)

            left = (new_w - WIDTH) // 2
            top = (new_h - HEIGHT) // 2
            canvas = resized.crop((left, top, left + WIDTH, top + HEIGHT))
            # Sharpen background template to eliminate resize blurriness
            canvas = canvas.filter(ImageFilter.UnsharpMask(radius=2, percent=135, threshold=2))

            overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            draw = ImageDraw.Draw(overlay)

            # -------------------------------------------------------------
            # 1. TOP BRAND HEADER: Clean frosted glass bar covering old logo
            # -------------------------------------------------------------
            header_h = 190
            for y in range(header_h + 60):
                alpha = int(245 * (1 - (y / (header_h + 60)) * 0.4)) if y < header_h else int(150 * (1 - (y - header_h) / 60))
                draw.line([(0, y), (WIDTH, y)], fill=(8, 12, 22, alpha), width=1)

            # Tauhid Ads Lab Brand Pill (Left)
            pill_x, pill_y = 100, 48
            pill_w, pill_h = 640, 96
            draw.rounded_rectangle(
                [pill_x, pill_y, pill_x + pill_w, pill_y + pill_h],
                radius=48,
                fill=(15, 23, 42, 240),
                outline=(0, 220, 255, 180),
                width=3
            )
            # Live Green Dot
            draw.ellipse([pill_x + 32, pill_y + 32, pill_x + 64, pill_y + 64], fill=(16, 185, 129))
            draw.text((pill_x + 84, pill_y + 26), BRAND_NAME.upper(), fill=(255, 255, 255), font=get_font(38, bold=True))

            # Website Pill (Right)
            web_text = f"🌐 {BRAND_WEBSITE}"
            w_font = get_font(36, bold=True)
            w_bbox = draw.textbbox((0, 0), web_text, font=w_font)
            w_w = (w_bbox[2] - w_bbox[0]) + 72
            draw.rounded_rectangle(
                [WIDTH - 100 - w_w, pill_y, WIDTH - 100, pill_y + pill_h],
                radius=48,
                fill=(15, 23, 42, 225),
                outline=(59, 130, 246, 140),
                width=2
            )
            draw.text((WIDTH - 100 - w_w + 36, pill_y + 28), web_text, fill=(56, 189, 248), font=w_font)

            # -------------------------------------------------------------
            # 2. DYNAMIC HEADLINE OVERLAY CARD (Upper-Left)
            # -------------------------------------------------------------
            category = post_data.get("badge", post_data.get("category", "SERVER-SIDE TRACKING")).upper()
            h1 = post_data.get("graphic_title_line1", "STOP BLIND ATTRIBUTION").upper().strip(".")
            h2 = post_data.get("graphic_title_line2", "UPGRADE TO SERVER-SIDE").upper().strip(".")
            sub = post_data.get("graphic_subtitle", "Why browser pixels miss 30% of conversions and how sGTM fixes it.")

            card_x = 100
            card_y = 290
            card_w = 1240

            cat_font = get_font(28, bold=True)
            h1_font = get_font(68, bold=True)
            h2_font = get_font(84, bold=True)
            sub_font = get_font(34, bold=False)

            wrapped_h1 = textwrap.fill(h1, width=22)
            wrapped_h2 = textwrap.fill(h2, width=18)
            wrapped_sub = textwrap.fill(sub, width=42)

            cat_box = draw.textbbox((0, 0), category, font=cat_font)
            h1_box = draw.textbbox((0, 0), wrapped_h1, font=h1_font)
            h2_box = draw.textbbox((0, 0), wrapped_h2, font=h2_font)
            sub_box = draw.textbbox((0, 0), wrapped_sub, font=sub_font)

            card_h = (cat_box[3] - cat_box[1]) + (h1_box[3] - h1_box[1]) + (h2_box[3] - h2_box[1]) + (sub_box[3] - sub_box[1]) + 190

            # Card Diffused Drop Shadow
            shadow_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            s_draw = ImageDraw.Draw(shadow_layer)
            s_draw.rounded_rectangle([card_x + 8, card_y + 20, card_x + card_w - 8, card_y + card_h + 24], radius=40, fill=(0, 0, 0, 80))
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(24))
            overlay = Image.alpha_composite(shadow_layer, overlay)
            draw = ImageDraw.Draw(overlay)

            # Frosted glass card backing
            draw.rounded_rectangle(
                [card_x, card_y, card_x + card_w, card_y + card_h],
                radius=40,
                fill=(9, 14, 26, 230),
                outline=(0, 220, 255, 140),
                width=2
            )

            # Topic Badge
            badge_text = f"● {category}"
            draw.rounded_rectangle(
                [card_x + 48, card_y + 36, card_x + 48 + draw.textbbox((0,0), badge_text, font=cat_font)[2] + 40, card_y + 92],
                radius=28,
                fill=(30, 41, 59, 235),
                outline=(245, 158, 11, 200),
                width=2
            )
            draw.text((card_x + 68, card_y + 48), badge_text, fill=(251, 191, 36), font=cat_font)

            # Line 1 (White Bold)
            y_cursor = card_y + 116
            draw.text((card_x + 48, y_cursor), wrapped_h1, fill=(255, 255, 255), font=h1_font)
            y_cursor += (h1_box[3] - h1_box[1]) + 16

            # Line 2 (Neon Cyan Accent)
            draw.text((card_x + 48, y_cursor), wrapped_h2, fill=(0, 240, 255), font=h2_font)
            y_cursor += (h2_box[3] - h2_box[1]) + 20

            # Subtitle (Muted Slate)
            draw.text((card_x + 48, y_cursor), wrapped_sub, fill=(203, 213, 225), font=sub_font, spacing=8)

            # -------------------------------------------------------------
            # 3. BOTTOM CONTACT DOCK: Covers old phone, website & address
            # -------------------------------------------------------------
            dock_h = 200
            dock_y = HEIGHT - dock_h

            draw.rectangle(
                [0, dock_y, WIDTH, HEIGHT],
                fill=(7, 10, 20, 250),
                outline=(30, 41, 59, 255),
                width=2
            )

            # Left: WhatsApp Pill Button
            wa_w = 860
            draw.rounded_rectangle(
                [100, dock_y + 36, 100 + wa_w, dock_y + dock_h - 36],
                radius=52,
                fill=(37, 211, 102)
            )
            draw.text((150, dock_y + 70), f"💬 WhatsApp: {BRAND_PHONE}", fill=(10, 15, 29), font=get_font(38, bold=True))

            # Right: Strategy Session / Calendly CTA
            cta_title = f"🚀 {post_data.get('cta_text', 'CLAIM FREE TRACKING AUDIT').upper()}"
            draw.text((1040, dock_y + 48), cta_title, fill=(0, 240, 255), font=get_font(40, bold=True))
            draw.text((1040, dock_y + 104), f"📅 {BRAND_CALENDLY}", fill=(148, 163, 184), font=get_font(30, bold=False))

            # Merge and finalize at 2K Ultra-HD
            final_composite = Image.alpha_composite(canvas, overlay).convert("RGB")
            final_composite.save(output_path, "PNG", compress_level=1)
            print(f"[Image Engine] Ultra-HD 2K Composite saved: {output_path}")
            return output_path

    except Exception as e:
        print(f"[Image Engine] Error rendering template poster: {e}. Falling back to master banner.")
        return render_master_banner(post_data, output_path, is_linkedin=is_linkedin)

def render_personal_brand_graphic(post_data, output_path, is_linkedin=False):
    """
    Renders high-converting Personal Branding Feed Post Graphic matching the creator style
    requested by Md. Tauhidul Islam Bhuian (Warm minimalist beige + personal photo + bold typography + orange CTA dock).
    """
    WIDTH, HEIGHT = 1080, 1080
    portrait_path = os.path.join(os.path.dirname(__file__), "tauhid_portrait.jpg")

    if not os.path.exists(portrait_path):
        print("[Personal Brand Engine] tauhid_portrait.jpg not found, falling back to template poster.")
        return render_template_poster(post_data, output_path, is_linkedin=is_linkedin)

    # 1. Warm Minimalist Cream Background (#FFFDF8)
    base = Image.new("RGBA", (WIDTH, HEIGHT), (255, 253, 248, 255))
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    # Ambient warm golden glow behind subject
    glow_center_x, glow_center_y = WIDTH // 2, 650
    for r in range(400, 0, -20):
        alpha = int(35 * (1 - (r / 400)))
        glow_draw.ellipse(
            [glow_center_x - r, glow_center_y - r, glow_center_x + r, glow_center_y + r],
            fill=(254, 215, 170, alpha)
        )
    base = Image.alpha_composite(base, glow)
    draw = ImageDraw.Draw(base)

    # -------------------------------------------------------------
    # 2. TOP BRAND PILL (Vibrant Orange like 'Rasel Insights')
    # -------------------------------------------------------------
    brand_pill_x, brand_pill_y = 60, 48
    brand_pill_h = 50
    brand_font = get_font(19, bold=True)
    brand_text = f"✦ {BRAND_NAME.upper()}"
    bbox = draw.textbbox((0, 0), brand_text, font=brand_font)
    brand_pill_w = (bbox[2] - bbox[0]) + 44

    draw.rounded_rectangle(
        [brand_pill_x, brand_pill_y, brand_pill_x + brand_pill_w, brand_pill_y + brand_pill_h],
        radius=25,
        fill=(255, 122, 0)
    )
    draw.text((brand_pill_x + 22, brand_pill_y + 14), brand_text, fill=(255, 255, 255), font=brand_font)

    # -------------------------------------------------------------
    # 3. CATEGORY PILL (Soft Butter Yellow like 'এআই প্রম্পট')
    # -------------------------------------------------------------
    cat_y = brand_pill_y + brand_pill_h + 16
    cat_h = 38
    cat_font = get_font(14, bold=True)
    category = post_data.get("badge", post_data.get("category", "SERVER-SIDE TRACKING")).upper()
    cat_text = f"● {category}"
    c_bbox = draw.textbbox((0, 0), cat_text, font=cat_font)
    cat_w = (c_bbox[2] - c_bbox[0]) + 32

    draw.rounded_rectangle(
        [brand_pill_x, cat_y, brand_pill_x + cat_w, cat_y + cat_h],
        radius=19,
        fill=(254, 243, 199),
        outline=(245, 158, 11, 160),
        width=1
    )
    draw.text((brand_pill_x + 16, cat_y + 10), cat_text, fill=(180, 83, 9), font=cat_font)

    # -------------------------------------------------------------
    # 4. DOMINANT HEADLINE (Bold High-Contrast Swiss Black)
    # -------------------------------------------------------------
    title_y = cat_y + cat_h + 18
    h1 = post_data.get("graphic_title_line1", "").strip(".")
    h2 = post_data.get("graphic_title_line2", "").strip(".")
    full_title = post_data.get("title", f"{h1} {h2}").strip()
    
    title_font = get_font(38, bold=True)
    wrapped_title = textwrap.fill(full_title, width=28)
    draw.text((brand_pill_x, title_y), wrapped_title, fill=(17, 24, 39), font=title_font, spacing=8)

    t_box = draw.textbbox((brand_pill_x, title_y), wrapped_title, font=title_font, spacing=8)
    after_title_y = t_box[3] + 14

    # Accent Underline Bar (Warm Amber/Yellow)
    draw.rounded_rectangle(
        [brand_pill_x, after_title_y, brand_pill_x + 130, after_title_y + 8],
        radius=4,
        fill=(245, 158, 11)
    )

    # Subtitle
    sub_y = after_title_y + 16
    sub_text = post_data.get("graphic_subtitle", post_data.get("core_concept", "Reconcile your revenue 1:1 with Server-Side GTM."))
    sub_font = get_font(18, bold=False)
    wrapped_sub = textwrap.fill(sub_text, width=44)
    draw.text((brand_pill_x, sub_y), wrapped_sub, fill=(75, 85, 99), font=sub_font, spacing=6)

    # -------------------------------------------------------------
    # 5. PERSONAL PORTRAIT (Md. Tauhidul Islam Bhuian)
    # -------------------------------------------------------------
    try:
        with Image.open(portrait_path) as p_img:
            p_rgba = p_img.convert("RGBA")
            
            # Card dimensions for portrait arch / capsule
            card_w = 680
            card_h = 580
            card_x = (WIDTH - card_w) // 2
            card_y = HEIGHT - 110 - card_h + 30 # Sits right behind the bottom bar

            # Scale and crop portrait to fill card
            p_scaled = p_rgba.resize((card_w, int(card_w * (p_rgba.height / p_rgba.width))), Image.Resampling.LANCZOS)
            
            # Create rounded capsule mask with soft top corners
            mask = Image.new("L", (card_w, card_h), 0)
            m_draw = ImageDraw.Draw(mask)
            m_draw.rounded_rectangle([0, 0, card_w, card_h], radius=44, fill=255)

            # Soft drop shadow under the portrait capsule
            shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            s_draw = ImageDraw.Draw(shadow)
            s_draw.rounded_rectangle([card_x + 6, card_y + 16, card_x + card_w - 6, card_y + card_h + 18], radius=44, fill=(15, 23, 42, 35))
            shadow = shadow.filter(ImageFilter.GaussianBlur(22))
            base = Image.alpha_composite(base, shadow)

            # Composite cropped portrait
            p_crop = p_scaled.crop((0, 0, card_w, card_h))
            base.paste(p_crop, (card_x, card_y), mask)

            # Clean border outline around portrait card
            c_overlay = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
            co_draw = ImageDraw.Draw(c_overlay)
            co_draw.rounded_rectangle([card_x, card_y, card_x + card_w, card_y + card_h], radius=44, outline=(255, 255, 255, 220), width=3)
            base = Image.alpha_composite(base, c_overlay)

    except Exception as pe:
        print(f"[Personal Brand Engine] Portrait rendering error: {pe}")

    # -------------------------------------------------------------
    # 6. SIGNATURE BOTTOM ACTION DOCK (Vivid Orange CTA Pill)
    # -------------------------------------------------------------
    draw = ImageDraw.Draw(base)
    dock_x = 50
    dock_y = HEIGHT - 100
    dock_w = WIDTH - 100
    dock_h = 74

    # Diffused shadow under dock
    d_shadow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ds_draw = ImageDraw.Draw(d_shadow)
    ds_draw.rounded_rectangle([dock_x + 4, dock_y + 10, dock_x + dock_w - 4, dock_y + dock_h + 12], radius=37, fill=(255, 122, 0, 50))
    d_shadow = d_shadow.filter(ImageFilter.GaussianBlur(16))
    base = Image.alpha_composite(base, d_shadow)

    draw = ImageDraw.Draw(base)
    draw.rounded_rectangle(
        [dock_x, dock_y, dock_x + dock_w, dock_y + dock_h],
        radius=37,
        fill=(255, 122, 0)
    )

    # Dock Text: Website and WhatsApp
    dock_text = f"🌐 {BRAND_WEBSITE}   |   💬 WhatsApp: {BRAND_PHONE}"
    draw.text((dock_x + 36, dock_y + 24), dock_text, fill=(255, 255, 255), font=get_font(21, bold=True))

    # Right Icon Badge (White Circle with Orange Arrow)
    circle_size = 46
    cx = dock_x + dock_w - 60
    cy = dock_y + (dock_h - circle_size) // 2
    draw.ellipse([cx, cy, cx + circle_size, cy + circle_size], fill=(255, 255, 255))
    draw.text((cx + 14, cy + 9), "➔", fill=(255, 122, 0), font=get_font(24, bold=True))

    # 7. Final Output Save
    final_img = base.convert("RGB")
    final_img.save(output_path, "PNG", quality=98)
    print(f"[Personal Brand Engine] Successfully generated: {output_path}")
    return output_path

def create_facebook_graphic(post_data, output_path="fb_graphic.png"):
    """Creates attention-grabbing Facebook & Instagram feed graphic using Tauhid's personal brand style."""
    return render_personal_brand_graphic(post_data, output_path, is_linkedin=False)

def create_linkedin_graphic(post_data, output_path="li_graphic.png"):
    """Creates executive authority LinkedIn feed graphic using Tauhid's personal brand style."""
    return render_personal_brand_graphic(post_data, output_path, is_linkedin=True)

if __name__ == "__main__":
    sample_data = {
        "category": "GOOGLE ADS · AWARENESS",
        "graphic_title_line1": "STOP BOOSTING POSTS",
        "graphic_title_line2": "CAPTURE ACTIVE BUYERS",
        "graphic_subtitle": "Why Google Search ads beat Facebook boosting for local businesses every time.",
        "bullet_points": [
            "Top #1 Position on Google",
            "Direct Inbound Phone Calls",
            "Zero Wasted Negative Keywords",
            "100% Attribution & Tracking"
        ],
        "cta_text": "BOOK FREE ADS AUDIT"
    }
    create_facebook_graphic(sample_data, "test_fb_modern.png")
    create_linkedin_graphic(sample_data, "test_li_modern.png")
