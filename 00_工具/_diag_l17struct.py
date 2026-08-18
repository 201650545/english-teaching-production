# -*- coding: utf-8 -*-
import re
base=r'D:\英语教学\邓兴华'
h=open(base+r'\第17课时\课件成品_网页PPT\第17课时_课件_中等.html',encoding='utf-8').read()
# find one single_choice quiz-q full block
print("=== L17 one single_choice quiz-q (full block) ===")
for m in re.finditer(r'<div class="quiz-q"[^>]*data-interaction-type="single_choice"[^>]*>',h):
    start=m.start()
    # find matching close: count divs
    seg=h[start:]
    depth=0; i=0; end=None
    # simple: cut 1200 chars
    print(seg[:1200])
    print("----END SC----")
    break
print("\n=== L17 one fill_in quiz-q (full block) ===")
for m in re.finditer(r'<div class="quiz-q"[^>]*data-interaction-type="fill_in"[^>]*>',h):
    seg=h[m.start():]
    print(seg[:900])
    print("----END FI----")
    break