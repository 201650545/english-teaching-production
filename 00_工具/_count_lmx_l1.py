# -*- coding: utf-8 -*-
"""统计李民宪 L1 课件交互形式分布（补充修复④验收）"""
import re

html = open(r"D:\英语教学\李民宪\第01课时\第01课时_课件.html", encoding="utf-8").read()
sel = len(re.findall(r'class="quiz-opt"', html))
hl = len(re.findall(r'class="hl-word"', html))
fc = len(re.findall(r'class="flash-card"', html))
mc = len(re.findall(r'class="match-item"', html))
sort = len(re.findall(r'class="sort-card"', html))
past = len(re.findall(r'class="past-card"', html))
comp = len(re.findall(r'class="compass-item"', html))
asm = len(re.findall(r'class="asm-chip"', html))
fill = len(re.findall(r'class="fill-q"', html))
print("quiz-opt 选择题:", sel)
total = sel + hl + fc + mc + sort + past + comp + asm + fill
print("非选择交互: GM-V02", hl, "/ 听写翻牌", fc, "/ 连线", mc, "/ 拖拽", sort, "/ 过去式翻牌", past, "/ 罗盘", comp, "/ 词块", asm, "/ 任务型填空", fill)
print("选择题占比: %.0f%%  (需≤50%%)" % (sel * 100 / total))
print("含 CW-VISUAL-CONTRACT:", "CW-VISUAL-CONTRACT" in html)
print("含 CW-CSS-EXTRA:", "CW-CSS-EXTRA" in html)