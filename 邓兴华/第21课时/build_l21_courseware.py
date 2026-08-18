# -*- coding: utf-8 -*-
"""邓兴华 L21 讲评课件（阶段测试Ⅲ · 五段式）生成脚本（重写·语法干净版）"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "00_工具"))
import build_dxh_l21_25 as B

out_dir = os.path.join(HERE, "课件成品_网页PPT")
os.makedirs(out_dir, exist_ok=True)

NAV = """<div class="nav-bar">
  <div class="nav-item" data-segment="1" onclick="jumpToSegment(1)"><span class="nav-num">①</span>测试概况</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="2" onclick="jumpToSegment(2)"><span class="nav-num">②</span>高频错题精讲</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="3" onclick="jumpToSegment(3)"><span class="nav-num">③</span>考点雷达</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="4" onclick="jumpToSegment(4)"><span class="nav-num">④</span>薄弱专项</div>
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
add('<div class="cover-wrap"><div class="cover-badge">阶段测试Ⅲ</div>'
    '<div class="cover-title">七上–八上中段诊断 · 讲评</div>'
    '<div class="cover-sub">G01–G54 全部 54 个考点 + 前 400 词跨阶诊断</div>'
    '<div class="cover-tagline">测试 + 讲评 · 五段式</div>'
    '<div class="cover-info"><div class="cover-info-num"><div class="ci-label">覆盖考点</div><div class="ci-val">54</div></div>'
    '<div class="cover-info-num"><div class="ci-label">词汇范围</div><div class="ci-val">400+</div></div>'
    '<div class="cover-info-num"><div class="ci-label">讲评页数</div><div class="ci-val">42</div></div>'
    '<div class="cover-info-num"><div class="ci-label">满分</div><div class="ci-val">100</div></div></div>'
    '<div class="cover-emoji">📊</div></div>', 1, "阶段测试Ⅲ · 讲评", "七上–八上中段诊断")

add(B.section_head("总", "全卷概况")
    + B.stats_panel([("92%", "班均得分率"), ("54", "覆盖考点"), ("42", "讲评页数"), ("C", "主要薄弱等级")])
    + B.rule_cards([("zhug", "诊断范围", "测试卷覆盖 L1–L20 全部 54 个语法考点（G01–G54）与前 400 词。本讲评聚焦高频错题、薄弱考点与提升计划。"),
                    ("xing", "讲评方式", "五段式：①测试概况 → ②高频错题精讲 → ③考点雷达 → ④薄弱专项 → ⑤总结提升。交互题点击作答可即时自检。"),
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
    + "<tr><td>21</td><td>G52 过去时</td><td>38%</td><td>did 后加原形</td></tr>"
    + "<tr><td>37</td><td>G49 不定代词</td><td>34%</td><td>形容词后置</td></tr>"
    + "<tr><td>45</td><td>G38 why/because</td><td>30%</td><td>because 与 so 混用</td></tr>"
    + "<tr><td>33</td><td>G31 冠词</td><td>28%</td><td>a/an 判断</td></tr>"
    + "<tr><td>50</td><td>G26 三单否定</td><td>26%</td><td>doesn't 后还原</td></tr></tbody></table></div>"
    + B.sub_label("点击自检一题")
    + B.quiz_html([("错题 21：He ____ (not watch) TV yesterday.", "didn't watch", ["doesn't watch", "not watch"])]), 1, "高频错题预览", "Top 错题")

# ================= 20 测试语境词速览 =================
add(B.section_head("词", "测试语境词 · 20 词速览")
    + B.sub_label("本卷 20 个测试语境词，随讲评自然习得")
    + B.vocab_cards([
        (("grade", "/ɡreɪd/", "n./v.", "年级；分数", "a good grade / grade the paper", "She got a good grade in math.")),
        (("score", "/skɔː(r)/", "n./v.", "分数；得分", "a high score / score a goal", "He got a high score on the test.")),
        (("mark", "/mɑːk/", "n./v.", "分数；标记", "full marks / mark the answer", "I marked the correct answer.")),
        (("correct", "/kəˈrekt/", "adj./v.", "正确的；改正", "the correct answer / correct sth.", "Choose the correct word.")),
        (("mistake", "/mɪˈsteɪk/", "n./v.", "错误", "make a mistake / mistake A for B", "Everyone makes mistakes.")),
        (("error", "/ˈerə(r)/", "n.", "错误；误差", "a spelling error / an error", "There is an error in the paper.")),
        (("improve", "/ɪmˈpruːv/", "v.", "提高；改进", "improve English / improve skills", "Reading can improve your English.")),
        (("review", "/rɪˈvjuː/", "v./n.", "复习；回顾", "review the lesson / a review", "I review my notes before the test.")),
        (("prepare", "/prɪˈpeə(r)/", "v.", "准备", "prepare for / prepare the meal", "We prepared for the exam.")),
        (("plan", "/plæn/", "n./v.", "计划；打算", "make a plan / plan to do", "I plan to study hard.")),
        (("goal", "/ɡəʊl/", "n.", "目标；球门", "set a goal / reach a goal", "My goal is to pass the test.")),
        (("memory", "/ˈmeməri/", "n.", "记忆；回忆", "a good memory / in memory of", "I have a good memory for words.")),
        (("practice", "/ˈpræktɪs/", "n./v.", "练习；实践", "practice doing / daily practice", "Practice makes perfect.")),
        (("progress", "/ˈprəʊɡres/", "n.", "进步；进展", "make progress / progress in", "You made great progress.")),
        (("result", "/rɪˈzʌlt/", "n.", "结果；成绩", "test result / as a result", "The result was excellent.")),
        (("subject", "/ˈsʌbdʒɪkt/", "n.", "科目；主题", "my favorite subject / a subject", "English is my favorite subject.")),
        (("skill", "/skɪl/", "n.", "技能；技巧", "language skills / a skill", "Reading skill is important.")),
        (("doubt", "/daʊt/", "n./v.", "怀疑；疑问", "no doubt / doubt sth.", "There is no doubt about it.")),
        (("courage", "/ˈkʌrɪdʒ/", "n.", "勇气", "have courage / take courage", "She had the courage to speak.")),
        (("confident", "/ˈkɒnfɪdənt/", "adj.", "自信的", "be confident of / confident in", "I am confident of my answer."))]), 2, "测试语境词", "20 词速览")

# ================= 段2 高频错题精讲 =================
add(B.section_head("讲", "代词系统 · G01–G06")
    + B.rule_cards([("zhug", "主格与宾格", "I/me, he/him, she/her：作主语用主格，作宾语用宾格。动词前用主格，动词或介词后用宾格。"),
                    ("bin", "物主代词", "my/mine, your/yours：形容词性后接名词（my book），名词性单独用（The book is mine）。"),
                    ("warn", "高频错因", "She 与 her 误用；I 与 me 误用；my 与 mine 误用。")])
    + B.quiz_html([("主格、宾格判断：____ goes to school every day.（主格）", "He", ["Him", "His"]),
                   ("物主代词：This is ____ book.（形容词性物主代词）", "my", ["mine", "I"]),
                   ("介词后应用宾格：Give it to ____.", "her", ["she", "hers"]),
                   ("名词性物主代词：The pen is ____.", "mine", ["my", "me"]),
                   ("动词后用宾格：Please help ____.", "us", ["we", "our"]),
                   ("形容词性物主代词后接？", "名词", ["动词", "形容词"]),
                   ("The book is ____.（名词性物主代词，我的）", "mine", ["my", "I"])]), 2, "代词系统错题", "G01–G06")

add(B.section_head("讲", "be 动词 · G03/G05")
    + B.rule_cards([("qita", "be 动词搭配", "I am / He is / You are；复数主语用 are；否定加 not，疑问提前。"),
                    ("warn", "常见错误", "He are → He is；They is → They are；I is → I am。")])
    + B.quiz_html([("____ she a teacher?", "Is", ["Are", "Am"]),
                   ("We ____ students.", "are", ["is", "am"]),
                   ("I ____ a student.", "am", ["is", "are"]),
                   ("否定句：He ____ a doctor.", "isn't", ["aren't", "am not"]),
                   ("复数be动词：The apples ____ fresh.", "are", ["is", "am"]),
                   ("I 与 am 搭配：____ a teacher.", "I am", ["I is", "I are"]),
                   ("Did you ____ at home last night?（过去be）", "be", ["was", "were"])]), 2, "be 动词错题", "G03/G05")

add(B.section_head("讲", "名词·介词·数词 · G07–G12")
    + B.rule_cards([("ming", "名词所有格", "名词+'s 表所有（Tom's bag）；of 用于无生命物（the name of the school）。"),
                    ("xing", "方位介词", "in/on/under/behind/next to/between 表示空间关系。"),
                    ("qita", "基数词拼写", "one–twenty 拼写牢记；十几有 special 拼写（twelve/thirteen）；整十数加 -ty。")])
    + B.quiz_html([("The book is ____ the desk.（在…上面）", "on", ["in", "under"]),
                   ("Tom's bag（所有格含义）", "Tom 的包", ["Tom 们的包", "Tom 是包"]),
                   ("between…and… 表示？", "在…和…之间", ["在…上面", "在…后面"]),
                   ("The cat is ____ the sofa.（在…下面）", "under", ["on", "behind"]),
                   ("The school is ____ the park.（在…旁边）", "next to", ["in front", "under"]),
                   ("in the morning 表？", "在早上", ["在晚上", "在下午"]),
                   ("The name ____ the school is Long.（所有格）", "of", ["'s", "to"]),
                   ("The bag is ____ the desk and the chair.（两者之间）", "between", ["behind", "under"]),
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
                   ("____ careful!（小心）", "Be", ["Is", "Are"]),
                   ("否定祈使句用哪个词开头？", "Don't", ["Not", "No't"]),
                   ("____ the door, please.（请关门）", "Close", ["Closing", "Closes"])]), 2, "祈使句错题", "G13")

add(B.section_head("讲", "疑问句六宝 · G22")
    + B.rule_cards([("bin", "六疑问词", "What 什么 / Where 哪里 / When 何时 / Why 为什么 / Who 谁 / How 怎样。")])
    + B.quiz_html([("____ is your name?", "What", ["Where", "When"]),
                   ("____ do you go to school?（方式）", "How", ["What", "Who"]),
                   ("____ is the library?（地点）", "Where", ["When", "Why"]),
                   ("____ do you like English?（原因）", "Why", ["Where", "Who"]),
                   ("____ is your birthday?（时间）", "When", ["What", "How"]),
                   ("____ pen is this?（谁的）", "Whose", ["What", "How"]),
                   ("____ do you spell it?（方式）", "How", ["When", "Who"]),
                   ("____ is the weather like?（什么）", "What", ["Where", "Why"])]), 2, "疑问词错题", "G22")

add(B.section_head("讲", "like/want/would like · G15/G18")
    + B.rule_cards([("xing", "动词搭配", "like to do / want to do / would like to do：后接不定式。")])
    + B.quiz_html([("I would like ____ some milk.", "to drink", ["drinking", "drink"]),
                   ("They like ____ football.", "to play", ["playing to", "and play"])])
    + B.drag_q([("I would like ", "to drink", " some milk."),
                ("She wants ", "to go", " shopping."),
                ("He wants ", "to be", " a doctor.")], ["to drink", "to go", "to be"])
    , 2, "动词搭配", "G15/G18")

add(B.section_head("讲", "一般现在时 · G16/G25")
    + B.rule_cards([("ming", "非三单与三单", "I/You/复数用原形；He/She/It 用 -s/-es；否定 don't/doesn't + 原形。"),
                    ("warn", "三单规则", "一般加 -s；ch/sh/x/o 加 -es；辅音+y 变 -ies。")])
    + B.quiz_html([("She ____ (go) to school by bus.", "goes", ["go", "going"]),
                   ("They ____ (not like) tea.", "don't like", ["doesn't like", "not like"]),
                   ("He ____ (watch) TV in the evening.", "watches", ["watch", "watchs"]),
                   ("My father ____ (work) in a hospital.", "works", ["work", "working"]),
                   ("The sun ____ (rise) in the east.", "rises", ["rise", "raising"]),
                   ("否定：I ____ (not like) coffee.", "don't like", ["doesn't like", "not like"]),
                   ("He ____ (go) to bed at ten.", "goes", ["go", "going"]),
                   ("They ____ (play) football on Sundays.", "play", ["plays", "playing"])]), 2, "一般现在时", "G16/G25")

add(B.section_head("讲", "过去时 was/were · G19")
    + B.rule_cards([("zhug", "be 过去式", "I/He/She 用 was；You/We/They 用 were；否定 wasn't/weren't；疑问提前。")])
    + B.quiz_html([("I ____ at home yesterday.", "was", ["were", "am"]),
                   ("They ____ very happy.", "were", ["was", "are"]),
                   ("She ____ not at school last week.", "was", ["were", "is"]),
                   ("____ you at the party last night?", "Were", ["Was", "Are"]),
                   ("I ____ (be) very tired yesterday.", "was", ["were", "am"]),
                   ("The boys ____ (be) in the park last Sunday.", "were", ["was", "is"]),
                   ("She ____ (be) not hungry just now.", "was", ["were", "is"]),
                   ("____ they at home last night?", "Were", ["Was", "Are"])]), 2, "was/were", "G19")

add(B.section_head("讲", "过去时 did · G20/G52")
    + B.rule_cards([("qita", "实义动词过去式", "规则动词加 -ed；否定 didn't + 原形；疑问 Did + 原形。"),
                    ("warn", "高频错因", "didn't 后接过去式（如 didn't went）是典型错误。")])
    + B.quiz_html([("He ____ (play) football yesterday.", "played", ["plays", "playing"]),
                   ("Did you ____ the movie last night?", "watch", ["watched", "watching"]),
                   ("She didn't ____ to school yesterday.", "go", ["went", "going"]),
                   ("We ____ (visit) the museum last month.", "visited", ["visits", "visiting"])]), 2, "did 过去时", "G20/G52")

add(B.section_head("讲", "三单变化 · G25/G26")
    + B.rule_cards([("warn", "三单规则", "一般加 -s；ch/sh/x/o 加 -es；辅音+y 变 -ies。"),
                    ("bin", "否定疑问", "三单否定用 doesn't + 原形；疑问 Does + 原形。")])
    + B.quiz_html([("He ____ (watch) TV every evening.", "watches", ["watch", "watchs"]),
                   ("She ____ (study) hard.", "studies", ["studys", "study"]),
                   ("____ he like apples?", "Does", ["Do", "Is"]),
                   ("She doesn't ____ (like) coffee.", "like", ["likes", "liking"])]), 2, "三单变化", "G25/G26")

add(B.section_head("讲", "情态动词 · G28")
    + B.rule_cards([("bin", "can/must", "can 表能力/许可；must 表必须；后接动词原形。"),
                    ("qita", "礼貌处理", "Could/Would 表更礼貌的请求。")])
    + B.quiz_html([("You ____ finish your homework first.（必须）", "must", ["can", "may"]),
                   ("____ you swim?", "Can", ["Must", "Do"]),
                   ("She can ____ (play) the piano.", "play", ["plays", "playing"]),
                   ("You must ____ (be) quiet in the library.", "be", ["is", "being"])]), 2, "情态动词", "G28")

add(B.section_head("讲", "冠词 · G31")
    + B.rule_cards([("xing", "a/an/the", "a 辅音音素开头；an 元音音素开头；the 特指。")])
    + B.quiz_html([("She is ____ English teacher.", "an", ["a", "the"]),
                   ("I have ____ apple.", "an", ["a", "the"]),
                   ("He is ____ tall boy.", "a", ["an", "the"]),
                   ("____ sun rises in the east.（特指）", "The", ["A", "An"])]), 2, "冠词错题", "G31")

add(B.section_head("讲", "some/any 与不定代词 · G33/G49")
    + B.rule_cards([("ming", "some/any", "some 肯定/邀请；any 否定/疑问。"),
                    ("qita", "复合不定代词", "someone/anything 作主语谓语单数；形容词后置。")])
    + B.quiz_html([("Would you like ____ tea?", "some", ["any", "no"]),
                   ("I have ____ (something) interesting to tell you.", "something", ["anything", "nothing"]),
                   ("There isn't ____ milk in the fridge.", "any", ["some", "a"]),
                   ("____ interesting is in the box.", "Something", ["Some", "Anything"])]), 2, "不定代词", "G33/G49")

add(B.section_head("讲", "would like / how much · G34/G35")
    + B.rule_cards([("zhug", "询问与意愿", "would like to do；how much 问不可数/价格；how many 问可数复数。")])
    + B.quiz_html([("____ milk do you need?", "How much", ["How many", "How often"]),
                   ("I would like ____ a book.", "to buy", ["buying", "buy"]),
                   ("____ books are there on the desk?", "How many", ["How much", "How often"]),
                   ("How much is the shirt?（价格）", "It's 20 yuan.", ["It's red.", "It's big."])]), 2, "would like", "G34/G35")

add(B.section_head("讲", "外貌·因果 · G37–G38")
    + B.rule_cards([("bin", "have/has", "I/You/We/They 用 have；He/She/It 用 has；描述外貌用 have/has。"),
                    ("warn", "because 与 so", "because 表原因，so 表结果，二者不连用。"),
                    ("qita", "why 提问", "why 询问原因，用 because 回答。")])
    + B.quiz_html([("She ____ long hair.", "has", ["have", "is"]),
                   ("They ____ big eyes.", "have", ["has", "is"]),
                   ("My sister ____ big eyes.", "has", ["is", "have"]),
                   ("He ____ a round face.", "has", ["have", "is"]),
                   ("____ do you like winter?", "Why", ["What", "How"]),
                   ("I was tired, ____ I slept early.", "so", ["because", "but"]),
                   ("He didn't come ____ he was ill.", "because", ["so", "but"]),
                   ("—Why are you late? —____ I missed the bus.", "Because", ["So", "But"])]), 2, "外貌因果", "G37–G38")

add(B.section_head("讲", "天气·礼貌请求 · G40–G41")
    + B.rule_cards([("qita", "天气表达", "It's + 形容词：rainy/windy/sunny/cloudy。"),
                    ("xing", "would like", "would like + 名词 / to do，表客气请求。")])
    + B.quiz_html([("表示多风：It's ____.", "windy", ["wind", "winding"]),
                   ("表示有雨：It's ____.", "rainy", ["rain", "raining"]),
                   ("It's sunny.（含义）", "晴朗", ["多风", "多云"]),
                   ("表示多云：It's ____.", "cloudy", ["cloud", "clouding"]),
                   ("Would you like ____ a movie?（看）", "to watch", ["watch", "watching"]),
                   ("Would you like some ____?（茶）", "tea", ["teas", "teas"]),
                   ("I'd like ____ a book.", "to read", ["reading", "read"]),
                   ("Would you like ____ coffee?", "some", ["any", "no"])]), 2, "天气礼貌请求", "G40–G41")

add(B.section_head("讲", "频度副词 · G43")
    + B.rule_cards([("bin", "频度副词", "always/usually/often/sometimes/never 表示频率，位于实义动词前、be 动词后。")])
    + B.quiz_html([("how often 对什么提问？", "频率", ["地点", "时间点"]),
                   ("always 表示？", "总是", ["从不", "有时"]),
                   ("He ____ goes to school by bike.（总是）", "always", ["never", "sometimes"]),
                   ("频度副词 often 位于？", "实义动词前", ["句末", "名词后"])]), 2, "频度副词", "G43")

add(B.section_head("讲", "现在进行时 · G46")
    + B.rule_cards([("warn", "ing 拼写", "一般加 -ing；e 结尾去 e；重读闭音节双写末字母。"),
                    ("zhug", "进行时标志", "now/look/listen/at the moment。")])
    + B.quiz_html([("I am ____ (write) a letter.", "writing", ["writeing", "writting"]),
                   ("Look! They ____ (run).", "are running", ["is running", "run"]),
                   ("She is ____ (swim) now.", "swimming", ["swiming", "swims"]),
                   ("Listen! The bird ____ (sing).", "is singing", ["sing", "sings"])]), 2, "现在进行时", "G46")

add(B.section_head("讲", "比较级/最高级 · G55/G56")
    + B.rule_cards([("bin", "比较/最高", "短词 -er/-est，长词 more/most；最高级前加 the。"),
                    ("warn", "同级比较", "as + 原级 + as；not as/so + 原级 + as。")])
    + B.quiz_html([("Tom is ____ (tall) than Jack.", "taller", ["tall", "tallest"]),
                   ("She is ____ (popular) girl in class.", "the most popular", ["most popular", "more popular"]),
                   ("He is as ____ (tall) as his brother.", "tall", ["taller", "tallest"]),
                   ("Beijing is the ____ (big) city in China.", "biggest", ["big", "bigger"])]), 2, "比较/最高级", "G55/G56")

# ================= 段3 考点雷达 =================
add(B.section_head("雷", "考点掌握度雷达 · 总览")
    + B.stats_panel([("强", "代词系统"), ("中", "时态系统"), ("弱", "区分句"), ("需补", "三单/情态")])
    + B.game_board("G01–G54 考点掌握度", "🛰️", "点击左侧选项作答自检",
                   B.quiz_html([("代词与 be（G01–G06）掌握如何？", "较扎实", ["待提升", "需重学"]),
                                ("过去时（G52）本卷错率最高，属于？", "需重点巩固", ["已掌握", "不需复习"])])), 3, "考点雷达总览", "54 考点分布")

add(B.section_head("雷", "脆弱考点 · 时态定位")
    + B.rule_cards([("warn", "过去时 vs 现在时", "看时间状语：yesterday→过去，every day→现在。"),
                    ("qita", "进行时标志", "now/look/listen 用进行时。")])
    + B.quiz_html([("I ____ (go) to school yesterday.", "went", ["go", "goes"]),
                   ("标志词判断：now 用哪个时态？", "现在进行时", ["一般过去时", "一般将来时"]),
                   ("every day 标志什么时态？", "一般现在时", ["过去时", "进行时"]),
                   ("last week 标志？", "一般过去时", ["一般现在时", "进行时"])]), 3, "时态雷达", "时态薄弱定位")

add(B.section_head("雷", "脆弱考点 · 句法定位")
    + B.rule_cards([("ming", "区分 because/so", "原因用 because，结果用 so，不连用。"),
                    ("bin", "区分 some/any", "肯定用 some，否定/疑问用 any。")])
    + B.quiz_html([("I was tired, ____ I slept.", "so", ["because", "but"]),
                   ("There isn't ____ milk.", "any", ["some", "a"]),
                   ("____ you like some tea?（邀请）", "Would", ["Do", "Are"]),
                   ("He didn't come ____ he was ill.", "because", ["so", "but"])]), 3, "句法雷达", "区分薄弱")

add(B.section_head("雷", "错因类型分析")
    + "<div class='content-table'><table><thead><tr><th>错因</th><th>占比</th><th>对策</th></tr></thead><tbody>"
    + "<tr><td>时态混淆</td><td>35%</td><td>标志词定位</td></tr>"
    + "<tr><td>固定搭配</td><td>28%</td><td>口诀记忆</td></tr>"
    + "<tr><td>语序错误</td><td>22%</td><td>句式结构</td></tr>"
    + "<tr><td>词义辨析</td><td>15%</td><td>语境推断</td></tr></tbody></table></div>", 3, "错因分析", "高频错因")

add(B.section_head("雷", "高频考法回顾")
    + B.rule_cards([("zhug", "中考高频", "时态填空、固定搭配、疑问词选择、比较级是高频考法。")])
    + B.quiz_html([("划线提问：I go to school at 8.（对时间提问）", "When do you go to school?", ["What do you go?", "Where do you go?"]),
                   ("选择正确固定搭配", "look forward to doing", ["look forward to do", "look forward do"]),
                   ("实义动词三单疑问助动词用？", "does", ["do", "is"]),
                   ("最高级前必须加？", "the", ["a", "an"])]), 3, "高频考法", "考法回顾")

add(B.section_head("雷", "易错点对照")
    + "<div class='content-table'><table><thead><tr><th>易错</th><th>正确</th></tr></thead><tbody>"
    + "<tr><td>He didn't went.</td><td>He didn't go.</td></tr>"
    + "<tr><td>Because..., so...</td><td>Because... 或 So...</td></tr>"
    + "<tr><td>someting interesting</td><td>something interesting</td></tr>"
    + "<tr><td>more tall</td><td>taller</td></tr>"
    + "<tr><td>He is tallest in class.</td><td>He is the tallest in class.</td></tr></tbody></table></div>", 3, "易错点对照", "混淆排除")

# ================= 段4 薄弱专项 =================
add(B.section_head("专", "阅读 A 篇 · 信息定位法")
    + B.rule_cards([("zhug", "五步法", "速读抓主旨 → 精读划关键词 → 解题回原文 → 排除干扰项 → 复述巩固。")])
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

add(B.section_head("专", "词汇错题 · 测试词辨析")
    + B.rule_cards([("bin", "相近词", "grade(分数)/score(得分)/mark(标记) 义近辨析。"),
                    ("qita", "形近词", "mistake(错误)/mistake A for B(把A误当B)。")])
    + B.quiz_html([("He made a ____ in the test.（错误）", "mistake", ["success", "pleasure"]),
                   ("选出正确搭配", "make progress", ["do progress", "make progresses"]),
                   ("be confident of 的含义？", "对…有信心", ["对…失望", "对…怀疑"]),
                   ("prepare for 的含义？", "为…准备", ["为…后悔", "为…争论"])]), 4, "词汇错题", "测试词")

# ================= 段5 总结提升 =================
add(B.section_head("结", "薄弱考点清单")
    + "<div class='content-table'><table><thead><tr><th>等级</th><th>考点</th><th>学习动作</th></tr></thead><tbody>"
    + "<tr><td>C</td><td>G52 过去时</td><td>L20 课件回顾</td></tr>"
    + "<tr><td>C</td><td>G49 不定代词</td><td>L19 课件回顾</td></tr>"
    + "<tr><td>B</td><td>G38 because/so</td><td>口诀强化</td></tr>"
    + "<tr><td>B</td><td>G26 三单否定</td><td>变式练习</td></tr></tbody></table></div>", 5, "薄弱清单", "按等级")

add(B.section_head("结", "下阶段建议 · Stage 6")
    + B.rule_cards([("zhug", "Stage 6 预告", "L22 起进入比较级/最高级系统归纳（G55-G57）、条件句（L23）、状语从句（L24）、动名词与不定式（L25）等八上难点。"),
                    ("xing", "学习建议", "每日 20 词滚动 + 错题本复盘 + 两日一测。"),
                    ("bin", "错题本方法", "错题分三类：时态/搭配/语序，各配 3 道变式题。")]), 5, "下阶段建议", "Stage 6")

add(B.section_head("结", "核心口诀总览")
    + B.rule_cards([("ming", "过去时", "doesn't/didn't 后加原形。"),
                    ("bin", "不定代词", "形容词后置，谓语单数。"),
                    ("qita", "区分句", "because 表因，so 表果，不连用。"),
                    ("warn", "比较级", "短词 -er，长词 more，最高级加 the。"),
                    ("xing", "祈使句", "动词原形开头，Don't 表否定。"),
                    ("zhug", "同级比较", "as + 原级 + as，否定 not as/so…as。")]), 5, "核心口诀", "一页速览")

add(B.section_head("结", "课堂思维导图")
    + B.mind_map(21, "阶段测试Ⅲ · 讲评", [
        ("考点雷达", "代词 / 时态 / 区分句 / 三单 / 情态"),
        ("高频错题", "过去时 / 不定代词 / because / 冠词"),
        ("薄弱专项", "阅读五步法 / 写作 / 词汇 / 简答"),
        ("提升计划", "每日 20 词 / 错题本 / 两日一测"),
        ("下阶段", "Stage 6 · 比较级 / 条件句 / 从句"),
        ("总目标", "突破 90% 正确率")]), 5, "思维导图", "全课收尾")

add(B.section_head("结", "错题复盘 · 三色笔记法")
    + B.rule_cards([("ming", "红色错因", "时态混淆/固定搭配——用红笔标出错误类型，配 3 道变式题。"),
                    ("xing", "黄色易错", "语序/词义——用黄笔勾出易错点，每日晨读巩固。"),
                    ("bin", "绿色掌握", "已连续两次做对的题——用绿笔标记，进入巩固通道。")])
    + B.stats_panel([("红", "时态/搭配"), ("黄", "语序/词义"), ("绿", "已掌握"), ("目标", "绿≥80%")])
    + B.quiz_html([("错题本第一原则是？", "先归因再复习", ["直接抄答案", "只背单词"]),
                   ("变式题的作用是？", "检验是否真正掌握", ["增加负担", "浪费时间"]),
                   ("连续几次做对可标记为掌握？", "两次", ["一次", "三次"])]), 5, "错题复盘", "三色笔记法")

add(B.section_head("结", "Stage 6 衔接 · 课程地图")
    + "<div class='content-table'><table><thead><tr><th>课次</th><th>语法主线</th><th>衔接要点</th></tr></thead><tbody>"
    + "<tr><td>L22</td><td>比较级/最高级/同级</td><td>G55–G57 系统归纳</td></tr>"
    + "<tr><td>L23</td><td>条件句 if 主将从现</td><td>G58–G59 + 祈使句</td></tr>"
    + "<tr><td>L24</td><td>原因/结果/让步从句</td><td>G60–G61 连接词</td></tr>"
    + "<tr><td>L25</td><td>动名词 vs 不定式</td><td>G62–G63 用法辨析</td></tr></tbody></table></div>"
    + B.rule_cards([("zhug", "衔接建议", "本讲评已诊断 54 考点与前 400 词，L22 起进入八上重难点主线。"),
                    ("qita", "自律提醒", "错题本三色分区 + 每日 20 词滚动 + 两日一测。")])
    + B.quiz_html([("L22 的语法主线是？", "比较级/最高级", ["条件句", "被动语态"]),
                   ("L24 重点学习哪类从句？", "原因/结果/让步", ["定语从句", "宾语从句"]),
                   ("L25 辨析哪两种结构？", "动名词 vs 不定式", ["主格 vs 宾格", "单数 vs 复数"])]), 5, "Stage 6 地图", "衔接规划")

total = p - 1
seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
page_meta = {i: {"p": "CORE", "m": 2} for i in range(1, total + 1)}

js = B.js_extra(total, seg_pages, page_meta)
css = B.CSS_EXTRA
out = os.path.join(out_dir, "第21课时_课件_中等.html")
size = B.write_courseware(21, "第21课时 · 阶段测试Ⅲ讲评", pages, NAV, "Stage 5 · L21", css, js, out)
print("L21 课件生成：%s (%d bytes, %d pages)" % (out, size, total))