# -*- coding: utf-8 -*-
"""李民宪 L06 配套练习（培优）生成。内容直接存 paragraphs（无需 split）。
含听力20分（独立不计入笔试）+ 阅读30 + 语言运用25 + 综合技能25 + 语法诊断20。"""
import json, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


bp = _load("bp", "build_practice_paper.py")
content = json.load(open(os.path.join(HERE, "practice_content_LMX_L06.json"), encoding="utf-8"))

# 语法诊断：questions 中含 opts 的为单项选择(mc)，不含 opts 的为填空(fill)
gd = content["grammar_diag"]
gd["mc"] = [q for q in gd["questions"] if q.get("opts")]
gd["fill"] = [q for q in gd["questions"] if not q.get("opts")]

card = {
    "lesson": 6, "student": "李民宪", "tier": "培优", "stage": "S1", "type": "normal",
    "grammar": ["borrow/lend 辨析·give a lift·until", "祈使句与提建议(Let's/Can you help/Why not)", "社区活动信息(when/where/who/what/why)"],
    "theme": "Unit 2 Home Sweet Home② 家庭合作与社区",
    "vocab": {"new_count": 10, "review_count": 20, "theme": "community"},
    "phonics": "-all/-ill/-ell", "listening": True,
}

out = os.path.join(os.path.dirname(HERE), "李民宪", "第06课时", "第06课时_配套练习_培优.docx")
p = bp.build_practice(card, content, out)
print("配套练习生成：%s (%d bytes)" % (p, os.path.getsize(p)))