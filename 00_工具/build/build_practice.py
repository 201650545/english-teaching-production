#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""统一配套练习构建入口（P1-1 脚本收口）。

用法:
    python build_practice.py --content <assembled.json> --out <output.docx>

assembled.json 契约：{"card": {...}, "content": {...}}
——即 `build_practice_paper.build_practice(card, content, out_path)` 直接消费的
「已拼装」形态（reading_a/b/c、w5、cloze、grammar_fill、sa、writing、
grammar_diag 均已按引擎契约组装完毕）。

本入口内部只做两件事：加载内容 JSON + 调用既有引擎，不复制任何业务逻辑。
旧课时专属的一次性脚本（含各自的读JSON/转换/拼装逻辑）已归档到
`00_工具/archive_scripts/`；新课时只需产出已拼装的内容 JSON 并调用本入口。
"""
import argparse
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL_DIR = os.path.join(os.path.dirname(HERE), "engine")  # 00_工具/engine（引擎所在）


def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(TOOL_DIR, fname))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser(description="统一配套练习构建入口")
    ap.add_argument("--content", required=True, help="已拼装 JSON（card + content 两键）")
    ap.add_argument("--out", required=True, help="输出 .docx 路径")
    ap.add_argument("--student", help="可选：学生代号（与 card 校验，以 card 为准）")
    ap.add_argument("--lesson", type=int, help="可选：课时号（与 card 校验，以 card 为准）")
    args = ap.parse_args()

    with open(args.content, encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict) or "card" not in data or "content" not in data:
        sys.exit(f"[错误] {args.content} 必须是 {{card, content}} 两键的已拼装 JSON")

    card, content = data["card"], data["content"]
    if args.student and card.get("student") != args.student:
        print(f"[提示] --student {args.student} ≠ card.student={card.get('student')}，以 card 为准")
    if args.lesson and card.get("lesson") != args.lesson:
        print(f"[提示] --lesson {args.lesson} ≠ card.lesson={card.get('lesson')}，以 card 为准")

    bp = _load("bp", "build_practice_paper.py")
    out = bp.build_practice(card, content, args.out)
    print(f"配套练习生成：{out} ({os.path.getsize(out)} bytes)")


if __name__ == "__main__":
    main()
