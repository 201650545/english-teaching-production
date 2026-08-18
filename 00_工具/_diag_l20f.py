import re
b=r'D:\英语教学\邓兴华'
h=open(b+r'\第20课时\课件成品_网页PPT\第20课时_课件_中等.html',encoding='utf-8').read()
tag_re = re.compile(r'<(/)?([a-zA-Z][a-zA-Z0-9]*)([^>]*?)(/?)>', re.S)
stack=[]  # (tagname, attrs, pos)
in_script=in_style=False
for m in tag_re.finditer(h):
    closing,tagname,attrs,selfclose=m.group(1),m.group(2).lower(),m.group(3),m.group(4)
    if tagname=='script': in_script=not closing; continue
    if tagname=='style': in_style=not closing; continue
    if in_script or in_style: continue
    if not closing and not selfclose:
        stack.append((tagname,attrs,m.start()))
    elif closing:
        if tagname=='div' and stack:
            # pop the last div
            for i in range(len(stack)-1,-1,-1):
                if stack[i][0]=='div':
                    del stack[i]; break
        elif tagname=='div':
            pass
print('remaining open divs at EOF:',sum(1 for s in stack if s[0]=='div'))
unclosed=[s for s in stack if s[0]=='div']
for s in unclosed[-10:]:
    pos=s[2]
    print('--- unclosed div @',pos,'---')
    print(h[pos:pos+120].replace('\n','\\n'))
    print()