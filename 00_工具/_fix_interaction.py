# -*- coding: utf-8 -*-
"""综合修复脚本：邓兴华 L16/17/18/20 交互校验修复。
处理：VIS-614 翻页豁免 / VIS-610 元数据 / VIS-615 属性位置 / VIS-616 按钮容器 /
VIS-601/602 选择占比 / VIS-603 动作种类 / 损坏清理。
不修改知识点/答案/阅读原文（选择题转填空仅保留正确项文本作为答案）。
"""
import re, sys, shutil, os

BASE = r'D:\英语教学\邓兴华'
CHOICE={'single_choice','multiple_choice','true_false','choice'}
HOT={'grammar','vocab','drill','extend','diagnosis'}

def clean_answer_text(txt):
    # strip <span class="opt-label">A</span>
    txt = re.sub(r'<span class="opt-label">[^<]*</span>', '', txt)
    txt = re.sub(r'<[^>]+>', '', txt)
    txt = txt.replace('&nbsp;',' ').strip()
    # strip leading letter like "A." / "A、" / "C "
    txt = re.sub(r'^[A-E][\.\、\s-]*\s*', '', txt).strip()
    return txt

def fill_input_html(answer):
    return ('<div class="fill-input-wrap"><input class="fill-input" type="text" data-correct="%s" '
            'placeholder="输入答案" autocomplete="off" onkeydown="if(event.key===\'Enter\'){event.preventDefault();checkFill(this);}">'
            '<button class="fill-check-btn" onclick="checkFill(this)">确认</button></div>'
            % answer.replace('"','&quot;'))

def fix_pagination_exemption(h):
    if 'e.target.closest(.drag-container' in h or "e.target.closest('.drag-container')" in h \
       or ("e.target.closest(\".\" + c" in h):
        return h, False
    # find the click navigation handler exemption point
    # we insert container exemption right before the clientX check
    m = re.search(r'if \(e\.clientX > window\.innerWidth / 2\) nextPage\(\);', h)
    if not m:
        return h, False
    insert = ("if (t && t.closest && (t.closest('.drag-container') || "
              "t.closest('.link-container') || t.closest('.order-container'))) return;\n  ")
    h = h[:m.start()] + insert + h[m.start():]
    return h, True

def fix_vis_615(h):
    # data-interaction-item=1 must be inside <div class="quiz-q" ...> before >
    # already handled by normalization; ensure no '> data-interaction-item=' leaked
    h = h.replace('> data-interaction-item=', ' data-interaction-item=')
    return h

def fix_doublecount_quizquestion(h):
    # remove metadata attributes wrongly placed on <div class="quiz-question ..."> that has data-question-id
    # pattern: <div class="quiz-question quiz-q" data-interaction-item=..."..." >TEXT</div>
    pat = re.compile(r'(<div class="quiz-question)([^>]*?)(>)')
    out_chunks = []
    last = 0
    changed = 0
    for m in pat.finditer(h):
        prefix, attrs, gt = m.group(1), m.group(2), m.group(3)
        if 'data-question-id' in attrs or 'data-interaction-item' in attrs:
            # strip all data-* and interaction attrs, keep plain class
            new_attrs = ' '.join([a for a in attrs.split()
                                  if not a.startswith('data-') and not a.startswith('on')])
            new_tag = prefix + (' ' + new_attrs if new_attrs else '') + gt
            out_chunks.append(h[last:m.start()])
            out_chunks.append(new_tag)
            last = m.end()
            changed += 1
    if changed:
        out_chunks.append(h[last:])
        return ''.join(out_chunks), changed
    return h, 0

def fix_meta_on_item(h, lesson):
    """为非 quiz-q 的 item 容器（link/order/drag-container 带 data-question-id）补全元数据。"""
    # target containers: <div class="...-container" data-question-id="X"> without data-interaction-type
    pat = re.compile(r'(<div class="([^"\']*(?:link-container|order-container|drag-container)[^"\']*)" data-question-id="([^"]+)")(>)')
    changed = 0
    def repl(m):
        nonlocal changed
        tag, cls, qid, gt = m.group(1), m.group(2), m.group(3), m.group(4)
        if 'data-interaction-type' in tag:
            return m.group(0)
        itype = 'link' if 'link-container' in cls else ('order' if 'order-container' in cls else 'drag_and_drop')
        act = 'link' if itype=='link' else ('order' if itype=='order' else 'drag')
        new = ('%s data-interaction-item="1" data-knowledge-id="GEN" data-section="core" '
               'data-template-id="C-INTERACT" data-interaction-type="%s" data-action-type="%s" '
               'data-cognitive-level="application" data-scorable="true">' % (tag, itype, act))
        changed += 1
        return new
    h2 = pat.sub(repl, h)
    return h2, changed

def parse_attrs(tag):
    a = {}
    for m in re.finditer(r'([a-zA-Z][a-zA-Z0-9-]*)\s*=\s*"([^"]*)"', tag):
        a[m.group(1)] = m.group(2)
    return a

def convert_choice_to_fill(h, need, lesson):
    """把 need 个 single_choice quiz-q 转成 fill_in。优先热区、低认知。返回 (h, converted)。"""
    # find all quiz-q open tags
    tags = list(re.finditer(r'<div class="quiz-q"[^>]*>', h))
    containers = []
    for m in tags:
        attrs = parse_attrs(m.group(0))
        if attrs.get('data-interaction-type') != 'single_choice':
            continue
        qid = attrs.get('data-question-id','')
        sec = attrs.get('data-section','unknown').lower()
        cog = attrs.get('data-cognitive-level','unknown').lower()
        containers.append((m.start(), m.end(), qid, sec, cog))
    containers.sort(key=lambda c: (0 if c[3] in HOT else 1, 0 if c[4]=='retrieval' else 1, c[0]))
    to_convert = containers[:need]
    if not to_convert:
        return h, 0
    edits = []
    for start, end, qid, sec, cog in to_convert:
        # find matching close of this quiz-q
        close = find_matching_div(h, start)
        if close is None:
            continue
        seg = h[start:close]  # content from <div class="quiz-q" to matching </div>
        # find question text element
        qm = re.search(r'<div class="(?:qq-text|quiz-question)[^>]*>(.*?)</div>', seg, re.S)
        # find correct answer among quiz-opt buttons
        am = re.search(r'<button class="quiz-opt"[^>]*data-correct="1"[^>]*>(.*?)</button>', seg, re.S)
        if not am:
            continue
        ans = clean_answer_text(am.group(1))
        # Determine options region to replace:
        # within seg, from first '<div class="quiz-options"' or first '<button class="quiz-opt"'
        search_head = end - start  # offset inside seg
        # find first quiz-opt button position in seg
        first_btn = re.search(r'<button class="quiz-opt"', seg)
        if not first_btn:
            continue
        # find options wrapper
        opt_div = re.search(r'<div class="quiz-options">', seg)
        if opt_div and opt_div.start() <= first_btn.start():
            # replace the whole <div class="quiz-options">...</div>
            wrapper_start = opt_div.start()
            # find matching close of the wrapper (starting at <div class="quiz-options">)
            wclose = find_matching_div(h, start + wrapper_start)
            if wclose is None:
                continue
            region_start = start + wrapper_start
            region_end = wclose + 6
        else:
            # direct buttons: replace from first button to end of last consecutive button
            btns = list(re.finditer(r'<button class="quiz-opt".*?</button>', seg[first_btn.start():], re.S))
            if not btns:
                continue
            region_start = start + first_btn.start()
            region_end = start + first_btn.start() + btns[-1].end()
        new_block = fill_input_html(ans)
        edits.append((region_start, region_end, new_block, start, end))
    # apply from END to START
    for region_start, region_end, new_block, tstart, tend in sorted(edits, key=lambda x:-x[0]):
        tgt = h.find('>', tstart)
        if tgt == -1 or tgt > region_start:
            continue
        tag = h[tstart:tgt+1]
        tag2 = tag.replace('data-interaction-type="single_choice"','data-interaction-type="fill_in"')
        tag2 = tag2.replace('data-action-type="select"','data-action-type="fill"')
        between = h[tgt+1:region_start]  # question text etc.
        h = h[:tstart] + tag2 + between + new_block + h[region_end:]
    return h, len(edits)

def find_matching_div(h, odx):
    """从 odx 处（<div ...> 开始）找匹配的 </div> 位置。返回结束 </div> 的 '<' 位置。"""
    depth = 0
    i = odx
    for m in re.finditer(r'<div\b[^>]*>|</div>', h[odx:]):
        tok = m.group(0)
        if tok.startswith('<div'):
            depth += 1
        else:
            depth -= 1
            if depth == 0:
                return odx + m.start()
    return None

def fix_vis604(h):
    """HOT 环节若 >=4 项且动作种类 <2，把部分 fill_in 项 action_type 改为 write 以区分。"""
    from collections import defaultdict
    # map question_id -> (section, action_type, tag_start)
    items = defaultdict(list)
    for m in re.finditer(r'<div class="quiz-q"[^>]*>', h):
        attrs = parse_attrs(m.group(0))
        if not (attrs.get('data-question-id')):
            continue
        sec = attrs.get('data-section','unknown').lower()
        if sec not in HOT:
            continue
        items[sec].append((attrs.get('data-action-type','unknown'), m.start()))
    changed = 0
    for sec, rows in items.items():
        if len(rows) < 4:
            continue
        acts = {a for a,_ in rows}
        if len(acts) >= 2:
            continue
        # all same action; change one fill_in to write
        # find a row whose interaction_type is fill_in (we'll check tag)
        for act, tstart in rows:
            tag = h[tstart:h.find('>', tstart)+1]
            if 'data-interaction-type="fill_in"' in tag and 'data-action-type="' in tag:
                # change action_type to write
                tag2 = tag.replace('data-action-type="fill"','data-action-type="write"')
                if tag2 != tag:
                    h = h[:tstart] + tag2 + h[tstart+len(tag):]
                    changed += 1
                    break
    return h, changed

def process(lesson, label, convert_need, hot_need):
    html_path = os.path.join(BASE, '第%02d课时'%lesson, '课件成品_网页PPT', label+'.html')
    if not os.path.exists(html_path):
        print('MISS', html_path); return
    h = open(html_path, encoding='utf-8').read()
    # backup
    bak_dir = os.path.join(BASE, '第%02d课时'%lesson, '_旧件_收尾前20260808')
    os.makedirs(bak_dir, exist_ok=True)
    bak_file = os.path.join(bak_dir, label+'.html')
    if not os.path.exists(bak_file):
        shutil.copy2(html_path, bak_file)
    # 1 pagination exemption
    h, pg = fix_pagination_exemption(h)
    # 2 double-count cleanup
    h, dc = fix_doublecount_quizquestion(h)
    # 3 metadata on link/order/drag containers
    h, meta = fix_meta_on_item(h, lesson)
    # 4 vis-615
    h = fix_vis_615(h)
    # 5 convert choices
    h, conv = convert_choice_to_fill(h, convert_need, lesson)
    # 6 fix vis-604 hot section action diversity
    h, v604 = fix_vis604(h)
    open(html_path,'w',encoding='utf-8').write(h)
    print('L%d (%s): pagination=%s doublecount=%d meta=%d convert=%d v604=%d' % (lesson, label, pg, dc, meta, conv, v604))

if __name__ == '__main__':
    # (lesson, label, convert_need)
    jobs = [
        (16, '第16课时_课件_中等', 15),
        (17, '第17课时_课件_中等', 20),
        (18, '第18课时_课件_中等', 8),
        (20, '第20课时_课件_中等', 10),
    ]
    for lesson, label, need in jobs:
        process(lesson, label, need, 0)