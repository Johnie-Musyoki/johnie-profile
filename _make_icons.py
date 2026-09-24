"""Generate the Open Graph share image, favicon and touch icon.

The social card is what shows up when the profile link is pasted into
LinkedIn, WhatsApp, Slack or X, so it is built from the site's own palette
rather than being a screenshot of the page.
"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "img")

# Palette lifted from assets/css/main.css
BG = (29, 26, 58)
PANEL = (37, 33, 74)
DEEP = (22, 20, 46)
PURPLE = (91, 75, 214)
LILAC = (123, 97, 255)
PINK = (252, 92, 125)
TEXT = (245, 245, 250)
MUTED = (168, 164, 196)

FONT_BOLD = r"C:\Windows\Fonts\arialbd.ttf"
FONT_REG = r"C:\Windows\Fonts\arial.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def gradient(size, top, bottom, diagonal=False):
    """Linear gradient; `diagonal` runs corner to corner."""
    w, h = size
    base = Image.new("RGB", (w, h))
    d = ImageDraw.Draw(base)
    if diagonal:
        steps = w + h
        for i in range(steps):
            t = i / (steps - 1)
            c = tuple(int(top[j] + (bottom[j] - top[j]) * t) for j in range(3))
            d.line([(i, 0), (0, i)], fill=c, width=2)
    else:
        for y in range(h):
            t = y / max(h - 1, 1)
            c = tuple(int(top[j] + (bottom[j] - top[j]) * t) for j in range(3))
            d.line([(0, y), (w, y)], fill=c)
    return base


def glow(img, center, radius, color, strength=0.55):
    """Soft radial light, the same spotlight motif as the hero."""
    layer = Image.new("RGB", img.size, (0, 0, 0))
    mask = Image.new("L", img.size, 0)
    d = ImageDraw.Draw(mask)
    d.ellipse([center[0] - radius, center[1] - radius,
               center[0] + radius, center[1] + radius], fill=int(255 * strength))
    mask = mask.filter(ImageFilter.GaussianBlur(radius * 0.45))
    layer.paste(color, (0, 0), mask)
    return _screen(img, layer)


def _screen(a, b):
    """Screen blend via Pillow's ImageChop, so numpy is not required."""
    inv_a = ImageChops.invert(a)
    inv_b = ImageChops.invert(b)
    # screen(a,b) = 255 - (255-a)*(255-b)/255
    return ImageChops.invert(ImageChops.multiply(inv_a, inv_b))


def build_og():
    W, H = 1200, 630
    img = gradient((W, H), DEEP, BG, diagonal=True)
    img = glow(img, (980, 120), 460, PURPLE, 0.60)
    img = glow(img, (150, 560), 380, PINK, 0.26)

    d = ImageDraw.Draw(img)

    # Accent bar down the left edge.
    d.rectangle([0, 0, 12, H], fill=LILAC)

    # Portrait, cropped to a circle and rimmed.
    photo = Image.open(os.path.join(OUT, "john.jpg")).convert("RGB")
    side = 300
    # Scale to cover a square, biased upward so the face stays in frame.
    scale = max(side / photo.width, side / photo.height)
    photo = photo.resize((int(photo.width * scale), int(photo.height * scale)), Image.LANCZOS)
    left = (photo.width - side) // 2
    top = int((photo.height - side) * 0.18)
    photo = photo.crop((left, top, left + side, top + side))

    mask = Image.new("L", (side, side), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, side - 1, side - 1], fill=255)
    cx, cy = W - side - 96, (H - side) // 2 - 18

    # Soft halo behind the portrait.
    halo = Image.new("RGB", (W, H), (0, 0, 0))
    hmask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(hmask).ellipse([cx - 34, cy - 34, cx + side + 34, cy + side + 34], fill=120)
    hmask = hmask.filter(ImageFilter.GaussianBlur(40))
    halo.paste(LILAC, (0, 0), hmask)
    img = _screen(img, halo)
    d = ImageDraw.Draw(img)

    img.paste(photo, (cx, cy), mask)
    d.ellipse([cx - 5, cy - 5, cx + side + 5, cy + side + 5], outline=LILAC, width=5)

    # Text block.
    x = 88
    d.text((x, 150), "JOHN MUSYOKI", font=font(FONT_BOLD, 74), fill=TEXT)
    d.text((x, 246), "Cyber Security Consultant", font=font(FONT_BOLD, 40), fill=LILAC)

    d.line([x, 318, x + 120, 318], fill=PINK, width=6)

    body = [
        "Vulnerability assessment  ·  Penetration testing",
        "IT audit  ·  Incident response advisory",
        "Nairobi, Kenya",
    ]
    y = 352
    for line in body:
        d.text((x, y), line, font=font(FONT_REG, 29), fill=MUTED)
        y += 46

    d.text((x, H - 78), "johnie-musyoki.github.io/johnie-profile",
           font=font(FONT_REG, 24), fill=(128, 124, 158))

    path = os.path.join(OUT, "og.png")
    img.save(path, "PNG", optimize=True)
    return path


def build_favicon():
    """Shield mark on the brand gradient, square, for the browser tab."""
    S = 512
    img = gradient((S, S), LILAC, PURPLE, diagonal=True)
    d = ImageDraw.Draw(img)

    # Shield outline.
    pad = 118
    top, bot = 96, S - 108
    pts = [
        (S // 2, top),
        (S - pad, top + 62),
        (S - pad, S // 2 + 18),
        (S // 2, bot),
        (pad, S // 2 + 18),
        (pad, top + 62),
    ]
    d.polygon(pts, fill=(255, 255, 255, 0))
    # White keyhole: a circle over a tapered stem.
    d.ellipse([S // 2 - 52, S // 2 - 88, S // 2 + 52, S // 2 + 16], fill=(255, 255, 255))
    d.polygon([
        (S // 2 - 40, S // 2 - 34),
        (S // 2 + 40, S // 2 - 34),
        (S // 2 + 18, S // 2 + 104),
        (S // 2 - 18, S // 2 + 104),
    ], fill=(255, 255, 255))

    path = os.path.join(OUT, "favicon.svg")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" role="img" aria-label="John Musyoki">
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#{LILAC[0]:02x}{LILAC[1]:02x}{LILAC[2]:02x}"/>
    <stop offset="1" stop-color="#{PURPLE[0]:02x}{PURPLE[1]:02x}{PURPLE[2]:02x}"/>
  </linearGradient></defs>
  <rect width="512" height="512" fill="url(#g)"/>
  <path d="M256 96 L394 158 L394 274 Q394 372 256 404 Q118 372 118 274 L118 158 Z"
        fill="#ffffff" opacity="0.16"/>
  <path d="M256 96 L394 158 L394 274 Q394 372 256 404 Q118 372 118 274 L118 158 Z"
        fill="none" stroke="#ffffff" stroke-width="18" stroke-linejoin="round"/>
  <circle cx="256" cy="222" r="54" fill="#ffffff"/>
  <path d="M216 268 L296 268 L274 342 L238 342 Z" fill="#ffffff"/>
</svg>'''
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(svg)

    # Raster copies for the manifest and iOS.
    png = img.convert("RGBA")
    png.resize((180, 180), Image.LANCZOS).save(
        os.path.join(OUT, "apple-touch-icon.png"), "PNG", optimize=True)
    png.resize((32, 32), Image.LANCZOS).save(
        os.path.join(OUT, "favicon-32.png"), "PNG", optimize=True)
    return path


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("og:", build_og())
    print("favicon:", build_favicon())
