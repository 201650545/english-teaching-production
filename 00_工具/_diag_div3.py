# -*- coding: utf-8 -*-
import re, importlib.util
spec = importlib.util.spec_from_file_location("t", r"D:\英语教学\00_工具\_transform_dxh.py")
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)
path = r"D:\英语教学\邓兴华\第13课时\课件成品_网页PPT\第13课时_课件_中等.html"
raw = open(path, encoding="utf-8").read()
parts = re.split(r'<div class="slide["\s]', raw)
part = parts[1]
idx = part.find('class="slide-content"')
start = part.rfind('<div', 0, idx)
gt = part.find('>', idx)
end = t.matching_close(part, start)
inner = part[gt+1:end]
print("start:", start, "gt:", gt, "end:", end)
print("inner opens:", inner.count('<div'), "closes:", inner.count('</div>'))
# show the segment from end-60 to end+30
print("around end:", part[end-60:end+30].replace("\n"," "))
# also full part tail
print("part tail:", part[-120:].replace("\n"," "))
# count div in whole part
print("part opens:", part.count('<div'), "closes:", part.count('</div>'))