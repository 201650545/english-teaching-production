import re
b=r'D:\英语教学\邓兴华'
h=open(b+r'\第17课时\课件成品_网页PPT\第17课时_课件_中等.html',encoding='utf-8').read()
# find data-question-id that are NOT inside quiz-q (extra items causing VIS-610)
# find all elements with data-question-id and their open tag
for m in re.finditer(r'data-question-id="([^"]*)"',h):
    qid=m.group(1)
    # find the enclosing tag start
    lt=h.rfind('<',0,m.start())
    tagstart=h.rfind('<div',0,m.start())
    # is this inside a quiz-q? check nearest quiz-q open and its close
    qq=h.rfind('<div class="quiz-q"',0,m.start())
    gt=h.find('>',qq) if qq!=-1 else -1
    if qq==-1 or not (qq<m.start()<gt):
        # this data-question-id is NOT in a quiz-q open tag
        # print the tag containing it
        print('NON-quiz-q data-question-id:',qid)
        print('   ',h[tagstart:tagstart+250].replace('\n','\\n'))
        print()