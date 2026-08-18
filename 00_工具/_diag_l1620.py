# -*- coding: utf-8 -*-
import re
base=r'D:\英语教学\邓兴华'
for n in (16,20):
    h=open(base+r'\第%d课时\课件成品_网页PPT\第%d课时_课件_中等.html'%(n,n),encoding='utf-8').read()
    print("========== L%d =========="%n)
    i=h.find("document.addEventListener('click'")
    if i<0: i=h.find("addEventListener('click'")
    print(h[i:i+1200])
    print("\n--- containers with data-question-id ---")
    for m in re.finditer(r'<div class="(drag-container|link-container|order-container)"[^>]*>',h):
        print("  ",m.group(0)[:260])
    print("\n")