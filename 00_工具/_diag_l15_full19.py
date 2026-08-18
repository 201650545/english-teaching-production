# -*- coding: utf-8 -*-
import re
path = r"D:\英语教学\邓兴华\第15课时\课件成品_网页PPT\第15课时_课件_中等.html"
src = open(path, encoding="utf-8").read()
pages = list(re.finditer(r'<div class="page(?: active)?" id="page(\d+)"', src))

def get_page(n):
    for pi, m in enumerate(pages):
        if m.group(1) == str(n):
            start = m.start()
            end = pages[pi+1].start() if pi+1 < len(pages) else len(src)
            return src[start:end], start
    return None, None

seg, start = get_page(19)
print("=== page19 full (segment offset from page start) ===")
# print with a live div-depth trace per line region
lines = re.split(r'(<div\b|</div>)', seg)
depth = 0
buf = ""
counts_open = 0
counts_close = 0
for tok in lines:
    if tok == "<div":
        counts_open += 1
        depth += 1
    elif tok == "</div>":
        counts_close += 1
        depth -= 1
print("total <div: %d  </div>: %d  end depth: %d" % (counts_open, counts_close, depth))

# Print each <div ...> and </div> token with running depth to spot unclosed
re_tok = re.compile(r'<div\b[^>]*>|</div>')
pos = 0
depth = 0
for m in re_tok.finditer(seg):
    t = m.group(0)
    ch = t[1:4]
    if ch == "div" and not t.startswith('</'):
        depth += 1
        label = "OPEN  " + t[:60]
    else:
        depth -= 1
        label = "CLOSE " + t
    rel = m.start()
    ctx = seg[max(0, m.start()-40):m.start()+10].replace("\n", " ")
    print("d=%2d %s" % (depth, label))
print("FINAL depth:", depth)