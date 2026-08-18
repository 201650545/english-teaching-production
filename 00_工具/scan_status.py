# -*- coding: utf-8 -*-
import os, glob, subprocess, re

base = 'D:/英语教学/许颖嘉'
for i in range(1, 26):
    dir_name = "第%02d课时" % i
    folder = os.path.join(base, dir_name)
    if not os.path.exists(folder):
        print("%s: ❌ 文件夹缺失" % dir_name)
        continue
    
    html_files = glob.glob(os.path.join(folder, "**/*.html"), recursive=True)
    if not html_files:
        print("%s: ❌ HTML缺失" % dir_name)
        continue
    
    h = html_files[0]
    content = open(h, encoding='utf-8', errors='ignore').read()
    contract = 'page-id' if ('quiz-opt' in content and 'page' in content) else 'old/unknown'
    
    r = subprocess.run(['python', 'D:/英语教学/00_工具/verify_v2.py', h], capture_output=True, text=True, encoding='utf-8')
    is_pass = (r.returncode == 0 and contract == 'page-id')
    status = 'PASS ✅' if is_pass else 'FAIL/LEGACY ❌'
    print("%s: 契约=%-8s | 状态=%-12s | 文件=%s" % (dir_name, contract, status, os.path.basename(h)))
