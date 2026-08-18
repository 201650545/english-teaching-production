import re
b=r'D:\英语教学\邓兴华'
h=open(b+r'\第20课时\课件成品_网页PPT\第20课时_课件_中等.html',encoding='utf-8').read()
sc=len(re.findall(r'<div class="quiz-q"[^>]*data-interaction-type="single_choice"[^>]*>',h))
fi=len(re.findall(r'<div class="quiz-q"[^>]*data-interaction-type="fill_in"[^>]*>',h))
print('single_choice quiz-q:',sc,'fill_in quiz-q:',fi)
# list first few single_choice quiz-q question-ids
for m in re.finditer(r'<div class="quiz-q"[^>]*data-interaction-type="single_choice"[^>]*>',h):
    tag=m.group(0)
    q=re.search(r'data-question-id="([^"]*)"',tag)
    print('  ',q.group(1) if q else '?')