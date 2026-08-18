# -*- coding: utf-8 -*-
"""李民宪 L08 配套练习（培优）生成。内容直接存 paragraphs。含听力20分。"""
import json, os, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))


def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


bp = _load("bp", "build_practice_paper.py")
content = json.load(open(os.path.join(HERE, "practice_content_LMX_L08.json"), encoding="utf-8"))

gd = content["grammar_diag"]
gd["mc"] = [q for q in gd["questions"] if q.get("opts")]
gd["fill"] = [q for q in gd["questions"] if not q.get("opts")]

card = {
    "lesson": 8, "student": "李民宪", "tier": "培优", "stage": "S1", "type": "normal",
    "grammar": ["比较级复现运用(more/as/the most)", "Fact vs Opinion 区分", "观点表达句型(In my opinion/For example/However)"],
    "theme": "Unit 3 Same or Different?② 友谊与观点",
    "vocab": {"new_count": 10, "review_count": 20, "theme": "friendship"},
    "phonics": "-tion/-sion (/ʃən/ vs /ʒən/)", "listening": True,
}

out = os.path.join(os.path.dirname(HERE), "李民宪", "第08课时", "第08课时_配套练习_培优.docx")
p = bp.build_practice(card, content, out)
print("配套练习生成：%s (%d bytes)" % (p, os.path.getsize(p)))