# -*- coding: utf-8 -*-
import re
from collections import Counter

p = r'D:\英语教学\邓兴华\第08课时\课件成品_网页PPT\第08课时_课件.html'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

# Change Q14 (page28): "memorable" means ____. Currently A=Unforgettable correct, B=Boring wrong
# Swap B and A: make B=Unforgettable (correct), A=Boring (wrong)
# Wait, that would make B=9 again. Instead, change to C=Unforgettable
# Current options: A=Unforgettable, B=Boring, C=Terrible
# Change to: A=Boring, B=Terrible, C=Unforgettable

# Actually let me check current state of Q14
# After the redistribution, Q14 "The word memorable means" 
# Originally: A=Boring(wrong), B=Unforgettable(correct), C=Terrible(wrong)
# After first fix it's still the same since I didn't touch it

# Let me swap one A to C. Q13 "What did they try first" currently A=Beach volleyball(correct)
# Change to: A=Swimming(wrong), B=Lunch(wrong), C=Beach volleyball(correct)
c = c.replace(
    """<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,'原文：we tried beach volleyball，正确！','bq1')"><span class="opt-label">A</span>Beach volleyball</button>
<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,'原文说先尝试排球，游泳是下午的。','bq1')"><span class="opt-label">B</span>Swimming</button>
<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,'原文说先尝试排球，午餐在之后。','bq1')"><span class="opt-label">C</span>Lunch</button>""",
    """<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,'原文说先尝试排球，游泳是下午的。','bq1')">A. <span class="opt-label">A</span>Swimming</button>
<button class="quiz-opt" data-correct="0" onclick="handleQuiz(this,false,'原文说先尝试排球，午餐在之后。','bq1')">B. <span class="opt-label">B</span>Lunch</button>
<button class="quiz-opt" data-correct="1" onclick="handleQuiz(this,true,'原文：we tried beach volleyball，正确！','bq1')">C. <span class="opt-label">C</span>Beach volleyball</button>"""
)

# Check
pattern = r'<button class="quiz-opt" data-correct="1"[^>]*>([A-E])\.\s*<span'
matches = re.findall(pattern, c)
dist = Counter(matches)
print('New distribution:', dict(dist))
print('Total:', sum(dist.values()))
max_count = max(dist.values())
max_pct = max_count / sum(dist.values())
print('Max:', max_count, '(%.0f%%)' % (max_pct * 100))

with open(p, 'w', encoding='utf-8') as f:
    f.write(c)

print('File size:', len(c.encode('utf-8')))
