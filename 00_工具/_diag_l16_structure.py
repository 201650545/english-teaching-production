import re
h = open(r'D:\英语教学\邓兴华\第16课时\课件成品_网页PPT\第16课时_课件_中等.html', encoding='utf-8').read()
print('quiz-q count:', len(re.findall(r'class="quiz-q"', h)))
print('quiz-container count:', len(re.findall(r'class="quiz-container"', h)))
print('data-interaction-item count:', len(re.findall(r'data-interaction-item', h)))
print('data-interaction-type count:', len(re.findall(r'data-interaction-type', h)))
print('quiz-opt count:', len(re.findall(r'class="quiz-opt"', h)))
print('data-question-id count:', len(re.findall(r'data-question-id', h)))
print('--- sample data-interaction-item occurrences (context) ---')
for m in list(re.finditer(r'data-interaction-item', h))[:8]:
    print(repr(h[m.start()-70:m.start()+90]))
    print('~~~~~')