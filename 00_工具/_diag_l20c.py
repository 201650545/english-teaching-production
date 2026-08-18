import re
b=r'D:\英语教学\邓兴华'
h=open(b+r'\第20课时\课件成品_网页PPT\第20课时_课件_中等.html',encoding='utf-8').read()
tag_re = re.compile(r'<(/)?([a-zA-Z][a-zA-Z0-9]*)([^>]*?)(/?)>', re.S)
div_stack=[]
in_script=in_style=False
detached=[]
for m in tag_re.finditer(h):
    closing,tagname,attrs,selfclose=m.group(1),m.group(2).lower(),m.group(3),m.group(4)
    if tagname=='script': in_script=not closing; continue
    if tagname=='style': in_style=not closing; continue
    if in_script or in_style: continue
    if not closing and not selfclose:
        if tagname=='div':
            is_q=bool(re.search(r'\bquiz-q\b',attrs))
            div_stack.append(is_q)
        for tok in ('quiz-opt','fill-input','drag-word'):
            if re.search(r'class="[^"]*\b'+tok+r'\b',attrs or ''):
                if not any(div_stack):
                    detached.append((tok,m.start(),m.group(0)[:80]))
    elif closing:
        if tagname=='div' and div_stack: div_stack.pop()
from collections import Counter
print('detached count:',len(detached))
print('by token:',Counter(t[0] for t in detached))
for tok,pos,gtag in detached[:12]:
    print('---',tok,'@',pos,'---')
    print(h[pos-150:pos+150].replace('\n','\\n'))
    print()