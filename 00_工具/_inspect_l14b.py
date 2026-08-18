# -*- coding: utf-8 -*-
import re
d = open(r"D:\英语教学\邓兴华\第14课时\课件成品_网页PPT\第14课时_课件_中等.html", encoding="utf-8").read()
i = d.find('class="quiz-question"')
print("=== L14 quiz-question sample ===")
print(d[i-100:i+1600].replace("\n"," "))