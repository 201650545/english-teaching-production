# -*- coding: utf-8 -*-
import os, re, json
base = r"d:\英语教学\李民宪"
print("=== 1. 蓝图 ===")
for n in range(6,11):
    p = os.path.join(base, "内容蓝图", "单课", "第%02d课_内容蓝图.md" % n)
    print("蓝图 L%02d: %s %s" % (n, "存在" if os.path.exists(p) else "缺失", str(os.path.getsize(p))+"B" if os.path.exists(p) else ""))

print("=== 2. 课件 ===")
for n in range(6,11):
    p = os.path.join(base, "第%02d课时" % n, "课件成品_网页PPT", "第%02d课时_课件_培优.html" % n)
    if not os.path.exists(p):
        print("课件 L%02d: 缺失" % n); continue
    d = open(p, encoding="utf-8").read()
    ids = [int(x) for x in re.findall(r'id="page(\d+)"', d)]
    pages = max(ids) if ids else 0
    size = os.path.getsize(p)
    print("课件 L%02d: pages=%d size=%dkB contract=%s" % (n, pages, size//1024, "CW-VISUAL-CONTRACT:1" in d))

print("=== 3. 练习 ===")
for n in range(6,11):
    p = os.path.join(base, "第%02d课时" % n, "第%02d课时_配套练习_培优.docx" % n)
    print("练习 L%02d: %s %s" % (n, "存在" if os.path.exists(p) else "缺失", str(os.path.getsize(p))+"B" if os.path.exists(p) else ""))

print("=== 4. 契约 6 件套 ===")
names = ["1_课程概要.md","2_大纲脚本.md","3_演讲意图.md","4_素材清单.md","5_页面规划.json","6_动效与素材.json"]
for n in range(6,11):
    folder = os.path.join(base, "第%02d课时" % n, "契约")
    ok, jsons = 0, []
    for nm in names:
        p = os.path.join(folder, nm)
        if os.path.exists(p):
            ok += 1
            if nm.endswith(".json"):
                try:
                    json.load(open(p, encoding="utf-8"))
                    jsons.append(nm+":OK")
                except Exception as e:
                    jsons.append(nm+":BAD")
    print("契约 L%02d: %d/6 齐全; JSON=%s" % (n, ok, jsons))