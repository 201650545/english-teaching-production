# -*- coding: utf-8 -*-
"""L26 配套练习驱动（复用 build_practice_paper.py 引擎，不修改引擎）。
结构：exam_spec v2026.2（不含听力）→ 阅读30 + 语言25 + 综合25 + 语法诊断附录(不计分)。
首行缩进 1 字符、答案随机化(seed=26, 相邻不同字母) 由引擎统一处理。
"""
import os, json, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from build_practice_paper import build_practice

def main():
    content = json.load(open(os.path.join(HERE, "practice_content_XYJ_L26.json"), encoding="utf-8"))
    card = {
        "lesson": 26,
        "student": "许颖嘉",
        "tier": "基础",
        "stage": "S5",
        "type": "sprint",
        "grammar": ["书面表达 SOP 五步（审题/列点/成句/连段/检查）"],
        "theme": "书面表达 SOP · 自我介绍",
        "vocab": {"new_count": 0, "review_count": 0, "theme": "writing"},
        "phonics": "-",
        "listening": False,
    }
    out = os.path.join(os.path.dirname(HERE), "许颖嘉", "第26课时", "第26课时_配套练习_基础.docx")
    p = build_practice(card, content, out)
    print("配套练习生成：%s (%d bytes)" % (p, os.path.getsize(p)))

if __name__ == "__main__":
    main()
