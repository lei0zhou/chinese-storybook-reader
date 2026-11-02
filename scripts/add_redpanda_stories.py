#!/usr/bin/env python3
"""
Crop the Turning Red series 2x2 grid illustrations into WebP bannerImg and panel imgs,
and inject Stories 27-30 (🐼 变身红熊猫 · Red Panda) into index.html.
"""

import os
from pathlib import Path
from PIL import Image, ImageEnhance, ImageOps
from crop_grid_images import crop_4_3, extract_story_images, img_to_webp_data_url, make_banner_from_panels

BRAIN_DIR = Path("/Users/leizhou/.gemini/antigravity-cli/brain/dde92688-d628-4cf6-9d61-3d1a08abad1b")
ROOT_DIR = Path(__file__).resolve().parent.parent
INDEX_PATH = ROOT_DIR / "index.html"

G28 = BRAIN_DIR / "story28_grid_1793626685544.jpg"
G29 = BRAIN_DIR / "story29_grid_1793626687224.jpg"
G30 = BRAIN_DIR / "story30_grid_1793626682455.jpg"
G27_OUT = BRAIN_DIR / "story27_grid_composite.jpg"


def build_story27_grid() -> Path:
    """Create a 2x2 grid for Story 27 from reframed watercolor crops of G28 & G29."""
    im28 = Image.open(G28).convert("RGB")
    im29 = Image.open(G29).convert("RGB")
    w, h = im28.size
    hw, hh = w // 2, h // 2

    # Panel 1: Close-up of Mei transforming in pink smoke (from G28 top-left center crop)
    p1_raw = im28.crop((int(hw * 0.16), int(hh * 0.08), int(hw * 0.88), int(hh * 0.96)))
    p1 = ImageEnhance.Color(p1_raw.resize((hw, hh), Image.Resampling.LANCZOS)).enhance(1.12)

    # Panel 2: Giant fluffy red panda indoors with big bushy tail (from G29 top-right mirrored & zoomed)
    p2_raw = ImageOps.mirror(im29.crop((hw + int(hw * 0.05), int(hh * 0.05), w - int(hw * 0.03), int(hh * 0.95))))
    p2 = ImageEnhance.Warmth(p2_raw.resize((hw, hh), Image.Resampling.LANCZOS)) if hasattr(ImageEnhance, "Warmth") else p2_raw.resize((hw, hh), Image.Resampling.LANCZOS)

    # Panel 3: Red panda behind the bedroom doorway (from G29 bottom-left right-side crop Focusing on panda at door)
    p3_raw = im29.crop((int(hw * 0.22), hh + int(hh * 0.06), int(hw * 0.96), h - int(hh * 0.04)))
    p3 = p3_raw.resize((hw, hh), Image.Resampling.LANCZOS)

    # Panel 4: Glowing pink sparkles transformation back into Mei with red glasses (from G28 bottom-right center crop)
    p4_raw = im28.crop((hw + int(hw * 0.14), hh + int(hh * 0.04), w - int(hw * 0.14), h - int(hh * 0.06)))
    p4 = p4_raw.resize((hw, hh), Image.Resampling.LANCZOS)

    grid = Image.new("RGB", (w, h), (255, 255, 255))
    grid.paste(p1, (0, 0))
    grid.paste(p2, (hw, 0))
    grid.paste(p3, (0, hh))
    grid.paste(p4, (hw, hh))
    grid.save(G27_OUT, format="JPEG", quality=92)
    return G27_OUT


def main() -> None:
    g27 = build_story27_grid()
    grid_files = {
        27: g27,
        28: G28,
        29: G29,
        30: G30,
    }

    assets = {}
    for sid, gpath in grid_files.items():
        b_url, p_urls = extract_story_images(gpath, quality=80)
        assets[sid] = (b_url, p_urls)
        print(f"Story {sid}: banner={len(b_url)} chars, panels={[len(u) for u in p_urls]}")

    s27_b, s27_p = assets[27]
    s28_b, s28_p = assets[28]
    s29_b, s29_p = assets[29]
    s30_b, s30_p = assets[30]

    new_stories_js = f"""  }},
  {{
    id: 27,
    category: "redpanda",
    icon: "🐼",
    title: "27. 一激动就变红熊猫！",
    titleText: "一激动就变红熊猫！",
    titlePinyin: "yì jī dòng jiù biàn hóng xióng māo",
    titleRuby: `<span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>激<rt>jī</rt></ruby><ruby>动<rt>dòng</rt></ruby></span><span class="word-group"><ruby>就<rt>jiù</rt></ruby><ruby>变<rt>biàn</rt></ruby></span><span class="word-group"><ruby>红<rt>hóng</rt></ruby><ruby>熊<rt>xióng</rt></ruby><ruby>猫<rt>māo</rt></ruby></span><span class="punct">！</span>`,
    titleEn: "Poof! Turning into a Giant Red Panda!",
    titleEnHtml: `<span class="en-word-group">Poof!</span> <span class="en-word-group">Turning into</span> <span class="en-word-group">a Giant</span> <span class="en-word-group">Red Panda!</span>`,
    subtitle: "变身红熊猫 第1集 · 4 句 · 奇幻成长",
    bannerImg: "{s27_b}",
    sentences: [
      {{
        img: "{s27_p[0]}",
        text: "早上起床照镜子，美美一激动，“砰”的一声变成了巨大的红熊猫！",
        ruby: `<span class="word-group"><ruby>早<rt>zǎo</rt></ruby><ruby>上<rt>shang</rt></ruby></span><span class="word-group"><ruby>起<rt>qǐ</rt></ruby><ruby>床<rt>chuáng</rt></ruby></span><span class="word-group"><ruby>照<rt>zhào</rt></ruby><ruby>镜<rt>jìng</rt></ruby><ruby>子<rt>zi</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>美<rt>měi</rt></ruby><ruby>美<rt>měi</rt></ruby></span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>激<rt>jī</rt></ruby><ruby>动<rt>dòng</rt></ruby></span><span class="punct">，“</span><span class="word-group"><ruby>砰<rt>pēng</rt></ruby></span><span class="punct">”</span><span class="word-group"><ruby>的<rt>de</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>声<rt>shēng</rt></ruby></span><span class="word-group"><ruby>变<rt>biàn</rt></ruby><ruby>成<rt>chéng</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>巨<rt>jù</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>红<rt>hóng</rt></ruby><ruby>熊<rt>xióng</rt></ruby><ruby>猫<rt>māo</rt></ruby></span><span class="punct">！</span>`,
        en: "Looking in the mirror after waking up, Mei got excited and POOF—turned into a giant red panda!",
        enHtml: `<span class="en-word-group">Looking in the mirror</span> <span class="en-word-group">after waking up,</span> <span class="en-word-group">Mei got excited</span> <span class="en-word-group">and POOF—turned into</span> <span class="en-word-group">a giant red panda!</span>`
      }},
      {{
        img: "{s27_p[1]}",
        text: "她毛茸茸的大尾巴把房间里的闹钟和书本全都扫到了地上。",
        ruby: `<span class="word-group"><ruby>她<rt>tā</rt></ruby></span><span class="word-group"><ruby>毛<rt>máo</rt></ruby><ruby>茸<rt>róng</rt></ruby><ruby>茸<rt>róng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>尾<rt>wěi</rt></ruby><ruby>巴<rt>ba</rt></ruby></span><span class="word-group"><ruby>把<rt>bǎ</rt></ruby><ruby>房<rt>fáng</rt></ruby><ruby>间<rt>jiān</rt></ruby><ruby>里<rt>lǐ</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>闹<rt>nào</rt></ruby><ruby>钟<rt>zhōng</rt></ruby></span><span class="word-group"><ruby>和<rt>hé</rt></ruby><ruby>书<rt>shū</rt></ruby><ruby>本<rt>běn</rt></ruby></span><span class="word-group"><ruby>全<rt>quán</rt></ruby><ruby>都<rt>dōu</rt></ruby></span><span class="word-group"><ruby>扫<rt>sǎo</rt></ruby><ruby>到<rt>dào</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>地<rt>dì</rt></ruby><ruby>上<rt>shang</rt></ruby></span><span class="punct">。</span>`,
        en: "Her big fluffy tail swept the alarm clock and books in her room right onto the floor.",
        enHtml: `<span class="en-word-group">Her big fluffy tail</span> <span class="en-word-group">swept the alarm clock</span> <span class="en-word-group">and books in her room</span> <span class="en-word-group">right onto the floor.</span>`
      }},
      {{
        img: "{s27_p[2]}",
        text: "妈妈在门外敲门，美美赶紧深呼吸，心里默念“冷静、冷静”！",
        ruby: `<span class="word-group"><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby></span><span class="word-group"><ruby>在<rt>zài</rt></ruby><ruby>门<rt>mén</rt></ruby><ruby>外<rt>wài</rt></ruby></span><span class="word-group"><ruby>敲<rt>qiāo</rt></ruby><ruby>门<rt>mén</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>美<rt>měi</rt></ruby><ruby>美<rt>měi</rt></ruby></span><span class="word-group"><ruby>赶<rt>gǎn</rt></ruby><ruby>紧<rt>jǐn</rt></ruby></span><span class="word-group"><ruby>深<rt>shēn</rt></ruby><ruby>呼<rt>hū</rt></ruby><ruby>吸<rt>xī</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>心<rt>xīn</rt></ruby><ruby>里<rt>lǐ</rt></ruby><ruby>默<rt>mò</rt></ruby><ruby>念<rt>niàn</rt></ruby></span><span class="punct">“</span><span class="word-group"><ruby>冷<rt>lěng</rt></ruby><ruby>静<rt>jìng</rt></ruby></span><span class="punct">、</span><span class="word-group"><ruby>冷<rt>lěng</rt></ruby><ruby>静<rt>jìng</rt></ruby></span><span class="punct">”！</span>`,
        en: 'Mom knocked outside the door, so Mei quickly took a deep breath and silently chanted, "Calm down, calm down!"',
        enHtml: `<span class="en-word-group">Mom knocked</span> <span class="en-word-group">outside the door,</span> <span class="en-word-group">so Mei quickly took a deep breath</span> <span class="en-word-group">and silently chanted,</span> <span class="en-word-group">"Calm down, calm down!"</span>`
      }},
      {{
        img: "{s27_p[3]}",
        text: "一团粉红色的烟雾散开，她终于变回了戴红眼镜的小女孩！",
        ruby: `<span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>团<rt>tuán</rt></ruby></span><span class="word-group"><ruby>粉<rt>fěn</rt></ruby><ruby>红<rt>hóng</rt></ruby><ruby>色<rt>sè</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>烟<rt>yān</rt></ruby><ruby>雾<rt>wù</rt></ruby></span><span class="word-group"><ruby>散<rt>sàn</rt></ruby><ruby>开<rt>kāi</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>她<rt>tā</rt></ruby><ruby>终<rt>zhōng</rt></ruby><ruby>于<rt>yú</rt></ruby></span><span class="word-group"><ruby>变<rt>biàn</rt></ruby><ruby>回<rt>huí</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>戴<rt>dài</rt></ruby><ruby>红<rt>hóng</rt></ruby><ruby>眼<rt>yǎn</rt></ruby><ruby>镜<rt>jìng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>女<rt>nǚ</rt></ruby><ruby>孩<rt>hái</rt></ruby></span><span class="punct">！</span>`,
        en: "A puff of pink smoke cleared, and she finally turned back into a little girl wearing red glasses!",
        enHtml: `<span class="en-word-group">A puff of pink smoke</span> <span class="en-word-group">cleared,</span> <span class="en-word-group">and she finally turned back</span> <span class="en-word-group">into a little girl</span> <span class="en-word-group">wearing red glasses!</span>`
      }}
    ],
    vocab: [
      {{ hz: "激动", py: "jī dòng", en: "excited" }},
      {{ hz: "红熊猫", py: "hóng xióng māo", en: "red panda" }},
      {{ hz: "深呼吸", py: "shēn hū xī", en: "deep breath" }},
      {{ hz: "冷静", py: "lěng jìng", en: "calm down" }}
    ]
  }},
  {{
    id: 28,
    category: "redpanda",
    icon: "🧡",
    title: "28. 操场上的毛茸茸大抱抱",
    titleText: "操场上的毛茸茸大抱抱",
    titlePinyin: "cāo chǎng shàng de máo róng róng dà bào bào",
    titleRuby: `<span class="word-group"><ruby>操<rt>cāo</rt></ruby><ruby>场<rt>chǎng</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>毛<rt>máo</rt></ruby><ruby>茸<rt>róng</rt></ruby><ruby>茸<rt>róng</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>抱<rt>bào</rt></ruby><ruby>抱<rt>bào</rt></ruby></span>`,
    titleEn: "The Fluffy Giant Hug on the Playground",
    titleEnHtml: `<span class="en-word-group">The Fluffy</span> <span class="en-word-group">Giant Hug</span> <span class="en-word-group">on the Playground</span>`,
    subtitle: "变身红熊猫 第2集 · 4 句 · 奇幻成长",
    bannerImg: "{s28_b}",
    sentences: [
      {{
        img: "{s28_p[0]}",
        text: "体育课打躲避球时，美美太想赢了，耳朵和尾巴突然冒了出来！",
        ruby: `<span class="word-group"><ruby>体<rt>tǐ</rt></ruby><ruby>育<rt>yù</rt></ruby><ruby>课<rt>kè</rt></ruby></span><span class="word-group"><ruby>打<rt>dǎ</rt></ruby><ruby>躲<rt>duǒ</rt></ruby><ruby>避<rt>bì</rt></ruby><ruby>球<rt>qiú</rt></ruby><ruby>时<rt>shí</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>美<rt>měi</rt></ruby><ruby>美<rt>měi</rt></ruby></span><span class="word-group"><ruby>太<rt>tài</rt></ruby><ruby>想<rt>xiǎng</rt></ruby><ruby>赢<rt>yíng</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>耳<rt>ěr</rt></ruby><ruby>朵<rt>duo</rt></ruby></span><span class="word-group"><ruby>和<rt>hé</rt></ruby><ruby>尾<rt>wěi</rt></ruby><ruby>巴<rt>ba</rt></ruby></span><span class="word-group"><ruby>突<rt>tū</rt></ruby><ruby>然<rt>rán</rt></ruby></span><span class="word-group"><ruby>冒<rt>mào</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>出<rt>chū</rt></ruby><ruby>来<rt>lái</rt></ruby></span><span class="punct">！</span>`,
        en: "While playing dodgeball in P.E. class, Mei wanted to win so badly that her ears and tail suddenly popped out!",
        enHtml: `<span class="en-word-group">While playing dodgeball</span> <span class="en-word-group">in P.E. class,</span> <span class="en-word-group">Mei wanted to win so badly</span> <span class="en-word-group">that her ears and tail</span> <span class="en-word-group">suddenly popped out!</span>`
      }},
      {{
        img: "{s28_p[1]}",
        text: "三个好朋友围过来，用温暖的拥抱帮她挡住了大家的视线。",
        ruby: `<span class="word-group"><ruby>三<rt>sān</rt></ruby><ruby>个<rt>gè</rt></ruby></span><span class="word-group"><ruby>好<rt>hǎo</rt></ruby><ruby>朋<rt>péng</rt></ruby><ruby>友<rt>you</rt></ruby></span><span class="word-group"><ruby>围<rt>wéi</rt></ruby><ruby>过<rt>guò</rt></ruby><ruby>来<rt>lái</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>用<rt>yòng</rt></ruby><ruby>温<rt>wēn</rt></ruby><ruby>暖<rt>nuǎn</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>拥<rt>yōng</rt></ruby><ruby>抱<rt>bào</rt></ruby></span><span class="word-group"><ruby>帮<rt>bāng</rt></ruby><ruby>她<rt>tā</rt></ruby></span><span class="word-group"><ruby>挡<rt>dǎng</rt></ruby><ruby>住<rt>zhù</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>家<rt>jiā</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>视<rt>shì</rt></ruby><ruby>线<rt>xiàn</rt></ruby></span><span class="punct">。</span>`,
        en: "Her three best friends gathered around and used a warm hug to shield her from everyone's view.",
        enHtml: `<span class="en-word-group">Her three best friends</span> <span class="en-word-group">gathered around</span> <span class="en-word-group">and used a warm hug</span> <span class="en-word-group">to shield her</span> <span class="en-word-group">from everyone's view.</span>`
      }},
      {{
        img: "{s28_p[2]}",
        text: "朋友们摸着她像云朵一样软乎乎的橘色肚皮，开心得直尖叫！",
        ruby: `<span class="word-group"><ruby>朋<rt>péng</rt></ruby><ruby>友<rt>you</rt></ruby><ruby>们<rt>men</rt></ruby></span><span class="word-group"><ruby>摸<rt>mō</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>她<rt>tā</rt></ruby></span><span class="word-group"><ruby>像<rt>xiàng</rt></ruby><ruby>云<rt>yún</rt></ruby><ruby>朵<rt>duǒ</rt></ruby><ruby>一<rt>yí</rt></ruby><ruby>样<rt>yàng</rt></ruby></span><span class="word-group"><ruby>软<rt>ruǎn</rt></ruby><ruby>乎<rt>hū</rt></ruby><ruby>乎<rt>hū</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>橘<rt>jú</rt></ruby><ruby>色<rt>sè</rt></ruby><ruby>肚<rt>dù</rt></ruby><ruby>皮<rt>pí</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>开<rt>kāi</rt></ruby><ruby>心<rt>xīn</rt></ruby><ruby>得<rt>de</rt></ruby></span><span class="word-group"><ruby>直<rt>zhí</rt></ruby><ruby>尖<rt>jiān</rt></ruby><ruby>叫<rt>jiào</rt></ruby></span><span class="punct">！</span>`,
        en: "Her friends patted her cloud-soft orange belly and squealed with delight!",
        enHtml: `<span class="en-word-group">Her friends</span> <span class="en-word-group">patted her cloud-soft</span> <span class="en-word-group">orange belly</span> <span class="en-word-group">and squealed</span> <span class="en-word-group">with delight!</span>`
      }},
      {{
        img: "{s28_p[3]}",
        text: "听到死党们哼起最喜欢的合唱歌，美美笑着缩回成普通模样。",
        ruby: `<span class="word-group"><ruby>听<rt>tīng</rt></ruby><ruby>到<rt>dào</rt></ruby></span><span class="word-group"><ruby>死<rt>sǐ</rt></ruby><ruby>党<rt>dǎng</rt></ruby><ruby>们<rt>men</rt></ruby></span><span class="word-group"><ruby>哼<rt>hēng</rt></ruby><ruby>起<rt>qǐ</rt></ruby></span><span class="word-group"><ruby>最<rt>zuì</rt></ruby><ruby>喜<rt>xǐ</rt></ruby><ruby>欢<rt>huan</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>合<rt>hé</rt></ruby><ruby>唱<rt>chàng</rt></ruby><ruby>歌<rt>gē</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>美<rt>měi</rt></ruby><ruby>美<rt>měi</rt></ruby></span><span class="word-group"><ruby>笑<rt>xiào</rt></ruby><ruby>着<rt>zhe</rt></ruby></span><span class="word-group"><ruby>缩<rt>suō</rt></ruby><ruby>回<rt>huí</rt></ruby><ruby>成<rt>chéng</rt></ruby></span><span class="word-group"><ruby>普<rt>pǔ</rt></ruby><ruby>通<rt>tōng</rt></ruby><ruby>模<rt>mú</rt></ruby><ruby>样<rt>yàng</rt></ruby></span><span class="punct">。</span>`,
        en: "Hearing her besties hum their favorite choir song, Mei smiled and shrank back to her normal self.",
        enHtml: `<span class="en-word-group">Hearing her besties</span> <span class="en-word-group">hum their favorite choir song,</span> <span class="en-word-group">Mei smiled</span> <span class="en-word-group">and shrank back</span> <span class="en-word-group">to her normal self.</span>`
      }}
    ],
    vocab: [
      {{ hz: "躲避球", py: "duǒ bì qiú", en: "dodgeball" }},
      {{ hz: "拥抱", py: "yōng bào", en: "hug" }},
      {{ hz: "视线", py: "shì xiàn", en: "line of sight" }},
      {{ hz: "软乎乎", py: "ruǎn hū hū", en: "soft and fluffy" }}
    ]
  }},
  {{
    id: 29,
    category: "redpanda",
    icon: "🥟",
    title: "29. 老爸的香喷喷竹笋包",
    titleText: "老爸的香喷喷竹笋包",
    titlePinyin: "lǎo bà de xiāng pēn pēn zhú sǔn bāo",
    titleRuby: `<span class="word-group"><ruby>老<rt>lǎo</rt></ruby><ruby>爸<rt>bà</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>香<rt>xiāng</rt></ruby><ruby>喷<rt>pēn</rt></ruby><ruby>喷<rt>pēn</rt></ruby></span><span class="word-group"><ruby>竹<rt>zhú</rt></ruby><ruby>笋<rt>sǔn</rt></ruby><ruby>包<rt>bāo</rt></ruby></span>`,
    titleEn: "Dad's Fragrant Bamboo Shoot Buns",
    titleEnHtml: `<span class="en-word-group">Dad's</span> <span class="en-word-group">Fragrant</span> <span class="en-word-group">Bamboo Shoot</span> <span class="en-word-group">Buns</span>`,
    subtitle: "变身红熊猫 第3集 · 4 句 · 奇幻成长",
    bannerImg: "{s29_b}",
    sentences: [
      {{
        img: "{s29_p[0]}",
        text: "放学回家肚子咕咕叫，厨房里飘来老爸蒸竹笋包子的香味。",
        ruby: `<span class="word-group"><ruby>放<rt>fàng</rt></ruby><ruby>学<rt>xué</rt></ruby><ruby>回<rt>huí</rt></ruby><ruby>家<rt>jiā</rt></ruby></span><span class="word-group"><ruby>肚<rt>dù</rt></ruby><ruby>子<rt>zi</rt></ruby></span><span class="word-group"><ruby>咕<rt>gū</rt></ruby><ruby>咕<rt>gū</rt></ruby><ruby>叫<rt>jiào</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>厨<rt>chú</rt></ruby><ruby>房<rt>fáng</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="word-group"><ruby>飘<rt>piāo</rt></ruby><ruby>来<rt>lái</rt></ruby></span><span class="word-group"><ruby>老<rt>lǎo</rt></ruby><ruby>爸<rt>bà</rt></ruby></span><span class="word-group"><ruby>蒸<rt>zhēng</rt></ruby><ruby>竹<rt>zhú</rt></ruby><ruby>笋<rt>sǔn</rt></ruby><ruby>包<rt>bāo</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>香<rt>xiāng</rt></ruby><ruby>味<rt>wèi</rt></ruby></span><span class="punct">。</span>`,
        en: "Coming home from school with a rumbling tummy, the aroma of Dad's steamed bamboo-shoot buns drifted from the kitchen.",
        enHtml: `<span class="en-word-group">Coming home from school</span> <span class="en-word-group">with a rumbling tummy,</span> <span class="en-word-group">the aroma of Dad's</span> <span class="en-word-group">steamed bamboo-shoot buns</span> <span class="en-word-group">drifted from the kitchen.</span>`
      }},
      {{
        img: "{s29_p[1]}",
        text: "美美一闻到香味就变成大红熊猫，把头卡在了厨房推拉门里！",
        ruby: `<span class="word-group"><ruby>美<rt>měi</rt></ruby><ruby>美<rt>měi</rt></ruby></span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>闻<rt>wén</rt></ruby><ruby>到<rt>dào</rt></ruby><ruby>香<rt>xiāng</rt></ruby><ruby>味<rt>wèi</rt></ruby></span><span class="word-group"><ruby>就<rt>jiù</rt></ruby><ruby>变<rt>biàn</rt></ruby><ruby>成<rt>chéng</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>红<rt>hóng</rt></ruby><ruby>熊<rt>xióng</rt></ruby><ruby>猫<rt>māo</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>把<rt>bǎ</rt></ruby><ruby>头<rt>tóu</rt></ruby></span><span class="word-group"><ruby>卡<rt>kǎ</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>厨<rt>chú</rt></ruby><ruby>房<rt>fáng</rt></ruby></span><span class="word-group"><ruby>推<rt>tuī</rt></ruby><ruby>拉<rt>lā</rt></ruby><ruby>门<rt>mén</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="punct">！</span>`,
        en: "As soon as Mei smelled the fragrance, she turned into a giant red panda and got her head stuck in the kitchen sliding door!",
        enHtml: `<span class="en-word-group">As soon as Mei</span> <span class="en-word-group">smelled the fragrance,</span> <span class="en-word-group">she turned into a giant red panda</span> <span class="en-word-group">and got her head stuck</span> <span class="en-word-group">in the kitchen sliding door!</span>`
      }},
      {{
        img: "{s29_p[2]}",
        text: "温柔的老爸一点也不害怕，笑着端来一整笼热腾腾的大包子。",
        ruby: `<span class="word-group"><ruby>温<rt>wēn</rt></ruby><ruby>柔<rt>róu</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>老<rt>lǎo</rt></ruby><ruby>爸<rt>bà</rt></ruby></span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>点<rt>diǎn</rt></ruby><ruby>也<rt>yě</rt></ruby><ruby>不<rt>bú</rt></ruby><ruby>害<rt>hài</rt></ruby><ruby>怕<rt>pà</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>笑<rt>xiào</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>端<rt>duān</rt></ruby><ruby>来<rt>lái</rt></ruby></span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>整<rt>zhěng</rt></ruby><ruby>笼<rt>lóng</rt></ruby></span><span class="word-group"><ruby>热<rt>rè</rt></ruby><ruby>腾<rt>téng</rt></ruby><ruby>腾<rt>téng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>包<rt>bāo</rt></ruby><ruby>子<rt>zi</rt></ruby></span><span class="punct">。</span>`,
        en: "Gentle Dad wasn't scared at all and smilingly brought over a whole steamer basket of piping-hot buns.",
        enHtml: `<span class="en-word-group">Gentle Dad</span> <span class="en-word-group">wasn't scared at all</span> <span class="en-word-group">and smilingly brought over</span> <span class="en-word-group">a whole steamer basket</span> <span class="en-word-group">of piping-hot buns.</span>`
      }},
      {{
        img: "{s29_p[3]}",
        text: "红熊猫美美一口一个大包子，幸福地晃着两只毛茸茸的圆耳朵！",
        ruby: `<span class="word-group"><ruby>红<rt>hóng</rt></ruby><ruby>熊<rt>xióng</rt></ruby><ruby>猫<rt>māo</rt></ruby><ruby>美<rt>měi</rt></ruby><ruby>美<rt>měi</rt></ruby></span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>口<rt>kǒu</rt></ruby><ruby>一<rt>yí</rt></ruby><ruby>个<rt>gè</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>包<rt>bāo</rt></ruby><ruby>子<rt>zi</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>幸<rt>xìng</rt></ruby><ruby>福<rt>fú</rt></ruby><ruby>地<rt>de</rt></ruby></span><span class="word-group"><ruby>晃<rt>huàng</rt></ruby><ruby>着<rt>zhe</rt></ruby></span><span class="word-group"><ruby>两<rt>liǎng</rt></ruby><ruby>只<rt>zhī</rt></ruby></span><span class="word-group"><ruby>毛<rt>máo</rt></ruby><ruby>茸<rt>róng</rt></ruby><ruby>茸<rt>róng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>圆<rt>yuán</rt></ruby><ruby>耳<rt>ěr</rt></ruby><ruby>朵<rt>duo</rt></ruby></span><span class="punct">！</span>`,
        en: "Red Panda Mei gobbled up the big buns one by one, happily wiggling her two fluffy round ears!",
        enHtml: `<span class="en-word-group">Red Panda Mei</span> <span class="en-word-group">gobbled up the big buns</span> <span class="en-word-group">one by one,</span> <span class="en-word-group">happily wiggling</span> <span class="en-word-group">her two fluffy round ears!</span>`
      }}
    ],
    vocab: [
      {{ hz: "竹笋", py: "zhú sǔn", en: "bamboo shoot" }},
      {{ hz: "蒸笼", py: "zhēng lóng", en: "steamer basket" }},
      {{ hz: "温柔", py: "wēn róu", en: "gentle" }},
      {{ hz: "热腾腾", py: "rè téng téng", en: "piping hot" }}
    ]
  }},
  {{
    id: 30,
    category: "redpanda",
    icon: "🌕",
    title: "30. 红月之夜的古庙合唱",
    titleText: "红月之夜的古庙合唱",
    titlePinyin: "hóng yuè zhī yè de gǔ miào hé chàng",
    titleRuby: `<span class="word-group"><ruby>红<rt>hóng</rt></ruby><ruby>月<rt>yuè</rt></ruby><ruby>之<rt>zhī</rt></ruby><ruby>夜<rt>yè</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>古<rt>gǔ</rt></ruby><ruby>庙<rt>miào</rt></ruby></span><span class="word-group"><ruby>合<rt>hé</rt></ruby><ruby>唱<rt>chàng</rt></ruby></span>`,
    titleEn: "The Red Moon Night Temple Choir",
    titleEnHtml: `<span class="en-word-group">The Red Moon</span> <span class="en-word-group">Night</span> <span class="en-word-group">Temple Choir</span>`,
    subtitle: "变身红熊猫 第4集 · 4 句 · 奇幻成长",
    bannerImg: "{s30_b}",
    sentences: [
      {{
        img: "{s30_p[0]}",
        text: "红月升起的夜晚，全家人来到挂满红灯笼的祠堂准备仪式。",
        ruby: `<span class="word-group"><ruby>红<rt>hóng</rt></ruby><ruby>月<rt>yuè</rt></ruby></span><span class="word-group"><ruby>升<rt>shēng</rt></ruby><ruby>起<rt>qǐ</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>夜<rt>yè</rt></ruby><ruby>晚<rt>wǎn</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>全<rt>quán</rt></ruby><ruby>家<rt>jiā</rt></ruby><ruby>人<rt>rén</rt></ruby></span><span class="word-group"><ruby>来<rt>lái</rt></ruby><ruby>到<rt>dào</rt></ruby></span><span class="word-group"><ruby>挂<rt>guà</rt></ruby><ruby>满<rt>mǎn</rt></ruby><ruby>红<rt>hóng</rt></ruby><ruby>灯<rt>dēng</rt></ruby><ruby>笼<rt>long</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>祠<rt>cí</rt></ruby><ruby>堂<rt>táng</rt></ruby></span><span class="word-group"><ruby>准<rt>zhǔn</rt></ruby><ruby>备<rt>bèi</rt></ruby><ruby>仪<rt>yí</rt></ruby><ruby>式<rt>shì</rt></ruby></span><span class="punct">。</span>`,
        en: "On the night the red moon rose, the whole family came to the ancestral temple hung with red lanterns to prepare the ceremony.",
        enHtml: `<span class="en-word-group">On the night</span> <span class="en-word-group">the red moon rose,</span> <span class="en-word-group">the whole family came to</span> <span class="en-word-group">the ancestral temple hung with red lanterns</span> <span class="en-word-group">to prepare the ceremony.</span>`
      }},
      {{
        img: "{s30_p[1]}",
        text: "外婆和阿姨们敲起大鼓，唱起了古老又温暖的平安歌谣。",
        ruby: `<span class="word-group"><ruby>外<rt>wài</rt></ruby><ruby>婆<rt>pó</rt></ruby></span><span class="word-group"><ruby>和<rt>hé</rt></ruby><ruby>阿<rt>ā</rt></ruby><ruby>姨<rt>yí</rt></ruby><ruby>们<rt>men</rt></ruby></span><span class="word-group"><ruby>敲<rt>qiāo</rt></ruby><ruby>起<rt>qǐ</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>鼓<rt>gǔ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>唱<rt>chàng</rt></ruby><ruby>起<rt>qǐ</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>古<rt>gǔ</rt></ruby><ruby>老<rt>lǎo</rt></ruby><ruby>又<rt>yòu</rt></ruby><ruby>温<rt>wēn</rt></ruby><ruby>暖<rt>nuǎn</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>平<rt>píng</rt></ruby><ruby>安<rt>ān</rt></ruby><ruby>歌<rt>gē</rt></ruby><ruby>谣<rt>yáo</rt></ruby></span><span class="punct">。</span>`,
        en: "Grandma and the aunts beat the big drum and sang an ancient, warm song of peace.",
        enHtml: `<span class="en-word-group">Grandma and the aunts</span> <span class="en-word-group">beat the big drum</span> <span class="en-word-group">and sang</span> <span class="en-word-group">an ancient, warm</span> <span class="en-word-group">song of peace.</span>`
      }},
      {{
        img: "{s30_p[2]}",
        text: "大红熊猫美美在月光下高高跃起，带着妈妈一起在云朵间飞翔！",
        ruby: `<span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>红<rt>hóng</rt></ruby><ruby>熊<rt>xióng</rt></ruby><ruby>猫<rt>māo</rt></ruby><ruby>美<rt>měi</rt></ruby><ruby>美<rt>měi</rt></ruby></span><span class="word-group"><ruby>在<rt>zài</rt></ruby><ruby>月<rt>yuè</rt></ruby><ruby>光<rt>guāng</rt></ruby><ruby>下<rt>xià</rt></ruby></span><span class="word-group"><ruby>高<rt>gāo</rt></ruby><ruby>高<rt>gāo</rt></ruby><ruby>跃<rt>yuè</rt></ruby><ruby>起<rt>qǐ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>带<rt>dài</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby></span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>起<rt>qǐ</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>云<rt>yún</rt></ruby><ruby>朵<rt>duǒ</rt></ruby><ruby>间<rt>jiān</rt></ruby></span><span class="word-group"><ruby>飞<rt>fēi</rt></ruby><ruby>翔<rt>xiáng</rt></ruby></span><span class="punct">！</span>`,
        en: "Giant Red Panda Mei leaped high under the moonlight, carrying Mom to soar among the clouds!",
        enHtml: `<span class="en-word-group">Giant Red Panda Mei</span> <span class="en-word-group">leaped high</span> <span class="en-word-group">under the moonlight,</span> <span class="en-word-group">carrying Mom</span> <span class="en-word-group">to soar among the clouds!</span>`
      }},
      {{
        img: "{s30_p[3]}",
        text: "她学会了接纳这股神奇的熊猫力量，全家人紧紧拥抱在一起！",
        ruby: `<span class="word-group"><ruby>她<rt>tā</rt></ruby><ruby>学<rt>xué</rt></ruby><ruby>会<rt>huì</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>接<rt>jiē</rt></ruby><ruby>纳<rt>nà</rt></ruby></span><span class="word-group"><ruby>这<rt>zhè</rt></ruby><ruby>股<rt>gǔ</rt></ruby><ruby>神<rt>shén</rt></ruby><ruby>奇<rt>qí</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>熊<rt>xióng</rt></ruby><ruby>猫<rt>māo</rt></ruby><ruby>力<rt>lì</rt></ruby><ruby>量<rt>liàng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>全<rt>quán</rt></ruby><ruby>家<rt>jiā</rt></ruby><ruby>人<rt>rén</rt></ruby></span><span class="word-group"><ruby>紧<rt>jǐn</rt></ruby><ruby>紧<rt>jǐn</rt></ruby></span><span class="word-group"><ruby>拥<rt>yōng</rt></ruby><ruby>抱<rt>bào</rt></ruby><ruby>在<rt>zài</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>起<rt>qǐ</rt></ruby></span><span class="punct">！</span>`,
        en: "She learned to embrace this magical panda power, and the whole family hugged each other tightly!",
        enHtml: `<span class="en-word-group">She learned to embrace</span> <span class="en-word-group">this magical panda power,</span> <span class="en-word-group">and the whole family</span> <span class="en-word-group">hugged each other tightly!</span>`
      }}
    ],
    vocab: [
      {{ hz: "红月", py: "hóng yuè", en: "red moon" }},
      {{ hz: "祠堂", py: "cí táng", en: "ancestral temple" }},
      {{ hz: "歌谣", py: "gē yáo", en: "folk song" }},
      {{ hz: "接纳", py: "jiē nà", en: "accept and embrace" }}
    ]
  }}
];"""

    html = INDEX_PATH.read_text(encoding="utf-8")

    target_end = """      { hz: "银河", py: "yín hé", en: "Milky Way" },
      { hz: "睡袋", py: "shuì dài", en: "sleeping bag" }
    ]
  }
];"""

    assert target_end in html, "Could not find end of Story 26 in index.html"
    html = html.replace(
        target_end,
        """      { hz: "银河", py: "yín hé", en: "Milky Way" },
      { hz: "睡袋", py: "shuì dài", en: "sleeping bag" }
    ]
"""
        + new_stories_js,
        1,
    )

    old_categories = """const CATEGORIES = [
  { id: 'all', label: '✨ 全部故事 · All (26)' },
  { id: 'bluepup', label: '🐾 蓝小狗一家 · Blue Pup (4)' },
  { id: 'dogcop', label: '🐶 神探汪汪 · Dog Cop (4)' },
  { id: 'weird', label: '🤪 疯狂学校 · My Weird School (4)' },
  { id: 'adventure', label: '🕵️ 脑洞探秘 · Mystery & Sci-Fi (2)' },
  { id: 'school', label: '🏫 校园日常 · School Life (4)' },
  { id: 'fairy', label: '🐾 童话绘本 · Animal Tales (8)' }
];"""

    new_categories = """const CATEGORIES = [
  { id: 'all', label: '✨ 全部故事 · All (30)' },
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
    print("Successfully updated index.html with Turning Red Stories 27-30 and updated CATEGORIES!")


if __name__ == "__main__":
    main()
