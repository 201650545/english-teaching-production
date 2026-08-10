#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""题库 JSON Schema 校验（P1-2）。

对 01_数据/banks/ 下每个题库 JSON 按 01_数据/schemas/ 对应 Schema 校验
「必填字段 + 类型」，不依赖第三方库。命中任一违规即 exit 1。

用法：python validate_banks.py            # 校验全部
      python validate_banks.py vocab_bank # 校验单个
"""
import io
import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 英语教学
BANKS = os.path.join(BASE, "01_数据", "banks")
SCHEMAS = os.path.join(BASE, "01_数据", "schemas")

BANK_TO_SCHEMA = {
    "base_vocab.json": "base_vocab.schema.json",
    "grammar_bank.json": "grammar_bank.schema.json",
    "passage_bank.json": "passage_bank.schema.json",
    "passage_bank_supplement.json": "passage_bank_supplement.schema.json",
    "passage_questions.json": "passage_questions.schema.json",
    "phonics_bank.json": "phonics_bank.schema.json",
    "vocab_bank.json": "vocab_bank.schema.json",
}

_TYPE_OK = {"string": str, "number": (int, float), "integer": int, "boolean": bool,
            "array": list, "object": dict, "null": type(None)}


def check_type(val, type_spec, path):
    """校验一个值的类型；type_spec 可为 str / list(联合) / None(任意)。"""
    if type_spec is None or val is None:
        return []
    specs = type_spec if isinstance(type_spec, list) else [type_spec]
    for t in specs:
        if t in _TYPE_OK and isinstance(val, _TYPE_OK[t]):
            return []
    return [f"{path}: 类型不符（期望 {type_spec}，实际 {type(val).__name__}）"]


def check_obj(obj, schema, path):
    """校验 object：required 字段存在 + 属性类型。"""
    errors = []
    for req in schema.get("required", []):
        if req not in obj:
            errors.append(f"{path}: 缺必填字段「{req}」")
    props = schema.get("properties", {})
    for k, prop in props.items():
        if k in obj and isinstance(prop, dict):
            errors += check_type(obj[k], prop.get("type"), f"{path}.{k}")
    return errors


def validate(bank_name):
    bank_path = os.path.join(BANKS, bank_name)
    schema_file = BANK_TO_SCHEMA.get(bank_name)
    if not schema_file or not os.path.isfile(schema_path := os.path.join(SCHEMAS, schema_file)):
        return [f"{bank_name}: 无对应 Schema（{schema_file}）"], 0

    data = json.load(io.open(bank_path, encoding="utf-8"))
    schema = json.load(io.open(schema_path, encoding="utf-8"))
    errors = []
    n = 0

    # 顶层 object 必填/类型
    if schema.get("type") == "object":
        errors += check_obj(data, schema, bank_name)
        # 键控库：逐条目校验 additionalProperties 的 required/type
        ap = schema.get("additionalProperties", {})
        if ap and isinstance(data, dict):
            for key, val in data.items():
                n += 1
                errors += check_obj(val, ap, f"{bank_name}.{key}")
        # 列表字段（words 等）：逐元素校验 items
        for k, prop in schema.get("properties", {}).items():
            if isinstance(prop, dict) and prop.get("items") and isinstance(data.get(k), list):
                for i, it in enumerate(data[k]):
                    n += 1
                    errors += check_obj(it, prop["items"], f"{bank_name}.{k}[{i}]")
    elif schema.get("type") == "array":
        for i, it in enumerate(data):
            n += 1
            errors += check_obj(it, schema.get("items", {}), f"{bank_name}[{i}]")

    return errors, n


def main():
    names = sys.argv[1:] or list(BANK_TO_SCHEMA)
    total_err = 0
    for name in names:
        errors, n = validate(name)
        if errors:
            total_err += len(errors)
            print(f"[失败] {name}（{n} 条目，{len(errors)} 违规）")
            for e in errors[:8]:
                print(f"   - {e}")
        else:
            print(f"[通过] {name}（{n} 条目）")
    print(f"\n校验完成：{'全部通过 ✔' if total_err == 0 else f'{total_err} 处违规 ✘'}")
    sys.exit(0 if total_err == 0 else 1)


if __name__ == "__main__":
    main()
