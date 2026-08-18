# -*- coding: utf-8 -*-
import re, collections
base=r'D:\英语教学\邓兴华'
def parse_attrs(tag):
    return dict(re.findall(r'([a-zA-Z-]+)="([^"]*)"', tag))
def bal(h):
    return len(re.findall(r'<div\b',h)), len(re.findall(r'</div>',h))
for n in (16,17,20):
    h=open(base+r'\第%d课时\课件成品_网页PPT\第%d课时_课件_中等.html'%(n,n),encoding='utf-8').read()
    print("========== L%d (bytes=%d) =========="%(n,len(h)))
    print("div balance:",bal(h))
    qq=list(re.finditer(r'<div class="quiz-q"[^>]*>',h))
    print("quiz-q count (open tags):",len(qq))
    itype=collections.Counter(); act=collections.Counter(); sec=collections.Counter(); cog=collections.Counter()
    missing_meta=[]
    for m in qq:
        a=parse_attrs(m.group(0))
        it=str(a.get('data-interaction-type','unknown'))
        itype[it]+=1
        act[a.get('data-action-type','unknown')]+=1
        sec[a.get('data-section','unknown')]+=1
        cog[a.get('data-cognitive-level','unknown')]+=1
        miss=[k for k in ('data-knowledge-id','data-section','data-template-id','data-interaction-type','data-action-type','data-cognitive-level') if not a.get(k)]
        if miss:
            missing_meta.append((a.get('data-question-id','?'),miss,a.get('data-sector','')))
    print("interaction-type:",dict(itype))
    print("action-type:",dict(act))
    print("section:",dict(sec))
    print("cognitive:",dict(cog))
    print("quiz-q missing metadata count:",len(missing_meta))
    for qid,miss,_ in missing_meta[:15]:
        print("   qid=%s missing=%s"%(qid,miss))
    print("leaked '> data-interaction-item=' count:",len(re.findall(r'> data-interaction-item=',h)))
    print("quiz-opt button count:",len(re.findall(r'class="quiz-opt"',h)))
    for c in ('drag-container','link-container','order-container'):
        if re.search(r'class="[^"]*\b%s\b'%c,h):
            print("  has",c)
    print("  e.target.closest('.drag-container'):", "e.target.closest('.drag-container')" in h)
    print("  e.target.closest('.link-container'):", "e.target.closest('.link-container')" in h)
    print("  e.target.closest('.order-container'):", "e.target.closest('.order-container')" in h)