# -*- coding: utf-8 -*-
"""Final acceptance verification for 邓兴华 L13/L14/L15 practice DOCX.
Follows the _verify_l08_docx.py structural pattern (结构/题号/答案齐全).
"""
import os, re, sys
from docx import Document

def check(lesson):
    path = r"D:\英语教学\邓兴华\第%02d课时\第%02d课时_配套练习_中等.docx" % (lesson, lesson)
    print("=" * 60)
    print("L%d docx: %s" % (lesson, os.path.basename(path)))
    if not os.path.exists(path):
        print("  FAIL: file missing")
        return False
    print("  文件存在, 大小 %d bytes" % os.path.getsize(path))
    doc = Document(path)
    paras = [p.text for p in doc.paragraphs]
    full = "\n".join(paras)
    ok = True

    # 1. 主标题
    heading = None
    for p in paras[:6]:
        if "配套练习" in p:
            heading = p.strip()
            break
    if heading:
        print("  主标题: %s" % heading[:80])
    else:
        print("  FAIL: 未找到主标题(含'配套练习')")
        ok = False

    # 2. 结构部分
    parts = ["第一部分", "第二部分", "第三部分", "四", "参考答案", "双向细目表"]
    for kw in ["第一部分", "第二部分", "第三部分", "第四部分", "参考答案", "双向细目表"]:
        found = [p.strip()[:60] for p in paras if kw in p]
        status = found[:2] if found else "未找到"
        print("  [%s] -> %s" % (kw.replace("部分", "部分/"), status if isinstance(status, list) else status))
        if kw in ("第一部分", "第二部分", "第三部分", "参考答案", "双向细目表"):
            pass
    # 结构判断：一/二/三部分 + 参考答案 + 双向细目表
    sec_count = sum(1 for kw in ("第一部分", "第二部分", "第三部分", "第四部分") if any(kw in p for p in paras))
    has_answers = any("参考答案" in p for p in paras)
    has_table = any("双向细目表" in p for p in paras)
    print("  结构部分数: %d | 参考答案: %s | 双向细目表: %s" % (sec_count, has_answers, has_table))
    if sec_count < 3:
        print("  FAIL: 结构部分不足3个")
        ok = False
    if not has_answers:
        print("  FAIL: 缺参考答案")
        ok = False
    if not has_table:
        print("  FAIL: 缺双向细目表")
        ok = False

    # 3. 溯源ID
    ids = sorted(set(re.findall(r"DXH\d+_L\d+(?:_\w+)?", full)))
    print("  溯源ID数: %d %s" % (len(ids), ids[:10]))
    if not ids:
        print("  FAIL: 无溯源ID")
        ok = False

    # 4. 题号连续性（全卷连续，允许部分小节标题分隔）
    #   exam_spec: 笔试100分 -> 阅读+语言+综合+语法诊断
    nums = []
    for p in paras:
        m = re.match(r"^\s*(\d{1,2})[\.、．]\s*", p)
        if m:
            nums.append(int(m.group(1)))
    nums_set = sorted(set(nums))
    expected = list(range(1, max(nums_set) + 1)) if nums_set else []
    missing = [n for n in expected if n not in nums_set]
    dup = [n for n in set(nums_set) if nums.count(n) > 1]
    print("  题号范围: %s..%s (共%d个不同题号, %d个题号段落)" % (
        nums_set[0] if nums_set else "-", nums_set[-1] if nums_set else "-",
        len(nums_set), len(nums)))
    print("  缺失题号: %s" % (missing if missing else "无"))
    print("  重复题号: %s" % (dup if dup else "无"))
    if missing:
        print("  FAIL: 题号不连续, 缺失 %s" % missing)
        ok = False
    if nums_set and nums_set != expected:
        print("  FAIL: 题号集不与1..max连续")
        ok = False

    # 5. 答案齐全（参考答案中应含答案标注）
    if has_answers:
        ans_text = "\n".join(p for p in paras if "参考答案" in p or p.strip().startswith("1."))
        print("  答案区样例: %s" % ans_text[:200])

    # 6. L14/L15 禁过去时
    if lesson in (14, 15):
        PAST = [" was ", " were ", " went ", " came ", " had ", " did ", " said ",
                " told ", " saw ", " got ", " made ", " took ", " gave ", " bought ",
                " paid ", " spent ", " ate ", " drank ", " yesterday "]
        hits = {}
        for w in PAST:
            c = full.count(w)
            if c:
                hits[w.strip()] = c
        print("  过去时红线: %s" % ("PASS ✅" if not hits else "FAIL: " + str(hits)))
        if hits:
            ok = False

    print("  => %s" % ("PASS ✅" if ok else "FAIL ❌"))
    return ok

if __name__ == "__main__":
    results = [check(L) for L in (13, 14, 15)]
    print("=" * 60)
    print("汇总: %s" % ("ALL PASS ✅" if all(results) else "HAS FAILURE ❌"))
    sys.exit(0 if all(results) else 1)