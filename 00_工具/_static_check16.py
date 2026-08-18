# -*- coding: utf-8 -*-
"""L16 课件静态完整性核验：逐页非空、双契约、交互函数、IndexedDB、音效、翻页豁免。"""
import re

html = open(r"D:\英语教学\邓兴华\第16课时\课件成品_网页PPT\第16课时_课件_中等.html", encoding="utf-8").read()

# 1. 逐页核验：page-id 与页内容
pages = re.findall(r'<div class="page[^"]*"[^>]*data-page-id="(\d+)"[^>]*>(.*?)(?=<div class="page|</body>)', html, re.S)
print("页面总数(data-page-id):", len(pages))
empty = []
for pid, body in pages:
    txt = re.sub(r"<[^>]+>", "", body).strip()
    n = len(txt)
    if n < 30:
        empty.append((pid, n))
print("空/过短页(内容<30字):", empty if empty else "无")

# 2. 双契约标记
print("CW-VISUAL-CONTRACT:1 =", html.count("CW-VISUAL-CONTRACT:1"))
print("CW-INTERACTION-CONTRACT:1 =", html.count("CW-INTERACTION-CONTRACT:1"))
print("CW-CSS-EXTRA =", html.count("CW-CSS-EXTRA") // 2)

# 3. 交互函数定义
for fn in ["checkOpt", "fillCheck", "dragSubmit", "orderCheck", "matchPick", "flipCard"]:
    print("fn %-12s %s" % (fn, ("function %s" % fn) in html))

# 4. 音效
for snd in ["playCorrect", "playError", "playPageTurn"]:
    print("snd %-14s %s" % (snd, snd in html))

# 5. IndexedDB 落库
for kw in ["indexedDB", "openDB", "onupgradeneeded", "objectStore", "put("]:
    print("IDB %-16s %s" % (kw, html.count(kw)))

# 6. 翻页豁免容器
for c in ["quiz-container", "drag-container", "link-container", "order-container"]:
    print("豁免 %-16s %s" % (c, html.count(c)))

# 7. 左右半屏翻页 + 键盘
print("半屏翻页 left/right:", html.count("pageTurn") + html.count("halfScreen"))
print("键盘箭头:", "ArrowLeft" in html or "arrowleft" in html.lower())

# 8. 红金主题
print("红金 E63946:", html.count("E63946"), "| 强调 FFD700:", html.count("FFD700"), "| 背景 FFF8F0:", html.count("FFF8F0"))