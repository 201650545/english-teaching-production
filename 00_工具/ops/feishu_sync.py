#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语教学流水线 → 飞书多维表格 状态看板同步脚本
==================================================
数据流向：本地（D:\\英语教学）→ 飞书「英语教学流水线」Base →「课程进度看板」表
原则：本地 = 规范真源；飞书 = 状态镜像。单向同步，飞书不改数据。

独占写入声明（P2-3）：本脚本为「英语教学流水线」Base →「课程进度看板」表
（tblDQL47cLPeDkqg）的**唯一写入方**。AI Hub 中央平台 feishu_sync.py 写的是
另一张飞书 Base（AI Hub 网关数据 4 表），与本脚本无交集，双写分工见
`TOPOLOGY.md`。

用法：
    python feishu_sync.py init    # 全量新建记录（首跑，表应为空）
    python feishu_sync.py sync    # 增量同步（按「课时编号」匹配更新，缺则新建）
    python feishu_sync.py --dry   # 只打印将写入的记录，不调飞书

注意：lark-cli 为 .ps1 包装器，PowerShell 传 JSON 参数会剥引号导致
invalid_fields_json。本脚本一律 subprocess 直调 node run.js（参数数组）。
"""

import json
import os
import re
import subprocess
import sys

# ---------- 常量 ----------
BASE = r"D:\英语教学"
BASE_TOKEN = "LIg7bTJN4aVPVOsgW7ncnFJOn3c"
TABLE_ID = "tblDQL47cLPeDkqg"          # 课程进度看板
REPORT_DIR = os.path.join(BASE, "00_总规划", "05_交付与审核记录")
TOOL_DIR = os.path.join(BASE, "00_工具")

NODE = r"D:\Program Files\nodejs\node.exe"
RUNJS = os.path.expandvars(r"%APPDATA%\npm\node_modules\@larksuite\cli\scripts\run.js")

STUDENTS = ["邓兴华", "许颖嘉", "李民宪"]

# ---------- lark-cli 调用封装 ----------

def lark(args, timeout=120):
    """直调 node run.js，参数数组传参，返回解析后的 JSON dict。"""
    cmd = [NODE, RUNJS] + args
    r = subprocess.run(cmd, capture_output=True, text=True,
                       encoding="utf-8", errors="replace", timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"lark-cli 失败 rc={r.returncode}\nSTDERR: {r.stderr[:800]}")
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        raise RuntimeError(f"lark-cli 输出非 JSON:\n{r.stdout[:800]}")

def list_existing_keys():
    """拉取当前表已存在的课时编号集合。

    注意：+record-list 返回 data.data 为「二维数组」，每行是字段值数组
    （按 data.fields 字段名顺序），不直接含 record_id。故本函数仅用于
    「课时编号是否已存在」去重判断；record_id 用 search 逐条精确查。
    """
    data = lark(["base", "+record-list", "--base-token", BASE_TOKEN,
                 "--table-id", TABLE_ID, "--format", "json"])
    rows = data.get("data", {}).get("data") or []
    keys = set()
    for row in rows:
        if row and row[0]:
            keys.add(row[0])
    return keys

def find_record_id(key):
    """按 课时编号==key 精确查 record_id；不存在返回 None。"""
    filt = {"logic": "and", "conditions": [["课时编号", "==", key]]}
    data = lark(["base", "+record-search",
                 "--base-token", BASE_TOKEN, "--table-id", TABLE_ID,
                 "--keyword", key, "--search-field", "课时编号",
                 "--filter-json", json.dumps(filt, ensure_ascii=False),
                 "--format", "json", "--limit", "1"])
    ids = (data.get("data", {}) or {}).get("record_id_list") or []
    return ids[0] if ids else None

def upsert_record(record, key):
    """写入/更新一条记录：课时编号已存在则更新，否则新建。"""
    rec_id = find_record_id(key)
    args = ["base", "+record-upsert", "--base-token", BASE_TOKEN,
            "--table-id", TABLE_ID, "--json", json.dumps(record, ensure_ascii=False),
            "--format", "json"]
    if rec_id:
        args += ["--record-id", rec_id]
    out = lark(args)
    ok = out.get("ok")
    if not ok:
        raise RuntimeError(f"upsert 失败: {json.dumps(out, ensure_ascii=False)[:500]}")
    return rec_id is not None

# ---------- 本地扫描 ----------

def scan_lesson_dir(student, lesson_no):
    """扫描单个课目录，判定四件套存在性与课型。返回字段 dict。"""
    lesson_dir = os.path.join(BASE, student, f"第{lesson_no:02d}课时")
    key = f"{student}-L{lesson_no:02d}"

    # 蓝图：内容蓝图/单课/第XX课_内容蓝图.md
    blueprint = os.path.exists(os.path.join(
        BASE, student, "内容蓝图", "单课", f"第{lesson_no:02d}课_内容蓝图.md"))
    # 兼容未补零：第6课_内容蓝图.md
    if not blueprint:
        blueprint = os.path.exists(os.path.join(
            BASE, student, "内容蓝图", "单课", f"第{lesson_no}课_内容蓝图.md"))

    # 契约：契约/ 下 1_..6_.. 六件
    contract_dir = os.path.join(lesson_dir, "契约")
    contract = False
    if os.path.isdir(contract_dir):
        files = os.listdir(contract_dir)
        contract = all(any(f.startswith(f"{i}_") for f in files) for i in range(1, 7))

    # 课件：课件成品_网页PPT/*.html（排除 _旧件 目录与备份）
    cw_dir = os.path.join(lesson_dir, "课件成品_网页PPT")
    courseware = False
    if os.path.isdir(cw_dir):
        for f in os.listdir(cw_dir):
            fp = os.path.join(cw_dir, f)
            if os.path.isfile(fp) and f.endswith(".html") and "_旧件" not in f:
                courseware = True
                break
    # 兼容课件直接放课目录（许颖嘉 L05）
    if not courseware and os.path.isdir(lesson_dir):
        for f in os.listdir(lesson_dir):
            fp = os.path.join(lesson_dir, f)
            if os.path.isfile(fp) and f.endswith(".html") and not f.endswith(".bak"):
                courseware = True
                break

    # 练习：课目录下 第XX课时_配套练习_*.docx
    practice = False
    if os.path.isdir(lesson_dir):
        for f in os.listdir(lesson_dir):
            if f.endswith(".docx") and "配套练习" in f:
                practice = True
                break

    # 课名/语法点/课型：解析契约概要
    name, grammar, course_type = extract_from_contract(student, lesson_no, lesson_dir)

    return {
        "课时编号": key,
        "学生": student,
        "课时": lesson_no,
        "课名/语法点": name,
        "课型": course_type,
        "蓝图": blueprint,
        "课件": courseware,
        "练习": practice,
        "契约": contract,
        "状态": derive_status(blueprint, courseware, practice, contract),
        "汇报文件": match_report(student, lesson_no),
        "复核结论": "待复核",
        "已知偏差": "",
    }

def extract_from_contract(student, lesson_no, lesson_dir):
    """从契约 1_课程概要.md 提取 课名/语法点/课型。各线格式不同，柔性解析。"""
    cfile = os.path.join(lesson_dir, "契约", "1_课程概要.md")
    name = f"L{lesson_no:02d}"
    grammar = ""
    course_type = "授课课"
    if not os.path.isfile(cfile):
        return name, grammar, course_type
    try:
        text = open(cfile, encoding="utf-8").read(4000)
    except (OSError, UnicodeDecodeError):
        return name, grammar, course_type

    # 课名
    m = re.search(r"\*\*课名\*\*[：:]\s*(.+)", text)          # 邓兴华
    if not m:
        m = re.search(r"\*\*课题\*\*[：:]\s*(.+)", text)      # 李民宪
    if not m:
        m = re.search(r"\*\*主题\*\*[：:]\s*(.+)", text)      # 许颖嘉
    if m:
        name = f"L{lesson_no:02d} {m.group(1).strip()[:60]}"

    # 语法点（许颖嘉）
    mg = re.search(r"\*\*语法\*\*[：:]\s*(.+)", text)
    if mg:
        grammar = mg.group(1).strip()[:80]

    # 课型
    mt = re.search(r"\*\*课型\*\*[：:]\s*(.+)", text)
    if mt:
        t = mt.group(1)
        if "讲评" in t or "测试" in t:
            course_type = "测试课" if "测试" in t and "讲评" not in t else "讲评课"
        elif "授课" in t:
            course_type = "授课课"

    if grammar:
        name = f"{name}｜{grammar}"
    return name, grammar, course_type

def derive_status(bp, cw, pr, ct):
    """四件套齐全 → 已交付；缺项 → 缺练习/缺契约 等。"""
    if bp and cw and pr and ct:
        return "已交付"
    missing = []
    if not bp:
        missing.append("蓝图")
    if not cw:
        missing.append("课件")
    if not pr:
        missing.append("练习")
    if not ct:
        missing.append("契约")
    return "缺" + "/".join(missing)

def match_report(student, lesson_no):
    """从 05_交付与审核记录 文件名匹配该课归属的汇报文件。"""
    if not os.path.isdir(REPORT_DIR):
        return ""
    lesson_roman = f"L{lesson_no:02d}"
    best = ""
    for f in os.listdir(REPORT_DIR):
        if student not in f:
            continue
        # 提取文件名里的 Lxx-Lxx 或 Lxx 范围（第二个数字前无 L）
        ranges = re.findall(r"L(\d{2})-(\d{2})", f)
        singles = re.findall(r"L(\d{2})", f)
        covered = False
        for a, b in ranges:
            if int(a) <= lesson_no <= int(b):
                covered = True
                break
        if not covered:
            for s in singles:
                if int(s) == lesson_no:
                    covered = True
                    break
        if covered:
            best = f  # 取最后一个匹配（最新汇报）
    return best if best else ""

# ---------- 主流程 ----------

def build_all_records():
    records = []
    for student in STUDENTS:
        sdir = os.path.join(BASE, student)
        if not os.path.isdir(sdir):
            continue
        for d in sorted(os.listdir(sdir)):
            m = re.fullmatch(r"第(\d{2})课时", d)
            if not m:
                continue
            rec = scan_lesson_dir(student, int(m.group(1)))
            if rec:
                records.append(rec)
    return records

def main():
    dry = "--dry" in sys.argv
    mode = "init" if "init" in sys.argv else "sync"

    records = build_all_records()
    print(f"扫描到 {len(records)} 个课时记录")

    if mode == "sync":
        existing = list_existing_keys()
        print(f"飞书现有 {len(existing)} 条记录")

    if dry:
        for rec in records:
            print(json.dumps(rec, ensure_ascii=False))
        return

    created = updated = 0
    for rec in records:
        try:
            is_update = upsert_record(rec, rec["课时编号"])
            if is_update:
                updated += 1
                print(f"  更新 {rec['课时编号']}")
            else:
                created += 1
                print(f"  新建 {rec['课时编号']}")
        except RuntimeError as e:
            print(f"  失败 {rec['课时编号']}: {e}")

    print(f"\n完成：新建 {created}，更新 {updated}，总计 {len(records)}")

if __name__ == "__main__":
    main()
