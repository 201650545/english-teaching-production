# -*- coding: utf-8 -*-
import re

path = r"D:\英语教学\邓兴华\第15课时\课件成品_网页PPT\第15课时_课件_中等.html"
src = open(path, encoding="utf-8").read()

# Find page boundaries
pages = list(re.finditer(r'<div class="page(?: active)?" id="page(\d+)"', src))
for pi, m in enumerate(pages):
    start = m.start()
    end = pages[pi+1].start() if pi+1 < len(pages) else len(src)
    seg = src[start:end]
    # skip the opening <div class="page"> tag itself
    # tokenize div opens/closes
    opens = re.findall(r'<div\b', seg)
    closes = re.findall(r'</div>', seg)
    # stack trace: find deepest imbalance
    stack = 0
    max_stack = 0
    unbalanced = 0
    # walk tokens in order using regex finditer
    tokens = list(re.finditer(r'<div\b|</div>', seg))
    depth = 0
    problems = []
    for t in tokens:
        if t.group(0) == '<div':
            depth += 1
            max_stack = max(max_stack, depth)
        else:
            depth -= 1
            if depth < 0:
                problems.append(t.start())
    if len(opens) != len(closes):
        print("page%s: open=%d close=%d 深度结束=%d" % (m.group(1), len(opens), len(closes), depth))