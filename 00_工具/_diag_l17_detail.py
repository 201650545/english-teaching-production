# -*- coding: utf-8 -*-
import re
base=r'D:\英语教学\邓兴华'
h=open(base+r'\第17课时\课件成品_网页PPT\第17课时_课件_中等.html',encoding='utf-8').read()
print("=== L17: all data-interaction-item occurrences context ===")
for m in re.finditer(r'data-interaction-item=',h):
    s=max(0,m.start()-120); e=m.start()+60
    ctx=h[s:e].replace('\n',' ')
    print("  ...",ctx,"...")

print("\n=== L17: data-question-id open tags (non quiz-q class) ===")
for m in re.finditer(r'<([a-z][a-z0-9]*)\s[^>]*data-question-id=',h):
    tag=h[m.start():m.end()+80]
    cls=re.search(r'class="([^"]*)"',tag)
    print("  tag=%s class=%s"%(m.group(1), cls.group(1) if cls else None))

print("\n=== L17: quiz-q tag samples (first 3) ===")
for m in list(re.finditer(r'<div class="quiz-q"[^>]*>',h))[:3]:
    print("  ",m.group(0)[:200])

print("\n=== L17: page-turn click handler (search addEventListener) ===")
for m in re.finditer(r"addEventListener\('click'",h):
    seg=h[m.start()-80:m.start()+400]
    print(seg[:480].replace('\n',' '))
    print("  ---")