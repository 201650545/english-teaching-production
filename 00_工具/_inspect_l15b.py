# -*- coding: utf-8 -*-
import re
d = open(r"D:\英语教学\邓兴华\第15课时\课件成品_网页PPT\第15课时_课件_中等.html", encoding="utf-8").read()
# sample quiz-block
i = d.find('class="quiz-block"')
print("=== quiz-block sample ===")
print(d[i-80:i+1200].replace("\n"," "))
print()
# sample new-word / item-card
j = d.find('class="item-card"')
print("=== item-card sample ===")
print(d[j-100:j+900].replace("\n"," "))