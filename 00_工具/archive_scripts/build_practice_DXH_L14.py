# -*- coding: utf-8 -*-
"""邓兴华 L14 配套练习（中等）生成。"""
import json, os, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

with open(os.path.join(HERE, "practice_content_DXH_L14.json"), encoding="utf-8") as f:
    content = json.load(f)

spec = importlib.util.spec_from_file_location("bp", os.path.join(HERE, "build_practice_paper.py"))
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

card = {
    "lesson": 14,
    "student": "邓兴华",
    "tier": "中等",
    "stage": "S4",
    "type": "normal",
    "grammar": ["G37 外貌 be vs have/has", "G38 why-because 因果", "G39 描述性形容词"],
    "theme": "外貌·人物描述",
    "vocab": {"new_count": 20, "review_count": 140, "theme": "appearance"},
    "phonics": "oa /əʊ/ · ou/ow /aʊ/",
    "listening": False,
}

out = os.path.join(os.path.dirname(HERE), "邓兴华", "第14课时", "第14课时_配套练习_中等.docx")
p = bp.build_practice(card, content, out)
print("L14 配套练习生成：%s (%d bytes)" % (p, os.path.getsize(p)))