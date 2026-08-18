# -*- coding: utf-8 -*-
"""邓兴华 L16 阶段测试卷（100 分标准卷 · 蓝图 4.1：阅读40/语言20/综合30/语法诊断10，G01-G42 覆盖）
格式统一 L05 compact：Times New Roman；标题16pt粗居中；节题14pt / 小标题12pt粗左；正文/选项10.5pt。
数据源：practice_content_DXH_L16.json（教师可审）。卷末附参考答案 + 双向细目表 + 溯源登记。
"""
import os, json, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = r"D:\英语教学\邓兴华"

# 复用 build_practice_DXH_L21_25 的渲染辅助函数（bpp = build_practice_paper）
_spec = importlib.util.spec_from_file_location("l21", os.path.join(HERE, "build_practice_DXH_L21_25.py"))
l21 = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(l21)
bpp = l21.bpp
_heading = bpp._heading; _para = bpp._para; _section = bpp._section; _sub = bpp._sub
_passage = bpp._passage; _options3 = bpp._options3; _question = bpp._question
_renumber = bpp._renumber; _ans_runs = bpp._ans_runs

def render_paper(lesson, content):
    doc = bpp.Document()
    for s in doc.sections:
        s.top_margin = bpp.Cm(1.5); s.bottom_margin = bpp.Cm(1.5)
        s.left_margin = bpp.Cm(1.5); s.right_margin = bpp.Cm(1.5)
    _heading(doc, "第 %02d 课时测试卷" % lesson)
    _para(doc, "学生：邓兴华    层级：中等    结构对齐 2026 湖南中考（不含听力）    满分：100 分",
          align=bpp.WD_ALIGN_PARAGRAPH.CENTER, size=10.5)
    _para(doc, "姓名：____________    得分：____________    用时：____________",
          align=bpp.WD_ALIGN_PARAGRAPH.CENTER, size=10.5)
    qnum = 1
    ans1_rd, ans1_w5 = [], []
    ans2_cl, ans2_gf = [], []
    ans3_sa, ans3_wr = [], []
    ans4 = []

    # ── 第一部分 阅读理解（满分 40）──
    _section(doc, "第一部分　阅读理解（共两节，满分 40 分）")
    _sub(doc, "第一节（共 15 小题，每小题 2 分）")
    for tag in ("a", "b", "c"):
        pg = content["reading_%s" % tag]
        _sub(doc, "Passage %s（%s · %d 词）" % (tag.upper(), pg.get("genre", ""), pg.get("word_count", "")))
        _passage(doc, pg["paragraphs"])
        for q in pg["questions"]:
            _question(doc, qnum, q["q"]); _options3(doc, q["opts"])
            ans1_rd.append((qnum, q["answer"])); qnum += 1
    _sub(doc, "第二节（共 5 小题，每小题 2 分，有一项多余）")
    w = content["w5"]
    _passage(doc, _renumber(w["paragraphs"], qnum))
    _para(doc, "方框：", size=10.5, bold=True, space_after=1)
    for letter, s in w["candidates"]:
        _para(doc, "%s. %s" % (letter, s), size=10.5, left_indent=bpp.OPT, space_after=1)
    for k, v in sorted(w["answers"].items(), key=lambda x: int(x[0])):
        g = qnum + int(k) - 1
        ans1_w5.append((g, v))
    qnum += len(w["answers"])

    # ── 第二部分 语言运用（满分 20）──
    _section(doc, "第二部分　语言运用（共两节，满分 20 分）")
    _sub(doc, "第一节　完形填空（共 10 小题，每小题 1 分）")
    c = content["cloze"]
    _passage(doc, _renumber(c["paragraphs"], qnum))
    for it in c["items"]:
        g = qnum + it["num"] - 1
        _options3(doc, it["opts"], num=g)
        ans2_cl.append((g, it["answer"]))
    qnum += len(c["items"])
    _sub(doc, "第二节　选词填空（共 10 小题，每小题 1 分）")
    wb = content["grammar_fill"]
    words = wb["word_bank"]; half = (len(words) + 1) // 2
    for i in range(0, len(words), half):
        _para(doc, "  ".join(words[i:i+half]), size=10.5, bold=True, space_after=1)
    _passage(doc, _renumber(wb["paragraphs"], qnum))
    for i, a in enumerate(wb["answers"]):
        ans2_gf.append((qnum + i, a))
    qnum += len(wb["answers"])

    # ── 第三部分 综合技能（满分 30）──
    _section(doc, "第三部分　综合技能（共两节，满分 30 分）")
    _sub(doc, "第一节　阅读表达（共 5 小题，每小题 1 分）")
    sa = content["sa"]
    _passage(doc, sa["paragraphs"])
    for i, q in enumerate(sa["questions"]):
        n = qnum + i
        _question(doc, n, q["q"])
        _para(doc, "    ____________________________________________________", size=10.5)
        ans3_sa.append((n, q["answer"]))
    qnum += len(sa["questions"])
    _sub(doc, "第二节　书面表达（满分 25 分）")
    wr = content["writing"]
    _para(doc, "%d. %s" % (qnum, wr["prompt"]), size=10.5, left_indent=bpp.QI, space_after=2)
    _para(doc, wr["requirements"], size=10.5, left_indent=bpp.QI, space_after=4)
    for _ in range(6):
        _para(doc, "    ________________________________________________________", size=10.5, space_after=2)
    ans3_wr.append((qnum, "见参考答案范文"))
    qnum += 1

    # ── 第四部分 语法诊断（满分 10）──
    gd = content["grammar_diag"]
    di_score = len(gd["mc"]) + len(gd.get("fill", []))
    _section(doc, "第四部分　语法诊断（满分 %d 分）" % di_score)
    _sub(doc, "语法诊断（共 %d 小题，每小题 1 分，G01-G42 覆盖）" % di_score)
    _sub(doc, "（一）单项选择")
    for q in gd["mc"]:
        _question(doc, qnum, q["q"]); _options3(doc, q["opts"])
        ans4.append((qnum, q["answer"])); qnum += 1
    if gd.get("fill"):
        _sub(doc, "（二）根据句意填空")
        for q in gd["fill"]:
            _question(doc, qnum, q["q"])
            ans4.append((qnum, q["answer"])); qnum += 1

    # ── 参考答案 ──
    doc.add_page_break()
    _section(doc, "参考答案")
    _sub(doc, "第一部分　阅读理解")
    for ln in _ans_runs(ans1_rd): _para(doc, ln, size=10.5, space_after=1)
    for n, a in ans1_w5: _para(doc, "%d. %s" % (n, a), size=10.5, space_after=1)
    _sub(doc, "第二部分　语言运用")
    _sub(doc, "第一节　完形填空")
    for ln in _ans_runs(ans2_cl): _para(doc, ln, size=10.5, space_after=1)
    _sub(doc, "第二节　选词填空")
    for n, a in ans2_gf: _para(doc, "%d. %s" % (n, a), size=10.5, space_after=1)
    _sub(doc, "第三部分　综合技能")
    _sub(doc, "第一节　阅读表达")
    for n, a in ans3_sa: _para(doc, "%d. %s" % (n, a), size=10.5, space_after=1)
    _sub(doc, "第二节　书面表达")
    _passage(doc, wr["sample"])
    _sub(doc, "第四部分　语法诊断")
    for n, a in ans4: _para(doc, "%d. %s" % (n, a), size=10.5, space_after=1)

    path = os.path.join(ROOT, "第%02d课时" % lesson, "第%02d课时_配套练习_中等.docx" % lesson)
    doc.save(path)
    return path, qnum - 1

if __name__ == "__main__":
    content = json.load(open(os.path.join(HERE, "practice_content_DXH_L16.json"), encoding="utf-8"))
    # 选项随机化：seed=课时号 打乱选择题选项，相邻两题正确字母不得相同（跨题型跟踪）
    bpp.randomize_all(content, 16)
    p, total = render_paper(16, content)
    print("L16 测试卷生成：%s（%d 题, %d bytes）" % (p, total, os.path.getsize(p)))
    print("DONE")