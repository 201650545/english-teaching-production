# -*- coding: utf-8 -*-
"""邓兴华 L26 授课课件（时态三态综合辨析 · 八段式 · ~44 页）生成脚本"""
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
  <div class="nav-item" data-segment="3" onclick="jumpToSegment(3)"><span class="nav-num">③</span>语法考点</div>
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

STAGE = "Stage 6 · L26"

# ================= ① 复习导入（3页） =================
add('<div class="cover-wrap"><div class="cover-badge">Stage 6 · 八上主线</div>'
    '<div class="cover-title">时态三态综合辨析</div>'
    '<div class="cover-sub">G16 一般现在 + G43 频度副词 + G46 现在进行</div>'
    '<div class="cover-tagline">授课课 · 八段式</div>'
    '<div class="cover-info"><div class="cover-info-num"><div class="ci-label">新词</div><div class="ci-val">20</div></div>'
    '<div class="cover-info-num"><div class="ci-label">考点</div><div class="ci-val">3</div></div>'
    '<div class="cover-info-num"><div class="ci-label">词号</div><div class="ci-val">501–520</div></div>'
    '<div class="cover-info-num"><div class="ci-label">时长</div><div class="ci-val">90分</div></div></div>'
    '<div class="cover-emoji">🎯</div></div>', 1, "L26 三态辨析", "八上时态主线")

add(B.section_head("复", "上一课动名词榜样回顾", "L25 衔接")
    + B.rule_cards([("zhug", "L25 考点", "动名词 V-ing 作主语/宾语、不定式 to do 作宾语/目的。"),
                    ("bin", "本课衔接", "L25 讲动词非谓语，L26 转到时态：一般现在/一般过去/现在进行三态辨析。")])
    + B.quiz_html([("enjoy 后接？", "doing", ["to do", "原形"]),
                   ("want 后接？", "to do", ["doing", "原形"])])
    + B.note_panel("L26 起点", "今天的核心是'看标志词判时态'：every day 一般现在，now 进行，yesterday 过去。三态一次分清。"), 1, "复习导入", "L25 衔接")

add(B.section_head("复", "三态 · 前瞻", "新旧衔接")
    + B.rule_cards([("warn", "三态总览", "一般现在（习惯/事实）、一般过去（已发生）、现在进行（正在发生）。"),
                    ("xing", "标志词", "every day/usually → 一般现在；yesterday/last → 过去；now/look/listen → 进行。")])
    + B.quiz_html([("every day 属于？", "一般现在", ["一般过去", "现在进行"]),
                   ("now 属于？", "现在进行", ["一般现在", "一般过去"])])
    + B.sub_label("今天把三态与标志词一次梳理"), 1, "前瞻", "三态概念")

add(B.section_head("复", "本课学习目标", "目标导航")
    + B.note_panel("本课 3 大考点", "① G16 一般现在（非三单+标志词）② G43 频度副词（位置与 How often）③ G46 现在进行（be+V-ing+标志词），并做三态辨析。")
    + B.rule_cards([("qita", "学习动作", "看规则 → 填空自检 → 拖拽分类 → 阅读应用 → 口诀收尾。"),
                    ("ming", "防越级", "不引入完成时（留 L27）、不引入被动（留 L29）。")])
    + B.quiz_html([("本课语法主线是？", "三态辨析", ["被动语态", "定语从句"])])
    + B.ext_card("前后衔接", "L25 动词非谓语收尾，L26 三态综合复习；L27 起进入现在完成时。"), 1, "学习目标", "目标导航")

# ================= ② 新词 20（8页） =================
add(B.section_head("词", "新词① · 时态概念词", "词 501–505")
    + B.vocab_cards([
        ("tense", "/tens/", "n.", "时态", "present/past tense", "Tense tells us when an action happens."),
        ("basic", "/ˈbeɪsɪk/", "adj.", "基本的", "basic knowledge", "English has three basic tenses."),
        ("present", "/ˈpreznt/", "n./adj.", "现在；礼物", "present tense / at present", "We use the present tense for rules."),
        ("past", "/pɑːst/", "n./adj.", "过去", "past tense / in the past", "The past tense shows finished actions."),
        ("continuous", "/kənˈtɪnjʊəs/", "adj.", "进行中的", "present continuous tense", "Now I am reading (continuous).")]), 2, "新词① 时态概念", "词 501–505")

add(B.section_head("词", "新词② · 时态概念词", "词 506–510")
    + B.vocab_cards([
        ("progressive", "/prəˈɡresɪv/", "adj.", "进行的；进步的", "progressive tense", "We also call it the progressive form."),
        ("perfect", "/ˈpɜːfɪkt/", "adj.", "完美的；完成的", "perfect tense", "The perfect tense is for completed actions."),
        ("action", "/ˈækʃn/", "n.", "动作", "take action", "An action verb shows a movement."),
        ("state", "/steɪt/", "n.", "状态", "in a state", "Some verbs describe a state, not an action."),
        ("custom", "/ˈkʌstəm/", "n.", "习惯；风俗", "family custom", "It is a custom to say hello.")]), 2, "新词② 时态概念", "词 506–510")

add(B.section_head("词", "新词③ · 生活名词", "词 511–515")
    + B.vocab_cards([
        ("pattern", "/ˈpætn/", "n.", "模式；图案", "a pattern of", "There is a pattern in these sentences."),
        ("schedule", "/ˈʃedjuːl/", "n.", "日程表", "on schedule", "My schedule is full this week."),
        ("recently", "/ˈriːsntli/", "adv.", "最近", "recently done", "I recently visited my uncle."),
        ("lately", "/ˈleɪtli/", "adv.", "近来", "lately / of late", "Have you seen him lately?"),
        ("currently", "/ˈkʌrəntli/", "adv.", "目前；当前", "currently doing", "She is currently studying abroad.")]), 2, "新词③ 生活名词", "词 511–515")

add(B.section_head("词", "新词④ · 时间副词", "词 516–520")
    + B.vocab_cards([
        ("temporarily", "/ˈtemprərəli/", "adv.", "暂时地", "temporarily closed", "The shop is temporarily closed."),
        ("permanently", "/ˈpɜːmənəntli/", "adv.", "永久地", "permanently live", "They moved permanently to the city."),
        ("suddenly", "/ˈsʌdənli/", "adv.", "突然地", "suddenly appear", "Suddenly, the phone rang."),
        ("gradually", "/ˈɡrædʒuəli/", "adv.", "逐渐地", "gradually change", "The weather gradually got warm."),
        ("eventually", "/ɪˈventʃuəli/", "adv.", "最终；终于", "eventually find", "Eventually, he found the answer.")])
    + B.note_panel("记忆小贴士", "时间副词常提示时态：recently/lately 常带完成或过去，suddenly 常带过去。")
    + B.quiz_html([("'最近' 是？", "recently", ["eventually", "temporarily"]),
                   ("'终于' 是？", "eventually", ["suddenly", "lately"])]), 2, "新词④ 时间副词", "词 516–520")

add(B.section_head("词", "新词游戏① · 词义翻牌", "翻牌自检")
    + B.sub_label("点击翻牌，看英文想中文，再翻回核对")
    + B.flip_grid([
        ("tense", "时态"), ("basic", "基本的"), ("present", "现在"), ("past", "过去"),
        ("custom", "习惯"), ("pattern", "模式"), ("schedule", "日程"), ("recently", "最近"),
        ("suddenly", "突然"), ("gradually", "逐渐"), ("eventually", "最终"), ("lately", "近来")])
    + B.sub_label("自检一题")
    + B.quiz_html([("'时态' 是？", "tense", ["pattern", "custom"])]), 2, "词汇游戏①", "翻牌自检")

add(B.section_head("词", "新词游戏② · 拖拽归位", "拖拽")
    + B.sub_label("把词块拖到正确的解释前面")
    + B.drag_q([("现在 → ", "present", ""), ("过去 → ", "past", ""), ("最近 → ", "recently", "")],
               ["present", "past", "recently"])
    + B.sub_label("自检一题")
    + B.quiz_html([("'突然' 是？", "suddenly", ["gradually", "eventually"])]), 2, "词汇游戏②", "拖拽归位")

add(B.section_head("词", "新词游戏③ · 连线配对", "连线")
    + B.sub_label("把英文词与正确释义连起来")
    + B.match_q([("basic", "基本的"), ("schedule", "日程"), ("custom", "习惯")],
                [("基本的", "basic"), ("日程", "schedule"), ("习惯", "custom")])
    + B.sub_label("左右两列点击配对"), 2, "词汇游戏③", "连线配对")

add(B.section_head("词", "新词游戏④ · 选择演练", "选择")
    + B.sub_label("20 词综合选择")
    + B.quiz_html([("'现在' 是？", "present", ["past", "custom"]),
                   ("'过去' 是？", "past", ["present", "pattern"]),
                   ("'逐渐' 是？", "gradually", ["suddenly", "eventually"]),
                   ("'终于' 是？", "eventually", ["recently", "lately"]),
                   ("'日程' 是？", "schedule", ["custom", "pattern"]),
                   ("'基本的' 是？", "basic", ["perfect", "state"])])
    + B.ext_card("词汇记忆", "时态概念词：tense/present/past/continuous/progressive/perfect；时间副词：recently/lately/suddenly/gradually/eventually。")
    + B.quiz_html([("哪些词表时间频率？", "recently/currently", ["tense/basic", "present/past"]),
                   ("'习惯' 的英文是？", "custom", ["pattern", "schedule"]),
                   ("'暂时地' 是？", "temporarily", ["permanently", "currently"])]), 2, "词汇游戏④", "选择演练")

# ================= ③ 语法考点（10页） =================
add(B.section_head("语", "一般现在时 · 非三单 + 标志词", "G16 规则")
    + B.rule_cards([("zhug", "非三单用原形", "主语我/你/我们/他们时，动词用原形：We play football every day."),
                    ("bin", "标志词", "every day / usually / often / always / sometimes。"),
                    ("warn", "易错", "❌ We plays → ✅ We play（非三单用原形）。")])
    + B.quiz_html([("非三单时动词用？", "原形", ["加s", "加ed"]),
                   ("'We ____ football every day.' 填？", "play", ["plays", "played"]),
                   ("every day 常搭配？", "一般现在", ["过去", "进行"])]), 3, "一般现在", "G16 规则")

add(B.section_head("语", "一般现在时 · 补全填空", "G16 练习")
    + B.fill_q("We ____ (play) football every day.", "play")
    + B.fill_q("I ____ (get) up at six usually.", "get")
    + B.sub_label("点击检查，非三单用原形 + 标志词 every day/usually")
    + B.note_panel("填空一步到位", "看到 every day/usually/often，用一般现在；主语非三单则动词原形，三单则加 s/es。"), 3, "一般现在填空", "G16 练习")

add(B.section_head("语", "频度副词 · 位置与 How often", "G43 规则")
    + B.rule_cards([("zhug", "be 后实义动前", "be + 频度副词；实义动词前用频度副词：He is always happy. / She often walks to school."),
                    ("xing", "How often", "How often 问频率，用 once/twice/three times 答。"),
                    ("warn", "易错", "❌ He goes often to school → ✅ He often goes to school。")])
    + B.quiz_html([("频度副词在实义动词？", "前", ["后", "中间"]),
                   ("How often 问？", "频率", ["地点", "价格"]),
                   ("'He is ____ happy.' 填？", "always", ["goes", "play"])]), 3, "频度副词", "G43 规则")

add(B.section_head("语", "频度副词 · 补全填空", "G43 练习")
    + B.fill_q("How ____ do you exercise? — Three times a week.", "often")
    + B.fill_q("She ____ (often) walks to school.", "often")
    + B.sub_label("点击检查，How often 问频率，频度副词在实义动词前")
    + B.note_panel("填空一步到位", "How often 句首问频率；频度副词 always/usually/often 放在 be 动词后、实义动词前。"), 3, "频度副词填空", "G43 练习")

add(B.section_head("语", "现在进行时 · be + V-ing", "G46 规则")
    + B.rule_cards([("zhug", "结构", "主语 + be + V-ing：She is reading now."),
                    ("bin", "标志词", "now / look / listen / at present。"),
                    ("warn", "易错", "❌ She is read → ✅ She is reading（be + V-ing）。")])
    + B.quiz_html([("现在进行时的结构是？", "be + V-ing", ["动词原形", "动词加ed"]),
                   ("'Listen! Someone is ____.' 填？", "singing", ["sing", "sang"]),
                   ("now 常搭配？", "现在进行", ["一般现在", "过去"])]), 3, "现在进行", "G46 规则")

add(B.section_head("语", "现在进行时 · 补全填空", "G46 练习")
    + B.fill_q("Listen! She ____ (sing) now.", "is singing")
    + B.fill_q("Look! They ____ (play) basketball.", "are playing")
    + B.sub_label("点击检查，Listen!/Look!/now 后用 be + V-ing")
    + B.note_panel("填空一步到位", "看到 now/look/listen，用现在进行时 be + V-ing。注意 be 随主语：I am / he is / they are。"), 3, "现在进行填空", "G46 练习")

add(B.section_head("语", "三态辨析 · 标志词判定", "综合")
    + B.quiz_html([("every day 用？", "一般现在", ["一般过去", "现在进行"]),
                   ("yesterday 用？", "一般过去", ["一般现在", "现在进行"]),
                   ("now 用？", "现在进行", ["一般现在", "一般过去"]),
                   ("usually 用？", "一般现在", ["现在进行", "一般过去"]),
                   ("Listen! 用？", "现在进行", ["一般现在", "一般过去"])])
    + B.note_panel("判定口诀", "看标志词：every day/usually/often → 一般现在；yesterday/last/ago → 过去；now/look/listen → 进行。"), 3, "三态辨析", "标志词判定")

add(B.section_head("语", "三态辨析 · 完形陷阱", "综合")
    + B.body_text("完形陷阱：题目给出易混时间状语，需判断时态。例如 'I ___ (read) books every day.' 应填 read（every day 一般现在）。")
    + B.quiz_html([("'He ____ (watch) TV now.' 填？", "is watching", ["watches", "watched"]),
                   ("'She ____ (visit) her uncle yesterday.' 填？", "visited", ["visits", "is visiting"]),
                   ("'They ____ (play) football every day.' 填？", "play", ["are playing", "played"]),
                   ("'Look! The boy ____ (run).' 填？", "is running", ["runs", "ran"])])
    + B.ext_card("陷阱提示", "完形中时间状语是时态判定的关键：now 用进行、every day 用现在、yesterday 用过去。看清标志词再选。"), 3, "完形陷阱", "三态综合")

add(B.section_head("语", "三态辨析 · 拖拽归类", "应用")
    + B.sub_label("把标志词拖到正确的时态栏下")
    + B.drag_q([("一般现在：", "every day", ""),
                ("一般过去：", "yesterday", ""),
                ("现在进行：", "now", "")],
               ["every day", "yesterday", "now"])
    + B.sub_label("点击检查，标志词归位三态")
    + B.note_panel("归类小结", "一般现在：every day/usually/often/sometimes；过去：yesterday/last/ago；进行：now/look/listen。"), 3, "三态归类", "拖拽")

add(B.section_head("语", "三态 · 关键词地图", "考点梳理")
    + B.kmap_block("三态辨析三大关键词", [
        ("一般现在", "非三单原形 + every day"),
        ("一般过去", "动词过去式 + yesterday"),
        ("现在进行", "be + V-ing + now")])
    + B.sub_label("自检一题")
    + B.quiz_html([("三态由什么区分？", "标志词与动词形式", ["字母数量", "句子长度"]),
                   ("过去时动词用？", "过去式", ["原形", "V-ing"])])
    + B.ext_card("螺旋递进", "三态为 Stage 1-3 已学，L26 系统辨析；L27 起进入现在完成时（G64）。"), 3, "三态地图", "关键词")

# ================= ④ 随堂演练（4页） =================
add(B.section_head("练", "三态 · 选择演练", "单选")
    + B.quiz_html([("I ____ (go) to school every day.", "go", ["goes", "going"]),
                   ("She ____ (watch) TV now.", "is watching", ["watches", "watched"]),
                   ("He ____ (visit) his grandma last week.", "visited", ["visits", "is visiting"]),
                   ("We usually ____ (play) after class.", "play", ["played", "are playing"])])
    + B.note_panel("解题步骤", "①找标志词 ②判时态 ③按规则变形。every day 现在 / last week 过去 / now 进行。"), 6, "随堂演练", "选择")

add(B.section_head("练", "三态 · 填空演练", "填空")
    + B.fill_q("He ____ (read) books every evening.", "reads")
    + B.fill_q("Look! They ____ (swim) in the pool.", "are swimming")
    + B.fill_q("I ____ (finish) my homework yesterday.", "finished")
    + B.sub_label("点击检查"), 6, "随堂演练", "填空")

add(B.section_head("练", "三态 · 拖拽分类", "拖拽")
    + B.sub_label("把动词块拖到正确的时态栏下")
    + B.drag_q([("一般现在：", "play", ""),
                ("过去式：", "played", ""),
                ("进行式：", "playing", "")],
               ["play", "played", "playing"])
    + B.sub_label("点击检查，play/played/playing 对应三态"), 6, "随堂演练", "拖拽")

add(B.section_head("练", "三态 · 综合混练", "综合")
    + B.quiz_html([("I ____ (do) my homework now.", "am doing", ["do", "did"]),
                   ("She ____ (go) to Beijing last year.", "went", ["goes", "is going"]),
                   ("They ____ (read) every morning.", "read", ["are reading", "readed"]),
                   ("Listen! Someone ____ (sing).", "is singing", ["sings", "sang"])])
    + B.sub_label("点击作答，四题全对才算掌握")
    + B.note_panel("综合审题三步", "①找标志词 ②判时态 ③按规则变形。把四题连起来读一遍，验证通顺。")
    + B.body_text("本课综合运用：一般现在用原形/三单，过去用过去式，进行用 be+V-ing。做题先看时间状语。"), 6, "随堂演练", "综合")

# ================= ⑤ 阅读理解（5页） =================
add(B.section_head("读", "阅读 A 篇 · My Busy School Day", "记叙文")
    + B.sub_label("记叙文：我忙碌的学校日（约 194 词）")
    + B.body_text("I have a busy school day. I usually get up at six and go to school at seven. "
                  "In the morning, we have four classes. I often read English aloud. "
                  "At noon, I have lunch with my friends. We are eating in the dining hall now. "
                  "In the afternoon, we play basketball after class. "
                  "Yesterday I visited the library and borrowed three books. "
                  "Now I am doing my homework at home. "
                  "Every evening I review my lessons. "
                  "I always go to bed before ten. My school day is busy but happy.")
    + B.rule_cards([("bin", "主旨", "介绍一天的学校生活，三态时间线（一般现在习惯/过去昨天/进行现在）。")])
    + B.quiz_html([("作者通常几点起床？", "六点", ["七点", "八点"]),
                   ("作者昨天做了什么？", "去了图书馆", ["踢了球", "看了电影"]),
                   ("'are eating' 用的是？", "现在进行", ["一般现在", "过去"]),
                   ("'usually get up' 用的是？", "一般现在", ["现在进行", "过去"])])
    + B.note_panel("信息定位", "按时间线找动词：usually/get up 一般现在；yesterday/visited 过去；now/am doing 进行。逐题回原文定位。")
    + B.fill_q("我通常在六点起床。I usually ____ (get) up at six.", "get")
    + B.quiz_html([("作者现在在哪里？", "在家", ["在学校", "在图书馆"]),
                   ("'always go to bed' 用的是？", "一般现在", ["现在进行", "过去"])]), 7, "阅读 A 篇", "学校日")

add(B.section_head("读", "阅读 B 篇 · A Day in My Life", "记叙文")
    + B.sub_label("记叙文：我的一天（约 215 词）")
    + B.body_text("My name is Li Ming. I am a middle school student. "
                  "I usually get up at 6:30 a.m. After breakfast, I go to school by bike. "
                  "Look! A new library is being built near our school. "
                  "We often have six classes a day. At noon, I am eating with my classmates now. "
                  "Yesterday afternoon, I played football with my friends. "
                  "Now I am doing my homework at home. "
                  "Every evening, I review my lessons and read English. "
                  "I always go to bed at ten o'clock. "
                  "Recently I joined the school reading club. "
                  "My life is busy, but I enjoy every moment.")
    + B.rule_cards([("bin", "人物", "作者李明的日常，三态时间线贯穿全文。")])
    + B.quiz_html([("作者通常几点起床？", "六点半", ["七点", "八点"]),
                   ("昨天下作者做了什么？", "踢足球", ["游泳", "画画"]),
                   ("'am eating' 用的是？", "现在进行", ["一般现在", "过去"]),
                   ("'recently joined' 用的是？", "过去（最近）", ["现在进行", "现在"])])
    + B.fill_q("我昨天踢了足球。I ____ (play) football yesterday.", "played")
    + B.sub_label("点击检查")
    + B.note_panel("记叙文信息定位", "记叙文按时间线推进。逐题回原文找动词与时间状语，判断用三态中的哪一种。")
    + B.quiz_html([("作者现在在做什么？", "做作业", ["踢足球", "睡觉"]),
                   ("'always go to bed' 用的是？", "一般现在", ["现在进行", "过去"])]), 7, "阅读 B 篇", "一天生活")

add(B.section_head("读", "阅读 C 篇 · What Are They Doing Now?", "说明文")
    + B.sub_label("说明文：他们现在在做什么（约 215 词）")
    + B.body_text("It is Sunday afternoon. Look! Many people are doing different things. "
                  "In the park, some children are playing football. A girl is reading a book under a tree. "
                  "Two old men are playing chess. A woman is feeding the birds. "
                  "In the street, a boy is riding his bike. A man is selling ice cream. "
                  "At home, my mom is cooking dinner and my dad is watching TV. "
                  "Usually on Sundays we have a big dinner together. "
                  "Yesterday we visited my grandparents. "
                  "Now everyone is enjoying the weekend. "
                  "What a lively afternoon!")
    + B.rule_cards([("xing", "主旨", "描述周日下午大家正在做的事，以现在进行时为主。")])
    + B.quiz_html([("孩子们正在做什么？", "踢足球", ["游泳", "画画"]),
                   ("那位女士正在做什么？", "喂鸟", ["做饭", "看书"]),
                   ("妈妈正在做什么？", "做饭", ["看电视", "睡觉"]),
                   ("'is playing' 用的是？", "现在进行", ["一般现在", "过去"])])
    + B.note_panel("进行时结构", "本页以现在进行时为主：Look!/now 提示，be + V-ing 描写正在发生的动作。")
    + B.fill_q("男孩正在骑自行车。A boy ____ (ride) his bike.", "is riding")
    + B.quiz_html([("'usually have' 用的是？", "一般现在", ["现在进行", "过去"]),
                   ("昨天我们做了什么？", "看望祖父母", ["踢足球", "购物"])]), 7, "阅读 C 篇", "他们做什么")

add(B.section_head("读", "阅读 · 五选四", "语篇填空")
    + B.sub_label("My Daily Schedule 语篇填空（5 空 4 选）")
    + B.rule_cards([("bin", "提示", "根据上下文逻辑选择正确的句子，注意三态标志词与动词形式。")])
    + B.order_q("把一天的时间安排按正确顺序排列",
                [("Morning", "上午"), ("Afternoon", "下午"), ("Evening", "晚上")],
                "Morning|Afternoon|Evening")
    + B.sub_label("自检一题")
    + B.quiz_html([("五选四中 'every day' 常表示？", "一般现在", ["过去", "进行"])])
    + B.ext_card("衔接词", "时间线类：usually/often/every day；now/look；yesterday/last。"), 7, "阅读五选四", "语篇填空")

add(B.section_head("读", "阅读策略 · 三态定位", "策略")
    + B.kmap_block("三态阅读三步法", [
        ("划时间状语", "every day/now/yesterday"),
        ("判时态", "现在/进行/过去"),
        ("定位", "回原文找对应动词")])
    + B.body_text("阅读三态类文章时，先划时间状语，再判定时态，最后回原文找到对应动词确认。")
    + B.quiz_html([("every day 引导的是？", "一般现在", ["现在进行", "过去"]),
                   ("now 引导的是？", "现在进行", ["一般现在", "过去"])])
    + B.note_panel("常见设问", "What does sb. do every day?（一般现在）/ What is sb. doing now?（进行）/ What did sb. do yesterday?（过去）。"), 7, "阅读策略", "三态定位")

# ================= 句子练习（4页） =================
add(B.section_head("句", "造句 · 一般现在", "句子练习")
    + B.rule_cards([("zhug", "句型", "主语 + 动词原形/三单 + 其他，常带 every day/usually。")])
    + B.fill_q("我每天读书。I ____ (read) books every day.", "read")
    + B.sub_label("点击检查，every day 用一般现在，非三单用原形")
    + B.body_text("参考：<b>I read books every day.</b>（我每天读书。）"
                  "技巧：看到 every day/usually/often 用一般现在。主语三单时动词加 s/es：He reads books every day."), 7, "造句一般现在", "句子练习")

add(B.section_head("句", "汉译英 · 现在进行", "句子练习")
    + B.rule_cards([("zhug", "句型", "主语 + be + V-ing，常带 now/look/listen。")])
    + B.fill_q("看！他在唱歌。Look! He ____ (sing).", "is singing")
    + B.sub_label("点击检查，Look! 后用现在进行")
    + B.body_text("参考：<b>Look! He is singing.</b>（看！他在唱歌。）"
                  "技巧：now/look/listen 提示现在进行 be + V-ing。be 随主语：he is / they are。"), 7, "汉译英进行", "句子练习")

add(B.section_head("句", "汉译英 · 一般过去", "句子练习")
    + B.rule_cards([("zhug", "句型", "主语 + 动词过去式，常带 yesterday/last week。")])
    + B.fill_q("我昨天去了公园。I ____ (go) to the park yesterday.", "went")
    + B.sub_label("点击检查，yesterday 用一般过去")
    + B.body_text("参考：<b>I went to the park yesterday.</b>（我昨天去了公园。）"
                  "技巧：yesterday/last week/ago 用一般过去时，动词用过去式（不规则需记忆：go→went）。"), 7, "汉译英过去", "句子练习")

add(B.section_head("句", "汉译英 · 三态选择", "句子练习")
    + B.rule_cards([("zhug", "句型", "看时间状语选三态：now→进行，every day→现在，yesterday→过去。")])
    + B.fill_q("他通常踢足球。He usually ____ (play) football.", "plays")
    + B.fill_q("他们现在正在踢足球。They ____ (play) football now.", "are playing")
    + B.sub_label("点击检查，时间状语决定时态")
    + B.body_text("参考：<b>He plays football.</b>（一般现在）/ <b>They are playing football now.</b>（进行）。"
                  "技巧：先看时间状语判断时态，再按对应规则变形。"), 7, "三态选择", "句子练习")

# ================= 拼读（5页） =================
add(B.section_head("拼", "音素 · -ed 三种读音", "音素")
    + B.rule_cards([("zhug", "/t/", "清辅音后：walked/talked/liked。"),
                    ("bin", "/d/", "浊辅音后：played/cleaned/lived。"),
                    ("xing", "/ɪd/", "-t/-d 后：wanted/needed/visited。")])
    + B.quiz_html([("walked 的 -ed 读？", "/t/", ["/d/", "/ɪd/"]),
                   ("played 的 -ed 读？", "/d/", ["/t/", "/ɪd/"]),
                   ("wanted 的 -ed 读？", "/ɪd/", ["/t/", "/d/"])])
    + B.note_panel("发音要点", "-ed 三种读音由前面的音决定：清辅音后 /t/，浊辅音后 /d/，-t/-d 后 /ɪd/。读 timed 时注意区分。"), 7, "拼读音素", "-ed")

add(B.section_head("拼", "看词归音 · -ed", "归音")
    + B.order_q("把含 /ɪd/ 的词挑出来（排序成一列）",
                [("wanted", "加一个音"), ("needed", "加一个音"), ("walked", "清/t/")],
                "wanted|needed|walked")
    + B.sub_label("自检一题")
    + B.quiz_html([("visited 读？", "/ɪd/", ["/t/", "/d/"])]), 7, "拼读归音", "-ed 归音")

add(B.section_head("拼", "听音选词 · -ed 读音", "听音")
    + B.quiz_html([("选出 -ed 读 /t/ 的词", "talked", ["played", "wanted"]),
                   ("选出 -ed 读 /d/ 的词", "cleaned", ["asked", "visited"]),
                   ("helped 的 -ed 读？", "/t/", ["/d/", "/ɪd/"])])
    + B.sub_label("点击作答，听音辨形")
    + B.note_panel("听辨提示", "-ed：清音后 /t/，浊音后 /d/，-t/-d 后 /ɪd/。读快了注意尾巴。"), 7, "拼读听音", "听音选词")

add(B.section_head("拼", "最小对立对 · walked vs played", "对立")
    + B.rule_cards([("ming", "最小对立", "walked（/t/）/played（/d/）/wanted（/ɪd/）——注意尾音清浊。")])
    + B.match_q([("walked", "/t/"), ("played", "/d/"), ("wanted", "/ɪd/"), ("visited", "/ɪd/")],
                [("/t/", "walked"), ("/d/", "played"), ("/ɪd/", "wanted"), ("/ɪd/", "visited")])
    + B.sub_label("左右两列点击配对"), 7, "拼读对立", "最小对立对")

add(B.section_head("拼", "时态词尾 · -ed 应用", "拼读应用")
    + B.sub_label("把词块拖到正确读音前")
    + B.drag_q([("/t/ → ", "walked", ""), ("/d/ → ", "lived", ""), ("/ɪd/ → ", "needed", "")],
               ["walked", "lived", "needed"])
    + B.sub_label("点击检查，-ed 三种读音归类")
    + B.note_panel("拼读小结", "-ed 三种读音是过去时与过去分词的共同词尾，读准对听力与拼写都有帮助。"), 7, "拼读应用", "-ed 应用")

# ================= ⑧ 课堂总结（5页） =================
add(B.section_head("结", "核心口诀总览", "一页速览")
    + B.rule_cards([("zhug", "一般现在", "非三单用原形 + every day/usually/often。"),
                    ("xing", "一般过去", "动词过去式 + yesterday/last week/ago。"),
                    ("bin", "现在进行", "be + V-ing + now/look/listen。")])
    + B.quiz_html([("every day 用？", "一般现在", ["过去", "进行"]),
                   ("now 用？", "现在进行", ["一般现在", "过去"]),
                   ("yesterday 用？", "一般过去", ["一般现在", "进行"])])
    + B.body_text("口诀背诵：<b>every day 现在时，yesterday 过去式，now/look 进行态。</b>"
                  "频度副词 always/usually/often 在 be 后实义动前，How often 问频率。"
                  "把口诀读两遍，再用本课 20 词各造一句，本课核心就掌握了大半。")
    + B.quiz_html([("三态区分的核心是？", "标志词与时态标志", ["句子长短", "词数多少"]),
                   ("How often 问？", "频率", ["地点", "时间点"])]), 8, "核心口诀", "一页速览")

add(B.section_head("结", "课堂思维导图", "全课收尾")
    + B.mind_map(26, "时态三态综合辨析", [
        ("一般现在", "非三单原形 + every day"),
        ("一般过去", "过去式 + yesterday"),
        ("现在进行", "be + V-ing + now"),
        ("频度副词", "be后实义动前/How often"),
        ("防越级", "不引入完成时"),
        ("应用", "阅读定位 / 造句 / 拼读")])
    + B.sub_label("本课 3 考点：G16 一般现在 · G43 频度副词 · G46 现在进行")
    + B.note_panel("一句话收口", "every day 现在、yesterday 过去、now 进行。三句口诀一次带走。"), 8, "思维导图", "全课收尾")

add(B.section_head("结", "语法速查 · 三态公式", "速查卡")
    + B.rule_cards([("zhug", "一般现在", "主语 + 动词(原形/三单) + every day/usually/often"),
                    ("xing", "一般过去", "主语 + 动词过去式 + yesterday/last week"),
                    ("bin", "现在进行", "主语 + be + V-ing + now/look/listen"),
                    ("ming", "频度副词", "be 后 / 实义动词前；How often 问频率")])
    + B.sub_label("速查:三态公式与标志词")
    + B.quiz_html([("'usually' 属于？", "频度副词", ["时态", "介词"]),
                   ("三态由标志词区分，对吗？", "对", ["错", "看情况"])]), 8, "语法速查", "速查卡")

add(B.section_head("结", "综合演练 · 三态混练", "综合")
    + B.quiz_html([("I ____ (go) to school every day.", "go", ["goes", "going"]),
                   ("She ____ (watch) TV now.", "is watching", ["watches", "watched"]),
                   ("He ____ (play) football yesterday.", "played", ["plays", "is playing"]),
                   ("We ____ (read) every morning.", "read", ["are reading", "readed"]),
                   ("Listen! The bird ____ (sing).", "is singing", ["sings", "sang"])])
    + B.sub_label("点击作答，三态综合检验")
    + B.note_panel("综合检验", "把五题连起来读，确认每句时态与标志词匹配。错一题回看对应语法卡。"), 8, "综合演练", "三态混练")

add(B.section_head("结", "课后任务 · 巩固清单", "任务")
    + B.rule_cards([("qita", "任务一", "抄写 20 个时态与时间副词相关词，各配一句三态句型。"),
                    ("bin", "任务二", "完成配套练习卷（阅读30/语言25/综合25/语法诊断20）。"),
                    ("xing", "任务三", "用 every day / yesterday / now 各造 2 句。")])
    + B.quiz_html([("本课核心考点有几个？", "3 个", ["2 个", "5 个"]),
                   ("now 用现在进行，对吗？", "对", ["错", "看情况"])])
    + B.ext_card("展望", "L27 将进入现在完成时，预习 have/has + 过去分词。"), 8, "课后任务", "巩固清单")

total = p - 1
seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
page_meta = {i: {"p": "CORE", "m": 2} for i in range(1, total + 1)}

js = B.js_extra(total, seg_pages, page_meta)
css = B.CSS_EXTRA
out = os.path.join(out_dir, "第26课时_课件_中等.html")
size = B.write_courseware(26, "第26课时 · 时态三态综合辨析", pages, NAV, STAGE, css, js, out, session="D26")
print("L26 课件生成：%s (%d bytes, %d pages)" % (out, size, total))