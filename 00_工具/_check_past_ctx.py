import re, zipfile, os
b=r'D:\英语教学\邓兴华'
def docx_text(p):
    z=zipfile.ZipFile(p); xml=z.read('word/document.xml').decode('utf-8')
    # insert spaces between paragraphs and runs
    xml=xml.replace('</w:p>','\n').replace('</w:r>',' ')
    return re.sub(r'<[^>]+>','',xml)
for L in (17,18,19):
    p=os.path.join(b,'第%d课时'%L,'第%d课时_配套练习_中等.docx'%L)
    t=docx_text(p)
    print('='*20,'L%d'%L,'='*20)
    for w in ['looked','ran','read']:
        for m in re.finditer(r'\b'+w+r'\b',t,re.I):
            print('  [%s] ...%s...'%(w,t[max(0,m.start()-60):m.start()+60].replace('\n','|')))
            print()