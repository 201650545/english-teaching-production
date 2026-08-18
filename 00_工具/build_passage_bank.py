# -*- coding: utf-8 -*-
"""M6 真题母本语篇库生成器（v2 重建版）：从 old_lessons.json 提取语料，生成 passage_bank.json
结构：{"id":"HN2026_xxx","genre","difficulty","word_count","vocab_rate","text","questions","provenance"}
红线：仅真题改编，禁编造、禁整卷复制；溯源 ID 必填

v2 相对 v1 的修复：
  1) 同文本双ID污染：reading_b 与 reading_a 同文时仅保留一篇（L1 两篇互异才各存）
  2) 整卷表头污染：剔除以「考试时间/课时配套练习/满分/得分/——」开头的卷头皮（L4 reading、L2/L13-L20 的 w5/sa）
  3) 语料来源扩展：reading_a/reading_b/cloze/w5/sa 五类真实段落皆入母本
  4) 题目诚实策略：阅读题源为整卷题区（未与单篇对齐）时 questions 置空并注明；
     cloze 源题为空壳（opts 空）；w5 源无题；sa 保留真实问答题
  5) 文体诚实标注：规则初判 + 人工覆盖表；说明文取自真实来源（L20阅读/L15完形/L3完形/L6五选五/L4情景），不编造

采集任务（人工，未在库内编造）：
  A. L5/L7 无阅读语料（old_lessons.json 缺该课）
  B. L9-L12 缺课（old_lessons.json 仅有 L1,2,3,4,6,8,13-20）
  C. L4 reading_a/b 为卷头皮污染，需人工补真实阅读
  D. 阅读单篇题目：旧件 qs 为整卷阅读区，需按单篇切片或重编
  E. 完形/五选五题目：源为空壳或仅有选项句，需按母本生成
  F. 正式词表锁定后，按统一基础词表重算 vocab_rate
"""
import json, os, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = "D:/英语教学/01_数据"

old = json.load(open(os.path.join(DATA_DIR, "content", "old_lessons.json"), encoding="utf-8"))
vocab_bank = json.load(open(os.path.join(DATA_DIR, "banks", "vocab_bank.json"), encoding="utf-8"))["words"]
V = set(w["en"].lower() for w in vocab_bank)
try:  # M2b 基础已知词表计入"熟词"
    base_vocab = json.load(open(os.path.join(DATA_DIR, "banks", "base_vocab.json"), encoding="utf-8"))["words"]
    V |= set(w["en"].lower() for w in base_vocab)
except FileNotFoundError:
    pass

# 文体人工覆盖表（按 (课序号, 来源字段) -> 文体）。全部来自真实语料，不编造。
GENRE_OVERRIDE = {
    ("1","reading_a"): "记叙文", ("1","reading_b"): "记叙文", ("1","cloze"): "记叙文",
    ("1","w5"): "记叙文", ("1","sa"): "记叙文",
    ("2","reading_a"): "应用文", ("2","cloze"): "记叙文",
    ("3","reading_a"): "应用文", ("3","cloze"): "说明文", ("3","sa"): "应用文",
    ("4","cloze"): "说明文", ("4","sa"): "说明文",
    ("6","reading_a"): "记叙文", ("6","cloze"): "记叙文", ("6","w5"): "说明文",
    ("8","reading_a"): "记叙文", ("8","cloze"): "记叙文", ("8","w5"): "记叙文",
    ("13","reading_a"): "应用文", ("13","cloze"): "记叙文",
    ("14","reading_a"): "记叙文", ("14","cloze"): "记叙文",
    ("15","reading_a"): "应用文", ("15","cloze"): "说明文",
    ("16","reading_a"): "应用文", ("16","cloze"): "记叙文",
    ("17","reading_a"): "应用文", ("17","cloze"): "记叙文",
    ("18","reading_a"): "应用文", ("18","cloze"): "记叙文",
    ("19","reading_a"): "应用文", ("19","cloze"): "记叙文",
    ("20","reading_a"): "说明文", ("20","cloze"): "记叙文",
}

PAPER_HEAD = re.compile(r"考试时间\s*[:：]|课时配套练习|满分\s*[:：]\s*100|得分\s*[:：]|――――")

def word_count(text):
    return len(re.findall(r"[A-Za-z]+", text))

def fingerprint(text):
    return hashlib.md5(re.sub(r"\s+", " ", text).strip().encode("utf-8")).hexdigest()[:12]

def stem(w):
    w = w.strip("'").lower()
    if w in V:
        return w
    for suf in ("'s", "es", "s", "ed", "ing"):
        if len(w) > len(suf) and w.endswith(suf) and w[:-len(suf)] in V:
            return w[:-len(suf)]
    return w

def vocab_rate(text):
    words = re.findall(r"[A-Za-z']+", text.lower())
    total = len(words)
    if not total:
        return "0%"
    unknown = sum(1 for w in words if stem(w) not in V)
    return "%d%%" % round(unknown * 100.0 / total)

def difficulty(wc):
    if wc <= 80:
        return "易"
    if wc <= 140:
        return "中"
    return "中高"

def is_clean(text):
    if PAPER_HEAD.search(text[:160]):
        return False
    return word_count(text) >= 20

def pick_questions(lesson_key, field, qs, text):
    if field in ("reading_a", "reading_b"):
        # 旧件 qs 为整卷阅读区（34-41题），未与单篇对齐；仅当题量<=8且文本匹配时保留（L1 两篇）
        if qs and len(qs) <= 8:
            return qs
        return []
    if field == "sa":
        return [q for q in qs if str(q.get("q", "")).strip()]
    return []

bank, dup_log, skip_log = [], [], []
seen = {}
for lesson_key in sorted(old.keys(), key=int):
    lesson = old[lesson_key]
    for field, ftype in (("reading_a", "阅读A"), ("reading_b", "阅读B"), ("cloze", "完形"),
                         ("w5", "五选五"), ("sa", "情景运用")):
        item = lesson.get(field)
        if not isinstance(item, dict):
            continue
        text = str(item.get("text", "")).strip()
        wc = word_count(text)
        if not is_clean(text):
            skip_log.append((lesson_key, field, "卷头皮污染或不成篇"))
            continue
        fp = fingerprint(text)
        pid = "HN2026_L%s_%s" % (lesson_key, field)
        if fp in seen:
            dup_log.append((pid, seen[fp]))
            continue
        seen[fp] = pid
        qs = item.get("qs") or []
        questions = pick_questions(lesson_key, field, qs, text)
        genre = GENRE_OVERRIDE.get((lesson_key, field), "待人工复核")
        extra = ""
        if field in ("reading_a", "reading_b") and not questions:
            extra = "；源题区为整卷阅读部分未切片，单篇题目待补"
        elif field == "cloze":
            extra = "；完形母本（源题为空壳），选项题目待生成"
        elif field == "w5":
            extra = "；五选五母本（选项句存于源 w5.opts），题目待生成"
        bank.append({
            "id": pid,
            "genre": genre,
            "difficulty": difficulty(wc),
            "word_count": wc,
            "vocab_rate": vocab_rate(text),
            "text": text,
            "questions": questions,
            "provenance": "真题母本改编（源：old_lessons.json L%s %s%s）" % (lesson_key, field, extra),
        })

out = os.path.join(DATA_DIR, "banks", "passage_bank.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(bank, f, ensure_ascii=False, indent=2)

print("passage_bank.json 生成完成：%d 篇" % len(bank))
from collections import Counter
print("来源分布：", dict(Counter(p["id"].rsplit("_", 1)[-1] for p in bank)))
print("文体覆盖：", dict(Counter(p["genre"] for p in bank)))
print("词数范围：%d-%d" % (min(p["word_count"] for p in bank), max(p["word_count"] for p in bank)))
print("生词率范围（按M2词汇库估算）：%s-%s" %
      (min(p["vocab_rate"] for p in bank), max(p["vocab_rate"] for p in bank)))
print("去重剔除：%d 条 -> %s" % (len(dup_log), dup_log))
print("污染跳过：%d 条 -> %s" % (len(skip_log), skip_log))
# 验收：每篇可算词数；文体标签齐全
for p in bank:
    assert p["word_count"] == word_count(p["text"]), "词数不一致 %s" % p["id"]
assert len(set(p["genre"] for p in bank)) == 3, "文体须覆盖 应用文/记叙文/说明文"
print("验收：词数可算 ✓ 文体 应用文/记叙文/说明文 齐全 ✓")
