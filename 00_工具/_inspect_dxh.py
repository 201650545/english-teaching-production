# -*- coding: utf-8 -*-
import re
for n in (14, 15):
    p = r"D:\英语教学\邓兴华\第%d课时\课件成品_网页PPT\第%d课时_课件_中等.html" % (n, n)
    d = open(p, encoding="utf-8").read()
    print("=== L%d len=%d ===" % (n, len(d)))
    print("slide< count:", d.count("<div class=\"slide"))
    print("slide-content:", d.count("slide-content"))
    print("data-page:", d.count("data-page"))
    print("data-section:", d.count("data-section"))
    print("class=slide\" :", d.count("class=\"slide\""))
    # find first occurrence of 'slide'
    i = d.find("slide")
    print("first 'slide' context:", d[i-60:i+80].replace("\n"," ")[:200])
    # find any div with class containing slide
    for m in re.finditer(r'<div[^>]*slide[^>]*>', d):
        print("DIV:", m.group(0)[:120])
        break