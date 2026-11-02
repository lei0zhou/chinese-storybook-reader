import base64
import io
import os
import re
from PIL import Image

BRAIN_DIR = "/Users/leizhou/.gemini/antigravity-cli/brain/dde92688-d628-4cf6-9d61-3d1a08abad1b"
INDEX_PATH = "/Users/leizhou/Downloads/chinese-storybook-reader/index.html"

GRID_FILES = {
    19: os.path.join(BRAIN_DIR, "story19_grid_1793625765389.jpg"),
    20: os.path.join(BRAIN_DIR, "story20_grid_1793625760926.jpg"),
    21: os.path.join(BRAIN_DIR, "story21_grid_1793625783320.jpg"),
    22: os.path.join(BRAIN_DIR, "story22_grid_1793625802362.jpg"),
}

def img_to_webp_data_url(pil_img, quality=80):
    buf = io.BytesIO()
    pil_img.save(buf, format="WEBP", quality=quality, method=6)
    b64 = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/webp;base64,{b64}"

def crop_4_3(pil_img):
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

def make_banner_from_panels(p1, p2):
    # Create a 640x240 panoramic banner by blending p1 (left 330px) and p2 (right 330px) with a smooth 20px crossfade in the center
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

def extract_story_images(grid_path):
    im = Image.open(grid_path).convert("RGB")
    w, h = im.size
    mx = int(w * 0.025)
    my = int(h * 0.025)
    cx = int(w * 0.018)
    cy = int(h * 0.018)
    mid_x = w // 2
    mid_y = h // 2

    boxes = [
        (mx, my, mid_x - cx, mid_y - cy),          # Top-Left (Panel 1)
        (mid_x + cx, my, w - mx, mid_y - cy),      # Top-Right (Panel 2)
        (mx, mid_y + cy, mid_x - cx, h - my),      # Bottom-Left (Panel 3)
        (mid_x + cx, mid_y + cy, w - mx, h - my),  # Bottom-Right (Panel 4)
    ]
    panels = [crop_4_3(im.crop(b)) for b in boxes]
    banner = make_banner_from_panels(panels[0], panels[1])
    return img_to_webp_data_url(banner, quality=80), [img_to_webp_data_url(p, quality=80) for p in panels]

assets = {}
for sid, gpath in GRID_FILES.items():
    banner_url, panel_urls = extract_story_images(gpath)
    assets[sid] = (banner_url, panel_urls)
    print(f"Story {sid}: banner={len(banner_url)} chars, panels={[len(u) for u in panel_urls]}")

s19_b, s19_p = assets[19]
s20_b, s20_p = assets[20]
s21_b, s21_p = assets[21]
s22_b, s22_p = assets[22]

new_stories_js = f"""  }},
  {{
    id: 19,
    category: "dogcop",
    icon: "🐶",
    title: "19. 神探汪汪与坏蛋橘猫",
    titleText: "神探汪汪与坏蛋橘猫",
    titlePinyin: "shén tàn wāng wāng yǔ huài dàn jú māo",
    titleRuby: `<span class="word-group"><ruby>神<rt>shén</rt></ruby><ruby>探<rt>tàn</rt></ruby></span><span class="word-group"><ruby>汪<rt>wāng</rt></ruby><ruby>汪<rt>wāng</rt></ruby></span><span class="word-group"><ruby>与<rt>yǔ</rt></ruby></span><span class="word-group"><ruby>坏<rt>huài</rt></ruby><ruby>蛋<rt>dàn</rt></ruby></span><span class="word-group"><ruby>橘<rt>jú</rt></ruby><ruby>猫<rt>māo</rt></ruby></span>`,
    titleEn: "Dog Cop and the Villain Orange Cat",
    titleEnHtml: `<span class="en-word-group">Dog Cop</span> <span class="en-word-group">and</span> <span class="en-word-group">the Villain</span> <span class="en-word-group">Orange Cat</span>`,
    subtitle: "神探汪汪 第1集 · 4 句 · 爆笑漫画",
    bannerImg: "{s19_b}",
    sentences: [
      {{
        img: "{s19_p[0]}",
        text: "神探汪汪戴着蓝色警帽，他是全城最勇敢的狗狗警察！",
        ruby: `<span class="word-group"><ruby>神<rt>shén</rt></ruby><ruby>探<rt>tàn</rt></ruby></span><span class="word-group"><ruby>汪<rt>wāng</rt></ruby><ruby>汪<rt>wāng</rt></ruby></span><span class="word-group"><ruby>戴<rt>dài</rt></ruby><ruby>着<rt>zhe</rt></ruby></span><span class="word-group"><ruby>蓝<rt>lán</rt></ruby><ruby>色<rt>sè</rt></ruby></span><span class="word-group"><ruby>警<rt>jǐng</rt></ruby><ruby>帽<rt>mào</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>他<rt>tā</rt></ruby><ruby>是<rt>shì</rt></ruby></span><span class="word-group"><ruby>全<rt>quán</rt></ruby><ruby>城<rt>chéng</rt></ruby></span><span class="word-group"><ruby>最<rt>zuì</rt></ruby><ruby>勇<rt>yǒng</rt></ruby><ruby>敢<rt>gǎn</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>狗<rt>gǒu</rt></ruby><ruby>狗<rt>gou</rt></ruby></span><span class="word-group"><ruby>警<rt>jǐng</rt></ruby><ruby>察<rt>chá</rt></ruby></span><span class="punct">！</span>`,
        en: "Dog Cop wears a blue police cap; he is the bravest doggy police officer in the whole city!",
        enHtml: `<span class="en-word-group">Dog Cop</span> <span class="en-word-group">wears</span> <span class="en-word-group">a blue police cap;</span> <span class="en-word-group">he is</span> <span class="en-word-group">the bravest</span> <span class="en-word-group">doggy police officer</span> <span class="en-word-group">in the whole city!</span>`
      }},
      {{
        img: "{s19_p[1]}",
        text: "坏蛋橘猫造了一台吸尘器坦克，想把全城的骨头都吸走。",
        ruby: `<span class="word-group"><ruby>坏<rt>huài</rt></ruby><ruby>蛋<rt>dàn</rt></ruby></span><span class="word-group"><ruby>橘<rt>jú</rt></ruby><ruby>猫<rt>māo</rt></ruby></span><span class="word-group"><ruby>造<rt>zào</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>台<rt>tái</rt></ruby></span><span class="word-group"><ruby>吸<rt>xī</rt></ruby><ruby>尘<rt>chén</rt></ruby><ruby>器<rt>qì</rt></ruby></span><span class="word-group"><ruby>坦<rt>tǎn</rt></ruby><ruby>克<rt>kè</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>想<rt>xiǎng</rt></ruby><ruby>把<rt>bǎ</rt></ruby></span><span class="word-group"><ruby>全<rt>quán</rt></ruby><ruby>城<rt>chéng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>骨<rt>gǔ</rt></ruby><ruby>头<rt>tou</rt></ruby></span><span class="word-group"><ruby>都<rt>dōu</rt></ruby><ruby>吸<rt>xī</rt></ruby><ruby>走<rt>zǒu</rt></ruby></span><span class="punct">。</span>`,
        en: "Villain Orange Cat built a vacuum cleaner tank to suck up all the bones in the city.",
        enHtml: `<span class="en-word-group">Villain Orange Cat</span> <span class="en-word-group">built</span> <span class="en-word-group">a vacuum cleaner tank</span> <span class="en-word-group">to suck up</span> <span class="en-word-group">all the bones</span> <span class="en-word-group">in the city.</span>`
      }},
      {{
        img: "{s19_p[2]}",
        text: "汪汪闻着香肠味追上去，却不小心扑倒了市长先生舔了三口！",
        ruby: `<span class="word-group"><ruby>汪<rt>wāng</rt></ruby><ruby>汪<rt>wāng</rt></ruby></span><span class="word-group"><ruby>闻<rt>wén</rt></ruby><ruby>着<rt>zhe</rt></ruby></span><span class="word-group"><ruby>香<rt>xiāng</rt></ruby><ruby>肠<rt>cháng</rt></ruby><ruby>味<rt>wèi</rt></ruby></span><span class="word-group"><ruby>追<rt>zhuī</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>去<rt>qù</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>却<rt>què</rt></ruby></span><span class="word-group"><ruby>不<rt>bù</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>心<rt>xīn</rt></ruby></span><span class="word-group"><ruby>扑<rt>pū</rt></ruby><ruby>倒<rt>dǎo</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>市<rt>shì</rt></ruby><ruby>长<rt>zhǎng</rt></ruby><ruby>先<rt>xiān</rt></ruby><ruby>生<rt>sheng</rt></ruby></span><span class="word-group"><ruby>舔<rt>tiǎn</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>三<rt>sān</rt></ruby><ruby>口<rt>kǒu</rt></ruby></span><span class="punct">！</span>`,
        en: "Dog Cop chased after the scent of sausages, but accidentally tackled Mr. Mayor and licked him three times!",
        enHtml: `<span class="en-word-group">Dog Cop</span> <span class="en-word-group">chased after</span> <span class="en-word-group">the scent of sausages,</span> <span class="en-word-group">but accidentally</span> <span class="en-word-group">tackled Mr. Mayor</span> <span class="en-word-group">and licked him</span> <span class="en-word-group">three times!</span>`
      }},
      {{
        img: "{s19_p[3]}",
        text: "他扔出一只飞盘卡住机器，坏蛋橘猫掉进了泡泡水桶里！",
        ruby: `<span class="word-group"><ruby>他<rt>tā</rt></ruby></span><span class="word-group"><ruby>扔<rt>rēng</rt></ruby><ruby>出<rt>chū</rt></ruby></span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>只<rt>zhī</rt></ruby></span><span class="word-group"><ruby>飞<rt>fēi</rt></ruby><ruby>盘<rt>pán</rt></ruby></span><span class="word-group"><ruby>卡<rt>kǎ</rt></ruby><ruby>住<rt>zhù</rt></ruby></span><span class="word-group"><ruby>机<rt>jī</rt></ruby><ruby>器<rt>qì</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>坏<rt>huài</rt></ruby><ruby>蛋<rt>dàn</rt></ruby></span><span class="word-group"><ruby>橘<rt>jú</rt></ruby><ruby>猫<rt>māo</rt></ruby></span><span class="word-group"><ruby>掉<rt>diào</rt></ruby><ruby>进<rt>jìn</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>泡<rt>pào</rt></ruby><ruby>泡<rt>pao</rt></ruby></span><span class="word-group"><ruby>水<rt>shuǐ</rt></ruby><ruby>桶<rt>tǒng</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="punct">！</span>`,
        en: "He threw a frisbee to jam the machine, and Villain Orange Cat tumbled right into a bucket of soapy bubbles!",
        enHtml: `<span class="en-word-group">He threw</span> <span class="en-word-group">a frisbee</span> <span class="en-word-group">to jam the machine,</span> <span class="en-word-group">and Villain Orange Cat</span> <span class="en-word-group">tumbled right into</span> <span class="en-word-group">a bucket of soapy bubbles!</span>`
      }}
    ],
    vocab: [
      {{ hz: "神探", py: "shén tàn", en: "super detective" }},
      {{ hz: "警帽", py: "jǐng mào", en: "police cap" }},
      {{ hz: "吸尘器", py: "xī chén qì", en: "vacuum cleaner" }},
      {{ hz: "飞盘", py: "fēi pán", en: "frisbee" }}
    ]
  }},
  {{
    id: 20,
    category: "dogcop",
    icon: "🐱",
    title: "20. 机器小猫与超级球球",
    titleText: "机器小猫与超级球球",
    titlePinyin: "jī qì xiǎo māo yǔ chāo jí qiú qiú",
    titleRuby: `<span class="word-group"><ruby>机<rt>jī</rt></ruby><ruby>器<rt>qì</rt></ruby></span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>猫<rt>māo</rt></ruby></span><span class="word-group"><ruby>与<rt>yǔ</rt></ruby></span><span class="word-group"><ruby>超<rt>chāo</rt></ruby><ruby>级<rt>jí</rt></ruby></span><span class="word-group"><ruby>球<rt>qiú</rt></ruby><ruby>球<rt>qiú</rt></ruby></span>`,
    titleEn: "Little Kitty, Robot Buddy, and the Giant Tennis Ball",
    titleEnHtml: `<span class="en-word-group">Little Kitty,</span> <span class="en-word-group">Robot Buddy,</span> <span class="en-word-group">and the Giant</span> <span class="en-word-group">Tennis Ball</span>`,
    subtitle: "神探汪汪 第2集 · 4 句 · 爆笑漫画",
    bannerImg: "{s20_b}",
    sentences: [
      {{
        img: "{s20_p[0]}",
        text: "小橘猫善良又调皮，他和铁皮机器人是神探汪汪的好帮手。",
        ruby: `<span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>橘<rt>jú</rt></ruby><ruby>猫<rt>māo</rt></ruby></span><span class="word-group"><ruby>善<rt>shàn</rt></ruby><ruby>良<rt>liáng</rt></ruby></span><span class="word-group"><ruby>又<rt>yòu</rt></ruby><ruby>调<rt>tiáo</rt></ruby><ruby>皮<rt>pí</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>他<rt>tā</rt></ruby><ruby>和<rt>hé</rt></ruby></span><span class="word-group"><ruby>铁<rt>tiě</rt></ruby><ruby>皮<rt>pí</rt></ruby></span><span class="word-group"><ruby>机<rt>jī</rt></ruby><ruby>器<rt>qì</rt></ruby><ruby>人<rt>rén</rt></ruby></span><span class="word-group"><ruby>是<rt>shì</rt></ruby></span><span class="word-group"><ruby>神<rt>shén</rt></ruby><ruby>探<rt>tàn</rt></ruby><ruby>汪<rt>wāng</rt></ruby><ruby>汪<rt>wāng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>好<rt>hǎo</rt></ruby><ruby>帮<rt>bāng</rt></ruby><ruby>手<rt>shǒu</rt></ruby></span><span class="punct">。</span>`,
        en: "Little Orange Kitty is kind and playful, and he and Tin Robot are Dog Cop's best helpers.",
        enHtml: `<span class="en-word-group">Little Orange Kitty</span> <span class="en-word-group">is kind and playful,</span> <span class="en-word-group">and he and Tin Robot</span> <span class="en-word-group">are Dog Cop's</span> <span class="en-word-group">best helpers.</span>`
      }},
      {{
        img: "{s20_p[1]}",
        text: "坏蛋博士放出了一个房子那么大的绿色网球，在街上乱蹦！",
        ruby: `<span class="word-group"><ruby>坏<rt>huài</rt></ruby><ruby>蛋<rt>dàn</rt></ruby></span><span class="word-group"><ruby>博<rt>bó</rt></ruby><ruby>士<rt>shì</rt></ruby></span><span class="word-group"><ruby>放<rt>fàng</rt></ruby><ruby>出<rt>chū</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>一<rt>yí</rt></ruby><ruby>个<rt>gè</rt></ruby></span><span class="word-group"><ruby>房<rt>fáng</rt></ruby><ruby>子<rt>zi</rt></ruby></span><span class="word-group"><ruby>那<rt>nà</rt></ruby><ruby>么<rt>me</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>绿<rt>lǜ</rt></ruby><ruby>色<rt>sè</rt></ruby></span><span class="word-group"><ruby>网<rt>wǎng</rt></ruby><ruby>球<rt>qiú</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>在<rt>zài</rt></ruby><ruby>街<rt>jiē</rt></ruby><ruby>上<rt>shàng</rt></ruby></span><span class="word-group"><ruby>乱<rt>luàn</rt></ruby><ruby>蹦<rt>bèng</rt></ruby></span><span class="punct">！</span>`,
        en: "The villain doctor unleashed a green tennis ball as big as a house, bouncing wildly down the street!",
        enHtml: `<span class="en-word-group">The villain doctor</span> <span class="en-word-group">unleashed</span> <span class="en-word-group">a green tennis ball</span> <span class="en-word-group">as big as a house,</span> <span class="en-word-group">bouncing wildly</span> <span class="en-word-group">down the street!</span>`
      }},
      {{
        img: "{s20_p[2]}",
        text: "神探汪汪一看见大球就控制不住自己，摇着尾巴飞奔过去！",
        ruby: `<span class="word-group"><ruby>神<rt>shén</rt></ruby><ruby>探<rt>tàn</rt></ruby></span><span class="word-group"><ruby>汪<rt>wāng</rt></ruby><ruby>汪<rt>wāng</rt></ruby></span><span class="word-group"><ruby>一<rt>yí</rt></ruby><ruby>看<rt>kàn</rt></ruby><ruby>见<rt>jiàn</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>球<rt>qiú</rt></ruby></span><span class="word-group"><ruby>就<rt>jiù</rt></ruby></span><span class="word-group"><ruby>控<rt>kòng</rt></ruby><ruby>制<rt>zhì</rt></ruby><ruby>不<rt>bú</rt></ruby><ruby>住<rt>zhù</rt></ruby></span><span class="word-group"><ruby>自<rt>zì</rt></ruby><ruby>己<rt>jǐ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>摇<rt>yáo</rt></ruby><ruby>着<rt>zhe</rt></ruby></span><span class="word-group"><ruby>尾<rt>wěi</rt></ruby><ruby>巴<rt>ba</rt></ruby></span><span class="word-group"><ruby>飞<rt>fēi</rt></ruby><ruby>奔<rt>bēn</rt></ruby><ruby>过<rt>guò</rt></ruby><ruby>去<rt>qù</rt></ruby></span><span class="punct">！</span>`,
        en: "As soon as Dog Cop saw the giant ball, he couldn't control himself and sprinted over wagging his tail!",
        enHtml: `<span class="en-word-group">As soon as</span> <span class="en-word-group">Dog Cop</span> <span class="en-word-group">saw the giant ball,</span> <span class="en-word-group">he couldn't control himself</span> <span class="en-word-group">and sprinted over</span> <span class="en-word-group">wagging his tail!</span>`
      }},
      {{
        img: "{s20_p[3]}",
        text: "机器人变形为超大网球拍，砰的一声把大球打飞到了外太空！",
        ruby: `<span class="word-group"><ruby>机<rt>jī</rt></ruby><ruby>器<rt>qì</rt></ruby><ruby>人<rt>rén</rt></ruby></span><span class="word-group"><ruby>变<rt>biàn</rt></ruby><ruby>形<rt>xíng</rt></ruby><ruby>为<rt>wéi</rt></ruby></span><span class="word-group"><ruby>超<rt>chāo</rt></ruby><ruby>大<rt>dà</rt></ruby></span><span class="word-group"><ruby>网<rt>wǎng</rt></ruby><ruby>球<rt>qiú</rt></ruby><ruby>拍<rt>pāi</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>砰<rt>pēng</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>声<rt>shēng</rt></ruby></span><span class="word-group"><ruby>把<rt>bǎ</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>球<rt>qiú</rt></ruby></span><span class="word-group"><ruby>打<rt>dǎ</rt></ruby><ruby>飞<rt>fēi</rt></ruby><ruby>到<rt>dào</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>外<rt>wài</rt></ruby><ruby>太<rt>tài</rt></ruby><ruby>空<rt>kōng</rt></ruby></span><span class="punct">！</span>`,
        en: "The robot transformed into a giant tennis racket and smashed the big ball all the way into outer space with a BANG!",
        enHtml: `<span class="en-word-group">The robot</span> <span class="en-word-group">transformed into</span> <span class="en-word-group">a giant tennis racket</span> <span class="en-word-group">and smashed the big ball</span> <span class="en-word-group">all the way into outer space</span> <span class="en-word-group">with a BANG!</span>`
      }}
    ],
    vocab: [
      {{ hz: "帮手", py: "bāng shǒu", en: "helper" }},
      {{ hz: "网球", py: "wǎng qiú", en: "tennis ball" }},
      {{ hz: "控制", py: "kòng zhì", en: "control" }},
      {{ hz: "太空", py: "tài kōng", en: "outer space" }}
    ]
  }},
  {{
    id: 21,
    category: "dogcop",
    icon: "🌭",
    title: "21. 会跑的热狗大盗",
    titleText: "会跑的热狗大盗",
    titlePinyin: "huì pǎo de rè gǒu dà dào",
    titleRuby: `<span class="word-group"><ruby>会<rt>huì</rt></ruby><ruby>跑<rt>pǎo</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>热<rt>rè</rt></ruby><ruby>狗<rt>gǒu</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>盗<rt>dào</rt></ruby></span>`,
    titleEn: "The Runaway Hot Dog Bandits",
    titleEnHtml: `<span class="en-word-group">The Runaway</span> <span class="en-word-group">Hot Dog</span> <span class="en-word-group">Bandits</span>`,
    subtitle: "神探汪汪 第3集 · 4 句 · 爆笑漫画",
    bannerImg: "{s21_b}",
    sentences: [
      {{
        img: "{s21_p[0]}",
        text: "坏蛋橘猫喷了复活药水，热狗车里的香肠全都长出小短腿跑啦！",
        ruby: `<span class="word-group"><ruby>坏<rt>huài</rt></ruby><ruby>蛋<rt>dàn</rt></ruby></span><span class="word-group"><ruby>橘<rt>jú</rt></ruby><ruby>猫<rt>māo</rt></ruby></span><span class="word-group"><ruby>喷<rt>pēn</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>复<rt>fù</rt></ruby><ruby>活<rt>huó</rt></ruby></span><span class="word-group"><ruby>药<rt>yào</rt></ruby><ruby>水<rt>shuǐ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>热<rt>rè</rt></ruby><ruby>狗<rt>gǒu</rt></ruby><ruby>车<rt>chē</rt></ruby><ruby>里<rt>lǐ</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>香<rt>xiāng</rt></ruby><ruby>肠<rt>cháng</rt></ruby></span><span class="word-group"><ruby>全<rt>quán</rt></ruby><ruby>都<rt>dōu</rt></ruby></span><span class="word-group"><ruby>长<rt>zhǎng</rt></ruby><ruby>出<rt>chū</rt></ruby></span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>短<rt>duǎn</rt></ruby><ruby>腿<rt>tuǐ</rt></ruby></span><span class="word-group"><ruby>跑<rt>pǎo</rt></ruby><ruby>啦<rt>la</rt></ruby></span><span class="punct">！</span>`,
        en: "Villain Orange Cat sprayed a magic potion, and all the sausages in the hot dog cart grew stubby little legs and ran away!",
        enHtml: `<span class="en-word-group">Villain Orange Cat</span> <span class="en-word-group">sprayed</span> <span class="en-word-group">a magic potion,</span> <span class="en-word-group">and all the sausages</span> <span class="en-word-group">in the hot dog cart</span> <span class="en-word-group">grew stubby little legs</span> <span class="en-word-group">and ran away!</span>`
      }},
      {{
        img: "{s21_p[1]}",
        text: "几十根热狗排着队冲进超市，把番茄酱挤得到处都是。",
        ruby: `<span class="word-group"><ruby>几<rt>jǐ</rt></ruby><ruby>十<rt>shí</rt></ruby><ruby>根<rt>gēn</rt></ruby></span><span class="word-group"><ruby>热<rt>rè</rt></ruby><ruby>狗<rt>gǒu</rt></ruby></span><span class="word-group"><ruby>排<rt>pái</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>队<rt>duì</rt></ruby></span><span class="word-group"><ruby>冲<rt>chōng</rt></ruby><ruby>进<rt>jìn</rt></ruby></span><span class="word-group"><ruby>超<rt>chāo</rt></ruby><ruby>市<rt>shì</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>把<rt>bǎ</rt></ruby></span><span class="word-group"><ruby>番<rt>fān</rt></ruby><ruby>茄<rt>qié</rt></ruby><ruby>酱<rt>jiàng</rt></ruby></span><span class="word-group"><ruby>挤<rt>jǐ</rt></ruby><ruby>得<rt>de</rt></ruby></span><span class="word-group"><ruby>到<rt>dào</rt></ruby><ruby>处<rt>chù</rt></ruby><ruby>都<rt>dōu</rt></ruby><ruby>是<rt>shì</rt></ruby></span><span class="punct">。</span>`,
        en: "Dozens of hot dogs marched in a line into the supermarket, squirting ketchup everywhere.",
        enHtml: `<span class="en-word-group">Dozens of hot dogs</span> <span class="en-word-group">marched in a line</span> <span class="en-word-group">into the supermarket,</span> <span class="en-word-group">squirting ketchup</span> <span class="en-word-group">everywhere.</span>`
      }},
      {{
        img: "{s21_p[2]}",
        text: "神探汪汪和小橘猫踩着旱冰鞋，拿着大面包夹子左右包抄！",
        ruby: `<span class="word-group"><ruby>神<rt>shén</rt></ruby><ruby>探<rt>tàn</rt></ruby><ruby>汪<rt>wāng</rt></ruby><ruby>汪<rt>wāng</rt></ruby></span><span class="word-group"><ruby>和<rt>hé</rt></ruby></span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>橘<rt>jú</rt></ruby><ruby>猫<rt>māo</rt></ruby></span><span class="word-group"><ruby>踩<rt>cǎi</rt></ruby><ruby>着<rt>zhe</rt></ruby></span><span class="word-group"><ruby>旱<rt>hàn</rt></ruby><ruby>冰<rt>bīng</rt></ruby><ruby>鞋<rt>xié</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>拿<rt>ná</rt></ruby><ruby>着<rt>zhe</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>面<rt>miàn</rt></ruby><ruby>包<rt>bāo</rt></ruby></span><span class="word-group"><ruby>夹<rt>jiā</rt></ruby><ruby>子<rt>zi</rt></ruby></span><span class="word-group"><ruby>左<rt>zuǒ</rt></ruby><ruby>右<rt>yòu</rt></ruby><ruby>包<rt>bāo</rt></ruby><ruby>抄<rt>chāo</rt></ruby></span><span class="punct">！</span>`,
        en: "Dog Cop and Little Kitty put on roller skates and flanked them left and right with giant bread tongs!",
        enHtml: `<span class="en-word-group">Dog Cop</span> <span class="en-word-group">and Little Kitty</span> <span class="en-word-group">put on roller skates</span> <span class="en-word-group">and flanked them</span> <span class="en-word-group">left and right</span> <span class="en-word-group">with giant bread tongs!</span>`
      }},
      {{
        img: "{s21_p[3]}",
        text: "所有淘气热狗都被夹进了面包里，全城举办了盛大的野餐派对！",
        ruby: `<span class="word-group"><ruby>所<rt>suǒ</rt></ruby><ruby>有<rt>yǒu</rt></ruby></span><span class="word-group"><ruby>淘<rt>táo</rt></ruby><ruby>气<rt>qì</rt></ruby></span><span class="word-group"><ruby>热<rt>rè</rt></ruby><ruby>狗<rt>gǒu</rt></ruby></span><span class="word-group"><ruby>都<rt>dōu</rt></ruby><ruby>被<rt>bèi</rt></ruby></span><span class="word-group"><ruby>夹<rt>jiā</rt></ruby><ruby>进<rt>jìn</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>面<rt>miàn</rt></ruby><ruby>包<rt>bāo</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>全<rt>quán</rt></ruby><ruby>城<rt>chéng</rt></ruby></span><span class="word-group"><ruby>举<rt>jǔ</rt></ruby><ruby>办<rt>bàn</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>盛<rt>shèng</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>野<rt>yě</rt></ruby><ruby>餐<rt>cān</rt></ruby></span><span class="word-group"><ruby>派<rt>pài</rt></ruby><ruby>对<rt>duì</rt></ruby></span><span class="punct">！</span>`,
        en: "Every mischievous hot dog was scooped right into a bun, and the whole city threw a grand picnic party!",
        enHtml: `<span class="en-word-group">Every mischievous hot dog</span> <span class="en-word-group">was scooped right into a bun,</span> <span class="en-word-group">and the whole city</span> <span class="en-word-group">threw a grand</span> <span class="en-word-group">picnic party!</span>`
      }}
    ],
    vocab: [
      {{ hz: "药水", py: "yào shuǐ", en: "potion" }},
      {{ hz: "香肠", py: "xiāng cháng", en: "sausage" }},
      {{ hz: "番茄酱", py: "fān qié jiàng", en: "ketchup" }},
      {{ hz: "旱冰鞋", py: "hàn bīng xié", en: "roller skates" }}
    ]
  }},
  {{
    id: 22,
    category: "dogcop",
    icon: "🚀",
    title: "22. 喷嚏喷气背包大救援",
    titleText: "喷嚏喷气背包大救援",
    titlePinyin: "pēn tì pēn qì bēi bāo dà jiù yuán",
    titleRuby: `<span class="word-group"><ruby>喷<rt>pēn</rt></ruby><ruby>嚏<rt>tì</rt></ruby></span><span class="word-group"><ruby>喷<rt>pēn</rt></ruby><ruby>气<rt>qì</rt></ruby></span><span class="word-group"><ruby>背<rt>bēi</rt></ruby><ruby>包<rt>bāo</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>救<rt>jiù</rt></ruby><ruby>援<rt>yuán</rt></ruby></span>`,
    titleEn: "The Sneeze-Jetpack Big Rescue",
    titleEnHtml: `<span class="en-word-group">The Sneeze-Jetpack</span> <span class="en-word-group">Big Rescue</span>`,
    subtitle: "神探汪汪 第4集 · 4 句 · 爆笑漫画",
    bannerImg: "{s22_b}",
    sentences: [
      {{
        img: "{s22_p[0]}",
        text: "小橘猫给神探汪汪发明了火箭背包，可是开关居然是打喷嚏！",
        ruby: `<span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>橘<rt>jú</rt></ruby><ruby>猫<rt>māo</rt></ruby></span><span class="word-group"><ruby>给<rt>gěi</rt></ruby></span><span class="word-group"><ruby>神<rt>shén</rt></ruby><ruby>探<rt>tàn</rt></ruby><ruby>汪<rt>wāng</rt></ruby><ruby>汪<rt>wāng</rt></ruby></span><span class="word-group"><ruby>发<rt>fā</rt></ruby><ruby>明<rt>míng</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>火<rt>huǒ</rt></ruby><ruby>箭<rt>jiàn</rt></ruby></span><span class="word-group"><ruby>背<rt>bēi</rt></ruby><ruby>包<rt>bāo</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>可<rt>kě</rt></ruby><ruby>是<rt>shì</rt></ruby></span><span class="word-group"><ruby>开<rt>kāi</rt></ruby><ruby>关<rt>guān</rt></ruby></span><span class="word-group"><ruby>居<rt>jū</rt></ruby><ruby>然<rt>rán</rt></ruby><ruby>是<rt>shì</rt></ruby></span><span class="word-group"><ruby>打<rt>dǎ</rt></ruby><ruby>喷<rt>pēn</rt></ruby><ruby>嚏<rt>tì</rt></ruby></span><span class="punct">！</span>`,
        en: "Little Kitty invented a rocket backpack for Dog Cop, but the switch is actually sneezing!",
        enHtml: `<span class="en-word-group">Little Kitty</span> <span class="en-word-group">invented</span> <span class="en-word-group">a rocket backpack</span> <span class="en-word-group">for Dog Cop,</span> <span class="en-word-group">but the switch</span> <span class="en-word-group">is actually sneezing!</span>`
      }},
      {{
        img: "{s22_p[1]}",
        text: "每当坏蛋橘猫经过，汪汪对猫毛过敏，“阿嚏”一声就飞上天！",
        ruby: `<span class="word-group"><ruby>每<rt>měi</rt></ruby><ruby>当<rt>dāng</rt></ruby></span><span class="word-group"><ruby>坏<rt>huài</rt></ruby><ruby>蛋<rt>dàn</rt></ruby></span><span class="word-group"><ruby>橘<rt>jú</rt></ruby><ruby>猫<rt>māo</rt></ruby></span><span class="word-group"><ruby>经<rt>jīng</rt></ruby><ruby>过<rt>guò</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>汪<rt>wāng</rt></ruby><ruby>汪<rt>wāng</rt></ruby></span><span class="word-group"><ruby>对<rt>duì</rt></ruby></span><span class="word-group"><ruby>猫<rt>māo</rt></ruby><ruby>毛<rt>máo</rt></ruby></span><span class="word-group"><ruby>过<rt>guò</rt></ruby><ruby>敏<rt>mǐn</rt></ruby></span><span class="punct">，“</span><span class="word-group"><ruby>阿<rt>ā</rt></ruby><ruby>嚏<rt>tì</rt></ruby></span><span class="punct">”</span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>声<rt>shēng</rt></ruby></span><span class="word-group"><ruby>就<rt>jiù</rt></ruby><ruby>飞<rt>fēi</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>天<rt>tiān</rt></ruby></span><span class="punct">！</span>`,
        en: 'Whenever Villain Orange Cat walks by, Dog Cop is allergic to cat fur and blasts into the sky with an "ACHOO!"',
        enHtml: `<span class="en-word-group">Whenever</span> <span class="en-word-group">Villain Orange Cat</span> <span class="en-word-group">walks by,</span> <span class="en-word-group">Dog Cop</span> <span class="en-word-group">is allergic to cat fur</span> <span class="en-word-group">and blasts into the sky</span> <span class="en-word-group">with an "ACHOO!"</span>`
      }},
      {{
        img: "{s22_p[2]}",
        text: "他在空中翻了三个跟头，刚好接住了从钟楼掉下来的局长杯子。",
        ruby: `<span class="word-group"><ruby>他<rt>tā</rt></ruby></span><span class="word-group"><ruby>在<rt>zài</rt></ruby><ruby>空<rt>kōng</rt></ruby><ruby>中<rt>zhōng</rt></ruby></span><span class="word-group"><ruby>翻<rt>fān</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>三<rt>sān</rt></ruby><ruby>个<rt>gè</rt></ruby></span><span class="word-group"><ruby>跟<rt>gēn</rt></ruby><ruby>头<rt>tou</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>刚<rt>gāng</rt></ruby><ruby>好<rt>hǎo</rt></ruby></span><span class="word-group"><ruby>接<rt>jiē</rt></ruby><ruby>住<rt>zhù</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>从<rt>cóng</rt></ruby><ruby>钟<rt>zhōng</rt></ruby><ruby>楼<rt>lóu</rt></ruby></span><span class="word-group"><ruby>掉<rt>diào</rt></ruby><ruby>下<rt>xià</rt></ruby><ruby>来<rt>lái</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>局<rt>jú</rt></ruby><ruby>长<rt>zhǎng</rt></ruby></span><span class="word-group"><ruby>杯<rt>bēi</rt></ruby><ruby>子<rt>zi</rt></ruby></span><span class="punct">。</span>`,
        en: "He did three somersaults in midair and caught the Police Chief's mug right as it fell from the clock tower.",
        enHtml: `<span class="en-word-group">He did</span> <span class="en-word-group">three somersaults</span> <span class="en-word-group">in midair</span> <span class="en-word-group">and caught</span> <span class="en-word-group">the Police Chief's mug</span> <span class="en-word-group">right as it fell</span> <span class="en-word-group">from the clock tower.</span>`
      }},
      {{
        img: "{s22_p[3]}",
        text: "警察局长高兴地发给他一块大肉骨头勋章，汪汪开心地直转圈！",
        ruby: `<span class="word-group"><ruby>警<rt>jǐng</rt></ruby><ruby>察<rt>chá</rt></ruby></span><span class="word-group"><ruby>局<rt>jú</rt></ruby><ruby>长<rt>zhǎng</rt></ruby></span><span class="word-group"><ruby>高<rt>gāo</rt></ruby><ruby>兴<rt>xìng</rt></ruby><ruby>地<rt>de</rt></ruby></span><span class="word-group"><ruby>发<rt>fā</rt></ruby><ruby>给<rt>gěi</rt></ruby><ruby>他<rt>tā</rt></ruby></span><span class="word-group"><ruby>一<rt>yí</rt></ruby><ruby>块<rt>kuài</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>肉<rt>ròu</rt></ruby><ruby>骨<rt>gǔ</rt></ruby><ruby>头<rt>tou</rt></ruby></span><span class="word-group"><ruby>勋<rt>xūn</rt></ruby><ruby>章<rt>zhāng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>汪<rt>wāng</rt></ruby><ruby>汪<rt>wāng</rt></ruby></span><span class="word-group"><ruby>开<rt>kāi</rt></ruby><ruby>心<rt>xīn</rt></ruby><ruby>地<rt>de</rt></ruby></span><span class="word-group"><ruby>直<rt>zhí</rt></ruby><ruby>转<rt>zhuàn</rt></ruby><ruby>圈<rt>quān</rt></ruby></span><span class="punct">！</span>`,
        en: "The Police Chief happily awarded him a giant meat-bone medal, and Dog Cop spun around in circles with joy!",
        enHtml: `<span class="en-word-group">The Police Chief</span> <span class="en-word-group">happily awarded him</span> <span class="en-word-group">a giant meat-bone medal,</span> <span class="en-word-group">and Dog Cop</span> <span class="en-word-group">spun around in circles</span> <span class="en-word-group">with joy!</span>`
      }}
    ],
    vocab: [
      {{ hz: "火箭", py: "huǒ jiàn", en: "rocket" }},
      {{ hz: "喷嚏", py: "pēn tì", en: "sneeze" }},
      {{ hz: "过敏", py: "guò mǐn", en: "allergic" }},
      {{ hz: "勋章", py: "xūn zhāng", en: "medal" }}
    ]
  }}
];"""

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

target_end = """      { hz: "外星人", py: "wài xīng rén", en: "alien" },
      { hz: "陨石", py: "yǔn shí", en: "meteorite" }
    ]
  }
];"""

assert target_end in html, "Could not find end of Story 18 in index.html"
html = html.replace(target_end, """      { hz: "外星人", py: "wài xīng rén", en: "alien" },
      { hz: "陨石", py: "yǔn shí", en: "meteorite" }
    ]
""" + new_stories_js, 1)

old_categories = """const CATEGORIES = [
  { id: 'all', label: '✨ 全部故事 · All (18)' },
  { id: 'weird', label: '🤪 疯狂学校 · My Weird School (4)' },
  { id: 'adventure', label: '🕵️ 脑洞探秘 · Mystery & Sci-Fi (2)' },
  { id: 'school', label: '🏫 校园日常 · School Life (4)' },
  { id: 'fairy', label: '🐾 童话绘本 · Animal Tales (8)' }
];"""

new_categories = """const CATEGORIES = [
  { id: 'all', label: '✨ 全部故事 · All (22)' },
  { id: 'dogcop', label: '🐶 神探汪汪 · Dog Cop (4)' },
  { id: 'weird', label: '🤪 疯狂学校 · My Weird School (4)' },
  { id: 'adventure', label: '🕵️ 脑洞探秘 · Mystery & Sci-Fi (2)' },
  { id: 'school', label: '🏫 校园日常 · School Life (4)' },
  { id: 'fairy', label: '🐾 童话绘本 · Animal Tales (8)' }
];"""

assert old_categories in html, "Could not find CATEGORIES in index.html"
html = html.replace(old_categories, new_categories, 1)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Successfully updated index.html with Stories 19-22 and updated CATEGORIES!")
