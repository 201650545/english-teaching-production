import os, re, hashlib, json

BASE = "D:/英语教学/许颖嘉"
HTML_DIR = "课件成品_网页PPT"

def fingerprint(lesson):
    fn = f"第{lesson:02d}课时_课件_基础.html"
    path = os.path.join(BASE, f"第{lesson:02d}课时", HTML_DIR, fn)
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        html = f.read()
    # 提取 <style> 内容
    styles = re.findall(r'<style[^>]*>(.*?)</style>', html, re.S)
    css = "\n".join(styles)
    # 提取 JS 公共部分（脚本）
    scripts = re.findall(r'<script[^>]*>(.*?)</script>', html, re.S)
    js = "\n".join(scripts)
    # 页数
    pages = re.findall(r'id="page(\d+)"', html)
    page_max = max(int(p) for p in pages) if pages else 0
    # 题型数
    quiz_q = len(re.findall(r'class="quiz-q"', html))
    quiz_opt = len(re.findall(r'data-qid', html))
    # 主题色
    theme_match = re.search(r'THEME:\s*(\S+)', html)
    theme = theme_match.group(1) if theme_match else "default"
    # primary/accent
    primary = re.search(r'--primary\s*:\s*([^;]+)', html)
    accent = re.search(r'--accent\s*:\s*([^;]+)', html)
    return {
        "lesson": lesson,
        "size": len(html),
        "pages": page_max,
        "quiz_q": quiz_q,
        "quiz_opt": quiz_opt,
        "css_hash": hashlib.md5(css.encode()).hexdigest()[:12],
        "css_len": len(css),
        "js_hash": hashlib.md5(js.encode()).hexdigest()[:12],
        "theme": theme,
        "primary": primary.group(1).strip() if primary else "",
        "accent": accent.group(1).strip() if accent else "",
    }

results = []
for i in range(1, 27):
    r = fingerprint(i)
    if r:
        results.append(r)

# 聚类：按 css_hash 分组
groups = {}
for r in results:
    groups.setdefault(r["css_hash"], []).append(r["lesson"])

print("=== CSS 哈希聚类 ===")
for h, lessons in sorted(groups.items(), key=lambda x: -len(x[1])):
    print(f"  {h}: {lessons}")

print("\n=== 逐课明细 ===")
for r in results:
    print(f"L{r['lesson']:02d}: {r['size']}B {r['pages']}页 quiz_q={r['quiz_q']} data-qid={r['quiz_opt']} cssH={r['css_hash']} theme={r['theme']}")

with open("D:/英语教学/00_工具/_cluster_result.json", "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print("\n结果已存 _cluster_result.json")
