# -*- coding: utf-8 -*-
import zipfile, re
from xml.etree import ElementTree as ET
def docx_text(path):
    z = zipfile.ZipFile(path)
    xml = z.read("word/document.xml").decode("utf-8")
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    root = ET.fromstring(xml)
    return ["".join(t.text or "" for t in p.iter(ns+"t")) for p in root.iter(ns+"p")]
for L in (13,14):
    paras = docx_text(r"D:\英语教学\邓兴华\第%d课时\第%d课时_配套练习_中等.docx" % (L,L))
    print("===== L%d 前45段 =====" % L)
    for i,p in enumerate(paras[:45]):
        if p.strip(): print(i, "|", p[:80])
    print("===== L%d 后30段 =====" % L)
    for i,p in enumerate(paras[-30:]):
        if p.strip(): print(len(paras)-30+i, "|", p[:80])
    print()