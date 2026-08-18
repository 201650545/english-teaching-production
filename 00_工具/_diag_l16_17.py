import re
from collections import Counter
b=r'D:\英语教学\邓兴华'
for L in (16,17):
    h=open(b+(r'\第%d课时\课件成品_网页PPT\第%d课时_课件_中等.html'%(L,L)),encoding='utf-8').read()
    print('='*30,'L%d'%L,'='*30)
    # broken interaction tags: value containing ' data-knowledge-id='
    for m in re.finditer(r'data-interaction-type="[^"]* data-knowledge-id=',h):
        print('BROKEN TAG @',m.start())
        # find the quiz-q open
        qs=h.rfind('<div class="quiz-q"',0,m.start())
        print('  quiz-q:',h[qs:m.start()+80].replace('\n','\\n'))
    # find quiz-q tags with garbled interaction-type values
    for m in re.finditer(r'<div class="quiz-q"[^>]*>',h):
        tag=m.group(0)
        if 'data-knowledge-id=' in tag and tag.find('data-knowledge-id=')!=tag.rfind('data-knowledge-id='):
            print('DUP knowledge-id in quiz-q @',m.start(),':',tag[:200])
    # link/order containers
    for c in ('link-container','order-container','drag-container'):
        for m in re.finditer(r'class="[^"]*\b'+c+r'\b"',h):
            seg=h[m.start()-100:m.start()+400]
            print('%s container @ %d: %s'%(c,m.start(),seg.split('>')[0][-200:]))
    print()