#!/usr/bin/env python3
"""
Render rich storybook 2x2 grid illustrations for:
- Stories 37-40: 🍫 奇幻巧克力工厂 · Chocolate Factory (Willy Wonka inspired)
- Stories 41-44: 🎃 搞怪万圣节 · Halloween Tales

Crop them into WebP bannerImg and panel imgs, and inject Stories 37-44 into index.html.
"""

import math
import random
from pathlib import Path
from PIL import Image, ImageDraw
from crop_grid_images import extract_story_images
from add_poetry_stories import build_grid, make_xuan_paper

BRAIN_DIR = Path("/Users/leizhou/.gemini/antigravity-cli/brain/dde92688-d628-4cf6-9d61-3d1a08abad1b")
ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT_DIR / "index.html"


def draw_candy_cane(d: ImageDraw.ImageDraw, x: int, y_bot: int, h: int = 85) -> None:
    d.line([(x, y_bot), (x, y_bot - h)], fill=(252, 250, 248), width=10)
    d.arc([x - 18, y_bot - h - 18, x + 18, y_bot - h + 18], start=180, end=360, fill=(252, 250, 248), width=10)
    for sy in range(y_bot - 12, y_bot - h, -18):
        d.line([(x - 5, sy), (x + 5, sy - 7)], fill=(235, 55, 65), width=5)


def draw_lollipop(d: ImageDraw.ImageDraw, x: int, y_bot: int, r: int = 24, col1=(255, 105, 165), col2=(255, 235, 110)) -> None:
    d.line([(x, y_bot), (x, y_bot - 65)], fill=(245, 240, 230), width=5)
    cy = y_bot - 65 - r
    d.ellipse([x - r, cy - r, x + r, cy + r], fill=col1, outline=(195, 55, 110), width=2)
    d.ellipse([x - int(r * 0.65), cy - int(r * 0.65), x + int(r * 0.65), cy + int(r * 0.65)], fill=col2)
    d.ellipse([x - int(r * 0.3), cy - int(r * 0.3), x + int(r * 0.3), cy + int(r * 0.3)], fill=(255, 255, 255))


def draw_pumpkin(d: ImageDraw.ImageDraw, cx: int, cy: int, r: int = 58, glowing: bool = True, winking: bool = False) -> None:
    # Stem
    d.polygon([(cx - 8, cy - r + 6), (cx - 4, cy - r - 22), (cx + 12, cy - r - 18), (cx + 8, cy - r + 6)], fill=(68, 128, 52), outline=(42, 82, 32), width=2)
    # Ribs
    for dx, rx_scale in [(-int(r * 0.55), 0.65), (int(r * 0.55), 0.65), (-int(r * 0.28), 0.72), (int(r * 0.28), 0.72), (0, 0.78)]:
        rx = int(r * rx_scale)
        ry = int(r * 0.85)
        d.ellipse([cx + dx - rx, cy - ry, cx + dx + rx, cy + ry], fill=(248, 128, 28), outline=(175, 72, 12), width=3)
    # Face
    face_col = (255, 238, 95) if glowing else (65, 35, 18)
    # Left eye
    if winking:
        d.arc([cx - int(r * 0.52), cy - int(r * 0.32), cx - int(r * 0.14), cy - int(r * 0.04)], start=180, end=360, fill=face_col, width=5)
    else:
        d.polygon([(cx - int(r * 0.35), cy - int(r * 0.42)), (cx - int(r * 0.55), cy - int(r * 0.08)), (cx - int(r * 0.15), cy - int(r * 0.08))], fill=face_col)
    # Right eye
    d.polygon([(cx + int(r * 0.35), cy - int(r * 0.42)), (cx + int(r * 0.15), cy - int(r * 0.08)), (cx + int(r * 0.55), cy - int(r * 0.08))], fill=face_col)
    # Nose
    d.polygon([(cx, cy - int(r * 0.08)), (cx - 10, cy + int(r * 0.10)), (cx + 10, cy + int(r * 0.10))], fill=face_col)
    # Grinning mouth
    d.chord([cx - int(r * 0.62), cy - int(r * 0.05), cx + int(r * 0.62), cy + int(r * 0.62)], start=10, end=170, fill=face_col, outline=(145, 55, 10), width=2)
    # Cute pumpkin tooth
    d.rectangle([cx - 8, cy + int(r * 0.18), cx + 8, cy + int(r * 0.32)], fill=(248, 128, 28))


def render_story37_ticket() -> Path:
    """37. 藏在巧克力里的金奖券"""
    W, H = 480, 360
    panels = []
    for idx in range(4):
        im = make_xuan_paper(W, H, (58, 36, 92), (118, 68, 148), seed=370 + idx)
        d = ImageDraw.Draw(im)
        rng = random.Random(3700 + idx)
        for _ in range(28):
            sx, sy = rng.randint(15, W - 15), rng.randint(15, H - 15)
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 235, 130))

        if idx == 0:
            # Charlie holding a red-wrapped chocolate bar
            d.rectangle([140, 110, 340, 250], fill=(105, 52, 28), outline=(65, 28, 12), width=4)
            d.rectangle([140, 145, 340, 248], fill=(215, 45, 65), outline=(145, 22, 35), width=3)
            d.ellipse([205, 165, 275, 225], fill=(255, 215, 75))
        elif idx == 1:
            # Sparkling Golden Ticket gleaming inside peeled silver foil
            for r_glow in range(135, 75, -12):
                d.ellipse([240 - r_glow, 180 - r_glow, 240 + r_glow, 180 + r_glow], fill=(255, 225, 115))
            d.rectangle([115, 105, 365, 245], fill=(255, 212, 55), outline=(195, 138, 18), width=5)
            d.rectangle([130, 120, 350, 230], outline=(165, 110, 12), width=2)
        elif idx == 2:
            # Grandpa and Charlie dancing with joy in cozy bedroom
            d.rectangle([0, 245, W, H], fill=(145, 95, 62))
            for cx, cy, col in [(175, 195, (95, 155, 225)), (305, 215, (235, 95, 75))]:
                d.ellipse([cx - 24, cy - 55, cx + 24, cy - 7], fill=(252, 215, 188), outline=(75, 48, 35), width=2)
                d.polygon([(cx - 32, cy + 55), (cx - 22, cy - 5), (cx + 22, cy - 5), (cx + 32, cy + 55)], fill=col, outline=(65, 42, 30), width=2)
        else:
            # Candy maker in purple top hat at grand wrought-iron gates
            for gx in range(70, 420, 35):
                d.line([(gx, 75), (gx, 310)], fill=(45, 45, 55), width=4)
            # Purple top hat & coat
            px, py = 240, 215
            d.polygon([(px - 42, H), (px - 26, py - 10), (px + 26, py - 10), (px + 42, H)], fill=(138, 45, 165), outline=(68, 18, 88), width=3)
            d.ellipse([px - 24, py - 56, px + 24, py - 8], fill=(252, 218, 192), outline=(68, 18, 88), width=3)
            d.rectangle([px - 36, py - 62, px + 36, py - 52], fill=(118, 32, 145), outline=(55, 12, 72), width=2)
            d.rectangle([px - 24, py - 110, px + 24, py - 58], fill=(138, 45, 165), outline=(55, 12, 72), width=3)
            d.rectangle([px - 24, py - 72, px + 24, py - 60], fill=(255, 205, 55))
        panels.append(im)
    return build_grid(panels, BRAIN_DIR / "story37_grid.jpg")


def render_story38_waterfall() -> Path:
    """38. 巧克力瀑布与薄荷草地"""
    W, H = 480, 360
    panels = []
    for idx in range(4):
        im = make_xuan_paper(W, H, (255, 228, 238), (195, 245, 215), seed=380 + idx)
        d = ImageDraw.Draw(im)
        # Mint-green candy hills
        d.ellipse([-60, 145, 310, 320], fill=(98, 212, 145), outline=(58, 158, 98), width=3)
        d.ellipse([190, 150, 540, 320], fill=(82, 198, 132), outline=(58, 158, 98), width=3)
        # Melted chocolate river
        d.polygon([(140, 165), (330, 165), (440, H), (40, H)], fill=(112, 58, 32), outline=(78, 38, 18), width=3)
        for ry in range(195, H - 15, 32):
            d.arc([140, ry, 340, ry + 18], start=0, end=180, fill=(158, 92, 55), width=3)

        if idx == 0:
            # Candy Hall view with giant lollipops & candy canes
            draw_lollipop(d, 85, 225, 28)
            draw_lollipop(d, 395, 230, 30, (115, 205, 255), (255, 165, 215))
            draw_candy_cane(d, 135, 235, 75)
            draw_candy_cane(d, 345, 235, 75)
        elif idx == 1:
            # Giant cascading chocolate waterfall with creamy foam swirls
            d.rectangle([155, 0, 325, 235], fill=(118, 62, 34), outline=(78, 38, 18), width=3)
            for fx in range(160, 330, 32):
                d.ellipse([fx - 22, 210, fx + 22, 252], fill=(245, 225, 205), outline=(185, 135, 98), width=2)
        elif idx == 2:
            # Mint candy grass & rainbow candy fruit tree
            d.rectangle([225, 115, 255, 235], fill=(145, 85, 48), outline=(92, 52, 25), width=3)
            d.ellipse([155, 25, 325, 145], fill=(255, 145, 185), outline=(205, 85, 132), width=3)
            for cx, cy, col in [(195, 65, (255, 220, 65)), (245, 55, (95, 215, 255)), (285, 78, (135, 235, 115)), (215, 105, (255, 115, 95))]:
                d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=col, outline=(255, 255, 255), width=2)
        else:
            # Little helpers marching with candy canes
            for hx in (125, 240, 355):
                d.ellipse([hx - 20, 145, hx + 20, 185], fill=(255, 185, 135), outline=(95, 55, 35), width=2)
                d.ellipse([hx - 22, 128, hx + 22, 152], fill=(75, 175, 95), outline=(42, 112, 55), width=2)
                d.rectangle([hx - 22, 185, hx + 22, 245], fill=(235, 75, 95), outline=(145, 35, 52), width=2)
                draw_candy_cane(d, hx + 28, 245, 60)
        panels.append(im)
    return build_grid(panels, BRAIN_DIR / "story38_grid.jpg")


def render_story39_blueberry() -> Path:
    """39. 变蓝莓大球的魔法口香糖"""
    W, H = 480, 360
    panels = []
    for idx in range(4):
        im = make_xuan_paper(W, H, (232, 220, 255), (175, 195, 252), seed=390 + idx)
        d = ImageDraw.Draw(im)
        if idx == 0:
            # Invention machine bubbling with colorful foam
            d.rectangle([135, 115, 345, 285], fill=(185, 198, 218), outline=(85, 98, 122), width=4)
            for bx, by, br, col in [(185, 85, 24, (255, 135, 185)), (240, 68, 30, (125, 225, 255)), (295, 88, 22, (255, 225, 95))]:
                d.ellipse([bx - br, by - br, bx + br, by + br], fill=col, outline=(255, 255, 255), width=2)
            # Strip of magic chewing gum
            d.rectangle([195, 185, 285, 215], fill=(255, 165, 210), outline=(195, 85, 145), width=3)
        elif idx == 1:
            # Thought bubbles of tomato soup, roast beef, and blueberry pie
            for bx, by, col in [(120, 120, (245, 95, 75)), (240, 95, (185, 115, 68)), (360, 120, (98, 85, 215))]:
                d.ellipse([bx - 48, by - 38, bx + 48, by + 38], fill=(255, 252, 245), outline=(145, 135, 185), width=3)
                d.ellipse([bx - 28, by - 20, bx + 28, by + 20], fill=col)
            d.ellipse([205, 205, 275, 275], fill=(255, 215, 192), outline=(85, 55, 45), width=3)
        elif idx == 2:
            # Giant round violet-blue blueberry ball girl!
            d.ellipse([125, 65, 355, 295], fill=(88, 72, 205), outline=(48, 35, 135), width=4)
            d.ellipse([155, 95, 215, 145], fill=(135, 122, 238))
            d.ellipse([212, 42, 268, 92], fill=(115, 98, 225), outline=(48, 35, 135), width=3)
            # Little hands & feet sticking out
            d.ellipse([98, 165, 132, 195], fill=(115, 98, 225), outline=(48, 35, 135), width=3)
            d.ellipse([348, 165, 382, 195], fill=(115, 98, 225), outline=(48, 35, 135), width=3)
        else:
            # Rolling the giant blueberry ball across the floor
            d.rectangle([0, 265, W, H], fill=(215, 195, 235))
            d.ellipse([145, 75, 335, 265], fill=(88, 72, 205), outline=(48, 35, 135), width=4)
            for hx in (95, 385):
                d.ellipse([hx - 18, 185, hx + 18, 220], fill=(255, 185, 135), outline=(85, 52, 32), width=2)
                d.rectangle([hx - 18, 220, hx + 18, 268], fill=(235, 75, 95), outline=(145, 35, 52), width=2)
        panels.append(im)
    return build_grid(panels, BRAIN_DIR / "story39_grid.jpg")


def render_story40_elevator() -> Path:
    """40. 飞向云端的玻璃大电梯"""
    W, H = 480, 360
    panels = []
    for idx in range(4):
        im = make_xuan_paper(W, H, (135, 205, 252), (235, 248, 255), seed=400 + idx)
        d = ImageDraw.Draw(im)
        # Fluffy white clouds
        for cx, cy in [(85, 265), (240, 285), (395, 260), (140, 85), (355, 75)]:
            d.ellipse([cx - 55, cy - 28, cx + 55, cy + 28], fill=(255, 255, 255))
            d.ellipse([cx - 32, cy - 42, cx + 32, cy + 15], fill=(255, 255, 255))

        if idx in (0, 2):
            # Transparent Great Glass Elevator
            d.rectangle([155, 65, 325, 255], fill=(215, 242, 255), outline=(95, 145, 185), width=5)
            d.polygon([(155, 65), (240, 25), (325, 65)], fill=(195, 232, 252), outline=(95, 145, 185), width=4)
            if idx == 2:
                # Rainbow frosting jet stream below elevator
                rainbow_cols = [(255, 95, 115), (255, 185, 75), (255, 235, 85), (95, 215, 135), (95, 175, 255)]
                for i, rc in enumerate(rainbow_cols):
                    rx = 175 + i * 32
                    d.polygon([(rx - 14, 255), (rx + 14, 255), (rx + 24, H), (rx - 24, H)], fill=rc)
        elif idx == 1:
            # Hundreds of glowing colorful buttons inside glass elevator
            d.rectangle([65, 35, 415, 325], fill=(225, 245, 255), outline=(95, 145, 185), width=5)
            cols = [(255, 75, 95), (255, 195, 55), (85, 215, 125), (85, 165, 255), (215, 105, 245)]
            for r_i, by in enumerate(range(70, 295, 38)):
                for c_i, bx in enumerate(range(105, 390, 42)):
                    col = cols[(r_i + c_i) % len(cols)]
                    d.ellipse([bx - 13, by - 13, bx + 13, by + 13], fill=col, outline=(255, 255, 255), width=2)
        else:
            # Aerial view of gingerbread-house town below
            d.rectangle([0, 195, W, H], fill=(165, 222, 155))
            for hx in (95, 240, 385):
                d.rectangle([hx - 42, 215, hx + 42, 295], fill=(195, 125, 68), outline=(125, 72, 32), width=3)
                d.polygon([(hx - 52, 215), (hx, 165), (hx + 52, 215)], fill=(255, 250, 245), outline=(215, 165, 135), width=3)
        panels.append(im)
    return build_grid(panels, BRAIN_DIR / "story40_grid.jpg")


def render_story41_pumpkin() -> Path:
    """41. 会咧嘴笑的南瓜灯笼"""
    W, H = 480, 360
    panels = []
    for idx in range(4):
        im = make_xuan_paper(W, H, (38, 24, 68), (88, 48, 98), seed=410 + idx)
        d = ImageDraw.Draw(im)
        if idx == 0:
            # Big uncarved round orange pumpkin on autumn porch
            d.rectangle([0, 255, W, H], fill=(115, 72, 45))
            d.polygon([(232, 118), (236, 88), (252, 92), (248, 118)], fill=(68, 128, 52), width=2)
            d.ellipse([155, 115, 325, 275], fill=(248, 128, 28), outline=(175, 72, 12), width=4)
        elif idx == 1:
            # Carving triangle eyes and curved smiling mouth
            d.rectangle([0, 255, W, H], fill=(115, 72, 45))
            draw_pumpkin(d, 240, 195, 75, glowing=False)
        elif idx == 2:
            # Golden glowing Jack-o'-Lantern with warm aura
            for r_glow in range(135, 75, -10):
                d.ellipse([240 - r_glow, 195 - r_glow, 240 + r_glow, 195 + r_glow], fill=(165, 95, 45))
            d.rectangle([0, 265, W, H], fill=(95, 58, 38))
            draw_pumpkin(d, 240, 195, 78, glowing=True)
        else:
            # Winking Jack-o'-Lantern on windowsill under full moon
            d.ellipse([355, 35, 435, 115], fill=(255, 242, 165))
            d.rectangle([0, 255, W, H], fill=(85, 52, 38))
            draw_pumpkin(d, 215, 195, 75, glowing=True, winking=True)
        panels.append(im)
    return build_grid(panels, BRAIN_DIR / "story41_grid.jpg")


def render_story42_parade() -> Path:
    """42. 不给糖就捣蛋大游行"""
    W, H = 480, 360
    panels = []
    for idx in range(4):
        im = make_xuan_paper(W, H, (32, 22, 62), (78, 45, 95), seed=420 + idx)
        d = ImageDraw.Draw(im)
        # String of glowing fairy lights across top
        d.arc([-20, -25, W + 20, 85], start=0, end=180, fill=(95, 85, 115), width=2)
        for lx in range(45, W - 30, 55):
            d.ellipse([lx - 8, 42, lx + 8, 58], fill=(255, 195, 65))

        if idx == 0:
            # Kids in wizard cape, dinosaur suit, and superhero cape
            for kx, col, hat in [(125, (115, 65, 195), True), (240, (85, 195, 95), False), (355, (235, 65, 75), False)]:
                d.polygon([(kx - 36, 295), (kx - 20, 175), (kx + 20, 175), (kx + 36, 295)], fill=col, outline=(45, 25, 65), width=3)
                d.ellipse([kx - 22, 130, kx + 22, 174], fill=(255, 218, 192), outline=(45, 25, 65), width=2)
                if hat:
                    d.polygon([(kx - 34, 135), (kx, 72), (kx + 34, 135)], fill=(85, 42, 155), outline=(45, 22, 85), width=2)
        elif idx == 1:
            # Pumpkin candy buckets overflowing with treats
            draw_pumpkin(d, 165, 215, 58, glowing=True)
            draw_pumpkin(d, 315, 215, 58, glowing=True)
            d.arc([115, 125, 215, 215], start=180, end=360, fill=(45, 45, 55), width=4)
            d.arc([265, 125, 365, 215], start=180, end=360, fill=(45, 45, 55), width=4)
        elif idx == 2:
            # Plump platter of fruit candies, lollipops & chocolates
            d.ellipse([75, 165, 405, 315], fill=(255, 235, 195), outline=(195, 135, 65), width=4)
            for cx, cy, col in [(155, 225, (255, 95, 135)), (215, 205, (95, 205, 255)), (275, 235, (255, 205, 65)), (325, 215, (135, 225, 105)), (240, 255, (145, 82, 48))]:
                d.ellipse([cx - 22, cy - 16, cx + 22, cy + 16], fill=col, outline=(255, 255, 255), width=2)
        else:
            # Paper bats & glowing lantern street celebration
            d.ellipse([365, 65, 435, 135], fill=(255, 238, 145))
            for bx, by in [(125, 115), (245, 95), (315, 145)]:
                d.polygon([(bx, by), (bx - 32, by - 16), (bx - 18, by + 10), (bx, by + 4), (bx + 18, by + 10), (bx + 32, by - 16)], fill=(42, 32, 58))
            draw_pumpkin(d, 140, 265, 45, glowing=True)
            draw_pumpkin(d, 340, 265, 45, glowing=True)
        panels.append(im)
    return build_grid(panels, BRAIN_DIR / "story42_grid.jpg")


def render_story43_ghost() -> Path:
    """43. 胆小鬼幽灵找朋友"""
    W, H = 480, 360
    panels = []

    def draw_cute_ghost(d: ImageDraw.ImageDraw, gx: int, gy: int, rosy: bool = False) -> None:
        d.ellipse([gx - 52, gy - 68, gx + 52, gy + 28], fill=(250, 252, 255), outline=(145, 162, 195), width=3)
        d.polygon(
            [
                (gx - 52, gy - 15),
                (gx - 58, gy + 58),
                (gx - 28, gy + 42),
                (gx, gy + 60),
                (gx + 28, gy + 42),
                (gx + 58, gy + 58),
                (gx + 52, gy - 15),
            ],
            fill=(250, 252, 255),
            outline=(145, 162, 195),
            width=3,
        )
        d.ellipse([gx - 22, gy - 32, gx - 10, gy - 18], fill=(35, 40, 55))
        d.ellipse([gx + 10, gy - 32, gx + 22, gy - 18], fill=(35, 40, 55))
        if rosy:
            d.ellipse([gx - 36, gy - 16, gx - 18, gy - 4], fill=(255, 155, 175))
            d.ellipse([gx + 18, gy - 16, gx + 36, gy - 4], fill=(255, 155, 175))
        d.arc([gx - 14, gy - 16, gx + 14, gy + 4], start=0, end=180, fill=(35, 40, 55), width=3)

    for idx in range(4):
        im = make_xuan_paper(W, H, (48, 38, 82), (98, 72, 138), seed=430 + idx)
        d = ImageDraw.Draw(im)
        if idx == 0:
            # Cute shy ghost in cozy attic
            draw_cute_ghost(d, 240, 195, rosy=False)
        elif idx == 1:
            # Costume party with balloons & confetti
            for bx, by, col in [(95, 105, (255, 115, 155)), (385, 95, (115, 215, 255)), (145, 75, (255, 215, 75))]:
                d.ellipse([bx - 24, by - 30, bx + 24, by + 30], fill=col, outline=(255, 255, 255), width=2)
            draw_cute_ghost(d, 240, 205, rosy=True)
        elif idx == 2:
            # Glowing lollipop gift to the little ghost
            draw_cute_ghost(d, 205, 195, rosy=True)
            draw_lollipop(d, 315, 255, 34, (255, 95, 165), (255, 235, 95))
        else:
            # Rosy-cheeked ghost surrounded by happy friends
            draw_cute_ghost(d, 240, 185, rosy=True)
            draw_pumpkin(d, 105, 245, 42, glowing=True)
            draw_pumpkin(d, 375, 245, 42, glowing=True)
        panels.append(im)
    return build_grid(panels, BRAIN_DIR / "story43_grid.jpg")


def render_story44_broom() -> Path:
    """44. 小女巫的爆米花扫帚"""
    W, H = 480, 360
    panels = []
    for idx in range(4):
        im = make_xuan_paper(W, H, (28, 32, 72), (82, 58, 118), seed=440 + idx)
        d = ImageDraw.Draw(im)
        rng = random.Random(4400 + idx)
        # Crescent moon
        d.ellipse([365, 32, 435, 102], fill=(255, 242, 155))
        d.ellipse([385, 25, 445, 88], fill=(35, 36, 78))

        # Broomstick across sky
        d.line([(85, 195), (325, 175)], fill=(145, 92, 45), width=8)
        d.polygon([(85, 195), (35, 170), (28, 220)], fill=(215, 165, 65), outline=(135, 95, 32), width=2)

        # Popcorn puffs helper
        def draw_popcorn(px: int, py: int) -> None:
            for dx, dy in [(-6, -4), (6, -4), (0, 5), (-5, 4), (5, 4)]:
                d.ellipse([px + dx - 8, py + dy - 8, px + dx + 8, py + dy + 8], fill=(255, 242, 185), outline=(215, 155, 65), width=1)

        if idx == 0:
            # Little witch in pointed hat with black cat on broomstick
            wx, wy = 235, 155
            d.polygon([(wx - 35, wy - 25), (wx, wy - 85), (wx + 35, wy - 25)], fill=(95, 45, 155), outline=(45, 18, 78), width=3)
            d.ellipse([wx - 20, wy - 28, wx + 20, wy + 12], fill=(255, 218, 192), outline=(45, 18, 78), width=2)
            # Black cat
            d.ellipse([285, 148, 318, 178], fill=(35, 35, 42))
        elif idx == 1:
            # Broomstick tail popping out golden caramel popcorn clouds!
            for _ in range(18):
                draw_popcorn(rng.randint(35, 195), rng.randint(145, 265))
        elif idx == 2:
            # Owl on tree branch catching falling popcorn snowflakes
            d.line([(280, 265), (W, 245)], fill=(95, 62, 38), width=10)
            ox, oy = 355, 215
            d.ellipse([ox - 28, oy - 35, ox + 28, oy + 35], fill=(165, 115, 72), outline=(95, 62, 35), width=3)
            d.ellipse([ox - 16, oy - 18, ox - 4, oy - 6], fill=(255, 235, 95))
            d.ellipse([ox + 4, oy - 18, ox + 16, oy - 6], fill=(255, 235, 95))
            for _ in range(22):
                draw_popcorn(rng.randint(45, W - 45), rng.randint(65, 310))
        else:
            # Treehouse deck party with big bowl of warm caramel popcorn
            d.rectangle([60, 235, 420, 325], fill=(155, 102, 58), outline=(95, 58, 28), width=3)
            for _ in range(20):
                draw_popcorn(rng.randint(165, 315), rng.randint(175, 225))
            d.chord([145, 185, 335, 285], start=0, end=180, fill=(235, 75, 65), outline=(155, 35, 28), width=3)
        panels.append(im)
    return build_grid(panels, BRAIN_DIR / "story44_grid.jpg")


def main() -> None:
    grid_files = {
        37: render_story37_ticket(),
        38: render_story38_waterfall(),
        39: render_story39_blueberry(),
        40: render_story40_elevator(),
        41: render_story41_pumpkin(),
        42: render_story42_parade(),
        43: render_story43_ghost(),
        44: render_story44_broom(),
    }

    assets = {}
    for sid, gpath in grid_files.items():
        b_url, p_urls = extract_story_images(gpath, quality=80)
        assets[sid] = (b_url, p_urls)
        print(f"Story {sid}: banner={len(b_url)} chars, panels={[len(u) for u in p_urls]}")

    s37_b, s37_p = assets[37]
    s38_b, s38_p = assets[38]
    s39_b, s39_p = assets[39]
    s40_b, s40_p = assets[40]
    s41_b, s41_p = assets[41]
    s42_b, s42_p = assets[42]
    s43_b, s43_p = assets[43]
    s44_b, s44_p = assets[44]

    new_stories_js = f"""  }},
  {{
    id: 37,
    category: "wonka",
    icon: "🎫",
    title: "37. 藏在巧克力里的金奖券",
    titleText: "藏在巧克力里的金奖券",
    titlePinyin: "cáng zài qiǎo kè lì lǐ de jīn jiǎng quàn",
    titleRuby: `<span class="word-group"><ruby>藏<rt>cáng</rt></ruby><ruby>在<rt>zài</rt></ruby></span><span class="word-group"><ruby>巧<rt>qiǎo</rt></ruby><ruby>克<rt>kè</rt></ruby><ruby>力<rt>lì</rt></ruby><ruby>里<rt>lǐ</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>金<rt>jīn</rt></ruby><ruby>奖<rt>jiǎng</rt></ruby><ruby>券<rt>quàn</rt></ruby></span>`,
    titleEn: "The Golden Ticket Hidden in the Chocolate Bar",
    titleEnHtml: `<span class="en-word-group">The Golden Ticket</span> <span class="en-word-group">Hidden in</span> <span class="en-word-group">the Chocolate Bar</span>`,
    subtitle: "巧克力工厂 第1集 · 4 句 · 奇幻童话",
    bannerImg: "{s37_b}",
    sentences: [
      {{
        img: "{s37_p[0]}",
        text: "小男孩查理用攒下的零花钱，买了一块香甜的奶油巧克力。",
        ruby: `<span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>男<rt>nán</rt></ruby><ruby>孩<rt>hái</rt></ruby><ruby>查<rt>chá</rt></ruby><ruby>理<rt>lǐ</rt></ruby></span><span class="word-group"><ruby>用<rt>yòng</rt></ruby><ruby>攒<rt>zǎn</rt></ruby><ruby>下<rt>xià</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>零<rt>líng</rt></ruby><ruby>花<rt>huā</rt></ruby><ruby>钱<rt>qián</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>买<rt>mǎi</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>一<rt>yí</rt></ruby><ruby>块<rt>kuài</rt></ruby></span><span class="word-group"><ruby>香<rt>xiāng</rt></ruby><ruby>甜<rt>tián</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>奶<rt>nǎi</rt></ruby><ruby>油<rt>yóu</rt></ruby><ruby>巧<rt>qiǎo</rt></ruby><ruby>克<rt>kè</rt></ruby><ruby>力<rt>lì</rt></ruby></span><span class="punct">。</span>`,
        en: `Little boy Charlie used his saved pocket money to buy a sweet creamy chocolate bar.`,
        enHtml: `<span class="en-word-group">Little boy Charlie</span> <span class="en-word-group">used his saved pocket money</span> <span class="en-word-group">to buy a sweet</span> <span class="en-word-group">creamy chocolate bar.</span>`
      }},
      {{
        img: "{s37_p[1]}",
        text: "他轻轻剥开银色锡纸，里面竟然闪耀着一张金灿灿的奖券！",
        ruby: `<span class="word-group"><ruby>他<rt>tā</rt></ruby><ruby>轻<rt>qīng</rt></ruby><ruby>轻<rt>qīng</rt></ruby><ruby>剥<rt>bāo</rt></ruby><ruby>开<rt>kāi</rt></ruby></span><span class="word-group"><ruby>银<rt>yín</rt></ruby><ruby>色<rt>sè</rt></ruby><ruby>锡<rt>xī</rt></ruby><ruby>纸<rt>zhǐ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>里<rt>lǐ</rt></ruby><ruby>面<rt>miàn</rt></ruby><ruby>竟<rt>jìng</rt></ruby><ruby>然<rt>rán</rt></ruby></span><span class="word-group"><ruby>闪<rt>shǎn</rt></ruby><ruby>耀<rt>yào</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>张<rt>zhāng</rt></ruby></span><span class="word-group"><ruby>金<rt>jīn</rt></ruby><ruby>灿<rt>càn</rt></ruby><ruby>灿<rt>càn</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>奖<rt>jiǎng</rt></ruby><ruby>券<rt>quàn</rt></ruby></span><span class="punct">！</span>`,
        en: `He gently peeled back the silver foil, and inside gleamed a sparkling Golden Ticket!`,
        enHtml: `<span class="en-word-group">He gently peeled back</span> <span class="en-word-group">the silver foil,</span> <span class="en-word-group">and inside gleamed</span> <span class="en-word-group">a sparkling Golden Ticket!</span>`
      }},
      {{
        img: "{s37_p[2]}",
        text: "爷爷激动得从床上跳起来，拉着查理在房间里开心地跳舞！",
        ruby: `<span class="word-group"><ruby>爷<rt>yé</rt></ruby><ruby>爷<rt>ye</rt></ruby></span><span class="word-group"><ruby>激<rt>jī</rt></ruby><ruby>动<rt>dòng</rt></ruby><ruby>得<rt>de</rt></ruby></span><span class="word-group"><ruby>从<rt>cóng</rt></ruby><ruby>床<rt>chuáng</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>跳<rt>tiào</rt></ruby><ruby>起<rt>qǐ</rt></ruby><ruby>来<rt>lái</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>拉<rt>lā</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>查<rt>chá</rt></ruby><ruby>理<rt>lǐ</rt></ruby></span><span class="word-group"><ruby>在<rt>zài</rt></ruby><ruby>房<rt>fáng</rt></ruby><ruby>间<rt>jiān</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="word-group"><ruby>开<rt>kāi</rt></ruby><ruby>心<rt>xīn</rt></ruby><ruby>地<rt>de</rt></ruby><ruby>跳<rt>tiào</rt></ruby><ruby>舞<rt>wǔ</rt></ruby></span><span class="punct">！</span>`,
        en: `Grandpa jumped out of bed with excitement and danced happily around the room with Charlie!`,
        enHtml: `<span class="en-word-group">Grandpa jumped out of bed</span> <span class="en-word-group">with excitement</span> <span class="en-word-group">and danced happily</span> <span class="en-word-group">around the room with Charlie!</span>`
      }},
      {{
        img: "{s37_p[3]}",
        text: "戴着紫色高礼帽的糖果厂长，在铸铁大门前热情地欢迎他们！",
        ruby: `<span class="word-group"><ruby>戴<rt>dài</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>紫<rt>zǐ</rt></ruby><ruby>色<rt>sè</rt></ruby></span><span class="word-group"><ruby>高<rt>gāo</rt></ruby><ruby>礼<rt>lǐ</rt></ruby><ruby>帽<rt>mào</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>糖<rt>táng</rt></ruby><ruby>果<rt>guǒ</rt></ruby><ruby>厂<rt>chǎng</rt></ruby><ruby>长<rt>zhǎng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>在<rt>zài</rt></ruby><ruby>铸<rt>zhù</rt></ruby><ruby>铁<rt>tiě</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>门<rt>mén</rt></ruby><ruby>前<rt>qián</rt></ruby></span><span class="word-group"><ruby>热<rt>rè</rt></ruby><ruby>情<rt>qíng</rt></ruby><ruby>地<rt>de</rt></ruby><ruby>欢<rt>huān</rt></ruby><ruby>迎<rt>yíng</rt></ruby><ruby>他<rt>tā</rt></ruby><ruby>们<rt>men</rt></ruby></span><span class="punct">！</span>`,
        en: `Wearing a purple top hat, the candy factory owner warmly welcomed them at the iron gates!`,
        enHtml: `<span class="en-word-group">Wearing a purple top hat,</span> <span class="en-word-group">the candy factory owner</span> <span class="en-word-group">warmly welcomed them</span> <span class="en-word-group">at the iron gates!</span>`
      }}
    ],
    vocab: [
      {{ hz: "零花钱", py: "líng huā qián", en: "pocket money" }},
      {{ hz: "金奖券", py: "jīn jiǎng quàn", en: "Golden Ticket" }},
      {{ hz: "闪耀", py: "shǎn yào", en: "gleam and sparkle" }},
      {{ hz: "高礼帽", py: "gāo lǐ mào", en: "top hat" }}
    ]
  }},
  {{
    id: 38,
    category: "wonka",
    icon: "🍫",
    title: "38. 巧克力瀑布与薄荷草地",
    titleText: "巧克力瀑布与薄荷草地",
    titlePinyin: "qiǎo kè lì pù bù yǔ bò he cǎo dì",
    titleRuby: `<span class="word-group"><ruby>巧<rt>qiǎo</rt></ruby><ruby>克<rt>kè</rt></ruby><ruby>力<rt>lì</rt></ruby></span><span class="word-group"><ruby>瀑<rt>pù</rt></ruby><ruby>布<rt>bù</rt></ruby></span><span class="word-group"><ruby>与<rt>yǔ</rt></ruby></span><span class="word-group"><ruby>薄<rt>bò</rt></ruby><ruby>荷<rt>he</rt></ruby></span><span class="word-group"><ruby>草<rt>cǎo</rt></ruby><ruby>地<rt>dì</rt></ruby></span>`,
    titleEn: "The Chocolate Waterfall and Mint Meadow",
    titleEnHtml: `<span class="en-word-group">The Chocolate Waterfall</span> <span class="en-word-group">and</span> <span class="en-word-group">Mint Meadow</span>`,
    subtitle: "巧克力工厂 第2集 · 4 句 · 奇幻童话",
    bannerImg: "{s38_b}",
    sentences: [
      {{
        img: "{s38_p[0]}",
        text: "推开糖果大厅的大门，眼前是一条哗啦啦流淌的热巧克力河！",
        ruby: `<span class="word-group"><ruby>推<rt>tuī</rt></ruby><ruby>开<rt>kāi</rt></ruby></span><span class="word-group"><ruby>糖<rt>táng</rt></ruby><ruby>果<rt>guǒ</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>厅<rt>tīng</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>门<rt>mén</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>眼<rt>yǎn</rt></ruby><ruby>前<rt>qián</rt></ruby><ruby>是<rt>shì</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>条<rt>tiáo</rt></ruby></span><span class="word-group"><ruby>哗<rt>huā</rt></ruby><ruby>啦<rt>lā</rt></ruby><ruby>啦<rt>lā</rt></ruby><ruby>流<rt>liú</rt></ruby><ruby>淌<rt>tǎng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>热<rt>rè</rt></ruby><ruby>巧<rt>qiǎo</rt></ruby><ruby>克<rt>kè</rt></ruby><ruby>力<rt>lì</rt></ruby><ruby>河<rt>hé</rt></ruby></span><span class="punct">！</span>`,
        en: `Pushing open the doors to the Candy Hall, a warm river of melted chocolate rushed before their eyes!`,
        enHtml: `<span class="en-word-group">Pushing open the doors</span> <span class="en-word-group">to the Candy Hall,</span> <span class="en-word-group">a warm river of melted chocolate</span> <span class="en-word-group">rushed before their eyes!</span>`
      }},
      {{
        img: "{s38_p[1]}",
        text: "巨大的巧克力瀑布从高处冲下来，把巧克力和得又香又滑。",
        ruby: `<span class="word-group"><ruby>巨<rt>jù</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>巧<rt>qiǎo</rt></ruby><ruby>克<rt>kè</rt></ruby><ruby>力<rt>lì</rt></ruby><ruby>瀑<rt>pù</rt></ruby><ruby>布<rt>bù</rt></ruby></span><span class="word-group"><ruby>从<rt>cóng</rt></ruby><ruby>高<rt>gāo</rt></ruby><ruby>处<rt>chù</rt></ruby><ruby>冲<rt>chōng</rt></ruby><ruby>下<rt>xià</rt></ruby><ruby>来<rt>lái</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>把<rt>bǎ</rt></ruby><ruby>巧<rt>qiǎo</rt></ruby><ruby>克<rt>kè</rt></ruby><ruby>力<rt>lì</rt></ruby></span><span class="word-group"><ruby>和<rt>huò</rt></ruby><ruby>得<rt>de</rt></ruby><ruby>又<rt>yòu</rt></ruby><ruby>香<rt>xiāng</rt></ruby><ruby>又<rt>yòu</rt></ruby><ruby>滑<rt>huá</rt></ruby></span><span class="punct">。</span>`,
        en: `A giant chocolate waterfall cascaded from high above, churning the chocolate rich and smooth.`,
        enHtml: `<span class="en-word-group">A giant chocolate waterfall</span> <span class="en-word-group">cascaded from high above,</span> <span class="en-word-group">churning the chocolate</span> <span class="en-word-group">rich and smooth.</span>`
      }},
      {{
        img: "{s38_p[2]}",
        text: "河岸上的青草全是薄荷糖做的，连树上的果子都是彩虹硬糖！",
        ruby: `<span class="word-group"><ruby>河<rt>hé</rt></ruby><ruby>岸<rt>àn</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>青<rt>qīng</rt></ruby><ruby>草<rt>cǎo</rt></ruby></span><span class="word-group"><ruby>全<rt>quán</rt></ruby><ruby>是<rt>shì</rt></ruby><ruby>薄<rt>bò</rt></ruby><ruby>荷<rt>he</rt></ruby><ruby>糖<rt>táng</rt></ruby><ruby>做<rt>zuò</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>连<rt>lián</rt></ruby><ruby>树<rt>shù</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>果<rt>guǒ</rt></ruby><ruby>子<rt>zi</rt></ruby></span><span class="word-group"><ruby>都<rt>dōu</rt></ruby><ruby>是<rt>shì</rt></ruby><ruby>彩<rt>cǎi</rt></ruby><ruby>虹<rt>hóng</rt></ruby><ruby>硬<rt>yìng</rt></ruby><ruby>糖<rt>táng</rt></ruby></span><span class="punct">！</span>`,
        en: `The grass along the riverbank was made of mint candy, and even the fruit on the trees were rainbow hard candies!`,
        enHtml: `<span class="en-word-group">The grass along the riverbank</span> <span class="en-word-group">was made of mint candy,</span> <span class="en-word-group">and even the fruit on the trees</span> <span class="en-word-group">were rainbow hard candies!</span>`
      }},
      {{
        img: "{s38_p[3]}",
        text: "快乐的小矮人们排着队，一边摇晃拐杖糖一边唱着有趣的歌！",
        ruby: `<span class="word-group"><ruby>快<rt>kuài</rt></ruby><ruby>乐<rt>lè</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>矮<rt>ǎi</rt></ruby><ruby>人<rt>rén</rt></ruby><ruby>们<rt>men</rt></ruby></span><span class="word-group"><ruby>排<rt>pái</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>队<rt>duì</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>边<rt>biān</rt></ruby><ruby>摇<rt>yáo</rt></ruby><ruby>晃<rt>huàng</rt></ruby><ruby>拐<rt>guǎi</rt></ruby><ruby>杖<rt>zhàng</rt></ruby><ruby>糖<rt>táng</rt></ruby></span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>边<rt>biān</rt></ruby><ruby>唱<rt>chàng</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>有<rt>yǒu</rt></ruby><ruby>趣<rt>qù</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>歌<rt>gē</rt></ruby></span><span class="punct">！</span>`,
        en: `Cheerful little helpers marched in a row, twirling candy canes and singing funny songs!`,
        enHtml: `<span class="en-word-group">Cheerful little helpers</span> <span class="en-word-group">marched in a row,</span> <span class="en-word-group">twirling candy canes</span> <span class="en-word-group">and singing funny songs!</span>`
      }}
    ],
    vocab: [
      {{ hz: "瀑布", py: "pù bù", en: "waterfall" }},
      {{ hz: "薄荷糖", py: "bò he táng", en: "mint candy" }},
      {{ hz: "河岸", py: "hé àn", en: "riverbank" }},
      {{ hz: "拐杖糖", py: "guǎi zhàng táng", en: "candy cane" }}
    ]
  }},
  {{
    id: 39,
    category: "wonka",
    icon: "🫐",
    title: "39. 变蓝莓大球的魔法口香糖",
    titleText: "变蓝莓大球的魔法口香糖",
    titlePinyin: "biàn lán méi dà qiú de mó fǎ kǒu xiāng táng",
    titleRuby: `<span class="word-group"><ruby>变<rt>biàn</rt></ruby><ruby>蓝<rt>lán</rt></ruby><ruby>莓<rt>méi</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>球<rt>qiú</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>魔<rt>mó</rt></ruby><ruby>法<rt>fǎ</rt></ruby></span><span class="word-group"><ruby>口<rt>kǒu</rt></ruby><ruby>香<rt>xiāng</rt></ruby><ruby>糖<rt>táng</rt></ruby></span>`,
    titleEn: "The Magic Chewing Gum That Turns You into a Giant Blueberry",
    titleEnHtml: `<span class="en-word-group">The Magic Chewing Gum</span> <span class="en-word-group">That Turns You into</span> <span class="en-word-group">a Giant Blueberry</span>`,
    subtitle: "巧克力工厂 第3集 · 4 句 · 奇幻童话",
    bannerImg: "{s39_b}",
    sentences: [
      {{
        img: "{s39_p[0]}",
        text: "发明室的机器冒着彩色泡泡，造出了一片神奇的三餐口香糖。",
        ruby: `<span class="word-group"><ruby>发<rt>fā</rt></ruby><ruby>明<rt>míng</rt></ruby><ruby>室<rt>shì</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>机<rt>jī</rt></ruby><ruby>器<rt>qì</rt></ruby></span><span class="word-group"><ruby>冒<rt>mào</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>彩<rt>cǎi</rt></ruby><ruby>色<rt>sè</rt></ruby><ruby>泡<rt>pào</rt></ruby><ruby>泡<rt>pao</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>造<rt>zào</rt></ruby><ruby>出<rt>chū</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>一<rt>yí</rt></ruby><ruby>片<rt>piàn</rt></ruby></span><span class="word-group"><ruby>神<rt>shén</rt></ruby><ruby>奇<rt>qí</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>三<rt>sān</rt></ruby><ruby>餐<rt>cān</rt></ruby><ruby>口<rt>kǒu</rt></ruby><ruby>香<rt>xiāng</rt></ruby><ruby>糖<rt>táng</rt></ruby></span><span class="punct">。</span>`,
        en: `The machine in the Invention Room bubbled with colorful foam and produced a magical three-course-meal chewing gum.`,
        enHtml: `<span class="en-word-group">The machine in the Invention Room</span> <span class="en-word-group">bubbled with colorful foam</span> <span class="en-word-group">and produced a magical</span> <span class="en-word-group">three-course-meal chewing gum.</span>`
      }},
      {{
        img: "{s39_p[1]}",
        text: "调皮的女孩刚嚼了三口，尝到了番茄汤、烤牛肉和蓝莓派的味道！",
        ruby: `<span class="word-group"><ruby>调<rt>tiáo</rt></ruby><ruby>皮<rt>pí</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>女<rt>nǚ</rt></ruby><ruby>孩<rt>hái</rt></ruby></span><span class="word-group"><ruby>刚<rt>gāng</rt></ruby><ruby>嚼<rt>jiáo</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>三<rt>sān</rt></ruby><ruby>口<rt>kǒu</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>尝<rt>cháng</rt></ruby><ruby>到<rt>dào</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>番<rt>fān</rt></ruby><ruby>茄<rt>qié</rt></ruby><ruby>汤<rt>tāng</rt></ruby></span><span class="punct">、</span><span class="word-group"><ruby>烤<rt>kǎo</rt></ruby><ruby>牛<rt>niú</rt></ruby><ruby>肉<rt>ròu</rt></ruby></span><span class="word-group"><ruby>和<rt>hé</rt></ruby><ruby>蓝<rt>lán</rt></ruby><ruby>莓<rt>méi</rt></ruby><ruby>派<rt>pài</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>味<rt>wèi</rt></ruby><ruby>道<rt>dao</rt></ruby></span><span class="punct">！</span>`,
        en: `After chewing just three times, the cheeky girl tasted tomato soup, roast beef, and blueberry pie!`,
        enHtml: `<span class="en-word-group">After chewing just three times,</span> <span class="en-word-group">the cheeky girl tasted</span> <span class="en-word-group">tomato soup, roast beef,</span> <span class="en-word-group">and blueberry pie!</span>`
      }},
      {{
        img: "{s39_p[2]}",
        text: "突然她的鼻子变成了紫蓝色，肚子咕噜噜鼓成了一个大蓝莓球！",
        ruby: `<span class="word-group"><ruby>突<rt>tū</rt></ruby><ruby>然<rt>rán</rt></ruby><ruby>她<rt>tā</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>鼻<rt>bí</rt></ruby><ruby>子<rt>zi</rt></ruby></span><span class="word-group"><ruby>变<rt>biàn</rt></ruby><ruby>成<rt>chéng</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>紫<rt>zǐ</rt></ruby><ruby>蓝<rt>lán</rt></ruby><ruby>色<rt>sè</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>肚<rt>dù</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>咕<rt>gū</rt></ruby><ruby>噜<rt>lū</rt></ruby><ruby>噜<rt>lū</rt></ruby></span><span class="word-group"><ruby>鼓<rt>gǔ</rt></ruby><ruby>成<rt>chéng</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>一<rt>yí</rt></ruby><ruby>个<rt>gè</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>蓝<rt>lán</rt></ruby><ruby>莓<rt>méi</rt></ruby><ruby>球<rt>qiú</rt></ruby></span><span class="punct">！</span>`,
        en: `Suddenly her nose turned violet-blue, and her tummy puffed up into a giant blueberry ball!`,
        enHtml: `<span class="en-word-group">Suddenly her nose</span> <span class="en-word-group">turned violet-blue,</span> <span class="en-word-group">and her tummy puffed up</span> <span class="en-word-group">into a giant blueberry ball!</span>`
      }},
      {{
        img: "{s39_p[3]}",
        text: "小矮人们推着圆滚滚的蓝莓球去果汁房，逗得大家哈哈大笑！",
        ruby: `<span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>矮<rt>ǎi</rt></ruby><ruby>人<rt>rén</rt></ruby><ruby>们<rt>men</rt></ruby></span><span class="word-group"><ruby>推<rt>tuī</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>圆<rt>yuán</rt></ruby><ruby>滚<rt>gǔn</rt></ruby><ruby>滚<rt>gǔn</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>蓝<rt>lán</rt></ruby><ruby>莓<rt>méi</rt></ruby><ruby>球<rt>qiú</rt></ruby></span><span class="word-group"><ruby>去<rt>qù</rt></ruby><ruby>果<rt>guǒ</rt></ruby><ruby>汁<rt>zhī</rt></ruby><ruby>房<rt>fáng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>逗<rt>dòu</rt></ruby><ruby>得<rt>de</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>家<rt>jiā</rt></ruby><ruby>哈<rt>hā</rt></ruby><ruby>哈<rt>hā</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>笑<rt>xiào</rt></ruby></span><span class="punct">！</span>`,
        en: `The little helpers rolled the round blueberry ball to the Juicing Room, making everyone laugh out loud!`,
        enHtml: `<span class="en-word-group">The little helpers rolled</span> <span class="en-word-group">the round blueberry ball</span> <span class="en-word-group">to the Juicing Room,</span> <span class="en-word-group">making everyone laugh out loud!</span>`
      }}
    ],
    vocab: [
      {{ hz: "发明室", py: "fā míng shì", en: "invention room" }},
      {{ hz: "口香糖", py: "kǒu xiāng táng", en: "chewing gum" }},
      {{ hz: "蓝莓派", py: "lán méi pài", en: "blueberry pie" }},
      {{ hz: "圆滚滚", py: "yuán gǔn gǔn", en: "plump and round" }}
    ]
  }},
  {{
    id: 40,
    category: "wonka",
    icon: "🛗",
    title: "40. 飞向云端的玻璃大电梯",
    titleText: "飞向云端的玻璃大电梯",
    titlePinyin: "fēi xiàng yún duān de bō li dà diàn tī",
    titleRuby: `<span class="word-group"><ruby>飞<rt>fēi</rt></ruby><ruby>向<rt>xiàng</rt></ruby><ruby>云<rt>yún</rt></ruby><ruby>端<rt>duān</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>玻<rt>bō</rt></ruby><ruby>璃<rt>li</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>电<rt>diàn</rt></ruby><ruby>梯<rt>tī</rt></ruby></span>`,
    titleEn: "The Great Glass Elevator Soaring into the Clouds",
    titleEnHtml: `<span class="en-word-group">The Great Glass Elevator</span> <span class="en-word-group">Soaring into</span> <span class="en-word-group">the Clouds</span>`,
    subtitle: "巧克力工厂 第4集 · 4 句 · 奇幻童话",
    bannerImg: "{s40_b}",
    sentences: [
      {{
        img: "{s40_p[0]}",
        text: "善良的查理通过了所有考验，和厂长一起走进透明的玻璃电梯。",
        ruby: `<span class="word-group"><ruby>善<rt>shàn</rt></ruby><ruby>良<rt>liáng</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>查<rt>chá</rt></ruby><ruby>理<rt>lǐ</rt></ruby></span><span class="word-group"><ruby>通<rt>tōng</rt></ruby><ruby>过<rt>guò</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>所<rt>suǒ</rt></ruby><ruby>有<rt>yǒu</rt></ruby><ruby>考<rt>kǎo</rt></ruby><ruby>验<rt>yàn</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>和<rt>hé</rt></ruby><ruby>厂<rt>chǎng</rt></ruby><ruby>长<rt>zhǎng</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>起<rt>qǐ</rt></ruby><ruby>走<rt>zǒu</rt></ruby><ruby>进<rt>jìn</rt></ruby></span><span class="word-group"><ruby>透<rt>tòu</rt></ruby><ruby>明<rt>míng</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>玻<rt>bō</rt></ruby><ruby>璃<rt>li</rt></ruby><ruby>电<rt>diàn</rt></ruby><ruby>梯<rt>tī</rt></ruby></span><span class="punct">。</span>`,
        en: `Kind-hearted Charlie passed every test and stepped into the transparent glass elevator with the factory owner.`,
        enHtml: `<span class="en-word-group">Kind-hearted Charlie</span> <span class="en-word-group">passed every test</span> <span class="en-word-group">and stepped into</span> <span class="en-word-group">the transparent glass elevator</span> <span class="en-word-group">with the factory owner.</span>`
      }},
      {{
        img: "{s40_p[1]}",
        text: "电梯上有成百上千个发光按钮，可以飞往工厂的任何一个角落！",
        ruby: `<span class="word-group"><ruby>电<rt>diàn</rt></ruby><ruby>梯<rt>tī</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>有<rt>yǒu</rt></ruby></span><span class="word-group"><ruby>成<rt>chéng</rt></ruby><ruby>百<rt>bǎi</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>千<rt>qiān</rt></ruby><ruby>个<rt>gè</rt></ruby><ruby>发<rt>fā</rt></ruby><ruby>光<rt>guāng</rt></ruby><ruby>按<rt>àn</rt></ruby><ruby>钮<rt>niǔ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>可<rt>kě</rt></ruby><ruby>以<rt>yǐ</rt></ruby><ruby>飞<rt>fēi</rt></ruby><ruby>往<rt>wǎng</rt></ruby><ruby>工<rt>gōng</rt></ruby><ruby>厂<rt>chǎng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>任<rt>rèn</rt></ruby><ruby>何<rt>hé</rt></ruby><ruby>一<rt>yí</rt></ruby><ruby>个<rt>gè</rt></ruby><ruby>角<rt>jiǎo</rt></ruby><ruby>落<rt>luò</rt></ruby></span><span class="punct">！</span>`,
        en: `The elevator had hundreds of glowing buttons that could fly to any corner of the factory!`,
        enHtml: `<span class="en-word-group">The elevator had</span> <span class="en-word-group">hundreds of glowing buttons</span> <span class="en-word-group">that could fly to</span> <span class="en-word-group">any corner of the factory!</span>`
      }},
      {{
        img: "{s40_p[2]}",
        text: "查理按下红色按钮，玻璃电梯喷出彩虹糖霜，直冲上蓝天白云！",
        ruby: `<span class="word-group"><ruby>查<rt>chá</rt></ruby><ruby>理<rt>lǐ</rt></ruby><ruby>按<rt>àn</rt></ruby><ruby>下<rt>xià</rt></ruby><ruby>红<rt>hóng</rt></ruby><ruby>色<rt>sè</rt></ruby><ruby>按<rt>àn</rt></ruby><ruby>钮<rt>niǔ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>玻<rt>bō</rt></ruby><ruby>璃<rt>li</rt></ruby><ruby>电<rt>diàn</rt></ruby><ruby>梯<rt>tī</rt></ruby></span><span class="word-group"><ruby>喷<rt>pēn</rt></ruby><ruby>出<rt>chū</rt></ruby><ruby>彩<rt>cǎi</rt></ruby><ruby>虹<rt>hóng</rt></ruby><ruby>糖<rt>táng</rt></ruby><ruby>霜<rt>shuāng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>直<rt>zhí</rt></ruby><ruby>冲<rt>chōng</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>蓝<rt>lán</rt></ruby><ruby>天<rt>tiān</rt></ruby><ruby>白<rt>bái</rt></ruby><ruby>云<rt>yún</rt></ruby></span><span class="punct">！</span>`,
        en: `Charlie pressed the red button, and the glass elevator blasted rainbow frosting straight up into the blue sky and clouds!`,
        enHtml: `<span class="en-word-group">Charlie pressed the red button,</span> <span class="en-word-group">and the glass elevator</span> <span class="en-word-group">blasted rainbow frosting</span> <span class="en-word-group">straight up into the blue sky and clouds!</span>`
      }},
      {{
        img: "{s40_p[3]}",
        text: "从高空往下看，整座小镇像涂满了奶油的姜饼屋一样美丽！",
        ruby: `<span class="word-group"><ruby>从<rt>cóng</rt></ruby><ruby>高<rt>gāo</rt></ruby><ruby>空<rt>kōng</rt></ruby><ruby>往<rt>wǎng</rt></ruby><ruby>下<rt>xià</rt></ruby><ruby>看<rt>kàn</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>整<rt>zhěng</rt></ruby><ruby>座<rt>zuò</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>镇<rt>zhèn</rt></ruby></span><span class="word-group"><ruby>像<rt>xiàng</rt></ruby><ruby>涂<rt>tú</rt></ruby><ruby>满<rt>mǎn</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>奶<rt>nǎi</rt></ruby><ruby>油<rt>yóu</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>姜<rt>jiāng</rt></ruby><ruby>饼<rt>bǐng</rt></ruby><ruby>屋<rt>wū</rt></ruby></span><span class="word-group"><ruby>一<rt>yí</rt></ruby><ruby>样<rt>yàng</rt></ruby><ruby>美<rt>měi</rt></ruby><ruby>丽<rt>lì</rt></ruby></span><span class="punct">！</span>`,
        en: `Looking down from high in the sky, the whole town looked as beautiful as gingerbread houses frosted with cream!`,
        enHtml: `<span class="en-word-group">Looking down from high in the sky,</span> <span class="en-word-group">the whole town looked</span> <span class="en-word-group">as beautiful as gingerbread houses</span> <span class="en-word-group">frosted with cream!</span>`
      }}
    ],
    vocab: [
      {{ hz: "考验", py: "kǎo yàn", en: "test and trial" }},
      {{ hz: "透明", py: "tòu míng", en: "transparent" }},
      {{ hz: "按钮", py: "àn niǔ", en: "button" }},
      {{ hz: "姜饼屋", py: "jiāng bǐng wū", en: "gingerbread house" }}
    ]
  }},
  {{
    id: 41,
    category: "halloween",
    icon: "🎃",
    title: "41. 会咧嘴笑的南瓜灯笼",
    titleText: "会咧嘴笑的南瓜灯笼",
    titlePinyin: "huì liě zuǐ xiào de nán guā dēng long",
    titleRuby: `<span class="word-group"><ruby>会<rt>huì</rt></ruby><ruby>咧<rt>liě</rt></ruby><ruby>嘴<rt>zuǐ</rt></ruby><ruby>笑<rt>xiào</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>南<rt>nán</rt></ruby><ruby>瓜<rt>guā</rt></ruby></span><span class="word-group"><ruby>灯<rt>dēng</rt></ruby><ruby>笼<rt>long</rt></ruby></span>`,
    titleEn: "The Grinning Jack-o'-Lantern",
    titleEnHtml: `<span class="en-word-group">The Grinning</span> <span class="en-word-group">Jack-o'-Lantern</span>`,
    subtitle: "搞怪万圣节 第1集 · 4 句 · 节日探险",
    bannerImg: "{s41_b}",
    sentences: [
      {{
        img: "{s41_p[0]}",
        text: "万圣节的傍晚，小乐和妹妹抱回了一个圆滚滚的大橘色南瓜。",
        ruby: `<span class="word-group"><ruby>万<rt>wàn</rt></ruby><ruby>圣<rt>shèng</rt></ruby><ruby>节<rt>jié</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>傍<rt>bàng</rt></ruby><ruby>晚<rt>wǎn</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>乐<rt>lè</rt></ruby><ruby>和<rt>hé</rt></ruby><ruby>妹<rt>mèi</rt></ruby><ruby>妹<rt>mei</rt></ruby></span><span class="word-group"><ruby>抱<rt>bào</rt></ruby><ruby>回<rt>huí</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>一<rt>yí</rt></ruby><ruby>个<rt>gè</rt></ruby></span><span class="word-group"><ruby>圆<rt>yuán</rt></ruby><ruby>滚<rt>gǔn</rt></ruby><ruby>滚<rt>gǔn</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>橘<rt>jú</rt></ruby><ruby>色<rt>sè</rt></ruby><ruby>南<rt>nán</rt></ruby><ruby>瓜<rt>guā</rt></ruby></span><span class="punct">。</span>`,
        en: `On Halloween evening, Xiaole and his sister carried home a big round orange pumpkin.`,
        enHtml: `<span class="en-word-group">On Halloween evening,</span> <span class="en-word-group">Xiaole and his sister</span> <span class="en-word-group">carried home</span> <span class="en-word-group">a big round orange pumpkin.</span>`
      }},
      {{
        img: "{s41_p[1]}",
        text: "他们挖出南瓜籽，给大南瓜刻上了三角形的眼睛和弯弯的笑嘴。",
        ruby: `<span class="word-group"><ruby>他<rt>tā</rt></ruby><ruby>们<rt>men</rt></ruby><ruby>挖<rt>wā</rt></ruby><ruby>出<rt>chū</rt></ruby><ruby>南<rt>nán</rt></ruby><ruby>瓜<rt>guā</rt></ruby><ruby>籽<rt>zǐ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>给<rt>gěi</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>南<rt>nán</rt></ruby><ruby>瓜<rt>guā</rt></ruby></span><span class="word-group"><ruby>刻<rt>kè</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>三<rt>sān</rt></ruby><ruby>角<rt>jiǎo</rt></ruby><ruby>形<rt>xíng</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>眼<rt>yǎn</rt></ruby><ruby>睛<rt>jing</rt></ruby></span><span class="word-group"><ruby>和<rt>hé</rt></ruby><ruby>弯<rt>wān</rt></ruby><ruby>弯<rt>wān</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>笑<rt>xiào</rt></ruby><ruby>嘴<rt>zuǐ</rt></ruby></span><span class="punct">。</span>`,
        en: `They scooped out the pumpkin seeds and carved triangle eyes and a curved smiling mouth onto the big pumpkin.`,
        enHtml: `<span class="en-word-group">They scooped out the pumpkin seeds</span> <span class="en-word-group">and carved triangle eyes</span> <span class="en-word-group">and a curved smiling mouth</span> <span class="en-word-group">onto the big pumpkin.</span>`
      }},
      {{
        img: "{s41_p[2]}",
        text: "放进一盏温暖的电子小蜡烛，南瓜灯笼立刻发出金黄色的光芒！",
        ruby: `<span class="word-group"><ruby>放<rt>fàng</rt></ruby><ruby>进<rt>jìn</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>盏<rt>zhǎn</rt></ruby><ruby>温<rt>wēn</rt></ruby><ruby>暖<rt>nuǎn</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>电<rt>diàn</rt></ruby><ruby>子<rt>zǐ</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>蜡<rt>là</rt></ruby><ruby>烛<rt>zhú</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>南<rt>nán</rt></ruby><ruby>瓜<rt>guā</rt></ruby><ruby>灯<rt>dēng</rt></ruby><ruby>笼<rt>long</rt></ruby></span><span class="word-group"><ruby>立<rt>lì</rt></ruby><ruby>刻<rt>kè</rt></ruby><ruby>发<rt>fā</rt></ruby><ruby>出<rt>chū</rt></ruby><ruby>金<rt>jīn</rt></ruby><ruby>黄<rt>huáng</rt></ruby><ruby>色<rt>sè</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>光<rt>guāng</rt></ruby><ruby>芒<rt>máng</rt></ruby></span><span class="punct">！</span>`,
        en: `Placing a warm LED candle inside, the jack-o'-lantern immediately glowed with golden light!`,
        enHtml: `<span class="en-word-group">Placing a warm LED candle inside,</span> <span class="en-word-group">the jack-o'-lantern</span> <span class="en-word-group">immediately glowed</span> <span class="en-word-group">with golden light!</span>`
      }},
      {{
        img: "{s41_p[3]}",
        text: "窗外的南瓜灯对着月亮眨了眨眼，好像在对小朋友说节日快乐！",
        ruby: `<span class="word-group"><ruby>窗<rt>chuāng</rt></ruby><ruby>外<rt>wài</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>南<rt>nán</rt></ruby><ruby>瓜<rt>guā</rt></ruby><ruby>灯<rt>dēng</rt></ruby></span><span class="word-group"><ruby>对<rt>duì</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>月<rt>yuè</rt></ruby><ruby>亮<rt>liang</rt></ruby><ruby>眨<rt>zhǎ</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>眨<rt>zhǎ</rt></ruby><ruby>眼<rt>yǎn</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>好<rt>hǎo</rt></ruby><ruby>像<rt>xiàng</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>对<rt>duì</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>朋<rt>péng</rt></ruby><ruby>友<rt>you</rt></ruby></span><span class="word-group"><ruby>说<rt>shuō</rt></ruby><ruby>节<rt>jié</rt></ruby><ruby>日<rt>rì</rt></ruby><ruby>快<rt>kuài</rt></ruby><ruby>乐<rt>lè</rt></ruby></span><span class="punct">！</span>`,
        en: `Outside the window, the jack-o'-lantern winked at the moon as if wishing the children a Happy Halloween!`,
        enHtml: `<span class="en-word-group">Outside the window,</span> <span class="en-word-group">the jack-o'-lantern winked at the moon</span> <span class="en-word-group">as if wishing the children</span> <span class="en-word-group">a Happy Halloween!</span>`
      }}
    ],
    vocab: [
      {{ hz: "万圣节", py: "wàn shèng jié", en: "Halloween" }},
      {{ hz: "南瓜灯", py: "nán guā dēng", en: "jack-o'-lantern" }},
      {{ hz: "蜡烛", py: "là zhú", en: "candle" }},
      {{ hz: "眨眼", py: "zhǎ yǎn", en: "wink and blink" }}
    ]
  }},
  {{
    id: 42,
    category: "halloween",
    icon: "🍬",
    title: "42. 不给糖就捣蛋大游行",
    titleText: "不给糖就捣蛋大游行",
    titlePinyin: "bù gěi táng jiù dǎo dàn dà yóu xíng",
    titleRuby: `<span class="word-group"><ruby>不<rt>bù</rt></ruby><ruby>给<rt>gěi</rt></ruby><ruby>糖<rt>táng</rt></ruby></span><span class="word-group"><ruby>就<rt>jiù</rt></ruby><ruby>捣<rt>dǎo</rt></ruby><ruby>蛋<rt>dàn</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>游<rt>yóu</rt></ruby><ruby>行<rt>xíng</rt></ruby></span>`,
    titleEn: "The Trick-or-Treat Costume Parade",
    titleEnHtml: `<span class="en-word-group">The Trick-or-Treat</span> <span class="en-word-group">Costume</span> <span class="en-word-group">Parade</span>`,
    subtitle: "搞怪万圣节 第2集 · 4 句 · 节日探险",
    bannerImg: "{s42_b}",
    sentences: [
      {{
        img: "{s42_p[0]}",
        text: "小朋友们穿上披风戴上尖顶帽，打扮成小巫师、小恐龙和小超人！",
        ruby: `<span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>朋<rt>péng</rt></ruby><ruby>友<rt>you</rt></ruby><ruby>们<rt>men</rt></ruby></span><span class="word-group"><ruby>穿<rt>chuān</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>披<rt>pī</rt></ruby><ruby>风<rt>fēng</rt></ruby><ruby>戴<rt>dài</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>尖<rt>jiān</rt></ruby><ruby>顶<rt>dǐng</rt></ruby><ruby>帽<rt>mào</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>打<rt>dǎ</rt></ruby><ruby>扮<rt>bàn</rt></ruby><ruby>成<rt>chéng</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>巫<rt>wū</rt></ruby><ruby>师<rt>shī</rt></ruby></span><span class="punct">、</span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>恐<rt>kǒng</rt></ruby><ruby>龙<rt>lóng</rt></ruby><ruby>和<rt>hé</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>超<rt>chāo</rt></ruby><ruby>人<rt>rén</rt></ruby></span><span class="punct">！</span>`,
        en: `The children put on capes and pointed hats, dressing up as little wizards, dinosaurs, and superheroes!`,
        enHtml: `<span class="en-word-group">The children put on capes</span> <span class="en-word-group">and pointed hats,</span> <span class="en-word-group">dressing up as little wizards,</span> <span class="en-word-group">dinosaurs, and superheroes!</span>`
      }},
      {{
        img: "{s42_p[1]}",
        text: "大家提着南瓜小桶去敲邻居家的门，大声喊“不给糖就捣蛋”！",
        ruby: `<span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>家<rt>jiā</rt></ruby><ruby>提<rt>tí</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>南<rt>nán</rt></ruby><ruby>瓜<rt>guā</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>桶<rt>tǒng</rt></ruby></span><span class="word-group"><ruby>去<rt>qù</rt></ruby><ruby>敲<rt>qiāo</rt></ruby><ruby>邻<rt>lín</rt></ruby><ruby>居<rt>jū</rt></ruby><ruby>家<rt>jiā</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>门<rt>mén</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>声<rt>shēng</rt></ruby><ruby>喊<rt>hǎn</rt></ruby></span><span class="punct">“</span><span class="word-group"><ruby>不<rt>bù</rt></ruby><ruby>给<rt>gěi</rt></ruby><ruby>糖<rt>táng</rt></ruby><ruby>就<rt>jiù</rt></ruby><ruby>捣<rt>dǎo</rt></ruby><ruby>蛋<rt>dàn</rt></ruby></span><span class="punct">”！</span>`,
        en: `Everyone carried little pumpkin buckets, knocked on neighbors' doors, and shouted, "Trick or treat!"`,
        enHtml: `<span class="en-word-group">Everyone carried little pumpkin buckets,</span> <span class="en-word-group">knocked on neighbors' doors,</span> <span class="en-word-group">and shouted,</span> <span class="en-word-group">"Trick or treat!"</span>`
      }},
      {{
        img: "{s42_p[2]}",
        text: "热心的张奶奶端出大果盘，往每个小桶里塞满了水果糖和巧克力。",
        ruby: `<span class="word-group"><ruby>热<rt>rè</rt></ruby><ruby>心<rt>xīn</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>张<rt>zhāng</rt></ruby><ruby>奶<rt>nǎi</rt></ruby><ruby>奶<rt>nai</rt></ruby></span><span class="word-group"><ruby>端<rt>duān</rt></ruby><ruby>出<rt>chū</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>果<rt>guǒ</rt></ruby><ruby>盘<rt>pán</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>往<rt>wǎng</rt></ruby><ruby>每<rt>měi</rt></ruby><ruby>个<rt>gè</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>桶<rt>tǒng</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="word-group"><ruby>塞<rt>sāi</rt></ruby><ruby>满<rt>mǎn</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>果<rt>guǒ</rt></ruby><ruby>糖<rt>táng</rt></ruby><ruby>和<rt>hé</rt></ruby><ruby>巧<rt>qiǎo</rt></ruby><ruby>克<rt>kè</rt></ruby><ruby>力<rt>lì</rt></ruby></span><span class="punct">。</span>`,
        en: `Warm-hearted Grandma Zhang brought out a big tray and filled every bucket with fruit candies and chocolates.`,
        enHtml: `<span class="en-word-group">Warm-hearted Grandma Zhang</span> <span class="en-word-group">brought out a big tray</span> <span class="en-word-group">and filled every bucket</span> <span class="en-word-group">with fruit candies and chocolates.</span>`
      }},
      {{
        img: "{s42_p[3]}",
        text: "整条街道挂满了彩灯和纸蝙蝠，到处都是小朋友欢快的笑声！",
        ruby: `<span class="word-group"><ruby>整<rt>zhěng</rt></ruby><ruby>条<rt>tiáo</rt></ruby><ruby>街<rt>jiē</rt></ruby><ruby>道<rt>dào</rt></ruby></span><span class="word-group"><ruby>挂<rt>guà</rt></ruby><ruby>满<rt>mǎn</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>彩<rt>cǎi</rt></ruby><ruby>灯<rt>dēng</rt></ruby><ruby>和<rt>hé</rt></ruby><ruby>纸<rt>zhǐ</rt></ruby><ruby>蝙<rt>biān</rt></ruby><ruby>蝠<rt>fú</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>到<rt>dào</rt></ruby><ruby>处<rt>chù</rt></ruby><ruby>都<rt>dōu</rt></ruby><ruby>是<rt>shì</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>朋<rt>péng</rt></ruby><ruby>友<rt>you</rt></ruby></span><span class="word-group"><ruby>欢<rt>huān</rt></ruby><ruby>快<rt>kuài</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>笑<rt>xiào</rt></ruby><ruby>声<rt>shēng</rt></ruby></span><span class="punct">！</span>`,
        en: `The whole street was hung with fairy lights and paper bats, filled everywhere with children's cheerful laughter!`,
        enHtml: `<span class="en-word-group">The whole street was hung</span> <span class="en-word-group">with fairy lights and paper bats,</span> <span class="en-word-group">filled everywhere with</span> <span class="en-word-group">children's cheerful laughter!</span>`
      }}
    ],
    vocab: [
      {{ hz: "披风", py: "pī fēng", en: "cape" }},
      {{ hz: "尖顶帽", py: "jiān dǐng mào", en: "pointed hat" }},
      {{ hz: "捣蛋", py: "dǎo dàn", en: "play a trick" }},
      {{ hz: "蝙蝠", py: "biān fú", en: "bat" }}
    ]
  }},
  {{
    id: 43,
    category: "halloween",
    icon: "👻",
    title: "43. 胆小鬼幽灵找朋友",
    titleText: "胆小鬼幽灵找朋友",
    titlePinyin: "dǎn xiǎo guǐ yōu líng zhǎo péng you",
    titleRuby: `<span class="word-group"><ruby>胆<rt>dǎn</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>鬼<rt>guǐ</rt></ruby></span><span class="word-group"><ruby>幽<rt>yōu</rt></ruby><ruby>灵<rt>líng</rt></ruby></span><span class="word-group"><ruby>找<rt>zhǎo</rt></ruby><ruby>朋<rt>péng</rt></ruby><ruby>友<rt>you</rt></ruby></span>`,
    titleEn: "The Shy Little Ghost Looking for Friends",
    titleEnHtml: `<span class="en-word-group">The Shy Little Ghost</span> <span class="en-word-group">Looking for</span> <span class="en-word-group">Friends</span>`,
    subtitle: "搞怪万圣节 第3集 · 4 句 · 节日探险",
    bannerImg: "{s43_b}",
    sentences: [
      {{
        img: "{s43_p[0]}",
        text: "阁楼里住着一只白床单一样的小幽灵，它其实是个怕黑的胆小鬼！",
        ruby: `<span class="word-group"><ruby>阁<rt>gé</rt></ruby><ruby>楼<rt>lóu</rt></ruby><ruby>里<rt>lǐ</rt></ruby><ruby>住<rt>zhù</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>只<rt>zhī</rt></ruby></span><span class="word-group"><ruby>白<rt>bái</rt></ruby><ruby>床<rt>chuáng</rt></ruby><ruby>单<rt>dān</rt></ruby><ruby>一<rt>yí</rt></ruby><ruby>样<rt>yàng</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>幽<rt>yōu</rt></ruby><ruby>灵<rt>líng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>它<rt>tā</rt></ruby><ruby>其<rt>qí</rt></ruby><ruby>实<rt>shí</rt></ruby><ruby>是<rt>shì</rt></ruby><ruby>个<rt>gè</rt></ruby></span><span class="word-group"><ruby>怕<rt>pà</rt></ruby><ruby>黑<rt>hēi</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>胆<rt>dǎn</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>鬼<rt>guǐ</rt></ruby></span><span class="punct">！</span>`,
        en: `In the attic lived a little white-sheet ghost who was actually a scaredy-cat afraid of the dark!`,
        enHtml: `<span class="en-word-group">In the attic lived</span> <span class="en-word-group">a little white-sheet ghost</span> <span class="en-word-group">who was actually a scaredy-cat</span> <span class="en-word-group">afraid of the dark!</span>`
      }},
      {{
        img: "{s43_p[1]}",
        text: "万圣节这天晚上，大家都在办化装舞会，没人害怕这只小幽灵。",
        ruby: `<span class="word-group"><ruby>万<rt>wàn</rt></ruby><ruby>圣<rt>shèng</rt></ruby><ruby>节<rt>jié</rt></ruby><ruby>这<rt>zhè</rt></ruby><ruby>天<rt>tiān</rt></ruby><ruby>晚<rt>wǎn</rt></ruby><ruby>上<rt>shang</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>家<rt>jiā</rt></ruby><ruby>都<rt>dōu</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>办<rt>bàn</rt></ruby><ruby>化<rt>huà</rt></ruby><ruby>装<rt>zhuāng</rt></ruby><ruby>舞<rt>wǔ</rt></ruby><ruby>会<rt>huì</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>没<rt>méi</rt></ruby><ruby>人<rt>rén</rt></ruby><ruby>害<rt>hài</rt></ruby><ruby>怕<rt>pà</rt></ruby></span><span class="word-group"><ruby>这<rt>zhè</rt></ruby><ruby>只<rt>zhī</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>幽<rt>yōu</rt></ruby><ruby>灵<rt>líng</rt></ruby></span><span class="punct">。</span>`,
        en: `On Halloween night, everyone was having a costume party, so nobody was afraid of the little ghost.`,
        enHtml: `<span class="en-word-group">On Halloween night,</span> <span class="en-word-group">everyone was having a costume party,</span> <span class="en-word-group">so nobody was afraid of</span> <span class="en-word-group">the little ghost.</span>`
      }},
      {{
        img: "{s43_p[2]}",
        text: "小女孩送给它一根发光棒棒糖，拉着它一起跳起了搞笑骷髅舞！",
        ruby: `<span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>女<rt>nǚ</rt></ruby><ruby>孩<rt>hái</rt></ruby><ruby>送<rt>sòng</rt></ruby><ruby>给<rt>gěi</rt></ruby><ruby>它<rt>tā</rt></ruby></span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>根<rt>gēn</rt></ruby><ruby>发<rt>fā</rt></ruby><ruby>光<rt>guāng</rt></ruby><ruby>棒<rt>bàng</rt></ruby><ruby>棒<rt>bàng</rt></ruby><ruby>糖<rt>táng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>拉<rt>lā</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>它<rt>tā</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>起<rt>qǐ</rt></ruby></span><span class="word-group"><ruby>跳<rt>tiào</rt></ruby><ruby>起<rt>qǐ</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>搞<rt>gǎo</rt></ruby><ruby>笑<rt>xiào</rt></ruby><ruby>骷<rt>kū</rt></ruby><ruby>髅<rt>lóu</rt></ruby><ruby>舞<rt>wǔ</rt></ruby></span><span class="punct">！</span>`,
        en: `A little girl gave it a glowing lollipop and pulled it in to dance the funny skeleton dance together!`,
        enHtml: `<span class="en-word-group">A little girl gave it</span> <span class="en-word-group">a glowing lollipop</span> <span class="en-word-group">and pulled it in to dance</span> <span class="en-word-group">the funny skeleton dance together!</span>`
      }},
      {{
        img: "{s43_p[3]}",
        text: "小幽灵开心得脸颊红扑扑，终于交到了一群喜欢它的好朋友！",
        ruby: `<span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>幽<rt>yōu</rt></ruby><ruby>灵<rt>líng</rt></ruby><ruby>开<rt>kāi</rt></ruby><ruby>心<rt>xīn</rt></ruby><ruby>得<rt>de</rt></ruby></span><span class="word-group"><ruby>脸<rt>liǎn</rt></ruby><ruby>颊<rt>jiá</rt></ruby><ruby>红<rt>hóng</rt></ruby><ruby>扑<rt>pū</rt></ruby><ruby>扑<rt>pū</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>终<rt>zhōng</rt></ruby><ruby>于<rt>yú</rt></ruby><ruby>交<rt>jiāo</rt></ruby><ruby>到<rt>dào</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>群<rt>qún</rt></ruby></span><span class="word-group"><ruby>喜<rt>xǐ</rt></ruby><ruby>欢<rt>huan</rt></ruby><ruby>它<rt>tā</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>好<rt>hǎo</rt></ruby><ruby>朋<rt>péng</rt></ruby><ruby>友<rt>you</rt></ruby></span><span class="punct">！</span>`,
        en: `The little ghost was so happy its cheeks turned rosy pink, finally making a group of good friends!`,
        enHtml: `<span class="en-word-group">The little ghost was so happy</span> <span class="en-word-group">its cheeks turned rosy pink,</span> <span class="en-word-group">finally making a group of</span> <span class="en-word-group">good friends!</span>`
      }}
    ],
    vocab: [
      {{ hz: "阁楼", py: "gé lóu", en: "attic" }},
      {{ hz: "幽灵", py: "yōu líng", en: "ghost" }},
      {{ hz: "化装舞会", py: "huà zhuāng wǔ huì", en: "costume party" }},
      {{ hz: "棒棒糖", py: "bàng bàng táng", en: "lollipop" }}
    ]
  }},
  {{
    id: 44,
    category: "halloween",
    icon: "🧹",
    title: "44. 小女巫的爆米花扫帚",
    titleText: "小女巫的爆米花扫帚",
    titlePinyin: "xiǎo nǚ wū de bào mǐ huā sào zhou",
    titleRuby: `<span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>女<rt>nǚ</rt></ruby><ruby>巫<rt>wū</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>爆<rt>bào</rt></ruby><ruby>米<rt>mǐ</rt></ruby><ruby>花<rt>huā</rt></ruby></span><span class="word-group"><ruby>扫<rt>sào</rt></ruby><ruby>帚<rt>zhou</rt></ruby></span>`,
    titleEn: "The Little Witch's Popcorn Broomstick",
    titleEnHtml: `<span class="en-word-group">The Little Witch's</span> <span class="en-word-group">Popcorn</span> <span class="en-word-group">Broomstick</span>`,
    subtitle: "搞怪万圣节 第4集 · 4 句 · 节日探险",
    bannerImg: "{s44_b}",
    sentences: [
      {{
        img: "{s44_p[0]}",
        text: "糊涂小女巫骑着魔法扫帚去参加派对，怀里还抱着黑猫咪咪。",
        ruby: `<span class="word-group"><ruby>糊<rt>hú</rt></ruby><ruby>涂<rt>tu</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>女<rt>nǚ</rt></ruby><ruby>巫<rt>wū</rt></ruby></span><span class="word-group"><ruby>骑<rt>qí</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>魔<rt>mó</rt></ruby><ruby>法<rt>fǎ</rt></ruby><ruby>扫<rt>sào</rt></ruby><ruby>帚<rt>zhou</rt></ruby></span><span class="word-group"><ruby>去<rt>qù</rt></ruby><ruby>参<rt>cān</rt></ruby><ruby>加<rt>jiā</rt></ruby><ruby>派<rt>pài</rt></ruby><ruby>对<rt>duì</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>怀<rt>huái</rt></ruby><ruby>里<rt>lǐ</rt></ruby><ruby>还<rt>hái</rt></ruby><ruby>抱<rt>bào</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>黑<rt>hēi</rt></ruby><ruby>猫<rt>māo</rt></ruby><ruby>咪<rt>mī</rt></ruby><ruby>咪<rt>mī</rt></ruby></span><span class="punct">。</span>`,
        en: `The scatterbrained little witch rode her magic broomstick to the party, hugging her black cat Mimi in her arms.`,
        enHtml: `<span class="en-word-group">The scatterbrained little witch</span> <span class="en-word-group">rode her magic broomstick to the party,</span> <span class="en-word-group">hugging her black cat Mimi</span> <span class="en-word-group">in her arms.</span>`
      }},
      {{
        img: "{s44_p[1]}",
        text: "她念错了飞行咒语，扫帚尾巴不冒火花，反而喷出了焦糖爆米花！",
        ruby: `<span class="word-group"><ruby>她<rt>tā</rt></ruby><ruby>念<rt>niàn</rt></ruby><ruby>错<rt>cuò</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>飞<rt>fēi</rt></ruby><ruby>行<rt>xíng</rt></ruby><ruby>咒<rt>zhòu</rt></ruby><ruby>语<rt>yǔ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>扫<rt>sào</rt></ruby><ruby>帚<rt>zhou</rt></ruby><ruby>尾<rt>wěi</rt></ruby><ruby>巴<rt>ba</rt></ruby><ruby>不<rt>bú</rt></ruby><ruby>冒<rt>mào</rt></ruby><ruby>火<rt>huǒ</rt></ruby><ruby>花<rt>huā</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>反<rt>fǎn</rt></ruby><ruby>而<rt>ér</rt></ruby><ruby>喷<rt>pēn</rt></ruby><ruby>出<rt>chū</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>焦<rt>jiāo</rt></ruby><ruby>糖<rt>táng</rt></ruby><ruby>爆<rt>bào</rt></ruby><ruby>米<rt>mǐ</rt></ruby><ruby>花<rt>huā</rt></ruby></span><span class="punct">！</span>`,
        en: `She mixed up the flying spell, so instead of sparks, the tail of her broomstick popped out caramel popcorn!`,
        enHtml: `<span class="en-word-group">She mixed up the flying spell,</span> <span class="en-word-group">so instead of sparks,</span> <span class="en-word-group">the tail of her broomstick</span> <span class="en-word-group">popped out caramel popcorn!</span>`
      }},
      {{
        img: "{s44_p[2]}",
        text: "香脆的爆米花像雪花一样飘下来，树上的猫头鹰伸长翅膀去接。",
        ruby: `<span class="word-group"><ruby>香<rt>xiāng</rt></ruby><ruby>脆<rt>cuì</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>爆<rt>bào</rt></ruby><ruby>米<rt>mǐ</rt></ruby><ruby>花<rt>huā</rt></ruby></span><span class="word-group"><ruby>像<rt>xiàng</rt></ruby><ruby>雪<rt>xuě</rt></ruby><ruby>花<rt>huā</rt></ruby><ruby>一<rt>yí</rt></ruby><ruby>样<rt>yàng</rt></ruby><ruby>飘<rt>piāo</rt></ruby><ruby>下<rt>xià</rt></ruby><ruby>来<rt>lái</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>树<rt>shù</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>猫<rt>māo</rt></ruby><ruby>头<rt>tóu</rt></ruby><ruby>鹰<rt>yīng</rt></ruby></span><span class="word-group"><ruby>伸<rt>shēn</rt></ruby><ruby>长<rt>cháng</rt></ruby><ruby>翅<rt>chì</rt></ruby><ruby>膀<rt>bǎng</rt></ruby><ruby>去<rt>qù</rt></ruby><ruby>接<rt>jiē</rt></ruby></span><span class="punct">。</span>`,
        en: `Crunchy popcorn floated down like snowflakes while the owl in the tree stretched out its wings to catch them.`,
        enHtml: `<span class="en-word-group">Crunchy popcorn floated down</span> <span class="en-word-group">like snowflakes</span> <span class="en-word-group">while the owl in the tree</span> <span class="en-word-group">stretched out its wings to catch them.</span>`
      }},
      {{
        img: "{s44_p[3]}",
        text: "小女巫降落在树屋平台上，请所有小动物一起吃热乎乎的爆米花！",
        ruby: `<span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>女<rt>nǚ</rt></ruby><ruby>巫<rt>wū</rt></ruby><ruby>降<rt>jiàng</rt></ruby><ruby>落<rt>luò</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>树<rt>shù</rt></ruby><ruby>屋<rt>wū</rt></ruby><ruby>平<rt>píng</rt></ruby><ruby>台<rt>tái</rt></ruby><ruby>上<rt>shàng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>请<rt>qǐng</rt></ruby><ruby>所<rt>suǒ</rt></ruby><ruby>有<rt>yǒu</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>动<rt>dòng</rt></ruby><ruby>物<rt>wù</rt></ruby></span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>起<rt>qǐ</rt></ruby><ruby>吃<rt>chī</rt></ruby><ruby>热<rt>rè</rt></ruby><ruby>乎<rt>hū</rt></ruby><ruby>乎<rt>hū</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>爆<rt>bào</rt></ruby><ruby>米<rt>mǐ</rt></ruby><ruby>花<rt>huā</rt></ruby></span><span class="punct">！</span>`,
        en: `The little witch landed on the treehouse deck and treated all the little animals to warm caramel popcorn!`,
        enHtml: `<span class="en-word-group">The little witch landed</span> <span class="en-word-group">on the treehouse deck</span> <span class="en-word-group">and treated all the little animals</span> <span class="en-word-group">to warm caramel popcorn!</span>`
      }}
    ],
    vocab: [
      {{ hz: "扫帚", py: "sào zhou", en: "broomstick" }},
      {{ hz: "咒语", py: "zhòu yǔ", en: "magic spell" }},
      {{ hz: "爆米花", py: "bào mǐ huā", en: "popcorn" }},
      {{ hz: "猫头鹰", py: "māo tóu yīng", en: "owl" }}
    ]
  }}
];"""

    html = INDEX_PATH.read_text(encoding="utf-8")

    target_end = """      { hz: "田田", py: "tián tián", en: "lush and round" },
      { hz: "捉迷藏", py: "zhuō mí cáng", en: "hide-and-seek" }
    ]
  }
];"""

    assert target_end in html, "Could not find end of Story 36 in index.html"
    html = html.replace(
        target_end,
        """      { hz: "田田", py: "tián tián", en: "lush and round" },
      { hz: "捉迷藏", py: "zhuō mí cáng", en: "hide-and-seek" }
    ]
"""
        + new_stories_js,
        1,
    )

    old_categories = """const CATEGORIES = [
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

    new_categories = """const CATEGORIES = [
  { id: 'all', label: '✨ 全部故事 · All (44)' },
  { id: 'halloween', label: '🎃 搞怪万圣节 · Halloween (4)' },
  { id: 'wonka', label: '🍫 巧克力工厂 · Chocolate Factory (4)' },
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
    print("Successfully updated index.html with Willy Wonka (37-40) and Halloween (41-44) stories!")


if __name__ == "__main__":
    main()
