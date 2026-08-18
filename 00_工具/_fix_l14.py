# -*- coding: utf-8 -*-
"""L14 修复：合并 page42 题2进 page41、重编号、末尾新增 Exit Ticket 页、补 CSS/JS"""
import re, sys

path = r'd:\英语教学\邓兴华\第14课时\课件成品_网页PPT\第14课时_课件_中等.html'
with open(path, encoding='utf-8') as f:
    h = f.read()
orig = h

def check(name, cond):
    print(('PASS' if cond else 'FAIL'), '-', name)
    if not cond:
        sys.exit(1)

# ============ 1. 合并 page42 的题2(quiz-q Q023) 进 page41 ============
# 提取 page42 中的 quiz-q 块
m = re.search(r'(?s)<div class="quiz-q" data-qid="Q023.*?</div></div>', h)
check('定位 Q023 题块', m is not None)
q023 = m.group(0)

# 在 page41 的 Q022 题块结束后插入 Q023
anchor_q022 = '<div class="quiz-explain" data-answer="1">✅ house 的 ou 发 /aʊ/；horse 发 /ɔː/。</div></div>'
check('定位 page41 Q022 结束锚点', anchor_q022 in h)
h = h.replace(anchor_q022, anchor_q022 + '\n' + q023, 1)

# 删除整个 page42 块
pat42 = re.compile(r'(?s)<div class="page" id="page42">.*?(?=\n<div class="page" id="page43">)')
h2, n = pat42.subn('', h)
check('删除 page42 整页', n == 1)
h = h2

# ============ 2. 重编号 page43..45 -> page42..44（用临时标记避免级联） ============
for i in range(43, 46):
    h = h.replace('id="page%d"' % i, 'id="TMPP%d"' % i)
for i in range(43, 46):
    h = h.replace('id="TMPP%d"' % i, 'id="page%d"' % (i - 1))
# PAGE_META 键重编号
for i in range(43, 46):
    h = h.replace('"%d": {"p": "CORE", "m": 5}' % i, '"TMPM%d": {"p": "CORE", "m": 5}' % i)
for i in range(43, 46):
    h = h.replace('"TMPM%d": {"p": "CORE", "m": 5}' % i, '"%d": {"p": "CORE", "m": 5}' % (i - 1))

# ============ 3. 新增 Exit Ticket 页 (page45) ============
exit_html = '''
<div class="page" id="page45">
  <div class="page-content">
    <h1 class="page-title">🎫 Exit Ticket · 出门检测</h1>
    <p class="page-subtitle"></p>
<div class="section-header"><span class="sh-icon">🎫</span></div>
<div class="section-divider"></div>
<div class="card" style="margin-bottom:12px;padding:10px 16px;"><div style="font-size:13px;color:var(--text-secondary);">完成以下检测题，再离开课堂！</div></div>

<div class="quiz-q" data-question-id="L14-EX-01" data-knowledge-id="G37" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="recognition">
<div class="quiz-question">1. She ____ long black hair. (填入 has 或 have)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="has" placeholder="填入 has 或 have"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>主语 she 第三人称单数，用 has 表示拥有。</div>
</div>

<div class="quiz-q" data-question-id="L14-EX-02" data-knowledge-id="G37" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="retrieval">
<div class="quiz-question">2. He ____ tall. (填入 is 或 are)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="is" placeholder="填入 is 或 are"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>描述身高特征用 be 动词，he 第三人称单数用 is。</div>
</div>

<div class="quiz-q" data-question-id="L14-EX-03" data-knowledge-id="G38" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="retrieval">
<div class="quiz-question">3. Why is she happy? ____ she has a new doll. (填入 Because 或 So)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="because" placeholder="填入 Because 或 So"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>why 问原因，用 because 回答。</div>
</div>

<div class="quiz-q" data-question-id="L14-EX-04" data-knowledge-id="G39" data-section="diagnosis" data-template-id="fill_in" data-interaction-type="fill_in" data-action-type="type" data-cognitive-level="application">
<div class="quiz-question">4. 翻译并填空：他有黑色的眼睛。He has ____ ____ eyes. (填入 black 和两个词中合适的颜色词)</div>
<div class="fill-input-wrap"><input type="text" class="fill-input" data-correct="black" placeholder="颜色词"> <button class="interact-btn" onclick="checkFill(this)">检查</button></div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>形容词修饰名词放前面：black eyes 黑眼睛。</div>
</div>

<div class="quiz-q" data-question-id="L14-EX-05" data-knowledge-id="G37" data-section="diagnosis" data-template-id="self_check" data-interaction-type="self_check" data-action-type="reflect" data-cognitive-level="recognition">
<div class="quiz-question">5. 自我评估：今天的内容掌握得怎么样？（点击选项完成自评）</div>
<div class="self-check-row">
<span class="self-check-btn" onclick="selfCheck(this,\'我已掌握 be 动词描述外貌\')">我已掌握 be 动词描述外貌</span>
<span class="self-check-btn" onclick="selfCheck(this,\'我已掌握 have/has 表示拥有\')">我已掌握 have/has 表示拥有</span>
<span class="self-check-btn" onclick="selfCheck(this,\'我已掌握 why/because 因果\')">我已掌握 why/because 因果</span>
<span class="self-check-btn" onclick="selfCheck(this,\'我还需要复习一下\')">我还需要复习一下</span>
</div>
<div class="quiz-feedback"><span class="feedback-label">提示：</span>诚实评估有助于下次复习更高效！</div>
</div>

  </div>
</div>
'''

# 在旧 page45（课堂总结，现为 page44）之后、外层闭合 </div> 之前插入
anchor_tail = '''<div class="nav-zone left" onclick="prevSlide()"><span class="nav-hint">◀</span></div>
  
  </div>
</div>

</div>'''
check('定位页尾插入锚点', anchor_tail in h)
h = h.replace(anchor_tail, '''<div class="nav-zone left" onclick="prevSlide()"><span class="nav-hint">◀</span></div>
  
  </div>
</div>

''' + exit_html + '''
</div>''', 1)

# ============ 4. 补 CSS ============
css_add = '''
.fill-input-wrap{margin:8px 0}
.interact-btn{background:var(--brand);color:#fff;border:none;border-radius:6px;padding:6px 14px;font-size:15px;cursor:pointer;margin-left:6px;}
.interact-btn:hover{opacity:.88}
.self-check-row{display:flex;flex-wrap:wrap;gap:10px;margin:10px 0}
.self-check-btn{display:inline-block;padding:8px 14px;background:#fff;border:2px solid #E5E7EB;border-radius:10px;font-size:15px;cursor:pointer;}
.self-check-btn:hover{border-color:var(--brand);background:var(--brand-light);color:#fff}
.self-check-btn.self-checked{border-color:var(--correct);background:#E7F6EF;color:var(--correct);font-weight:600}
'''
# 插到 .fill-input-wrap 附近（fill-answer 规则之后）
anchor_css = '\n.fill-answer{display:none;font-size:16px;color:var(--correct);font-weight:600;margin-top:4px;}'
check('定位 CSS 锚点', anchor_css in h)
h = h.replace(anchor_css, anchor_css + css_add, 1)

# ============ 5. 补 JS: checkFill / selfCheck ============
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

# ============ 6. 更新导航配置 ============
h = h.replace('var totalPages = 45;', 'var totalPages = 45;')  # 页数不变
h = h.replace('"7": [35, 44], "8": [45, 45]', '"7": [35, 43], "8": [44, 45]')
h = h.replace('<div class="page-counter" id="pageCounter">1 / 45</div>', '<div class="page-counter" id="pageCounter">1 / 45</div>')

# ============ 校验 ============
check('totalPages=45 存在', h.count('var totalPages = 45;') >= 1)
pages = re.findall(r'id="page(\d+)"', h)
check('页数=45', len(pages) == 45)
check('页码连续 1..45', sorted(int(p) for p in pages) == list(range(1, 46)))
check('无 TMPP 残留', 'TMPP' not in h)
check('无 TMPM 残留', 'TMPM' not in h)
check('Exit Ticket 5题存在', h.count('L14-EX-0') >= 5)
check('checkFill 函数存在', 'function checkFill' in h)
check('selfCheck 函数存在', 'function selfCheck' in h)
# div平衡
st = 0
for ln in h.split('\n'):
    st += len(re.findall(r'<div\b', ln)) - len(re.findall(r'</div>', ln))
check('div 平衡', st == 0)

with open(path, 'w', encoding='utf-8') as f:
    f.write(h)
print('OK 已写入，字符数', len(orig), '->', len(h))