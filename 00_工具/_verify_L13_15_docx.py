# -*- coding: utf-8 -*-
import io, re, zipfile, sys
from xml.etree import ElementTree as ET

def docx_text(path):
    z = zipfile.ZipFile(path)
    xml = z.read("word/document.xml").decode("utf-8")
    ns = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
    root = ET.fromstring(xml)
    paras = []
    for p in root.iter(ns+"p"):
        texts = [t.text or "" for t in p.iter(ns+"t")]
        paras.append("".join(texts))
    return paras

PAST = [" was "," were "," went "," came "," had "," did "," said "," told ",
        " saw "," got "," made "," took "," gave "," bought "," paid "," spent ",
        " ate "," drank "," walked "," visited "," stayed "," arrived "," asked ",
        " wanted "," started "," finished "," played "," watched "," studied ",
        " lived "," learned "," learnt "," thanked "," smiled "," yesterday"]

for L in (13,14,15):
    path = r"D:\英语教学\邓兴华\第%d课时\第%d课时_配套练习_中等.docx" % (L,L)
    paras = docx_text(path)
    full = "\n".join(paras)
    print("========== L%d DOCX (%d 段落) ==========" % (L, len(paras)))
    # 结构标题
    for kw in ["一、","二、","三、","四、","阅读","语言运用","综合技能","语法巩固","双向细目表","溯源"]:
        if kw in full:
            pass
    import re as _re
    secs = [p for p in paras if _re.match(r'^[一二三四]、', p)]
    print("部分标题:", secs)
    # 溯源ID
    ids = sorted(set(_re.findall(r"DXH\d+_L\d+\w*", full)))
    print("溯源ID数:", len(ids), ids[:8])
    # 题号连续检查
    nums = [int(m) for p in paras for m in _re.findall(r'^\s*(\d{1,2})\.\s', p)]
    nums2 = [int(m) for p in paras for m in _re.findall(r'^\s*(\d{1,2})[、．.]\s', p)]
    allnums = sorted(set(nums+nums2))
    expect = list(range(1, max(allnums)+1)) if allnums else []
    print("题号样本:", allnums[:5], "...", allnums[-5:] if allnums else [])
    print("题号连续:", allnums == expect if allnums else "N/A")
    # 细目表
    print("含双向细目表:", "双向细目表" in full, "| 含溯源登记:", "溯源" in full)
    # 过去时（L14/L15红线）
    if L in (14,15):
        finds = {}
        for w in PAST:
            c = full.count(w)
            if c: finds[w.strip()] = c
        print("L%d 过去时命中:" % L, finds if finds else "NONE ✅")
    print()