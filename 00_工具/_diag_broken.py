import re
b=r'D:\英语教学\邓兴华'
for L,pos in ((16,80592),(17,99495)):
    h=open(b+(r'\第%d课时\课件成品_网页PPT\第%d课时_课件_中等.html'%(L,L)),encoding='utf-8').read()
    qs=h.rfind('<div class="quiz-q"',0,pos)
    print('='*20,'L%d broken quiz-q'%L,'='*20)
    # print from the broken attr to the matching close
    print(h[qs:qs+700])
    print()