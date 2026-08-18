# -*- coding: utf-8 -*-
import re
d = open(r"D:\英语教学\邓兴华\第13课时\课件成品_网页PPT\第13课时_课件_中等.html", encoding="utf-8").read()
i = d.find('class="quiz-question"')
print("=== quiz-question sample ===")
print(d[i-120:i+1400].replace("\n"," "))