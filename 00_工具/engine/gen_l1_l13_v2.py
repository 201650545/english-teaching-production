# -*- coding: utf-8 -*-
"""
可复用 V2 课件生成器（内容驱动）· 许颖嘉 L1–L13 重做
调用 courseware_core 框架层，内置铁律样式（对称网格/grammar_cards/分段阅读/奶油面板/代词矩阵）。
用法：python gen_l1_l13_v2.py 1   （生成第1课）
"""
import os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = "D:/英语教学/01_数据"

sys.path.insert(0, HERE)
from courseware_core import page, vocab_cards, build_courseware

OLD = json.load(open(os.path.join(DATA_DIR, "content", "old_lessons.json"), encoding="utf-8"))

# ===================== 铁律样式 CSS =====================
CSS_EXTRA = """
/* 显眼小标题 */
.section-head{display:flex;align-items:center;gap:12px;margin:18px 0 14px;}
.sh-num{display:inline-flex;align-items:center;justify-content:center;width:34px;height:34px;border-radius:50%;
  background:var(--brand);color:#fff;font-size:18px;font-weight:700;flex:0 0 auto;box-shadow:0 2px 8px rgba(230,57,70,.3);}
.sh-title{font-size:23px;font-weight:700;color:var(--brand);}
/* 胶囊小标题 */
.sub-label{display:inline-block;padding:6px 16px;margin:14px 0 10px;border-radius:20px;
  background:linear-gradient(135deg,#FF8A5B,#E63946);color:#fff;font-size:16px;font-weight:600;box-shadow:0 2px 8px rgba(230,57,70,.2);}
/* 要点 2 列 */
.kp-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:10px 0;}
.kp-item{display:flex;align-items:flex-start;gap:10px;background:#fff;border-left:5px solid var(--brand);
  border-radius:12px;padding:12px 16px;box-shadow:0 2px 9px rgba(0,0,0,.06);}
.kp-item-full{grid-column:1/-1;}
.kp-dot{width:10px;height:10px;border-radius:50%;background:var(--accent);margin-top:6px;flex:0 0 auto;}
.kp-key{font-weight:700;color:var(--brand);}
.kp-desc{color:var(--text-secondary);line-height:1.7;}
/* 易错 2 列 */
.error-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:10px 0;}
.error-card{background:#fff5f5;border:2px solid var(--brand);border-radius:12px;padding:12px 14px;}
.error-card-full{grid-column:1/-1;}
.err-wrong{color:#c0392b;text-decoration:line-through;font-weight:700;font-size:17px;}
.err-arrow{color:var(--brand);font-weight:700;margin:4px 0;}
.err-right{color:var(--correct);font-weight:700;font-size:17px;}
/* 例句 2 列 */
.eg-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:10px 0;}
.eg-card{background:#f8fbff;border:2px solid var(--accent);border-radius:12px;padding:12px 16px;}
.eg-card-full{grid-column:1/-1;}
.eg-en{font-size:18px;font-weight:700;color:var(--text-primary);line-height:1.6;}
.eg-note{display:inline-block;margin-top:6px;padding:3px 10px;border-radius:12px;background:var(--accent-light);color:#7a5b00;font-size:14px;}
/* 语法要点色卡 6 色（2026-08-03 改版：标题条+记忆分级，解决"平铺无层次/标题不突出"） */
.rule-grid{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:12px 0;}
.rule-card{position:relative;border-radius:14px;overflow:hidden;color:#fff;box-shadow:0 4px 12px rgba(0,0,0,.16);}
.rule-card::before{content:'';position:absolute;left:0;top:0;bottom:0;width:6px;background:rgba(255,255,255,.32);}
.rule-key::before{width:8px;background:#FFD700;}
.rc-zhug{background:#3B82F6;} .rc-bin{background:#06A77D;} .rc-xing{background:#F59E0B;}
.rc-ming{background:#8B5CF6;} .rc-warn{background:#E63946;} .rc-qita{background:#14B8A6;}
.rc-cat{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:8px 12px 8px 16px;
  font-size:16px;font-weight:800;letter-spacing:1px;background:rgba(0,0,0,.20);}
.rc-badge{flex-shrink:0;font-size:12px;font-weight:800;padding:2px 9px;border-radius:10px;letter-spacing:0;white-space:nowrap;}
.rc-badge.key{background:#FFD700;color:#7a5b00;}
.rc-badge.warn{background:#fff;color:#C62828;}
.rc-badge.hint{background:rgba(255,255,255,.30);color:#fff;}
.rc-text{padding:10px 14px 12px 16px;font-size:16px;font-weight:500;line-height:1.55;}
/* 翻牌自检 */
.recall-grid{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin:12px 0;}
.recall-card{height:120px;perspective:800px;cursor:pointer;}
.recall-inner{position:relative;width:100%;height:100%;transition:transform .5s;transform-style:preserve-3d;}
.recall-card.flipped .recall-inner{transform:rotateY(180deg);}
.recall-front,.recall-back{position:absolute;inset:0;backface-visibility:hidden;border-radius:14px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;padding:10px;text-align:center;box-shadow:0 3px 10px rgba(0,0,0,.1);}
.recall-front{background:#fff;border:2px dashed var(--brand);}
.recall-back{background:var(--brand);color:#fff;transform:rotateY(180deg);}
.recall-q{font-size:16px;font-weight:700;color:var(--brand);}
.recall-hint{font-size:13px;color:var(--text-secondary);margin-top:6px;}
.recall-a{font-size:17px;font-weight:700;line-height:1.5;}
/* 阅读分段 */
.reading-passage{padding:14px 18px;background:#f8fbff;border:2px solid var(--accent);border-radius:14px;font-size:18px;line-height:1.9;margin:10px 0;}
.reading-passage p{margin:0 0 10px;}
.reading-passage p:last-child{margin-bottom:0;}
/* 选择题 */
.quiz-q{background:#fff;border:1px solid #ffe0d0;border-radius:12px;padding:14px 16px;margin:12px 0;box-shadow:0 2px 9px rgba(230,57,70,.07);}
.quiz-q .qq-text{font-size:17px;font-weight:600;margin-bottom:10px;}
.quiz-opt{display:block;width:100%;text-align:left;padding:9px 14px;margin:6px 0;border:2px solid #eee;border-radius:10px;
  font-size:16px;background:#fafafa;transition:all .15s;}
.quiz-opt:hover{border-color:var(--brand);}
.quiz-opt.opt-correct{background:var(--correct-row-bg);border-color:var(--correct);color:var(--correct);font-weight:700;}
.quiz-opt.opt-wrong{background:var(--error-row-bg);border-color:var(--error);color:var(--error);font-weight:700;}
/* 奶油底笔记面板 */
.body-text{background:#fffaf2;border:1px solid #ffe0b0;border-left:5px solid var(--accent);border-radius:12px;
  padding:14px 18px;color:var(--text-secondary);line-height:1.8;margin:10px 0;font-size:16px;}
.note-panel{background:#fffaf2;border:2px solid var(--accent);border-radius:14px;padding:14px 18px;margin:10px 0;line-height:1.8;}
.note-panel .np-title{font-weight:700;color:var(--brand);margin-bottom:6px;}
/* 自然拼读卡 */
.phonics-grid{display:grid;grid-template-columns:repeat(5,1fr);gap:12px;margin:12px 0;}
.phonics-card{background:#fff;border:2px solid var(--sop-blue);border-radius:14px;padding:14px 10px;text-align:center;box-shadow:0 2px 9px rgba(59,130,246,.12);}
.phonics-card .pc-letter{font-size:30px;font-weight:800;color:var(--sop-blue);}
.phonics-card .pc-word{font-size:17px;font-weight:700;margin-top:6px;}
.phonics-card .pc-cn{font-size:14px;color:var(--text-secondary);margin-top:4px;}
/* 知识图谱 */
.kmap{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0;}
.kmap-node{background:#fff;border:2px solid var(--sop-purple);border-radius:14px;padding:12px 14px;}
.kmap-node .kn-title{font-weight:700;color:var(--sop-purple);}
.kmap-node .kn-body{color:var(--text-secondary);font-size:15px;line-height:1.6;margin-top:4px;}
/* 人称代词彩色矩阵 */
.pm-table{width:100%;border-collapse:collapse;margin:12px 0;font-size:16px;}
.pm-table th,.pm-table td{border:1px solid #ffd0c0;padding:9px 8px;text-align:center;}
.pm-table th{background:#fff0e6;font-weight:700;color:var(--brand);}
.pm-table .pm-num{background:#fde2d8;}
.pm-table .pm-zhug{color:#3B82F6;font-weight:700;background:#fafdff;}
.pm-table .pm-bin{color:#06A77D;font-weight:700;background:#fafdff;}
.pm-table .pm-xing{color:#F59E0B;font-weight:700;background:#fafdff;}
.pm-table .pm-ming{color:#8B5CF6;font-weight:700;background:#fafdff;}
/* 封面 */
.cover-wrap{display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;text-align:center;}
.cover-title{font-size:46px;font-weight:800;color:var(--brand);text-shadow:0 3px 12px rgba(230,57,70,.2);}
.cover-sub{font-size:22px;color:var(--text-secondary);margin-top:10px;}
.cover-info{margin-top:24px;display:flex;gap:18px;flex-wrap:wrap;justify-content:center;}
.cover-info-num{background:#fff;border:2px solid var(--brand);border-radius:16px;padding:12px 22px;box-shadow:0 3px 12px rgba(230,57,70,.12);}
.cover-info-num .ci-label{font-size:14px;color:var(--text-secondary);}
.cover-info-num .ci-val{font-size:26px;font-weight:800;color:var(--brand);}
"""

# ===================== helper 渲染 =====================
def section_head(num, title):
    return '<div class="section-head"><span class="sh-num">%s</span><span class="sh-title">%s</span></div>' % (num, title)

def sub_label(text):
    return '<div class="sub-label">%s</div>' % text

def key_points(points):
    out = ['<div class="kp-grid">']
    n = len(points)
    for i, (kw, desc) in enumerate(points):
        cls = "kp-item kp-item-full" if (n % 2 == 1 and i == n - 1) else "kp-item"
        out.append('<div class="%s"><span class="kp-dot"></span><span class="kp-key">%s</span><span class="kp-desc">%s</span></div>' % (cls, kw, desc))
    out.append('</div>')
    return "\n".join(out)

def error_callout(items):
    out = ['<div class="error-grid">']
    n = len(items)
    for i, (wrong, right) in enumerate(items):
        cls = "error-card error-card-full" if (n % 2 == 1 and i == n - 1) else "error-card"
        out.append('<div class="%s"><div class="err-wrong">%s</div><div class="err-arrow">→</div><div class="err-right">%s</div></div>' % (cls, wrong, right))
    out.append('</div>')
    return "\n".join(out)

def example_section(examples):
    out = ['<div class="eg-grid">']
    n = len(examples)
    for i, (en, cn) in enumerate(examples):
        cls = "eg-card eg-card-full" if (n % 2 == 1 and i == n - 1) else "eg-card"
        out.append('<div class="%s"><div class="eg-en">%s</div><div class="eg-note">%s</div></div>' % (cls, en, cn))
    out.append('</div>')
    return "\n".join(out)

COLORKEY = {"主格": "rc-zhug", "宾格": "rc-bin", "形物": "rc-xing", "名物": "rc-ming", "警示": "rc-warn", "其他": "rc-qita",
            "用法": "rc-zhug", "构成": "rc-bin", "易错": "rc-xing", "例句": "rc-ming", "注意": "rc-warn", "口诀": "rc-qita"}
def grammar_cards(cards):
    out = ['<div class="rule-grid">']
    for cat, text in cards:
        ck = COLORKEY.get(cat, "rc-qita")
        out.append('<div class="rule-card %s"><div class="rc-cat">%s</div><div class="rc-text">%s</div></div>' % (ck, cat, text))
    out.append('</div>')
    return "\n".join(out)

def recall_grid(cards):
    out = ['<div class="recall-grid">']
    for q, a in cards:
        out.append('<div class="recall-card" onclick="flipCard(this)"><div class="recall-inner">'
                   '<div class="recall-front"><div class="recall-q">%s</div><div class="recall-hint">点击翻牌自检</div></div>'
                   '<div class="recall-back"><div class="recall-a">%s</div></div></div></div>' % (q, a))
    out.append('</div>')
    return "\n".join(out)

def reading_block(title, paras, questions):
    out = [section_head("读", title)]
    out.append('<div class="reading-passage">')
    for p in paras:
        out.append('<p>%s</p>' % p)
    out.append('</div>')
    for qnum, q, opts in questions:
        out.append('<div class="quiz-q"><div class="qq-text">%s. %s</div>' % (qnum, q))
        for letter, text, cor in opts:
            out.append('<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text))
        out.append('</div>')
    return "\n".join(out)

def five_pick_block(title, paras, options, answers):
    out = [section_head("读", title)]
    out.append('<div class="reading-passage">')
    for p in paras:
        out.append('<p>%s</p>' % p)
    out.append('</div>')
    out.append('<div class="body-text">从下面 A–E 选项中选出最佳句子填入短文空白处。</div>')
    for num in sorted(answers.keys()):
        ans = answers[num]
        out.append('<div class="quiz-q"><div class="qq-text">__（%d）__ 应填：</div>' % num)
        for letter, text in options:
            cor = '1' if letter == ans else '0'
            out.append('<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text))
        out.append('</div>')
    return "\n".join(out)

def phonics_block(items):
    out = [section_head("拼", "自然拼读 · 短元音"), sub_label("元音字母 a / e / i / o / u 的短音"), '<div class="phonics-grid">']
    for letter, word, cn in items:
        out.append('<div class="phonics-card"><div class="pc-letter">%s</div><div class="pc-word">%s</div><div class="pc-cn">%s</div></div>' % (letter, word, cn))
    out.append('</div>')
    return "\n".join(out)

def pronoun_matrix():
    rows = [
        ("单数", "第一", "I", "me", "my", "mine"),
        ("单数", "第二", "you", "you", "your", "yours"),
        ("单数", "第三(男)", "he", "him", "his", "his"),
        ("单数", "第三(女)", "she", "her", "her", "hers"),
        ("复数", "第一", "we", "us", "our", "ours"),
        ("复数", "第二", "you", "you", "your", "yours"),
        ("复数", "第三", "they", "them", "their", "theirs"),
    ]
    out = ['<table class="pm-table">']
    out.append('<tr><th class="pm-num">数</th><th>人称</th><th class="pm-zhug">主格</th><th class="pm-bin">宾格</th><th class="pm-xing">形物代</th><th class="pm-ming">名物代</th></tr>')
    last_num = None
    for num, person, zhug, bin_, xing, ming in rows:
        if num != last_num:
            cnt = sum(1 for r in rows if r[0] == num)
            out.append('<tr><th class="pm-num" rowspan="%d">%s</th>' % (cnt, num))
            last_num = num
        else:
            out.append('<tr>')
        out.append('<th>%s</th><td class="pm-zhug">%s</td><td class="pm-bin">%s</td><td class="pm-xing">%s</td><td class="pm-ming">%s</td></tr>' % (person, zhug, bin_, xing, ming))
    out.append('</table>')
    return "\n".join(out)

# ===================== L1 内容 =====================
VOCAB_L1 = [
    ("name","/neɪm/","n.","名字","first name / family name","My name is Tom.","名字→name，a 像名字的框"),
    ("friend","/frend/","n.","朋友","make friends","He is my good friend.","朋友→friend，end 结尾"),
    ("phone","/fəʊn/","n.","电话","phone number","Call me on my phone.","电话→phone，ph 发音/f/"),
    ("number","/ˈnʌmbə/","n.","数字；号码","phone number","What's your number?","号码→number，num 开头"),
    ("school","/skuːl/","n.","学校","go to school","I like my school.","学校→school，ch 发音/k/"),
    ("teacher","/ˈtiːtʃə/","n.","老师","English teacher","She is a teacher.","教→teach+er 人"),
    ("student","/ˈstjuːdnt/","n.","学生","a new student","I am a student.","学→stud+ent 人"),
    ("class","/klɑːs/","n.","班级；课","in Class 3","We are in the same class.","班级→class，cl 开头"),
    ("China","/ˈtʃaɪnə/","n.","中国","in China","I am from China.","中国→China，首字母大写"),
    ("English","/ˈɪŋɡlɪʃ/","n./adj.","英语；英国的","English teacher","I speak English.","英语→English，sh 发音/ʃ/"),
    ("his","/hɪz/","pron.","他的","his name","His book is red.","他的→his（形物代）"),
    ("her","/hɜː/","pron.","她的","her friend","Her pen is new.","她的→her（形物代）"),
    ("their","/ðeə/","pron.","他们的","their school","Their class is big.","他们的→their"),
    ("our","/ˈaʊə/","pron.","我们的","our teacher","Our room is tidy.","我们的→our"),
    ("yours","/jɔːz/","pron.","你的（名物）","a friend of yours","Is this book yours?","你的→yours（名物代）"),
    ("welcome","/ˈwelkəm/","v./int.","欢迎","welcome to","Welcome to our class!","欢迎→welcome，come 来"),
    ("meet","/miːt/","v.","遇见；结识","nice to meet you","I meet a new boy.","遇见→meet，ee 长音/iː/"),
    ("nice","/naɪs/","adj.","好的；友好的","nice to","She is a nice girl.","友好→nice，i 发/aɪ/"),
    ("spell","/spel/","v.","拼写","spell it","How do you spell it?","拼写→spell，ll 双写"),
    ("zero","/ˈzɪərəʊ/","num.","零","number zero","Zero is a number.","零→zero，z 开头"),
]

GRAMMAR_L1 = [
    {
        "title": "语法① · 人称代词主格与宾格（I/me, he/him, she/her）",
        "usage": "主格站在动词前面作<b>主语</b>；宾格站在动词或介词后面作<b>宾语</b>。主语用主格，宾语用宾格，二者不可混用。",
        "examples": [
            ("I am a new student.", "我是一名新生。（主格 I 作主语）"),
            ("He helps me.", "他帮助我。（宾格 me 作宾语）"),
            ("She likes him.", "她喜欢他。（him 宾格作宾语）"),
            ("We meet them at school.", "我们在学校遇见他们。"),
            ("This gift is for her.", "这份礼物是给她的。（介词 for 后用宾格）"),
            ("You teach us English.", "你教我们英语。（宾格 us 作宾语）"),
            ("They invite her to the party.", "他们邀请她参加派对。"),
            ("The letter is from him.", "这封信来自他。（介词 from 后用宾格）"),
        ],
        "keypoints": [
            ("主格＝主语", "在句子中充当动作发出者，位于动词之前：I / we / you / he / she / it / they。"),
            ("宾格＝宾语", "在动词或介词之后充当动作承受者：me / us / you / him / her / it / them。"),
            ("介词后用宾格", "with / for / to / from 等介词后面一律用宾格，如 with me、for him。"),
            ("不可混用", "主语位置绝不能用宾格（× Me am…），宾语位置绝不能用主格（× helps I）。"),
        ],
        "errors": [
            ("Me am a student.", "I am a student."),
            ("He helps I.", "He helps me."),
            ("This is for he.", "This is for him."),
            ("Her likes apples.", "She likes apples."),
        ],
        "mnemonic": "主格站前当主语，宾格跟后作宾语；动介后面用宾格，I-me / he-him / she-her 记清楚。",
        "cards": [("主格","I / we / you / he / she / it / they（作主语）"),
                  ("宾格","me / us / you / him / her / it / them（作宾语）"),
                  ("警示","介词（with/for/to）后必须用宾格，不可用主格。")],
    },
    {
        "title": "语法② · 形容词性与名词性物主代词（my/mine, your/yours）",
        "usage": "形容词性物主代词<b>后面必须加名词</b>（my book）；名词性物主代词<b>单独使用</b>，相当于“形物代＋名词”（mine = my book）。",
        "examples": [
            ("This is my book.", "这是我的书。（形物代＋名词）"),
            ("This book is mine.", "这本书是我的。（名物代单独用）"),
            ("Is this your pen?", "这是你的钢笔吗？（形物代＋名词）"),
            ("The pen is yours.", "钢笔是你的。（名物代单独）"),
            ("His car is new; hers is old.", "他的车是新的，她的是旧的。"),
            ("The red bag is hers.", "红色包是她的。（名物代单独）"),
            ("Our cat is small; theirs is big.", "我们的猫小，他们的大。"),
            ("Is this pen his or mine?", "这支笔是他的还是我的？"),
        ],
        "keypoints": [
            ("形物代后跟名", "my / your / his / her / its / our / their 必须再加名词，不能单独结尾。"),
            ("名物代单独用", "mine / yours / his / hers / its / ours / theirs 自带“名词”，后面不加名词。"),
            ("两者可互换", "my book = the book is mine，表达“我的”两种形式。"),
            ("his / its 同形", "his、its 的形物代与名物代拼写相同，靠后接有无名词判断。"),
        ],
        "errors": [
            ("This book is my.", "This book is mine."),
            ("Mine book is red.", "My book is red."),
            ("The car is your.", "The car is yours."),
            ("Her is a teacher.", "She is a teacher."),
        ],
        "mnemonic": "形物代后必跟名，名物代后莫加名；my-mine / your-yours，his-his / its-its 要分清。",
        "cards": [("形物","my / your / his / her / its / our / their（＋名词）"),
                  ("名物","mine / yours / his / hers / its / ours / theirs（单独用）"),
                  ("警示","句末单独“我的”用 mine，不可用 my。")],
    },
    {
        "title": "语法③ · be 动词（am/is/are）与人称搭配",
        "usage": "be 动词随主语的人称和数变化：<b>我(I)用 am，你(you)用 are，is 连着他(it)她(she)它(he)；复数(we/you/they)全用 are</b>。",
        "examples": [
            ("I am a student.", "我是一名学生。（I → am）"),
            ("He is my brother.", "他是我的兄弟。（he → is）"),
            ("She is a teacher.", "她是一位老师。（she → is）"),
            ("They are good friends.", "他们是好朋友。（they → are）"),
            ("We are in Class 3.", "我们在三班。（we → are）"),
            ("You are a good student.", "你是个好学生。（you → are）"),
            ("It is a nice day.", "天气真好。（it → is）"),
            ("Those books are new.", "那些书是新的。（复数 → are）"),
        ],
        "keypoints": [
            ("I 用 am", "第一人称单数 I 搭配 am。"),
            ("you 用 are", "第二人称 you（单/复）搭配 are。"),
            ("he/she/it 用 is", "第三人称单数搭配 is。"),
            ("复数用 are", "we / you / they 等复数主语搭配 are。"),
        ],
        "errors": [
            ("I is a boy.", "I am a boy."),
            ("He are tall.", "He is tall."),
            ("They is students.", "They are students."),
            ("She am happy.", "She is happy."),
        ],
        "mnemonic": "我用 am 你用 are，is 连着他她它；复数主语全用 are，be 动搭配要记牢。",
        "cards": [("am","I（我）"),
                  ("is","he / she / it（他她它）"),
                  ("are","you / we / they（你我们他们）"),
                  ("警示","be 动词必须与主语人称一致，不可乱搭。")],
    },
]

GRAMMAR_NOTE_L1 = {
    1: "人称代词格变化常在完形填空与语法填空中设题，尤以“介词后误用主格”“并列主语误用宾格”为高频陷阱。",
    2: "形物代/名物代辨析是湖南中考省卷常客，命题点多在于“句末单独用 my”“后接名词用 mine”等混淆。",
    3: "be 动词与人称一致是基础分，单选、填空、改错都会考，务必做到“见主语即反应 am/is/are”。",
}

RECALL_L1 = [
    ("“我”作主语用哪个代词？", "主格 I（I am a student.）"),
    ("动词后面“我”用哪个？", "宾格 me（He helps me.）"),
    ("“我的书”用 my 还是 mine？", "my book（形物代＋名词）"),
    ("“这本书是我的”用 my 还是 mine？", "mine（名物代单独用）"),
    ("“我是”be 动词用哪个？", "am（I am…）"),
    ("“他是/她是”be 动词用哪个？", "is（He/She is…）"),
    ("“我们是/你们是”be 动词？", "are（We/You are…）"),
    ("介词 for 后面用主格还是宾格？", "宾格（for him / for her）"),
    ("“他们的”形物代？", "their（their school）"),
    ("“他们的”名物代？", "theirs（The book is theirs.）"),
    ("“她”作宾语用哪个？", "her（He helps her.）"),
    ("“你”的 be 动词？", "are（You are…）"),
]

PHONICS_L1 = [
    ("a","cat /kæt/","猫·短音/æ/"),
    ("e","bed /bed/","床·短音/e/"),
    ("i","sit /sɪt/","坐·短音/ɪ/"),
    ("o","dog /dɒg/","狗·短音/ɒ/"),
    ("u","cup /kʌp/","杯·短音/ʌ/"),
    ("a","map /mæp/","地图·短音/æ/"),
    ("e","pen /pen/","钢笔·短音/e/"),
    ("i","pig /pɪg/","猪·短音/ɪ/"),
    ("o","box /bɒks/","盒子·短音/ɒ/"),
    ("u","bus /bʌs/","公交·短音/ʌ/"),
]

QUIZ_L1 = [
    ("1. — ____ your name Tom? — Yes, it ____.", [("A","Is; is","1"),("B","Am; is","0"),("C","Are; am","0"),("D","Is; am","0")]),
    ("2. This is ____ book. That book is ____.", [("A","my; your","0"),("B","mine; yours","0"),("C","my; yours","1"),("D","mine; your","0")]),
    ("3. He helps ____ with English.", [("A","I","0"),("B","my","0"),("C","me","1"),("D","we","0")]),
    ("4. — Are they your friends? — ____.", [("A","Yes, they are","1"),("B","Yes, they is","0"),("C","No, they is","0"),("D","Yes, he are","0")]),
    ("5. The gift is for ____. It is ____ gift.", [("A","her; her","0"),("B","she; her","0"),("C","her; hers","0"),("D","her; his","1")]),
    ("6. We ____ in Class 2 and they ____ in Class 3.", [("A","am; is","0"),("B","is; are","0"),("C","is; is","0"),("D","are; are","1")]),
]

QUIZ_EXTRA_L1 = [
    ("7. — Is this ____ pencil? — No, it's ____.", [("A","your; mine","1"),("B","your; my","0"),("C","yours; mine","0"),("D","yours; my","0")]),
    ("8. ____ and ____ are in the same class.", [("A","I; he","0"),("B","Me; him","0"),("C","I; him","0"),("D","He; I","1")]),
    ("9. Her name ____ Lucy and ____ from England.", [("A","is; she is","1"),("B","are; she is","0"),("C","is; her is","0"),("D","am; she","0")]),
    ("10. These books are ____. Give ____ to ____.", [("A","their; them; they","0"),("B","theirs; them; them","0"),("C","theirs; them; their","0"),("D","theirs; them; they","1")]),
    ("11. — How ____ your parents? — ____ fine.", [("A","is; He is","0"),("B","are; They are","1"),("C","am; They are","0"),("D","are; We are","0")]),
    ("12. This is ____ dog. ____ name is Coco.", [("A","we; It","0"),("B","our; Its","1"),("C","us; Its","0"),("D","our; It","0")]),
]

QUIZ_EXTRA2_L1 = [
    ("13. — ____ this your eraser? — No, it ____.", [("A","Is; isn't","1"),("B","Are; aren't","0"),("C","Am; am not","0"),("D","Is; is","0")]),
    ("14. He ____ my brother and I ____ his friend.", [("A","am; am","0"),("B","is; am","1"),("C","are; is","0"),("D","is; is","0")]),
    ("15. — Are these ____ shoes? — Yes, they are ____.", [("A","you; your","0"),("B","your; your","0"),("C","your; yours","1"),("D","yours; yours","0")]),
    ("16. We ____ in the library and they ____ in the classroom.", [("A","am; is","0"),("B","is; are","0"),("C","are; is","0"),("D","are; are","1")]),
    ("17. ____ and ____ are from England.", [("A","He; she","1"),("B","Him; her","0"),("C","He; her","0"),("D","Him; she","0")]),
    ("18. This gift is for ____. ____ likes it.", [("A","he; He","0"),("B","him; He","1"),("C","his; His","0"),("D","him; His","0")]),
    ("19. The blue pen is ____. ____ pen is red.", [("A","my; My","0"),("B","mine; My","0"),("C","mine; My","1"),("D","my; Mine","0")]),
    ("20. — ____ your parents teachers? — Yes, ____.", [("A","Is; he is","0"),("B","Are; we are","0"),("C","Am; they are","0"),("D","Are; they are","1")]),
]

DRILL_L1 = [
    ("我是新生。", "I am a new student."),
    ("这是我的书。", "This is my book."),
    ("他是我的兄弟。", "He is my brother."),
    ("这本书是你的。", "This book is yours."),
    ("我们在三班。", "We are in Class 3."),
    ("她是一名老师。", "She is a teacher."),
    ("她的名字是露西。", "Her name is Lucy."),
    ("他们是好朋友。", "They are good friends."),
    ("欢迎来到我们学校！", "Welcome to our school!"),
    ("你能拼写它吗？", "Can you spell it?"),
    ("那是他的钢笔。", "That is his pen."),
    ("我和他是同学。", "He and I are classmates."),
]

CLOZE_L1 = [
    ("Hello! I am a new ___ .", [("student","1"),("teacher","0"),("school","0")]),
    ("My ___ is Tom.", [("name","1"),("friend","0"),("number","0")]),
    ("I am from ___ .", [("China","1"),("English","0"),("class","0")]),
    ("My English ___ is Mr. Zhang.", [("teacher","1"),("student","0"),("friend","0")]),
    ("___ to our class!", [("Welcome","1"),("Meet","0"),("Spell","0")]),
    ("Can you ___ your name?", [("spell","1"),("meet","0"),("welcome","0")]),
    ("This is my good ___ .", [("friend","1"),("phone","0"),("number","0")]),
    ("She is an English ___ .", [("teacher","1"),("student","0"),("class","0")]),
]

CROSS_L1 = [
    ("名字", "name", [("name","1"),("nice","0"),("number","0")]),
    ("朋友", "friend", [("friend","1"),("family","0"),("phone","0")]),
    ("老师", "teacher", [("student","0"),("teacher","1"),("school","0")]),
    ("学生", "student", [("class","0"),("student","1"),("China","0")]),
    ("电话", "phone", [("phone","1"),("pen","0"),("book","0")]),
    ("欢迎", "welcome", [("welcome","1"),("meet","0"),("spell","0")]),
    ("遇见", "meet", [("meet","1"),("make","0"),("help","0")]),
    ("拼写", "spell", [("say","0"),("spell","1"),("speak","0")]),
]

# 近义词/形近词辨析
VDIFF_L1 = [
    ("name / nice", "name 名字；nice 友好的——形近易混，记“name 有 a 是名，nice 有 i 是善”。"),
    ("friend / family", "friend 朋友；family 家庭——都含 f，记“friend 友人，family 家人”。"),
    ("phone / photo", "phone 电话；photo 照片——ph 发音同 /f/，记“phone 通，photo 图”。"),
    ("teacher / student", "teacher 老师（教的人）；student 学生（学的人）——角色相对。"),
    ("number / member", "number 数字/号码；member 成员——number 数得清，member 是成员。"),
    ("her / his", "her 她的（形物/宾格）；his 他的——性别不同，别写反。"),
]

# 听写自测（点击翻牌）
VDICT_L1 = [
    ("名字", "name"), ("朋友", "friend"), ("电话", "phone"), ("老师", "teacher"),
    ("学生", "student"), ("学校", "school"), ("班级", "class"), ("中国", "China"),
    ("欢迎", "welcome"), ("遇见", "meet"), ("拼写", "spell"), ("零", "zero"),
]

# 语法考点中考考法小测（每考点 2 题，答案分布平衡）
GEXTRA_L1 = {
    1: [("1. 选正确句子：", [("A","Me and he are friends.","0"),("B","He and I are friends.","1"),("C","Him and I are friends.","0"),("D","He and me are friends.","0")]),
        ("2. 介词后应选：This is a gift for ____.", [("A","him","1"),("B","he","0"),("C","his","0"),("D","he's","0")])],
    2: [("3. 选正确句子：", [("A","This book is my.","0"),("B","This is mine book.","0"),("C","This book is mine.","1"),("D","This book is my's.","0")]),
        ("4. 填空：The red pen is ____ (your).", [("A","your","0"),("B","yours","1"),("C","you","0"),("D","you're","0")])],
    3: [("5. 选正确句子：", [("A","I is a boy.","0"),("B","He are tall.","0"),("C","They is students.","0"),("D","She is happy.","1")]),
        ("6. 填空：You and I ____ (be) good friends.", [("A","am","0"),("B","is","0"),("C","are","1"),("D","be","0")])],
}

# 随堂改错专练（答案分布 A,B,C,A,B）
ERRDRILL_L1 = [
    ("找出错误并改正：Me am a new student.", [("A","Me→I","1"),("B","am→is","0"),("C","student→students","0")]),
    ("找出错误并改正：He helps I with English.", [("A","He→Him","0"),("B","I→me","1"),("C","helps→help","0")]),
    ("找出错误并改正：This book is my.", [("A","is→are","0"),("B","book→books","0"),("C","my→mine","1")]),
    ("找出错误并改正：They is in Class 3.", [("A","They→We","0"),("B","is→are","1"),("C","Class→class","0")]),
    ("找出错误并改正：Her likes apples.", [("A","Her→She","1"),("B","likes→like","0"),("C","apples→apple","0")]),
]

# 代词填空综合（语篇，答案分布 B,A,A,C）
PRONFILL_L1 = [
    ("1. ___ (I) name is Tom. ___ (I) am a student.", [("A","I; I","0"),("B","My; I","1"),("C","My; Me","0")]),
    ("2. This is ___ (we) dog. The dog is ___ (we).", [("A","our; ours","1"),("B","we; we","0"),("C","us; our","0")]),
    ("3. He helps ___ (they) and ___ (they) help ___ (he).", [("A","them; they; him","1"),("B","they; them; he","0"),("C","them; them; he","0")]),
    ("4. — Is this pencil ___ (you)? — Yes, it is ___ (you).", [("A","your; your","0"),("B","yours; your","0"),("C","yours; yours","1")]),
]

# ===================== 构建 L1 =====================
def build_lesson_1():
    pages = {}
    seg = {}
    p = 1
    def add(inner, seg_id, title="第1课 · 代词、be动词与问候句型", subtitle="Making New Friends · 七上基础"):
        nonlocal p
        pages[p] = page(p, title, subtitle, inner, active=(p == 1))
        seg.setdefault(seg_id, [p, p])
        seg[seg_id][1] = p
        p += 1

    # ---- 段1 复习导入 ----
    cover = ('<div class="cover-wrap"><div class="cover-title">第 1 课</div>'
             '<div class="cover-sub">代词、be 动词与问候句型 · 七上基础</div>'
             '<div class="cover-info">'
             '<div class="cover-info-num"><div class="ci-label">新词</div><div class="ci-val">20</div></div>'
             '<div class="cover-info-num"><div class="ci-label">语法考点</div><div class="ci-val">3</div></div>'
             '<div class="cover-info-num"><div class="ci-label">页数</div><div class="ci-val">42</div></div>'
             '</div></div>')
    add(cover, 1, "第1课 · 代词、be动词与问候句型", "封面")
    goal = (section_head("标", "本课学习目标") +
            key_points([("20 中考高频词", "name/friend/phone 等校园交际核心词，滚动复现。"),
                        ("3 大语法考点", "①人称代词主格宾格 ②形容词/名词性物主代词 ③be动词 am/is/are。"),
                        ("阅读主题", "Making New Friends at School，训练细节定位。"),
                        ("自然拼读", "短元音 a/e/i/o/u 拼读规律。")]) +
            '<div class="kmap">' +
            '<div class="kmap-node"><div class="kn-title">词汇</div><div class="kn-body">20 个校园交际高频词，含人称/物主代词。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">语法</div><div class="kn-body">主格宾格、形物名物、be 动词 am/is/are。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">阅读</div><div class="kn-body">A/B 叙事细节 + C 五选四逻辑衔接。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">拼读</div><div class="kn-body">短元音 a/e/i/o/u 的 CVC 拼读。</div></div>' +
            '</div>' +
            '<div class="note-panel"><div class="np-title">先测后学提示</div>先翻下面的卡片自检已学知识，再进入系统讲解。</div>' +
            '<div class="note-panel"><div class="np-title">闯关目标</div>能正确区分主格/宾格、形物/名物代词，并能随主语熟练选用 am/is/are，即可通关本课。</div>')
    add(goal, 1)
    rev = (section_head("测", "复习检测 · 翻牌自检") +
           '<div class="body-text">点击卡片翻面，看看这些基础知识点你都掌握了吗？</div>' +
           recall_grid(RECALL_L1) +
           '<div class="note-panel"><div class="np-title">检测说明</div>翻牌后对照答案，错一处即回到对应语法页重学，务必全对再进入新词。</div>')
    add(rev, 1)
    warm = (section_head("测", "易混知识预热") +
            key_points([("主格 or 宾格?", "动词前用主格，动词/介词后用宾格。"),
                        ("形物 or 名物?", "后接名词用形物(my book)，单独用名物(mine)。"),
                        ("am/is/are?", "随主语人称变化，不可乱搭。")]) +
            '<div class="note-panel"><div class="np-title">学习路径</div>先判断词在句中“站前（主语）还是跟后（宾语/介词后）”，再决定主格/宾格；先看“后有无名词”再决定形物/名物。</div>' +
            '<div class="sub-label">语境示例</div>' +
            example_section([("I like her.", "I 主格作主语，her 宾格作宾语"),
                             ("This is my dog.", "my 形物代＋名词"),
                             ("The dog is mine.", "mine 名物代单独用"),
                             ("They are happy.", "they 复数用 are")]) +
            '<div class="note-panel"><div class="np-title">本课主线</div>'
            '代词（主格/宾格/物主）+ be 动词，是七上最核心的语法地基。</div>')
    add(warm, 1)

    # ---- 段2 新词20 ----
    add(section_head("词", "新词 ①（1–10）· 校园交际核心词") + sub_label("点击卡片记忆 · 含音标/搭配/例句") + vocab_cards(VOCAB_L1[:10]), 2)
    add(section_head("词", "新词 ②（11–20）· 代词与交际动词") + sub_label("含音标/搭配/例句") + vocab_cards(VOCAB_L1[10:]), 2)
    add(section_head("词", "新词速记 · 分组策略") +
        '<div class="note-panel"><div class="np-title">记忆策略</div>'
        '① 按“人名/学校/物品/代词”分组记；② 用搭配短语带动单词；③ 每词造一句。</div>' +
        key_points([("人称代词组", "I/me, he/him, she/her, we/us, they/them。"),
                    ("物主代词组", "my/mine, your/yours, his, her/hers, our/ours, their/theirs。"),
                    ("校园名词组", "school/teacher/student/class/China/English。"),
                    ("交际动词组", "meet/welcome/spell/nice/name/number/phone/friend。")]) +
        '<div class="sub-label">高频搭配</div>' +
        key_points([("first name", "名字（与 family name 相对）"),
                    ("phone number", "电话号码"),
                    ("English teacher", "英语老师"),
                    ("good friend", "好朋友"),
                    ("welcome to", "欢迎来到…")]) +
        '<div class="note-panel"><div class="np-title">词族扩展</div>'
        '① 动词变人：teach→teacher, study→student, help→helper；② 名物代＝形物代＋名词：my book＝mine；'
        '③ 国家→语言：China→Chinese（本课 English 同源）；④ 数字链：zero/one/two… 与 number 搭配。</div>', 2)
    cloze_inner = section_head("词", "词汇运用 · 选词填空")
    for q, opts in CLOZE_L1:
        cloze_inner += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for w, cor in opts:
            cloze_inner += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s</button>' % (cor, w)
        cloze_inner += '</div>'
    cloze_inner += '<div class="body-text">用本课新词补全句子，巩固词义与搭配。</div>'
    cloze_inner += '<div class="note-panel"><div class="np-title">解析</div>① student 与 new 搭配；② name 回答“名字”；③ China 表国籍；④ teacher 对应 English；⑤ Welcome 表欢迎；⑥ spell 与 name 搭配；⑦ friend 好朋友；⑧ teacher 表职业。</div>'
    add(cloze_inner, 2)
    vdiff = (section_head("词", "新词 ③ · 近义词/形近词辨析") + sub_label("形近词成对记，避免拼写混淆") +
             key_points([(kw, desc) for kw, desc in VDIFF_L1]) +
             '<div class="note-panel"><div class="np-title">辨析口诀</div>形近看首尾字母，词义靠搭配；name/nice、phone/photo 最易混，多写三遍。</div>' +
             '<div class="body-text">辨析不是死记，而是“见词想搭档”：name→first name，phone→number，teacher→student 成对出现。</div>')
    add(vdiff, 2)
    vdict = (section_head("词", "新词 ④ · 听写自测（点击翻牌）") + sub_label("看中文，翻牌核对英文拼写") +
             recall_grid([(cn, en) for cn, en in VDICT_L1]) +
             '<div class="body-text">家长可对照此页听写；错词请回到新词页重记。</div>' +
             '<div class="note-panel"><div class="np-title">记忆提示</div>先记“人称/物主”代词（I/me/my/mine…），再记“校园/交际”名词与动词，分组记忆效率更高。</div>')
    add(vdict, 2)

    # ---- 段3 语法精讲 ----
    for gi, g in enumerate(GRAMMAR_L1, 1):
        t = g["title"]
        pa = (section_head("法", "考点%d · 构成与用法 + 例句" % gi) +
              '<div class="sub-label">一 · 构成与用法</div>' +
              '<div class="body-text">%s</div>' % g["usage"] +
              '<div class="sub-label">二 · 典型例句</div>' +
              example_section(g["examples"]) +
              '<div class="sub-label">三 · 中考怎么考</div>' +
              '<div class="note-panel"><div class="np-title">考法预警</div>%s</div>' % GRAMMAR_NOTE_L1.get(gi, ""))
        add(pa, 3, t, "语法精讲")
        pb = (section_head("法", "考点%d · 易错 + 口诀 + 色卡" % gi) +
              '<div class="sub-label">三 · 高频易错</div>' +
              error_callout(g["errors"]) +
              '<div class="sub-label">四 · 记忆口诀</div>' +
              '<div class="note-panel"><div class="np-title">口诀</div>%s</div>' % g["mnemonic"] +
              '<div class="sub-label">五 · 语法要点色卡</div>' +
              grammar_cards(g["cards"]))
        add(pb, 3, t, "语法精讲")
        pc = section_head("法", "考点%d · 中考考法·即时小测" % gi)
        for q, opts in GEXTRA_L1.get(gi, []):
            pc += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
            for letter, text, cor in opts:
                pc += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
            pc += '</div>'
        pc += '<div class="body-text">中考常在语篇中混考“格”与“be 动词”，看清主语人称再下笔。</div>'
        add(pc, 3, t, "语法精讲")
    add(section_head("法", "代词全家福 · 彩色矩阵") + sub_label("主格/宾格/形物代/名物代 一网打尽") +
        pronoun_matrix() +
        '<div class="note-panel"><div class="np-title">记忆顺序</div>'
        'I, me, my, mine / you, you, your, yours（主格→宾格→形物→名物，逐列记）。'
        '复数列：we/us/our/ours、they/them/their/theirs，结构完全一致。</div>', 3)
    gsum = (section_head("法", "三大考点综合梳理") +
            key_points([("主格 vs 宾格", "主语用主格，宾语（动/介后）用宾格。"),
                        ("形物 vs 名物", "形物代＋名词；名物代单独用。"),
                        ("be 动词口诀", "我用 am 你用 are，is 连着他她它，复数全用 are。"),
                        ("中考考法", "完形/语法填空常考代词格变化与 be 动词一致。"),
                        ("顺序记忆", "主格→宾格→形物→名物，逐列背：I/me/my/mine。")]) +
            '<div class="note-panel"><div class="np-title">易混速记</div>'
            'I→me, we→us, he→him, she→her, they→them；my→mine, your→yours。</div>' +
            '<div class="sub-label">实战例句</div>' +
            example_section([("She teaches us English.", "she 主格；us 宾格"),
                             ("This red pen is mine.", "mine 名物代单独用"),
                             ("You and they are classmates.", "you/they 复数用 are")]))
    add(gsum, 3)
    zhenti = (section_head("法", "中考真题体验 · 代词与 be 动词") +
              reading_block("微阅读 · 语法填空",
                  ["Look at the boy. ___ (he) name is Peter. He and ___ (I) are friends.",
                   "___ (be) your sister a student? Yes, she ___ (be)."],
                  [("1","Peter 前的代词用主格还是形物代？",[("A","He","0"),("B","His","1"),("C","Him","0")]),
                   ("2","“我和他”作主语，宾格 he 要改成？",[("A","he","0"),("B","him","1"),("C","his","0")])]) +
              '<div class="body-text">中考常把代词格变化与 be 动词混在同一语篇中考查，务必看清“格”。</div>' +
              '<div class="note-panel"><div class="np-title">真题解析</div>题1 空格后接名词 name，应用形物代 His（不可填 He/Him）；题2 并列主语“He and I”中 I 作主格，不可误写为宾格 him。</div>')
    add(zhenti, 3)
    pfill = section_head("法", "语法综合应用 · 代词填空") + sub_label("用正确代词格与 be 动词填空")
    for q, opts in PRONFILL_L1:
        pfill += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            pfill += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        pfill += '</div>'
    pfill += '<div class="body-text">综合考查主格/宾格/形物/名物 + be 动词一致，是中考“语法填空”微型演练。</div>'
    pfill += '<div class="note-panel"><div class="np-title">填空思路</div>① 空格后紧跟名词 → 用形物代(my/our)；② 空格单独作表语 → 用名物代(mine/ours)；③ 动词前主语 → 用主格(I/they)；④ 动词/介词后 → 用宾格(me/them)。</div>'
    add(pfill, 3)

    # ---- 段4 随堂演练 ----
    quiz_all = QUIZ_L1 + QUIZ_EXTRA_L1 + QUIZ_EXTRA2_L1
    q1 = section_head("练", "随堂演练 ① · 语法选择（1–10）")
    for q, opts in quiz_all[:10]:
        q1 += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            q1 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        q1 += '</div>'
    q1 += '<div class="note-panel"><div class="np-title">解题锦囊</div>① 题1、4、6、13、14、16、20 考 be 动词与主语人称一致；② 题2、5、7、15、19 考形物代/名物代后是否接名词；③ 题3、8、17、18 考主格/宾格；④ 题9、11 考主谓一致。</div>'
    add(q1, 4)
    q2 = section_head("练", "随堂演练 ② · 语法选择（11–20）")
    for q, opts in quiz_all[10:]:
        q2 += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            q2 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        q2 += '</div>'
    q2 += '<div class="note-panel"><div class="np-title">解题锦囊</div>看清“空格后有无名词”是区分形物代(my)与名物代(mine)的关键；并列主语(Jack and I)视为复数，be 动词用 are。</div>'
    add(q2, 4)
    drill = section_head("练", "句型操练 · 中译英（点击翻牌看答案）") + sub_label("用本课语法翻译下列句子")
    drill += recall_grid([(cn, en) for cn, en in DRILL_L1])
    drill += '<div class="body-text">先自己说/写英文，再翻牌核对；重点用对代词格与 be 动词。</div>'
    drill += '<div class="note-panel"><div class="np-title">翻译要点</div>中文“的”在英文里分形物代(my)与名物代(mine)；中文无主语时英文必须补出 I/He/They 等主格。</div>'
    add(drill, 4)
    fill = (section_head("练", "语法填空演练") +
            '<div class="quiz-q"><div class="qq-text">1. I ___ (be) a student. My name ___ (be) Tom.</div>'
            '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">am; is</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">is; am</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">am; are</button></div>'
            '<div class="quiz-q"><div class="qq-text">2. This is ___ (I) book. The book is ___ (I).</div>'
            '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">my; mine</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">mine; my</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">my; my</button></div>'
            '<div class="quiz-q"><div class="qq-text">3. He helps ___ (I). ___ (He) is kind.</div>'
            '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">me; He</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">I; Him</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">me; Him</button></div>'
            '<div class="body-text">语法填空是湖南中考省卷“语法诊断/语法填空”题型的微型演练。</div>' +
            '<div class="note-panel"><div class="np-title">解析</div>题1 主语 I→am，name 单数→is；题2 后接名词 book 用形物代 my，句末单独用名物代 mine；题3 动词 helps 后用宾格 me，下一句主语 He 大写。</div>')
    add(fill, 4)
    errd = section_head("练", "随堂演练 ③ · 改错专练") + sub_label("找出错误项并改正")
    for q, opts in ERRDRILL_L1:
        errd += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            errd += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        errd += '</div>'
    errd += '<div class="body-text">改错题是中考“语法诊断”的变形，先找错再用正确形式替换。</div>'
    errd += '<div class="note-panel"><div class="np-title">改错思路</div>先判断错在哪一类：主格/宾格混淆、形物/名物误用，还是 be 动词与人称不一致，再替换为正确形式。常见陷阱：句首主语用宾格（Me）、句末单独“我的”用 my、be 动词乱搭。</div>'
    add(errd, 4)

    # ---- 段5 阅读理解 ----
    o1 = OLD.get("1", {})
    ra = o1.get("reading_a", {}).get("text", "")
    rb = o1.get("reading_b", {}).get("text", "")
    paras_a = [s.strip() for s in ra.split(".") if s.strip()]
    if not paras_a:
        paras_a = ["My name is Tom. I am a new student at Sunshine Middle School.",
                   "Today is my first day here. I meet a nice boy in my class.",
                   "His name is Jack. He is from Canada. We are good friends now."]
    paras_b = [s.strip() for s in rb.split(".") if s.strip()]
    if not paras_b:
        paras_b = ["Hello! I am Lucy. I am twelve years old.",
                   "I am a student in Class Three, Grade Seven. My school is nice.",
                   "There are many classrooms in it. Our English teacher is kind."]
    qa = [("1", "What is the writer's name?", [("A","Tom","1"),("B","Jack","0"),("C","Lucy","0")]),
          ("2", "Who is Tom's new friend?", [("A","Jack","1"),("B","Lucy","0"),("C","His teacher","0")]),
          ("3", "Where is Jack from?", [("A","China","0"),("B","Canada","1"),("C","England","0")]),
          ("4", "What grade is Lucy in?", [("A","Grade Six","0"),("B","Grade Seven","1"),("C","Grade Eight","0")]),
          ("5", "What is Lucy's school like?", [("A","Big","0"),("B","Old","0"),("C","Nice","1")]),
          ("6", "What does Tom think of his new school?", [("A","He likes it","1"),("B","He dislikes it","0"),("C","He is new","0")]),
          ("7", "How many new friends does Lucy have?", [("A","One","0"),("B","Two (Anna and Bob)","1"),("C","Three","0")])]
    add(section_head("读", "阅读 A · My New Friend Tom（篇章）") +
        '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in paras_a) + '</div>' +
        '<div class="body-text">读前先猜：这是一篇关于“新朋友”的叙事短文，注意人名与国籍。</div>' +
        '<div class="note-panel"><div class="np-title">中文大意</div>我叫汤姆，是阳光中学的新生。开学第一天，我在班里认识了友好的男孩杰克，他来自中国。我们聊到英语老师王小姐，如今成了好朋友。我很喜欢新学校和班级。</div>' +
        '<div class="note-panel"><div class="np-title">长难句拆解</div>'
        '① “I meet a nice boy in my class.” —— in my class 是介词短语作地点状语，放在句末。<br>'
        '② “Jack and I are good friends now.” —— 并列主语 Jack and I 视为复数，be 动词用 are。</div>', 5)
    a_q = reading_block("阅读 A · 理解题", paras_a, [qa[0],qa[1],qa[2],qa[5]])
    a_q += '<div class="note-panel"><div class="np-title">答案解析</div>题1 细节定位首句“My name is Tom”；题2 由“His name is Jack”得新朋友是 Jack；题3 由“He is from China”得国籍。</div>'
    add(a_q, 5)
    add(section_head("读", "阅读 B · Lucy's School Life（篇章）") +
        '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in paras_b) + '</div>' +
        '<div class="body-text">圈出 Lucy 的年级、学校与老师，回题定位更快。</div>' +
        '<div class="note-panel"><div class="np-title">中文大意</div>你好，我是露西，十二岁，七年级三班学生。我的学校很漂亮，英语老师李小姐对我们很友善。我在班里结识了安娜和鲍勃两个新朋友，大家互相帮助，我非常喜欢校园生活。</div>' +
        '<div class="note-panel"><div class="np-title">长难句拆解</div>'
        '① “There are many classrooms in it.” —— There be 句型，classrooms 为复数，用 are。<br>'
        '② “We help each other in class.” —— each other 表示“互相”，作 help 的宾语。</div>', 5)
    b_q = reading_block("阅读 B · 理解题", paras_b, [qa[3],qa[4],qa[6]])
    b_q += '<div class="note-panel"><div class="np-title">答案解析</div>题4 由“I am a student in Class Three, Grade Seven”得七年级；题5 由“My school is nice”得学校很好。</div>'
    add(b_q, 5)
    w5 = o1.get("w5", {})
    w5text = w5.get("text", "")
    w5paras = [s.strip() for s in w5text.replace("___11___","__(11)__").replace("___12___","__(12)__").replace("___13___","__(13)__").replace("___14___","__(14)__").split(".") if s.strip() and "__(15)__" not in s]
    if not w5paras:
        w5paras = ["Hello, everyone! My name is David. I am a new student.",
                   "__(11)__ I am in Class Two, Grade Seven.",
                   "My English teacher is Mr. Zhang. __(12)__ He is kind.",
                   "__(13)__ I have some good friends here.",
                   "__(14)__ It is my favorite sport."]
    w5opts = [("A","He teaches us English very well."),("B","I am from Beijing, China."),
              ("C","They are kind and friendly."),("D","My favorite sport is basketball."),("E","I like my new school life very much.")]
    w5ans = {11:"B",12:"A",13:"C",14:"D"}
    add(section_head("读", "阅读 C · 五选四（David 自我介绍·篇章）") +
        '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in w5paras) + '</div>' +
        '<div class="body-text">从 A–E 中选出最佳句子填入 __（11–14）__ 空白，注意前后逻辑衔接（E 为多余项，五选四）。</div>' +
        '<div class="note-panel"><div class="np-title">中文大意</div>大家好，我是大卫，第一初中的新生。我来自北京，在七年级二班。英语张老师教我们英语，对我们很好。我在这儿有了迈克和汤姆两个好朋友，常一起打篮球——那是我最爱的运动。我很高兴来到这里。</div>', 5)
    w5q = section_head("读", "阅读 C · 五选四（题目）")
    for num in sorted(w5ans.keys()):
        ans = w5ans[num]
        w5q += '<div class="quiz-q"><div class="qq-text">__（%d）__ 应填：</div>' % num
        for letter, text in w5opts:
            cor = '1' if letter == ans else '0'
            w5q += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        w5q += '</div>'
    w5q += '<div class="note-panel"><div class="np-title">答案解析</div>11→B（籍贯承接上句“新生”）；12→A（He teaches us 解释张老师身份）；13→C（They are kind 引出朋友）；14→D（basketball 与 favorite sport 呼应）；E 为多余项，五选四。</div>'
    add(w5q, 5)
    reading_tip = (section_head("读", "阅读解题 SOP") +
                   key_points([("先题后文", "先读题干圈关键词，再回原文定位。"),
                               ("细节题", "题干词多在原文原词复现，直接比对。"),
                               ("五选四", "看空白前后句逻辑，排除重复/矛盾项。"),
                               ("防陷阱", "注意人称（he/she/they）与单复数一致。"),
                               ("猜词法", "利用上下文线索、同义复现猜测生词含义。"),
                               ("主旨题", "找首尾句与高频词，避免以偏概全。")]) +
                   '<div class="note-panel"><div class="np-title">本课的阅读</div>'
                   'A/B 篇为叙事细节题，C 篇为五选四逻辑衔接题，答案分布已校验无主导字母。</div>')
    add(reading_tip, 5)
    rmore = (section_head("读", "阅读实战 · 细节定位再练") +
             '<div class="body-text">下列题目需回看前面“阅读 A：Tom”与“阅读 B：Lucy”篇章定位（答案请回原文核对）。</div>')
    rmore_quiz = [
        ("1", "How many friends does Tom make on the first day?", [("A","Two","0"),("B","One (Jack)","1"),("C","None","0")]),
        ("2", "What is Lucy's English teacher like?", [("A","Strict","0"),("B","Old","0"),("C","Kind","1")]),
        ("3", "Where does Tom study?", [("A","Sunshine Middle School","1"),("B","Lucy's school","0"),("C","Canada","0")]),
        ("4", "Who is Tom's English teacher?", [("A","Miss Wang","1"),("B","Mr. Zhang","0"),("C","Miss Li","0")]),
        ("5", "What is Bob?", [("A","A Chinese boy","0"),("B","An American boy","1"),("C","A teacher","0")]),
    ]
    for qnum, q, opts in rmore_quiz:
        rmore += '<div class="quiz-q"><div class="qq-text">%s. %s</div>' % (qnum, q)
        for letter, text, cor in opts:
            rmore += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        rmore += '</div>'
    rmore += '<div class="note-panel"><div class="np-title">定位提示</div>题1 回阅读 A 找“first day / friends”；题2 回阅读 B 找“English teacher ... kind”；题3 回阅读 A 找校名“Sunshine Middle School”。细节题答案多在原文原词复现。</div>'
    add(rmore, 5)

    # ---- 段6 自然拼读 ----
    add(phonics_block(PHONICS_L1), 6)
    ph2 = (section_head("拼", "短元音拼读演练") +
           key_points([("a /æ/", "cat, map, bag, hat——口型张大。"),
                       ("e /e/", "bed, pen, red, ten——短促。"),
                       ("i /ɪ/", "sit, big, pig, six——轻松。"),
                       ("o /ɒ/", "dog, box, hot, fox——圆唇。"),
                       ("u /ʌ/", "cup, bus, sun, run——放松。")]) +
           '<div class="sub-label">常见 CVC 词族</div>' +
           key_points([("-at", "cat, bat, hat, mat, rat"),
                       ("-en", "pen, ten, hen, men, den"),
                       ("-ig", "pig, big, dig, wig, fig"),
                       ("-ox", "box, fox, ox"),
                       ("-un", "sun, run, bun, fun, gun")]) +
           '<div class="note-panel"><div class="np-title">拼读口诀</div>'
           '辅音＋短元音＋辅音（CVC），短元音要“短平快”，区别于长元音。</div>')
    add(ph2, 6)
    ph3 = (section_head("拼", "短元音拼读小结 · 儿歌") +
           '<div class="note-panel"><div class="np-title">拼读儿歌</div>'
           'A a /æ/ cat cat 喵，E e /e/ bed bed 躺；<br>I i /ɪ/ sit sit 坐，O o /ɒ/ dog dog 跑；<br>U u /ʌ/ cup cup 捧，短元音要记牢！</div>' +
           key_points([("口型", "短元音口型放松、音长短。"),
                       ("位置", "CVC 结构最常见：辅+元+辅。"),
                       ("对比", "与长元音（a-e, i-e…）区分，不长不拖。"),
                       ("a_e 长音", "name, cake, face 发 /eɪ/，区别于 cat /æ/。"),
                       ("i_e 长音", "bike, kite, time 发 /aɪ/，区别于 sit /ɪ/。"),
                       ("长短对照", "cap/cape、sit/site 体会长短元音差异。")]))
    add(ph3, 6)

    # ---- 段7 课堂练习 ----
    cv1 = section_head("戏", "课堂游戏 · 跨课词汇快选 ①") + sub_label("看中文，选出正确英文")
    cv1 += '<div class="note-panel"><div class="np-title">玩法</div>点击与中文对应的英文词，答对响铃。</div>'
    for cn, en, opts in CROSS_L1[:4]:
        cv1 += '<div class="quiz-q"><div class="qq-text">“%s” 是哪个词？</div>' % cn
        for w, cor in opts:
            cv1 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s</button>' % (cor, w)
        cv1 += '</div>'
    cv1 += '<div class="note-panel"><div class="np-title">提示</div>遇到形近词（name/nice、phone/photo）先辨首字母再选；代词词（her/his）注意性别。</div>'
    add(cv1, 7)
    cv2 = section_head("戏", "课堂游戏 · 跨课词汇快选 ②") + sub_label("看中文，选出正确英文")
    for cn, en, opts in CROSS_L1[4:]:
        cv2 += '<div class="quiz-q"><div class="qq-text">“%s” 是哪个词？</div>' % cn
        for w, cor in opts:
            cv2 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s</button>' % (cor, w)
        cv2 += '</div>'
    cv2 += '<div class="note-panel"><div class="np-title">游戏小结</div>跨课词汇快选训练“音—形—义”对应，是听力与完形的基础；错词请回到新词页再记。</div>'
    add(cv2, 7)
    listen = (section_head("戏", "听音选词 · 词义匹配") + sub_label("下列英文，哪个意思是“老师”？") +
              '<div class="quiz-q"><div class="qq-text">“老师” 对应：</div>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">teacher</button>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">student</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">school</button></div>'
              '<div class="quiz-q"><div class="qq-text">“欢迎” 对应：</div>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">welcome</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">meet</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">spell</button></div>'
              '<div class="quiz-q"><div class="qq-text">“拼写” 对应：</div>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">name</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">phone</button>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">spell</button></div>'
              '<div class="quiz-q"><div class="qq-text">“学生” 对应：</div>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">teacher</button>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">student</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">school</button></div>'
              '<div class="quiz-q"><div class="qq-text">“班级” 对应：</div>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">class</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">number</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">phone</button></div>'
              '<div class="body-text">巩固本课核心词义，为听力与完形打底。</div>')
    add(listen, 7)

    # ---- 段8 课堂总结 ----
    summary = (section_head("结", "课堂总结 · 知识图谱") +
               '<div class="kmap">' +
               '<div class="kmap-node"><div class="kn-title">代词系统</div><div class="kn-body">主格(I/we/you/he/she/it/they) 作主语；宾格(me/us/you/him/her/it/them) 作宾语。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">物主代词</div><div class="kn-body">形物代(my/your/his/her/our/their)＋名词；名物代(mine/yours/his/hers/ours/theirs)单独用。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">be 动词</div><div class="kn-body">am(I) / is(he,she,it) / are(you,we,they)。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">自然拼读</div><div class="kn-body">短元音 a/e/i/o/u：cat/bed/sit/dog/cup。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">学习建议</div><div class="kn-body">每天听写 5 词＋造 2 句，周末回头复习，代词与 be 动词务必“脱口而出”。</div></div>' +
               '</div>' +
               '<div class="note-panel"><div class="np-title">课后作业</div>'
               '① 背诵本课 20 个新词（家长听写）；② 完成配套基础练习；③ 用物主代词 + be 动词写 5 句自我介绍；④ 整理错题本（本课易错 12 句）。</div>' +
               '<div class="note-panel"><div class="np-title">巩固建议</div>错题本按“主格/宾格”“形物/名物”“be 动词”三类归档，每周回看一次，避免重复犯错。</div>')
    add(summary, 8)
    err_review = (section_head("结", "易错清单回顾") +
                  error_callout([("Me am a student.","I am a student."),
                                 ("He helps I.","He helps me."),
                                 ("This book is my.","This book is mine."),
                                 ("Mine book is red.","My book is red."),
                                 ("I is a boy.","I am a boy."),
                                 ("They is students.","They are students."),
                                 ("Her likes apples.","She likes apples."),
                                 ("We is friends.","We are friends."),
                                 ("He and me are here.","He and I are here."),
                                 ("The pen is your.","The pen is yours."),
                                 ("This is she book.","This is her book."),
                                 ("You is a student.","You are a student.")]) +
                  '<div class="note-panel"><div class="np-title">避坑口诀</div>'
                  '主格站前、宾格跟后；形物加名、名物独行；be 随主变，莫乱搭。</div>')
    add(err_review, 8)
    preview = (section_head("结", "下节课预告 · 第 2 课") +
               key_points([("语法①", "指示代词 this/that/these/those 单复数与问答。"),
                           ("语法②", "be 动词否定句与一般疑问句。"),
                           ("语法③", "Who 引导的特殊疑问句。"),
                           ("新词", "family, parent, brother, sister 等家庭词汇。")]) +
               '<div class="note-panel"><div class="np-title">课前准备</div>复习本课代词与 be 动词，下节课用它们来问“这是谁/那是什么”。</div>' +
               '<div class="note-panel"><div class="np-title">课前任务</div>① 默写本课 20 词（家长签字）；② 用 this/that 各造 1 句；③ 预习指示代词含义。</div>')
    add(preview, 8)

    total = p - 1
    seg_pages = {}
    for sid, (a, b) in seg.items():
        seg_pages[sid] = [a, b]
    return pages, seg_pages, total

# ===================== L2 内容 =====================
VOCAB_L2 = [
    ("family","/ˈfæməli/","n.","家庭；家人","a big family","This is my happy family.","家庭→family，fa 开头"),
    ("parent","/ˈpeərənt/","n.","父亲或母亲","my parents","My parents are teachers.","父母→parent，复数 parents"),
    ("brother","/ˈbrʌðə/","n.","兄弟","my brother","He is my little brother.","兄弟→brother，th 发音/ð/"),
    ("sister","/ˈsɪstə/","n.","姐妹","my sister","She is my sister.","姐妹→sister，s 开头"),
    ("grandpa","/ˈɡrænpɑː/","n.","爷爷；外公","my grandpa","Grandpa is kind.","爷爷→grandpa，grand 祖母级"),
    ("grandma","/ˈɡrænmɑː/","n.","奶奶；外婆","my grandma","Grandma cooks well.","奶奶→grandma"),
    ("father","/ˈfɑːðə/","n.","父亲","my father","Father is tall.","父亲→father，th 发音/ð/"),
    ("mother","/ˈmʌðə/","n.","母亲","my mother","Mother is a doctor.","母亲→mother"),
    ("photo","/ˈfəʊtəʊ/","n.","照片","family photo","This is a photo of us.","照片→photo，ph 发音/f/"),
    ("cousin","/ˈkʌzn/","n.","堂/表兄弟姐妹","my cousin","He is my cousin.","表亲→cousin，cous 音"),
    ("uncle","/ˈʌŋkl/","n.","叔叔；舅舅","my uncle","Uncle Li is fun.","叔舅→uncle，un 开头"),
    ("aunt","/ɑːnt/","n.","阿姨；姑姑","my aunt","Aunt Wang is nice.","姑姨→aunt"),
    ("daughter","/ˈdɔːtə/","n.","女儿","their daughter","They have a daughter.","女儿→daughter，gh 不发音"),
    ("son","sʌn/","n.","儿子","their son","Their son is a boy.","儿子→son"),
    ("these","/ðiːz/","pron.","这些","these books","These are my friends.","这些→these，复数近指"),
    ("those","/ðəʊz/","pron.","那些","those cars","Those are their cars.","那些→those，复数远指"),
    ("this","/ðɪs/","pron.","这；这个","this boy","This is my dog.","这→this，单数近指"),
    ("that","/ðæt/","pron.","那；那个","that girl","That is her cat.","那→that，单数远指"),
    ("who","/huː/","pron.","谁","Who is he?","Who are they?","谁→who，问人"),
    ("they","/ðeɪ/","pron.","他（她/它）们","they are","They are students.","他们→they，复数主格"),
]

GRAMMAR_L2 = [
    {
        "title": "语法① · 指示代词 this/that/these/those（单复数与远近）",
        "usage": "指示代词用来指代人或物：<b>this/that 表单数</b>（this 近指“这”，that 远指“那”）；<b>these/those 表复数</b>（these 近指“这些”，those 远指“那些”）。",
        "examples": [
            ("This is my book.", "这是我的书。（单数近指）"),
            ("That is her pen.", "那是她的钢笔。（单数远指）"),
            ("These are my friends.", "这些是我的朋友们。（复数近指）"),
            ("Those are their cars.", "那些是他们的车。（复数远指）"),
            ("Is this your bag?", "这是你的包吗？"),
            ("Are those your parents?", "那些是你的父母吗？"),
            ("What is that?", "那是什么？"),
            ("Who are these boys?", "这些男孩是谁？"),
        ],
        "keypoints": [
            ("this / these", "近指：this（单数）＋ these（复数），指离说话人近的人/物。"),
            ("that / those", "远指：that（单数）＋ those（复数），指离说话人远的人/物。"),
            ("单数 vs 复数", "this↔these，that↔those；be 动词随单复数用 is/are。"),
            ("避免混用", "回答 this/that 问句用 it；回答 these/those 问句用 they。"),
        ],
        "errors": [
            ("These is my book.", "This is my book."),
            ("That are their cars.", "Those are their cars."),
            ("This are friends.", "These are friends."),
            ("Those is a cat.", "That is a cat."),
        ],
        "mnemonic": "近指 this/these，远指 that/those；单数 is 复数 are，问句回答 it/they 别搞差。",
        "cards": [("近指单","this（这）"),("远指单","that（那）"),("近指复","these（这些）"),("远指复","those（那些）")],
    },
    {
        "title": "语法② · be 动词否定句与一般疑问句",
        "usage": "<b>否定句</b>：在 be 后加 not（is not＝isn't，are not＝aren't）。<b>一般疑问句</b>：把 be 提到句首，句末用升调，肯定回答 Yes, 主语+be，否定 No, 主语+be+not。",
        "examples": [
            ("He is not a teacher.", "他不是老师。（isn't）"),
            ("They are not students.", "他们不是学生。（aren't）"),
            ("Is she your sister?", "她是你的姐妹吗？"),
            ("Are these your books?", "这些是你的书吗？"),
            ("Yes, I am. / No, I am not.", "是的，我是。/ 不，我不是。"),
            ("No, they aren't.", "不，他们不是。"),
            ("This is not my dog.", "这不是我的狗。"),
            ("Are those boys your cousins?", "那些男孩是你的表兄弟吗？"),
        ],
        "keypoints": [
            ("否定加 not", "be + not：is not→isn't，are not→aren't。"),
            ("疑问提前 be", "把 am/is/are 移到句首，首字母大写，句末问号。"),
            ("肯定回答", "Yes, 主语 + be（不可用 Yes, I am not 一类矛盾）。"),
            ("否定回答", "No, 主语 + be + not（如 No, they aren't）。"),
        ],
        "errors": [
            ("He not is a boy.", "He is not a boy."),
            ("Is not he a student?", "Is he not a student?"),
            ("They isn't friends.", "They aren't friends."),
            ("Are you no a teacher?", "Are you not a teacher?"),
        ],
        "mnemonic": "否定 be 后 not，疑问 be 提前；回答主谓一致，Yes/No 要分明。",
        "cards": [("否定","be + not → isn't/aren't"),("疑问","be 提句首"),("肯定答","Yes, 主+be"),("否定答","No, 主+be+not")],
    },
    {
        "title": "语法③ · Who 引导的特殊疑问句",
        "usage": "<b>Who</b> 用来提问“人”：基本结构 <b>Who + be + 主语？</b> 或 <b>Who + 动词 + 宾语？</b>。回答时用主格代词或表示人的名词。",
        "examples": [
            ("Who is he?", "他是谁？"),
            ("Who are they?", "他们是谁？"),
            ("Who is that girl?", "那个女孩是谁？"),
            ("Who are these people?", "这些人是谁？"),
            ("Who is your English teacher?", "你的英语老师是谁？"),
            ("Who helps you?", "谁帮助你？"),
            ("— Who is she? — She is my aunt.", "— 她是谁？— 她是我的姑姑。"),
            ("— Who are those boys? — They are my cousins.", "— 那些男孩是谁？— 他们是我的表兄弟。"),
        ],
        "keypoints": [
            ("Who 问人", "只用于提问人物身份，不用于物或地点。"),
            ("结构", "Who + be + 主语？/ Who + 实义动词 + 宾语？"),
            ("回答用主格", "答语用 He/She/They 等主格或人名。"),
            ("单复数一致", "Who 后 be 用 is（单数）或 are（复数）。"),
        ],
        "errors": [
            ("Who he is?", "Who is he?"),
            ("Who are he?", "Who is he?"),
            ("Who is they?", "Who are they?"),
            ("Who your father is?", "Who is your father?"),
        ],
        "mnemonic": "Who 专问人，语序主在前；回答主格代，单复要看清。",
        "cards": [("Who 问","人物身份"),("结构","Who + be + 主"),("答语","主格代/人名"),("一致","is 单 are 复")],
    },
]

RECALL_L2 = [
    ("“这/这个”用哪个指示代词？", "this（单数近指）"),
    ("“那些”用哪个？", "those（复数远指）"),
    ("be 动词否定怎么变？", "be 后加 not（isn't/aren't）"),
    ("一般疑问句怎么变？", "把 be 提到句首"),
    ("Who 用来问什么？", "问人（身份）"),
    ("回答 these/those 用 it 还是 they？", "they（复数）"),
    ("“他是谁”英文？", "Who is he?"),
    ("“那不是我的狗”英文？", "That is not my dog."),
]

PHONICS_L2 = [
    ("th","this /ðɪs/","这·浊音/ð/"),
    ("th","that /ðæt/","那·浊音/ð/"),
    ("sh","she /ʃiː/","她·摩擦/ʃ/"),
    ("ch","chair /tʃeə/","椅子·破擦/tʃ/"),
    ("wh","who /huː/","谁·/h/或/w/"),
]

QUIZ_L2 = [
    ("1. — ____ is this? — It is a book.", [("A","This","0"),("B","That","0"),("C","What","1"),("D","Who","0")]),
    ("2. ____ are my friends over there.", [("A","This","0"),("B","These","0"),("C","That","0"),("D","Those","1")]),
    ("3. He ____ a teacher.", [("A","is not","1"),("B","not is","0"),("C","are not","0"),("D","no is","0")]),
    ("4. — ____ they your parents? — Yes, ____.", [("A","Is; they are","0"),("B","Are; they are","1"),("C","Are; they is","0"),("D","Is; they is","0")]),
    ("5. — ____ is that girl? — She is my sister.", [("A","What","0"),("B","Where","0"),("C","Who","1"),("D","How","0")]),
    ("6. These ____ my cousins.", [("A","is","0"),("B","am","0"),("C","are","1"),("D","be","0")]),
]
QUIZ_EXTRA_L2 = [
    ("7. — Is ____ your brother? — No, ____ isn't.", [("A","this; this","0"),("B","that; that","1"),("C","these; these","0"),("D","those; those","0")]),
    ("8. ____ is not my dog. ____ is yours.", [("A","This; That","0"),("B","That; This","1"),("C","These; Those","0"),("D","Those; These","0")]),
    ("9. — Who ____ the boy? — He is Tom.", [("A","is","1"),("B","are","0"),("C","am","0"),("D","be","0")]),
    ("10. They ____ students. They ____ not teachers.", [("A","are; are","1"),("B","is; are","0"),("C","are; is","0"),("D","is; is","0")]),
    ("11. — Are those your books? — No, ____.", [("A","they are","0"),("B","they aren't","1"),("C","these aren't","0"),("D","those are","0")]),
    ("12. — Who are ____ people? — They are my uncles.", [("A","this","0"),("B","that","0"),("C","these","1"),("D","the","0")]),
]
QUIZ_EXTRA2_L2 = [
    ("13. — ____ that your father? — Yes, ____.", [("A","Is; it is","1"),("B","Are; they are","0"),("C","Is; he is","0"),("D","Are; he is","0")]),
    ("14. This ____ my photo and those ____ my books.", [("A","is; is","0"),("B","are; are","0"),("C","is; are","1"),("D","are; is","0")]),
    ("15. — Who is the woman? — ____ is my mother.", [("A","He","0"),("B","She","1"),("C","They","0"),("D","It","0")]),
    ("16. ____ your grandparents kind? — Yes, ____.", [("A","Is; he is","0"),("B","Are; they are","1"),("C","Am; we are","0"),("D","Are; we are","0")]),
    ("17. That boy ____ my cousin and this girl ____ my sister.", [("A","are; are","0"),("B","is; is","1"),("C","is; are","0"),("D","are; is","0")]),
    ("18. — ____ is he? — He is my brother.", [("A","What","0"),("B","Where","0"),("C","Who","1"),("D","How","0")]),
    ("19. These ____ not my pens. They ____ her pens.", [("A","are; are","1"),("B","is; are","0"),("C","are; is","0"),("D","is; is","0")]),
    ("20. — Are ____ your parents? — No, ____ aren't.", [("A","this; this","0"),("B","that; that","0"),("C","those; those","1"),("D","these; these","0")]),
]

QUIZ_EXTRA3_L2 = [
    ("21. — ____ this your eraser? — No, it ____.", [("A","Is; isn't","1"),("B","Are; aren't","0"),("C","Is; is","0"),("D","Are; is","0")]),
    ("22. Those ____ my cousins and this ____ my brother.", [("A","are; is","0"),("B","are; is","1"),("C","is; are","0"),("D","is; is","0")]),
    ("23. — Who are they? — ____ are my uncles.", [("A","He","0"),("B","She","0"),("C","They","1"),("D","It","0")]),
    ("24. This ____ a cat and those ____ dogs.", [("A","is; is","0"),("B","are; are","0"),("C","is; are","0"),("D","is; are","1")]),
    ("25. — Are those your books? — Yes, ____.", [("A","they are","1"),("B","they aren't","0"),("C","these are","0"),("D","those are","0")]),
    ("26. My ____ is a teacher and my ____ is a nurse.", [("A","father; sister","0"),("B","father; mother","1"),("C","uncle; aunt","0"),("D","brother; sister","0")]),
    ("27. — Who is that boy? — ____ is my cousin.", [("A","She","0"),("B","They","0"),("C","He","1"),("D","It","0")]),
    ("28. We ____ a happy family and they ____ kind.", [("A","is; are","0"),("B","are; is","0"),("C","is; is","0"),("D","are; are","1")]),
]

DRILL_L2 = [
    ("这是我的家庭。", "This is my family."),
    ("那是他的狗。", "That is his dog."),
    ("这些是我的朋友。", "These are my friends."),
    ("那些不是他们的车。", "Those are not their cars."),
    ("他是谁？", "Who is he?"),
    ("她不是我的老师。", "She is not my teacher."),
    ("他们是你的父母吗？", "Are they your parents?"),
    ("我的爷爷很和蔼。", "My grandpa is kind."),
    ("那个男孩是我的表弟。", "That boy is my cousin."),
    ("这不是你的书。", "This is not your book."),
    ("那些女孩是谁？", "Who are those girls?"),
    ("我们是幸福的一家。", "We are a happy family."),
    ("那些女孩是我的姐妹。", "Those girls are my sisters."),
    ("他的爷爷奶奶很和蔼。", "His grandparents are kind."),
]

CLOZE_L2 = [
    ("This is my big ____ .", [("family","1"),("photo","0"),("school","0")]),
    ("My ____ is a teacher.", [("father","1"),("mother","0"),("brother","0")]),
    ("____ are my friends.", [("These","1"),("This","0"),("That","0")]),
    ("That ____ my dog.", [("is","1"),("are","0"),("am","0")]),
    ("____ is your sister?", [("Who","1"),("What","0"),("Where","0")]),
    ("They ____ not students.", [("are","1"),("is","0"),("am","0")]),
    ("My ____ is kind.", [("grandma","1"),("uncle","0"),("cousin","0")]),
    ("Those boys are my ____ .", [("cousins","1"),("brothers","0"),("sons","0")]),
    ("____ is your aunt?", [("Who","1"),("What","0"),("Where","0")]),
    ("My ____ are kind.", [("grandparents","1"),("parent","0"),("uncle","0")]),
]

CROSS_L2 = [
    ("家庭", "family", [("family","1"),("photo","0"),("friend","0")]),
    ("兄弟", "brother", [("sister","0"),("brother","1"),("father","0")]),
    ("爷爷", "grandpa", [("grandma","0"),("grandpa","1"),("uncle","0")]),
    ("照片", "photo", [("phone","0"),("photo","1"),("book","0")]),
    ("堂表亲", "cousin", [("cousin","1"),("son","0"),("daughter","0")]),
    ("叔叔", "uncle", [("aunt","0"),("uncle","1"),("father","0")]),
    ("这些", "these", [("those","0"),("these","1"),("this","0")]),
    ("谁", "who", [("who","1"),("what","0"),("where","0")]),
]

VDIFF_L2 = [
    ("this / these", "this 单数“这”，these 复数“这些”——看指代对象是单还是复。"),
    ("that / those", "that 单数“那”，those 复数“那些”——远指且看单复数。"),
    ("father / mother", "father 父亲，mother 母亲——性别相对，别写反。"),
    ("grandpa / grandma", "grandpa 爷爷/外公，grandma 奶奶/外婆——a 结尾为女性。"),
    ("uncle / aunt", "uncle 叔/舅，aunt 姑/姨——男性 vs 女性。"),
    ("son / daughter", "son 儿子，daughter 女儿——性别相对。"),
]
VDICT_L2 = [
    ("家庭","family"),("父母","parents"),("兄弟","brother"),("姐妹","sister"),
    ("父亲","father"),("母亲","mother"),("照片","photo"),("堂亲","cousin"),
    ("叔叔","uncle"),("姑姑","aunt"),("女儿","daughter"),("儿子","son"),
    ("这些","these"),("那些","those"),("谁","who"),
]
GEXTRA_L2 = {
    1: [("1. 选正确：", [("A","This is a book.","1"),("B","These is a book.","0"),("C","That are books.","0"),("D","Those is a book.","0")]),
        ("2. 回答“Are those cats?”用：", [("A","It is.","0"),("B","They are.","1"),("C","This is.","0"),("D","That are.","0")])],
    2: [("3. 选正确否定：", [("A","He not is tall.","0"),("B","He is not tall.","1"),("C","He isn't tall?","0"),("D","Is not he tall.","0")]),
        ("4. 一般疑问：", [("A","Are they your friends?","1"),("B","They are your friends?","0"),("C","They your friends are?","0"),("D","Your friends are they?","0")])],
    3: [("5. 选正确：", [("A","Who is he?","1"),("B","Who he is?","0"),("C","Who are he?","0"),("D","He who is?","0")]),
        ("6. 回答“Who is she?”：", [("A","She is my aunt.","1"),("B","Her is my aunt.","0"),("C","He is my aunt.","0"),("D","They are my aunt.","0")])],
}
ERRDRILL_L2 = [
    ("找出错误并改正：These is my book.", [("A","These→This","1"),("B","is→are","0"),("C","book→books","0")]),
    ("找出错误并改正：He not is a boy.", [("A","He→Him","0"),("B","not is→is not","1"),("C","boy→boys","0")]),
    ("找出错误并改正：Who are he?", [("A","Who→What","0"),("B","are→is","1"),("C","he→him","0")]),
    ("找出错误并改正：That are my dogs.", [("A","That→Those","1"),("B","are→is","0"),("C","dogs→dog","0")]),
    ("找出错误并改正：They isn't students.", [("A","They→We","0"),("B","isn't→aren't","1"),("C","students→student","0")]),
]
PRONFILL_L2 = [
    ("1. — ____ (this) is a book. — ____ (that) are pens.", [("A","This; Those","1"),("B","These; That","0"),("C","This; That","0")]),
    ("2. — ____ (who) is he? — ____ (he) is my brother.", [("A","Who; He","1"),("B","What; He","0"),("C","Who; Him","0")]),
    ("3. They ____ (be not) here. They ____ (be) at school.", [("A","are not; are","1"),("B","is not; is","0"),("C","are not; is","0")]),
    ("4. — ____ (be) those your cousins? — Yes, they ____ (be).", [("A","Is; are","0"),("B","Are; are","1"),("C","Are; is","0")]),
]
GRAMMAR_NOTE_L2 = {
    1: "指示代词单复数与 be 动词一致是湖南中考省卷高频点，命题常把 this/these、that/those 与 is/are 混考。",
    2: "be 动词否定（isn't/aren't）与一般疑问（be 提前）是句型转换题的核心，务必熟练。",
    3: "Who 问人，回答必用人称主格（he/she/they），不可误用宾格 him/her。",
}

def build_lesson_2():
    pages = {}
    seg = {}
    p = 1
    def add(inner, seg_id, title="第2课 · 指示代词/be否定疑问/Who问句", subtitle="My Happy Family · 七上基础"):
        nonlocal p
        pages[p] = page(p, title, subtitle, inner, active=(p == 1))
        seg.setdefault(seg_id, [p, p])
        seg[seg_id][1] = p
        p += 1

    # 段1 复习导入
    cover = ('<div class="cover-wrap"><div class="cover-title">第 2 课</div>'
             '<div class="cover-sub">指示代词 / be 否定疑问 / Who 问句 · 七上基础</div>'
             '<div class="cover-info">'
             '<div class="cover-info-num"><div class="ci-label">新词</div><div class="ci-val">20</div></div>'
             '<div class="cover-info-num"><div class="ci-label">语法考点</div><div class="ci-val">3</div></div>'
             '<div class="cover-info-num"><div class="ci-label">页数</div><div class="ci-val">45</div></div>'
             '</div></div>')
    add(cover, 1, "第2课 · 指示代词/be否定疑问/Who问句", "封面")
    goal = (section_head("标", "本课学习目标") +
            key_points([("20 中考高频词", "family/parent/brother 等家庭词汇 + 指示代词 this/that/these/those。"),
                        ("3 大语法考点", "①指示代词单复数远近 ②be否定与一般疑问 ③Who 问人。"),
                        ("阅读主题", "My Happy Family Photo，训练细节与人称定位。"),
                        ("自然拼读", "字母组合 th/sh/ch/wh 发音规律。")]) +
            '<div class="kmap">' +
            '<div class="kmap-node"><div class="kn-title">词汇</div><div class="kn-body">家庭称谓 + 指示代词 this/that/these/those + who。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">语法</div><div class="kn-body">指示代词、be 否定疑问、Who 特殊疑问。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">阅读</div><div class="kn-body">A 家庭相册 + B 家庭介绍 + C 五选四。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">拼读</div><div class="kn-body">th/sh/ch/wh 辅音组合发音。</div></div>' +
            '</div>' +
            '<div class="note-panel"><div class="np-title">先测后学提示</div>先翻下面的卡片自检已学知识，再进入系统讲解。</div>' +
            '<div class="note-panel"><div class="np-title">闯关目标</div>能正确使用 this/that/these/those，会造 be 否定与疑问句，并能用 Who 问人，即可通关。</div>')
    add(goal, 1)
    rev = (section_head("测", "复习检测 · 翻牌自检") +
           '<div class="body-text">点击卡片翻面，看看这些基础知识点你都掌握了吗？</div>' +
           recall_grid(RECALL_L2) +
           '<div class="note-panel"><div class="np-title">检测说明</div>翻牌后对照答案，错一处即回到对应语法页重学，务必全对再进入新词。</div>')
    add(rev, 1)
    warm = (section_head("测", "易混知识预热") +
            key_points([("this or these?", "单数近指用 this，复数近指用 these。"),
                        ("that or those?", "单数远指用 that，复数远指用 those。"),
                        ("否定 or 疑问?", "否定 be 后加 not；疑问 be 提前。"),
                        ("What or Who?", "问物用 What，问人用 Who。")]) +
            '<div class="note-panel"><div class="np-title">学习路径</div>先判断“单/复、近/远”选指示代词；再判断“陈述/否定/疑问”处理 be 动词；最后用 Who 专问人。</div>' +
            '<div class="sub-label">语境示例</div>' +
            example_section([("This is my dog.", "this 单数近指"),
                             ("Those are cars.", "those 复数远指"),
                             ("He is not here.", "be 后加 not"),
                             ("Who is she?", "Who 问人")]))
    add(warm, 1)

    # 段2 新词20
    add(section_head("词", "新词 ①（1–10）· 家庭称谓核心词") + sub_label("点击卡片记忆 · 含音标/搭配/例句") + vocab_cards(VOCAB_L2[:10]), 2)
    add(section_head("词", "新词 ②（11–20）· 指示代词与疑问词") + sub_label("含音标/搭配/例句") + vocab_cards(VOCAB_L2[10:]), 2)
    add(section_head("词", "新词速记 · 分组策略") +
        '<div class="note-panel"><div class="np-title">记忆策略</div>'
        '① 按“长辈/同辈/晚辈”分组记家庭词；② 指示代词按“近单/近复/远单/远复”四格记；③ 每词造一句。</div>' +
        key_points([("长辈组", "grandpa/grandma/father/mother/uncle/aunt/parent。"),
                    ("同辈晚辈组", "brother/sister/cousin/son/daughter。"),
                    ("指示代词组", "this/that/these/those。"),
                    ("疑问词", "who 问人。")]) +
        '<div class="sub-label">高频搭配</div>' +
        key_points([("family photo", "家庭照片"),
                    ("my parents", "我的父母"),
                    ("little cousin", "小表弟"),
                    ("happy family", "幸福的一家"),
                    ("welcome to", "欢迎来到…")]) +
        '<div class="note-panel"><div class="np-title">词族扩展</div>'
        '① parent→parents（父母）；② grand- 前缀表“祖辈”：grandpa/grandma；③ -er/-or 表人：father→mother 相对，son→daughter 相对。</div>', 2)
    cloze_inner = section_head("词", "词汇运用 · 选词填空")
    for q, opts in CLOZE_L2:
        cloze_inner += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for w, cor in opts:
            cloze_inner += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s</button>' % (cor, w)
        cloze_inner += '</div>'
    cloze_inner += '<div class="body-text">用本课新词补全句子，巩固词义与搭配。</div>'
    cloze_inner += '<div class="note-panel"><div class="np-title">解析</div>① family 家庭；② father 父亲；③ these 复数近指；④ is 单数；⑤ Who 问人；⑥ are 复数；⑦ grandma 奶奶；⑧ cousins 表亲。</div>'
    add(cloze_inner, 2)
    vdiff = (section_head("词", "新词 ③ · 近义词/形近词辨析") + sub_label("形近词成对记，避免拼写混淆") +
             key_points([(kw, desc) for kw, desc in VDIFF_L2]) +
             '<div class="note-panel"><div class="np-title">辨析口诀</div>指示看单复远近，长辈看性别结尾；father/mother、son/daughter 成对记，uncle/aunt 辨男女。</div>' +
             '<div class="body-text">辨析不是死记，而是“见词想搭档”：father→mother，grandpa→grandma，uncle→aunt。</div>')
    add(vdiff, 2)
    vdict = (section_head("词", "新词 ④ · 听写自测（点击翻牌）") + sub_label("看中文，翻牌核对英文拼写") +
             recall_grid([(cn, en) for cn, en in VDICT_L2]) +
             '<div class="body-text">家长可对照此页听写；错词请回到新词页重记。</div>' +
             '<div class="note-panel"><div class="np-title">记忆提示</div>先记“长辈/同辈”家庭词，再记“近单/近复/远单/远复”指示代词，分组记忆效率更高。</div>')
    add(vdict, 2)

    # 段3 语法精讲
    for gi, g in enumerate(GRAMMAR_L2, 1):
        t = g["title"]
        pa = (section_head("法", "考点%d · 构成与用法 + 例句" % gi) +
              '<div class="sub-label">一 · 构成与用法</div>' +
              '<div class="body-text">%s</div>' % g["usage"] +
              '<div class="sub-label">二 · 典型例句</div>' +
              example_section(g["examples"]) +
              '<div class="sub-label">三 · 中考怎么考</div>' +
              '<div class="note-panel"><div class="np-title">考法预警</div>%s</div>' % GRAMMAR_NOTE_L2.get(gi, ""))
        add(pa, 3, t, "语法精讲")
        pb = (section_head("法", "考点%d · 易错 + 口诀 + 色卡" % gi) +
              '<div class="sub-label">三 · 高频易错</div>' +
              error_callout(g["errors"]) +
              '<div class="sub-label">四 · 记忆口诀</div>' +
              '<div class="note-panel"><div class="np-title">口诀</div>%s</div>' % g["mnemonic"] +
              '<div class="sub-label">五 · 语法要点色卡</div>' +
              grammar_cards(g["cards"]))
        add(pb, 3, t, "语法精讲")
        pc = section_head("法", "考点%d · 中考考法·即时小测" % gi)
        for q, opts in GEXTRA_L2.get(gi, []):
            pc += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
            for letter, text, cor in opts:
                pc += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
            pc += '</div>'
        pc += '<div class="body-text">中考常在语篇中混考指示代词单复数与 be 动词，看清“近远/单复”再下笔。</div>'
        add(pc, 3, t, "语法精讲")
    dem_mat = (section_head("法", "指示代词全家福 · 远近单复表") + sub_label("this/that/these/those 一网打尽") +
        '<table class="pm-table">' +
        '<tr><th class="pm-num">远近</th><th>单数</th><th>复数</th><th class="pm-zhug">含义</th></tr>' +
        '<tr><th class="pm-num">近指</th><td class="pm-zhug">this</td><td class="pm-zhug">these</td><td>这 / 这些</td></tr>' +
        '<tr><th class="pm-num">远指</th><td class="pm-bin">that</td><td class="pm-bin">those</td><td>那 / 那些</td></tr>' +
        '</table>' +
        '<div class="note-panel"><div class="np-title">记忆顺序</div>近指 this→these（单→复），远指 that→those（单→复）；be 动词随单复数用 is/are。</div>')
    add(dem_mat, 3)
    gsum = (section_head("法", "三大考点综合梳理") +
            key_points([("指示代词", "this/that 单数，these/those 复数；近指 vs 远指。"),
                        ("be 否定疑问", "否定 be+not；疑问 be 提前。"),
                        ("Who 问人", "Who + be + 主？回答用主格。"),
                        ("中考考法", "句型转换与完形常考指示代词与 be 动词一致。"),
                        ("顺序记忆", "近单 this→近复 these→远单 that→远复 those。")]) +
            '<div class="note-panel"><div class="np-title">易混速记</div>this↔these，that↔those；否定 not 跟 be，疑问 be 领前。</div>' +
            '<div class="sub-label">实战例句</div>' +
            example_section([("These are my books.", "these 复数近指"),
                             ("That is not my pen.", "that 单数 + 否定"),
                             ("Who are they?", "Who 问人 + 复数")]))
    add(gsum, 3)
    zhenti = (section_head("法", "中考真题体验 · 指示代词与 be 动词") +
              reading_block("微阅读 · 语法填空",
                  ["Look at ____ (this) boy. ____ (that) girls are my sisters.",
                   "____ (be) your parents teachers? Yes, they ____ (be)."],
                  [("1","空格处用 this 还是 these？",[("A","this","1"),("B","these","0"),("C","that","0")]),
                   ("2","“我的父母”作主语，be 动词用？",[("A","is","0"),("B","are","1"),("C","am","0")])]) +
              '<div class="body-text">中考常把指示代词单复数与 be 动词混在同一语篇中考查，务必看清单复数。</div>' +
              '<div class="note-panel"><div class="np-title">真题解析</div>题1 空格后 boy 单数，用 this；题2 父母为复数，be 动词用 are。</div>')
    add(zhenti, 3)
    pfill = section_head("法", "语法综合应用 · 指示代词与 be 填空") + sub_label("用正确指示代词与 be 动词填空")
    for q, opts in PRONFILL_L2:
        pfill += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            pfill += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        pfill += '</div>'
    pfill += '<div class="body-text">综合考查指示代词单复数与 be 动词一致，是中考“语法填空”微型演练。</div>'
    pfill += '<div class="note-panel"><div class="np-title">填空思路</div>① 看指代对象单/复选 this/these 或 that/those；② 看主语人称/数选 am/is/are；③ Who 问人回答用主格。</div>'
    add(pfill, 3)

    # 段4 随堂演练
    quiz_all = QUIZ_L2 + QUIZ_EXTRA_L2 + QUIZ_EXTRA2_L2 + QUIZ_EXTRA3_L2
    q1 = section_head("练", "随堂演练 ① · 语法选择（1–14）")
    for q, opts in quiz_all[:14]:
        q1 += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            q1 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        q1 += '</div>'
    q1 += '<div class="note-panel"><div class="np-title">解题锦囊</div>① 题1、2、14、17、19、20、22 考指示代词单复数；② 题3、4、6、10、11、13、16、21、25 考 be 否定/疑问；③ 题5、9、12、15、18、23、27 考 Who 问人。</div>'
    add(q1, 4)
    q2 = section_head("练", "随堂演练 ② · 语法选择（15–28）")
    for q, opts in quiz_all[14:]:
        q2 += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            q2 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        q2 += '</div>'
    q2 += '<div class="note-panel"><div class="np-title">解题锦囊</div>看清“空格后有无名词/指代单复”是指示代词选题关键；be 动词随主语人称与数变化；Who 问人回答必用主格。</div>'
    add(q2, 4)
    drill = section_head("练", "句型操练 · 中译英（点击翻牌看答案）") + sub_label("用本课语法翻译下列句子")
    drill += recall_grid([(cn, en) for cn, en in DRILL_L2])
    drill += '<div class="body-text">先自己说/写英文，再翻牌核对；重点用对指示代词与 be 否定/疑问。</div>'
    drill += '<div class="note-panel"><div class="np-title">翻译要点</div>中文“这/那”对应 this/that（单）或 these/those（复）；“不是”译 be not；“谁”译 Who。</div>'
    add(drill, 4)
    fill = (section_head("练", "语法填空演练") +
            '<div class="quiz-q"><div class="qq-text">1. This ___ (be) a book. Those ___ (be) pens.</div>'
            '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">is; are</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">are; is</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">is; is</button></div>'
            '<div class="quiz-q"><div class="qq-text">2. ___ (Who) is he? He ___ (be not) my brother.</div>'
            '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">Who; is not</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">What; is not</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">Who; are not</button></div>'
            '<div class="quiz-q"><div class="qq-text">3. ___ (That) girls ___ (be) my sisters.</div>'
            '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">Those; are</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">That; are</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">Those; is</button></div>'
            '<div class="body-text">语法填空是湖南中考省卷“语法诊断/语法填空”题型的微型演练。</div>' +
            '<div class="note-panel"><div class="np-title">解析</div>题1 单数 this→is，复数 those→are；题2 Who 问人，主语 he→is not；题3 girls 复数→Those are。</div>')
    add(fill, 4)
    errd = section_head("练", "随堂演练 ③ · 改错专练") + sub_label("找出错误项并改正")
    for q, opts in ERRDRILL_L2:
        errd += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            errd += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        errd += '</div>'
    errd += '<div class="body-text">改错题是中考“语法诊断”的变形，先找错再用正确形式替换。</div>'
    errd += '<div class="note-panel"><div class="np-title">改错思路</div>先判断错在哪一类：指示代词单复数混淆、be 否定语序错、还是 Who 句型语序错，再替换。</div>'
    add(errd, 4)

    # 段5 阅读理解
    o2 = OLD.get("2", {})
    ra = o2.get("reading_a", {}).get("text", "")
    paras_a = [s.strip() for s in ra.replace("A Come", "Come").split(".") if s.strip()]
    if not paras_a:
        paras_a = ["Come and see our family photo album!", "It is big and nice.",
                   "In the first picture, you can see my grandpa and grandma.",
                   "In the next picture are my father, my mother and me.",
                   "Look at the little boy! That is my cute cousin.",
                   "We are a happy family."]
    rb_text = ("This is a photo of my family. The man is my father. "
               "The woman is my mother. The boy is my brother. "
               "The girl is my sister. We are a happy family. I love my family very much.")
    paras_b = [s.strip() for s in rb_text.split(".") if s.strip()]
    qa = [("1", "What is big and nice?", [("A","The photo album","1"),("B","The school","0"),("C","The classroom","0")]),
          ("2", "Who are in the first picture?", [("A","Father and mother","0"),("B","The cousin","0"),("C","Grandpa and grandma","1")]),
          ("3", "What are grandpa and grandma like?", [("A","Tall","0"),("B","Cute","0"),("C","Kind","1")]),
          ("4", "Who is the little boy?", [("A","The writer","0"),("B","The cousin","1"),("C","The brother","0")]),
          ("5", "Where does the writer welcome us?", [("A","To the class show","0"),("B","To a hospital","1"),("C","To a shop","0")]),
          ("6", "How is the family?", [("A","Small","0"),("B","Big and happy","1"),("C","Sad","0")]),
          ("7", "Who are in the next picture?", [("A","Father, mother and me","1"),("B","Grandparents","0"),("C","Cousins","0")])]
    add(section_head("读", "阅读 A · Our Family Photo（篇章）") +
        '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in paras_a) + '</div>' +
        '<div class="body-text">读前先猜：这是一篇关于“家庭相册”的说明，注意人物与位置关系。</div>' +
        '<div class="note-panel"><div class="np-title">中文大意</div>来看我们的家庭相册！它又大又漂亮。第一张照片里是你爷爷和奶奶，他们很和蔼。下一张是我爸爸、妈妈和我。看那个小男孩！那是我的可爱表弟。我们是一个幸福的家庭，欢迎来看我们的班级展示！</div>' +
        '<div class="note-panel"><div class="np-title">长难句拆解</div>'
        '① “In the next picture are my father, my mother and me.” —— 倒装句，正常语序为 My father… are in the next picture。<br>'
        '② “Look at the little boy!” —— Look at 后接宾语，the little boy 整体作宾语。</div>', 5)
    a_q = reading_block("阅读 A · 理解题", paras_a, [qa[0],qa[1],qa[2],qa[3]])
    a_q += '<div class="note-panel"><div class="np-title">答案解析</div>题1 细节定位首句“big and nice”指相册；题2 由“first picture…grandpa and grandma”得；题3 由“They are kind”得；题4 由“That is my cute cousin”得。</div>'
    add(a_q, 5)
    add(section_head("读", "阅读 B · My Family（篇章）") +
        '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in paras_b) + '</div>' +
        '<div class="body-text">圈出每个家庭成员，回题定位更快。</div>' +
        '<div class="note-panel"><div class="np-title">中文大意</div>这是一张我的全家福。这位男士是我爸爸，这位女士是我妈妈，这个男孩是我哥哥，这个女孩是我妹妹。我们是个幸福的家庭，我非常爱我的家。</div>' +
        '<div class="note-panel"><div class="np-title">长难句拆解</div>'
        '① “The man is my father.” —— 定冠词 the 特指前文提到的人；<br>'
        '② “I love my family very much.” —— very much 表程度，放在句末。</div>', 5)
    b_q = reading_block("阅读 B · 理解题", paras_b, [qa[4],qa[5],qa[6]])
    b_q += '<div class="note-panel"><div class="np-title">答案解析</div>题5 由“Welcome to our class show”得地点；题6 由“happy family”得幸福；题7 由“father, mother and me”得下一页人物。</div>'
    add(b_q, 5)
    w5paras = ["Hello! I am Linda.", "This is my family tree. __(11)__",
               "My father is a teacher and my mother is a nurse. __(12)__",
               "They are old but healthy. __(13)__", "My brother is a student. __(14)__",
               "I love my big family."]
    w5opts = [("A","I have a happy family."),("B","My grandparents are kind."),
              ("C","He likes playing basketball."),("D","She is a nice girl."),("E","We often have dinner together.")]
    w5ans = {11:"A",12:"B",13:"C",14:"E"}
    add(section_head("读", "阅读 C · 五选四（Linda's Family Tree·篇章）") +
        '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in w5paras) + '</div>' +
        '<div class="body-text">从 A–E 中选出最佳句子填入 __（11–14）__ 空白，注意前后逻辑衔接（D 为多余项，五选四）。</div>' +
        '<div class="note-panel"><div class="np-title">中文大意</div>你好，我是琳达。这是我的家谱。我有一个幸福的家庭。爸爸是老师，妈妈是护士。我的爷爷奶奶很和蔼，他们年迈但健康。我的哥哥是学生，他喜欢打篮球。我爱我的大家庭。</div>', 5)
    w5q = section_head("读", "阅读 C · 五选四（题目）")
    for num in sorted(w5ans.keys()):
        ans = w5ans[num]
        w5q += '<div class="quiz-q"><div class="qq-text">__（%d）__ 应填：</div>' % num
        for letter, text in w5opts:
            cor = '1' if letter == ans else '0'
            w5q += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        w5q += '</div>'
    w5q += '<div class="note-panel"><div class="np-title">答案解析</div>11→A（总起家庭）；12→B（爷爷奶奶和蔼，呼应 old but healthy）；13→C（He 指代 brother 打篮球）；14→E（全家共进晚餐，收束）；D 为多余项。</div>'
    add(w5q, 5)
    reading_tip = (section_head("读", "阅读解题 SOP") +
                   key_points([("先题后文", "先读题干圈关键词，再回原文定位。"),
                               ("细节题", "题干词多在原文原词复现，直接比对。"),
                               ("五选四", "看空白前后句逻辑，排除重复/矛盾项。"),
                               ("防陷阱", "注意指示代词 this/that/these/those 的单复数与人称。"),
                               ("猜词法", "利用上下文线索、同义复现猜测生词含义。"),
                               ("主旨题", "找首尾句与高频词，避免以偏概全。")]) +
                   '<div class="note-panel"><div class="np-title">本课的阅读</div>'
                   'A/B 篇为家庭细节题，C 篇为五选四逻辑衔接题，指示代词与人称一致是定位关键。</div>')
    add(reading_tip, 5)
    rmore = (section_head("读", "阅读实战 · 细节定位再练") +
             '<div class="body-text">下列题目需回看前面“阅读 A：相册”与“阅读 B：全家福”篇章定位（答案请回原文核对）。</div>')
    rmore_quiz = [
        ("1", "Where can we see the family photo album?", [("A","In a class show","1"),("B","In a hospital","0"),("C","In a shop","0")]),
        ("2", "Who is the cute boy in Picture One?", [("A","The writer's brother","0"),("B","The writer's cousin","1"),("C","The writer's father","0")]),
        ("3", "What is Linda's father?", [("A","A nurse","0"),("B","A teacher","1"),("C","A student","0")]),
        ("4", "Who does Linda love?", [("A","Her brother","0"),("B","Her family","1"),("C","Her friends","0")]),
        ("5", "Is Linda's brother a student?", [("A","Yes, he is","1"),("B","No, he isn't","0"),("C","He is a teacher","0")]),
        ("6", "What is Linda's mother?", [("A","A nurse","1"),("B","A teacher","0"),("C","A student","0")]),
        ("7", "Are Linda's grandparents healthy?", [("A","Yes, they are","1"),("B","No, they aren't","0"),("C","They are old","0")]),
    ]
    for qnum, q, opts in rmore_quiz:
        rmore += '<div class="quiz-q"><div class="qq-text">%s. %s</div>' % (qnum, q)
        for letter, text, cor in opts:
            rmore += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        rmore += '</div>'
    rmore += '<div class="note-panel"><div class="np-title">定位提示</div>题1 回阅读 A 找“class show”；题2 由“cute cousin”得表弟；题3 回阅读 B/C 找 father 职业；题4 由“love my family”得家人；题5 由“brother is a student”得。</div>'
    add(rmore, 5)

    # 段6 自然拼读
    add(phonics_block(PHONICS_L2), 6)
    ph2 = (section_head("拼", "字母组合拼读演练") +
           key_points([("th /ð/", "this, that, these, those, they——舌尖夹齿。"),
                       ("sh /ʃ/", "she, ship, fish, dish——气擦成音。"),
                       ("ch /tʃ/", "chair, china, much, rich——破擦成音。"),
                       ("wh /h//w/", "who, what, when, where——问词开头。"),
                       ("ph /f/", "photo, phone, phrase——ph 发 /f/。")]) +
           '<div class="sub-label">常见词族</div>' +
           key_points([("-at", "that, cat, hat, mat"),
                       ("-sh", "she, fish, dish"),
                       ("-ch", "chair, much, rich"),
                       ("-th", "this, that, with"),
                       ("-wh", "who, what, when")]) +
           '<div class="note-panel"><div class="np-title">拼读口诀</div>'
           'th 咬舌、sh 嘘气、ch 破擦、wh 问词、ph 发 f；组合发音要“稳准快”。</div>')
    add(ph2, 6)
    ph3 = (section_head("拼", "字母组合拼读小结 · 儿歌") +
           '<div class="note-panel"><div class="np-title">拼读儿歌</div>'
           'th th /ð/ this that 咬舌尖，sh sh /ʃ/ she ship 嘘一嘘；<br>ch ch /tʃ/ chair much 破擦响，wh wh /w/ who what 问起来；<br>ph ph /f/ photo phone 记分明，字母组合要记牢！</div>' +
           key_points([("口型", "th 舌尖轻触上齿，气流从缝逸出。"),
                       ("位置", "sh/ch 为双辅音组合，一次成音。"),
                       ("问词", "wh 开头多为疑问词 who/what/when/where。"),
                       ("ph 特例", "ph 在英语中固定发 /f/，如 photo/phone。"),
                       ("对比", "th 清浊：thank(清/θ/) vs this(浊/ð/)。"),
                       ("练习", "this/that 反复读，体会咬舌感。"),
                       ("sh/ch 区别", "sh 纯摩擦，ch 破擦带爆破，听感不同。"),
                       ("wh 发音", "who 在 o 前读 /h/，what/when 读 /w/。")]))
    add(ph3, 6)

    # 段7 课堂练习
    cv1 = section_head("戏", "课堂游戏 · 跨课词汇快选 ①") + sub_label("看中文，选出正确英文")
    cv1 += '<div class="note-panel"><div class="np-title">玩法</div>点击与中文对应的英文词，答对响铃。</div>'
    for cn, en, opts in CROSS_L2[:4]:
        cv1 += '<div class="quiz-q"><div class="qq-text">“%s” 是哪个词？</div>' % cn
        for w, cor in opts:
            cv1 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s</button>' % (cor, w)
        cv1 += '</div>'
    cv1 += '<div class="note-panel"><div class="np-title">提示</div>遇到形近词（father/mother、son/daughter）先辨性别再选；指示代词看单复远近。</div>'
    add(cv1, 7)
    cv2 = section_head("戏", "课堂游戏 · 跨课词汇快选 ②") + sub_label("看中文，选出正确英文")
    for cn, en, opts in CROSS_L2[4:]:
        cv2 += '<div class="quiz-q"><div class="qq-text">“%s” 是哪个词？</div>' % cn
        for w, cor in opts:
            cv2 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s</button>' % (cor, w)
        cv2 += '</div>'
    cv2 += '<div class="note-panel"><div class="np-title">游戏小结</div>跨课词汇快选训练“音—形—义”对应，是听力与完形的基础；错词请回到新词页再记。</div>'
    add(cv2, 7)
    listen = (section_head("戏", "听音选词 · 词义匹配") + sub_label("下列英文，哪个意思是“家庭”？") +
              '<div class="quiz-q"><div class="qq-text">“家庭” 对应：</div>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">family</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">photo</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">friend</button></div>'
              '<div class="quiz-q"><div class="qq-text">“兄弟” 对应：</div>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">sister</button>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">brother</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">cousin</button></div>'
              '<div class="quiz-q"><div class="qq-text">“这些” 对应：</div>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">these</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">those</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">this</button></div>'
              '<div class="quiz-q"><div class="qq-text">“谁” 对应：</div>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">who</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">what</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">where</button></div>'
              '<div class="body-text">巩固本课核心词义，为听力与完形打底。</div>')
    add(listen, 7)

    # 段8 课堂总结
    summary = (section_head("结", "课堂总结 · 知识图谱") +
               '<div class="kmap">' +
               '<div class="kmap-node"><div class="kn-title">指示代词</div><div class="kn-body">this/that 单数，these/those 复数；近指 vs 远指。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">be 否定疑问</div><div class="kn-body">否定 be+not；疑问 be 提前；回答主谓一致。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">Who 问人</div><div class="kn-body">Who + be + 主？回答用主格 he/she/they。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">自然拼读</div><div class="kn-body">th/sh/ch/wh/ph 字母组合发音。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">学习建议</div><div class="kn-body">每天听写 5 词＋造 2 句，周末回头复习，指示代词与 be 动词务必熟练。</div></div>' +
               '</div>' +
               '<div class="note-panel"><div class="np-title">课后作业</div>'
               '① 背诵本课 20 个新词（家长听写）；② 完成配套基础练习；③ 用指示代词 + be 疑问句写 5 句家庭介绍；④ 整理错题本（本课易错 10 句）。</div>' +
               '<div class="note-panel"><div class="np-title">巩固建议</div>错题本按“指示代词”“be 否定疑问”“Who”三类归档，每周回看一次，避免重复犯错。</div>')
    add(summary, 8)
    err_review = (section_head("结", "易错清单回顾") +
                  error_callout([("These is my book.","This is my book."),
                                 ("He not is a boy.","He is not a boy."),
                                 ("Who are he?","Who is he?"),
                                 ("That are my dogs.","Those are my dogs."),
                                 ("They isn't students.","They aren't students."),
                                 ("Who he is?","Who is he?"),
                                 ("This are friends.","These are friends."),
                                 ("Are not they here?","Are they not here?"),
                                 ("That is not my pen.","That is not my pen."),
                                 ("Who is they?","Who are they?")]) +
                  '<div class="note-panel"><div class="np-title">避坑口诀</div>指示看单复远近，否定 not 跟 be，疑问 be 领前；Who 专问人，语序主在前。</div>')
    add(err_review, 8)
    preview = (section_head("结", "下节课预告 · 第 3 课") +
               key_points([("语法①", "名词所有格（'s）与 of 属格。"),
                           ("语法②", "基数词（one–ten）与编号表达。"),
                           ("语法③", "Where 引导的特殊疑问句（地点）。"),
                           ("新词", "room/bed/desk/table 等方位与物品词汇。")]) +
               '<div class="note-panel"><div class="np-title">课前准备</div>复习本课指示代词与 be 动词，下节课用它们来问“东西在哪里 / 是谁的”。</div>' +
               '<div class="note-panel"><div class="np-title">课前任务</div>① 默写本课 20 词（家长签字）；② 用 Who 造 2 句；③ 预习名词所有格含义。</div>')
    add(preview, 8)

    total = p - 1
    seg_pages = {}
    for sid, (a, b) in seg.items():
        seg_pages[sid] = [a, b]
    return pages, seg_pages, total

# ===================== L3 内容 =====================
VOCAB_L3 = [
    ("room","/ruːm/","n.","房间","in the room","This is my room.","room 房间，oo 像两扇窗"),
    ("bed","/bed/","n.","床","go to bed","The book is on the bed.","bed 床，b 像床头"),
    ("desk","/desk/","n.","书桌","at the desk","Tom's desk is tidy.","desk 书桌，d 开头"),
    ("table","/ˈteɪbl/","n.","桌子","on the table","The ruler is on the table.","table 桌，ta 开头"),
    ("book","/bʊk/","n.","书","a Chinese book","I like this book.","book 书，oo 短音/ʊ/"),
    ("schoolbag","/ˈskuːlbæɡ/","n.","书包","my schoolbag","My schoolbag is blue.","school+bag 上学袋"),
    ("pencil","/ˈpensl/","n.","铅笔","a pencil box","I have a red pencil.","pen+cil 笔"),
    ("pen","/pen/","n.","钢笔","two pens","The pen is his.","pen 钢笔，en 结尾"),
    ("ruler","/ˈruːlə/","n.","尺子","a long ruler","Where is my ruler?","ruler 尺，rule+er"),
    ("eraser","/ɪˈreɪzə/","n.","橡皮","an eraser","Her eraser is white.","erase 擦+er→橡皮"),
    ("dictionary","/ˈdɪkʃənri/","n.","词典","an English dictionary","The dictionary is new.","diction 措辞+ary"),
    ("library","/ˈlaɪbrəri/","n.","图书馆","in the library","Go to the library.","libr 书+ary"),
    ("classroom","/ˈklɑːsruːm/","n.","教室","in the classroom","Our classroom is big.","class+room"),
    ("office","/ˈɒfɪs/","n.","办公室","the library office","Come to the office.","office 办公室，off 开头"),
    ("lost","/lɒst/","adj.","丢失的","a lost book","My card is lost.","lost 丢的，lose 过去"),
    ("found","/faʊnd/","v./adj.","找到","lost and found","The pen is found.","found find 过去"),
    ("thing","/θɪŋ/","n.","东西；物品","your things","Where are my things?","thing 东西，th 咬舌"),
    ("card","/kɑːd/","n.","卡片","a school ID card","My card is white.","card 卡，c 开头"),
    ("picture","/ˈpɪktʃə/","n.","图片；照片","a cat picture","There is a picture on it.","pict 画+ure"),
    ("computer","/kəmˈpjuːtə/","n.","电脑","on the computer","The computer is new.","compute 计算+er"),
]

GRAMMAR_L3 = [
    {
        "title": "语法① · 名词所有格（'s）与 of 属格",
        "usage": "有生命名词表“……的”在词尾加 <b>'s</b>（Tom's desk）；以 s 结尾的复数只加 <b>'</b>（the students' books）；无生命常用 <b>of</b> 属格（the cover of the dictionary）。注意 <b>it's</b>（it is 缩写）和 <b>its</b>（它的）完全不同。",
        "examples": [
            ("Tom's desk is tidy.", "汤姆的书桌很整洁。（单数名词+'s）"),
            ("The boy's pencil box is blue.", "男孩的文具盒是蓝色的。"),
            ("The students' books are new.", "学生们的书是新的。（复数 s 结尾加'）"),
            ("The cover of the dictionary is red.", "词典的封皮是红色的。（无生命用 of）"),
            ("The name of the school is long.", "学校的名字很长。"),
            ("This is my friend's room.", "这是我朋友的房间。"),
            ("The teachers' office is there.", "老师们的办公室在那边。"),
            ("Its color is blue.", "它的颜色是蓝色。（its 它的，无撇）"),
        ],
        "keypoints": [
            ("有生命加 's", "Tom's / the boy's，单数名词直接加 's。"),
            ("复数 s 结尾加 '", "students' / teachers'，以 s 结尾复数只加撇。"),
            ("无生命用 of", "the cover of the dictionary，无生命用 of 属格。"),
            ("it's ≠ its", "it's = it is 缩写；its = 它的，二者不可混。"),
        ],
        "errors": [
            ("its a book.", "It's a book."),
            ("The boy book is red.", "The boy's book is red."),
            ("cover of dictionary is red.", "The cover of the dictionary is red."),
            ("The students book are new.", "The students' books are new."),
        ],
        "mnemonic": "有生命加 's，复数 s 结尾只加 '；无生命用 of，it's 是缩写，its 才是‘它的’。",
        "cards": [("主格/用法","有生命名词+'s 表‘……的’"),
                  ("复数","以 s 结尾复数只加 '（students'）"),
                  ("警示","it's = it is；its = 它的，千万别混。")],
    },
    {
        "title": "语法② · 基数词（one–ten）与编号表达",
        "usage": "基数词 one, two, three … ten 表数量；<b>编号</b>用“名词 + 基数词”且名词与数字组合首字母大写：Class 3、Room 305、No. 1；表顺序也可用“the + 序数词”。",
        "examples": [
            ("I have three pens.", "我有三支钢笔。（数量）"),
            ("We are in Class 3.", "我们在三班。（编号：名词+基数词）"),
            ("My room is Room 305.", "我的房间是 305 室。"),
            ("This is No. 1 Middle School.", "这是第一中学。"),
            ("There are two books on the desk.", "桌上有两本书。"),
            ("He is Number 8 in the team.", "他在队里是 8 号。"),
            ("Ten students are in the library.", "十名学生在图书馆。"),
            ("The first book is mine.", "第一本书是我的。（序数词）"),
        ],
        "keypoints": [
            ("数量用基数词", "one–ten 直接表数目。"),
            ("编号大写", "Class 3 / Room 305，名词与数字组合首字母大写。"),
            ("顺序用序数词", "第一 the first，第二 the second。"),
            ("No. 缩写", "No. 1 = Number 1，编号常用。"),
        ],
        "errors": [
            ("class 3 is my class.", "Class 3 is my class."),
            ("I am in the class 3.", "I am in Class 3."),
            ("three book on the desk.", "three books on the desk."),
            ("The one book is red.", "The first book is red."),
        ],
        "mnemonic": "数量用基数，编号名词大写连数字；Class 3、Room 305，顺序改用 first/second。",
        "cards": [("基数词","one–ten 表数量"),
                  ("编号","Class 3 / Room 305（名词+数字，大写）"),
                  ("警示","编号名词首字母必须大写，不可用 class 3。")],
    },
    {
        "title": "语法③ · Where 引导的特殊疑问句（地点）",
        "usage": "<b>Where + be + 主语？</b> 用来问“某物/某人在哪里”，回答用 <b>It is / They are + 地点介词短语</b>（in/on/under）。be 动词随主语单复数变化。",
        "examples": [
            ("Where is my schoolbag?", "我的书包在哪里？（单数 → is）"),
            ("It is on the desk.", "它在书桌上。（答语含地点介词 on）"),
            ("Where are my books?", "我的书在哪里？（复数 → are）"),
            ("They are under the table.", "它们在桌子下面。（under 在……下）"),
            ("Where is Tom's ruler?", "汤姆的尺子在哪里？"),
            ("It is in the pencil box.", "它在文具盒里。（in 在……里）"),
            ("Where are the pens?", "那些钢笔在哪里？"),
            ("They are on the bed.", "它们在床上。"),
        ],
        "keypoints": [
            ("Where 问地点", "Where + be + 主语？专门问位置。"),
            ("答语带介词", "答语必须有 in/on/under 等地点介词。"),
            ("be 随主谓一致", "单数 is，复数 are。"),
            ("就近/指代", "it 代单数物，they 代复数物。"),
        ],
        "errors": [
            ("Where my book is?", "Where is my book?"),
            ("It on the desk.", "It is on the desk."),
            ("Where are my book?", "Where is my book?"),
            ("They is under the table.", "They are under the table."),
        ],
        "mnemonic": "Where 问地点，be 提前；答语 it/they + in/on/under，单 is 复 are 别乱。",
        "cards": [("Where","Where + be + 主语？问地点"),
                  ("答语","It/They + in/on/under + 地点"),
                  ("警示","疑问 be 提前，答语必有地点介词。")],
    },
]

GRAMMAR_NOTE_L3 = {
    1: "名词所有格是湖南中考省卷‘语法填空’高频点，尤以‘it's/its 混淆’‘复数 s 结尾漏撇’‘无生命误用 's’ 为三大陷阱。",
    2: "基数词与编号常考‘Class 3 首字母大写’‘编号名词在前’‘数量名词用复数’，单选与填空都可能出现。",
    3: "Where 问句是七上核心特殊疑问句，中考常在‘疑问语序 be 提前’与‘答语缺地点介词’设错，务必熟记句型。",
}

RECALL_L3 = [
    ("“汤姆的”书桌怎么说？", "Tom's desk（单数+'s）"),
    ("复数以 s 结尾怎么加所有格？", "只加 '（students'）"),
    ("“词典的封皮”用 's 还是 of？", "of（the cover of the dictionary）"),
    ("it's 和 its 区别？", "it's=it is；its=它的"),
    ("“三班”英文怎么写？", "Class 3（名词+数字大写）"),
    ("“305 室”英文？", "Room 305"),
    ("“我有三支钢笔”用哪个数词？", "three（基数词表数量）"),
    ("Where 问句语序？", "Where + be + 主语？"),
    ("“我的书包在哪”答语？", "It is on the desk."),
    ("复数物品 Where 答语 be 用？", "are（They are…）"),
    ("“在桌子下”介词？", "under（under the table）"),
    ("“在文具盒里”介词？", "in（in the pencil box）"),
]

PHONICS_L3 = [
    ("th","thing /θɪŋ/","东西·咬舌/θ/"),
    ("wh","where /weə/","哪里·问词"),
    ("ph","photo /ˈfəʊtəʊ/","照片·ph发/f/"),
    ("ng","ring /rɪŋ/","戒指·鼻音/ŋ/"),
    ("nk","think /θɪŋk/","想·鼻音+k"),
    ("th","that /ðæt/","那个·浊/ð/"),
    ("wh","what /wɒt/","什么·问词"),
    ("ph","phone /fəʊn/","电话·ph发/f/"),
    ("ng","sing /sɪŋ/","唱·鼻音"),
    ("nk","pink /pɪŋk/","粉·鼻音+k"),
]

QUIZ_L3 = [
    ("1. — Whose desk is this? — It's ____ desk.", [("A","Tom's","1"),("B","Toms","0"),("C","Tom","0"),("D","Toms'","0")]),
    ("2. — Where ____ your books? — ____ on the desk.", [("A","is; It is","0"),("B","are; They are","1"),("C","is; They are","0"),("D","are; It is","0")]),
    ("3. The cover ____ the dictionary is red.", [("A","for","0"),("B","to","0"),("C","of","1"),("D","'s","0")]),
    ("4. We are in ____ .", [("A","class 3","0"),("B","Class three","0"),("C","class Three","0"),("D","Class 3","1")]),
    ("5. — ____ is my ruler? — It is under the chair.", [("A","Where","1"),("B","What","0"),("C","Who","0"),("D","How","0")]),
    ("6. The ____ book is red.", [("A","students","0"),("B","student's","1"),("C","student","0"),("D","students'","0")]),
]

QUIZ_EXTRA_L3 = [
    ("7. — ____ this your eraser? — No, it's ____ .", [("A","Is; its","0"),("B","Are; its","0"),("C","Is; it's","1"),("D","Are; it's","0")]),
    ("8. There are ____ books in the schoolbag.", [("A","second","0"),("B","the two","0"),("C","twos","0"),("D","two","1")]),
    ("9. — Where ____ the pens? — ____ in the box.", [("A","are; They are","1"),("B","is; It is","0"),("C","is; They are","0"),("D","are; It is","0")]),
    ("10. This is my ____ room.", [("A","friend","0"),("B","friend's","1"),("C","friends","0"),("D","friends'","0")]),
    ("11. My room is ____ .", [("A","room 201","0"),("B","Room two zero one","0"),("C","Room 201","1"),("D","the room 201","0")]),
    ("12. — ____ is the boy's pencil box? — It is blue.", [("A","Who","0"),("B","How","0"),("C","Which","0"),("D","What color","1")]),
]

QUIZ_EXTRA2_L3 = [
    ("13. — Whose dictionary is this? — It's ____ .", [("A","the boy's","1"),("B","the boy","0"),("C","the boys","0"),("D","boy's","0")]),
    ("14. ____ students are in the classroom.", [("A","Tenth","0"),("B","Ten","1"),("C","The ten","0"),("D","Tens","0")]),
    ("15. — Where is Tom's ruler? — ____ under the book.", [("A","It are","0"),("B","Its","0"),("C","It's","1"),("D","It","0")]),
    ("16. The ____ office is on the first floor.", [("A","teacher","0"),("B","teachers","0"),("C","teacher's","0"),("D","teachers'","1")]),
    ("17. — ____ your schoolbag? — It is in the library.", [("A","Where's","1"),("B","Where","0"),("C","What","0"),("D","Who","0")]),
    ("18. The books are ____ the table.", [("A","in","0"),("B","on","1"),("C","of","0"),("D","for","0")]),
    ("19. — Is this ____ book? — No, it's ____ .", [("A","her; her","0"),("B","hers; her","0"),("C","her; hers","1"),("D","hers; hers","0")]),
    ("20. We are in ____ .", [("A","class 2","0"),("B","Class two","0"),("C","class Two","0"),("D","Class 2","1")]),
]

QUIZ_EXTRA3_L3 = [
    ("21. — ____ the students' books? — They are on the desk.", [("A","Where are","1"),("B","Where's","0"),("C","What are","0"),("D","Where","0")]),
    ("22. This is ____ eraser.", [("A","Tom","0"),("B","Tom's","1"),("C","Toms","0"),("D","Toms'","0")]),
    ("23. There are ____ notebooks in my schoolbag.", [("A","third","0"),("B","the three","0"),("C","three","1"),("D","threes","0")]),
    ("24. — Where ____ the dictionary? — ____ in the library.", [("A","are; They are","0"),("B","is; They are","0"),("C","are; It is","0"),("D","is; It is","1")]),
    ("25. The cover of ____ dictionary is red.", [("A","the","1"),("B","a","0"),("C","an","0"),("D","/","0")]),
    ("26. — ____ is my computer? — It is on the table.", [("A","What","0"),("B","Where","1"),("C","Who","0"),("D","Which","0")]),
    ("27. — Is this your card? — No, ____ is blue.", [("A","my","0"),("B","me","0"),("C","mine","1"),("D","I","0")]),
    ("28. Our classroom is ____ .", [("A","room 405","0"),("B","Room four zero five","0"),("C","the Room 405","0"),("D","Room 405","1")]),
]

DRILL_L3 = [
    ("这是汤姆的书桌。", "This is Tom's desk."),
    ("我的书包在书桌上。", "My schoolbag is on the desk."),
    ("尺子在哪里？", "Where is the ruler?"),
    ("它在文具盒里。", "It is in the pencil box."),
    ("我们在三班。", "We are in Class 3."),
    ("词典的封皮是红色的。", "The cover of the dictionary is red."),
    ("学生们的书是新的。", "The students' books are new."),
    ("我的橡皮是白色的。", "My eraser is white."),
    ("两支钢笔在书包里。", "Two pens are in the schoolbag."),
    ("它在桌子下面。", "It is under the table."),
    ("这是第一中学。", "This is No. 1 Middle School."),
    ("我的电脑是新的。", "My computer is new."),
]

CLOZE_L3 = [
    ("The blue pencil box is ___.", [("Tom's","1"),("Tom","0"),("Toms","0")]),
    ("There are two ___ and a ruler.", [("pen","0"),("pens","1"),("pencil","0")]),
    ("The red dictionary is ___.", [("his","1"),("he","0"),("him","0")]),
    ("___ eraser is that?", [("Who","0"),("What","0"),("Whose","1")]),
    ("Is it Tom's? No, it is not ___.", [("he","0"),("him","0"),("his","1")]),
    ("It is his ___ eraser.", [("sister","0"),("sisters","0"),("sister's","1")]),
    ("It is ___ the desk.", [("on","1"),("in","0"),("under","0")]),
    ("There are ___ books in it.", [("two","1"),("second","0"),("the two","0")]),
]

CROSS_L3 = [
    ("房间", "room", [("room","1"),("bed","0"),("desk","0")]),
    ("床", "bed", [("bed","1"),("book","0"),("bag","0")]),
    ("书桌", "desk", [("desk","1"),("table","0"),("chair","0")]),
    ("书包", "schoolbag", [("schoolbag","1"),("school","0"),("bag","0")]),
    ("铅笔", "pencil", [("pen","0"),("pencil","1"),("ruler","0")]),
    ("橡皮", "eraser", [("eraser","1"),("ruler","0"),("dictionary","0")]),
    ("词典", "dictionary", [("dictionary","1"),("library","0"),("office","0")]),
    ("图书馆", "library", [("library","1"),("classroom","0"),("office","0")]),
]

VDIFF_L3 = [
    ("desk / table", "desk 书桌（学习用）；table 桌子（用餐/放物），记‘desk 读书，table 吃饭’。"),
    ("pen / pencil", "pen 钢笔；pencil 铅笔，都带 p，记‘pen 灌墨，pencil 削木’。"),
    ("lost / found", "lost 丢失的（lose 过去）；found 找到的（find 过去），lost and found 失物招领。"),
    ("its / it's", "its 它的（无撇）；it's = it is 缩写，千万别混。"),
    ("room / classroom", "room 房间；classroom 教室（class+room），地点更具体。"),
    ("card / picture", "card 卡片；picture 图片/照片，picture 可指照片。"),
]

VDICT_L3 = [
    ("房间", "room"), ("床", "bed"), ("书桌", "desk"), ("桌子", "table"),
    ("书", "book"), ("书包", "schoolbag"), ("铅笔", "pencil"), ("钢笔", "pen"),
    ("尺子", "ruler"), ("橡皮", "eraser"), ("词典", "dictionary"), ("图书馆", "library"),
]

GEXTRA_L3 = {
    1: [("1. — Whose book is this? — It's ____ .", [("A","the boy","0"),("B","the boy's","1"),("C","the boys","0"),("D","boy's","0")]),
        ("2. The ____ office is there. (teacher)", [("A","teacher","0"),("B","teachers","0"),("C","teachers'","1"),("D","teacher's","0")])],
    2: [("3. We are in ____ .", [("A","class 3","0"),("B","Class 3","1"),("C","class three","0"),("D","Class three","0")]),
        ("4. There are ____ students. (ten)", [("A","ten","1"),("B","tenth","0"),("C","the ten","0"),("D","tens","0")])],
    3: [("5. — ____ your ruler? — It is on the desk.", [("A","Where","0"),("B","Where's","1"),("C","What","0"),("D","Who","0")]),
        ("6. — Where are the pens? — ____ in the box.", [("A","It is","0"),("B","Its","0"),("C","They are","1"),("D","It's","0")])],
}

ERRDRILL_L3 = [
    ("1. its a red book.", [("A","its a red book","0"),("B","It's a red book","1"),("C","It is red book","0")]),
    ("2. The boy book is new.", [("A","The boy book is new","0"),("B","The boy's book is new","1"),("C","The boys book is new","0")]),
    ("3. class 3 is my class.", [("A","class 3 is my class","0"),("B","Class 3 is my class","1"),("C","Class three is my class","0")]),
    ("4. Where my pen is?", [("A","Where my pen is","0"),("B","Where is my pen","1"),("C","Where pen is","0")]),
    ("5. They on the desk.", [("A","They on the desk","0"),("B","They are on the desk","1"),("C","They is on the desk","0")]),
]

PRONFILL_L3 = [
    ("1. This is ____ (Tom) desk. The ____ (book) are on it.", [("A","Tom's; books","1"),("B","Tom; book","0"),("C","Toms; books","0"),("D","Tom's; book","0")]),
    ("2. — ____ (Where) is my schoolbag? — ____ (It) is on the desk.", [("A","Where; It","1"),("B","What; It","0"),("C","Where; They","0"),("D","What; They","0")]),
    ("3. We are in ____ (Class) 3. There are ____ (ten) students.", [("A","Class; ten","1"),("B","class; ten","0"),("C","Class; tenth","0"),("D","class; ten","0")]),
    ("4. The ____ (student) books are new. They are on ____ (they) desks.", [("A","student's; their","0"),("B","students'; their","1"),("C","students; they","0"),("D","student; their","0")]),
]

def build_lesson_3():
    pages = {}
    seg = {}
    p = 1
    def add(inner, seg_id, title="第3课 · 名词所有格/基数词/Where问句", subtitle="Lost and Found · 七上基础"):
        nonlocal p
        pages[p] = page(p, title, subtitle, inner, active=(p == 1))
        seg.setdefault(seg_id, [p, p])
        seg[seg_id][1] = p
        p += 1

    # 段1 复习导入
    cover = ('<div class="cover-wrap"><div class="cover-title">第 3 课</div>'
             '<div class="cover-sub">名词所有格 / 基数词 / Where 问句 · 七上基础</div>'
             '<div class="cover-info">'
             '<div class="cover-info-num"><div class="ci-label">新词</div><div class="ci-val">20</div></div>'
             '<div class="cover-info-num"><div class="ci-label">语法考点</div><div class="ci-val">3</div></div>'
             '<div class="cover-info-num"><div class="ci-label">页数</div><div class="ci-val">45</div></div>'
             '</div></div>')
    add(cover, 1, "第3课 · 名词所有格/基数词/Where问句", "封面")
    goal = (section_head("标", "本课学习目标") +
            key_points([("20 中考高频词", "room/desk/book 等方位物品词 + 失物招领词汇。"),
                        ("3 大语法考点", "①名词所有格 's 与 of ②基数词与编号 ③Where 问地点。"),
                        ("阅读主题", "Lost and Found，训练细节定位与逻辑衔接。"),
                        ("自然拼读", "字母组合 th/wh/ph 与鼻音 ng/nk 发音规律。")]) +
            '<div class="kmap">' +
            '<div class="kmap-node"><div class="kn-title">词汇</div><div class="kn-body">房间物品 + 失物招领词 lost/found/thing/card。\n</div></div>' +
            '<div class="kmap-node"><div class="kn-title">语法</div><div class="kn-body">名词所有格、基数词编号、Where 特殊疑问句。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">阅读</div><div class="kn-body">A 失物招领通知 + B 图书馆规则 + C 五选四。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">拼读</div><div class="kn-body">th/wh/ph 组合 + ng/nk 鼻音。</div></div>' +
            '</div>' +
            '<div class="note-panel"><div class="np-title">先测后学提示</div>先翻下面的卡片自检已学知识，再进入系统讲解。</div>' +
            '<div class="note-panel"><div class="np-title">闯关目标</div>能正确使用 Tom\'s/students\' 所有格，会写 Class 3/Room 305 编号，并能用 Where 问地点，即可通关。</div>')
    add(goal, 1)
    rev = (section_head("测", "复习检测 · 翻牌自检") +
           '<div class="body-text">点击卡片翻面，看看这些基础知识点你都掌握了吗？</div>' +
           recall_grid(RECALL_L3) +
           '<div class="note-panel"><div class="np-title">检测说明</div>翻牌后对照答案，错一处即回到对应语法页重学，务必全对再进入新词。</div>')
    add(rev, 1)
    warm = (section_head("测", "易混知识预热") +
            key_points([("'s or of?", "有生命用 's，无生命用 of（the cover of the dictionary）。"),
                        ("class 3 or Class 3?", "编号名词首字母大写：Class 3。"),
                        ("Where or What?", "问地点用 Where，问物用 What。"),
                        ("it's or its?", "it's = it is；its = 它的。")]) +
            '<div class="note-panel"><div class="np-title">学习路径</div>先判断“有生命/无生命”选所有格形式；再判断“数量/编号”用基数词；最后用 Where 专问地点。</div>' +
            '<div class="sub-label">语境示例</div>' +
            example_section([("Tom's desk is tidy.", "单数+'s"),
                             ("The students' books are new.", "复数 s 结尾加'"),
                             ("Where is my ruler?", "Where 问地点"),
                             ("We are in Class 3.", "编号大写")]))
    add(warm, 1)

    # 段2 新词20
    add(section_head("词", "新词 ①（1–10）· 房间与物品核心词") + sub_label("点击卡片记忆 · 含音标/搭配/例句") + vocab_cards(VOCAB_L3[:10]), 2)
    add(section_head("词", "新词 ②（11–20）· 失物招领与场所词") + sub_label("含音标/搭配/例句") + vocab_cards(VOCAB_L3[10:]), 2)
    add(section_head("词", "新词速记 · 分组策略") +
        '<div class="note-panel"><div class="np-title">记忆策略</div>'
        '① 按“房间家具/文具/场所”三组记物品词；② 失物招领词 lost/found/thing/card 成串记；③ 每词造一句。</div>' +
        key_points([("房间家具组", "room/bed/desk/table/computer。"),
                    ("文具组", "book/schoolbag/pencil/pen/ruler/eraser/dictionary。"),
                    ("场所组", "library/classroom/office。"),
                    ("失物组", "lost/found/thing/card/picture。")]) +
        '<div class="sub-label">高频搭配</div>' +
        key_points([("in the room", "在房间里"),
                    ("on the desk", "在书桌上"),
                    ("lost and found", "失物招领"),
                    ("school ID card", "学生证"),
                    ("in the library", "在图书馆")]) +
        '<div class="note-panel"><div class="np-title">词族扩展</div>'
        '① class+room→classroom；② school+bag→schoolbag；③ -er 表物：ruler（尺）、eraser（橡皮）、computer（电脑）。</div>', 2)
    cloze_inner = section_head("词", "词汇运用 · 选词填空")
    for q, opts in CLOZE_L3:
        cloze_inner += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for w, cor in opts:
            cloze_inner += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s</button>' % (cor, w)
        cloze_inner += '</div>'
    cloze_inner += '<div class="body-text">用本课新词补全句子，巩固词义与搭配。</div>'
    cloze_inner += '<div class="note-panel"><div class="np-title">解析</div>① Tom\'s 所有格；② pens 复数；③ his 他的；④ Whose 问所属；⑤ his 名物代；⑥ sister\'s 所有格；⑦ on 在……上；⑧ two 基数词。</div>'
    add(cloze_inner, 2)
    vdiff = (section_head("词", "新词 ③ · 近义词/形近词辨析") + sub_label("形近词成对记，避免拼写混淆") +
             key_points([(kw, desc) for kw, desc in VDIFF_L3]) +
             '<div class="note-panel"><div class="np-title">辨析口诀</div>desk 读书 table 吃饭，pen 灌墨 pencil 削木；lost 丢 found 找，its 无撇 it\'s 是缩写。</div>' +
             '<div class="body-text">辨析不是死记，而是“见词想搭档”：desk↔table，pen↔pencil，lost↔found。</div>')
    add(vdiff, 2)
    vdict = (section_head("词", "新词 ④ · 听写自测（点击翻牌）") + sub_label("看中文，翻牌核对英文拼写") +
             recall_grid([(cn, en) for cn, en in VDICT_L3]) +
             '<div class="body-text">家长可对照此页听写；错词请回到新词页重记。</div>' +
             '<div class="note-panel"><div class="np-title">记忆提示</div>先记“房间/文具/场所”三组物品词，再记“失物招领”串词，分组记忆效率更高。</div>')
    add(vdict, 2)

    # 段3 语法精讲
    for gi, g in enumerate(GRAMMAR_L3, 1):
        t = g["title"]
        pa = (section_head("法", "考点%d · 构成与用法 + 例句" % gi) +
              '<div class="sub-label">一 · 构成与用法</div>' +
              '<div class="body-text">%s</div>' % g["usage"] +
              '<div class="sub-label">二 · 典型例句</div>' +
              example_section(g["examples"]) +
              '<div class="sub-label">三 · 中考怎么考</div>' +
              '<div class="note-panel"><div class="np-title">考法预警</div>%s</div>' % GRAMMAR_NOTE_L3.get(gi, ""))
        add(pa, 3, t, "语法精讲")
        pb = (section_head("法", "考点%d · 易错 + 口诀 + 色卡" % gi) +
              '<div class="sub-label">三 · 高频易错</div>' +
              error_callout(g["errors"]) +
              '<div class="sub-label">四 · 记忆口诀</div>' +
              '<div class="note-panel"><div class="np-title">口诀</div>%s</div>' % g["mnemonic"] +
              '<div class="sub-label">五 · 语法要点色卡</div>' +
              grammar_cards(g["cards"]))
        add(pb, 3, t, "语法精讲")
        pc = section_head("法", "考点%d · 中考考法·即时小测" % gi)
        for q, opts in GEXTRA_L3.get(gi, []):
            pc += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
            for letter, text, cor in opts:
                pc += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
            pc += '</div>'
        pc += '<div class="body-text">中考常在语篇中混考所有格、编号与 Where，看清“有生命/无生命/单复数”再下笔。</div>'
        add(pc, 3, t, "语法精讲")
    poss_mat = (section_head("法", "名词所有格速查表") + sub_label("有生命+'s / 复数+' / 无生命 of") +
        '<table class="pm-table">' +
        '<tr><th class="pm-num">名词类型</th><th>构成</th><th class="pm-zhug">示例</th><th>含义</th></tr>' +
        '<tr><th class="pm-num">单数</th><td>+ \'s</td><td class="pm-zhug">Tom\'s desk</td><td>汤姆的书桌</td></tr>' +
        '<tr><th class="pm-num">复数(s结尾)</th><td>+ \'</td><td class="pm-zhug">students\' books</td><td>学生们的书</td></tr>' +
        '<tr><th class="pm-num">无生命</th><td>of 属格</td><td class="pm-zhug">the cover of the dictionary</td><td>词典的封皮</td></tr>' +
        '</table>' +
        '<div class="note-panel"><div class="np-title">记忆顺序</div>单数 Tom→Tom\'s；复数 students→students\'；无生命用 of；it\'s 是缩写，its 才是“它的”。</div>')
    add(poss_mat, 3)
    gsum = (section_head("法", "三大考点综合梳理") +
            key_points([("名词所有格", "有生命+'s，复数 s 结尾+'，无生命用 of。"),
                        ("基数词与编号", "数量用 one–ten；编号 Class 3 / Room 305 大写。"),
                        ("Where 问地点", "Where + be + 主语？答语带 in/on/under。"),
                        ("中考考法", "语法填空常考 it's/its、Class 3 大写、疑问语序。"),
                        ("顺序记忆", "先判有生命/无生命，再判数量/编号，最后用 Where 问地点。")]) +
            '<div class="note-panel"><div class="np-title">易混速记</div>\'s↔of，class 3↔Class 3，Where↔What；it\'s 是缩写，its 才是“它的”。</div>' +
            '<div class="sub-label">实战例句</div>' +
            example_section([("The boy's pen is red.", "单数+'s"),
                             ("We are in Room 305.", "编号大写"),
                             ("Where are the books?", "Where 问地点 + 复数")]))
    add(gsum, 3)
    zhenti = (section_head("法", "中考真题体验 · 所有格与 Where") +
              reading_block("微阅读 · 语法填空",
                  ["Look at ____ (Tom) desk. The ____ (book) on it are his.",
                   "____ (Where) is my schoolbag? It ____ (be) on the desk."],
                  [("1","空格处用 Tom 的所有格还是 Tom？",[("A","Tom's","1"),("B","Tom","0"),("C","Toms","0")]),
                   ("2","“我的书包”提问用哪个词？",[("A","What","0"),("B","Where","1"),("C","Who","0")])]) +
              '<div class="body-text">中考常把名词所有格与 Where 混在同一语篇中考查，务必看清所属与地点。</div>' +
              '<div class="note-panel"><div class="np-title">真题解析</div>题1 单数名词所有格用 Tom\'s；题2 问地点用 Where。</div>')
    add(zhenti, 3)
    pfill = section_head("法", "语法综合应用 · 所有格/编号/Where 填空") + sub_label("用正确形式填空")
    for q, opts in PRONFILL_L3:
        pfill += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            pfill += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        pfill += '</div>'
    pfill += '<div class="body-text">综合考查名词所有格、基数词编号与 Where 问句，是中考“语法填空”微型演练。</div>'
    pfill += '<div class="note-panel"><div class="np-title">填空思路</div>① 看所属用 Tom\'s/students\'；② 编号 Class 3 大写；③ Where 问地点答语带介词。</div>'
    add(pfill, 3)

    # 段4 随堂演练
    quiz_all = QUIZ_L3 + QUIZ_EXTRA_L3 + QUIZ_EXTRA2_L3 + QUIZ_EXTRA3_L3
    q1 = section_head("练", "随堂演练 ① · 语法选择（1–14）")
    for q, opts in quiz_all[:14]:
        q1 += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            q1 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        q1 += '</div>'
    q1 += '<div class="note-panel"><div class="np-title">解题锦囊</div>① 题1、6、13、16、22 考名词所有格；② 题4、8、11、14、20、23、28 考基数词/编号；③ 题2、5、9、17、21、24、26 考 Where 问句；④ 题3、18、25 考 of 属格/介词。</div>'
    add(q1, 4)
    q2 = section_head("练", "随堂演练 ② · 语法选择（15–28）")
    for q, opts in quiz_all[14:]:
        q2 += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            q2 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        q2 += '</div>'
    q2 += '<div class="note-panel"><div class="np-title">解题锦囊</div>看清“空格后有无名词/单复数”是所有格选题关键；编号名词首字母必须大写；Where 问地点答语必带 in/on/under。</div>'
    add(q2, 4)
    drill = section_head("练", "句型操练 · 中译英（点击翻牌看答案）") + sub_label("用本课语法翻译下列句子")
    drill += recall_grid([(cn, en) for cn, en in DRILL_L3])
    drill += '<div class="body-text">先自己说/写英文，再翻牌核对；重点用对所有格、编号与 Where 问句。</div>'
    drill += '<div class="note-panel"><div class="np-title">翻译要点</div>中文“汤姆的”译 Tom\'s；“三班”译 Class 3；“在哪里”译 Where is/are；“在……上”译 on。</div>'
    add(drill, 4)
    fill = (section_head("练", "语法填空演练") +
            '<div class="quiz-q"><div class="qq-text">1. This ___ (be) Tom\'s desk. The ___ (book) are on it.</div>'
            '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">is; books</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">are; book</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">is; book</button></div>'
            '<div class="quiz-q"><div class="qq-text">2. ___ (Where) is my schoolbag? It ___ (be) on the desk.</div>'
            '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">Where; is</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">What; is</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">Where; are</button></div>'
            '<div class="quiz-q"><div class="qq-text">3. We are in ___ (Class) 3. There are ___ (ten) students.</div>'
            '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">Class; ten</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">class; ten</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">Class; tenth</button></div>'
            '<div class="body-text">语法填空是湖南中考省卷“语法诊断/语法填空”题型的微型演练。</div>' +
            '<div class="note-panel"><div class="np-title">解析</div>题1 单数 this→is，book 复数→books；题2 Where 问地点，主语 schoolbag→is；题3 编号 Class 3 大写，数量 ten。</div>')
    add(fill, 4)
    errd = section_head("练", "随堂演练 ③ · 改错专练") + sub_label("找出错误项并改正")
    for q, opts in ERRDRILL_L3:
        errd += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            errd += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        errd += '</div>'
    errd += '<div class="body-text">改错题是中考“语法诊断”的变形，先找错再用正确形式替换。</div>'
    errd += '<div class="note-panel"><div class="np-title">改错思路</div>先判断错在哪一类：所有格漏撇、编号未大写、Where 语序错、还是答语缺 be，再替换。</div>'
    add(errd, 4)

    # 段5 阅读理解
    paras_a = [
        "A Lost and Found in the School Library.",
        "We found these things in the school library this week.",
        "Come and see if any are yours.",
        "A blue pencil box with two pens and a ruler. Found Monday.",
        "A white eraser with a cat picture. Found Tuesday.",
        "An English dictionary with a red cover. Found Wednesday.",
        "Call us at 8866-5533 or come to the library office.",
        "You must describe your thing before taking it.",
    ]
    paras_b = [
        "Our school library is a quiet place for reading. Follow these rules.",
        "First, you must be quiet. Do not talk or run. Other students need a quiet place to read.",
        "Second, take care of the books. Do not write in them or tear pages. If you damage a book, you must pay.",
        "Third, keep your things with you. Put your schoolbag in the box. Do not leave your pencil box on the desk.",
        "You need a library card to borrow books. Ask the teacher for help.",
    ]
    qa = [("1", "When was the pencil box found?", [("A","On Monday","1"),("B","On Tuesday","0"),("C","On Wednesday","0")]),
          ("2", "What is on the eraser?", [("A","A dog picture","0"),("B","A cat picture","1"),("C","A bird picture","0")]),
          ("3", "What color is the dictionary?", [("A","White","0"),("B","Blue","0"),("C","Red","1")]),
          ("4", "How many things are mentioned in the notice?", [("A","Two","0"),("B","Three","1"),("C","Four","0")]),
          ("5", "What must you do before taking your thing?", [("A","Describe it","1"),("B","Pay for it","0"),("C","Sign your name","0")]),
          ("6", "What must you be in the library?", [("A","Quiet","1"),("B","Loud","0"),("C","Fast","0")]),
          ("7", "What should you NOT do with books?", [("A","Read them","0"),("B","Write in them","1"),("C","Borrow them","0")]),
          ("8", "Where should you put your schoolbag?", [("A","In the box","1"),("B","On the desk","0"),("C","At home","0")]),
          ("9", "What does the word \"damage\" mean in Chinese?", [("A","爱护","0"),("B","损坏","1"),("C","借用","0")]),
          ("10", "What do you need to borrow books?", [("A","A library card","1"),("B","A pen","0"),("C","Money","0")])]
    add(section_head("读", "阅读 A · Lost and Found（篇章）") +
        '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in paras_a) + '</div>' +
        '<div class="body-text">读前先猜：这是一篇“失物招领”通知，注意物品、颜色与招领时间。</div>' +
        '<div class="note-panel"><div class="np-title">中文大意</div>学校图书馆失物招领：本周我们在图书馆捡到这些物品，来看看有没有你的。一个蓝色文具盒（两支钢笔和一把尺子），周一捡到；一块白色橡皮（有猫的图案），周二捡到；一本红色封皮的英语词典，周三捡到。请拨打 8866-5533 或来图书馆办公室。领取前你必须描述你的物品。</div>' +
        '<div class="note-panel"><div class="np-title">长难句拆解</div>'
        '① “Come and see if any are yours.” —— if 引导宾语从句，yours 名物代＝your things。<br>'
        '② “You must describe your thing before taking it.” —— before 介词后接动名词 taking。</div>', 5)
    a_q = reading_block("阅读 A · 理解题", paras_a, [qa[0],qa[1],qa[2],qa[3],qa[4]])
    a_q += '<div class="note-panel"><div class="np-title">答案解析</div>题1 由“Found Monday”得文具盒周一捡到；题2 由“cat picture”得猫图案；题3 由“red cover”得红色封皮；题4 文具盒/橡皮/词典共三件；题5 由“describe your thing”得先描述。</div>'
    add(a_q, 5)
    add(section_head("读", "阅读 B · Library Rules（篇章）") +
        '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in paras_b) + '</div>' +
        '<div class="body-text">圈出每条规则的关键动作（quiet / take care / put…in the box），回题定位更快。</div>' +
        '<div class="note-panel"><div class="np-title">中文大意</div>我们学校图书馆是安静阅读的地方，请遵守规则。第一，必须安静，不要说话或奔跑；第二，爱护图书，不要在上面写字或撕页，损坏要赔偿；第三，保管好物品，把书包放进箱子里，别把文具盒留在桌上。借书需要借书卡，可请老师帮忙。</div>' +
        '<div class="note-panel"><div class="np-title">长难句拆解</div>'
        '① “Other students need a quiet place to read.” —— to read 不定式作后置定语；<br>'
        '② “If you damage a book, you must pay.” —— if 条件句，damage 意为“损坏”。</div>', 5)
    b_q = reading_block("阅读 B · 理解题", paras_b, [qa[5],qa[6],qa[7],qa[8],qa[9]])
    b_q += '<div class="note-panel"><div class="np-title">答案解析</div>题6 由“must be quiet”得安静；题7 由“Do not write in them”得不应写字；题8 由“Put your schoolbag in the box”得放进箱子；题9 damage＝损坏；题10 由“library card”得借书卡。</div>'
    add(b_q, 5)
    w5paras = ["Hello, everyone! I am Lisa from Class 3, Grade 7.",
               "I lost my schoolbag in the school library yesterday afternoon. __(16)__",
               "My schoolbag is blue and black. __(17)__",
               "There is a pencil box, an English dictionary, and three notebooks inside. __(18)__",
               "This schoolbag is important to me because I need my books for school. __(19)__",
               "I must find it today. You can also bring it to Class 3, Grade 7. Thank you for your help!"]
    w5opts = [("A","I am very worried about it."),
              ("B","A red pencil box is in it."),
              ("C","The dictionary is my favorite."),
              ("D","Please help me find it."),
              ("E","I like reading books in the library.")]
    w5ans = {16:"A",17:"B",18:"C",19:"D"}
    add(section_head("读", "阅读 C · 五选四（Lisa's Lost Notice·篇章）") +
        '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in w5paras) + '</div>' +
        '<div class="body-text">从 A–E 中选出最佳句子填入 __（16–19）__ 空白，注意前后逻辑衔接（E 为多余项，五选四）。</div>' +
        '<div class="note-panel"><div class="np-title">中文大意</div>大家好！我是七年级三班的丽莎。昨天下午我在学校图书馆丢了书包。我很担心。我的书包蓝黑相间。里面有个红色文具盒。文具盒里有一支钢笔、一本英语词典和三本笔记本。词典是我最爱的。这个书包对我很重要，因为我上学需要这些书。请帮我找找它。我今天必须找到。也可送到七年级三班，谢谢！</div>', 5)
    w5q = section_head("读", "阅读 C · 五选四（题目）")
    for num in sorted(w5ans.keys()):
        ans = w5ans[num]
        w5q += '<div class="quiz-q"><div class="qq-text">__（%d）__ 应填：</div>' % num
        for letter, text in w5opts:
            cor = '1' if letter == ans else '0'
            w5q += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        w5q += '</div>'
    w5q += '<div class="note-panel"><div class="np-title">答案解析</div>16→A（丢后担忧，衔接 lost）；17→B（蓝黑相间，进一步说里面有红文具盒）；18→C（列举内容后说词典最爱）；19→D（重要→请帮忙找）；E 为多余项（与丢书包无关）。</div>'
    add(w5q, 5)
    reading_tip = (section_head("读", "阅读解题 SOP") +
                   key_points([("先题后文", "先读题干圈关键词，再回原文定位。"),
                               ("细节题", "题干词多在原文原词复现，直接比对。"),
                               ("五选四", "看空白前后句逻辑，排除重复/矛盾项。"),
                               ("防陷阱", "注意名词所有格、编号大写与 Where 地点介词。"),
                               ("猜词法", "利用上下文线索猜测生词含义（如 damage）。"),
                               ("主旨题", "找首尾句与高频词，避免以偏概全。")]) +
                   '<div class="note-panel"><div class="np-title">本课的阅读</div>'
                   'A 篇为失物招领通知（细节题），B 篇为图书馆规则（规则类），C 篇为五选四逻辑衔接题，文体互异。</div>')
    add(reading_tip, 5)
    rmore = (section_head("读", "阅读实战 · 细节定位再练") +
             '<div class="body-text">下列题目需回看前面“阅读 A：失物招领”与“阅读 B：图书馆规则”篇章定位（答案请回原文核对）。</div>')
    rmore_quiz = [
        ("1", "What can you call to ask about lost things?", [("A","8866-5533","1"),("B","139-8877","0"),("C","5566-7788","0")]),
        ("2", "Where was the dictionary found?", [("A","On Monday","0"),("B","On Tuesday","0"),("C","On Wednesday","1")]),
        ("3", "What must you do before taking a lost thing?", [("A","Describe it","1"),("B","Pay money","0"),("C","Leave a card","0")]),
        ("4", "Can you talk loudly in the library?", [("A","Yes, you can","0"),("B","No, you must be quiet","1"),("C","Only in the morning","0")]),
        ("5", "Where should the pencil box NOT be?", [("A","In the box","0"),("B","On the desk","1"),("C","With you","0")]),
        ("6", "What do you need to borrow books?", [("A","A library card","1"),("B","A ruler","0"),("C","A dictionary","0")]),
        ("7", "Is the library a quiet place?", [("A","Yes, it is","1"),("B","No, it isn't","0"),("C","It is noisy","0")]),
    ]
    for qnum, q, opts in rmore_quiz:
        rmore += '<div class="quiz-q"><div class="qq-text">%s. %s</div>' % (qnum, q)
        for letter, text, cor in opts:
            rmore += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        rmore += '</div>'
    rmore += '<div class="note-panel"><div class="np-title">定位提示</div>题1 回阅读 A 找电话；题2 由“Found Wednesday”得词典周三；题3 由“describe your thing”得先描述；题4 由“must be quiet”得不可喧哗；题5 由“leave…on the desk”得不应留桌上；题6 借书卡；题7 图书馆安静。</div>'
    add(rmore, 5)

    # 段6 自然拼读
    add(phonics_block(PHONICS_L3), 6)
    ph2 = (section_head("拼", "字母组合拼读演练") +
           key_points([("th /θ//ð/", "thing, think, that, this——舌尖夹齿。"),
                       ("wh /w//h/", "where, what, who, when——问词开头。"),
                       ("ph /f/", "photo, phone, phrase——ph 发 /f/。"),
                       ("ng /ŋ/", "ring, sing, thing——鼻音成音。"),
                       ("nk /ŋk/", "think, pink, bank——鼻音加 k。")]) +
           '<div class="sub-label">常见词族</div>' +
           key_points([("-ing", "thing, ring, sing"),
                       ("-ink", "think, pink, link"),
                       ("-th", "this, that, with"),
                       ("-wh", "where, what, when"),
                       ("-ph", "photo, phone, phrase")]) +
           '<div class="note-panel"><div class="np-title">拼读口诀</div>'
           'th 咬舌、wh 问词、ph 发 f、ng 鼻音、nk 鼻音加 k；组合发音要“稳准快”。</div>')
    add(ph2, 6)
    ph3 = (section_head("拼", "字母组合拼读小结 · 儿歌") +
           '<div class="note-panel"><div class="np-title">拼读儿歌</div>'
           'th th /θ/ thing think 咬舌尖，wh wh /w/ where what 问起来；<br>ph ph /f/ photo phone 记分明，ng ng /ŋ/ ring sing 鼻音响；<br>nk nk /ŋk/ think pink 加 k 尾，字母组合要记牢！</div>' +
           key_points([("口型", "th 舌尖轻触上齿，气流从缝逸出。"),
                       ("位置", "wh 多为疑问词 who/what/when/where。"),
                       ("ph 特例", "ph 在英语中固定发 /f/，如 photo/phone。"),
                       ("ng 鼻音", "舌根抵软腭，气流从鼻出，如 ring/sing。"),
                       ("nk 组合", "ng 之后加 k，如 think/pink。"),
                       ("对比", "th 清浊：thank(清/θ/) vs this(浊/ð/)。"),
                       ("wh 发音", "who 在 o 前读 /h/，what/when 读 /w/。"),
                       ("练习", "this/that、where/what 反复读，体会咬舌与问词感。")]))
    add(ph3, 6)

    # 段7 课堂练习
    cv1 = section_head("戏", "课堂游戏 · 跨课词汇快选 ①") + sub_label("看中文，选出正确英文")
    cv1 += '<div class="note-panel"><div class="np-title">玩法</div>点击与中文对应的英文词，答对响铃。</div>'
    for cn, en, opts in CROSS_L3[:4]:
        cv1 += '<div class="quiz-q"><div class="qq-text">“%s” 是哪个词？</div>' % cn
        for w, cor in opts:
            cv1 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s</button>' % (cor, w)
        cv1 += '</div>'
    cv1 += '<div class="note-panel"><div class="np-title">提示</div>遇到形近词（desk/table、pen/pencil）先辨用途再选；失物招领词成串记。</div>'
    add(cv1, 7)
    cv2 = section_head("戏", "课堂游戏 · 跨课词汇快选 ②") + sub_label("看中文，选出正确英文")
    for cn, en, opts in CROSS_L3[4:]:
        cv2 += '<div class="quiz-q"><div class="qq-text">“%s” 是哪个词？</div>' % cn
        for w, cor in opts:
            cv2 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s</button>' % (cor, w)
        cv2 += '</div>'
    cv2 += '<div class="note-panel"><div class="np-title">游戏小结</div>跨课词汇快选训练“音—形—义”对应，是听力与完形的基础；错词请回到新词页再记。</div>'
    add(cv2, 7)
    listen = (section_head("戏", "听音选词 · 词义匹配") + sub_label("下列英文，哪个意思是“图书馆”？") +
              '<div class="quiz-q"><div class="qq-text">“图书馆” 对应：</div>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">library</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">office</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">classroom</button></div>'
              '<div class="quiz-q"><div class="qq-text">“橡皮” 对应：</div>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">ruler</button>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">eraser</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">dictionary</button></div>'
              '<div class="quiz-q"><div class="qq-text">“在哪里” 对应：</div>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">where</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">what</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">who</button></div>'
              '<div class="quiz-q"><div class="qq-text">“失物招领” 对应：</div>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">lost and found</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">library rules</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">computer room</button></div>'
              '<div class="body-text">巩固本课核心词义，为听力与完形打底。</div>')
    add(listen, 7)

    # 段8 课堂总结
    summary = (section_head("结", "课堂总结 · 知识图谱") +
               '<div class="kmap">' +
               '<div class="kmap-node"><div class="kn-title">名词所有格</div><div class="kn-body">有生命+\'s，复数 s 结尾+\'，无生命用 of；it\'s≠its。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">基数词编号</div><div class="kn-body">数量 one–ten；编号 Class 3 / Room 305 大写。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">Where 问句</div><div class="kn-body">Where + be + 主语？答语带 in/on/under。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">自然拼读</div><div class="kn-body">th/wh/ph 组合 + ng/nk 鼻音。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">学习建议</div><div class="kn-body">每天听写 5 词＋造 2 句，周末回头复习，所有格与 Where 务必熟练。</div></div>' +
               '</div>' +
               '<div class="note-panel"><div class="np-title">课后作业</div>'
               '① 背诵本课 20 个新词（家长听写）；② 完成配套基础练习；③ 用名词所有格 + Where 问句写 5 句物品位置；④ 整理错题本（本课易错 10 句）。</div>' +
               '<div class="note-panel"><div class="np-title">巩固建议</div>错题本按“所有格”“编号大写”“Where 语序”三类归档，每周回看一次，避免重复犯错。</div>')
    add(summary, 8)
    err_review = (section_head("结", "易错清单回顾") +
                  error_callout([("its a book.","It's a book."),
                                 ("The boy book is red.","The boy's book is red."),
                                 ("class 3 is my class.","Class 3 is my class."),
                                 ("Where my pen is?","Where is my pen?"),
                                 ("They on the desk.","They are on the desk."),
                                 ("The students book are new.","The students' books are new."),
                                 ("cover of dictionary is red.","The cover of the dictionary is red."),
                                 ("It on the bed.","It is on the bed."),
                                 ("Where are my book?","Where is my book?"),
                                 ("three book on the desk.","three books on the desk.")]) +
                  '<div class="note-panel"><div class="np-title">避坑口诀</div>所有格看有生命/无生命，编号 Class 3 大写，Where 把 be 提前；it\'s 是缩写，its 才是“它的”。</div>')
    add(err_review, 8)
    preview = (section_head("结", "下节课预告 · 第 4 课") +
               key_points([("语法①", "名词复数（规则与不规则变化）。"),
                           ("语法②", "tidy 与房间介词（in/on/under）综合运用。"),
                           ("语法③", "there be 句型（某处有某物）。"),
                           ("新词", "chair/sofa/clock 等更多房间物品词汇。")]) +
               '<div class="note-panel"><div class="np-title">课前准备</div>复习本课所有格与 Where 问句，下节课用它们描述“房间里有什么、在哪”。</div>' +
               '<div class="note-panel"><div class="np-title">课前任务</div>① 默写本课 20 词（家长签字）；② 用 Where 造 2 句；③ 预习名词复数变化规则。</div>')
    add(preview, 8)

    total = p - 1
    seg_pages = {}
    for sid, (a, b) in seg.items():
        seg_pages[sid] = [a, b]
    return pages, seg_pages, total

NAV = """<div class="nav-bar">
  <div class="nav-item" data-segment="1" onclick="jumpToSegment(1)"><span class="nav-num">①</span>复习导入</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="2" onclick="jumpToSegment(2)"><span class="nav-num">②</span>新词20</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="3" onclick="jumpToSegment(3)"><span class="nav-num">③</span>语法精讲</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="4" onclick="jumpToSegment(4)"><span class="nav-num">④</span>随堂演练</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="5" onclick="jumpToSegment(5)"><span class="nav-num">⑤</span>阅读理解</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="6" onclick="jumpToSegment(6)"><span class="nav-num">⑥</span>自然拼读</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="7" onclick="jumpToSegment(7)"><span class="nav-num">⑦</span>课堂练习</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="8" onclick="jumpToSegment(8)"><span class="nav-num">⑧</span>课堂总结</div>
</div>"""

JS_EXTRA_TPL = """
var totalPages = %d;
var segmentPages = %s;
function flipCard(el){ el.classList.toggle('flipped'); }
function checkOpt(btn){
  var q = btn.parentNode;
  if(q.dataset.done) return;
  q.dataset.done = '1';
  var opts = q.querySelectorAll('.quiz-opt');
  for(var i=0;i<opts.length;i++){ opts[i].disabled = true; }
  var ok = btn.dataset.correct === '1';
  if(ok){ btn.classList.add('opt-correct'); playCorrect(); }
  else {
    btn.classList.add('opt-wrong'); playError();
    for(var i=0;i<opts.length;i++){ if(opts[i].dataset.correct==='1'){ opts[i].classList.add('opt-correct'); } }
  }
}
"""

# ===================== L4 内容 =====================
VOCAB_L4 = [
    ("chair","/tʃeə/","n.","椅子","on the chair","The chair is near the window.","椅子→chair，ch 发音/tʃ/"),
    ("sofa","/ˈsəʊfə/","n.","沙发","on the sofa","The cat is on the sofa.","沙发→sofa，o 发/əʊ/"),
    ("wardrobe","/ˈwɔːdrəʊb/","n.","衣柜","in the wardrobe","Her clothes are in the wardrobe.","衣柜→ward+robe"),
    ("lamp","/læmp/","n.","台灯","a pink lamp","A lamp is on the desk.","台灯→lamp，l 开头"),
    ("shelf","/ʃelf/","n.","架子","on the shelf","The book is on the shelf.","架子→shelf，复 shelves"),
    ("drawer","/drɔː/","n.","抽屉","in the drawer","The keys are in the drawer.","抽屉→draw+er"),
    ("tidy","/ˈtaɪdi/","adj.","整洁的","a tidy room","Her room is tidy.","整洁→tidy，y 结尾"),
    ("messy","/ˈmesi/","adj.","凌乱的","a messy room","His room is messy.","凌乱→mess+y"),
    ("clean","/kliːn/","adj.","干净的","clean and tidy","The desk is clean.","干净→clean，ea 发/iː/"),
    ("dirty","/ˈdɜːti/","adj.","脏的","dirty clothes","The floor is dirty.","脏→dirty，y 结尾"),
    ("behind","/bɪˈhaɪnd/","prep.","在…后面","behind the door","The cat is behind the door.","后→behind，hind 后"),
    ("between","/bɪˈtwiːn/","prep.","在…之间","between A and B","A sofa is between them.","之间→between"),
    ("above","/əˈbʌv/","prep.","在…上方","above the chair","The picture is above the chair.","上→above，a 开头"),
    ("next","/nekst/","adj./adv.","下一个；紧邻","next to the window","The lamp is next to the window.","紧邻→next to"),
    ("always","/ˈɔːlweɪz/","adv.","总是","always tidy","He always tidies his room.","总是→always，al 开头"),
    ("never","/ˈnevə/","adv.","从不","never messy","She never makes it messy.","从不→never，e 结尾"),
    ("sometimes","/ˈsʌmtaɪmz/","adv.","有时","sometimes dirty","It is sometimes dirty.","有时→some+times"),
    ("soccer","/ˈsɒkə/","n.","足球","a soccer ball","He has a soccer ball.","足球→soccer，cc 双写"),
    ("ball","/bɔːl/","n.","球","under the ball","The ball is under the chair.","球→ball，all 双写"),
    ("habit","/ˈhæbɪt/","n.","习惯","a good habit","Keeping tidy is a good habit.","习惯→habit，bit 结尾"),
]

GRAMMAR_L4 = [
    {
        "title": "语法① · 名词复数（规则与不规则变化）",
        "usage": "英语中表“两个或以上”用<b>复数</b>。规则：一般加 <b>-s</b>（chairs, sofas）；以 s/x/ch/sh/o 结尾加 <b>-es</b>（boxes, watches, dishes）；<b>辅音字母+y</b> 结尾变 y 为 i 再加 -es（baby→babies）；<b>f/fe</b> 结尾变 ves（shelf→shelves）；<b>不规则</b>需单独记（child→children, man→men, foot→feet）。",
        "examples": [
            ("a chair → two chairs", "一般加 -s"),
            ("a box → three boxes", "x 结尾加 -es"),
            ("a shelf → two shelves", "f 变 ves"),
            ("a baby → two babies", "辅音+y 变 ies"),
            ("a child → many children", "不规则变化"),
            ("a man → two men", "不规则变化"),
        ],
        "errors": [
            ("There is two book.", "There are two books."),
            ("These box are new.", "These boxes are new."),
            ("He has three foots.", "He has three feet."),
            ("A childs is here.", "A child is here."),
            ("The shelf is white.", "The shelves are white."),
        ],
        "mnemonic": "一般加 s，s/x/ch/sh/o 加 es；辅音 y 改 ies；f/fe 改 ves；不规则 child/men/feet 单独记。",
        "cards": [("用法","一般加 -s：chair→chairs, sofa→sofas, lamp→lamps"),
                  ("构成","s/x/ch/sh/o 加 -es：box→boxes, watch→watches"),
                  ("易错","辅音+y 变 ies：baby→babies, family→families"),
                  ("例句","f/fe 变 ves：shelf→shelves, knife→knives"),
                  ("注意","不规则必须单独记：child→children, man→men, foot→feet"),
                  ("口诀","单变复，看词尾；es/ies/ves 各有规，不规则另背。")],
    },
    {
        "title": "语法② · 房间介词（on/in/under/behind/between/next to/above）",
        "usage": "<b>on</b> 在…上，<b>in</b> 在…里，<b>under</b> 在…下，<b>behind</b> 在…后，<b>between A and B</b> 在两者间，<b>next to</b> 紧邻，<b>above</b> 在…上方。介词后接代词宾格或名词。",
        "examples": [
            ("The book is on the desk.", "on 在…上"),
            ("The ball is under the bed.", "under 在…下"),
            ("The cat is behind the door.", "behind 在…后"),
            ("The lamp is next to the window.", "next to 紧邻"),
            ("The picture is above the chair.", "above 在…上方"),
            ("A sofa is between the desk and the chair.", "between 两者之间"),
        ],
        "errors": [
            ("The book is at the desk.", "The book is on the desk."),
            ("The ball is below the bed.", "The ball is under the bed."),
            ("The cat is after the door.", "The cat is behind the door."),
            ("Next the window is a lamp.", "Next to the window is a lamp."),
            ("Between the desk are a chair.", "Between the desk and the chair is a chair."),
        ],
        "mnemonic": "on 上 in 里 under 下，behind 后 above 上；between 两者间，next to 紧挨着。",
        "cards": [("用法","on 在…上 / in 在…里：表静态位置"),
                  ("构成","under 在…下 / behind 在…后：表方位"),
                  ("易错","between 必须接两者：between A and B"),
                  ("例句","next to 紧邻：lamp is next to the window"),
                  ("注意","above 在正上方；on 强调接触表面"),
                  ("口诀","方位介词要记牢，on/in/under/behind 跑不了。")],
    },
    {
        "title": "语法③ · There be 句型（某处有某物）",
        "usage": "<b>There be</b> 表示“某处有某物”。<b>There is</b> + 单数/不可数；<b>There are</b> + 复数。<b>就近原则</b>：be 随最近的主语变化（There is a book and two pens）。否定：There isn't / aren't；疑问：Is there...? Are there...?",
        "examples": [
            ("There is a desk in my room.", "there is + 单数"),
            ("There are two chairs.", "there are + 复数"),
            ("There is a book and two pens.", "就近原则：be 随最近主语"),
            ("There isn't any milk.", "否定：there isn't + 不可数"),
            ("Are there any balls?", "疑问：Are there + 复数"),
            ("How many books are there?", "How many + 复数提问"),
        ],
        "errors": [
            ("There have a book.", "There is a book."),
            ("There is two chairs.", "There are two chairs."),
            ("There are a book.", "There is a book."),
            ("Is there some pens?", "Are there any pens?"),
            ("There is book and pen.", "There is a book and a pen."),
        ],
        "mnemonic": "某地有某物，there be 来表；单数 is 复数 are，就近原则要记牢。",
        "cards": [("用法","There is + 单数/不可数；There are + 复数"),
                  ("构成","就近原则：be 随最近的主语变化"),
                  ("易错","there be 表存在，不用 have/has"),
                  ("例句","否定 There isn't / aren't；疑问 Is/Are there"),
                  ("注意","some 在疑问/否定中变 any"),
                  ("口诀","there be 存在句，is 单 are 复，就近不糊涂。")],
    },
]

GRAMMAR_NOTE_L4 = {
    1: "名词复数是湖南中考省卷高频考点，常与 there be 混考：先看主语单复选 is/are，再看就近原则。",
    2: "房间介词在完形与阅读中常考‘位置判断’，看清 on/in/under 的接触与包含关系，between 必接两者。",
    3: "There be 是省卷‘语法填空/完形’常客，就近原则是命题热点，注意 some→any 的转换。",
}

RECALL_L4 = [
    ("名词变复数，box 怎么变？", "boxes（加 -es）"),
    ("‘在…下’用哪个介词？", "under"),
    ("There ____ a book.（填 is/are）", "is（单数）"),
    ("shelf 的复数是？", "shelves（f 变 ves）"),
    ("‘紧邻窗户’怎么说？", "next to the window"),
    ("There ____ two chairs.（填 is/are）", "are（复数）"),
    ("child 的复数是？", "children（不规则）"),
    ("‘在…之间（两者）’用？", "between A and B"),
]

CLOZE_L4 = [
    ("Look at this nice photo of my home. This is my new ____.", [("park","0"),("room","1"),("school","0")]),
    ("It is small, ____ it is very clean and tidy.", [("so","0"),("and","0"),("but","1")]),
    ("My bed is ____ to the window.", [("next","1"),("under","0"),("in","0")]),
    ("On the bed, there is a soft blue ____.", [("desk","0"),("pillow","1"),("box","0")]),
    ("My computer is on the ____.", [("sofa","0"),("chair","0"),("desk","1")]),
    ("Under the desk, you can see my ____.", [("shoes","1"),("cats","0"),("keys","0")]),
    ("I have many ____, and they are all in the bookcase.", [("rooms","0"),("books","1"),("beds","0")]),
    ("I have many books, and they are all in the ____.", [("table","0"),("door","0"),("bookcase","1")]),
    ("I ____ clean my room on Sunday morning.", [("always","1"),("never","0"),("behind","0")]),
    ("It is a good ____ for me to keep every day.", [("day","0"),("habit","1"),("place","0")]),
]

VDIFF_L4 = [
    ("tidy / messy", "tidy 整洁的；messy 凌乱的，一对反义词。"),
    ("clean / dirty", "clean 干净的；dirty 脏的，一对反义词。"),
    ("on / in", "on 在物体表面上方；in 在内部里面。"),
    ("under / behind", "under 在正下方；behind 在后方。"),
    ("between / among", "between 两者之间；among 三者及以上。"),
    ("always / never", "always 总是；never 从不，一对反义词。"),
]

VDICT_L4 = [
    ("椅子","chair"),("沙发","sofa"),("衣柜","wardrobe"),("台灯","lamp"),("架子","shelf"),
    ("抽屉","drawer"),("整洁的","tidy"),("凌乱的","messy"),("干净的","clean"),("脏的","dirty"),
    ("在…后面","behind"),("在…之间","between"),("在…上方","above"),("足球","soccer"),("习惯","habit"),
]

PHONICS_L4 = [
    ("br","bread /br/","br 组合发 /br/，如 brown, brother"),
    ("cr","cry /kr/","cr 组合发 /kr/，如 crab, cry"),
    ("dr","draw /dr/","dr 组合发 /dr/，如 dress, draw"),
    ("fr","friend /fr/","fr 组合发 /fr/，如 fruit, free"),
    ("tr","tree /tr/","tr 组合发 /tr/，如 train, try"),
    ("gr","green /gr/","gr 组合发 /gr/，如 grade, grow"),
]

QUIZ_L4 = [
    ("There ____ a book on the desk.", [("A","is","1"),("B","are","0"),("C","have","0")]),
    ("These ____ are new.", [("A","box","0"),("B","boxes","1"),("C","boxs","0")]),
    ("The ball is ____ the bed.", [("A","on","0"),("B","in","0"),("C","under","1")]),
    ("There ____ two cats under the chair.", [("A","are","1"),("B","is","0"),("C","have","0")]),
    ("A shelf → two ____.", [("A","shelf","0"),("B","shelves","1"),("C","shelfs","0")]),
    ("The cat is ____ the door.", [("A","between","0"),("B","above","0"),("C","behind","1")]),
]
QUIZ_EXTRA_L4 = [
    ("There ____ a book and two pens.", [("A","is","1"),("B","are","0"),("C","have","0")]),
    ("The lamp is ____ the window.", [("A","under","0"),("B","next to","1"),("C","in","0")]),
    ("How many ____ are there in the room?", [("A","child","0"),("B","chily","0"),("C","children","1")]),
    ("The books are ____ the bookcase.", [("A","in","1"),("B","on","0"),("C","under","0")]),
    ("There ____ any apples on the table.", [("A","isn't","0"),("B","aren't","1"),("C","are","0")]),
    ("My shoes are ____ the bed.", [("A","on","0"),("B","below","0"),("C","under","1")]),
]
QUIZ_EXTRA2_L4 = [
    ("A knife → two ____.", [("A","knives","1"),("B","knifes","0"),("C","knife","0")]),
    ("____ the desk and the chair is a sofa.", [("A","Among","0"),("B","Between","1"),("C","Next","0")]),
    ("Tom ____ keeps his room tidy.", [("A","never","0"),("B","seldom","0"),("C","always","1")]),
    ("There ____ some water in the cup.", [("A","is","1"),("B","are","0"),("C","have","0")]),
    ("The picture is ____ the chair.", [("A","above","0"),("B","on","1"),("C","under","0")]),
    ("These ____ are messy.", [("A","room","0"),("B","roomes","0"),("C","rooms","1")]),
    ("The soccer ball is ____ the chair.", [("A","under","1"),("B","below","0"),("C","behind","0")]),
    ("The clothes are ____ the wardrobe.", [("A","on","0"),("B","in","1"),("C","under","0")]),
]
QUIZ_EXTRA3_L4 = [
    ("There ____ three books and a pen.", [("A","is","0"),("B","have","0"),("C","are","1")]),
    ("A baby → two ____.", [("A","babies","1"),("B","babys","0"),("C","baby","0")]),
    ("The dog is ____ the sofa.", [("A","on","0"),("B","under","1"),("C","next","0")]),
    ("How many ____ can you see?", [("A","box","0"),("B","boxs","0"),("C","boxes","1")]),
    ("There ____ a cat and two dogs.", [("A","is","1"),("B","are","0"),("C","have","0")]),
    ("The keys are ____ the drawer.", [("A","on","0"),("B","in","1"),("C","under","0")]),
    ("These ____ are red.", [("A","foot","0"),("B","foots","0"),("C","feet","1")]),
    ("____ the bed and the window is a desk.", [("A","Between","1"),("B","Among","0"),("C","Next","0")]),
]

DRILL_L4 = [
    ("我的房间很整洁。","My room is tidy."),
    ("书在书桌上。","The book is on the desk."),
    ("球在床底下。","The ball is under the bed."),
    ("猫在门后面。","The cat is behind the door."),
    ("桌子上有一盏台灯。","There is a lamp on the desk."),
    ("房间里有两个椅子。","There are two chairs in the room."),
    ("架子上有两本书。","There are two books on the shelf."),
    ("他总是收拾房间。","He always tidies his room."),
    ("她从不把房间弄乱。","She never makes her room messy."),
    ("沙发在书桌和椅子之间。","A sofa is between the desk and the chair."),
    ("图片在椅子上方。","The picture is above the chair."),
    ("衣柜里有很多衣服。","There are many clothes in the wardrobe."),
    ("保持整洁是个好习惯。","Keeping tidy is a good habit."),
    ("那些盒子是新的。","Those boxes are new."),
]

GEXTRA_L4 = {
    1: [("There ____ two books and a pen on the desk.", [("A","are","1"),("B","is","0"),("C","have","0")]),
        ("A ____ → two knives.", [("A","knife","0"),("B","knifes","0"),("C","knives","1")])],
    2: [("The soccer ball is ____ the chair.", [("A","on","0"),("B","under","1"),("C","in","0")]),
        ("A sofa is ____ the desk and the chair.", [("A","among","0"),("B","next","0"),("C","between","1")])],
    3: [("____ there any water in the glass?", [("A","Is","1"),("B","Are","0"),("C","Have","0")]),
        ("How many ____ are there on the desk?", [("A","book","0"),("B","books","1"),("C","bookes","0")])],
}

ERRDRILL_L4 = [
    ("There is two chair in the room.", [("A","is→are","0"),("B","chair→chairs","1"),("C","two→too","0")]),
    ("The book is at the desk.", [("A","at→on","1"),("B","book→books","0"),("C","the→a","0")]),
    ("These box are new.", [("A","These→Those","0"),("B","are→is","0"),("C","box→boxes","1")]),
    ("Next the window is a lamp.", [("A","Next→Next to","1"),("B","window→door","0"),("C","lamp→lamps","0")]),
    ("There have a cat under the bed.", [("A","have→has","0"),("B","have→are","0"),("C","have→is","1")]),
]

PRONFILL_L4 = [
    ("There ____ (be) two chairs in my room.", [("A","is","0"),("B","are","1"),("C","have","0")]),
    ("A box → three ____ (box).", [("A","box","0"),("B","boxs","0"),("C","boxes","1")]),
    ("The cat is ____ (behind) the door.", [("A","behind","1"),("B","under","0"),("C","above","0")]),
    ("He ____ (always) tidies his room.", [("A","never","0"),("B","sometimes","0"),("C","always","1")]),
]

def build_lesson_4():
    pages = {}
    seg = {}
    p = 1
    def add(inner, seg_id, title="第4课 · 名词复数/房间介词/There be", subtitle="My Tidy Room · 七上基础"):
        nonlocal p
        pages[p] = page(p, title, subtitle, inner, active=(p == 1))
        seg.setdefault(seg_id, [p, p])
        seg[seg_id][1] = p
        p += 1

    # 段1 复习导入
    cover = ('<div class="cover-wrap"><div class="cover-title">第 4 课</div>'
             '<div class="cover-sub">名词复数 / 房间介词 / There be 句型 · 七上基础</div>'
             '<div class="cover-info">'
             '<div class="cover-info-num"><div class="ci-label">新词</div><div class="ci-val">20</div></div>'
             '<div class="cover-info-num"><div class="ci-label">语法考点</div><div class="ci-val">3</div></div>'
             '<div class="cover-info-num"><div class="ci-label">页数</div><div class="ci-val">45</div></div>'
             '</div></div>')
    add(cover, 1, "第4课 · 名词复数/房间介词/There be", "封面")
    goal = (section_head("标", "本课学习目标") +
            key_points([("20 中考高频词", "chair/sofa/wardrobe 等房间物品 + tidy/messy/clean/dirty + 介词 behind/between/above。"),
                        ("3 大语法考点", "①名词复数变化 ②房间介词 ③There be 句型与就近原则。"),
                        ("阅读主题", "My Tidy Room，训练位置描述与细节定位。"),
                        ("自然拼读", "辅音连缀 br/cr/dr/fr/tr/gr 发音规律。")]) +
            '<div class="kmap">' +
            '<div class="kmap-node"><div class="kn-title">词汇</div><div class="kn-body">房间物品 + 整洁/凌乱形容词 + 方位介词。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">语法</div><div class="kn-body">名词复数、房间介词、There be 与就近原则。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">阅读</div><div class="kn-body">A 莉莉的卧室 + B 萨姆的房间 + C 五选四整理房间。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">拼读</div><div class="kn-body">br/cr/dr/fr/tr/gr 辅音连缀发音。</div></div>' +
            '</div>' +
            '<div class="note-panel"><div class="np-title">先测后学提示</div>先翻下面的卡片自检已学知识，再进入系统讲解。</div>' +
            '<div class="note-panel"><div class="np-title">闯关目标</div>能正确使用名词复数、用介词说出物品位置、并会用 There be 描述房间，即可通关。</div>')
    add(goal, 1)
    rev = (section_head("测", "复习检测 · 翻牌自检") +
           '<div class="body-text">点击卡片翻面，看看这些基础知识点你都掌握了吗？</div>' +
           recall_grid(RECALL_L4) +
           '<div class="note-panel"><div class="np-title">检测说明</div>翻牌后对照答案，错一处即回到对应语法页重学，务必全对再进入新词。</div>')
    add(rev, 1)
    warm = (section_head("测", "易混知识预热") +
            key_points([("单数 or 复数?", "一个用单数，两个及以上加 -s/-es。"),
                        ("on or in?", "表面上方用 on，内部里面用 in。"),
                        ("under or behind?", "正下方用 under，后方用 behind。"),
                        ("is or are?", "There is 接单数，There are 接复数。")]) +
            '<div class="note-panel"><div class="np-title">学习路径</div>先判断名词单复选复数形式；再用介词描述位置；最后用 There be 把“位置+物品”连成句。</div>' +
            '<div class="sub-label">语境示例</div>' +
            example_section([("two chairs", "复数加 -es/-s"),
                             ("on the desk", "表面上方用 on"),
                             ("under the bed", "正下方用 under"),
                             ("There is a lamp.", "There is 接单数")]))
    add(warm, 1)

    # 段2 新词20
    add(section_head("词", "新词 ①（1–10）· 房间物品与形容词") + sub_label("点击卡片记忆 · 含音标/搭配/例句") + vocab_cards(VOCAB_L4[:10]), 2)
    add(section_head("词", "新词 ②（11–20）· 方位介词与频率副词") + sub_label("含音标/搭配/例句") + vocab_cards(VOCAB_L4[10:]), 2)
    add(section_head("词", "新词速记 · 分组策略") +
        '<div class="note-panel"><div class="np-title">记忆策略</div>'
        '① 按“家具/形容词/介词/副词”分组记；② 反义词成对记 tidy↔messy、clean↔dirty、always↔never；③ 每词造一句。</div>' +
        key_points([("家具组", "chair/sofa/wardrobe/lamp/shelf/drawer。"),
                    ("形容词组", "tidy/messy/clean/dirty。"),
                    ("介词组", "behind/between/above/next to。"),
                    ("副词组", "always/never/sometimes。")]) +
        '<div class="sub-label">高频搭配</div>' +
        key_points([("a tidy room", "整洁的房间"),
                    ("clean and tidy", "干净整洁"),
                    ("next to the window", "紧邻窗户"),
                    ("a soccer ball", "足球"),
                    ("a good habit", "好习惯")]) +
        '<div class="note-panel"><div class="np-title">词族扩展</div>'
        '① 反义成对：tidy↔messy、clean↔dirty、always↔never；② 介词家族：on/in/under/behind/above/next to 构成“方位全景”。</div>', 2)
    cloze_inner = section_head("词", "词汇运用 · 选词填空")
    for q, opts in CLOZE_L4:
        cloze_inner += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for w, cor in opts:
            cloze_inner += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s</button>' % (cor, w)
        cloze_inner += '</div>'
    cloze_inner += '<div class="body-text">用本课新词补全短文，巩固词义与搭配。</div>'
    cloze_inner += '<div class="note-panel"><div class="np-title">解析</div>① room 房间；② but 表转折；③ next to 紧邻；④ pillow 枕头；⑤ desk 书桌；⑥ shoes 鞋；⑦ books 书；⑧ bookcase 书柜；⑨ always 总是；⑩ habit 习惯。</div>'
    add(cloze_inner, 2)
    vdiff = (section_head("词", "新词 ③ · 近义词/反义词辨析") + sub_label("反义成对记，避免混淆") +
             key_points([(kw, desc) for kw, desc in VDIFF_L4]) +
             '<div class="note-panel"><div class="np-title">辨析口诀</div>整洁看 tidy，凌乱看 messy；干净 clean，脏 dirty；总是 always，从不 never；方位 on/in/under/behind 各就位。</div>' +
             '<div class="body-text">辨析不是死记，而是“见词想搭档”：tidy↔messy，clean↔dirty，always↔never。</div>')
    add(vdiff, 2)
    vdict = (section_head("词", "新词 ④ · 听写自测（点击翻牌）") + sub_label("看中文，翻牌核对英文拼写") +
             recall_grid([(cn, en) for cn, en in VDICT_L4]) +
             '<div class="body-text">家长可对照此页听写；错词请回到新词页重记。</div>' +
             '<div class="note-panel"><div class="np-title">记忆提示</div>先记“家具/形容词”再记“介词/副词”，反义词成对记效率更高。</div>')
    add(vdict, 2)

    # 段3 语法精讲
    for gi, g in enumerate(GRAMMAR_L4, 1):
        t = g["title"]
        pa = (section_head("法", "考点%d · 构成与用法 + 例句" % gi) +
              '<div class="sub-label">一 · 构成与用法</div>' +
              '<div class="body-text">%s</div>' % g["usage"] +
              '<div class="sub-label">二 · 典型例句</div>' +
              example_section(g["examples"]) +
              '<div class="sub-label">三 · 中考怎么考</div>' +
              '<div class="note-panel"><div class="np-title">考法预警</div>%s</div>' % GRAMMAR_NOTE_L4.get(gi, ""))
        add(pa, 3, t, "语法精讲")
        pb = (section_head("法", "考点%d · 易错 + 口诀 + 色卡" % gi) +
              '<div class="sub-label">三 · 高频易错</div>' +
              error_callout(g["errors"]) +
              '<div class="sub-label">四 · 记忆口诀</div>' +
              '<div class="note-panel"><div class="np-title">口诀</div>%s</div>' % g["mnemonic"] +
              '<div class="sub-label">五 · 语法要点色卡</div>' +
              grammar_cards(g["cards"]))
        add(pb, 3, t, "语法精讲")
        pc = section_head("法", "考点%d · 中考考法·即时小测" % gi)
        for q, opts in GEXTRA_L4.get(gi, []):
            pc += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
            for letter, text, cor in opts:
                pc += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
            pc += '</div>'
        pc += '<div class="body-text">中考常在语篇中混考名词单复与 There be，看清“单复/就近”再下笔。</div>'
        add(pc, 3, t, "语法精讲")
    prep_mat = (section_head("法", "房间介词全家福 · 方位一览表") + sub_label("on/in/under/behind/between/next to/above 一网打尽") +
        '<table class="pm-table">' +
        '<tr><th class="pm-num">介词</th><th>含义</th><th class="pm-xing">例句</th></tr>' +
        '<tr><td class="pm-zhug">on</td><td>在…上（表面）</td><td>on the desk</td></tr>' +
        '<tr><td class="pm-zhug">in</td><td>在…里（内部）</td><td>in the wardrobe</td></tr>' +
        '<tr><td class="pm-bin">under</td><td>在…下</td><td>under the bed</td></tr>' +
        '<tr><td class="pm-bin">behind</td><td>在…后</td><td>behind the door</td></tr>' +
        '<tr><td class="pm-ming">between</td><td>在两者间</td><td>between A and B</td></tr>' +
        '<tr><td class="pm-ming">next to</td><td>紧邻</td><td>next to the window</td></tr>' +
        '<tr><td class="pm-warn">above</td><td>在…上方</td><td>above the chair</td></tr>' +
        '</table>' +
        '<div class="note-panel"><div class="np-title">记忆顺序</div>on 上、in 里、under 下、behind 后、between 两者间、next to 紧邻、above 正上方。</div>')
    add(prep_mat, 3)
    gsum = (section_head("法", "三大考点综合梳理") +
            key_points([("名词复数", "一般加 -s；s/x/ch/sh/o 加 -es；f/fe 变 ves；不规则单独记。"),
                        ("房间介词", "on/in/under/behind/between/next to/above 描述位置。"),
                        ("There be", "There is 单数，There are 复数；就近原则。"),
                        ("中考考法", "完形与语法填空常考单复数一致与就近原则。"),
                        ("顺序记忆", "先变复数，再选介词，最后套 There be。")]) +
            '<div class="note-panel"><div class="np-title">易混速记</div>box→boxes，shelf→shelves，child→children；on/in/under 三基位；there is/are 随主语。</div>' +
            '<div class="sub-label">实战例句</div>' +
            example_section([("two boxes", "x 结尾加 -es"),
                             ("on the desk", "表面上方"),
                             ("There are two chairs.", "there are 接复数")]))
    add(gsum, 3)
    zhenti = (section_head("法", "中考真题体验 · 名词复数与 There be") +
              reading_block("微阅读 · 语法填空",
                  ["There ____ (be) a desk and two chairs in my room.",
                   "A shelf has many ____ (book) on it."],
                  [("1","空格处 be 动词用 is 还是 are？",[("A","is","1"),("B","are","0"),("C","have","0")]),
                   ("2","shelf 后的 book 应填单数还是复数？",[("A","book","0"),("B","books","1"),("C","bookes","0")])]) +
              '<div class="body-text">中考常把名词单复数与 There be 混在同一语篇中考查，务必看清单复数与就近。</div>' +
              '<div class="note-panel"><div class="np-title">真题解析</div>题1 最近主语 a desk 单数，用 is；题2 many 后接复数 books。</div>')
    add(zhenti, 3)
    pfill = section_head("法", "语法综合应用 · There be 与复数填空") + sub_label("用正确形式填空")
    for q, opts in PRONFILL_L4:
        pfill += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            pfill += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        pfill += '</div>'
    pfill += '<div class="body-text">综合考查名词复数与 There be 一致，是中考“语法填空”微型演练。</div>'
    pfill += '<div class="note-panel"><div class="np-title">填空思路</div>① 看主语单/复选 is/are；② 看名词是否加 -s/-es；③ there be 表存在不用 have。</div>'
    add(pfill, 3)

    # 段4 随堂演练
    quiz_all = QUIZ_L4 + QUIZ_EXTRA_L4 + QUIZ_EXTRA2_L4 + QUIZ_EXTRA3_L4
    q1 = section_head("练", "随堂演练 ① · 语法选择（1–14）")
    for q, opts in quiz_all[:14]:
        q1 += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            q1 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        q1 += '</div>'
    q1 += '<div class="note-panel"><div class="np-title">解题锦囊</div>① 题1、4、7、10、13、16、19、22、25、28 考 There is/are 与就近；② 题2、5、9、13、18、22、24、27 考名词复数；③ 题3、6、8、11、17、20、23 考房间介词。</div>'
    add(q1, 4)
    q2 = section_head("练", "随堂演练 ② · 语法选择（15–28）")
    for q, opts in quiz_all[14:]:
        q2 += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            q2 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        q2 += '</div>'
    q2 += '<div class="note-panel"><div class="np-title">解题锦囊</div>看清“空格后是单数还是复数”选 is/are；名词尾字母决定加 -s 还是 -es；介词看“接触/包含/方位”。</div>'
    add(q2, 4)
    drill = section_head("练", "句型操练 · 中译英（点击翻牌看答案）") + sub_label("用本课语法翻译下列句子")
    drill += recall_grid([(cn, en) for cn, en in DRILL_L4])
    drill += '<div class="body-text">先自己说/写英文，再翻牌核对；重点用对名词复数与 There be。</div>'
    drill += '<div class="note-panel"><div class="np-title">翻译要点</div>中文“有”在“某处”用 There is/are；物品位置用 on/in/under/behind/between；复数名词莫忘 -s。</div>'
    add(drill, 4)
    fill = (section_head("练", "语法填空演练") +
            '<div class="quiz-q"><div class="qq-text">1. There ____ (be) a book. There ____ (be) two pens.</div>'
            '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">is; are</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">are; is</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">is; is</button></div>'
            '<div class="quiz-q"><div class="qq-text">2. A box ____ (become) two ____ (box).</div>'
            '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">becomes; boxes</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">become; box</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">becomes; box</button></div>'
            '<div class="quiz-q"><div class="qq-text">3. The cat is ____ (behind) the door.</div>'
            '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">behind</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">under</button>'
            '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">above</button></div>'
            '<div class="body-text">语法填空是湖南中考省卷“语法诊断/语法填空”题型的微型演练。</div>' +
            '<div class="note-panel"><div class="np-title">解析</div>题1 单数 a book→is，复数 two pens→are；题2 box 三单 becomes，复数 boxes；题3 behind 在门后。</div>')
    add(fill, 4)
    errd = section_head("练", "随堂演练 ③ · 改错专练") + sub_label("找出错误项并改正")
    for q, opts in ERRDRILL_L4:
        errd += '<div class="quiz-q"><div class="qq-text">%s</div>' % q
        for letter, text, cor in opts:
            errd += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        errd += '</div>'
    errd += '<div class="body-text">改错题是中考“语法诊断”的变形，先找错再用正确形式替换。</div>'
    errd += '<div class="note-panel"><div class="np-title">改错思路</div>先判断错在哪一类：名词单复数、介词误用、还是 There be 与 have 混淆，再替换。</div>'
    add(errd, 4)

    # 段5 阅读理解
    ra_text = ("Lily is a middle school student. Her bedroom is very beautiful, clean and tidy. "
               "In her room, a warm bed is near the window. Next to the bed, there is a desk. "
               "A pink lamp is on the desk. Her clothes are in the big wardrobe. "
               "Under the chair, there is a blue soccer ball. "
               "Lily likes to read books at her desk every evening. "
               "She thinks a clean and tidy room always makes her feel very happy every single day of her life.")
    paras_a = [s.strip() for s in ra_text.split(".") if s.strip()]
    rb_text = ("Tim has a younger brother named Sam. Sam is a very sweet boy, but his bedroom is always extremely messy. "
               "His books are on the cold floor, and his schoolbag is under the chair. "
               "His clothes are everywhere in the room. Yesterday afternoon, Sam could not find his keys anywhere in the house. "
               "Tim decided to help him clean up quickly. They cleaned the desk together, put all the books into the tall bookcase, and arranged the clothes nicely. "
               "Now the room is very clean and tidy. Their mother was very happy and gave them some fresh red apples. "
               "Sam promised to keep his room tidy from now on.")
    paras_b = [s.strip() for s in rb_text.split(".") if s.strip()]
    qa = [("1", "Where is Lily's bed?", [("A","Near the window","1"),("B","On the floor","0"),("C","Under the chair","0")]),
          ("2", "What is on the desk?", [("A","A book","0"),("B","A pink lamp","1"),("C","A computer","0")]),
          ("3", "Where is the soccer ball?", [("A","On the bed","0"),("B","In the wardrobe","0"),("C","Under the chair","1")]),
          ("4", "What does Lily like to do at her desk?", [("A","Read books","1"),("B","Watch TV","0"),("C","Play soccer","0")]),
          ("5", "What does a tidy room make Lily feel?", [("A","Sad","0"),("B","Happy","1"),("C","Tired","0")])]
    add(section_head("读", "阅读 A · Lily's Bedroom（篇章）") +
        '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in paras_a) + '</div>' +
        '<div class="body-text">读前先猜：这是一篇关于“整洁卧室”的说明，注意家具与位置关系。</div>' +
        '<div class="note-panel"><div class="np-title">中文大意</div>莉莉是一名中学生，她的卧室漂亮、干净又整洁。房间里，一张温暖的床靠近窗户；床边有一张书桌，桌上有一盏粉色台灯。她的衣服在大衣柜里。椅子下面有一个蓝色的足球。莉莉每天傍晚喜欢在桌前读书，她觉得干净整洁的房间让她每天都很开心。</div>' +
        '<div class="note-panel"><div class="np-title">长难句拆解</div>'
        '① “Next to the bed, there is a desk.” —— there be 句型，a desk 单数用 is；<br>'
        '② “a clean and tidy room always makes her feel very happy” —— make sb. feel + adj. 让某人感到……。</div>', 5)
    a_q = reading_block("阅读 A · 理解题", paras_a, [qa[0],qa[1],qa[2],qa[3],qa[4]])
    a_q += '<div class="note-panel"><div class="np-title">答案解析</div>题1 由“a warm bed is near the window”得靠窗；题2 由“A pink lamp is on the desk”得台灯；题3 由“Under the chair…a blue soccer ball”得椅下；题4 由“likes to read books”得读书；题5 由“makes her feel very happy”得开心。</div>'
    add(a_q, 5)
    add(section_head("读", "阅读 B · Sam's Room（篇章）") +
        '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in paras_b) + '</div>' +
        '<div class="body-text">圈出位置词（on the floor / under the chair / in the bookcase），回题定位更快。</div>' +
        '<div class="note-panel"><div class="np-title">中文大意</div>蒂姆有个弟弟叫萨姆。萨姆很乖，但卧室总是特别乱：书在地上，书包在椅下，衣服到处都是。昨天下午萨姆找不到钥匙，蒂姆帮他收拾，把书放进高书柜、衣服叠好。现在房间干净整洁，妈妈很高兴，给了他们红苹果，萨姆答应以后保持整洁。</div>' +
        '<div class="note-panel"><div class="np-title">长难句拆解</div>'
        '① “His books are on the cold floor” —— 复数主语 books 配 are；<br>'
        '② “They cleaned the desk together, put…into the tall bookcase” —— 并列谓语 cleaned / put。</div>', 5)
    qb = [("1", "What was Sam's room like before?", [("A","Clean","0"),("B","Messy","1"),("C","Large","0")]),
          ("2", "Where was Sam's schoolbag?", [("A","Under the chair","1"),("B","On the desk","0"),("C","In the bookcase","0")]),
          ("3", "Who helped Sam clean the room?", [("A","His sister","0"),("B","His brother Tim","1"),("C","His mother","0")]),
          ("4", "What did mother give them?", [("A","Some books","0"),("B","New keys","0"),("C","Some apples","1")]),
          ("5", "What did Sam promise to do?", [("A","Keep his room tidy","1"),("B","Buy a new desk","0"),("C","Clean once a month","0")])]
    b_q = reading_block("阅读 B · 理解题", paras_b, [qb[0],qb[1],qb[2],qb[3],qb[4]])
    b_q += '<div class="note-panel"><div class="np-title">答案解析</div>题1 由“always extremely messy”得凌乱；题2 由“schoolbag is under the chair”得椅下；题3 由“Tim decided to help him”得哥哥蒂姆；题4 由“gave them some fresh red apples”得苹果；题5 由“promised to keep his room tidy”得保持整洁。</div>'
    add(b_q, 5)
    w5paras = ["Keeping your room tidy is a good habit. __(11)__",
               "First, clean your study desk and put all your books in the tall bookcase carefully. __(12)__",
               "Second, make your bed neatly every morning after you wake up. __(13)__",
               "Third, put your shoes under the bed or in the shoe cabinet. __(14)__",
               "A tidy room helps you find your things quickly and feel happy."]
    w5opts = [("A","Here are three easy ways to do it."),
              ("B","You should also keep your clothes in the wardrobe."),
              ("C","This keeps your desk clean and tidy."),
              ("D","A messy room makes you feel sad and tired."),
              ("E","Your room looks nice and clean every day.")]
    w5ans = {11:"A",12:"C",13:"B",14:"E"}
    add(five_pick_block("阅读 C · 五选四（Keep Your Room Tidy·篇章）", w5paras, w5opts, w5ans) +
        '<div class="body-text">从 A–E 中选出最佳句子填入 __（11–14）__ 空白，注意前后逻辑衔接（D 为多余项，五选四）。</div>' +
        '<div class="note-panel"><div class="np-title">中文大意</div>保持房间整洁是个好习惯。这里有三种简单方法：一、清理书桌把书放进高书柜（这样书桌整洁）；二、每天早晨叠好床（衣服也要放进衣柜）；三、鞋放在床下或鞋柜。整洁的房间让你找东西快、心情好。</div>', 5)
    c_q = section_head("读", "阅读 C · 五选四（题目）")
    for num in sorted(w5ans.keys()):
        ans = w5ans[num]
        c_q += '<div class="quiz-q"><div class="qq-text">__（%d）__ 应填：</div>' % num
        for letter, text in w5opts:
            cor = '1' if letter == ans else '0'
            c_q += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        c_q += '</div>'
    c_q += '<div class="note-panel"><div class="np-title">答案解析</div>11→A（总起三种方法）；12→C（承接“清理书桌”说书桌整洁）；13→B（承接“叠床”补充衣服入柜）；14→E（收束，房间整洁）；D 为多余项。</div>'
    add(c_q, 5)
    reading_tip = (section_head("读", "阅读解题 SOP") +
                   key_points([("先题后文", "先读题干圈关键词，再回原文定位。"),
                               ("细节题", "题干词多在原文原词复现，直接比对。"),
                               ("位置题", "Where 问位置，找 on/in/under/behind 等介词短语。"),
                               ("五选四", "看空白前后句逻辑，排除重复/矛盾项。"),
                               ("猜词法", "利用上下文线索、同义复现猜测生词含义。"),
                               ("主旨题", "找首尾句与高频词，避免以偏概全。")]) +
                   '<div class="note-panel"><div class="np-title">本课的阅读</div>'
                   'A/B 篇为房间细节题（位置+态度），C 篇为五选四逻辑衔接题，介词与名词复数是定位关键。</div>')
    add(reading_tip, 5)
    rmore = (section_head("读", "阅读实战 · 细节定位再练") +
             '<div class="body-text">下列题目需回看前面“阅读 A：莉莉卧室”与“阅读 B：萨姆房间”篇章定位（答案请回原文核对）。</div>')
    rmore_quiz = [
        ("1", "Where is Lily's pink lamp?", [("A","On the desk","1"),("B","Under the bed","0"),("C","In the wardrobe","0")]),
        ("2", "Whose bedroom is always messy?", [("A","Lily's","0"),("B","Sam's","1"),("C","Tim's","0")]),
        ("3", "Where did Tim put the books?", [("A","On the floor","0"),("B","In the bookcase","0"),("C","Under the chair","1")]),
        ("4", "What does Lily do every evening?", [("A","Watch TV","0"),("B","Play soccer","0"),("C","Read books","1")]),
        ("5", "What did mother give Sam and Tim?", [("A","New books","0"),("B","Red apples","1"),("C","Blue balls","0")]),
        ("6", "Where are Lily's clothes?", [("A","On the floor","0"),("B","Under the chair","0"),("C","In the wardrobe","1")]),
        ("7", "Did Sam promise to keep his room tidy?", [("A","Yes, he did","1"),("B","No, he didn't","0"),("C","He never did","0")]),
    ]
    for qnum, q, opts in rmore_quiz:
        rmore += '<div class="quiz-q"><div class="qq-text">%s. %s</div>' % (qnum, q)
        for letter, text, cor in opts:
            rmore += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        rmore += '</div>'
    rmore += '<div class="note-panel"><div class="np-title">定位提示</div>题1 回阅读 A 找“pink lamp is on the desk”；题2 由“Sam…messy”得；题3 由“put all the books into the tall bookcase”得；题4 由“read books every evening”得；题5 由“red apples”得；题6 由“clothes are in the big wardrobe”得；题7 由“promised to keep…tidy”得。</div>'
    add(rmore, 5)

    # 段6 自然拼读
    add(phonics_block(PHONICS_L4), 6)
    ph2 = (section_head("拼", "辅音连缀拼读演练") +
           key_points([("br /br/", "bread, brown, brother——双唇爆破+摩擦。"),
                       ("cr /kr/", "cry, crab, cry——舌根爆破+摩擦。"),
                       ("dr /dr/", "draw, dress, drive——浊化连缀。"),
                       ("fr /fr/", "friend, fruit, free——唇齿摩擦+流音。"),
                       ("tr /tr/", "tree, train, try——清化连缀。"),
                       ("gr /gr/", "green, grade, grow——舌根爆破+流音。")]) +
           '<div class="sub-label">常见词族</div>' +
           key_points([("-ead", "bread, read, head"),
                       ("-ee", "tree, green, free"),
                       ("-ai", "train, rain, brain"),
                       ("-ow", "grow, brown, draw"),
                       ("-iend", "friend, fiend")]) +
           '<div class="note-panel"><div class="np-title">拼读口诀</div>'
           'br 面包 brother 来，cr 哭 cry crab 在；dr 画 draw dress 穿，fr 友 friend fruit 甜；tr 树 tree train 跑，gr 绿 green grade 高；连缀发音要“快连”。</div>')
    add(ph2, 6)
    ph3 = (section_head("拼", "辅音连缀拼读小结 · 儿歌") +
           '<div class="note-panel"><div class="np-title">拼读儿歌</div>'
           'br br /br/ bread brother 面包香，cr cr /kr/ cry crab 哭嚷嚷；<br>dr dr /dr/ draw dress 画又穿，fr fr /fr/ friend fruit 友甜甜；<br>tr tr /tr/ tree train 树跑快，gr gr /gr/ green grade 绿高高；<br>辅音连缀连着读，发音流利真叫棒！</div>' +
           key_points([("口型", "br/dr 需双唇参与，tr/dr 舌尖卷起。"),
                       ("位置", "cr/gr 舌根与软腭接触成爆破。"),
                       ("fr", "上齿轻触下唇发摩擦，再加流音 r。"),
                       ("tr/dr 区别", "tr 清（不振动声带），dr 浊（振动声带）。"),
                       ("br/gr 区别", "br 双唇，gr 舌根，位置不同。"),
                       ("练习", "bread/brown 反复读，体会连缀感。"),
                       ("词族", "tree/green/free 同含 /iː/ 长音。"),
                       ("对比", "连缀是两个辅音一次成音，不插入元音。")]))
    add(ph3, 6)

    # 段7 课堂练习
    cv_quiz = [
        ("椅子", "chair", [("chair","1"),("sofa","0"),("lamp","0")]),
        ("衣柜", "wardrobe", [("drawer","0"),("wardrobe","1"),("shelf","0")]),
        ("整洁的", "tidy", [("messy","0"),("tidy","1"),("clean","0")]),
        ("在…后面", "behind", [("under","0"),("behind","1"),("above","0")]),
        ("足球", "soccer", [("ball","0"),("soccer","1"),("habit","0")]),
        ("在…之间", "between", [("between","1"),("above","0"),("next","0")]),
        ("总是", "always", [("never","0"),("always","1"),("sometimes","0")]),
        ("抽屉", "drawer", [("drawer","1"),("wardrobe","0"),("sofa","0")]),
    ]
    cv1 = section_head("戏", "课堂游戏 · 跨课词汇快选 ①") + sub_label("看中文，选出正确英文")
    cv1 += '<div class="note-panel"><div class="np-title">玩法</div>点击与中文对应的英文词，答对响铃。</div>'
    for cn, en, opts in cv_quiz[:4]:
        cv1 += '<div class="quiz-q"><div class="qq-text">“%s” 是哪个词？</div>' % cn
        for w, cor in opts:
            cv1 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s</button>' % (cor, w)
        cv1 += '</div>'
    cv1 += '<div class="note-panel"><div class="np-title">提示</div>遇到反义词（tidy/messy、clean/dirty）先辨褒贬再选；介词看方位。</div>'
    add(cv1, 7)
    cv2 = section_head("戏", "课堂游戏 · 跨课词汇快选 ②") + sub_label("看中文，选出正确英文")
    for cn, en, opts in cv_quiz[4:]:
        cv2 += '<div class="quiz-q"><div class="qq-text">“%s” 是哪个词？</div>' % cn
        for w, cor in opts:
            cv2 += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s</button>' % (cor, w)
        cv2 += '</div>'
    cv2 += '<div class="note-panel"><div class="np-title">游戏小结</div>跨课词汇快选训练“音—形—义”对应，是听力与完形的基础；错词请回到新词页再记。</div>'
    add(cv2, 7)
    listen = (section_head("戏", "听音选词 · 词义匹配") + sub_label("下列英文，哪个意思是“整洁的”？") +
              '<div class="quiz-q"><div class="qq-text">“整洁的” 对应：</div>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">tidy</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">messy</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">dirty</button></div>'
              '<div class="quiz-q"><div class="qq-text">“在…下” 对应：</div>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">on</button>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">under</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">in</button></div>'
              '<div class="quiz-q"><div class="qq-text">“架子” 对应：</div>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">shelf</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">sofa</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">chair</button></div>'
              '<div class="quiz-q"><div class="qq-text">“在…之间” 对应：</div>'
              '<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)">between</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">behind</button>'
              '<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)">above</button></div>'
              '<div class="body-text">巩固本课核心词义，为听力与完形打底。</div>')
    add(listen, 7)

    # 段8 课堂总结
    summary = (section_head("结", "课堂总结 · 知识图谱") +
               '<div class="kmap">' +
               '<div class="kmap-node"><div class="kn-title">名词复数</div><div class="kn-body">-s/-es/-ies/-ves；不规则 child→children, man→men, foot→feet。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">房间介词</div><div class="kn-body">on/in/under/behind/between/next to/above 描述位置。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">There be</div><div class="kn-body">There is 单数，There are 复数；就近原则。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">自然拼读</div><div class="kn-body">br/cr/dr/fr/tr/gr 辅音连缀发音。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">学习建议</div><div class="kn-body">每天听写 5 词＋造 2 句，周末回头复习，名词复数与 There be 务必熟练。</div></div>' +
               '</div>' +
               '<div class="note-panel"><div class="np-title">课后作业</div>'
               '① 背诵本课 20 个新词（家长听写）；② 完成配套基础练习；③ 用 There be + 介词写 5 句描述自己房间；④ 整理错题本（本课易错 10 句）。</div>' +
               '<div class="note-panel"><div class="np-title">巩固建议</div>错题本按“名词复数”“房间介词”“There be”三类归档，每周回看一次，避免重复犯错。</div>')
    add(summary, 8)
    err_review = (section_head("结", "易错清单回顾") +
                  error_callout([("There is two book.","There are two books."),
                                 ("These box are new.","These boxes are new."),
                                 ("The book is at the desk.","The book is on the desk."),
                                 ("Next the window is a lamp.","Next to the window is a lamp."),
                                 ("There have a cat.","There is a cat."),
                                 ("A childs is here.","A child is here."),
                                 ("The ball is below the bed.","The ball is under the bed."),
                                 ("Between the desk are a chair.","Between the desk and the chair is a chair."),
                                 ("The shelf is white.","The shelves are white."),
                                 ("Is there some pens?","Are there any pens?")]) +
                  '<div class="note-panel"><div class="np-title">避坑口诀</div>名词变复看词尾，es/ies/ves 各有规；方位 on/in/under 准，there be 存在不用 have。</div>')
    add(err_review, 8)
    preview = (section_head("结", "下节课预告 · 第 5 课") +
               key_points([("语法①", "祈使句（表请求、命令、建议）。"),
                           ("语法②", "What 引导的特殊疑问句。"),
                           ("语法③", "like 的用法（喜欢）。"),
                           ("新词", "food/sport/like 等日常词汇。")]) +
               '<div class="note-panel"><div class="np-title">课前准备</div>复习本课名词复数与 There be，下节课用它来“描述喜欢的东西与发出指令”。</div>' +
               '<div class="note-panel"><div class="np-title">课前任务</div>① 默写本课 20 词（家长签字）；② 用 There be 写 3 句房间描述；③ 预习祈使句含义。</div>')
    add(preview, 8)

    total = p - 1
    seg_pages = {}
    for sid, (a, b) in seg.items():
        seg_pages[sid] = [a, b]
    return pages, seg_pages, total

TITLES = {1:"第1课 · 人称代词与be动词", 2:"第2课 · 指示代词/be否定疑问/Who问句", 3:"第3课 · 名词所有格/基数词/Where问句", 4:"第4课 · 名词复数/房间介词/There be"}
BUILDERS = {1: build_lesson_1, 2: build_lesson_2, 3: build_lesson_3, 4: build_lesson_4}

def main():
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    builder = BUILDERS.get(n)
    if not builder:
        print("未实现第%d课" % n); sys.exit(1)
    pages, seg_pages, total = builder()
    js_extra = JS_EXTRA_TPL % (total, json.dumps(seg_pages, ensure_ascii=False))
    title = TITLES.get(n, "第%d课" % n)
    html = build_courseware(title, pages, js_extra,
                            session="L%d" % n, nav_html=NAV,
                            stage_badge="Stage 1 · L%d 七上基础" % n, n_pages=total, css_extra=CSS_EXTRA)
    out = "D:/英语教学/许颖嘉/第%02d课/课件成品_网页PPT/第%02d课_课件.html" % (n, n)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write(html)
    print("WRITTEN", out, "bytes", len(html.encode("utf-8")), "pages", total)

if __name__ == "__main__":
    main()
