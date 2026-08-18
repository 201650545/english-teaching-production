# -*- coding: utf-8 -*-
import os, re
base = r"d:\英语教学\李民宪"
for n in range(6,11):
    p = os.path.join(base, "第%02d课时" % n, "课件成品_网页PPT", "第%02d课时_课件_培优.html" % n)
    d = open(p, encoding="utf-8").read()
    # 提取 onclick="xxx(this)" 函数名
    onclick = set(re.findall(r'onclick="([A-Za-z_$][\w$]*)\s*\(', d))
    # 提取定义：function fn( 或 fn = function 或 window.fn =
    defined = set(re.findall(r'function\s+([A-Za-z_$][\w$]*)\s*\(', d))
    defined |= set(re.findall(r'([A-Za-z_$][\w$]*)\s*=\s*function\s*\(', d))
    defined |= set(re.findall(r'window\.([A-Za-z_$][\w$]*)\s*=\s*function', d))
    missing = sorted(onclick - defined)
    print("L%02d: onclick函数=%d, 定义=%d, 缺失=%s" % (n, len(onclick), len(defined), missing if missing else "无"))
    if missing:
        print("   缺失函数:", missing)