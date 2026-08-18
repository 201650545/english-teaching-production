# -*- coding: utf-8 -*-
import re
h=open(r'D:\英语教学\邓兴华\第20课时\课件成品_网页PPT\第20课时_课件_中等.html',encoding='utf-8').read()
for i,m in enumerate(re.finditer(r'<script[^>]*>(.*?)</script>', h, re.S)):
    tag=m.group(0)
    # find the opening script tag attrs
    open_tag=tag[:tag.find('>')+1]
    body=m.group(1)
    print("=== block %d opening tag: %s ==="%(i,open_tag))
    print(body[:300])
    print("...len=%d...\n"%(len(body)))
# also check other script tags with type attr
for m in re.finditer(r'<script[^>]*>',h):
    print("SCRIPT TAG:",m.group(0))