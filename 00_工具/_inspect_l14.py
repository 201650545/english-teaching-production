# -*- coding: utf-8 -*-
import re
d = open(r"D:\英语教学\邓兴华\第14课时\课件成品_网页PPT\第14课时_课件_中等.html", encoding="utf-8").read()
cc = {}
for cls in re.findall(r'class="([^"]+)"', d):
    for c in cls.split():
        cc[c] = cc.get(c,0)+1
print("=== L14 interesting classes ===")
for c,k in sorted(cc.items(), key=lambda x:-x[1]):
    if 3 < k < 400:
        print("%4d %s" % (k,c))
# find any onclick handlers
print("\nonclick handlers:", sorted(set(re.findall(r'onclick="([a-zA-Z]+)', d))))
print("checkQuiz count:", d.count('checkQuiz('))
print("selectAnswer count:", d.count('selectAnswer('))
print("data-correct count:", d.count('data-correct'))
# sample a quiz-like element
i = d.find('qq-text')
print("\nqq-text sample:", d[i-100:i+400].replace("\n"," ") if i!=-1 else "none")