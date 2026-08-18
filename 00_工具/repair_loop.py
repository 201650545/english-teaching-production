# -*- coding: utf-8 -*-
"""M10 自动修复环：生成 -> verify_v2 -> 再平衡/重分页 -> 复检，3 轮内自动修复或报具体原因
"""
import json, os, subprocess, sys, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))

def run_verify(html_path):
    r = subprocess.run([sys.executable, os.path.join(HERE, "verify_v2.py"), html_path],
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode == 0, r.stdout

def repair_loop(card, build_fn, out_path, max_rounds=3):
    """build_fn(card) -> html string。循环生成+校验，3 轮内自动修复或报原因。"""
    for round_i in range(1, max_rounds + 1):
        html = build_fn(card)
        open(out_path, "w", encoding="utf-8").write(html)
        ok, report = run_verify(out_path)
        print("== 修复环 第%d轮 ==" % round_i)
        print(report)
        if ok:
            print("==> 修复环 PASS（第%d轮）" % round_i)
            return True, round_i
    print("==> 修复环 FAIL：3 轮内未通过，请人工复核 verify_v2 报告")
    return False, max_rounds

if __name__ == "__main__":
    import courseware_engine
    card = {
        "lesson": 5, "student": "许颖嘉", "tier": "基础", "stage": "S1", "type": "normal",
        "grammar": ["祈使句基础", "What特殊疑问句", "like的用法"], "theme": "食物与日常",
        "vocab": {"new_count": 20, "review_count": 0, "theme": "food"},
        "phonics": "bl/cl/fl/gl/pl/sl",
        "reading": {"genres": ["记叙文", "说明文", "应用文"], "w5": True, "vocab_rate": "15%"},
        "listening": False,
        "interactions": {"count_equals_new_knowledge_points": True},
        "output": ["html", "docx", "outline_courseware", "outline_practice"]
    }
    out = os.path.join(HERE, "test_L5_courseware.html")
    repair_loop(card, courseware_engine.build_lesson, out)
