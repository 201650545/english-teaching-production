import re
b=r'D:\英语教学\邓兴华'
h=open(b+r'\第20课时\课件成品_网页PPT\第20课时_课件_中等.html',encoding='utf-8').read()
# find the quiz-q open before 60381
pos=60381
# find quiz-q open
qstart=h.rfind('<div class="quiz-q"',0,pos)
# dump from qstart to qstart+1200
print(h[qstart:qstart+1200])