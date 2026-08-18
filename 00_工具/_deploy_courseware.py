# -*- coding: utf-8 -*-
import shutil, io, os
pairs = [
    (r"D:\英语教学\00_工具\_L13_new.html", r"D:\英语教学\邓兴华\第13课时\课件成品_网页PPT\第13课时_课件_中等.html"),
    (r"D:\英语教学\00_工具\_L14_new.html", r"D:\英语教学\邓兴华\第14课时\课件成品_网页PPT\第14课时_课件_中等.html"),
    (r"D:\英语教学\00_工具\_L15_new.html", r"D:\英语教学\邓兴华\第15课时\课件成品_网页PPT\第15课时_课件_中等.html"),
]
for src, dst in pairs:
    shutil.copy2(src, dst)
    c = io.open(dst, encoding="utf-8").read()
    pages = len(__import__("re").findall(r'id="page\d+"', c))
    size = os.path.getsize(dst)
    print(dst, "size=%d" % size, "pages=%d" % pages)