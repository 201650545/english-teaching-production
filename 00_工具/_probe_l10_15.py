# -*- coding: utf-8 -*-
"""探查 L10-L15 六课缺陷结构"""
import re, os

BASE = r"D:\英语教学\邓兴华"
def p(n):
    return os.path.join(BASE, "第%d课时" % n, "课件成品_网页PPT", "第%d课时_课件_中等.html" % n)

def probe(n):
    h = open(p(n), encoding="utf-8").read()
    print("=" * 60)
    print("L%02d  大小:%dB  页数:%d" % (n, len(h.encode("utf-8")), h.count('class="page"')))
    # 契约类型
    print("  契约: page-id=%d(40-45) / slide=%d / quiz-opt=%d / checkQuiz=%d" % (
        len(re.findall(r'id="page\d+"', h)), len(re.findall(r'class="slide', h)),
        h.count('class="quiz-opt'), h.count('checkQuiz(')))
    # 快闪
    print("  mini-flash-item=%d  mini-flash-grid=%d" % (h.count('mini-flash-item'), h.count('mini-flash-grid')))
    print("  flipCard定义=%s  调用=%d" % ("function flipCard" in h, h.count("flipCard(")))
    # 拖拽分类
    print("  sortCard调用=%d  sortCard2=%d  pickCard=%d  dropCard=%d" % (
        h.count("sortCard("), h.count("sortCard2("), h.count("pickCard("), h.count("dropCard(")))
    print("  dd-bin=%d  data-cat=%d" % (h.count("dd-bin"), h.count("data-cat")))
    # 连线
    print("  link-container=%d  match-item=%d  data-pair=%d  linkCheck=%d" % (
        h.count("link-container"), h.count("match-item"), h.count("data-pair"), h.count("linkCheck(")))
    # 五选四答案泄漏
    for pat in [r"答案[:：]", r"正确答案"]:
        m = re.findall(pat, h)
        if m:
            print("  泄漏[%s]: %d处" % (pat, len(m)))
    # Exit Ticket
    ex = re.findall(r"L%d-EX-\d+" % n, h)
    print("  ExitTicket题ID=%d %s" % (len(set(ex)), sorted(set(ex))))
    print("  exit-ticket类=%d  self-check/自评=%d" % (h.count("exit-ticket") + h.count("exit_ticket") + h.count("exitTicket"), h.count("自评") + h.count("self-check")))
    # 翻页机制
    print("  翻页: goPage=%d prevPage=%d nextPage=%d" % (h.count("goPage("), h.count("prevPage("), h.count("nextPage(")))
    # 页面id分布（找 Exit Ticket 在哪页）
    page_ids = re.findall(r'id="page(\d+)"', h)
    print("  page-id 范围: %s ... %s (共%d)" % (page_ids[0] if page_ids else "-", page_ids[-1] if page_ids else "-", len(page_ids)))

for n in range(10, 16):
    probe(n)
