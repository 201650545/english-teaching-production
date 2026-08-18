# -*- coding: utf-8 -*-
import re
html = open(r"D:\英语教学\邓兴华\第16课时\课件成品_网页PPT\第16课时_课件_中等.html", encoding="utf-8").read()
for cls in ["quiz-opt", "fill-input", "drag-container", "link-container", "order-container", "match-", "flip-card", "sort-option", "drop-zone", "choice-btn"]:
    n = html.count('class="%s' % cls) + html.count("class='%s" % cls) + html.count('"%s ' % cls)
    print("class %-16s %d" % (cls, n))
print("--- 关键函数定义 ---")
for fn in ["checkOpt", "fillCheck", "dragSubmit", "dragCheck", "orderCheck", "matchPick", "linkCheck", "flipCard", "playCorrect", "playError", "playPageTurn"]:
    found = ("function %s" % fn) in html or ("%s(" % fn) in html
    print("%-14s %s" % (fn, found))
print("--- 双契约标记 ---")
for m in ["CW-VISUAL-CONTRACT:1", "CW-INTERACTION-CONTRACT:1", "CW-CSS-EXTRA"]:
    print(m, html.count(m))