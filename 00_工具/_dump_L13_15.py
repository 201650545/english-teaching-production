# -*- coding: utf-8 -*-
import re
from docx import Document
for lesson, path in [(13, r"D:\英语教学\邓兴华\第13课时\第13课时_配套练习_中等.docx"),
                     (15, r"D:\英语教学\邓兴华\第15课时\第15课时_配套练习_中等.docx")]:
    print("="*40, f"L{lesson}", "="*40)
    doc = Document(path)
    for i,p in enumerate(doc.paragraphs):
        t = p.text.strip()
        if t:
            print(f"[{i}] {t[:100]}")
    print()