# -*- coding: utf-8 -*-
"""Backup old DXH courseware + run transformation for L13/L14/L15."""
import os, shutil, importlib.util

HERE = r"D:\英语教学\00_工具"
def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

T = _load("trans", "_transform_dxh.py")

BASE = r"D:\英语教学\邓兴华"
CONF = {
    13: ("shopping",  r"第13课时\课件成品_网页PPT\第13课时_课件_中等.html"),
    14: ("appearance", r"第14课时\课件成品_网页PPT\第14课时_课件_中等.html"),
    15: ("weather",   r"第15课时\课件成品_网页PPT\第15课时_课件_中等.html"),
}
SEG = {1:"复习导入",2:"新词20",3:"语法3考点",4:"随堂演练",5:"阅读理解",6:"句子练习",7:"自然拼读",8:"课堂总结"}

for lesson, (theme, rel) in CONF.items():
    old_dir = os.path.join(BASE, "第%d课时" % lesson, "课件成品_网页PPT")
    old_path = os.path.join(old_dir, "第%d课时_课件_中等.html" % lesson)
    bak = os.path.join(old_dir, "_旧件_slide_L%d" % lesson)
    os.makedirs(bak, exist_ok=True)
    shutil.copy2(old_path, os.path.join(bak, "第%d课时_课件_中等.html" % lesson))
    print("[backup] L%d -> %s" % (lesson, bak))
    out_path = os.path.join(HERE, "_L%d_new.html" % lesson)
    total, size = T.transform(old_path, lesson, SEG, out_path, theme)
    print("[L%d] 新课件: 页数=%d 体积=%d bytes" % (lesson, total, size))