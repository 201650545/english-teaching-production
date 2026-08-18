# -*- coding: utf-8 -*-
from docx import Document
for lesson, path in [(13, r"D:\英语教学\邓兴华\第13课时\第13课时_配套练习_中等.docx"),
                     (14, r"D:\英语教学\邓兴华\第14课时\第14课时_配套练习_中等.docx")]:
    print("="*40, f"L{lesson} TAIL", "="*40)
    doc = Document(path)
    tail = [p.text.strip() for p in doc.paragraphs if p.text.strip()][-25:]
    for t in tail:
        print(t[:150])
    print()