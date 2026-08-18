import json, os, re
d = json.load(open(r'D:\英语教学\00_工具\practice_content_DXH_L19.json', encoding='utf-8'))
txt = json.dumps(d, ensure_ascii=False)
past_kw = [' was ', ' were ', ' went ', ' came ', ' had ', ' did ', ' yesterday', ' last week',
           ' ago', ' cooked', ' played', ' visited', ' walked', ' watched', ' studied',
           ' bought', ' taught', ' ate ', ' drank ', ' broke', ' took', ' gave', ' made ',
           'Last year', 'Last weekend', 'two days ago', 'last month', 'last night']
for k in past_kw:
    c = (' '+txt+' ').count(k)
    if c:
        print('HIT', repr(k), c)
# print all reading/cloze paragraphs
for key in ['reading_a','reading_b','reading_c','w5','cloze']:
    v = d.get(key)
    if isinstance(v, dict):
        print('---', key, 'paragraphs:', v.get('paragraphs'))
        for q in v.get('questions',[]):
            print('   Q', q.get('q'))
    elif isinstance(v, list):
        print('---', key, 'list start:', json.dumps(v[:2], ensure_ascii=False)[:400])