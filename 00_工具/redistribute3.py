# -*- coding: utf-8 -*-
import re
from collections import Counter

p = r'D:\英语教学\邓兴华\第08课时\课件成品_网页PPT\第08课时_课件.html'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

# Find Q13 (bq1) and swap: A=Beach volleyball(correct) -> C=Beach volleyball(correct)
# Current: A. Beach volleyball (correct), B. Swimming (wrong), C. Lunch (wrong)
# Target:  A. Swimming (wrong), B. Lunch (wrong), C. Beach volleyball (correct)

old = """<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,'原文：we tried beach volleyball，正确！','bq1')">A. <span class="opt-label">A</span>Beach volleyball</button>
<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,'原文说先尝试排球，游泳是下午的。','bq1')">B. <span class="opt-label">B</span>Swimming</button>
<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,'原文说先尝试排球，午餐在之后。','bq1')">C. <span class="opt-label">C</span>Lunch</button>"""

new = """<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,'原文说先尝试排球，游泳是下午的。','bq1')">A. <span class="opt-label">A</span>Swimming</button>
<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,'原文说先尝试排球，午餐在之后。','bq1')">B. <span class="opt-label">B</span>Lunch</button>
<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,'原文：we tried beach volleyball，正确！','bq1')">C. <span class="opt-label">C</span>Beach volleyball</button>"""

if old in c:
    c = c.replace(old, new)
    print('Q13 swapped successfully')
else:
    print('Q13 pattern not found!')
    # Try to find it
    idx = c.find('bq1')
    if idx >= 0:
        print('Context:', repr(c[idx-300:idx+100]))

# Check distribution
pattern = r'<button class="quiz-opt" data-correct="1"[^>]*>([A-E])\.\s*<span'
matches = re.findall(pattern, c)
dist = Counter(matches)
print('New distribution:', dict(dist))
print('Total:', sum(dist.values()))
if dist:
    max_count = max(dist.values())
    max_pct = max_count / sum(dist.values())
    print('Max:', max_count, '(%.0f%%)' % (max_pct * 100))

with open(p, 'w', encoding='utf-8') as f:
    f.write(c)

print('File size:', len(c.encode('utf-8')))
