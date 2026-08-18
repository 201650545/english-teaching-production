# -*- coding: utf-8 -*-
"""L13 课件交互修复：flip-card接线 + 新建Exit Ticket"""
import shutil, os, re, sys

SRC = r"d:\英语教学\邓兴华\第13课时\课件成品_网页PPT\第13课时_课件_中等.html"
BAK = r"d:\英语教学\邓兴华\第13课时\课件成品_网页PPT\_旧件_交互修复前20260811"

def check(label, ok):
    print(("PASS" if ok else "FAIL") + " | " + label)
    if not ok:
        sys.exit("STOP: " + label)

os.makedirs(BAK, exist_ok=True)
bakpath = os.path.join(BAK, os.path.basename(SRC))
if not os.path.exists(bakpath):
    shutil.copy2(SRC, bakpath)
print("backup ->", bakpath)

with open(SRC, "r", encoding="utf-8") as f:
    h = f.read()

# 1) CSS: fill-input-wrap + self-check (插在 .fill-answer.show 后)
css_anchor = ".fill-answer.show{display:block;}"
css_add = ".fill-answer.show{display:block;}\n.fill-input-wrap{margin:8px 0}\n.self-check-row{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0}\n.self-check-btn{display:inline-block;padding:8px 14px;background:#fff;border:2px solid #E5E7EB;border-radius:10px;font-size:15px;cursor:pointer;transition:var(--transition)}\n.self-check-btn:hover{border-color:var(--brand);background:var(--brand-light);color:#fff}\n.self-check-btn.self-checked{border-color:var(--correct);background:#E7F6EF;color:var(--correct);font-weight:600}"
check("CSS .fill-answer.show 锚点", h.count(css_anchor) == 1)
h = h.replace(css_anchor, css_add)

# 2) flip-card 接线：page3 末尾插入易错拼写纠错卡
flip_anchor = """<span class="vg-blank" data-answer="yuan" onclick="vgCheck(this)" ondblclick="vgUndo(this)" data-interaction-type="blank_pick"></span>
</div>
</div>

  </div>
</div>

<div class="page" id="page4">"""
check("page3 掷骰子结束锚点", h.count(flip_anchor) == 1)
flip_html = """<span class="vg-blank" data-answer="yuan" onclick="vgCheck(this)" ondblclick="vgUndo(this)" data-interaction-type="blank_pick"></span>
</div>
</div>

<div class="section-header"><span class="sh-icon">🔄</span></div>
<div class="section-divider"></div>
<div class="card" style="margin-bottom:12px;padding:10px 16px;">
<div class="card-title">🃏 易错拼写 · 点击卡片翻转核对</div>
<div style="font-size:13px;color:var(--text-secondary);">正面是常见错误拼写，点击翻面查看正确拼写！</div>
</div>
<div style="display:grid;grid-template-columns:repeat(5,1fr);gap:10px;">
<div class="flip-card" onclick="flipCard(this)"><div class="flip-card-inner"><div class="flip-card-front"><div class="flip-wrong">✗ desert</div><div class="flip-hint">点击翻面</div></div><div class="flip-card-back"><div class="flip-right">✓ dessert 甜点</div><div class="flip-explain">dessert 有两个 s</div></div></div></div>
<div class="flip-card" onclick="flipCard(this)"><div class="flip-card-inner"><div class="flip-card-front"><div class="flip-wrong">✗ prise</div><div class="flip-hint">点击翻面</div></div><div class="flip-card-back"><div class="flip-right">✓ price 价格</div><div class="flip-explain">price 含 ice</div></div></div></div>
<div class="flip-card" onclick="flipCard(this)"><div class="flip-card-inner"><div class="flip-card-front"><div class="flip-wrong">✗ chang</div><div class="flip-hint">点击翻面</div></div><div class="flip-card-back"><div class="flip-right">✓ change 找零</div><div class="flip-explain">change 含 an</div></div></div></div>
<div class="flip-card" onclick="flipCard(this)"><div class="flip-card-inner"><div class="flip-card-front"><div class="flip-wrong">✗ snak</div><div class="flip-hint">点击翻面</div></div><div class="flip-card-back"><div class="flip-right">✓ snack 零食</div><div class="flip-explain">snack 含 ck</div></div></div></div>
<div class="flip-card" onclick="flipCard(this)"><div class="flip-card-inner"><div class="flip-card-front"><div class="flip-wrong">✗ markt</div><div class="flip-hint">点击翻面</div></div><div class="flip-card-back"><div class="flip-right">✓ market 市场</div><div class="flip-explain">market 含 er</div></div></div></div>
</div>

  </div>
</div>

<div class="page" id="page4">"""
h = h.replace(flip_anchor, flip_html)

# 3) 重编号：原 page45(课堂总结) -> page46
check("原 id=page45 唯一", h.count('id="page45"') == 1)
h = h.replace('id="page45"', 'id="page46"')

# 4) 插入 Exit Ticket 新页（课堂总结 page46 之前，id=page45）
exit_anchor = """<div class="page" id="page46">
  <div class="page-content">
    <h1 class="page-title">课堂总结 · 核心知识点大打卡</h1>"""
check("课堂总结 page46 锚点", h.count(exit_anchor) == 1)
exit_html = """<div class="page" id="page45">
  <div class="page-content">
    <h1 class="page-title">Exit Ticket · 出门检测</h1>
    <p class="page-subtitle"></p>

<div class="section-header"><span class="sh-icon">🎫</span></div>
<div class="section-divider"></div>
<div class="card" style="margin-bottom:12px;padding:10px 16px;"><div style="font-size:13px;color:var(--text-secondary);">完成以下检测题，再离开课堂！</div></div>
<div class="quiz-q" data-question-id="L13-EX-01" data-knowledge-id="G34" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="application">
<div class="quiz-question">1. I'd like ____ buy some bread. (填入 to 或 from)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="to" placeholder="填入 to 或 from"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>would like to do sth.：想要做某事。</div>
</div>
<div class="quiz-q" data-question-id="L13-EX-02" data-knowledge-id="G35" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="retrieval">
<div class="quiz-question">2. ____ sugar do you need? (填入 much 或 many)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="much" placeholder="填入 much 或 many"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>sugar 不可数，用 how much 提问数量。</div>
</div>
<div class="quiz-q" data-question-id="L13-EX-03" data-knowledge-id="G35" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="application">
<div class="quiz-question">3. ____ dumplings would you like? (填入 much 或 many)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="many" placeholder="填入 much 或 many"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>dumplings 可数复数，用 how many 提问数量。</div>
</div>
<div class="quiz-q" data-question-id="L13-EX-04" data-knowledge-id="G36" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="retrieval">
<div class="quiz-question">4. The pancake ____ three yuan. (填入 costs 或 cost)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="costs" placeholder="填入 costs 或 cost"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>cost 主语是物，第三人称单数加 s：The pancake costs 3 yuan。</div>
</div>
<div class="quiz-q" data-question-id="L13-EX-05" data-knowledge-id="G34" data-section="diagnosis" data-template-id="self_check" data-interaction-type="self_check" data-action-type="reflect" data-cognitive-level="recognition">
<div class="quiz-question">5. 自我评估：今天的内容掌握得怎么样？（点击选项完成自评）</div>
<div class="self-check-row">
<span class="self-check-btn" onclick="selfCheck(this,'我已掌握 would like 用法')">我已掌握 would like 用法</span>
<span class="self-check-btn" onclick="selfCheck(this,'我已掌握 how much/how many 提问')">我已掌握 how much/how many 提问</span>
<span class="self-check-btn" onclick="selfCheck(this,'我已掌握价格与货币表达')">我已掌握价格与货币表达</span>
<span class="self-check-btn" onclick="selfCheck(this,'我还需要复习一下')">我还需要复习一下</span>
</div>
<div class="quiz-feedback"><span class="feedback-label">提示：</span>诚实评估有助于下次复习更高效！</div>
</div>

  </div>
</div>

"""
h = h.replace(exit_anchor, exit_html + exit_anchor)

# 5) totalPages 45->46
check("totalPages=45 存在", h.count("var totalPages = 45;") >= 1)
h = h.replace("var totalPages = 45;", "var totalPages = 46;")

# 6) segmentPages 新版第8段
seg_old = '"8": [45, 45]}'
check("segmentPages 新版第8段", h.count(seg_old) == 1)
h = h.replace(seg_old, '"8": [45, 46]}')

# 7) PAGE_META 加 46
meta_old = '"45": {"p": "CORE", "m": 5}};'
check("PAGE_META 45 结尾", h.count(meta_old) == 1)
h = h.replace(meta_old, '"45": {"p": "CORE", "m": 5}, "46": {"p": "CORE", "m": 5}};')

# 8) page-counter 硬编码
counter_old = '>1 / 45</div>'
check("page-counter 1/45", h.count(counter_old) == 1)
h = h.replace(counter_old, '>1 / 46</div>')

# 9) 新增 checkFill + selfCheck 函数（插在 flipCard 函数后）
fc_anchor = "function flipCard(el){ el.classList.toggle('flipped'); }"
check("flipCard 函数锚点", h.count(fc_anchor) == 1)
new_js = fc_anchor + """
// === Exit Ticket: checkFill 填空判题 ===
function checkFill(btn){
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  var wrap = btn.closest('.fill-input-wrap') || btn.parentNode;
  var input = wrap.querySelector('input.fill-input');
  if(!input || input.dataset.done) return;
  var val = input.value.trim().toLowerCase();
  var correct = (input.getAttribute('data-correct')||'').toLowerCase();
  if(!val){ input.focus(); return; }
  input.dataset.done='1';
  var ok = val === correct;
  if(ok){ input.classList.add('correct'); if(typeof playCorrect==='function') playCorrect(); }
  else {
    input.classList.add('wrong'); if(typeof playError==='function') playError();
    var q = input.closest('.quiz-q');
    if(q){ var ans=document.createElement('div'); ans.className='fill-answer show'; ans.textContent='正确答案：'+correct; q.appendChild(ans); }
  }
  var parent = input.closest('[data-question-id]');
  var qid = parent ? parent.getAttribute('data-question-id') : '';
  if(typeof saveAnswer==='function') saveAnswer(qid, val, correct, ok, 1, 0, false);
}
// === Exit Ticket: selfCheck 自评 ===
function selfCheck(el,label){
  if(typeof event!=='undefined'&&event)event.stopPropagation();
  var row = el.closest('.self-check-row'); if(!row) return;
  var btns = row.querySelectorAll('.self-check-btn');
  for(var i=0;i<btns.length;i++) btns[i].classList.remove('self-checked');
  el.classList.add('self-checked');
  var q = el.closest('.quiz-q');
  if(q){
    var fb = q.querySelector('.quiz-feedback');
    if(fb){ fb.className='quiz-feedback show'; fb.innerHTML='<span class="feedback-label">已记录：</span>'+label; }
    var qid = q.getAttribute('data-question-id')||'';
    if(typeof saveAnswer==='function') saveAnswer(qid, label, '', 1, 1, 0, false);
  }
}"""
h = h.replace(fc_anchor, new_js)

# 校验
opens = h.count("<div")
closes = h.count("</div>")
check("flip-card 使用数>=5", h.count('class="flip-card"') >= 5)
check("L13-EX-01..05 存在", all(("L13-EX-0%d" % i) in h for i in range(1,6)))
check("totalPages=46 存在", h.count("var totalPages = 46;") >= 1)

with open(SRC, "w", encoding="utf-8") as f:
    f.write(h)
print("div opens=%d closes=%d diff=%d" % (opens, closes, opens - closes))
print("L13 修复完成")