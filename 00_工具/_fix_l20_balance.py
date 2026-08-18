# -*- coding: utf-8 -*-
import re, shutil, os
BASE=r'D:\英语教学\邓兴华'; LESSON=20
SRC=os.path.join(BASE,'第%d课时'%LESSON,'课件成品_网页PPT','第%d课时_课件_中等.html'%LESSON)
h=open(SRC,encoding='utf-8').read()
def bal(): return len(re.findall(r'<div\b',h)),len(re.findall(r'</div>',h))
op,cl=bal(); print('before',op,cl)
# pages that are unclosed (from tracker)
pages=['page10','page13','page19','page20','page21','page22','page35','page37']
# insert </div> before each such page div
for pg in pages:
    pat='<div class="page" id="%s">'%pg
    if pat in h:
        h=h.replace(pat,'</div>\n'+pat,1)
op,cl=bal(); print('after pages',op,cl)
# close presentation + audio + ext-card before </body>
# insert sufficient closes before </body>
need=0
# count current
need=len(re.findall(r'<div\b',h))-len(re.findall(r'</div>',h))
print('need closes before body:',need)
if need>0:
    idx=h.rfind('</body>')
    h=h[:idx]+'</div>\n'*need+h[idx:]
open(SRC,'w',encoding='utf-8').write(h)
op,cl=bal(); print('after body',op,cl)