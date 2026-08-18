# -*- coding: utf-8 -*-
"""L11 交互修复：快闪真召回 / 拖拽真判定(双游戏) / 新建 Exit Ticket"""
import re

P = r"D:\英语教学\邓兴华\第11课时\课件成品_网页PPT\第11课时_课件_中等.html"
h = open(P, encoding="utf-8").read()
orig = h

# ── 1. 快闪真召回：CSS 隐藏中文 + flipCard 重写 ──
css_old = ".mini-flash-item .mf-cn{font-size:11px;color:var(--text-light)}"
css_new = ".mini-flash-item .mf-cn{font-size:11px;color:var(--text-light);display:none}\n.mini-flash-item.mf-flipped .mf-cn{display:block}"
assert css_old in h, "L11 CSS mf-cn 未找到"
h = h.replace(css_old, css_new)

flip_old = "function flipCard(card) { if(typeof event!=='undefined'&&event)event.stopPropagation(); card.style.transform = card.style.transform === 'scale(1.05)' ? '' : 'scale(1.05)'; }"
flip_new = "function flipCard(card) { if(typeof event!=='undefined'&&event)event.stopPropagation(); card.classList.toggle('mf-flipped'); }"
assert flip_old in h, "L11 flipCard 未找到"
h = h.replace(flip_old, flip_new)
print("flipCard 重写: OK")

# ── 2. 拖拽真判定：sortCard → pickCard/dropCard（bin- 前缀）──
# 2a. 卡片：sortCard(this,'x') → pickCard(this)
cards1 = re.findall(r'(<span class="dd-card" data-cat="([^"]+)" onclick="sortCard\(this,\'[^\']+\'\)"[^>]*>)', h)
for full, cat in cards1:
    new_tag = full.replace("onclick=\"sortCard(this,'" + cat + "')\"", "onclick=\"pickCard(this)\"")
    h = h.replace(full, new_tag)
print("sortCard 卡片改 pickCard:", len(cards1))

# 2b. 箱子：bin- 前缀 dd-bin 补 onclick=dropCard
bins1 = re.findall(r'(<div class="dd-bin bin-\d"[^>]*id="bin-([^"]+)"[^>]*>)', h)
for full, bid in bins1:
    if "onclick" in full:
        new_tag = re.sub(r'onclick="[^"]*"', "onclick=\"dropCard(this,'" + bid + "')\"", full)
    else:
        new_tag = full[:-1] + " onclick=\"dropCard(this,'" + bid + "')\">"
    h = h.replace(full, new_tag)
print("bin- 箱子改 dropCard:", len(bins1))

# 2c. sortCard2 卡片：sortCard2(this,'x') → pickCard2(this)
cards2 = re.findall(r'(<span class="dd-card" data-cat="([^"]+)" onclick="sortCard2\(this,\'[^\']+\'\)"[^>]*>)', h)
for full, cat in cards2:
    new_tag = full.replace("onclick=\"sortCard2(this,'" + cat + "')\"", "onclick=\"pickCard2(this)\"")
    h = h.replace(full, new_tag)
print("sortCard2 卡片改 pickCard2:", len(cards2))

# 2d. bin2- 箱子补 onclick=dropCard2
bins2 = re.findall(r'(<div class="dd-bin bin-\d"[^>]*id="bin2-([^"]+)"[^>]*>)', h)
for full, bid in bins2:
    if "onclick" in full:
        new_tag = re.sub(r'onclick="[^"]*"', "onclick=\"dropCard2(this,'" + bid + "')\"", full)
    else:
        new_tag = full[:-1] + " onclick=\"dropCard2(this,'" + bid + "')\">"
    h = h.replace(full, new_tag)
print("bin2- 箱子改 dropCard2:", len(bins2))

# 2e. 替换 sortCard/sortCard2 函数段为两段式（含撤销）
sc_start = h.find("// === Sort Card ===")
sc_end = h.find("// === Mind Map ===")
assert sc_start != -1 and sc_end != -1, "L11 sortCard 段未找到"
new_funcs = """// === Pick Card / Drop Card (two-step sort) ===
var pendingCard = null;
function pickCard(card) {
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  if (pendingCard && pendingCard !== card) { pendingCard.style.background = ''; pendingCard.classList.remove('picked'); }
  if (pendingCard === card) { pendingCard = null; card.style.background = ''; card.classList.remove('picked'); var fb = document.getElementById('dd-feedback'); if (fb) { fb.className = 'game-feedback'; fb.innerHTML = ''; } return; }
  pendingCard = card; card.style.background = '#FEF3C7'; card.classList.add('picked');
  var fb = document.getElementById('dd-feedback'); if (fb) { fb.className = 'game-feedback show'; fb.innerHTML = '📍 已选中 "' + card.textContent.trim() + '"，请点击对应的分类箱！'; }
}
function dropCard(bin, category) {
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  if (!pendingCard) { var fb = document.getElementById('dd-feedback'); if (fb) { fb.className = 'game-feedback show'; fb.innerHTML = '👆 请先点击一个词汇卡片选中，再点击分类箱！'; } return; }
  var card = pendingCard; pendingCard = null; card.style.background = ''; card.classList.remove('picked');
  var isCorrect = card.getAttribute('data-cat') === category;
  if (isCorrect) { card.classList.add('correct'); playCorrect(); showBubble(true); bin.appendChild(card); }
  else { card.classList.add('wrong'); playError(); showBubble(false); var fb = document.getElementById('dd-feedback'); if (fb) { fb.className = 'game-feedback show wrong'; fb.innerHTML = '❌ 不对哦，再试试！双击卡片可撤销。'; } }
}
// === Pick Card 2 / Drop Card 2 (G30 preposition sort) ===
var pendingCard2 = null;
function pickCard2(card) {
  event.stopPropagation();
  if (pendingCard2 && pendingCard2 !== card) { pendingCard2.style.background = ''; pendingCard2.classList.remove('picked'); }
  if (pendingCard2 === card) { pendingCard2 = null; card.style.background = ''; card.classList.remove('picked'); var fb = document.getElementById('dd-feedback2'); if (fb) { fb.className = 'game-feedback'; fb.innerHTML = ''; } return; }
  pendingCard2 = card; card.style.background = '#FEF3C7'; card.classList.add('picked');
  var fb = document.getElementById('dd-feedback2'); if (fb) { fb.className = 'game-feedback show'; fb.innerHTML = '📍 已选中 "' + card.textContent.trim() + '"，请点击对应的介词箱！'; }
}
function dropCard2(bin, category) {
  event.stopPropagation();
  if (!pendingCard2) { var fb = document.getElementById('dd-feedback2'); if (fb) { fb.className = 'game-feedback show'; fb.innerHTML = '👆 请先点击一个时间词卡选中，再点击介词箱！'; } return; }
  var card = pendingCard2; pendingCard2 = null; card.style.background = ''; card.classList.remove('picked');
  var isCorrect = card.getAttribute('data-cat') === category;
  if (isCorrect) { card.classList.add('correct'); playCorrect(); showBubble(true); bin.appendChild(card); }
  else { card.classList.add('wrong'); playError(); showBubble(false); var fb = document.getElementById('dd-feedback2'); if (fb) { fb.className = 'game-feedback show wrong'; fb.innerHTML = '❌ 不对哦，再试试！双击卡片可撤销。'; } }
}
// === Undo Card ===
function undoCard(card) {
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  if (!card.classList.contains('wrong') && !card.classList.contains('correct')) return;
  card.classList.remove('wrong', 'correct');
  var pool = document.getElementById('dd-pool'); if (pool && pool.contains(card)) { }
  var pool2 = document.getElementById('dd-pool2');
  if (card.closest('#dd-pool2') || document.getElementById('dd-pool2').contains(card)) { document.getElementById('dd-pool2').appendChild(card); }
  else { document.getElementById('dd-pool').appendChild(card); }
  var fb = document.getElementById('dd-feedback'); var fb2 = document.getElementById('dd-feedback2');
  if (fb) { fb.className = 'game-feedback show'; fb.innerHTML = '↩️ 已撤销，请重新分类。'; }
}
"""
h = h[:sc_start] + new_funcs + h[sc_end:]
print("两段式函数注入: OK")

# 2f. 卡片补 ondblclick 撤销
# 已处理的卡片再补 ondblclick（若没有）
h = h.replace('class="dd-card" data-cat="', 'class="dd-card" ondblclick="undoCard(this)" data-cat="')
print("卡片 ondblclick 补全: OK")

# ── 3. 新建 Exit Ticket 页（插在 page41 总结页之前）──
exit_page = """<!-- ===================== PAGE 41: Exit Ticket ===================== -->
<div class="page" id="page41">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🎫</span> Exit Ticket · 出门检测</div>
<div class="section-header"><span class="sh-icon">✅</span><span class="sh-text">完成以下检测题再离开课堂！</span></div>
<div class="quiz-q" data-question-id="L11-EX-01" data-knowledge-id="G28" data-section="diagnosis" data-template-id="single_choice" data-interaction-type="single_choice" data-action-type="choose" data-cognitive-level="application">
<div class="quiz-question">1. 你在走廊奔跑，老师应该说：</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">A</span> Don't run in the hallway.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">B</span> You can run here.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Please wear a uniform.</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>mustn't/don't 表禁止，校园里不能奔跑。</div>
</div>
<div class="quiz-q" data-question-id="L11-EX-02" data-knowledge-id="G29" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="retrieval">
<div class="quiz-question">2. 写出下列单词的复数形式：foot → ____；mouse → ____</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="feet, mice" placeholder="用逗号分隔，如 feet, mice"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>foot 变元音→feet；mouse 变元音→mice。</div>
</div>
<div class="quiz-q" data-question-id="L11-EX-03" data-knowledge-id="G30" data-section="diagnosis" data-template-id="single_choice" data-interaction-type="single_choice" data-action-type="choose" data-cognitive-level="application">
<div class="quiz-question">3. I usually play basketball ____ Sunday.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> in</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> on</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> at</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>具体星期几用 on：on Sunday。</div>
</div>
<div class="quiz-q" data-question-id="L11-EX-04" data-knowledge-id="G28" data-section="diagnosis" data-template-id="single_choice" data-interaction-type="single_choice" data-action-type="choose" data-cognitive-level="application">
<div class="quiz-question">4. The library is quiet. We ____ talk loudly.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> can</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> mustn't</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> have to</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>mustn't 表禁止，图书馆禁止大声说话。</div>
</div>
<div class="quiz-q" data-question-id="L11-EX-05" data-knowledge-id="G28" data-section="diagnosis" data-template-id="self_check" data-interaction-type="self_check" data-action-type="reflect" data-cognitive-level="recognition">
<div class="quiz-question">5. 自我评估：今天的内容掌握得怎么样？</div>
<div class="self-check-row">
<button class="quiz-opt self-opt" data-correct="1" onclick="checkOpt(this)">我已掌握 can/must/mustn't 用法</button>
<button class="quiz-opt self-opt" data-correct="1" onclick="checkOpt(this)">我已掌握不规则复数与时间介词</button>
<button class="quiz-opt self-opt" data-correct="0" onclick="checkOpt(this)">我还需要复习一下</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">提示：</span>诚实评估有助于下次复习更高效！</div>
</div>
</div>

"""
# 插在 PAGE 41: 课堂总结 之前
anchor = "<!-- ===================== PAGE 41: 课堂总结 ===================== -->"
assert anchor in h, "L11 课堂总结注释未找到"
h = h.replace(anchor, exit_page + anchor, 1)
print("Exit Ticket 页插入: OK")

# ── 4. 页数自增：page41 总结→page42，page42 占位→page43，pageCounter 更新 ──
# 先处理占位页（page42 隐藏）→ page43
h = h.replace('<!-- ===================== PAGE 42: 视觉合同占位（隐藏 div） ===================== -->',
              '<!-- ===================== PAGE 43: 视觉合同占位（隐藏 div） ===================== -->', 1)
h = h.replace('<div class="page" id="page42" style="display:none !important">',
              '<div class="page" id="page43" style="display:none !important">', 1)
# 原总结页 page41 → page42（注意顺序：先改 page42 占位，再改总结页）
h = h.replace('<!-- ===================== PAGE 41: 课堂总结 ===================== -->\n<div class="page" id="page41">',
              '<!-- ===================== PAGE 42: 课堂总结 ===================== -->\n<div class="page" id="page42">', 1)
# pageCounter
h = h.replace('id="pageCounter">1 / 42<', 'id="pageCounter">1 / 43<')
h = h.replace('id="pageCounter">1 / 41<', 'id="pageCounter">1 / 43<')
print("页数重编号: OK")

open(P, "w", encoding="utf-8").write(h)
print("L11 写回完成, 大小: %d -> %d" % (len(orig.encode("utf-8")), len(h.encode("utf-8"))))
