# -*- coding: utf-8 -*-
"""邓兴华 L12 配套练习（中等）生成。"""
import json, os, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

with open(os.path.join(HERE, "practice_content_DXH_L12.json"), encoding="utf-8") as f:
    content = json.load(f)

spec = importlib.util.spec_from_file_location("bp", os.path.join(HERE, "build_practice_paper.py"))
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

card = {
    "lesson": 12,
    "student": "邓兴华",
    "tier": "中等",
    "stage": "S3",
    "type": "normal",
    "grammar": ["G31 冠词 a/an/the", "G32 可数/不可数与量词结构", "G33 some/any 用法"],
    "theme": "餐厅点餐综合",
    "vocab": {"new_count": 20, "review_count": 140, "theme": "restaurant_comprehensive"},
    "phonics": "ou /aʊ/",
    "listening": False,
}

out = os.path.join(os.path.dirname(HERE), "邓兴华", "第12课时", "第12课时_配套练习_中等.docx")
p = bp.build_practice(card, content, out)
print("L12 配套练习生成：%s (%d bytes)" % (p, os.path.getsize(p)))
