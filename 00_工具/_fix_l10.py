# -*- coding: utf-8 -*-
"""L10 交互修复：快闪真召回 / 拖拽真判定 / 连线错位 / 五选四泄漏 / Exit Ticket 5题"""
import re

P = r"D:\英语教学\邓兴华\第10课时\课件成品_网页PPT\第10课时_课件_中等.html"
h = open(P, encoding="utf-8").read()
orig = h

# ── 1. 快闪真召回：20卡补 onclick + 中文初始隐藏 + flipCard 重写 ──
# 1a. CSS：mf-cn 默认隐藏
css_old = ".mini-flash-item .mf-cn{font-size:11px;color:var(--text-light)}"
css_new = ".mini-flash-item .mf-cn{font-size:11px;color:var(--text-light);display:none}\n.mini-flash-item.mf-flipped .mf-cn{display:block}\n.mini-flash-item.mf-flipped .mf-word{color:var(--brand-dark)}"
assert css_old in h, "CSS mf-cn 未找到"
h = h.replace(css_old, css_new)

# 1b. 快闪页 page3 的 20 张卡补 onclick（仅该页，含 mf-word 且无 onclick 的 mini-flash-item）
def add_onclick(m):
    tag = m.group(0)
    if "onclick" in tag:
        return tag
    return tag.replace('class="mini-flash-item"', 'class="mini-flash-item" onclick="flipCard(this)"')
# 只处理 page3 区域（从 PAGE 3 注释到 PAGE 4 注释之间）
p3_start = h.find("PAGE 3: 复习导入 P2 - 词汇快闪")
p3_end = h.find("PAGE 4:", p3_start)
seg = h[p3_start:p3_end]
seg_new = re.sub(r'<div class="mini-flash-item">', add_onclick, seg)
cnt = len(re.findall(r'class="mini-flash-item" onclick="flipCard\(this\)"', seg_new))
h = h[:p3_start] + seg_new + h[p3_end:]
print("快闪卡 onclick 补全:", cnt, "张")

# 1c. 重写 flipCard 函数（toggle 中文显示）
flip_old = "function flipCard(card) {\n  if(typeof event!=='undefined'&&event)event.stopPropagation();\n  card.style.transform = card.style.transform === 'scale(1.05)' ? '' : 'scale(1.05)';\n}"
flip_new = """function flipCard(card) {
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  card.classList.toggle('mf-flipped');
}"""
assert flip_old in h, "L10 flipCard 函数未找到"
h = h.replace(flip_old, flip_new)
print("flipCard 重写: OK")

# ── 2. 拖拽分类改两段式真判定（pickCard + dropCard）──
# 2a. 卡片 onclick 从 sortCard(this,'x') 改 pickCard(this)
cards = re.findall(r'(<div class="dd-card" data-cat="([^"]+)" onclick="sortCard\(this,\'[^\']+\'\)"[^>]*>)', h)
for full, cat in cards:
    new_tag = full.replace("onclick=\"sortCard(this,'" + cat + "')\"", "onclick=\"pickCard(this)\"")
    h = h.replace(full, new_tag)
print("dd-card 改 pickCard:", len(cards), "张")

# 2b. 箱子 onclick 从空/占位 改为 dropCard(this,'分类')
bins = re.findall(r'(<div class="dd-bin bin-\d" id="bin-([^"]+)"[^>]*onclick="[^"]*"[^>]*>)', h)
for full, bid in bins:
    new_tag = re.sub(r'onclick="[^"]*"', "onclick=\"dropCard(this,'" + bid + "')\"", full)
    h = h.replace(full, new_tag)
print("dd-bin 改 dropCard:", len(bins), "个")

# 2c. 替换 sortCard 函数为 pickCard+dropCard（保留双击撤销）
sc_old_start = h.find("// === Sort Card (Drag & Drop alternative: click to sort) ===")
sc_old_end = h.find("// === Toggle Mind Map Branches ===")
assert sc_old_start != -1 and sc_old_end != -1, "sortCard 段未找到"
new_funcs = """// === Pick Card / Drop Card (two-step: select card, then click bin) ===
var pendingCard = null;
function pickCard(card) {
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  var pool = card.closest('.dd-pool');
  if (pendingCard && pendingCard !== card) {
    pendingCard.style.background = '';
    pendingCard.classList.remove('picked');
  }
  if (pendingCard === card) {
    pendingCard = null;
    card.style.background = '';
    card.classList.remove('picked');
    var fb = document.getElementById('dd-feedback');
    if (fb) { fb.className = 'game-feedback'; fb.innerHTML = ''; }
    return;
  }
  pendingCard = card;
  card.style.background = '#FEF3C7';
  card.classList.add('picked');
  var fb = document.getElementById('dd-feedback');
  if (fb) { fb.className = 'game-feedback show'; fb.innerHTML = '📍 已选中 "' + card.textContent.trim() + '"，请点击对应的分类箱！'; }
}
function dropCard(bin, category) {
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  if (!pendingCard) {
    var fb = document.getElementById('dd-feedback');
    if (fb) { fb.className = 'game-feedback show'; fb.innerHTML = '👆 请先点击一个词汇卡片选中，再点击分类箱！'; }
    return;
  }
  var card = pendingCard;
  pendingCard = null;
  card.style.background = '';
  card.classList.remove('picked');
  var isCorrect = card.getAttribute('data-cat') === category;
  if (isCorrect) {
    card.classList.add('correct');
    playCorrect();
    showBubble(true);
    bin.appendChild(card);
  } else {
    card.classList.add('wrong');
    playError();
    showBubble(false);
    var fb = document.getElementById('dd-feedback');
    if (fb) { fb.className = 'game-feedback show wrong'; fb.innerHTML = '❌ 不对哦，再试试！双击卡片可撤销。'; }
  }
}
"""
h = h[:sc_old_start] + new_funcs + h[sc_old_end:]
print("pickCard/dropCard 函数注入: OK")

# 2d. 答错双击撤销：给 dd-card 补 ondblclick
h = h.replace('class="dd-card" data-cat="', 'class="dd-card" ondblclick="undoCard(this)" data-cat="')
h = h.replace('class="dd-card" ondblclick="undoCard(this)" onclick="pickCard(this)"', 'class="dd-card" ondblclick="undoCard(this)" onclick="pickCard(this)"')
# 注入 undoCard
undo_fn = """
// === Undo Card (double-click a wrong card to return to pool) ===
function undoCard(card) {
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  if (!card.classList.contains('wrong') && !card.classList.contains('correct')) return;
  card.classList.remove('wrong', 'correct');
  var pool = document.querySelector('.dd-pool');
  if (pool) pool.appendChild(card);
  var fb = document.getElementById('dd-feedback');
  if (fb) { fb.className = 'game-feedback show'; fb.innerHTML = '↩️ 已撤销，请重新分类。'; }
}
"""
anchor = "// === Toggle Mind Map Branches ==="
h = h.replace(anchor, undo_fn + "\n" + anchor, 1)
print("undoCard 注入: OK")

# ── 3. 连线错位重排（page11）──
# 左列保持：study(1) answer(2) complete(3) understand(4) practice(5)
# 右列改为：geography(1) the question(2) the exercise(3) the problem(4) the reason(5)
right_old = """<div class="link-right">
<div class="link-item" data-pair="1" onclick="linkClick(this)">the question</div>
<div class="link-item" data-pair="2" onclick="linkClick(this)">the exercise</div>
<div class="link-item" data-pair="3" onclick="linkClick(this)">geography</div>
<div class="link-item" data-pair="4" onclick="linkClick(this)">the problem</div>
<div class="link-item" data-pair="5" onclick="linkClick(this)">the reason</div>
</div>"""
right_new = """<div class="link-right">
<div class="link-item" data-pair="1" onclick="linkClick(this)">geography</div>
<div class="link-item" data-pair="2" onclick="linkClick(this)">the question</div>
<div class="link-item" data-pair="3" onclick="linkClick(this)">the exercise</div>
<div class="link-item" data-pair="4" onclick="linkClick(this)">the problem</div>
<div class="link-item" data-pair="5" onclick="linkClick(this)">the reason</div>
</div>"""
assert right_old in h, "L10 page11 连线右列未找到"
h = h.replace(right_old, right_new)
print("连线重排: OK")

# ── 4. 五选四答案泄漏删除（1342行）──
leak_old = '<div class="tip-box"><div class="tip-title">💡 答案：1-B 2-D 3-A 4-E（C是干扰项）</div><div class="tip-content">C "play games all day" 与学习建议矛盾，是干扰项。</div></div>'
if leak_old in h:
    h = h.replace(leak_old, '<div class="tip-box"><div class="tip-title">💡 解题提示</div><div class="tip-content">C "play games all day" 与学习建议矛盾，是干扰项。</div></div>')
    print("五选四泄漏删除: OK")
else:
    # 兜底：按正则删除含 答案：1-B 的 tip-title
    m = re.search(r'<div class="tip-title">💡 答案：[^<]*</div>', h)
    if m:
        h = h.replace(m.group(0), '<div class="tip-title">💡 解题提示</div>')
        print("五选四泄漏删除(正则): OK")
    else:
        print("五选四泄漏: 未找到，跳过")

# ── 5. Exit Ticket 补第5题（自评）──
# 在 L10-EX-04 题后、page40 闭合前插入自评题
ex4_end = '<div class="quiz-feedback"><span class="feedback-label">解析：</span>nurse /nɜːs/，ur 发 /ɜː/。</div>\n</div>\n</div>'
ex5_new = """<div class="quiz-q" data-question-id="L10-EX-05" data-knowledge-id="G25" data-section="diagnosis" data-template-id="self_check" data-interaction-type="self_check" data-action-type="reflect" data-cognitive-level="recognition">
<div class="quiz-question">5. 自我评估：今天的内容掌握得怎么样？</div>
<div class="self-check-row">
<button class="quiz-opt self-opt" data-correct="1" onclick="checkOpt(this)">我已掌握三单 -s 与 does/doesn't 用法</button>
<button class="quiz-opt self-opt" data-correct="1" onclick="checkOpt(this)">我已掌握学科与学习动作词汇</button>
<button class="quiz-opt self-opt" data-correct="0" onclick="checkOpt(this)">我还需要复习一下</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">提示：</span>诚实评估有助于下次复习更高效！</div>
</div>
</div>"""
assert ex4_end in h, "L10 EX-04 结尾未找到"
h = h.replace(ex4_end, ex4_end + ex5_new, 1)
print("Exit Ticket 补第5题: OK")

# ── 写回 ──
open(P, "w", encoding="utf-8").write(h)
print("L10 写回完成, 大小: %d -> %d" % (len(orig.encode("utf-8")), len(h.encode("utf-8"))))
