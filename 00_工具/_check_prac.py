import json, re, os
base = r'D:\英语教学\00_工具'
for lesson in [16,17,18,19,20]:
    fn = os.path.join(base, 'practice_content_DXH_L%02d.json' % lesson)
    if not os.path.exists(fn):
        print('L%d: NO JSON' % lesson); continue
    d = json.load(open(fn, encoding='utf-8'))
    txt = json.dumps(d, ensure_ascii=False)
    # source ids
    src = re.findall(r'"(?:source|source_id|src|origin|trace|来源|溯源)"\s*:\s*"([^"]*)"', txt)
    print('L%d: source_ids=%d sample=%s' % (lesson, len(src), src[:3]))
    # past tense check (L17-19 forbidden)
    past_kw = [' was ', ' were ', ' went ', ' came ', ' had ', ' did ', ' -ed ', ' yesterday', ' last week', ' cooked', ' played', ' visited', ' walked', ' watched', ' studied', ' bought', ' taught', ' ate ', ' drank ']
    if lesson in (17,18,19):
        hits = [k for k in past_kw if k in txt]
        print('    past_tokens(hits):', hits if hits else 'NONE ✅')
    else:
        print('    (L%d past allowed)' % lesson)
    # check structure keys
    print('    keys:', list(d.keys()))