# -*- coding: utf-8 -*-
import re, os
base = r"d:\英语教学\李民宪"
for n in [1,6,7,8,9,10]:
    p = os.path.join(base, "第%02d课时" % n, "课件成品_网页PPT", "第%02d课时_课件_培优.html" % n)
    if not os.path.exists(p):
        print("L%02d: MISSING" % n); continue
    d = open(p, encoding="utf-8").read()
    ids = [int(x) for x in re.findall(r'id="page(\d+)"', d)]
    size = os.path.getsize(p)
    print("L%02d pages=%d size=%dKB" % (n, (max(ids) if ids else 0), size//1024))