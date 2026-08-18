import re, zipfile, os
b=r'D:\英语教学\邓兴华'
def docx_text(p):
    z=zipfile.ZipFile(p); xml=z.read('word/document.xml').decode('utf-8')
    xml=xml.replace('</w:p>','\n').replace('</w:r>',' ')
    return re.sub(r'<[^>]+>','',xml)
p=os.path.join(b,'第18课时','第18课时_配套练习_中等.docx')
t=docx_text(p)
# dump around question 24-29
idx=0
for m in re.finditer(r'\b(2[4-9])\.\s',t):
    print('----- Q%d -----'%int(m.group(1)))
    print(t[m.start():m.start()+350].replace('\n','|'))
    print()