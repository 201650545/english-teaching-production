# -*- coding: utf-8 -*-
"""邓兴华 L06 配套练习（中等）拼装 + 生成。
reading_a/w5/cloze 取补题库 passage_questions.json + passage_bank.json（真题母本改编）；
reading_b/c 从 practice_content_DXH_L06.json 转 text→paragraphs；
wordbank→grammar_fill；grammar_diag 拆 5 选择 + 5 填空。
"""
import json, os, re, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
bp = _load("bp", "build_practice_paper.py")

bank = json.load(open(os.path.join(HERE, "passage_bank.json"), encoding="utf-8"))
pq = json.load(open(os.path.join(HERE, "passage_questions.json"), encoding="utf-8"))
c6 = json.load(open(os.path.join(HERE, "practice_content_DXH_L06.json"), encoding="utf-8"))

def split_paras(text, per=3):
    """把一段话按句切分并每 per 句合并为一个段落（保留原标点，对齐 L05 阅读段落格式）。"""
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip())
             if s.strip() and s.strip() not in ("A", "A.")]
    return [" ".join(sents[i:i+per]) for i in range(0, len(sents), per)]

# ---- reading_a（补题库） ----
ra_bank = next(x for x in bank if x["id"] == "HN2026_L6_reading_a")
ra_qs = pq["reading"]["HN2026_L6_reading_a"]
ra_paras = split_paras(ra_bank["text"].replace("A ", "", 1), per=2)
reading_a = {
    "id": ra_bank["id"], "genre": ra_bank.get("genre", "记叙文"),
    "difficulty": ra_bank.get("difficulty", "基础"), "word_count": ra_bank.get("word_count", 86),
    "provenance": ra_bank.get("provenance", "真题母本改编"), "paragraphs": ra_paras, "questions": ra_qs,
}

# ---- reading_b / reading_c（L06 JSON：text→paragraphs） ----
reading_b = dict(c6["reading_b"]); reading_b["paragraphs"] = split_paras(reading_b.pop("text"), per=2)
reading_c = dict(c6["reading_c"]); reading_c["paragraphs"] = split_paras(reading_c.pop("text"), per=2)

# ---- w5（补题库） ----
w5_bank = next(x for x in bank if x["id"] == "HN2026_L6_w5")
w5_data = pq["w5"]["HN2026_L6_w5"]
w5_txt = w5_bank["text"].strip()
# 越级改写（G16 上限仅一般现在时非三单；去将来时 will，保留语义；passage_bank 母本不动）
w5_txt = w5_txt.replace("for a healthy life that you will love!", "for a healthy life.")
# 把第 k 个无编号 ___ 替换为 ___k___
parts = w5_txt.split("___")
w5_re = parts[0]
for i in range(1, len(parts)):
    w5_re += "___%d___%s" % (i, parts[i])
w5_paras = split_paras(w5_re, per=2)
w5 = {
    "id": "HN2026_L6_w5", "title": "阅读短文，从方框中选择最佳句子填入空白处（有一项为多余选项）",
    "paragraphs": w5_paras, "candidates": w5_data["candidates"],
    "answers": {str(b["num"]): b["answer"] for b in w5_data["blanks"]},
}

# ---- cloze（补题库，编号 21-30 → 1-10） ----
cl_items = pq["cloze"]["HN2026_L6_cloze"]
cl_items = [dict(it, num=i + 1) for i, it in enumerate(cl_items)]
cl_bank = next(x for x in bank if x["id"] == "HN2026_L6_cloze")
cl_txt = cl_bank["text"].strip()
# 编号 21-30 → 1-10（顺序替换）
def ren_cl(m):
    return "___%d___" % (int(m.group(1)) - 20)
cl_txt = re.sub(r"___(\d+)___", ren_cl, cl_txt)
cl_paras = split_paras(cl_txt, per=2)
cloze = {"id": "HN2026_L6_cloze", "title": "阅读短文，从每题所给的 A、B、C 三个选项中选出最佳选项",
         "paragraphs": cl_paras, "items": cl_items}

# ---- grammar_fill（wordbank→grammar_fill） ----
wb = c6["wordbank"]
grammar_fill = {"id": wb["id"], "title": wb.get("title", "从方框内选择适当的词并用其正确形式填空"),
                "paragraphs": [wb["passage"]], "word_bank": wb["word_bank"], "answers": wb["answers"],
                "绑定": "G16·G17·G18·want to do"}

# ---- sa（text→paragraphs） ----
sa = dict(c6["sa"]); sa["paragraphs"] = split_paras(sa.pop("text"), per=2)

# ---- writing ----
writing = dict(c6["writing"])

# ---- grammar_diag（10 选择 → 5 选择 + 5 填空） ----
gd = c6["grammar_diag"]
gd_qs = gd["questions"]
mc = gd_qs[:5]
fill = [
    {"q": "用所给词的适当形式填空：I ___ (like) apples.", "answer": "like"},
    {"q": "We ___ (not eat) fast food.", "answer": "don't eat"},
    {"q": "___ (do) you want rice?", "answer": "Do"},
    {"q": "I want ___ (eat) an apple.", "answer": "to eat"},
    {"q": "I drink two ___ (egg) every morning.", "answer": "eggs"},
]
grammar_diag = {"id": gd["id"], "title": gd.get("title", "语法复盘（G16·G17·G18）"), "mc": mc, "fill": fill}

content = {
    "_doc": "邓兴华 L06 配套练习内容（中等）· 2026-08-03 重出。阅读A/五选四/完形取 passage_questions 补题库（真题母本改编）；阅读B/C、选词、简答、书面、语法诊断取本文件。",
    "reading_a": reading_a, "reading_b": reading_b, "reading_c": reading_c,
    "w5": w5, "cloze": cloze, "grammar_fill": grammar_fill,
    "sa": sa, "writing": writing, "grammar_diag": grammar_diag,
}

card = {
    "lesson": 6, "student": "邓兴华", "tier": "中等", "stage": "S2", "type": "normal",
    "grammar": ["一般现在时实义动词", "食物可数与不可数", "want to do"],
    "theme": "三餐与饮食习惯", "vocab": {"new_count": 20, "review_count": 0, "theme": "food"},
    "phonics": "26字母总复习+5易混音对", "listening": False,
}

out = os.path.join(os.path.dirname(HERE), "邓兴华", "第06课", "第06课_配套练习_中等.docx")
p = bp.build_practice(card, content, out)
print("配套练习生成：%s (%d bytes)" % (p, os.path.getsize(p)))
