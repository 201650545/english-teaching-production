# -*- coding: utf-8 -*-
import re, subprocess
p=r'D:\英语教学\邓兴华\第20课时\课件成品_网页PPT\第20课时_课件_中等.html'
h=open(p,encoding='utf-8').read()
# Extract main script block
m=re.search(r'<script>(.*?)</script>', h, re.S)
js=m.group(1)
# find any stray CSS-like tokens inside JS
stray=re.findall(r'z-index\s*:\s*\d+', js)
print("z-index occurrences in JS:", stray)
# fix the specific corruption
bad="if (!val) { input.focus(); return; } z-index:2; }"
if bad in js:
    js=js.replace(bad, "if (!val) { input.focus(); return; }")
    print("FIXED checkFill corruption")
# generic: remove any ' } z-index:NN; }' pattern inside JS (CSS injection)
js2=re.sub(r'\}\s*z-index\s*:\s*\d+;\s*\}', '}', js)
if js2!=js:
    print("generic cleanup applied")
    js=js2
# scan for other garbage patterns
for pat in (r'\.\w+-\w+\s*\{\s*\}', r'z-index', r'\b\d+px\b'):
    c=len(re.findall(pat,js))
    if c: print("  leftover %s count=%d"%(pat,c))
m2=re.search(r'<script>(.*?)</script>', h, re.S)
h=h[:m2.start(1)]+js+h[:m2.end(1)]
open(p,'w',encoding='utf-8').write(h)
print("saved")
# re-check with node
m=re.search(r'<script>(.*?)</script>', h, re.S)
out=r'c:\Users\郭永涛\.trae-cn\work\6a7141c62ff0270ea9a4e208\_l20_main2.js'
open(out,'w',encoding='utf-8').write(m.group(1))
r=subprocess.run(['C:\\Users\\郭永涛\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\playwright\\driver\\node.exe','--check',out],capture_output=True,text=True)
print("node RC:",r.returncode)
print(r.stderr[-800:])