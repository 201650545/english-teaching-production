import os, re, hashlib

BASE = "D:/英语教学/许颖嘉"
HTML_DIR = "课件成品_网页PPT"

def selectors(lesson):
    fn = f"第{lesson:02d}课时_课件_基础.html"
    path = os.path.join(BASE, f"第{lesson:02d}课时", HTML_DIR, fn)
    with open(path, encoding="utf-8") as f:
        html = f.read()
    styles = re.findall(r'<style[^>]*>(.*?)</style>', html, re.S)
    css = "\n".join(styles)
    # 提取所有选择器（花括号前的部分）
    sels = set()
    for m in re.finditer(r'([^{}]+)\{', css):
        sel = m.group(1).strip()
        if sel and not sel.startswith('/*') and not sel.startswith('@'):
            for part in sel.split(','):
                part = part.strip()
                if part:
                    sels.add(part)
    return sels

# 对比 22 课（L01-16,19-25）
core = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,19,20,21,22,23,24,25]
base_sel = selectors(core[0])
print(f"基准课 L{core[0]:02d} 选择器数: {len(base_sel)}")
print("\n差异课:")
for l in core[1:]:
    s = selectors(l)
    diff = base_sel ^ s
    print(f"  L{l:02d}: 选择器数={len(s)} 与基准差集={len(diff)}")

# 列出关键选择器供 recipe 设计
print("\n=== 关键选择器（含 body/.sh/.quiz/.card/.btn/.page/.progress/.tab/feedback）===")
for sel in sorted(base_sel):
    if any(k in sel for k in ['body','sh','quiz','card','btn','page','progress','tab','feedback','correct','wrong','option','head','title','nav','cover','opt']):
        print(f"  {sel}")
