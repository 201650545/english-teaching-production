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
            return src[start:end]
    return None

# Show tail of page19 (6 open / 5 close) — last 600 chars
seg = get_page(19)
print("=== page19 tail ===")
print(seg[-700:])

# Show tail of page3 (230 open/206 close, +24) — last 1500 chars
seg3 = get_page(3)
print("\n=== page3 tail ===")
print(seg3[-1500:])

# Show tail of page2 (+2)
seg2 = get_page(2)
print("\n=== page2 tail ===")
print(seg2[-900:])