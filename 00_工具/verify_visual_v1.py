# -*- coding: utf-8 -*-
"""verify_visual_v1.py — 视觉静态检查模块（批次2 V1.1）

仅使用 Python 标准库（html.parser / re / json）。
独立 CLI 运行且可被 verify_v2.py 导入。
不修改输入 HTML，不改变 CSS 声明。

--force 模式（§六 2026-08-04）：对任何 HTML 都执行必需视觉层检查 CSS-I001，
忽略 CW-VISUAL-CONTRACT:1 标记门控，用于校验现存/未带标记课件
（如 L26 重做版、L17/L18、邓兴华 slide 旧件）。

=== 这是保守静态近似，不等同浏览器完整 CSS 解析或 computed style。===
"""
from __future__ import annotations
DATA_DIR = "D:/英语教学/01_数据"

import html.parser
import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Optional, Sequence

# ── 数据结构 ──────────────────────────────────────────────────

@dataclass
class VisualFinding:
    code: str            # 如 "CSS-I001", "VIS-W101"
    severity: str        # "ERROR" | "HIGH-WARN" | "WARN" | "INFO"
    message: str
    page: str | None = None
    evidence: str | None = None

# ── HTML 解析器 ───────────────────────────────────────────────

class _HTMLCollector(html.parser.HTMLParser):
    """收集 HTML 中的 class、style 块、页面 id、标签计数等。"""
    def __init__(self):
        super().__init__()
        self.style_blocks: list[str] = []
        self.script_blocks: list[str] = []
        self.html_classes: set[str] = set()
        self.page_ids: list[str] = []
        self.page_tags: dict[str, int] = {}   # page_id -> 标签数
        self._in_style = False
        self._in_script = False
        self._current_page = "unknown"
        self._page_depth = 0
        self._in_page = False
        self._tag_count = 0
        self._depth = 0
        self._page_class = ""

    def handle_starttag(self, tag, attrs):
        self._tag_count += 1
        self._depth += 1
        d = dict(attrs)
        cls = d.get("class", "")
        if cls:
            for c in cls.split():
                self.html_classes.add(c)
        # 检测 page / slide 容器
        is_page = ("page" in cls.split() if cls else False) or tag == "div" and d.get("id", "").startswith("page")
        is_slide = ("slide" in cls.split() if cls else False)
        if is_page or is_slide:
            pid = d.get("id", f"p{len(self.page_ids)+1}")
            if pid not in self.page_ids:
                self.page_ids.append(pid)
            self._current_page = pid
            self._in_page = True
            self._page_depth = self._depth
            self._page_class = "page" if is_page else "slide"
        if tag == "style" and not self._in_style:
            self._in_style = True
        if tag == "script" and not self._in_script:
            self._in_script = True

    def handle_endtag(self, tag):
        self._depth -= 1
        if self._in_page and self._depth < self._page_depth:
            # 记录当前页标签数
            if self._current_page not in self.page_tags:
                self.page_tags[self._current_page] = 0
            self.page_tags[self._current_page] = self._tag_count
            self._in_page = False
            self._tag_count = 0
        if tag == "style" and self._in_style:
            self._in_style = False
        if tag == "script" and self._in_script:
            self._in_script = False

    def handle_data(self, data):
        if self._in_style:
            self.style_blocks.append(data)
        elif self._in_script:
            self.script_blocks.append(data)

    def handle_comment(self, data):
        # 收集注释用于合同标记检测
        pass

# ── CSS 近似解析 ──────────────────────────────────────────────

def _extract_bracket_depth(css: str) -> int:
    """简易花括号深度检查，忽略注释和字符串。"""
    cleaned = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    cleaned = re.sub(r'"(?:[^"\\]|\\.)*"', '', cleaned)
    cleaned = re.sub(r"'(?:[^'\\]|\\.)*'", '', cleaned)
    depth = 0
    for ch in cleaned:
        if ch == '{': depth += 1
        elif ch == '}': depth -= 1
    return depth

def _parse_css_selectors(css: str, section: str = "unknown") -> list[dict[str, Any]]:
    """近似 CSS 选择器提取。返回 [{selector, section, properties}]。

    注意：这是保守静态近似，不冒充浏览器完整 CSS 解析。
    """
    # 删除注释前先提取边界标记用于合同检测
    markers = []
    for m in re.finditer(r'/\* <(/?CW-[A-Z-]+).*?\*/', css):
        markers.append(m.group(0))

    cleaned = re.sub(r'/\*.*?\*/', '', css, flags=re.S)
    rules = []
    # 逐块提取：匹配选择器 { 声明 }
    pattern = re.compile(r'([^{}]+?)\s*\{([^}]*)\}')
    for m in pattern.finditer(cleaned):
        sel_raw = m.group(1).strip()
        decl = m.group(2).strip()
        if not sel_raw or not decl:
            continue
        # 跳过 @keyframes 中的 from/to/%
        if sel_raw in ('from', 'to') or re.match(r'^\d+%$', sel_raw):
            continue
        # 拆分逗号选择器
        for s in re.split(r'\s*,\s*', sel_raw):
            s = s.strip()
            if not s:
                continue
            props = {}
            for p in re.split(r'\s*;\s*', decl):
                p = p.strip()
                if ':' in p:
                    k, v = p.split(':', 1)
                    props[k.strip()] = v.strip()
            rules.append({
                "selector": s,
                "section": section,
                "properties": props,
                "class_selector": s if s.startswith('.') else None,
            })
    return rules, markers

# ── 加载合同 ──────────────────────────────────────────────────

def load_visual_contract(path: str | None = None) -> dict[str, Any]:
    """加载视觉合同 JSON。"""
    if path is None:
        path = os.path.join(DATA_DIR, "schemas", "visual_contract_v1.json")
    if not os.path.exists(path):
        # 尝试从当前目录找
        path = os.path.join(DATA_DIR, "schemas", "visual_contract_v1.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"visual_contract_v1.json 未找到: {path}")
    return json.load(open(path, encoding="utf-8"))

# ── 主检查函数 ────────────────────────────────────────────────

def inspect_visual_html(
    html: str,
    contract: dict[str, Any] | None = None,
    *,
    contract_mode: str = "page-id",
    force: bool = False,
) -> list[VisualFinding]:
    """对 HTML 课件执行视觉检查。返回 findings 列表。

    contract: 视觉合同 dict（如为 None 会自动加载）
    contract_mode: "page-id" | "slide" | "unknown"
    force: 为 True 时对任何 HTML 都执行必需视觉层检查（CSS-I001），
           忽略 CW-VISUAL-CONTRACT:1 标记门控。用于校验现存/未带标记课件。
    """
    if contract is None:
        contract = load_visual_contract()

    findings: list[VisualFinding] = []
    thresholds = contract.get("thresholds", {})
    font_warn = thresholds.get("font_warn_px", 18)
    font_high = thresholds.get("font_high_risk_px", 16)

    # ── 解析 HTML ──
    collector = _HTMLCollector()
    try:
        collector.feed(html)
    except Exception as exc:
        findings.append(VisualFinding("CSS-PARSE", "WARN", f"HTML 解析异常: {exc}"))
        return findings

    # 合并 style 文本
    css_text = "\n".join(collector.style_blocks)
    # 合并 script 文本
    js_text = "\n".join(collector.script_blocks)

    # 解析 CSS
    all_rules = []
    all_markers = []
    # 按 section 分段解析（如果 CSS 中有合同标记，按标记分段）
    sections = re.split(r'(/\* <CW-SECTION[^>]*>\s*\*/)', css_text)
    current_section = "unknown"
    for seg in sections:
        seg = seg.strip()
        if seg.startswith("/* <CW-SECTION"):
            m = re.search(r'name="([^"]+)"', seg)
            current_section = m.group(1) if m else "unknown"
        elif seg:
            rules, markers = _parse_css_selectors(seg, current_section)
            all_rules.extend(rules)
            all_markers.extend(markers)

    # CSS 选择器集合
    css_class_selectors = set()
    css_all_selectors = set()
    for r in all_rules:
        css_all_selectors.add(r["selector"])
        # 从选择器中提取所有类名（支持复合选择器 .a.b / 后代 .a .b）
        for m in re.finditer(r'\.([A-Za-z_][\w-]*)', r["selector"]):
            css_class_selectors.add(m.group(1))

    # ── 检测合同标记（仅新合同 page-id） ──
    has_contract_marker = "CW-VISUAL-CONTRACT:1" in html
    is_new_contract = contract_mode == "page-id" and has_contract_marker
    # --force 模式：对任何 HTML 都执行必需视觉层检查（忽略合同标记门控）
    run_req_check = force or is_new_contract

    # ── CSS-I001：必需视觉层缺失（--force 或新合同课件） ──
    # 规则（§一 1.1）：若任一必需选择器在 HTML 中被使用（class="xxx" 出现）
    # 但 <style> 中没有同名选择器定义 → ERROR，阻止交付（打印"视觉层缺失：xxx"）。
    if run_req_check:
        # 取对应契约的必需视觉选择器清单
        if contract_mode == "slide":
            req_sels = contract.get("always_required_selectors_slide", [])
        else:
            req_sels = contract.get("always_required_selectors_page", [])
        missing_used = []
        for sel in req_sels:
            cls = sel[1:] if sel.startswith('.') else sel
            # HTML 中使用了该 class 但 CSS 中无同名选择器
            if cls in collector.html_classes and cls not in css_class_selectors:
                missing_used.append(sel)
        high_absent = 0  # 必需类整体消失的计数（HTML 中完全未出现的主类）
        for sel in req_sels:
            cls = sel[1:] if sel.startswith('.') else sel
            if cls not in collector.html_classes:
                high_absent += 1
        if missing_used:
            findings.append(VisualFinding("CSS-I001", "ERROR",
                f"必需视觉层缺失: {', '.join(missing_used[:12])}"
                + (f" 等 {len(missing_used)} 项" if len(missing_used) > 12 else ""),
                evidence="HTML 使用但 <style> 无同名选择器"))
        # 必需类整体大面积消失（如 section-head 类全无）→ ERROR
        if req_sels and high_absent >= len(req_sels) * 0.5:
            findings.append(VisualFinding("CSS-I001", "ERROR",
                f"必需视觉层整体大面积消失: {high_absent}/{len(req_sels)} 个必需类在 HTML 中未出现",
                evidence="视觉层疑似被整体删除"))

        # 合同标记检查（仅新合同课件强制；--force 下也检查 CSS_EXTRA 完整性）
        req_markers = contract.get("required_markers", [])
        markers_joined = " ".join(all_markers) + " " + css_text
        for mkr in req_markers:
            if (mkr not in markers_joined and mkr not in html) and is_new_contract:
                findings.append(VisualFinding("CSS-I001", "ERROR",
                    f"必需视觉标记缺失: {mkr}"))

        # CSS_EXTRA 开始/结束标记（新合同强制；--force 下仅提示）
        if "<CW-CSS-EXTRA" not in markers_joined and "<CW-CSS-EXTRA" not in html:
            findings.append(VisualFinding("CSS-I001",
                "ERROR" if is_new_contract else "WARN",
                "CSS_EXTRA 开始标记缺失 (<CW-CSS-EXTRA)"))
        if "</CW-CSS-EXTRA>" not in markers_joined and "</CW-CSS-EXTRA>" not in html:
            findings.append(VisualFinding("CSS-I001",
                "ERROR" if is_new_contract else "WARN",
                "CSS_EXTRA 结束标记缺失 (</CW-CSS-EXTRA>)"))

    # ── CSS-I003：视觉层疑似整体删除 ──
    if run_req_check and len(css_class_selectors) == 0:
        findings.append(VisualFinding("CSS-I003", "ERROR",
            "CSS_EXTRA 选择器数为 0，视觉层疑似整体删除"))
    if run_req_check and not css_text.strip():
        findings.append(VisualFinding("CSS-I003", "ERROR",
            "CSS_EXTRA 正文为空，视觉层疑似整体删除"))

    # ── CSS-I002：使用组件的必需选择器缺失 ──
    # 遍历 HTML 出现的 class，检查其组件合同
    component_contracts = contract.get("component_contracts", {})
    for html_cls in sorted(collector.html_classes):
        required_sel = component_contracts.get(html_cls)
        if not required_sel:
            continue
        for sel in required_sel:
            # 去掉前导点转到 class 名
            sel_cls = sel[1:] if sel.startswith('.') else sel
            if sel_cls not in css_class_selectors:
                findings.append(VisualFinding("CSS-I002", "ERROR" if run_req_check else "WARN",
                    f"组件 {html_cls} 的必需选择器 {sel} 在 CSS 中未定义",
                    evidence=f"触发class: {html_cls}"))

    # ── CSS-I004：style 块损坏 ──
    style_open = html.count("<style")
    style_close = html.count("</style>")
    if style_open != style_close:
        findings.append(VisualFinding("CSS-I004", "ERROR",
            f"<style> 开合不平衡: {style_open} open / {style_close} close"))
    bd = _extract_bracket_depth(css_text)
    if bd != 0:
        findings.append(VisualFinding("CSS-I004", "WARN" if not is_new_contract else "ERROR",
            f"CSS 花括号不平衡: {bd}"))

    # ── CSS-W001：HTML class 无静态选择器 ──
    allow_classes = set(contract.get("allow_classes", []))
    # JS 动态 class
    js_dynamic_classes = set()
    # classList.add/remove/toggle('class')
    for m in re.finditer(r'classList\.(?:add|remove|toggle)\(["\']([^"\']+)["\']', js_text):
        for cls in m.group(1).split():
            js_dynamic_classes.add(cls)
    # className = 'class'
    for m in re.finditer(r'className\s*=\s*["\']([^"\']+)["\']', js_text):
        for cls in m.group(1).split():
            js_dynamic_classes.add(cls)
    # setAttribute('class', 'class')
    for m in re.finditer(r'setAttribute\(["\']class["\'],\s*["\']([^"\']+)["\']', js_text):
        for cls in m.group(1).split():
            js_dynamic_classes.add(cls)
    # classList.replace('old', 'new')
    for m in re.finditer(r'classList\.replace\(["\']([^"\']+)["\'],\s*["\']([^"\']+)["\']', js_text):
        js_dynamic_classes.add(m.group(1))
        js_dynamic_classes.add(m.group(2))
    no_selector = []
    for cls in sorted(collector.html_classes):
        if cls in css_class_selectors or cls in allow_classes or cls in js_dynamic_classes:
            continue
        no_selector.append(cls)
    if no_selector:
        findings.append(VisualFinding("CSS-W001", "WARN",
            f"{len(no_selector)} 个 HTML class 无同名 CSS 选择器定义",
            evidence=", ".join(no_selector[:15])))

    # ── CSS-W002：CSS 孤儿选择器 ──
    all_html_and_js = collector.html_classes | js_dynamic_classes | allow_classes
    orphan = [s for s in sorted(css_class_selectors)
              if s not in all_html_and_js]
    ratio = len(orphan) / len(css_class_selectors) if css_class_selectors else 0
    if ratio > thresholds.get("orphan_selector_ratio_warn", 0.25):
        findings.append(VisualFinding("CSS-W002", "WARN",
            f"孤儿选择器占比 {ratio:.0%} > 25%",
            evidence=", ".join(orphan[:10])))

    # ── CSS-W003：重复选择器 ──
    seen = {}
    dups = []
    for r in all_rules:
        sel = r["selector"]
        if sel not in seen:
            seen[sel] = []
        seen[sel].append(r)
    for sel, occ in seen.items():
        if len(occ) >= 2:
            dups.append(f"{sel} ({len(occ)}x)")
    if dups:
        findings.append(VisualFinding("CSS-W003", "WARN",
            f"{len(dups)} 个重复选择器",
            evidence=", ".join(dups[:8])))

    # ── CSS-W004：主题层越权 ──
    forbidden_props = set(contract.get("theme_forbidden_properties", []))
    for r in all_rules:
        if r["section"] != "theme":
            continue
        for prop in r["properties"]:
            if prop in forbidden_props:
                findings.append(VisualFinding("CSS-W004", "WARN",
                    f"主题层越权: {r['selector']} 含 {prop}",
                    evidence=f"{prop}: {r['properties'][prop]}"))
                break

    # ── CSS-W005：!important 治理 ──
    important_count = css_text.count("!important")
    if important_count > thresholds.get("important_high_risk", 10):
        findings.append(VisualFinding("CSS-W005", "HIGH-WARN",
            f"!important 总数 {important_count} > {thresholds.get('important_high_risk', 10)}"))
    elif important_count > thresholds.get("important_warn", 5):
        findings.append(VisualFinding("CSS-W005", "WARN",
            f"!important 总数 {important_count} > {thresholds.get('important_warn', 5)}"))

    # ── CSS-W007/W008：直接颜色/圆角/阴影过多 ──
    hex_colors = set(re.findall(r'#[0-9a-fA-F]{3,8}', css_text))
    if len(hex_colors) > thresholds.get("direct_color_warn", 18):
        findings.append(VisualFinding("CSS-W007", "WARN",
            f"直接颜色字面量 {len(hex_colors)} > {thresholds.get('direct_color_warn', 18)}"))
    radii = set(re.findall(r'border-radius\s*:\s*([^;]+)', css_text))
    if len(radii) > thresholds.get("radius_value_warn", 6):
        findings.append(VisualFinding("CSS-W008", "WARN",
            f"不同 border-radius 值 {len(radii)} > {thresholds.get('radius_value_warn', 6)}"))
    shadows = set(re.findall(r'box-shadow\s*:\s*([^;]+)', css_text))
    if len(shadows) > thresholds.get("shadow_value_warn", 8):
        findings.append(VisualFinding("CSS-W008", "WARN",
            f"不同 box-shadow 值 {len(shadows)} > {thresholds.get('shadow_value_warn', 8)}"))

    # ── VIS-W101：小字号 ──
    for r in all_rules:
        for prop, val in r["properties"].items():
            if prop in ("font-size",):
                px = re.findall(r'(\d+)px', val)
                if px and int(px[0]) < font_high:
                    findings.append(VisualFinding("VIS-W101", "HIGH-WARN",
                        f"字号过小: {r['selector']} = {val}",
                        evidence=f"< {font_high}px"))
                elif px and int(px[0]) < font_warn:
                    findings.append(VisualFinding("VIS-W101", "WARN",
                        f"字号偏小: {r['selector']} = {val}",
                        evidence=f"< {font_warn}px"))

    # ── VIS-W106：例词长串 ──
    long_word_seq = re.findall(
        r'\b[A-Za-z][A-Za-z\'-]*\b(?:\s*[,，;；]\s*\b[A-Za-z][A-Za-z\'-]*\b){5,}',
        html)
    if long_word_seq:
        findings.append(VisualFinding("VIS-W106", "WARN",
            f"发现 {len(long_word_seq)} 处例词长串（≥6 个逗号分隔英文词）",
            evidence=long_word_seq[0][:80]))

    # ── VIS-W201：卡片过多（近似） ──
    card_count = html.count('class="') - html.count('class="page') - html.count('class="quiz-opt')
    # 粗略统计：page 约 40-45，quiz-opt 约 100-300
    # 用 card 关键词近似
    card_keywords = sum(html.count(f'class="{k}') for k in
                        ['card', 'ext-card', 'game-board', 'vocab-card', 'rule-card',
                         'note-panel', 'kmap-node'])
    if card_keywords > thresholds.get("cards_warn", 8) * 10:
        findings.append(VisualFinding("VIS-W201", "WARN",
            f"卡片/块较多: 约 {card_keywords} 个"))

    # ── VIS-W301：长解析默认展开（近似） ──
    for m in re.finditer(r'<div[^>]*class="[^"]*explain[^"]*"[^>]*>([\s\S]{0,500})</div>', html):
        text = re.sub(r'<[^>]+>', '', m.group(1)).strip()
        if len(text) > 400:
            findings.append(VisualFinding("VIS-W301", "WARN",
                f"解析默认展开，文本 {len(text)} 字符 > 400"))
            break

    # ── VIS-W401：缺少减弱动画 ──
    if "animation" in css_text or "transition" in css_text:
        if "prefers-reduced-motion" not in css_text:
            findings.append(VisualFinding("VIS-W401", "WARN",
                "存在 animation/transition 但无 prefers-reduced-motion"))

    # ── VIS-W402：无限动画过多 ──
    infinite_count = css_text.count("infinite")
    if infinite_count > 2:
        findings.append(VisualFinding("VIS-W402", "WARN",
            f"无限动画 {infinite_count} 处 > 2"))
    # 阅读/规则页出现无限动画
    reading_has_infinite = bool(re.search(
        r'(reading|passage|rule|error).*?animation.*?infinite',
        css_text, re.I | re.S))
    if reading_has_infinite:
        findings.append(VisualFinding("VIS-W402", "WARN",
            "阅读/规则/解析页存在无限动画"))

    # ── VIS-W206：超宽阅读容器 ──
    if not re.search(r'max-width\s*:\s*\d+', css_text):
        findings.append(VisualFinding("VIS-W206", "WARN",
            "阅读正文可能无 max-width 限制"))

    # ── VIS-W207：固定高度+隐藏溢出 ──
    for r in all_rules:
        props = r["properties"]
        height = props.get("height", "")
        ov = props.get("overflow", "")
        if re.match(r'\d+px', height) and 'hidden' in ov:
            findings.append(VisualFinding("VIS-W207", "WARN",
                f"固定高度+隐藏溢出: {r['selector']}"))

    # ── VIS-W304：触屏目标风险 ──
    for r in all_rules:
        for prop, val in r["properties"].items():
            if prop in ("width", "height", "min-width", "min-height"):
                px = re.findall(r'(\d+)px', val)
                if px and int(px[0]) < 44 and int(px[0]) > 0:
                    findings.append(VisualFinding("VIS-W304", "WARN",
                        f"触屏目标 {r['selector']} {prop}={val} < 44px"))
                    break

    # ── VIS-W403：装饰干扰 ──
    if re.search(r'canvas|particles|floating|blink', html, re.I):
        readings = ["reading", "passage", "rule", "error"]
        found = False
        for r_cls in readings:
            pages_with_reading = re.findall(
                r'<div[^>]*class="[^"]*' + r_cls + r'[^"]*"[\s\S]{0,200}?(?:canvas|particles|floating)',
                html, re.I)
            if pages_with_reading:
                found = True
                break
        if found:
            findings.append(VisualFinding("VIS-W403", "WARN",
                "阅读/规则/解析页含装饰干扰（Canvas/粒子/漂浮）"))

    # ── CSS-W009：--cw-* 变量缺 fallback ──
    cw_vars_used = set(re.findall(r'var\((--cw-[\w-]+)', css_text))
    cw_vars_defined = set(re.findall(r'--cw-[\w-]+', css_text))
    # 通常定义在 :root 中，也在 var() 引用中
    for v in cw_vars_used:
        if v not in cw_vars_defined:
            # 检查是否有 fallback
            has_fb = bool(re.search(r'var\(' + re.escape(v) + r'\s*,', css_text))
            if not has_fb:
                findings.append(VisualFinding("CSS-W009", "WARN",
                    f"自定义属性 {v} 缺少 fallback"))

    # ── VIS-W204：疑似空页 ──
    # 通过页面内可见文本计数近似
    for pid in collector.page_ids:
        # 用正则找该页面的文本内容
        page_pattern = re.compile(
            r'<div[^>]*(?:id="' + re.escape(pid) + r'"|class="[^"]*page[^"]*")[\s\S]{0,3000}?'
            r'</div>\s*<!--\s*end\s+page',
            re.I)
        if not page_pattern.search(html):
            continue
        # 更简单的近似：检查页面内是否包含字母
        text = re.sub(r'<[^>]+>', '', html)
        if len(text.strip()) < 20:
            findings.append(VisualFinding("VIS-W204", "WARN",
                f"疑似空页: {pid}"))

    # ── VIS-W303：缺少焦点或按压状态 ──
    has_focus_visible = ":focus-visible" in css_text or ":focus" in css_text
    has_active = ":active" in css_text
    if collector.html_classes & {"quiz-opt", "btn", "button"} and not has_focus_visible:
        findings.append(VisualFinding("VIS-W303", "WARN",
            "存在按钮/选项但无 :focus-visible"))
    if collector.html_classes & {"quiz-opt", "btn", "button"} and not has_active:
        findings.append(VisualFinding("VIS-W303", "WARN",
            "存在触屏选项但无 :active 状态"))

    return findings

# ── CLI 入口 ──────────────────────────────────────────────────

def main(argv: Sequence[str] | None = None) -> int:
    if argv is None:
        argv = sys.argv[1:]
    if not argv:
        print("用法: python verify_visual_v1.py <html_path> [--contract PATH] [--json] [--force]")
        return 2

    html_path = argv[0]
    contract_path = None
    output_json = False
    force = False

    i = 1
    while i < len(argv):
        if argv[i] == "--contract" and i + 1 < len(argv):
            contract_path = argv[i + 1]
            i += 2
        elif argv[i] == "--json":
            output_json = True
            i += 1
        elif argv[i] == "--force":
            force = True
            i += 1
        else:
            i += 1

    if not os.path.exists(html_path):
        print(f"ERROR: 文件不存在 {html_path}", file=sys.stderr)
        return 2

    try:
        html = open(html_path, encoding="utf-8").read()
    except Exception as exc:
        print(f"ERROR: 读取文件失败 {exc}", file=sys.stderr)
        return 2

    try:
        contract = load_visual_contract(contract_path)
    except Exception as exc:
        print(f"ERROR: 加载合同失败 {exc}", file=sys.stderr)
        return 2

    # 检测契约类型
    contract_mode = "page-id"
    if re.search(r'<div class="slide(?:"| )', html):
        contract_mode = "slide"

    findings = inspect_visual_html(html, contract, contract_mode=contract_mode, force=force)

    errors = [f for f in findings if f.severity == "ERROR"]
    high_warns = [f for f in findings if f.severity == "HIGH-WARN"]
    warns = [f for f in findings if f.severity == "WARN"]
    infos = [f for f in findings if f.severity == "INFO"]

    if output_json:
        import dataclasses
        def _asdict(o):
            return dataclasses.asdict(o)
        result = {
            "file": os.path.basename(html_path),
            "contract_mode": contract_mode,
            "force": force,
            "errors": len(errors),
            "high_warns": len(high_warns),
            "warns": len(warns),
            "findings": [_asdict(f) for f in findings],
        }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        sev_order = ["ERROR", "HIGH-WARN", "WARN", "INFO"]
        for sev in sev_order:
            items = [f for f in findings if f.severity == sev]
            for f in items:
                tag = f"[{f.severity}]"
                print(f"{tag:20s} {f.code:12s} {f.message}")
                if f.evidence:
                    print(f"{'':20s} 证据: {f.evidence}")
        print(f"\n视觉检查{'(--force)' if force else ''}: ERROR={len(errors)}  HIGH-WARN={len(high_warns)}  WARN={len(warns)}")

    return 1 if errors else 0

if __name__ == "__main__":
    sys.exit(main())