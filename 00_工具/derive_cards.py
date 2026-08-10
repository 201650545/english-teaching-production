# -*- coding: utf-8 -*-
"""M1 简报派生器：学生简报(4行) + lesson_map.json → 课程卡（引擎唯一输入）。
用法: python derive_cards.py <student_brief.json> <lesson_no|all>"""
import json, sys
DATA_DIR = "D:/英语教学/01_数据"

TIER_RATE = {"基础": "15%", "中等": "17%", "培优": "20%"}
GENRES = ["记叙文", "说明文", "应用文"]

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def derive_card(brief, lesson_no, lesson_map):
    """由简报 + 大纲数据 派生单课课程卡。"""
    lm = lesson_map
    key = str(lesson_no)
    if key in lm["lessons"]:
        m = lm["lessons"][key]
        card = {
            "lesson": lesson_no,
            "student": brief["student"],
            "tier": brief["tier"],
            "stage": m["stage"],
            "type": m["type"],
            "grammar": m["grammar"],
            "theme": m.get("name", m["theme"]),
            "vocab": {
                "new_count": brief["new_words"] if m["type"] == "normal" else 0,
                "review_count": brief["review_words"] if m["type"] == "normal" else brief["new_words"] + brief["review_words"],
                "theme": m["vocab_theme"]
            },
            "phonics": m["phonics"],
            "reading": {"genres": GENRES, "w5": True, "vocab_rate": TIER_RATE[brief["tier"]]},
            "listening": bool(brief.get("listening", False)),
            "interactions": {"count_equals_new_knowledge_points": True},
            "output": ["html", "docx", "outline_courseware", "outline_practice"]
        }
    else:
        sp = lm["sprint"]
        assert sp["range"][0] <= lesson_no <= sp["range"][1], "课时超出范围"
        diag = sp["diagnostics"].get(str(lesson_no))
        card = {
            "lesson": lesson_no,
            "student": brief["student"],
            "tier": brief["tier"],
            "stage": "S5-8",
            "type": "sprint",
            "grammar": ["60考点综合应用"],
            "theme": diag if diag else "省卷五大题型SOP演练",
            "vocab": {"new_count": 0, "review_count": brief["new_words"] + brief["review_words"], "theme": "review"},
            "phonics": "综合复习",
            "reading": {"genres": GENRES, "w5": True, "vocab_rate": TIER_RATE[brief["tier"]]},
            "listening": bool(brief.get("listening", False)),
            "skills_rotation": sp["skills"],
            "is_diagnostic": bool(diag),
            "interactions": {"count_equals_new_knowledge_points": True},
            "output": ["html", "docx", "outline_courseware", "outline_practice"]
        }
    return card

def main():
    brief = load(sys.argv[1])
    lm = load(os.path.join(DATA_DIR, "schemas", "lesson_map.json"))
    target = sys.argv[2] if len(sys.argv) > 2 else "all"
    # 红线第一章第7条：派生新课课程卡时主题查重（复习/诊断课 review 豁免）。
    from check_theme_reuse import load_registry, cmd_check
    reg = load_registry()
    student = brief["student"]
    def gate(card):
        cmd_check(reg, student, card["lesson"], card["vocab"]["theme"], exclude_lesson=card["lesson"])
    if target == "all":
        cards = [derive_card(brief, n, lm) for n in range(1, int(brief.get("lessons_total", 40)) + 1)]
        for card in cards:
            gate(card)
        print(json.dumps(cards, ensure_ascii=False, indent=1))
    else:
        card = derive_card(brief, int(target), lm)
        gate(card)
        print(json.dumps(card, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
