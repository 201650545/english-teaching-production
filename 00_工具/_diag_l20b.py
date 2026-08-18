import re
b=r'D:\英语教学\邓兴华'
h=open(b+r'\第20课时\课件成品_网页PPT\第20课时_课件_中等.html',encoding='utf-8').read()

def dump(desc, region):
    print('='*20, desc, '='*20)
    print(h[region:region+400].replace('\n','\\n'))

# 1. leaked data-interaction-item not inside quiz-q
for m in re.finditer(r'data-interaction-item=',h):
    start=h.rfind('<div class="quiz-q"',0,m.start())
    if start==-1:
        dump('LEAKED data-interaction-item (no quiz-q before)', m.start()-200); break
    else:
        gt=h.find('>',start)
        if not (start < m.start() < gt):
            dump('LEAKED data-interaction-item (after quiz-q close)', m.start()-200); break

# 2. data-question-id not in a quiz-q div (the 2 extra)
for m in re.finditer(r'data-question-id=',h):
    start=h.rfind('<div class="quiz-q"',0,m.start())
    gt=h.find('>', start) if start!=-1 else -1
    if start==-1 or not (start < m.start() < gt):
        dump('data-question-id OUTSIDE quiz-q', m.start()-150); print()

# 3. quiz-opt outside quiz-q container
# Build quiz-q spans
opens=sorted([m.start() for m in re.finditer(r'<div class="quiz-q"',h)])
count_out=0
shown=0
for m in re.finditer(r'class="quiz-opt"',h):
    pos=m.start()
    # find innermost enclosing quiz-q: the last quiz-q open before pos that hasn't closed before pos
    enclosed=False
    # find nearest quiz-q open before pos
    cand=[o for o in opens if o<pos]
    if cand:
        # check if within that quiz-q's closing div; approximate by scanning to next quiz-q open or page boundary
        prev=cand[-1]
        # find matching close of prev container - use next quiz-q open OR </div></div></div> pattern
        nxt=pos
        # simple: if there's a quiz-q open between prev and pos, then not directly enclosed
    # Instead, detect: if nearest preceding quiz-q open, and no closing </div>... too complex
    # Use simple heuristic: count opens/closes between prev quiz-q and pos
    sector=h[prev if cand else 0:pos]
    if cand:
        depth=sector.count('<div')-sector.count('</div>')
        if depth>=1:
            enclosed=True
    if not enclosed:
        count_out+=1
        if shown<3:
            dump('quiz-opt OUTSIDE quiz-q', pos-120); print()
            shown+=1
print('quiz-opt outside quiz-q (heuristic):',count_out)

# 4. unclosed divs - find page boundaries
# find <div class="page" regions
pages=[m.start() for m in re.finditer(r'class="page"',h)]
print('page divs:',len(pages))