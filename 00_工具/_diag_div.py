# -*- coding: utf-8 -*-
import re, importlib.util
spec = importlib.util.spec_from_file_location("t", r"D:\英语教学\00_工具\_transform_dxh.py")
t = importlib.util.module_from_spec(spec); spec.loader.exec_module(t)

for n, path in [(13, r"D:\英语教学\邓兴华\第13课时\课件成品_网页PPT\第13课时_课件_中等.html"),
                (14, r"D:\英语教学\邓兴华\第14课时\课件成品_网页PPT\第14课时_课件_中等.html"),
                (15, r"D:\英语教学\邓兴华\第15课时\课件成品_网页PPT\第15课时_课件_中等.html")]:
    raw = open(path, encoding="utf-8").read()
    css = re.search(r'<style>(.*?)</style>', raw, re.S).group(1)
    filtered = t.filter_css(css)
    parts = re.split(r'<div class="slide["\s]', raw)
    seq = []
    for part in parts[1:]:
        inner = t.extract_slide_content(part)
        if inner is not None:
            seq.append(inner)
    print("=== L%d: %d slides ===" % (n, len(seq)))
    total_o = total_c = 0
    for k, inner in enumerate(seq):
        o = inner.count('<div'); c = inner.count('</div>')
        total_o += o; total_c += c
        if o != c:
            print("  slide %d: div %d/%d diff=%d" % (k, o, c, o-c))
    print("  TOTAL div %d/%d diff=%d" % (total_o, total_c, total_o-total_c))
    print("  filtered CSS div? opens=%d closes=%d" % (filtered.count('{'), 0))