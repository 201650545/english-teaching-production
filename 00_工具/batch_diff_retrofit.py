# -*- coding: utf-8 -*-
"""
许颖嘉 26 课视觉差异化批处理 (A层 22 课脚本化 + L05/L17/L18/L26 同套 recipe)
仅注入 CSS 变量层 + 封面/组件变体，不改知识点/题干/判题/IndexedDB。
每课改动前备份到 _旧件_差异化20260806\
"""
import os, re, hashlib, json, shutil

BASE = "D:/英语教学/许颖嘉"
HTML_DIR = "课件成品_网页PPT"
BAK_DIR_NAME = "_旧件_差异化20260806"

# ============ 26 课 recipe 分配（连续三课不重复） ============
# R1×6 + R2×5 + R3×5 + R4×5 + R5×5 = 26
RECIPE_MAP = {
    1:"R1", 2:"R4", 3:"R2", 4:"R5", 5:"R3", 6:"R1", 7:"R4", 8:"R2", 9:"R5",
    10:"R3", 11:"R1", 12:"R4", 13:"R2", 14:"R5", 15:"R3", 16:"R1", 17:"R2",
    18:"R4", 19:"R5", 20:"R3", 21:"R1", 22:"R4", 23:"R2", 24:"R5", 25:"R3", 26:"R1"
}

# ============ 5 个 recipe 的 CSS（覆盖变量 + 组件变体） ============

# 通用封面安全区变体（仅视觉，不动结构/事件）
COVER_VARIANTS = {
# R1 编辑杂志：左对齐大标题 + 编号 + 分隔线强调
# !important 用于覆盖主题CSS的 !important（如 neo-brutalism 白底覆盖）
"R1": """
.cover-wrap{justify-content:center;background:linear-gradient(160deg,#0f172a 0%,#1e293b 55%,#334155 100%)!important;}
.cover-wrap::after{display:none!important;}
.cover-title{font-size:44px;font-weight:900;letter-spacing:1px;text-align:left;width:82%;color:#fff;text-shadow:0 2px 12px rgba(0,0,0,.35);}
.cover-subtitle{text-align:left;width:82%;color:#e2e8f0;border-left:4px solid var(--accent);padding-left:12px;margin-top:6px;}
.cover-tagline{text-align:left;width:82%;color:#94a3b8;font-style:italic;}
.cover-badge{background:var(--accent);color:#0f172a;font-weight:800;border-radius:2px;padding:4px 14px;letter-spacing:2px;}
.cover-info{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.15);border-radius:4px;}
"""
,
# R2 档案推理：文件标签顶栏 + 虚线边框 + 印章
"R2": """
.cover-wrap{justify-content:flex-start;background:linear-gradient(180deg,#f4efe6 0%,#ece4d3 60%,#ddd2bc 100%)!important;padding-top:60px;}
.cover-wrap::after{display:none!important;}
.cover-wrap::before{content:'ARCHIVE';position:absolute;top:18px;right:24px;font-size:13px;letter-spacing:4px;color:#b08968;border:2px solid #b08968;padding:4px 10px;border-radius:2px;transform:rotate(-3deg);}
.cover-title{font-size:40px;font-weight:700;color:#3d2f1f;border-bottom:3px dashed #b08968;padding-bottom:10px;width:80%;}
.cover-subtitle{color:#6b5a48;font-family:'Courier New',monospace;}
.cover-badge{background:#3d2f1f;color:#f4efe6;border-radius:2px;padding:3px 12px;letter-spacing:2px;}
.cover-info{background:rgba(61,47,31,.06);border:1px dashed #b08968;border-radius:2px;}
"""
,
# R3 自然手账：纸张质感 + 田野标签 + 森林色
"R3": """
.cover-wrap{justify-content:center;background:linear-gradient(165deg,#eef4e6 0%,#dce8d0 50%,#c8dbb4 100%)!important;}
.cover-wrap::after{display:none!important;}
.cover-wrap::before{content:'';position:absolute;inset:0;background-image:radial-gradient(rgba(90,120,70,.12) 1px,transparent 1px);background-size:22px 22px;}
.cover-title{font-size:42px;font-weight:800;color:#2f4a2a;text-shadow:0 1px 0 rgba(255,255,255,.6);}
.cover-subtitle{color:#4a6b3d;font-style:italic;}
.cover-tagline{color:#6b8558;font-size:15px;}
.cover-badge{background:#5a7846;color:#fff;border-radius:20px;padding:4px 16px;}
.cover-info{background:rgba(255,255,255,.55);border:1px solid #a8c08a;border-radius:12px;}
"""
,
# R4 任务游戏：关卡式 + 进度强调 + 明快
"R4": """
.cover-wrap{justify-content:center;background:linear-gradient(135deg,#1d3557 0%,#2a4d69 55%,#457b9d 100%)!important;}
.cover-wrap::after{display:none!important;}
.cover-wrap::before{content:'LEVEL ' counter(none);position:absolute;top:20px;left:24px;font-size:40px;font-weight:900;color:rgba(255,255,255,.15);}
.cover-title{font-size:46px;font-weight:900;color:#fff;letter-spacing:2px;text-transform:uppercase;text-shadow:0 4px 0 rgba(0,0,0,.2);}
.cover-subtitle{color:#e0fbfc;font-weight:600;}
.cover-badge{background:#ffb703;color:#1d3557;font-weight:900;border-radius:6px;padding:5px 18px;box-shadow:0 3px 0 #c98a00;}
.cover-info{background:rgba(255,255,255,.1);border:2px solid #ffb703;border-radius:10px;}
"""
,
# R5 极简学术：大留白 + 高对比 + 克制
"R5": """
.cover-wrap{justify-content:center;background:#fafafa!important;padding:40px;}
.cover-wrap::after{display:none!important;}
.cover-title{font-size:40px;font-weight:600;color:#111;letter-spacing:.5px;max-width:70%;}
.cover-subtitle{color:#555;font-weight:400;}
.cover-tagline{color:#888;font-size:14px;}
.cover-badge{background:#fff;color:#111;border:1.5px solid #111;border-radius:0;padding:3px 12px;letter-spacing:1px;font-weight:600;}
.cover-info{background:#fff;border:1px solid #ddd;border-radius:0;}
"""
}

# 每个 recipe 的组件级变体（仅视觉，不改判题/结构）
RECIPE_COMPONENT_CSS = {
# R1 编辑杂志：矩形轻描边卡片 + 中性色高对比 + 单强调红
"R1": """
:root{
  --brand:#c0392b; --accent:#e67e22; --brand-light:#d94f3d; --accent-light:#f0a35e;
  --bg-start:#f5f5f2; --bg-end:#ececea;
  --text-primary:#1a1a1a; --text-secondary:#4a4a4a;
  --card-bg:#ffffff; --card-shadow:none;
  --page-shadow:none;
}
body{color:#1a1a1a;}
.page{background:#f5f5f2;}
.quiz-opt,.card,.vocab-card,.ext-card,.eg-card,.rule-card,.recall-card{background:#fff;border:1.5px solid #d1d1cf;border-radius:4px;box-shadow:none;}
.quiz-opt:hover{border-color:#c0392b;}
.section-head .sh-num{background:#c0392b;border-radius:2px;}
.nav-item.active{background:#c0392b;}
.progress-bar-fill{background:linear-gradient(90deg,#c0392b,#e67e22);}
"""
,
# R2 档案推理：深绿棕克制 + 虚线边框 + 文件标签
"R2": """
:root{
  --brand:#4a5d45; --accent:#b08968; --brand-light:#5f7560; --accent-light:#c9a885;
  --bg-start:#f4efe6; --bg-end:#ece4d3;
  --text-primary:#2d2a26; --text-secondary:#5c564c;
  --card-bg:#fbf8f1; --card-shadow:none;
  --page-shadow:none;
}
body{color:#2d2a26;}
.page{background:#f4efe6;}
.quiz-opt,.card,.vocab-card,.ext-card,.eg-card,.recall-card{background:#fbf8f1;border:1.5px dashed #b08968;border-radius:3px;box-shadow:none;}
.quiz-opt:hover{border-style:solid;border-color:#4a5d45;}
.section-head .sh-num{background:#4a5d45;border-radius:2px;}
.nav-item.active{background:#4a5d45;}
.rule-card{border-left:4px solid #b08968;}
.progress-bar-fill{background:linear-gradient(90deg,#4a5d45,#b08968);}
"""
,
# R3 自然手账：纸张卡片 + 圆角 + 森林绿
"R3": """
:root{
  --brand:#3f6b35; --accent:#7a9b57; --brand-light:#5a8a4a; --accent-light:#9db97e;
  --bg-start:#f2f7ec; --bg-end:#e3eed6;
  --text-primary:#2f3a2c; --text-secondary:#5a6b52;
  --card-bg:#ffffff; --card-shadow:0 2px 8px rgba(90,120,70,.12);
  --page-shadow:none;
}
body{color:#2f3a2c;}
.page{background:#f2f7ec;}
.quiz-opt,.card,.vocab-card,.ext-card,.eg-card,.recall-card{background:#fff;border:1px solid #c8dbb4;border-radius:14px;box-shadow:0 2px 8px rgba(90,120,70,.1);}
.quiz-opt:hover{border-color:#3f6b35;background:#f0f7ea;}
.section-head .sh-num{background:#3f6b35;border-radius:10px;}
.nav-item.active{background:#3f6b35;border-radius:8px;}
.progress-bar-fill{background:linear-gradient(90deg,#3f6b35,#7a9b57);}
"""
,
# R4 任务游戏：明快 + 重圆角 + 进度强调
"R4": """
:root{
  --brand:#1d3557; --accent:#ffb703; --brand-light:#2a4d69; --accent-light:#ffcc4d;
  --bg-start:#f0f7fb; --bg-end:#e3eef5;
  --text-primary:#152238; --text-secondary:#425a70;
  --card-bg:#ffffff; --card-shadow:0 4px 14px rgba(29,53,87,.14);
  --page-shadow:none;
}
body{color:#152238;}
.page{background:#f0f7fb;}
.quiz-opt,.card,.vocab-card,.ext-card,.eg-card,.recall-card{background:#fff;border:2px solid #dbe9f2;border-radius:12px;box-shadow:0 4px 14px rgba(29,53,87,.12);}
.quiz-opt:hover{border-color:#ffb703;transform:translateY(-1px);}
.section-head .sh-num{background:#1d3557;border-radius:8px;}
.nav-item.active{background:#1d3557;border-radius:6px;}
.rule-card{border-top:4px solid #ffb703;}
.progress-bar-fill{background:linear-gradient(90deg,#ffb703,#ffcc4d);}
"""
,
# R5 极简学术：大留白 + 高对比 + 克制边框
"R5": """
:root{
  --brand:#1f3a5f; --accent:#8fa6c0; --brand-light:#2e4f7d; --accent-light:#a9bcd2;
  --bg-start:#ffffff; --bg-end:#f5f7fa;
  --text-primary:#1c1c1c; --text-secondary:#4a4a4a;
  --card-bg:#ffffff; --card-shadow:none;
  --page-shadow:none;
}
body{color:#1c1c1c;}
.page{background:#fff;}
.quiz-opt,.card,.vocab-card,.ext-card,.eg-card,.recall-card{background:#fff;border:1px solid #e2e2e2;border-radius:0;box-shadow:none;}
.quiz-opt:hover{border-color:#1f3a5f;background:#f5f7fa;}
.section-head .sh-num{background:#1f3a5f;border-radius:0;}
.nav-item.active{background:#1f3a5f;border-radius:0;}
.rule-card{border-left:3px solid #1f3a5f;}
.progress-bar-fill{background:#1f3a5f;}
"""
}

# 正误反馈语义色保留（叠加在 recipe 上，含文字/图标不靠纯色）
FEEDBACK_SAFE = """
.quiz-opt.opt-correct,.quiz-opt.correct,.fb-bubble.correct,.game-option.correct,.game-feedback.correct{background:#e8f5e9!important;color:#1e7e47!important;border-color:#2e9e5b!important;}
.quiz-opt.opt-wrong,.quiz-opt.wrong,.fb-bubble.wrong,.game-option.wrong,.game-feedback.wrong{background:#ffebee!important;color:#c62828!important;border-color:#e04a4a!important;}
"""

def recipe_css(recipe):
    return ("/* <CW-DIFF-STYLE family=\"" + recipe + "\"> */\n"
            + RECIPE_COMPONENT_CSS[recipe]
            + COVER_VARIANTS[recipe]
            + FEEDBACK_SAFE
            + "/* </CW-DIFF-STYLE> */\n")

def process_lesson(lesson):
    recipe = RECIPE_MAP[lesson]
    fn = f"第{lesson:02d}课时_课件_基础.html"
    path = os.path.join(BASE, f"第{lesson:02d}课时", HTML_DIR, fn)
    if not os.path.exists(path):
        return {"lesson": lesson, "ok": False, "err": "HTML not found"}
    # 备份
    bak_dir = os.path.join(BASE, f"第{lesson:02d}课时", HTML_DIR, BAK_DIR_NAME)
    os.makedirs(bak_dir, exist_ok=True)
    bak = os.path.join(bak_dir, fn)
    if not os.path.exists(bak):
        shutil.copy2(path, bak)
    # 读取
    with open(path, encoding="utf-8") as f:
        html = f.read()
    # 若已注入过同 recipe，跳过（幂等）
    if f"<CW-DIFF-STYLE family=\"{recipe}\">" in html:
        return {"lesson": lesson, "ok": True, "recipe": recipe, "skipped": True}
    # 在最后一个 </style> 前注入 recipe CSS
    idx = html.rfind("</style>")
    if idx < 0:
        return {"lesson": lesson, "ok": False, "err": "no style block"}
    css = recipe_css(recipe)
    html = html[:idx] + css + html[idx:]
    # 注入 style_family 标记
    marker = "<!-- CW-STYLE-FAMILY:" + recipe + " -->"
    if "CW-STYLE-FAMILY" not in html:
        html = html.replace("</head>", marker + "</head>")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return {"lesson": lesson, "ok": True, "recipe": recipe, "skipped": False}

def verify_no_3repeat():
    seq = [RECIPE_MAP[i] for i in range(1, 27)]
    for i in range(len(seq)-2):
        if seq[i] == seq[i+1] == seq[i+2]:
            return False, i+1
    return True, None

def main():
    ok, pos = verify_no_3repeat()
    print(f"连续三课不重复检查: {'PASS' if ok else 'FAIL at位置'+str(pos)}")
    counts = {}
    for r in RECIPE_MAP.values():
        counts[r] = counts.get(r, 0) + 1
    print("recipe 计数:", counts)
    results = []
    for i in range(1, 27):
        r = process_lesson(i)
        results.append(r)
        status = "OK" if r["ok"] else "FAIL"
        extra = f" ({r['recipe']})" if r.get("recipe") else ""
        skip = " [已注入跳过]" if r.get("skipped") else ""
        print(f"  L{i:02d}: {r['recipe']} {status}{skip}")
    with open(os.path.join(BASE, "00_结果_差异化分配.json"), "w", encoding="utf-8") as f:
        json.dump({"map": RECIPE_MAP, "results": results}, f, ensure_ascii=False, indent=2)
    print("\n完成。分配表已存 00_结果_差异化分配.json")

if __name__ == "__main__":
    main()