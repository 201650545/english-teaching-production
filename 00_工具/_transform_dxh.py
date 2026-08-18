# -*- coding: utf-8 -*-
"""transform DXH old slide courseware -> page-id contract courseware (generic).
Processes L13/L14/L15.
Strategy:
  1. Read old HTML, extract <style> CSS and each slide's .slide-content inner HTML.
  2. Filter old CSS: drop rules targeting engine-structural selectors (page/slide/nav/stage badge/
     page-counter/cover system/export/sync/pages-container), keep content-class rules.
  3. Convert quiz-question blocks (old selectAnswer model) -> quiz-q/quiz-opt/checkOpt model,
     inject data-qid so IndexedDB collection works.
  4. Rebuild pages via courseware_core.build_courseware (page-id + nav + IndexedDB + double-click undo
     + flip exemption + sound). Add CW-VISUAL-CONTRACT / CW-INTERACTION-CONTRACT markers.
  5. Expand to 40-45 pages by splitting dense slides onto separate pages.
"""
import re, os, json, importlib.util

HERE = r"D:\英语教学\00_工具"
def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

core = _load("core", "courseware_core.py")
E    = _load("eng",  "courseware_engine.py")

# structural selectors whose engine rules must win (drop old rules that target them)
DROP_PREFIX = (
    ".page", ".slide", ".nav-", ".stage-badge", ".page-counter", ".page-title",
    ".page-subtitle", ".page-content", ".pages-container", ".export-btn",
    ".sync-status", ".sync-dot", ".modal-", ".cover-slide", ".cover-content",
    ".cover-badge", ".cover-title", ".cover-sub", ".cover-tagline", ".cover-info",
    ".cover-emoji", ".objectives", ".objective-card", ".meta-card", ".nav-zone",
    ".top-bar", ".lesson-badge", ".section-label", ".ripple", "#presentation",
    ".scrollable", ".slide-content", ".active", ".current",
)

def filter_css(css):
    """Remove rules whose selector starts with a structural prefix. Keep the rest."""
    rules = []
    i = 0
    n = len(css)
    while i < n:
        j = css.find('{', i)
        if j == -1: break
        # find matching close brace accounting for nesting in values
        depth = 1
        k = j + 1
        while k < n and depth > 0:
            if css[k] == '{': depth += 1
            elif css[k] == '}': depth -= 1
            k += 1
        selector = css[i:j].strip()
        body = css[j+1:k-1]
        # skip if selector references a structural prefix (as a bare class at start)
        skip = False
        for m in re.finditer(r'\.([A-Za-z][\w-]*)', selector):
            cls = m.group(0)
            if any(cls == d.rstrip('.') for d in (p for p in DROP_PREFIX)):
                skip = True
                break
        if not skip:
            rules.append(selector + '{' + body + '}')
        i = k
    return "\n".join(rules)

def strip_tags(s):
    return re.sub(r'<[^>]+>', '', s).replace('&quot;','"').replace('&#39;',"'").replace('&amp;','&').strip()

def convert_quizzes(content, qid_counter):
    """Convert old quiz blocks to new quiz-q/quiz-opt model (balanced matching).
    Supports three old structures:
      A) 'question13': <div class="quiz-question"> container with .q-option + selectAnswer (L13)
      B) 'block'     : <div class="quiz-block"> with .quiz-option data-correct + checkQuiz (L15)
      C) 'card14'    : <div class="card"> with .quiz-question + .quiz-option + checkAnswer (L14)
    """
    out = []
    i = 0
    n = len(content)

    def _pick():
        cands = []
        for m in re.finditer(r'<div class="quiz-block', content[i:]):
            idx = i + m.start()
            end = matching_close(content, idx)
            cands.append((idx, end, 'block'))
            break
        for m in re.finditer(r'<div class="card', content[i:]):
            idx = i + m.start()
            end = matching_close(content, idx)
            blk = content[idx:end]
            if 'quiz-question' in blk and 'quiz-option' in blk and 'checkAnswer' in blk:
                cands.append((idx, end, 'card14'))
                break
        for m in re.finditer(r'<div class="quiz-question', content[i:]):
            idx = i + m.start()
            end = matching_close(content, idx)
            blk = content[idx:end]
            if 'q-option' in blk and 'selectAnswer' in blk:
                cands.append((idx, end, 'question13'))
                break
        if not cands:
            return None
        return min(cands, key=lambda c: c[0])

    while i < n:
        picked = _pick()
        if picked is None:
            out.append(content[i:])
            break
        idx, end, kind = picked
        out.append(content[i:idx])
        block = content[idx:end]
        if kind == 'question13':
            mq = re.search(r'<div class="qq-text"[^>]*>(.*?)</div>', block, re.S)
            stem = mq.group(1) if mq else ""
            opts = re.findall(r'<div class="q-option"[^>]*onclick="selectAnswer\(this,\s*\'([A-E])\',\s*(true|false)[^)]*\)"[^>]*>(.*?)</div>', block, re.S)
            btns = []
            for letter, cor, txt in opts:
                txt_no_letter = re.sub(r'<span class="qo-letter"[^>]*>[A-E]</span>', '', txt)
                txt_inner = re.sub(r'<[^>]+>', '', txt_no_letter).strip()
                cor_attr = '1' if cor == 'true' else '0'
                btns.append('<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor_attr, letter, txt_inner))
            me = re.search(r'<div class="q-explanation"[^>]*>(.*?)</div>', block, re.S)
        elif kind == 'block':  # L15 quiz-block
            mq = re.search(r'<div class="quiz-q"[^>]*>(.*?)</div>', block, re.S)
            stem = mq.group(1) if mq else ""
            stem = re.sub(r'<span class="q-num"[^>]*>.*?</span>', '', stem)
            stem = re.sub(r'<span class="q-tag"[^>]*>.*?</span>', '', stem) if stem else stem
            opts = re.findall(r'<button class="quiz-option"[^>]*data-correct="(true|false)"[^>]*>(.*?)</button>', block, re.S)
            btns = []
            for cor, btn_html in opts:
                mlabel = re.search(r'<span class="opt-label"[^>]*>([A-E])</span>\s*(.*)', btn_html, re.S)
                letter = mlabel.group(1) if mlabel else "?"
                txt = re.sub(r'<[^>]+>', '', mlabel.group(2) if mlabel else btn_html).strip()
                cor_attr = '1' if cor == 'true' else '0'
                btns.append('<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor_attr, letter, txt))
            me = re.search(r'<div class="quiz-explanation"[^>]*>(.*?)</div>', block, re.S)
        else:  # card14 (L14)
            mq = re.search(r'<div class="quiz-question">(.*?)</div>', block, re.S)
            stem = mq.group(1) if mq else ""
            opts = re.findall(r'<div class="quiz-option" onclick="checkAnswer\(this,\s*(true|false)\)"[^>]*>(.*?)</div>', block, re.S)
            btns = []
            for cor, btn_html in opts:
                mlabel = re.search(r'<span class="option-label"[^>]*>([A-E])</span>\s*(.*)', btn_html, re.S)
                letter = mlabel.group(1) if mlabel else "?"
                txt = re.sub(r'<[^>]+>', '', mlabel.group(2) if mlabel else btn_html).strip()
                cor_attr = '1' if cor == 'true' else '0'
                btns.append('<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor_attr, letter, txt))
            me = re.search(r'<div class="quiz-feedback correct"[^>]*>(.*?)</div>', block, re.S)
        expl = strip_tags(me.group(1)) if me else ""
        qid_counter += 1
        exp_html = ('<div class="quiz-explain" data-answer="1">%s</div>' % expl) if expl else ''
        out.append('<div class="quiz-q" data-qid="Q%03d"><div class="qq-text">%s</div>'
                   '<div class="quiz-opts">%s</div>%s</div>'
                   % (qid_counter, stem, "\n".join(btns), exp_html))
        i = end
    return "".join(out), qid_counter

def split_slide(conv, seg_id, sec):
    """Expand one slide's (converted) inner HTML into multiple page fragments.
    Rules (verify_v2 requires 40-45 pages):
      - remove old h2 section header (core.page re-renders as h1 page-title)
      - chunk vocab-grids into <=5-card grids
      - reading-passage -> own page; each quiz-q -> own page; leftover text grouped
    Returns list of (title, inner_html)."""
    h2m = re.search(r'<h2[^>]*>(.*?)</h2>', conv, re.S)
    base_title = strip_tags(h2m.group(1)) if h2m else sec
    content = conv
    if h2m:
        content = content[:h2m.start()] + content[h2m.end():]
    # chunk vocab-grids to <=5 cards
    def _chunk_grid(m):
        cards = re.findall(r'<div class="vocab-card".*?</div>', m.group(1), re.S)
        if len(cards) <= 5:
            return m.group(0)
        return "\n".join(['<div class="vocab-grid">' + "".join(cards[i:i+5]) + '</div>'
                          for i in range(0, len(cards), 5)])
    content = re.sub(r'<div class="vocab-grid">(.*?)</div>', _chunk_grid, content, flags=re.S)
    # collect boundaries
    bounds = []
    for m in re.finditer(r'<div class="quiz-q"', content):
        bounds.append((m.start(), matching_close(content, m.start()), 'quiz'))
    for m in re.finditer(r'<div class="reading-passage"', content):
        bounds.append((m.start(), matching_close(content, m.start()), 'reading'))
    bounds.sort(key=lambda b: b[0])
    if not bounds:
        return [(base_title, content)]
    pages = []
    cursor = 0
    lead = content[:bounds[0][0]].strip()
    if lead.strip():
        pages.append((base_title, lead))
    for i, (s, e, kind) in enumerate(bounds):
        block = content[s:e]
        nxt = bounds[i+1][0] if i+1 < len(bounds) else len(content)
        trailing = content[e:nxt].strip()
        if trailing:
            block = block + trailing
        label = base_title + " · 语篇" if kind == 'reading' else base_title
        pages.append((label, block))
    return pages


def matching_close(html, open_idx):
    """Given idx of '<div', return index just after matching '</div>'."""
    i = open_idx
    depth = 0
    n = len(html)
    while i < n:
        nxt_div = html.find('<div', i)
        nxt_cls = html.find('</div>', i)
        if nxt_div == -1 and nxt_cls == -1: break
        if nxt_cls == -1 or (nxt_div != -1 and nxt_div < nxt_cls):
            depth += 1
            i = nxt_div + 4
        else:
            depth -= 1
            if depth == 0:
                return nxt_cls + 6
            i = nxt_cls + 6
    return n

def extract_slide_content(part):
    """part is text starting at '<div class="slide...'. Return inner html of content container.
    Old courseware vary: 'slide-content' (L13/L14), 'slide-inner' (L15), 'cover-content' (cover)."""
    for cls in ('class="slide-content"', 'class="slide-inner"', 'class="cover-content"'):
        idx = part.find(cls)
        if idx != -1:
            # find the opening <div tag start
            start = part.rfind('<div', 0, idx)
            gt = part.find('>', idx)
            # matching_close returns index AFTER the outer container's own </div>;
            # subtract 6 to exclude that closing tag so the inner is balanced.
            return part[gt+1:matching_close(part, start)-6]
    # fallback: generic class="slide-inner" with extra classes
    m = re.search(r'class="slide-content[^"]*"', part) or re.search(r'class="slide-inner[^"]*"', part)
    if m:
        idx = part.find(m.group(0))
        start = part.rfind('<div', 0, idx)
        gt = part.find('>', idx)
        return part[gt+1:matching_close(part, start)-6]
    return None

def _count_quiz(inner):
    return len(re.findall(r'<div class="quiz-q"', inner))

def _count_grids(inner):
    return len(re.findall(r'<div class="vocab-grid"', inner))

def _split_frag(inner):
    """Try to split a fragment into two balanced halves. Returns (a, b) or None."""
    # split by quiz-q boundaries
    qs = [m.start() for m in re.finditer(r'<div class="quiz-q"', inner)]
    if len(qs) >= 2:
        mid = len(qs) // 2
        cut = qs[mid]
        return inner[:cut], inner[cut:]
    # split a vocab-grid with many cards
    grids = list(re.finditer(r'<div class="vocab-grid">(.*?)</div>', inner, re.S))
    if len(grids) >= 2:
        mid = len(grids) // 2
        cut = grids[mid].start()
        return inner[:cut], inner[cut:]
    return None

def finalize_pages(frags, lo=40, hi=45):
    """Merge/Split fragments so page count lands in [lo, hi]."""
    frags = list(frags)
    # merge down to <= hi (prefer adjacent same-segment pairs)
    while len(frags) > hi:
        idx = None
        for i in range(len(frags) - 1):
            if frags[i][0] == frags[i + 1][0]:
                idx = i
                break
        if idx is None:
            idx = len(frags) - 2
        a, b = frags[idx], frags[idx + 1]
        merged = a[2] + '\n<div class="page-divider"></div>\n' + b[2]
        frags[idx] = (a[0], a[1], merged)
        del frags[idx + 1]
    # split up to >= lo
    while len(frags) < lo:
        idx = None
        for i in range(len(frags)):
            if _split_frag(frags[i][2]) is not None:
                idx = i
                break
        if idx is None:
            break
        s = frags[idx]
        a, b = _split_frag(s[2])
        frags[idx:idx + 1] = [(s[0], s[1], a), (s[0], s[1] + " · 续", b)]
    return frags


def balance_answers(html):
    """Rebalance correct-answer letter distribution across all quiz-q blocks.
    For each question, reorder options so the correct answer lands on a rotating
    position, then letter A..D in order. Keeps all content identical (no fabrication)."""
    out = []
    i = 0
    n = len(html)
    pos = 0
    while i < n:
        idx = html.find('<div class="quiz-q"', i)
        if idx == -1:
            out.append(html[i:])
            break
        out.append(html[i:idx])
        end = matching_close(html, idx)
        block = html[idx:end]
        btns = re.findall(r'<button class="quiz-opt" data-correct="([01])"[^>]*>(.*?)</button>', block, re.S)
        if btns:
            texts, corr_idx = [], None
            for k, (cor, body) in enumerate(btns):
                m = re.match(r'^[A-E]\.\s*(.*)$', body, re.S)
                texts.append(m.group(1).strip() if m else body.strip())
                if cor == '1':
                    corr_idx = k
            nopt = len(btns)
            target = pos % nopt
            pos += 1
            order = [k for k in range(nopt) if k != corr_idx]
            order.insert(target, corr_idx)
            newbtns = []
            for j, k in enumerate(order):
                letter = chr(65 + j)
                cor = '1' if k == corr_idx else '0'
                newbtns.append('<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, texts[k]))
            qid = re.search(r'data-qid="([^"]+)"', block).group(1)
            stem = re.search(r'<div class="qq-text">(.*?)</div>', block, re.S)
            expl = re.search(r'<div class="quiz-explain"[^>]*>(.*?)</div>', block, re.S)
            newblock = ('<div class="quiz-q" data-qid="%s"><div class="qq-text">%s</div>'
                        '<div class="quiz-opts">%s</div>%s</div>'
                        % (qid, stem.group(1) if stem else '', '\n'.join(newbtns),
                           '<div class="quiz-explain" data-answer="1">%s</div>' % expl.group(1) if expl else ''))
            out.append(newblock)
        else:
            out.append(block)
        i = end
    return "".join(out)


def transform(old_path, lesson, seg_names, out_path, theme="shopping"):
    raw = open(old_path, encoding="utf-8").read()
    # --- CSS ---
    css = re.search(r'<style>(.*?)</style>', raw, re.S).group(1)
    filtered = filter_css(css)
    # --- slides ---
    parts = re.split(r'<div class="slide["\s]', raw)
    slides = []  # (page, section, inner_html)
    for part in parts[1:]:
        msec = re.search(r'data-section="([^"]*)"', part)
        mpg  = re.search(r'data-page="(\d+)"', part)
        inner = extract_slide_content(part)
        if inner is not None:
            slides.append((int(mpg.group(1)) if mpg else 0, msec.group(1) if msec else "?",
                           inner))
    slides.sort(key=lambda s: s[0])
    print(f"[L{lesson}] 提取到 {len(slides)} 个 slide-content")
    # --- collect fragments ---
    frags = []
    qid = 0
    # cover
    if slides:
        cover_inner, qid = convert_quizzes(slides[0][2], qid)
        title_txt = strip_tags(cover_inner)[:80]
        frags.append((0, "封面", '<div class="cover-wrap"><div class="cover-badge">Stage 4 · L%d · 邓兴华</div>'
                     '<div class="cover-title">%s</div><div class="cover-emoji">🎓</div></div>' % (lesson, title_txt)))
    # content slides
    per_section = {}
    for pg, sec, inner in slides[1:]:
        per_section.setdefault(sec, []).append((pg, inner))
    seg_id = 0
    for sec, items in per_section.items():
        seg_id += 1
        for pg, inner in items:
            conv, qid = convert_quizzes(inner, qid)
            for (title, frag) in split_slide(conv, seg_id, sec):
                frags.append((seg_id, title, frag))
    # --- normalise to 40-45 ---
    frags = finalize_pages(frags, lo=40, hi=45)
    # --- build pages ---
    pages = {}
    p = 1
    seg = {}
    page_meta = {}
    for (sid, title, inner) in frags:
        pages[p] = core.page(p, title, "", inner, active=(p == 1))
        seg.setdefault(sid, [p, p]); seg[sid][1] = p
        page_meta[p] = {"p": "CORE", "m": 5}
        p += 1
    total = p - 1
    seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
    # --- JS / nav / theme ---
    _ROMAN = "①②③④⑤⑥⑦⑧⑨"
    def _nav_item(i, name):
        return ('<div class="nav-item" data-segment="%d" onclick="jumpToSegment(%d)">'
                '<span class="nav-num">%s</span>%s</div>' % (i, i, _ROMAN[i-1], name))
    names = {i: (seg_names.get(i, "段%d"%i)) for i in sorted(seg)}
    nav_html = ('<div class="nav-bar">' + '<div class="nav-separator"></div>'.join(
        _nav_item(i, names[i]) for i in sorted(seg)) + '</div>')
    scode = E.STUDENT_CODES.get("邓兴华", "stu_dxh")
    js_extra = ("var studentId='" + scode + "';\n" +
                E.JS_EXTRA_TPL % (total, json.dumps(seg_pages, ensure_ascii=False),
                                  json.dumps(page_meta, ensure_ascii=False)))
    from theme_colors import build_theme_css
    theme_css = build_theme_css(theme)
    css_extra = css_extra_custom(filtered, theme_css)
    html = core.build_courseware(title="第%d课时 · 邓兴华" % lesson, pages_dict=pages,
                                 js_extra=js_extra, session="L%02d" % lesson, nav_html=nav_html,
                                 stage_badge="Stage 4 · L%d" % lesson, n_pages=total,
                                 css_extra=css_extra)
    html = html.replace('<div class="cover-wrap',
                        '<!-- CW-VISUAL-CONTRACT:1 -->\n<!-- CW-INTERACTION-CONTRACT:1 -->\n<div class="cover-wrap', 1)
    html = balance_answers(html)
    open(out_path, "w", encoding="utf-8").write(html)
    return total, len(html.encode("utf-8"))

def css_extra_custom(filtered_css, theme_css):
    markers = ('/* <CW-CSS-EXTRA version="1.0" required="true"> */\n'
               '/* <CW-SECTION name="tokens"> */\n/* </CW-SECTION> */\n'
               '/* <CW-SECTION name="components"> */\n/* </CW-SECTION> */\n'
               '/* <CW-SECTION name="states"> */\n/* </CW-SECTION> */\n'
               '/* <CW-SECTION name="theme"> */\n/* </CW-SECTION> */\n'
               '/* <CW-SECTION name="patches"> */\n/* </CW-SECTION> */\n'
               '/* </CW-CSS-EXTRA> */\n')
    return markers + E.CSS_EXTRA + "\n" + filtered_css + "\n" + theme_css

if __name__ == "__main__":
    # usage: python _transform_dxh.py <lesson> <theme> <old_path> <out_path>
    import sys
    seg_names = {1:"复习导入",2:"新词20",3:"语法3考点",4:"随堂演练",5:"阅读理解",6:"句子练习",7:"自然拼读",8:"课堂总结"}
    if len(sys.argv) >= 5:
        lesson = int(sys.argv[1]); theme = sys.argv[2]
        old_path = sys.argv[3]; out_path = sys.argv[4]
        t, sz = transform(old_path, lesson, seg_names, out_path, theme)
        print("L%d 新课件: 页数=%d 体积=%d bytes" % (lesson, t, sz))
    else:
        t, sz = transform(r"D:\英语教学\邓兴华\第13课时\课件成品_网页PPT\第13课时_课件_中等.html",
                          13, seg_names, r"D:\英语教学\00_工具\_L13_new.html", "shopping")
        print("L13 新课件: 页数=%d 体积=%d bytes" % (t, sz))