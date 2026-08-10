# -*- coding: utf-8 -*-
"""邓兴华 L06 课件 builder（page-id 契约，课程设计卡 2026-08-03 确认）
课名：一般现在时实义动词与 want/like 表达
  G16 一般现在时非三单主语（肯定/否定/疑问）
  G17 食物可数与不可数名词分类
  G18 want to do sth. 结构
  20 三餐食物词 / L6 特殊收官拼读（26字母总复习 + 5 易混音对）
  阅读 A 母本改编(HN2026_L6_reading_a) + B 原创调查(teacher_authored) + C 五选四母本(HN2026_L6_w5)
精简结构：CORE/EXTEND/HOME 三级，不堆冗余拓展页。
复用 courseware_engine 的 helper 与阅读块；内容全部换为 L06。
"""
import json, os, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

core = _load("core", "courseware_core.py")
g    = _load("g",    "gen_l1_l13_v2.py")
E    = _load("eng",  "courseware_engine.py")

section_head = g.section_head
sub_label    = g.sub_label
key_points   = g.key_points
page         = core.page
build_courseware = core.build_courseware
quiz_html    = E.quiz_html
flash_grid   = E.flash_grid
game_board   = E.game_board
vocab_cn2en  = E.vocab_cn2en

# ============================================================
# 一、内容数据
# ============================================================
# L06 20 词（内容蓝图 §一 卡片原样）
L06_WORDS = [
    ("food", "/fuːd/", "n.", "食物", "healthy food / fast food", "I like healthy food.", "food 里两个 o 像两个鸡蛋"),
    ("fruit", "/fruːt/", "n.", "水果", "fresh fruit / fruit salad", "I eat fruit every day.", "fr-ui-t 音似福如它"),
    ("vegetable", "/ˈvedʒtəbl/", "n.", "蔬菜", "green vegetables", "We should eat more vegetables.", "veget(植物)+able(能)"),
    ("apple", "/ˈæpl/", "n.", "苹果", "an apple / apple juice", "An apple a day keeps the doctor away.", "a-pp-le 音似阿婆"),
    ("banana", "/bəˈnɑːnə/", "n.", "香蕉", "a banana / banana milk", "I have a banana for breakfast.", "ba-na-na 三根香蕉"),
    ("orange", "/ˈɒrɪndʒ/", "n.", "橙子", "an orange / orange juice", "I drink orange juice every morning.", "o-range 首字母像橙子"),
    ("strawberry", "/ˈstrɔːbəri/", "n.", "草莓", "strawberries", "I like strawberries very much.", "straw(稻草)+berry(浆果)"),
    ("tomato", "/təˈmɑːtəʊ/", "n.", "西红柿", "tomatoes", "I don't like tomatoes.", "to-ma-to 音似他码头"),
    ("potato", "/pəˈteɪtəʊ/", "n.", "土豆", "potatoes / potato chips", "My father likes potatoes.", "po-ta-to 音似剖它头"),
    ("milk", "/mɪlk/", "n.", "牛奶", "a glass of milk", "I drink milk every morning.", "mi-lk 牛奶加蜜更好喝"),
    ("bread", "/bred/", "n.", "面包", "a piece of bread", "I have bread for breakfast.", "bread 里藏 read(读)"),
    ("chicken", "/ˈtʃɪkɪn/", "n.", "鸡肉", "fried chicken", "I like chicken but not fish.", "chick(小鸡)+en"),
    ("rice", "/raɪs/", "n.", "米饭", "a bowl of rice", "We eat rice for lunch.", "rice 里藏 ice(冰)"),
    ("eggs", "/eɡz/", "n.", "鸡蛋", "boiled eggs / fry eggs", "I eat two eggs every morning.", "egg 加 s 变复数"),
    ("breakfast", "/ˈbrekfəst/", "n.", "早餐", "have breakfast", "I have breakfast at 7:00.", "break(打破)+fast(斋戒)"),
    ("lunch", "/lʌntʃ/", "n.", "午餐", "have lunch", "We have lunch at school.", "lunch 音似浪吃"),
    ("dinner", "/ˈdɪnə(r)/", "n.", "晚餐", "have dinner", "My family have dinner together.", "din-ner 音似订呢"),
    ("like", "/laɪk/", "v.", "喜欢", "like sth. / like to do", "I like apples and bananas.", "like 音似赖客"),
    ("want", "/wɒnt/", "v.", "想要", "want sth. / want to do", "I want to eat an apple.", "want 里藏 ant(蚂蚁)"),
    ("eat", "/iːt/", "v.", "吃", "eat sth. / eat breakfast", "I eat breakfast at home.", "eat 音似亿特"),
]

# L5 复习：20 运动词（复习导入词汇快闪）
L5_SPORT_WORDS = [
    ("basketball", "/ˈbɑːskɪtbɔːl/", "n.", "篮球", "play basketball", "We play basketball after class.", ""),
    ("soccer", "/ˈsɒkə(r)/", "n.", "足球", "play soccer", "Tom plays soccer with friends.", ""),
    ("volleyball", "/ˈvɒlibɔːl/", "n.", "排球", "play volleyball", "She plays volleyball on weekends.", ""),
    ("tennis", "/ˈtenɪs/", "n.", "网球", "play tennis", "Tennis is difficult for me.", ""),
    ("ping-pong", "/ˈpɪŋpɒŋ/", "n.", "乒乓球", "play ping-pong", "Ping-pong needs quick hands.", ""),
    ("bat", "/bæt/", "n.", "球拍", "a baseball bat", "I have a baseball bat.", ""),
    ("ball", "/bɔːl/", "n.", "球", "pass the ball", "Pass the ball to me.", ""),
    ("TV", "/ˌtiːˈviː/", "n.", "电视", "watch TV", "I watch TV on weekends.", ""),
    ("team", "/tiːm/", "n.", "队", "a basketball team", "Our team is very good.", ""),
    ("sport", "/spɔːt/", "n.", "运动", "do sports", "Sports make us happy.", ""),
    ("good", "/ɡʊd/", "adj.", "好的", "be good at", "Our team is good.", ""),
    ("interesting", "/ˈɪntrəstɪŋ/", "adj.", "有趣的", "an interesting game", "Soccer is interesting.", ""),
    ("fun", "/fʌn/", "adj./n.", "有趣的", "have fun", "We have fun together.", ""),
    ("relaxing", "/rɪˈlæksɪŋ/", "adj.", "放松的", "a relaxing sport", "Ping-pong is relaxing.", ""),
    ("boring", "/ˈbɔːrɪŋ/", "adj.", "无聊的", "a boring book", "Soccer is not boring.", ""),
    ("difficult", "/ˈdɪfɪkəlt/", "adj.", "困难的", "a difficult question", "Tennis is difficult.", ""),
    ("easy", "/ˈiːzi/", "adj.", "容易的", "an easy question", "Ping-pong is easy for me.", ""),
    ("play", "/pleɪ/", "v.", "玩；打", "play sports", "I like to play basketball.", ""),
    ("sound", "/saʊnd/", "v.", "听起来", "sound good", "That sounds fun.", ""),
    ("watch", "/wɒtʃ/", "v.", "观看", "watch games", "We watch games on TV.", ""),
]

# ============================================================
# 二、辅助
# ============================================================
def ext_card(w):
    en, ph, pos, cn, coll, ex, hook = w
    return ('<div class="ext-card"><div class="ext-word">%s</div>'
            '<div class="ext-ph">%s · %s</div><div class="ext-cn">%s</div>'
            '<div class="ext-coll">搭配：%s</div><div class="ext-ex">例句：%s</div>'
            '<div class="ext-hook">💡 %s</div></div>' % (en, ph, pos, cn, coll, ex, hook))

# L06 自绘样式（引擎 page-id CSS 缺 vg/ext-word/gb/gtp/ep 等类，用主题变量补齐）
CSS_L06 = r"""
.vg{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px;margin:10px 0}
.ext-word{font-size:26px;font-weight:800;color:var(--brand);margin-bottom:2px}
.ext-ph{font-size:14px;color:var(--text-secondary)}
.ext-cn{font-size:20px;font-weight:700;color:var(--text-primary);margin:4px 0}
.ext-coll{font-size:14px;color:var(--text-secondary)}
.ext-ex{font-size:14px;margin-top:6px;color:var(--text-primary);line-height:1.6}
.ext-hook{font-size:13px;margin-top:6px;color:var(--sop-purple);background:var(--table-highlight-bg);border-left:3px solid var(--accent);padding:6px 8px;border-radius:6px}
.gb{background:var(--card-bg);border-radius:12px;padding:18px;box-shadow:var(--card-shadow);border-top:4px solid var(--brand);margin:10px 0}
.gb h3{margin:0 0 10px;color:var(--text-primary)}
.gtp{font-size:14px;color:var(--text-primary);background:var(--bg-start);border-radius:8px;padding:10px 14px;margin:8px 0;border-left:4px solid var(--accent)}
.ep{background:var(--error-row-bg);border-radius:8px;padding:12px 14px;margin:8px 0}
.el{display:inline-block;font-weight:800;color:var(--error);margin-bottom:4px}
.ec2{font-size:14px;color:var(--text-primary);line-height:1.7}
"""

def vocab_groups(words, size=5):
    return [words[i:i+size] for i in range(0, len(words), size)]

def new_word_page(title, words, label):
    body = section_head("词", title) + '<div class="body-text"><span class="highlight">%s</span>音标 · 词性 · 中文 · 中考搭配 · 例句 · 记忆法，翻牌自检。</div>' % label
    body += '<div class="vg">' + "".join(ext_card(w) for w in words) + '</div>'
    body += '<div class="note-panel"><div class="np-title">跟读要点</div>先听老师范读两遍，再跟读三遍，最后捂住英文看中文说英文。</div>'
    return body

# ============================================================
# 三、页面装配
# ============================================================
def build_l06():
    _QSEQ_save = E._QSEQ
    E._QSEQ = 0
    card = {
        "lesson": 6, "student": "邓兴华", "tier": "中等", "stage": "S2", "type": "normal",
        "grammar": ["一般现在时实义动词", "食物可数与不可数", "want to do"], "theme": "三餐与饮食习惯",
        "vocab": {"new_count": 20, "review_count": 0, "theme": "food"},
        "phonics": "26字母总复习+5易混音对",
    }
    title = "第6课时 · 三餐与饮食习惯"
    stage_badge = "中等 · Stage 2 · L6"
    pages = {}
    seg = {}
    page_meta = {}
    p = 1
    def add(inner, seg_id, t="", sub="", priority="CORE", minutes=5):
        nonlocal p
        pages[p] = page(p, t, sub, inner, active=(p == 1))
        seg.setdefault(seg_id, [p, p]); seg[seg_id][1] = p
        page_meta[p] = {"p": priority, "m": minutes}
        p += 1

    # ---- 段1 封面 + 复习导入（强制 3 页复习 L5） ----
    cover = ('<div class="cover-wrap">'
             '<div class="cover-badge">第 6 课时 · 邓兴华</div>'
             '<div class="cover-title">三餐与饮食习惯</div>'
             '<div class="cover-sub">一般现在时实义动词 · want/like 表达</div>'
             '<div class="cover-tagline">中等 · 初二</div>'
             '<div class="cover-info">'
             '<div class="cover-info-num"><div class="ci-label">新词</div><div class="ci-val">20</div></div>'
             '<div class="cover-info-num"><div class="ci-label">语法考点</div><div class="ci-val">3</div></div>'
             '<div class="cover-info-num"><div class="ci-label">页数</div><div class="ci-val">42</div></div>'
             '</div>'
             '<div class="cover-emoji">🍎🥛🍚</div></div>')
    add(cover, 1)

    goal = (section_head("标", "本课学习目标") +
            '<div class="chip-row">'
            '<div class="chip"><span class="chip-icon">🆕</span>20 个三餐与食物高频词</div>'
            '<div class="chip"><span class="chip-icon">🧩</span>一般现在时 / 可数不可数 / want to do</div>'
            '<div class="chip"><span class="chip-icon">📖</span>记叙 / 调查 / 说明阅读</div>'
            '<div class="chip"><span class="chip-icon">🔤</span>26 字母总复习 + 5 组易混音对</div>'
            '</div>' +
            '<div class="kmap">' +
            '<div class="kmap-node"><div class="kn-title">词汇</div><div class="kn-body">20 个食物、三餐与动作词，滚动复现。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">语法</div><div class="kn-body">非三单一般现在时、可数与不可数、want to do。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">阅读</div><div class="kn-body">饮食习惯：莉莉 / 调查 / 健康饮食。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">拼读</div><div class="kn-body">26 字母收官 + 5 组易混音对听辨。</div></div>' +
            '</div>' +
            '<div class="note-panel"><div class="np-title">闯关规则</div>先玩「上节课闯关」唤醒 L5 的祈使句/What/like，再进入本课新词与语法，全对即可通关。</div>')
    add(goal, 1, "第6课时 · 学习目标", "四个模块一目了然")

    # 复习 L5 语法闯关：G13 祈使句 / G14 What 问句 / G15 like to do
    l5_g = [("___ the door, please.", "Open", ["Opening", "Opens"]),
            ("Don't ___ in the classroom.", "run", ["runs", "running"]),
            ("___ sports do you like?", "What", ["How", "Where"]),
            ("Do you like tennis?", "Yes, I ___.", ["do", "am", "does"]),
            ("I like ___ basketball.", "to play", ["playing", "plays"]),
            ("___ you like soccer?", "Do", ["Are", "Does"])]
    l5g = (section_head("复", "上节课 · 语法快闪闯关") +
           '<div class="body-text">还记得上节课的 <span class="highlight">祈使句 Do/Don&#39;t / What 问句 / like to do</span> 吗？点击作答，答对有彩带动画！</div>' +
           game_board("祈使句 / What 问句 / like 用法", "⚡", "从上节课 3 个语法点各抽几题，快速唤醒记忆。", quiz_html(l5_g)) +
           '<div class="note-panel"><div class="np-title">闯关提示</div>祈使句动词原形开头，否定 Don&#39;t + 原形；What 问句看答语选疑问词；like 后接名词或 to do；一般疑问句答语用 do。</div>')
    add(l5g, 1, "上节课 · 语法闯关", "祈使句 · What 问句 · like")

    # 复习 L5 词汇闯关：20 运动词
    l5_v = [("篮球 是哪个词？", "basketball", ["soccer", "volleyball"]),
            ("有趣的 是哪个词？", "interesting", ["boring", "easy"]),
            ("球拍 是哪个词？", "bat", ["ball", "team"]),
            ("困难的 是哪个词？", "difficult", ["easy", "fun"]),
            ("观看 是哪个词？", "watch", ["play", "sound"]),
            ("放松的 是哪个词？", "relaxing", ["interesting", "boring"]),
            ("听起来 是哪个词？", "sound", ["play", "watch"]),
            ("队伍 是哪个词？", "team", ["sport", "TV"])]
    l5v = (section_head("复", "上节课 · 词汇闯关") +
           '<div class="body-text">上节课 20 个运动词还记得吗？先闯关再翻牌自检。</div>' +
           game_board("运动词 8 连问", "🎮", "看中文，选英文，音形义一次叫醒。", quiz_html(l5_v)) +
           '<div class="sub-label">翻牌自检 · 上节课 20 词（点击翻面）</div>' +
           flash_grid([(w[3], w[0]) for w in L5_SPORT_WORDS]))
    add(l5v, 1, "上节课 · 词汇闯关", "运动 20 词 · 翻牌自检")

    # 复习 L5 核心句型
    l5s = (section_head("复", "上节课 · 核心句型口头演练") +
           '<div class="body-text"><span class="highlight">快速口头翻译</span>（每人一句，看谁又快又准）</div>' +
           key_points([("①", "What sports do you like?（你喜欢什么运动？）→ I like to play basketball."),
                       ("②", "Let's play soccer after class.（下课后我们踢足球吧。）→ Good idea! / Sounds fun!"),
                       ("③", "Tennis is difficult, but it is interesting.（网球难，但有趣。）")]) +
           '<div class="note-panel"><div class="np-title">复习要点</div>What 问句 + like to do 是今天 want to do 的垫脚石：like to do → want to do 都是「动词 + to + 原形」。</div>')
    add(l5s, 1, "上节课 · 核心句型", "口头翻译 · 唤醒 to do")

    # ---- 段2 词汇新授（20 词 4 组 + 总览 + 闯关） ----
    grps = vocab_groups(L06_WORDS)
    add(new_word_page("三餐与食物词 · 第一组", grps[0], "食物总称与水果 1–5"), 2, "新词 ①", "food/fruit/vegetable/apple/banana")
    add(new_word_page("三餐与食物词 · 第二组", grps[1], "水果续 · 6–10"), 2, "新词 ②", "orange/strawberry/tomato/potato/milk")
    add(new_word_page("三餐与食物词 · 第三组", grps[2], "主食与三餐 · 11–15"), 2, "新词 ③", "bread/chicken/rice/eggs/breakfast")
    add(new_word_page("三餐与食物词 · 第四组", grps[3], "三餐与动词 · 16–20"), 2, "新词 ④", "lunch/dinner/like/want/eat")
    vocab_overview = (section_head("词", "新词总览 · 20 词卡片墙") +
                      '<div class="body-text"><span class="highlight">全部 20 词</span> 按可数 / 不可数 / 动词分三区，建立本课词场全貌。</div>' +
                      '<div class="sub-label">🍎 可数名词</div>' +
                      '<div class="vg">' + "".join(ext_card(w) for w in [L06_WORDS[2], L06_WORDS[3], L06_WORDS[4], L06_WORDS[5], L06_WORDS[6], L06_WORDS[7], L06_WORDS[8], L06_WORDS[13]]) + '</div>' +
                      '<div class="sub-label">🥛 不可数名词</div>' +
                      '<div class="vg">' + "".join(ext_card(w) for w in [L06_WORDS[0], L06_WORDS[1], L06_WORDS[9], L06_WORDS[10], L06_WORDS[11], L06_WORDS[12], L06_WORDS[14], L06_WORDS[15], L06_WORDS[16]]) + '</div>' +
                      '<div class="sub-label">✋ 动词</div>' +
                      '<div class="vg">' + "".join(ext_card(w) for w in [L06_WORDS[17], L06_WORDS[18], L06_WORDS[19]]) + '</div>')
    add(vocab_overview, 2, "新词总览", "可数 / 不可数 / 动词 三区")
    vocab_quiz = (section_head("词", "新词闯关 · 看中文选英文") +
                  '<div class="body-text"><span class="highlight">8 连问</span> 抽查今天 20 词，答对才算过关。</div>' +
                  game_board("食物词 8 连问", "🍎", "看中文，选英文，检验记忆效果。",
                             quiz_html([("西红柿 是哪个词？", "tomato", ["potato", "strawberry"]),
                                        ("草莓 是哪个词？", "strawberry", ["orange", "banana"]),
                                        ("早餐 是哪个词？", "breakfast", ["lunch", "dinner"]),
                                        ("想要 是哪个词？", "want", ["like", "eat"]),
                                        ("米饭 是哪个词？", "rice", ["bread", "chicken"]),
                                        ("蔬菜 是哪个词？", "vegetable", ["fruit", "food"]),
                                        ("牛奶 是哪个词？", "milk", ["water", "juice"]),
                                        ("晚餐 是哪个词？", "dinner", ["lunch", "breakfast"])])))
    add(vocab_quiz, 2, "新词闯关", "20 词抽查")

    # ---- 段3 语法 G16/G17/G18 ----
    g16a = (section_head("法", "G16 · 一般现在时（非三单主语）构成与用法") +
            '<div class="body-text"><span class="highlight">口诀：我你我们和他们，动词原形不变化；否定 don&#39;t 加原形，疑问 Do 开头加原形。</span></div>' +
            '<div class="formula-box"><div class="formula-label">结构公式（主语 = I / you / we / they / 复数名词）</div>' +
            '<div class="formula-main">肯定：主语 + 动词原形 + …</div>' +
            '<div class="formula-main">否定：主语 + don&#39;t + 动词原形 + …</div>' +
            '<div class="formula-main">疑问：Do + 主语 + 动词原形 + …?</div>' +
            '<div class="formula-ex">I eat an apple. ／ We like vegetables. ／ They don&#39;t drink milk. ／ Do you want breakfast?</div></div>' +
            '<div class="gtp"><strong>⚠️ 三单留到 L10：</strong>he / she / it / 单数名词作主语本课不涉及，动词也不加 -s。</div>' +
            '<div class="ep"><span class="el">中考辨析</span><div class="ec2">① don&#39;t = do not；② 否定和疑问句中动词必须用原形（I don&#39;t like... ✅ / I don&#39;t likes... ❌）；③ 实义动词否定不借 be 动词（I am not like... ❌）。</div></div>')
    add(g16a, 3, "G16 · 构成与用法", "非三单 · 肯定/否定/疑问")
    g16b = (section_head("法", "G16 · 易错专练") +
            '<div class="body-text">找出<b>正确</b>的表达，并说出错因。</div>' +
            quiz_html([("I ___ apples.", "don't like", ["don't likes", "am not like"]),
                       ("Do you ___ rice for lunch?", "want", ["wants", "wanting"]),
                       ("They ___ bread every morning.", "eat", ["eats", "eating"]),
                       ("___ we eat fruit?", "Do", ["Are", "Does"]),
                       ("I not like milk. 的正确说法？", "I don't like milk.", ["I not like milk.", "I am not like milk."]),
                       ("We ___ vegetables at school.", "eat", ["eats", "are eat"])]) +
            '<div class="note-panel"><div class="np-title">改错思路</div>don&#39;t / Do 后接动词原形；非三单主语动词不加 -s；否定用 don&#39;t 不用 not 直接否定实义动词。</div>')
    add(g16b, 3, "G16 · 易错与色卡", "don't 后原形 · Do 后原形")

    g17a = (section_head("法", "G17 · 食物可数与不可数名词分类") +
            '<div class="body-text"><span class="highlight">口诀：能数有复数（apples, eggs），不能数没复数（milk, rice, bread）。</span></div>' +
            '<div class="gb"><h3>本课 20 词分类</h3><table class="gt">' +
            '<tr><th>类别</th><th>特点</th><th>本课词汇</th></tr>' +
            '<tr><td>可数</td><td>有复数，可加 a/an</td><td class="ec">apple/banana/orange/strawberry/tomato/potato/eggs/vegetable</td></tr>' +
            '<tr><td>不可数</td><td>无复数，不加 a/an</td><td class="ec">food/fruit/milk/bread/rice/chicken(鸡肉)/breakfast/lunch/dinner</td></tr>' +
            '</table></div>' +
            '<div class="gtp"><strong>复数变化：</strong>strawberry→strawberries（辅音+y 去 y 加 ies）；tomato→tomatoes / potato→potatoes（以 o 结尾加 -es）；其余直接加 -s。</div>' +
            '<div class="ep"><span class="el">中考辨析</span><div class="ec2">可数名词单数不能裸奔（an apple ✅ / apple ❌）；可数泛指用复数（I like apples）；不可数直接用它本身（I drink milk）。</div></div>')
    add(g17a, 3, "G17 · 构成与用法", "可数 / 不可数 分类")
    g17b = (section_head("法", "G17 · 易错专练") +
            '<div class="body-text">选择<b>正确</b>的表达，理解为什么。</div>' +
            quiz_html([("I like ___.", "apples", ["apple", "a apple"]),
                       ("I drink ___ every morning.", "milk", ["milks", "a milk"]),
                       ("We eat ___ for lunch.", "rice", ["rices", "a rice"]),
                       ("___ 是 strawberries 的正确来源。", "strawberry", ["strawberrys", "strawberies"]),
                       ("I like ___（西红柿）。", "tomatoes", ["tomatos", "tomato"]),
                       ("The doctor says ___ is good for us.", "fruit", ["fruits", "a fruit"])]) +
            '<div class="note-panel"><div class="np-title">改错思路</div>可数泛指用复数；不可数不变复数、不加 a/an；o 结尾加 -es；辅音+y 去 y 加 ies。</div>')
    add(g17b, 3, "G17 · 易错与色卡", "tomatoes · strawberries · 不可数不加s")

    g18a = (section_head("法", "G18 · want to do sth. 结构") +
            '<div class="body-text"><span class="highlight">口诀：want 后接 to do，想要做某事；想要某物直接接，want sth. 要记牢。</span></div>' +
            '<div class="formula-box"><div class="formula-label">结构公式</div>' +
            '<div class="formula-main">want to do sth.：I want to eat an apple.</div>' +
            '<div class="formula-main">want sth.：I want an apple.</div>' +
            '<div class="formula-main">want sb. to do sth.：I want you to eat breakfast.</div>' +
            '<div class="formula-main">否定：I don&#39;t want to eat rice.</div>' +
            '<div class="formula-main">疑问：Do you want to drink milk?</div></div>' +
            '<div class="gtp"><strong>螺旋链：</strong>L5 like to do → <b>L6 want to do</b> → L13 would like to do（三阶完成）。</div>' +
            '<div class="ep"><span class="el">中考辨析</span><div class="ec2">want 后必须接 to do（不定式），不能接 doing（I want to eat ✅ / I want eating ❌）；to 后用动词原形。</div></div>')
    add(g18a, 3, "G18 · 构成与用法", "want to do / want sth / want sb to do")
    g18b = (section_head("法", "G18 · 易错专练") +
            '<div class="body-text">选择<b>正确</b>的 want 用法。</div>' +
            quiz_html([("I ___ an apple.", "want", ["want to", "wanting"]),
                       ("I want ___ a banana.", "to eat", ["eat", "eating"]),
                       ("They don't want ___ fast food.", "to eat", ["eat", "eating"]),
                       ("___ you want to drink milk?", "Do", ["Are", "Does"]),
                       ("I want ___ an orange（想要一个橙子）。", "want", ["want to", "wanting"]),
                       ("She wants to ___ healthy food.（三单留至 L10，此处仅认识）", "eat", ["eats", "eating"])]) +
            '<div class="note-panel"><div class="np-title">改错思路</div>want sth.（要某物）vs want to do（要做某事）；want 后不接 doing；to 后动词原形。</div>')
    add(g18b, 3, "G18 · 易错与色卡", "want to do · to 后原形")

    gsum = (section_head("法", "三大考点综合梳理") +
            g.grammar_cards([("用法", "一般现在时表经常性习惯；本课仅非三单主语"),
                             ("构成", "主语 + 动词原形；否定 don&#39;t + 原形；疑问 Do 开头"),
                             ("易错", "don&#39;t 后动词不加 -s；可数泛指用复数；不可数不加 s"),
                             ("例句", "I eat an apple every day. ／ We don&#39;t drink cola."),
                             ("注意", "三单（he/she/it）留至 L10；量词表达留至 L12"),
                             ("口诀", "原形走天下；否定 don&#39;t 加原形；Do 开头问一句")]) +
            key_points([("G16 一般现在时", "非三单主语 + 动词原形；否定 don&#39;t + 原形；疑问 Do 开头。例句：I like milk. / They don&#39;t eat bread."),
                        ("G17 可数不可数", "可数有复数可加 a/an；不可数无复数不加 a/an。例句：apples ✅ / milks ❌"),
                        ("G18 want to do", "want sth. 要某物；want to do 要做某事；to 后原形。例句：I want to eat an apple.")]) +
            '<div class="note-panel"><div class="np-title">三考点怎么连</div>三条都发生在「一般现在时 · 三餐饮食」这个主题里：用一般现在时说三餐（G16），用可数不可数聊食物（G17），用 want to do 表达想吃想喝（G18）。</div>')
    add(gsum, 3, "三大考点综合梳理", "一条主线 · 三个考点")

    # 中考真题体验：HN2026_L6_cloze 完形（真题母本改编）
    zhenti = (section_head("法", "中考真题体验 · 完形填空") +
              '<div class="body-text"><span class="highlight">2026 湖南中考结构改编 · 完形填空</span>（一般现在时 + 可数不可数 + want/like 综合）。选出最恰当的一项。</div>' +
              game_board("健康饮食完形", "📝", "短文中动词时态与名词单复数混考，正是本课考点。",
                         quiz_html([("I ___ healthy food every day.", "like", ["likes", "am"]),
                                    ("I ___ milk and bread with my mum.", "have", ["has", "drink"]),
                                    ("I ___ like fast food.", "don't", ["doesn't", "am not"]),
                                    ("We eat rice and ___ for lunch.", "vegetables", ["vegetable", "meats"]),
                                    ("We ___ water, not cola or juice.", "drink", ["drinks", "drinking"])])) +
              '<div class="note-panel"><div class="np-title">真题解析</div>① 主语 I 用原形 like；② I 用 have；③ I 否定用 don&#39;t；④ 泛指蔬菜用复数；⑤ we 用原形 drink。三单形式（likes/has/doesn&#39;t）本课先认识，L10 系统学。</div>')
    add(zhenti, 3, "中考真题体验", "完形 5 空 · 母本改编")

    pfill = (section_head("法", "语法综合填空 · G16/G17/G18 混考") +
             '<div class="body-text">本课三考点一次性混考，检测是否真正掌握。</div>' +
             quiz_html([("I ___ two eggs every morning.", "eat", ["eats", "eating"]),
                        ("___ your family have dinner together?", "Do", ["Does", "Are"]),
                        ("I want to ___ an orange.", "eat", ["eats", "eating"]),
                        ("My friends ___ milk.", "don't drink", ["don't drinks", "doesn't drink"]),
                        ("We like ___（蔬菜）。", "vegetables", ["vegetable", "a vegetable"]),
                        ("They want ___ apples.", "to eat", ["eat", "eating"])]) +
             '<div class="note-panel"><div class="np-title">自查</div>全对说明 G16/G17/G18 过关；错了回看对应「易错」页。</div>')
    add(pfill, 3, "语法综合填空", "三考点混考")

    # ---- 段4 随堂演练 + 句型 + 改错 ----
    q1 = (section_head("练", "随堂演练 ① · 一般现在时与 want to do") +
          quiz_html([("I ___ milk every morning.", "drink", ["drinks", "drinking"]),
                     ("We ___ fruit after dinner.", "eat", ["eats", "eating"]),
                     ("___ you want rice?", "Do", ["Are", "Does"]),
                     ("They don't ___ bread.", "like", ["likes", "liking"]),
                     ("I want ___ an apple.", "to eat", ["eat", "eating"]),
                     ("My friends ___ vegetables.", "like", ["likes", "liking"])]) +
          '<div class="note-panel"><div class="np-title">演练要点</div>主语是非三单（I/we/they/复数）时，动词原形；don&#39;t / Do 后也原形。</div>')
    add(q1, 4, "随堂演练 ①", "G16/G18 选择")
    q2 = (section_head("练", "随堂演练 ② · 可数与不可数") +
          quiz_html([("I like ___（草莓）。", "strawberries", ["strawberrys", "strawberies"]),
                     ("I drink a glass of ___ every day.", "milk", ["milks", "milkies"]),
                     ("We eat ___（土豆）for lunch.", "potatoes", ["potatos", "potato"]),
                     ("___（西红柿）are good for us.", "Tomatoes", ["Tomatos", "Tomato"]),
                     ("The doctor says ___ is healthy.", "fruit", ["fruits", "a fruit"]),
                     ("I eat two ___（鸡蛋）every morning.", "eggs", ["egg", "egges"])]) +
          '<div class="note-panel"><div class="np-title">演练要点</div>可数名词单复数变化（o 结尾加 -es、辅音+y 加 -ies）；不可数名词不变。</div>')
    add(q2, 4, "随堂演练 ②", "G17 选择")
    q3 = (section_head("练", "随堂演练 ③ · 综合诊断") +
          quiz_html([("Lily ___ breakfast at 7:00.", "has", ["have", "having"]),
                     ("We ___ rice and chicken for lunch.", "eat", ["eats", "eating"]),
                     ("Do they ___ bananas?", "want", ["wants", "wanting"]),
                     ("I don't ___ fast food.", "like", ["likes", "liking"]),
                     ("Tom wants ___ a basketball team.", "to join", ["join", "joining"]),
                     ("___ we eat fruit after meals?", "Should", ["Are", "Does"])]) +
          '<div class="note-panel"><div class="np-title">诊断说明</div>题 1/5 是认识性的三单/want to do 表达，本课以认识为主，L10 系统学习。</div>')
    add(q3, 4, "随堂演练 ③", "综合诊断")

    drill = (section_head("练", "句型操练 · 中译英") +
             '<div class="body-text"><span class="highlight">把中文翻成英文</span>（口头或笔头），再对照参考译文自检。</div>' +
             key_points([("①", "我每天吃一个苹果。→ I eat an apple every day."),
                         ("②", "他们不喜欢快餐。→ They don't like fast food."),
                         ("③", "你想喝牛奶吗？→ Do you want to drink milk?"),
                         ("④", "我晚饭想吃米饭和鸡肉。→ I want to eat rice and chicken for dinner."),
                         ("⑤", "我们早餐吃鸡蛋和面包。→ We eat eggs and bread for breakfast.")]) +
             '<div class="note-panel"><div class="np-title">翻译要点</div>非三单主语动词原形；否定 don&#39;t；疑问 Do 开头；want to do 表想吃想喝。</div>')
    add(drill, 4, "句型操练", "中译英 · 翻牌自检")

    err = (section_head("练", "改错专练 · 选一选") +
           '<div class="body-text">五组易错句，选择<b>正确</b>版本，理解为什么错。</div>' +
           quiz_html([("I don't likes milk. 的正确写法？", "I don't like milk.", ["I don't likes milk.", "I am not like milk."]),
                      ("Do you wants rice? 的正确写法？", "Do you want rice?", ["Do you wants rice?", "Are you want rice?"]),
                      ("I drink milks. 的正确写法？", "I drink milk.", ["I drink milks.", "I drink a milk."]),
                      ("I like tomato. 的正确写法？", "I like tomatoes.", ["I like tomato.", "I like tomatos."]),
                      ("I want eat an apple. 的正确写法？", "I want to eat an apple.", ["I want eat an apple.", "I want eating an apple."])]) +
           '<div class="note-panel"><div class="np-title">改错思路</div>don&#39;t/Do 后原形；不可数不加 s；可数泛指复数；want 后接 to do。</div>')
    add(err, 4, "改错专练", "选出正确句子 · 理解错因")

    # ---- 段5 阅读理解（左文右题） ----
    passages = json.load(open(os.path.join(HERE, "passage_bank.json"), encoding="utf-8"))
    pa = next((x for x in passages if x["id"] == "HN2026_L6_reading_a"), passages[0])
    paras_a = [s.strip() + "." for s in pa["text"].replace("A ", "").split(".") if s.strip()]
    a_quiz = [("1. What does Lily have for breakfast?", "milk and bread", ["rice and chicken", "apples and oranges"]),
              ("2. Where does Lily have lunch?", "at school", ["at home", "in a restaurant"]),
              ("3. What fruit does her family eat for dinner?", "apples, bananas, oranges", ["strawberries", "tomatoes"]),
              ("4. Which food does Lily NOT like?", "fast food", ["healthy food", "vegetables"]),
              ("5. What is the main idea?", "Healthy Eating Habits", ["My School", "Favorite Fruit"])]
    ra_page = (section_head("读", "阅读 A · Healthy Eating Habits（左文右题）") +
               '<div class="pri-row"><span class="pri-badge pri-core">CORE · 课堂必做</span>'
               '<span class="pri-note">课堂精读 · 三篇都读，A 是课上必须完成</span></div>' +
               '<div class="read-split">' +
               '<div class="read-left">' +
               '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in paras_a) + '</div>' +
               '<div class="note-panel"><div class="np-title">中文大意</div>莉莉每天有良好饮食习惯：早餐在家喝牛奶吃面包，午餐在学校和同学吃米饭、蔬菜和鸡肉，晚餐和家人吃水果。她喜欢健康食物，不喜欢快餐。</div>' +
               '<div class="note-panel"><div class="np-title">长难句拆解</div>① She has good eating habits. —— 三单 has（本课认识，L10 学）。<br>② Fruit and milk help her grow tall and strong. —— help sb. do sth.</div>' +
               '</div>' +
               '<div class="read-right">' +
               '<div class="read-right-head">📝 理解题 · 边读边选</div>' +
               '<div class="read-qs-scroll">' +
               quiz_html(a_quiz, cols=False) +
               '</div></div></div>' +
               '<div class="note-panel"><div class="np-title">答案解析</div>题1 For breakfast, I have milk and bread；题2 For lunch at school；题3 my family eat apples, bananas and oranges；题4 I do not like fast food；题5 主旨为健康饮食习惯。</div>')
    add(ra_page, 5, "阅读 A · 篇章＋理解题", "左文右题 · 边读边选", priority="CORE", minutes=8)

    # 阅读 B：饮食习惯调查（teacher_authored 原创，2026-08-02 授权）
    b_text = ("Here is a survey about students' eating habits in our school. We ask fifty students. "
              "Thirty-two students eat breakfast every day. They have eggs, bread and milk for breakfast. "
              "Eighteen students don't eat breakfast. They are often late for school. "
              "For lunch, most students eat rice, vegetables and chicken at school. "
              "After class, many students eat fruit. They want to be healthy. "
              "But some students like fast food. Fast food is delicious, but it is not good for our bodies. "
              "Good eating habits help students grow tall and strong. Do you have good eating habits?")
    paras_b = [x.strip() + "." for x in b_text.split(".") if x.strip()]
    b_quiz = [("1. How many students eat breakfast every day?", "thirty-two", ["eighteen", "fifty"]),
              ("2. What do these students have for breakfast?", "eggs, bread and milk", ["rice and chicken", "fruit and juice"]),
              ("3. What do most students eat for lunch?", "rice, vegetables and chicken", ["fast food", "eggs and bread"]),
              ("4. What does the word \"delicious\" mean?", "very tasty", ["very healthy", "very cheap"]),
              ("5. What is the best title?", "A Survey on Eating Habits", ["My Favorite Food", "Fast Food"])]
    rb_page = (section_head("读", "阅读 B · A Survey on Eating Habits（左文右题）") +
               '<div class="pri-row"><span class="pri-badge pri-extend">EXTEND · 时间充足时做</span>'
               '<span class="pri-note">调查报告 · 训练数字与对比信息</span></div>' +
               '<div class="read-split">' +
               '<div class="read-left">' +
               '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in paras_b) + '</div>' +
               '<div class="note-panel"><div class="np-title">中文大意</div>一项关于学生饮食习惯的调查：50 名学生中 32 人每天吃早餐，18 人不吃；午餐大多在学校吃米饭蔬菜鸡肉；有些学生喜欢快餐，但快餐对身体不好。</div>' +
               '<div class="note-panel"><div class="np-title">长难句拆解</div>① They want to be healthy. —— want to do 本课核心结构。<br>② Good eating habits help students grow tall. —— help sb. do sth.</div>' +
               '</div>' +
               '<div class="read-right">' +
               '<div class="read-right-head">📝 理解题 · 边读边选</div>' +
               '<div class="read-qs-scroll">' +
               quiz_html(b_quiz, cols=False) +
               '</div></div></div>' +
               '<div class="note-panel"><div class="np-title">答案解析</div>题1 数字定位 Thirty-two students；题2 eggs, bread and milk；题3 rice, vegetables and chicken；题4 delicious=非常美味（词义题）；题5 全文围绕饮食习惯调查。</div>')
    add(rb_page, 5, "阅读 B · 篇章＋理解题", "左文右题 · 调查文", priority="EXTEND", minutes=6)

    # 阅读 C：五选四（HN2026_L6_w5 母本）
    w5text = ("Eating healthy food is important for every student at school. Good food is the fuel for your body and your brain. "
              "A good breakfast helps you listen and learn in class with a clear mind. __(11)__ "
              "We should eat fruit every day after our three meals because fruit gives us vitamins. __(12)__ "
              "Fresh vegetables help our body grow tall and stay strong, so eat them often. __(13)__ "
              "Drink milk for strong bones and white teeth every morning before school. __(14)__ "
              "A good diet keeps us happy and full of energy for the whole day.")
    w5paras = [s.strip() for s in w5text.split(".") if s.strip()]
    w5opts = [("A", "Fruit gives us vitamins."), ("B", "We also need water every day."),
              ("C", "Candy is bad for our teeth."), ("D", "Exercise is good for us, too."),
              ("E", "Cola is a good drink for health.")]
    w5ans = {11: "A", 12: "B", 13: "D", 14: "C"}
    rc_page = (section_head("读", "阅读 C · 五选四（左文右题）") +
               '<div class="pri-row"><span class="pri-badge pri-home">HOME · 课后完成</span>'
               '<span class="pri-note">逻辑衔接专练 · 课后自测</span></div>' +
               '<div class="read-split">' +
               '<div class="read-left">' +
               '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in w5paras) + '</div>' +
               '<div class="note-panel"><div class="np-title">中文大意</div>健康饮食对学生很重要。好早餐帮助专心听讲；每天吃水果补维生素；多吃蔬菜长得高；早餐前喝牛奶强健骨骼；健康饮食让人整天有活力。</div>' +
               '</div>' +
               '<div class="read-right">' +
               '<div class="read-right-head">📝 五选四 · 逻辑衔接</div>' +
               '<div class="read-qs-scroll">' +
               '<div class="sub-label">从 A–E 中选最佳句填入空白（E 为多余项）</div>')
    for num in sorted(w5ans.keys()):
        ans = w5ans[num]
        rc_page += '<div class="w5-qq">__（%d）__ 应填：</div><div class="w5-opts">' % num
        for letter, text in w5opts:
            cor = '1' if letter == ans else '0'
            rc_page += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        rc_page += '</div>'
    rc_page += ('</div></div></div>' +
                '<div class="note-panel"><div class="np-title">答案解析</div>11→A（fruit 与 vitamins 呼应）；12→B（water 与 drink 呼应）；13→D（exercise 与 body 呼应）；14→C（candy 与 teeth 呼应）；E 为多余项，五选四。</div>')
    add(rc_page, 5, "阅读 C · 篇章＋五选四", "左文右题 · 逻辑衔接", priority="HOME", minutes=6)

    reading_tip = (section_head("读", "阅读解题 SOP") +
                   key_points([("① 先题后文", "先读题干圈关键词，再回原文定位。"),
                               ("② 细节题", "题干词多在原文原词复现，直接比对。"),
                               ("③ 词义题", "回该词所在句，用上下文（近义/反义/举例）猜词。"),
                               ("④ 推断题", "选「文中能推出」的，不选「文中没有说」的。"),
                               ("⑤ 主旨题", "看首尾段 + 每段首句，找反复出现的中心词。"),
                               ("⑥ 五选四", "先看空格前后句，找指代/逻辑连接词（because/so/but）。")]) +
                   '<div class="note-panel"><div class="np-title">本课阅读怎么练</div>A 篇课堂精读，B 篇同桌讨论，C 篇课后自测。做完回原文划出答案依据。</div>')
    add(reading_tip, 5, "阅读解题 SOP", "六步法")

    # ---- 段6 拼读（26 字母收官 + 5 易混音对） ----
    ph26 = (section_head("拼", "L6 拼读收官 · 26 字母总复习") +
            '<div class="body-text"><span class="highlight">Aa–Zz 全部 26 个字母</span>，本课不学新字母，把 L1–L5 学的音素整体回顾一遍。</div>' +
            '<div class="vg">' + "".join(
                '<div class="ext-card"><div class="ext-word">%s</div><div class="ext-cn">%s</div></div>' % (L, P)
                for L, P in [("Aa", "/æ/"), ("Bb", "/b/"), ("Cc", "/k/"), ("Dd", "/d/"), ("Ee", "/e/"),
                             ("Ff", "/f/"), ("Gg", "/ɡ/"), ("Hh", "/h/"), ("Ii", "/ɪ/"), ("Jj", "/dʒ/"),
                             ("Kk", "/k/"), ("Ll", "/l/"), ("Mm", "/m/"), ("Nn", "/n/"), ("Oo", "/ɒ/"),
                             ("Pp", "/p/"), ("Qq", "/kw/"), ("Rr", "/r/"), ("Ss", "/s/"), ("Tt", "/t/"),
                             ("Uu", "/ʌ/"), ("Vv", "/v/"), ("Ww", "/w/"), ("Xx", "/ks/"), ("Yy", "/j/"),
                             ("Zz", "/z/")]) + '</div>' +
            '<div class="note-panel"><div class="np-title">读法提示</div>26 个字母的「音素音」（不是字母名）是拼读的地基，逐个带读两遍，重点盯 5 组易混音对。</div>')
    add(ph26, 6, "26 字母总复习", "Aa–Zz 音素全表")

    pairs = [
        ("b / d", "/b/ vs /d/", [("bad", "dad"), ("big", "dig")], "b 双唇闭合；d 舌尖抵上齿龈"),
        ("p / q", "/p/ vs /kw/", [("pig", "quick"), ("pen", "queen")], "p 双唇送气；q 是 k+w 双音"),
        ("m / n", "/m/ vs /n/", [("map", "nap"), ("man", "Nan")], "m 双唇鼻音；n 齿龈鼻音"),
        ("f / v", "/f/ vs /v/", [("fan", "van"), ("fat", "vat")], "f 清音不振动；v 浊音振动声带"),
        ("e / i", "/e/ vs /ɪ/", [("ten", "tin"), ("set", "sit")], "/e/ 嘴张较大；/ɪ/ 嘴张较小"),
    ]
    pair_desc = [("Bb vs Dd", "bad/dad · big/dig"), ("Pp vs Qq", "pig/quick · pen/queen"),
                 ("Mm vs Nn", "map/nap · man/Nan"), ("Ff vs Vv", "fan/van · fat/vat"),
                 ("Ee vs Ii", "ten/tin · set/sit")]
    ph_pairs = (section_head("拼", "易混音对 · 5 组最小对立对（朗读词汇表）") +
                '<div class="body-text"><span class="highlight">20 个最小对立对词</span>：只差一个音、意思不同的词对，是辨音最好的练习。教师范读，学生跟读，体会发音部位差异。</div>' +
                '<div class="vg">' + "".join(
                    '<div class="ext-card"><div class="ext-word">%s</div><div class="ext-ph">%s</div><div class="ext-cn">%s</div><div class="ext-hook">%s</div></div>'
                    % (t, s, " · ".join(a + "/" + b for a, b in w), note)
                    for (t, s, w, note) in zip([p[0] for p in pairs], [p[1] for p in pairs], [p[2] for p in pairs], [p[3] for p in pairs])) + '</div>' +
                '<div class="note-panel"><div class="np-title">发音要领</div>' + "；".join("%s：%s" % (t, n) for t, _, _, n in pairs) + '。</div>')
    add(ph_pairs, 6, "易混音对 · 朗读词汇表", "5 对 × 4 = 20 词")

    ph_quiz1 = (section_head("拼", "看词辨音 · 选出发音不同的词") +
                quiz_html([("下列哪组含 /b/？", "big", ["pig", "quick"]),
                           ("哪组含 /kw/？", "queen", ["pen", "map"]),
                           ("哪组含 /n/？", "nap", ["map", "man"]),
                           ("哪组含 /f/（清音）？", "fan", ["van", "vat"]),
                           ("哪组含 /ɪ/？", "sit", ["set", "ten"])]) +
                '<div class="note-panel"><div class="np-title">辨音口诀</div>b/d 看双唇还是齿龈；p/q 看是单音还是双音；m/n 看鼻音出口；f/v 摸喉咙看振动；e/i 看嘴张开大小。</div>')
    add(ph_quiz1, 6, "看词归音", "5 题辨音")

    ph_quiz2 = (section_head("拼", "最小对立对听辨 · 教师读词选一") +
                '<div class="body-text"><span class="highlight">听老师读，选你听到的词</span>（口试练习，选后自行核对）。</div>' +
                quiz_html([("bad 还是 dad？", "bad", ["dad", "bed"]),
                           ("pig 还是 quick？", "quick", ["pig", "pen"]),
                           ("map 还是 nap？", "nap", ["map", "man"]),
                           ("fan 还是 van？", "van", ["fan", "fat"]),
                           ("ten 还是 tin？", "ten", ["tin", "tan"])]) +
                '<div class="note-panel"><div class="np-title">口试说明</div>此题为口试练习：教师朗读，学生指认；课后可让家长读词抽查。</div>')
    add(ph_quiz2, 6, "最小对立对听辨", "5 题口试")

    ph_quiz3 = (section_head("拼", "拼读综合闯关") +
                quiz_html([("哪个词以 /d/ 开头？", "dad", ["map", "nap"]),
                           ("哪个词以 /v/ 开头？", "van", ["fan", "fat"]),
                           ("哪个词含 /e/？", "set", ["sit", "pig"]),
                           ("哪个词含 /kw/？", "queen", ["quick", "pen"]),
                           ("哪个词以 /m/ 开头？", "map", ["nap", "Nan"]),
                           ("哪个词是含 /b/ 的三字母词？", "big", ["dig", "pig"])]) +
                '<div class="note-panel"><div class="np-title">收官标准</div>26 字母音素全认 + 5 组易混音对能辨清，拼读 Stage 1 即通关，下阶段进入字母组合。</div>')
    add(ph_quiz3, 6, "拼读综合闯关", "26 字母收官验收")

    # ---- 段7 课堂游戏 ----
    game1 = (section_head("戏", "课堂游戏 ① · 跨课词汇快选") +
             '<div class="body-text"><span class="highlight">上节课（运动）VS 本课（食物）</span>：看中文，在两组词里快速选对——检验会不会「串台」。</div>' +
             game_board("运动 or 食物？", "🎮", "听到/看到中文，快速点对应的英文词。",
                        quiz_html([("篮球（上节课）", "basketball", ["banana", "bread"]),
                                   ("牛奶（本课）", "milk", ["team", "tennis"]),
                                   ("足球（上节课）", "soccer", ["rice", "strawberry"]),
                                   ("早餐（本课）", "breakfast", ["bat", "ball"]),
                                   ("排球（上节课）", "volleyball", ["tomato", "potato"]),
                                   ("苹果（本课）", "apple", ["sport", "sound"])])) +
             '<div class="note-panel"><div class="np-title">设计意图</div>跨课词汇混排，强化新旧词边界，防止遗忘或混淆。</div>')
    add(game1, 7, "课堂游戏 ①", "跨课词汇快选")

    game2 = (section_head("戏", "课堂游戏 ② · 听音选词") +
             '<div class="body-text"><span class="highlight">教师读一个词，学生抢答选出</span>；也可以分两组对抗，比速度比准确。</div>' +
             game_board("听音抢答", "👂", "读音 → 看词 → 判断发音，巩固 5 组易混音对。",
                        quiz_html([("听到 /d/ 开头的词？", "dad", ["bad", "map"]),
                                   ("听到 /v/ 开头的词？", "van", ["fan", "fat"]),
                                   ("听到 /n/ 结尾的词？", "nap", ["map", "man"]),
                                   ("听到 /e/ 的词？", "set", ["sit", "pig"]),
                                   ("听到 /kw/ 的词？", "queen", ["pen", "queen"])])) +
             '<div class="note-panel"><div class="np-title">口令</div>起立抢答 · 答对得一分 · 答错给对方加一分。</div>')
    add(game2, 7, "课堂游戏 ②", "听音选词 · 易混音对")

    # ---- 段8 Exit Ticket + 总结 + 预告 ----
    # Exit Ticket：5 题（2 词汇主动提取 + 2 核心语法 + 1 真题迁移）
    fw = L06_WORDS
    # 2 词汇主动提取（看中文选英文，选本课已学但未作为正确答案考过的词）
    et_qs = [("「鸡肉」的英文是？", "chicken", ["breakfast", "orange"]),
             ("「土豆」的英文是？", "potato", ["tomato", "bread"]),
             ("I ___ (don't like / doesn't like) fast food.", "don't like", ["doesn't like", "am not like"]),
             ("___ (milk / milks) is good for us.", "milk", ["milks", "a milk"])]
    et_body = (section_head("检", "Exit Ticket · 退出检测") +
               '<div class="body-text"><span class="highlight">5 题形成性检测</span>：2 词汇主动提取 ＋ 2 核心语法 ＋ 1 真题迁移。<b>课堂自查，不计入正式练习卷</b>。</div>' +
               quiz_html(et_qs))
    et_body += ('<div class="quiz-q"><div class="qq-text">真题迁移 · 开放作答</div>' +
                '<div class="body-text" style="margin:6px 0">用 <b>want to do</b> 写一句「你晚饭想吃什么、喝什么」，再口头自测 G16 否定句。</div>' +
                '<details class="et-ref" onclick="event.stopPropagation()"><summary style="cursor:pointer;color:#8b1e1e;font-weight:700">点击查看参考思路</summary>' +
                '<div class="note-panel" style="margin-top:8px"><div class="np-title">参考思路（形成性自查 · 不批改）</div>I want to eat rice and chicken for dinner. ／ I want to drink milk. ／ I don&#39;t like cola.</div></details></div>')
    et_body += ('<div class="note-panel"><div class="np-title">Exit Ticket 说明</div>答错当场回看对应语法/词汇页，全部弄懂才算过关。</div>')
    add(et_body, 8, "Exit Ticket", "2 词汇 + 2 语法 + 1 迁移")

    summary = (section_head("结", "课堂总结 · 知识图谱") +
               '<div class="body-text"><span class="highlight">今天 20 词 + 3 语法 + 拼读收官</span>，一图收拢。</div>' +
               key_points([("🍎 20 词", "食物/水果/三餐/动词，按可数与不可数分类记。例句：tomatoes ✅ / milks ❌"),
                           ("🧩 G16", "非三单主语 + 动词原形；don't + 原形；Do 开头。例句：I don't like fast food."),
                           ("🧩 G17", "可数有复数，不可数不加 s。例句：an apple ✅ / a milk ❌"),
                           ("🧩 G18", "want sth. / want to do，to 后原形。例句：I want to eat an apple."),
                           ("🔤 拼读", "26 字母收官，5 组易混音对能辨清。b/d · p/q · m/n · f/v · e/i")]) +
               '<div class="note-panel"><div class="np-title">下课口令</div>「今天你吃了什么？」用一般现在时回答：I eat ... for breakfast/lunch/dinner.</div>')
    add(summary, 8, "课堂总结", "知识图谱")

    preview = (section_head("预", "下节课预告 · 阶段测试Ⅰ") +
               '<div class="body-text"><span class="highlight">L7 是阶段测试Ⅰ</span>：G01–G18 全部考点 + 140 词大诊断，本课 G16/G17/G18 是最后三块新拼图。</div>' +
               '<div class="note-panel"><div class="np-title">课前准备</div>① 复习本课 20 词（家长抽背）；② 用 want to do 各造 2 句；③ 把 L1–L6 三个错最多的考点记下来，测试前集中攻。</div>' +
               '<div class="note-panel"><div class="np-title">今晚任务</div>① 默写 20 词（家长签字）；② 完成阅读 C 五选四；③ 朗读 20 个最小对立对词。</div>')
    add(preview, 8, "下节课预告", "L7 阶段测试Ⅰ")

    # ---- 段9 思维导图（自建 2 页） ----
    def mm_panel(label, icon, color, items):
        color_cls = {"mm-red": "", "mm-blue": "blue", "mm-green": "green",
                     "mm-gold": "gold", "mm-purple": "purple", "mm-teal": "teal"}.get(color, "")
        chips = "".join('<div style="margin:2px 0">· %s</div>' % x for x in items)
        return ('<div class="ext-card %s"><div class="ext-cat">%s %s</div>'
                '<div class="ext-body">%s</div></div>' % (color_cls, icon, label, chips))
    mm = (section_head("图", "课堂思维导图 · 本课全貌") +
          '<div class="body-text"><span class="highlight">六块拼图</span>：词汇 · 语法 ×3 · 阅读 · 拼读 · 复习(L5)。收尾用这张图复述一遍。</div>' +
          '<div class="mm-cards">' +
          mm_panel("词汇 20", "🍎", "mm-red", ["可数：apple/strawberry/tomato", "不可数：milk/rice/bread", "三餐：breakfast/lunch/dinner", "动词：like/want/eat"]) +
          mm_panel("G16 一般现在时", "🧩", "mm-blue", ["非三单 + 原形", "否定 don't + 原形", "疑问 Do 开头", "I don't like fast food."]) +
          mm_panel("G17 可数不可数", "🧩", "mm-blue", ["可数有复数", "不可数不加 s", "tomatoes/strawberries", "a glass of milk"]) +
          mm_panel("G18 want to do", "🧩", "mm-blue", ["want sth. 要某物", "want to do 要做", "to 后动词原形", "I want to eat an apple."]) +
          mm_panel("阅读", "📖", "mm-green", ["A 莉莉三餐（母本改编）", "B 饮食习惯调查（原创）", "C 五选四（母本改编）", "先题后文 · 回原文定位"]) +
          mm_panel("拼读收官", "🔤", "mm-purple", ["26 字母音素全表", "5 组易混音对", "20 个最小对立对", "b/d · p/q · m/n · f/v · e/i"]) +
          mm_panel("复习 L5", "🔁", "mm-gold", ["祈使句 Do/Don't", "What 问句", "like to do", "运动 20 词"]) +
          '</div>')
    add(mm, 9, "课堂思维导图", "本课全貌 · 含 L5 复习")

    mm_full = (section_head("图", "思维导图 · 完整内容页") +
               '<div class="body-text"><span class="highlight">词汇全表 · 语法全表 · 复习全表</span> 逐项铺开，对照自测。</div>' +
               '<div class="sub-label">本课 20 词</div>' +
               '<div class="vg">' + "".join(ext_card(w) for w in fw) + '</div>' +
               '<div class="sub-label">语法速查</div>' +
               key_points([("G16", "非三单：I/you/we/they/复数 + 原形；don't + 原形；Do 开头。例句：I eat / They don't eat / Do you eat?"),
                           ("G17", "可数有复数（an apple/apples）；不可数无复数（milk/rice）。例句：I like apples. / I drink milk."),
                           ("G18", "want sth. / want to do / to 后原形。例句：I want to eat an apple.")]) +
               '<div class="sub-label">上节课（L5）复习</div>' +
               key_points([("G13", "祈使句：V原形 / Don't + V原形 / Please + V原形。例句：Open the door. / Don't run."),
                           ("G14", "What 问句：What + do + 主语 + V原形…? 例句：What sports do you like?"),
                           ("G15", "like sth. / like to do。例句：I like to play basketball.")]) +
               '<div class="note-panel"><div class="np-title">课后复盘</div>看着全表逐项自测：能否读出每个词、讲清每条语法、说出上节课三个语法点？卡住处标记为 L7 测试前重点。</div>')
    add(mm_full, 9, "思维导图 · 完整内容", "词汇全表 · 语法全表 · 复习全表")

    total = p - 1
    seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
    scode = E.STUDENT_CODES.get("邓兴华", "stu_dxh")
    js_extra = ("var studentId='" + scode + "';\n" +
                E.JS_EXTRA_TPL % (total, json.dumps(seg_pages, ensure_ascii=False),
                                  json.dumps(page_meta, ensure_ascii=False)))
    html = build_courseware(title=title, pages_dict=pages, js_extra=js_extra,
                            session="L06", nav_html=E.NAV,
                            stage_badge=stage_badge, n_pages=total, css_extra=E.CSS_EXTRA + CSS_L06)
    return html

if __name__ == "__main__":
    out = os.path.join(HERE, "test_L6_courseware.html")
    html = build_l06()
    open(out, "w", encoding="utf-8").write(html)
    print("L6 课件生成：%s (%d bytes)" % (out, len(html.encode("utf-8"))))
