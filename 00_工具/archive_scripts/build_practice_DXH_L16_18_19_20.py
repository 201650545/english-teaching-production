# -*- coding: utf-8 -*-
"""邓兴华 L16/L18/L19/L20 配套练习（中等）批量生成。"""
import json, os, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

spec = importlib.util.spec_from_file_location("bp", os.path.join(HERE, "build_practice_paper.py"))
bp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bp)

CARDS = {
    16: {"stage": "S4", "theme": "阶段测试Ⅱ·学习工具与学术任务", "grammar": ["G01-G42滚动"], "phonics": "无（测试课）"},
    18: {"stage": "S5", "theme": "现在进行时·家务", "grammar": ["G46 现在进行时", "G47 V-ing变化", "G48 标志词"], "phonics": "le /l/"},
    19: {"stage": "S5", "theme": "复合不定代词·周末", "grammar": ["G49 复合不定代词", "G50 形容词后置", "G51 主谓一致"], "phonics": "ture /tʃə/·tion /ʃə/"},
    20: {"stage": "S5", "theme": "语法终点·旅行综合", "grammar": ["G52 过去时全套", "G53 不定代词过去时", "G54 频度副词跨时态"], "phonics": "tion /ʃən/·ture /tʃə/"},
}

for lesson, meta in CARDS.items():
    content = json.load(open(os.path.join(HERE, "practice_content_DXH_L%02d.json" % lesson), encoding="utf-8"))
    card = {
        "lesson": lesson,
        "student": "邓兴华",
        "tier": "中等",
        "stage": meta["stage"],
        "type": "normal",
        "grammar": meta["grammar"],
        "theme": meta["theme"],
        "vocab": {"new_count": 20, "review_count": 0, "theme": meta["theme"]},
        "phonics": meta["phonics"],
        "listening": False,
    }
    out = os.path.join(os.path.dirname(HERE), "邓兴华", "第%02d课时" % lesson, "第%02d课时_配套练习_中等.docx" % lesson)
    p = bp.build_practice(card, content, out)
    print("L%d 配套练习生成：%s (%d bytes)" % (lesson, p, os.path.getsize(p)))
print("DONE")