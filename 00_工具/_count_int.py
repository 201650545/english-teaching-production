# -*- coding: utf-8 -*-
import re
pats = {
    'quiz-opt(单选)': 'quiz-opt',
    'fill-q(填空)': 'fill-q',
    'fill-input(input)': 'fill-input',
    'drag-word(拖拽)': 'drag-word',
    'order-item(排序)': 'order-item',
    'match-item(连线)': 'match-item',
    'flip-card(翻牌)': 'flip-card',
    'kmap(思维导图)': 'kmap',
    'mind-map': 'mind-map',
}
out = []
for l in [21, 22, 23, 24, 25]:
    p = r'D:\英语教学\邓兴华\第%d课时\课件成品_网页PPT\第%d课时_课件_中等.html' % (l, l)
    s = open(p, encoding='utf-8').read()
    cnt = {k: len(re.findall(v, s)) for k, v in pats.items()}
    types = [k.split('(')[0] for k, c in cnt.items() if c > 0]
    out.append('L%d' % l + ' ' + str(cnt) + ' 动作种类=%d' % len(types))
print('\n'.join(out))
open(r'D:\英语教学\00_总规划\05_交付与审核记录\_int_count_tmp.txt', 'w', encoding='utf-8').write('\n'.join(out))