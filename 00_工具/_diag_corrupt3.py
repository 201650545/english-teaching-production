import re, os
base = r'D:\英语教学\邓兴华'
for lesson in ['第16课时','第17课时']:
    path = os.path.join(base, lesson, '课件成品_网页PPT', lesson + '_课件_中等.html')
    h = open(path, encoding='utf-8').read()
    print('='*20, lesson, '='*20)
    for m in re.finditer(r'<div class="quiz-(?:q|container)"', h):
        start = m.start(); end = h.find('>', start)
        t = h[start:end+1]
        if 'data-interaction-type' in t and ('data-interacdata' in t or 'data-idata' in t or 'data-interaction-tdata' in t or 'data-interaction-type="s' in t or 'data-interaction-type="single_' in t or 'data-interaction-type="fill_in"' in t):
            print(t)
            print('---')