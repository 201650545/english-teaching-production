# -*- coding: utf-8 -*-
import re, subprocess
p=r'D:\英语教学\邓兴华\第20课时\课件成品_网页PPT\第20课时_课件_中等.html'
data=open(p,encoding='utf-8').read()
# find main script
m=re.search(r'<script>(.*?)</script>', data, re.S)
body=m.group(1)
# cut at first '<!DOCTYPE' inside body
idx=body.find('<!DOCTYPE')
if idx!=-1:
    body=body[:idx]
    print("cut at <!DOCTYPE>, removed", len(m.group(1))-idx, "chars")
# save
data2=data[:m.start(1)]+body+data[m.end(1):]
open(p,'w',encoding='utf-8').write(data2)
print("new len:", len(data2))
print("div balance:", len(re.findall(r'<div\b',data2)), len(re.findall(r'</div>',data2)))
print("pages:", len(re.findall(r'id="page\d+"',data2)))
# node check
mm=re.search(r'<script>(.*?)</script>', data2, re.S)
out=r'c:\Users\郭永涛\.trae-cn\work\6a7141c62ff0270ea9a4e208\_l20_main4.js'
open(out,'w',encoding='utf-8').write(mm.group(1))
r=subprocess.run(['C:\\Users\\郭永涛\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\playwright\\driver\\node.exe','--check',out],capture_output=True,text=True)
print("node RC:", r.returncode)
print(r.stderr[-500:])
print("z-index in JS:", 'z-index' in mm.group(1))