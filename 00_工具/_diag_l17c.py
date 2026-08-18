# -*- coding: utf-8 -*-
import re
base=r'D:\英语教学\邓兴华'
h=open(base+r'\第17课时\课件成品_网页PPT\第17课时_课件_中等.html',encoding='utf-8').read()
print("=== L17 link-container full tags ===")
for m in re.finditer(r'<div class="link-container"[^>]*>',h):
    print("  ",m.group(0))
print("\n=== L17 order-container full tags ===")
for m in re.finditer(r'<div class="order-container"[^>]*>',h):
    print("  ",m.group(0))
print("\n=== L17: any element (non div) with data-question-id ===")
for m in re.finditer(r'<([a-z][a-z0-9]*)[^>]*data-question-id=',h):
    print("  tag=%s"%m.group(1))
print("\n=== L17 full click handler ===")
i=h.find("document.addEventListener('click'")
print(h[i:i+1400])