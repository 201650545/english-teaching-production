# -*- coding: utf-8 -*-
import re
p = r"d:\英语教学\李民宪\第06课时\课件成品_网页PPT\第06课时_课件_培优.html"
d = open(p, encoding="utf-8").read()
onclick = sorted(set(re.findall(r'onclick="([A-Za-z_$][\w$]*)\s*\(', d)))
print("onclick函数(%d): %s" % (len(onclick), ", ".join(onclick)))
# 所有 function 定义
fns = sorted(set(re.findall(r'function\s+([A-Za-z_$][\w$]*)\s*\(', d)))
print("定义函数(%d): %s" % (len(fns), ", ".join(fns)))