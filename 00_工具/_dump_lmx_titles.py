# -*- coding: utf-8 -*-
import re, os
base = r"d:\英语教学\李民宪"
def dump(n):
    p = os.path.join(base, "第%02d课时" % n, "课件成品_网页PPT", "第%02d课时_课件_培优.html" % n)
    d = open(p, encoding="utf-8").read()
    # 段落标题：section-head 的文本 或 每页 page-title
    titles = re.findall(r'class="page-title">([^<]+)<', d)
    subs = re.findall(r'class="page-subtitle">([^<]+)<', d)
    print("="*20, "L%02d" % n, "pages from titles:", len(titles))
    for i,(t,s) in enumerate(zip(titles,subs),1):
        print("%2d. %s | %s" % (i, t, s))
dump(1)
dump(6)