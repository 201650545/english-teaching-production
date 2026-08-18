# -*- coding: utf-8 -*-
import re, subprocess
p=r'D:\英语教学\邓兴华\第20课时\课件成品_网页PPT\第20课时_课件_中等.html'
data=open(p,encoding='utf-8').read()
# structure: HEAD + '<script>' + fixed_js + HEAD2 + '<script>' + original_js
i_script=data.find('<script>')          # 150705
# fixed_js is between first <script> and the second <head> (HEAD2 start)
i_head2=data.find('<head>', i_script+8) # 172932
fixed_js=data[i_script+8:i_head2]
HEAD=data[:i_script]
TAIL='\n\n</body>\n</html>\n'
correct=HEAD+'<script>'+fixed_js+'</script>'+TAIL
open(p,'w',encoding='utf-8').write(correct)
print("reconstructed len:", len(correct))
print("div balance opens/closes:", len(re.findall(r'<div\b',correct)), len(re.findall(r'</div>',correct)))
# node check main script
m=re.search(r'<script>(.*?)</script>', correct, re.S)
out=r'c:\Users\郭永涛\.trae-cn\work\6a7141c62ff0270ea9a4e208\_l20_main3.js'
open(out,'w',encoding='utf-8').write(m.group(1))
r=subprocess.run(['C:\\Users\\郭永涛\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\playwright\\driver\\node.exe','--check',out],capture_output=True,text=True)
print("node RC:", r.returncode)
print(r.stderr[-600:])
# verify no z-index in JS
print("z-index in JS:", 'z-index' in m.group(1))
# check tail
print("ends with:", repr(correct[-40:]))