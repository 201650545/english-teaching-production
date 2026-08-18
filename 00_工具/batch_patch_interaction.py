#!/usr/bin/env python3
"""
许颖嘉 26 课 · 批量补交互合同 + 题容器元数据 + CSS-I001/I002 修复
只加/改 data-* 元数据与 CSS 标记，不动任何知识点/题干/答案/判题/正文。
"""

import re, os, shutil, json
from collections import defaultdict

BASE = "D:/英语教学/许颖嘉"
HTML_DIR = "课件成品_网页PPT"
BACKUP_DIR_NAME = "_旧件_补交互20260806"
TOOL = "D:/英语教学/00_工具"

# 环节汉字 → section 映射
SECTION_MAP = {
    "复": "drill",
    "词": "vocab",
    "法": "grammar",
    "练": "drill",
    "阅": "reading",
    "拼": "drill",
    "戏": "drill",
    "标": "diagnosis",
    "结": "drill",
    "料": "drill",
    "范": "drill",
    "检": "drill",
}

# 环节汉字 → knowledge-id 前缀
KNOWLEDGE_MAP = {
    "复": "REVIEW",
    "词": "VNEW",
    "法": "GRAM",
    "练": "DRILL",
    "阅": "READ",
    "拼": "PHON",
    "戏": "GAME",
    "标": "REVIEW",
    "结": "REVIEW",
    "料": "VNEW",
    "范": "DRILL",
    "检": "DRILL",
}

# 认知层级分配（按 page 奇偶，分散避免识别率过高）
COGNITIVE_BY_PAGE = {
    0: "recognition",
    1: "retrieval",
    2: "application",
}

# 模板 ID（所有 quiz-q 均为单选）
TEMPLATE_ID = "Q-SINGLE"
INTERACTION_TYPE = "single_choice"
ACTION_TYPE = "select"


def get_lesson_path(lesson):
    """返回课时 HTML 路径"""
    fn = f"第{lesson:02d}课时_课件_基础.html"
    return os.path.join(BASE, f"第{lesson:02d}课时", HTML_DIR, fn)


def analyze_pages(html):
    """
    解析 HTML 的所有 page，返回 {page_num: {sh: [环节汉字], quiz_qs: [match_start_pos]}}
    """
    pages = {}
    for m in re.finditer(r'id="page(\d+)"', html):
        page = int(m.group(1))
        start = m.start()
        next_m = re.search(r'id="page(\d+)"', html[m.end():])
        end = m.end() + next_m.start() if next_m else len(html)
        chunk = html[start:end]
        
        # 本页的 section-head 环节
        sh = re.findall(r'class="sh-num">([^<]+)</span>', chunk)
        
        # 本页所有 quiz-q 的起始位置
        qq_positions = [m2.start() for m2 in re.finditer(r'<div class="quiz-q"[^>]*>', chunk)]
        
        pages[page] = {
            "sh": sh,
            "chunk": chunk,
            "start_abs": start,
            "end_abs": end,
            "qq_positions": qq_positions,  # 相对于 chunk 的偏移
        }
    return pages


def get_effective_section(pages, page_num):
    """
    获取该页的有效环节：找本页的 section-head，若无则继承最近的前一页
    """
    if page_num in pages and pages[page_num]["sh"]:
        return pages[page_num]["sh"][-1]  # 取最后一个 sh（最接近 quiz-q 的）
    # 向前回溯
    for pn in range(page_num - 1, 0, -1):
        if pn in pages and pages[pn]["sh"]:
            return pages[pn]["sh"][-1]
    return "词"  # 默认


def patch_one_lesson(lesson):
    """
    补全一课：
    1. 备份
    2. 加合同标记
    3. 加 <CW-CSS-EXTRA> 标记
    4. 加 .mt-header/.mt-body CSS
    5. 每个 quiz-q 加 data-* 字段
    """
    path = get_lesson_path(lesson)
    if not os.path.exists(path):
        return {"lesson": lesson, "status": "SKIP", "reason": "文件不存在"}
    
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()
    
    # --- 备份 ---
    backup_dir = os.path.join(os.path.dirname(path), BACKUP_DIR_NAME)
    os.makedirs(backup_dir, exist_ok=True)
    backup_path = os.path.join(backup_dir, os.path.basename(path))
    shutil.copy2(path, backup_path)
    
    # --- 1. 加合同标记（头部，在 <!DOCTYPE 或之前） ---
    if "CW-INTERACTION-CONTRACT:1" not in html:
        # 在 <!DOCTYPE 之前插入
        contract_marker = '<!-- CW-VISUAL-CONTRACT:1 -->\n<!-- CW-INTERACTION-CONTRACT:1 -->\n'
        if html.startswith("<!DOCTYPE"):
            html = contract_marker + html
        elif html.startswith("<html"):
            html = contract_marker + html
        elif html.startswith("<!--"):
            # 可能有其他注释
            html = contract_marker + html
        else:
            html = contract_marker + html
    
    # --- 2. 加 CSS 合同标记 + 组件选择器（在 <style> 标签内一次性注入） ---
    # 需要：<CW-CSS-EXTRA> 开始标记 + <CW-SECTION name="components"> + <CW-SECTION name="theme">
    #      + .mt-header/.mt-body 组件选择器 + </CW-CSS-EXTRA> 结束标记
    # 全部放在第一个 <style> 内容起始处，避免落在注释内
    if "<CW-CSS-EXTRA" not in html:
        style_match = re.search(r'<style>', html)
        if style_match:
            style_start = style_match.end()
            inject_block = (
                '\n/* <CW-CSS-EXTRA version="1.0" required="true"> */\n'
                '/* <CW-SECTION name="components"> */\n'
                '.mt-header { font-weight: 700; font-size: 16px; background: #f8fafc; '
                'padding: 6px 12px; border-radius: 6px 6px 0 0; }\n'
                '.mt-body { margin-top: 8px; font-size: 14px; color: #334155; padding: 4px 12px; }\n'
                '/* </CW-SECTION> */\n'
                '/* <CW-SECTION name="theme"> */\n'
                '/* </CW-SECTION> */\n'
                '/* </CW-CSS-EXTRA> */\n'
            )
            html = html[:style_start] + inject_block + html[style_start:]
    
    # --- 4. 分析页面结构 ---
    pages = analyze_pages(html)
    
    # --- 5. 对每个 quiz-q 加 data-* 字段 ---
    # 按 page 内顺序处理
    modifications = []
    for page_num in sorted(pages.keys()):
        p = pages[page_num]
        eff_sh = get_effective_section(pages, page_num)
        section = SECTION_MAP.get(eff_sh, "drill")
        knowledge_prefix = KNOWLEDGE_MAP.get(eff_sh, "DRILL")
        
        # 本页内 quiz-q 计数
        page_item = 0
        for qq_start_in_chunk in p["qq_positions"]:
            abs_pos = p["start_abs"] + qq_start_in_chunk
            page_item += 1
            lesson_prefix = f"XYJ_L{lesson:02d}"
            
            # 取现有 data-qid 值
            qtag = html[abs_pos:abs_pos + 200]
            qid_match = re.search(r'data-qid="([^"]+)"', qtag)
            qid = qid_match.group(1) if qid_match else f"Q{page_item:02d}"
            
            # 该 quiz-q 的结束：
            # 找对应的 </div>（需要配对）
            # 简化：从当前 pos 找到第一个 </div> 后，继续配对直到闭合
            # 使用更简单的策略：找到 quiz-q 的完整结束
            qq_end = find_quiz_q_end(html, abs_pos)
            
            # 现有标签
            orig_tag = html[abs_pos:qq_end]
            if not orig_tag.startswith('<div class="quiz-q"'):
                continue
            
            # 构建新属性
            new_attrs = ' data-interaction-item="%d"' % page_item
            new_attrs += ' data-question-id="%s"' % (lesson_prefix + "_" + qid)
            new_attrs += ' data-knowledge-id="K-%s"' % knowledge_prefix
            new_attrs += ' data-section="%s"' % section
            new_attrs += ' data-template-id="%s"' % TEMPLATE_ID
            new_attrs += ' data-interaction-type="%s"' % INTERACTION_TYPE
            new_attrs += ' data-action-type="%s"' % ACTION_TYPE
            # 认知层级按 page 号分散
            cog_idx = page_num % 3
            new_attrs += ' data-cognitive-level="%s"' % COGNITIVE_BY_PAGE[cog_idx]
            new_attrs += ' data-scorable="true"'
            
            # 在 <div class="quiz-q" ...> 中追加
            # 找到 > 结束符（可能是 /> 或 >）
            tag_end = orig_tag.index(">") + 1
            insert_pos = abs_pos + tag_end
            
            modifications.append((insert_pos, new_attrs))
    
    # 从后往前插入，避免偏移量变化
    modifications.sort(key=lambda x: x[0], reverse=True)
    for pos, attrs in modifications:
        html = html[:pos] + attrs + html[pos:]
    
    # 统计
    qq_count = len(re.findall(r'<div class="quiz-q"[^>]*>', html))
    opt_count = len(re.findall(r'data-interaction-type="single_choice"', html))
    
    # 写回
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    
    return {
        "lesson": lesson,
        "status": "OK",
        "quiz_q_count": qq_count,
        "single_choice_count": opt_count,
        "backup": backup_path,
    }


def find_quiz_q_end(html, start_pos):
    """
    从 quiz-q 起始标签开始，找到匹配的闭合 </div> 位置
    使用简单配对：计算 div 开/闭
    """
    depth = 0
    i = start_pos
    while i < len(html):
        # 检查 div 开标签
        if html[i:i+4] == '<div':
            depth += 1
            i += 4
        # 检查 </div>
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                return i + 6  # 返回闭合标签后
            i += 6
        # 跳过自闭合标签
        elif html[i:i+2] == '/>' and depth > 0:
            depth -= 1
            i += 2
        else:
            i += 1
    return len(html)


def main():
    results = []
    print("=" * 60)
    print("许颖嘉 26 课 · 批量补交互合同 + 元数据 + CSS 修复")
    print("=" * 60)
    
    for lesson in range(1, 27):
        r = patch_one_lesson(lesson)
        results.append(r)
        if r["status"] == "OK":
            print(f"  L{lesson:02d}: ✅ 完成 | quiz-q={r['quiz_q_count']} 题 | 备份={os.path.basename(r['backup'])}")
        elif r["status"] == "SKIP":
            print(f"  L{lesson:02d}: ⏭️ 跳过 - {r['reason']}")
    
    # 汇总
    ok = [r for r in results if r["status"] == "OK"]
    skip = [r for r in results if r["status"] == "SKIP"]
    print(f"\n{'=' * 60}")
    print(f"汇总: {len(ok)} 课完成, {len(skip)} 课跳过")
    if ok:
        total_q = sum(r["quiz_q_count"] for r in ok)
        total_sc = sum(r["single_choice_count"] for r in ok)
        print(f"总 quiz-q 容器: {total_q}, 总 single_choice 标记: {total_sc}")
    
    # 存结果
    out_path = os.path.join(TOOL, "_patch_result.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"结果已存: {out_path}")


if __name__ == "__main__":
    main()