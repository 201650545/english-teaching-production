# -*- coding: utf-8 -*-
import zipfile, re
from xml.etree import ElementTree as ET
def docx_text(path):
    z = zipfile.ZipFile(path)
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    root = ET.fromstring(z.read("word/document.xml"))
    return ["".join(t.text or "" for t in p.iter(ns+"t")) for p in root.iter(ns+"p")]
for L in (13,14,15):
    paras = docx_text(r"D:\英语教学\邓兴华\第%d课时\第%d课时_配套练习_中等.docx" % (L,L))
    print("===== L%d 诊断/附件/第四部分 =====" % L)
    for p in paras:
        if '诊断' in p or '附件' in p or re.match(r'^第四部分', p):
            print(" |", p[:70])
    # reference answer present?
    full="\n".join(paras)
    print("含参考答案:", "参考答案" in full or "参考" in full)
    print()