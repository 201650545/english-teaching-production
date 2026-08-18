# -*- coding: utf-8 -*-
import re
h = open(r"D:\英语教学\邓兴华\第16课时\课件成品_网页PPT\第16课时_课件_中等.html", encoding="utf-8").read()
pages = re.findall(r'<div class="page"[^>]*>(.*?)</div>\s*(?=<div class="page"|<script|</body>)', h, re.S)
print("page元素数:", len(pages))
empty = []
for i, b in enumerate(pages, 1):
    t = re.sub(r"<[^>]+>", "", b).strip()
    if len(t) < 30:
        empty.append((i, len(t)))
print("空页:", empty if empty else "无")
for kw in ["gotoPage", "goPage", "showPage", "currentPage", "nav-pill", "navPill", "data-page", "pageTurn", "scrollTo"]:
    print(kw, h.count(kw))