# -*- coding: utf-8 -*-
"""邓兴华 L08 配套练习（中等）拼装 + 生成。
结构对齐 exam_spec v2026.3（不含听力，笔试100分）。
语篇来源：真题母本改编/仿真题，溯源ID已登记。
时态：一般过去时 was/were + 规则动词-ed + 过去时间状语（G19-G21）。
"""
import json, os, sys, re, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# 加载内容模块
from practice_content_DXH_L08 import content

# 加载生成器
spec = importlib.util.spec_from_file_location("bp", os.path.join(HERE, "build_practice_paper.py"))
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

# 课程卡
card = {
    "lesson": 8,
    "student": "邓兴华",
    "tier": "中等",
    "stage": "S3",
    "type": "normal",
    "grammar": ["G19 was/were", "G20 规则动词-ed+didn't+原形", "G21 过去时间状语"],
    "theme": "过去时·旅行经历",
    "vocab": {"new_count": 20, "review_count": 140, "theme": "travel_past"},
    "phonics": "ai/ay /eɪ/",
    "listening": False,
}

# 输出路径
out = os.path.join(os.path.dirname(HERE), "邓兴华", "第08课时", "第08课时_配套练习.docx")

# 生成
p = bp.build_practice(card, content, out)
print("配套练习生成：%s (%d bytes)" % (p, os.path.getsize(p)))
