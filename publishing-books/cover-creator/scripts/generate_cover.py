#!/usr/bin/env python3
"""
KDP Cover Generator v2 — Print-ready PDF covers from art + text.

Key improvements over v1:
- Gradient overlays instead of flat dark wash (preserves art tonal range)
- Art-aware cropping: "gravity" parameter controls which part of the image to keep
- Better text positioning with top/bottom zones instead of fixed y-coordinates
- Configurable via JSON file or inline CONFIG dict
- Outputs PNG preview + PDF at 300 DPI

Usage:
  python3 generate_cover.py                    # Uses CONFIG dict
  python3 generate_cover.py config.json        # Uses JSON config file
  python3 generate_cover.py --art path.jpg     # Override art path
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json, os, sys

# ============================================================================
# CONFIG — Edit for each book, or pass a JSON file as argv[1]
# ============================================================================

CONFIG = {
    # --- Book metadata ---
    "title": "THE CRUISE\nOF THE NONA",
    "subtitle": "",
    "author_line_1": "HILAIRE BELLOC",
    "author_line_2": "",
    "spine_title": "THE CRUISE OF THE NONA",
    "spine_author": "BELLOC",

    # --- Dimensions ---
    "trim_w": 5.5,
    "trim_h": 8.5,
    "page_count": 450,
    "paper": "cream",       # "cream" or "white"

    # --- Cover art ---
    "art_path": "",
    # Gravity: where to anchor when cropping landscape art to portrait.
    # "top" keeps sky, "center" splits evenly, "bottom" keeps foreground.
    # Value 0.0-1.0: 0.0=top, 0.5=center, 1.0=bottom
    "art_gravity": 0.3,
    # Overlay: gradient from top (dark) to middle (transparent) to bottom (dark)
    # This preserves the painting's midtones while making text zones readable.
    "overlay_top_alpha": 160,     # 0-255, darkness at very top
    "overlay_bottom_alpha": 120,  # 0-255, darkness at very bottom
    "overlay_mid_clear": 0.45,    # 0.0-1.0, vertical position where overlay is thinnest
    # Mirror art on back cover
    "mirror_art_on_back": True,
    "mirror_art_alpha": 35,

    # --- Front cover layout ---
    "front_align": "center",
    # Title zone: vertical fraction of cover where title sits (0.0=top edge, 1.0=bottom)
    "title_zone_top": 0.08,      # Start title this far from top (fraction of safe area)
    "author_zone_bottom": 0.08,  # Author this far from bottom (fraction of safe area)

    # --- Colors ---
    "bg_color": (25, 22, 20),
    "spine_color": (20, 18, 16),
    "title_color": (255, 250, 235),
    "subtitle_color": (240, 230, 210),
    "author_color": (255, 250, 235),
    "spine_title_color": (220, 200, 160),
    "spine_author_color": (240, 230, 215),
    "back_body_color": (230, 220, 205),
    "back_question_color": (210, 190, 145),
    "back_quote_color": (220, 200, 160),
    "back_attrib_color": (230, 220, 205),
    "praise_header_color": (210, 190, 145),
    "separator_color": (210, 190, 145),
    "category_color": (150, 145, 135),

    # --- Font sizes (at 300 DPI) ---
    "title_size": 130,
    "subtitle_size": 50,
    "author_size_1": 60,
    "author_size_2": 40,
    "back_body_size": 38,
    "back_question_size": 40,
    "back_quote_size": 40,
    "back_attrib_size": 30,
    "praise_header_size": 26,
    "category_size": 26,

    # --- Font families ---
    "title_font": "bodoni-bold",
    "subtitle_font": "baskerville-italic",
    "author_font": "bodoni-sc",

    # --- Back cover content ---
    "back_paragraphs": [
        "Hilaire Belloc sails his cutter Nona from Holyhead around the English coast to Shoreham. The tides and headlands set him thinking \u2014 about the Great War, the corruption of Parliament, the Irish tragedy, the trade of letters, and the strange mercy of the sea.",
    ],
    "back_question": "",
    "back_body": [
        "This is not really a book about sailing. It is Belloc at his freest: unguarded, digressive, brilliant, writing as a man thinks when he is alone on the water. The closing pages on the sea are among the finest in the language.",
        "First published in 1925. This new edition restores the text for modern readers.",
    ],
    "praise_header": "",
    "quotes": [
        ("\u201cThe Nona is the boat I love.\u201d", "\u2014 Hilaire Belloc"),
    ],
    "categories": "Sailing / Travel Writing / Essays",

    # --- Output ---
    "output_dir": "",       # Empty = same dir as script
    "output_name": "cover",
}

# ============================================================================
DPI = 300
def inches(n): return int(n * DPI)
PAPER_MULT = {"cream": 0.0025, "white": 0.002252}

# === FONTS ===
FONT_DIR = "/System/Library/Fonts/Supplemental"

def load_font(name, size):
    fonts = {
        "bodoni": (f"{FONT_DIR}/Bodoni 72.ttc", 0),
        "bodoni-bold": (f"{FONT_DIR}/Bodoni 72.ttc", 2),
        "bodoni-italic": (f"{FONT_DIR}/Bodoni 72.ttc", 1),
        "bodoni-sc": (f"{FONT_DIR}/Bodoni 72 Smallcaps Book.ttf", 0),
        "baskerville": (f"{FONT_DIR}/Baskerville.ttc", 0),
        "baskerville-semibold": (f"{FONT_DIR}/Baskerville.ttc", 2),
        "baskerville-italic": (f"{FONT_DIR}/Baskerville.ttc", 1),
        "baskerville-bold": (f"{FONT_DIR}/Baskerville.ttc", 4),
    }
    path, index = fonts.get(name, fonts["baskerville"])
    try:
        return ImageFont.truetype(path, size, index=index)
    except Exception:
        return ImageFont.truetype(path, size)

# === TEXT HELPERS ===

def _wrap_lines(draw, text, font, max_w):
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = f"{current} {word}".strip()
        if draw.textbbox((0, 0), test, font=font)[2] > max_w and current:
            lines.append(current)
            current = word
        else:
            current = test
    if current:
        lines.append(current)
    return lines

def draw_text_block(draw, text, y, font, fill, left, right, align="left", line_spacing=1.4):
    """Draw wrapped text with alignment. Returns final y position."""
    max_w = right - left
    for line in _wrap_lines(draw, text, font, max_w):
        bbox = draw.textbbox((0, 0), line, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        if align == "right":
            x = right - tw
        elif align == "center":
            x = left + (max_w - tw) // 2
        else:
            x = left
        draw.text((x, y), line, font=font, fill=fill)
        y += int(th * line_spacing)
    return y

def draw_single_line(draw, text, y, font, fill, left, right, align="left"):
    """Draw single line with alignment. Returns text height."""
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    if align == "right":
        x = right - tw
    elif align == "center":
        x = left + (right - left - tw) // 2
    else:
        x = left
    draw.text((x, y), text, font=font, fill=fill)
    return th

def auto_scale_font(draw, text, font_name, max_size, max_height):
    for sz in range(max_size, 8, -1):
        font = load_font(font_name, sz)
        bbox = draw.textbbox((0, 0), text, font=font)
        if bbox[3] - bbox[1] <= max_height:
            return font, sz
    return load_font(font_name, 8), 8


# === ART PROCESSING ===

def crop_art_to_cover(art, target_w, target_h, gravity=0.5):
    """
    Crop art to fill target dimensions, using gravity to control
    which part of the image is preserved.

    gravity 0.0 = keep top (sky), 1.0 = keep bottom (foreground)
    """
    art_ratio = art.width / art.height
    target_ratio = target_w / target_h

    if art_ratio > target_ratio:
        # Art is wider than needed — crop sides
        new_w = int(art.height * target_ratio)
        left = (art.width - new_w) // 2  # Center horizontally
        art = art.crop((left, 0, left + new_w, art.height))
    else:
        # Art is shorter than needed — crop top/bottom using gravity
        new_h = int(art.width / target_ratio)
        max_offset = art.height - new_h
        top = int(max_offset * gravity)
        art = art.crop((0, top, art.width, top + new_h))

    return art.resize((target_w, target_h), Image.LANCZOS)


def apply_gradient_overlay(art, top_alpha, bottom_alpha, mid_clear=0.45):
    """
    Apply a gradient overlay that darkens top and bottom while preserving
    the painting's midtones. This makes text readable at edges without
    killing the art.

    mid_clear: vertical position (0-1) where the overlay is most transparent
    """
    overlay = Image.new("RGBA", art.size, (0, 0, 0, 0))
    draw_ov = ImageDraw.Draw(overlay)

    h = art.height
    mid_y = int(h * mid_clear)

    for y in range(h):
        if y < mid_y:
            # Top zone: dark → clear
            t = y / mid_y
            # Ease-out curve for smoother transition
            t = t * t
            alpha = int(top_alpha * (1 - t))
        else:
            # Bottom zone: clear → dark
            t = (y - mid_y) / (h - mid_y)
            # Ease-in curve
            t = t * t
            alpha = int(bottom_alpha * t)
        draw_ov.line([(0, y), (art.size[0], y)], fill=(0, 0, 0, alpha))

    art_rgba = art.convert("RGBA")
    composited = Image.alpha_composite(art_rgba, overlay)
    return composited.convert("RGB")


# === BUILD COVER ===

def build_cover(cfg):
    BLEED = inches(0.125)
    SAFETY = inches(0.25)
    TRIM_W = inches(cfg["trim_w"])
    TRIM_H = inches(cfg["trim_h"])
    spine_inches = cfg["page_count"] * PAPER_MULT[cfg["paper"]]
    SPINE_W = inches(spine_inches)

    CANVAS_W = BLEED + TRIM_W + SPINE_W + TRIM_W + BLEED
    CANVAS_H = BLEED + TRIM_H + BLEED

    # Key coordinates
    BACK_RIGHT = BLEED + TRIM_W
    SPINE_LEFT = BACK_RIGHT
    SPINE_RIGHT = SPINE_LEFT + SPINE_W
    FRONT_LEFT = SPINE_RIGHT

    FRONT_SAFE_LEFT = FRONT_LEFT + SAFETY
    FRONT_SAFE_RIGHT = FRONT_LEFT + TRIM_W - SAFETY
    FRONT_SAFE_TOP = BLEED + SAFETY
    FRONT_SAFE_BOTTOM = CANVAS_H - BLEED - SAFETY

    BACK_SAFE_LEFT = BLEED + SAFETY
    BACK_SAFE_RIGHT = BACK_RIGHT - SAFETY

    print(f"Canvas: {CANVAS_W}x{CANVAS_H}px ({CANVAS_W/DPI:.3f}\"x{CANVAS_H/DPI:.3f}\")")
    print(f"Spine: {spine_inches:.3f}\" = {SPINE_W}px")

    # --- Load art ---
    art_path = cfg["art_path"]
    if not art_path or not os.path.exists(art_path):
        print(f"ERROR: Art file not found: {art_path}")
        sys.exit(1)
    art_orig = Image.open(art_path)
    print(f"Art source: {art_orig.size[0]}x{art_orig.size[1]}px")

    # --- Create canvas ---
    cover = Image.new("RGB", (CANVAS_W, CANVAS_H), cfg["bg_color"])
    draw = ImageDraw.Draw(cover)

    # --- Back cover: mirrored art ---
    if cfg.get("mirror_art_on_back"):
        back_area_w = TRIM_W + BLEED
        back_area_h = CANVAS_H
        mirror = crop_art_to_cover(art_orig.copy(), back_area_w, back_area_h, gravity=0.5)
        mirror = mirror.transpose(Image.FLIP_LEFT_RIGHT)

        # Apply heavy darkening so text is readable
        mirror = apply_gradient_overlay(mirror, 40, 40, mid_clear=0.5)

        mirror_rgba = mirror.convert("RGBA")
        alpha = cfg.get("mirror_art_alpha", 35)
        bg_layer = Image.new("RGBA", mirror.size, cfg["bg_color"] + (255,))
        mirror_rgba.putalpha(alpha)
        blended = Image.alpha_composite(bg_layer, mirror_rgba).convert("RGB")
        cover.paste(blended, (0, 0))
        draw = ImageDraw.Draw(cover)

    # --- Spine ---
    draw.rectangle([SPINE_LEFT, 0, SPINE_RIGHT, CANVAS_H], fill=cfg["spine_color"])

    # Amazon spine safety: 0.0625" on each side
    SPINE_PADDING = inches(0.0625)
    SPINE_USABLE = SPINE_W - (SPINE_PADDING * 2)

    if SPINE_USABLE > 20:
        spine_t_font, spine_t_sz = auto_scale_font(
            draw, cfg["spine_title"], "baskerville-semibold", 60, SPINE_USABLE)
        spine_a_font, spine_a_sz = auto_scale_font(
            draw, cfg["spine_author"], "baskerville", 48, SPINE_USABLE)

        st_img = Image.new("RGBA", (CANVAS_H, SPINE_W), (0, 0, 0, 0))
        st_draw = ImageDraw.Draw(st_img)

        bbox_t = st_draw.textbbox((0, 0), cfg["spine_title"], font=spine_t_font)
        tw = bbox_t[2] - bbox_t[0]
        th = bbox_t[3] - bbox_t[1]
        st_draw.text(
            ((CANVAS_H // 2 - tw) // 2 + inches(0.3), (SPINE_W - th) // 2),
            cfg["spine_title"], font=spine_t_font, fill=cfg["spine_title_color"])

        bbox_a = st_draw.textbbox((0, 0), cfg["spine_author"], font=spine_a_font)
        tw2 = bbox_a[2] - bbox_a[0]
        th2 = bbox_a[3] - bbox_a[1]
        st_draw.text(
            (CANVAS_H // 2 + (CANVAS_H // 2 - tw2) // 2 - inches(0.3), (SPINE_W - th2) // 2),
            cfg["spine_author"], font=spine_a_font, fill=cfg["spine_author_color"])

        st_img = st_img.rotate(-90, expand=True)
        cover.paste(st_img, (SPINE_LEFT, 0), st_img)
        print(f"Spine text: title {spine_t_sz}pt, author {spine_a_sz}pt")

    # --- Front cover art ---
    front_area_w = TRIM_W + BLEED
    front_area_h = CANVAS_H

    art = crop_art_to_cover(art_orig.copy(), front_area_w, front_area_h,
                            gravity=cfg.get("art_gravity", 0.3))
    art = apply_gradient_overlay(art,
                                  cfg.get("overlay_top_alpha", 160),
                                  cfg.get("overlay_bottom_alpha", 120),
                                  cfg.get("overlay_mid_clear", 0.45))

    cover.paste(art, (FRONT_LEFT, 0))
    draw = ImageDraw.Draw(cover)

    # --- Front cover text ---
    align = cfg["front_align"]
    text_pad = inches(0.2)
    text_left = FRONT_SAFE_LEFT + text_pad
    text_right = FRONT_SAFE_RIGHT - text_pad
    safe_height = FRONT_SAFE_BOTTOM - FRONT_SAFE_TOP

    # Title — positioned in upper zone
    title_y_start = FRONT_SAFE_TOP + int(safe_height * cfg.get("title_zone_top", 0.08))
    title_font = load_font(cfg["title_font"], cfg["title_size"])

    # Handle multi-line titles (split by \n)
    # title_line_scale: list of scale factors for each line (1.0 = normal)
    # e.g. [1.0, 0.7, 1.3] makes line 3 bigger than line 1
    title_lines = cfg["title"].split("\n")
    line_scales = cfg.get("title_line_scale", [1.0] * len(title_lines))
    title_leading = cfg.get("title_leading", 1.35)
    y = title_y_start
    for i, line in enumerate(title_lines):
        scale = line_scales[i] if i < len(line_scales) else 1.0
        line_font = load_font(cfg["title_font"], int(cfg["title_size"] * scale))
        h = draw_single_line(draw, line, y, line_font, cfg["title_color"],
                             text_left, text_right, align)
        y += int(h * title_leading)

    # Subtitle
    if cfg.get("subtitle"):
        sub_font = load_font(cfg["subtitle_font"], cfg["subtitle_size"])
        y += inches(0.05)
        draw_single_line(draw, cfg["subtitle"], y, sub_font,
                         cfg["subtitle_color"], text_left, text_right, align)

    # Author — positioned in lower zone
    author_y = FRONT_SAFE_BOTTOM - int(safe_height * cfg.get("author_zone_bottom", 0.08))
    author_font = load_font(cfg["author_font"], cfg["author_size_1"])
    bbox_a = draw.textbbox((0, 0), cfg["author_line_1"], font=author_font)
    author_h = bbox_a[3] - bbox_a[1]

    if cfg.get("author_line_2"):
        author_font_2 = load_font(cfg["author_font"], cfg["author_size_2"])
        bbox_a2 = draw.textbbox((0, 0), cfg["author_line_2"], font=author_font_2)
        total_h = author_h + inches(0.08) + (bbox_a2[3] - bbox_a2[1])
        ay = author_y - total_h
        draw_single_line(draw, cfg["author_line_1"], ay, author_font,
                         cfg["author_color"], text_left, text_right, align)
        draw_single_line(draw, cfg["author_line_2"], ay + author_h + inches(0.08),
                         author_font_2, cfg["author_color"], text_left, text_right, align)
    else:
        draw_single_line(draw, cfg["author_line_1"], author_y - author_h, author_font,
                         cfg["author_color"], text_left, text_right, align)

    # --- Back cover text ---
    back_pad = inches(0.5)
    ml = BACK_SAFE_LEFT + back_pad
    mr = BACK_SAFE_RIGHT - back_pad

    body_font = load_font("baskerville", cfg["back_body_size"])
    question_font = load_font("baskerville-semibold", cfg["back_question_size"])
    quote_font = load_font("baskerville-bold", cfg["back_quote_size"])
    attrib_font = load_font("baskerville", cfg["back_attrib_size"])
    praise_font = load_font("baskerville", cfg["praise_header_size"])

    y = BLEED + SAFETY + inches(0.4)

    for para in cfg.get("back_paragraphs", []):
        y = draw_text_block(draw, para, y, body_font, cfg["back_body_color"], ml, mr, "left", 1.5)
        y += inches(0.15)

    if cfg.get("back_question"):
        y = draw_text_block(draw, cfg["back_question"], y, question_font,
                            cfg["back_question_color"], ml, mr, "center", 1.5)
        y += inches(0.12)

    for para in cfg.get("back_body", []):
        y = draw_text_block(draw, para, y, body_font, cfg["back_body_color"], ml, mr, "left", 1.5)
        y += inches(0.1)

    y += inches(0.08)

    # Separator
    sep_inset = inches(0.6)
    draw.line([(ml + sep_inset, y), (mr - sep_inset, y)],
              fill=cfg["separator_color"], width=2)
    y += inches(0.15)

    # Praise header
    if cfg.get("praise_header"):
        draw_single_line(draw, cfg["praise_header"], y, praise_font,
                         cfg["praise_header_color"], ml, mr, "center")
        bbox_ph = draw.textbbox((0, 0), cfg["praise_header"], font=praise_font)
        y += int((bbox_ph[3] - bbox_ph[1]) * 1.8)

    # Quotes
    for quote_text, attribution in cfg.get("quotes", []):
        y = draw_text_block(draw, quote_text, y, quote_font,
                            cfg["back_quote_color"], ml, mr, "left", 1.4)
        if attribution:
            h = draw_single_line(draw, attribution, y, attrib_font,
                                 cfg["back_attrib_color"], ml, mr, "right")
            y += int(h * 1.8)
        y += inches(0.12)

    # Barcode zone
    barcode_right = BACK_RIGHT - SAFETY
    barcode_bottom = CANVAS_H - BLEED - SAFETY
    barcode_left = barcode_right - inches(2.0)
    barcode_top = barcode_bottom - inches(1.2)
    draw.rectangle([barcode_left, barcode_top, barcode_right, barcode_bottom],
                   fill=(255, 255, 255), outline=(200, 200, 200), width=1)

    # Categories
    if cfg.get("categories"):
        cat_font = load_font("baskerville", cfg["category_size"])
        cat_y = barcode_bottom - inches(0.3)
        draw_single_line(draw, cfg["categories"], cat_y, cat_font,
                         cfg["category_color"], ml, ml + inches(3), "left")

    # --- Save ---
    out_dir = cfg.get("output_dir") or os.path.dirname(os.path.abspath(__file__))
    name = cfg.get("output_name", "cover")
    png_path = os.path.join(out_dir, f"{name}.png")
    pdf_path = os.path.join(out_dir, f"{name}.pdf")
    cover.save(png_path, dpi=(DPI, DPI))
    cover.save(pdf_path, "PDF", resolution=DPI)
    print(f"\nSaved: {png_path}")
    print(f"Saved: {pdf_path}")
    print(f"Dimensions: {cover.width}x{cover.height}px ({cover.width/DPI:.3f}\"x{cover.height/DPI:.3f}\")")
    return png_path, pdf_path


if __name__ == "__main__":
    cfg = CONFIG.copy()

    # Load JSON config if provided
    if len(sys.argv) > 1:
        arg = sys.argv[1]
        if arg.endswith(".json") and os.path.exists(arg):
            with open(arg) as f:
                cfg.update(json.load(f))
        elif arg == "--art" and len(sys.argv) > 2:
            cfg["art_path"] = sys.argv[2]
        elif os.path.exists(arg):
            cfg["art_path"] = arg

    if not cfg["art_path"]:
        print("Usage: python3 generate_cover.py <art.jpg>")
        print("       python3 generate_cover.py config.json")
        sys.exit(1)

    build_cover(cfg)
