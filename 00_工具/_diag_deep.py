# -*- coding: utf-8 -*-
import re, sys
from collections import Counter
base = r'D:\英语教学\邓兴华'
courses = {
    16: '第16课时\课件成品_网页PPT\第16课时_课件_中等.html',
    17: '第17课时\课件成品_网页PPT\第17课时_课件_中等.html',
    18: '第18课时\课件成品_网页PPT\第18课时_课件_中等.html',
    19: '第19课时\课件成品_网页PPT\第19课时_课件_中等.html',
    20: '第20课时\课件成品_网页PPT\第20课时_课件_中等.html',
}
out=[]
for L, rel in courses.items():
    p=base+'\\'+rel
    h=open(p,encoding='utf-8').read()
    out.append("=== L%d ==="%L)
    # all elements carrying data-question-id (any tag)
    qids=re.findall(r'<([a-z][a-z0-9]*)[^>]*data-question-id="[^"]*"', h)
    out.append("  elements with data-question-id: %d -> tags: %s" % (len(qids), dict(Counter(qids))))
    # quiz-question carrying data-question-id (double count)
    dq=len(re.findall(r'<div class="quiz-question[^"]*"[^>]*data-question-id=', h))
    out.append("  quiz-question with data-question-id (double-count): %d" % dq)
    # corrupted patterns
    for pat,name in [(r'data-idata-interaction-type','data-idata-interaction-type'),
                     (r'data-interacdata-interaction-type','data-interacdata...'),
                     (r'data-interaction-tdata','data-interaction-tdata'),
                     (r'data-interaction-type="[a-z_]*"action-type','type-garbled'),
                     (r'data-interaction-type="[^"]*"[^>]*data-','trailing-attr'),
                     (r'quiz-question">[^<]*data-interaction-type','question-text-corrupt')]:
        c=len(re.findall(pat,h))
        if c: out.append("    corrupt[%s]: %d" % (name,c))
    # quiz-opt count
    out.append("  quiz-opt count: %d" % len(re.findall(r'class="quiz-opt"',h)))
    # data-interaction-item count
    out.append("  data-interaction-item=1 count: %d" % len(re.findall(r'data-interaction-item="1"',h)))
    # div balance
    out.append("  div opens=%d closes=%d diff=%d" % (len(re.findall(r'<div\b',h)), len(re.findall(r'</div>',h)), len(re.findall(r'<div\b',h))-len(re.findall(r'</div>',h))))
    # pagination handler exempt
    out.append("  click-handler-drag-exempt: %s" % ("e.target.closest('.drag-container')" in h))
sys.stdout.buffer.write(("\n".join(out)).encode('utf-8','replace'))