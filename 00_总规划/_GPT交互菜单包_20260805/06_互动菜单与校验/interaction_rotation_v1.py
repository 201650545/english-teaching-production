#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json
from collections import Counter
from pathlib import Path

MIN_ACTIONS = {"foundation": 3, "medium": 4, "advanced": 5}

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def stable_number(*parts: str) -> int:
    value = "|".join(parts).encode("utf-8")
    return int(hashlib.sha256(value).hexdigest()[:16], 16)

def recent_ids(history, knowledge_id, lesson_index, window=2):
    return {
        row.get("template_id")
        for row in history
        if row.get("knowledge_id") == knowledge_id
        and isinstance(row.get("lesson_index"), int)
        and 0 < lesson_index - row["lesson_index"] <= window
    }

def assign(menu, payload):
    action_counts = Counter()
    previous = []
    history = payload.get("history", [])
    result = []

    for item in payload["items"]:
        candidates = [
            t for t in menu["templates"]
            if t["section"] == item["section"]
            and item["content_type"] in t["content_types"]
        ]
        if not candidates:
            raise ValueError(f"无候选模板：{item}")

        recent = recent_ids(
            history, item["knowledge_id"], payload["lesson_index"]
        )
        preferred = [t for t in candidates if t["template_id"] not in recent]
        relaxed = not preferred
        pool = preferred or candidates

        scored = []
        for t in pool:
            action = t["primary_action"]
            penalty = action_counts[action] * 3
            if previous and previous[-1] == action:
                penalty += 4
            if len(previous) >= 2 and previous[-2:] == [action, action]:
                penalty += 100
            if t["template_id"] in recent:
                penalty += 5
            tie = stable_number(
                "interaction-v1", payload["level"], payload["lesson_id"],
                item["knowledge_id"], item["section"], item["slot_id"],
                t["template_id"]
            )
            scored.append((penalty, tie, t))

        scored.sort(key=lambda row: (row[0], row[1]))
        chosen = scored[0][2]
        action = chosen["primary_action"]
        action_counts[action] += 1
        previous.append(action)
        result.append({
            "slot_id": item["slot_id"],
            "knowledge_id": item["knowledge_id"],
            "template_id": chosen["template_id"],
            "action_type": action,
            "rotation_relaxed": relaxed
        })

    return {
        "version": "1.0",
        "lesson_id": payload["lesson_id"],
        "level": payload["level"],
        "action_counts": dict(action_counts),
        "unique_actions": sorted(action_counts),
        "meets_level_action_target":
            len(action_counts) >= MIN_ACTIONS[payload["level"]],
        "assignments": result
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--menu", type=Path, required=True)
    parser.add_argument("--request", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = assign(load(args.menu), load(args.request))
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
