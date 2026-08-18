# -*- coding: utf-8 -*-
"""删除 L13 空壳页 page38 并重编号，减到 45 页"""
import re, sys

path = r'd:\英语教学\邓兴华\第13课时\课件成品_网页PPT\第13课时_课件_中等.html'
with open(path, encoding='utf-8') as f:
    h = f.read()
orig = h

def check(name, cond):
    print(('PASS' if cond else 'FAIL'), '-', name)
    if not cond:
        sys.exit(1)

# 1) 删除 page38 空壳块（直到下一个 page39 之前）
pat = re.compile(r'(?s)<div class="page" id="page38">.*?(?=\n<div class="page" id="page39">)')
h2, n = pat.subn('', h)
check('删除 page38 空壳块', n == 1)
h = h2

# 2) 重编号 page39..46 -> page38..45
for i in range(39, 47):
    h = h.replace('id="page%d"' % i, 'id="page%d"' % (i - 1))
    # PAGE_META 键
    h = h.replace('"%d": {"p": "CORE", "m": 5}' % i, '"%d": {"p": "CORE", "m": 5}' % (i - 1))

# 3) totalPages 46 -> 45（两处）
h = h.replace('var totalPages = 46;', 'var totalPages = 45;')
h = h.replace('var totalPages = 25;', 'var totalPages = 25;')  # 旧脚本不动

# 4) segmentPages 更新（第二套，实际生效）
h = h.replace('"7": [37, 44], "8": [45, 46]', '"7": [37, 43], "8": [44, 45]')

check('totalPages=45 存在', h.count('var totalPages = 45;') >= 1)
check('无 page46 残留', 'id="page46"' not in h)
# 页数应正好 45 个连续 page1..45
pages = re.findall(r'id="page(\d+)"', h)
check('页数=45', len(pages) == 45)
check('页码连续 1..45', sorted(int(p) for p in pages) == list(range(1, 46)))
check('无 TOTAL-46 残留', '"8": [45, 46]' not in h)

with open(path, 'w', encoding='utf-8') as f:
    f.write(h)
print('OK 已写入，字符数', len(orig), '->', len(h))