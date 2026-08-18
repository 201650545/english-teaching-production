# -*- coding: utf-8 -*-
import re
for n in range(16, 21):
    p = 'D:/英语教学/邓兴华/第%02d课时/课件成品_网页PPT/第%02d课时_课件_中等.html' % (n, n)
    html = open(p, encoding='utf-8').read()
    patterns = {
        'interacdata': r'data-interacdata-interaction-type',
        'idata': r'data-idata-interaction-type',
        'tdatainteraction': r'data-interaction-tdata',
        'sdata': r'data-interaction-type="sdata',
        'single_data': r'data-interaction-type="single_data',
        'fillin_datadata': r'data-interaction-type="fill_in" datadata',
        'fillin_data': r'data-interaction-type="fill_in"data',
    }
    print('==== L%d ====' % n)
    for name, pat in patterns.items():
        c = len(re.findall(pat, html))
        if c:
            print('  %s: %d' % (name, c))
    print('  data-question-id= count:', len(re.findall(r'data-question-id=', html)))
    print('  data-interaction-item= count:', len(re.findall(r'data-interaction-item=', html)))
    print('  quiz-container div:', html.count('quiz-container'))
    print('  quiz-q div:', len(re.findall(r'<div class="quiz-q"', html)))
    print('  quiz-opt count:', len(re.findall(r'class="quiz-opt"', html)))
    print('  fill-input count:', len(re.findall(r'class="fill-input"', html)))
    print('  drag-container:', html.count('drag-container'))
    print('  link-container:', html.count('link-container'))
    print('  order-container:', html.count('order-container'))
    print('  CW-INTERACTION-CONTRACT:', html.count('CW-INTERACTION-CONTRACT'))