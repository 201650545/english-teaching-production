# -*- coding: utf-8 -*-
import io
files = [
    r"D:\英语教学\00_工具\_L13_new.html",
    r"D:\英语教学\00_工具\_L14_new.html",
    r"D:\英语教学\00_工具\_L15_new.html",
]
OLD = "var q=btn.parentNode; if(q.dataset.done) return; q.dataset.done='1';"
NEW = "var q=btn.closest('.quiz-container')||btn.closest('.quiz-q')||btn.parentNode; if(q.dataset.done) return; q.dataset.done='1';"
for f in files:
    s = io.open(f, encoding="utf-8").read()
    n = s.count(OLD)
    if n == 0:
        print(f, "NO MATCH")
        continue
    s = s.replace(OLD, NEW)
    io.open(f, "w", encoding="utf-8").write(s)
    print(f, "patched", n, "occurrences")