# -*- coding: utf-8 -*-
import re, subprocess, os
h=open(r'D:\英语教学\邓兴华\第20课时\课件成品_网页PPT\第20课时_课件_中等.html',encoding='utf-8').read()
scripts=re.findall(r'<script[^>]*>(.*?)</script>', h, re.S)
print("num script blocks:", len(scripts))
js="\n".join(scripts)
out=r'c:\Users\郭永涛\.trae-cn\work\6a7141c62ff0270ea9a4e208\_l20_js_extract.js'
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out,'w',encoding='utf-8').write(js)
print("wrote", out, len(js))
# find suspicious ':' token errors - look for text like label: inside
# run node --check
r=subprocess.run(['C:\\Users\\郭永涛\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\playwright\\driver\\node.exe','--check',out],capture_output=True,text=True)
print("RC:",r.returncode)
print("STDOUT:",r.stdout[-2000:])
print("STDERR:",r.stderr[-2000:])