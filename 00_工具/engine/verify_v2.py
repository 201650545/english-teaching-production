# -*- coding: utf-8 -*-
"""verify_v2 校验器（M4+）：多结构自适应。
支持三种课件契约：
  A. page-id  契约：<div class="page" id="pageN"> + <button class="quiz-opt" data-correct="0|1">A. …
     （许颖嘉 L1-L4 / 新引擎 courseware_engine 产物）
  B. slide    契约：<div class="slide"> + checkQuiz(this,'A','B',…) 字母签名 或 checkQuiz(this,true,…) 布尔签名
     （邓兴华 L01-L15 旧版）
  C. 无标记   契约：无 data-correct / 无 checkQuiz / 无 quiz-opt（页面可翻页但答案不可判）
     （邓兴华部分课 / 李民宪早期课）

硬规则(FAIL即拒收)：体积/页数/div平衡/残留/JS/答案可判性/答案分布无主导字母
软规则(警告)：六色卡丰富度/防越级扫描/页数偏离
用法：python verify_v2.py <html_path> [<html_path2> ...]
"""
import sys, re, os, subprocess, tempfile
# 视觉检查模块（批次2 V1.0）
from verify_visual_v1 import inspect_visual_html, load_visual_contract

RESIDUALS = ["L22_", "clozeTest", "wordMatch", "crossGame", "L22_answers"]
# 防越级名单：2026-08-02 教师决定，比较级/最高级对邓兴华自 L5 起合法（提前教学），
# 故 better/best/worse/worst/more/most 移出；保留将来时/完成时/被动。
FORBIDDEN = ["will ", "be going to", "shall ", "have been", "has been", "is made", "are made"]
RC_CLASSES = ["rc-zhug", "rc-bin", "rc-xing", "rc-ming", "rc-warn", "rc-qita"]

# 页数标准：page-id 契约要求 40-45；slide 契约按旧版 25-35 区间给软警告（不硬 FAIL，因旧课件非 40-45）
PAGE_ID_MIN, PAGE_ID_MAX = 40, 45
SLIDE_MIN, SLIDE_MAX = 25, 60

def _resolve_node():
    """定位 node 可执行文件：优先 playwright driver 目录，其次 PATH。
    Windows 下 subprocess 用裸命令名 'node' 时有 CreateProcess 解析问题，
    故解析为绝对路径以保证稳定。"""
    import shutil
    candidates = []
    # 常见 playwright driver 位置
    rel = os.path.join("Lib", "site-packages", "playwright", "driver", "node.exe")
    for base in (os.path.dirname(sys.prefix) if sys.prefix else "", os.path.dirname(sys.executable)):
        if base:
            candidates.append(os.path.join(base, rel))
    sh = shutil.which("node")
    if sh:
        candidates.append(sh)
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return "node"


def detect_contract(html):
    """自动识别课件契约类型"""
    id_pages = len(re.findall(r'<div class="page[^"]*" id="page\d+"', html)) or \
                len(re.findall(r'id="page\d+"', html))
    # slide 页面容器：<div class="slide"> 或 <div class="slide cover-slide active">（排除 slide-title 等子元素）
    slides = len(re.findall(r'<div class="slide(?:"| )', html))
    quiz_opt_dc = len(re.findall(r'quiz-opt[^>]*data-correct="[01]"', html))
    check_quiz = len(re.findall(r'checkQuiz\(', html))
    data_correct = len(re.findall(r'data-correct="[01]"', html))
    check_opt = len(re.findall(r'checkOpt\(', html))

    if id_pages >= 1 and (quiz_opt_dc >= 1 or check_opt >= 1):
        return "page-id", id_pages, "quiz-opt"
    if slides >= 1:
        # slide 契约：进一步判断答案标记类型
        if check_quiz >= 1:
            # 字母签名 or 布尔签名
            ck_letter = len(re.findall(r"checkQuiz\([^)]*'([A-E])'", html))
            ck_bool = len(re.findall(r"checkQuiz\([^)]*(?:true|false)", html))
            mode = "checkQuiz-letter" if ck_letter > ck_bool else "checkQuiz-bool"
            return "slide", slides, mode
        if data_correct >= 1:
            return "slide", slides, "data-correct"
        return "slide", slides, "none"
    if data_correct >= 1:
        return "page-id", id_pages, "data-correct"
    return "unknown", id_pages or 0, "none"

def extract_answer_dist(html, contract, mode):
    """提取答案字母分布。返回 (dist dict, total, n_correct_questions)"""
    dist = {}
    n_ans = 0
    if contract == "page-id" and mode == "quiz-opt":
        for mm in re.finditer(r'<button class="quiz-opt" data-correct="1"[^>]*>([A-E])\.', html):
            dist[mm.group(1)] = dist.get(mm.group(1), 0) + 1
        n_ans = sum(dist.values())
    elif contract == "slide" and mode == "checkQuiz-letter":
        # checkQuiz(this,'A','B',…) → 第一个引号内为正确项字母
        for mm in re.finditer(r"checkQuiz\(\s*[^,]*,\s*'([A-E])'", html):
            dist[mm.group(1)] = dist.get(mm.group(1), 0) + 1
        n_ans = sum(dist.values())
    elif contract in ("page-id", "slide") and mode == "data-correct":
        # data-correct="1" 且带字母前缀
        for mm in re.finditer(r'data-correct="1"[^>]*>([A-E])\.', html):
            dist[mm.group(1)] = dist.get(mm.group(1), 0) + 1
        n_ans = sum(dist.values())
    # checkQuiz-bool / none：无法解析字母分布
    return dist, n_ans

def count_questions(html, contract, mode):
    """统计可判题目数（用于唯一正确项检查）"""
    if contract == "page-id" and mode == "quiz-opt":
        return len(re.findall(r'<button class="quiz-opt" data-correct="1"', html))
    if contract == "slide" and mode in ("checkQuiz-letter", "checkQuiz-bool"):
        return len(re.findall(r'checkQuiz\(', html))
    if mode == "data-correct":
        return len(re.findall(r'data-correct="1"', html))
    return 0

def check_one(path, force=False):
    html = open(path, encoding="utf-8").read()
    size = len(html.encode("utf-8"))
    contract, npage, mode = detect_contract(html)
    opens = len(re.findall(r'<div\b', html))
    closes = len(re.findall(r'</div>', html))
    resid = {r: html.count(r) for r in RESIDUALS}
    n_q = count_questions(html, contract, mode)

    # JS node --check
    js_ok, js_err = False, ""
    m = re.search(r'<script>(.*?)</script>', html, re.S)
    if m:
        # 写到被检 HTML 同目录（tempfile 短8.3路径 node 无法 lstat，导致误报）
        # 用 ASCII 文件名，避免中文路径问题；校验后删除。
        tmp = os.path.join(os.path.dirname(os.path.abspath(path)), "_v2chk_%d.js" % os.getpid())
        try:
            with open(tmp, "w", encoding="utf-8") as fj:
                fj.write(m.group(1))
            node_exe = _resolve_node()
            r = subprocess.run([node_exe, "--check", tmp], capture_output=True, text=True)
            js_ok = r.returncode == 0
            js_err = r.stderr.strip()
        finally:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass

    # 答案分布
    dist, total_d = extract_answer_dist(html, contract, mode)
    top_share = (max(dist.values()) / total_d) if total_d else 0
    dist_ok = total_d == 0 or top_share <= 0.40

    # 六色卡丰富度
    rc_used = [c for c in RC_CLASSES if ('rule-card ' + c) in html]

    # 防越级扫描
    hits = []
    for kw in FORBIDDEN:
        c = html.count(kw)
        if c:
            hits.append("%s×%d" % (kw.strip(), c))

    # 报告
    print("== verify_v2 校验 ==  %s  [契约:%s] [页数:%d]" % (os.path.basename(path), contract, npage))
    hard = []
    def line(label, ok, detail=""):
        hard.append(ok)
        print("%-12s: %s %s %s" % (label, detail, "✓" if ok else "✗ FAIL", ""))
    # 体积规则：page-id 契约 ≥150KB 硬规则；slide 契约软警告（教师 2026-08-03 决定，与已交付 L01-L03 一致）
    if contract == "page-id":
        line("文件大小", size >= 153600, "%dB (≥153600)" % size)
    elif contract == "slide":
        if size >= 153600:
            print("%-12s: %dB (≥153600) ✓" % ("文件大小", size))
        else:
            print("%-12s: %dB (<153600) ⚠️ slide 契约软警告（见 L01-L03 先例）" % ("文件大小", size))
    else:
        line("文件大小", size >= 153600, "%dB (≥153600)" % size)
    # 页数：page-id 契约 40-45 硬规则；slide 契约软警告
    if contract == "page-id":
        page_ok = PAGE_ID_MIN <= npage <= PAGE_ID_MAX
        line("页数", page_ok, "%d (40-45)" % npage)
    elif contract == "slide":
        in_range = SLIDE_MIN <= npage <= SLIDE_MAX
        if in_range:
            print("%-12s: %d 页 (slide, 25-60 软区间) ✓" % ("页数", npage))
        else:
            print("%-12s: %d 页 (slide, 25-60 软区间) ⚠️ 偏离" % ("页数", npage))
    else:
        print("%-12s: %d (未知契约，跳过页数判定) ⚠️" % ("页数", npage))
    line("div平衡", opens == closes, "%d/%d" % (opens, closes))
    line("残留框架", all(v == 0 for v in resid.values()), str(resid))
    line("JS检查", js_ok, "" if js_ok else js_err)
    # 答案可判性：page-id 须有 quiz-opt；slide 须有 checkQuiz 或 data-correct
    ans_ok = True
    if contract == "page-id" and mode == "none":
        ans_ok = False
    elif contract == "slide" and mode == "none":
        print("%-12s: 无答案标记（checkQuiz/data-correct）⚠️ 需人工确认是否有判题交互" % "答案可判")
    line("答案可判", ans_ok, "%s / %d 题" % (mode, n_q))
    line("答案分布", dist_ok, "%s 最大占比%.0f%%(≤40%%)" % (dist, top_share * 100))
    print("%-12s: %d 个可判题" % ("题量", n_q))
    print("%-12s: 使用 %d/6 色 %s %s" % ("六色卡", len(rc_used), rc_used,
          "⚠️ 偏少" if len(rc_used) < 4 else "✓"))
    print("%-12s: %s" % ("防越级", "命中 " + ", ".join(hits[:6]) + "（需人工复核）" if hits else "未命中 ✓"))
    # A5 性能软检查（A类报告 2026-08-03 落地；仅软警告不 FAIL，阈值为本项目初始参数）
    perf = []
    def _pc(label, n, thr):
        if n > thr:
            perf.append("%s %d 处(>%d)" % (label, n, thr))
    _pc("无限动画", html.count("infinite"), 2)
    # 只计 blur 声明（拼接式 CSS 中 backdrop-filter:none 不算大面积模糊）
    _pc("backdrop-filter:blur", html.count("backdrop-filter:blur") + html.count("-webkit-backdrop-filter:blur"), 2)
    _pc("will-change", html.count("will-change"), 3)
    _pc("getBoundingClientRect", html.count("getBoundingClientRect"), 4)
    if "prefers-reduced-motion" not in html:
        perf.append("缺 prefers-reduced-motion")
    if "/* THEME:" not in html:
        perf.append("缺主题化配色注入(/* THEME:)")
    if perf:
        print("%-12s: %s ⚠️" % ("性能软检查", "; ".join(perf)))
    else:
        print("%-12s: ✓" % ("性能软检查"))
    # P0 兼容软警告（2026-08-03）：检测 checkOpt(event) 旧调用模式。
    # 该模式会传入事件对象而非按钮元素 —— 虽已被 checkOpt 入口兼容保护兜底，
    # 但仍是潜在回归源，须提示改为 checkOpt(this)。
    legacy_ev = html.count("checkOpt(event)")
    if legacy_ev:
        print("%-12s: checkOpt(event) ×%d ⚠️ 建议改为 checkOpt(this)（已由入口兼容保护兜底）" % ("兼容检查", legacy_ev))
    else:
        print("%-12s: 无 checkOpt(event) 旧调用 ✓" % ("兼容检查"))

    # 批次2：视觉检查（CSS完整性 + 视觉软检查 V1.0）
    try:
        v_contract = load_visual_contract()
        v_findings = inspect_visual_html(html, v_contract, contract_mode=contract, force=force)
        v_errors = [f for f in v_findings if f.severity == "ERROR"]
        v_high_warns = [f for f in v_findings if f.severity == "HIGH-WARN"]
        v_warns = [f for f in v_findings if f.severity == "WARN"]
        if v_errors:
            print("%-12s: %d ERROR（风格包规范 2026-08-06：视觉层放开，不阻止交付）" % ("视觉完整性", len(v_errors)))
            for f in v_errors:
                print("  [CSS-%s] %s" % (f.code, f.message))
        if v_high_warns:
            print("%-12s: %d HIGH-WARN" % ("视觉高警告", len(v_high_warns)))
            for f in v_high_warns:
                print("  [%s] %s" % (f.code, f.message))
        if v_warns:
            print("%-12s: %d WARN" % ("视觉软检查", len(v_warns)))
            for f in v_warns[:5]:
                print("  [%s] %s" % (f.code, f.message))
            if len(v_warns) > 5:
                print("  ... 还有 %d 项" % (len(v_warns) - 5))
        else:
            print("%-12s: ✓" % ("视觉检查"))
    except Exception as exc:
        print("%-12s: VIS-CHECK-ERROR %s" % ("视觉检查", exc))
        # 新合同课件若视觉检查异常，按安全原则失败
        if contract == "page-id" and "CW-VISUAL-CONTRACT:1" in html:
            hard.append(False)

    ok = all(hard)
    print("==> %s %s\n" % ("PASS ✅" if ok else "FAIL ❌", path))
    return ok

def main():
    args = sys.argv[1:]
    # --force 通用模式：对任何 HTML 都执行 CSS-I001（忽略 CW-VISUAL-CONTRACT:1 标记门控）
    force = "--force" in args
    args = [a for a in args if a != "--force"]
    if not args:
        print("用法: python verify_v2.py [--force] <html_path> [...]"); sys.exit(2)
    results = [check_one(p, force=force) for p in args]
    mode = "（--force 强制必需视觉层检查）" if force else ""
    print("== 汇总: %d/%d PASS %s ==" % (sum(results), len(results), mode))
    sys.exit(0 if all(results) else 1)

if __name__ == "__main__":
    main()
