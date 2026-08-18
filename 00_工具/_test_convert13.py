# -*- coding: utf-8 -*-
import re, importlib.util
spec = importlib.util.spec_from_file_location("t", r"D:\英语教学\00_工具\_transform_dxh.py")
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)

d = open(r"D:\英语教学\邓兴华\第13课时\课件成品_网页PPT\第13课时_课件_中等.html", encoding="utf-8").read()
# test opts regex on a q-option
sample = '<div class="q-option" onclick="selectAnswer(this,\'A\',false,event)"><span class="qo-letter">A</span>any</div>'
m = re.search(r'<div class="q-option"[^>]*onclick="selectAnswer\(this,\s*\'([A-E])\',\s*(true|false)[^)]*\)"[^>]*>(.*?)</div>', sample, re.S)
print("opts regex match:", m.groups() if m else None)

# Now test convert_quizzes on a slide content that has quiz-question
# find quiz-question index
idx = d.find('<div class="quiz-question"')
print("quiz-question idx:", idx)
# get the enclosing slide-content
# find the slide opening before idx
slide_open = d.rfind('<div class="slide', 0, idx)
print("slide_open:", slide_open, d[slide_open:slide_open+60])
# extract slide-content inner
content = t.extract_slide_content(d[slide_open:])
print("extracted content len:", len(content) if content else None)
if content:
    print("has quiz-question in extracted:", 'quiz-question' in content)
    # run convert
    out, qid = t.convert_quizzes(content, 0)
    print("qid after convert:", qid)
    print("quiz-opt count:", out.count('class="quiz-opt"'))
    # show a bit
    j = out.find('quiz-opt')
    print("first quiz-opt:", out[j-40:j+120] if j!=-1 else "NONE")