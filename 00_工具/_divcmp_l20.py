# -*- coding: utf-8 -*-
import re, sys
def check(p, label):
    h = open(p, encoding='utf-8').read()
    opens = len(re.findall(r'<div\b', h))
    closes = len(re.findall(r'</div>', h))
    sys.stdout.buffer.write(("%s: opens=%d closes=%d diff=%d\n" % (label, opens, closes, opens-closes)).encode('utf-8','replace'))
check(r'D:\英语教学\邓兴华\第20课时\_旧件_收尾前20260808\课件成品_网页PPT\第20课时_课件_中等.html', 'L20 backup')
check(r'D:\英语教学\邓兴华\第20课时\课件成品_网页PPT\第20课时_课件_中等.html', 'L20 current')