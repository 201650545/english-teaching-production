# -*- coding: utf-8 -*-
"""邓兴华 L07 课件 builder（阶段测试Ⅰ·讲评课，五段式，page-id 契约）
课名：阶段测试Ⅰ · 七上基础综合诊断（L1-L6 全部 18 个语法考点 · 120 词综合诊断）
结构（41 页）：
  ① 测试概况 4 页（封面/讲评课总纲/全卷得分分布/Top10 高频错题）
  ② 语法错题精讲 10 页（P5 代词类 G01/G02/G04 · P6 be动词类 G03/G05 · P7 疑问句类 G06/G09/G14
     · P8 名词类 G07/G10/G17 · P9 介词类 G12 · P10 祈使句类 G13 · P11 动词搭配类 G15/G18
     · P12 时态类 G16 · P13 数词类 G08 · P14 综合错题 G10-G18）
  ③ 词汇错题精讲 5 页（L1+L2 / L3+L4 / L5 / L6 / 策略总结）
  ④ 阅读写作讲评 5 页（阅读A / 阅读B / 五选四 / 简答翻译 / 写作范文）
  ⑤ 总结 3 页（薄弱考点清单 / 下阶段计划 / 核心口诀总览）
  + 延伸练习 14 页（语法×4 / 词汇×2 / 阅读×2 / 数词×1 / 综合诊断×5）
内容全部从 第07课时_课件.html 原样提取，不虚构。
全部使用引擎标准类名；旧版类（bar-chart/err-rate/grade-tag/gpoint-* 等）在 CSS_L07 自绘补齐。
"""
import json, os, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

core = _load("core", "courseware_core.py")
g    = _load("g",    "gen_l1_l13_v2.py")
E    = _load("eng",  "courseware_engine.py")

section_head = g.section_head
sub_label    = g.sub_label
key_points   = g.key_points
grammar_cards= g.grammar_cards
page         = core.page
build_courseware = core.build_courseware
quiz_html    = E.quiz_html
flash_grid   = E.flash_grid
game_board   = E.game_board
ext_cards    = E.ext_cards

# 视觉合同标记（courseware_engine.py 第 1911-1924 行 5 个 CW-SECTION 标记）
CSS_CONTRACT_MARKERS = (
    '/* <CW-CSS-EXTRA version="1.0" required="true"> */\n'
    '/* <CW-SECTION name="tokens"> */\n'
    '/* </CW-SECTION> */\n'
    '/* <CW-SECTION name="components"> */\n'
    '/* </CW-SECTION> */\n'
    '/* <CW-SECTION name="states"> */\n'
    '/* </CW-SECTION> */\n'
    '/* <CW-SECTION name="theme"> */\n'
    '/* </CW-SECTION> */\n'
    '/* <CW-SECTION name="patches"> */\n'
    '/* </CW-SECTION> */\n'
    '/* </CW-CSS-EXTRA> */\n'
)

# ============================================================
# L07 自绘样式（旧版类 + 引擎缺失类，用主题变量补齐；主文本≥18px，触屏目标≥44px）
# ============================================================
CSS_L07 = r"""
/* formula-box 覆盖为红金复习主题（引擎默认蓝底，与本课 review 主题不符） */
.formula-box{background:linear-gradient(140deg,#7A1420,#B0303E);border-radius:20px;padding:20px 24px;color:#fff;box-shadow:0 4px 16px rgba(230,57,70,.25);margin:12px 0;}
.formula-box .formula-text{font-size:26px;font-weight:900;color:#FFE66D;line-height:1.5;margin-bottom:6px;}
.formula-box .formula-sub{font-size:18px;color:#FFD9D9;line-height:1.5;}
.formula-label{font-size:20px;color:#FFE66D;font-weight:700;margin-bottom:8px;}
.formula-main{font-size:26px;font-weight:900;color:#FFD9D9;line-height:1.5;}
.formula-ex{font-size:20px;color:#fff;margin-top:10px;line-height:1.5;}
.formula-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:12px 0;}
.formula-mini{background:#fff;border-radius:12px;padding:12px 16px;box-shadow:0 2px 10px rgba(0,0,0,.08);border-left:4px solid var(--brand);}
.formula-mini:nth-child(odd){border-left-color:var(--accent);}
.formula-mini-num{font-size:18px;font-weight:800;color:var(--brand);margin-bottom:4px;}
.formula-mini-text{font-size:18px;line-height:1.5;color:var(--text-primary);}

/* 卡片 / 栅格 */
.card{background:#fff;border-radius:14px;padding:14px 18px;box-shadow:0 2px 12px rgba(0,0,0,.08);margin:10px 0;}
.card-title{font-size:22px;font-weight:800;color:var(--brand);margin-bottom:8px;}
.card-content{font-size:18px;line-height:1.7;color:var(--text-primary);}
.grid-2{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:10px 0;}
.grid-3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:10px 0;}
.grid-4{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:10px;margin:10px 0;}

/* 提示框 */
.tip-box{background:var(--table-highlight-bg);border-left:4px solid var(--accent);border-radius:10px;padding:12px 16px;margin:12px 0;font-size:18px;line-height:1.6;color:var(--text-primary);}
.tip-box strong{color:var(--brand);}

/* 对错对照 */
.compare-box{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin:12px 0;}
.compare-side{border-radius:12px;padding:14px 16px;font-size:18px;line-height:1.8;}
.compare-wrong{background:var(--error-row-bg);border:1px solid rgba(230,57,70,.3);}
.compare-correct{background:var(--correct-row-bg);border:1px solid rgba(6,167,125,.3);}
.compare-label{font-weight:800;margin-bottom:6px;}
.compare-wrong .compare-label{color:var(--error);}
.compare-correct .compare-label{color:var(--correct);}

/* 表格 */
.error-table{width:100%;border-collapse:collapse;margin:10px 0;font-size:18px;box-shadow:0 2px 10px rgba(0,0,0,.08);border-radius:10px;overflow:hidden;}
.error-table thead{background:var(--table-header-bg);color:#fff;}
.error-table th{padding:9px 12px;font-size:18px;font-weight:700;text-align:center;}
.error-table td{padding:8px 10px;border-bottom:1px solid #f0e0d0;text-align:center;font-size:17px;line-height:1.5;}
.error-table tbody tr:nth-child(even){background:rgba(255,248,225,.5);}

/* 柱状图（得分分布） */
.bar-chart{display:flex;align-items:flex-end;justify-content:space-around;gap:8px;height:220px;padding:10px 4px 0;margin:8px 0;}
.bar-item{display:flex;flex-direction:column;align-items:center;justify-content:flex-end;flex:1;min-width:0;}
.bar-value{font-size:18px;font-weight:800;color:var(--brand);margin-bottom:4px;}
.bar{width:60%;max-width:46px;background:linear-gradient(180deg,var(--brand),var(--brand-light));border-radius:6px 6px 0 0;min-height:10px;}
.bar.accent{background:linear-gradient(180deg,#B8860B,#F5C542);}
.bar.warn{background:linear-gradient(180deg,#C0392B,#E67E73);}
.bar-label{font-size:16px;color:var(--text-secondary);margin-top:6px;text-align:center;line-height:1.3;}

/* 错误率徽标 / 等级徽标 */
.err-rate{color:var(--error);font-weight:800;}
.grade-tag{display:inline-block;padding:2px 10px;border-radius:10px;font-size:16px;font-weight:800;color:#fff;}
.grade-tag.grade-a{background:#06A77D;}
.grade-tag.grade-b{background:#F59E0B;}
.grade-tag.grade-c{background:#E63946;}

/* 考点精讲细节（gpoint-*） */
.gpoint-detail{background:#fff;border-radius:12px;padding:14px 18px;margin:12px 0;box-shadow:0 2px 10px rgba(0,0,0,.08);border-top:4px solid var(--accent);}
.gpoint-header{display:flex;align-items:center;gap:10px;margin-bottom:8px;}
.gpoint-title{font-size:20px;font-weight:800;color:var(--brand);}
.gpoint-tag{background:var(--accent);color:#333;font-size:14px;font-weight:700;padding:2px 10px;border-radius:10px;}
.gpoint-body{font-size:18px;line-height:1.8;color:var(--text-primary);}

/* 词汇卡补充 */
.vocab-word{font-size:24px;font-weight:800;color:var(--brand);}
.vocab-meaning{font-size:19px;color:var(--text-primary);margin:2px 0;font-weight:600;}
.vocab-tip{font-size:17px;color:var(--sop-purple);line-height:1.5;}

/* 正误例 */
.wrong-ex{color:var(--error);font-weight:700;}
.correct-ex{color:var(--correct);font-weight:700;}

/* 作文范文区 */
.essay-box{background:#fff;border-radius:12px;padding:18px 22px;box-shadow:0 2px 12px rgba(0,0,0,.08);border-left:4px solid var(--accent);font-size:19px;line-height:1.8;color:var(--text-primary);}
.essay-score{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0;}
.score-item{background:#fff;border-radius:10px;padding:10px 16px;box-shadow:0 2px 8px rgba(0,0,0,.06);font-size:18px;line-height:1.5;flex:1 1 200px;}
.score-item strong{color:var(--brand);}

/* 触屏目标 ≥44px */
.quiz-opt{min-height:44px;display:flex;align-items:center;}

/* 词汇策略三级卡配色 */
.rule-card{font-size:18px;line-height:1.7;}
.rule-card em{font-style:normal;color:var(--text-secondary);font-size:17px;}
"""

# ============================================================
# 页面装配
# ============================================================
def build_l07():
    _QSEQ_save = E._QSEQ
    E._QSEQ = 0
    card = {
        "lesson": 7, "student": "邓兴华", "tier": "中等", "stage": "S2", "type": "test",
        "grammar": ["G01-G18 全考点诊断", "五类错题精讲", "阶段测试讲评"],
        "theme": "阶段测试Ⅰ",
        "vocab": {"theme": "review"},
        "phonics": "阶段测试Ⅰ讲评（无拼读新授）",
    }
    title = "第7课时 · 阶段测试Ⅰ讲评"
    stage_badge = "中等 · Stage 2 · L7 阶段测试Ⅰ"
    pages = {}
    seg = {}
    page_meta = {}
    p = 1
    def add(inner, seg_id, t="", sub="", priority="CORE", minutes=5):
        nonlocal p
        pages[p] = page(p, t, sub, inner, active=(p == 1))
        seg.setdefault(seg_id, [p, p]); seg[seg_id][1] = p
        page_meta[p] = {"p": priority, "m": minutes}
        p += 1

    # ---- 段1 测试概况 ----
    cover = ('<div class="cover-wrap">'
             '<div class="cover-badge">阶段测试Ⅰ · 邓兴华</div>'
             '<div class="cover-title">七上基础综合诊断</div>'
             '<div class="cover-sub">L1-L6 全部 18 个语法考点 · 120 词 · 讲评课件</div>'
             '<div class="cover-tagline">📐 五段式讲评 · 🎯 G01-G18 全覆盖 · 📝 120 词诊断</div>'
             '<div class="cover-info">'
             '<div class="cover-info-num"><div class="ci-label">测试范围</div><div class="ci-val">L1-L6</div></div>'
             '<div class="cover-info-num"><div class="ci-label">考点数</div><div class="ci-val">18</div></div>'
             '<div class="cover-info-num"><div class="ci-label">词汇量</div><div class="ci-val">120</div></div>'
             '<div class="cover-info-num"><div class="ci-label">满分</div><div class="ci-val">100</div></div>'
             '</div>'
             '<div class="cover-emoji">📊</div></div>')
    add(cover, 1)

    outline = (section_head("总", "阶段测试Ⅰ · 讲评课总纲") +
               '<div class="body-text"><span class="highlight">五段式讲评</span>：先看测试概况，再按语法/词汇/阅读写作三大错题精讲，最后总结提升计划并做延伸巩固。</div>' +
               '<div class="kmap">' +
               '<div class="kmap-node"><div class="kn-title">① 测试概况</div><div class="kn-body">得分分布 · Top10 高频错题</div></div>' +
               '<div class="kmap-node"><div class="kn-title">② 语法错题精讲</div><div class="kn-body">G01-G18 分 10 组精讲</div></div>' +
               '<div class="kmap-node"><div class="kn-title">③ 词汇错题精讲</div><div class="kn-body">L1-L6 词汇诊断与策略</div></div>' +
               '<div class="kmap-node"><div class="kn-title">④ 阅读写作讲评</div><div class="kn-body">阅读A/B、五选四、简答翻译、写作范文</div></div>' +
               '<div class="kmap-node"><div class="kn-title">⑤ 总结提升</div><div class="kn-body">薄弱考点清单 · 下阶段计划 · 口诀总览</div></div>' +
               '</div>' +
               '<div class="note-panel"><div class="np-title">讲评目标</div>① 找出失分点与错因；② 逐一精讲突破；③ 制定下阶段巩固计划；④ 延伸练习巩固到位。</div>')
    add(outline, 1, "讲评课总纲", "五段式")

    score_dist = (section_head("况", "测试概况 · 全卷得分分布") +
        '<div class="body-text"><span class="highlight">全班均值 71%（B 级）</span>，阅读 A 篇得分率最高（78%），完形与阅读 C 篇最低。</div>' +
        '<div class="card"><div class="card-title">📈 题型得分率（全班均值）</div>' +
        '<div class="bar-chart">' +
        '<div class="bar-item"><div class="bar-value">78%</div><div class="bar" style="height:140px;"></div><div class="bar-label">阅读A</div></div>' +
        '<div class="bar-item"><div class="bar-value">65%</div><div class="bar accent" style="height:117px;"></div><div class="bar-label">阅读B</div></div>' +
        '<div class="bar-item"><div class="bar-value">60%</div><div class="bar warn" style="height:108px;"></div><div class="bar-label">阅读C</div></div>' +
        '<div class="bar-item"><div class="bar-value">72%</div><div class="bar" style="height:130px;"></div><div class="bar-label">五选四</div></div>' +
        '<div class="bar-item"><div class="bar-value">55%</div><div class="bar warn" style="height:99px;"></div><div class="bar-label">完形</div></div>' +
        '<div class="bar-item"><div class="bar-value">68%</div><div class="bar accent" style="height:122px;"></div><div class="bar-label">选词</div></div>' +
        '<div class="bar-item"><div class="bar-value">70%</div><div class="bar" style="height:126px;"></div><div class="bar-label">作文</div></div>' +
        '<div class="bar-item"><div class="bar-value">58%</div><div class="bar warn" style="height:104px;"></div><div class="bar-label">诊断</div></div>' +
        '</div></div>' +
        '<div class="tip-box"><strong>📌 诊断结论：</strong>阅读 C 篇（健康饮食角）和完形填空得分率最低，可数/不可数名词（G17）和方位介词（G12）是主要失分点。阅读 A 篇得分率最高（78%），说明应用文信息定位法掌握较好。</div>' +
        '<div class="card"><div class="card-title">🎯 G01-G18 考点掌握度雷达解读</div>' +
        '<div class="body-text">得分率&lt;65% 的红色区域集中在 <span class="highlight">G02 物主代词、G07 名词所有格、G10 名词复数、G12 方位介词、G17 可数/不可数</span> 五个考点，是本课讲评重点。</div>' +
        key_points([("最高 A 级", "G01 代词主宾格 85% · G03 be 动词 88% · G13 祈使句 82%"),
                    ("良好 B 级", "G04/G05/G06/G08/G09/G11/G14/G15/G16/G18 均值 71%"),
                    ("待提升 C 级", "G02 物主代词 65% · G07 所有格 62% · G10 复数 60% · G12 方位介词 55% · G17 可数不可数 58%")]) +
        '</div>')
    add(score_dist, 1, "全卷得分分布", "题型得分率 · 考点雷达解读")

    top10 = (section_head("况", "测试概况 · Top 10 高频错题") +
        '<div class="body-text"><span class="highlight">Top 10 错题</span>集中在代词类（G02）、名词类（G07/G10/G17）、方位介词（G12）三大薄弱区。</div>' +
        '<table class="content-table"><thead><tr><th>#</th><th>题号</th><th>题型</th><th>考点</th><th>错误率</th><th>主导错因</th><th>定位</th></tr></thead><tbody>' +
        '<tr><td>1</td><td>55</td><td>语法诊断</td><td>G09+G12 Where/方位介词</td><td class="err-rate">72%</td><td>介词搭配混淆</td><td>→ 语法P9</td></tr>' +
        '<tr><td>2</td><td>56</td><td>语法诊断</td><td>G10-G18 综合</td><td class="err-rate">68%</td><td>多考点交叉失误</td><td>→ 语法P14</td></tr>' +
        '<tr><td>3</td><td>48</td><td>语法诊断</td><td>G02 物主代词</td><td class="err-rate">65%</td><td>形/名物主混用</td><td>→ 语法P5</td></tr>' +
        '<tr><td>4</td><td>38</td><td>选词填空</td><td>G10 名词规则复数</td><td class="err-rate">60%</td><td>复数词尾错误</td><td>→ 语法P8</td></tr>' +
        '<tr><td>5</td><td>28</td><td>完形填空</td><td>G07 名词所有格</td><td class="err-rate">58%</td><td>&#39;s 撇号位置错误</td><td>→ 语法P8</td></tr>' +
        '<tr><td>6</td><td>15</td><td>阅读C篇</td><td>G17 可数/不可数</td><td class="err-rate">55%</td><td>不可数加 s</td><td>→ 语法P8</td></tr>' +
        '<tr><td>7</td><td>53</td><td>语法诊断</td><td>G07 名词所有格</td><td class="err-rate">52%</td><td>所有格结构错误</td><td>→ 语法P8</td></tr>' +
        '<tr><td>8</td><td>20</td><td>五选四</td><td>G12 方位介词</td><td class="err-rate">50%</td><td>句际逻辑+介词双重失误</td><td>→ 语法P9</td></tr>' +
        '<tr><td>9</td><td>45</td><td>简答翻译</td><td>G06 Who 疑问句</td><td class="err-rate">48%</td><td>简答不完整</td><td>→ 阅读P22</td></tr>' +
        '<tr><td>10</td><td>39</td><td>选词填空</td><td>G02 物主代词</td><td class="err-rate">45%</td><td>my/mine 混淆</td><td>→ 语法P5</td></tr>' +
        '</tbody></table>' +
        '<div class="tip-box"><strong>📊 数据洞察：</strong>错因前三名：1 语法规则记忆不牢（42%）、2 语境理解偏差（31%）、3 粗心看错题（27%）。讲评按考点类别逐一突破。</div>')
    add(top10, 1, "Top10 高频错题", "三大薄弱区")

    # ---- 段2 语法错题精讲（10 页） ----
    # P5 代词类
    g_pron = (section_head("法", "语法错题精讲 · 代词类 G01/G02/G04") +
        '<div class="formula-box"><div class="formula-text">主格做主语，宾格做宾语；形物加名词，名物独立用</div>' +
        '<div class="formula-sub">G01 人称代词主格与宾格 · G02 形容词性与名词性物主代词 · G04 指示代词单复数</div></div>' +
        '<div class="grid-3">' +
        '<div class="rule-card rc-zhug"><strong>🔑 G01 主格 vs 宾格</strong><br>Can you help <b>me</b> with <b>my</b> English?<br>Is <b>this</b> your ruler? Yes, <b>it</b> is.<br><em>动词/介词后用宾格</em></div>' +
        '<div class="rule-card rc-bin"><strong>🔑 G02 形物 vs 名物</strong><br>my book = mine<br>your → yours<br>his → his | her → hers<br><em>mine 后不能再接名词</em></div>' +
        '<div class="rule-card rc-xing"><strong>🔑 G04 指示代词</strong><br>this 近单 / these 近复<br>that 远单 / those 远复<br><em>答语用 it / they</em></div>' +
        '</div>' +
        '<div class="compare-box">' +
        '<div class="compare-side compare-wrong"><div class="compare-label">❌ 常见错误</div>help <b>I</b>(应用宾格)<b>my</b>(✓)<br>your; my(空后无名词应用名物)<br>this; it(复数用 these/they)</div>' +
        '<div class="compare-side compare-correct"><div class="compare-label">✅ 正确写法</div>Can you help <b>me</b> with <b>my</b> English?<br>Is <b>this</b> your ruler? Yes, <b>it</b> is.</div>' +
        '</div>' +
        quiz_html([
            ("【第47题·G01】Can you help ___ with ___ English?（你能帮我学英语吗？）", "me; my", ["I; my", "me; mine"]),
            ("【第48题·G02】- Is this ruler ___? - No, ___ is in the pencil box.（这把尺子是你的吗？不，我的在文具盒里。）", "yours; mine", ["your; my", "yours; my"]),
            ("【第50题·G04】- Are ___ your friends? - Yes, ___ are.（那些是你的朋友吗？是的，他们是。）", "those; they", ["this; they", "those; it"]),
        ]) +
        '<div class="note-panel"><div class="np-title">精讲要点</div>① 动词/介词后用宾格（help me）；② 空后无名词用名词性物主代词；③ 复数呼应：these/those + they。<b>G02 物主代词为 Top3 高频错题。</b></div>')
    add(g_pron, 2, "代词类 G01/G02/G04", "主格/宾格 · 物主 · 指示", minutes=8)

    # P6 be动词类
    g_be = (section_head("法", "语法错题精讲 · be动词类 G03/G05") +
        '<div class="formula-box"><div class="formula-text">I am, You are, He/She/It is; They/We are</div>' +
        '<div class="formula-sub">G03 be 动词与人称代词主格搭配 · G05 be 动词否定句与一般疑问句</div></div>' +
        '<div class="grid-2">' +
        '<div class="rule-card rc-zhug"><strong>🔑 G03 be 搭配口诀</strong><br>I → am（唯一搭配）<br>He/She/It → is（三单用 is）<br>You/We/They → are<br>❌ He are → ✅ He is<br><em>并列看总数：Tom and I = are</em></div>' +
        '<div class="rule-card rc-bin"><strong>🔑 G05 be 否定与疑问</strong><br>否定：be + not<br>疑问：be 提前 → Is she...?<br>回答：Yes, 主格 + be.<br>❌ Does she is? → ✅ Is she?<br><em>be 句型不借 do/does!</em></div>' +
        '</div>' +
        '<div class="compare-box">' +
        '<div class="compare-side compare-wrong"><div class="compare-label">❌ 常见错误</div>My brother and I <b>is</b> students.<br><b>Does</b> she your teacher?<br>They <b>isn&#39;t</b> my friends.</div>' +
        '<div class="compare-side compare-correct"><div class="compare-label">✅ 正确写法</div>My brother and I <b>are</b> students.<br><b>Is</b> she your teacher?<br>They <b>aren&#39;t</b> my friends.</div>' +
        '</div>' +
        quiz_html([
            ("【第49题·G03】My brother and I ___ students.（我弟弟和我是学生。）", "are", ["is", "am"]),
            ("【第51题·G05】- ___ your father a teacher? - Yes, ___.（你爸爸是老师吗？是的，他是。）", "Is; he is", ["Are; he is", "Does; he does"]),
            ("【变式题·G05】They ___ not my classmates. They ___ in Class 2.（他们不是我的同班同学。他们在二班。）", "are; are", ["are; is", "is; are"]),
        ]) +
        '<div class="note-panel"><div class="np-title">精讲要点</div>并列主语（and 连接）为复数用 are；be 动词句否定/疑问直接用 be，不借助 do/does；简答用主格 + be。</div>')
    add(g_be, 2, "be动词类 G03/G05", "be 搭配 · 否定/疑问", minutes=8)

    # P7 疑问句类
    g_wh = (section_head("法", "语法错题精讲 · 疑问句类 G06/G09/G14") +
        '<div class="formula-box"><div class="formula-text">Who 问人，Where 问地点，What 问事物</div>' +
        '<div class="formula-sub">G06 Who 疑问句 · G09 Where + There be · G14 What 疑问句</div></div>' +
        '<div class="grid-3">' +
        '<div class="rule-card rc-zhug"><strong>🔑 G06 Who</strong><br>Who is that girl? → She is my cousin.<br>Who are they? → They are my friends.<br><em>回答用 He/She/They</em></div>' +
        '<div class="rule-card rc-bin"><strong>🔑 G09 Where + There be</strong><br>Where is the book? → It&#39;s on the desk.<br>There is/are... 某处有某物<br><em>is 配单数，are 配复数</em></div>' +
        '<div class="rule-card rc-xing"><strong>🔑 G14 What</strong><br>What is this? → It&#39;s a dictionary.<br>What are those? → They are tomatoes.<br><em>单数用 it，复数用 they</em></div>' +
        '</div>' +
        '<div class="gpoint-detail"><div class="gpoint-header"><span class="gpoint-title">📋 疑问句回答规范</span><span class="gpoint-tag">重要</span></div>' +
        '<div class="gpoint-body"><strong>Who 问人 → 用人名/身份回答：</strong>Who is he? → He is Tom.<br>' +
        '<strong>Where 问地点 → 用方位介词短语回答：</strong>Where is it? → It&#39;s on/in/under...<br>' +
        '<strong>What 问事物 → 用事物名称回答：</strong>What is this? → It&#39;s a pen.<br>' +
        '<span class="wrong-ex">⚠️ 常见错误：回答不完整，如 Who is he? 只回答 &#34;Tom&#34; 而非 &#34;He is Tom.&#34;</span></div></div>' +
        quiz_html([
            ("【第52题·G06】- ___ is that boy over there? - He is my cousin, Tom.（那边那个男孩是谁？）", "Who", ["What", "Where"]),
            ("【第55题·G09+G12】- Where ___ the strawberries? - ___ are on the table.（草莓在哪里？它们在桌上。）", "are; They", ["is; They", "are; It"]),
        ]) +
        '<div class="note-panel"><div class="np-title">精讲要点</div>疑问词按回答选（问人 Who / 问地 Where / 问物 What）；复数名词用 are + They 回答。<b>第55题错误率 72%，Top1。</b></div>')
    add(g_wh, 2, "疑问句类 G06/G09/G14", "Who/Where/What", minutes=8)

    # P8 名词类
    g_noun = (section_head("法", "语法错题精讲 · 名词类 G07/G10/G17") +
        '<div class="formula-box"><div class="formula-text">所有格加 &#39;s，复数加 s/es；可数能数，不可数不能数</div>' +
        '<div class="formula-sub">G07 名词所有格 · G10 可数名词规则复数 · G17 可数与不可数名词分类</div></div>' +
        '<div class="grid-3">' +
        '<div class="rule-card rc-zhug"><strong>🔑 G07 名词所有格</strong><br>单数加 &#39;s：Tom&#39;s book<br>复数加 &#39;：students&#39; room<br>不规则加 &#39;s：children&#39;s toys<br>of 结构：the door of the room<br><em>有生命 → &#39;s；无生命 → of</em></div>' +
        '<div class="rule-card rc-bin"><strong>🔑 G10 规则复数</strong><br>一般加 -s：book→books<br>s/x/sh/ch 加 -es：box→boxes<br>辅音+y 变 ies：family→families<br>o 结尾：tomato→tomatoes<br><em>❌ tomatos → ✅ tomatoes</em></div>' +
        '<div class="rule-card rc-xing"><strong>🔑 G17 可数 vs 不可数</strong><br>可数：apple/schoolbag<br>不可数：milk/bread/rice/water<br>不可数不能加 s，谓语用 is<br><em>❌ milks → ✅ milk</em></div>' +
        '</div>' +
        '<div class="compare-box">' +
        '<div class="compare-side compare-wrong"><div class="compare-label">❌ 常见错误</div>This is <b>Toms</b> room.<br>I have two <b>boxs</b>.<br>There is some <b>milks</b>.</div>' +
        '<div class="compare-side compare-correct"><div class="compare-label">✅ 正确写法</div>This is <b>Tom&#39;s</b> room.<br>I have two <b>boxes</b>.<br>There is some <b>milk</b>.</div>' +
        '</div>' +
        quiz_html([
            ("【第53题·G07】This is ___ room. It&#39;s very tidy.（这是Tom的房间，非常整洁。）", "Tom's", ["Toms", "Toms'"]),
            ("【第56题·G10/G17综合】There ___ some ___ on the table.（桌上有一些牛奶和面包。）", "is; milk and bread", ["are; milk and bread", "is; milks and breads"]),
            ("【变式题·G10】I have two ___ and three ___ in my room.（我房间有两个盒子和三个书架。）", "boxes; bookcases", ["boxs; bookcases", "boxes; bookcase"]),
        ]) +
        '<div class="note-panel"><div class="np-title">精讲要点</div>名词类三大失分点：所有格撇号位置、规则复数词尾、不可数加 s。<b>G07/G10/G17 均为 C 级，需专项巩固。</b></div>')
    add(g_noun, 2, "名词类 G07/G10/G17", "所有格 · 复数 · 不可数", minutes=8)

    # P9 介词类 G12
    g_prep = (section_head("法", "语法错题精讲 · 介词类 G12") +
        '<div class="formula-box"><div class="formula-text">in 里面，on 上面，under 下面；behind 后面，next to 旁边，between...and... 中间</div>' +
        '<div class="formula-sub">G12 方位介词短语扩展</div></div>' +
        '<div class="card"><div class="card-title">🧭 方位介词矩阵</div>' +
        '<div class="grid-3">' +
        '<div class="rule-card rc-zhug" style="text-align:center;"><strong>in</strong><br>在...里面<br><em>in the room</em></div>' +
        '<div class="rule-card rc-bin" style="text-align:center;"><strong>on</strong><br>在...上面<br><em>on the desk</em></div>' +
        '<div class="rule-card rc-xing" style="text-align:center;"><strong>under</strong><br>在...下面<br><em>under the bed</em></div>' +
        '<div class="rule-card rc-ming" style="text-align:center;"><strong>behind</strong><br>在...后面<br><em>behind the door</em></div>' +
        '<div class="rule-card rc-warn" style="text-align:center;"><strong>next to</strong><br>在...旁边<br><em>next to the sofa</em></div>' +
        '<div class="rule-card rc-qita" style="text-align:center;"><strong>between A and B</strong><br>在A和B之间<br><em>between the bed and the desk</em></div>' +
        '</div></div>' +
        '<div class="gpoint-detail"><div class="gpoint-header"><span class="gpoint-title">⚠️ G12 高频易错点</span><span class="gpoint-tag">错误率 72%</span></div>' +
        '<div class="gpoint-body"><strong>1 between...and... 结构：</strong>必须搭配 and，不能换成 or。<br>' +
        '<span class="wrong-ex">between the desk or the chair</span> → <span class="correct-ex">between the desk and the chair</span><br>' +
        '<strong>2 next to vs near：</strong>next to = 紧挨着（距离最近）。<br>' +
        '<strong>3 behind vs after：</strong>behind 表空间，after 表时间。<br>' +
        '<strong>4 in vs on vs under：</strong>in 内部，on 表面接触，under 正下方。</div></div>' +
        quiz_html([
            ("【第55题·G12】The schoolbag is ___ the desk ___ the chair.（书包在桌子和椅子之间。）", "between; and", ["next to; and", "behind; and"]),
            ("【变式题·G12】Look! The cat is ___ the sofa. I can&#39;t see it.（猫在沙发后面，我看不到它。）", "behind", ["on", "in"]),
        ]) +
        '<div class="tip-box"><strong>📌 记忆口诀：</strong>“in 里 on 上 under 下，behind 后面 next to 旁，between...and... 夹中间，方位介词要记牢！”</div>')
    add(g_prep, 2, "介词类 G12", "方位介词 · 重点巩固", minutes=8)

    # P10 祈使句类 G13
    g_imp = (section_head("法", "语法错题精讲 · 祈使句类 G13") +
        '<div class="formula-box"><div class="formula-text">Do 做肯定祈使，Don&#39;t 做否定祈使；动词原形开头，主语 you 省略</div>' +
        '<div class="formula-sub">G13 Do / Don&#39;t 祈使句</div></div>' +
        '<div class="grid-2">' +
        '<div class="rule-card rc-zhug"><strong>🔑 肯定祈使句</strong><br>结构：动词原形 + 其他<br>Open the door.（开门）<br>Please sit down.（请坐）<br>Come here, please.<br><em>please 可加句首或句末</em></div>' +
        '<div class="rule-card rc-warn"><strong>🔑 否定祈使句</strong><br>结构：Don&#39;t + 动词原形<br>Don&#39;t be late.<br>Don&#39;t open the window.<br>❌ Doesn&#39;t open → ✅ Don&#39;t open<br><em>否定只用 Don&#39;t，不用 Doesn&#39;t</em></div>' +
        '</div>' +
        '<div class="compare-box">' +
        '<div class="compare-side compare-wrong"><div class="compare-label">❌ 常见错误</div><b>Not</b> play in the classroom!<br><b>Doesn&#39;t</b> open the door.<br><b>You open</b> the book, please.</div>' +
        '<div class="compare-side compare-correct"><div class="compare-label">✅ 正确写法</div><b>Don&#39;t</b> play in the classroom!<br><b>Don&#39;t</b> open the door.<br><b>Open</b> the book, please.（省略 you）</div>' +
        '</div>' +
        quiz_html([
            ("【第56题·G13】___ play soccer in the classroom!（不要在教室里踢足球！）", "Don't", ["Not", "Doesn't"]),
            ("【变式题·G13】___ quiet, please. The baby is sleeping.（请安静，宝宝在睡觉。）", "Be", ["Are", "Is"]),
        ]) +
        '<div class="tip-box"><strong>📌 记忆口诀：</strong>“祈使句，无主语，动词原形就可以；要否定，Don&#39;t 加，只用 Don&#39;t 不用别的！”</div>')
    add(g_imp, 2, "祈使句类 G13", "Do / Don't 祈使", minutes=7)

    # P11 动词搭配类 G15/G18
    g_verb = (section_head("法", "语法错题精讲 · 动词搭配类 G15/G18") +
        '<div class="formula-box"><div class="formula-text">like + 名词（复数）/ like to do（喜欢做）；want to do sth.（想要做某事）</div>' +
        '<div class="formula-sub">G15 like + 名词复数 / like to do · G18 want to do sth.</div></div>' +
        '<div class="grid-2">' +
        '<div class="rule-card rc-zhug"><strong>🔑 G15 like 用法</strong><br>like + 名词：I like apples.<br>like + 名词复数：She likes tomatoes.<br>like to do：They like to play basketball.<br>❌ like apple → ✅ like apples<br><em>运动名称不加复数：like basketball</em></div>' +
        '<div class="rule-card rc-bin"><strong>🔑 G18 want to do</strong><br>want to + 动词原形：I want to eat.<br>want + 名词：I want an apple.<br>❌ want eat → ✅ want to eat<br>❌ want to eating → ✅ want to eat<br><em>want to be = 想成为</em></div>' +
        '</div>' +
        '<div class="gpoint-detail"><div class="gpoint-header"><span class="gpoint-title">🔄 G15 → G18 螺旋链</span><span class="gpoint-tag">螺旋递进</span></div>' +
        '<div class="gpoint-body"><strong>L5 G15：</strong>like + 名词复数 / like to do（首次接触 to do）<br>' +
        '<strong>L6 G18：</strong>want to do sth.（巩固 to do 结构）<br>' +
        '<strong>本课诊断：</strong>like to do + want to do 综合考查<br>' +
        '<em>核心记忆：to + 动词原形 = “要做”某事，to 不能省略，后面跟原形不能加 -ing。</em></div></div>' +
        quiz_html([
            ("【第56题·G15/G18】My sister likes ___ and she wants ___ a volleyball player.（我姐姐喜欢排球，她想当排球运动员。）", "volleyball; to be", ["volleyball; be", "volleyballs; be"]),
            ("【变式题·G15/G18】We like ___ fruit, but we don&#39;t like ___ ice-cream.（我们喜欢水果，但不喜欢冰淇淋。）", "to eat; to eat", ["eat; eat", "eating; eating"]),
            ("【变式题·G15/G18】Tom ___ bananas, but he ___ strawberries.（Tom 喜欢香蕉，但不喜欢草莓。）", "likes; doesn't like", ["like; don't like", "likes; don't like"]),
        ]) +
        '<div class="note-panel"><div class="np-title">精讲要点</div>like + 事物用复数名词，like + 行为用 to do；want 后接事物用名词，接行为用 to do。<b>三单 likes/doesn&#39;t 此处仅诊断预警，L10 正式学。</b></div>')
    add(g_verb, 2, "动词搭配类 G15/G18", "like / want to do", minutes=8)

    # P12 时态类 G16
    g_ts = (section_head("法", "语法错题精讲 · 时态类 G16") +
        '<div class="formula-box"><div class="formula-text">一般现在时，非三单用原形；否定 don&#39;t 加原形；三单留至 L10</div>' +
        '<div class="formula-sub">G16 一般现在时非三单肯定与 don&#39;t 否定</div></div>' +
        '<div class="grid-2">' +
        '<div class="rule-card rc-zhug"><strong>🔑 肯定句（非三单）</strong><br>I/You/We/They + 动词原形<br>I play basketball every day.<br>They watch TV on weekends.<br><em>频率副词放动词前：I always eat breakfast.</em></div>' +
        '<div class="rule-card rc-warn"><strong>🔑 否定句（非三单）</strong><br>I/You/We/They + don&#39;t + 动词原形<br>I don&#39;t play soccer.<br>They don&#39;t watch TV.<br>❌ They doesn&#39;t → ✅ They don&#39;t<br><em>don&#39;t = do not，后接原形</em></div>' +
        '</div>' +
        '<div class="gpoint-detail"><div class="gpoint-header"><span class="gpoint-title">⚠️ 防越级边界</span><span class="gpoint-tag">重要</span></div>' +
        '<div class="gpoint-body"><strong>Stage 2 只学：</strong>I/You/We/They + 动词原形（非三单）<br>' +
        '<strong>L10 才学：</strong>He/She/It + 动词 -s/es（三单变化）<br>' +
        '<strong>本课诊断</strong>中 he/she 做主语时用 be 动词搭配（is），不用行为动词三单形式。<br>' +
        '<em>第 56 题综合题中 He likes / He wants to 仅作诊断预警，正式教学在 L10。</em></div></div>' +
        quiz_html([
            ("【第56题·G16】We ___ TV every evening. We ___ TV in the morning.（我们晚上看电视。我们早上不看电视。）", "watch; don't watch", ["watch; don't", "watches; don't"]),
            ("【变式题·G16】They ___ soccer after school, but they ___ basketball.（他们放学后踢足球，但不打篮球。）", "play; don't play", ["play; don't play", "plays; don't play"]),
        ]) +
        '<div class="tip-box"><strong>📌 口诀：</strong>“I/You/We/They 加原形，否定 don&#39;t 跟原形；三单变化留 L10，现在只考非三单！”</div>')
    add(g_ts, 2, "时态类 G16", "非三单 · don't 否定", minutes=7)

    # P13 数词类 G08
    g_num = (section_head("法", "语法错题精讲 · 数词类 G08") +
        '<div class="formula-box"><div class="formula-text">1-12 独立记，13-19 都加 -teen；20/30/40/50 整十加 -ty，连字符连接几十几</div>' +
        '<div class="formula-sub">G08 基数词 1-100 拼写与修饰名词</div></div>' +
        '<div class="grid-2">' +
        '<div class="rule-card rc-zhug"><strong>🔑 1-20 拼写</strong><br>one two three four five six seven eight nine ten<br>eleven twelve thirteen fourteen fifteen<br>sixteen seventeen eighteen nineteen twenty<br>❌ fiveteen → ✅ fifteen<br><em>特殊拼写：fifteen、eighteen</em></div>' +
        '<div class="rule-card rc-bin"><strong>🔑 整十与几十几</strong><br>20 twenty, 30 thirty, 40 forty, 50 fifty<br>21 twenty-one, 35 thirty-five（连字符！）<br>❌ twenty one → ✅ twenty-one<br>❌ fourty → ✅ forty<br><em>注意：forty 没有 u！</em></div>' +
        '</div>' +
        '<div class="gpoint-detail"><div class="gpoint-header"><span class="gpoint-title">📞 数词的实际应用场景</span><span class="gpoint-tag">应用</span></div>' +
        '<div class="gpoint-body"><strong>1 电话号码：</strong>逐位读，287-5926 → two eight seven, five nine two six<br>' +
        '<strong>2 年龄：</strong>按数值读，13 → thirteen<br>' +
        '<strong>3 数量：</strong>修饰名词，three apples, twenty students<br>' +
        '<strong>4 考试得分：</strong>按数值读，95 → ninety-five<br>' +
        '<em>规则总结：号码类逐位读，数量/年龄按数值读。</em></div></div>' +
        quiz_html([
            ("【第54题·G08】- How old is your sister? - She is ___.（你妹妹多大了？她十三岁了。）", "thirteen", ["one three", "thirteenth"]),
            ("【变式题·G08】There are ___ students in our class. Twenty ___ and sixteen girls.（我们班有36人，20男16女。）", "thirty-six; boys", ["thirty-six; boy", "thirtysix; boys"]),
            ("【变式题·G08】My phone number is 555-2871. 请选出正确读法：", "five five five, two eight seven one", ["five hundred fifty-five, two thousand eight hundred seventy-one", "fifty-five, twenty-eight seventy-one"]),
        ]) +
        '<div class="card"><div class="card-title">📋 基数词易错拼写对照表</div>' +
        '<table class="error-table"><thead><tr><th>数字</th><th>正确</th><th>常见错误</th><th>记忆法</th></tr></thead><tbody>' +
        '<tr><td>13</td><td>thirteen</td><td>thriteen</td><td>three → thirteen</td></tr>' +
        '<tr><td>15</td><td>fifteen</td><td>fiveteen</td><td>ve 变 f</td></tr>' +
        '<tr><td>18</td><td>eighteen</td><td>eightteen</td><td>只一个 t</td></tr>' +
        '<tr><td>40</td><td>forty</td><td>fourty</td><td>去掉 u!</td></tr>' +
        '<tr><td>21</td><td>twenty-one</td><td>twentyone</td><td>必须有连字符!</td></tr>' +
        '</tbody></table></div>' +
        '<div class="tip-box"><strong>📌 重点提醒：</strong>号码/房间号逐位读；年龄/数量按数值读；注意 forty（非 fourty）和 fifteen（非 fiveteen）。</div>')
    add(g_num, 2, "数词类 G08", "基数词 1-100", minutes=7)

    # P14 综合错题 G10-G18
    g_comp = (section_head("法", "语法错题精讲 · 综合错题（跨考点）") +
        '<div class="body-text"><span class="highlight">第56题 · G10-G18 综合诊断短文</span>：阅读短文，选出最佳选项填空。综合诊断 G10-G18 全部 9 个考点。</div>' +
        '<div class="card"><div class="card-title">🔬 综合诊断短文</div>' +
        '<div class="body-text">My friend Tom <b>___1__</b> (like) sports. He <b>___2__</b> (want) to be a soccer player. He has two <b>___3__</b> (soccer ball). They are under his bed. &#34;Don&#39;t <b>___4__</b> (be) late for the match!&#34; his mother says. Tom and his team <b>___5__</b> (not/watch) TV before a match. They eat healthy food - <b>___6__</b> (strawberry) and <b>___7__</b> (milk) every morning. Tom&#39;s room is very <b>___8__</b> (tidy). His books are <b>___9__</b> (介词) the desk and the chair.</div></div>' +
        quiz_html([
            ("1.（G15 like用法）Tom ___ sports.", "likes", ["like", "liking"]),
            ("2.（G18 want to do）He ___ be a soccer player.", "wants to", ["want", "want to"]),
            ("3.（G10 复数）He has two ___.", "soccer balls", ["soccer ball", "soccer balles"]),
            ("4.（G13 祈使句）Don't ___ late for the match!", "be", ["is", "are"]),
            ("5.（G16 非三单否定）Tom and his team ___ TV before a match.", "don't watch", ["doesn't watch", "don't watching"]),
            ("6.（G10/G17 复数陷阱）They eat ___ every morning.", "strawberries", ["strawberry", "strawberryies"]),
            ("7.（G17 不可数名词）and ___ every morning.", "milk", ["milks", "milkies"]),
            ("8.（G11 形容词）Tom's room is very ___.", "tidy(表语)", ["tidy(定语)", "tidies"]),
            ("9.（G12 方位介词）His books are ___ the desk and the chair.", "between", ["on", "behind"]),
        ]) +
        '<div class="note-panel"><div class="np-title">精讲要点</div>综合题错误率 68%，Top2。①②③ 涉及三单/want to do 仅诊断预警；④ 祈使句 Don&#39;t + 原形；⑤ 复数主语用 don&#39;t；⑥⑦ 不可数与复数陷阱；⑧ 形容词做表语；⑨ between...and。</div>')
    add(g_comp, 2, "综合错题 G10-G18", "跨考点诊断", minutes=9)

    # ---- 段3 词汇错题精讲（5 页） ----
    # P15 L1+L2
    v_l12 = (section_head("词", "词汇错题精讲 · L1 + L2 组") +
        '<div class="formula-box"><div class="formula-text">theirs/yours/mine = 形容词性物主 + s；this/that 单数，these/those 复数</div>' +
        '<div class="formula-sub">L1 问候·交友·个人信息 | L2 家庭·指示代词</div></div>' +
        '<div class="grid-2">' +
        '<div class="vocab-card"><div class="vocab-word">theirs /ðɛərz/</div><div class="vocab-meaning">pron. 他们的（名词性物主代词）</div><div class="vocab-tip">⚠️ their + s = theirs，无撇号</div></div>' +
        '<div class="vocab-card"><div class="vocab-word">yours /jɔːrz/</div><div class="vocab-meaning">pron. 你的/你们的（名词性物主代词）</div><div class="vocab-tip">⚠️ your + s = yours，无撇号</div></div>' +
        '<div class="vocab-card"><div class="vocab-word">these /ðiːz/</div><div class="vocab-meaning">pron. 这些（this 的复数）</div><div class="vocab-tip">⚠️ 咬舌音 /ð/，近处复数</div></div>' +
        '<div class="vocab-card"><div class="vocab-word">those /ðoʊz/</div><div class="vocab-meaning">pron. 那些（that 的复数）</div><div class="vocab-tip">⚠️ 咬舌音 /ð/，远处复数</div></div>' +
        '</div>' +
        '<div class="gpoint-detail"><div class="gpoint-header"><span class="gpoint-title">📋 名词性物主代词全表</span><span class="gpoint-tag">G02 核心</span></div>' +
        '<div class="gpoint-body"><strong>形容词性 → 名词性对照：</strong><br>my → mine | your → yours | his → his | her → hers | our → ours | their → theirs<br>' +
        '<strong>记忆法：</strong>除 his 不变外，其余都是“形容词性 + s”。<br>' +
        '<span class="wrong-ex">❌ This is mine book.（mine 后不能再接名词）</span></div></div>' +
        quiz_html([
            ("【词汇诊断】- Whose ruler is this? - It's not mine. It's ___.（不是我的，是他们的。）", "theirs", ["their", "their's"]),
            ("【词汇诊断】- Are ___ your parents? - Yes, ___ are my parents. They are ___.", "those; they; mine", ["these; it; my", "those; they; my"]),
        ]) +
        '<div class="note-panel"><div class="np-title">精讲要点</div>空后无名词 → 用名词性物主代词；名词性物主代词不加撇号。<b>G02 物主代词为 Top3 高频错题。</b></div>')
    add(v_l12, 3, "词汇 L1+L2 组", "物主 · 指示", minutes=7)

    # P16 L3+L4
    v_l34 = (section_head("词", "词汇错题精讲 · L3 + L4 组") +
        '<div class="formula-box"><div class="formula-text">复合词拆分记：school+bag=schoolbag；everywhere=every+where；between=be+tween</div>' +
        '<div class="formula-sub">L3 文具·失物招领 | L4 房间·家具·方位</div></div>' +
        '<div class="grid-2">' +
        '<div class="vocab-card"><div class="vocab-word">dictionary /ˈdɪkʃənɛri/</div><div class="vocab-meaning">n. 词典</div><div class="vocab-tip">🔧 拆分：dict+ion+ary；复数 dictionaries</div></div>' +
        '<div class="vocab-card"><div class="vocab-word">schoolbag /ˈskuːlbæɡ/</div><div class="vocab-meaning">n. 书包</div><div class="vocab-tip">🔧 复合词：school+bag 一个词</div></div>' +
        '<div class="vocab-card"><div class="vocab-word">everywhere /ˈɛvriwɛər/</div><div class="vocab-meaning">adv. 到处；处处</div><div class="vocab-tip">🔧 every+where；Your books are everywhere!</div></div>' +
        '<div class="vocab-card"><div class="vocab-word">between /bɪˈtwiːn/</div><div class="vocab-meaning">prep. 在...之间</div><div class="vocab-tip">⚠️ 固定搭配 between A and B（不用 or&nbsp;）</div></div>' +
        '</div>' +
        '<div class="card"><div class="card-title">🔧 复合词拆分法详解</div>' +
        '<div class="rule-card rc-zhug"><strong>名词 + 名词 = 复合名词：</strong>school+bag=schoolbag | class+room=classroom | note+book=notebook<br>' +
        '<strong>代词 + 副词 = 复合副词：</strong>every+where=everywhere | every+one=everyone</div>' +
        '<div class="tip-box"><strong>解题技巧：</strong>遇到长词先拆——schoolbag = school + bag。拆完各部分含义相加即可猜出整词意思。</div></div>' +
        quiz_html([
            ("【词汇诊断】I can't find my ___. It's not in my ___.（我找不到词典了，它不在书包里。）", "dictionary; schoolbag", ["dictionary; school bag", "dictionarys; schoolbag"]),
        ]) +
        '<div class="note-panel"><div class="np-title">精讲要点</div>schoolbag 是一个词（不分开写）；dictionary 复数为 dictionaries（辅音+y 变 ies）。</div>')
    add(v_l34, 3, "词汇 L3+L4 组", "复合词 · 文具方位", minutes=7)

    # P17 L5
    v_l5 = (section_head("词", "词汇错题精讲 · L5 组") +
        '<div class="formula-box"><div class="formula-text">-ing 形容词描述事物特征：relaxing/boring/interesting；主语是事物 → -ing</div>' +
        '<div class="formula-sub">L5 运动·喜好表达 - -ing 形容词辨析</div></div>' +
        '<div class="grid-3">' +
        '<div class="vocab-card"><div class="vocab-word">relaxing</div><div class="vocab-meaning">adj. 令人放松的</div><div class="vocab-tip">✅ The game is relaxing.<br>≠ relaxed（人感到放松）</div></div>' +
        '<div class="vocab-card"><div class="vocab-word">boring</div><div class="vocab-meaning">adj. 令人无聊的</div><div class="vocab-tip">✅ The movie is boring.<br>≠ bored（人感到无聊）</div></div>' +
        '<div class="vocab-card"><div class="vocab-word">interesting</div><div class="vocab-meaning">adj. 有趣的</div><div class="vocab-tip">✅ The book is interesting.<br>≠ interested（人感兴趣）</div></div>' +
        '</div>' +
        '<div class="gpoint-detail"><div class="gpoint-header"><span class="gpoint-title">⚠️ fun vs funny 辨析</span><span class="gpoint-tag">易混</span></div>' +
        '<div class="gpoint-body"><strong>fun</strong> = 有趣、好玩（享受）<span class="correct-ex">Playing basketball is fun.</span><br>' +
        '<strong>funny</strong> = 滑稽、好笑（搞笑）<span class="correct-ex">The clown is funny.</span><br>' +
        '<span class="wrong-ex">The game is funny.（错误：游戏有趣应说 fun）</span></div></div>' +
        quiz_html([
            ("【词汇诊断】I don't like this movie. It is ___.（我不喜欢这部电影，它很无聊。）", "boring", ["relaxing", "interesting"]),
            ("【变式题】Playing volleyball with friends is ___. We all enjoy it.（和朋友打排球很有趣。）", "relaxing", ["boring", "difficult"]),
        ]) +
        '<div class="note-panel"><div class="np-title">精讲要点</div>-ing 形容词描述事物特征（令人...）；主语的感受用 -ed（L 后续学）。字面线索：don&#39;t like → 负面 → boring；enjoy → 正面 → relaxing。</div>')
    add(v_l5, 3, "词汇 L5 组", "-ing 形容词", minutes=7)

    # P18 L6
    v_l6 = (section_head("词", "词汇错题精讲 · L6 组") +
        '<div class="formula-box"><div class="formula-text">o 结尾名词复数：多数加 -s，少数加 -es；strawberry→strawberries, tomato→tomatoes</div>' +
        '<div class="formula-sub">L6 食物·健康饮食 - 复数陷阱 + 不可数名词</div></div>' +
        '<div class="grid-2">' +
        '<div class="card"><div class="card-title">🍅 o 结尾名词复数陷阱</div>' +
        '<div class="rule-card rc-warn"><strong>加 -es 的（必须死记）：</strong>tomato → tomatoes<br>potato → potatoes<br><em>口诀：“两个土豆两个西红柿，加 es 不加 s”</em></div>' +
        '<div class="rule-card rc-zhug"><strong>加 -s 的（大多数）：</strong>photo → photos<br>piano → pianos<br>radio → radios<br><em>元音+o 结尾加 -s</em></div>' +
        '<div class="rule-card rc-qita"><strong>y 结尾变 ies：</strong>strawberry → strawberries<br>family → families<br><em>辅音+y → 变 y 为 i 加 es</em></div></div>' +
        '<div class="card"><div class="card-title">🥛 不可数名词（不能加 s）</div>' +
        '<div class="rule-card rc-ming">milk 牛奶 / bread 面包 / rice 米饭 / water 水 / food 食物 / fruit 水果<br><em>不可数 = 用 is，不用 are；不加 s；some + 不可数</em></div>' +
        '<div class="tip-box"><strong>📝 记忆法：</strong>液体（milk/water）、粉末（rice）、无法数清的（bread/food）→ 不可数。</div></div>' +
        '</div>' +
        quiz_html([
            ("【词汇诊断】I'd like some ___ and ___ for breakfast.（我早饭想吃些西红柿和面包。）", "tomatoes; bread", ["tomatos; breads", "tomatoes; breads"]),
            ("【变式题】There are some ___ and ___ on the table.（桌上有一些草莓和牛奶。）", "strawberries; milk", ["strawberry; milk", "strawberries; milks"]),
        ]) +
        '<div class="note-panel"><div class="np-title">精讲要点</div>o 结尾少数加 -es（tomato/potato）；不可数不加 s。<b>L6 词汇掌握率 55%，重点巩固。</b></div>')
    add(v_l6, 3, "词汇 L6 组", "复数陷阱 · 不可数", minutes=7)

    # P19 词汇策略总结
    v_strat = (section_head("词", "词汇错题精讲 · 词汇策略总结") +
        '<div class="grid-3">' +
        '<div class="card" style="border-top:4px solid var(--brand);"><div class="card-title">1 🔧 复合词拆分法</div><div class="card-content">遇到长词先拆分：school+bag=schoolbag｜every+where=everywhere｜every+one=everyone｜note+book=notebook<br><span class="highlight">口诀：</span>“长词不要怕，拆开看看它！”</div></div>' +
        '<div class="card" style="border-top:4px solid var(--accent);"><div class="card-title">2 🔍 语境推断法</div><div class="card-content">通过上下文猜词义：同义/反义（but/or）、定义（is/means）、举例（like/such as）、因果（because/so）。<br><em>The food is delicious, so I eat a lot. → delicious = 好吃的</em></div></div>' +
        '<div class="card" style="border-top:4px solid var(--sop-purple);"><div class="card-title">3 📖 猜词法</div><div class="card-content">不影响答题的生词 → 跳过；影响理解的 → 语境推断；关键位置的 → 词缀/词根分析。<br><em>中考允许 15%-20% 生词。</em></div></div>' +
        '</div>' +
        '<div class="card"><div class="card-title">📊 词汇诊断总结 · L1-L6 掌握度</div>' +
        '<div class="grid-4">' +
        '<div class="rule-card rc-zhug" style="text-align:center;"><strong>L1</strong><br>78%<br><span class="grade-tag grade-a">A</span> 进入Stage3</div>' +
        '<div class="rule-card rc-bin" style="text-align:center;"><strong>L2</strong><br>72%<br><span class="grade-tag grade-b">B</span> 少量巩固</div>' +
        '<div class="rule-card rc-xing" style="text-align:center;"><strong>L3</strong><br>65%<br><span class="grade-tag grade-b">B</span> 补充变式</div>' +
        '<div class="rule-card rc-ming" style="text-align:center;"><strong>L4</strong><br>60%<br><span class="grade-tag grade-c">C</span> 专项巩固</div>' +
        '<div class="rule-card rc-warn" style="text-align:center;"><strong>L5</strong><br>70%<br><span class="grade-tag grade-b">B</span> 少量巩固</div>' +
        '<div class="rule-card rc-qita" style="text-align:center;"><strong>L6</strong><br>55%<br><span class="grade-tag grade-c">C</span> 重点巩固</div>' +
        '</div>' +
        '<div class="tip-box"><strong>📌 重点巩固：</strong>L4（方位词汇 everywhere/between）和 L6（食物复数 strawberry/tomato/potato + 不可数 milk/bread）掌握率偏低，建议每天抄写 10 个易错词并造句。</div></div>' +
        '<div class="card"><div class="card-title">🔧 词汇记忆方法总结</div>' +
        '<div class="rule-card rc-zhug"><strong>1 分类记忆法：</strong>按主题分组记（食物/文具/家具/运动），每组 20 词关联记忆。</div>' +
        '<div class="rule-card rc-bin"><strong>2 词根词缀法：</strong>-er 表人/物（teacher/eraser）；-tion 表名词。拆词根：dict+ion+ary=dictionary。</div>' +
        '<div class="rule-card rc-xing"><strong>3 语境记忆法：</strong>不孤立背词，放入句子中记（The milk is on the table.）。</div>' +
        '<div class="rule-card rc-ming"><strong>4 联想记忆法：</strong>strawberry = straw(稻草)+berry(浆果)；basketball = basket+ball。</div>' +
        '</div>')
    add(v_strat, 3, "词汇策略总结", "L1-L6 掌握度 · 记忆法", minutes=6)

    # ---- 段4 阅读写作讲评（5 页） ----
    # P20 阅读A篇
    r_a = (section_head("读", "阅读与写作讲评 · 阅读A篇") +
        '<div class="card"><div class="card-title">📄 阅读 A 篇 · 应用文信息定位法</div>' +
        '<div class="rule-card rc-zhug"><strong>文章主题：</strong>A Student Information Card（学生信息卡）—— 86 词，应用文<br>' +
        '<strong>考点覆盖：</strong>G06 Who 提问、G08 基数词、G14 What 提问、G07 所有格<br>' +
        '<strong>全班得分率：</strong>78%（最高分题型）</div></div>' +
        '<div class="card"><div class="card-title">🎯 应用文信息定位法 · 三步解题</div>' +
        '<div class="grid-3">' +
        '<div class="rule-card rc-zhug" style="text-align:center;"><strong>Step 1</strong><br>读题干<br>划出关键词<br>（人名/数字/疑问词）</div>' +
        '<div class="rule-card rc-bin" style="text-align:center;"><strong>Step 2</strong><br>回原文<br>定位对应区域<br>（信息卡/表格）</div>' +
        '<div class="rule-card rc-xing" style="text-align:center;"><strong>Step 3</strong><br>对比选项<br>选最优答案<br>排除干扰项</div>' +
        '</div></div>' +
        '<div class="gpoint-detail"><div class="gpoint-header"><span class="gpoint-title">📖 信息卡内容预览</span><span class="gpoint-tag">背景</span></div>' +
        '<div class="gpoint-body"><strong>Name:</strong> Li Ming ｜ <strong>Age:</strong> 13 ｜ <strong>Phone:</strong> 287-5962<br>' +
        '<strong>School:</strong> No. 1 Middle School ｜ <strong>Class:</strong> Class 3, Grade 7<br>' +
        '<strong>Family:</strong> Father (teacher), Mother (teacher), Sister (student)<br>' +
        '<strong>Favorite food:</strong> Apples, milk</div></div>' +
        quiz_html([
            ("【阅读A篇·第1题】Who is the information card about?（信息卡是关于谁的？）", "Li Ming", ["Tom Smith", "Wang Fang"]),
            ("【阅读A篇·第3题·G08】What is Li Ming's phone number?（李明的电话号码是多少？）", "287-5962", ["287-5926", "278-5926"]),
        ]) +
        '<div class="tip-box"><strong>📌 常见错误：</strong>① 不回原文定位，凭印象答题；② 被“部分正确”干扰项迷惑；③ Who/What/Where 疑问词搞混；④ 数字题看错位（5926 和 5962 易混）。</div>')
    add(r_a, 4, "阅读 A 篇", "应用文信息定位", minutes=8)

    # P21 阅读B篇
    r_b = (section_head("读", "阅读与写作讲评 · 阅读B篇") +
        '<div class="card"><div class="card-title">📄 阅读 B 篇 · 记叙文细节 + 词义策略</div>' +
        '<div class="rule-card rc-bin"><strong>文章主题：</strong>My Busy School Week（我忙碌的校园一周）—— 107 词，记叙文<br>' +
        '<strong>考点覆盖：</strong>G11 形容词、G15 like+复数/to do、G16 一般现在时、G18 want to do<br>' +
        '<strong>全班得分率：</strong>65%</div></div>' +
        '<div class="grid-2">' +
        '<div class="card"><div class="card-title">🔍 记叙文解题策略</div>' +
        '<div class="rule-card rc-zhug"><strong>1 时间线索法：</strong>圈出 first/then/after that/finally 理清顺序</div>' +
        '<div class="rule-card rc-bin"><strong>2 情感线索法：</strong>圈出 happy/sad/tired 理解作者态度</div>' +
        '<div class="rule-card rc-xing"><strong>3 细节定位法：</strong>题干关键词 → 原文定位 → 逐句对比</div>' +
        '<div class="rule-card rc-ming"><strong>4 推断题策略：</strong>答案必须有原文证据支持</div></div>' +
        '<div class="card"><div class="card-title">📖 词义题解题策略</div>' +
        '<div class="rule-card rc-ming"><strong>词义题标志：</strong>The word &#34;___&#34; probably means...<br><strong>步骤：</strong>1 找生词所在句 2 读前后句找线索 3 代入选项验证</div>' +
        '<div class="rule-card rc-warn"><strong>⚠️ 易错点：</strong>不要选认识但不符合语境的常见义。如 match 在此文是“相配”而非“比赛”，需根据上下文判断。</div></div>' +
        '</div>' +
        quiz_html([
            ("【阅读B篇·词义题】The word \"score\" in Paragraph 2 probably means ___.", "得分", ["分数", "比分记录"]),
            ("【阅读B篇·推断题】How does the writer feel about his school week?（作者对校园一周的感受？）", "Busy but happy.", ["Bored and tired.", "Angry and sad."]),
        ]) +
        '<div class="note-panel"><div class="np-title">精讲要点</div>标题 “My Busy School Week” → busy；文中 “I like to play basketball” “It is relaxing and fun” → happy。推断题需原文证据。</div>')
    add(r_b, 4, "阅读 B 篇", "记叙文 · 词义题", minutes=8)

    # P22 五选四
    r_w5 = (section_head("读", "阅读与写作讲评 · 五选四") +
        '<div class="card"><div class="card-title">📄 五选四 · 句际逻辑与代词指代</div>' +
        '<div class="rule-card rc-xing"><strong>文章主题：</strong>My School Life（我的校园生活）—— 106 词<br>' +
        '<strong>考点覆盖：</strong>G09 Where/There be、G12 方位介词、G11 形容词、G13 祈使句、G15 like<br>' +
        '<strong>全班得分率：</strong>72%（第 20 题错误率 50%）</div></div>' +
        '<div class="grid-2">' +
        '<div class="card"><div class="card-title">🔗 句际逻辑四大线索</div>' +
        '<div class="rule-card rc-zhug"><strong>1 代词指代：</strong>空后 he/she/it/they → 前文须有对应名词</div>' +
        '<div class="rule-card rc-bin"><strong>2 连接词：</strong>but/however（转折）、so/because（因果）</div>' +
        '<div class="rule-card rc-xing"><strong>3 词汇复现：</strong>空前后同根词/同义词/反义词 → 逻辑相关</div>' +
        '<div class="rule-card rc-ming"><strong>4 时空顺序：</strong>first/then/next 或方位变化</div></div>' +
        '<div class="card"><div class="card-title">📝 五选四解题步骤</div>' +
        '<div class="rule-card rc-zhug"><strong>Step 1:</strong> 通读全文了解大意<br><strong>Step 2:</strong> 读空格前后句找逻辑线索<br><strong>Step 3:</strong> 排除明显不符选项<br><strong>Step 4:</strong> 代入验证指代与逻辑<br><strong>Step 5:</strong> 处理干扰项</div>' +
        '<div class="tip-box"><strong>⚠️ 重点：</strong>第 20 题（错误率 50%）考 between...and... 方位介词，回看 G12 考点。</div></div>' +
        '</div>' +
        quiz_html([
            ("【五选四·第16题】前句:My classroom is big and clean. ___ 后句:There are 30 desks and chairs in it.", "It is on the second floor.", ["I like playing basketball.", "My favorite subject is English."]),
            ("【五选四·第20题·G12】前句:The library is next to the classroom. ___ 后句:You can find many interesting books there.", "It is between the classroom and the garden.", ["It is behind the school.", "I don't like reading."]),
        ]) +
        '<div class="note-panel"><div class="np-title">精讲要点</div>后句 it 指代教室 → 空须出现 classroom 信息；方位介词用 between...and... 承接前句位置描写。</div>')
    add(r_w5, 4, "五选四", "句际逻辑 · 代词指代", minutes=8)

    # P23 简答翻译
    r_qa = (section_head("读", "阅读与写作讲评 · 简答翻译") +
        '<div class="grid-2">' +
        '<div class="card"><div class="card-title">✏️ 简答题解题策略</div>' +
        '<div class="rule-card rc-zhug"><strong>1 疑问词选择：</strong>Who → 人名/身份；Where → 地点（方位介词）；What → 事物/活动</div>' +
        '<div class="rule-card rc-bin"><strong>2 完整作答规范：</strong>特殊疑问用完整句；一般疑问 Yes, 主格+be.<br>❌ &#34;Tom.&#34; → ✅ &#34;He is Tom.&#34;</div>' +
        '<div class="rule-card rc-warn"><strong>⚠️ 常见失分：</strong>第 45 题错误率 48%！Who 提问用 “Tom” 而非完整句回答。</div></div>' +
        '<div class="card"><div class="card-title">🌐 英译中技巧</div>' +
        '<div class="rule-card rc-xing"><strong>第 45 题（英译中）：</strong>My friend and I like to play basketball after school.<br>→ 我和我的朋友喜欢放学后打篮球。</div>' +
        '<div class="rule-card rc-ming"><strong>英译中三步法：</strong>1 找主干 2 调语序 3 补修饰（时间/地点状语放句末前）</div>' +
        '<div class="rule-card rc-qita"><strong>语序调整：</strong>after school 英语句末 → 中文“放学后”放动词前</div></div>' +
        '</div>' +
        quiz_html([
            ("【简答·第41题·G06】Who is Tom's English teacher?（用完整句回答）", "His English teacher is Miss Wang.", ["Miss Wang.", "She is Miss Wang."]),
            ("【简答·第42题·G09】Where is the library?（图书馆在哪里？用完整句回答）", "It is next to the classroom.", ["Next to the classroom.", "Is next to the classroom."]),
        ]) +
        '<div class="note-panel"><div class="np-title">精讲要点</div>简答题要求完整作答（中考评分标准）；Where 提问用方位介词短语 + 完整句。</div>')
    add(r_qa, 4, "简答翻译", "完整作答 · 英译中", minutes=7)

    # P24 写作范文
    r_wr = (section_head("读", "阅读与写作讲评 · 写作范文") +
        '<div class="essay-box"><p>Hello, everyone! My name is Li Ming. I am 13 years old. I am from China. I am a student in No. 1 Middle School.</p>' +
        '<p>There are four people in my family — my father, my mother, my sister and I. My father is a teacher. My mother is a teacher, too. They are great. My sister and I are students. We love our family.</p>' +
        '<p>I like sports. I play basketball with my friends after school. It is relaxing and fun. I also like healthy food. I eat apples and bananas every day. I drink milk in the morning. I don&#39;t like ice-cream because it is not healthy.</p>' +
        '<p>I want to be a basketball player. I think it is interesting. What about you?</p></div>' +
        '<div class="essay-score">' +
        '<div class="score-item"><strong>内容 10/10</strong>：自我介绍+家庭+兴趣+饮食，四要素齐全</div>' +
        '<div class="score-item"><strong>语言 9/10</strong>：G03 be✅ G07 所有格✅ G15 like✅ G16 一般现在时✅ G18 want to do✅</div>' +
        '<div class="score-item"><strong>结构 5/5</strong>：四段分明，逻辑清晰</div>' +
        '<div class="score-item"><strong>总分 24/25</strong> 🌟</div>' +
        '</div>' +
        '<div class="grid-2">' +
        '<div class="card"><div class="card-title">✅ 范文亮点（考点运用）</div>' +
        '<div class="rule-card rc-zhug"><strong>1</strong> G01 代词正确：I/my/me/we/our<br>' +
        '<strong>2</strong> G03 be 动词：I am / They are / We are<br>' +
        '<strong>3</strong> G15 like + 运动：I like sports<br>' +
        '<strong>4</strong> G15 like + 复数：I eat apples and bananas<br>' +
        '<strong>5</strong> G17 可数/不可数：apples / milk<br>' +
        '<strong>6</strong> G18 want to do：I want to be a basketball player</div></div>' +
        '<div class="card"><div class="card-title">⚠️ 常见失分点</div>' +
        '<div class="rule-card rc-warn"><strong>1</strong> be 动词搭配：He are...（应 is）<br>' +
        '<strong>2</strong> like + 单数：I like apple（应 apples）<br>' +
        '<strong>3</strong> want 漏 to：I want be...（应 want to be）<br>' +
        '<strong>4</strong> 不可数加 s：milks / breads<br>' +
        '<strong>5</strong> 内容不完整：缺家庭/饮食/兴趣<br>' +
        '<strong>6</strong> 句型单一：通篇 I am... I like...</div></div>' +
        '</div>' +
        '<div class="card"><div class="card-title">📐 写作评分标准拆解（25 分制）</div>' +
        '<div class="grid-3">' +
        '<div class="rule-card rc-zhug"><strong>内容（10 分）</strong>自我介绍 2.5 / 家庭 2.5 / 兴趣 2.5 / 饮食 2.5<br><em>缺一项扣 2.5 分</em></div>' +
        '<div class="rule-card rc-bin"><strong>语言（10 分）</strong>be 动词 2 / 代词 2 / 复数不可数 2 / like-want 2 / 拼写标点 2<br><em>每语法错扣 0.5 分</em></div>' +
        '<div class="rule-card rc-xing"><strong>结构（5 分）</strong>分段 2 / 逻辑 2 / 首尾 1<br><em>无分段扣 2 分</em></div>' +
        '</div></div>' +
        '<div class="tip-box"><strong>📝 写作提分建议：</strong>1 每段不同句型开头；2 至少用 5 个考点；3 检查可数/不可数；4 检查 be 动词；5 字数 75-85 词。</div>')
    add(r_wr, 4, "写作范文", "范文赏析 · 评分标准", minutes=8)

    # ---- 段5 总结（3 页） ----
    # P25 薄弱考点清单
    s_weak = (section_head("结", "总结与提升 · 薄弱考点清单") +
        '<div class="card"><div class="card-title">🎯 G01-G18 诊断等级清单</div>' +
        '<table class="error-table"><thead><tr><th>考点</th><th>名称</th><th>得分率</th><th>等级</th><th>后续动作</th></tr></thead><tbody>' +
        '<tr><td>G01</td><td>人称代词主格与宾格</td><td>85%</td><td><span class="grade-tag grade-a">A</span></td><td>进入Stage3</td></tr>' +
        '<tr><td>G02</td><td>形容词性与名词性物主代词</td><td>65%</td><td><span class="grade-tag grade-c">C</span></td><td>补充变式</td></tr>' +
        '<tr><td>G03</td><td>be 动词搭配</td><td>88%</td><td><span class="grade-tag grade-a">A</span></td><td>进入Stage3</td></tr>' +
        '<tr><td>G04</td><td>指示代词单复数</td><td>80%</td><td><span class="grade-tag grade-b">B</span></td><td>少量巩固</td></tr>' +
        '<tr><td>G05</td><td>be 否定与疑问</td><td>76%</td><td><span class="grade-tag grade-b">B</span></td><td>少量巩固</td></tr>' +
        '<tr><td>G06</td><td>Who 疑问句</td><td>72%</td><td><span class="grade-tag grade-b">B</span></td><td>补充简答</td></tr>' +
        '<tr><td>G07</td><td>名词所有格</td><td>62%</td><td><span class="grade-tag grade-c">C</span></td><td>专项巩固</td></tr>' +
        '<tr><td>G08</td><td>基数词 1-100</td><td>78%</td><td><span class="grade-tag grade-b">B</span></td><td>少量巩固</td></tr>' +
        '<tr><td>G09</td><td>Where + There be</td><td>70%</td><td><span class="grade-tag grade-b">B</span></td><td>补充变式</td></tr>' +
        '<tr><td>G10</td><td>可数名词规则复数</td><td>60%</td><td><span class="grade-tag grade-c">C</span></td><td>专项巩固</td></tr>' +
        '<tr><td>G11</td><td>形容词定语/表语</td><td>75%</td><td><span class="grade-tag grade-b">B</span></td><td>少量巩固</td></tr>' +
        '<tr><td>G12</td><td>方位介词扩展</td><td>55%</td><td><span class="grade-tag grade-c">C</span></td><td>重点专项</td></tr>' +
        '<tr><td>G13</td><td>Do/Don&#39;t 祈使句</td><td>82%</td><td><span class="grade-tag grade-a">A</span></td><td>进入Stage3</td></tr>' +
        '<tr><td>G14</td><td>What 疑问句</td><td>79%</td><td><span class="grade-tag grade-b">B</span></td><td>少量巩固</td></tr>' +
        '<tr><td>G15</td><td>like + 复数/to do</td><td>68%</td><td><span class="grade-tag grade-b">B</span></td><td>补充变式</td></tr>' +
        '<tr><td>G16</td><td>一般现在时非三单</td><td>73%</td><td><span class="grade-tag grade-b">B</span></td><td>少量巩固</td></tr>' +
        '<tr><td>G17</td><td>可数/不可数分类</td><td>58%</td><td><span class="grade-tag grade-c">C</span></td><td>重点专项</td></tr>' +
        '<tr><td>G18</td><td>want to do sth.</td><td>71%</td><td><span class="grade-tag grade-b">B</span></td><td>少量巩固</td></tr>' +
        '</tbody></table></div>' +
        '<div class="grid-4">' +
        '<div class="rule-card rc-zhug" style="text-align:center;"><strong>A 级 90%+</strong><br>3 个<br>G01/G03/G13<br>✅ 进Stage3</div>' +
        '<div class="rule-card rc-bin" style="text-align:center;"><strong>B 级 75-89%</strong><br>10 个<br>少量巩固<br>补充变式</div>' +
        '<div class="rule-card rc-warn" style="text-align:center;"><strong>C 级 50-74%</strong><br>5 个<br>G02/G07/G10/G12/G17<br>🔴 重点专项</div>' +
        '<div class="rule-card rc-qita" style="text-align:center;"><strong>D 级 &lt;50%</strong><br>0 个<br>无大面积薄弱<br>✅ 整体达标</div>' +
        '</div>' +
        '<div class="tip-box"><strong>📊 诊断结论：</strong>整体 B 级（均值 71%），5 个 C 级考点需在 Stage 3 前重点巩固。名词类（G07/G10/G17）和方位介词（G12）是共性薄弱点。</div>')
    add(s_weak, 5, "薄弱考点清单", "G01-G18 等级", minutes=7)

    # P26 下阶段计划
    s_plan = (section_head("结", "总结与提升 · 下阶段计划") +
        '<div class="grid-2">' +
        '<div class="card" style="border-top:4px solid var(--brand);"><div class="card-title">📘 Stage 3（L8-L12）预习重点</div>' +
        '<div class="rule-card rc-zhug"><strong>L8：</strong>可数/不可数深化（量词 a cup of / a piece of）→ 螺旋自 G17</div>' +
        '<div class="rule-card rc-bin"><strong>L9：</strong>情态动词 can/can&#39;t（能力表达）</div>' +
        '<div class="rule-card rc-xing"><strong>L10：</strong>一般现在时三单（he/she/it + -s/es）→ 螺旋自 G16</div>' +
        '<div class="rule-card rc-ming"><strong>L11：</strong>What time / When 疑问句 + 频度副词</div>' +
        '<div class="rule-card rc-warn"><strong>L12：</strong>Stage 3 阶段测试 + 综合语篇</div></div>' +
        '<div class="card" style="border-top:4px solid var(--accent);"><div class="card-title">📝 本阶段巩固任务（C 级专项）</div>' +
        '<div class="rule-card rc-zhug"><strong>任务 1 · 词汇巩固：</strong>复习 L4 方位介词；L6 食物复数；抄写不可数名词 10 个并造句</div>' +
        '<div class="rule-card rc-bin"><strong>任务 2 · 语法巩固：</strong>G02 物主变形 10 题；G07 所有格 5+5；G10 复数 20 个；G12 画房间图造 6 句；G17 分类 20 词</div>' +
        '<div class="rule-card rc-xing"><strong>任务 3 · 阅读训练：</strong>每天 1 篇短文（80-100 词）；每周 1 篇五选四</div>' +
        '<div class="rule-card rc-ming"><strong>任务 4 · 写作训练：</strong>模仿范文写 80 词自我介绍（含家庭+兴趣+饮食）</div></div>' +
        '</div>' +
        '<div class="tip-box"><strong>📅 时间安排：</strong>建议在 L8 前完成（约 1-2 周）。优先巩固 G12 方位介词和 G17 可数/不可数（得分率最低）。</div>' +
        '<div class="grid-2">' +
        '<div class="card" style="border-top:4px solid var(--brand);"><div class="card-title">🔴 C 级考点专项巩固计划</div>' +
        '<div class="rule-card rc-warn"><strong>G12 方位介词（55%）：</strong>画房间平面图用 6 介词各写 1 句；between...and... 专项 10 题（2 天）</div>' +
        '<div class="rule-card rc-warn"><strong>G17 可数/不可数（58%）：</strong>分类 30 词；造 10 句（5 可数复数 + 5 不可数）（2 天）</div>' +
        '<div class="rule-card rc-warn"><strong>G10 名词复数（60%）：</strong>写 30 个复数；重点 o 结尾和 y 结尾（1 天）</div></div>' +
        '<div class="card" style="border-top:4px solid var(--accent);"><div class="card-title">🟡 B 级考点少量巩固</div>' +
        '<div class="rule-card rc-bin"><strong>G02 物主代词（65%）：</strong>10 道形/名物主转换（1 天）</div>' +
        '<div class="rule-card rc-bin"><strong>G07 名词所有格（62%）：</strong>写 5 个 &#39;s + 5 个 of（1 天）</div>' +
        '<div class="rule-card rc-bin"><strong>其他 B 级：</strong>G04/G05/G06/G08/G09/G11/G14/G15/G16/G18 各 5 道变式（2 天）</div></div>' +
        '</div>')
    add(s_plan, 5, "下阶段计划", "Stage3 预习 · 巩固任务", minutes=7)

    # P27 核心口诀总览
    s_rhyme = (section_head("结", "总结与提升 · 核心口诀总览") +
        '<div class="formula-box"><div class="formula-text">G01-G18 全部口诀 · 一页速览</div>' +
        '<div class="formula-sub">考前复习专用 · Stage 2 · L07 阶段测试讲评</div></div>' +
        '<div class="formula-grid">' +
        '<div class="formula-mini"><div class="formula-mini-num">G01 · 代词主格/宾格</div><div class="formula-mini-text">主格做主语，宾格做宾语；介词动词后，宾格来站岗</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G02 · 物主代词</div><div class="formula-mini-text">形物加名词，名物独立用；my book / mine，加 s 变名物</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G03 · be 动词搭配</div><div class="formula-mini-text">I 用 am，you 用 are；is 连着他她它，复数一律都用 are</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G04 · 指示代词</div><div class="formula-mini-text">this 近单 that 远单；these 近复 those 远复；答语用 it/they</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G05 · be 否定/疑问</div><div class="formula-mini-text">否定 be+not，疑问 be 提前；简答用主格，Yes/No 开头</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G06 · Who 疑问句</div><div class="formula-mini-text">Who 问人，回答用姓名/身份；Who is...? → He/She is...</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G07 · 名词所有格</div><div class="formula-mini-text">单数加 &#39;s，复数 s 后加 &#39;；不规则加 &#39;s，无生命用 of</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G08 · 基数词</div><div class="formula-mini-text">1-12 独立记，13-19 加 -teen；整十加 -ty，几十几用连字符</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G09 · Where/There be</div><div class="formula-mini-text">Where 问地点，There be 表存在；is 配单数，are 配复数</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G10 · 名词规则复数</div><div class="formula-mini-text">一般加 -s，s/x/sh/ch 加 -es；辅音+y 变 ies</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G11 · 形容词</div><div class="formula-mini-text">定语放名词前，表语放 be 后；原级不变化，不涉比较级</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G12 · 方位介词</div><div class="formula-mini-text">in 里 on 上 under 下；behind 后 next to 旁；between...and... 中间放</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G13 · 祈使句</div><div class="formula-mini-text">肯定动词原形开头，否定 Don&#39;t 加原形；主语 you 省略</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G14 · What 疑问句</div><div class="formula-mini-text">What 问事物，What is this/that? → It&#39;s a/an...</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G15 · like 用法</div><div class="formula-mini-text">like + 名词复数（喜某物）；like to do（喜做某事）</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G16 · 一般现在时非三单</div><div class="formula-mini-text">I/You/We/They + 原形；否定 don&#39;t + 原形</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G17 · 可数/不可数</div><div class="formula-mini-text">可数能加 s，不可数不能加；液体粉末不可数，milk/bread/rice</div></div>' +
        '<div class="formula-mini"><div class="formula-mini-num">G18 · want to do</div><div class="formula-mini-text">want to + 动词原形；to do 不定式，to 不能省</div></div>' +
        '</div>' +
        '<div class="note-panel"><div class="np-title">🎉 完成</div>G01-G18 全部 18 个考点口诀已回顾完毕！下一步：按诊断等级巩固 C 级考点 → 进入 Stage 3（L8-L12）。</div>')
    add(s_rhyme, 5, "核心口诀总览", "G01-G18 一页速览", minutes=6)

    # ---- 延伸练习（14 页，可精简排版：每题 quiz 用 quiz_html 紧凑呈现） ----
    def ext_page_quiz(title, sub, questions, note):
        return (section_head("延", title) +
                '<div class="body-text"><span class="highlight">延伸巩固</span>：独立完成，点击选项即时对答案，错题回看对应精讲页。</div>' +
                quiz_html(questions) +
                '<div class="note-panel"><div class="np-title">延伸要点</div>%s</div>' % note)

    # P28 语法延伸·代词与be
    add(ext_page_quiz("语法延伸 · 代词与be动词", "G01-G05",
        [("This is not my pen. ___ is blue.", "Mine", ["They", "Them", "Their"]),
         ("___ your sister a student? Yes, she ___.", "Is; is", ["Are; is", "Is; are", "Are; are"]),
         ("These are ___ books. Where are ___?", "our; ours", ["we; us", "us; we", "ours; our"]),
         ("___ is my best friend. ___ often play together.", "He; We", ["Him; Us", "His; Our", "She; Them"])],
         "名词性物主代词做主语/表语独立使用；be 动词三单用 is；主格做主语。"), 6)

    # P29 语法延伸·疑问句与名词
    add(ext_page_quiz("语法延伸 · 疑问句与名词", "G06-G10/G17",
        [("___ is your schoolbag? It's on the desk.", "Where", ["What", "Who", "How"]),
         ("___ is that girl? She is my cousin.", "Who", ["What", "Where", "When"]),
         ("There ___ some milk and two apples on the table.", "is", ["are", "be", "am"]),
         ("I have two ___ and some ___ for breakfast.", "eggs; bread", ["egg; bread", "eggs; breads", "egg; breads"])],
         "Where 问地点、Who 问人；There be 就近原则（milk 不可数用 is）；egg 可数复数加 s，bread 不可数不加 s。"), 6)

    # P30 语法延伸·介词与祈使句
    add(ext_page_quiz("语法延伸 · 介词与祈使句", "G12-G13",
        [("Your ruler is ___ the desk. I can't see it.", "under", ["on", "in", "next to"]),
         ("___ open the window. It's too hot.", "Please", ["Not", "Don't", "No"]),
         ("___ make noise in the library.", "Don't", ["Please", "Not", "No"]),
         ("The cat is ___ the box and the chair.", "between", ["on", "in", "under"])],
         "can't see → under（被遮挡）；肯定祈使用 Please，否定祈使用 Don&#39;t；between...and... 表两者之间。"), 6)

    # P31 语法延伸·动词搭配与时态
    add(ext_page_quiz("语法延伸 · 动词搭配与时态", "G15-G16/G18",
        [("She likes ___ basketball after school.", "to play", ["play", "plays", "playing the"]),
         ("He wants ___ a doctor when he grows up.", "to be", ["be", "being", "is"]),
         ("We ___ like sports. We ___ play tennis.", "don't; don't", ["doesn't; doesn't", "don't; doesn't", "aren't; don't"]),
         ("How many ___ can you see in the picture?", "tomatoes", ["tomato", "tomatos", "a tomato"])],
         "like to do / want to do 后接 to + 原形；we 非三单否定用 don&#39;t；tomato 复数加 -es。"), 6)

    # P32 词汇延伸·L1-L3词义
    add(ext_page_quiz("词汇延伸 · L1-L3 词义辨析", "L1-L3",
        [("This is not ___ book. ___ is on the desk. (I/my/mine)", "my; Mine", ["I; I", "mine; My", "my; I"]),
         ("Can you spell ___? D-I-C-T-I-O-N-A-R-Y.", "dictionary", ["schoolbag", "eraser", "pencil"]),
         ("___ are my grandparents. ___ love me very much.", "These; They", ["This; They", "Those; Them", "That; Their"]),
         ("My keys are ___. I find them in my bag.", "everywhere", ["lose", "there", "here"])],
         "形容词性物主 my 后接名词，名词；名词性物主 mine 独立做主语。"), 6)

    # P33 词汇延伸·L4-L6 复数与不可数
    add(ext_page_quiz("词汇延伸 · L4-L6 复数与不可数", "L1-L6",
        [("I like ___. It's very sweet and red.", "strawberry", ["tomato", "potato", "milk"]),
         ("How much ___ do you drink every day?", "milk", ["apples", "eggs", "bananas"]),
         ("The movie is ___. I don't want to see it again.", "boring", ["relaxing", "interesting", "fun"]),
         ("We need some ___ for the salad.", "tomatoes", ["milks", "breads", "rices"])],
         "strawberry 草莓甜且红；how much+不可数（milk）；无聊用 boring；some+可数复数 tomatoes。"), 6)

    # P34 阅读延伸·信息匹配
    add(ext_page_quiz("阅读延伸 · 信息匹配", "阅读A/B 技巧",
        [("Read: Name: Tom / Age: 13 / Grade: 7 / School: No.1 MS. What grade is Tom in?", "Grade 7", ["Grade 6", "Grade 8", "Grade 9"]),
         ("\"My Busy School Week\" is a ___ text.", "记叙文", ["说明文", "应用文", "议论文"]),
         ("In \"A Healthy Eating Corner\", the writer mainly ___.", "introduces healthy eating habits", ["tells a story about food", "lists school rules", "describes a trip"]),
         ("五选四: The missing sentence should ___.", "connect the ideas before and after", ["start a new topic", "repeat the first sentence", "give a conclusion"])],
         "信息卡直接定位；My Busy School Week 为记叙文；A Healthy Eating Corner 介绍健康饮食习惯；五选四缺失句连接前后文。"), 6)

    # P35 阅读延伸·写作策略
    add(ext_page_quiz("阅读延伸 · 写作策略", "写作 结构·翻译",
        [("When writing a self-introduction, you should include ___.", "name, age, family, and hobbies", ["name only", "name and age only", "school rules"]),
         ("Translation: \"我有一个姐姐和一个弟弟\" → ___", "I have a sister and a brother.", ["I has a sister and a brother.", "I have sister and brother.", "I has a sister and a brothers."]),
         ("Good writing should have ___ structure.", "beginning, body, and ending", ["only sentences", "many difficult words", "no punctuation"]),
         ("In translation, \"Where is your dictionary?\" → ___", "Where is your dictionary?", ["What is your dictionary?", "How is your dictionary?", "Who is your dictionary?"])],
         "自我介绍含姓名/年龄/家庭/兴趣；I+have；写作三段结构；Where 问地点。"), 6)

    # P36 数词延伸·1-100拼写
    add(ext_page_quiz("数词延伸 · 1-100 拼写与运用", "G08",
        [("How do you spell 15?", "fifteen", ["fiveteen", "fiftteen", "fivety"]),
         ("How do you spell 40?", "forty", ["fourty", "fourteen", "fortee"]),
         ("23 is spelled as ___.", "twenty-three", ["tweny-three", "twentyth-three", "twenythree"]),
         ("\"There are ___ days in a week.\"", "seven", ["five", "twelve", "twenty"])],
         "15=fifteen（five→fif）；40=forty（无 u）；几十几用连字符；一周 7 天。"), 6)

    # P37 综合诊断·语法综合
    add(ext_page_quiz("综合诊断 · 语法综合运用", "综合诊断",
        [("___ is your English teacher? Miss Wang.", "Who", ["What", "Where", "How"]),
         ("There ___ a book and two pens on the desk.", "is", ["are", "be", "am"]),
         ("Don't ___ in class. Listen to the teacher.", "talk", ["to talk", "talking", "talks"]),
         ("I ___ like apples, but I ___ bananas.", "don't; like", ["don't; doesn't", "doesn't; like", "am not; like"])],
         "问人用 Who；There be 就近原则；Don't+原形；I 非三单否定 don't。"), 6)

    # P38 综合诊断·词汇与句型
    add(ext_page_quiz("综合诊断 · 词汇与句型", "综合诊断",
        [("This dictionary is ___. It's not ___.", "mine; yours", ["my; your", "my; yours", "mine; your"]),
         ("Let's ___ sports after school.", "play", ["to play", "plays", "playing"]),
         ("___ your cousin have a soccer ball?", "Does", ["Do", "Is", "Are"]),
         ("The strawberries ___ delicious.", "are", ["is", "be", "am"])],
         "名词性物主做表语；Let's+原形；三单疑问 Does；复数用 are。"), 6)

    # P39 综合诊断·易错题集锦
    add(ext_page_quiz("综合诊断 · 易错题集锦", "综合诊断",
        [("___ your father a teacher? No, he ___.", "Is; isn't", ["Does; doesn't", "Are; aren't", "Is; is"]),
         ("My friend and I ___ students.", "are", ["is", "am", "be"]),
         ("Please ___ your homework to school tomorrow.", "bring", ["to bring", "bringing", "brings"]),
         ("___ food do you like? I like healthy food.", "What kind of", ["Where", "How", "Who"])],
         "a teacher 后用 be；we 用 are；祈使句原形；问种类 What kind of。"), 6)

    # P40 综合诊断·高频考点强化
    add(ext_page_quiz("综合诊断 · 高频考点强化", "综合诊断",
        [("___ brother is a student. ___ is in No.1 Middle School.", "My; He", ["I; He", "Mine; His", "My; His"]),
         ("We don't have ___ bread. Let's buy some.", "any", ["some", "a", "an"]),
         ("She wants ___ a new bike for her birthday.", "to get", ["get", "getting", "gets"]),
         ("Do you like ___? Yes, I do. It's fun.", "to play tennis", ["play tennis", "playing the tennis", "plays tennis"])],
         "形物 My 修饰名词、主格 He 做主语；否定句用 any；want to do；like to do、tennis 不加 the。"), 6)

    # P41 综合诊断·阶段冲刺
    add(ext_page_quiz("综合诊断 · 阶段冲刺", "综合诊断",
        [("This is ___ eraser and that is ___ ruler.", "an; a", ["a; a", "an; an", "a; an"]),
         ("Are these your ___? Yes, they are.", "dictionaries", ["dictionary", "dictionarys", "a dictionary"]),
         ("Where ___ your keys? They're on the table.", "are", ["is", "am", "be"]),
         ("What ___ your mother do? She is a doctor.", "does", ["do", "is", "are"])],
         "eraser 元音用 an、ruler 辅音用 a；辅音+y 变 ies；keys 复数用 are；三单 does。"), 6)

    total = p - 1
    seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
    # 段名映射（与 add() 各段标题对应）；L07 实际 6 段，导航只渲染真实存在的段。
    # 修复：引擎默认 NAV 为 9 段模板，若直接使用会导致第 7/8/9 个 nav-item 的 data-segment
    # 在 segmentPages 中无对应，updateNav() 遍历时 segmentPages[seg] 为 undefined → pages[0] 抛异常，
    # 中断 updateNav() 之后的 updateCounter()，页码不更新。故按 seg 实际键动态生成匹配导航。
    _ROMAN = "①②③④⑤⑥⑦⑧⑨"
    _NAMES = {1: "测试概况", 2: "语法精讲", 3: "词汇精讲", 4: "阅读写作", 5: "总结提升", 6: "延伸练习"}
    def _nav_item(i):
        return ('<div class="nav-item" data-segment="%d" onclick="jumpToSegment(%d)">'
                '<span class="nav-num">%s</span>%s</div>'
                % (i, i, _ROMAN[i - 1], _NAMES.get(i, "段%d" % i)))
    nav_html = ('<div class="nav-bar">' +
                '<div class="nav-separator"></div>'.join(_nav_item(i) for i in sorted(seg)) +
                '</div>')
    scode = E.STUDENT_CODES.get("邓兴华", "stu_dxh")
    js_extra = ("var studentId='" + scode + "';\n" +
                E.JS_EXTRA_TPL % (total, json.dumps(seg_pages, ensure_ascii=False),
                                  json.dumps(page_meta, ensure_ascii=False)))
    from theme_colors import build_theme_css
    theme_css = build_theme_css(card.get("vocab", {}).get("theme", "review"))
    html = build_courseware(title=title, pages_dict=pages, js_extra=js_extra,
                          session="L07", nav_html=nav_html,
                          stage_badge=stage_badge, n_pages=total,
                          css_extra=CSS_CONTRACT_MARKERS + E.CSS_EXTRA + CSS_L07 + theme_css)
    html = html.replace('<div class="cover-wrap', '<!-- CW-VISUAL-CONTRACT:1 -->\n<div class="cover-wrap', 1)
    return html


if __name__ == "__main__":
    out = os.path.join(HERE, "test_L7_courseware.html")
    html = build_l07()
    open(out, "w", encoding="utf-8").write(html)
    print("L7 课件生成：%s (%d bytes)" % (out, len(html.encode("utf-8"))))