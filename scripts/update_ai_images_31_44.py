#!/usr/bin/env python3
"""
Replace procedural illustrations for Stories 31-44 in index.html with
AI-generated watercolor illustrations from image-generator subagents:
- Stories 31-36 (📜 古诗绘本 · Classical Poems): 2x2 grids (story31_grid_ai_*.jpg .. story36_grid_ai_*.jpg)
- Stories 37-44 (🍫 巧克力工厂 & 🎃 搞怪万圣节): 2x4 8-panel grids (story37_38_grid_ai_*.jpg .. story43_44_grid_ai_*.jpg)
"""

import glob
import re
from pathlib import Path
from PIL import Image

from crop_grid_images import (
    crop_4_3,
    extract_story_images,
    img_to_webp_data_url,
    make_banner_from_panels,
)

ROOT = Path(__file__).resolve().parent.parent
INDEX_HTML = ROOT / "index.html"
ARTIFACT_DIR = Path(
    "/Users/leizhou/.gemini/antigravity-cli/brain/dde92688-d628-4cf6-9d61-3d1a08abad1b"
)


def find_latest_artifact(prefix: str) -> Path:
    matches = sorted(glob.glob(str(ARTIFACT_DIR / f"{prefix}_*.jpg")))
    if not matches:
        raise FileNotFoundError(f"No artifact found matching {prefix}_*.jpg in {ARTIFACT_DIR}")
    return Path(matches[-1])


def extract_two_stories_from_2x4_grid(
    grid_path: str | Path, quality: int = 80
) -> tuple[tuple[str, list[str]], tuple[str, list[str]]]:
    """
    Crop a 2-row x 4-column (8-panel) grid image into two stories:
    - Top row (4 panels left-to-right) -> Story A (banner_url, [p1, p2, p3, p4])
    - Bottom row (4 panels left-to-right) -> Story B (banner_url, [p1, p2, p3, p4])
    """
    im = Image.open(grid_path).convert("RGB")
    w, h = im.size
    mx = int(w * 0.015)
    my = int(h * 0.022)
    gx = int(w * 0.010)
    gy = int(h * 0.018)

    col_w = w / 4.0
    mid_y = h // 2

    def get_row_story(row_idx: int) -> tuple[str, list[str]]:
        y1 = my if row_idx == 0 else mid_y + gy
        y2 = (mid_y - gy) if row_idx == 0 else (h - my)
        panels = []
        for c in range(4):
            x1 = int(c * col_w) + (mx if c == 0 else gx)
            x2 = int((c + 1) * col_w) - (mx if c == 3 else gx)
            panels.append(crop_4_3(im.crop((x1, y1, x2, y2))))
        banner = make_banner_from_panels(panels[0], panels[1])
        return img_to_webp_data_url(banner, quality=quality), [
            img_to_webp_data_url(p, quality=quality) for p in panels
        ]

    return get_row_story(0), get_row_story(1)


def replace_story_images_in_html(
    html: str, story_id: int, banner_url: str, panel_urls: list[str]
) -> str:
    """Replace bannerImg and the 4 sentence img data URLs for a given story_id in index.html."""
    if story_id < 44:
        pattern = re.compile(
            rf"(id:\s*{story_id}\b.*?)(?=id:\s*{story_id + 1}\b)",
            re.DOTALL,
        )
    else:
        pattern = re.compile(
            rf"(id:\s*{story_id}\b.*?)(?=\n\];)",
            re.DOTALL,
        )

    m = pattern.search(html)
    if not m:
        raise ValueError(f"Could not locate story id: {story_id} in index.html")

    block = m.group(1)

    # Replace bannerImg (supports single or double quotes)
    block_new, n_banner = re.subn(
        r"""bannerImg:\s*['"]data:image/webp;base64,[^'"]*['"]""",
        f"bannerImg: '{banner_url}'",
        block,
        count=1,
    )
    if n_banner != 1:
        raise ValueError(f"Expected 1 bannerImg in story {story_id}, replaced {n_banner}")

    # Replace the 4 sentence img fields in order (supports single or double quotes)
    panel_iter = iter(panel_urls)
    count = 0

    def repl_img(match: re.Match) -> str:
        nonlocal count
        count += 1
        return f"img: '{next(panel_iter)}'"

    block_new = re.sub(
        r"""img:\s*['"]data:image/webp;base64,[^'"]*['"]""",
        repl_img,
        block_new,
    )
    if count != 4:
        raise ValueError(f"Expected 4 sentence imgs in story {story_id}, replaced {count}")

    return html[: m.start(1)] + block_new + html[m.end(1) :]


def main() -> None:
    story_images: dict[int, tuple[str, list[str]]] = {}

    # 1. Stories 31-36 from 2x2 grids
    for sid in range(31, 37):
        grid_path = find_latest_artifact(f"story{sid}_grid_ai")
        print(f"Cropping Story {sid} (2x2) from {grid_path.name} ...")
        story_images[sid] = extract_story_images(grid_path)

    # 2. Stories 37-44 from 2x4 8-panel grids
    pairs = [(37, 38), (39, 40), (41, 42), (43, 44)]
    for s_top, s_bot in pairs:
        grid_path = find_latest_artifact(f"story{s_top}_{s_bot}_grid_ai")
        print(f"Cropping Stories {s_top} & {s_bot} (2x4) from {grid_path.name} ...")
        story_images[s_top], story_images[s_bot] = extract_two_stories_from_2x4_grid(grid_path)

    html = INDEX_HTML.read_text(encoding="utf-8")
    for sid in range(31, 45):
        banner_url, panel_urls = story_images[sid]
        html = replace_story_images_in_html(html, sid, banner_url, panel_urls)

    INDEX_HTML.write_text(html, encoding="utf-8")
    print("Successfully updated AI illustrations for Stories 31-44 in index.html!")


if __name__ == "__main__":
    main()
