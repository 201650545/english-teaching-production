# -*- coding: utf-8 -*-
"""邓兴华 L11 配套练习（中等）生成。"""
import json, os, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# 加载内容
with open(os.path.join(HERE, "practice_content_DXH_L11.json"), encoding="utf-8") as f:
    content = json.load(f)

# 加载生成器
spec = importlib.util.spec_from_file_location("bp", os.path.join(HERE, "build_practice_paper.py"))
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

card = {
    "lesson": 11,
    "student": "邓兴华",
    "tier": "中等",
    "stage": "S3",
    "type": "normal",
    "grammar": ["G28 can/would/should", "G29 不规则名词复数", "G30 时间介词 in/on/at"],
    "theme": "食物与点餐",
    "vocab": {"new_count": 20, "review_count": 140, "theme": "food_ordering"},
    "phonics": "oo /uː/ /ʊ/",
    "listening": False,
}

out = os.path.join(os.path.dirname(HERE), "邓兴华", "第11课时", "第11课时_配套练习_中等.docx")
p = bp.build_practice(card, content, out)
print("L11 配套练习生成：%s (%d bytes)" % (p, os.path.getsize(p)))
