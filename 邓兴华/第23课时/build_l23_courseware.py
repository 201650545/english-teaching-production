# -*- coding: utf-8 -*-
"""邓兴华 L23 授课课件（if 条件句 G58 + unless G59 + 祈使句and/or · 八段式 · ~44 页）生成脚本"""
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
  <div class="nav-item" data-segment="3" onclick="jumpToSegment(3)"><span class="nav-num">③</span>if条件句</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="4" onclick="jumpToSegment(4)"><span class="nav-num">④</span>unless</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="5" onclick="jumpToSegment(5)"><span class="nav-num">⑤</span>祈使句and/or</div>
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

STAGE = "Stage 6 · L23"

# ================= ① 复习导入（3页） =================
add('<div class="cover-wrap"><div class="cover-badge">Stage 6 · 八上主线</div>'
    '<div class="cover-title">if 条件句 · unless · 祈使句 and/or</div>'
    '<div class="cover-sub">G58 主将从现 + G59 unless + 祈使句 and/or + 将来</div>'
    '<div class="cover-tagline">授课课 · 八段式</div>'
    '<div class="cover-info"><div class="cover-info-num"><div class="ci-label">新词</div><div class="ci-val">20</div></div>'
    '<div class="cover-info-num"><div class="ci-label">考点</div><div class="ci-val">3</div></div>'
    '<div class="cover-info-num"><div class="ci-label">词号</div><div class="ci-val">441–460</div></div>'
    '<div class="cover-info-num"><div class="ci-label">时长</div><div class="ci-val">90分</div></div></div>'
    '<div class="cover-emoji">🔀</div></div>', 1, "L23 条件状语", "八上条件句主线")

add(B.section_head("复", "上一课比较级回顾", "L22 衔接")
    + B.rule_cards([("zhug", "L22 考点", "比较级 -er/more + than ｜ 最高级 the + -est/most + in/of ｜ 同级 as/not as...as。"),
                    ("bin", "本课衔接", "L22 讲形容词比较，L23 转到条件状语从句 if/unless 与祈使句综合。")])
    + B.quiz_html([("L22 讲的是什么内容？", "比较级·最高级·同级", ["条件句", "祈使句"]),
                   ("比较级句型 A ____ 比较级 than B 中空里填？", "is", ["are", "am"])])
    + B.note_panel("L23 起点", "今天学的 if 条件句能表达'如果…就…'，是未来最常用的交际句型之一。"), 1, "复习导入", "L22 衔接")

add(B.section_head("复", "条件句 · 前瞻", "新旧衔接")
    + B.rule_cards([("warn", "什么是条件句", "if 引导条件状语从句，从句用一般现在时，主句用 will + 动词原形（主将从现）。"),
                    ("xing", "unless 用法", "unless = if not（除非），表否定条件。")])
    + B.quiz_html([("if 条件句中'主将从现'指的是？", "从句现在时，主句将来时", ["主句现在时", "都用过去时"]),
                   ("unless 等于？", "if not", ["if", "because"])])
    + B.sub_label("今天把 if / unless / 祈使句三条线一次梳理"), 1, "前瞻", "条件句概念")

add(B.section_head("复", "本课学习目标", "目标导航")
    + B.note_panel("本课 3 大考点", "① G58 if 真实条件句（主将从现）② G59 unless 否定条件句 ③ 祈使句 + and/or + 将来(The more, the better / Work hard, and you'll succeed)。")
    + B.rule_cards([("qita", "学习动作", "看规则 → 填空自检 → 拖拽拆分 → 阅读应用 → 口诀收尾。"),
                    ("ming", "防越级", "仅限真实条件句，不引入虚拟语气。")])
    + B.quiz_html([("本课语法主线是？", "if/unless 条件句", ["被动", "完成时"])])
    + B.ext_card("前后衔接", "L22 比较级收尾，L23 条件句新开辩证；L24 将转到原因/结果/让步状语。")
    + B.note_panel("学习提示", "条件句是写作与口语的高频句型。掌握主将从现，一项技能通三处（if/unless/祈使句and/or）。")
    + B.quiz_html([("'主将从现' 的'现'指？", "从句用现在时", ["主句用现在时", "都用过去时"]),
                   ("unless 与 if not 能否互换？", "能", ["不能", "看情况"])]), 1, "学习目标", "目标导航")

# ================= ② 新词 20（8页） =================
add(B.section_head("词", "新词① · 条件与可能", "词 441–446")
    + B.vocab_cards([
        (("if", "/ɪf/", "conj.", "如果", "if you want / what if", "If you study, you will pass.")),
        (("unless", "/ənˈles/", "conj.", "除非", "unless you try / unless it rains", "You can't win unless you try.")),
        (("condition", "/kənˈdɪʃn/", "n.", "条件", "under the condition / a condition", "This is a condition of the plan.")),
        (("possible", "/ˈpɒsəbl/", "adj.", "可能的", "if possible / be possible", "It is possible to finish today.")),
        (("impossible", "/ɪmˈpɒsəbl/", "adj.", "不可能的", "it is impossible / nothing impossible", "It is impossible to do it alone.")),
        (("advice", "/ədˈvaɪs/", "n.", "建议", "give advice / a piece of advice", "My teacher gave me good advice."))])
    + B.note_panel("if 与 unless 对照", "if 表肯定条件，unless 表否定条件（=if not）。本课核心对比词 pair。")
    + B.ext_card("培优搭配", "give advice to sb（给某人建议）、a piece of advice（一条建议）、under the condition that（在…条件下）。"), 2, "新词① 条件与可能", "词 441–446")

add(B.section_head("词", "新词② · 决定与选择", "词 447–450")
    + B.vocab_cards([
        (("suggest", "/səˈdʒest/", "v.", "建议", "suggest doing / suggest that", "I suggest going early.")),
        (("decision", "/dɪˈsɪʒn/", "n.", "决定", "make a decision / a big decision", "She made a wise decision.")),
        (("choose", "/tʃuːz/", "v.", "选择", "choose to do / choose from", "You can choose a gift.")),
        (("choice", "/tʃɔɪs/", "n.", "选择", "make a choice / have no choice", "He had no choice but to wait."))])
    + B.note_panel("记忆辨析", "choose 动词（选择），choice 名词（选择）；make a decision 做决定。"), 2, "新词② 决定选择", "词 447–450")

add(B.section_head("词", "新词③ · 未来与成败", "词 451–456")
    + B.vocab_cards([
        (("future", "/ˈfjuːtʃə(r)/", "n.", "未来", "in the future / future plans", "What will you do in the future?")),
        (("succeed", "/səkˈsiːd/", "v.", "成功", "succeed in doing / succeed at", "You will succeed if you try.")),
        (("fail", "/feɪl/", "v.", "失败", "fail to do / fail the test", "Don't be afraid to fail.")),
        (("effort", "/ˈefət/", "n.", "努力", "make an effort / with effort", "Success needs effort.")),
        (("practice", "/ˈpræktɪs/", "n./v.", "练习", "practice doing / daily practice", "Practice makes perfect.")),
        (("improve", "/ɪmˈpruːv/", "v.", "提高", "improve English / improve skills", "He wants to improve his English."))]), 2, "新词③ 未来成败", "词 451–456")

add(B.section_head("词", "新词④ · 目标与结果", "词 457–460")
    + B.vocab_cards([
        (("progress", "/ˈprəʊɡres/", "n.", "进步", "make progress / progress in", "You made great progress.")),
        (("goal", "/ɡəʊl/", "n.", "目标", "set a goal / reach a goal", "My goal is to pass the test.")),
        (("plan", "/plæn/", "n./v.", "计划", "make a plan / plan to do", "I plan to study abroad.")),
        (("result", "/rɪˈzʌlt/", "n.", "结果", "as a result / test result", "The result was good."))])
    + B.note_panel("记忆小贴士", "goal 目标、plan 计划、progress 进步、result 结果——是条件句与未来主题的常用词族。"), 2, "新词④ 目标结果", "词 457–460")

add(B.section_head("词", "新词游戏① · 词义翻牌", "翻牌自检")
    + B.sub_label("点击翻牌，看英文想中文，再翻回核对")
    + B.flip_grid([
        ("if", "如果"), ("unless", "除非"), ("condition", "条件"),
        ("possible", "可能的"), ("advice", "建议"), ("decision", "决定"),
        ("choose", "选择"), ("future", "未来"), ("succeed", "成功"),
        ("goal", "目标"), ("progress", "进步"), ("result", "结果")])
    + B.sub_label("自检一题")
    + B.quiz_html([("unless 的意思是？", "除非", ["如果", "因为"])]), 2, "词汇游戏①", "翻牌自检")

add(B.section_head("词", "新词游戏② · 拖拽归位", "拖拽")
    + B.sub_label("把词块拖到正确的解释前面")
    + B.drag_q([("如果 → ", "if", ""),
                ("除非 → ", "unless", ""),
                ("建议（名）→ ", "advice", "")],
               ["if", "unless", "advice"])
    + B.sub_label("自检一题")
    + B.quiz_html([("'make a decision' 意思是？", "做决定", ["做计划", "做选择"])]), 2, "词汇游戏②", "拖拽归位")

add(B.section_head("词", "新词游戏③ · 连线配对", "连线")
    + B.sub_label("把英文词与正确释义连起来")
    + B.match_q([("future", "未来"), ("goal", "目标"), ("succeed", "成功")],
                [("未来", "future"), ("目标", "goal"), ("成功", "succeed")])
    + B.sub_label("左右两列点击配对"), 2, "词汇游戏③", "连线配对")

add(B.section_head("词", "新词游戏④ · 选择演练", "选择")
    + B.sub_label("20 词综合选择")
    + B.quiz_html([("'可能的' 是？", "possible", ["impossible", "future"]),
                   ("'建议'（动词）是？", "suggest", ["advice", "decision"]),
                   ("'选择'（动词）是？", "choose", ["choice", "plan"]),
                   ("'努力' 是？", "effort", ["result", "goal"]),
                   ("'进步' 是？", "progress", ["plan", "choice"]),
                   ("'除非' 是？", "unless", ["if", "because"])])
    + B.ext_card("词汇记忆", "条件句高频词：if（如果）、unless（除非）、condition（条件）、succeed（成功）、fail（失败）。"), 2, "词汇游戏④", "选择演练")

# ================= ③ if 条件句 G58（5页） =================
add(B.section_head("语", "if 真实条件句 · 主将从现", "G58 规则")
    + B.rule_cards([("zhug", "结构", "if + 一般现在时，主句 will + 动词原形。从句用现在时表将来，主句用将来时。"),
                    ("xing", "例句", "If it rains, we will stay at home.（如果下雨，我们就待在家。）主句 We will stay。"),
                    ("warn", "易错", "❌ If it will rain → ✅ If it rains（从句不用将来时）。")])
    + B.quiz_html([("if 从句用哪种时态？", "一般现在时", ["将来时", "过去时"]),
                   ("主句用哪种时态？", "will + 原形", ["现在时", "过去时"]),
                   ("If it ____ (rain), we will stay home.", "rains", ["will rain", "rained"])])
    + B.note_panel("主将从现详解", "主句表主事件的将来结果，从句表条件。条件用一般现在时表达'将来'，这是英语的固定规则，不是时态错误。")
    + B.quiz_html([("If she ____ (get) up early, she will catch the bus.", "gets", ["will get", "got"]),
                   ("主句 will 后接？", "动词原形", ["动词ing", "过去式"])]), 3, "if条件句", "G58 规则")

add(B.section_head("语", "if 条件句 · 补全填空", "G58 练习")
    + B.fill_q("If you ____ (study) hard, you will succeed.", "study")
    + B.fill_q("____ (come) early, you will get a seat.", "If you come")
    + B.sub_label("点击检查，从句用现在时")
    + B.note_panel("填空三步", "①找 if ②从句用一般现在时（三单加 -s）③主句用 will + 原形。"), 3, "if填空", "G58 练习")

add(B.section_head("语", "if 条件句 · 拖拽成句", "G58 应用")
    + B.sub_label("把词块按正确顺序拖入生成条件句")
    + B.drag_q([("If I ", "have", " time, I will help you."),
                ("If she ", "works", " hard, she will pass the test.")],
               ["have", "works"])
    + B.sub_label("自检一题")
    + B.quiz_html([("If I ____ free, I will call you.", "am", ["will be", "was"]),
                   ("主句 will 后接？", "动词原形", ["动词ing", "过去式"])]), 3, "if拖拽", "G58 应用")

add(B.section_head("语", "if 条件句 · 排序成句", "G58 排序")
    + B.order_q("把词块排成正确的条件句",
                [("If", "条件连词"), ("you", "主语"), ("work", "动词"), ("hard", "副词"), ("you will pass", "主句")],
                "If|you|work|hard|you will pass")
    + B.sub_label("自检一题")
    + B.quiz_html([("'主将从现'原则适用于？", "if 条件句", ["宾语从句", "定语从句"]),
                   ("从句动词三单：If she ____ (go)...", "goes", ["go", "will go"])]), 3, "if排序", "G58 排序")

add(B.section_head("语", "if 条件句 · 关键词地图", "考点梳理")
    + B.kmap_block("if 条件句三大关键词", [
        ("if", "如果，引导条件从句"),
        ("will", "主句将来时 + 原形"),
        ("现在时", "从句用一般现在时")])
    + B.sub_label("自检一题")
    + B.quiz_html([("if 从句能不能用 will？", "不能", ["能", "看情况"]),
                   ("If you want to go, ____ me.", "tell", ["told", "telling"])])
    + B.ext_card("特例提醒", "if 有时也引导宾语从句（表'是否'），此时时态不受主将从现约束：I don't know if he will come.（宾语从句可用 will）。")
    + B.quiz_html([("I don't know if he ____ come.（宾语从句）", "will", ["comes", "came"]),
                   ("条件句中 if 从句用？", "现在时", ["将来时", "过去时"])]), 3, "if地图", "关键词")

# ================= ④ unless G59（4页） =================
add(B.section_head("语", "unless 否定条件句", "G59 规则")
    + B.rule_cards([("zhug", "unless = if not", "除非：unless 引导的从句放否定条件，主句用将来时。"),
                    ("xing", "例句", "You won't pass unless you study.（除非你学习，否则不会通过。）"),
                    ("warn", "易错", "unless 已含否定，从句不再加 not（❌ unless you don't study → ✅ unless you study）。")])
    + B.quiz_html([("unless 等于？", "if not", ["if", "because"]),
                   ("unless 从句还能加 not 吗？", "不能", ["能", "看情况"]),
                   ("You won't win ____ you try.", "unless", ["if", "because"])])
    + B.note_panel("unless 双重否定", "unless 本身含否定，句意等于'如果不…就…'。理解时拆成 if not 更清晰：Unless you study = If you don't study。")
    + B.quiz_html([("Unless she comes = ____.", "if she doesn't come", ["if she comes", "because she comes"]),
                   ("主句：You ____ not succeed unless you try.", "will", ["does", "did"])]), 4, "unless规则", "G59 规则")

add(B.section_head("语", "unless · 补全填空", "G59 练习")
    + B.fill_q("We can't go out ____ (除非) it stops raining.", "unless")
    + B.fill_q("____ (如果你不) hurry, you will miss the bus. (用 unless)", "Unless you")
    + B.sub_label("点击检查，unless 表否定条件")
    + B.note_panel("unless ↔ if not 互换", "Unless you hurry = If you don't hurry。两者可互换，语义相同。"), 4, "unless填空", "G59 练习")

add(B.section_head("语", "unless · 连线互换", "G59 连线")
    + B.match_q([("unless you go", "if you don't go"), ("unless it rains", "if it doesn't rain"), ("unless she comes", "if she doesn't come")],
                [("if you don't go", "unless you go"), ("if it doesn't rain", "unless it rains"), ("if she doesn't come", "unless she comes")])
    + B.sub_label("左右两列点击配对，unless 换成 if not"), 4, "unless连线", "G59 连线")

add(B.section_head("语", "unless · 双列选择", "G59 辨析")
    + B.quiz_html([("unless you study 等于？", "if you don't study", ["if you study", "because you study"]),
                   ("除非下雨，我们出去。Unless it ____, we will go out.", "rains", ["will rain", "rained"]),
                   ("主句将来时：You ____ fail unless you practice.", "will", ["does", "did"])])
    + B.ext_card("辨析", "unless 放句首或句中均可，主句常用 will；从句永远用一般现在时表将来。")
    + B.note_panel("unless 全解析", "unless = if not。两者可替换：Unless you try = If you don't try。主句用 will + 原形，从句用一般现在时。")
    + B.fill_q("你不尝试就不会成功。You won't succeed ____ you try. (除非)", "unless")
    + B.quiz_html([("unless 引导的是？", "否定条件", ["肯定条件", "让步"]),
                   ("除非你努力。____ you work hard.", "Unless", ["If", "Because"])]), 4, "unless双列", "G59 辨析")

# ================= ⑤ 祈使句 and/or（4页） =================
add(B.section_head("语", "祈使句 + and/or + 将来", "祈使句综合")
    + B.rule_cards([("zhug", "结构", "祈使句 + and + 将来句（肯定结果）；祈使句 + or + 将来句（否定后果）。"),
                    ("xing", "and 例", "Work hard, and you'll succeed.（努力，你就会成功。）"),
                    ("warn", "or 例", "Hurry up, or you'll be late.（快点，否则你会迟到。）")])
    + B.quiz_html([("祈使句 + and 表示？", "肯定结果", ["否定后果", "并列"]),
                   ("祈使句 + or 表示？", "否定后果", ["肯定结果", "原因"]),
                   ("Work hard, ____ you'll succeed.", "and", ["or", "but"])]), 5, "祈使句and/or", "祈使句综合")

add(B.section_head("语", "祈使句 · 补全填空", "祈使句练习")
    + B.fill_q("____ (work) hard, and you'll succeed.", "Work")
    + B.fill_q("____ (hurry) up, or you'll be late.", "Hurry")
    + B.sub_label("点击检查，and 跟 or 的选择")
    + B.note_panel("选择 and / or", "看语义：and 连接积极结果，or 连接消极后果。")
    + B.fill_q("Be careful, ____ (and/or) you will not fall.", "and")
    + B.quiz_html([("'Don't ____ up, or you'll fail.' 填？", "give", ["giving", "gave"]),
                   ("祈使句 + and 表示？", "积极结果", ["消极后果", "疑问"])]), 5, "祈使句填空", "祈使句练习")

add(B.section_head("语", "祈使句 · 拖拽搭配", "祈使句应用")
    + B.sub_label("把 and / or 拖到正确的句子")
    + B.drag_q([("Study hard, ____ you will pass.", "and", ""),
                ("Be careful, ____ you will fall.", "or", "")],
               ["and", "or"])
    + B.sub_label("自检一题")
    + B.quiz_html([("'Be quiet, ____ the teacher will be angry.' 填？", "or", ["and", "but"]),
                   ("'Do your best, ____ you'll be proud.' 填？", "and", ["or", "so"])]), 5, "祈使句拖拽", "祈使句应用")

add(B.section_head("语", "祈使句 · 排序成句", "祈使句排序")
    + B.order_q("把词块排成正确的祈使句 + or",
                [("Hurry", "祈使"), ("up", "副词"), ("or", "否则"), ("you'll", "主句"), ("be late", "结果")],
                "Hurry|up|or|you'll|be late")
    + B.sub_label("自检一题")
    + B.quiz_html([("祈使句以哪个词开头？", "动词原形", ["名词", "形容词"]),
                   ("'Don't give up' 是什么句？", "否定祈使句", ["陈述句", "疑问句"])]), 5, "祈使句排序", "祈使句排序")

# ================= ⑥ 随堂演练（4页） =================
add(B.section_head("练", "条件句 · 选择演练", "单选")
    + B.quiz_html([("If it ____ sunny, we will go hiking.", "is", ["will be", "was"]),
                   ("You will fail ____ you work hard.", "unless", ["if", "because"]),
                   ("____ late, or you'll miss the bus.", "Don't be", ["Be", "Being"]),
                   ("If she ____ hard, she will improve.", "practices", ["will practice", "practice"])])
    + B.note_panel("解题步骤", "①找 if/unless/祈使句 ②从句用现在时 ③主句 will + 原形 ④and/or 看结果正负。")
    + B.quiz_html([("Unless you hurry, you ____ miss it.", "will", ["does", "did"]),
                   ("If I ____ (be) free, I will join you.", "am", ["will be", "was"]),
                   ("____ your best, and you'll be proud.", "Do", ["Doing", "To do"])]), 6, "随堂演练", "选择")

add(B.section_head("练", "条件句 · 填空演练", "填空")
    + B.fill_q("If you ____ (come) early, you will get a seat.", "come")
    + B.fill_q("You can't pass unless you ____ (study).", "study")
    + B.fill_q("Work hard, and you ____ (succeed).", "will succeed")
    + B.sub_label("点击检查"), 6, "随堂演练", "填空")

add(B.section_head("练", "条件句 · 拖拽排序", "排序")
    + B.sub_label("把词块按正确顺序拖入（排序）")
    + B.order_q("把条件句按正确顺序排列",
                [("If", "连词"), ("you", "主语"), ("practice", "动词"), ("every day", "时间"), ("you will improve", "主句")],
                "If|you|practice|every day|you will improve")
    + B.sub_label("自检一题"), 6, "随堂演练", "排序")

add(B.section_head("练", "条件句 · 综合混练", "综合")
    + B.quiz_html([("If I ____ time, I will help you.", "have", ["will have", "had"]),
                   ("Unless you hurry, you ____ late.", "will be", ["are", "were"]),
                   ("____ quiet, or the baby will wake up.", "Be", ["Being", "To be"]),
                   ("If she works hard, she ____ succeed.", "will", ["does", "did"])])
    + B.sub_label("点击作答，四题全对才算掌握")
    + B.note_panel("综合判定法", "①看 if/unless/祈使句 ②确定从句现在时、主句 will ③and/or 看结果正负 ④动词用原形。")
    + B.quiz_html([("If you ____ (want) to go, tell me.", "want", ["wanted", "will want"]),
                   ("____ up, or you'll miss the beginning.", "Hurry", ["Hurrying", "To hurry"])]), 6, "随堂演练", "综合")

# ================= ⑦ 阅读理解（5页） =================
add(B.section_head("读", "阅读 A 篇 · If I Become a Volunteer", "应用文")
    + B.sub_label("应用文：志愿服务条件（约 195 词）")
    + B.body_text("If I become a volunteer, I will help people in need. I will teach children to read and help old people in the community. "
                  "If I have free time, I will join the environmental club and clean up the park. "
                  "Unless I practice, I won't be a good volunteer. So I will practice my skills every week. "
                  "Work hard, and you'll be a great volunteer. "
                  "Being a volunteer is not just about time; it is about love and effort. "
                  "I believe if we all give a little, the world will become a better place.")
    + B.quiz_html([("If I become a volunteer, I will ____.", "help people", ["sleep", "play"]),
                   ("Unless I practice, I won't be a ____ volunteer.", "good", ["bad", "lazy"]),
                   ("作者在哪里打扫公园？", "the park", ["school", "home"]),
                   ("'Work hard' 在这里是？", "祈使句", ["疑问句", "名词"])])
    + B.note_panel("应用文信息定位", "先看首句 if 条件，再逐题回原文找 will / unless / 祈使句关键词。")
    + B.quiz_html([("作者每周会做什么来提高技能？", "practice skills", ["sleep", "quit"]),
                   ("成为好志愿者需要？", "practice", ["money", "laziness"])]), 7, "阅读 A 篇", "志愿者")

add(B.section_head("读", "阅读 B 篇 · If I Study Abroad", "记叙文")
    + B.sub_label("记叙文：留学计划（约 215 词）")
    + B.body_text("If I study abroad, I will learn a new language and make friends from different countries. "
                  "I really want to improve my English, so I will practice speaking every day. "
                  "Unless I save money, I can't go abroad. So my plan is to work part-time and save a part of my salary. "
                  "My parents give me good advice: work hard, and you'll realize your dream. "
                  "I often set goals and make a plan. I believe if I keep trying, the result will be great. "
                  "Choosing where to go is a big decision, but I am ready for it. "
                  "In the future, I hope to study in a famous university.")
    + B.rule_cards([("bin", "人物", "作者想出国留学，计划打工存钱、每天练口语。")])
    + B.quiz_html([("If I study abroad, I will learn a new ____.", "language", ["song", "game"]),
                   ("Unless I save money, I ____ go abroad.", "can't", ["can", "will"]),
                   ("作者建议如何实现梦想？", "work hard", ["give up", "sleep"]),
                   ("'make a plan' 的意思是？", "做计划", ["放弃", "后悔"])])
    + B.fill_q("我每天练习口语。I will practice ____ (speak) every day.", "speaking")
    + B.sub_label("点击检查")
    + B.note_panel("记叙文信息定位", "记叙文按时间/计划推进。逐题回原文找 if / unless / 将来的动作，注意作者的观点与计划。")
    + B.quiz_html([("作者打算出国做什么？", "learn a new language", ["sleep", "quit"]),
                   ("谁给作者建议？", "parents", ["teachers", "strangers"])]), 7, "阅读 B 篇", "留学")

add(B.section_head("读", "阅读 C 篇 · If You Fail, Try Again", "说明文")
    + B.sub_label("说明文：失败与坚持（约 215 词）")
    + B.body_text("What should you do if you fail? Many people feel sad, but failure is not the end. "
                  "If you fail a test, you can review your mistakes and try again. "
                  "Unless you give up, you still have a chance to succeed. "
                  "Effort is the key. If you make an effort, you will make progress. "
                  "Remember: practice makes perfect. If you practice more, you will get better results. "
                  "Set a goal, make a plan, and work hard. Then, you will see progress step by step. "
                  "Do not be afraid of failure. It is a teacher that helps you grow.")
    + B.rule_cards([("xing", "主旨", "失败不可怕，努力+坚持才能进步。")])
    + B.quiz_html([("失败后应该怎么做？", "复习再试", ["放弃", "伤心"]),
                   ("Unless you give up, you ____ a chance.", "still have", ["lose", "cancel"]),
                   ("'practice makes perfect' 意思是？", "熟能生巧", ["三心二意", "投机取巧"]),
                   ("作者认为失败是？", "成长的老师", ["终点", "惩罚"])])
    + B.note_panel("主旨题技巧", "说明文主旨看首尾句。首句 What should you do if you fail 引出话题，末句 Do not be afraid 点明主旨。")
    + B.fill_q("努力是成功的关键。Effort is the ____ (key/keys) to success.", "key")
    + B.quiz_html([("作者建议失败后？", "review and retry", ["give up", "complain"]),
                   ("'set a goal' 的意思是？", "设定目标", ["放弃目标", "隐藏目标"])]), 7, "阅读 C 篇", "坚持")

add(B.section_head("读", "阅读 · 五选四", "语篇填空")
    + B.sub_label("My Future Plan 语篇填空（5 空 4 选）")
    + B.rule_cards([("bin", "提示", "根据上下文逻辑选择正确的衔接句，注意条件与结果。")])
    + B.order_q("把语篇衔接句按正确逻辑顺序排列",
                [("First", "首先"), ("Then", "然后"), ("Finally", "最后")],
                "First|Then|Finally")
    + B.sub_label("自检一题")
    + B.quiz_html([("五选四中 'however' 表示？", "转折", ["并列", "因果"])])
    + B.ext_card("衔接词", "条件关系：if / unless；结果关系：so / therefore；转折：however / but。")
    + B.fill_q("表因果的衔接词是 ____ (so / however).", "so")
    + B.sub_label("点击检查，注意上下文逻辑"), 7, "阅读五选四", "语篇填空")

add(B.section_head("读", "阅读策略 · 条件信息定位", "策略")
    + B.kmap_block("条件类阅读三步法", [
        ("划条件词", "找出 if / unless / 祈使句"),
        ("判主从句", "从句现在时，主句将来时"),
        ("找结果", "主句 will 后接的动作")])
    + B.body_text("阅读条件类文章时，先划 if/unless，再判断主从句，最后定位主句结果。")
    + B.quiz_html([("条件类阅读第一步是？", "划条件词", ["直接选 C", "背单词"]),
                   ("看到 unless 说明是？", "否定条件", ["肯定条件", "并列"])])
    + B.note_panel("常见设问", "What will happen if...? / What should you do unless...? 这类设问回原文找条件句主句即可。")
    + B.quiz_html([("'What will happen if it rains?' 问的是？", "结果", ["条件", "原因"]),
                   ("unless 从句表达？", "否定条件", ["肯定条件", "并列"])]), 7, "阅读策略", "信息定位")

# ================= 句子练习（3页） =================
add(B.section_head("句", "造句 · if 条件句", "句子练习")
    + B.rule_cards([("zhug", "句型", "If + 现在时，主句 will + 原形。")])
    + B.fill_q("如果明天下雨，我们就不去公园。If it ____ (rain) tomorrow, we won't go to the park.", "rains")
    + B.sub_label("点击检查，从句用现在时")
    + B.body_text("参考：<b>If you are tired, you should rest.</b>（如果你累了，应该休息。）")
    + B.quiz_html([("If you are tired, you ____ rest.", "should", ["shoulds", "willing"]),
                   ("从句现在时：If he ____ (come), we will start.", "comes", ["came", "will come"])]), 7, "造句if", "句子练习")

add(B.section_head("句", "汉译英 · unless", "句子练习")
    + B.rule_cards([("zhug", "句型", "主句将来时 + unless + 现在时。")])
    + B.fill_q("除非你努力，否则你不会成功。You won't succeed ____ you work hard.", "unless")
    + B.sub_label("点击检查，unless = if not"), 7, "汉译英unless", "句子练习")

add(B.section_head("句", "汉译英 · 祈使句 and/or", "句子练习")
    + B.rule_cards([("zhug", "句型", "祈使句 + and/or + 将来句。")])
    + B.fill_q("快点，否则你会迟到。Hurry up, ____ you'll be late.", "or")
    + B.sub_label("点击检查，看结果正负"), 7, "汉译英祈使", "句子练习")

# ================= 拼读（4页） =================
add(B.section_head("拼", "音素 · 元音 /ɪ/ vs /ə(r)/", "音素")
    + B.rule_cards([("zhug", "/ɪ/", "短元音：if, it, sit, big；口型扁平。"),
                    ("xing", "/ə(r)/", "轻元音：better, teacher, worker；词尾 -er 弱读。")])
    + B.quiz_html([("if 中 i 发？", "/ɪ/", ["/eɪ/", "/ɑː/"]),
                   ("teacher 中 er 发？", "/ə(r)/", ["/ɪ/", "/eɪ/"])])
    + B.note_panel("发音要点", "/ɪ/ 是紧短元音，/ə(r)/ 是放松轻元音。读 if 时口型扁平迅速。")
    + B.quiz_html([("sit 中 i 发？", "/ɪ/", ["/iː/", "/eɪ/"]),
                   ("worker 中 er 发？", "/ə(r)/", ["/ɪ/", "/iː/"])]), 7, "拼读音素", "元音")

add(B.section_head("拼", "看词归音 · /ɪ/ 还是 /ə(r)/", "归音")
    + B.order_q("把含 /ɪ/ 的词挑出来（排序成一列）",
                [("if", "短元音"), ("sit", "短元音"), ("teacher", "轻元音")],
                "if|sit|teacher")
    + B.sub_label("自检一题")
    + B.quiz_html([("better 中 er 发？", "/ə(r)/", ["/ɪ/", "/eɪ/"])]), 7, "拼读归音", "/ɪ/ vs /ə(r)/")

add(B.section_head("拼", "听音选词 · 含 /ɪ/", "听音")
    + B.quiz_html([("选出含 /ɪ/ 的词", "if", ["teacher", "but"]),
                   ("选出含 /ə(r)/ 的词", "worker", ["if", "sit"]),
                   ("until 中 i 发？", "/ɪ/", ["/eɪ/", "/ɑː/"])])
    + B.sub_label("点击作答，听音辨形")
    + B.note_panel("听辨提示", "/ɪ/ 短促清晰，/ə(r)/ 弱读含混；抓词尾 -er 与词中短元音区分。"), 7, "拼读听音", "听音选词")

add(B.section_head("拼", "最小对立对 · /ɪ/ vs /iː/", "对立")
    + B.rule_cards([("ming", "最小对立", "if / eat；sit / seat；fill / feel——注意长短音区分。")])
    + B.match_q([("sit", "/sɪt/"), ("seat", "/siːt/"), ("fill", "/fɪl/")],
                [("/sɪt/", "sit"), ("/siːt/", "seat"), ("/fɪl/", "fill")])
    + B.sub_label("左右两列点击配对"), 7, "拼读对立", "最小对立对")

# ================= ⑧ 课堂总结（3页） =================
add(B.section_head("结", "核心口诀总览", "一页速览")
    + B.rule_cards([("zhug", "if 条件句", "主将从现：从句现在时，主句 will + 原形。"),
                    ("xing", "unless", "= if not，除非；从句不再加 not。"),
                    ("bin", "祈使句 and/or", "and 积极结果，or 消极后果。")])
    + B.quiz_html([("if 从句用现在时对吗？", "对", ["错", "不一定"]),
                   ("unless 还能和 not 连用吗？", "不能", ["能", "看情况"])]), 8, "核心口诀", "一页速览")

add(B.section_head("结", "课堂思维导图", "全课收尾")
    + B.mind_map(23, "if 条件句 · unless · 祈使句", [
        ("if", "主将从现 / 从句现在时"),
        ("unless", "= if not / 否定条件"),
        ("祈使句", "and 积极 / or 消极"),
        ("易错", "从句不用 will / unless 不加 not"),
        ("应用", "阅读定位条件词 / 造句 / 拼读"),
        ("防越级", "不引入虚拟语气")])
    + B.sub_label("本课 3 考点：G58 if · G59 unless · 祈使句综合")
    + B.note_panel("一句话收口", "if 表如果、unless 表除非、祈使句 and/or 表因果。三句口诀带走，本课完成。")
    + B.fill_q("除非你练习，否则你不会进步。You won't improve ____ (unless/if) you practice.", "unless")
    + B.quiz_html([("主将从现适用于？", "if 条件句", ["宾语从句", "定语从句"]),
                   ("'Be careful, ____ you'll fall.' 填？", "or", ["and", "but"])]), 8, "思维导图", "全课收尾")

add(B.section_head("结", "课后任务 · 巩固清单", "任务")
    + B.rule_cards([("qita", "任务一", "抄写 20 个条件句相关词，各配一句 if/unless 例句。"),
                    ("bin", "任务二", "完成配套练习卷（阅读30/语言25/综合25/语法诊断20）。"),
                    ("xing", "任务三", "用 if / unless / 祈使句 and/or 各写 2 句。")])
    + B.quiz_html([("本课核心考点有几个？", "3 个", ["2 个", "5 个"]),
                   ("if 从句能直接用 will 吗？", "不能", ["能", "看情况"])])
    + B.ext_card("展望", "L24 将转到原因/结果/让步状语从句，预习 because / although / so 等词。")
    + B.note_panel("收尾提示", "条件句三句口诀：if 表如果、unless 表除非、and/or 看结果。课后按任务清单逐步巩固。"), 8, "课后任务", "巩固清单")

total = p - 1
seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
page_meta = {i: {"p": "CORE", "m": 2} for i in range(1, total + 1)}

js = B.js_extra(total, seg_pages, page_meta)
css = B.CSS_EXTRA
out = os.path.join(out_dir, "第23课时_课件_中等.html")
size = B.write_courseware(23, "第23课时 · if条件句·unless·祈使句", pages, NAV, STAGE, css, js, out, session="D23")
print("L23 课件生成：%s (%d bytes, %d pages)" % (out, size, total))