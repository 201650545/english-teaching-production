#!/usr/bin/env python3
"""Safely merge validated w5 records into passage_bank.json.

Default mode is dry-run. Use --apply to write.
Supported target shapes:
1) JSON root list
2) JSON object with a list field named "passages"

Unknown shapes abort without changing the target.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import sys
import tempfile
from typing import Any


EXPECTED_IDS = {"HN2026_L1_w5", "HN2026_L6_w5", "HN2026_L8_w5"}
EXPECTED_BLANKS = ["11", "12", "13", "14"]


class ValidationError(ValueError):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> Any:
    if not path.is_file():
        raise ValidationError(f"文件不存在：{path}")
    if path.stat().st_size > 100 * 1024 * 1024:
        raise ValidationError(f"拒绝解析超过100MB的JSON：{path}")
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except UnicodeDecodeError as exc:
        raise ValidationError(f"不是UTF-8/UTF-8-SIG：{path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValidationError(f"JSON格式错误：{path}: {exc}") from exc


def validate_record(rec: Any) -> None:
    if not isinstance(rec, dict):
        raise ValidationError("每条记录必须是对象")
    required = {
        "id", "passage_with_blanks", "options", "answers",
        "extra", "rationale", "note"
    }
    missing = required - rec.keys()
    if missing:
        raise ValidationError(f"{rec.get('id', '?')}: 缺少字段 {sorted(missing)}")

    rid = rec["id"]
    if not isinstance(rid, str) or not rid.strip():
        raise ValidationError("id必须是非空字符串")

    passage = rec["passage_with_blanks"]
    if not isinstance(passage, str):
        raise ValidationError(f"{rid}: passage_with_blanks必须是字符串")
    blanks = re.findall(r"__\((\d+)\)__", passage)
    if blanks != EXPECTED_BLANKS:
        raise ValidationError(f"{rid}: 空位必须依次为11—14，实际{blanks}")
    if "__(15)__" in passage:
        raise ValidationError(f"{rid}: 禁止保留空15")

    options = rec["options"]
    if not isinstance(options, list) or len(options) != 5:
        raise ValidationError(f"{rid}: options必须恰好5项")
    if any(not isinstance(x, list) or len(x) != 2 for x in options):
        raise ValidationError(f"{rid}: 每个option必须是[字母, 文本]")
    letters = [x[0] for x in options]
    texts = [x[1] for x in options]
    if letters != list("ABCDE"):
        raise ValidationError(f"{rid}: 选项字母必须按A—E")
    if len(set(texts)) != 5:
        raise ValidationError(f"{rid}: 选项文本重复")
    if any(not isinstance(t, str) or not t.strip() for t in texts):
        raise ValidationError(f"{rid}: 选项文本不能为空")

    answers = rec["answers"]
    if not isinstance(answers, dict) or list(answers.keys()) != EXPECTED_BLANKS:
        raise ValidationError(f"{rid}: answers键必须按11—14")
    answer_letters = list(answers.values())
    if len(set(answer_letters)) != 4:
        raise ValidationError(f"{rid}: 4个正确选项必须互不重复")
    if not set(answer_letters).issubset(set(letters)):
        raise ValidationError(f"{rid}: 答案包含不存在的选项")

    extra = rec["extra"]
    if extra not in letters:
        raise ValidationError(f"{rid}: extra不在A—E")
    if extra in answer_letters:
        raise ValidationError(f"{rid}: extra不能成为答案")

    rationale = rec["rationale"]
    if not isinstance(rationale, dict) or set(rationale.keys()) != set(EXPECTED_BLANKS):
        raise ValidationError(f"{rid}: rationale必须完整覆盖11—14")

    inserted = passage
    option_map = dict(options)
    for blank, letter in answers.items():
        inserted = inserted.replace(f"__({blank})__", option_map[letter], 1)
    if re.search(r"__\(\d+\)__", inserted):
        raise ValidationError(f"{rid}: 插入答案后仍有占位符")


def validate_source(records: Any) -> list[dict[str, Any]]:
    if not isinstance(records, list):
        raise ValidationError("源JSON根节点必须是数组")
    for rec in records:
        validate_record(rec)
    ids = [rec["id"] for rec in records]
    if len(ids) != len(set(ids)):
        raise ValidationError("源JSON存在重复ID")
    if set(ids) != EXPECTED_IDS:
        raise ValidationError(f"源ID集合不符：{ids}")
    return records


def get_target_list(target: Any) -> tuple[list[Any], str]:
    if isinstance(target, list):
        return target, "root-list"
    if isinstance(target, dict) and isinstance(target.get("passages"), list):
        return target["passages"], "object.passages"
    raise ValidationError(
        "未知passage_bank根结构。仅支持根数组，或包含数组字段passages的对象；"
        "为避免破坏文件，脚本已中止。"
    )


def merge_records(
    target_items: list[Any],
    source_items: list[dict[str, Any]],
    duplicate_policy: str,
) -> tuple[list[Any], dict[str, int]]:
    result = list(target_items)
    positions: dict[str, int] = {}
    for i, item in enumerate(result):
        if isinstance(item, dict) and isinstance(item.get("id"), str):
            rid = item["id"]
            if rid in positions:
                raise ValidationError(f"目标库本身存在重复ID：{rid}")
            positions[rid] = i

    added = replaced = skipped = 0
    for item in source_items:
        rid = item["id"]
        if rid not in positions:
            positions[rid] = len(result)
            result.append(item)
            added += 1
            continue
        if duplicate_policy == "abort":
            raise ValidationError(
                f"目标已存在ID {rid}。默认策略为abort，未写入。"
                "可人工核对后使用--on-duplicate skip或replace。"
            )
        if duplicate_policy == "skip":
            skipped += 1
            continue
        if duplicate_policy == "replace":
            result[positions[rid]] = item
            replaced += 1
            continue
        raise AssertionError(duplicate_policy)

    return result, {"added": added, "replaced": replaced, "skipped": skipped}


def atomic_write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
        text=True,
    )
    temp_path = Path(temp_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)
            f.write("\n")
            f.flush()
            os.fsync(f.fileno())
        # Re-parse the completed temp file before replacement.
        load_json(temp_path)
        os.replace(temp_path, path)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--target", required=True, type=Path)
    parser.add_argument(
        "--on-duplicate",
        choices=("abort", "skip", "replace"),
        default="abort",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="实际写入；未指定时只做演练。",
    )
    args = parser.parse_args()

    try:
        source = validate_source(load_json(args.source))
        target = load_json(args.target)
        target_items, shape = get_target_list(target)
        merged_items, stats = merge_records(
            target_items, source, args.on_duplicate
        )

        if shape == "root-list":
            merged_target: Any = merged_items
        else:
            merged_target = dict(target)
            merged_target["passages"] = merged_items

        before_hash = sha256(args.target)
        print(f"目标结构：{shape}")
        print(f"目标SHA-256（写入前）：{before_hash}")
        print(f"计划结果：{stats}")
        print(f"合并后条数：{len(merged_items)}")

        if not args.apply:
            print("DRY RUN通过：未修改任何文件。")
            print("确认无误后追加 --apply 执行。")
            return 0

        stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup = args.target.with_name(f"{args.target.name}.bak_{stamp}")
        shutil.copy2(args.target, backup)
        if sha256(backup) != before_hash:
            raise ValidationError("备份哈希与原文件不一致，已中止")

        atomic_write_json(args.target, merged_target)
        after = load_json(args.target)
        after_items, _ = get_target_list(after)
        after_ids = {
            x.get("id") for x in after_items
            if isinstance(x, dict) and isinstance(x.get("id"), str)
        }
        missing = EXPECTED_IDS - after_ids
        if missing:
            raise ValidationError(
                f"写入后缺少目标ID：{sorted(missing)}；请从备份恢复"
            )

        print(f"备份文件：{backup}")
        print(f"目标SHA-256（写入后）：{sha256(args.target)}")
        print("APPLY完成：JSON已重新解析，三个目标ID均存在。")
        return 0

    except ValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"OS ERROR: {exc}", file=sys.stderr)
        return 3


if __name__ == "__main__":
    raise SystemExit(main())
