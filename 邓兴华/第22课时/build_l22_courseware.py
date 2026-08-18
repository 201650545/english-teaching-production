# -*- coding: utf-8 -*-
"""邓兴华 L22 授课课件（比较级·最高级系统归纳 + 同级比较 · 八段式 · ~44 页）生成脚本"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "00_工具"))
import build_dxh_l21_25 as B

out_dir = os.path.join(HERE, "课件成品_网页PPT")
os.makedirs(out_dir, exist_ok=True)

NAV = """<div class="nav-bar">
  <div class="nav-item" data-segment="1" onclick="jumpToSegment(1)"><span class="nav-num">①</span>复习导入</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="2" onclick="jumpToSegment(2)"><span class="nav-num">②</span>新词20</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="3" onclick="jumpToSegment(3)"><span class="nav-num">③</span>比较级</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="4" onclick="jumpToSegment(4)"><span class="nav-num">④</span>最高级</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="5" onclick="jumpToSegment(5)"><span class="nav-num">⑤</span>同级比较</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="6" onclick="jumpToSegment(6)"><span class="nav-num">⑥</span>随堂演练</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="7" onclick="jumpToSegment(7)"><span class="nav-num">⑦</span>阅读</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="8" onclick="jumpToSegment(8)"><span class="nav-num">⑧</span>总结</div>
</div>"""

pages = {}
seg = {}
p = 1
def add(inner, seg_id, t="", sub=""):
    global p
    pages[p] = B._pg(p, t, sub, inner, active=(p == 1))
    seg.setdefault(seg_id, [p, p])
    seg[seg_id][1] = p
    p += 1

STAGE = "Stage 6 · L22"

# ================= ① 复习导入（3页） =================
add('<div class="cover-wrap"><div class="cover-badge">Stage 6 · 八上主线</div>'
    '<div class="cover-title">比较级 · 最高级 · 同级比较</div>'
    '<div class="cover-sub">G55 比较级系统归纳 + G56 最高级 + G57 as...as</div>'
    '<div class="cover-tagline">授课课 · 八段式</div>'
    '<div class="cover-info"><div class="cover-info-num"><div class="ci-label">新词</div><div class="ci-val">20</div></div>'
    '<div class="cover-info-num"><div class="ci-label">考点</div><div class="ci-val">3</div></div>'
    '<div class="cover-info-num"><div class="ci-label">词号</div><div class="ci-val">421–440</div></div>'
    '<div class="cover-info-num"><div class="ci-label">时长</div><div class="ci-val">90分</div></div></div>'
    '<div class="cover-emoji">📏</div></div>', 1, "L22 比较最高级", "八上重难点主线")

add(B.section_head("复", "上一课测试词回顾", "L21 衔接")
    + B.rule_cards([("zhug", "L21 测试词", "grade / score / improve / review / prepare / result / confident 等 20 个测试语境词。"),
                    ("bin", "本课衔接", "L21 已诊断 54 考点，L22 起进入比较级/最高级系统归纳。")])
    + B.quiz_html([("L21 讲评中错率最高的考点是？", "过去时", ["比较级", "祈使句"]),
                   ("本册到 L21 已累计学了多少个词？", "约 420 词", ["约 200 词", "约 100 词"])])
    + B.note_panel("L22 起点", "今天从比较级/最高级/同级比较三个考点正式开始新阶段系统学习。"), 1, "复习导入", "L21 衔接")

add(B.section_head("复", "比较级·最高级 · L5 基础回顾", "新旧衔接")
    + B.rule_cards([("xing", "L5 已学", "比较级 taller / 最高级 the tallest 已在 L5 提前引入基础。"),
                    ("warn", "本课深化", "系统归纳规则：短词 -er/-est，长词 more/most，as...as 同级。")])
    + B.quiz_html([("tall 的比较级是？", "taller", ["tallest", "more tall"]),
                   ("the tallest 是？", "最高级", ["比较级", "原级"])])
    + B.sub_label("今天把规则一次讲清"), 1, "新旧衔接", "L5 基础回顾")

add(B.section_head("复", "本课学习目标", "目标导航")
    + B.note_panel("本课 3 大考点", "① G55 比较级系统归纳（-er / more / than）② G56 最高级（the + -est / most / in-of）③ G57 as...as 同级比较。")
    + B.rule_cards([("qita", "学习动作", "看规则 → 做题自检 → 拖拽排序 → 阅读应用 → 口诀收尾。"),
                    ("ming", "防越级", "本课仅限形容词/副词比较最高级，不引入完成时比较。")])
    + B.quiz_html([("本课语法主线是？", "比较级·最高级·同级", ["条件句", "被动语态"])])
    + B.ext_card("前后衔接", "比较级在 L5 已埋基础（taller / the tallest），本课系统归纳规则并排除混淆项；L23 起转到 if 条件句。")
    + B.quiz_html([("比较级最早在哪个阶段引入？", "L5", ["L22", "L1"]),
                   ("本课之后 L23 将学习？", "if 条件句", ["完成时", "被动语态"])]), 1, "学习目标", "目标导航")

# ================= ② 新词 20（8页） =================
add(B.section_head("词", "新词① · 身高与体型", "词 421–426")
    + B.vocab_cards([
        (("tall", "/tɔːl/", "adj.", "高的", "taller than / a tall building", "Tom is taller than Jack.")),
        (("short", "/ʃɔːt/", "adj.", "矮的；短的", "shorter than / a short story", "My sister is shorter than me.")),
        (("long", "/lɒŋ/", "adj.", "长的", "longer than / a long river", "This river is longer than that one.")),
        (("big", "/bɪɡ/", "adj.", "大的", "bigger than / a big city", "Beijing is bigger than our town.")),
        (("small", "/smɔːl/", "adj.", "小的", "smaller than / a small town", "The town is smaller than the city.")),
        (("fast", "/fɑːst/", "adj./adv.", "快的；快地", "faster than / run fast", "He runs faster than me."))]), 2, "新词① 身高体型", "词 421–426")

add(B.section_head("词", "新词② · 速度与价格", "词 427–432")
    + B.vocab_cards([
        (("slow", "/sləʊ/", "adj.", "慢的", "slower than / a slow train", "The bus is slower than the car.")),
        (("cheap", "/tʃiːp/", "adj.", "便宜的", "cheaper than / cheap food", "The food here is cheaper.")),
        (("expensive", "/ɪkˈspensɪv/", "adj.", "昂贵的", "more expensive than", "This watch is more expensive.")),
        (("popular", "/ˈpɒpjələ(r)/", "adj.", "受欢迎的", "more popular than / be popular with", "She is more popular than me.")),
        (("serious", "/ˈsɪəriəs/", "adj.", "严肃的", "more serious than", "He is more serious than his brother.")),
        (("outgoing", "/ˈaʊtɡəʊɪŋ/", "adj.", "外向的", "more outgoing than / be outgoing", "She is more outgoing than me."))]), 2, "新词② 速度价格", "词 427–432")

add(B.section_head("词", "新词③ · 人物性格", "词 433–438")
    + B.vocab_cards([
        (("quiet", "/ˈkwaɪət/", "adj.", "安静的", "quieter than / be quiet", "He is quieter than his sister.")),
        (("hard-working", "/ˌhɑːdˈwɜːkɪŋ/", "adj.", "努力的", "more hard-working than", "She is more hard-working than me.")),
        (("talented", "/ˈtæləntɪd/", "adj.", "有天赋的", "more talented than / be talented in", "He is talented in music.")),
        (("creative", "/kriˈeɪtɪv/", "adj.", "有创造力的", "more creative than", "She is more creative than me.")),
        (("humorous", "/ˈhjuːmərəs/", "adj.", "幽默的", "more humorous than", "He is more humorous than his friend.")),
        (("friendly", "/ˈfrendli/", "adj.", "友好的", "friendlier than / be friendly to", "She is friendlier than me."))]), 2, "新词③ 人物性格", "词 433–438")

add(B.section_head("词", "新词④ · 才智", "词 439–440")
    + B.vocab_cards([
        (("lazy", "/ˈleɪzi/", "adj.", "懒惰的", "lazier than / be lazy", "Don't be lazy. Work hard.")),
        (("smart", "/smɑːt/", "adj.", "聪明的", "smarter than / be smart", "He is smarter than me."))])
    + B.note_panel("记忆小贴士", "比较级多是 -er；多音节词用 more，如 more popular / more expensive。")
    + B.ext_card("培优搭配", "be lazy about（对…懒惰）、be smart at（擅长…）、smarter and smarter（越来越聪明）。")
    + B.quiz_html([("smart 的比较级是？", "smarter", ["smartest", "more smart"]),
                   ("lazy 的比较级是（辅音+y）？", "lazier", ["lazyier", "more lazy"]),
                   ("more popular 是？（多音节）", "比较级", ["最高级", "原级"])]), 2, "新词④ 才智", "词 439–440")

add(B.section_head("词", "新词游戏① · 词义翻牌", "翻牌自检")
    + B.sub_label("点击翻牌，看英文想中文，再翻回核对")
    + B.flip_grid([
        ("taller", "更高的"), ("cheaper", "更便宜的"), ("quieter", "更安静的"),
        ("more popular", "更受欢迎的"), ("more outgoing", "更外向的"), ("smarter", "更聪明的"),
        ("more expensive", "更昂贵的"), ("hard-working", "努力的"), ("creative", "有创造力的")])
    + B.sub_label("自检一题")
    + B.quiz_html([("'她比他更友好' 用哪个词？", "friendlier", ["friend", "friendly"])]), 2, "词汇游戏①", "翻牌自检")

add(B.section_head("词", "新词游戏② · 拖拽归位", "拖拽")
    + B.sub_label("把词块拖到正确的解释前面")
    + B.drag_q([("更快的 → ", "faster", ""),
                ("更严肃的 → ", "more serious", ""),
                ("更懒惰的 → ", "lazier", "")],
               ["faster", "more serious", "lazier"])
    + B.sub_label("自检一题")
    + B.quiz_html([("'有天赋的' 是？", "talented", ["talented", "tall", "quiet"])]), 2, "词汇游戏②", "拖拽归位")

add(B.section_head("词", "新词游戏③ · 连线配对", "连线")
    + B.sub_label("把英文词与正确释义连起来")
    + B.match_q([("tall", "高的"), ("cheap", "便宜的"), ("outgoing", "外向的")],
                [("高的", "tall"), ("便宜的", "cheap"), ("外向的", "outgoing")])
    + B.sub_label("左右两列点击配对"), 2, "词汇游戏③", "连线配对")

add(B.section_head("词", "新词游戏④ · 选择演练", "选择")
    + B.sub_label("20 词综合选择")
    + B.quiz_html([("'昂贵的' 是？", "expensive", ["cheap", "smart"]),
                   ("'努力的' 是？", "hard-working", ["lazy", "quiet"]),
                   ("'幽默的' 是？", "humorous", ["serious", "slow"]),
                   ("'友好的' 是？", "friendly", ["tall", "long"]),
                   ("'有创造力的' 是？", "creative", ["lazy", "short"]),
                   ("'受欢迎的' 是？", "popular", ["slow", "big"])])
    + B.ext_card("词汇记忆", "性格词常用比较级表达：more outgoing（更外向）、more hard-working（更努力）、friendlier（更友好）。"), 2, "词汇游戏④", "选择演练")

# ================= ③ 比较级 G55（5页） =================
add(B.section_head("语", "比较级构成 · 规则矩阵", "G55 规则")
    + B.rule_cards([("zhug", "单音节加 -er", "tall → taller；nice → nicer（以 e 结尾加 r）；easy → easier（辅音+y 变 ier）；big → bigger（重读闭音节双写）。"),
                    ("xing", "多音节 more + 原级", "popular → more popular；expensive → more expensive。"),
                    ("warn", "比较级 + than", "A is taller than B；than 后接代词用宾格（He is taller than me.）。")])
    + B.quiz_html([("tall 的比较级是？", "taller", ["tallest", "more tall"]),
                   ("big 的比较级是？", "bigger", ["biger", "more big"]),
                   ("popular 的比较级是？", "more popular", ["popularer", "popularest"]),
                   ("nice 的比较级是？", "nicer", ["nices", "more nice"])]), 3, "比较级构成", "G55 规则")

add(B.section_head("语", "比较级 · 混淆项排除", "G55 辨析")
    + B.rule_cards([("ming", "易错", "❌ more tall → ✅ taller；❌ He is taller as Tom → ✅ taller than Tom。")])
    + B.quiz_html([("下面哪个是错的？", "more big", ["bigger", "taller"]),
                   ("比较级句中用哪个词连接？", "than", ["as", "to"]),
                   ("much 可修饰比较级：much ____", "taller", ["more tall", "tallest"])]), 3, "比较级易错", "G55 辨析")

add(B.section_head("语", "比较级 · 补全填空", "G55 练习")
    + B.fill_q("Tom is ____ (tall) than Jack.", "taller")
    + B.fill_q("This book is ____ (easy) than that one.", "easier")
    + B.sub_label("点击检查")
    + B.note_panel("填空一步到位", "看到 than 就写比较级；单音节加 -er，辅音+y 变 ier，多音节 more + 原级。写完后把句子读一遍验证通顺。"), 3, "比较级填空", "G55 练习")

add(B.section_head("语", "比较级 · 拖拽成句", "G55 应用")
    + B.sub_label("把词块拖到正确位置组成比较句")
    + B.drag_q([("She is ", "more outgoing", " than me."),
                ("This river is ", "longer", " than that one.")],
               ["more outgoing", "longer"])
    + B.sub_label("自检一题")
    + B.quiz_html([("'比…更便宜' 是？", "cheaper than", ["cheap than", "cheapest than"])]), 3, "比较级成句", "G55 应用")

add(B.section_head("语", "比较级 · 语境应用", "实际运用")
    + B.body_text("比较级帮助我们对比。例如：<b>This city is bigger but noisier.</b> 城市越大，往往越热闹。")
    + B.game_board("比较级应用自检", "📈", "点击作答自检掌握情况",
                   B.quiz_html([("一般来说，更大的城市往往？", "更热闹", ["更安静", "更便宜"]),
                                ("比较级句中用 than 表示？", "比…更", ["和…一样", "最"])]))
    + B.ext_card("拓展", "much / a little 可修饰比较级：much taller（高得多）、a little bigger（稍大一点）。")
    + B.fill_q("这本书比那本厚得多。This book is much ____ (thick) than that one.", "thicker")
    + B.quiz_html([("much taller 的意思是？", "高得多", ["高一点", "高一样"]),
                   ("a little bigger 的意思是？", "稍大一点", ["最大", "一样大"])]), 3, "比较级应用", "语境运用")

# ================= ④ 最高级 G56（5页） =================
add(B.section_head("语", "最高级构成 · 规则矩阵", "G56 规则")
    + B.rule_cards([("zhug", "单音节加 -est", "tall → the tallest；nice → the nicest；easy → the easiest；big → the biggest。"),
                    ("xing", "多音节 the most + 原级", "popular → the most popular。"),
                    ("warn", "范围用 in / of", "in + 大范围；of + 集体；三者以上才用最高级；最高级前必须加 the。")])
    + B.quiz_html([("tall 的最高级是？", "the tallest", ["the taller", "tallest"]),
                   ("popular 的最高级是？", "the most popular", ["the popularest", "the popularer"]),
                   ("big 的最高级是？", "the biggest", ["the bigest", "the most big"]),
                   ("最高级前必须加？", "the", ["a", "an"])]), 4, "最高级构成", "G56 规则")

add(B.section_head("语", "最高级 · 范围 in/of", "G56 辨析")
    + B.rule_cards([("bin", "范围表达", "He is the tallest in our class.（in + 大范围）；She is the fastest of the three.（of + 集体）。")])
    + B.quiz_html([("He is the tallest ____ our class.", "in", ["of", "than"]),
                   ("She is the best ____ the three.", "of", ["in", "than"]),
                   ("The ____ (big) city in China is Beijing.", "biggest", ["bigger", "most big"])]), 4, "最高级范围", "G56 in/of")

add(B.section_head("语", "最高级 · 补全填空", "G56 练习")
    + B.fill_q("This is the ____ (easy) question.", "easiest")
    + B.fill_q("He is the ____ (tall) boy in class.", "tallest")
    + B.sub_label("点击检查")
    + B.note_panel("填空三步", "①主语三者以上提示最高级 ②选 the + 正确词形 ③in/of 范围。多音节记得 the most + 原级。"), 4, "最高级填空", "G56 练习")

add(B.section_head("语", "最高级 · 排序成句", "G56 应用")
    + B.order_q("把词块排成正确的最高级句子", 
                [("the", "定冠词"), ("tallest", "最高级"), ("in", "介词"), ("class", "范围")],
                "the|tallest|in|class")
    + B.sub_label("自检一题")
    + B.quiz_html([("'最高级加 the' 的规则对吗？", "对", ["错", "不确定"])]), 4, "最高级排序", "G56 应用")

add(B.section_head("语", "最高级 · 关键词地图", "考点梳理")
    + B.kmap_block("最高级三大关键词", [
        ("the", "最高级前必须加 the"),
        ("-est / most", "短词 -est，长词 the most"),
        ("in / of", "in 大范围，of 集体")])
    + B.sub_label("自检一题")
    + B.quiz_html([("最高级范围 of 后面常接？", "集体", ["大地点", "时间"])])
    + B.ext_card("特例提醒", "good → best（最好）、bad → worst（最差）是不规则最高级，需单独记忆；many/much → most（最多）。")
    + B.quiz_html([("good 的最高级是？", "best", ["goodest", "goods"]),
                   ("bad 的最高级是？", "worst", ["baddest", "wards"]),
                   ("most 是哪个词的最高级？", "many/much", ["big", "tall"])]), 4, "最高级地图", "关键词")

# ================= ⑤ 同级比较 G57（4页） =================
add(B.section_head("语", "同级比较 as...as · 首次", "G57 规则")
    + B.rule_cards([("zhug", "as + 原级 + as", "和…一样：Tom is as tall as Jack.（两者一样高）"),
                    ("xing", "not as/so + 原级 + as", "不如…：He is not as tall as me.（不如我高）"),
                    ("warn", "易错", "as...as 中间用原级，不用比较级（❌ as taller as → ✅ as tall as）。")])
    + B.quiz_html([("as...as 中间用？", "原级", ["比较级", "最高级"]),
                   ("not as tall as = ？", "shorter than", ["taller than", "the tallest"])]), 5, "同级比较", "G57 as...as")

add(B.section_head("语", "同级比较 · 连线配对", "连线")
    + B.match_q([("as tall as", "一样高"), ("not as fast as", "不如…快"), ("as big as", "一样大")],
                [("一样高", "as tall as"), ("一样大", "as big as"), ("不如…快", "not as fast as")])
    + B.sub_label("左右两列点击配对"), 5, "同级连线", "G57 配对")

add(B.section_head("语", "同级比较 · 补全填空", "G57 练习")
    + B.fill_q("She is as ____ (smart) as him.", "smart")
    + B.fill_q("He is not as ____ (fast) as me.", "fast")
    + B.sub_label("点击检查，注意用原级")
    + B.note_panel("同级要点", "as...as / not as/so...as 中间永远用原级；否定式反向可换成比较级（not as tall as = shorter than）。"), 5, "同级填空", "G57 练习")

add(B.section_head("语", "同级比较 · 双列选择", "G57 辨析")
    + B.quiz_html([("as big as 表示？", "一样大", ["更大", "更小"]),
                   ("not so fast as = ？", "不如…快", ["一样快", "最快"]),
                   ("as...as 中间用原级对吗？", "对", ["错", "不确定"])])
    + B.ext_card("辨析", "not as tall as = shorter than；not as fast as = slower than。同级反向等于比较级。")
    + B.note_panel("口诀", "as...as 一样高，not so...as 矮一截；同级中间用原级，别把比较级往里塞。")
    + B.fill_q("这本书和那本一样新。This book is as ____ (new) as that one.", "new")
    + B.quiz_html([("not as new as =？", "older than", ["newer than", "the newest"])]), 5, "同级双列", "G57 辨析")

# ================= ⑥ 随堂演练（4页） =================
add(B.section_head("练", "比较最高级 · 选择演练", "单选")
    + B.quiz_html([("My bag is ____ (big) than yours.", "bigger", ["big", "biggest"]),
                   ("This is the ____ (interesting) book of all.", "most interesting", ["more interesting", "interestingest"]),
                   ("He is ____ (tall) than his brother.", "taller", ["tallest", "the taller"]),
                   ("She runs as ____ (fast) as her sister.", "fast", ["faster", "fastest"])])
    + B.note_panel("解题步骤", "①找信号词（than/the+范围/as...as）②定级别 ③选词形。多音节词记得加 more/most，不要写成 -er/-est。")
    + B.quiz_html([("interesting 的最高级是？", "most interesting", ["interestingest", "more interesting"]),
                   ("as fast as 中间用？", "fast", ["faster", "fastest"]),
                   ("the tallest 是什么级？", "最高级", ["比较级", "原级"])]), 6, "随堂演练", "选择")

add(B.section_head("练", "比较最高级 · 填空演练", "填空")
    + B.fill_q("Beijing is the ____ (big) city in China.", "biggest")
    + B.fill_q("Mary is ____ (friendly) than me.", "friendlier")
    + B.fill_q("This river is as ____ (long) as that one.", "long")
    + B.sub_label("点击检查"), 6, "随堂演练", "填空")

add(B.section_head("练", "比较最高级 · 拖拽排序", "排序")
    + B.sub_label("把比较词块拖到正确位置（排序）")
    + B.order_q("把最高级句子按正确顺序排列", 
                [("She", "主语"), ("is", "be"), ("the most", "最高级"), ("popular", "形容词"), ("in class", "范围")],
                "She|is|the most|popular|in class")
    + B.sub_label("自检一题"), 6, "随堂演练", "排序")

add(B.section_head("练", "比较最高级 · 综合混练", "综合")
    + B.quiz_html([("The Yangtze is ____ (long) river in China.", "the longest", ["longer", "long"]),
                   ("He is ____ (outgoing) than his brother.", "more outgoing", ["most outgoing", "outgoing"]),
                   ("She is as ____ (smart) as him.", "smart", ["smarter", "smartest"]),
                   ("This is ____ (cheap) of the three.", "the cheapest", ["cheaper", "cheap"])])
    + B.sub_label("点击作答，四题全对才算掌握")
    + B.note_panel("比较级·最高级·同级 三合一判定法", "先看句中有无 than（比较级）、有无 the + 范围（最高级）、有无 as...as（同级原级），再决定用词形。这是本课最核心的解题路径。")
    + B.quiz_html([("句中有 than 时应用？", "比较级", ["最高级", "原级"]),
                   ("句中有 the...in class 时应用？", "最高级", ["比较级", "原级"]),
                   ("句中有 as...as 时应用？", "原级", ["比较级", "最高级"])]), 6, "随堂演练", "综合")

# ================= ⑦ 阅读理解（5页） =================
add(B.section_head("读", "阅读 A 篇 · Comparing Two Cities", "应用文")
    + B.sub_label("应用文：两座城市比较（约 192 词）")
    + "<div class='content-table'><table><thead><tr><th>城市</th><th>面积</th><th>消费</th><th>人气</th></tr></thead><tbody>"
    + "<tr><td>City A</td><td>big</td><td>expensive</td><td>popular</td></tr>"
    + "<tr><td>City B</td><td>small</td><td>cheap</td><td>quiet</td></tr></tbody></table></div>"
    + B.body_text("City A is a big city with a large population. It is more expensive to live there, but many people think it is more popular and lively. "
                  "City B is a small town. It is cheaper and quieter, and the air is cleaner. "
                  "Some people prefer City A because there are more jobs and more fun places. "
                  "Others prefer City B because it is less crowded and more peaceful. "
                  "In fact, City A is twice as big as City B, but City B is even more popular with families. "
                  "Both cities have their own advantages. The best choice depends on what you want in life.")
    + B.quiz_html([("City A is ____ than City B.", "bigger", ["smaller", "cheaper"]),
                   ("City B is ____ than City A.", "cheaper", ["more expensive", "bigger"]),
                   ("City A 相比 City B 生活在哪方面更贵？", "消费", ["交通", "教育"]),
                   ("作者认为如何选择城市？", "取决于生活需求", ["只看大小", "只看人气"])])
    + B.note_panel("应用文信息表读法", "遇到表格型应用文，先看表头（面积/消费/人气），再逐格比对，最后回原文补充细节。表内数据是答案的主要来源。")
    + B.quiz_html([("哪个城市更受家庭欢迎？", "City B", ["City A", "一样"]),
                   ("哪个城市更安静？", "City B", ["City A", "一样"])]), 7, "阅读 A 篇", "城市比较")

add(B.section_head("读", "阅读 B 篇 · Two Friends", "记叙文")
    + B.sub_label("记叙文：两个朋友比较（约 215 词）")
    + B.body_text("Jack and Tom are my best friends. Jack is more outgoing and more humorous than Tom. He always tells funny stories and makes everyone laugh. "
                  "Tom is quieter and more hard-working than Jack. He studies harder and gets better grades. "
                  "Jack is more popular in our class because he is friendly and creative. "
                  "However, Tom is more talented in music, and he can play the guitar very well. "
                  "I think both of them are great. Jack is more fun to be with, while Tom is more dependable when I need help. "
                  "They are as smart as each other, but they have different personalities. "
                  "Having two such friends makes my life richer and more interesting.")
    + B.rule_cards([("bin", "人物", "Jack 外向幽默，Tom 安静努力；Jack 更受欢迎，Tom 更用功。")])
    + B.quiz_html([("Jack 是 ____ 的。（外向）", "more outgoing", ["quieter", "lazier"]),
                   ("Tom 是 ____ 的。（努力）", "more hard-working", ["more outgoing", "more humorous"]),
                   ("谁更受欢迎？", "Jack", ["Tom", "一样"]),
                   ("谁在音乐上更有天赋？", "Tom", ["Jack", "作者"])])
    + B.note_panel("对比信息定位", "读到比较类记叙文，先把两个主人公的形容词各列一行，再逐题回原文圈出比较词（than / as...as / the+最高级），即可快速锁定答案。")
    + B.fill_q("Jack 比 Tom 更 ____ (outgoing)。", "more outgoing")
    + B.sub_label("点击检查，注意多音节用 more"), 7, "阅读 B 篇", "朋友比较")

add(B.section_head("读", "阅读 C 篇 · Why Comparisons Help", "说明文")
    + B.sub_label("说明文：比较促进进步（约 215 词）")
    + B.body_text("Why do we compare ourselves with others? Comparisons can be very helpful. "
                  "When we compare our grades with a friend's, we can see our differences and find what to improve. "
                  "For example, if your friend is more careful than you, you can learn to check your work more slowly. "
                  "If someone is more creative, you can try new ideas and practice more. "
                  "Comparisons also help us set goals. Seeing a better example makes us want to be better. "
                  "But we should not compare to feel bad. The goal is to grow, not to feel jealous. "
                  "In short, comparisons are useful when they push us to work harder and become a better version of ourselves.")
    + B.rule_cards([("xing", "主旨", "比较帮助我们看清差距、设定目标、取得进步。")])
    + B.quiz_html([("比较的主要好处是？", "帮助进步", ["浪费时间", "让人自满"]),
                   ("文中 'set a goal' 的意思是？", "设定目标", ["放弃", "比较"]),
                   ("比较时应该避免什么心态？", "嫉妒", ["学习", "合作"]),
                   ("作者建议如何利用比较？", "找到差距并改进", ["只找优点", "盲目攀比"])])
    + B.fill_q("比较让我们看到差 (gap) 并找到要 ____ (improve) 的地方。", "improve")
    + B.note_panel("主旨判断技巧", "说明文主旨常出现在首尾句。首句 Why 引出话题，末句 In short 总结观点，两处划出来即可定位主旨。"), 7, "阅读 C 篇", "比较的意义")

add(B.section_head("读", "阅读 · 五选四", "语篇填空")
    + B.sub_label("My Best Friend 语篇填空（5 空 4 选）")
    + B.rule_cards([("bin", "提示", "根据上下文逻辑选择正确的衔接句，注意指代与转折。")])
    + B.order_q("把语篇衔接句按正确逻辑顺序排列", 
                [("First", "首先"), ("Then", "然后"), ("Finally", "最后")],
                "First|Then|Finally")
    + B.sub_label("自检一题")
    + B.quiz_html([("五选四中 'however' 表示？", "转折", ["并列", "因果"])])
    + B.ext_card("衔接词", "表示并列：and/also；表示转折：however/but；表示递进：besides/moreover；表示因果：so/therefore。五选四常考这些衔接词。")
    + B.fill_q("表转折的衔接词是 ____ (however / first)。", "however")
    + B.sub_label("点击检查，注意上下文逻辑"), 7, "阅读五选四", "语篇填空")

add(B.section_head("读", "阅读策略 · 比较信息定位", "策略")
    + B.kmap_block("比较类阅读三步法", [
        ("划比较词", "找出 than / as...as / the + 最高级"),
        ("回原文", "定位比较对象与数据"),
        ("比大小", "判断谁大谁小、谁最")])
    + B.body_text("阅读比较类文章时，先找比较词，再回原文定位，最后判断大小关系。")
    + B.quiz_html([("比较类阅读第一步是？", "划比较词", ["直接选 C", "背单词"]),
                   ("看到 than 说明是？", "比较关系", ["并列关系", "让步关系"])])
    + B.note_panel("常见设问", "Who is taller? / Which is cheaper? / What is the biggest? 设问常围绕比较对象与程度副词（much/a little/the most）设题，回原文圈数据即可。")
    + B.quiz_html([("'Which is cheaper?' 问的是？", "更便宜的那个", ["最贵", "一样"]),
                   ("much 修饰比较级表示？", "程度更强", ["程度更弱", "时态变化"])]), 7, "阅读策略", "信息定位")

# ================= 句子练习（3页） =================
add(B.section_head("句", "造句 · 比较级", "句子练习")
    + B.rule_cards([("zhug", "句型", "A + is/are + 比较级 + than + B。")])
    + B.fill_q("造句：我的书包比你的大。My bag is ____ (big) than yours.", "bigger")
    + B.sub_label("点击检查，注意比较级形式")
    + B.body_text("参考例句：<b>My brother is two years older than me.</b>（我哥比我大两岁。）比较级常与倍数、年龄、尺寸搭配，表达更精确的对比。")
    + B.quiz_html([("'比...大两岁' 用哪种表达？", "two years older than", ["two many older", "older two than"]),
                   ("比较级前可加 much 表示？", "程度加强", ["时态", "否定"])]), 7, "造句比较级", "句子练习")

add(B.section_head("句", "汉译英 · 最高级", "句子练习")
    + B.rule_cards([("zhug", "句型", "the + 最高级 + in/of + 范围。")])
    + B.fill_q("他是班里最高的男生。He is ____ (tall) boy in class.", "the tallest")
    + B.sub_label("点击检查，别忘了 the")
    + B.body_text("参考：<b>Mount Qomolangma is the highest mountain in the world.</b>（珠峰是世界最高峰。）最高级用于三者以上，必须带 the。")
    + B.quiz_html([("最高级前必须加？", "the", ["a", "an"]),
                   ("'the most beautiful' 是？", "最美丽的", ["更美丽", "美丽"])]), 7, "汉译英最高级", "句子练习")

add(B.section_head("句", "汉译英 · 同级比较", "句子练习")
    + B.rule_cards([("zhug", "句型", "as + 原级 + as（一样）；not as/so + 原级 + as（不如）。")])
    + B.fill_q("她和他一样高。She is ____ (tall) as him.", "as tall")
    + B.sub_label("点击检查，同级用原级")
    + B.note_panel("同级口诀", "一样就用 as...as，不如用 not as/so...as；中间永远原级，别写比较级。这是 L22 同级比较的收尾句。"), 7, "汉译英同级", "句子练习")

# ================= 拼读（4页） =================
add(B.section_head("拼", "音素 · -er 词尾 /ə(r)/", "音素")
    + B.rule_cards([("zhug", "-er /ə(r)/", "比较级词尾 er 发 /ə(r)/，轻读：taller, shorter, faster, smarter, quieter, friendlier。"),
                    ("xing", "对比 -est", "最高级词尾 est 发 /ɪst/：tallest, shortest, fastest, smartest。")])
    + B.quiz_html([("taller 中 er 发？", "/ə(r)/", ["/eɪ/", "/ɪ/"]),
                   ("fastest 中 est 发？", "/ɪst/", ["/ə(r)/", "/ɑː/"])])
    + B.note_panel("发音要点", "-er 是轻声舒母音 /ə(r)/，口型放松；-est 是紧元音 /ɪ/ + /st/ 连读，末尾 t 常弱化。拼读时先读词干再加词尾。")
    + B.quiz_html([("quieter 中 er 发？", "/ə(r)/", ["/ɪst/", "/eɪ/"]),
                   ("smartest 中 est 发？", "/ɪst/", ["/ə(r)/", "/ɑː/"])]), 7, "拼读 -er", "音素")

add(B.section_head("拼", "看词归音 · -er 还是 -est", "归音")
    + B.order_q("把含 /ə(r)/ 的比较级词挑出来（排序成一列）", 
                [("taller", "比较级"), ("shorter", "比较级"), ("fastest", "最高级")],
                "taller|shorter|fastest")
    + B.sub_label("自检一题")
    + B.quiz_html([("quieter 是？", "比较级", ["最高级", "原级"])]), 7, "拼读归音", "-er/-est")

add(B.section_head("拼", "听音选词 · 含 /ə(r)/", "听音")
    + B.quiz_html([("选出含 /ə(r)/ 的词", "taller", ["tallest", "more"]),
                   ("选出含 /ɪst/ 的词", "fastest", ["faster", "fast"]),
                   ("friendlier 词尾发？", "/ə(r)/", ["/ɪst/", "/eɪ/"])])
    + B.sub_label("点击作答，听音辨形")
    + B.note_panel("听辨提示", "-er 结尾多为比较级、轻读 /ə(r)/；-est 结尾多为最高级、读 /ɪst/。听音时抓词尾长短与轻重即可区分。")
    + B.quiz_html([("quieter 结尾 /ə(r)/ 表示它是？", "比较级", ["最高级", "原级"]),
                   ("tallest 结尾 /ɪst/ 表示它是？", "最高级", ["比较级", "原级"])]), 7, "拼读听音", "听音选词")

add(B.section_head("拼", "最小对立对 · 比较 vs 最高", "对立")
    + B.rule_cards([("ming", "最小对立", "taller / tallest；faster / fastest；quieter / quietest——注意 -er 与 -est 的区分。")])
    + B.match_q([("taller", "更高的"), ("tallest", "最高的"), ("faster", "更快的")],
                [("更高的", "taller"), ("最高的", "tallest"), ("更快的", "faster")])
    + B.sub_label("左右两列点击配对"), 7, "拼读对立", "最小对立对")

# ================= ⑧ 课堂总结（3页） =================
add(B.section_head("结", "核心口诀总览", "一页速览")
    + B.rule_cards([("zhug", "比较级", "短词加 -er，长词 more 前；比谁就用 than，加强再加 much。"),
                    ("xing", "最高级", "the 一定在前面；短词 -est，长词 most 前；范围 in/of，三者以上才最高。"),
                    ("bin", "同级比较", "as...as 一样；not as/so...as 不如。")])
    + B.quiz_html([("'比较级 + than' 表？", "比…更", ["和…一样", "最"])]), 8, "核心口诀", "一页速览")

add(B.section_head("结", "课堂思维导图", "全课收尾")
    + B.mind_map(22, "比较级 · 最高级 · 同级比较", [
        ("比较级", "短词 -er / 长词 more / than 连接"),
        ("最高级", "the + -est / most / in-of 范围"),
        ("同级比较", "as...as 一样 / not as/so...as 不如"),
        ("易错", "最高级加 the / 同级用原级 / more tall 错误"),
        ("应用", "阅读找比较词 / 造句 / 拼读 -er/-est"),
        ("防越级", "不引入完成时比较")])
    + B.sub_label("本课 3 考点：G55 比较级 · G56 最高级 · G57 同级比较")
    + B.note_panel("一句话收口", "比较级比两者（+than）、最高级三者以上（the+…+in/of）、同级用 as/not as...as。三句口诀带走，本课完成。")
    + B.quiz_html([("比较级用于比较？", "两者", ["三者以上", "单个"]),
                   ("最高级用于比较？", "三者以上", ["两者", "单个"])]), 8, "思维导图", "全课收尾")

add(B.section_head("结", "课后任务 · 巩固清单", "任务")
    + B.rule_cards([("qita", "任务一", "抄写 20 个比较级词形，各配一句例句。"),
                    ("bin", "任务二", "完成配套练习卷（阅读30/语言25/综合25/语法诊断20）。"),
                    ("xing", "任务三", "用比较级/最高级各写 3 句，描述你的家人或朋友。")])
    + B.quiz_html([("本课核心考点有几个？", "3 个", ["2 个", "5 个"]),
                   ("比较级句式 A ____ 比较级 than B. 空中填？", "is", ["am", "are"])])
    + B.ext_card("展望", "L23 将转入 if 真实条件句（主将从现），预习 if / unless / condition 等词。"), 8, "课后任务", "巩固清单")

total = p - 1
seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
page_meta = {i: {"p": "CORE", "m": 2} for i in range(1, total + 1)}

js = B.js_extra(total, seg_pages, page_meta)
css = B.CSS_EXTRA
out = os.path.join(out_dir, "第22课时_课件_中等.html")
size = B.write_courseware(22, "第22课时 · 比较级·最高级·同级比较", pages, NAV, STAGE, css, js, out, session="D22")
print("L22 课件生成：%s (%d bytes, %d pages)" % (out, size, total))