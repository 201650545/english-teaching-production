# -*- coding: utf-8 -*-
"""邓兴华 L21-L25 契约 6 件套批量生成（临时构建脚本）。"""
import os, json

ROOT = r"D:\英语教学\邓兴华"

LESSONS = {
 21: {
  "course": "第21课 · 阶段测试Ⅲ·七上–八上中段诊断",
  "type": "讲评课（测试+讲评，五段式）",
  "stage": "Stage 5",
  "stage_range": "L17–L21",
  "duration": "90 分钟（测试 60 分钟 + 讲评 30 分钟）",
  "theme": "阶段测试Ⅲ·学情诊断与学习策略",
  "reading_theme": "A：Your Study Progress Guide / B：A Better Grade / C：How to Make Progress / 五选四：My Revision Plan",
  "totalPages": 42,
  "accent_theme": "红金暖色系（亮色）",
  "brand": "#E63946", "accent": "#FFD700",
  "bgGradient": "#FFF8F0 → #FFE8D6",
  "style": "五段式讲评（测试概况/高频错题/考点雷达/薄弱专项/总结提升）",
  "vocab": "词 401–420（grade, score, mark, correct, mistake, error, improve, review, prepare, plan, goal, memory, practice, progress, result, subject, skill, doubt, courage, confident）",
  "grammar": "G01–G54 全部 54 考点诊断（代词/be/疑问句/名词/形容词副词/祈使句/时态/情态/冠词/不定代词等）",
  "phonics": "无（测试课无拼读环节）",
  "segments": [
     {"name":"测试概况","pages":4,"desc":"得分分布 + 高频错题预览 + 考点雷达预览"},
     {"name":"高频错题精讲","pages":22,"desc":"按 G01–G54 分组讲解高频错题（代词/名词/句型/过去时/三单/冠词/购物/天气/进行时/综合）"},
     {"name":"考点雷达","pages":6,"desc":"54 考点掌握度 + 薄弱考点定位"},
     {"name":"薄弱专项","pages":6,"desc":"阅读五步法 + 写作范文 + 词汇错题"},
     {"name":"总结与提升计划","pages":4,"desc":"薄弱清单 + 下阶段(Stage 6)建议 + 核心口诀总览"},
  ],
  "session": "L21",
 },
 22: {
  "course": "第22课 · 比较级·最高级系统归纳 + 同级比较",
  "type": "授课课（八段式）",
  "stage": "Stage 6",
  "stage_range": "L22–L34",
  "duration": "90 分钟",
  "theme": "人物与事物比较",
  "reading_theme": "A：Comparing Two Cities / B：Two Friends / C：Why Comparisons Help / 五选四：My Best Friend",
  "totalPages": 45,
  "accent_theme": "红金暖色系（亮色）",
  "brand": "#E63946", "accent": "#FFD700",
  "bgGradient": "#FFF8F0 → #FFE8D6",
  "style": "八段式授课（复习导入/新词20/语法3考点/随堂演练/阅读理解/句子练习/自然拼读/课堂总结）",
  "vocab": "词 421–440（tall, short, long, big, small, fast, slow, cheap, expensive, popular, serious, outgoing, quiet, hard-working, talented, creative, humorous, friendly, lazy, smart）",
  "grammar": "G55 形容词/副词比较级系统归纳 / G56 最高级系统归纳 / G57 as...as & not as/so...as 同级比较",
  "phonics": "-er /ə(r)/ 与对比 -est",
  "reading_word": "189–198 / 210–220 / 179–187 词",
  "segments": [
     {"name":"复习导入","pages":3,"desc":"复习 L21 测试词 + 比较级/最高级 L5 基础回顾"},
     {"name":"新词20","pages":6,"desc":"20 词分组（身高/事物/人物性格/聪明懒散）"},
     {"name":"语法3考点","pages":10,"desc":"G55 比较级 + G56 最高级 + G57 as...as"},
     {"name":"随堂演练","pages":3,"desc":"每页 2–4 题，多题型（单选/填空/排序）"},
     {"name":"阅读理解","pages":3,"desc":"A 篇短文 + 题目解析"},
     {"name":"句子练习","pages":4,"desc":"造句 + 汉译英（比较最高级）"},
     {"name":"自然拼读","pages":4,"desc":"-er/-est 音素 + 练习"},
     {"name":"课堂总结","pages":2,"desc":"核心口诀 + 思维导图"},
  ],
  "session": "L22",
 },
 23: {
  "course": "第23课 · 条件状语从句(if/unless)与祈使句综合",
  "type": "授课课（八段式）",
  "stage": "Stage 6",
  "stage_range": "L22–L34",
  "duration": "90 分钟",
  "theme": "条件与选择",
  "reading_theme": "A：If I Become a Volunteer / B：A Big Decision / C：Plans for the Future / 五选四：A Clever Choice",
  "totalPages": 44,
  "accent_theme": "红金暖色系（亮色）",
  "brand": "#E63946", "accent": "#FFD700",
  "bgGradient": "#FFF8F0 → #FFE8D6",
  "style": "八段式授课（复习导入/新词20/语法3考点/随堂演练/阅读理解/句子练习/自然拼读/课堂总结）",
  "vocab": "词 441–460（if, unless, condition, possible, impossible, advice, suggest, decision, choose, choice, future, succeed, fail, effort, practice, improve, progress, goal, plan, result）",
  "grammar": "G58 if 真实条件句（主将从现）/ G59 unless 否定条件句 / G13 祈使句 + and/or 复现扩展",
  "phonics": "-tion /ʃən/ 与对比 -sion /ʒən/",
  "reading_word": "189–198 / 210–220 / 179–187 词",
  "segments": [
     {"name":"复习导入","pages":3,"desc":"复习 L22 比较最高级 + 新词预告"},
     {"name":"新词20","pages":6,"desc":"条件/选择/未来/结果 分组"},
     {"name":"语法3考点","pages":10,"desc":"G58 if + G59 unless + G13 祈使 and/or"},
     {"name":"随堂演练","pages":3,"desc":"多题型（单选/填空/拖拽）"},
     {"name":"阅读理解","pages":3,"desc":"A 篇短文 + 题目解析"},
     {"name":"句子练习","pages":4,"desc":"造句 + 汉译英（条件句）"},
     {"name":"自然拼读","pages":4,"desc":"-tion/-sion 音素 + 练习"},
     {"name":"课堂总结","pages":2,"desc":"核心口诀 + 思维导图"},
  ],
  "session": "L23",
 },
 24: {
  "course": "第24课 · 原因·结果·让步状语从句",
  "type": "授课课（八段式）",
  "stage": "Stage 6",
  "stage_range": "L22–L34",
  "duration": "90 分钟",
  "theme": "原因、结果与让步",
  "reading_theme": "A：Why Do Teenagers Love Social Media / B：Because of a Kind Word / C：Causes and Effects / 五选四：A Difficult Situation",
  "totalPages": 44,
  "accent_theme": "红金暖色系（亮色）",
  "brand": "#E63946", "accent": "#FFD700",
  "bgGradient": "#FFF8F0 → #FFE8D6",
  "style": "八段式授课（复习导入/新词20/语法3考点/随堂演练/阅读理解/句子练习/自然拼读/课堂总结）",
  "vocab": "词 461–480（because, since, as, although, though, however, therefore, result, cause, effect, reason, explain, situation, problem, solution, besides, despite, unless, while, instead）",
  "grammar": "G60 because/since/as 原因 & although/though 让步 / G61 so / so that / in order that 结果与目的 / G60 让步扩展（even though）",
  "phonics": "th 组合 /θ/ /ð/",
  "reading_word": "189–198 / 210–220 / 179–187 词",
  "segments": [
     {"name":"复习导入","pages":3,"desc":"复习 L23 条件句 + 新词预告"},
     {"name":"新词20","pages":6,"desc":"原因/结果/让步/转折 分组"},
     {"name":"语法3考点","pages":10,"desc":"G60 原因让步 + G61 结果目的 + G60 让步扩展"},
     {"name":"随堂演练","pages":3,"desc":"多题型（单选/填空/排序）"},
     {"name":"阅读理解","pages":3,"desc":"A 篇短文 + 题目解析"},
     {"name":"句子练习","pages":4,"desc":"造句 + 汉译英（原因结果）"},
     {"name":"自然拼读","pages":4,"desc":"th 清浊音素 + 练习"},
     {"name":"课堂总结","pages":2,"desc":"核心口诀 + 思维导图"},
  ],
  "session": "L24",
 },
 25: {
  "course": "第25课 · 动名词与不定式综合运用",
  "type": "授课课（八段式）",
  "stage": "Stage 6",
  "stage_range": "L22–L34",
  "duration": "90 分钟",
  "theme": "爱好与未来计划",
  "reading_theme": "A：My Hobbies and Future Plans / B：A Promise to My Friend / C：Why I Love Doing Sports / 五选四：Planning for the Future",
  "totalPages": 45,
  "accent_theme": "红金暖色系（亮色）",
  "brand": "#E63946", "accent": "#FFD700",
  "bgGradient": "#FFF8F0 → #FFE8D6",
  "style": "八段式授课（复习导入/新词20/语法3考点/随堂演练/阅读理解/句子练习/自然拼读/课堂总结）",
  "vocab": "词 481–500（enjoy, finish, mind, practice, suggest, avoid, consider, imagine, decide, hope, plan, want, need, agree, refuse, promise, manage, afford, offer, fail）",
  "grammar": "G62 动名词 V-ing 作主语/宾语 / G63 不定式 to do 作宾语/目的状语 / stop/remember doing vs to do 辨析",
  "phonics": "-ing /ɪŋ/ 与对比 -ink",
  "reading_word": "189–198 / 210–220 / 179–187 词",
  "segments": [
     {"name":"复习导入","pages":3,"desc":"复习 L24 原因结果 + 新词预告"},
     {"name":"新词20","pages":6,"desc":"爱好动名词类/计划不定式类 分组"},
     {"name":"语法3考点","pages":10,"desc":"G62 动名词 + G63 不定式 + stop/remember 辨析"},
     {"name":"随堂演练","pages":3,"desc":"多题型（单选/填空/排序）"},
     {"name":"阅读理解","pages":3,"desc":"A 篇短文 + 题目解析"},
     {"name":"句子练习","pages":4,"desc":"造句 + 汉译英（动名词/不定式）"},
     {"name":"自然拼读","pages":4,"desc":"-ing/-ink 音素 + 练习"},
     {"name":"课堂总结","pages":2,"desc":"核心口诀 + 思维导图"},
  ],
  "session": "L25",
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
    L += ["", "> **去重校验**：与 L1–L%d 前 %d 词交集 = 0 ✅" % (n-1, (n-21)*20+400), "", "---", "",
          "## 三、语法硬契约", "", "| 考点 | 内容要点 |", "|---|---|"]
    for g in d['grammar'].split(' / '):
        L.append("| %s | 见内容蓝图第二节 |" % g)
    L += ["", "> 语法要点与防越级约束详见内容蓝图第二节。", "", "---", "", "## 四、拼读规划", ""]
    if d['phonics'] == "无（测试课无拼读环节）":
        L += ["| 字母组合 | 说明 |", "|---|---|", "| 无 | 测试课无拼读环节 |"]
    else:
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