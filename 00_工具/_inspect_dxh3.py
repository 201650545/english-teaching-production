# -*- coding: utf-8 -*-
import re
d = open(r"D:\英语教学\邓兴华\第13课时\课件成品_网页PPT\第13课时_课件_中等.html", encoding="utf-8").read()
class_count = {}
for cls in re.findall(r'class="([^"]+)"', d):
    for c in cls.split():
        class_count[c] = class_count.get(c, 0) + 1
# print counts sorted
for c, n in sorted(class_count.items(), key=lambda x:-x[1]):
    if 5 < n < 400:
        print("%4d %s" % (n, c))