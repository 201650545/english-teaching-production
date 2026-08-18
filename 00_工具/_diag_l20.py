import re, collections
b=r'D:\英语教学\邓兴华'
h=open(b+r'\第20课时\课件成品_网页PPT\第20课时_课件_中等.html',encoding='utf-8').read()
print('div open',len(re.findall(r'<div\b',h)),'close',len(re.findall(r'</div>',h)))
print('quiz-q with data-question-id',len(re.findall(r'<div class="quiz-q"[^>]*data-question-id',h)))
print('data-interaction-item= count',len(re.findall(r'data-interaction-item=',h)))
print('leaked > data-interaction-item=',len(re.findall(r'> data-interaction-item=',h)))
print('quiz-opt count',len(re.findall(r'class="quiz-opt"',h)))
print('data-question-id count',len(re.findall(r'data-question-id=',h)))
m=re.search(r'<div class="quiz-q"[^>]*>',h)
print('SAMPLE quiz-q tag:',m.group(0) if m else None)
leaked=[]
for m in re.finditer(r'data-interaction-item=',h):
    start=h.rfind('<div class="quiz-q"',0,m.start())
    if start==-1:
        leaked.append(m.start())
    else:
        gt=h.find('>',start)
        if not (start < m.start() < gt):
            leaked.append(m.start())
print('data-interaction-item NOT inside quiz-q tag:',len(leaked))
print('total quiz-q divs',len(re.findall(r'class="quiz-q"',h)))
missing_meta=0
for m in re.finditer(r'<div class="quiz-q"[^>]*>',h):
    tag=m.group(0)
    for k in ['data-knowledge-id','data-section','data-template-id','data-interaction-type','data-action-type','data-cognitive-level']:
        if not re.search(re.escape(k)+r'=',tag):
            missing_meta+=1
            break
print('quiz-q missing at least one metadata key:',missing_meta)