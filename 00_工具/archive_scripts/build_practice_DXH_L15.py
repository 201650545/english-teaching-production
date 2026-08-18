# -*- coding: utf-8 -*-
"""邓兴华 L15 配套练习（中等）生成。"""
import json, os, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

with open(os.path.join(HERE, "practice_content_DXH_L15.json"), encoding="utf-8") as f:
    content = json.load(f)

spec = importlib.util.spec_from_file_location("bp", os.path.join(HERE, "build_practice_paper.py"))
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

card = {
    "lesson": 15,
    "student": "邓兴华",
    "tier": "中等",
    "stage": "S4",
    "type": "normal",
    "grammar": ["G40 天气表达句型", "G41 Could-Would 礼貌请求", "G42 非人称 It"],
    "theme": "天气·季节与度假",
    "vocab": {"new_count": 20, "review_count": 140, "theme": "weather"},
    "phonics": "oo /uː/ · ew /juː/",
    "listening": False,
}

out = os.path.join(os.path.dirname(HERE), "邓兴华", "第15课时", "第15课时_配套练习_中等.docx")
p = bp.build_practice(card, content, out)
print("L15 配套练习生成：%s (%d bytes)" % (p, os.path.getsize(p)))