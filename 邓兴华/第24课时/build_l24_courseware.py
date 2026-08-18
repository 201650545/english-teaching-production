# -*- coding: utf-8 -*-
"""邓兴华 L24 授课课件（原因/结果/让步状语从句 · 八段式 · ~44 页）生成脚本"""
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
  <div class="nav-item" data-segment="3" onclick="jumpToSegment(3)"><span class="nav-num">③</span>原因状语</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="4" onclick="jumpToSegment(4)"><span class="nav-num">④</span>让步状语</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="5" onclick="jumpToSegment(5)"><span class="nav-num">⑤</span>结果目的</div>
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

STAGE = "Stage 6 · L24"

# ================= ① 复习导入（3页） =================
add('<div class="cover-wrap"><div class="cover-badge">Stage 6 · 八上主线</div>'
    '<div class="cover-title">原因·结果·让步状语从句</div>'
    '<div class="cover-sub">G60 because/although + G61 so/so that</div>'
    '<div class="cover-tagline">授课课 · 八段式</div>'
    '<div class="cover-info"><div class="cover-info-num"><div class="ci-label">新词</div><div class="ci-val">20</div></div>'
    '<div class="cover-info-num"><div class="ci-label">考点</div><div class="ci-val">2</div></div>'
    '<div class="cover-info-num"><div class="ci-label">词号</div><div class="ci-val">461–480</div></div>'
    '<div class="cover-info-num"><div class="ci-label">时长</div><div class="ci-val">90分</div></div></div>'
    '<div class="cover-emoji">🔗</div></div>', 1, "L24 状语从句", "八上状语从句主线")

add(B.section_head("复", "上一课条件句回顾", "L23 衔接")
    + B.rule_cards([("zhug", "L23 考点", "if 条件句（主将从现）+ unless（=if not）+ 祈使句 and/or + 将来。"),
                    ("bin", "本课衔接", "L23 讲条件句，L24 转到原因/结果/让步状语从句。")])
    + B.quiz_html([("L23 学到的主将从句规则是？", "从句现在时，主句将来时", ["都用过去时", "都用将来时"]),
                   ("unless 等于？", "if not", ["if", "because"])])
    + B.note_panel("L24 起点", "今天学的 because/although/so 表示因果关系与让步转折，是连词综合运用的一课。"), 1, "复习导入", "L23 衔接")

add(B.section_head("复", "状语从句 · 前瞻", "新旧衔接")
    + B.rule_cards([("warn", "什么是状语从句", "状语从句由连词引导，表原因(because)、让步(although)、结果/目的(so/so that)等。"),
                    ("xing", "避免混用", "because 与 so 不能同时出现在同一句（because...so 是错误）。")])
    + B.quiz_html([("because 表？", "原因", ["让步", "结果"]),
                   ("although 表？", "让步", ["原因", "结果"])])
    + B.sub_label("今天把原因/让步/结果三条线一次梳理"), 1, "前瞻", "状语从句概念")

add(B.section_head("复", "本课学习目标", "目标导航")
    + B.note_panel("本课 2 大考点", "① G60 because/since/as 原因状语 + although/though 让步状语 ② G61 so / so that / in order that 结果与目的状语。")
    + B.rule_cards([("qita", "学习动作", "看规则 → 填空自检 → 拖拽搭配 → 阅读应用 → 口诀收尾。"),
                    ("ming", "防越级", "不引入定语从句（留至 L33）。")])
    + B.quiz_html([("本课语法主线是？", "原因/结果/让步状语", ["定语从句", "被动"])])
    + B.ext_card("前后衔接", "L23 条件句收尾，L24 状语从句新开；L25 将转到动名词与不定式。"), 1, "学习目标", "目标导航")

# ================= ② 新词 20（8页） =================
add(B.section_head("词", "新词① · 因果连词", "词 461–466")
    + B.vocab_cards([
        (("because", "/bɪˈkɒz/", "conj.", "因为", "because of / because + 句子", "I stayed because it was raining.")),
        (("since", "/sɪns/", "conj.", "既然；自从", "since then / since + 句子", "Since you're here, let's start.")),
        (("as", "/æz/", "conj.", "因为；当…时", "as soon as / as a result", "As it rained, we stayed in.")),
        (("although", "/ɔːlˈðəʊ/", "conj.", "虽然", "although + 句子", "Although it was late, he kept working.")),
        (("though", "/ðəʊ/", "conj.", "虽然", "even though / though + 句子", "Though tired, she smiled.")),
        (("however", "/haʊˈevə(r)/", "adv.", "然而", "however + 句子", "He is kind. However, he is strict."))]), 2, "新词① 因果连词", "词 461–466")

add(B.section_head("词", "新词② · 结果与原因", "词 467–470")
    + B.vocab_cards([
        (("therefore", "/ˈðeəfɔː(r)/", "adv.", "因此", "therefore + 句子", "It rained; therefore, we stayed.")),
        (("result", "/rɪˈzʌlt/", "n.", "结果", "as a result / result in", "As a result, we won.")),
        (("cause", "/kɔːz/", "n./v.", "原因；导致", "the cause of / cause trouble", "What caused the problem?")),
        (("effect", "/ɪˈfekt/", "n.", "影响；效果", "have an effect on / take effect", "TV has an effect on children."))])
    + B.note_panel("cause/effect 对比", "cause 是因，effect 是果。cause 也可作动词表'导致'。"), 2, "新词② 结果原因", "词 467–470")

add(B.section_head("词", "新词③ · 解释与问题", "词 471–476")
    + B.vocab_cards([
        (("reason", "/ˈriːzn/", "n.", "理由", "the reason for / for this reason", "Tell me the reason.")),
        (("explain", "/ɪkˈspleɪn/", "v.", "解释", "explain sth to sb / explain why", "Can you explain the rule?")),
        (("situation", "/ˌsɪtʃuˈeɪʃn/", "n.", "情况", "in this situation / a difficult situation", "We are in a hard situation.")),
        (("problem", "/ˈprɒbləm/", "n.", "问题", "solve a problem / no problem", "We have a big problem.")),
        (("solution", "/səˈluːʃn/", "n.", "解决办法", "a solution to / find a solution", "We found a solution.")),
        (("besides", "/bɪˈsaɪdz/", "prep.", "除…之外", "besides + 名词 / besides", "Besides English, I study French."))]), 2, "新词③ 解释问题", "词 471–476")

add(B.section_head("词", "新词④ · 让步与替代", "词 477–480")
    + B.vocab_cards([
        (("despite", "/dɪˈspaɪt/", "prep.", "尽管", "despite + 名词 / in spite of", "Despite the rain, we went out.")),
        (("unless", "/ənˈles/", "conj.", "除非", "unless + 句子", "We'll fail unless we try.")),
        (("while", "/waɪl/", "conj.", "当…时；然而", "while + 句子 / while", "While I read, he wrote.")),
        (("instead", "/ɪnˈsted/", "adv.", "代替", "instead of / instead", "I'll go instead of you."))])
    + B.note_panel("记忆小贴士", "despite/although 都表让步；despite+名词，although+句子；instead 表替代。"), 2, "新词④ 让步替代", "词 477–480")

add(B.section_head("词", "新词游戏① · 词义翻牌", "翻牌自检")
    + B.sub_label("点击翻牌，看英文想中文，再翻回核对")
    + B.flip_grid([
        ("because", "因为"), ("although", "虽然"), ("however", "然而"),
        ("therefore", "因此"), ("cause", "原因"), ("effect", "影响"),
        ("reason", "理由"), ("solution", "办法"), ("despite", "尽管"),
        ("unless", "除非"), ("while", "当…时"), ("instead", "代替")])
    + B.sub_label("自检一题")
    + B.quiz_html([("however 的意思是？", "然而", ["因为", "因此"])]), 2, "词汇游戏①", "翻牌自检")

add(B.section_head("词", "新词游戏② · 拖拽归位", "拖拽")
    + B.sub_label("把词块拖到正确的解释前面")
    + B.drag_q([("因为 → ", "because", ""),
                ("虽然 → ", "although", ""),
                ("因此 → ", "therefore", "")],
               ["because", "although", "therefore"])
    + B.sub_label("自检一题")
    + B.quiz_html([("'solve a problem' 意思是？", "解决问题", ["制造问题", "忽略问题"])]), 2, "词汇游戏②", "拖拽归位")

add(B.section_head("词", "新词游戏③ · 连线配对", "连线")
    + B.sub_label("把英文词与正确释义连起来")
    + B.match_q([("because", "因为"), ("despite", "尽管"), ("instead", "代替")],
                [("因为", "because"), ("尽管", "despite"), ("代替", "instead")])
    + B.sub_label("左右两列点击配对"), 2, "词汇游戏③", "连线配对")

add(B.section_head("词", "新词游戏④ · 选择演练", "选择")
    + B.sub_label("20 词综合选择")
    + B.quiz_html([("'然而' 是？", "however", ["therefore", "because"]),
                   ("'原因' 是？", "cause", ["effect", "result"]),
                   ("'解释' 是？", "explain", ["describe", "arrive"]),
                   ("'办法' 是？", "solution", ["problem", "reason"]),
                   ("'尽管' 是？", "despite", ["because", "unless"]),
                   ("'代替' 是？", "instead", ["while", "since"])])
    + B.ext_card("词汇记忆", "因果连词族：because/since/as（因为）、so/therefore（所以）、although/though（虽然）。")
    + B.quiz_html([("'the reason for' 中 for 后接？", "名词", ["句子", "动词原形"]),
                   ("'explain sth to sb' 意思是？", "向某人解释某事", ["向某人借东西", "向某人道歉"]),
                   ("'in this situation' 意思是？", "在这种情况下", ["在那种天气", "在某个餐厅"]),
                   ("'besides English' 意思是？", "除了英语之外", ["英语之内", "只有英语"]),
                   ("'instead of' 意思是？", "而不是", ["然后", "因为"]),
                   ("'as a result' 表？", "结果", ["原因", "让步"])]), 2, "词汇游戏④", "选择演练")

# ================= ③ 原因状语 G60（5页） =================
add(B.section_head("语", "because/since/as · 原因状语", "G60 规则")
    + B.rule_cards([("zhug", "because", "表直接原因，语气最强：I stayed home because it rained.。"),
                    ("xing", "since / as", "表已知原因，译'既然/因为'：Since you are tired, rest.。"),
                    ("warn", "because 与 so 不连用", "❌ Because it rained, so we stayed. → ✅ Because it rained, we stayed. 或 It rained, so we stayed.")])
    + B.quiz_html([("because 表？", "原因", ["结果", "让步"]),
                   ("since 可译作？", "既然", ["然而", "因此"]),
                   ("because 与 so 能连用吗？", "不能", ["能", "看情况"])]), 3, "原因状语", "G60 because")

add(B.section_head("语", "原因状语 · 补全填空", "G60 练习")
    + B.fill_q("I was late ____ (because/since) of the traffic.", "because")
    + B.fill_q("____ (因为) it was cold, we wore coats. (用 since)", "Since")
    + B.sub_label("点击检查，because 后接名词用 because of")
    + B.note_panel("because vs because of", "because + 句子；because of + 名词/短语：because it rained / because of the rain。"), 3, "原因填空", "G60 练习")

add(B.section_head("语", "原因状语 · 拖拽成句", "G60 应用")
    + B.sub_label("把词块按正确顺序拖入生成原因句")
    + B.drag_q([("I stayed in ", "because", " it was raining."),
                ("Since you are free, ", "come", " and help me.")],
               ["because", "come"])
    + B.sub_label("自检一题")
    + B.quiz_html([("because of 后接？", "名词", ["句子", "动词"]),
                   ("'潜在'原因语气较弱的是？", "since/as", ["because", "so"])]), 3, "原因拖拽", "G60 应用")

add(B.section_head("语", "原因状语 · 排序成句", "G60 排序")
    + B.order_q("把词块排成正确的原因句",
                [("Because", "连词"), ("it", "主语"), ("rained", "动词"), ("we", "主句"), ("stayed home", "结果")],
                "Because|it|rained|we|stayed home")
    + B.sub_label("自检一题")
    + B.quiz_html([("'因为下雨' 用 because of 应接？", "the rain", ["it rained", "raining"]),
                   ("since 表原因语气比 because？", "弱", ["强", "一样"])]), 3, "原因排序", "G60 排序")

add(B.section_head("语", "原因状语 · 关键词地图", "考点梳理")
    + B.kmap_block("原因状语三大关键词", [
        ("because", "直接原因 + 句子"),
        ("since/as", "已知原因，既然"),
        ("because of", "+ 名词/短语")])
    + B.sub_label("自检一题")
    + B.quiz_html([("because of 后面接的是？", "名词/短语", ["完整句子", "动词原形"]),
                   ("'既然你在这里' 用哪个词最佳？", "since", ["because", "so"])]), 3, "原因地图", "关键词")

# ================= ④ 让步状语（4页） =================
add(B.section_head("语", "although/though · 让步状语", "G60 让步")
    + B.rule_cards([("zhug", "although/though", "虽然：although 较正式，though 较口语；引导让步从句。"),
                    ("xing", "however", "然而：为副词，连接前后两个独立句，后接逗号。"),
                    ("warn", "不与 but 连用", "although 与 but 不能同时用（❌ Although it was late, but he came. → 去掉 but）。")])
    + B.quiz_html([("although 表？", "让步", ["原因", "结果"]),
                   ("although 能与 but 连用吗？", "不能", ["能", "看情况"]),
                   ("____ it was hard, he finished it.", "Although", ["Because", "So"])]), 4, "让步状语", "G60 although")

add(B.section_head("语", "让步状语 · 补全填空", "G60 练习")
    + B.fill_q("____ (虽然) it was late, he kept working. (用 although)", "Although")
    + B.fill_q("Though she was tired, ____ she smiled. (填 although/but 二选一)", "but")
    + B.sub_label("点击检查，注意 although 与 but 取舍")
    + B.note_panel("although vs but", "although 放从句句首引导让步，but 连接并列分句表达转折。同一句只能用一个。"), 4, "让步填空", "G60 练习")

add(B.section_head("语", "让步状语 · 连线互换", "G60 连线")
    + B.match_q([("Although it rained", "it rained, but"), ("Though he is young", "he is young, but"), ("Although tired", "tired, but")],
                [("it rained, but", "Although it rained"), ("he is young, but", "Though he is young"), ("tired, but", "Although tired")])
    + B.sub_label("左右两列点击配对，although 换成 but"), 4, "让步连线", "G60 连线")

add(B.section_head("语", "让步状语 · 双列选择", "G60 辨析")
    + B.quiz_html([("although 引导的从句在主句前后均可，对吗？", "对", ["错", "不一定"]),
                   ("However 后常接？", "逗号", ["句点后动词", "介词"]),
                   ("____ he was busy, he still helped me. 填？", "Although", ["Because", "So"])])
    + B.ext_card("辨析", "although/though 让步；however 表转折，前后是两个独立句。三者都是 L24 高频考点。"), 4, "让步双列", "G60 辨析")

# ================= ⑤ 结果目的 G61（4页） =================
add(B.section_head("语", "so / so that · 结果目的", "G61 规则")
    + B.rule_cards([("zhug", "so", "所以：表结果，I was tired, so I slept.。"),
                    ("xing", "so that", "以便：表目的，I study hard so that I can pass.。"),
                    ("warn", "in order that", "为了：较正式，后接 can/may/will。")])
    + B.quiz_html([("so 表？", "结果", ["目的", "原因"]),
                   ("so that 表？", "目的", ["结果", "让步"]),
                   ("I got up early ____ I could catch the bus.", "so that", ["because", "although"])]), 5, "结果目的", "G61 so")

add(B.section_head("语", "结果目的 · 补全填空", "G61 练习")
    + B.fill_q("He was tired, ____ (so/so that) he went to bed early.", "so")
    + B.fill_q("She spoke loudly so that everyone ____ (can/could) hear her.", "could")
    + B.sub_label("点击检查，so 结果、so that 目的")
    + B.note_panel("so vs so that", "so 引导结果从句（因果），so that 引导目的从句（以便）。看主句是否表'为了'。"), 5, "结果目的填空", "G61 练习")

add(B.section_head("语", "结果目的 · 拖拽搭配", "G61 应用")
    + B.sub_label("把 so / so that 拖到正确的句子")
    + B.drag_q([("It was hot, ____ we turned on the fan.", "so", ""),
                ("I save money ____ I can buy a bike.", "so that", "")],
               ["so", "so that"])
    + B.sub_label("自检一题")
    + B.quiz_html([("'以便' 用哪个词？", "so that", ["so", "because"]),
                   ("'所以' 用哪个词？", "so", ["so that", "although"])]), 5, "结果目的拖拽", "G61 应用")

add(B.section_head("语", "结果目的 · 排序成句", "G61 排序")
    + B.order_q("把词块排成正确的目的句",
                [("I", "主语"), ("study", "动词"), ("hard", "副词"), ("so that", "目的"), ("I can pass", "结果")],
                "I|study|hard|so that|I can pass")
    + B.sub_label("自检一题")
    + B.quiz_html([("in order that 较？", "正式", ["口语", "错误"]),
                   ("so that 后常接 can/may/will，对吗？", "对", ["错", "不一定"])]), 5, "结果目的排序", "G61 排序")

# ================= ⑥ 随堂演练（4页） =================
add(B.section_head("练", "状语从句 · 选择演练", "单选")
    + B.quiz_html([("I was happy ____ I got a gift.", "because", ["although", "so that"]),
                   ("____ he is old, he is strong.", "Although", ["Because", "So"]),
                   ("He was sick, ____ he stayed home.", "so", ["so that", "although"]),
                   ("She works hard ____ she can pass.", "so that", ["so", "because"])])
    + B.note_panel("解题步骤", "①看逻辑关系（原因/让步/结果/目的）②选连词 ③检查 because/although 不与 so/but 连用。"), 6, "随堂演练", "选择")

add(B.section_head("练", "状语从句 · 填空演练", "填空")
    + B.fill_q("The game was over, so we ____ (go) home.", "went")
    + B.fill_q("Although it was hot, ____ (he/him) kept working.", "he")
    + B.fill_q("Since you are free, ____ (come/came) with us.", "come")
    + B.sub_label("点击检查"), 6, "随堂演练", "填空")

add(B.section_head("练", "状语从句 · 拖拽排序", "排序")
    + B.sub_label("把词块按正确顺序拖入（排序）")
    + B.order_q("把让步句按正确顺序排列",
                [("Although", "连词"), ("he", "主语"), ("was", "be"), ("tired", "形容词"), ("he kept going", "主句")],
                "Although|he|was|tired|he kept going")
    + B.sub_label("自检一题"), 6, "随堂演练", "排序")

add(B.section_head("练", "状语从句 · 综合混练", "综合")
    + B.quiz_html([("I stayed home ____ it was raining.", "because", ["although", "so that"]),
                   ("Although it was cold, we ____ out.", "went", ["go", "will go"]),
                   ("He failed, so he ____ again.", "tried", ["try", "tries"]),
                   ("She studies hard so that she ____ pass.", "can", ["does", "did"])])
    + B.sub_label("点击作答，四题全对才算掌握")
    + B.note_panel("综合审题三步", "①看主句与从句逻辑（因/果/让步/目的）②选对连词 ③检查全句时态是否一致。把四题连起来读一遍，验证通顺。")
    + B.quiz_html([("'I stayed home because it was raining.' 中 because 说明？", "我待家的原因", ["我待家的结果", "我待家的目的"]),
                   ("'She studies hard so that she can pass.' 中 so that 说明？", "她努力的目的", ["她努力的原因", "她努力的结果"]),
                   ("四项中哪项表让步？", "Although it was cold", ["I stayed home because", "He failed so", "She studies hard so that"])])
    + B.body_text("本课综合运用：because 表因、although 表让步、so 表果、so that 表目的。"
                  "做题时先判断逻辑再选词，特别注意 because...so 与 although...but 不能同时出现。"), 6, "随堂演练", "综合")

# ================= ⑦ 阅读理解（5页） =================
add(B.section_head("读", "阅读 A 篇 · Why Do Teenagers Love Social Media", "说明文")
    + B.sub_label("说明文：青少年为什么爱社交媒体（约 195 词）")
    + B.body_text("Why do teenagers love social media? There are several reasons. "
                  "Because social media is easy to use, many teens can share photos and ideas quickly. "
                  "Since they can talk to friends at any time, it makes them feel connected. "
                  "Although it is fun, too much time online can be a problem. "
                  "So parents should help teens balance their time. "
                  "Experts say that because teens love social media, they need rules. "
                  "Therefore, families should set clear limits. "
                  "In short, social media is useful, but we must use it wisely.")
    + B.quiz_html([("青少年为什么爱社交媒体？（原因）", "easy to use", ["too expensive", "no fun"]),
                   ("'feel connected' 意思是？", "感到被联系/有归属", ["感到孤独", "感到无聊"]),
                   ("although 引导的从句表？", "让步", ["原因", "结果"]),
                   ("作者建议家长做什么？", "设定规则", ["没收手机", "不管"])])
    + B.note_panel("说明文信息定位", "说明文常以 why 开头引出原因，逐题回原文找 because/since/although/so 等连词定位。")
    + B.quiz_html([("'feel connected' 的相反意思大概是？", "感到孤独", ["感到兴奋", "感到充实"]),
                   ("家长应帮孩子做什么？", "平衡上网时间", ["多买手机", "不闻不问"])])
    + B.body_text("关键句回看：<b>Because social media is easy to use, many teens can share photos quickly.</b> "
                  "这里 because 说明原因；<b>Although it is fun, too much time online can be a problem.</b> "
                  "这里 although 表让步，说明'虽然有趣但有害'。"
                  "最后一句话 <b>we must use it wisely</b> 是作者的建议，说明社交媒体要'明智使用'。")
    + B.fill_q("因为社交媒体容易使用，许多青少年能快速分享照片。____ social media is easy to use, many teens can share photos quickly. (用because)", "Because")
    + B.fill_q("虽然有趣，但上网太多可能是个问题。____ it is fun, too much time online can be a problem. (用although)", "Although")
    + B.sub_label("点击检查，注意 because 与 although 的用法区分")
    + B.quiz_html([("'share photos and ideas quickly' 中 quickly 修饰？", "share", ["photos", "ideas"]),
                   ("最后一句表达作者什么态度？", "明智使用", ["完全禁止", "无限制使用"])]), 7, "阅读 A 篇", "社交媒体")

add(B.section_head("读", "阅读 B 篇 · A Reason to Help", "记叙文")
    + B.sub_label("记叙文：帮助的理由（约 215 词）")
    + B.body_text("Last week, I saw an old man who could not cross the street. "
                  "Because the traffic was heavy, I decided to help him. "
                  "Although I was in a hurry, I stopped and walked with him. "
                  "He thanked me, so I felt very happy. "
                  "Since helping others is easy, everyone can do it. "
                  "However, many people are too busy to notice. "
                  "I think everyone should help, so our community will be warmer. "
                  "As a result, more people may start to help each other. "
                  "One small act can bring great change.")
    + B.rule_cards([("bin", "人物", "作者帮助老人过马路，感到快乐，呼吁大家互助。")])
    + B.quiz_html([("作者为什么帮助老人？", "交通繁忙", ["想出名", "被迫"]),
                   ("although 从句的内容是？", "作者很忙", ["老人很忙", "天气很好"]),
                   ("'too busy to notice' 意思是？", "忙到没注意", ["闲到无事", "故意忽略"]),
                   ("作者希望社区变得更？", "温暖", ["冷漠", "拥挤"])])
    + B.fill_q("因为交通繁忙，我决定帮他。____ the traffic was heavy, I decided to help him. (用because)", "Because")
    + B.sub_label("点击检查")
    + B.note_panel("记叙文信息定位", "记叙文按事件推进。逐题回原文找 because/although/so 等连词与动作，注意作者的情感变化。")
    + B.quiz_html([("作者帮助老人后的心情是？", "高兴", ["难过", "生气"]),
                   ("'one small act' 意思是？", "一个小行动", ["一个大笑话", "一场大雨"])])
    + B.body_text("情感线索回看：作者从 <b>decided to help</b>（决定帮助）到 <b>felt very happy</b>（感到快乐），"
                  "再到 <b>one small act can bring great change</b>（一个小行动能带来大改变）。"
                  "记叙文的考点常在这些情感变化与因果连词上，如 because 说明动机、so 说明结果。")
    + B.fill_q("虽然我很忙，我还是停下来陪他走。____ I was in a hurry, I stopped and walked with him. (用although)", "Although")
    + B.fill_q("他感谢了我，所以我很高兴。He thanked me, ____ I felt very happy. (用so)", "so")
    + B.sub_label("点击检查，注意 although 与 so 的使用语境")
    + B.quiz_html([("'As a result' 相当于？", "因此", ["然而", "例如"]),
                   ("作者希望更多人？", "互相帮助", ["各忙各的", "远离老人"]),
                   ("'too busy to notice' 中 to notice 表？", "目的/结果", ["原因", "让步"])]), 7, "阅读 B 篇", "助人")

add(B.section_head("读", "阅读 C 篇 · Solving a Problem", "说明文")
    + B.sub_label("说明文：解决问题（约 215 词）")
    + B.body_text("Every problem has a solution. First, you should understand the problem. "
                  "Because you need to know the cause before you can fix the effect. "
                  "For example, if a student fails a test, the reason might be no review. "
                  "So the solution is to make a study plan. "
                  "Although it takes time, hard work always pays off. "
                  "Therefore, don't give up when you meet a problem. "
                  "Explain the situation to your teacher or parents, and they can give you advice. "
                  "In this way, you can turn a problem into a chance to grow.")
    + B.rule_cards([("xing", "主旨", "每个问题都有解决办法，先找原因再定方案。")])
    + B.quiz_html([("解决问题前先要？", "理解问题", ["直接放弃", "责怪别人"]),
                   ("'the reason might be no review' 意思是？", "原因可能是没复习", ["原因是不聪明", "没人在意"]),
                   ("作者建议遇到问题不要？", "放弃", ["坚持", "思考"]),
                   ("'turn...into' 意思是？", "把…变成", ["把…扔掉", "把…隐藏"])])
    + B.note_panel("cause/effect 结构", "说明文常用 cause（原因）→ solution（办法）结构，找 because/reason 定位因，找 so/solution 定位果。")
    + B.fill_q("失败的原因是没复习。The reason is no ____ (review/revise).", "review")
    + B.quiz_html([("作者建议制定？", "学习计划", ["新手机", "新游戏"]),
                   ("'pay off' 意思是？", "有回报", ["付钱", "放弃"])])
    + B.body_text("结构回看：这篇说明文按 <b>问题→原因→办法</b> 展开。"
                  "先提出问题（Every problem has a solution），再分析原因（the cause before the effect），"
                  "最后给出办法（make a study plan / explain to your teacher）。"
                  "遇到此类文章，可用 <b>cause → effect → solution</b> 三步快速理清逻辑。")
    + B.quiz_html([("文章按什么顺序展开？", "问题→原因→办法", ["时间→地点→人物", "票数→排名→奖项"]),
                   ("'don't give up' 意思是？", "不要放弃", ["不要开始", "不要休息"]),
                   ("向老师或家长诉说情况可以？", "得到建议", ["得到奖品", "免作业"]),
                   ("'turn a problem into a chance' 意思是？", "把问题变成机会", ["把机会变成问题", "把问题藏起来"])]), 7, "阅读 C 篇", "解决问题")

add(B.section_head("读", "阅读 · 五选四", "语篇填空")
    + B.sub_label("My Day 语篇填空（5 空 4 选）")
    + B.rule_cards([("bin", "提示", "根据上下文逻辑选择正确的衔接句，注意因果与转折。")])
    + B.order_q("把语篇衔接句按正确逻辑顺序排列",
                [("First", "首先"), ("Then", "然后"), ("Finally", "最后")],
                "First|Then|Finally")
    + B.sub_label("自检一题")
    + B.quiz_html([("五选四中 'therefore' 表示？", "因果", ["并列", "让步"])])
    + B.ext_card("衔接词", "因果：because/so/therefore；转折：although/though/however。"), 7, "阅读五选四", "语篇填空")

add(B.section_head("读", "阅读策略 · 因果信息定位", "策略")
    + B.kmap_block("因果类阅读三步法", [
        ("划连词", "找出 because/although/so/however"),
        ("判关系", "原因是因，so 是果，although 让步"),
        ("定位", "回原文找对应句子")])
    + B.body_text("阅读因果类文章时，先划连词，再判断逻辑关系，最后回原文定位。")
    + B.quiz_html([("because 引导的是？", "原因", ["结果", "让步"]),
                   ("so 引导的是？", "结果", ["原因", "让步"])])
    + B.note_panel("常见设问", "Why...?（找 because/since/as）/ What is the result?（找 so/therefore）。"), 7, "阅读策略", "信息定位")

# ================= 句子练习（3页） =================
add(B.section_head("句", "造句 · because 原因", "句子练习")
    + B.rule_cards([("zhug", "句型", "Because + 从句，主句。或 主句 because + 从句。")])
    + B.fill_q("因为下雨，我们待在家。____ it rained, we stayed at home.", "Because")
    + B.sub_label("点击检查，because 不能与 so 连用")
    + B.body_text("参考：<b>I stayed home because it rained.</b>（因为下雨我待在家。）"
                  "技巧：先说结果，再用 because 补原因。若用 because 起句，主句在后，中间用逗号。"
                  "注意 because 后接完整句子，若是名词短语则用 because of。")
    + B.quiz_html([("'因为堵车我迟到了' 用 because of 应接？", "the traffic", ["it was crowded", "crowded"]),
                   ("because 引导的是？", "原因从句", ["结果从句", "让步从句"]),
                   ("He was late because ____.", "he missed the bus", ["of he missed", "the bus was"])]), 7, "造句because", "句子练习")

add(B.section_head("句", "汉译英 · although", "句子练习")
    + B.rule_cards([("zhug", "句型", "Although + 从句，主句。")])
    + B.fill_q("虽然他很累，但他没有放弃。____ he was tired, he didn't give up.", "Although")
    + B.sub_label("点击检查，although 不与 but 连用")
    + B.body_text("参考：<b>Although he was tired, he didn't give up.</b>"
                  "注意中文里常说'虽然…但是…'，英语里 although 与 but 只能选一个。"
                  "用 although 起句，后面不能再出现 but；若用 but，则前面不再用 although。")
    + B.quiz_html([("下面哪句正确？", "Although tired, he kept going", ["Although tired, but he kept going", "but kept going he"]),
                   ("'虽然还早，他已经到了' 用 although 应接？", "It was still early", ["early", "of early"]),
                   ("though 与 although 相比更？", "口语化", ["更正式", "只能用于句首"])]), 7, "汉译英although", "句子练习")

add(B.section_head("句", "汉译英 · so that", "句子练习")
    + B.rule_cards([("zhug", "句型", "主句 so that 从句（以便）。")])
    + B.fill_q("她早起以便能赶上公交。She got up early ____ she could catch the bus.", "so that")
    + B.sub_label("点击检查，so that 表目的")
    + B.body_text("参考：<b>She got up early so that she could catch the bus.</b>"
                  "so that 引导目的状语，后接 can/may/could 等情态动词。"
                  "若表结果只用 so：She got up late, so she missed the bus.（结果）"
                  "区别：so + 结果，so that + 目的。看主句动作是否有'以便'意图。")
    + B.quiz_html([("'I study hard ____ I can win.' 填？", "so that", ["so", "although"]),
                   ("'所以' 用哪个词？", "so", ["so that", "because"]),
                   ("so that 后常接？", "情态动词", ["名词", "过去分词"])]), 7, "汉译英so that", "句子练习")

# ================= 拼读（4页） =================
add(B.section_head("拼", "音素 · 连词中的元音", "音素")
    + B.rule_cards([("zhug", "/ɔː/", "长元音：although, because 中的 au/aw；口型圆。"),
                    ("xing", "/ə(r)/", "轻元音：however, therefore 中的 er；词尾弱读。")])
    + B.quiz_html([("although 中 al 发？", "/ɔː/", ["/ɪ/", "/eɪ/"]),
                   ("however 中 er 发？", "/ə(r)/", ["/ɔː/", "/iː/"])])
    + B.note_panel("发音要点", "/ɔː/ 圆唇长读，/ə(r)/ 松唇弱读。读 although 时 o 圆唇，读 however 时 er 弱化。"), 7, "拼读音素", "元音")

add(B.section_head("拼", "看词归音 · /ɔː/ 还是 /ə(r)/", "归音")
    + B.order_q("把含 /ɔː/ 的词挑出来（排序成一列）",
                [("although", "长元音"), ("because", "长元音"), ("however", "轻元音")],
                "although|because|however")
    + B.sub_label("自检一题")
    + B.quiz_html([("therefore 中 er 发？", "/ə(r)/", ["/ɔː/", "/iː/"])]), 7, "拼读归音", "/ɔː/ vs /ə(r)/")

add(B.section_head("拼", "听音选词 · 含 /ɔː/", "听音")
    + B.quiz_html([("选出含 /ɔː/ 的词", "although", ["however", "since"]),
                   ("选出含 /ə(r)/ 的词", "therefore", ["although", "because"]),
                   ("because 中 au 发？", "/ə/", ["/ɔː/", "/eɪ/"])])
    + B.sub_label("点击作答，听音辨形")
    + B.note_panel("听辨提示", "although 的 al 重读 /ɔː/，however 的 er 弱读 /ə(r)/。连词拼接读要快而清。"), 7, "拼读听音", "听音选词")

add(B.section_head("拼", "最小对立对 · /ɔː/ vs /əʊ/", "对立")
    + B.rule_cards([("ming", "最小对立", "although / also；though / those——注意 /ɔː/ 与 /əʊ/ 区分。")])
    + B.match_q([("although", "/ɔːlðəʊ/"), ("though", "/ðəʊ/"), ("also", "/ˈɔːlsəʊ/")],
                [("/ɔːlðəʊ/", "although"), ("/ðəʊ/", "though"), ("/ˈɔːlsəʊ/", "also")])
    + B.sub_label("左右两列点击配对"), 7, "拼读对立", "最小对立对")

# ================= ⑧ 课堂总结（3页） =================
add(B.section_head("结", "核心口诀总览", "一页速览")
    + B.rule_cards([("zhug", "原因", "because 直接因，since/as 既然；because of + 名词。"),
                    ("xing", "让步", "although/though 虽然，不与 but 连用；however 然而。"),
                    ("bin", "结果目的", "so 所以，so that 以便；in order that 表目的。")])
    + B.quiz_html([("because 与 so 能连用吗？", "不能", ["能", "看情况"]),
                   ("although 与 but 能连用吗？", "不能", ["能", "看情况"])])
    + B.body_text("口诀背诵：<b>because 因、although 让步、so 结果、so that 目的。</b>"
                  "四个连词各管一摊，因为所以不能叠，虽然但是只能一。"
                  "because of 接名词，so that 后接 can/may 表目的。"
                  "把口诀读两遍，再用本课 20 词各造一句，本课核心就掌握了大半。")
    + B.quiz_html([("'四连词' 指哪些？", "because/although/so/so that", ["is/am/are/be", "and/or/but/so"]),
                   ("because of 后接？", "名词", ["完整句子", "动词原形"]),
                   ("本课口诀的核心是？", "四连词各司其职", ["越多越难", "越精确越好"])]), 8, "核心口诀", "一页速览")

add(B.section_head("结", "课堂思维导图", "全课收尾")
    + B.mind_map(24, "原因·结果·让步状语从句", [
        ("原因", "because/since/as + because of"),
        ("让步", "although/though + however"),
        ("结果目的", "so / so that / in order that"),
        ("易错", "because-not-so / although-not-but"),
        ("应用", "阅读定位连词 / 造句 / 拼读"),
        ("防越级", "不引入定语从句")])
    + B.sub_label("本课 2 考点：G60 because/although · G61 so/so that")
    + B.note_panel("一句话收口", "because 表因、although 表让步、so 表果、so that 表目的。四连词一次带走。"), 8, "思维导图", "全课收尾")

add(B.section_head("结", "课后任务 · 巩固清单", "任务")
    + B.rule_cards([("qita", "任务一", "抄写 20 个状语从句相关词，各配一句因果句。"),
                    ("bin", "任务二", "完成配套练习卷（阅读30/语言25/综合25/语法诊断20）。"),
                    ("xing", "任务三", "用 because / although / so that 各写 2 句。")])
    + B.quiz_html([("本课核心考点有几个？", "2 个", ["3 个", "5 个"]),
                   ("because 与 so 同时用对吗？", "错", ["对", "看情况"])])
    + B.ext_card("展望", "L25 将转到动名词与不定式，预习 enjoy / finish / decide / plan 等词。"), 8, "课后任务", "巩固清单")

total = p - 1
seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
page_meta = {i: {"p": "CORE", "m": 2} for i in range(1, total + 1)}

js = B.js_extra(total, seg_pages, page_meta)
css = B.CSS_EXTRA
out = os.path.join(out_dir, "第24课时_课件_中等.html")
size = B.write_courseware(24, "第24课时 · 原因·结果·让步状语", pages, NAV, STAGE, css, js, out, session="D24")
print("L24 课件生成：%s (%d bytes, %d pages)" % (out, size, total))