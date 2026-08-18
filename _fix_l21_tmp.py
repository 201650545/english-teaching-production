# -*- coding: utf-8 -*-
import io
p = r"D:\英语教学\邓兴华\第21课时\build_l21_courseware.py"
raw = io.open(p, encoding="utf-8").read()
lines = raw.split("\n")
ln = lines[123]
print("FULL line124:", repr(ln))
print("has 'behind':", 'behind' in ln)
print("has '])])),':", ']' + ')' + ']' + ')' + ')' + ')' + ',' in ln)
print("has 'behind\"]\":", 'behind"]' in ln)
print("last 50:", repr(ln[-50:]))
# find the bracket pattern
for i in range(len(ln)-10, len(ln)):
    print(i, repr(ln[i]))