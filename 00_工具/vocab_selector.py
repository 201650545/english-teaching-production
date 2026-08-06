# -*- coding: utf-8 -*-
"""M2 选词器：按主题+去重自动供词。
select(theme, count) → 该课新词列表；主题词不足时先预警再按频率补位，绝不用已用词。"""
import json, sys

def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

def select(theme, count, bank_path="vocab_bank.json", used_path="used_vocab.json", extra_used=None):
    bank = load(bank_path)["words"]
    used = set(load(used_path)["all"])
    if extra_used:
        used |= set(extra_used)
    # 未用词：主题优先，其余按入库顺序补位
    fresh = [w for w in bank if w["en"] not in used]
    themed = [w for w in fresh if w["theme"] == theme]
    others = [w for w in fresh if w["theme"] != theme]
    picked = (themed + others)[:count]
    result = {
        "theme": theme, "requested": count, "picked": len(picked),
        "theme_matched": len([w for w in picked if w["theme"] == theme]),
        "warning": None,
        "words": picked
    }
    if len(picked) < count:
        result["warning"] = "⚠️ 词库不足：仅供 %d/%d 个，请先扩充 %s 主题词库" % (len(picked), count, theme)
    elif result["theme_matched"] < count:
        result["warning"] = "ℹ️ 主题词 %d 个不足 %d，已用通用高频词补位 %d 个" % (result["theme_matched"], count, count - result["theme_matched"])
    return result

if __name__ == "__main__":
    theme = sys.argv[1] if len(sys.argv) > 1 else "food"
    count = int(sys.argv[2]) if len(sys.argv) > 2 else 20
    r = select(theme, count)
    print("主题:", r["theme"], "| 需求:", r["requested"], "| 实供:", r["picked"], "| 主题命中:", r["theme_matched"])
    if r["warning"]:
        print(r["warning"])
    for i, w in enumerate(r["words"], 1):
        print("%2d. %-12s %-14s %-6s %s" % (i, w["en"], w["phonetic"], w["pos"], w["cn"]))
