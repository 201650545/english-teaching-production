import re
from collections import Counter
b=r'D:\英语教学\邓兴华'
for L in (16,17,20):
    h=open(b+(r'\第%d课时\课件成品_网页PPT\第%d课时_课件_中等.html'%(L,L)),encoding='utf-8').read()
    print('='*30,'L%d'%L,'='*30)
    # interaction types from quiz-q
    it=Counter()
    act=Counter()
    sec=Counter()
    for m in re.finditer(r'<div class="quiz-q"[^>]*>',h):
        tag=m.group(0)
        def ga(n):
            mm=re.search(n+r'="([^"]*)"',tag); return mm.group(1) if mm else '?'
        it[ga('data-interaction-type')]+=1
        act[ga('data-action-type')]+=1
        sec[ga('data-section')]+=1
    print('interaction_type:',dict(it))
    print('action_type:',dict(act))
    print('section:',dict(sec))
    tot=sum(it.values())
    choices=sum(v for k,v in it.items() if k in ('single_choice','multiple_choice','true_false','choice'))
    fill=sum(v for k,v in it.items() if k in ('fill_in','write'))
    print('total quiz-q=%d choices=%d (%.1f%%) fill/write=%d'%(tot,choices,100*choices/tot if tot else 0,fill))
    # broken: premature </div> after question text
    broken=len(re.findall(r'data-scorable="true">[^<]*?</div>\s*<div class="quiz-options"',h))
    print('broken premature-close quiz-q:',broken)
    # link/order/drag containers
    for c in ('link-container','order-container','drag-container','match-container'):
        print(c,':',len(re.findall(r'class="[^"]*\b'+c+r'\b"',h)))
    # pagination exemption
    print('has drag exempt:', "e.target.closest('.drag-container')" in h, 'link:', "e.target.closest('.link-container')" in h,'order:', "e.target.closest('.order-container')" in h)
    print('has click-zone:', bool(re.search(r'click-zone',h)))
    print()