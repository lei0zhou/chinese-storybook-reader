import base64
import io
import os
from PIL import Image

BRAIN_DIR = "/Users/leizhou/.gemini/antigravity-cli/brain/dde92688-d628-4cf6-9d61-3d1a08abad1b"
INDEX_PATH = "/Users/leizhou/Downloads/chinese-storybook-reader/index.html"

GRID_FILES = {
    23: os.path.join(BRAIN_DIR, "story23_grid_1793626081522.jpg"),
    24: os.path.join(BRAIN_DIR, "story24_grid_1793626082623.jpg"),
    25: os.path.join(BRAIN_DIR, "story25_grid_1793626093958.jpg"),
    26: os.path.join(BRAIN_DIR, "story26_grid_1793626105637.jpg"),
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
        (mx, my, mid_x - cx, mid_y - cy),
        (mid_x + cx, my, w - mx, mid_y - cy),
        (mx, mid_y + cy, mid_x - cx, h - my),
        (mid_x + cx, mid_y + cy, w - mx, h - my),
    ]
    panels = [crop_4_3(im.crop(b)) for b in boxes]
    banner = make_banner_from_panels(panels[0], panels[1])
    return img_to_webp_data_url(banner, quality=80), [img_to_webp_data_url(p, quality=80) for p in panels]

assets = {}
for sid, gpath in GRID_FILES.items():
    banner_url, panel_urls = extract_story_images(gpath)
    assets[sid] = (banner_url, panel_urls)
    print(f"Story {sid}: banner={len(banner_url)} chars, panels={[len(u) for u in panel_urls]}")

s23_b, s23_p = assets[23]
s24_b, s24_p = assets[24]
s25_b, s25_p = assets[25]
s26_b, s26_p = assets[26]

new_stories_js = f"""  }},
  {{
    id: 23,
    category: "bluepup",
    icon: "🎈",
    title: "23. 气球不准落地！",
    titleText: "气球不准落地！",
    titlePinyin: "qì qiú bù zhǔn luò dì",
    titleRuby: `<span class="word-group"><ruby>气<rt>qì</rt></ruby><ruby>球<rt>qiú</rt></ruby></span><span class="word-group"><ruby>不<rt>bù</rt></ruby><ruby>准<rt>zhǔn</rt></ruby></span><span class="word-group"><ruby>落<rt>luò</rt></ruby><ruby>地<rt>dì</rt></ruby></span><span class="punct">！</span>`,
    titleEn: "Keepy Uppy: Don't Let the Balloon Touch the Ground!",
    titleEnHtml: `<span class="en-word-group">Keepy Uppy:</span> <span class="en-word-group">Don't Let</span> <span class="en-word-group">the Balloon</span> <span class="en-word-group">Touch the Ground!</span>`,
    subtitle: "蓝小狗一家 第1集 · 4 句 · 温馨家庭",
    bannerImg: "{s23_b}",
    sentences: [
      {{
        img: "{s23_p[0]}",
        text: "蓝小狗姐姐和橘小狗妹妹吹起红气球，在客厅玩“气球不准落地”！",
        ruby: `<span class="word-group"><ruby>蓝<rt>lán</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>狗<rt>gǒu</rt></ruby></span><span class="word-group"><ruby>姐<rt>jiě</rt></ruby><ruby>姐<rt>jie</rt></ruby></span><span class="word-group"><ruby>和<rt>hé</rt></ruby></span><span class="word-group"><ruby>橘<rt>jú</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>狗<rt>gǒu</rt></ruby></span><span class="word-group"><ruby>妹<rt>mèi</rt></ruby><ruby>妹<rt>mei</rt></ruby></span><span class="word-group"><ruby>吹<rt>chuī</rt></ruby><ruby>起<rt>qǐ</rt></ruby></span><span class="word-group"><ruby>红<rt>hóng</rt></ruby><ruby>气<rt>qì</rt></ruby><ruby>球<rt>qiú</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>在<rt>zài</rt></ruby><ruby>客<rt>kè</rt></ruby><ruby>厅<rt>tīng</rt></ruby></span><span class="word-group"><ruby>玩<rt>wán</rt></ruby></span><span class="punct">“</span><span class="word-group"><ruby>气<rt>qì</rt></ruby><ruby>球<rt>qiú</rt></ruby></span><span class="word-group"><ruby>不<rt>bù</rt></ruby><ruby>准<rt>zhǔn</rt></ruby><ruby>落<rt>luò</rt></ruby><ruby>地<rt>dì</rt></ruby></span><span class="punct">”！</span>`,
        en: 'Big Sister Blue Pup and Little Sister Orange Pup blew up a red balloon to play "Keepy Uppy" in the living room!',
        enHtml: `<span class="en-word-group">Big Sister Blue Pup</span> <span class="en-word-group">and Little Sister Orange Pup</span> <span class="en-word-group">blew up a red balloon</span> <span class="en-word-group">to play "Keepy Uppy"</span> <span class="en-word-group">in the living room!</span>`
      }},
      {{
        img: "{s23_p[1]}",
        text: "眼看气球快要碰到地板，狗爸爸一个滑铲，用鼻尖把气球顶了起来！",
        ruby: `<span class="word-group"><ruby>眼<rt>yǎn</rt></ruby><ruby>看<rt>kàn</rt></ruby></span><span class="word-group"><ruby>气<rt>qì</rt></ruby><ruby>球<rt>qiú</rt></ruby></span><span class="word-group"><ruby>快<rt>kuài</rt></ruby><ruby>要<rt>yào</rt></ruby></span><span class="word-group"><ruby>碰<rt>pèng</rt></ruby><ruby>到<rt>dào</rt></ruby></span><span class="word-group"><ruby>地<rt>dì</rt></ruby><ruby>板<rt>bǎn</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>狗<rt>gǒu</rt></ruby><ruby>爸<rt>bà</rt></ruby><ruby>爸<rt>ba</rt></ruby></span><span class="word-group"><ruby>一<rt>yí</rt></ruby><ruby>个<rt>gè</rt></ruby></span><span class="word-group"><ruby>滑<rt>huá</rt></ruby><ruby>铲<rt>chǎn</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>用<rt>yòng</rt></ruby><ruby>鼻<rt>bí</rt></ruby><ruby>尖<rt>jiān</rt></ruby></span><span class="word-group"><ruby>把<rt>bǎ</rt></ruby><ruby>气<rt>qì</rt></ruby><ruby>球<rt>qiú</rt></ruby></span><span class="word-group"><ruby>顶<rt>dǐng</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>起<rt>qǐ</rt></ruby><ruby>来<rt>lái</rt></ruby></span><span class="punct">！</span>`,
        en: "Just as the balloon was about to touch the floor, Dog Dad slid across the rug and bounced it up with the tip of his nose!",
        enHtml: `<span class="en-word-group">Just as the balloon</span> <span class="en-word-group">was about to touch the floor,</span> <span class="en-word-group">Dog Dad slid across the rug</span> <span class="en-word-group">and bounced it up</span> <span class="en-word-group">with the tip of his nose!</span>`
      }},
      {{
        img: "{s23_p[2]}",
        text: "红气球飘过沙发飞向花盆，狗妈妈也笑着加入一起拍气球。",
        ruby: `<span class="word-group"><ruby>红<rt>hóng</rt></ruby><ruby>气<rt>qì</rt></ruby><ruby>球<rt>qiú</rt></ruby></span><span class="word-group"><ruby>飘<rt>piāo</rt></ruby><ruby>过<rt>guò</rt></ruby></span><span class="word-group"><ruby>沙<rt>shā</rt></ruby><ruby>发<rt>fā</rt></ruby></span><span class="word-group"><ruby>飞<rt>fēi</rt></ruby><ruby>向<rt>xiàng</rt></ruby></span><span class="word-group"><ruby>花<rt>huā</rt></ruby><ruby>盆<rt>pén</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>狗<rt>gǒu</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby></span><span class="word-group"><ruby>也<rt>yě</rt></ruby><ruby>笑<rt>xiào</rt></ruby><ruby>着<rt>zhe</rt></ruby></span><span class="word-group"><ruby>加<rt>jiā</rt></ruby><ruby>入<rt>rù</rt></ruby></span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>起<rt>qǐ</rt></ruby></span><span class="word-group"><ruby>拍<rt>pāi</rt></ruby><ruby>气<rt>qì</rt></ruby><ruby>球<rt>qiú</rt></ruby></span><span class="punct">。</span>`,
        en: "The red balloon floated over the sofa toward the flowerpot, and Dog Mom laughed and joined in to tap it.",
        enHtml: `<span class="en-word-group">The red balloon</span> <span class="en-word-group">floated over the sofa</span> <span class="en-word-group">toward the flowerpot,</span> <span class="en-word-group">and Dog Mom laughed</span> <span class="en-word-group">and joined in</span> <span class="en-word-group">to tap it.</span>`
      }},
      {{
        img: "{s23_p[3]}",
        text: "最后气球稳稳停在爸爸毛茸茸的尾巴上，全家人开心得拍手大笑！",
        ruby: `<span class="word-group"><ruby>最<rt>zuì</rt></ruby><ruby>后<rt>hòu</rt></ruby></span><span class="word-group"><ruby>气<rt>qì</rt></ruby><ruby>球<rt>qiú</rt></ruby></span><span class="word-group"><ruby>稳<rt>wěn</rt></ruby><ruby>稳<rt>wěn</rt></ruby></span><span class="word-group"><ruby>停<rt>tíng</rt></ruby><ruby>在<rt>zài</rt></ruby></span><span class="word-group"><ruby>爸<rt>bà</rt></ruby><ruby>爸<rt>ba</rt></ruby></span><span class="word-group"><ruby>毛<rt>máo</rt></ruby><ruby>茸<rt>róng</rt></ruby><ruby>茸<rt>róng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>尾<rt>wěi</rt></ruby><ruby>巴<rt>ba</rt></ruby><ruby>上<rt>shàng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>全<rt>quán</rt></ruby><ruby>家<rt>jiā</rt></ruby><ruby>人<rt>rén</rt></ruby></span><span class="word-group"><ruby>开<rt>kāi</rt></ruby><ruby>心<rt>xīn</rt></ruby><ruby>得<rt>de</rt></ruby></span><span class="word-group"><ruby>拍<rt>pāi</rt></ruby><ruby>手<rt>shǒu</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>笑<rt>xiào</rt></ruby></span><span class="punct">！</span>`,
        en: "Finally the balloon landed steadily on Dad's fluffy tail, and the whole family clapped and laughed with joy!",
        enHtml: `<span class="en-word-group">Finally</span> <span class="en-word-group">the balloon landed steadily</span> <span class="en-word-group">on Dad's fluffy tail,</span> <span class="en-word-group">and the whole family</span> <span class="en-word-group">clapped and laughed</span> <span class="en-word-group">with joy!</span>`
      }}
    ],
    vocab: [
      {{ hz: "气球", py: "qì qiú", en: "balloon" }},
      {{ hz: "客厅", py: "kè tīng", en: "living room" }},
      {{ hz: "地板", py: "dì bǎn", en: "floor" }},
      {{ hz: "鼻尖", py: "bí jiān", en: "tip of the nose" }}
    ]
  }},
  {{
    id: 24,
    category: "bluepup",
    icon: "🏨",
    title: "24. 客厅大酒店开张啦",
    titleText: "客厅大酒店开张啦",
    titlePinyin: "kè tīng dà jiǔ diàn kāi zhāng la",
    titleRuby: `<span class="word-group"><ruby>客<rt>kè</rt></ruby><ruby>厅<rt>tīng</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>酒<rt>jiǔ</rt></ruby><ruby>店<rt>diàn</rt></ruby></span><span class="word-group"><ruby>开<rt>kāi</rt></ruby><ruby>张<rt>zhāng</rt></ruby><ruby>啦<rt>la</rt></ruby></span>`,
    titleEn: "The Living Room Grand Hotel Is Open!",
    titleEnHtml: `<span class="en-word-group">The Living Room</span> <span class="en-word-group">Grand Hotel</span> <span class="en-word-group">Is Open!</span>`,
    subtitle: "蓝小狗一家 第2集 · 4 句 · 温馨家庭",
    bannerImg: "{s24_b}",
    sentences: [
      {{
        img: "{s24_p[0]}",
        text: "两只小狗戴上小礼帽当经理，欢迎提着玩具行李箱的狗爸爸入住！",
        ruby: `<span class="word-group"><ruby>两<rt>liǎng</rt></ruby><ruby>只<rt>zhī</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>狗<rt>gǒu</rt></ruby></span><span class="word-group"><ruby>戴<rt>dài</rt></ruby><ruby>上<rt>shàng</rt></ruby></span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>礼<rt>lǐ</rt></ruby><ruby>帽<rt>mào</rt></ruby></span><span class="word-group"><ruby>当<rt>dāng</rt></ruby><ruby>经<rt>jīng</rt></ruby><ruby>理<rt>lǐ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>欢<rt>huān</rt></ruby><ruby>迎<rt>yíng</rt></ruby></span><span class="word-group"><ruby>提<rt>tí</rt></ruby><ruby>着<rt>zhe</rt></ruby></span><span class="word-group"><ruby>玩<rt>wán</rt></ruby><ruby>具<rt>jù</rt></ruby></span><span class="word-group"><ruby>行<rt>xíng</rt></ruby><ruby>李<rt>lǐ</rt></ruby><ruby>箱<rt>xiāng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>狗<rt>gǒu</rt></ruby><ruby>爸<rt>bà</rt></ruby><ruby>爸<rt>ba</rt></ruby></span><span class="word-group"><ruby>入<rt>rù</rt></ruby><ruby>住<rt>zhù</rt></ruby></span><span class="punct">！</span>`,
        en: "The two little pups put on bellhop hats as managers and welcomed Dog Dad with his toy suitcase!",
        enHtml: `<span class="en-word-group">The two little pups</span> <span class="en-word-group">put on bellhop hats</span> <span class="en-word-group">as managers</span> <span class="en-word-group">and welcomed Dog Dad</span> <span class="en-word-group">with his toy suitcase!</span>`
      }},
      {{
        img: "{s24_p[1]}",
        text: "她们用彩色沙发靠垫和毯子，搭了一间亮着彩灯的枕头城堡房间。",
        ruby: `<span class="word-group"><ruby>她<rt>tā</rt></ruby><ruby>们<rt>men</rt></ruby></span><span class="word-group"><ruby>用<rt>yòng</rt></ruby><ruby>彩<rt>cǎi</rt></ruby><ruby>色<rt>sè</rt></ruby></span><span class="word-group"><ruby>沙<rt>shā</rt></ruby><ruby>发<rt>fā</rt></ruby></span><span class="word-group"><ruby>靠<rt>kào</rt></ruby><ruby>垫<rt>diàn</rt></ruby></span><span class="word-group"><ruby>和<rt>hé</rt></ruby><ruby>毯<rt>tǎn</rt></ruby><ruby>子<rt>zi</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>搭<rt>dā</rt></ruby><ruby>了<rt>le</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>间<rt>jiān</rt></ruby></span><span class="word-group"><ruby>亮<rt>liàng</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>彩<rt>cǎi</rt></ruby><ruby>灯<rt>dēng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>枕<rt>zhěn</rt></ruby><ruby>头<rt>tou</rt></ruby></span><span class="word-group"><ruby>城<rt>chéng</rt></ruby><ruby>堡<rt>bǎo</rt></ruby></span><span class="word-group"><ruby>房<rt>fáng</rt></ruby><ruby>间<rt>jiān</rt></ruby></span><span class="punct">。</span>`,
        en: "They used colorful sofa cushions and blankets to build a pillow-castle room glowing with fairy lights.",
        enHtml: `<span class="en-word-group">They used</span> <span class="en-word-group">colorful sofa cushions</span> <span class="en-word-group">and blankets</span> <span class="en-word-group">to build a pillow-castle room</span> <span class="en-word-group">glowing with fairy lights.</span>`
      }},
      {{
        img: "{s24_p[2]}",
        text: "妹妹端来木头水果和布煎饼，假装给爸爸送上美味的客房早餐！",
        ruby: `<span class="word-group"><ruby>妹<rt>mèi</rt></ruby><ruby>妹<rt>mei</rt></ruby></span><span class="word-group"><ruby>端<rt>duān</rt></ruby><ruby>来<rt>lái</rt></ruby></span><span class="word-group"><ruby>木<rt>mù</rt></ruby><ruby>头<rt>tou</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>果<rt>guǒ</rt></ruby></span><span class="word-group"><ruby>和<rt>hé</rt></ruby></span><span class="word-group"><ruby>布<rt>bù</rt></ruby><ruby>煎<rt>jiān</rt></ruby><ruby>饼<rt>bǐng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>假<rt>jiǎ</rt></ruby><ruby>装<rt>zhuāng</rt></ruby></span><span class="word-group"><ruby>给<rt>gěi</rt></ruby><ruby>爸<rt>bà</rt></ruby><ruby>爸<rt>ba</rt></ruby></span><span class="word-group"><ruby>送<rt>sòng</rt></ruby><ruby>上<rt>shàng</rt></ruby></span><span class="word-group"><ruby>美<rt>měi</rt></ruby><ruby>味<rt>wèi</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>客<rt>kè</rt></ruby><ruby>房<rt>fáng</rt></ruby><ruby>早<rt>zǎo</rt></ruby><ruby>餐<rt>cān</rt></ruby></span><span class="punct">！</span>`,
        en: "Little Sister brought wooden fruits and felt pancakes, pretending to serve Dad a delicious room-service breakfast!",
        enHtml: `<span class="en-word-group">Little Sister</span> <span class="en-word-group">brought wooden fruits</span> <span class="en-word-group">and felt pancakes,</span> <span class="en-word-group">pretending to serve Dad</span> <span class="en-word-group">a delicious room-service breakfast!</span>`
      }},
      {{
        img: "{s24_p[3]}",
        text: "狗爸爸吃得津津有味，给客厅大酒店贴上了五颗闪亮的金星好评！",
        ruby: `<span class="word-group"><ruby>狗<rt>gǒu</rt></ruby><ruby>爸<rt>bà</rt></ruby><ruby>爸<rt>ba</rt></ruby></span><span class="word-group"><ruby>吃<rt>chī</rt></ruby><ruby>得<rt>de</rt></ruby></span><span class="word-group"><ruby>津<rt>jīn</rt></ruby><ruby>津<rt>jīn</rt></ruby><ruby>有<rt>yǒu</rt></ruby><ruby>味<rt>wèi</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>给<rt>gěi</rt></ruby></span><span class="word-group"><ruby>客<rt>kè</rt></ruby><ruby>厅<rt>tīng</rt></ruby><ruby>大<rt>dà</rt></ruby><ruby>酒<rt>jiǔ</rt></ruby><ruby>店<rt>diàn</rt></ruby></span><span class="word-group"><ruby>贴<rt>tiē</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>五<rt>wǔ</rt></ruby><ruby>颗<rt>kē</rt></ruby></span><span class="word-group"><ruby>闪<rt>shǎn</rt></ruby><ruby>亮<rt>liàng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>金<rt>jīn</rt></ruby><ruby>星<rt>xīng</rt></ruby><ruby>好<rt>hǎo</rt></ruby><ruby>评<rt>píng</rt></ruby></span><span class="punct">！</span>`,
        en: "Dog Dad ate with great relish and gave the Living Room Grand Hotel a five-gold-star review!",
        enHtml: `<span class="en-word-group">Dog Dad</span> <span class="en-word-group">ate with great relish</span> <span class="en-word-group">and gave</span> <span class="en-word-group">the Living Room Grand Hotel</span> <span class="en-word-group">a five-gold-star review!</span>`
      }}
    ],
    vocab: [
      {{ hz: "酒店", py: "jiǔ diàn", en: "hotel" }},
      {{ hz: "行李箱", py: "xíng lǐ xiāng", en: "suitcase" }},
      {{ hz: "靠垫", py: "kào diàn", en: "cushion" }},
      {{ hz: "假装", py: "jiǎ zhuāng", en: "pretend" }}
    ]
  }},
  {{
    id: 25,
    category: "bluepup",
    icon: "🎹",
    title: "25. 神奇魔法木琴",
    titleText: "神奇魔法木琴",
    titlePinyin: "shén qí mó fǎ mù qín",
    titleRuby: `<span class="word-group"><ruby>神<rt>shén</rt></ruby><ruby>奇<rt>qí</rt></ruby></span><span class="word-group"><ruby>魔<rt>mó</rt></ruby><ruby>法<rt>fǎ</rt></ruby></span><span class="word-group"><ruby>木<rt>mù</rt></ruby><ruby>琴<rt>qín</rt></ruby></span>`,
    titleEn: "The Magic Freeze Xylophone",
    titleEnHtml: `<span class="en-word-group">The Magic</span> <span class="en-word-group">Freeze</span> <span class="en-word-group">Xylophone</span>`,
    subtitle: "蓝小狗一家 第3集 · 4 句 · 温馨家庭",
    bannerImg: "{s25_b}",
    sentences: [
      {{
        img: "{s25_p[0]}",
        text: "姐妹俩在后院找到一架彩虹木琴，宣布只要敲一下就能定住任何人！",
        ruby: `<span class="word-group"><ruby>姐<rt>jiě</rt></ruby><ruby>妹<rt>mèi</rt></ruby><ruby>俩<rt>liǎ</rt></ruby></span><span class="word-group"><ruby>在<rt>zài</rt></ruby><ruby>后<rt>hòu</rt></ruby><ruby>院<rt>yuàn</rt></ruby></span><span class="word-group"><ruby>找<rt>zhǎo</rt></ruby><ruby>到<rt>dào</rt></ruby></span><span class="word-group"><ruby>一<rt>yí</rt></ruby><ruby>架<rt>jià</rt></ruby></span><span class="word-group"><ruby>彩<rt>cǎi</rt></ruby><ruby>虹<rt>hóng</rt></ruby><ruby>木<rt>mù</rt></ruby><ruby>琴<rt>qín</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>宣<rt>xuān</rt></ruby><ruby>布<rt>bù</rt></ruby></span><span class="word-group"><ruby>只<rt>zhǐ</rt></ruby><ruby>要<rt>yào</rt></ruby><ruby>敲<rt>qiāo</rt></ruby><ruby>一<rt>yí</rt></ruby><ruby>下<rt>xià</rt></ruby></span><span class="word-group"><ruby>就<rt>jiù</rt></ruby><ruby>能<rt>néng</rt></ruby><ruby>定<rt>dìng</rt></ruby><ruby>住<rt>zhù</rt></ruby></span><span class="word-group"><ruby>任<rt>rèn</rt></ruby><ruby>何<rt>hé</rt></ruby><ruby>人<rt>rén</rt></ruby></span><span class="punct">！</span>`,
        en: "The two sisters found a rainbow xylophone in the backyard and declared that one tap could freeze anyone!",
        enHtml: `<span class="en-word-group">The two sisters</span> <span class="en-word-group">found a rainbow xylophone</span> <span class="en-word-group">in the backyard</span> <span class="en-word-group">and declared that one tap</span> <span class="en-word-group">could freeze anyone!</span>`
      }},
      {{
        img: "{s25_p[1]}",
        text: "叮咚一声，正在拿水管浇花的狗爸爸立刻单脚金鸡独立，一动不动！",
        ruby: `<span class="word-group"><ruby>叮<rt>dīng</rt></ruby><ruby>咚<rt>dōng</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>声<rt>shēng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>正<rt>zhèng</rt></ruby><ruby>在<rt>zài</rt></ruby></span><span class="word-group"><ruby>拿<rt>ná</rt></ruby><ruby>水<rt>shuǐ</rt></ruby><ruby>管<rt>guǎn</rt></ruby></span><span class="word-group"><ruby>浇<rt>jiāo</rt></ruby><ruby>花<rt>huā</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>狗<rt>gǒu</rt></ruby><ruby>爸<rt>bà</rt></ruby><ruby>爸<rt>ba</rt></ruby></span><span class="word-group"><ruby>立<rt>lì</rt></ruby><ruby>刻<rt>kè</rt></ruby></span><span class="word-group"><ruby>单<rt>dān</rt></ruby><ruby>脚<rt>jiǎo</rt></ruby></span><span class="word-group"><ruby>金<rt>jīn</rt></ruby><ruby>鸡<rt>jī</rt></ruby><ruby>独<rt>dú</rt></ruby><ruby>立<rt>lì</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>一<rt>yí</rt></ruby><ruby>动<rt>dòng</rt></ruby><ruby>不<rt>bú</rt></ruby><ruby>动<rt>dòng</rt></ruby></span><span class="punct">！</span>`,
        en: "With a DING-DONG, Dog Dad, who was watering flowers with a hose, froze on one foot like a statue!",
        enHtml: `<span class="en-word-group">With a DING-DONG,</span> <span class="en-word-group">Dog Dad,</span> <span class="en-word-group">who was watering flowers with a hose,</span> <span class="en-word-group">froze on one foot</span> <span class="en-word-group">like a statue!</span>`
      }},
      {{
        img: "{s25_p[2]}",
        text: "两只小狗咯咯直笑，给变成雕像的爸爸戴上了大草帽和搞笑太阳镜。",
        ruby: `<span class="word-group"><ruby>两<rt>liǎng</rt></ruby><ruby>只<rt>zhī</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>狗<rt>gǒu</rt></ruby></span><span class="word-group"><ruby>咯<rt>gē</rt></ruby><ruby>咯<rt>gē</rt></ruby><ruby>直<rt>zhí</rt></ruby><ruby>笑<rt>xiào</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>给<rt>gěi</rt></ruby></span><span class="word-group"><ruby>变<rt>biàn</rt></ruby><ruby>成<rt>chéng</rt></ruby><ruby>雕<rt>diāo</rt></ruby><ruby>像<rt>xiàng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>爸<rt>bà</rt></ruby><ruby>爸<rt>ba</rt></ruby></span><span class="word-group"><ruby>戴<rt>dài</rt></ruby><ruby>上<rt>shàng</rt></ruby><ruby>了<rt>le</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>草<rt>cǎo</rt></ruby><ruby>帽<rt>mào</rt></ruby></span><span class="word-group"><ruby>和<rt>hé</rt></ruby></span><span class="word-group"><ruby>搞<rt>gǎo</rt></ruby><ruby>笑<rt>xiào</rt></ruby><ruby>太<rt>tài</rt></ruby><ruby>阳<rt>yáng</rt></ruby><ruby>镜<rt>jìng</rt></ruby></span><span class="punct">。</span>`,
        en: "Giggling nonstop, the two pups put a big straw hat and funny sunglasses onto their statue Dad.",
        enHtml: `<span class="en-word-group">Giggling nonstop,</span> <span class="en-word-group">the two pups</span> <span class="en-word-group">put a big straw hat</span> <span class="en-word-group">and funny sunglasses</span> <span class="en-word-group">onto their statue Dad.</span>`
      }},
      {{
        img: "{s25_p[3]}",
        text: "妹妹再敲一下木琴解开魔法，狗爸爸嗷呜一声追着她们满院子跑！",
        ruby: `<span class="word-group"><ruby>妹<rt>mèi</rt></ruby><ruby>妹<rt>mei</rt></ruby></span><span class="word-group"><ruby>再<rt>zài</rt></ruby><ruby>敲<rt>qiāo</rt></ruby><ruby>一<rt>yí</rt></ruby><ruby>下<rt>xià</rt></ruby></span><span class="word-group"><ruby>木<rt>mù</rt></ruby><ruby>琴<rt>qín</rt></ruby></span><span class="word-group"><ruby>解<rt>jiě</rt></ruby><ruby>开<rt>kāi</rt></ruby><ruby>魔<rt>mó</rt></ruby><ruby>法<rt>fǎ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>狗<rt>gǒu</rt></ruby><ruby>爸<rt>bà</rt></ruby><ruby>爸<rt>ba</rt></ruby></span><span class="word-group"><ruby>嗷<rt>áo</rt></ruby><ruby>呜<rt>wū</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>声<rt>shēng</rt></ruby></span><span class="word-group"><ruby>追<rt>zhuī</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>她<rt>tā</rt></ruby><ruby>们<rt>men</rt></ruby></span><span class="word-group"><ruby>满<rt>mǎn</rt></ruby><ruby>院<rt>yuàn</rt></ruby><ruby>子<rt>zi</rt></ruby><ruby>跑<rt>pǎo</rt></ruby></span><span class="punct">！</span>`,
        en: "Little Sister tapped the xylophone again to break the spell, and Dog Dad howled playfully and chased them all around the yard!",
        enHtml: `<span class="en-word-group">Little Sister</span> <span class="en-word-group">tapped the xylophone again</span> <span class="en-word-group">to break the spell,</span> <span class="en-word-group">and Dog Dad howled playfully</span> <span class="en-word-group">and chased them</span> <span class="en-word-group">all around the yard!</span>`
      }}
    ],
    vocab: [
      {{ hz: "木琴", py: "mù qín", en: "xylophone" }},
      {{ hz: "后院", py: "hòu yuàn", en: "backyard" }},
      {{ hz: "雕像", py: "diāo xiàng", en: "statue" }},
      {{ hz: "太阳镜", py: "tài yáng jìng", en: "sunglasses" }}
    ]
  }},
  {{
    id: 26,
    category: "bluepup",
    icon: "⛺",
    title: "26. 后院睡前露营夜",
    titleText: "后院睡前露营夜",
    titlePinyin: "hòu yuàn shuì qián lù yíng yè",
    titleRuby: `<span class="word-group"><ruby>后<rt>hòu</rt></ruby><ruby>院<rt>yuàn</rt></ruby></span><span class="word-group"><ruby>睡<rt>shuì</rt></ruby><ruby>前<rt>qián</rt></ruby></span><span class="word-group"><ruby>露<rt>lù</rt></ruby><ruby>营<rt>yíng</rt></ruby><ruby>夜<rt>yè</rt></ruby></span>`,
    titleEn: "Backyard Bedtime Camping Under the Stars",
    titleEnHtml: `<span class="en-word-group">Backyard</span> <span class="en-word-group">Bedtime Camping</span> <span class="en-word-group">Under the Stars</span>`,
    subtitle: "蓝小狗一家 第4集 · 4 句 · 温馨家庭",
    bannerImg: "{s26_b}",
    sentences: [
      {{
        img: "{s26_p[0]}",
        text: "傍晚的时候，爸爸妈妈带着两只小狗，在后院的大树下搭起小帐篷。",
        ruby: `<span class="word-group"><ruby>傍<rt>bàng</rt></ruby><ruby>晚<rt>wǎn</rt></ruby><ruby>的<rt>de</rt></ruby><ruby>时<rt>shí</rt></ruby><ruby>候<rt>hou</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>爸<rt>bà</rt></ruby><ruby>爸<rt>ba</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby></span><span class="word-group"><ruby>带<rt>dài</rt></ruby><ruby>着<rt>zhe</rt></ruby></span><span class="word-group"><ruby>两<rt>liǎng</rt></ruby><ruby>只<rt>zhī</rt></ruby><ruby>小<rt>xiǎo</rt></ruby><ruby>狗<rt>gǒu</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>在<rt>zài</rt></ruby><ruby>后<rt>hòu</rt></ruby><ruby>院<rt>yuàn</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>大<rt>dà</rt></ruby><ruby>树<rt>shù</rt></ruby><ruby>下<rt>xià</rt></ruby></span><span class="word-group"><ruby>搭<rt>dā</rt></ruby><ruby>起<rt>qǐ</rt></ruby></span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>帐<rt>zhàng</rt></ruby><ruby>篷<rt>peng</rt></ruby></span><span class="punct">。</span>`,
        en: "In the evening, Mom and Dad helped the two little pups pitch a cozy tent under the big tree in the backyard.",
        enHtml: `<span class="en-word-group">In the evening,</span> <span class="en-word-group">Mom and Dad</span> <span class="en-word-group">helped the two little pups</span> <span class="en-word-group">pitch a cozy tent</span> <span class="en-word-group">under the big tree in the backyard.</span>`
      }},
      {{
        img: "{s26_p[1]}",
        text: "草丛里飞出许多一闪一闪的萤火虫，像提着小灯笼跟她们打招呼。",
        ruby: `<span class="word-group"><ruby>草<rt>cǎo</rt></ruby><ruby>丛<rt>cóng</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="word-group"><ruby>飞<rt>fēi</rt></ruby><ruby>出<rt>chū</rt></ruby></span><span class="word-group"><ruby>许<rt>xǔ</rt></ruby><ruby>多<rt>duō</rt></ruby></span><span class="word-group"><ruby>一<rt>yì</rt></ruby><ruby>闪<rt>shǎn</rt></ruby><ruby>一<rt>yì</rt></ruby><ruby>闪<rt>shǎn</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>萤<rt>yíng</rt></ruby><ruby>火<rt>huǒ</rt></ruby><ruby>虫<rt>chóng</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>像<rt>xiàng</rt></ruby><ruby>提<rt>tí</rt></ruby><ruby>着<rt>zhe</rt></ruby></span><span class="word-group"><ruby>小<rt>xiǎo</rt></ruby><ruby>灯<rt>dēng</rt></ruby><ruby>笼<rt>long</rt></ruby></span><span class="word-group"><ruby>跟<rt>gēn</rt></ruby><ruby>她<rt>tā</rt></ruby><ruby>们<rt>men</rt></ruby></span><span class="word-group"><ruby>打<rt>dǎ</rt></ruby><ruby>招<rt>zhāo</rt></ruby><ruby>呼<rt>hu</rt></ruby></span><span class="punct">。</span>`,
        en: "Many twinkling fireflies flew out of the grass, waving hello like they were carrying tiny lanterns.",
        enHtml: `<span class="en-word-group">Many twinkling fireflies</span> <span class="en-word-group">flew out of the grass,</span> <span class="en-word-group">waving hello</span> <span class="en-word-group">like they were carrying</span> <span class="en-word-group">tiny lanterns.</span>`
      }},
      {{
        img: "{s26_p[2]}",
        text: "全家人坐在野餐垫上抬头看银河，数着夜空里亮晶晶的星星。",
        ruby: `<span class="word-group"><ruby>全<rt>quán</rt></ruby><ruby>家<rt>jiā</rt></ruby><ruby>人<rt>rén</rt></ruby></span><span class="word-group"><ruby>坐<rt>zuò</rt></ruby><ruby>在<rt>zài</rt></ruby></span><span class="word-group"><ruby>野<rt>yě</rt></ruby><ruby>餐<rt>cān</rt></ruby><ruby>垫<rt>diàn</rt></ruby><ruby>上<rt>shàng</rt></ruby></span><span class="word-group"><ruby>抬<rt>tái</rt></ruby><ruby>头<rt>tóu</rt></ruby><ruby>看<rt>kàn</rt></ruby><ruby>银<rt>yín</rt></ruby><ruby>河<rt>hé</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>数<rt>shǔ</rt></ruby><ruby>着<rt>zhe</rt></ruby></span><span class="word-group"><ruby>夜<rt>yè</rt></ruby><ruby>空<rt>kōng</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="word-group"><ruby>亮<rt>liàng</rt></ruby><ruby>晶<rt>jīng</rt></ruby><ruby>晶<rt>jīng</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>星<rt>xīng</rt></ruby><ruby>星<rt>xing</rt></ruby></span><span class="punct">。</span>`,
        en: "The whole family sat on a picnic mat looking up at the Milky Way and counting the sparkling stars in the night sky.",
        enHtml: `<span class="en-word-group">The whole family</span> <span class="en-word-group">sat on a picnic mat</span> <span class="en-word-group">looking up at the Milky Way</span> <span class="en-word-group">and counting the sparkling stars</span> <span class="en-word-group">in the night sky.</span>`
      }},
      {{
        img: "{s26_p[3]}",
        text: "钻进温暖的睡袋里，听妈妈用手电筒照着绘本讲晚安故事，真幸福呀！",
        ruby: `<span class="word-group"><ruby>钻<rt>zuān</rt></ruby><ruby>进<rt>jìn</rt></ruby></span><span class="word-group"><ruby>温<rt>wēn</rt></ruby><ruby>暖<rt>nuǎn</rt></ruby><ruby>的<rt>de</rt></ruby></span><span class="word-group"><ruby>睡<rt>shuì</rt></ruby><ruby>袋<rt>dài</rt></ruby><ruby>里<rt>lǐ</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>听<rt>tīng</rt></ruby><ruby>妈<rt>mā</rt></ruby><ruby>妈<rt>ma</rt></ruby></span><span class="word-group"><ruby>用<rt>yòng</rt></ruby><ruby>手<rt>shǒu</rt></ruby><ruby>电<rt>diàn</rt></ruby><ruby>筒<rt>tǒng</rt></ruby></span><span class="word-group"><ruby>照<rt>zhào</rt></ruby><ruby>着<rt>zhe</rt></ruby><ruby>绘<rt>huì</rt></ruby><ruby>本<rt>běn</rt></ruby></span><span class="word-group"><ruby>讲<rt>jiǎng</rt></ruby><ruby>晚<rt>wǎn</rt></ruby><ruby>安<rt>ān</rt></ruby><ruby>故<rt>gù</rt></ruby><ruby>事<rt>shi</rt></ruby></span><span class="punct">，</span><span class="word-group"><ruby>真<rt>zhēn</rt></ruby><ruby>幸<rt>xìng</rt></ruby><ruby>福<rt>fú</rt></ruby><ruby>呀<rt>ya</rt></ruby></span><span class="punct">！</span>`,
        en: "Snuggling into warm sleeping bags and listening to Mom read a bedtime storybook by flashlight felt so happy!",
        enHtml: `<span class="en-word-group">Snuggling into</span> <span class="en-word-group">warm sleeping bags</span> <span class="en-word-group">and listening to Mom</span> <span class="en-word-group">read a bedtime storybook by flashlight</span> <span class="en-word-group">felt so happy!</span>`
      }}
    ],
    vocab: [
      {{ hz: "帐篷", py: "zhàng peng", en: "tent" }},
      {{ hz: "萤火虫", py: "yíng huǒ chóng", en: "firefly" }},
      {{ hz: "银河", py: "yín hé", en: "Milky Way" }},
      {{ hz: "睡袋", py: "shuì dài", en: "sleeping bag" }}
    ]
  }}
];"""

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

target_end = """      { hz: "过敏", py: "guò mǐn", en: "allergic" },
      { hz: "勋章", py: "xūn zhāng", en: "medal" }
    ]
  }
];"""

assert target_end in html, "Could not find end of Story 22 in index.html"
html = html.replace(target_end, """      { hz: "过敏", py: "guò mǐn", en: "allergic" },
      { hz: "勋章", py: "xūn zhāng", en: "medal" }
    ]
""" + new_stories_js, 1)

old_categories = """const CATEGORIES = [
  { id: 'all', label: '✨ 全部故事 · All (22)' },
  { id: 'dogcop', label: '🐶 神探汪汪 · Dog Cop (4)' },
  { id: 'weird', label: '🤪 疯狂学校 · My Weird School (4)' },
  { id: 'adventure', label: '🕵️ 脑洞探秘 · Mystery & Sci-Fi (2)' },
  { id: 'school', label: '🏫 校园日常 · School Life (4)' },
  { id: 'fairy', label: '🐾 童话绘本 · Animal Tales (8)' }
];"""

new_categories = """const CATEGORIES = [
  { id: 'all', label: '✨ 全部故事 · All (26)' },
  { id: 'bluepup', label: '🐾 蓝小狗一家 · Blue Pup (4)' },
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

print("Successfully updated index.html with Bluey Stories 23-26 and updated CATEGORIES!")
