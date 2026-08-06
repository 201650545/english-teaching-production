# -*- coding: utf-8 -*-
import re

p = r'D:\英语教学\邓兴华\第08课时\课件成品_网页PPT\第08课时_课件.html'
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

# Find all quiz-opt with data-correct="1" and extract their letter
pattern = r'<button class="quiz-opt" data-correct="1"[^>]*>([A-E])\.\s*<span class="opt-label">([A-E])</span>([^<]*)'
matches = re.findall(pattern, c)
print('Correct answers:')
for i, (letter_prefix, label, text) in enumerate(matches):
    print(f'  Q{i+1}: {letter_prefix}. {text.strip()}')

# Count distribution
from collections import Counter
dist = Counter(m[0] for m in matches)
print('\nDistribution:', dict(dist))
print('Total:', sum(dist.values()))
