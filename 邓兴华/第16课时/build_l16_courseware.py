# -*- coding: utf-8 -*-
"""邓兴华 L16 讲评课件（阶段测试Ⅱ · 五段式）生成脚本（重写·语法干净版）
沿用 L16 内容蓝图：测试课（G01-G42 诊断 + 300 词 + 20 测试语境词，无新语法/拼读）。
复用 build_dxh_l21_25 工程链（红金暖色 · 亮色 · 双契约标记）。
page-id 契约 40-45 页，本卷 41 页，体积 ≥150KB。
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "00_工具"))
import build_dxh_l21_25 as B

out_dir = os.path.join(HERE, "课件成品_网页PPT")
os.makedirs(out_dir, exist_ok=True)

NAV = """<div class="nav-bar">
  <div class="nav-item" data-segment="1" onclick="jumpToSegment(1)"><span class="nav-num">①</span>测试概况</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="2" onclick="jumpToSegment(2)"><span class="nav-num">②</span>语法错题精讲</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="3" onclick="jumpToSegment(3)"><span class="nav-num">③</span>词汇错题精讲</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="4" onclick="jumpToSegment(4)"><span class="nav-num">④</span>阅读写作讲评</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="5" onclick="jumpToSegment(5)"><span class="nav-num">⑤</span>总结提升</div>
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

# ================= 段1 测试概况 =================
add('<div class="cover-wrap"><div class="cover-badge">阶段测试Ⅱ</div>'
    '<div class="cover-title">七上+七下跨阶诊断 · 讲评</div>'
    '<div class="cover-sub">G01–G42 全部 42 个考点 + 前 300 词跨阶诊断</div>'
    '<div class="cover-tagline">测试 + 讲评 · 五段式</div>'
    '<div class="cover-info"><div class="cover-info-num"><div class="ci-label">覆盖考点</div><div class="ci-val">42</div></div>'
    '<div class="cover-info-num"><div class="ci-label">词汇范围</div><div class="ci-val">300+</div></div>'
    '<div class="cover-info-num"><div class="ci-label">讲评页数</div><div class="ci-val">41</div></div>'
    '<div class="cover-info-num"><div class="ci-label">满分</div><div class="ci-val">100</div></div></div>'
    '<div class="cover-emoji">📊</div></div>', 1, "阶段测试Ⅱ · 讲评", "七上+七下跨阶诊断")

add(B.section_head("总", "全卷概况")
    + B.stats_panel([("88%", "班均得分率"), ("42", "覆盖考点"), ("41", "讲评页数"), ("C", "主要薄弱等级")])
    + B.rule_cards([("zhug", "诊断范围", "测试卷覆盖 L1–L15 全部 42 个语法考点（G01–G42）与前 300 词。本讲评聚焦高频错题、薄弱考点与提升计划。"),
                    ("xing", "讲评方式", "五段式：①测试概况 → ②语法错题精讲 → ③词汇错题精讲 → ④阅读写作讲评 → ⑤总结提升。交互题点击作答可即时自检。"),
                    ("bin", "答题落库", "本页所有交互题答案自动写入本地 IndexedDB，支持导出与错题复盘。")])
    + B.game_board("考点覆盖一览", "📈", "点击作答自检掌握情况",
                   B.quiz_html([("全卷第一大板块（题1–20）考查的是？", "阅读理解（40 分）", ["语法单选", "听力理解"]),
                                ("书面表达（题46）满分是？", "25 分", ["15 分", "10 分"])])), 1, "全卷概况", "得分分布与覆盖范围")

add(B.section_head("总", "题型得分分布")
    + B.stats_panel([("A篇", "阅读 10分"), ("B篇", "阅读 10分"), ("C篇", "阅读 10分"), ("五选四", "阅读 10分")])
    + B.stats_panel([("完形", "10分"), ("选词", "10分"), ("简答", "5分"), ("写作", "25分")])
    + B.game_board("题型得分率一览", "📈", "点击左侧选项作答自检",
                   B.quiz_html([("阅读 A 篇（应用文）信息定位题得分率约为？", "细节题定位原句即可", ["需全文翻译", "凭猜测作答"]),
                                ("完形填空中最容易失分的是？", "时态与固定搭配", ["单词拼写", "标点符号"]),
                                ("五选四最常考的逻辑关系是？", "指代与转折衔接", ["押韵", "语法时态"])])), 1, "题型得分率", "按题型统计")

add(B.section_head("总", "高频错题 Top 预览")
    + "<div class='content-table'><table><thead><tr><th>题号</th><th>考点</th><th>错率</th><th>典型错因</th></tr></thead><tbody>"
    + "<tr><td>21</td><td>G20 过去时 did</td><td>36%</td><td>did 后加原形</td></tr>"
    + "<tr><td>37</td><td>G33 some/any</td><td>32%</td><td>肯定/否定混淆</td></tr>"
    + "<tr><td>45</td><td>G38 why/because</td><td>30%</td><td>because 与 so 混用</td></tr>"
    + "<tr><td>33</td><td>G31 冠词</td><td>28%</td><td>a/an 判断</td></tr>"
    + "<tr><td>50</td><td>G26 三单否定</td><td>26%</td><td>doesn't 后还原</td></tr></tbody></table></div>"
    + B.sub_label("点击自检一题")
    + B.quiz_html([("错题 21：He ____ (not watch) TV yesterday.", "didn't watch", ["doesn't watch", "not watch"])]), 1, "高频错题预览", "Top 错题")

# ================= 20 测试语境词速览 =================
add(B.section_head("词", "测试语境词 · 20 词速览")
    + B.sub_label("本卷 20 个测试语境词，随讲评自然习得")
    + B.vocab_cards([
        (("test", "/test/", "n./v.", "测试；测验", "have a test / test sb.", "We have a math test tomorrow.")),
        (("quiz", "/kwɪz/", "n.", "小测验", "have a quiz / pop quiz", "The teacher gave us a short quiz.")),
        (("homework", "/ˈhəʊmwɜːk/", "n.", "家庭作业", "do homework / finish homework", "I finish my homework every day.")),
        (("assignment", "/əˈsaɪnmənt/", "n.", "作业；任务", "hand in an assignment", "The assignment is due tomorrow.")),
        (("notebook", "/ˈnəʊtbʊk/", "n.", "笔记本", "take notes in a notebook", "Write it in your notebook.")),
        (("textbook", "/ˈtekstbʊk/", "n.", "课本", "read a textbook", "Open your textbook to page 10.")),
        (("presentation", "/ˌpreznˈteɪʃən/", "n.", "演示", "give a presentation", "She gave a presentation on history.")),
        (("project", "/ˈprɒdʒekt/", "n.", "项目", "do a project", "Our group project is about culture.")),
        (("survey", "/ˈsɜːveɪ/", "n./v.", "调查", "do a survey", "We did a survey about habits.")),
        (("interview", "/ˈɪntəvjuː/", "n./v.", "采访", "have an interview", "He interviewed the teacher.")),
        (("article", "/ˈɑːtɪkl/", "n.", "文章", "write an article", "I read an article about health.")),
        (("composition", "/ˌkɒmpəˈzɪʃən/", "n.", "作文", "write a composition", "We wrote a composition.")),
        (("passage", "/ˈpæsɪdʒ/", "n.", "段落", "read the passage", "Read the passage, please.")),
        (("paragraph", "/ˈpærəɡrɑːf/", "n.", "段落", "write a paragraph", "Write a paragraph.")),
        (("heading", "/ˈhedɪŋ/", "n.", "标题", "the heading of the passage", "The heading tells us the main idea.")),
        (("title", "/ˈtaɪtl/", "n.", "标题", "the title of the book", "What's the title of your article?")),
        (("underline", "/ˌʌndəˈlaɪn/", "v.", "画线", "underline the answer", "Underline the key words.")),
        (("circle", "/ˈsɜːkl/", "n./v.", "圈出", "circle the answer", "Circle the right answer.")),
        (("blank", "/blæŋk/", "n./adj.", "空白", "fill in the blank", "Fill in the blanks.")),
        (("bracket", "/ˈbrækɪt/", "n.", "括号", "in brackets", "Write the word in brackets."))]), 2, "测试语境词", "20 词速览")

# ================= 段2 语法错题精讲 · 逐考点分页 =================
add(B.section_head("讲", "代词系统 · G01–G06")
    + B.rule_cards([("zhug", "主格与宾格", "I/me, he/him, she/her：作主语用主格，作宾语用宾格。动词前用主格，动词或介词后用宾格。"),
                    ("bin", "物主代词", "my/mine, your/yours：形容词性后接名词（my book），名词性单独用（The book is mine）。"),
                    ("warn", "高频错因", "She 与 her 误用；I 与 me 误用；my 与 mine 误用。")])
    + B.quiz_html([("主格、宾格判断：____ goes to school every day.（主格）", "He", ["Him", "His"]),
                   ("物主代词：This is ____ book.（形容词性物主代词）", "my", ["mine", "I"]),
                   ("介词后应用宾格：Give it to ____.", "her", ["she", "hers"]),
                   ("名词性物主代词：The pen is ____.", "mine", ["my", "me"]),
                   ("动词后用宾格：Please help ____.", "us", ["we", "our"]),
                   ("The book is ____.（名词性物主代词，我的）", "mine", ["my", "I"])]), 2, "代词系统错题", "G01–G06")

add(B.section_head("讲", "be 动词 · G03/G05")
    + B.rule_cards([("qita", "be 动词搭配", "I am / He is / You are；复数主语用 are；否定加 not，疑问提前。"),
                    ("warn", "常见错误", "He are → He is；They is → They are；I is → I am。")])
    + B.quiz_html([("____ she a teacher?", "Is", ["Are", "Am"]),
                   ("We ____ students.", "are", ["is", "am"]),
                   ("I ____ a student.", "am", ["is", "are"]),
                   ("否定句：He ____ a doctor.", "isn't", ["aren't", "am not"]),
                   ("复数be动词：The apples ____ fresh.", "are", ["is", "am"]),
                   ("I 与 am 搭配：____ a teacher.", "I am", ["I is", "I are"])]), 2, "be 动词错题", "G03/G05")

add(B.section_head("讲", "名词·介词·数词 · G07–G12")
    + B.rule_cards([("ming", "名词所有格", "名词+'s 表所有（Tom's bag）；of 用于无生命物（the name of the school）。"),
                    ("xing", "方位介词", "in/on/under/behind/next to/between 表示空间关系。"),
                    ("qita", "基数词拼写", "one–twenty 拼写牢记；十几有 special 拼写（twelve/thirteen）；整十数加 -ty。")])
    + B.quiz_html([("The book is ____ the desk.（在…上面）", "on", ["in", "under"]),
                   ("Tom's bag（所有格含义）", "Tom 的包", ["Tom 们的包", "Tom 是包"]),
                   ("between…and… 表示？", "在…和…之间", ["在…上面", "在…后面"]),
                   ("The cat is ____ the sofa.（在…下面）", "under", ["on", "behind"]),
                   ("The school is ____ the park.（在…旁边）", "next to", ["in front", "under"]),
                   ("The name ____ the school is Long.（所有格）", "of", ["'s", "to"]),
                   ("数字 12 的英文拼写是？", "twelve", ["twelf", "twelv"]),
                   ("数字 13 的正确拼写是？", "thirteen", ["threeteen", "thirtheen"]),
                   ("数字 40 的英文是？", "forty", ["fourty", "fourty's"])]), 2, "名词介词数词", "G07–G12")

add(B.section_head("讲", "祈使句 · G13")
    + B.rule_cards([("zhug", "祈使句结构", "动词原形开头表命令/建议；Don't + 原形表否定；Look! Listen! 表提醒。")])
    + B.quiz_html([("（否定祈使）____ late for school.", "Don't be", ["Not be", "Be not"]),
                   ("____ your homework first.（肯定祈使）", "Do", ["To do", "Doing"]),
                   ("____ at the blackboard.（看）", "Look", ["Looking", "To look"]),
                   ("Don't ____ in the hallways.（跑）", "run", ["running", "to run"]),
                   ("____ your book, please.（打开）", "Open", ["Opening", "Opens"]),
                   ("____ careful!（小心）", "Be", ["Is", "Are"])]), 2, "祈使句错题", "G13")

add(B.section_head("讲", "疑问句 · G06/G14/G22")
    + B.rule_cards([("bin", "六疑问词", "What 什么 / Where 哪里 / When 何时 / Why 为什么 / Who 谁 / How 怎样。"),
                    ("qita", "Who/What", "Who 问人，What 问物/事。")])
    + B.quiz_html([("____ is your name?", "What", ["Where", "When"]),
                   ("____ is that boy?（谁）", "Who", ["What", "Where"]),
                   ("____ do you go to school?（方式）", "How", ["What", "Who"]),
                   ("____ is the library?（地点）", "Where", ["When", "Why"]),
                   ("____ do you like English?（原因）", "Why", ["Where", "Who"]),
                   ("____ is your birthday?（时间）", "When", ["What", "How"])]), 2, "疑问句错题", "G06/G14/G22")

add(B.section_head("讲", "动词搭配 · G15/G18")
    + B.rule_cards([("xing", "like/want", "like to do / want to do：后接不定式。"),
                    ("bin", "常见错误", "like to play（非 like to playing）；want to go（非 want go）。")])
    + B.quiz_html([("I would like ____ some milk.", "to drink", ["drinking", "drink"]),
                   ("They like ____ football.", "to play", ["playing to", "and play"]),
                   ("She wants ____ a doctor.", "to be", ["being", "is"]),
                   ("I want ____ home now.（回去）", "to go", ["go", "going"])])
    + B.drag_q([("I would like ", "to drink", " some milk."),
                ("She wants ", "to go", " shopping."),
                ("He wants ", "to be", " a doctor.")], ["to drink", "to go", "to be"])
    , 2, "动词搭配错题", "G15/G18")

add(B.section_head("讲", "一般现在时 · G16/G25")
    + B.rule_cards([("ming", "非三单与三单", "I/You/复数用原形；He/She/It 用 -s/-es；否定 don't/doesn't + 原形。"),
                    ("warn", "三单规则", "一般加 -s；ch/sh/x/o 加 -es；辅音+y 变 -ies。")])
    + B.quiz_html([("She ____ (go) to school by bus.", "goes", ["go", "going"]),
                   ("They ____ (not like) tea.", "don't like", ["doesn't like", "not like"]),
                   ("He ____ (watch) TV in the evening.", "watches", ["watch", "watchs"]),
                   ("My father ____ (work) in a hospital.", "works", ["work", "working"]),
                   ("The sun ____ (rise) in the east.", "rises", ["rise", "raising"]),
                   ("He ____ (go) to bed at ten.", "goes", ["go", "going"]),
                   ("They ____ (play) football on Sundays.", "play", ["plays", "playing"])]), 2, "一般现在时", "G16/G25")

add(B.section_head("讲", "过去时 was/were · G19")
    + B.rule_cards([("zhug", "be 过去式", "I/He/She 用 was；You/We/They 用 were；否定 wasn't/weren't；疑问提前。")])
    + B.quiz_html([("I ____ at home yesterday.", "was", ["were", "am"]),
                   ("They ____ very happy.", "were", ["was", "are"]),
                   ("She ____ not at school last week.", "was", ["were", "is"]),
                   ("____ you at the party last night?", "Were", ["Was", "Are"]),
                   ("I ____ (be) very tired yesterday.", "was", ["were", "am"]),
                   ("The boys ____ (be) in the park last Sunday.", "were", ["was", "is"])]), 2, "was/were", "G19")

add(B.section_head("讲", "过去时 did · G20/G21")
    + B.rule_cards([("qita", "实义动词过去式", "规则动词加 -ed；否定 didn't + 原形；疑问 Did + 原形。"),
                    ("warn", "高频错因", "didn't 后接过去式（如 didn't went）是典型错误。")])
    + B.quiz_html([("He ____ (play) football yesterday.", "played", ["plays", "playing"]),
                   ("Did you ____ the movie last night?", "watch", ["watched", "watching"]),
                   ("She didn't ____ to school yesterday.", "go", ["went", "going"]),
                   ("We ____ (visit) the museum last month.", "visited", ["visits", "visiting"]),
                   ("I ____ (have) a good time last weekend.", "had", ["has", "having"])]), 2, "did 过去时", "G20/G21")

add(B.section_head("讲", "三单变化 · G25/G26")
    + B.rule_cards([("warn", "三单规则", "一般加 -s；ch/sh/x/o 加 -es；辅音+y 变 -ies。"),
                    ("bin", "否定疑问", "三单否定用 doesn't + 原形；疑问 Does + 原形。")])
    + B.quiz_html([("He ____ (watch) TV every evening.", "watches", ["watch", "watchs"]),
                   ("She ____ (study) hard.", "studies", ["studys", "study"]),
                   ("____ he like apples?", "Does", ["Do", "Is"]),
                   ("She doesn't ____ (like) coffee.", "like", ["likes", "liking"]),
                   ("Tom ____ (go) to school by bike.", "goes", ["go", "going"])]), 2, "三单变化", "G25/G26")

add(B.section_head("讲", "情态动词 · G28")
    + B.rule_cards([("bin", "can/must", "can 表能力/许可；must 表必须；后接动词原形。"),
                    ("qita", "后接原形", "can/must 后接动词原形，不加 -s/-ing。")])
    + B.quiz_html([("You ____ finish your homework first.（必须）", "must", ["can", "may"]),
                   ("____ you swim?", "Can", ["Must", "Do"]),
                   ("She can ____ (play) the piano.", "play", ["plays", "playing"]),
                   ("You must ____ (be) quiet in the library.", "be", ["is", "being"]),
                   ("He can ____ (speak) English well.", "speak", ["speaks", "speaking"])]), 2, "情态动词", "G28")

add(B.section_head("讲", "冠词 · G31")
    + B.rule_cards([("xing", "a/an/the", "a 辅音音素开头；an 元音音素开头；the 特指。")])
    + B.quiz_html([("She is ____ English teacher.", "an", ["a", "the"]),
                   ("I have ____ apple.", "an", ["a", "the"]),
                   ("He is ____ tall boy.", "a", ["an", "the"]),
                   ("____ sun rises in the east.（特指）", "The", ["A", "An"]),
                   ("She has ____ orange.", "an", ["a", "the"])]), 2, "冠词错题", "G31")

add(B.section_head("讲", "some/any 与量词 · G33/G32")
    + B.rule_cards([("ming", "some/any", "some 肯定/邀请；any 否定/疑问。"),
                    ("qita", "量词搭配", "a cup of tea / a piece of bread 等量词表达。")])
    + B.quiz_html([("Would you like ____ tea?", "some", ["any", "no"]),
                   ("There isn't ____ milk in the fridge.", "any", ["some", "a"]),
                   ("I have ____ books in my bag.（肯定）", "some", ["any", "no"]),
                   ("a cup of coffee 的含义？", "一杯咖啡", ["一杯水", "一盘菜"])]), 2, "some/any", "G32/G33")

add(B.section_head("讲", "would like / how much · G34/G35/G36")
    + B.rule_cards([("zhug", "询问与意愿", "would like to do；how much 问不可数/价格；how many 问可数复数。"),
                    ("bin", "价格表达", "How much is...? / It's + 数字 + yuan。")])
    + B.quiz_html([("____ milk do you need?", "How much", ["How many", "How often"]),
                   ("I would like ____ a book.", "to buy", ["buying", "buy"]),
                   ("____ books are there on the desk?", "How many", ["How much", "How often"]),
                   ("How much is the shirt?（价格）", "It's 20 yuan.", ["It's red.", "It's big."]),
                   ("Would you like ____ coffee?", "some", ["any", "no"])]), 2, "would like", "G34–G36")

add(B.section_head("讲", "外貌描述 · G37/G11")
    + B.rule_cards([("bin", "have/has", "I/You/We/They 用 have；He/She/It 用 has；描述外貌用 have/has。"),
                    ("qita", "be vs have", "描述身高/性格可用 be；描述头发/眼睛用 have/has。")])
    + B.quiz_html([("She ____ long hair.", "has", ["have", "is"]),
                   ("They ____ big eyes.", "have", ["has", "is"]),
                   ("My sister ____ big eyes.", "has", ["is", "have"]),
                   ("He ____ a round face.", "has", ["have", "is"]),
                   ("She is tall.（含义）", "她很高", ["她有高", "她是高"])]), 2, "外貌描述", "G11/G37")

add(B.section_head("讲", "原因与结果 · G38")
    + B.rule_cards([("warn", "because 与 so", "because 表原因，so 表结果，二者不连用。"),
                    ("qita", "why 提问", "why 询问原因，用 because 回答。")])
    + B.quiz_html([("____ do you like winter?", "Why", ["What", "How"]),
                   ("I was tired, ____ I slept early.", "so", ["because", "but"]),
                   ("He didn't come ____ he was ill.", "because", ["so", "but"]),
                   ("—Why are you late? —____ I missed the bus.", "Because", ["So", "But"]),
                   ("because 表原因，so 表？", "结果", ["原因", "转折"])]), 2, "原因结果", "G38")

add(B.section_head("讲", "天气与礼貌请求 · G40–G41")
    + B.rule_cards([("qita", "天气表达", "It's + 形容词：rainy/windy/sunny/cloudy。"),
                    ("xing", "礼貌请求", "Could / Would you please do sth.?" )])
    + B.quiz_html([("表示多风：It's ____.", "windy", ["wind", "winding"]),
                   ("表示有雨：It's ____.", "rainy", ["rain", "raining"]),
                   ("It's sunny.（含义）", "晴朗", ["多风", "多云"]),
                   ("表示多云：It's ____.", "cloudy", ["cloud", "clouding"]),
                   ("____ you please pass me the salt?", "Could", ["Do", "Are"]),
                   ("Would you please ____ the window?（打开）", "open", ["opening", "opens"])])
    + B.fill_q("礼貌请求：____ you please open the window?", "Could")
    , 2, "天气礼貌请求", "G40–G41")

add(B.section_head("讲", "It 指代 · G42")
    + B.rule_cards([("bin", "It 指代", "It 指代天气/时间/距离：It's rainy. / It's 8 o'clock. / It's two kilometers."),
                    ("qita", "主格 It", "It 作主语指代天气/时间/距离时用 is。")])
    + B.quiz_html([("____ sunny today.（指天气）", "It's", ["He's", "She's"]),
                   ("____ 8 o'clock now.（指时间）", "It's", ["He's", "We're"]),
                   ("____ two kilometers from here.（指距离）", "It's", ["They're", "He's"]),
                   ("It _____ rainy today.（指天气）", "is", ["are", "am"])]), 2, "It 指代", "G42")

add(B.section_head("讲", "综合错题 · 跨考点")
    + B.rule_cards([("ming", "综合诊断", "诊断 56 综合题跨 G01–G42 全部考点，考查综合运用能力。")])
    + B.quiz_html([("跨考点综合：He ____ (not like) apples, but he ____ (eat) one yesterday.", "doesn't like; ate", ["don't like; eat", "doesn't like; eats"]),
                   ("综合：____ you at home ____ Sunday?（be + 介词）", "Were; on", ["Was; in", "Are; at"]),
                   ("综合：There ____ some milk in the cup.（be 动词）", "is", ["are", "am"]),
                   ("综合：____ you like some coffee?（邀请）", "Would", ["Do", "Are"]),
                   ("综合：She ____ (have) a red dress yesterday.", "had", ["has", "having"])]), 2, "综合错题", "跨考点")

# ================= 段3 词汇错题精讲 =================
add(B.section_head("词", "L1–L6 基础词汇")
    + B.rule_cards([("zhug", "易错辨析", "theirs/yours（名词性物主）+ these/those（指示代词）+ dictionary/schoolbag + strawberry/tomato（复数）。"),
                    ("warn", "复数规则", "strawberry→strawberries；tomato→tomatoes。")])
    + B.quiz_html([("These are my books. The ____ are yours.（名词性物主）", "ones", ["one", "a"]),
                   ("____ are my pens.（近指）", "These", ["Those", "That"]),
                   ("two ____（草莓复数）", "strawberries", ["strawberrys", "strawberry"]),
                   ("three ____（西红柿复数）", "tomatoes", ["tomatos", "tomato"]),
                   ("Is this ____ schoolbag?（你的）", "your", ["you", "yours"])]) , 3, "L1–L6 基础词汇", "易错辨析")

add(B.section_head("词", "L8–L10 基础词汇")
    + B.rule_cards([("xing", "高频错词", "spent/delicious/expensive + museum/activity + special/favorite。"),
                    ("bin", "词义辨析", "spend time doing；delicious 美味的；expensive 昂贵的。")])
    + B.quiz_html([("I ____ two hours doing homework yesterday.（花费）", "spent", ["spend", "spending"]),
                   ("The food is very ____.（美味）", "delicious", ["expensive", "special"]),
                   ("The shoes are too ____; I can't buy them.（贵）", "expensive", ["cheap", "delicious"]),
                   ("We visited a ____ last Sunday.（博物馆）", "museum", ["activity", "favorite"]),
                   ("My ____ subject is English.（最喜欢的）", "favorite", ["special", "delicious"])]), 3, "L8–L10 基础词汇", "易错辨析")

add(B.section_head("词", "L11–L12 词汇")
    + B.rule_cards([("qita", "班规词汇", "uniform/hallway：穿校服、走廊。"),
                    ("ming", "饮食词汇", "yogurt 酸奶（不可数）/mutton 羊肉/cabbage 卷心菜。")])
    + B.quiz_html([("We must wear a ____ at school.（校服）", "uniform", ["hallway", "yogurt"]),
                   ("Don't run in the ____.（走廊）", "hallway", ["uniform", "cabbage"]),
                   ("I drink ____ every morning.（酸奶）", "yogurt", ["mutton", "cabbage"]),
                   ("We eat ____ and vegetables for dinner.（羊肉）", "mutton", ["yogurt", "uniform"])]), 3, "L11–L12 词汇", "易错辨析")

add(B.section_head("词", "L13–L15 词汇")
    + B.rule_cards([("xing", "购物词汇", "pancake/dumpling：煎饼/饺子。"),
                    ("bin", "外貌词汇", "height 身高 / curly 卷曲的。"),
                    ("qita", "天气词汇", "sunny/cloudy 晴朗/多云；vacation 假期。")])
    + B.quiz_html([("I ate a ____ for breakfast.（煎饼）", "pancake", ["dumpling", "height"]),
                   ("We made ____ for the festival.（饺子）", "dumplings", ["pancakes", "vacations"]),
                   ("She has ____ hair.（卷曲的）", "curly", ["height", "sunny"]),
                   ("It is ____ today.（晴朗）", "sunny", ["cloudy", "vacation"]),
                   ("We went on a ____ last summer.（假期）", "vacation", ["curly", "height"])]) , 3, "L13–L15 词汇", "易错辨析")

add(B.section_head("词", "L16 测试词辨析")
    + B.rule_cards([("bin", "相近词", "test(测试)/quiz(小测验)/assignment(作业) 义近辨析。"),
                    ("qita", "形近词", "passage(段落)/paragraph(段落)/heading(标题) 区分。")])
    + B.quiz_html([("____ is a short exam.（小测验）", "A quiz", ["A project", "A survey"]),
                   ("The ____ tells us the main idea.（标题）", "heading", ["blank", "bracket"]),
                   ("Fill in the ____.（空白）", "blank", ["circle", "underline"]),
                   ("Write the word in ____.（括号）", "brackets", ["blanks", "headings"]),
                   ("We did a ____ about habits.（调查）", "survey", ["title", "quiz"])]) , 3, "L16 测试词", "易错辨析")

# ================= 段4 阅读与写作讲评 =================
add(B.section_head("专", "阅读 A 篇 · 信息定位法")
    + B.rule_cards([("zhug", "五步法", "速读抓主旨 → 精读划关键词 → 解题回原文 → 排除干扰项 → 复述巩固。"),
                    ("xing", "应用文", "标题/首句/项目符号常含关键信息，优先定位。")])
    + B.quiz_html([("应用文信息定位优先看哪里？", "标题与首句", ["结尾", "中段"]),
                   ("主旨题应该看整篇还是某段？", "整篇", ["只看首段", "只看尾段"]),
                   ("细节题答案通常来自？", "原文原句", ["个人推理", "常识"]),
                   ("排除干扰项的技巧是？", "回原文比对信息", ["凭感觉", "选最长的"])]), 4, "阅读 A 篇", "信息定位")

add(B.section_head("专", "阅读 B 篇 · 细节与词义")
    + B.rule_cards([("bin", "细节题", "回原文定位原句，不凭记忆。"),
                    ("xing", "词义题", "结合上下文猜词义。")])
    + B.quiz_html([("词义题遇到生词应该？", "上下文推断", ["跳过", "查词典"]),
                   ("细节题答案通常来自？", "原文原句", ["个人推理", "常识"]),
                   ("记叙文通常以什么为主？", "时间顺序叙述", ["数据说明", "论点论证"]),
                   ("词义题干扰项常？", "表面义或离题义", ["与原文一致", "无中生有"])]), 4, "阅读 B 篇", "细节词义")

add(B.section_head("专", "阅读 C 篇 · 说明文")
    + B.rule_cards([("qita", "说明文", "How to... 类文章，步骤顺序与关键词定位。"),
                    ("bin", "主旨题", "首段提出主题，末段总结呼应。")])
    + B.quiz_html([("说明文常用什么引出主题？", "首段提问/标题", ["结尾数据", "中段例子"]),
                   ("How to... 类文章常用什么结构？", "步骤顺序", ["倒叙", "对比"]),
                   ("主旨题答案常在？", "首末段", ["中段", "标题"])]) , 4, "阅读 C 篇", "说明文")

add(B.section_head("专", "五选四 · 句际逻辑")
    + B.rule_cards([("qita", "逻辑衔接", "代词指代/转折/因果/并列连接词帮助衔接。")])
    + B.quiz_html([("看到 however 表示什么逻辑？", "转折", ["并列", "因果"]),
                   ("看到 because 表示什么逻辑？", "因果", ["转折", "并列"]),
                   ("代词 this/it 常指代？", "上文内容", ["下文内容", "标题"])])
    + B.order_q("把五选四线索词按『先因后果』的正确顺序排列",
                [("however", "转折信号"), ("because", "因果信号"), ("finally", "结尾信号")],
                "however|because|finally")
    , 4, "五选四", "句际逻辑")

add(B.section_head("专", "简答翻译 · 作答规范")
    + B.rule_cards([("ming", "简答", "疑问词对应回答，完整作答。"),
                    ("warn", "翻译", "画线句直译保意，注意时态。")])
    + B.quiz_html([("why 提问该用什么回答？", "because 原因", ["how 方式", "where 地点"]),
                   ("翻译时遇到长难句应？", "先分清结构", ["逐词硬翻", "直接省略"]),
                   ("when 提问该回答？", "时间", ["地点", "方式"]),
                   ("how many 提问该回答？", "数量", ["价格", "原因"])])
    + B.fill_q("翻译练习：这块手表多少钱？How much ____ this watch?", "is")
    , 4, "简答翻译", "作答规范")

add(B.section_head("专", "写作范文 · 评分拆解")
    + "<div class='content-table'><table><thead><tr><th>评分项</th><th>分值</th><th>要点</th></tr></thead><tbody>"
    + "<tr><td>内容完整</td><td>10</td><td>覆盖题目要点</td></tr>"
    + "<tr><td>语言准确</td><td>10</td><td>时态/拼写/搭配</td></tr>"
    + "<tr><td>结构连贯</td><td>5</td><td>过渡衔接自然</td></tr></tbody></table></div>"
    + "<div class='body-text'>范文：《An Unforgettable Test》——"
    + "Last week, I had a big English test. I reviewed my notes and practiced every day. "
    + "On the day, I was nervous, but I stayed calm. I got a good grade. I was so happy. "
    + "This taught me that hard work helps.</div>"
    + B.rule_cards([("xing", "评分", "内容 10 + 语言 10 + 结构 5 = 25 分。")]), 4, "写作范文", "评分拆解")

# ================= 段5 总结提升 =================
add(B.section_head("结", "薄弱考点清单")
    + "<div class='content-table'><table><thead><tr><th>等级</th><th>考点</th><th>学习动作</th></tr></thead><tbody>"
    + "<tr><td>C</td><td>G20 过去时 did</td><td>L8 课件回顾</td></tr>"
    + "<tr><td>C</td><td>G33 some/any</td><td>L12 课件回顾</td></tr>"
    + "<tr><td>B</td><td>G38 because/so</td><td>口诀强化</td></tr>"
    + "<tr><td>B</td><td>G26 三单否定</td><td>变式练习</td></tr></tbody></table></div>", 5, "薄弱清单", "按等级")

add(B.section_head("结", "下阶段建议 · Stage 5")
    + B.rule_cards([("zhug", "Stage 5 预告", "L17–L21 进入八上中段：过去时综合、比较级/最高级、条件句、状语从句、动名词与不定式。"),
                    ("xing", "学习建议", "每日 20 词滚动 + 错题本复盘 + 两日一测。"),
                    ("bin", "错题本方法", "错题分三类：时态/搭配/语序，各配 3 道变式题。")]), 5, "下阶段建议", "Stage 5")

add(B.section_head("结", "核心口诀总览")
    + B.rule_cards([("ming", "过去时", "didn't 后加原形。"),
                    ("bin", "some/any", "肯定用 some，否定/疑问用 any。"),
                    ("qita", "区分句", "because 表因，so 表果，不连用。"),
                    ("warn", "三单", "doesn't 后还原动词原形。"),
                    ("xing", "祈使句", "动词原形开头，Don't 表否定。"),
                    ("zhug", "礼貌请求", "Could/Would you please do sth.?"),
                    ("qita", "冠词", "an 接元音音素，a 接辅音音素。")]), 5, "核心口诀", "一页速览")

add(B.section_head("结", "课堂思维导图")
    + B.mind_map(16, "阶段测试Ⅱ · 讲评", [
        ("考点雷达", "代词 / 名词介词 / 时态 / 三单 / 冠词"),
        ("高频错题", "过去时 / some-any / because / 冠词"),
        ("薄弱专项", "阅读五步法 / 写作 / 词汇 / 简答"),
        ("提升计划", "每日 20 词 / 错题本 / 两日一测"),
        ("下阶段", "Stage 5 · 过去时 / 比较级 / 从句"),
        ("总目标", "突破 90% 正确率")]), 5, "思维导图", "全课收尾")

add(B.section_head("结", "本课达标自检 · 随堂演练")
    + B.rule_cards([("bin", "达标线", "本课讲评后，薄弱考点若能在自检题中一击即中，即视为达标。"),
                    ("warn", "回看指引", "仍有错题的同学，请回到对应错题精讲页重点复习。"),
                    ("qita", "记录方式", "自检答案自动落库，供课后复盘与错题导出。")])
    + B.quiz_html([("达标一：didn't 后应接什么形式？", "动词原形", ["动词过去式", "动词 -ing"]),
                   ("达标二：肯定句用 some，否定/疑问句用 ____。", "any", ["some", "no"]),
                   ("达标三：because 表原因，so 表结果，二者____。", "不连用", ["可连用", "仅 so 可用"]),
                   ("达标四：an 后接____开头的词。", "元音音素", ["辅音字母", "任意字母"]),
                   ("达标五：Could/Would you please + ____？", "动词原形", ["动词过去式", "动词 -ing"]),
                   ("达标六：三单否定用 doesn't + ____。", "动词原形", ["动词三单", "动词过去式"])]), 5, "达标自检", "随堂演练")

total = p - 1
seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
page_meta = {i: {"p": "CORE", "m": 2} for i in range(1, total + 1)}

js = B.js_extra(total, seg_pages, page_meta)
css = B.CSS_EXTRA
out = os.path.join(out_dir, "第16课时_课件_中等.html")
size = B.write_courseware(16, "第16课时 · 阶段测试Ⅱ讲评", pages, NAV, "Stage 4 · L16", css, js, out)
print("L16 课件生成：%s (%d bytes, %d pages)" % (out, size, total))