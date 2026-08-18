# -*- coding: utf-8 -*-
"""L12 课件交互修复：快闪真召回 + 拖拽真判定(两段式+双击撤销) + 新建Exit Ticket"""
import shutil, os, re, sys

SRC = r"d:\英语教学\邓兴华\第12课时\课件成品_网页PPT\第12课时_课件_中等.html"
BAK = r"d:\英语教学\邓兴华\第12课时\课件成品_网页PPT\_旧件_交互修复前20260811"

def check(label, ok):
    print(("PASS" if ok else "FAIL") + " | " + label)
    if not ok:
        sys.exit("STOP: " + label)

# 1) 备份
os.makedirs(BAK, exist_ok=True)
bakname = os.path.basename(SRC).replace(".html", "_原版.html") if not os.path.exists(os.path.join(BAK, os.path.basename(SRC))) else os.path.basename(SRC)
bakpath = os.path.join(BAK, bakname)
if not os.path.exists(bakpath):
    shutil.copy2(SRC, bakpath)
print("backup ->", bakpath)

with open(SRC, "r", encoding="utf-8") as f:
    h = f.read()

# 2) CSS 快闪：中文默认隐藏 + mf-flipped 显示
css_old = ".mini-flash-item .mf-cn{font-size:11px;color:var(--text-light)}"
css_new = ".mini-flash-item .mf-cn{font-size:11px;color:var(--text-light);display:none}\n.mini-flash-item.mf-flipped .mf-cn{display:block}"
check("CSS mini-flash mf-cn 存在", h.count(css_old) == 1)
h = h.replace(css_old, css_new)

# 3) CSS .picked 高亮（加在 .dd-card.wrong 后）
picked_css = ".dd-card.picked{background:#FEF3C7 !important;border-color:#F59E0B !important;font-weight:600}"
anchor_wrong = ".dd-card.wrong{background:#FEE2E2;border-color:#DC2626}"
check("CSS .dd-card.wrong 存在", h.count(anchor_wrong) == 1)
h = h.replace(anchor_wrong, anchor_wrong + "\n" + picked_css)

# 4) CSS self-check（加在 .quiz-feedback 区后，用 .quiz-q 定义前）
selfcheck_css = (
    ".self-check-row{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0}\n"
    ".self-check-btn{display:inline-block;padding:8px 14px;background:#fff;border:2px solid #E5E7EB;border-radius:10px;font-size:15px;cursor:pointer;transition:var(--transition)}\n"
    ".self-check-btn:hover{border-color:var(--brand);background:var(--brand-light);color:var(--text-white)}\n"
    ".self-check-btn.self-checked{border-color:var(--success,#16A34A);background:#E7F6EF;color:var(--success,#16A34A);font-weight:600}"
)
quizq_css = ".quiz-q{background:var(--card-bg);border-radius:var(--radius-sm);padding:16px;margin:10px 0;box-shadow:var(--card-shadow);border-left:4px solid var(--brand)}"
check("CSS .quiz-q 存在", h.count(quizq_css) == 1)
h = h.replace(quizq_css, selfcheck_css + "\n" + quizq_css)

# 5) flipCard JS 重写：toggle mf-flipped
js_old = """function flipCard(card) {
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  card.style.transform = card.style.transform === 'scale(1.05)' ? '' : 'scale(1.05)';
}"""
js_new = """function flipCard(card) {
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  card.classList.toggle('mf-flipped');
}"""
check("flipCard 原函数唯一", h.count(js_old) == 1)
h = h.replace(js_old, js_new)

# 6) 游戏1（page5 食物分类）卡片 -> pickCard+undoCard
for cat in ["food", "drink", "restaurant"]:
    old = "onclick=\"sortCard(this,'%s')\"" % cat
    new = "onclick=\"pickCard(this)\" ondblclick=\"undoCard(this)\""
    n = h.count(old)
    check("游戏1 卡片 %s 数量" % cat, n >= 1)
    h = h.replace(old, new)

# 7) 游戏1 箱子 -> dropCard
for cat in ["food", "drink", "restaurant"]:
    old = "onclick=\"sortCard(null,'%s')\"" % cat
    new = "onclick=\"dropCard(this,'%s')\"" % cat
    n = h.count(old)
    check("游戏1 箱子 %s 数量" % cat, n >= 1)
    h = h.replace(old, new)

# 8) 游戏2（G31 冠词分类）卡片 -> pickCard2+undoCard
for cat in ["a", "an", "the", "zero"]:
    old = "onclick=\"sortCard(this,'%s')\"" % cat
    new = "onclick=\"pickCard2(this)\" ondblclick=\"undoCard(this)\""
    n = h.count(old)
    check("游戏2 卡片 %s 数量" % cat, n >= 1)
    h = h.replace(old, new)

# 9) 游戏2 箱子 -> dropCard2
for cat in ["a", "an", "the", "zero"]:
    old = "onclick=\"sortCard(null,'%s')\"" % cat
    new = "onclick=\"dropCard2(this,'%s')\"" % cat
    n = h.count(old)
    check("游戏2 箱子 %s 数量" % cat, n >= 1)
    h = h.replace(old, new)

# 10) 替换 sortCard 函数为新两段式 + undoCard
sort_old_start = "// === Sort Card (Drag & Drop alternative: click to sort) ==="
sort_old_end = "// === Export Data ==="
i0 = h.find(sort_old_start)
i1 = h.find(sort_old_end)
check("sortCard 函数块定位", i0 != -1 and i1 != -1 and i0 < i1)
new_funcs = """// === 拖拽分类真判定（两段式：点词选中 -> 点箱判定；答错双击撤销）===
var pendingCard = null;
var pendingCard2 = null;
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
function pickCard2(card) {
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  if (pendingCard2 && pendingCard2 !== card) { pendingCard2.style.background = ''; pendingCard2.classList.remove('picked'); }
  if (pendingCard2 === card) { pendingCard2 = null; card.style.background = ''; card.classList.remove('picked'); var fb = document.getElementById('dd-feedback-g31'); if (fb) { fb.className = 'game-feedback'; fb.innerHTML = ''; } return; }
  pendingCard2 = card; card.style.background = '#FEF3C7'; card.classList.add('picked');
  var fb = document.getElementById('dd-feedback-g31'); if (fb) { fb.className = 'game-feedback show'; fb.innerHTML = '📍 已选中 "' + card.textContent.trim() + '"，请点击对应的冠词区域！'; }
}
function dropCard2(bin, category) {
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  if (!pendingCard2) { var fb = document.getElementById('dd-feedback-g31'); if (fb) { fb.className = 'game-feedback show'; fb.innerHTML = '👆 请先点击一个名词卡片选中，再点击冠词区域！'; } return; }
  var card = pendingCard2; pendingCard2 = null; card.style.background = ''; card.classList.remove('picked');
  var isCorrect = card.getAttribute('data-cat') === category;
  if (isCorrect) { card.classList.add('correct'); playCorrect(); showBubble(true); bin.appendChild(card); }
  else { card.classList.add('wrong'); playError(); showBubble(false); var fb = document.getElementById('dd-feedback-g31'); if (fb) { fb.className = 'game-feedback show wrong'; fb.innerHTML = '❌ 不对哦，再试试！双击卡片可撤销。'; } }
}
function undoCard(card) {
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  if (!card.classList.contains('wrong') && !card.classList.contains('correct')) return;
  card.classList.remove('wrong', 'correct');
  var pool31 = document.getElementById('g31-pool');
  if (pool31 && pool31.contains(card)) {
    pool31.appendChild(card);
    var fb31 = document.getElementById('dd-feedback-g31');
    if (fb31) { fb31.className = 'game-feedback show'; fb31.innerHTML = '↩️ 已撤销，请重新分类。'; }
  } else {
    var pool = document.getElementById('dd-pool');
    if (pool) pool.appendChild(card);
    var fb = document.getElementById('dd-feedback');
    if (fb) { fb.className = 'game-feedback show'; fb.innerHTML = '↩️ 已撤销，请重新分类。'; }
  }
}
// === Self Check (Exit Ticket 自评) ===
function selfCheck(el, label) {
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  var row = el.closest('.self-check-row');
  if (!row) return;
  var btns = row.querySelectorAll('.self-check-btn');
  for (var i = 0; i < btns.length; i++) btns[i].classList.remove('self-checked');
  el.classList.add('self-checked');
  var q = el.closest('.quiz-q');
  if (q) {
    var fb = q.querySelector('.quiz-feedback');
    if (fb) { fb.className = 'quiz-feedback show'; fb.innerHTML = '<span class="feedback-label">已记录：</span>' + label; }
    saveAnswer(q.getAttribute('data-question-id'), label, 1);
  }
}
// === Export Data ==="""
h = h[:i0] + new_funcs + h[i1:]

# 11) 重编号：原 page40/41/42 -> page41/42/43（先改原有，避免冲突）
# 注释
h = h.replace("<!-- ===================== PAGE 40: 课堂总结 ===================== -->", "<!-- ===================== PAGE 41: 课堂总结 ===================== -->")
h = h.replace("<!-- ===================== PAGE 41: 封底 ===================== -->", "<!-- ===================== PAGE 42: 封底 ===================== -->")
h = h.replace("<!-- ===================== PAGE 42: 视觉合同占位（隐藏 div） ===================== -->", "<!-- ===================== PAGE 43: 视觉合同占位（隐藏 div） ===================== -->")
# id（先改 42->43, 41->42, 40->41，新Exit用40）
h = h.replace("id=\"page42\"", "id=\"page43\"")
h = h.replace("id=\"page41\"", "id=\"page42\"")
h = h.replace("id=\"page40\"", "id=\"page41\"")
# 占位页 sh-num 文本
h = h.replace('<span class="sh-num">42</span>', '<span class="sh-num">43</span>')
# 元数据数组注释
h = h.replace("{priority:\"CORE\",estimated_minutes:5},   // P40 课堂总结", "{priority:\"CORE\",estimated_minutes:3},   // P40 Exit Ticket\n{priority:\"CORE\",estimated_minutes:5},   // P41 课堂总结")
h = h.replace("// P41 封底", "// P42 封底")
h = h.replace("// P42 视觉合同占位", "// P43 视觉合同占位")
# SECTION_PAGES 第8节
h = h.replace("var SECTION_PAGES = {1:1, 2:6, 3:13, 4:25, 5:28, 6:31, 7:35, 8:40};", "var SECTION_PAGES = {1:1, 2:6, 3:13, 4:25, 5:28, 6:31, 7:35, 8:41};")
# totalPages
check("totalPages=42 存在", "var totalPages = 42;" in h)
h = h.replace("var totalPages = 42;", "var totalPages = 43;")

# 12) 插入 Exit Ticket 新页（课堂总结 page41 之前）
exit_html = """<!-- ===================== PAGE 40: Exit Ticket ===================== -->
<div class="page" id="page40">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🎫</span> Exit Ticket · 出门检测</div>
<div class="section-header"><span class="sh-icon">✅</span><span class="sh-text">完成以下检测题再离开课堂！</span></div>
<div class="quiz-q" data-question-id="L12-EX-01" data-knowledge-id="G31" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="application">
<div class="quiz-question">1. I'd like ____ orange, please. (填入 a 或 an)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="an" placeholder="填入 a 或 an"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>orange 以元音音素开头，用 an：an orange。</div>
</div>
<div class="quiz-q" data-question-id="L12-EX-02" data-knowledge-id="G32" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="retrieval">
<div class="quiz-question">2. 补全量词：two ____ of bread (填入 piece 或 pieces)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="pieces" placeholder="填入 piece 或 pieces"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>bread 不可数名词，用量词 pieces：two pieces of bread。</div>
</div>
<div class="quiz-q" data-question-id="L12-EX-03" data-knowledge-id="G33" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="retrieval">
<div class="quiz-question">3. Is there ____ milk in the fridge? (填入 some 或 any)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="any" placeholder="填入 some 或 any"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>疑问句一般用 any：Is there any milk?。</div>
</div>
<div class="quiz-q" data-question-id="L12-EX-04" data-knowledge-id="G33" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="application">
<div class="quiz-question">4. Would you like ____ tea? (填入 some 或 any)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="some" placeholder="填入 some 或 any"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>Would you like 表礼貌请求/邀请，用 some：some tea。</div>
</div>
<div class="quiz-q" data-question-id="L12-EX-05" data-knowledge-id="G31" data-section="diagnosis" data-template-id="self_check" data-interaction-type="self_check" data-action-type="reflect" data-cognitive-level="recognition">
<div class="quiz-question">5. 自我评估：今天的内容掌握得怎么样？（点击选项完成自评）</div>
<div class="self-check-row">
<span class="self-check-btn" onclick="selfCheck(this,'我已掌握冠词 a/an/the 用法')">我已掌握冠词 a/an/the 用法</span>
<span class="self-check-btn" onclick="selfCheck(this,'我已掌握可数/不可数量词表达')">我已掌握可数/不可数量词表达</span>
<span class="self-check-btn" onclick="selfCheck(this,'我已掌握 some/any 用法')">我已掌握 some/any 用法</span>
<span class="self-check-btn" onclick="selfCheck(this,'我还需要复习一下')">我还需要复习一下</span>
</div>
<div class="quiz-feedback"><span class="feedback-label">提示：</span>诚实评估有助于下次复习更高效！</div>
</div>
</div>

"""
anchor = "<!-- ===================== PAGE 41: 课堂总结 ===================== -->"
check("课堂总结注释锚点", h.count(anchor) == 1)
h = h.replace(anchor, exit_html + anchor)

# 13) 校验：残留 sortCard 引用应为 0
leftover = re.findall(r"sortCard\([^)]*\)", h)
check("无残留 sortCard 调用", len(leftover) == 0)

# div 平衡校验
opens = h.count("<div")
closes = h.count("</div>")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(h)
print("div opens=%d closes=%d diff=%d" % (opens, closes, opens - closes))
print("totalPages=43:", "var totalPages = 43;" in h)
print("L12 修复完成")