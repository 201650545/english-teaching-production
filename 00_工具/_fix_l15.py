# -*- coding: utf-8 -*-
"""L15 修复：删除五选四答案泄漏、末尾新增 Exit Ticket 页(page43)、补 CSS/JS、更新导航"""
import re, sys

path = r'd:\英语教学\邓兴华\第15课时\课件成品_网页PPT\第15课时_课件_中等.html'
with open(path, encoding='utf-8') as f:
    h = f.read()
orig = h

def check(name, cond):
    print(('PASS' if cond else 'FAIL'), '-', name)
    if not cond:
        sys.exit(1)

# ============ 1. 删除五选四答案泄漏行 ============
leak = '<div style="font-size:12px;color:var(--ink-light);margin-top:8px">正确答案：①B ②E ③D ④A（C为干扰项）</div>'
check('定位五选四泄漏行', leak in h)
h = h.replace(leak, '', 1)
check('五选四泄漏已删除', '正确答案：①B ②E' not in h)

# ============ 2. 新增 Exit Ticket 页 (page43) ============
exit_html = '''
<div class="page" id="page43">
  <div class="page-content">
    <h1 class="page-title">🎫 Exit Ticket · 出门检测</h1>
    <p class="page-subtitle"></p>
<div class="section-header"><span class="sh-icon">🎫</span></div>
<div class="section-divider"></div>
<div class="card" style="margin-bottom:12px;padding:10px 16px;"><div style="font-size:13px;color:var(--ink-light);">完成以下检测题，再离开课堂！</div></div>

<div class="quiz-q" data-question-id="L15-EX-01" data-knowledge-id="G40" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="recognition">
<div class="quiz-question">1. ____ the weather like today? (填入 How's 或 What's)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="what's" placeholder="填入 What's 或 How's"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>What's the weather like? = 天气怎么样？like 后接 what 提问。</div>
</div>

<div class="quiz-q" data-question-id="L15-EX-02" data-knowledge-id="G41" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="retrieval">
<div class="quiz-question">2. Could you please ____ the window? (填入 open 或 opening)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="open" placeholder="填入 open 或 opening"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>Could you please + 动词原形：礼貌请求对方做某事。</div>
</div>

<div class="quiz-q" data-question-id="L15-EX-03" data-knowledge-id="G42" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="retrieval">
<div class="quiz-question">3. ____ is seven o'clock. It's time to go home. (填入 It 或 He)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="it" placeholder="填入 It 或 He"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>It 指时间：It's seven o'clock. 现在七点了。</div>
</div>

<div class="quiz-q" data-question-id="L15-EX-04" data-knowledge-id="G40" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="application">
<div class="quiz-question">4. 翻译并填空：今天天气晴朗。____ sunny today. (填入 It's 或 He's)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="it's" placeholder="填入 It's 或 He's"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>It's sunny. 用 It 指代天气。</div>
</div>

<div class="quiz-q" data-question-id="L15-EX-05" data-knowledge-id="G40" data-section="diagnosis" data-template-id="self_check" data-interaction-type="self_check" data-action-type="reflect" data-cognitive-level="recognition">
<div class="quiz-question">5. 自我评估：今天的内容掌握得怎么样？（点击选项完成自评）</div>
<div class="self-check-row">
<span class="self-check-btn" onclick="selfCheck(this,\'我已掌握天气表达\')">我已掌握天气表达</span>
<span class="self-check-btn" onclick="selfCheck(this,\'我已掌握 Could/Would 礼貌请求\')">我已掌握 Could/Would 礼貌请求</span>
<span class="self-check-btn" onclick="selfCheck(this,\'我已掌握非人称 It\')">我已掌握非人称 It</span>
<span class="self-check-btn" onclick="selfCheck(this,\'我还需要复习一下\')">我还需要复习一下</span>
</div>
<div class="quiz-feedback"><span class="feedback-label">提示：</span>诚实评估有助于下次复习更高效！</div>
</div>

  </div>
</div>
'''

# 在 page42 之后、外层闭合 </div> 之前插入。page42 结束于 "</div>\n  </div>\n</div>\n</div><div class=\"page-counter\""
anchor_tail = '</div>\n  </div>\n</div>\n</div><div class="page-counter" id="pageCounter">1 / 42</div>'
check('定位页尾插入锚点', anchor_tail in h)
h = h.replace(anchor_tail, '</div>\n  </div>\n</div>\n' + exit_html + '\n</div><div class="page-counter" id="pageCounter">1 / 43</div>', 1)

# ============ 3. 补 CSS ============
css_add = '''
.fill-input-wrap{margin:8px 0}
.interact-btn{background:var(--brand);color:#fff;border:none;border-radius:6px;padding:6px 14px;font-size:15px;cursor:pointer;margin-left:6px;}
.interact-btn:hover{opacity:.88}
.self-check-row{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0}
.self-check-btn{display:inline-block;padding:8px 14px;background:#fff;border:2px solid #E5E7EB;border-radius:10px;font-size:15px;cursor:pointer;}
.self-check-btn:hover{border-color:var(--brand);background:var(--brand-light);color:#fff}
.self-check-btn.self-checked{border-color:var(--correct);background:#E7F6EF;color:var(--correct);font-weight:600}
'''
anchor_css = '\n.fill-answer{display:none;font-size:16px;color:var(--correct);font-weight:600;margin-top:4px;}'
check('定位 CSS 锚点', anchor_css in h)
h = h.replace(anchor_css, anchor_css + css_add, 1)

# ============ 4. 补 JS: checkFill / selfCheck ============
js_add = '''
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
}
'''
anchor_js = 'function flipCard(el){ el.classList.toggle(\'flipped\'); }'
check('定位 JS 锚点 flipCard', anchor_js in h)
h = h.replace(anchor_js, anchor_js + js_add, 1)

# ============ 5. 更新导航配置 ============
h = h.replace('var totalPages = 42;', 'var totalPages = 43;')
h = h.replace('"8": [41, 42]', '"8": [41, 43]')
# PAGE_META 增加 43 键
h = h.replace('"42": {"p": "CORE", "m": 5}};', '"42": {"p": "CORE", "m": 5}, "43": {"p": "CORE", "m": 5}};')

# ============ 校验 ============
check('totalPages=43 存在', h.count('var totalPages = 43;') >= 1)
pages = re.findall(r'id="page(\d+)"', h)
check('页数=43', len(pages) == 43)
check('页码连续 1..43', sorted(int(p) for p in pages) == list(range(1, 44)))
check('Exit Ticket 5题存在', h.count('L15-EX-0') >= 5)
check('checkFill 函数存在', 'function checkFill' in h)
check('selfCheck 函数存在', 'function selfCheck' in h)
check('无五选四答案泄漏', '正确答案：①B ②E' not in h)
# div平衡
st = 0
for ln in h.split('\n'):
    st += len(re.findall(r'<div\b', ln)) - len(re.findall(r'</div>', ln))
check('div 平衡', st == 0)

with open(path, 'w', encoding='utf-8') as f:
    f.write(h)
print('OK 已写入，字符数', len(orig), '->', len(h))