# -*- coding: utf-8 -*-
"""邓兴华 L16/17/18/20 课件交互容器规范化修复。
只改容器开标签的 class 与 data-* 元数据，不改任何知识点/题干/答案/阅读原文。
步骤：
  1. 备份原 HTML
  2. 定位每个交互容器（quiz-q / quiz-container，含 quiz-opt / fill-input / 元数据）
  3. 依据容器内 DOM 判定 interaction_type / action_type
  4. 重建开标签为 <div class="quiz-q" data-interaction-item="1" data-...>
  5. 修复翻页豁免（VIS-614）
"""
import re, os, shutil

BASE = r'D:\英语教学\邓兴华'
BACKUP = '_旧件_收尾前20260808'

INTERACT = {
    'fill_input': ('fill_in', 'fill'),
    'order': ('order', 'order'),
    'link': ('link', 'link'),
    'drag': ('drag_and_drop', 'drag'),
    'choice': ('single_choice', 'select'),
}

def find_block_end(html, open_pos):
    """从 open_pos 的 <div 开始，返回匹配的 </div> 结束位置（含）"""
    i = open_pos + 4
    depth = 1
    n = len(html)
    while i < n:
        if html[i:i+4] == '<div' and not html[i:i+5] == '<div/':
            # check not <div...> self close --- we count any <div opener
            depth += 1
            i += 4
        elif html[i:i+6] == '</div>':
            depth -= 1
            if depth == 0:
                return i + 6
            i += 6
        else:
            i += 1
    return n

def detect_itype(inner):
    if re.search(r'class="[^"]*fill-input', inner):
        return INTERACT['fill_input']
    if re.search(r'class="[^"]*(?:order-chunk|order-item|order-opt)', inner):
        return INTERACT['order']
    if re.search(r'class="[^"]*(?:link-item|match-item|ec-q|ec-ev)', inner):
        return INTERACT['link']
    if re.search(r'class="[^"]*(?:drag-word|drag-slot|drag-bin|draggable|dd-card)', inner):
        return INTERACT['drag']
    if re.search(r'class="[^"]*quiz-opt', inner):
        return INTERACT['choice']
    return INTERACT['choice']

def extract_attr(open_tag, name):
    m = re.search(r'data-%s="([^"]*)"' % name, open_tag)
    return m.group(1) if m else None

def process(lesson, label):
    html_path = os.path.join(BASE, '第%02d课时' % lesson, '课件成品_网页PPT', label+'.html')
    if not os.path.exists(html_path):
        print('MISS', html_path); return
    bak_dir = os.path.join(BASE, '第%02d课时' % lesson, BACKUP, '课件成品_网页PPT')
    os.makedirs(bak_dir, exist_ok=True)
    bak_file = os.path.join(bak_dir, label+'.html')
    if not os.path.exists(bak_file):
        shutil.copy2(html_path, bak_file)
    h = open(html_path, encoding='utf-8').read()

    # 收集交互容器开标签位置
    opens = []
    for m in re.finditer(r'<div class="quiz-(?:q|container)"', h):
        opens.append((m.start(), m.group(0)))
    # 也收集带 data-interaction-item 但非上述 class 的容器（如 quiz-cols 内嵌）
    # 先处理 quiz-q/quiz-container
    changed = 0
    seq = 0
    # 从后往前替换，避免偏移
    replacements = []
    for start, prefix in opens:
        end = h.find('>', start)
        if end == -1:
            continue
        open_tag = h[start:end+1]
        inner_start = end + 1
        # 找匹配闭合
        b_end = find_block_end(h, start)
        inner = h[inner_start:b_end]
        seq += 1
        itype, action = detect_itype(inner)
        # 提取完好值
        qid = extract_attr(open_tag, 'question-id')
        old_qid = extract_attr(open_tag, 'qid')
        kid = extract_attr(open_tag, 'knowledge-id')
        sec = extract_attr(open_tag, 'section')
        tid = extract_attr(open_tag, 'template-id')
        cog = extract_attr(open_tag, 'cognitive-level')
        if not qid:
            qid = old_qid if old_qid else 'L%02d_ITM_%03d' % (lesson, seq)
        if not kid: kid = 'GEN'
        if not sec: sec = 'core'
        if not tid: tid = 'C-POINT-GENERAL'
        if not cog: cog = 'application'
        new_tag = ('<div class="quiz-q" data-interaction-item="1" '
                   'data-question-id="%s" data-knowledge-id="%s" data-section="%s" '
                   'data-template-id="%s" data-interaction-type="%s" data-action-type="%s" '
                   'data-cognitive-level="%s" data-scorable="true">' % (
                       qid, kid, sec, tid, itype, action, cog))
        replacements.append((start, end+1, new_tag))
        changed += 1
    # 应用（从后往前）
    for start, oend, new_tag in sorted(replacements, key=lambda x: -x[0]):
        h = h[:start] + new_tag + h[oend:]
    # 写回
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(h)
    print('L%d: rebuilt %d containers -> %s' % (lesson, changed, html_path))
    return changed

if __name__ == '__main__':
    for lesson, label in [(16,'第16课时_课件_中等'),(17,'第17课时_课件_中等'),
                          (18,'第18课时_课件_中等'),(20,'第20课时_课件_中等')]:
        process(lesson, label)
    print('DONE')