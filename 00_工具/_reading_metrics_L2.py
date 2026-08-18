# -*- coding: utf-8 -*-
import re
html = open('_tmp_L2.html', encoding='utf-8').read()

# 提取三篇阅读正文（按 page id 划分）
def passage_words(page_id):
    m = re.search(r'<div class="page" id="%s">(.*?)</div>\s*</div>\s*<div class="page"' % page_id, html, re.S)
    if not m:
        m = re.search(r'<div class="page" id="%s">(.*?)</div>\s*</div>\s*<!--' % page_id, html, re.S)
    block = m.group(1)
    paras = re.findall(r'<p class="read-body">(.*?)</p>', block, re.S)
    text = ' '.join(paras)
    words = re.findall(r"[A-Za-z']+", text)
    return words, text

NEW = {'seem','bored','someone','diary','enjoyable','activity','decide','try','bird','bicycle'}

for pid, name in [('page23','A'),
                  ('page25','B'),
                  ('page27','C')]:
    words, text = passage_words(pid)
    # 还原词形（过去式/复数 → 原形）
    def stem(w):
        w = w.lower()
        for s in ('seemed','enjoyed'):
            if w==s: return s[:-1] if w=='seemed' else 'enjoy'
        # 简单规则化
        if w.endswith('ies') and len(w)>4: return w[:-3]+'y'
        if w.endswith('s') and not w.endswith('ss') and len(w)>3: return w[:-1]
        if w.endswith('ed') and len(w)>3: return w[:-2]
        if w.endswith('ing') and len(w)>4: return w[:-3]
        return w
    new_used = set()
    for w in words:
        s = stem(w)
        if s in NEW:
            new_used.add(s)
    total = len(words)
    rate = 100.0*len(new_used)/total
    # 判断是否任务型
    task = '任务型' if pid=='page27' else '非任务型'
    print('%s篇(%s): 词数=%d  新词=%s  生词率=%.1f%%  %s' % (name,pid,total,sorted(new_used),rate,task))