# -*- coding: utf-8 -*-
"""M5 语法库增强：从许颖嘉 单课内容蓝图 语法详案 逐课填实 grammar_bank.json
数据源：许颖嘉\内容蓝图\单课\第XX课_内容蓝图.md（语法详案：口诀/公式矩阵/例句/中考辨析/易错点/防越级约束）
映射：grammar_bank 条目 lesson + 序号 ↔ 蓝图 语法①/②/③

v2 修复：
  1) 例句抽取只取表头含「示例/例句」的表；拒绝阅读策略行、---、**、占位等脏数据
  2) 多例句单元格按 / 拆分；编号例句 + 表例句去重后最多 6 条
  3) 中考考法/六色卡/易错5 统一 clean_md 清洗（去 **、>、|、多余空白）
  4) 越级清洗逻辑保留（FORBIDDEN 词表），防 verify_v2 扫描
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
BLUEPRINT_DIR = os.path.join(os.path.dirname(HERE), "许颖嘉", "内容蓝图", "单课")

def clean_md(text):
    """清理 markdown 标记：>、|、**、首尾空白"""
    t = re.sub(r"[>|]", "", str(text))
    t = t.replace("**", "")
    return re.sub(r"\s+", " ", t).strip()

JUNK = re.compile(r"---|\*\*|占位|待补|TODO|TBD")
READING_TIP = re.compile(r"速读|精读|圈出|通读|划关键词|回答[\"“]")

def is_good_example(x):
    x = str(x).strip()
    if not x:
        return False
    if JUNK.search(x) or READING_TIP.search(x):
        return False
    return len(re.findall(r"[A-Za-z]+", x)) >= 2

def split_tables(block):
    """把块内 markdown 表格拆成独立表格（每张表 = 行列表，跳过 --- 分隔行）"""
    tables, cur = [], None
    for line in block.splitlines():
        s = line.strip()
        if s.startswith("|") and s.endswith("|"):
            if "---" in s:
                continue  # 分隔行：不打断表格
            if cur is None:
                cur = []
            cur.append(line)
        else:
            if cur:
                tables.append(cur)
                cur = None
    if cur:
        tables.append(cur)
    return tables

def parse_grammar_block(block):
    """解析单个 语法①②③ 子块，返回 dict"""
    d = {}
    # 口诀：**口诀**：后内容（可能是 > "..."、> 文本、或直接文本）
    m = re.search(r"\*\*口诀\*\*[:：]\s*(?:>\s*)?[\"“]?(.*?)[\"”]?\s*(?:\n|$)", block, re.S)
    if m:
        d["口诀"] = m.group(1).strip().replace("\n", " ")
    # 防越级约束
    m = re.search(r"\*\*防越级约束\*\*[:：]\s*(.*?)(?:\n\s*\n|\n---|\n###|\Z)", block, re.S)
    if m:
        d["防越级约束"] = m.group(1).strip().replace("\n", " ")
    # 规律总结/规律记忆法（> 引用行）
    m = re.search(r">\s*\*\*(规律总结|规律记忆法|语法总结|记忆规律)[^*]*\*\*[:：]\s*(.*?)(?:\n\s*\n|\Z)", block, re.S)
    if m:
        d["规律总结"] = clean_md(m.group(2))
    # 例句：编号列表
    ex = re.findall(r"^\s*(\d+)[\.、]\s*(.+)$", block, re.M)
    if ex:
        d["例句"] = [clean_md(t.strip()) for _, t in ex]
    # 表格示例列：仅取表头含「示例/例句」的表，且只收合法例句
    table_ex = []
    for rows in split_tables(block):
        header_cells = [c.strip() for c in rows[0].strip().strip("|").split("|")] if rows else []
        if not any(("示例" in c or "例句" in c) for c in header_cells):
            continue
        idx = next((i for i, c in enumerate(header_cells) if "示例" in c or "例句" in c), None)
        if idx is None:
            continue
        for row in rows[1:]:
            cells = [clean_md(c) for c in row.strip().strip("|").split("|")]
            if idx >= len(cells):
                continue
            for piece in re.split(r"\s*/\s*", cells[idx]):
                piece = piece.strip()
                if is_good_example(piece):
                    table_ex.append(piece)
    d["表例句"] = list(dict.fromkeys(table_ex))[:12]
    # 中考辨析：**中考辨析**：后的 - 列表
    mb = re.search(r"\*\*中考辨析\*\*[:：]\s*(.*?)(?:\n\s*\n|\n---|\n###|\n\*\*易错点|\Z)", block, re.S)
    if mb:
        bullets = re.findall(r"[-*]\s*(.+)", mb.group(1))
        d["中考考法"] = [b.strip() for b in bullets]
    # 易错点：**易错点**：后的 ❌→✅ 列表
    me = re.search(r"\*\*易错点\*\*[:：]\s*(.*?)(?:\n\s*\n|\n---|\n###|\Z)", block, re.S)
    if me:
        pairs = re.findall(r"[-*]\s*❌\s*(.+?)\s*→\s*✅\s*(.+)", me.group(1))
        d["易错5"] = [(w.strip(), r.strip()) for w, r in pairs]
    return d

def extract_lesson_grammar(lesson_no):
    path = os.path.join(BLUEPRINT_DIR, "第%02d课_内容蓝图.md" % lesson_no)
    if not os.path.exists(path):
        return []
    s = open(path, encoding="utf-8").read()
    i = s.find("## 二、语法详案")
    if i == -1:
        return []
    sec = s[i:]
    blocks = re.split(r"### 语法[①②③][：:]", sec)
    out = []
    for b in blocks[1:]:
        b = re.split(r"\n## ", b, maxsplit=1)[0]  # 截断到下一个顶级节（练习结构蓝图等）
        title = b.split("\n", 1)[0].strip()
        parsed = parse_grammar_block(b)
        parsed["标题"] = title
        out.append(parsed)
    return out


def seed_bank(lesson_map):
    """若 grammar_bank.json 不存在，从 lesson_map 重建占位条目"""
    bank = {}
    for L in range(1, 22):
        gnames = lesson_map.get(str(L), {}).get("grammar", [])
        stage = lesson_map.get(str(L), {}).get("stage", "")
        for g in gnames:
            bank[g] = {
                "构成": "%s 的基本构成规则（详见课件语法页）" % g,
                "例句6": ["例句%d：%s 的典型例句。" % (i, g) for i in range(1, 7)],
                "易错5": ["易错%d：%s 的高频易错。" % (i, g) for i in range(1, 6)],
                "口诀": "%s 记忆口诀（见课件语法页）" % g,
                "六色卡": {c: "%s 的%s要点" % (g, c) for c in ["用法","构成","易错","例句","注意","口诀"]},
                "中考考法": "%s 的中考考查方式" % g,
                "stage": stage,
                "lesson": int(L) if str(L).isdigit() else 0,
            }
    return bank


FORBIDDEN = ["will ", "be going to", "shall ", "better", "best", "worse", "worst",
             " more ", " most ", "have been", "has been", "is made", "are made"]

def _has_forbidden(text):
    return any(kw in text for kw in FORBIDDEN)

def scrub_entry(entry):
    """删除渲染字段中的越级表述（防 verify_v2 扫描；同时符合项目防越级红线）"""
    if isinstance(entry.get("例句6"), list):
        entry["例句6"] = [x for x in entry["例句6"] if not _has_forbidden(x)]
    if isinstance(entry.get("易错5"), list):
        entry["易错5"] = [x for x in entry["易错5"] if not _has_forbidden(x)]
    for field in ["构成", "口诀", "中考考法"]:
        v = entry.get(field, "")
        if isinstance(v, str) and _has_forbidden(v):
            parts = re.split(r"[；;。]", v)
            keep = [p for p in parts if p and not _has_forbidden(p)]
            entry[field] = "；".join(keep)
    six = entry.get("六色卡", {})
    for cat in list(six.keys()):
        v = six.get(cat, "")
        if isinstance(v, str) and _has_forbidden(v):
            parts = re.split(r"[；;。]", v)
            keep = [p for p in parts if p and not _has_forbidden(p)]
            six[cat] = "；".join(keep) or entry.get("口诀", "")
    return entry


def enrich(grammar_bank, lesson_map):
    n_filled = 0
    n_missing = 0
    missing_info = []
    for L in range(1, 21):
        gnames = lesson_map.get(str(L), {}).get("grammar", [])
        if not gnames:
            continue
        blocks = extract_lesson_grammar(L)
        for idx, gname in enumerate(gnames):
            if gname not in grammar_bank:
                continue
            entry = grammar_bank[gname]
            blk = blocks[idx] if idx < len(blocks) else {}
            if not blk or not blk.get("口诀"):
                n_missing += 1
                missing_info.append("L%d %s" % (L, gname))
                continue
            juzhen = blk.get("规律总结", blk.get("防越级约束", ""))
            usage = clean_md(juzhen) or blk.get("口诀", "")
            entry["构成"] = clean_md(juzhen) or "（蓝图未提供构成要点，见口诀与公式矩阵）"
            ex_all = (blk.get("例句") or []) + (blk.get("表例句") or [])
            ex_all = [x for x in ex_all if is_good_example(x)]
            entry["例句6"] = list(dict.fromkeys(ex_all))[:6]
            entry["易错5"] = [clean_md("%s → %s" % (w, r)) for w, r in (blk.get("易错5") or [])[:5]]
            entry["口诀"] = clean_md(blk.get("口诀", ""))
            six = {}
            six["用法"] = usage
            six["构成"] = clean_md(blk.get("防越级约束") or usage)
            six["易错"] = clean_md("%s → %s" % tuple(blk["易错5"][0])) if blk.get("易错5") else clean_md(entry["口诀"])
            six["例句"] = clean_md((blk.get("例句") or ["（蓝图未提供例句）"])[0])
            six["注意"] = clean_md((blk.get("中考考法") or [usage])[0])
            six["口诀"] = clean_md(blk.get("口诀", ""))
            entry["六色卡"] = six
            entry["中考考法"] = clean_md("；".join(blk.get("中考考法") or []))[:200] or "（蓝图未提供中考考法）"
            n_filled += 1
    return n_filled, n_missing, missing_info

if __name__ == "__main__":
    gb_path = os.path.join(HERE, "grammar_bank.json")
    lm_path = os.path.join(HERE, "lesson_map.json")
    lm = json.load(open(lm_path, encoding="utf-8"))["lessons"]
    if os.path.exists(gb_path):
        gb = json.load(open(gb_path, encoding="utf-8"))
    else:
        gb = seed_bank(lm)
        print("grammar_bank.json 不存在，已从 lesson_map 重建占位条目")
    n, miss, info = enrich(gb, lm)
    scrubbed = 0
    for k in gb:
        before = json.dumps(gb[k], ensure_ascii=False)
        gb[k] = scrub_entry(gb[k])
        if json.dumps(gb[k], ensure_ascii=False) != before:
            scrubbed += 1
    json.dump(gb, open(gb_path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("越级清洗 %d 个考点" % scrubbed)
    print("填实 %d 个考点，未填 %d 个" % (n, miss))
    for m in info:
        print("  未填:", m)
    # 验收：L5 三考点六字段齐全
    for k in ["祈使句基础", "What特殊疑问句", "like的用法"]:
        e = gb[k]
        ok = all(f in e for f in ["构成","例句6","易错5","口诀","六色卡","中考考法"]) and len(e["六色卡"]) == 6
        print("L5 验收", k, "OK" if ok else "FAIL", "例句数:", len(e["例句6"]), "易错数:", len(e["易错5"]))
