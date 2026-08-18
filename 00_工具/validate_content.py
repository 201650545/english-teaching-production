#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""内容 JSON 有效性校验（P3-1 CI 用）。

对 01_数据/content/ 下每个 *.json 做结构性校验：
  1) 必须是合法 JSON（解析成功）；
  2) 顶层必须是非空 dict（内容节键控对象）。

不校验具体业务语义（各文件节键异构：reading_a/b/c、w5、cloze、grammar_*、
content_plan、nl_map 等），只拦「坏 JSON / 空对象」这一类数据完整性问题。
命中任一违规即 exit 1。

用法：python validate_content.py            # 校验全部
      python validate_content.py <文件名>   # 校验单个
"""
import io
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 英语教学
CONTENT_DIR = os.path.join(BASE, "01_数据", "content")


def validate(fname):
    path = os.path.join(CONTENT_DIR, fname)
    try:
        data = json.load(io.open(path, encoding="utf-8"))
    except json.JSONDecodeError as e:
        return [f"{fname}: JSON 解析失败（line {e.lineno} col {e.colno}: {e.msg}）"]
    except UnicodeDecodeError as e:
        return [f"{fname}: 编码错误（{e}）"]
    if not isinstance(data, dict):
        return [f"{fname}: 顶层必须是对象（实际 {type(data).__name__}）"]
    if not data:
        return [f"{fname}: 空对象"]
    return []


def main():
    names = sys.argv[1:] or sorted(
        n for n in os.listdir(CONTENT_DIR) if n.endswith(".json"))
    total_err = 0
    for name in names:
        errors = validate(name)
        if errors:
            total_err += len(errors)
            for e in errors:
                print(f"[失败] {e}")
        else:
            print(f"[通过] {name}")
    print(f"\n校验完成：{'全部通过 ✔' if total_err == 0 else f'{total_err} 处违规 ✘'}")
    sys.exit(0 if total_err == 0 else 1)


if __name__ == "__main__":
    main()
