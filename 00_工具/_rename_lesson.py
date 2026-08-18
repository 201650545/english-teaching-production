# -*- coding: utf-8 -*-
"""邓兴华/李民宪：第XX课 -> 第XX课时（目录+标准交付文件），归档/契约/part/分件/bak 不动。"""
import os, re
renamed = 0
for student in ('邓兴华', '李民宪'):
    base = os.path.join('.', student)
    if not os.path.isdir(base): continue
    for d in sorted(os.listdir(base)):
        m = re.match(r'^第(\d+)课$', d)
        if not m: continue
        n = int(m.group(1))
        old = os.path.join(base, d)
        # 递归改内部标准文件名 第XX课_ -> 第XX课时_
        for root, dirs, files in os.walk(old):
            if '归档' in root or '.bak' in root: continue
            for f in files:
                if f.startswith('第%02d课_' % n):
                    nf = f.replace('第%02d课_' % n, '第%02d课时_' % n)
                    os.rename(os.path.join(root, f), os.path.join(root, nf))
                    renamed += 1
        os.rename(old, os.path.join(base, '第%02d课时' % n))
        print('  %s: %s -> 第%02d课时' % (student, d, n))
print('内部文件改名 %d 个' % renamed)
