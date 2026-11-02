# 🎈 中文少儿绘本朗读器 · Chinese Children's Storybook Reader

An interactive bilingual (Chinese–English) illustrated storybook reader for children, featuring:

- **44 Illustrated Stories across 10 Series**:
  - 🎃 **搞怪万圣节 · Halloween (4)** — Spooky-cute Halloween trick-or-treat & friendly ghost adventures (Stories 41–44)
  - 🍫 **巧克力工厂 · Chocolate Factory (4)** — *Willy Wonka*-inspired magical candy factory tales (Stories 37–40)
  - 📜 **古诗绘本 · Classical Poems (6)** — Beloved Tang, Song & Han classical poems paired with child-friendly story scenes (Stories 31–36: 《咏鹅》, 《静夜思》, 《春晓》, 《悯农》, 《小池》, 《江南》)
  - 🐼 **变身红熊猫 · Red Panda (4)** — *Turning Red*-inspired magical red panda & friendship stories (Stories 27–30)
  - 🐾 **蓝小狗一家 · Blue Pup (4)** — *Bluey*-inspired family & pretend-play stories (Stories 23–26)
  - 🐶 **神探汪汪 · Dog Cop (4)** — *Dog Man*-inspired hilarious comic adventures (Stories 19–22)
  - 🤪 **疯狂学校 · My Weird School (4)** — Wacky elementary school stories (Stories 13–16)
  - 🕵️ **脑洞探秘 · Mystery & Sci-Fi (2)** — Mystery & time-travel adventures (Stories 17–18)
  - 🏫 **校园日常 · School Life (4)** — Relatable elementary school life (Stories 9–12)
  - 🐾 **童话绘本 · Animal Tales (8)** — Classic animal picture-book tales (Stories 1–8)
- **Word-by-Word & Full-Sentence Audio**: Tap any Chinese word group (`.word-group`), English phrase (`.en-word-group`), vocabulary chip, or full sentence to hear natural neural speech (`zh-CN-XiaoxiaoNeural` & `en-US-AnaNeural`) pre-generated in [`audio/`](audio/), with automatic fallback to browser TTS (`Tingting` / system voices).
- **🔤 Pinyin Toggle**: One-click button (`#btnTogglePinyin`) to hide or show Pinyin across story titles, sentences, vocabulary chips, flashcards, and the writing studio.
- **🃏 3D Interactive Story Flashcards**: Flip cards for both **Key Vocabulary** and **Story Phrases**, complete with audio playback, example sentence context, illustration preview, and mastery tracking.
- **✍️ Hanzi Writer Stroke-Order & Writing Studio**: Step-by-step animated stroke order and interactive stroke-tracing quiz (`HanziWriter`) for every vocabulary character and story character.

---

## 🛠️ Content & Audio Tooling (`uv` + `edge-tts` + `Pillow`)

All scripts used to crop 2x2 storybook grid illustrations, inject new story series into [`index.html`](index.html), and pre-generate neural TTS MP3s are located in [`scripts/`](scripts/) and managed via [`uv`](https://docs.astral.sh/uv/) and [`pyproject.toml`](pyproject.toml).

### 1. Install Dependencies with `uv`

```bash
uv sync
```

This installs:
- [`edge-tts`](https://github.com/rany2/edge-tts) — Microsoft Edge Neural TTS client (`zh-CN-XiaoxiaoNeural` and `en-US-AnaNeural`)
- [`Pillow`](https://python-pillow.org/) — Image processing for cropping 2x2 grid illustrations into `640x240` panoramic WebP banners and `320x240` 4:3 sentence thumbnails

### 2. Generate / Update Neural TTS Audio (`scripts/generate_audio.py`)

Whenever you add or edit stories, sentences, word groups, or vocabulary in [`index.html`](index.html), run:

```bash
uv run python scripts/generate_audio.py
```

What [`scripts/generate_audio.py`](scripts/generate_audio.py) does:
1. Extracts the inline `<script>` from [`index.html`](index.html) and validates JavaScript syntax using `node --check`.
2. Parses the `STORIES` array and collects every unique:
   - Chinese story title, sentence, `.word-group` phrase, vocabulary word, and single Hanzi character (`[\u4e00-\u9fff]`)
   - English story title, sentence, `.en-word-group` phrase, vocabulary gloss, and flashcard phrase hint
3. Computes the deterministic 64-bit FNV-1a hash (`fnv1a_hex`) matching `fnv1aHex()` in [`index.html`](index.html):
   - Chinese MP3 path: `audio/zh_<fnv1a_hex>.mp3`
   - English MP3 path: `audio/en_<fnv1a_hex>.mp3`
4. Synthesizes only the missing MP3 files concurrently via `edge-tts` and verifies zero missing audio files.

### 3. Crop 2x2 Grid Illustrations (`scripts/crop_grid_images.py`)

To preview or extract WebP data URLs (`bannerImg` + 4 panel `img`s) from a 2x2 storybook grid image:

```bash
uv run python scripts/crop_grid_images.py path/to/story_grid.jpg
```

### 4. Series Addition Scripts

- [`scripts/add_dogman_stories.py`](scripts/add_dogman_stories.py) — Crops the 2x2 grids and adds Stories 19–22 (`🐶 神探汪汪 · Dog Cop`).
- [`scripts/add_bluey_stories.py`](scripts/add_bluey_stories.py) — Crops the 2x2 grids and adds Stories 23–26 (`🐾 蓝小狗一家 · Blue Pup`).
- [`scripts/add_redpanda_stories.py`](scripts/add_redpanda_stories.py) — Crops the 2x2 grids and adds Stories 27–30 (`🐼 变身红熊猫 · Red Panda`).
- [`scripts/add_poetry_stories.py`](scripts/add_poetry_stories.py) — Renders Chinese ink-and-watercolor illustrations and adds Stories 31–36 (`📜 古诗绘本 · Classical Poems`).
- [`scripts/add_wonka_halloween_stories.py`](scripts/add_wonka_halloween_stories.py) — Renders storybook illustrations and adds Stories 37–40 (`🍫 巧克力工厂 · Chocolate Factory`) and Stories 41–44 (`🎃 搞怪万圣节 · Halloween`).
