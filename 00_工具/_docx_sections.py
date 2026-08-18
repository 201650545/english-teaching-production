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
    print("===== L%d 部分/分标题 =====" % L)
    for p in paras:
        if re.match(r'^第[一二三四]部分', p) or re.match(r'^第[一二三四]节', p):
            print(" |", p)
    # count max question number
    nums=[]
    for p in paras:
        m=re.match(r'^\s*(\d{1,2})\s*$', p) or re.match(r'^\s*(\d{1,2})\.\s*\S', p) or re.match(r'^\s*(\d{1,2})([、．])\s*\S', p)
        if m: nums.append(int(m.group(1)))
    print("题号序列数:", len(nums), "max:", max(nums) if nums else 0)
    print()