# -*- coding: utf-8 -*-
import re, subprocess, os
h=open(r'D:\英语教学\邓兴华\第20课时\课件成品_网页PPT\第20课时_课件_中等.html',encoding='utf-8').read()
m=re.search(r'<script>(.*?)</script>', h, re.S)
js=m.group(1)
out=r'c:\Users\郭永涛\.trae-cn\work\6a7141c62ff0270ea9a4e208\_l20_main.js'
open(out,'w',encoding='utf-8').write(js)
lines=js.split('\n')
print("total lines:", len(lines))
r=subprocess.run(['C:\\Users\\郭永涛\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\playwright\\driver\\node.exe','--check',out],capture_output=True,text=True)
print("RC:",r.returncode)
print("STDERR:",r.stderr[-1500:])
# print lines around 395
print("=== lines 385-410 ===")
for i in range(384, min(410,len(lines))):
    print("%4d: %s"%(i+1, lines[i]))