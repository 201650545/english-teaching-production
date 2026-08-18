# -*- coding: utf-8 -*-
import re
for n in [16, 17, 18, 20]:
    p = 'D:/英语教学/邓兴华/第%02d课时/课件成品_网页PPT/第%02d课时_课件_中等.html' % (n, n)
    html = open(p, encoding='utf-8').read()
    print('======= L%d ======' % n)
    # 捕获所有 quiz 容器开标签（quiz-q / quiz-container，含 data-question-id 或 data-interaction-item）
    for m in re.finditer(r'<div class="(quiz-q|quiz-container)"[^>]*>', html):
        tag = m.group(0)
        had = []
        for attr in ['data-question-id','data-knowledge-id','data-section','data-template-id',
                     'data-interaction-type','data-action-type','data-cognitive-level','data-scorable','data-qid']:
            had.append(attr + ('=Y' if ('%s=' % attr) in tag else '=N'))
        if len(tag) > 400:
            tag = tag[:400] + '...'
        print('  ', tag)
    print()