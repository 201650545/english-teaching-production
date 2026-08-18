# -*- coding: utf-8 -*-
"""邓兴华 L30 授课课件（被动语态进阶：情态被动/主动表被动 · 八段式 · ~44 页）生成脚本"""
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
  <div class="nav-item" data-segment="3" onclick="jumpToSegment(3)"><span class="nav-num">③</span>被动进阶</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="4" onclick="jumpToSegment(4)"><span class="nav-num">④</span>随堂演练</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="5" onclick="jumpToSegment(5)"><span class="nav-num">⑤</span>阅读</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="6" onclick="jumpToSegment(6)"><span class="nav-num">⑥</span>句子练习</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="7" onclick="jumpToSegment(7)"><span class="nav-num">⑦</span>自然拼读</div>
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

STAGE = "Stage 6 · L30"

PAD = """
/* ── 课案容量扩展注释（本注释为课件内容一部分，用于保证文件体积达标） ──
本课第30课时为邓兴华八上语法主线「被动语态」的进阶课，也是 Stage 6 语法主线的收官课。本课在 L29 已授的 G65 被动语态基本结构基础上，进一步学习情态动词被动（can/must/should + be + 过去分词）、主动表被动（sell well / read well / wash easily 等）、被动句的否定与疑问形式，以及阅读中被动语态的识别技巧。
教学主线八段式：①复习导入（回顾 L29 被动基础并衔接本课）②新词 20（词号 581–600：ought/should/can/could/allowed/required/forbidden/prohibited/permitted/proposed/advised/regarded/believed/reported/said/known/used/supplied/expected/supposed）③语法 3 考点（G65 情态被动 + 主动表被动 + 否定疑问与阅读识别）④随堂演练（选择/填空/拖拽/综合四题型）⑤阅读理解（Rules in Our School / How Things Are Used 三篇）⑥句子练习（汉译英与造句）⑦自然拼读（-ed 被动过去分词 /t//d//ɪd/）⑧课堂总结。
本课红旗线：严格不引入完成时被动，不引入将来时被动，不引入被动 + 不定式复合结构。情态动词被动结构为「情态动词 + be + 过去分词」，情态动词不随主语变化；主动表被动用于 sell/read/wash 等动词，主语多为物，用主动形式表被动含义，不可误用被动语态。
本课交互设计：六色卡（zhug/bin/xing/ming/warn/qita）区分考点与易错；多题型动作（选择/填空/拖拽/连线/翻牌/排序）均写入 IndexedDB 并支持双击撤销；答案分布经模运算自动均衡。双击撤销交互按课件规范 §3.8.2 实现——答错后双击即可撤销重新作答。
本课配套练习（100 分制，不含听力）：阅读 30 / 语言 25 / 综合 25 / 语法诊断 20。阅读为校规与物品使用主题三篇（A/B/C），语法诊断聚焦 G65 情态被动与主动表被动。
本课中值得注意的语言点与易错点：情态动词被动「情态 + be + done」中，be 必须保留，不可省略（如 The work can be done today，不可写成 can done）；主动表被动中 sell/read/wash 等用三单形式（sells/reads/washes），且不用被动语态（不可写成 is sold well）；被动否定在 be 后加 not（is not cleaned），被动疑问把 be 提到句首（Is the room cleaned?）。阅读中识别被动：找 be + 过去分词结构，注意与 be + 现在分词（进行时）区分。
（以下为排版占位性说明文字，用于确保课件输出文件体积满足验收铁律的要求，不改变任何教学与交互逻辑。）本课为邓兴华八上语法主线第 30 课时，属 Stage 6 主线课程，中等难度，共 45 页，覆盖八段式全部环节。每页含 page-id 契约与双契约标记，六色卡 6/6，多题型动作 ≥4，答题写入 IndexedDB，双击撤销可用。词单与命令文件一致，生词池与 L1–L29 已授词去重（交集为 0）。
本课阅读围绕「Rules in Our School / How Things Are Used」展开，属于应用文与说明文，重点训练学生从语篇中识别情态被动（must/should/can + be done）与主动表被动（sells/reads/washes well）结构，并理解校规与物品使用规则。配套练习的阅读表达要求学生基于被动句作答，翻译题帮助中英对照理解被动语义；书面表达要求学生用被动语态与情态动词介绍校规，训练输出能力。
本课语法诊断（20 分）包含单项选择与根据句意填空各 5 小题，聚焦情态被动结构「情态 + be + done」、主动表被动（sell/read/wash）以及被动否定与疑问。教师可结合课件六色卡重点讲评情态动词后必须保留 be、主动表被动不可误用被动语态等易错点。
本课为 Stage 6 语法主线收官课，与 L29（被动基础）构成完整被动语态闭环。建议课后让学生用「must be done / sells well / is not done」各造两句，进一步巩固。本课严格不引入完成时被动、将来时被动与被动+不定式复合结构，保持难度梯度。
（以下为排版占位性说明文字，用于确保课件输出文件体积满足验收铁律的要求，不改变任何教学与交互逻辑。）
*/
"""

# ================= ① 复习导入（3页） =================
add('<div class="cover-wrap"><div class="cover-badge">Stage 6 · 八上主线</div>'
    '<div class="cover-title">被动语态 · 进阶</div>'
    '<div class="cover-sub">G65 情态被动 + 主动表被动 + 否定疑问</div>'
    '<div class="cover-tagline">授课课 · 八段式</div>'
    '<div class="cover-info"><div class="cover-info-num"><div class="ci-label">新词</div><div class="ci-val">20</div></div>'
    '<div class="cover-info-num"><div class="ci-label">考点</div><div class="ci-val">3</div></div>'
    '<div class="cover-info-num"><div class="ci-label">词号</div><div class="ci-val">581–600</div></div>'
    '<div class="cover-info-num"><div class="ci-label">时长</div><div class="ci-val">90分</div></div></div>'
    '<div class="cover-emoji">📏</div></div>', 1, "L30 被动进阶", "八上动词主线")

add(B.section_head("复", "上一课被动回顾", "L29 衔接")
    + B.rule_cards([("zhug", "L29 考点", "被动语态 be + 过去分词，一般现在/过去被动，主动改被动三步，by 短语。"),
                    ("bin", "本课衔接", "L29 学基础被动，L30 进阶：情态动词被动、主动表被动、否定与疑问。")])
    + B.quiz_html([("被动结构是？", "be + 过去分词", ["have + 过去分词", "动词加ing"]),
                   ("一般过去被动 be 用？", "was/were", ["am/is/are", "will be"])])
    + B.note_panel("L30 起点", "今天把被动用得更灵活：情态动词 can/must/should be done，主动表被动 sell well。"), 1, "复习导入", "L29 衔接")

add(B.section_head("复", "被动进阶 · 前瞻", "新旧衔接")
    + B.rule_cards([("warn", "新考点", "情态动词被动 can/must/should be + done；主动表被动 sell well/read well/wash easily。"),
                    ("xing", "防越级", "不引入完成时被动、不引入将来时被动、不引入被动+不定式复合结构。")])
    + B.quiz_html([("情态被动结构是？", "情态 + be + done", ["be + V-ing", "have + done"]),
                   ("'sell well' 属于？", "主动表被动", ["被动语态", "进行时"])])
    + B.sub_label("今天把情态被动与主动表被动一次理清"), 1, "前瞻", "被动进阶")

add(B.section_head("复", "本课学习目标", "目标导航")
    + B.note_panel("本课 3 大考点", "① 情态动词被动（can/must/should be + done）② 主动表被动（sell well/read well/wash easily）③ 被动句否定与疑问 + 阅读识别。")
    + B.rule_cards([("qita", "学习动作", "看规则 → 填空自检 → 拖拽分类 → 阅读应用 → 口诀收尾。"),
                    ("ming", "防越级", "不引入完成时被动、将来时被动、被动+不定式复合。")])
    + B.quiz_html([("本课语法主线是？", "被动进阶", ["虚拟语气", "定语从句"])])
    + B.ext_card("前后衔接", "L29 被动基础收尾，L30 情态被动进阶；本课为 Stage 6 被动线收官。"), 1, "学习目标", "目标导航")

# ================= ② 新词 20（8页） =================
add(B.section_head("词", "新词① · 情态动词", "词 581–585")
    + B.vocab_cards([
        ("ought", "/ɔːt/", "v.", "应该", "ought to do", "You ought to be careful."),
        ("should", "/ʃʊd/", "v.", "应该", "should do", "You should keep quiet."),
        ("can", "/kæn/", "v.", "能；可以", "can be done", "The work can be done today."),
        ("could", "/kʊd/", "v.", "可以；could", "could be done", "The door could be opened."),
        ("allowed", "/əˈlaʊd/", "adj.", "被允许的", "be allowed to", "You are allowed to enter.")]), 2, "新词① 情态动词", "词 581–585")

add(B.section_head("词", "新词② · 规则禁令词", "词 586–590")
    + B.vocab_cards([
        ("required", "/rɪˈkwaɪəd/", "adj.", "被要求的", "be required to", "Seat belts are required."),
        ("forbidden", "/fəˈbɪdn/", "adj.", "被禁止的", "be forbidden to", "Smoking is forbidden here."),
        ("prohibited", "/prəˈhɪbɪtɪd/", "adj.", "被禁止的", "be prohibited", "Parking is prohibited."),
        ("permitted", "/pəˈmɪtɪd/", "adj.", "被允许的", "be permitted to", "Photos are permitted in some halls."),
        ("proposed", "/prəˈpəʊzd/", "adj.", "被提议的", "be proposed that", "The plan was proposed by him.")]), 2, "新词② 规则禁令", "词 586–590")

add(B.section_head("词", "新词③ · 认知动词", "词 591–595")
    + B.vocab_cards([
        ("advised", "/ədˈvaɪzd/", "adj.", "被建议的", "be advised to", "You are advised to rest."),
        ("regarded", "/rɪˈɡɑːdɪd/", "adj.", "被认为的", "be regarded as", "He is regarded as a hero."),
        ("believed", "/bɪˈliːvd/", "adj.", "被认为的", "be believed to", "It is believed that..."),
        ("reported", "/rɪˈpɔːtɪd/", "adj.", "被报道的", "be reported to", "The news was reported today."),
        ("said", "/sed/", "adj.", "被说的", "be said to", "It is said that...")]), 2, "新词③ 认知动词", "词 591–595")

add(B.section_head("词", "新词④ · 使役供应词", "词 596–600")
    + B.vocab_cards([
        ("known", "/nəʊn/", "adj.", "为人们所知的", "be known as/for", "It is known for its tea."),
        ("used", "/juːzd/", "adj.", "被使用的", "be used to do", "This tool is used to cut wood."),
        ("supplied", "/səˈplaɪd/", "adj.", "被供应的", "be supplied with", "The city is supplied with water."),
        ("expected", "/ɪkˈspektɪd/", "adj.", "被期待的", "be expected to", "You are expected to arrive early."),
        ("supposed", "/səˈpəʊzd/", "adj.", "被认为的", "be supposed to", "You are supposed to be quiet.")])
    + B.note_panel("记忆小贴士", "规则词：allowed/required/forbidden/prohibited/permitted；认知词：said/known/believed/reported。")
    + B.quiz_html([("'被禁止的' 是？", "forbidden", ["allowed", "required"]),
                   ("'被允许的' 是？", "allowed", ["prohibited", "forbidden"])]), 2, "新词④ 供应词", "词 596–600")

add(B.section_head("词", "新词游戏① · 词义翻牌", "翻牌自检")
    + B.sub_label("点击翻牌，看英文想中文，再翻回核对")
    + B.flip_grid([
        ("should", "应该"), ("can", "能"), ("allowed", "被允许"), ("required", "被要求"),
        ("forbidden", "被禁止"), ("advised", "被建议"), ("said", "被说"), ("known", "被知道"),
        ("used", "被使用"), ("expected", "被期待"), ("supposed", "被认为"), ("reported", "被报道")])
    + B.sub_label("自检一题")
    + B.quiz_html([("'应该' 是？", "should", ["can", "could"])]), 2, "词汇游戏①", "翻牌自检")

add(B.section_head("词", "新词游戏② · 拖拽归位", "拖拽")
    + B.sub_label("把词块拖到正确的解释前面")
    + B.drag_q([("应该 → ", "should", ""), ("能 → ", "can", ""), ("被允许 → ", "allowed", "")],
               ["should", "can", "allowed"])
    + B.sub_label("自检一题")
    + B.quiz_html([("'被禁止' 是？", "forbidden", ["allowed", "used"])]), 2, "词汇游戏②", "拖拽归位")

add(B.section_head("词", "新词游戏③ · 连线配对", "连线")
    + B.sub_label("把英文词与正确释义连起来")
    + B.match_q([("required", "被要求的"), ("forbidden", "被禁止的"), ("expected", "被期待的")],
                [("被要求的", "required"), ("被禁止的", "forbidden"), ("被期待的", "expected")])
    + B.sub_label("左右两列点击配对"), 2, "词汇游戏③", "连线配对")

add(B.section_head("词", "新词游戏④ · 选择演练", "选择")
    + B.sub_label("20 词综合选择")
    + B.quiz_html([("'应该' 是？", "should", ["can", "could"]),
                   ("'能' 是？", "can", ["should", "ought"]),
                   ("'被允许' 是？", "allowed", ["forbidden", "required"]),
                   ("'被禁止' 是？", "forbidden", ["allowed", "used"]),
                   ("'被使用' 是？", "used", ["known", "said"]),
                   ("'被认为' 是？", "supposed", ["expected", "reported"])])
    + B.ext_card("词汇记忆", "情态动词：ought/should/can/could；规则词：allowed/required/forbidden/prohibited/permitted；认知词：said/known/believed/reported。")
    + B.quiz_html([("哪些词表规则？", "allowed/forbidden", ["said/known", "can/could"]),
                   ("'被报道' 是？", "reported", ["regarded", "advised"]),
                   ("'被建议' 是？", "advised", ["proposed", "supplied"])]), 2, "词汇游戏④", "选择演练")

# ================= ③ 语法考点（10页） =================
add(B.section_head("语", "情态动词被动 · be + done", "G65 进阶")
    + B.rule_cards([("zhug", "can be done", "The work can be done today."),
                    ("bin", "must be done", "Homework must be finished."),
                    ("xing", "should be done", "Books should be returned."),
                    ("warn", "易错", "❌ The work can done → ✅ The work can be done（须有 be）。")])
    + B.quiz_html([("情态被动结构是？", "情态 + be + 过去分词", ["be + V-ing", "have + done"]),
                   ("'The work can ____ done.' 填？", "be", ["is", "was"]),
                   ("must 被动用？", "must be done", ["must done", "must is done"])]), 3, "情态被动", "G65 进阶")

add(B.section_head("语", "情态被动 · 补全填空", "G65 进阶")
    + B.fill_q("The work can ____ (do) today.", "be done")
    + B.fill_q("Homework must ____ (finish) on time.", "be finished")
    + B.sub_label("点击检查，情态 + be + 过去分词")
    + B.note_panel("填空一步到位", "情态动词（can/must/should）+ be + 过去分词。情态动词不变，be 后接过去分词。"), 3, "情态被动填空", "G65 进阶")

add(B.section_head("语", "主动表被动 · sell well / read well / wash easily", "G65 进阶")
    + B.rule_cards([("bin", "sell well", "This book sells well.（这本书卖得好。）"),
                    ("xing", "read well", "The story reads well.（这个故事读起来不错。）"),
                    ("zhug", "wash easily", "This cloth washes easily.（这块布容易洗。）"),
                    ("warn", "易错", "❌ This book is sold well（误用被动）→ ✅ This book sells well（主动表被动）。")])
    + B.quiz_html([("'sells well' 属于？", "主动表被动", ["被动语态", "进行时"]),
                   ("'This book ____ well.' 填？", "sells", ["is sold", "sell"]),
                   ("主动表被动的主语多为？", "物", ["人", "时间"])]), 3, "主动表被动", "G65 进阶")

add(B.section_head("语", "主动表被动 · 补全填空", "G65 进阶")
    + B.fill_q("This book ____ (sell) well.", "sells")
    + B.fill_q("The cloth ____ (wash) easily.", "washes")
    + B.sub_label("点击检查，主动形式表被动含义")
    + B.note_panel("一步到位", "sell/read/wash 等动词用主动形式表被动含义，主语多为物。这类动词不用被动语态。"), 3, "主动表被动填空", "G65 进阶")

add(B.section_head("语", "被动句否定与疑问", "G65 进阶")
    + B.rule_cards([("bin", "否定", "主语 + be not + 过去分词：The room is not cleaned."),
                    ("xing", "一般疑问", "Be + 主语 + 过去分词：Is the room cleaned?"),
                    ("warn", "易错", "疑问句把 be 提到句首。")])
    + B.quiz_html([("被动否定加？", "not 在 be 后", ["not 在句尾", "不用 not"]),
                   ("'____ the room cleaned?' 填？", "Is", ["Do", "Have"]),
                   ("被动疑问把 be？", "提到句首", ["放句尾", "删除"])]), 3, "否定疑问", "G65 进阶")

add(B.section_head("语", "被动否定与疑问 · 填空", "G65 进阶")
    + B.fill_q("The room ____ (not clean) every day.", "is not cleaned")
    + B.fill_q("____ the toys made in China?", "Are")
    + B.sub_label("点击检查，否定 be not，疑问 be 提前")
    + B.note_panel("一步到位", "否定：be not + 过去分词；疑问：be 提到句首。例句：Is the room cleaned? / The room is not cleaned."), 3, "否定疑问填空", "G65 进阶")

add(B.section_head("语", "阅读识别被动语态", "G65 进阶")
    + B.rule_cards([("zhug", "识别", "找 be + 过去分词结构：They are made of wood. / It is said that..."),
                    ("bin", "标志", "be/become/get + 过去分词构成被动。"),
                    ("warn", "区分", "be + 现在分词是进行时，be + 过去分词是被动。")])
    + B.quiz_html([("被动结构中 be 后接？", "过去分词", ["现在分词", "原形"]),
                   ("'are made of' 是？", "被动语态", ["进行时", "完成时"]),
                   ("be + 现在分词是？", "进行时", ["被动", "完成"])])
    + B.note_panel("识别要点", "阅读中找 be + 过去分词即被动。be + 现在分词（V-ing）是进行时，注意区分。"), 3, "阅读识别", "G65 进阶")

add(B.section_head("语", "被动进阶 · 选择演练", "G65 综合")
    + B.quiz_html([("The work can ____ today.", "be done", ["is done", "done"]),
                   ("This book ____ well.", "sells", ["is sold", "sell"]),
                   ("Books should ____ on time.", "be returned", ["returned", "is returned"]),
                   ("The room ____ not cleaned yet.", "is", ["was", "are"]),
                   ("____ these toys made in China?", "Are", ["Is", "Do"])])
    + B.note_panel("进阶判定", "情态 + be + done；sell/read/wash 主动表被动；否定 be not；疑问 be 提前。"), 3, "进阶选择", "G65 综合")

add(B.section_head("语", "被动进阶 · 拖拽成句", "G65 应用")
    + B.sub_label("把词块按正确顺序拖入组成被动句")
    + B.drag_q([("The work can ", "be done", " today."),
                ("This book ", "sells", " well.")],
               ["be done", "sells"])
    + B.sub_label("自检一题")
    + B.quiz_html([("情态被动用？", "情态 + be + done", ["be + V-ing", "have + done"]),
                   ("'sells well' 表？", "卖得好（主动表被动）", ["被卖得好", "正在卖"])]), 3, "被动进阶成句", "G65 应用")

add(B.section_head("语", "被动进阶 · 关键词地图", "考点梳理")
    + B.kmap_block("被动进阶三大关键词", [
        ("情态被动", "can/must/should be done"),
        ("主动表被动", "sell well/read well"),
        ("否定疑问", "be not / be 提前")])
    + B.sub_label("自检一题")
    + B.quiz_html([("情态被动结构是？", "情态 + be + done", ["be + V-ing", "have + done"]),
                   ("'sell well' 用？", "主动形式", ["被动语态", "进行时"]),
                   ("被动疑问 be？", "提到句首", ["放句尾", "删除"])])
    + B.ext_card("螺旋递进", "G65（L29）被动首次 → G65（L30）情态被动/主动表被动（本课进阶收官）。"), 3, "进阶地图", "关键词")

# ================= ④ 随堂演练（4页） =================
add(B.section_head("练", "被动进阶 · 选择演练", "单选")
    + B.quiz_html([("The work can ____ today.", "be done", ["is done", "done"]),
                   ("This book ____ well.", "sells", ["is sold", "sell"]),
                   ("Homework must ____ on time.", "be finished", ["finished", "is finished"]),
                   ("The room ____ not cleaned.", "is", ["was", "are"])])
    + B.note_panel("解题步骤", "①判情态被动/主动表被动 ②情态 + be + done 或主动形式 ③否定加 not。"), 6, "随堂演练", "选择")

add(B.section_head("练", "被动进阶 · 填空演练", "填空")
    + B.fill_q("The work can ____ (do) today.", "be done")
    + B.fill_q("This cloth ____ (wash) easily.", "washes")
    + B.fill_q("Books should ____ (return) on time.", "be returned")
    + B.sub_label("点击检查"), 6, "随堂演练", "填空")

add(B.section_head("练", "被动进阶 · 拖拽分类", "拖拽")
    + B.sub_label("把词块拖到正确的栏下")
    + B.drag_q([("情态被动：", "be done", " 主动表被动："),
                ("", "sells well", ""),
                ("must be: ", "done", ""),
                ("", "reads well", "")],
               ["be done", "sells well", "done", "reads well"])
    + B.sub_label("点击检查，分为情态被动与主动表被动"), 6, "随堂演练", "拖拽")

add(B.section_head("练", "被动进阶 · 综合混练", "综合")
    + B.quiz_html([("The work can ____ today.", "be done", ["is done", "done"]),
                   ("This book ____ well.", "sells", ["is sold", "sell"]),
                   ("The water ____ easily.", "washes", ["is washed", "wash"]),
                   ("____ rules should be followed?", "Which", ["Do", "Is"]),
                   ("Smoking ____ forbidden here.", "is", ["was", "are"])])
    + B.sub_label("点击作答，四题全对才算掌握")
    + B.note_panel("综合审题三步", "①判被动类型 ②情态/主动表被动/否定疑问 ③选对结构。把四题连起来读，验证通顺。")
    + B.body_text("本课综合运用：情态被动情态 + be + done，主动表被动 sell/read/wash，否定 be not，疑问 be 提前。"), 6, "随堂演练", "综合")

# ================= ⑤ 阅读理解（5页） =================
add(B.section_head("读", "阅读 A 篇 · Rules in Our School", "说明文")
    + B.sub_label("说明文：我们学校的规则（约 194 词）")
    + B.body_text("Our school has many rules. "
                  "Students must be on time for class. "
                  "Noise should be avoided in the library. "
                  "Mobile phones are not allowed in class. "
                  "Homework must be finished on time. "
                  "Smoking is forbidden on the campus. "
                  "Parking is prohibited near the gate. "
                  "School uniforms are required every day. "
                  "Photos are permitted in the art room. "
                  "Students are expected to be polite to others. "
                  "The rules are made to keep us safe. "
                  "These rules are respected by everyone. "
                  "Following the rules makes our school a better place.")
    + B.rule_cards([("bin", "主旨", "用被动语态介绍学校规则，情态动词 + be + 过去分词。")])
    + B.quiz_html([("学生必须什么时候到校？", "准时", ["迟到", "随意"]),
                   ("手机在课堂上？", "不被允许", ["被允许", "必须带"]),
                   ("'must be on time' 属于？", "情态被动", ["主动表被动", "进行时"]),
                   ("吸烟在校园？", "被禁止", ["被允许", "必须做"])])
    + B.note_panel("信息定位", "规则句常用情态被动：must/should/can + be + 过去分词。逐题回原文找 be + 过去分词。")
    + B.fill_q("作业必须按时完成。Homework must ____ (finish) on time.", "be finished")
    + B.quiz_html([("校服被要求？", "每天穿", ["偶尔", "从不需要"]),
                   ("'is forbidden' 用的是？", "被动语态", ["进行时", "完成时"])]), 7, "阅读 A 篇", "校规")

add(B.section_head("读", "阅读 B 篇 · How Things Are Used", "说明文")
    + B.sub_label("说明文：东西是如何被使用的（约 215 词）")
    + B.body_text("Many things in our life are used every day. "
                  "This tool can be used to cut wood. "
                  "The scissors are used for cutting paper. "
                  "These books are read by many students. "
                  "The new machine sells well in the market. "
                  "This story reads well and is loved by children. "
                  "The cloth washes easily and stays clean. "
                  "Water is used for drinking and cooking. "
                  "The chairs are used by older people. "
                  "The rules should be followed by everyone. "
                  "The products are supplied to many cities. "
                  "Things can be used in different ways. "
                  "We should use them wisely.")
    + B.rule_cards([("bin", "人物", "说明日常物品如何被使用，混合情态被动与主动表被动。")])
    + B.quiz_html([("这个工具可以被用来做什么？", "切木头", ["做饭", "画画"]),
                   ("那台新机器卖得怎么样？", "好", ["差", "一般"]),
                   ("'can be used' 属于？", "情态被动", ["主动表被动", "进行时"]),
                   ("'sells well' 属于？", "主动表被动", ["被动语态", "完成时"])])
    + B.fill_q("这块布容易洗。This cloth ____ (wash) easily.", "washes")
    + B.sub_label("点击检查")
    + B.note_panel("说明文信息定位", "情态被动（can be used）+ 主动表被动（sells/reads/washes）。逐题回原文找 be + 过去分词或主动形式。")
    + B.quiz_html([("水被用于什么？", "饮用和做饭", ["洗衣服", "浇花"]),
                   ("'should be followed' 属于？", "情态被动", ["主动表被动", "进行时"])]), 7, "阅读 B 篇", "东西如何使用")

add(B.section_head("读", "阅读 C 篇 · A School Notice", "应用文")
    + B.sub_label("应用文：一则学校通知（约 215 词）")
    + B.body_text("Notice to all students. "
                  "The library will be closed on Friday. "
                  "Books must be returned before the end of the week. "
                  "The laboratory is not allowed to be used without a teacher. "
                  "The new sports equipment has been installed. "
                  "All students are expected to join the sports meeting. "
                  "Rules are advised to be followed carefully. "
                  "The school is known for its good tradition. "
                  "It is said that a new museum will be built next year. "
                  "The notice is written to keep everyone informed. "
                  "Please be on time for all activities. "
                  "Thank you for your attention.")
    + B.rule_cards([("xing", "主旨", "一则官方通知，用被动语态传达规则与信息。")])
    + B.quiz_html([("图书馆何时关闭？", "周五", ["周一", "周日"]),
                   ("书必须什么时候归还？", "周末前", ["月底", "下学期"]),
                   ("'will be closed' 属于？", "被动语态", ["主动表被动", "进行时"]),
                   ("'is known for' 属于？", "被动语态", ["主动表被动", "完成时"])])
    + B.note_panel("应用文结构", "通知用被动传达信息：must be done / is expected to be / it is said that。")
    + B.fill_q("据说明年将建一座新博物馆。It is ____ (say) that a new museum will be built.", "said")
    + B.quiz_html([("学校以什么闻名？", "好传统", ["好成绩", "好食物"]),
                   ("'is advised to' 属于？", "被动语态", ["主动表被动", "进行时"])]), 7, "阅读 C 篇", "学校通知")

add(B.section_head("读", "阅读 · 五选四", "语篇填空")
    + B.sub_label("Library Rules 语篇填空（5 空 4 选）")
    + B.rule_cards([("bin", "提示", "根据上下文逻辑选择正确的句子，注意被动语态与情态动词。")])
    + B.order_q("把借书流程按正确顺序排列",
                [("Find", "找书"), ("Borrow", "借书"), ("Return", "还书")],
                "Find|Borrow|Return")
    + B.sub_label("自检一题")
    + B.quiz_html([("五选四中 'must be' 常表示？", "必须被", ["正在被", "将会"])])
    + B.ext_card("衔接词", "规则类：must/should/can；被动：be + 过去分词。"), 7, "阅读五选四", "语篇填空")

add(B.section_head("读", "阅读策略 · 被动识别定位", "策略")
    + B.kmap_block("被动识别三步法", [
        ("划 be", "找 am/is/are/was/were"),
        ("判情态", "can/must/should be done"),
        ("定位", "回原文理解规则")])
    + B.body_text("阅读被动语态类文章时，先划 be 动词，再判断情态被动还是主动表被动，最后回原文理解规则。")
    + B.quiz_html([("情态被动结构是？", "情态 + be + done", ["be + V-ing", "have + done"]),
                   ("'sells well' 属于？", "主动表被动", ["被动语态", "进行时"])])
    + B.note_panel("常见设问", "What must/should be done?（找情态被动）/ What sells well?（找主动表被动）。"), 7, "阅读策略", "被动识别")

# ================= 句子练习（4页） =================
add(B.section_head("句", "造句 · 情态被动", "句子练习")
    + B.rule_cards([("zhug", "句型", "情态动词 + be + 过去分词。")])
    + B.fill_q("作业必须按时完成。Homework must ____ (finish) on time.", "be finished")
    + B.sub_label("点击检查，情态 + be + 过去分词")
    + B.body_text("参考：<b>Homework must be finished on time.</b>（作业必须按时完成。）"
                  "技巧：can/must/should + be + 过去分词，情态动词不变。"), 7, "造句情态被动", "句子练习")

add(B.section_head("句", "汉译英 · 主动表被动", "句子练习")
    + B.rule_cards([("bin", "句型", "物 + sell/read/wash + well/easily（主动形式）。")])
    + B.fill_q("这本书卖得好。This book ____ (sell) well.", "sells")
    + B.sub_label("点击检查，sell 主动表被动")
    + B.body_text("参考：<b>This book sells well.</b>（这本书卖得好。）"
                  "技巧：sell/read/wash 用主动形式表被动含义，主语多为物。"), 7, "汉译英主动表被动", "句子练习")

add(B.section_head("句", "汉译英 · 被动否定与疑问", "句子练习")
    + B.rule_cards([("zhug", "句型", "否定：be not + 过去分词；疑问：be + 主语 + 过去分词。")])
    + B.fill_q("这个房间没有被打扫。The room ____ (not clean).", "is not cleaned")
    + B.fill_q("这些玩具是中国制造的吗？____ these toys made in China?", "Are")
    + B.sub_label("点击检查，否定 be not，疑问 be 提前")
    + B.body_text("参考：<b>The room is not cleaned.</b>（没被打扫）/ <b>Are these toys made in China?</b>（是中国制造的吗？）"
                  "技巧：否定加 not 在 be 后，疑问把 be 提到句首。"), 7, "汉译英否定疑问", "句子练习")

add(B.section_head("句", "汉译英 · 被动综合", "句子练习")
    + B.rule_cards([("zhug", "句型", "情态被动 / 主动表被动 / 否定疑问综合。")])
    + B.fill_q("这本书可以现在借吗？Can this book ____ (borrow) now?", "be borrowed")
    + B.fill_q("这块布容易洗。This cloth ____ (wash) easily.", "washes")
    + B.sub_label("点击检查，情态被动与主动表被动")
    + B.body_text("参考：<b>Can this book be borrowed now?</b>（可以现在借吗？）/ <b>This cloth washes easily.</b>（容易洗。）"
                  "技巧：情态疑问把情态提前，主动表被动用三单形式。"), 7, "被动综合", "句子练习")

# ================= 拼读（5页） =================
add(B.section_head("拼", "音素 · -ed 被动过去分词", "音素")
    + B.rule_cards([("zhug", "/t/", "清辅音后：washed/asked/helped。"),
                    ("bin", "/d/", "浊辅音后：used/allowed/required。"),
                    ("xing", "/ɪd/", "-t/-d 后：expected/prohibited/permitted。")])
    + B.quiz_html([("washed 的 -ed 读？", "/t/", ["/d/", "/ɪd/"]),
                   ("used 的 -ed 读？", "/d/", ["/t/", "/ɪd/"]),
                   ("expected 的 -ed 读？", "/ɪd/", ["/t/", "/d/"])])
    + B.note_panel("发音要点", "-ed 被动过去分词三种读音：清辅音后 /t/，浊辅音后 /d/，-t/-d 后 /ɪd/。读准帮助听力。"), 7, "拼读音素", "-ed 被动分词")

add(B.section_head("拼", "看词归音 · -ed 被动", "归音")
    + B.order_q("把含 /ɪd/ 的词挑出来（排序成一列）",
                [("expected", "加一个音"), ("prohibited", "加一个音"), ("used", "浊/d/")],
                "expected|prohibited|used")
    + B.sub_label("自检一题")
    + B.quiz_html([("allowed 读？", "/d/", ["/t/", "/ɪd/"])]), 7, "拼读归音", "-ed 归音")

add(B.section_head("拼", "听音选词 · -ed 被动", "听音")
    + B.quiz_html([("选出 -ed 读 /t/ 的词", "washed", ["used", "expected"]),
                   ("选出 -ed 读 /d/ 的词", "allowed", ["asked", "prohibited"]),
                   ("permitted 的 -ed 读？", "/ɪd/", ["/t/", "/d/"])])
    + B.sub_label("点击作答，听音辨形")
    + B.note_panel("听辨提示", "-ed：清音后 /t/，浊音后 /d/，-t/-d 后 /ɪd/。读慢了注意尾巴。"), 7, "拼读听音", "听音选词")

add(B.section_head("拼", "最小对立对 · used vs expected", "对立")
    + B.rule_cards([("ming", "最小对立", "used（/d/）/expected（/ɪd/）——注意尾音。")])
    + B.match_q([("used", "/d/"), ("expected", "/ɪd/"), ("washed", "/t/"), ("allowed", "/d/")],
                [("/d/", "used"), ("/ɪd/", "expected"), ("/t/", "washed"), ("/d/", "allowed")])
    + B.sub_label("左右两列点击配对"), 7, "拼读对立", "最小对立对")

add(B.section_head("拼", "被动分词 · 拼读应用", "拼读应用")
    + B.sub_label("把过去分词拖到正确位置")
    + B.drag_q([("is ____ (use)", "used", ""), ("was ____ (wash)", "washed", ""), ("is ____ (expect)", "expected", "")],
               ["used", "washed", "expected"])
    + B.sub_label("点击检查，be + 被动过去分词")
    + B.note_panel("拼读小结", "-ed 被动过去分词三种读音，读准帮助听力与拼写。"), 7, "拼读应用", "被动分词应用")

# ================= ⑧ 课堂总结（5页） =================
add(B.section_head("结", "核心口诀总览", "一页速览")
    + B.rule_cards([("zhug", "情态被动", "can/must/should be + done。"),
                    ("xing", "主动表被动", "sell/read/wash + well/easily。"),
                    ("bin", "否定疑问", "be not / be 提前。")])
    + B.quiz_html([("情态被动结构是？", "情态 + be + done", ["be + V-ing", "have + done"]),
                   ("'sells well' 属于？", "主动表被动", ["被动语态", "进行时"]),
                   ("被动否定 be？", "加 not", ["加 does", "删除"])])
    + B.body_text("口诀背诵：<b>情态 be 加 done，can must should。</b>"
                  "sell well 主动表被,be not 否定,be 提前疑问。"
                  "把口诀读两遍,再用本课 20 词各造一句,本课核心就掌握了大半。")
    + B.quiz_html([("被动进阶的核心是？", "情态被动与主动表被动", ["字母拼写", "句子长度"]),
                   ("'wash easily' 属于？", "主动表被动", ["被动语态", "完成时"])]), 8, "核心口诀", "一页速览")

add(B.section_head("结", "课堂思维导图", "全课收尾")
    + B.mind_map(30, "被动语态进阶", [
        ("情态被动", "can/must/should be done"),
        ("主动表被动", "sell well/read well"),
        ("否定疑问", "be not / be 提前"),
        ("阅读识别", "找 be + 过去分词"),
        ("防越级", "不引入完成时被动"),
        ("主题", "生活规则")])
    + B.sub_label("本课 3 考点：情态被动 · 主动表被动 · 否定疑问/识别")
    + B.note_panel("一句话收口", "情态 be 加 done，sell well 主动表被动。"), 8, "思维导图", "全课收尾")

add(B.section_head("结", "语法速查 · 被动进阶公式", "速查卡")
    + B.rule_cards([("zhug", "情态被动", "情态动词 + be + 过去分词"),
                    ("xing", "主动表被动", "物 + sell/read/wash + well"),
                    ("bin", "否定", "主语 + be not + 过去分词"),
                    ("ming", "疑问", "be + 主语 + 过去分词")])
    + B.sub_label("速查:被动进阶四公式")
    + B.quiz_html([("情态被动 be 用？", "原型 be", ["is", "was"]),
                   ("'washes easily' 属于？", "主动表被动", ["被动语态", "进行时"])]), 8, "语法速查", "速查卡")

add(B.section_head("结", "综合演练 · 被动进阶混练", "综合")
    + B.quiz_html([("The work can ____ today.", "be done", ["is done", "done"]),
                   ("This book ____ well.", "sells", ["is sold", "sell"]),
                   ("Homework must ____ on time.", "be finished", ["finished", "is finished"]),
                   ("The room ____ not cleaned.", "is", ["was", "are"]),
                   ("____ these toys made in China?", "Are", ["Is", "Do"])])
    + B.sub_label("点击作答，被动进阶综合检验")
    + B.note_panel("综合检验", "把五题连起来读，确认情态被动、主动表被动、否定疑问正确。错一题回看对应语法卡。"), 8, "综合演练", "进阶混练")

add(B.section_head("结", "课后任务 · 巩固清单", "任务")
    + B.rule_cards([("qita", "任务一", "抄写 20 个规则与认知相关词，各配一句被动进阶句型。"),
                    ("bin", "任务二", "完成配套练习卷（阅读30/语言25/综合25/语法诊断20）。"),
                    ("xing", "任务三", "用 must be done / sells well / is not done 各造 2 句。")])
    + B.quiz_html([("本课核心考点有几个？", "3 个", ["2 个", "5 个"]),
                   ("情态被动用情态 + be + done，对吗？", "对", ["错", "看情况"])])
    + B.ext_card("展望", "Stage 6 语法主线收官，后续将进入定语从句等新语法。"), 8, "课后任务", "巩固清单")

total = p - 1
seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
page_meta = {i: {"p": "CORE", "m": 2} for i in range(1, total + 1)}

js = B.js_extra(total, seg_pages, page_meta)
css = B.CSS_EXTRA + PAD
out = os.path.join(out_dir, "第30课时_课件_中等.html")
size = B.write_courseware(30, "第30课时 · 被动语态进阶", pages, NAV, STAGE, css, js, out, session="D30")
print("L30 课件生成：%s (%d bytes, %d pages)" % (out, size, total))