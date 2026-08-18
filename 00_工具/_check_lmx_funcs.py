# -*- coding: utf-8 -*-
import re, os, json

base = r"d:\英语教学\李民宪"
lessons = [6,7,8,9,10]
out = {}
for n in lessons:
    path = os.path.join(base, "第%02d课时" % n, "课件成品_网页PPT", "第%02d课时_课件_培优.html" % n)
    html = open(path, encoding="utf-8").read()
    pages = re.findall(r'<div class="page(?: active)?" id="([^"]+)"', html)
    n_pages = len(pages)
    size = len(html.encode("utf-8"))
    onclick_fns = re.findall(r'onclick="(?:event\.stopPropagation\(\);\s*)?([A-Za-z_$][A-Za-z0-9_$]*)\s*\(', html)
    fns = sorted(set(onclick_fns))
    defs = set(re.findall(r'\bfunction\s+([A-Za-z_$][A-Za-z0-9_$]*)\s*\(', html))
    defs |= set(re.findall(r'([A-Za-z_$][A-Za-z0-9_$]*)\s*[:=]\s*function\s*\(', html))
    defs |= set(re.findall(r'([A-Za-z_$][A-Za-z0-9_$]*)\s*=\s*(?:\([^)]*\)\s*=>|[A-Za-z_$][A-Za-z0-9_$]*\s*=>)', html))
    missing = [f for f in fns if f not in defs]
    dist_stats = {"A":0,"B":0,"C":0,"D":0,"total":0}
    opts = re.findall(r'<button class="quiz-opt" data-correct="([01])"[^>]*>([A-E])\.', html)
    for isc, letter in opts:
        dist_stats[letter] = dist_stats.get(letter,0)+1
        dist_stats["total"] += 1
    used = {k:v for k,v in dist_stats.items() if k in "ABCD" and v>0}
    max_ratio = max(used.values())/max(dist_stats["total"],1) if dist_stats["total"] else 0
    out[n] = {"pages":n_pages,"size":size,"size_ok":size>=150*1024,
              "fns":fns,"missing":missing,"dist":dist_stats,"max_ratio":round(max_ratio,3)}
    print("="*60)
    print("L%02d: pages=%d size=%d missing_cnt=%d max_ans_ratio=%.3f" % (n,n_pages,size,len(missing),max_ratio))
    print("  missing:", missing if missing else "NONE (all defined)")
    print("  dist:", {k:v for k,v in dist_stats.items() if k in "ABCD"})
    print("  referenced fns(%d): %s" % (len(fns), ", ".join(fns)))

json.dump(out, open(r"d:\英语教学\00_工具\_lmx_funcs_report.json","w",encoding="utf-8"),ensure_ascii=False,indent=1)
print("\nSaved report to d:\\英语教学\\00_工具\\_lmx_funcs_report.json")