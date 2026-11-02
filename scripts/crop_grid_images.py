#!/usr/bin/env python3
"""
Utility functions to crop a 2x2 storybook grid illustration into:
- 1 panoramic WebP banner data URL (640x240)
- 4 sentence thumbnail WebP data URLs (320x240, 4:3 aspect ratio)

Usage:
    uv run python scripts/crop_grid_images.py path/to/story_grid.jpg
"""

import base64
import io
import sys
from pathlib import Path
from PIL import Image


def img_to_webp_data_url(pil_img: Image.Image, quality: int = 80) -> str:
    buf = io.BytesIO()
    pil_img.save(buf, format="WEBP", quality=quality, method=6)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/webp;base64,{b64}"


def crop_4_3(pil_img: Image.Image) -> Image.Image:
    w, h = pil_img.size
    target_ratio = 4.0 / 3.0
    cur_ratio = w / float(h)
    if cur_ratio > target_ratio:
        new_w = int(h * target_ratio)
        left = (w - new_w) // 2
        pil_img = pil_img.crop((left, 0, left + new_w, h))
    else:
        new_h = int(w / target_ratio)
        top = (h - new_h) // 2
        pil_img = pil_img.crop((0, top, w, top + new_h))
    return pil_img.resize((320, 240), Image.Resampling.LANCZOS)


def make_banner_from_panels(p1: Image.Image, p2: Image.Image) -> Image.Image:
    """Create a 640x240 panoramic banner by blending top-left and top-right panels."""
    p1_r = p1.resize((330, 240), Image.Resampling.LANCZOS)
    p2_r = p2.resize((330, 240), Image.Resampling.LANCZOS)
    banner = Image.new("RGB", (640, 240))
    banner.paste(p1_r.crop((0, 0, 310, 240)), (0, 0))
    banner.paste(p2_r.crop((20, 0, 330, 240)), (330, 0))
    for x in range(20):
        alpha = x / 19.0
        col1 = p1_r.crop((310 + x, 0, 310 + x + 1, 240))
        col2 = p2_r.crop((x, 0, x + 1, 240))
        blended = Image.blend(col1, col2, alpha)
        banner.paste(blended, (310 + x, 0))
    return banner


def extract_story_images(grid_path: str | Path, quality: int = 80) -> tuple[str, list[str]]:
    im = Image.open(grid_path).convert("RGB")
    w, h = im.size
    mx = int(w * 0.025)
    my = int(h * 0.025)
    cx = int(w * 0.018)
    cy = int(h * 0.018)
    mid_x = w // 2
    mid_y = h // 2

    boxes = [
        (mx, my, mid_x - cx, mid_y - cy),          # Top-Left (Sentence 1)
        (mid_x + cx, my, w - mx, mid_y - cy),      # Top-Right (Sentence 2)
        (mx, mid_y + cy, mid_x - cx, h - my),      # Bottom-Left (Sentence 3)
        (mid_x + cx, mid_y + cy, w - mx, h - my),  # Bottom-Right (Sentence 4)
    ]
    panels = [crop_4_3(im.crop(b)) for b in boxes]
    banner = make_banner_from_panels(panels[0], panels[1])
    return img_to_webp_data_url(banner, quality=quality), [
        img_to_webp_data_url(p, quality=quality) for p in panels
    ]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: uv run python scripts/crop_grid_images.py <grid_image.jpg>")
        raise SystemExit(1)
    b_url, p_urls = extract_story_images(sys.argv[1])
    print(f"Banner WebP data URL length: {len(b_url)}")
    for i, u in enumerate(p_urls, 1):
        print(f"Panel {i} WebP data URL length: {len(u)}")
