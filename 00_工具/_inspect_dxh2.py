# -*- coding: utf-8 -*-
import re
for n in (14, 15):
    p = r"D:\英语教学\邓兴华\第%d课时\课件成品_网页PPT\第%d课时_课件_中等.html" % (n, n)
    d = open(p, encoding="utf-8").read()
    print("=== L%d ===" % n)
    # split like transform does
    parts = re.split(r'<div class="slide\s', d)
    print("parts count:", len(parts))
    # print first 3 parts' content-beginning
    for i, part in enumerate(parts[1:3]):
        print("--- part", i+1, "head ---")
        print(part[:300].replace("\n"," "))
    # within a part, find inner container class
    if parts[1:]:
        inner = parts[1]
        # find all class="..." near start
        for m in re.finditer(r'class="([^"]*)"', inner[:2000]):
            pass
        # print first few div opens
        opens = re.findall(r'<div[^>]*>', inner[:1500])
        for o in opens[:6]:
            print("OPEN:", o[:90])