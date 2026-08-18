# -*- coding: utf-8 -*-
import docx, os, re
base = r"d:\英语教学\邓兴华"
outs = {
 "L13": ("第13课时","第13课时_配套练习_中等_3+2.docx"),
 "L14": ("第14课时","第14课时_配套练习_中等_3+2.docx"),
}
for k,(sub,fn) in outs.items():
    p = os.path.join(base,sub,fn)
    d = docx.Document(p)
    print(f"\n########## {k} {fn} ##########")
    for i,pa in enumerate(d.paragraphs):
        t=pa.text.strip()
        if not t: continue
        if t.startswith("Passage"):
            print(f"  [{i}]{t}  <-- passage")
        elif re.match(r'^\d{1,2}\.\s', t) or "（填空）" in t or re.match(r'^\d{1,2}~', t) or "参考答案"==t:
            print(f"  [{i}]{t}")