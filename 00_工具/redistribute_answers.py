# -*- coding: utf-8 -*-
import re

p = r'D:\英语教学\邓兴华\第08课时\课件成品_网页PPT\第08课时_课件.html'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

# Strategy: For each quiz-container, swap options to redistribute correct answers
# Need to change 7 B answers to A or C so distribution is max 8

# Q1 (page24): I ____ at home yesterday evening. B=was correct
# Swap A and B: make A=was (correct), B=were (wrong)
c = c.replace(
    '<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,\'I 固定用 was，不能用 were。\',\'q1\')">A. <span class="opt-label">A</span>were</button>\n<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,\'I 用 was，正确！\',\'q1\')">B. <span class="opt-label">B</span>was</button>',
    '<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,\'I 用 was，正确！\',\'q1\')">A. <span class="opt-label">A</span>was</button>\n<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,\'I 固定用 was，不能用 were。\',\'q1\')">B. <span class="opt-label">B</span>were</button>'
)

# Q2 (page24): They ____ the museum last weekend. B=visited correct
# Swap B and C: make C=visited (correct), B=visiting (wrong)  
c = c.replace(
    '<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,\'visited 是 visit 的过去式，正确！\',\'q2\')">B. <span class="opt-label">B</span>visited</button>\n<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,\'visiting 是现在分词，不是过去式。\',\'q2\')">C. <span class="opt-label">C</span>visiting</button>',
    '<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,\'visiting 是现在分词，不是过去式。\',\'q2\')">B. <span class="opt-label">B</span>visiting</button>\n<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,\'visited 是 visit 的过去式，正确！\',\'q2\')">C. <span class="opt-label">C</span>visited</button>'
)

# Q4 (page25): I visited Beijing two years ____. B=ago correct
# Swap A and B: make A=ago (correct), B=before (wrong)
c = c.replace(
    '<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,\'ago 放在时间段之后，不能用 before。\',\'q5\')">A. <span class="opt-label">A</span>before</button>\n<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,\'two years ago，ago 放在时间段后，正确！\',\'q5\')">B. <span class="opt-label">B</span>ago</button>',
    '<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,\'two years ago，ago 放在时间段后，正确！\',\'q5\')">A. <span class="opt-label">A</span>ago</button>\n<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,\'ago 放在时间段之后，不能用 before。\',\'q5\')">B. <span class="opt-label">B</span>before</button>'
)

# Q6 (page25): ____ you enjoy the trip? B=Did correct
# Swap A and B: make A=Did (correct), B=Was (wrong)
c = c.replace(
    '<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,\'Was 用于 be 动词疑问句，enjoy 是实义动词。\',\'q6\')">A. <span class="opt-label">A</span>Was</button>\n<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,\'Did + 主语 + 原形 enjoy，正确！\',\'q6\')">B. <span class="opt-label">B</span>Did</button>',
    '<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,\'Did + 主语 + 原形 enjoy，正确！\',\'q6\')">A. <span class="opt-label">A</span>Did</button>\n<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,\'Was 用于 be 动词疑问句，enjoy 是实义动词。\',\'q6\')">B. <span class="opt-label">B</span>Was</button>'
)

# Q7 (page25): He ____ English yesterday. B=studied correct
# Swap A and B: make A=studied (correct), B=studyed (wrong)
c = c.replace(
    '<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,\'studyed 是错误拼写，辅音+y 结尾应 y 变 i 加 -ed。\',\'q7\')">A. <span class="opt-label">A</span>studyed</button>\n<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,\'studied 正确！辅音+y 结尾，y 变 i 加 -ed。\',\'q7\')">B. <span class="opt-label">B</span>studied</button>',
    '<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,\'studied 正确！辅音+y 结尾，y 变 i 加 -ed。\',\'q7\')">A. <span class="opt-label">A</span>studied</button>\n<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,\'studyed 是错误拼写，辅音+y 结尾应 y 变 i 加 -ed。\',\'q7\')">B. <span class="opt-label">B</span>studyed</button>'
)

# Q9 (page26): What time did they start the trip? B=8 a.m. correct
# Swap A and B: make A=8 a.m. (correct), B=6 a.m. (wrong)
c = c.replace(
    '<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,\'原文说 started at 8 a.m.，不是 6 a.m.。\',\'rq2\')">A. <span class="opt-label">A</span>6 a.m.</button>\n<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,\'原文：started the trip at 8 a.m.，正确！\',\'rq2\')">B. <span class="opt-label">B</span>8 a.m.</button>',
    '<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,\'原文：started the trip at 8 a.m.，正确！\',\'rq2\')">A. <span class="opt-label">A</span>8 a.m.</button>\n<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,\'原文说 started at 8 a.m.，不是 6 a.m.。\',\'rq2\')">B. <span class="opt-label">B</span>6 a.m.</button>'
)

# Q10 (page26): How did the writer feel? B=Happy correct
# Swap A and B: make A=Happy (correct), B=Terrible (wrong)
c = c.replace(
    '<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,\'原文说 I felt very happy，不是 terrible。\',\'rq3\')">A. <span class="opt-label">A</span>Terrible</button>\n<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,\'原文：I felt very happy，正确！\',\'rq3\')">B. <span class="opt-label">B</span>Happy</button>',
    '<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,\'原文：I felt very happy，正确！\',\'rq3\')">A. <span class="opt-label">A</span>Happy</button>\n<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,\'原文说 I felt very happy，不是 terrible。\',\'rq3\')">B. <span class="opt-label">B</span>Terrible</button>'
)

# Verify distribution
pattern = r'<button class="quiz-opt" data-correct="1"[^>]*>([A-E])\.\s*<span'
matches = re.findall(pattern, c)
from collections import Counter
dist = Counter(matches)
print('New distribution:', dict(dist))
print('Total:', sum(dist.values()))
max_count = max(dist.values())
max_pct = max_count / sum(dist.values())
print('Max:', max_count, '(%.0f%%)' % (max_pct * 100))

with open(p, 'w', encoding='utf-8') as f:
    f.write(c)

print('File size:', len(c.encode('utf-8')))
