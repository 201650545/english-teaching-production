# -*- coding: utf-8 -*-
import re
for n in (15,):
    d = open(r"D:\英语教学\邓兴华\第%d课时\课件成品_网页PPT\第%d课时_课件_中等.html" % (n,n), encoding="utf-8").read()
    cc = {}
    for cls in re.findall(r'class="([^"]+)"', d):
        for c in cls.split():
            cc[c] = cc.get(c,0)+1
    print("=== L%d ===" % n)
    for c,k in sorted(cc.items(), key=lambda x:-x[1]):
        if 3 < k < 300:
            print("%4d %s" % (k,c))