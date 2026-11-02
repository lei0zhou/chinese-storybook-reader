#!/usr/bin/env python3
"""
Render Chinese ink-and-watercolor (水墨设色绘本) 2x2 grid illustrations for Stories 31-36
(📜 古诗绘本 · Classical Poems), crop them into WebP bannerImg and panel imgs,
and inject Stories 31-36 into index.html.
"""

import math
import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
from crop_grid_images import extract_story_images

BRAIN_DIR = Path("/Users/leizhou/.gemini/antigravity-cli/brain/dde92688-d628-4cf6-9d61-3d1a08abad1b")
ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT_DIR / "index.html"


def make_xuan_paper(w: int, h: int, top_rgb: tuple[int, int, int], bot_rgb: tuple[int, int, int], seed: int = 42) -> Image.Image:
    """Create a warm Xuan-paper textured vertical gradient canvas."""
    rng = random.Random(seed)
    base = Image.new("RGB", (w, h))
    px = base.load()
    for y in range(h):
        t = y / max(1, h - 1)
        r = int(top_rgb[0] * (1 - t) + bot_rgb[0] * t)
        g = int(top_rgb[1] * (1 - t) + bot_rgb[1] * t)
        b = int(top_rgb[2] * (1 - t) + bot_rgb[2] * t)
        for x in range(w):
            grain = rng.randint(-5, 5)
            px[x, y] = (
                max(0, min(255, r + grain)),
                max(0, min(255, g + grain)),
                max(0, min(255, b + grain)),
            )
    return base


def draw_distant_mountains(img: Image.Image, y_base: int, color1: tuple[int, int, int, int], color2: tuple[int, int, int, int], seed: int = 1) -> None:
    """Draw layered misty ink-wash mountains."""
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    rng = random.Random(seed)
    pts1 = [(0, h), (0, y_base)]
    for x in range(0, w + 40, 40):
        dy = int(35 * math.sin(x * 0.015 + seed) + rng.randint(-12, 12))
        pts1.append((x, y_base + dy))
    pts1.append((w, h))
    d.polygon(pts1, fill=color1)

    pts2 = [(0, h), (0, y_base + 35)]
    for x in range(0, w + 40, 40):
        dy = int(28 * math.cos(x * 0.018 + seed * 2) + rng.randint(-10, 10))
        pts2.append((x, y_base + 35 + dy))
    pts2.append((w, h))
    d.polygon(pts2, fill=color2)

    blurred = overlay.filter(ImageFilter.GaussianBlur(radius=3))
    img.paste(Image.alpha_composite(img.convert("RGBA"), blurred).convert("RGB"))


def draw_goose(d: ImageDraw.ImageDraw, cx: int, cy: int, scale: float = 1.0, singing: bool = False, flip: bool = False) -> None:
    """Draw a charming Chinese picture-book white goose with red webbed feet and curved neck."""
    s = scale
    dir_x = -1 if flip else 1
    # Red webbed paddles under water
    d.polygon(
        [
            (cx - int(15 * s * dir_x), cy + int(22 * s)),
            (cx - int(32 * s * dir_x), cy + int(42 * s)),
            (cx - int(8 * s * dir_x), cy + int(44 * s)),
        ],
        fill=(225, 65, 50),
        outline=(150, 35, 25),
    )
    d.polygon(
        [
            (cx + int(5 * s * dir_x), cy + int(24 * s)),
            (cx - int(10 * s * dir_x), cy + int(46 * s)),
            (cx + int(16 * s * dir_x), cy + int(46 * s)),
        ],
        fill=(235, 80, 60),
        outline=(150, 35, 25),
    )
    # Plump white body
    bx0, by0 = cx - int(48 * s), cy - int(22 * s)
    bx1, by1 = cx + int(48 * s), cy + int(28 * s)
    d.ellipse([bx0, by0, bx1, by1], fill=(252, 252, 248), outline=(60, 70, 75), width=max(2, int(3 * s)))
    # Wing feather curve
    d.arc([cx - int(30 * s), cy - int(12 * s), cx + int(30 * s), cy + int(18 * s)], start=20, end=170, fill=(130, 145, 155), width=max(2, int(2 * s)))

    # Curved neck
    hx = cx + int((38 if not singing else 26) * s * dir_x)
    hy = cy - int((64 if not singing else 78) * s)
    neck_pts = [
        (cx + int(24 * s * dir_x), cy - int(8 * s)),
        (cx + int(42 * s * dir_x), cy - int(35 * s)),
        (hx, hy),
    ]
    d.line(neck_pts, fill=(60, 70, 75), width=max(4, int(18 * s)), joint="curve")
    d.line(neck_pts, fill=(252, 252, 248), width=max(2, int(13 * s)), joint="curve")

    # Head
    hr = int(16 * s)
    d.ellipse([hx - hr, hy - hr, hx + hr, hy + hr], fill=(252, 252, 248), outline=(60, 70, 75), width=max(2, int(2.5 * s)))
    # Orange forehead knob & beak
    d.ellipse([hx + int(6 * s * dir_x) - int(5 * s), hy - int(14 * s), hx + int(6 * s * dir_x) + int(5 * s), hy - int(4 * s)], fill=(245, 130, 35))
    if singing:
        # Open beak singing toward sky
        d.polygon(
            [
                (hx + int(8 * s * dir_x), hy - int(10 * s)),
                (hx + int(28 * s * dir_x), hy - int(28 * s)),
                (hx + int(16 * s * dir_x), hy - int(4 * s)),
            ],
            fill=(245, 135, 35),
            outline=(160, 75, 15),
        )
        d.polygon(
            [
                (hx + int(12 * s * dir_x), hy - int(4 * s)),
                (hx + int(32 * s * dir_x), hy - int(14 * s)),
                (hx + int(14 * s * dir_x), hy + int(4 * s)),
            ],
            fill=(235, 110, 30),
            outline=(160, 75, 15),
        )
        # Musical waves
        for r_w in (22, 34):
            d.arc(
                [hx + int(18 * s * dir_x) - int(r_w * s), hy - int(36 * s) - int(r_w * s), hx + int(18 * s * dir_x) + int(r_w * s), hy - int(36 * s) + int(r_w * s)],
                start=290,
                end=355,
                fill=(240, 140, 60),
                width=2,
            )
    else:
        d.polygon(
            [
                (hx + int(12 * s * dir_x), hy - int(6 * s)),
                (hx + int(34 * s * dir_x), hy),
                (hx + int(12 * s * dir_x), hy + int(7 * s)),
            ],
            fill=(245, 130, 35),
            outline=(160, 75, 15),
        )
    # Eye
    ex = hx + int(4 * s * dir_x)
    ey = hy - int(4 * s)
    d.ellipse([ex - int(3 * s), ey - int(3 * s), ex + int(3 * s), ey + int(3 * s)], fill=(30, 30, 35))


def build_grid(panels: list[Image.Image], out_path: Path) -> Path:
    pw, ph = panels[0].size
    border = 16
    gw, gh = pw * 2 + border * 3, ph * 2 + border * 3
    grid = Image.new("RGB", (gw, gh), (255, 255, 255))
    grid.paste(panels[0], (border, border))
    grid.paste(panels[1], (pw + border * 2, border))
    grid.paste(panels[2], (border, ph + border * 2))
    grid.paste(panels[3], (pw + border * 2, ph + border * 2))
    grid.save(out_path, format="JPEG", quality=92)
    return out_path


def render_story31_geese() -> Path:
    """31. 《咏鹅》· 骆宾王"""
    W, H = 480, 360
    panels = []
    for idx in range(4):
        im = make_xuan_paper(W, H, (224, 244, 238), (155, 218, 198), seed=310 + idx)
        draw_distant_mountains(im, 115, (120, 175, 165, 110), (90, 155, 142, 140), seed=31 + idx)
        d = ImageDraw.Draw(im)
        # Emerald water body
        d.rectangle([0, 170, W, H], fill=(118, 198, 176))
        # Ripples
        for ry in range(190, H - 15, 28):
            for rx in range(30, W - 40, 95):
                d.arc([rx, ry, rx + 65, ry + 14], start=0, end=180, fill=(210, 245, 235), width=2)
        # Willow branches at top
        for wx in range(20, W, 70):
            d.line([(wx, 0), (wx - 18, 65), (wx - 8, 120)], fill=(75, 135, 85), width=2)
            for ly in (25, 50, 75, 100):
                d.ellipse([wx - 22, ly, wx - 8, ly + 7], fill=(95, 165, 95))

        if idx == 0:
            # Three geese swimming in a row
            draw_goose(d, 130, 235, 0.85)
            draw_goose(d, 255, 255, 0.95)
            draw_goose(d, 375, 230, 0.8)
        elif idx == 1:
            # Close-up goose curving neck singing to blue sky
            draw_goose(d, 235, 255, 1.35, singing=True)
        elif idx == 2:
            # Snow-white feathers floating on emerald water with lotus leaves
            d.ellipse([50, 260, 150, 305], fill=(65, 155, 95), outline=(45, 115, 65), width=2)
            d.ellipse([340, 250, 445, 298], fill=(75, 165, 102), outline=(45, 115, 65), width=2)
            draw_goose(d, 240, 240, 1.25)
        else:
            # Red webbed feet paddling crystal ripples
            draw_goose(d, 185, 225, 1.15, singing=True)
            draw_goose(d, 335, 245, 1.0, flip=True)
            for r_rad in (35, 55, 75):
                d.arc([185 - r_rad, 265 - r_rad // 3, 185 + r_rad, 265 + r_rad // 3], start=0, end=360, fill=(235, 252, 248), width=2)
        panels.append(im)
    return build_grid(panels, BRAIN_DIR / "story31_grid.jpg")


def render_story32_moon() -> Path:
    """32. 《静夜思》· 李白"""
    W, H = 480, 360
    panels = []
    for idx in range(4):
        im = make_xuan_paper(W, H, (22, 34, 68), (58, 78, 122), seed=320 + idx)
        d = ImageDraw.Draw(im)
        # Twinkling stars
        rng = random.Random(3200 + idx)
        for _ in range(35):
            sx, sy = rng.randint(15, W - 15), rng.randint(15, 180)
            sr = rng.choice([1, 2, 2])
            d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=(255, 248, 210))

        # Glowing full moon
        mx, my, mr = (355 if idx != 2 else 240), (88 if idx != 2 else 82), (48 if idx != 2 else 58)
        for glow in range(mr + 28, mr, -4):
            d.ellipse([mx - glow, my - glow, mx + glow, my + glow], fill=(95, 118, 168))
        d.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(255, 250, 215), outline=(245, 232, 175), width=2)

        if idx == 0:
            # Wooden window & moonlight beam before the bed
            d.rectangle([0, 230, W, H], fill=(42, 52, 82))
            d.polygon([(mx - 30, my + 20), (mx + 30, my + 20), (320, H), (80, H)], fill=(185, 205, 238))
            # Wooden bed & child/poet in Tang robe
            d.rectangle([50, 210, 230, 310], fill=(125, 82, 52), outline=(78, 48, 28), width=3)
            d.rectangle([60, 225, 220, 265], fill=(235, 242, 250))
        elif idx == 1:
            # Frost-like silvery floor tiles sparkling under moonlight
            d.rectangle([0, 220, W, H], fill=(175, 202, 235))
            for gx in range(30, W, 65):
                d.line([(gx, 220), (gx - 25, H)], fill=(225, 240, 255), width=2)
            for _ in range(25):
                fx, fy = rng.randint(25, W - 25), rng.randint(230, H - 15)
                d.line([(fx - 6, fy), (fx + 6, fy)], fill=(255, 255, 255), width=2)
                d.line([(fx, fy - 6), (fx, fy + 6)], fill=(255, 255, 255), width=2)
        elif idx == 2:
            # Poet in Tang scholar robe raising head to gaze at the bright moon
            draw_distant_mountains(im, 215, (38, 54, 92, 180), (28, 40, 72, 220), seed=322)
            d = ImageDraw.Draw(im)
            # Figure looking up
            px, py = 240, 265
            d.polygon([(px - 36, H), (px - 22, py - 20), (px + 22, py - 20), (px + 36, H)], fill=(215, 228, 245), outline=(50, 65, 95), width=3)
            d.ellipse([px - 20, py - 58, px + 20, py - 18], fill=(252, 228, 205), outline=(50, 65, 95), width=3)
            d.ellipse([px - 12, py - 70, px + 12, py - 52], fill=(40, 45, 55))
        else:
            # Poet bowing head thinking of warm lantern-lit hometown in thought cloud
            draw_distant_mountains(im, 210, (42, 58, 96, 180), (30, 44, 78, 220), seed=323)
            d = ImageDraw.Draw(im)
            # Warm hometown cloud bubble
            d.ellipse([55, 45, 265, 175], fill=(255, 238, 198), outline=(235, 195, 125), width=3)
            # Little hometown house with red lantern inside cloud
            d.polygon([(115, 115), (160, 82), (205, 115)], fill=(185, 75, 55))
            d.rectangle([125, 115, 195, 155], fill=(245, 225, 195), outline=(120, 80, 50), width=2)
            d.ellipse([198, 115, 212, 130], fill=(235, 65, 45))
            # Poet bowing head on right
            px, py = 340, 265
            d.polygon([(px - 36, H), (px - 22, py - 20), (px + 22, py - 20), (px + 36, H)], fill=(215, 228, 245), outline=(50, 65, 95), width=3)
            d.ellipse([px - 20, py - 52, px + 20, py - 12], fill=(252, 228, 205), outline=(50, 65, 95), width=3)
        panels.append(im)
    return build_grid(panels, BRAIN_DIR / "story32_grid.jpg")


def render_story33_spring() -> Path:
    """33. 《春晓》· 孟浩然"""
    W, H = 480, 360
    panels = []
    for idx in range(4):
        if idx == 2:
            im = make_xuan_paper(W, H, (68, 96, 128), (118, 148, 168), seed=330 + idx)
        else:
            im = make_xuan_paper(W, H, (252, 236, 228), (218, 242, 215), seed=330 + idx)
        draw_distant_mountains(im, 165, (145, 195, 165, 110), (115, 175, 140, 140), seed=33 + idx)
        d = ImageDraw.Draw(im)
        rng = random.Random(3300 + idx)

        # Peach blossom branch across top
        d.line([(0, 55), (140, 75), (275, 48), (390, 70)], fill=(105, 68, 48), width=6)
        for bx, by in [(65, 62), (135, 74), (205, 60), (275, 48), (345, 64)]:
            for angle in range(0, 360, 72):
                px = bx + int(11 * math.cos(math.radians(angle)))
                py = by + int(11 * math.sin(math.radians(angle)))
                d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=(255, 175, 195), outline=(235, 125, 155))
            d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 225, 110))

        if idx == 0:
            # Cozy morning window with warm golden sunbeams
            d.ellipse([370, 35, 445, 110], fill=(255, 220, 115))
            d.rectangle([70, 140, 290, 320], fill=(245, 228, 205), outline=(135, 88, 55), width=4)
            d.ellipse([135, 195, 225, 275], fill=(255, 215, 190), outline=(95, 65, 45), width=2)
        elif idx == 1:
            # Cheerful singing birds perched on blossoming branches
            for bird_x, bird_y in [(155, 145), (315, 130)]:
                d.ellipse([bird_x - 22, bird_y - 16, bird_x + 22, bird_y + 16], fill=(255, 215, 95), outline=(85, 65, 35), width=2)
                d.ellipse([bird_x + 8, bird_y - 24, bird_x + 32, bird_y], fill=(255, 225, 115), outline=(85, 65, 35), width=2)
                d.polygon([(bird_x + 30, bird_y - 16), (bird_x + 44, bird_y - 22), (bird_x + 32, bird_y - 8)], fill=(240, 120, 40))
        elif idx == 2:
            # Gentle spring night rain & wind lines
            for _ in range(45):
                rx, ry = rng.randint(20, W - 20), rng.randint(40, H - 30)
                d.line([(rx, ry), (rx - 14, ry + 26)], fill=(205, 230, 250), width=2)
        else:
            # Green lawn covered in pink fallen peach petals
            d.rectangle([0, 225, W, H], fill=(138, 202, 128))
            for _ in range(55):
                px, py = rng.randint(20, W - 20), rng.randint(150, H - 15)
                d.ellipse([px - 7, py - 4, px + 7, py + 4], fill=(255, 172, 195), outline=(235, 130, 158))
        panels.append(im)
    return build_grid(panels, BRAIN_DIR / "story33_grid.jpg")


def render_story34_farmers() -> Path:
    """34. 《悯农》· 李绅"""
    W, H = 480, 360
    panels = []
    for idx in range(4):
        im = make_xuan_paper(W, H, (255, 240, 195), (215, 235, 165), seed=340 + idx)
        draw_distant_mountains(im, 160, (165, 195, 135, 120), (130, 175, 105, 150), seed=34 + idx)
        d = ImageDraw.Draw(im)
        # Golden midday sun
        d.ellipse([365, 28, 445, 108], fill=(255, 195, 55), outline=(245, 155, 35), width=3)
        # Terraced green/golden field
        d.rectangle([0, 205, W, H], fill=(152, 198, 96))
        for row_y in range(225, H - 10, 32):
            for gx in range(25, W - 20, 38):
                d.line([(gx, row_y + 18), (gx - 6, row_y - 10)], fill=(75, 145, 55), width=3)
                d.line([(gx, row_y + 18), (gx + 7, row_y - 8)], fill=(85, 155, 60), width=3)

        if idx == 0:
            # Farmer with bamboo hat hoeing under midday sun
            fx, fy = 225, 215
            d.polygon([(fx - 48, fy - 42), (fx, fy - 76), (fx + 48, fy - 42)], fill=(225, 185, 105), outline=(120, 85, 35), width=3)
            d.ellipse([fx - 20, fy - 45, fx + 20, fy - 5], fill=(242, 198, 162), outline=(95, 65, 45), width=2)
            d.polygon([(fx - 30, fy + 75), (fx - 20, fy - 5), (fx + 20, fy - 5), (fx + 30, fy + 75)], fill=(95, 135, 185), outline=(55, 80, 115), width=3)
            d.line([(fx - 15, fy + 20), (fx + 55, fy + 85)], fill=(120, 80, 40), width=5)
        elif idx == 1:
            # Close-up of crystal sweat drops falling onto green sprouts in rich soil
            d.rectangle([0, 250, W, H], fill=(135, 95, 62))
            for sx in (150, 240, 330):
                d.line([(sx, 260), (sx - 15, 175)], fill=(65, 155, 60), width=5)
                d.line([(sx, 260), (sx + 18, 180)], fill=(75, 168, 68), width=5)
            for dx, dy in [(195, 125), (245, 155), (285, 115)]:
                d.polygon([(dx, dy - 18), (dx - 11, dy + 6), (dx + 11, dy + 6)], fill=(135, 215, 250), outline=(65, 155, 215), width=2)
                d.ellipse([dx - 11, dy, dx + 11, dy + 20], fill=(135, 215, 250), outline=(65, 155, 215), width=2)
        elif idx == 2:
            # Porcelain bowl of steaming white rice
            d.ellipse([135, 175, 345, 275], fill=(255, 255, 252), outline=(185, 195, 210), width=3)
            d.chord([130, 195, 350, 335], start=0, end=180, fill=(75, 135, 205), outline=(45, 85, 145), width=4)
        else:
            # Golden harvest ears of grain & happy child cherishing every grain
            for gx in range(60, W - 50, 45):
                d.arc([gx - 20, 140, gx + 30, 290], start=200, end=340, fill=(235, 180, 45), width=5)
            d.ellipse([175, 165, 305, 275], fill=(255, 252, 245), outline=(215, 165, 55), width=3)
        panels.append(im)
    return build_grid(panels, BRAIN_DIR / "story34_grid.jpg")


def render_story35_pond() -> Path:
    """35. 《小池》· 杨万里"""
    W, H = 480, 360
    panels = []
    for idx in range(4):
        im = make_xuan_paper(W, H, (225, 246, 232), (142, 212, 188), seed=350 + idx)
        d = ImageDraw.Draw(im)
        # Clear pond water
        d.rectangle([0, 155, W, H], fill=(118, 202, 182))
        for ry in range(180, H - 20, 34):
            d.arc([80, ry, 390, ry + 18], start=0, end=180, fill=(195, 240, 228), width=2)

        if idx == 0:
            # Mossy spring rocks & gentle stream
            for rx, ry, rr in [(75, 155, 45), (145, 162, 36), (55, 195, 38)]:
                d.ellipse([rx - rr, ry - rr, rx + rr, ry + rr], fill=(115, 135, 122), outline=(75, 92, 82), width=3)
            d.polygon([(110, 155), (145, 160), (265, H), (165, H)], fill=(195, 245, 238))
        elif idx == 1:
            # Lush green tree shade reflected in sunny pond
            d.ellipse([-40, -35, 240, 145], fill=(82, 158, 92))
            d.ellipse([120, -45, 380, 125], fill=(98, 175, 105))
            d.ellipse([60, 210, 340, 330], fill=(88, 168, 145))
        elif idx == 2:
            # Pointed pink-and-green young lotus bud poking out of water
            d.ellipse([85, 245, 215, 295], fill=(68, 158, 95), outline=(45, 115, 65), width=2)
            d.line([(240, 320), (240, 165)], fill=(75, 145, 78), width=6)
            d.polygon([(240, 95), (212, 172), (240, 182), (268, 172)], fill=(252, 148, 175), outline=(215, 92, 125), width=3)
        else:
            # Red dragonfly perched on top of the pointed lotus bud
            d.line([(240, 330), (240, 175)], fill=(75, 145, 78), width=6)
            d.polygon([(240, 110), (214, 182), (240, 192), (266, 182)], fill=(252, 148, 175), outline=(215, 92, 125), width=3)
            # Dragonfly on tip (240, 110)
            d.ellipse([200, 88, 238, 102], fill=(215, 242, 252), outline=(145, 185, 205), width=2)
            d.ellipse([242, 88, 280, 102], fill=(215, 242, 252), outline=(145, 185, 205), width=2)
            d.line([(240, 82), (240, 138)], fill=(235, 65, 55), width=5)
            d.ellipse([234, 75, 246, 87], fill=(235, 65, 55))
        panels.append(im)
    return build_grid(panels, BRAIN_DIR / "story35_grid.jpg")


def render_story36_jiangnan() -> Path:
    """36. 《江南》· 汉乐府"""
    W, H = 480, 360
    panels = []
    for idx in range(4):
        im = make_xuan_paper(W, H, (215, 245, 238), (95, 192, 175), seed=360 + idx)
        d = ImageDraw.Draw(im)
        # Round green lotus leaves
        leaf_coords = [(85, 215, 62), (235, 245, 72), (385, 210, 64), (155, 145, 52), (325, 140, 55)]
        for lx, ly, lr in leaf_coords:
            d.ellipse([lx - lr, ly - int(lr * 0.65), lx + lr, ly + int(lr * 0.65)], fill=(68, 165, 98), outline=(42, 118, 68), width=3)
            for ang in range(0, 360, 45):
                ex = lx + int(lr * 0.85 * math.cos(math.radians(ang)))
                ey = ly + int(lr * 0.55 * math.sin(math.radians(ang)))
                d.line([(lx, ly), (ex, ey)], fill=(95, 192, 122), width=2)

        # Helper to draw little red koi fish
        def draw_koi(fx: int, fy: int, dir_x: int = 1) -> None:
            d.ellipse([fx - 22, fy - 11, fx + 22, fy + 11], fill=(245, 82, 55), outline=(185, 45, 25), width=2)
            d.polygon(
                [
                    (fx - 20 * dir_x, fy),
                    (fx - 38 * dir_x, fy - 14),
                    (fx - 38 * dir_x, fy + 14),
                ],
                fill=(252, 125, 85),
                outline=(185, 45, 25),
            )
            d.ellipse([fx + 10 * dir_x - 3, fy - 4, fx + 10 * dir_x + 3, fy + 2], fill=(25, 25, 30))

        if idx == 0:
            # Wooden boat gathering lotus pods
            d.polygon([(95, 255), (365, 255), (325, 305), (135, 305)], fill=(155, 98, 52), outline=(92, 55, 25), width=3)
        elif idx == 1:
            # Blooming pink lotus flowers among lush leaves
            for bx, by in [(165, 190), (315, 185)]:
                for dx in (-16, 0, 16):
                    d.ellipse([bx + dx - 14, by - 28, bx + dx + 14, by + 8], fill=(255, 162, 188), outline=(225, 105, 142), width=2)
        elif idx == 2:
            # Red fish playing hide-and-seek with bubbles
            draw_koi(155, 285, 1)
            draw_koi(335, 275, -1)
            for bx, by in [(190, 275), (202, 262), (295, 265)]:
                d.ellipse([bx - 5, by - 5, bx + 5, by + 5], outline=(235, 252, 250), width=2)
        else:
            # Fish darting east, west, south, north in joyful circle
            draw_koi(115, 275, 1)
            draw_koi(365, 275, -1)
            draw_koi(240, 185, 1)
            draw_koi(240, 315, -1)
        panels.append(im)
    return build_grid(panels, BRAIN_DIR / "story36_grid.jpg")


def main() -> None:
    grid_files = {
        31: render_story31_geese(),
        32: render_story32_moon(),
        33: render_story33_spring(),
        34: render_story34_farmers(),
        35: render_story35_pond(),
        36: render_story36_jiangnan(),
    }

    assets = {}
    for sid, gpath in grid_files.items():
        b_url, p_urls = extract_story_images(gpath, quality=80)
        assets[sid] = (b_url, p_urls)
        print(f"Story {sid}: banner={len(b_url)} chars, panels={[len(u) for u in p_urls]}")

    s31_b, s31_p = assets[31]
    s32_b, s32_p = assets[32]
    s33_b, s33_p = assets[33]
    s34_b, s34_p = assets[34]
    s35_b, s35_p = assets[35]
    s36_b, s36_p = assets[36]

    new_stories_js = f"""  }},
  {{
    id: 31,
    category: "poetry",
    icon: "🦢",
    title: "31. 《咏鹅》· 大白鹅唱山歌",
    titleText: "咏鹅，大白鹅唱山歌",
    titlePinyin: "yǒng é · dà bái é chàng shān gē",
    titleRuby: `<span class="punct">《</span><span class="word-group"><ruby>咏<rt>yǒng</rt></ruby><ruby>鹅<rt>é</rt></ruby></span><span class="punct">》· </span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>白<rt>bái</rt></ruby><ruby>鹅<rt>é</rt></ruby></span><span class="word-group"><ruby>唱<rt>chàng</rt></ruby><ruby>山<rt>shān</rt></ruby><ruby>歌<rt>gē</rt></ruby></span>`,
    titleEn: "Ode to the Goose · Luo Binwang (Tang Dynasty)",
    titleEnHtml: `<span class="en-word-group">Ode to the Goose</span> <span class="en-word-group">· Luo Binwang</span> <span class="en-word-group">(Tang Dynasty)</span>`,
    subtitle: "古诗绘本 · 唐 · 骆宾王",
    bannerImg: "{s31_b}",
    sentences: [
      {{
        img: "{s31_p[0]}",
        text: "鹅，鹅，鹅，大白鹅排着队游过小河！",
        ruby: `<span class="word-group"><ruby>鹅<rt>é</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>鹅<rt>é</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>鹅<rt>é</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>白<rt>bái</rt></ruby><ruby>鹅<rt>é</rt></ruby></span><span class="word-group"><ruby>排<rt>pái</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>队<rt>duì</rt></ruby></span><span class="word-group"><ruby>游<rt>yóu</rt></ruby><ruby>过<rt>guò</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>河<rt>hé</rt></ruby></span><span class="punct">！</span>`,
        en: '"Goose, goose, goose!" The big white geese swim in a row across the little river!',
        enHtml: `<span class="en-word-group">"Goose, goose, goose!"</span> <span class="en-word-group">The big white geese</span> <span class="en-word-group">swim in a row</span> <span class="en-word-group">across the little river!</span>`
      }},
      {{
        img: "{s31_p[1]}",
        text: "曲项向天歌，它们弯着长脖子对着蓝天欢快地唱歌。",
        ruby: `<span class="word-group"><ruby>曲<rt>qū</rt></ruby><ruby>项<rt>xiàng</rt></ruby></span><span class="word-group"><ruby>向<rt>xiàng</rt></ruby><ruby>天<rt>tiān</rt></ruby><ruby>歌<rt>gē</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>它<rt>tā</rt></ruby><ruby>们<rt>men</rt></ruby></span><span class="word-group"><ruby>弯<rt>wān</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>长<rt>cháng</rt></ruby><ruby>脖<rt>bó</rt></ruby><ruby>子<rt>zi</rt></ruby></span><span class="word-group"><ruby>对<rt>duì</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>蓝<rt>lán</rt></ruby><ruby>天<rt>tiān</rt></ruby></span><span class="word-group"><ruby>欢<rt>huān</rt></ruby><ruby>快<rt>kuài</rt></ruby><ruby>地<rt>de</rt></ruby><ruby>唱<rt>chàng</rt></ruby><ruby>歌<rt>gē</rt></ruby></span><span class="punct">。</span>`,
        en: '"Bending their necks to sing to the sky"—they curve their long necks and sing cheerfully to the blue sky.',
        enHtml: `<span class="en-word-group">"Bending their necks</span> <span class="en-word-group">to sing to the sky"—</span> <span class="en-word-group">they curve their long necks</span> <span class="en-word-group">and sing cheerfully</span> <span class="en-word-group">to the blue sky.</span>`
      }},
      {{
        img: "{s31_p[2]}",
        text: "白毛浮绿水，雪白的羽毛轻轻漂浮在碧绿的湖水上。",
        ruby: `<span class="word-group"><ruby>白<rt>bái</rt></ruby><ruby>毛<rt>máo</rt></ruby></span><span class="word-group"><ruby>浮<rt>fú</rt></ruby><ruby>绿<rt>lǜ</rt></ruby><ruby>水<rt>shuǐ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>雪<rt>xuě</rt></ruby><ruby>白<rt>bái</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>羽<rt>yǔ</rt></ruby><ruby>毛<rt>máo</rt></ruby></span><span class="word-group"><ruby>轻<rt>qīng</rt></ruby><ruby>轻<rt>qīng</rt></ruby><ruby>漂<rt>piāo</rt></ruby><ruby>浮<rt>fú</rt></ruby><ruby>在<rt>zài</rt></ruby></span><span class="word-group"><ruby>碧<rt>bì</rt></ruby><ruby>绿<rt>lǜ</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>湖<rt>hú</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>上<rt>shàng</rt></ruby></span><span class="punct">。</span>`,
        en: '"White feathers float on emerald water"—their snow-white feathers float gently on the green lake.',
        enHtml: `<span class="en-word-group">"White feathers</span> <span class="en-word-group">float on emerald water"—</span> <span class="en-word-group">their snow-white feathers</span> <span class="en-word-group">float gently</span> <span class="en-word-group">on the green lake.</span>`
      }},
      {{
        img: "{s31_p[3]}",
        text: "红掌拨清波，红色的脚掌像小船桨一样拨开清澈的水波！",
        ruby: `<span class="word-group"><ruby>红<rt>hóng</rt></ruby><ruby>掌<rt>zhǎng</rt></ruby></span><span class="word-group"><ruby>拨<rt>bō</rt></ruby><ruby>清<rt>qīng</rt></ruby><ruby>波<rt>bō</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>红<rt>hóng</rt></ruby><ruby>色<rt>sè</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>脚<rt>jiǎo</rt></ruby><ruby>掌<rt>zhǎng</rt></ruby></span><span class="word-group"><ruby>像<rt>xiàng</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>船<rt>chuán</rt></ruby><ruby>桨<rt>jiǎng</rt></ruby><ruby>一<rt>yí</rt></ruby><ruby>样<rt>yàng</rt></ruby></span><span class="word-group"><ruby>拨<rt>bō</rt></ruby><ruby>开<rt>kāi</rt></ruby></span><span class="word-group"><ruby>清<rt>qīng</rt></ruby><ruby>澈<rt>chè</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>波<rt>bō</rt></ruby></span><span class="punct">！</span>`,
        en: '"Red webbed feet paddle the clear waves"—their red feet paddle the crystal-clear ripples like little oars!',
        enHtml: `<span class="en-word-group">"Red webbed feet</span> <span class="en-word-group">paddle the clear waves"—</span> <span class="en-word-group">their red feet paddle</span> <span class="en-word-group">the crystal-clear ripples</span> <span class="en-word-group">like little oars!</span>`
      }}
    ],
    vocab: [
      {{ hz: "曲项", py: "qū xiàng", en: "curved neck" }},
      {{ hz: "白毛", py: "bái máo", en: "white feathers" }},
      {{ hz: "绿水", py: "lǜ shuǐ", en: "emerald water" }},
      {{ hz: "清波", py: "qīng bō", en: "clear ripples" }}
    ]
  }},
  {{
    id: 32,
    category: "poetry",
    icon: "🌙",
    title: "32. 《静夜思》· 月光下的思念",
    titleText: "静夜思，月光下的思念",
    titlePinyin: "jìng yè sī · yuè guāng xià de sī niàn",
    titleRuby: `<span class="punct">《</span><span class="word-group"><ruby>静<rt>jìng</rt></ruby><ruby>夜<rt>yè</rt></ruby><ruby>思<rt>sī</rt></ruby></span><span class="punct">》· </span><span class="word-group"><ruby>月<rt>yuè</rt></ruby><ruby>光<rt>guāng</rt></ruby><ruby>下<rt>xià</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>思<rt>sī</rt></ruby><ruby>念<rt>niàn</rt></ruby></span>`,
    titleEn: "Quiet Night Thoughts · Li Bai (Tang Dynasty)",
    titleEnHtml: `<span class="en-word-group">Quiet Night Thoughts</span> <span class="en-word-group">· Li Bai</span> <span class="en-word-group">(Tang Dynasty)</span>`,
    subtitle: "古诗绘本 · 唐 · 李白",
    bannerImg: "{s32_b}",
    sentences: [
      {{
        img: "{s32_p[0]}",
        text: "床前明月光，安静的夜晚，洁白的月光洒在小床前。",
        ruby: `<span class="word-group"><ruby>床<rt>chuáng</rt></ruby><ruby>前<rt>qián</rt></ruby></span><span class="word-group"><ruby>明<rt>míng</rt></ruby><ruby>月<rt>yuè</rt></ruby><ruby>光<rt>guāng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>安<rt>ān</rt></ruby><ruby>静<rt>jìng</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>夜<rt>yè</rt></ruby><ruby>晚<rt>wǎn</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>洁<rt>jié</rt></ruby><ruby>白<rt>bái</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>月<rt>yuè</rt></ruby><ruby>光<rt>guāng</rt></ruby></span><span class="word-group"><ruby>洒<rt>sǎ</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>床<rt>chuáng</rt></ruby><ruby>前<rt>qián</rt></ruby></span><span class="punct">。</span>`,
        en: '"Bright moonlight before my bed"—on a quiet night, silvery moonlight shines in front of the bed.',
        enHtml: `<span class="en-word-group">"Bright moonlight</span> <span class="en-word-group">before my bed"—</span> <span class="en-word-group">on a quiet night,</span> <span class="en-word-group">silvery moonlight shines</span> <span class="en-word-group">in front of the bed.</span>`
      }},
      {{
        img: "{s32_p[1]}",
        text: "疑是地上霜，诗人还以为是地上铺了一层亮晶晶的白霜。",
        ruby: `<span class="word-group"><ruby>疑<rt>yí</rt></ruby><ruby>是<rt>shì</rt></ruby></span><span class="word-group"><ruby>地<rt>dì</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>霜<rt>shuāng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>诗<rt>shī</rt></ruby><ruby>人<rt>rén</rt></ruby></span><span class="word-group"><ruby>还<rt>hái</rt></ruby><ruby>以<rt>yǐ</rt></ruby><ruby>为<rt>wéi</rt></ruby><ruby>是<rt>shì</rt></ruby></span><span class="word-group"><ruby>地<rt>dì</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>铺<rt>pū</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>层<rt>céng</rt></ruby></span><span class="word-group"><ruby>亮<rt>liàng</rt></ruby><ruby>晶<rt>jīng</rt></ruby><ruby>晶<rt>jīng</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>白<rt>bái</rt></ruby><ruby>霜<rt>shuāng</rt></ruby></span><span class="punct">。</span>`,
        en: '"I wonder if it is frost on the ground"—the poet thought a layer of sparkling white frost covered the floor.',
        enHtml: `<span class="en-word-group">"I wonder if it is</span> <span class="en-word-group">frost on the ground"—</span> <span class="en-word-group">the poet thought</span> <span class="en-word-group">a layer of sparkling white frost</span> <span class="en-word-group">covered the floor.</span>`
      }},
      {{
        img: "{s32_p[2]}",
        text: "举头望明月，他抬起头，静静望着天空中又大又圆的月亮。",
        ruby: `<span class="word-group"><ruby>举<rt>jǔ</rt></ruby><ruby>头<rt>tóu</rt></ruby></span><span class="word-group"><ruby>望<rt>wàng</rt></ruby><ruby>明<rt>míng</rt></ruby><ruby>月<rt>yuè</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>他<rt>tā</rt></ruby><ruby>抬<rt>tái</rt></ruby><ruby>起<rt>qǐ</rt></ruby><ruby>头<rt>tóu</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>静<rt>jìng</rt></ruby><ruby>静<rt>jìng</rt></ruby><ruby>望<rt>wàng</rt></ruby><ruby>着<rt>zhe</rt></ruby></span><span class="word-group"><ruby>天<rt>tiān</rt></ruby><ruby>空<rt>kōng</rt></ruby><ruby>中<rt>zhōng</rt></ruby></span><span class="word-group"><ruby>又<rt>yòu</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>又<rt>yòu</rt></ruby><ruby>圆<rt>yuán</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>月<rt>yuè</rt></ruby><ruby>亮<rt>liang</rt></ruby></span><span class="punct">。</span>`,
        en: '"Raising my head, I gaze at the bright moon"—he looks up quietly at the big round moon in the sky.',
        enHtml: `<span class="en-word-group">"Raising my head,</span> <span class="en-word-group">I gaze at the bright moon"—</span> <span class="en-word-group">he looks up quietly</span> <span class="en-word-group">at the big round moon</span> <span class="en-word-group">in the sky.</span>`
      }},
      {{
        img: "{s32_p[3]}",
        text: "低头思故乡，他低下头，想念远方温暖的家乡和亲人。",
        ruby: `<span class="word-group"><ruby>低<rt>dī</rt></ruby><ruby>头<rt>tóu</rt></ruby></span><span class="word-group"><ruby>思<rt>sī</rt></ruby><ruby>故<rt>gù</rt></ruby><ruby>乡<rt>xiāng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>他<rt>tā</rt></ruby><ruby>低<rt>dī</rt></ruby><ruby>下<rt>xià</rt></ruby><ruby>头<rt>tóu</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>想<rt>xiǎng</rt></ruby><ruby>念<rt>niàn</rt></ruby></span><span class="word-group"><ruby>远<rt>yuǎn</rt></ruby><ruby>方<rt>fāng</rt></ruby><ruby>温<rt>wēn</rt></ruby><ruby>暖<rt>nuǎn</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>家<rt>jiā</rt></ruby><ruby>乡<rt>xiāng</rt></ruby><ruby>和<rt>hé</rt></ruby><ruby>亲<rt>qīn</rt></ruby><ruby>人<rt>rén</rt></ruby></span><span class="punct">。</span>`,
        en: '"Lowering my head, I think of my hometown"—he bows his head, missing his warm hometown and family far away.',
        enHtml: `<span class="en-word-group">"Lowering my head,</span> <span class="en-word-group">I think of my hometown"—</span> <span class="en-word-group">he bows his head,</span> <span class="en-word-group">missing his warm hometown</span> <span class="en-word-group">and family far away.</span>`
      }}
    ],
    vocab: [
      {{ hz: "明月", py: "míng yuè", en: "bright moon" }},
      {{ hz: "地上霜", py: "dì shàng shuāng", en: "frost on the ground" }},
      {{ hz: "举头", py: "jǔ tóu", en: "raise one's head" }},
      {{ hz: "故乡", py: "gù xiāng", en: "hometown" }}
    ]
  }},
  {{
    id: 33,
    category: "poetry",
    icon: "🌸",
    title: "33. 《春晓》· 春天早晨的小鸟",
    titleText: "春晓，春天早晨的小鸟",
    titlePinyin: "chūn xiǎo · chūn tiān zǎo chen de xiǎo niǎo",
    titleRuby: `<span class="punct">《</span><span class="word-group"><ruby>春<rt>chūn</rt></ruby><ruby>晓<rt>xiǎo</rt></ruby></span><span class="punct">》· </span><span class="word-group"><ruby>春<rt>chūn</rt></ruby><ruby>天<rt>tiān</rt></ruby><ruby>早<rt>zǎo</rt></ruby><ruby>晨<rt>chen</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>鸟<rt>niǎo</rt></ruby></span>`,
    titleEn: "Spring Morning · Meng Haoran (Tang Dynasty)",
    titleEnHtml: `<span class="en-word-group">Spring Morning</span> <span class="en-word-group">· Meng Haoran</span> <span class="en-word-group">(Tang Dynasty)</span>`,
    subtitle: "古诗绘本 · 唐 · 孟浩然",
    bannerImg: "{s33_b}",
    sentences: [
      {{
        img: "{s33_p[0]}",
        text: "春眠不觉晓，春天的觉真香呀，不知不觉天就亮了！",
        ruby: `<span class="word-group"><ruby>春<rt>chūn</rt></ruby><ruby>眠<rt>mián</rt></ruby></span><span class="word-group"><ruby>不<rt>bù</rt></ruby><ruby>觉<rt>jué</rt></ruby><ruby>晓<rt>xiǎo</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>春<rt>chūn</rt></ruby><ruby>天<rt>tiān</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>觉<rt>jiào</rt></ruby></span><span class="word-group"><ruby>真<rt>zhēn</rt></ruby><ruby>香<rt>xiāng</rt></ruby><ruby>呀<rt>ya</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>不<rt>bù</rt></ruby><ruby>知<rt>zhī</rt></ruby><ruby>不<rt>bù</rt></ruby><ruby>觉<rt>jué</rt></ruby></span><span class="word-group"><ruby>天<rt>tiān</rt></ruby><ruby>就<rt>jiù</rt></ruby><ruby>亮<rt>liàng</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="punct">！</span>`,
        en: '"In spring sleep, dawn comes unnoticed"—spring sleep is so cozy that morning arrives before you know it!',
        enHtml: `<span class="en-word-group">"In spring sleep,</span> <span class="en-word-group">dawn comes unnoticed"—</span> <span class="en-word-group">spring sleep is so cozy</span> <span class="en-word-group">that morning arrives</span> <span class="en-word-group">before you know it!</span>`
      }},
      {{
        img: "{s33_p[1]}",
        text: "处处闻啼鸟，推开窗户，到处都能听见小鸟清脆的歌声。",
        ruby: `<span class="word-group"><ruby>处<rt>chù</rt></ruby><ruby>处<rt>chù</rt></ruby></span><span class="word-group"><ruby>闻<rt>wén</rt></ruby><ruby>啼<rt>tí</rt></ruby><ruby>鸟<rt>niǎo</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>推<rt>tuī</rt></ruby><ruby>开<rt>kāi</rt></ruby><ruby>窗<rt>chuāng</rt></ruby><ruby>户<rt>hu</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>到<rt>dào</rt></ruby><ruby>处<rt>chù</rt></ruby><ruby>都<rt>dōu</rt></ruby><ruby>能<rt>néng</rt></ruby><ruby>听<rt>tīng</rt></ruby><ruby>见<rt>jiàn</rt></ruby></span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>鸟<rt>niǎo</rt></ruby><ruby>清<rt>qīng</rt></ruby><ruby>脆<rt>cuì</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>歌<rt>gē</rt></ruby><ruby>声<rt>shēng</rt></ruby></span><span class="punct">。</span>`,
        en: '"Everywhere I hear birds singing"—opening the window, cheerful bird songs can be heard all around.',
        enHtml: `<span class="en-word-group">"Everywhere I hear</span> <span class="en-word-group">birds singing"—</span> <span class="en-word-group">opening the window,</span> <span class="en-word-group">cheerful bird songs</span> <span class="en-word-group">can be heard all around.</span>`
      }},
      {{
        img: "{s33_p[2]}",
        text: "夜来风雨声，昨天夜里，院子里响起了沙沙的春风和春雨声。",
        ruby: `<span class="word-group"><ruby>夜<rt>yè</rt></ruby><ruby>来<rt>lái</rt></ruby></span><span class="word-group"><ruby>风<rt>fēng</rt></ruby><ruby>雨<rt>yǔ</rt></ruby><ruby>声<rt>shēng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>昨<rt>zuó</rt></ruby><ruby>天<rt>tiān</rt></ruby><ruby>夜<rt>yè</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>院<rt>yuàn</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="word-group"><ruby>响<rt>xiǎng</rt></ruby><ruby>起<rt>qǐ</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>沙<rt>shā</rt></ruby><ruby>沙<rt>shā</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>春<rt>chūn</rt></ruby><ruby>风<rt>fēng</rt></ruby><ruby>和<rt>hé</rt></ruby><ruby>春<rt>chūn</rt></ruby><ruby>雨<rt>yǔ</rt></ruby><ruby>声<rt>shēng</rt></ruby></span><span class="punct">。</span>`,
        en: '"Last night came the sound of wind and rain"—last night, gentle spring wind and rain rustled in the courtyard.',
        enHtml: `<span class="en-word-group">"Last night came</span> <span class="en-word-group">the sound of wind and rain"—</span> <span class="en-word-group">last night,</span> <span class="en-word-group">gentle spring wind and rain</span> <span class="en-word-group">rustled in the courtyard.</span>`
      }},
      {{
        img: "{s33_p[3]}",
        text: "花落知多少，不知道树上的桃花瓣，在草地上落了多少朵呢？",
        ruby: `<span class="word-group"><ruby>花<rt>huā</rt></ruby><ruby>落<rt>luò</rt></ruby></span><span class="word-group"><ruby>知<rt>zhī</rt></ruby><ruby>多<rt>duō</rt></ruby><ruby>少<rt>shǎo</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>不<rt>bù</rt></ruby><ruby>知<rt>zhī</rt></ruby><ruby>道<rt>dào</rt></ruby></span><span class="word-group"><ruby>树<rt>shù</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>桃<rt>táo</rt></ruby><ruby>花<rt>huā</rt></ruby><ruby>瓣<rt>bàn</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>在<rt>zài</rt></ruby><ruby>草<rt>cǎo</rt></ruby><ruby>地<rt>dì</rt></ruby><ruby>上<rt>shàng</rt></ruby></span><span class="word-group"><ruby>落<rt>luò</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>多<rt>duō</rt></ruby><ruby>少<rt>shǎo</rt></ruby><ruby>朵<rt>duǒ</rt></ruby><ruby>呢<rt>ne</rt></ruby></span><span class="punct">？</span>`,
        en: '"How many blossoms fell, I wonder?"—who knows how many pink peach petals drifted onto the grass?',
        enHtml: `<span class="en-word-group">"How many blossoms fell,</span> <span class="en-word-group">I wonder?"—</span> <span class="en-word-group">who knows how many</span> <span class="en-word-group">pink peach petals</span> <span class="en-word-group">drifted onto the grass?</span>`
      }}
    ],
    vocab: [
      {{ hz: "春眠", py: "chūn mián", en: "spring sleep" }},
      {{ hz: "啼鸟", py: "tí niǎo", en: "singing birds" }},
      {{ hz: "风雨", py: "fēng yǔ", en: "wind and rain" }},
      {{ hz: "花落", py: "huā luò", en: "falling blossoms" }}
    ]
  }},
  {{
    id: 34,
    category: "poetry",
    icon: "🌾",
    title: "34. 《悯农》· 珍惜每一粒米",
    titleText: "悯农，珍惜每一粒米",
    titlePinyin: "mǐn nóng · zhēn xī měi yí lì mǐ",
    titleRuby: `<span class="punct">《</span><span class="word-group"><ruby>悯<rt>mǐn</rt></ruby><ruby>农<rt>nóng</rt></ruby></span><span class="punct">》· </span><span class="word-group"><ruby>珍<rt>zhēn</rt></ruby><ruby>惜<rt>xī</rt></ruby></span><span class="word-group"><ruby>每<rt>měi</rt></ruby><ruby>一<rt>yí</rt></ruby><ruby>粒<rt>lì</rt></ruby><ruby>米<rt>mǐ</rt></ruby></span>`,
    titleEn: "Sympathy for the Farmers · Li Shen (Tang Dynasty)",
    titleEnHtml: `<span class="en-word-group">Sympathy for the Farmers</span> <span class="en-word-group">· Li Shen</span> <span class="en-word-group">(Tang Dynasty)</span>`,
    subtitle: "古诗绘本 · 唐 · 李绅",
    bannerImg: "{s34_b}",
    sentences: [
      {{
        img: "{s34_p[0]}",
        text: "锄禾日当午，大太阳当空照，农夫伯伯正在田里辛勤地锄草。",
        ruby: `<span class="word-group"><ruby>锄<rt>chú</rt></ruby><ruby>禾<rt>hé</rt></ruby></span><span class="word-group"><ruby>日<rt>rì</rt></ruby><ruby>当<rt>dāng</rt></ruby><ruby>午<rt>wǔ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>太<rt>tài</rt></ruby><ruby>阳<rt>yáng</rt></ruby><ruby>当<rt>dāng</rt></ruby><ruby>空<rt>kōng</rt></ruby><ruby>照<rt>zhào</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>农<rt>nóng</rt></ruby><ruby>夫<rt>fū</rt></ruby><ruby>伯<rt>bó</rt></ruby><ruby>伯<rt>bo</rt></ruby></span><span class="word-group"><ruby>正<rt>zhèng</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>田<rt>tián</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="word-group"><ruby>辛<rt>xīn</rt></ruby><ruby>勤<rt>qín</rt></ruby><ruby>地<rt>de</rt></ruby><ruby>锄<rt>chú</rt></ruby><ruby>草<rt>cǎo</rt></ruby></span><span class="punct">。</span>`,
        en: '"Hoeing grain under the midday sun"—beneath the blazing noon sun, the farmer works hard weeding the field.',
        enHtml: `<span class="en-word-group">"Hoeing grain</span> <span class="en-word-group">under the midday sun"—</span> <span class="en-word-group">beneath the blazing noon sun,</span> <span class="en-word-group">the farmer works hard</span> <span class="en-word-group">weeding the field.</span>`
      }},
      {{
        img: "{s34_p[1]}",
        text: "汗滴禾下土，一滴滴晶莹的汗水，落进了绿油油的禾苗泥土里。",
        ruby: `<span class="word-group"><ruby>汗<rt>hàn</rt></ruby><ruby>滴<rt>dī</rt></ruby></span><span class="word-group"><ruby>禾<rt>hé</rt></ruby><ruby>下<rt>xià</rt></ruby><ruby>土<rt>tǔ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>滴<rt>dī</rt></ruby><ruby>滴<rt>dī</rt></ruby><ruby>晶<rt>jīng</rt></ruby><ruby>莹<rt>yíng</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>汗<rt>hàn</rt></ruby><ruby>水<rt>shuǐ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>落<rt>luò</rt></ruby><ruby>进<rt>jìn</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>绿<rt>lǜ</rt></ruby><ruby>油<rt>yóu</rt></ruby><ruby>油<rt>yóu</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>禾<rt>hé</rt></ruby><ruby>苗<rt>miáo</rt></ruby><ruby>泥<rt>ní</rt></ruby><ruby>土<rt>tǔ</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="punct">。</span>`,
        en: '"Sweat drips into the soil beneath the crops"—shining drops of sweat fall into the soil under the green sprouts.',
        enHtml: `<span class="en-word-group">"Sweat drips into</span> <span class="en-word-group">the soil beneath the crops"—</span> <span class="en-word-group">shining drops of sweat</span> <span class="en-word-group">fall into the soil</span> <span class="en-word-group">under the green sprouts.</span>`
      }},
      {{
        img: "{s34_p[2]}",
        text: "谁知盘中餐，你知道小碗里香喷喷的白米饭是怎么来的吗？",
        ruby: `<span class="word-group"><ruby>谁<rt>shuí</rt></ruby><ruby>知<rt>zhī</rt></ruby></span><span class="word-group"><ruby>盘<rt>pán</rt></ruby><ruby>中<rt>zhōng</rt></ruby><ruby>餐<rt>cān</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>你<rt>nǐ</rt></ruby><ruby>知<rt>zhī</rt></ruby><ruby>道<rt>dào</rt></ruby></span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>碗<rt>wǎn</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="word-group"><ruby>香<rt>xiāng</rt></ruby><ruby>喷<rt>pēn</rt></ruby><ruby>喷<rt>pēn</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>白<rt>bái</rt></ruby><ruby>米<rt>mǐ</rt></ruby><ruby>饭<rt>fàn</rt></ruby></span><span class="word-group"><ruby>是<rt>shì</rt></ruby><ruby>怎<rt>zěn</rt></ruby><ruby>么<rt>me</rt></ruby><ruby>来<rt>lái</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>吗<rt>ma</rt></ruby></span><span class="punct">？</span>`,
        en: '"Who knows that the food on our plate"—do you know where the fragrant white rice in your bowl comes from?',
        enHtml: `<span class="en-word-group">"Who knows that</span> <span class="en-word-group">the food on our plate"—</span> <span class="en-word-group">do you know where</span> <span class="en-word-group">the fragrant white rice in your bowl</span> <span class="en-word-group">comes from?</span>`
      }},
      {{
        img: "{s34_p[3]}",
        text: "粒粒皆辛苦，每一粒粮食都藏着农夫伯伯满满的汗水与辛劳！",
        ruby: `<span class="word-group"><ruby>粒<rt>lì</rt></ruby><ruby>粒<rt>lì</rt></ruby></span><span class="word-group"><ruby>皆<rt>jiē</rt></ruby><ruby>辛<rt>xīn</rt></ruby><ruby>苦<rt>kǔ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>每<rt>měi</rt></ruby><ruby>一<rt>yí</rt></ruby><ruby>粒<rt>lì</rt></ruby><ruby>粮<rt>liáng</rt></ruby><ruby>食<rt>shi</rt></ruby></span><span class="word-group"><ruby>都<rt>dōu</rt></ruby><ruby>藏<rt>cáng</rt></ruby><ruby>着<rt>zhe</rt></ruby></span><span class="word-group"><ruby>农<rt>nóng</rt></ruby><ruby>夫<rt>fū</rt></ruby><ruby>伯<rt>bó</rt></ruby><ruby>伯<rt>bo</rt></ruby></span><span class="word-group"><ruby>满<rt>mǎn</rt></ruby><ruby>满<rt>mǎn</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>汗<rt>hàn</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>与<rt>yǔ</rt></ruby><ruby>辛<rt>xīn</rt></ruby><ruby>劳<rt>láo</rt></ruby></span><span class="punct">！</span>`,
        en: `"Every single grain comes from hard work"—every grain of rice holds the farmer's sweat and dedication!`,
        enHtml: `<span class="en-word-group">"Every single grain</span> <span class="en-word-group">comes from hard work"—</span> <span class="en-word-group">every grain of rice</span> <span class="en-word-group">holds the farmer's sweat</span> <span class="en-word-group">and dedication!</span>`
      }}
    ],
    vocab: [
      {{ hz: "锄禾", py: "chú hé", en: "hoeing crops" }},
      {{ hz: "汗滴", py: "hàn dī", en: "drops of sweat" }},
      {{ hz: "盘中餐", py: "pán zhōng cān", en: "food on the plate" }},
      {{ hz: "辛苦", py: "xīn kǔ", en: "hard work" }}
    ]
  }},
  {{
    id: 35,
    category: "poetry",
    icon: "🪷",
    title: "35. 《小池》· 蜻蜓立在荷花尖",
    titleText: "小池，蜻蜓立在荷花尖",
    titlePinyin: "xiǎo chí · qīng tíng lì zài hé huā jiān",
    titleRuby: `<span class="punct">《</span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>池<rt>chí</rt></ruby></span><span class="punct">》· </span><span class="word-group"><ruby>蜻<rt>qīng</rt></ruby><ruby>蜓<rt>tíng</rt></ruby></span><span class="word-group"><ruby>立<rt>lì</rt></ruby><ruby>在<rt>zài</rt></ruby></span><span class="word-group"><ruby>荷<rt>hé</rt></ruby><ruby>花<rt>huā</rt></ruby><ruby>尖<rt>jiān</rt></ruby></span>`,
    titleEn: "The Little Pond · Yang Wanli (Song Dynasty)",
    titleEnHtml: `<span class="en-word-group">The Little Pond</span> <span class="en-word-group">· Yang Wanli</span> <span class="en-word-group">(Song Dynasty)</span>`,
    subtitle: "古诗绘本 · 宋 · 杨万里",
    bannerImg: "{s35_b}",
    sentences: [
      {{
        img: "{s35_p[0]}",
        text: "泉眼无声惜细流，泉水悄悄地流淌，舍不得发出一点声音。",
        ruby: `<span class="word-group"><ruby>泉<rt>quán</rt></ruby><ruby>眼<rt>yǎn</rt></ruby></span><span class="word-group"><ruby>无<rt>wú</rt></ruby><ruby>声<rt>shēng</rt></ruby></span><span class="word-group"><ruby>惜<rt>xī</rt></ruby><ruby>细<rt>xì</rt></ruby><ruby>流<rt>liú</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>泉<rt>quán</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>悄<rt>qiāo</rt></ruby><ruby>悄<rt>qiāo</rt></ruby><ruby>地<rt>de</rt></ruby><ruby>流<rt>liú</rt></ruby><ruby>淌<rt>tǎng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>舍<rt>shě</rt></ruby><ruby>不<rt>bu</rt></ruby><ruby>得<rt>de</rt></ruby><ruby>发<rt>fā</rt></ruby><ruby>出<rt>chū</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>点<rt>diǎn</rt></ruby><ruby>声<rt>shēng</rt></ruby><ruby>音<rt>yīn</rt></ruby></span><span class="punct">。</span>`,
        en: '"The spring silently treasures its slender stream"—the clear spring flows quietly without making a sound.',
        enHtml: `<span class="en-word-group">"The spring silently treasures</span> <span class="en-word-group">its slender stream"—</span> <span class="en-word-group">the clear spring flows quietly</span> <span class="en-word-group">without making a sound.</span>`
      }},
      {{
        img: "{s35_p[1]}",
        text: "树阴照水爱晴柔，大树的影子映在池水里，喜爱这晴朗温柔的风光。",
        ruby: `<span class="word-group"><ruby>树<rt>shù</rt></ruby><ruby>阴<rt>yīn</rt></ruby></span><span class="word-group"><ruby>照<rt>zhào</rt></ruby><ruby>水<rt>shuǐ</rt></ruby></span><span class="word-group"><ruby>爱<rt>ài</rt></ruby><ruby>晴<rt>qíng</rt></ruby><ruby>柔<rt>róu</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>树<rt>shù</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>影<rt>yǐng</rt></ruby><ruby>子<rt>zi</rt></ruby></span><span class="word-group"><ruby>映<rt>yìng</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>池<rt>chí</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>喜<rt>xǐ</rt></ruby><ruby>爱<rt>ài</rt></ruby><ruby>这<rt>zhè</rt></ruby><ruby>晴<rt>qíng</rt></ruby><ruby>朗<rt>lǎng</rt></ruby><ruby>温<rt>wēn</rt></ruby><ruby>柔<rt>róu</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>风<rt>fēng</rt></ruby><ruby>光<rt>guāng</rt></ruby></span><span class="punct">。</span>`,
        en: `"Tree shade reflected on water loves the sunny breeze"—the tree's reflection rests on the pond in the gentle sunshine.`,
        enHtml: `<span class="en-word-group">"Tree shade reflected on water</span> <span class="en-word-group">loves the sunny breeze"—</span> <span class="en-word-group">the tree's reflection</span> <span class="en-word-group">rests on the pond</span> <span class="en-word-group">in the gentle sunshine.</span>`
      }},
      {{
        img: "{s35_p[2]}",
        text: "小荷才露尖尖角，嫩绿的小荷叶刚刚从水面露出尖尖的一角。",
        ruby: `<span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>荷<rt>hé</rt></ruby></span><span class="word-group"><ruby>才<rt>cái</rt></ruby><ruby>露<rt>lù</rt></ruby></span><span class="word-group"><ruby>尖<rt>jiān</rt></ruby><ruby>尖<rt>jiān</rt></ruby><ruby>角<rt>jiǎo</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>嫩<rt>nèn</rt></ruby><ruby>绿<rt>lǜ</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>荷<rt>hé</rt></ruby><ruby>叶<rt>yè</rt></ruby></span><span class="word-group"><ruby>刚<rt>gāng</rt></ruby><ruby>刚<rt>gāng</rt></ruby><ruby>从<rt>cóng</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>面<rt>miàn</rt></ruby></span><span class="word-group"><ruby>露<rt>lù</rt></ruby><ruby>出<rt>chū</rt></ruby><ruby>尖<rt>jiān</rt></ruby><ruby>尖<rt>jiān</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>角<rt>jiǎo</rt></ruby></span><span class="punct">。</span>`,
        en: '"Tiny lotus buds just show their pointed tips"—tender lotus buds have just poked their pointed tips above the water.',
        enHtml: `<span class="en-word-group">"Tiny lotus buds</span> <span class="en-word-group">just show their pointed tips"—</span> <span class="en-word-group">tender lotus buds</span> <span class="en-word-group">have just poked their pointed tips</span> <span class="en-word-group">above the water.</span>`
      }},
      {{
        img: "{s35_p[3]}",
        text: "早有蜻蜓立上头，已经有一只红蜻蜓，轻巧地停在了荷花苞上！",
        ruby: `<span class="word-group"><ruby>早<rt>zǎo</rt></ruby><ruby>有<rt>yǒu</rt></ruby><ruby>蜻<rt>qīng</rt></ruby><ruby>蜓<rt>tíng</rt></ruby></span><span class="word-group"><ruby>立<rt>lì</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>头<rt>tóu</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>已<rt>yǐ</rt></ruby><ruby>经<rt>jīng</rt></ruby><ruby>有<rt>yǒu</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>只<rt>zhī</rt></ruby><ruby>红<rt>hóng</rt></ruby><ruby>蜻<rt>qīng</rt></ruby><ruby>蜓<rt>tíng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>轻<rt>qīng</rt></ruby><ruby>巧<rt>qiǎo</rt></ruby><ruby>地<rt>de</rt></ruby><ruby>停<rt>tíng</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>荷<rt>hé</rt></ruby><ruby>花<rt>huā</rt></ruby><ruby>苞<rt>bāo</rt></ruby><ruby>上<rt>shàng</rt></ruby></span><span class="punct">！</span>`,
        en: '"Already a dragonfly stands on top"—a little red dragonfly has already perched lightly on the bud!',
        enHtml: `<span class="en-word-group">"Already a dragonfly</span> <span class="en-word-group">stands on top"—</span> <span class="en-word-group">a little red dragonfly</span> <span class="en-word-group">has already perched lightly</span> <span class="en-word-group">on the bud!</span>`
      }}
    ],
    vocab: [
      {{ hz: "泉眼", py: "quán yǎn", en: "spring source" }},
      {{ hz: "树阴", py: "shù yīn", en: "tree shade" }},
      {{ hz: "小荷", py: "xiǎo hé", en: "young lotus" }},
      {{ hz: "蜻蜓", py: "qīng tíng", en: "dragonfly" }}
    ]
  }},
  {{
    id: 36,
    category: "poetry",
    icon: "🐟",
    title: "36. 《江南》· 小鱼荷叶捉迷藏",
    titleText: "江南，小鱼荷叶捉迷藏",
    titlePinyin: "jiāng nán · xiǎo yú hé yè zhuō mí cáng",
    titleRuby: `<span class="punct">《</span><span class="word-group"><ruby>江<rt>jiāng</rt></ruby><ruby>南<rt>nán</rt></ruby></span><span class="punct">》· </span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>鱼<rt>yú</rt></ruby><ruby>荷<rt>hé</rt></ruby><ruby>叶<rt>yè</rt></ruby></span><span class="word-group"><ruby>捉<rt>zhuō</rt></ruby><ruby>迷<rt>mí</rt></ruby><ruby>藏<rt>cáng</rt></ruby></span>`,
    titleEn: "Lotus Pond of Jiangnan · Han Dynasty Folk Song",
    titleEnHtml: `<span class="en-word-group">Lotus Pond of Jiangnan</span> <span class="en-word-group">· Han Dynasty</span> <span class="en-word-group">Folk Song</span>`,
    subtitle: "古诗绘本 · 汉乐府民歌",
    bannerImg: "{s36_b}",
    sentences: [
      {{
        img: "{s36_p[0]}",
        text: "江南可采莲，夏天到了，小朋友们划着小木船去池塘采莲蓬。",
        ruby: `<span class="word-group"><ruby>江<rt>jiāng</rt></ruby><ruby>南<rt>nán</rt></ruby></span><span class="word-group"><ruby>可<rt>kě</rt></ruby><ruby>采<rt>cǎi</rt></ruby><ruby>莲<rt>lián</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>夏<rt>xià</rt></ruby><ruby>天<rt>tiān</rt></ruby><ruby>到<rt>dào</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>朋<rt>péng</rt></ruby><ruby>友<rt>you</rt></ruby><ruby>们<rt>men</rt></ruby></span><span class="word-group"><ruby>划<rt>huá</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>木<rt>mù</rt></ruby><ruby>船<rt>chuán</rt></ruby></span><span class="word-group"><ruby>去<rt>qù</rt></ruby><ruby>池<rt>chí</rt></ruby><ruby>塘<rt>táng</rt></ruby><ruby>采<rt>cǎi</rt></ruby><ruby>莲<rt>lián</rt></ruby><ruby>蓬<rt>peng</rt></ruby></span><span class="punct">。</span>`,
        en: '"In Jiangnan we can gather lotus"—summer is here, and children row little wooden boats to pick lotus pods.',
        enHtml: `<span class="en-word-group">"In Jiangnan</span> <span class="en-word-group">we can gather lotus"—</span> <span class="en-word-group">summer is here,</span> <span class="en-word-group">and children row little wooden boats</span> <span class="en-word-group">to pick lotus pods.</span>`
      }},
      {{
        img: "{s36_p[1]}",
        text: "莲叶何田田，圆圆的绿荷叶挨挨挤挤，像一把把碧绿的小雨伞！",
        ruby: `<span class="word-group"><ruby>莲<rt>lián</rt></ruby><ruby>叶<rt>yè</rt></ruby></span><span class="word-group"><ruby>何<rt>hé</rt></ruby><ruby>田<rt>tián</rt></ruby><ruby>田<rt>tián</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>圆<rt>yuán</rt></ruby><ruby>圆<rt>yuán</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>绿<rt>lǜ</rt></ruby><ruby>荷<rt>hé</rt></ruby><ruby>叶<rt>yè</rt></ruby></span><span class="word-group"><ruby>挨<rt>āi</rt></ruby><ruby>挨<rt>āi</rt></ruby><ruby>挤<rt>jǐ</rt></ruby><ruby>挤<rt>jǐ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>像<rt>xiàng</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>把<rt>bǎ</rt></ruby><ruby>把<rt>bǎ</rt></ruby><ruby>碧<rt>bì</rt></ruby><ruby>绿<rt>lǜ</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>雨<rt>yǔ</rt></ruby><ruby>伞<rt>sǎn</rt></ruby></span><span class="punct">！</span>`,
        en: '"How lush and round the lotus leaves are!"—round green lotus leaves cluster together like emerald umbrellas!',
        enHtml: `<span class="en-word-group">"How lush and round</span> <span class="en-word-group">the lotus leaves are!"—</span> <span class="en-word-group">round green lotus leaves</span> <span class="en-word-group">cluster together</span> <span class="en-word-group">like emerald umbrellas!</span>`
      }},
      {{
        img: "{s36_p[2]}",
        text: "鱼戏莲叶间，快活的小红鱼在荷叶底下吐着泡泡捉迷藏。",
        ruby: `<span class="word-group"><ruby>鱼<rt>yú</rt></ruby><ruby>戏<rt>xì</rt></ruby></span><span class="word-group"><ruby>莲<rt>lián</rt></ruby><ruby>叶<rt>yè</rt></ruby><ruby>间<rt>jiān</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>快<rt>kuài</rt></ruby><ruby>活<rt>huo</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>红<rt>hóng</rt></ruby><ruby>鱼<rt>yú</rt></ruby></span><span class="word-group"><ruby>在<rt>zài</rt></ruby><ruby>荷<rt>hé</rt></ruby><ruby>叶<rt>yè</rt></ruby><ruby>底<rt>dǐ</rt></ruby><ruby>下<rt>xià</rt></ruby></span><span class="word-group"><ruby>吐<rt>tǔ</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>泡<rt>pào</rt></ruby><ruby>泡<rt>pao</rt></ruby><ruby>捉<rt>zhuō</rt></ruby><ruby>迷<rt>mí</rt></ruby><ruby>藏<rt>cáng</rt></ruby></span><span class="punct">。</span>`,
        en: '"Fish play among the lotus leaves"—happy little red fish blow bubbles and play hide-and-seek beneath the leaves.',
        enHtml: `<span class="en-word-group">"Fish play among</span> <span class="en-word-group">the lotus leaves"—</span> <span class="en-word-group">happy little red fish</span> <span class="en-word-group">blow bubbles and play hide-and-seek</span> <span class="en-word-group">beneath the leaves.</span>`
      }},
      {{
        img: "{s36_p[3]}",
        text: "鱼戏莲叶东，鱼戏莲叶西，小鱼一会儿游向东、一会儿游向西，热闹极了！",
        ruby: `<span class="word-group"><ruby>鱼<rt>yú</rt></ruby><ruby>戏<rt>xì</rt></ruby><ruby>莲<rt>lián</rt></ruby><ruby>叶<rt>yè</rt></ruby><ruby>东<rt>dōng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>鱼<rt>yú</rt></ruby><ruby>戏<rt>xì</rt></ruby><ruby>莲<rt>lián</rt></ruby><ruby>叶<rt>yè</rt></ruby><ruby>西<rt>xī</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>鱼<rt>yú</rt></ruby></span><span class="word-group"><ruby>一<rt>yí</rt></ruby><ruby>会<rt>huì</rt></ruby><ruby>儿<rt>r</rt></ruby><ruby>游<rt>yóu</rt></ruby><ruby>向<rt>xiàng</rt></ruby><ruby>东<rt>dōng</rt></ruby></span><span class="punct">、</span><span class="word-group"><ruby>一<rt>yí</rt></ruby><ruby>会<rt>huì</rt></ruby><ruby>儿<rt>r</rt></ruby><ruby>游<rt>yóu</rt></ruby><ruby>向<rt>xiàng</rt></ruby><ruby>西<rt>xī</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>热<rt>rè</rt></ruby><ruby>闹<rt>nao</rt></ruby><ruby>极<rt>jí</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="punct">！</span>`,
        en: '"Fish play east, fish play west"—the little fish dart east and west in a joyful game!',
        enHtml: `<span class="en-word-group">"Fish play east,</span> <span class="en-word-group">fish play west"—</span> <span class="en-word-group">the little fish</span> <span class="en-word-group">dart east and west</span> <span class="en-word-group">in a joyful game!</span>`
      }}
    ],
    vocab: [
      {{ hz: "采莲", py: "cǎi lián", en: "pick lotus" }},
      {{ hz: "莲叶", py: "lián yè", en: "lotus leaf" }},
      {{ hz: "田田", py: "tián tián", en: "lush and round" }},
      {{ hz: "捉迷藏", py: "zhuō mí cáng", en: "hide-and-seek" }}
    ]
  }}
];"""

    html = INDEX_PATH.read_text(encoding="utf-8")

    target_end = """      { hz: "歌谣", py: "gē yáo", en: "folk song" },
      { hz: "接纳", py: "jiē nà", en: "accept and embrace" }
    ]
  }
];"""

    assert target_end in html, "Could not find end of Story 30 in index.html"
    html = html.replace(
        target_end,
        """      { hz: "歌谣", py: "gē yáo", en: "folk song" },
      { hz: "接纳", py: "jiē nà", en: "accept and embrace" }
    ]
"""
        + new_stories_js,
        1,
    )

    old_categories = """const CATEGORIES = [
  { id: 'all', label: '✨ 全部故事 · All (30)' },
  { id: 'redpanda', label: '🐼 变身红熊猫 · Red Panda (4)' },
  { id: 'bluepup', label: '🐾 蓝小狗一家 · Blue Pup (4)' },
  { id: 'dogcop', label: '🐶 神探汪汪 · Dog Cop (4)' },
  { id: 'weird', label: '🤪 疯狂学校 · My Weird School (4)' },
  { id: 'adventure', label: '🕵️ 脑洞探秘 · Mystery & Sci-Fi (2)' },
  { id: 'school', label: '🏫 校园日常 · School Life (4)' },
  { id: 'fairy', label: '🐾 童话绘本 · Animal Tales (8)' }
];"""

    new_categories = """const CATEGORIES = [
  { id: 'all', label: '✨ 全部故事 · All (36)' },
  { id: 'poetry', label: '📜 古诗绘本 · Classical Poems (6)' },
  { id: 'redpanda', label: '🐼 变身红熊猫 · Red Panda (4)' },
  { id: 'bluepup', label: '🐾 蓝小狗一家 · Blue Pup (4)' },
  { id: 'dogcop', label: '🐶 神探汪汪 · Dog Cop (4)' },
  { id: 'weird', label: '🤪 疯狂学校 · My Weird School (4)' },
  { id: 'adventure', label: '🕵️ 脑洞探秘 · Mystery & Sci-Fi (2)' },
  { id: 'school', label: '🏫 校园日常 · School Life (4)' },
  { id: 'fairy', label: '🐾 童话绘本 · Animal Tales (8)' }
];"""

    assert old_categories in html, "Could not find CATEGORIES in index.html"
    html = html.replace(old_categories, new_categories, 1)

    INDEX_PATH.write_text(html, encoding="utf-8")
    print("Successfully updated index.html with Classical Poetry Stories 31-36 and updated CATEGORIES!")


if __name__ == "__main__":
    main()
