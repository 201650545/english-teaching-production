"""李民宪 L01 配套练习（培优）拼装 + 生成。
reading_a/w5/cloze 取 passage_questions.json + passage_bank.json（真题母本改编）；
reading_b/c 从 practice_content_LMX_L01.json 转 text→paragraphs；
wordbank→grammar_fill；grammar_diag 拆 5 选择 + 5 填空。
无听力（教师 2026-08-04 确认）。
"""
import json, os, re, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
bp = _load("bp", "build_practice_paper.py")

bank = json.load(open(os.path.join(HERE, "passage_bank.json"), encoding="utf-8"))
pq = json.load(open(os.path.join(HERE, "passage_questions.json"), encoding="utf-8"))
c1 = json.load(open(os.path.join(HERE, "practice_content_LMX_L01.json"), encoding="utf-8"))

def split_paras(text, per=3):
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip())
             if s.strip() and s.strip() not in ("A", "A.")]
    return [" ".join(sents[i:i+per]) for i in range(0, len(sents), per)]

# ---- reading_a（L01 JSON：真题母本扩写至培优词数，text→paragraphs） ----
reading_a = dict(c1["reading_a"]); reading_a["paragraphs"] = split_paras(reading_a.pop("text"), per=2)

# ---- reading_b / reading_c（L01 JSON：text→paragraphs） ----
reading_b = dict(c1["reading_b"]); reading_b["paragraphs"] = split_paras(reading_b.pop("text"), per=2)
reading_c = dict(c1["reading_c"]); reading_c["paragraphs"] = split_paras(reading_c.pop("text"), per=2)

# ---- w5（补题库） ----
w5_bank = next(x for x in bank if x["id"] == "HN2026_L1_w5")
w5_data = pq["w5"]["HN2026_L1_w5"]
w5_txt = w5_bank["text"].strip()
parts = w5_txt.split("___")
w5_re = parts[0]
for i in range(1, len(parts)):
    w5_re += "___%d___%s" % (i, parts[i])
w5_paras = split_paras(w5_re, per=2)
w5 = {
    "id": "HN2026_L1_w5", "title": "阅读短文，从方框中选择最佳句子填入空白处（有一项为多余选项）",
    "paragraphs": w5_paras, "candidates": w5_data["candidates"],
    "answers": {str(b["num"]): b["answer"] for b in w5_data["blanks"]},
}

# ---- cloze（补题库，编号 1-10） ----
cl_items = pq["cloze"]["HN2026_L1_cloze"]
cl_items = [dict(it, num=i + 1) for i, it in enumerate(cl_items)]
cl_bank = next(x for x in bank if x["id"] == "HN2026_L1_cloze")
cl_txt = cl_bank["text"].strip()
cl_paras = split_paras(cl_txt, per=2)
cloze = {"id": "HN2026_L1_cloze", "title": "阅读短文，从每题所给的 A、B、C 三个选项中选出最佳选项",
         "paragraphs": cl_paras, "items": cl_items}

# ---- grammar_fill（wordbank→grammar_fill） ----
wb = c1["grammar_fill"]
grammar_fill = {"id": wb["id"], "title": wb.get("title", "从方框内选择适当的词并用其正确形式填空"),
                "paragraphs": [wb["passage"]], "word_bank": wb["word_bank"], "answers": wb["answers"],
                "绑定": "五大句型·一般过去时·复合不定代词"}

# ---- sa（text→paragraphs） ----
sa = dict(c1["sa"]); sa["paragraphs"] = split_paras(sa.pop("text"), per=2)

# ---- writing ----
writing = dict(c1["writing"])

# ---- grammar_diag（10 选择 → 5 选择 + 5 填空） ----
gd = c1["grammar_diag"]
gd_qs = gd["questions"]
mc = gd_qs[:5]
fill = [
    {"q": "用所给词的适当形式填空：We (visit) ___ the museum last week.", "answer": "visited"},
    {"q": "用所给词的适当形式填空：She (be) ___ happy last week.", "answer": "was"},
    {"q": "用所给词的适当形式填空：There (be) ___ something in the box.", "answer": "is"},
    {"q": "用所给词的适当形式填空：Did you (go) ___ anywhere yesterday?", "answer": "go"},
    {"q": "用所给词的适当形式填空：He (show) ___ us his photos yesterday.", "answer": "showed"},
]
grammar_diag = {"id": gd["id"], "title": gd.get("title", "语法诊断（五大句型/过去时/不定代词）"), "mc": mc, "fill": fill}

content = {
    "_doc": "李民宪 L01 配套练习内容（培优）· 2026-08-04 重出。阅读A/五选四/完形取 passage_questions 补题库（真题母本改编）；阅读B/C、语法填空、简答、书面、语法诊断取本文件。无听力。",
    "reading_a": reading_a, "reading_b": reading_b, "reading_c": reading_c,
    "w5": w5, "cloze": cloze, "grammar_fill": grammar_fill,
    "sa": sa, "writing": writing, "grammar_diag": grammar_diag,
}

card = {
    "lesson": 1, "student": "李民宪", "tier": "培优", "stage": "S1", "type": "normal",
    "grammar": ["五大基本句型", "一般过去时", "复合不定代词"],
    "theme": "综合诊断与 Unit 1 假期主题导入", "vocab": {"new_count": 10, "review_count": 20, "theme": "review"},
    "phonics": "a_e/i_e/o_e/u_e", "listening": False,
}

out = os.path.join(os.path.dirname(HERE), "李民宪", "第01课时", "第01课时_配套练习.docx")
p = bp.build_practice(card, content, out)
print("配套练习生成：%s (%d bytes)" % (p, os.path.getsize(p)))