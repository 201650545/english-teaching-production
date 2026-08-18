# -*- coding: utf-8 -*-
"""M11 CI 门：课程卡哈希变更才重建；输出「课×规则」PASS/FAIL 表
"""
import json, os, hashlib, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
STATE_FILE = os.path.join(HERE, "build_state.json")

def card_hash(card):
    return hashlib.sha256(json.dumps(card, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()

def load_state():
    if os.path.exists(STATE_FILE):
        return json.load(open(STATE_FILE, encoding="utf-8"))
    return {}

def save_state(state):
    json.dump(state, open(STATE_FILE, "w", encoding="utf-8"), ensure_ascii=False, indent=2)

def build_all(cards, build_fn, out_dir):
    """cards=[(name, card, out_path)]。哈希变更才重建；输出 PASS/FAIL 表。"""
    state = load_state()
    results = []
    for name, card, out_path in cards:
        h = card_hash(card)
        if state.get(name) == h and os.path.exists(out_path):
            results.append((name, "SKIP（哈希未变）", "PASS"))
            continue
        html = build_fn(card)
        open(out_path, "w", encoding="utf-8").write(html)
        r = subprocess.run([sys.executable, os.path.join(HERE, "verify_v2.py"), out_path],
                           capture_output=True, text=True, encoding="utf-8")
        ok = r.returncode == 0
        state[name] = h
        results.append((name, "重建", "PASS" if ok else "FAIL"))
    save_state(state)
    print("== CI 门 · 课×规则 PASS/FAIL 表 ==")
    print("%-12s %-10s %s" % ("课程", "动作", "结果"))
    for name, action, res in results:
        print("%-12s %-10s %s" % (name, action, res))
    return all(res == "PASS" for _, _, res in results)

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
    build_all([("L5", card, out)], courseware_engine.build_lesson, HERE)
