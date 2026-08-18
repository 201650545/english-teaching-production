# -*- coding: utf-8 -*-
import re
path = r"D:\英语教学\邓兴华\第13课时\课件成品_网页PPT\第13课时_课件_中等.html"
c = open(path, encoding="utf-8").read()
# split by slide opening tags
parts = re.split(r'<div class="slide', c)
print("slide 块数:", len(parts)-1)
for i, part in enumerate(parts[1:], 1):
    # get data-section and data-page from the opening tag attributes
    msec = re.search(r'data-section="([^"]*)"', part)
    mpg  = re.search(r'data-page="(\d+)"', part)
    sec = msec.group(1) if msec else "?"
    pg  = mpg.group(1) if mpg else "?"
    # find titles
    heads = re.findall(r'<(h[1-3])[^>]*>(.*?)</\1>', part, re.S)
    heads = [re.sub(r'<[^>]+>','',h).strip()[:70] for _,h in heads]
    sh = re.findall(r'<h2[^>]*>(.*?)</h2>', part, re.S)
    sh = [re.sub(r'<[^>]+>','',x).strip()[:70] for x in sh]
    gf = re.findall(r'class="gf-title"[^>]*>(.*?)</div>', part, re.S)
    gf = [re.sub(r'<[^>]+>','',g).strip()[:50] for g in gf]
    print(f"P{pg} [{sec}] h={heads[:3]} gf={gf[:3]}")