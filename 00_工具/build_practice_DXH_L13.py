# -*- coding: utf-8 -*-
"""邓兴华 L13 配套练习（中等）生成。"""
import json, os, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

with open(os.path.join(HERE, "practice_content_DXH_L13.json"), encoding="utf-8") as f:
    content = json.load(f)

spec = importlib.util.spec_from_file_location("bp", os.path.join(HERE, "build_practice_paper.py"))
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

card = {
    "lesson": 13,
    "student": "邓兴华",
    "tier": "中等",
    "stage": "S3",
    "type": "normal",
    "grammar": ["G34 would like 点餐", "G35 how much-many 数量", "G36 货币价格表达"],
    "theme": "购物·食材与价格",
    "vocab": {"new_count": 20, "review_count": 140, "theme": "shopping_price"},
    "phonics": "ea /iː/ 与 /e/",
    "listening": False,
}

out = os.path.join(os.path.dirname(HERE), "邓兴华", "第13课时", "第13课时_配套练习_中等.docx")
p = bp.build_practice(card, content, out)
print("L13 配套练习生成：%s (%d bytes)" % (p, os.path.getsize(p)))