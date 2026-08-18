import subprocess, os, re, json

BASE = "D:/英语教学/许颖嘉"
HTML_DIR = "课件成品_网页PPT"
TOOL = "D:/英语教学/00_工具"
PYTHON = "C:/Users/郭永涛/.workbuddy/binaries/python/versions/3.13.12/python.exe"
VERIFY = os.path.join(TOOL, "verify_v2.py")
INTVERIFY = os.path.join(TOOL, "verify_interaction_v1.py")

results = []
for i in range(1, 27):
    fn = f"第{i:02d}课时_课件_基础.html"
    html_path = os.path.join(BASE, f"第{i:02d}课时", HTML_DIR, fn)
    if not os.path.exists(html_path):
        results.append({"lesson": i, "v2": "NOFILE", "inter": "NOFILE"})
        continue
    # verify_v2
    pro = subprocess.run([PYTHON, VERIFY, "--force", html_path], capture_output=True, text=True, timeout=120)
    v2_pass = "PASS" in (pro.stdout + pro.stderr)
    # verify_interaction
    pro2 = subprocess.run([PYTHON, INTVERIFY, "--force", html_path], capture_output=True, text=True, timeout=120)
    out2 = pro2.stdout + pro2.stderr
    inter_err = 0
    for line in out2.split("\n"):
        if "ERROR" in line and "VIS-" in line:
            inter_err += 1
    inter_warn = 0
    for line in out2.split("\n"):
        if "WARN" in line and "VIS-" in line:
            inter_warn += 1
    # 提取 v2 ERROR 数
    v2_error = -1
    m = re.search(r'视觉完整性.*?(\d+)\s*ERROR', out2 + pro2.stdout + pro.stderr)
    if m:
        v2_error = int(m.group(1))
    m2 = re.search(r'视觉完整性.*?(\d+)\s*ERROR', pro.stdout + pro.stderr)
    if m2:
        v2_error = int(m2.group(1))
    results.append({"lesson": i, "v2": "PASS" if v2_pass else "FAIL", "inter_err": inter_err, "inter_warn": inter_warn, "v2_error": v2_error})
    print(f"L{i:02d}: v2={'PASS' if v2_pass else 'FAIL'} v2E={v2_error} interERR={inter_err} interWARN={inter_warn}")

with open(os.path.join(TOOL, "_diff_verify_results.json"), "w") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
print(f"\n完成 {len(results)} 课")
