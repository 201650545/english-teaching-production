# -*- coding: utf-8 -*-
import zipfile, re
from xml.etree import ElementTree as ET
def docx_text(path):
    z = zipfile.ZipFile(path)
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    root = ET.fromstring(z.read("word/document.xml"))
    return ["".join(t.text or "" for t in p.iter(ns+"t")) for p in root.iter(ns+"p")]
for L in (12,):
    paras = docx_text(r"D:\英语教学\邓兴华\第12课时\第12课时_配套练习_中等.docx")
    print("===== L12 参考练习 前12段 =====")
    for p in paras[:12]:
        if p.strip(): print(" |", p[:90])
    print("===== L12 部分/分标题 =====")
    for p in paras:
        if re.match(r'^第[一二三四]部分', p): print(" |", p[:70])
    print("--- 含语法诊断/教学诊断? ---")
    for p in paras:
        if '诊断' in p: print(" |", p[:70]); break
    print("--- 含听力? ---")
    print("听力" in "\n".join(paras))