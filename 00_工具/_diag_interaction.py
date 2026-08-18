# -*- coding: utf-8 -*-
import re, sys, json
base = r'D:\英语教学\邓兴华'
courses = {
    16: '第16课时\课件成品_网页PPT\第16课时_课件_中等.html',
    17: '第17课时\课件成品_网页PPT\第17课时_课件_中等.html',
    18: '第18课时\课件成品_网页PPT\第18课时_课件_中等.html',
    19: '第19课时\课件成品_网页PPT\第19课时_课件_中等.html',
    20: '第20课时\课件成品_网页PPT\第20课时_课件_中等.html',
}
CHOICE={'single_choice','multiple_choice','true_false'}
HOT={'grammar','vocab','drill','extend','diagnosis'}
out=[]
for L, rel in courses.items():
    p = base + '\\' + rel
    h = open(p, encoding='utf-8').read()
    # find quiz-q containers
    items=[]
    for m in re.finditer(r'<div class="quiz-q"[^>]*data-question-id="([^"]*)"[^>]*>', h):
        qid=m.group(1)
        # metadata
        tag=m.group(0)
        def ga(name):
            mm=re.search(name+r'="([^"]*)"', tag)
            return mm.group(1) if mm else ''
        itype=ga('data-interaction-type')
        act=ga('data-action-type')
        sec=ga(r'data-section')
        kid=ga('data-knowledge-id')
        cog=ga('data-cognitive-level')
        # DOM: does this container have quiz-opt?
        # find container end roughly
        end=h.find('</div>', m.end())
        snippet=h[m.start():m.end()+400]
        has_opt='quiz-opt' in snippet or 'quiz-opt' in h[m.start():m.start()+600]
        items.append((qid,itype,act,sec,kid,cog,has_opt))
    out.append("=== L%d: %d quiz-q containers ===" % (L, len(items)))
    from collections import Counter
    c_itype=Counter(x[1] for x in items)
    c_act=Counter(x[2] for x in items)
    c_sec=Counter(x[3] for x in items)
    c_msai=Counter(x[1] for x in items if not x[1] or x[1]=='unknown')
    out.append("  interaction_type: %s" % dict(c_itype))
    out.append("  action_type: %s" % dict(c_act))
    out.append("  section: %s" % dict(c_sec))
    # counts
    total=len(items)
    choices=sum(1 for x in items if x[1] in CHOICE)
    hot=[x for x in items if x[3] in HOT]
    hotch=sum(1 for x in hot if x[1] in CHOICE)
    out.append("  choices=%d/%d (%.1f%%)  hot_choices=%d/%d (%.1f%%)" % (choices,total,100*choices/total if total else 0, hotch,len(hot),100*hotch/len(hot) if hot else 0))
    # missing metadata
    missing_meta=0
    for x in items:
        if not x[1] or x[1]=='unknown' or not x[2] or x[2]=='unknown' or not x[4] or x[4]=='unknown':
            missing_meta+=1
    out.append("  items missing metadata: %d" % missing_meta)
    out.append("  has_opt items: %d" % sum(1 for x in items if x[6]))
    # pagination exemption
    out.append("  drag-container present: %s link-container: %s order-container: %s" % (
        'drag-container' in h, 'link-container' in h, 'order-container' in h))
    out.append("  click handler has drag exempt: %s" % ("e.target.closest('.drag-container')" in h))
sys.stdout.buffer.write(("\n".join(out)).encode('utf-8','replace'))