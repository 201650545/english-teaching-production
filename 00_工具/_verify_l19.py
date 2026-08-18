# -*- coding: utf-8 -*-
import re, subprocess, os
p=r'D:\英语教学\邓兴华\第19课时\课件成品_网页PPT\第19课时_课件_中等.html'
h=open(p,encoding='utf-8').read()
size=len(h.encode('utf-8'))
print("bytes:", size, "(>=150KB:", size>=150*1024 if not size>=150000 else ")")
print("size>=150000:", size>=150000)
pages=re.findall(r'<div class="page[^"]*" id="page\d+"',h)
print("page divs:", len(pages))
ids=re.findall(r'id="page(\d+)"',h)
print("page ids:", len(ids), "max:", max(int(x) for x in ids) if ids else None)
print("CW-VISUAL-CONTRACT:", 'CW-VISUAL-CONTRACT:1' in h)
print("CW-INTERACTION-CONTRACT:", 'CW-INTERACTION-CONTRACT:1' in h)
# onclick functions
onclick=re.findall(r'onclick="([A-Za-z_][A-Za-z0-9_]*)\(',h)
fnset=set(onclick)
print("total onclick calls:", len(onclick), "unique functions:", len(fnset))
# JS-defined functions
js=re.search(r'<script>(.*?)</script>', h, re.S)
jsbody=js.group(1) if js else ''
defined=set(re.findall(r'function\s+([A-Za-z_][A-Za-z0-9_]*)', jsbody))
defined |= set(re.findall(r'window\.([A-Za-z_][A-Za-z0-9_]*)\s*=', jsbody))
defined |= set(re.findall(r'^\s*([A-Za-z_][A-Za-z0-9_]*)\s*=\s*function', jsbody, re.M))
# check each onclick fn defined as window[fn]
missing=[]
for fn in sorted(fnset):
    # check if fn is defined anywhere in jsbody
    if fn not in defined and not re.search(r'function\s+'+re.escape(fn)+r'\s*\(', jsbody):
        if not re.search(r'var\s+'+re.escape(fn)+r'\s*=', jsbody) and not re.search(r'window\.'+re.escape(fn)+r'\s*=', jsbody):
            missing.append(fn)
print("MISSING onclick functions:", missing)
print("\nAll onclick functions:")
for fn in sorted(fnset):
    status="DEFINED" if fn not in missing else "MISSING"
    print("  %-28s %s"%(fn, status))
# IndexedDB
print("\nIndexedDB:", 'indexedDB' in jsbody)
print("initDB:", 'function initDB' in jsbody or 'initDB' in jsbody)
# mind map
print("mindmap:", 'mindmap' in h.lower())
# double-click undo
print("double-click/undo:", 'dblclick' in jsbody or 'doubleClick' in jsbody or 'undo' in jsbody.lower())
# page transition animation
print("page transition animation (transition on .page):", bool(re.search(r'\.page[^{]*\{[^}]*transition', h)))
# node check
m=re.search(r'<script>(.*?)</script>', h, re.S)
out=r'c:\Users\郭永涛\.trae-cn\work\6a7141c62ff0270ea9a4e208\_l19_main.js'
open(out,'w',encoding='utf-8').write(m.group(1))
r=subprocess.run(['C:\\Users\\郭永涛\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\playwright\\driver\\node.exe','--check',out],capture_output=True,text=True)
print("node check RC:", r.returncode, r.stderr[-200:])