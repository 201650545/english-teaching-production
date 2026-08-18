# -*- coding: utf-8 -*-
import re, json
out = {}
for l in [21,22,23,24,25]:
    p = r'D:\英语教学\邓兴华\第%d课时\课件成品_网页PPT\第%d课时_课件_中等.html' % (l,l)
    s = open(p, encoding='utf-8').read()
    r = {}
    r['vis_contract'] = 'CW-VISUAL-CONTRACT:1' in s
    r['int_contract'] = 'CW-INTERACTION-CONTRACT:1' in s
    r['page_id_count'] = len(re.findall(r'page-id=', s))
    # pages: <div class="page ..."> or <section class="page..."
    r['page_divs'] = len(re.findall(r'<div class="page[ ">]', s))
    r['page_sections'] = len(re.findall(r'<section class="page[ ">]', s))
    r['cover_count'] = len(re.findall(r'class="[^"]*\bcover\b', s))
    r['mindmap'] = len(re.findall(r'mm-branch|mind-map|km-branch', s))
    r['sixcolor_cards'] = len(re.findall(r'class="[^"]*\b(color-1|color-2|color-3|color-4|color-5|color-6)\b', s))
    # answer distribution: count correct answer markers hidden
    r['quiz_opt'] = len(re.findall(r'class="quiz-opt"', s))
    # check answer-mask / hidden answers
    r['answer_mask'] = len(re.findall(r'answer-mask|mask-answer|hidden-answer', s))
    # check for .answer display:none reveal interaction (double-click undo)
    r['undo_hint'] = len(re.findall(r'双击|undo|dblclick', s))
    # flip transition animation check (should be none)
    r['flip_anim'] = len(re.findall(r'page-transition|flip-anim|pageflip', s))
    # IndexedDB
    r['indexeddb'] = len(re.findall(r'IndexedDB|indexedDB|initDB', s))
    # black screen check keywords
    r['black_screen'] = len(re.findall(r'background:#000|#000000', s))
    out[l] = r
    print('L%d:'%l, json.dumps(r, ensure_ascii=False))
json.dump(out, open(r'D:\英语教学\00_工具\_contract_check_result.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)