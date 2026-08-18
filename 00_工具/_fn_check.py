# -*- coding: utf-8 -*-
import re, json
ONCLICK_RE = re.compile(r'onclick="([A-Za-z_$][A-Za-z0-9_$]*)\(', re.S)
FN_DEF_RE = re.compile(r'function\s+(%s)\s*\(')
report = {}
for l in [21, 22, 23, 24, 25]:
    p = r'D:\英语教学\邓兴华\第%d课时\课件成品_网页PPT\第%d课时_课件_中等.html' % (l, l)
    s = open(p, encoding='utf-8').read()
    # extract JS
    scripts = re.findall(r'<script>(.*?)</script>', s, re.S)
    js = '\n'.join(scripts)
    names = set(ONCLICK_RE.findall(s))
    # filter out methods that are DOM object methods (event.stopPropagation etc not starting as onclick direct)
    # exclude known false positives
    EXCLUDE = {'event', 'window', 'document', 'this', 'alert', 'console', 'Array', 'Math', 'JSON'}
    undefined = []
    fn_defined = {}
    for n in sorted(names):
        if n in EXCLUDE:
            continue
        # is it a function def in js?
        defined = bool(re.search(r'(?:function\s+%s\s*\(|%s\s*[:=]\s*function|window\.%s)'
                                 % (re.escape(n), re.escape(n), re.escape(n)), js))
        if re.search(r'function\s+%s\s*\(' % re.escape(n), js):
            fn_defined[n] = 'function def'
        elif re.search(r'%s\s*=\s*function' % re.escape(n), js):
            fn_defined[n] = 'var = function'
        elif re.search(r'window\.%s' % re.escape(n), js):
            fn_defined[n] = 'window.x'
        else:
            undefined.append(n)
    report[l] = {'onclick_names': sorted(names), 'defined': fn_defined, 'undefined': undefined}
    print('L%d  onclick函数个数=%d 未定义=%s' % (l, len(fn_defined), undefined))
json.dump(report, open(r'D:\英语教学\00_总规划\05_交付与审核记录\_fn_report_tmp.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('report saved')