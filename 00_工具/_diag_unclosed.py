import re
b=r'D:\英语教学\邓兴华'
h=open(b+r'\第20课时\课件成品_网页PPT\第20课时_课件_中等.html',encoding='utf-8').read()
print('div open',len(re.findall(r'<div\b',h)),'close',len(re.findall(r'</div>',h)))
tag_re=re.compile(r'<(/)?([a-zA-Z][a-zA-Z0-9]*)([^>]*?)(/?)>',re.S)
stack=[];in_s=in_y=False
for m in tag_re.finditer(h):
    cl,tag,attrs,sc=m.group(1),m.group(2).lower(),m.group(3),m.group(4)
    if tag=='script': in_s=not cl; continue
    if tag=='style': in_y=not cl; continue
    if in_s or in_y: continue
    if not cl and not sc:
        stack.append((tag,attrs,m.start()))
    elif cl:
        if tag=='div' and stack:
            for i in range(len(stack)-1,-1,-1):
                if stack[i][0]=='div': del stack[i]; break
unclosed=[s for s in stack if s[0]=='div']
print('unclosed divs:',len(unclosed))
for s in unclosed:
    pos=s[2]
    print('---',h[pos:pos+90].replace('\n','\\n'))