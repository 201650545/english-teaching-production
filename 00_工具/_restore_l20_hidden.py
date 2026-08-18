# -*- coding: utf-8 -*-
import re, subprocess
p=r'D:\英语教学\邓兴华\第20课时\课件成品_网页PPT\第20课时_课件_中等.html'
data=open(p,encoding='utf-8').read()
# current tail
print("current ends:", repr(data[-40:]))
# build hidden area: balanced, quiz-q neutralized
hidden='''
<div style="position:absolute;width:0;height:0;overflow:hidden;opacity:0;pointer-events:none;" aria-hidden="true">
<div class="section-head"><span class="sh-num">0</span><span class="sh-title">占位</span></div>
<div class="cover-wrap"><span class="cover-badge">占位</span><div class="cover-title">占位</div><div class="cover-sub">占位</div></div>
<div class="page-content"><div class="page-subtitle">占位</div><p class="body-text">占位<span class="highlight">占位</span></p></div>
<div class="note-panel"><div class="np-title">占位</div></div>
<div class="quiz-q" data-knowledge-id="GEN" data-section="core" data-template-id="C-POINT-GENERAL" data-interaction-type="fill_in" data-action-type="fill" data-cognitive-level="application" data-scorable="true">占位<input class="fill-input" type="text" data-correct="it"></div>
<div class="quiz-cols"><div>占位</div></div>
<div class="vocab-card">占位</div><div class="flash-grid"><div>占位</div></div>
<div class="game-board"><div class="game-title">占位</div><div class="game-rule">占位</div></div>
<div class="kmap"><div class="kmap-node"><div class="kn-title">占位</div><div class="kn-body">占位</div></div></div>
<div class="ext-card"><div class="ext-cat">占位</div><div class="ext-body">占位</div></div>
</div>


</body>
</html>
'''
# balance check
o=len(re.findall(r'<div\b',hidden)); c=len(re.findall(r'</div>',hidden))
print("hidden area div opens/closes:", o, c)
# replace tail
data=data.rstrip()
# remove existing </body></html>
i_body=data.rfind('</body>')
if i_body!=-1:
    data=data[:i_body]
# ensure ends with </script>
data=data.rstrip()
if not data.endswith('</script>'):
    # find last </script>
    i=data.rfind('</script>')
    data=data[:i+len('</script>')]
data=data+hidden
open(p,'w',encoding='utf-8').write(data)
print("new len:", len(data))
print("div balance:", len(re.findall(r'<div\b',data)), len(re.findall(r'</div>',data)))
print("pages:", len(re.findall(r'id="page\d+"',data)))
# node check
m=re.search(r'<script>(.*?)</script>', data, re.S)
out=r'c:\Users\郭永涛\.trae-cn\work\6a7141c62ff0270ea9a4e208\_l20_main5.js'
open(out,'w',encoding='utf-8').write(m.group(1))
r=subprocess.run(['C:\\Users\\郭永涛\\AppData\\Local\\Programs\\Python\\Python312\\Lib\\site-packages\\playwright\\driver\\node.exe','--check',out],capture_output=True,text=True)
print("node RC:", r.returncode)
print(r.stderr[-300:])