#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, re
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from html.parser import HTMLParser
from pathlib import Path

CHOICE = {"single_choice","multiple_choice","true_false","choice"}
HOT = {"grammar","vocab","drill","extend","diagnosis"}
LEVELS = {
    "foundation": (.55,.45,.60,3),
    "medium": (.45,.35,.50,4),
    "advanced": (.30,.25,.35,5),
}

@dataclass
class Finding:
    code: str
    severity: str
    message: str
    evidence: dict | None = None

class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items = []
        self.contract = False
        self.buttons = 0

    def handle_comment(self, data):
        if "CW-INTERACTION-CONTRACT:1" in data:
            self.contract = True

    def handle_starttag(self, tag, attrs):
        a = {k:(v or "") for k,v in attrs}
        classes = set(a.get("class","").split())
        if "quiz-opt" in classes:
            self.buttons += 1
        if (
            a.get("data-interaction-item") == "1"
            or a.get("data-question-id")
        ):
            self.items.append({
                "question_id": a.get("data-question-id",""),
                "knowledge_id": a.get("data-knowledge-id",""),
                "section": a.get("data-section","unknown").lower(),
                "template_id": a.get("data-template-id",""),
                "interaction_type": a.get("data-interaction-type","unknown").lower(),
                "action_type": a.get("data-action-type","unknown").lower(),
                "cognitive_level": a.get("data-cognitive-level","unknown").lower(),
                "scorable": a.get("data-scorable","true").lower() != "false",
            })

def inspect(html, level="medium", force=False):
    choice_max, hot_max, recognition_max, min_actions = LEVELS[level]
    p = Parser()
    p.feed(html)
    items = [x for x in p.items if x["scorable"]]
    findings = []
    sev = lambda hard=True: "ERROR" if (force or p.contract) and hard else "WARN"

    required = [
        "question_id","knowledge_id","section","template_id",
        "interaction_type","action_type","cognitive_level"
    ]
    for row in items:
        missing = [
            key for key in required
            if not row.get(key) or row[key] == "unknown"
        ]
        if missing:
            findings.append(Finding(
                "VIS-610", sev(), f"缺少互动元数据：{missing}"
            ))

    # ── VIS-613：交互类型-DOM 匹配（反作弊） ──
    # 对每个 data-interaction-item 容器，检查其真实 DOM 是否匹配标签
    dom_mismatches = []
    real_choice_count = 0
    real_nonchoice_count = 0
    for row in items:
        qid = row.get("question_id", "")
        if not qid:
            continue
        itype = row.get("interaction_type", "unknown")
        # 找到该容器在 HTML 中的位置
        # 用 data-question-id 定位
        pattern = r'data-question-id="' + re.escape(qid) + r'"[^>]*>.*?(?=data-question-id="[^"]*"|</div>\s*(?:<div class="page|</div>\s*<div class="modal|$))'
        m = re.search(pattern, html, re.S)
        if not m:
            # 尝试更宽松的匹配
            pattern2 = r'data-question-id="' + re.escape(qid) + r'"[^>]*>.*?(?=</div>\s*</div>\s*</div>)'
            m2 = re.search(pattern2, html, re.S)
            if m2:
                snippet = m2.group(0)
            else:
                continue
        else:
            snippet = m.group(0)

        # 检查容器内是否有 quiz-opt → 该容器按 choice 计
        has_quiz_opt = 'class="quiz-opt"' in snippet or 'quiz-opt' in snippet
        if has_quiz_opt:
            real_choice_count += 1
        else:
            real_nonchoice_count += 1

        if itype in CHOICE:
            # choice 类型：允许 quiz-opt
            if not has_quiz_opt:
                # 检查是否有其他允许的交互
                pass  # 选择型容器无 quiz-opt 不报错（可能用了其他交互）
        elif itype in ("fill_in", "write"):
            # 必须含 input/textarea/contenteditable
            has_input = 'input' in snippet or 'textarea' in snippet or 'contenteditable' in snippet
            if not has_input:
                dom_mismatches.append((qid, itype, "缺少 input/textarea/contenteditable"))
        elif itype == "order":
            # 必须含可排序元素
            has_order = 'order-chunk' in snippet or 'order-item' in snippet or 'draggable' in snippet
            if not has_order:
                dom_mismatches.append((qid, itype, "缺少可排序元素"))
        elif itype == "drag_and_drop":
            has_drag = 'drag-word' in snippet or 'draggable' in snippet or 'drag-slot' in snippet
            if not has_drag:
                dom_mismatches.append((qid, itype, "缺少拖拽元素"))
        elif itype == "link":
            has_link = 'link-item' in snippet or 'ec-q' in snippet or 'ec-ev' in snippet or 'match-item' in snippet
            if not has_link:
                dom_mismatches.append((qid, itype, "缺少连线/配对元素"))

    for qid, itype, detail in dom_mismatches:
        findings.append(Finding(
            "VIS-613", "ERROR",
            f"交互类型-DOM 不匹配：{qid} 标签={itype}，{detail}"
        ))

    # ── 两口径占比 ──
    # 口径1：按标签算（原有逻辑）
    total = len(items)
    choices = [x for x in items if x["interaction_type"] in CHOICE]
    hot = [x for x in items if x["section"] in HOT]
    hot_choices = [x for x in hot if x["interaction_type"] in CHOICE]
    recognition = [x for x in items if x["cognitive_level"] == "recognition"]
    actions = {x["action_type"] for x in items if x["action_type"] != "unknown"}

    if total and len(choices)/total > choice_max:
        findings.append(Finding(
            "VIS-601", sev(),
            f"全课选择题占比（标签口径）{len(choices)/total:.1%}，超过{choice_max:.0%}"
        ))
    if hot and len(hot_choices)/len(hot) > hot_max:
        findings.append(Finding(
            "VIS-602", sev(),
            f"热区选择题占比（标签口径）{len(hot_choices)/len(hot):.1%}，超过{hot_max:.0%}"
        ))
    if total and len(actions) < min_actions:
        findings.append(Finding(
            "VIS-603", sev(),
            f"全课只有{len(actions)}种动作，要求至少{min_actions}种"
        ))
    if total and len(recognition)/total > recognition_max:
        findings.append(Finding(
            "VIS-606", sev(),
            f"纯识别占比（标签口径）{len(recognition)/total:.1%}，超过{recognition_max:.0%}"
        ))

    # 口径2：按 DOM 真实计数算（反作弊）
    real_total = real_choice_count + real_nonchoice_count
    if real_total:
        real_choice_ratio = real_choice_count / real_total
        if real_choice_ratio > choice_max:
            findings.append(Finding(
                "VIS-601-DOM", sev(),
                f"全课选择题占比（DOM口径）{real_choice_ratio:.1%} ({real_choice_count}/{real_total})，超过{choice_max:.0%}"
            ))
        # 热区 DOM 占比
        hot_items_dom = [x for x in items if x["section"] in HOT]
        hot_choice_dom = 0
        hot_total_dom = 0
        for row in hot_items_dom:
            qid = row.get("question_id", "")
            if not qid:
                continue
            pattern = r'data-question-id="' + re.escape(qid) + r'"[^>]*>'
            m = re.search(pattern, html, re.S)
            if not m:
                continue
            # 用 qid 找 snippet
            snippet = html[html.find(m.group(0)):html.find(m.group(0)) + 500]
            has_qo = 'class="quiz-opt"' in snippet or 'quiz-opt' in snippet
            if has_qo:
                hot_choice_dom += 1
            hot_total_dom += 1
        if hot_total_dom:
            hot_dom_ratio = hot_choice_dom / hot_total_dom
            if hot_dom_ratio > hot_max:
                findings.append(Finding(
                    "VIS-602-DOM", sev(),
                    f"热区选择题占比（DOM口径）{hot_dom_ratio:.1%} ({hot_choice_dom}/{hot_total_dom})，超过{hot_max:.0%}"
                ))

    by_section = defaultdict(list)
    by_knowledge = defaultdict(list)
    for row in items:
        by_section[row["section"]].append(row)
        by_knowledge[row["knowledge_id"]].append(row)

    for section, rows in by_section.items():
        if section in HOT and len(rows) >= 4:
            section_actions = {x["action_type"] for x in rows}
            if len(section_actions) < 2:
                findings.append(Finding(
                    "VIS-604", sev(),
                    f"{section}环节动作种类少于2"
                ))

    for kid, rows in by_knowledge.items():
        if kid and not any(
            x["cognitive_level"] in {"retrieval","application"}
            for x in rows
        ):
            findings.append(Finding(
                "VIS-608", "WARN",
                f"知识点{kid}只有识别题"
            ))
        counts = Counter(x["template_id"] for x in rows)
        duplicate = {k:v for k,v in counts.items() if k and v > 1}
        if duplicate:
            findings.append(Finding(
                "VIS-609", "WARN",
                f"知识点{kid}重复模板", duplicate
            ))

    if p.buttons > 160:
        findings.append(Finding(
            "VIS-611", "WARN",
            f"quiz-opt按钮共{p.buttons}个，疑似全选择事故"
        ))

    # ── VIS-614：交互容器必须在翻页豁免机制中（防复发） ──
    # 交互容器类若出现在课件中，必须被翻页机制豁免，否则点击会误触发翻页。
    # 两种翻页机制二选一：
    #   A) document 级 click 监听豁免名单（含 closest('.drag-container') 等）；
    #   B) click-zone 覆盖翻页（此时交互容器 CSS 需 z-index 高于 click-zone 的 1）。
    findings += _check_pagination_exemption(html, sev(True))

    return findings


def _check_pagination_exemption(html: str, sev_error: str) -> list[Finding]:
    contrad = html.count("data-interaction-contract") + html.count("CW-INTERACTION-CONTRACT")
    containers = {"drag-container", "link-container", "order-container"}
    present = {c for c in containers if re.search(r'class="[^"]*\b' + c + r'\b', html)}
    if not present:
        return []
    findings = []

    # 检测翻页机制
    has_doc_listener = ("addEventListener('click'" in html or 'addEventListener("click"' in html
                        or "document.addEventListener('click'" in html)
    has_click_zone = re.search(r'class="[^"]*\bclick-zone\b', html) is not None

    # 豁免名单须覆盖全部已出现的交互容器
    # 特征：翻页监听用 e.target.closest('.<c>')；交互函数内部用 el/btn.closest()，须区分。
    exempt_missing = []
    for c in present:
        if has_doc_listener and ("e.target.closest('." + c + "')" not in html
                                 and "e.target.closest(\".\" + c" not in html):
            exempt_missing.append(c)
    if exempt_missing:
        findings.append(Finding(
            "VIS-614", sev_error,
            f"翻页豁免名单漏了交互容器类：{exempt_missing}（点击会误触发翻页）"
        ))

    # click-zone 方案：交互容器 CSS 必须提 z-index 至 click-zone（z-index:1）之上
    if has_click_zone:
        zone_confirmed = bool(re.search(r'\.click-zone[^{]*\{[^}]*z-index\s*:\s*1\b', html, re.S))
        for c in present:
            m = re.search(r'\.' + c + r'[^{]*\{[^}]*\}', html, re.S)
            if m and ('.' + c + '{' in html or True):
                z = re.search(r'z-index\s*:\s*(\d+)', m.group(0))
                if not z or int(z.group(1)) <= 1:
                    findings.append(Finding(
                        "VIS-614", sev_error,
                        f"click-zone 覆盖翻页下，.{c} 的 z-index 未高于 click-zone(z-index:1)，点击会被覆盖层拦截"
                    ))
    return findings

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("html", type=Path)
    parser.add_argument("--level", choices=LEVELS, default="medium")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--force", action="store_true",
                        help="忽略 CW-INTERACTION-CONTRACT:1 标记门控，将 ERROR 按规则判定而非降级为 WARN")
    args = parser.parse_args()
    findings = inspect(args.html.read_text(encoding="utf-8"), args.level, force=args.force)
    if args.json:
        print(json.dumps([asdict(x) for x in findings], ensure_ascii=False, indent=2))
    else:
        for item in findings:
            print(f"{item.severity} {item.code}: {item.message}")
    return 1 if any(x.severity == "ERROR" for x in findings) else 0

if __name__ == "__main__":
    raise SystemExit(main())