# -*- coding: utf-8 -*-
"""Verify the generated DOCX file - part 2."""
from docx import Document

path = r"D:\英语教学\邓兴华\第08课时\第08课时_配套练习.docx"
doc = Document(path)

# Print paragraphs 80-169
for i, p in enumerate(doc.paragraphs[80:], 80):
    text = p.text.strip()
    if text:
        print(f"[{i}] {text[:120]}")
