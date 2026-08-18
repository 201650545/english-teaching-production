# -*- coding: utf-8 -*-
import re
for n in [16, 17, 20]:
    p = 'D:/英语教学/邓兴华/第%02d课时/课件成品_网页PPT/第%02d课时_课件_中等.html' % (n, n)
    html = open(p, encoding='utf-8').read()
    print('======= L%d ======' % n)
    # 找出含 data-interaction dc 或损坏模式的 quiz-container 开标签
    # 利用 quiz-container 开标签直到第一个 > 
    for m in re.finditer(r'<div class="quiz-container"', html):
        start = m.start()
        end = html.find('>', start)
        tag = html[start:end+1]
        # 只显示损坏的（含 data-interaction-type 但缺 data-question-id 正规形式或含奇怪后缀）
        print('  [' + str(len(tag)) + ']', tag.replace('\n','\\n'))
    print()