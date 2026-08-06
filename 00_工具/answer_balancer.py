# -*- coding: utf-8 -*-
"""M3 答案分布约束求解器：消除人工排字母（L4 曾 B34/C9 偏斜返工）。
输入: questions = [(题干, 正确项, [干扰项1, 干扰项2, ...]), ...]
输出: [(题干, [(字母, 文本, cor), ...]), ...]，正确项字母按轮转指派 → A/B/C(/D) 天然均衡。
validate(distribution) 供校验器调用。"""
import sys

LETTERS = "ABCDE"

def balance(questions, n_options=None, start=0):
    """questions: [(text, correct, [distractors]), ...]
    n_options: 每题选项数（None=按最多干扰项+1 自动，通常3）
    返回 [(text, [(letter, opt_text, "1"|"0"), ...]), ...]"""
    out = []
    for i, (text, correct, distractors) in enumerate(questions):
        k = n_options or (len(distractors) + 1)
        target = (start + i) % k                      # 轮转目标字母位
        opts = []
        di = iter(distractors)
        for pos in range(k):
            if pos == target:
                opts.append((LETTERS[pos], correct, "1"))
            else:
                opts.append((LETTERS[pos], next(di), "0"))
        out.append((text, opts))
    return out

def distribution(balanced):
    """统计 balanced 输出的正确字母分布。"""
    dist = {}
    for _, opts in balanced:
        for letter, _, cor in opts:
            if cor == "1":
                dist[letter] = dist.get(letter, 0) + 1
    return dist

def validate(dist, max_share=0.40):
    """校验无主导字母：占比最大者 ≤ max_share（默认40%）。返回 (ok, 说明)。"""
    total = sum(dist.values())
    if total == 0:
        return False, "无选择题"
    top = max(dist.values())
    share = top / total
    ok = share <= max_share
    return ok, ("分布 %s，最大占比 %.0f%%（阈值 %.0f%%）→ %s"
                % (dist, share * 100, max_share * 100, "合格" if ok else "主导字母偏斜"))

if __name__ == "__main__":
    # 演示：L4 式 28 题语法选择 → 自动均衡
    demo = [
        ("There ____ a book on the desk.", "is", ["are", "have"]),
        ("These ____ are new.", "boxes", ["box", "boxs"]),
        ("The ball is ____ the bed.", "under", ["on", "in"]),
        ("There ____ two cats.", "are", ["is", "have"]),
        ("A shelf → two ____.", "shelves", ["shelf", "shelfs"]),
        ("The cat is ____ the door.", "behind", ["between", "above"]),
        ("There ____ a book and two pens.", "is", ["are", "have"]),
        ("The lamp is ____ the window.", "next to", ["under", "in"]),
        ("How many ____ are there?", "children", ["child", "chily"]),
        ("The books are ____ the bookcase.", "in", ["on", "under"]),
        ("There ____ any apples.", "aren't", ["isn't", "are"]),
        ("My shoes are ____ the bed.", "under", ["on", "below"]),
        ("A knife → two ____.", "knives", ["knifes", "knife"]),
        ("____ the desk and the chair is a sofa.", "Between", ["Among", "Next"]),
        ("Tom ____ keeps his room tidy.", "always", ["never", "seldom"]),
        ("There ____ some water.", "is", ["are", "have"]),
        ("The picture is ____ the chair.", "on", ["above", "under"]),
        ("These ____ are messy.", "rooms", ["room", "roomes"]),
        ("The soccer ball is ____ the chair.", "under", ["below", "behind"]),
        ("The clothes are ____ the wardrobe.", "in", ["on", "under"]),
        ("There ____ three books and a pen.", "are", ["is", "have"]),
        ("A baby → two ____.", "babies", ["babys", "baby"]),
        ("The dog is ____ the sofa.", "under", ["on", "next"]),
        ("How many ____ can you see?", "boxes", ["box", "boxs"]),
        ("There ____ a cat and two dogs.", "is", ["are", "have"]),
        ("The keys are ____ the drawer.", "in", ["on", "under"]),
        ("These ____ are red.", "feet", ["foot", "foots"]),
        ("____ the bed and the window is a desk.", "Between", ["Among", "Next"]),
    ]
    b = balance(demo)
    dist = distribution(b)
    ok, msg = validate(dist)
    print("28题自动平衡 →", msg)
    for text, opts in b[:3]:
        print(" ", text, "→", ["%s.%s(%s)" % (l, t, c) for l, t, c in opts])
    sys.exit(0 if ok else 1)
