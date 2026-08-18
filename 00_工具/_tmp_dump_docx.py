# -*- coding: utf-8 -*-
import docx
p = r"d:\英语教学\邓兴华\第15课时\第15课时_配套练习_中等.docx"
d = docx.Document(p)
for i, pa in enumerate(d.paragraphs):
    t = pa.text
    if 140 <= i <= 168:
        print(f"[{i}]{t}")