import re, os
lessons = ['第16课时','第17课时','第18课时','第20课时']
base = r'D:\英语教学\邓兴华'
pat_lit = r'data-interaction-type="(?:fill_in|single_choice)"'

# 收集损坏开标签中含 data-interaction-type 字面量但又混入属性名的片段
corrupt_needles = [
    'data-interacdata-interaction-type',   # data-question-id 损坏
    'data-idata-interaction-type',          # data-knowledge-id 损坏
    'data-interaction-tdata-interaction-type',  # data-question-id 损坏
    'data-interaction-type="sdata-interaction-type',  # single_choicedata...
    'data-interaction-type="single_data-interaction-type',
    'data-interaction-type="single_choicedata-interaction-type',
    'data-interaction-type="fill_in" datadata-interaction-type',
    'data-interaction-type="fill_in"knowled',
    'data-interaction-type="fill_in"on-id',
    'data-interaction-type="fill_in"quest',
    '"data-interaction-type="fill_in"',
    'data-interaction-type="fill_in""',
    'datainteraction-type="fill_in"',
    'data-knowledge-idata-interaction-type',
    'data-knowleddata-interaction-type',
    'data-knowledge-iddata-interaction-type',
    'data-template-idata-interaction-type',
    'data-section="grammar"data-interaction-type',
]

for lesson in lessons:
    path = os.path.join(base, lesson, '课件成品_网页PPT', lesson.replace('课时','课时') + '_课件_中等.html')
    h = open(path, encoding='utf-8').read()
    print('========', lesson, '========')
    for nd in corrupt_needles:
        c = h.count(nd)
        if c:
            print('  %-55s x%d' % (nd, c))