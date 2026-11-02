#!/usr/bin/env python3
"""
Validate JS syntax in index.html, extract all Chinese & English strings across all stories
(titles, sentences, word groups, vocabulary, flashcard hints, and single Hanzi characters),
and generate any missing neural TTS MP3 files in audio/ using edge-tts.

Usage:
    uv run python scripts/generate_audio.py
"""

import asyncio
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path
import edge_tts

ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT_DIR / "index.html"
AUDIO_DIR = ROOT_DIR / "audio"

ZH_VOICE = "zh-CN-XiaoxiaoNeural"
EN_VOICE = "en-US-AnaNeural"


def fnv1a_hex(text: str) -> str:
    """Deterministic 64-bit FNV-1a hash matching fnv1aHex(text) in index.html."""
    h1 = 0x811C9DC5
    h2 = 0x01000193
    for b in text.strip().encode("utf-8"):
        h1 ^= b
        h1 = (h1 * 0x01000193) & 0xFFFFFFFF
        h2 ^= b
        h2 = (h2 * 0x811C9DC5) & 0xFFFFFFFF
    return f"{h1:08x}{h2:08x}"


def extract_texts_from_index(index_path: Path) -> tuple[list[str], list[str]]:
    html = index_path.read_text(encoding="utf-8")
    script_blocks = re.findall(r"<script>(.*?)</script>", html, flags=re.S)
    if len(script_blocks) != 1:
        raise RuntimeError(f"Expected 1 inline <script> block, found {len(script_blocks)}")

    js_code = script_blocks[0]
    with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tmp:
        tmp.write(js_code)
        tmp_js_path = tmp.name

    try:
        subprocess.run(["node", "--check", tmp_js_path], check=True)
        print("✅ JS syntax check passed!")

        node_extractor = f"""
const fs = require('fs');
const code = fs.readFileSync({json.dumps(tmp_js_path)}, 'utf8');
const storiesMatch = code.match(/const STORIES = (\\[[\\s\\S]*?\\n\\]);/);
if (!storiesMatch) {{
  console.error('Could not find STORIES array in index.html');
  process.exit(1);
}}
const STORIES = eval(storiesMatch[1]);

const zhSet = new Set();
const enSet = new Set();

for (const story of STORIES) {{
  if (story.titleText) zhSet.add(story.titleText.trim());
  if (story.titleEn) enSet.add(story.titleEn.trim());

  const allRubyHtml = [story.titleRuby, ...story.sentences.map(s => s.ruby)].join(' ');
  for (const m of allRubyHtml.matchAll(/<span class="word-group">(.*?)<\\/span>/g)) {{
    const hz = m[1].replace(/<rt>.*?<\\/rt>/g, '').replace(/<[^>]+>/g, '').trim();
    if (hz) zhSet.add(hz);
  }}
  for (const m of allRubyHtml.matchAll(/<ruby>([\\u4e00-\\u9fff])<rt>([^<]+)<\\/rt><\\/ruby>/g)) {{
    zhSet.add(m[1]);
  }}

  for (const m of (story.titleEnHtml || '').matchAll(/<span class="en-word-group">(.*?)<\\/span>/g)) {{
    const p = m[1].trim();
    if (p) enSet.add(p);
  }}

  const vocabLookup = new Map(story.vocab.map(v => [v.hz, v.en]));
  story.sentences.forEach((s, sIdx) => {{
    if (s.text) zhSet.add(s.text.trim());
    if (s.en) enSet.add(s.en.trim());
    const enGroups = Array.from((s.enHtml || '').matchAll(/<span class="en-word-group">(.*?)<\\/span>/g)).map(m => m[1].trim());
    enGroups.forEach(p => {{ if (p) enSet.add(p); }});

    const zhGroupMatches = Array.from(s.ruby.matchAll(/<span class="word-group">(.*?)<\\/span>/g));
    zhGroupMatches.forEach((m, gIdx) => {{
      const inner = m[1];
      const hz = inner.replace(/<rt>.*?<\\/rt>/g, '').replace(/<[^>]+>/g, '').trim();
      if (!hz) return;
      const enHint = vocabLookup.get(hz) || enGroups[Math.min(gIdx, enGroups.length - 1)] || `Sentence ${{sIdx + 1}} phrase`;
      if (enHint) enSet.add(enHint.trim());
    }});
  }});

  for (const v of story.vocab) {{
    if (v.hz) {{
      zhSet.add(v.hz.trim());
      for (const ch of Array.from(v.hz)) {{
        if (/[\\u4e00-\\u9fff]/.test(ch)) zhSet.add(ch);
      }}
    }}
    if (v.en) enSet.add(v.en.trim());
  }}
}}

console.log(JSON.stringify({{
  storyCount: STORIES.length,
  zh: Array.from(zhSet),
  en: Array.from(enSet)
}}));
"""
        res = subprocess.run(["node", "-e", node_extractor], capture_output=True, text=True, check=True)
        data = json.loads(res.stdout)
        print(f"📚 Stories parsed: {data['storyCount']}")
        return data["zh"], data["en"]
    finally:
        if os.path.exists(tmp_js_path):
            os.remove(tmp_js_path)


async def synthesize_missing(missing_zh: list[tuple[str, Path]], missing_en: list[tuple[str, Path]]) -> None:
    sem = asyncio.Semaphore(10)

    async def gen_one(text: str, voice: str, out_path: Path) -> None:
        async with sem:
            for attempt in range(4):
                try:
                    comm = edge_tts.Communicate(text, voice)
                    await comm.save(str(out_path))
                    if out_path.exists() and out_path.stat().st_size > 0:
                        return
                except Exception as exc:
                    if attempt == 3:
                        print(f"❌ ERROR generating {text!r} -> {out_path.name}: {exc}")
                    await asyncio.sleep(0.8 * (attempt + 1))

    tasks = [gen_one(t, ZH_VOICE, p) for t, p in missing_zh] + [
        gen_one(t, EN_VOICE, p) for t, p in missing_en
    ]
    if tasks:
        await asyncio.gather(*tasks)


def main() -> None:
    AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    zh_texts, en_texts = extract_texts_from_index(INDEX_PATH)
    print(f"🔍 Unique ZH strings: {len(zh_texts)} | Unique EN strings: {len(en_texts)}")

    missing_zh = [
        (t, AUDIO_DIR / f"zh_{fnv1a_hex(t)}.mp3")
        for t in zh_texts
        if not (AUDIO_DIR / f"zh_{fnv1a_hex(t)}.mp3").exists()
        or (AUDIO_DIR / f"zh_{fnv1a_hex(t)}.mp3").stat().st_size == 0
    ]
    missing_en = [
        (t, AUDIO_DIR / f"en_{fnv1a_hex(t)}.mp3")
        for t in en_texts
        if not (AUDIO_DIR / f"en_{fnv1a_hex(t)}.mp3").exists()
        or (AUDIO_DIR / f"en_{fnv1a_hex(t)}.mp3").stat().st_size == 0
    ]

    print(f"🎙️ Missing ZH MP3s to generate: {len(missing_zh)}")
    print(f"🎙️ Missing EN MP3s to generate: {len(missing_en)}")

    if missing_zh or missing_en:
        asyncio.run(synthesize_missing(missing_zh, missing_en))

    still_missing_zh = [t for t, p in missing_zh if not p.exists() or p.stat().st_size == 0]
    still_missing_en = [t for t, p in missing_en if not p.exists() or p.stat().st_size == 0]
    print(f"✅ Complete! Still missing ZH: {len(still_missing_zh)}, EN: {len(still_missing_en)}")
    if still_missing_zh or still_missing_en:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
