import re
b=r'D:\英语教学\邓兴华'
for L in (17,20):
    h=open(b+(r'\第%d课时\课件成品_网页PPT\第%d课时_课件_中等.html'%(L,L)),encoding='utf-8').read()
    print('='*25,'L%d'%L,'='*25)
    # VIS-615: > data-interaction-item= leak
    for m in re.finditer(r'> data-interaction-item=',h):
        print('LEAK > data-interaction-item= @',m.start())
        print('   ',h[m.start()-120:m.start()+120].replace('\n','\\n'))
    # data-interaction-item not inside quiz-q open tag
    for m in re.finditer(r'data-interaction-item=',h):
        qq=h.rfind('<div class="quiz-q"',0,m.start())
        gt=h.find('>',qq) if qq!=-1 else -1
        if qq==-1 or not (qq<m.start()<gt):
            print('data-interaction-item NOT in quiz-q tag @',m.start())
            lt=h.rfind('<div',0,m.start())
            print('   ',h[lt:lt+200].replace('\n','\\n'))
    # broken interaction-type value
    for m in re.finditer(r'data-interaction-type="[^"]* data-',h):
        print('BROKEN interaction-type @',m.start(),':',m.group(0))
    print()