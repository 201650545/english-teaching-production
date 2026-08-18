# -*- coding: utf-8 -*-
import re, importlib.util
spec = importlib.util.spec_from_file_location("t", r"D:\英语教学\00_工具\_transform_dxh.py")
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
path = r"D:\英语教学\邓兴华\第13课时\课件成品_网页PPT\第13课时_课件_中等.html"
raw = open(path, encoding="utf-8").read()
parts = re.split(r'<div class="slide["\s]', raw)
inner = t.extract_slide_content(parts[1])
print("LEN", len(inner))
print("HEAD:", inner[:200].replace("\n"," "))
print("TAIL:", inner[-260:].replace("\n"," "))
# also show the part around idx
part = parts[1]
idx = part.find('class="slide-content"')
print("idx found:", idx)
start = part.rfind('<div', 0, idx)
print("start tag:", part[start:part.find('>', start)+1])