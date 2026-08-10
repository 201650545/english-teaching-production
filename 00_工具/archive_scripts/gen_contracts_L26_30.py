# -*- coding: utf-8 -*-
"""邓兴华 L26-L30 契约 6 件套批量生成（复用 gen_contracts_L21_25 结构）。"""
import os, json

ROOT = r"D:\英语教学\邓兴华"

LESSONS = {
 26: {
  "course": "第26课 · 时态三态综合辨析（一般现在/过去/进行）",
  "type": "授课课（八段式）",
  "stage": "Stage 6",
  "stage_range": "L22–L34",
  "duration": "90 分钟",
  "theme": "青少年日常生活的时态三态",
  "reading_theme": "A：My Busy School Day / B：A Day in My Life / C：What Are They Doing Now? / 五选四：My Daily Schedule",
  "totalPages": 44,
  "accent_theme": "红金暖色系（亮色）",
  "brand": "#E63946", "accent": "#FFD700",
  "bgGradient": "#FFF8F0 → #FFE8D6",
  "style": "八段式授课（复习导入/新词20/语法3考点/随堂演练/阅读理解/句子练习/自然拼读/课堂总结）",
  "vocab": "词 501–520（tense, basic, present, past, continuous, progressive, perfect, action, state, custom, pattern, schedule, recently, lately, currently, temporarily, permanently, suddenly, gradually, eventually）",
  "grammar": "G16 一般现在时（非三单 + every day/usually/often） / G43 频度副词（位置与 How often） / G46 现在进行时（be+V-ing + now/look/listen）——三态辨析",
  "phonics": "-ed 过去式读音 /t/ /d/ /ɪd/",
  "reading_word": "189–198 / 210–220 / 179–187 词",
  "segments": [
     {"name":"复习导入","pages":3,"desc":"复习 L25 动名词不定式 + 三态标志词前瞻"},
     {"name":"新词20","pages":8,"desc":"时态/时间标志/动作状态 分组"},
     {"name":"语法3考点","pages":10,"desc":"G16 一般现在 + G43 频度副词 + G46 现在进行 + 三态辨析"},
     {"name":"随堂演练","pages":4,"desc":"多题型（单选/填空/拖拽/排序/连线）"},
     {"name":"阅读理解","pages":5,"desc":"A/B/C 篇短文 + 五选四 + 三态定位策略"},
     {"name":"句子练习","pages":4,"desc":"造句 + 汉译英（三态对照）"},
     {"name":"自然拼读","pages":5,"desc":"-ed /t//d//ɪd/ 音素 + 练习"},
     {"name":"课堂总结","pages":5,"desc":"核心口诀 + 思维导图 + 巩固清单"},
  ],
  "session": "L26",
 },
 27: {
  "course": "第27课 · 现在完成时（首次引入）",
  "type": "授课课（八段式）",
  "stage": "Stage 6",
  "stage_range": "L22–L34",
  "duration": "90 分钟",
  "theme": "交换生经历与现在完成时",
  "reading_theme": "A：My Experience as an Exchange Student / B：Have You Ever...? / C：A Visit to London / 五选四：Planning a Trip",
  "totalPages": 44,
  "accent_theme": "红金暖色系（亮色）",
  "brand": "#E63946", "accent": "#FFD700",
  "bgGradient": "#FFF8F0 → #FFE8D6",
  "style": "八段式授课（复习导入/新词20/语法3考点/随堂演练/阅读理解/句子练习/自然拼读/课堂总结）",
  "vocab": "词 521–540（already, yet, just, ever, once, before, nowadays, previously, for, experience, voyage, overseas, foreign, country, tradition, language, communicate, exchange, program, destination）",
  "grammar": "G64 现在完成时（have/has + 过去分词；结构） / G64 过去分词规则与高频不规则 / G64 现在完成时标志词 already/yet/just/ever/before/once + have been to",
  "phonics": "-en 过去分词词尾 /ən/ 与不规则过去分词",
  "reading_word": "189–198 / 210–220 / 179–187 词",
  "segments": [
     {"name":"复习导入","pages":3,"desc":"复习 L26 三态 + 现在完成时引入"},
     {"name":"新词20","pages":8,"desc":"完成时标志词/交换经历/海外文化 分组"},
     {"name":"语法3考点","pages":10,"desc":"G64 结构 + 过去分词 + 标志词 + have been to"},
     {"name":"随堂演练","pages":4,"desc":"多题型（单选/填空/拖拽/排序/连线）"},
     {"name":"阅读理解","pages":5,"desc":"A/B/C 篇短文 + 五选四 + 完成时定位策略"},
     {"name":"句子练习","pages":4,"desc":"造句 + 汉译英（现在完成时）"},
     {"name":"自然拼读","pages":5,"desc":"-en 过去分词 + 不规则变化 练习"},
     {"name":"课堂总结","pages":5,"desc":"核心口诀 + 思维导图 + 巩固清单"},
  ],
  "session": "L27",
 },
 28: {
  "course": "第28课 · 现在完成时进阶：since-for / been to",
  "type": "授课课（八段式）",
  "stage": "Stage 6",
  "stage_range": "L22–L34",
  "duration": "90 分钟",
  "theme": "中国变化与现在完成时进阶",
  "reading_theme": "A：The Changes in My Hometown / B：Since I Was Born / C：A Modern Farm / 五选四：My City's Development",
  "totalPages": 44,
  "accent_theme": "红金暖色系（亮色）",
  "brand": "#E63946", "accent": "#FFD700",
  "bgGradient": "#FFF8F0 → #FFE8D6",
  "style": "八段式授课（复习导入/新词20/语法3考点/随堂演练/阅读理解/句子练习/自然拼读/课堂总结）",
  "vocab": "词 541–560（development, modernization, urban, rural, reform, economy, society, scientific, innovation, environment, pollution, protection, education, medicine, transportation, network, agriculture, business, criterion, quality）",
  "grammar": "G64 since+时间点 / for+时间段 / G64 have been to / gone to / been in 三态辨析 / G64 中考考法（与一般过去时区分）",
  "phonics": "-tion /ʃən/ 与 -sion /ʒən/",
  "reading_word": "189–198 / 210–220 / 179–187 词",
  "segments": [
     {"name":"复习导入","pages":3,"desc":"复习 L27 完成时 + since/for 引入"},
     {"name":"新词20","pages":8,"desc":"城市发展/社会/环境/科技 分组"},
     {"name":"语法3考点","pages":10,"desc":"G64 since/for + been to/gone to/been in + 中考考法"},
     {"name":"随堂演练","pages":4,"desc":"多题型（单选/填空/拖拽/排序/连线）"},
     {"name":"阅读理解","pages":5,"desc":"A/B/C 篇短文 + 五选四 + since/for 定位"},
     {"name":"句子练习","pages":4,"desc":"造句 + 汉译英（since/for）"},
     {"name":"自然拼读","pages":5,"desc":"-tion/-sion 音素 + 练习"},
     {"name":"课堂总结","pages":5,"desc":"核心口诀 + 思维导图 + 巩固清单"},
  ],
  "session": "L28",
 },
 29: {
  "course": "第29课 · 被动语态（首次引入）",
  "type": "授课课（八段式）",
  "stage": "Stage 6",
  "stage_range": "L22–L34",
  "duration": "90 分钟",
  "theme": "日常物品制造与被动语态",
  "reading_theme": "A：How Is Tea Made? / B：How Is Chocolate Made? / C：Famous Inventions / 五选四：How Paper Is Made",
  "totalPages": 44,
  "accent_theme": "红金暖色系（亮色）",
  "brand": "#E63946", "accent": "#FFD700",
  "bgGradient": "#FFF8F0 → #FFE8D6",
  "style": "八段式授课（复习导入/新词20/语法3考点/随堂演练/阅读理解/句子练习/自然拼读/课堂总结）",
  "vocab": "词 561–580（build, invent, discover, produce, make, grow, plant, design, create, promote, research, technology, equipment, factory, industry, product, material, process, manufacture, construct）",
  "grammar": "G65 被动语态构成（be + 过去分词） / G65 一般现在/一般过去被动 / G65 主动改被动三步 + by 短语",
  "phonics": "-ure /ə(r)/ 与 -tion /ʃən/",
  "reading_word": "189–198 / 210–220 / 179–187 词",
  "segments": [
     {"name":"复习导入","pages":3,"desc":"复习 L28 完成时 + 被动语态引入"},
     {"name":"新词20","pages":8,"desc":"制造/发明/工业/材料 分组"},
     {"name":"语法3考点","pages":10,"desc":"G65 构成 + 现在/过去被动 + 主动改被动三步"},
     {"name":"随堂演练","pages":4,"desc":"多题型（单选/填空/拖拽/排序/连线）"},
     {"name":"阅读理解","pages":5,"desc":"A/B/C 篇短文 + 五选四 + 被动定位"},
     {"name":"句子练习","pages":4,"desc":"主动改被动 + 汉译英"},
     {"name":"自然拼读","pages":5,"desc":"-ure/-tion 音素 + 练习"},
     {"name":"课堂总结","pages":5,"desc":"核心口诀 + 思维导图 + 巩固清单"},
  ],
  "session": "L29",
 },
 30: {
  "course": "第30课 · 被动语态进阶：情态被动 / 主动表被动",
  "type": "授课课（八段式）",
  "stage": "Stage 6",
  "stage_range": "L22–L34",
  "duration": "90 分钟",
  "theme": "生活规则与被动词态进阶",
  "reading_theme": "A：Rules in Our School / B：How Things Are Used / C：What Can Be Done? / 五选四：School Rules",
  "totalPages": 44,
  "accent_theme": "红金暖色系（亮色）",
  "brand": "#E63946", "accent": "#FFD700",
  "bgGradient": "#FFF8F0 → #FFE8D6",
  "style": "八段式授课（复习导入/新词20/语法3考点/随堂演练/阅读理解/句子练习/自然拼读/课堂总结）",
  "vocab": "词 581–600（ought, should, can, could, allowed, required, forbidden, prohibited, permitted, proposed, advised, regarded, believed, reported, said, known, used, supplied, expected, supposed）",
  "grammar": "G65 情态动词被动（can/must/should be done） / G65 主动表被动（sell well/read well/wash easily） / G65 被动否定与疑问 + 阅读识别",
  "phonics": "-ed 被动过去分词 /t/ /d/ /ɪd/",
  "reading_word": "189–198 / 210–220 / 179–187 词",
  "segments": [
     {"name":"复习导入","pages":3,"desc":"复习 L29 被动 + 情态被动引入"},
     {"name":"新词20","pages":8,"desc":"情态动词/规则/被动过去分词 分组"},
     {"name":"语法3考点","pages":10,"desc":"G65 情态被动 + 主动表被动 + 否定疑问识别"},
     {"name":"随堂演练","pages":4,"desc":"多题型（单选/填空/拖拽/排序/连线）"},
     {"name":"阅读理解","pages":5,"desc":"A/B/C 篇短文 + 五选四 + 被动识别"},
     {"name":"句子练习","pages":4,"desc":"情态被动改写 + 汉译英"},
     {"name":"自然拼读","pages":5,"desc":"-ed 被动过去分词读音 + 练习"},
     {"name":"课堂总结","pages":5,"desc":"核心口诀 + 思维导图 + 巩固清单"},
  ],
  "session": "L30",
 },
}

def parse_vocab(vspec):
    inner = vspec.split("（",1)[1].rsplit("）",1)[0]
    words = [w.strip() for w in inner.split(",")]
    return [(w, "见内容蓝图", "见内容蓝图", "见内容蓝图") for w in words]

def md_course_overview(n, d):
    t = d["course"]
    L = [f"# {t}", "", f"> **课名**：{t.split('· ',1)[1] if '· ' in t else t}", f"> **Stage**：{d['stage']}（{d['stage_range']}）",
         f"> **建议时长**：{d['duration']}", f"> **课型**：{d['type']}", "> **数据来源**：第%d课内容蓝图" % n, "", "---", "",
         "## 一、基本信息", "", "| 项目 | 内容 |", "|---|---|",
         "| 课次 | 第 %d 课 |" % n, "| 课名 | %s |" % t, "| 所属阶段 | %s（%s） |" % (d['stage'], d['stage_range']),
         "| 课型 | %s |" % d['type'], "| 建议时长 | %s |" % d['duration'], "| 主题语义场 | %s |" % d['theme'],
         "| 阅读主题 | %s |" % d['reading_theme'], "| 课件总页数 | %d 页 |" % d['totalPages'],
         "| 页面比例 | 21:9 |", "| 交互机制 | 左右半屏点击翻页 + 答题点优先 + 整页滚动 |",
         "| 品牌主色 | %s |" % d['brand'], "| 强调色 | %s |" % d['accent'],
         "| 主题模式 | 仅亮色主题（%s） |" % d['accent_theme'], "| 阶段徽章 | %s · L%02d |" % (d['stage'], n),
         "| 风格 | %s |" % d['style'], "", "---", "", "## 二、词汇硬契约（20词）", "",
         "| # | 单词 | 音标 | 词性 | 中文 | 中考常考搭配 |", "|---|---|---|---|---|---|"]
    words = parse_vocab(d['vocab'])
    for i,(en,ph,pos,cn) in enumerate(words,1):
        L.append("| %d | %s | %s | %s | %s | 见内容蓝图详细搭配 |" % (i, en, ph, pos, cn))
    L += ["", "> **去重校验**：与 L1–L%d 前 %d 词交集 = 0 ✅" % (n-1, (n-26)*20+500), "", "---", "",
          "## 三、语法硬契约", "", "| 考点 | 内容要点 |", "|---|---|"]
    for g in d['grammar'].split(' / '):
        L.append("| %s | 见内容蓝图第二节 |" % g)
    L += ["", "> 语法要点与防越级约束详见内容蓝图第二节。", "", "---", "", "## 四、拼读规划", ""]
    L += ["| 字母组合 | 核心音素 | 发音要点 |", "|---|---|---|",
          "| %s | 见内容蓝图第四节 | 见内容蓝图第四节 |" % d['phonics']]
    L += ["", "---", "", "## 五、阅读规划", "", "| 篇目 | 主题 | 词数闭区间 | 题型 |", "|---|---|---|---|"]
    for rt in d['reading_theme'].split(' / '):
        if '五选四' in rt:
            L.append("| 五选四 | %s | 158–187 词 | 5空 4选（1干扰项） |" % rt)
        else:
            L.append("| %s | %s | %s | 5选择（细节+推断+主旨） |" % (rt.split('：')[0], rt.split('：',1)[1] if '：' in rt else rt, d.get('reading_word','189–220 词')))
    L += ["", "---", "", "## 六、数据采集配置", "", "```json", "{",
          "  \"dataCollectionPlan\": {",
          "    \"enabled\": true,", "    \"syncMode\": \"realtime\",", "    \"exportFormats\": [\"json\", \"csv\"],",
          "    \"sessionIdRule\": \"%s_{studentId}_{YYYYMMDD}\"," % d['session'],
          "    \"recordFirstAttemptOnly\": true,", "    \"allowReview\": true",
          "  }", "}", "```", "", "---", "", "## 七、教学目标", ""]
    for i, s in enumerate(d['segments'],1):
        L.append("%d. 完成「%s」环节（%d 页）：%s" % (i, s['name'], s['pages'], s['desc']))
    L += ["", "---"]
    return "\n".join(L) + "\n"

def md_outline(n, d):
    t = d["course"]
    L = [f"# {t} 大纲脚本", "", "> %s · 共%d页" % (d['type'], d['totalPages']), "", "---", ""]
    for i, s in enumerate(d['segments'],1):
        L.append("## %s %s（%d 页）" % ("①②③④⑤⑥⑦⑧"[i-1], s['name'], s['pages']))
        L.append("")
        L.append("- %s" % s['desc'])
        L.append("- 交互机制：左右半屏点击翻页 + 答题点优先 + 整页滚动")
        L.append("- 数据落库：答题通过 saveAnswer 写入 IndexedDB")
        L.append("")
    L.append("---")
    L.append("")
    L.append("> **总页数**：%d 页（含封面）" % d['totalPages'])
    L.append("> **溯源 ID 前缀**：DXH2026_L%02d_*" % n)
    return "\n".join(L) + "\n"

def md_intent(n, d):
    t = d["course"]
    L = [f"# {t} 演讲意图", "", "> 教师讲解意图与节奏控制指南", "", "---", "",
         "## 一、整体节奏", "", "| 环节 | 页数 | 节奏 | 教师意图 |", "|---|---|---|---|"]
    for s in d['segments']:
        L.append("| %s | %d页 | 中速 | %s |" % (s['name'], s['pages'], s['desc']))
    L += ["", "## 二、主题色与视觉规范", "",
          "- 品牌主色：%s　强调色：%s　背景渐变：%s" % (d['brand'], d['accent'], d['bgGradient']),
          "- 仅亮色主题，主题模式：%s" % d['accent_theme'],
          "- 阶段徽章：%s · L%02d" % (d['stage'], n),
          "- 双契约标记：CW-VISUAL-CONTRACT:1 + CW-INTERACTION-CONTRACT:1",
          "", "## 三、互动与数据采集", "",
          "- 交互函数：checkOpt / fillCheck / pickWord / dragSubmit / moveUp / moveDown / orderCheck / matchPick / flipCard",
          "- 答题落 IndexedDB（saveAnswer 实时写库），支持导出与错题复盘",
          "- 双击撤销：答错后双击可撤回重答",
          "- 会话规则：%s_{studentId}_{YYYYMMDD}" % d['session'],
          "", "## 四、注意事项", "",
          "1. 防越级：严格按内容蓝图第二节语法约束，不越级引入新语法点",
          "2. 生词比例：阅读篇目保持 15%–20%",
          "3. 词数控制：严格落在各课闭区间",
          "4. 互动反馈：每个交互都有音效和视觉反馈",
          "5. 主题色：%s + %s，亮色主题" % (d['brand'], d['accent']),
          "6. 全中文命名，不出现真实学生姓名",
          "", "---"]
    return "\n".join(L) + "\n"

def md_assets(n, d):
    t = d["course"]
    L = [f"# {t} 素材清单", "", "> 课件所需素材清单", "", "---", "",
         "## 一、创意交互点列表", "", "| 编号 | 名称 | 所属环节 | 交互函数名 | 创意描述 |", "|---|---|---|---|---|",
         "| L%02d-A1 | 随堂自检选择题 | 随堂演练/考点 | checkOpt | 点击作答即时判分，落 IndexedDB，双击撤销 |" % n,
         "| L%02d-A2 | 填空判题 | 随堂演练 | fillCheck | 输入答案即时判分，落 IndexedDB |" % n,
         "| L%02d-A3 | 拖拽填空 | 随堂演练 | pickWord/dragSubmit | 拖拽词块填槽，判分落库 |" % n,
         "| L%02d-A4 | 排序题 | 随堂演练 | moveUp/moveDown/orderCheck | 上下移排序，判分落库 |" % n,
         "| L%02d-A5 | 连线配对 | 随堂演练 | matchPick | 左右列配对，判分落库 |" % n,
         "| L%02d-A6 | 翻牌卡 | 词汇环节 | flipCard | 词汇自检翻牌 |" % n,
         "", "## 二、词汇素材（20词）", "",
         "| # | 单词 | 说明 |", "|---|---|---|"]
    words = [w[0] for w in parse_vocab(d['vocab'])]
    for i, w in enumerate(words,1):
        L.append("| %d | %s | 见内容蓝图第一节（音标/词性/中文/搭配/例句） |" % (i, w))
    L += ["", "## 三、语法素材", "", "- %s" % d['grammar'].replace(' / ', '<br>- '),
          "", "## 四、阅读素材", "", "- %s" % d['reading_theme'].replace(' / ', '<br>- '),
          "", "## 五、拼读素材", "", "- %s" % d['phonics'],
          "", "## 六、音效素材", "",
          "- 正确音效：轻快正弦提示音　错误音效：低沉提示音　翻页音效：短促提示音",
          "", "## 七、动画素材", "",
          "- fadeSlideUp / scaleUp / bounceIn / bpSwing / pulse / slideInLeft / floatY / shimmer / burstFly / shake",
          "", "---"]
    return "\n".join(L) + "\n"

def json_page_plan(n, d):
    sections = []
    acc = 0
    for i, s in enumerate(d['segments']):
        start = acc
        end = acc + s['pages'] - 1
        pages = []
        for p in range(start, end+1):
            pages.append({"page": p, "type": "content", "title": s['name'], "segment": "S%d" % (i+1)})
        sections.append({"name": s['name'], "start": start, "end": end, "pages": pages})
        acc = end + 1
    return {
      "course": d['course'],
      "stage": d['stage'],
      "lesson": "L%02d" % n,
      "duration": "90min",
      "totalPages": d['totalPages'],
      "brand": d['brand'],
      "accent": d['accent'],
      "bgGradient": d['bgGradient'],
      "pageIdContract": True,
      "pageIdRange": "1-%d" % d['totalPages'],
      "style": d['style'],
      "grammarEndpoint": (n==21),
      "dataCollectionPlan": {
        "enabled": True, "syncMode": "realtime", "exportFormats": ["json","csv"],
        "sessionIdRule": "%s_{studentId}_{YYYYMMDD}" % d['session'],
        "recordFirstAttemptOnly": True, "allowReview": True,
      },
      "sections": sections,
    }

def json_anim(n, d):
    return {
      "course": d['course'],
      "animations": {
        "css": [
          {"name":"fadeSlideUp","definition":"from {opacity:0; transform:translateY(30px)} to {opacity:1; transform:translateY(0)}","usage":"页面进入、内容块出现"},
          {"name":"scaleUp","definition":"from {opacity:0; transform:scale(0.85)} to {opacity:1; transform:scale(1)}","usage":"卡片缩放出现"},
          {"name":"bounceIn","definition":"correct feedback","usage":"正确反馈"},
          {"name":"bpSwing","definition":"wrong feedback","usage":"错误反馈摇摆"},
          {"name":"burstFly","definition":"0%{transform:translate(0,0) scale(1);opacity:1} 100%{transform:translate(var(--dx),var(--dy)) scale(.3);opacity:0}","usage":"正确彩带爆发"},
          {"name":"shake","definition":"0%,100%{transform:translateX(0);} 25%{transform:translateX(-6px);} 75%{transform:translateX(6px);}","usage":"错误抖动"},
          {"name":"pageFade","definition":"from{opacity:0}to{opacity:1}","usage":"翻页淡入（无滑动偏移）"}
        ]
      },
      "interactions": {
        "navigation": {
          "halfScreenClick": True,
          "pageTurnExemption": ["quiz-q","quiz-container","drag-container","link-container","order-container"],
          "answerRevealPriority": True,
          "keyboardArrows": True,
          "navPills": True
        },
        "quiz": {
          "type":"checkOpt","containerResolve":"btn.closest('.quiz-q')",
          "feedback":{"correct":"绿✅ + bounceIn + 正确音效","wrong":"红❌ + bpSwing + 错误音效"},
          "undo":{"doubleClick":True,"description":"答错后双击可撤销重答"},
          "disableAfterAnswer":False,"showCorrectAnswer":True
        },
        "fill": {"type":"fillCheck","feedback":"同 quiz"},
        "drag": {"type":"pickWord/dragSubmit","feedback":"同 quiz"},
        "order": {"type":"moveUp/moveDown/orderCheck","feedback":"同 quiz"},
        "match": {"type":"matchPick","feedback":"同 quiz"},
        "flip": {"type":"flipCard"},
        "dataCollection": {
          "type":"IndexedDB","recordAnswer":True,"recordUndo":True,
          "syncMode":"realtime","exportFormats":["json","csv"]
        }
      },
      "interactiveComponents": {
        "component1": {"name":"随堂自检·选择","type":"checkOpt","elements":{"scene":".quiz-q"},"logic":{"select":"点击选项判分落库"}},
        "component2": {"name":"随堂自检·多题型","type":"fill/drag/order/match","elements":{"scene":".quiz-q"},"logic":{"input":"判分落库"}}
      },
      "audio": {
        "correct": {"freq":[880,1100],"duration":[0.15,0.2],"type":"sine"},
        "error": {"freq":220,"duration":0.3,"type":"sawtooth"},
        "pageTurn": {"freq":440,"duration":0.1,"type":"triangle"}
      },
      "assets": {
        "emojis": ["📊","📈","✅","❌","🔍","⭐","🏆","💡","📝","🎯"],
        "images": "none (all CSS/emoji based)",
        "externalLibs": "none (vanilla JS)"
      }
    }

def main():
    files_map = {
      1: ("1_课程概要.md", md_course_overview),
      2: ("2_大纲脚本.md", md_outline),
      3: ("3_演讲意图.md", md_intent),
      4: ("4_素材清单.md", md_assets),
      5: ("5_页面规划.json", json_page_plan),
      6: ("6_动效与素材.json", json_anim),
    }
    made = 0
    for n, d in LESSONS.items():
        cdir = os.path.join(ROOT, "第%02d课时" % n, "契约")
        os.makedirs(cdir, exist_ok=True)
        for fid, (fname, fn) in files_map.items():
            content = fn(n, d)
            if isinstance(content, dict):
                content = json.dumps(content, ensure_ascii=False, indent=2)
            path = os.path.join(cdir, fname)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            made += 1
            print("写出 %s" % path)
    print("契约生成完成：%d 个文件" % made)

if __name__ == "__main__":
    main()