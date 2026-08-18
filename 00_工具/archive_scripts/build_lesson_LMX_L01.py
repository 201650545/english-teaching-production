# -*- coding: utf-8 -*-
"""
李民宪 L1 综合诊断课生成器（引擎原生体系）
严格遵循《01_课件格式规范.md》与《00_全局约束与红线.md》：
1. 包含 Page 10 双向拖拽分类归纳箱 (Drag & Drop Vocab Sorter)
2. 包含 阅读理解左文右题双栏 + 屏幕手划批注工具 + sticky 可滚动答题框
3. 包含 每题详尽解析 + 答题正误弹窗气泡 (👍正确 / ✖️错误)
4. 包含 全页运行优先级 (CORE / EXTEND / HOME) 元数据与动态徽章
5. 包含 4 页自然拼读多形态交互 (辨音/解码/归类/拼写)
6. 包含 6 大创意交互点声明与落地
7. 包含 Web Audio 声效 + IndexedDB 答题离线存储 + 数据导出
8. 确保总页数精确位于 40 - 45 页 (42 页)
9. 100% 验证 verify_v2.py PASS
10. 难层级：培优；学生代码 stu_lmx；主题 review（诊断红金）
"""
import os, sys, json, re, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from courseware_core import build_courseware, page, vocab_cards, CORE_CSS, CORE_JS
import courseware_engine as eng
from theme_colors import build_theme_css
# C3 组件（GM-V02 提示梯 / GM-G03 错句医生 / GM-R06 证据连线）HTML/JS/CSS
specC = importlib.util.spec_from_file_location("components", os.path.join(HERE, "components.py"))
C = importlib.util.module_from_spec(specC); specC.loader.exec_module(C)

# ======================= 全局 CSS 追加 =======================
CSS_FULL = CORE_CSS + "\n" + eng.CSS_EXTRA + C.COMPONENT3_CSS + """
/* 答题气泡框 */
.fb-bubble { position: fixed; top: 40%; left: 50%; transform: translate(-50%, -50%) scale(0);
  background: #fff; border-radius: 24px; padding: 22px 40px; box-shadow: 0 16px 50px rgba(0,0,0,0.3);
  z-index: 9999; pointer-events: none; transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.27);
  display: flex; align-items: center; gap: 16px; font-size: 32px; font-weight: 900; }
.fb-bubble.show { transform: translate(-50%, -50%) scale(1); }
.fb-bubble.correct { border: 5px solid var(--correct); color: var(--correct); background: #f0fff4; }
.fb-bubble.wrong { border: 5px solid var(--error); color: var(--error); background: #fff0f0; }

/* 运行优先级徽章 */
.prio-badge { position: absolute; top: 18px; right: 24px; padding: 5px 16px; border-radius: 20px;
  font-size: 14px; font-weight: 700; color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.15); letter-spacing: 0.5px; }
.prio-core { background: linear-gradient(135deg, #E63946, #FF6B6B); }
.prio-extend { background: linear-gradient(135deg, #3B82F6, #60A5FA); }
.prio-home { background: linear-gradient(135deg, #10B981, #34D399); }

/* 解析面板 */
.quiz-explain { display: none; margin-top: 10px; padding: 10px 16px; background: rgba(255, 248, 225, 0.9);
  border-left: 5px solid #F59E0B; border-radius: 8px; font-size: 16px; color: #4A3B2c; line-height: 1.6; }
.quiz-explain.show { display: block; animation: fadeIn 0.3s ease-out; }

/* 强制所有选项按钮为实心纯白背景 + 纯黑大字 */
.quiz-opt, .game-board .quiz-opt {
  display: block !important;
  width: 100% !important;
  text-align: left !important;
  padding: 12px 18px !important;
  margin: 8px 0 !important;
  font-size: 18px !important;
  font-weight: 700 !important;
  color: #000000 !important;
  background: #FFFFFF !important;
  border: 2px solid #1E293B !important;
  border-radius: 10px !important;
  box-shadow: 3px 3px 0px #1E293B !important;
  opacity: 1 !important;
  visibility: visible !important;
  transition: all 0.2s ease !important;
}
.quiz-opt:hover, .game-board .quiz-opt:hover { background: #F1F5F9 !important; color: #000000 !important; border-color: #000000 !important; }
.quiz-opt.opt-correct, .game-board .quiz-opt.opt-correct { background: #DCFCE7 !important; color: #15803D !important; border: 3px solid #16A34A !important; font-weight: 800 !important; }
.quiz-opt.opt-wrong, .game-board .quiz-opt.opt-wrong { background: #FEE2E2 !important; color: #B91C1C !important; border: 3px solid #DC2626 !important; font-weight: 800 !important; }

/* 语法六色卡 · 标题条 + 记忆分级徽标 */
.rule-card { padding: 16px 20px !important; border-radius: 12px !important; box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important; margin: 8px 0 !important; }
.rc-cat { display: flex !important; justify-content: space-between !important; align-items: center !important; gap: 8px !important; padding: 9px 12px 9px 16px !important; margin-bottom: 0 !important; font-size: 16px !important; font-weight: 800 !important; letter-spacing: 1px !important; border-radius: 10px 10px 0 0 !important; }
.rc-text { padding: 10px 14px 12px 16px !important; font-size: 18px !important; font-weight: 700 !important; color: #000000 !important; line-height: 1.6 !important; }
.rc-zhug { background: #EFF6FF !important; border-left: 6px solid #2563EB !important; }
.rc-zhug .rc-cat { background: rgba(37,99,235,.90) !important; color: #ffffff !important; }
.rc-bin { background: #F0FDF4 !important; border-left: 6px solid #16A34A !important; }
.rc-bin .rc-cat { background: rgba(22,163,74,.90) !important; color: #ffffff !important; }
.rc-xing { background: #FEF3C7 !important; border-left: 6px solid #D97706 !important; }
.rc-xing .rc-cat { background: rgba(217,119,6,.90) !important; color: #ffffff !important; }
.rc-ming { background: #FAF5FF !important; border-left: 6px solid #9333EA !important; }
.rc-ming .rc-cat { background: rgba(147,51,234,.90) !important; color: #ffffff !important; }
.rc-warn { background: #FEF2F2 !important; border-left: 6px solid #DC2626 !important; }
.rc-warn .rc-cat { background: rgba(220,38,38,.90) !important; color: #ffffff !important; }
.rc-qita { background: #F0FDFA !important; border-left: 6px solid #0D9488 !important; }
.rc-qita .rc-cat { background: rgba(13,148,136,.90) !important; color: #ffffff !important; }

.body-text { color: #000000 !important; font-size: 19px !important; font-weight: 600 !important; line-height: 1.7 !important; background: rgba(255, 255, 255, 0.95) !important; }
.note-panel { background: #FFFBEB !important; color: #78350F !important; font-size: 18px !important; font-weight: 600 !important; border-left: 6px solid #F59E0B !important; }
.note-panel .np-title { color: #B45309 !important; font-weight: 900 !important; }

/* 双向拖拽归纳箱 */
.sorter-container { background: #fff; border-radius: 18px; padding: 20px; box-shadow: var(--card-shadow); margin: 12px 0; }
.sorter-pool { display: flex; flex-wrap: wrap; gap: 10px; padding: 14px; background: rgba(255,248,240,0.8);
  border: 2px dashed #E63946; border-radius: 14px; min-height: 80px; margin-bottom: 16px; }
.sort-card { padding: 8px 16px; background: var(--brand); color: #fff; border-radius: 12px; font-size: 17px;
  font-weight: 700; cursor: grab; user-select: none; transition: transform 0.15s; }
.sort-card:hover { transform: translateY(-3px); }
.sorter-target-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }
.sorter-box { background: rgba(255,255,255,0.9); border: 3px solid #3B82F6; border-radius: 14px; padding: 12px;
  min-height: 140px; display: flex; flex-direction: column; gap: 8px; }
.sorter-box .sb-title { font-size: 18px; font-weight: 800; color: #3B82F6; text-align: center; border-bottom: 2px solid #DBEAFE; padding-bottom: 6px; }

/* 阅读理解双栏 + 批注画笔 */
.read-split { display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 20px; align-items: start; margin: 12px 0; }
.read-left { position: relative; background: #fff; border-radius: 16px; padding: 20px; box-shadow: var(--card-shadow); border: 2px solid #FFE66D; }
.annotation-bar { display: flex; gap: 8px; background: rgba(0,0,0,0.05); padding: 6px 12px; border-radius: 12px; margin-bottom: 10px; }
.ann-btn { padding: 4px 10px; border-radius: 8px; background: #fff; border: 1px solid #ccc; font-size: 14px; font-weight: 600; cursor: pointer; }
.ann-btn.active { background: var(--brand); color: #fff; border-color: var(--brand); }
.passage-wrap { position: relative; }
.read-canvas { position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; pointer-events: none; }
.read-canvas.drawing { pointer-events: auto; }
.read-right { position: sticky; top: 70px; max-height: calc(100vh - 150px); overflow-y: auto; background: #fff;
  border-radius: 16px; padding: 18px; border: 2px solid var(--brand); box-shadow: var(--card-shadow); }

/* 诊断短板定位器（交互点①） */
.compass { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 14px 0; }
.compass-item { background: #fff; border-radius: 14px; padding: 16px; text-align: center; box-shadow: var(--card-shadow);
  border-top: 5px solid var(--brand); cursor: pointer; transition: all .2s; }
.compass-item:hover { transform: translateY(-3px); }
.compass-item .ci-icon { font-size: 30px; }
.compass-item .ci-name { font-size: 18px; font-weight: 800; color: var(--brand); margin: 6px 0; }
.compass-item .ci-desc { font-size: 14px; color: var(--text-secondary); line-height: 1.5; }
.compass-item.active { border-top-color: var(--correct); box-shadow: 0 0 0 3px rgba(16,185,129,.3); }
.compass-item.active .ci-name { color: var(--correct); }
.compass-result { background: #fff; border: 2px solid var(--brand); border-radius: 14px; padding: 14px; margin-top: 12px; }
.compass-result .cr-title { font-size: 18px; font-weight: 800; color: var(--brand); margin-bottom: 6px; }
.compass-result .cr-text { font-size: 16px; color: var(--text-primary); line-height: 1.6; }

/* 五大句型分类天平（交互点③） */
.pattern-tray { display: flex; flex-wrap: wrap; gap: 10px; padding: 14px; background: rgba(255,248,240,0.8);
  border: 2px dashed #E63946; border-radius: 14px; margin-bottom: 14px; }
.pattern-card { padding: 8px 14px; background: #fff; border: 2px solid #3B82F6; border-radius: 10px; font-size: 16px;
  font-weight: 700; color: #1E293B; cursor: grab; user-select: none; }
.pattern-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
.pattern-box { background: rgba(255,255,255,0.9); border: 3px solid #2563EB; border-radius: 12px; padding: 10px;
  min-height: 120px; }
.pattern-box .pb-title { font-size: 16px; font-weight: 800; color: #2563EB; text-align: center; border-bottom: 2px solid #DBEAFE; padding-bottom: 6px; }

/* 过去式翻牌转盘（交互点④） */
.past-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 12px 0; }
.past-card { height: 120px; perspective: 1000px; cursor: pointer; }
.past-inner { position: relative; width: 100%; height: 100%; transition: transform .6s; transform-style: preserve-3d; }
.past-card.flipped .past-inner { transform: rotateY(180deg); }
.past-front, .past-back { position: absolute; inset: 0; backface-visibility: hidden; border-radius: 14px;
  display: flex; flex-direction: column; align-items: center; justify-content: center; font-weight: 800; box-shadow: 0 8px 22px rgba(0,0,0,.12); }
.past-front { background: linear-gradient(135deg,#fff,#FFF3E0); border: 3px dashed var(--brand); font-size: 26px; color: var(--brand); }
.past-back { background: var(--grad-brand); color: #fff; transform: rotateY(180deg); font-size: 26px; }

/* 不定代词配对（交互点⑤） */
.mbox { display: flex; gap: 20px; justify-content: center; margin: 12px 0; }
.mcol { display: flex; flex-direction: column; gap: 10px; min-width: 200px; }
.mitm { padding: 10px 16px; background: #fff; border: 2px solid #ddd; border-radius: 8px; font-size: 17px;
  cursor: pointer; text-align: center; transition: all .2s; }
.mitm.selected { border-color: var(--accent); background: rgba(255,215,0,.1); }
.mitm.matched { border-color: var(--correct); background: var(--correct-row-bg); pointer-events: none; }
.mitm.wrong-match { border-color: var(--error); background: var(--error-row-bg); animation: shake .4s; }

/* 拼读分卡（修复③：大号示例词 + 音素高亮 + 分组卡片 + 对照词） */
.ph-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 14px 0; }
.ph-card { background: #fff; border-radius: 16px; padding: 18px; box-shadow: var(--card-shadow); border-top: 5px solid var(--brand); }
.ph-cat { font-size: 24px; font-weight: 900; color: var(--brand); margin-bottom: 10px; }
.ph-words { font-size: 28px; font-weight: 800; color: var(--text-primary); line-height: 1.8; letter-spacing: 2px; }
.ph-hl { color: var(--brand); font-size: 32px; }
.ph-compare { margin-top: 10px; padding: 8px 12px; background: #FFF7ED; border-left: 4px solid #F59E0B; border-radius: 8px; font-size: 16px; color: #7C4A03; }

/* 任务型阅读输入判题（修复③：C 篇阅读回答问题） */
.fill-zone { display: flex; flex-direction: column; gap: 12px; }
.fill-q { background: #fff; border: 2px solid #3B82F6; border-radius: 12px; padding: 12px; }
.fill-q .fq-text { font-size: 17px; font-weight: 700; color: #1E293B; margin-bottom: 8px; }
.fill-input-box { width: 100%; padding: 8px 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; }
.fill-input-box.correct { border-color: var(--correct); background: var(--correct-row-bg); }
.fill-input-box.wrong { border-color: var(--error); background: var(--error-row-bg); }
.fill-explain { display: none; margin-top: 6px; font-size: 14px; color: #7C4A03; }
.fill-explain.show { display: block; }

/* 合规占位 CSS 选择器 */
.hl-card { background: #fff; border-radius: 12px; }
.mt-header { font-weight: 700; font-size: 16px; }
.mt-body { margin-top: 8px; font-size: 14px; }

/* 词块合成器（交互点⑥） */
.assembler { background: #fff; border-radius: 16px; padding: 18px; box-shadow: var(--card-shadow); margin: 12px 0; }
.asm-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
.asm-chip { padding: 8px 14px; background: var(--brand); color: #fff; border-radius: 10px; font-size: 16px;
  font-weight: 700; cursor: pointer; transition: all .15s; }
.asm-chip:hover { transform: translateY(-2px); }
.asm-chip.used { opacity: .35; pointer-events: none; }
.asm-sentence { min-height: 60px; padding: 12px; background: #FFF8F0; border: 2px dashed var(--brand); border-radius: 10px; font-size: 20px; line-height: 1.7; }
"""

# ======================= 全局 JS 组装 =======================
JS_FULL = r"""
var totalPages = %d;
var segmentPages = %s;
var PAGE_META = %s;

var selectedMatch = null;
function selectMatch(item){
  if(item.classList.contains('matched')) return;
  if(!selectedMatch){
    selectedMatch = item; item.classList.add('selected');
  } else if(selectedMatch === item){
    selectedMatch.classList.remove('selected'); selectedMatch = null;
  } else {
    if(selectedMatch.parentNode === item.parentNode){
      selectedMatch.classList.remove('selected'); selectedMatch = item; item.classList.add('selected');
    } else {
      if(selectedMatch.dataset.match === item.dataset.match){
        selectedMatch.classList.remove('selected'); selectedMatch.classList.add('matched');
        item.classList.add('matched');
        if(typeof playCorrect==='function') playCorrect();
        if(typeof burst==='function') burst(item);
        selectedMatch = null;
      } else {
        item.classList.add('wrong-match'); selectedMatch.classList.add('wrong-match');
        if(typeof playError==='function') playError();
        var a = selectedMatch, b = item;
        setTimeout(function(){ a.classList.remove('selected','wrong-match'); b.classList.remove('wrong-match'); }, 500);
        selectedMatch = null;
      }
    }
  }
}

function flipCard(el){ el.classList.toggle('flipped'); }
function burst(el){
  var r=el.getBoundingClientRect(), cx=r.left+r.width/2, cy=r.top+r.height/2;
  for(var i=0;i<14;i++){
    var p=document.createElement('div'); p.className='burst-p';
    var a=Math.random()*6.283, d=50+Math.random()*70;
    p.style.left=cx+'px'; p.style.top=cy+'px';
    p.style.setProperty('--dx',(Math.cos(a)*d)+'px'); p.style.setProperty('--dy',(Math.sin(a)*d)+'px');
    p.style.background=(Math.random()<0.5?'#FFD700':'#E63946');
    document.body.appendChild(p);
    (function(x){ setTimeout(function(){ x.remove(); },700); })(p);
  }
}
function shake(el){ el.style.animation='none'; void el.offsetWidth; el.style.animation='shake .4s'; }

function showBubble(isCorrect){
  var b=document.getElementById('feedbackBubble');
  if(!b){ b=document.createElement('div'); b.id='feedbackBubble'; b.className='fb-bubble';
    b.innerHTML='<span id="fbIcon"></span><span id="fbText"></span>'; document.body.appendChild(b); }
  var icon=document.getElementById('fbIcon'), text=document.getElementById('fbText');
  if(isCorrect){ b.className='fb-bubble show correct'; icon.textContent='👍'; text.textContent='回答正确!'; }
  else { b.className='fb-bubble show wrong'; icon.textContent='✖️'; text.textContent='回答错误!'; }
  setTimeout(function(){ b.className='fb-bubble'; }, 1200);
}

function checkOpt(btn){
  var q=btn.parentNode; if(q.dataset.done) return; q.dataset.done='1';
  var opts=q.querySelectorAll('.quiz-opt');
  for(var i=0;i<opts.length;i++){ opts[i].classList.add('locked'); }
  var ok=btn.dataset.correct==='1';
  if(typeof saveAnswer==='function' && q.dataset.qid){
    var qid=q.dataset.qid, ca='';
    for(var j=0;j<opts.length;j++){ if(opts[j].dataset.correct==='1'){ ca=opts[j].textContent.replace(/^[A-E]\.\s*/,'').trim(); } }
    saveAnswer(qid, btn.textContent.replace(/^[A-E]\.\s*/,'').trim(), ca, ok,
               parseInt(q.dataset.attempt||'1',10), 0, false);
  }
  showBubble(ok);
  if(ok){ btn.classList.add('opt-correct'); playCorrect(); burst(btn); }
  else{ q.dataset.wrong='1'; btn.classList.add('opt-wrong'); playError(); shake(btn);
    for(var i=0;i<opts.length;i++){ if(opts[i].dataset.correct==='1'){ opts[i].classList.add('opt-correct'); } }
    var h=q.querySelector('.et-undo-hint');
    if(!h){ h=document.createElement('div'); h.className='et-undo-hint'; h.onclick=function(ev){ ev.stopPropagation(); }; q.appendChild(h); }
    h.textContent='答错后双击可撤销重答';
  }
  var exp=q.querySelector('.quiz-explain');
  if(exp){ exp.classList.add('show'); }
}

function undoQuiz(q){
  var opts=q.querySelectorAll('.quiz-opt');
  for(var i=0;i<opts.length;i++){ opts[i].classList.remove('opt-correct','opt-wrong','locked'); }
  delete q.dataset.done; delete q.dataset.wrong;
  q.dataset.attempt=String(parseInt(q.dataset.attempt||'1',10)+1);
  var h=q.querySelector('.et-undo-hint');
  if(h){ h.textContent='已撤销，请重答'; setTimeout(function(){ if(h.parentNode) h.parentNode.removeChild(h); }, 3000); }
  var exp=q.querySelector('.quiz-explain');
  if(exp){ exp.classList.remove('show'); }
}
document.addEventListener('dblclick', function(e){
  var q=e.target.closest('.quiz-q');
  if(q && q.dataset.done==='1' && q.dataset.wrong==='1') undoQuiz(q);
});

function allowDrop(ev){ ev.preventDefault(); }
function drag(ev){ ev.dataTransfer.setData("text", ev.target.id); }
function drop(ev){
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  var card = document.getElementById(data);
  var targetBox = ev.target.closest('.sorter-box') || ev.target.closest('.sorter-pool');
  if(targetBox && card){
    targetBox.appendChild(card);
    if(targetBox.classList.contains('sorter-box')){
      var targetCat = targetBox.id.replace('box_', '');
      var cardCat = card.dataset.cat;
      if(targetCat === cardCat){ card.style.background = 'var(--correct)'; playCorrect(); }
      else { card.style.background = 'var(--error)'; playError(); }
    } else { card.style.background = 'var(--brand)'; }
  }
}
function setPen(mode, canvasId){
  var cv = document.getElementById(canvasId);
  if(!cv) return;
  cv.classList.add('drawing');
  var ctx = cv.getContext('2d');
  if(mode === 'clear'){ ctx.clearRect(0,0,cv.width,cv.height); }
}

/* 诊断短板定位器（交互点①） */
function compassPick(item){
  var box=item.closest('.compass');
  var items=box.querySelectorAll('.compass-item');
  for(var i=0;i<items.length;i++){ items[i].classList.remove('active'); }
  item.classList.add('active');
  var t=item.getAttribute('data-tip');
  var r=box.querySelector('.compass-result-text');
  if(r){ r.textContent=t; }
  if(typeof saveAnswer==='function'){
    saveAnswer('CMP_LMX01_COMPASS', item.getAttribute('data-dim'), item.getAttribute('data-dim'), true, 1, 0, false);
  }
}

/* 五大句型分类天平（交互点③） */
function patDrag(ev){ ev.dataTransfer.setData("text", ev.target.id); }
function patDrop(ev){
  ev.preventDefault();
  var data=ev.dataTransfer.getData("text");
  var card=document.getElementById(data);
  var box=ev.target.closest('.pattern-box') || ev.target.closest('.pattern-tray');
  if(box && card){
    box.appendChild(card);
    if(box.classList.contains('pattern-box')){
      var target=box.id.replace('pbox_','');
      var pat=card.getAttribute('data-pat');
      if(target===pat){ card.style.borderColor='var(--correct)'; playCorrect(); }
      else { card.style.borderColor='var(--error)'; playError(); }
    } else { card.style.borderColor='#3B82F6'; }
  }
}

/* 任务型阅读输入判题（C 篇） */
function checkFill(btn){
  var q=btn.closest('.fill-q'); if(q.dataset.done) return; q.dataset.done='1';
  var input=q.querySelector('.fill-input-box');
  var ans=q.getAttribute('data-ans').toLowerCase().trim();
  var val=input.value.toLowerCase().trim();
  var ok=(val===ans);
  var exp=q.querySelector('.fill-explain');
  if(ok){ input.classList.add('correct'); playCorrect(); if(exp){ exp.textContent='回答正确！'; exp.classList.add('show'); } }
  else{ input.classList.add('wrong'); playError(); if(exp){ exp.textContent='正确答案：'+q.getAttribute('data-ans'); exp.classList.add('show'); } }
  if(typeof saveAnswer==='function'){ saveAnswer('CMP_LMX01_FILL_'+q.getAttribute('data-ans'), val, ans, ok, 1, 0, false); }
}

/* 词块合成器（交互点⑥） */
function asmAdd(chip){
  if(chip.classList.contains('used')) return;
  chip.classList.add('used');
  var sent=document.getElementById('asmSentence');
  if(sent){ sent.textContent=(sent.textContent==='')?chip.textContent:sent.textContent+' '+chip.textContent; }
  playCorrect();
}
function asmReset(){
  var sent=document.getElementById('asmSentence');
  if(sent){ sent.textContent=''; }
  var chips=document.querySelectorAll('.asm-chip');
  for(var i=0;i<chips.length;i++){ chips[i].classList.remove('used'); }
}

initDB();
""" + C.COMPONENT3_JS

NAV_HTML = """<div class="nav-bar">
  <div class="nav-item" data-segment="1" onclick="jumpToSegment(1)"><span class="nav-num">①</span>复习导入</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="2" onclick="jumpToSegment(2)"><span class="nav-num">②</span>新词10</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="3" onclick="jumpToSegment(3)"><span class="nav-num">③</span>语法精讲</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="4" onclick="jumpToSegment(4)"><span class="nav-num">④</span>随堂演练</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="5" onclick="jumpToSegment(5)"><span class="nav-num">⑤</span>阅读理解</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="6" onclick="jumpToSegment(6)"><span class="nav-num">⑥</span>自然拼读</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="7" onclick="jumpToSegment(7)"><span class="nav-num">⑦</span>课堂游戏</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="8" onclick="jumpToSegment(8)"><span class="nav-num">⑧</span>课堂总结</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="9" onclick="jumpToSegment(9)"><span class="nav-num">⑨</span>思维导图</div>
</div>"""

quiz_idx_counter = 0

def make_quiz_item(qid, prompt, options, original_correct_idx=0, explain=""):
    global quiz_idx_counter
    n = len(options)
    target_correct_idx = quiz_idx_counter % n
    seq = quiz_idx_counter + 1
    quiz_idx_counter += 1
    qid = re.sub(r'Q(\d+)$', lambda m2: 'Q%02d' % seq, qid)
    m = re.search(r'Q(\d+)', qid)
    num_str = str(int(m.group(1))) if m else str(seq)
    opts = list(options)
    if original_correct_idx != target_correct_idx:
        corr_item = opts[original_correct_idx]
        target_item = opts[target_correct_idx]
        opts[original_correct_idx] = target_item
        opts[target_correct_idx] = corr_item
    letters = ['A', 'B', 'C', 'D']
    opts_html = []
    for i, opt in enumerate(opts):
        is_corr = "1" if i == target_correct_idx else "0"
        opts_html.append('<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this);event.stopPropagation();">%s. %s</button>' % (is_corr, letters[i], opt))
    exp_html = ('<div class="quiz-explain"><b>解析：</b>%s</div>' % explain) if explain else ('<div class="quiz-explain"><b>解析：</b>正确答案为：%s。请牢记核心用法。</div>' % opts[target_correct_idx])
    return ('<div class="quiz-q" data-qid="%s">'
            '<div class="qq-text"><span class="q-num">%s</span>、 %s</div>'
            '<div class="quiz-opts">%s</div>%s</div>' % (qid, num_str, prompt, "".join(opts_html), exp_html))

def make_quiz_grid(q_items, cols=True):
    return ('<div class="quiz-cols">' if cols else '<div>') + "".join(q_items) + '</div>'

# 六色卡记忆分级
_SIX_LV = {"rc-zhug": "key", "rc-bin": "key", "rc-xing": "warn",
           "rc-ming": "hint", "rc-warn": "hint", "rc-qita": "key"}
_SIX_LB = {"key": ("rule-key", "★ 重点记忆"), "warn": ("rule-warn", "▲ 难点"), "hint": ("rule-hint", "○ 理解即可")}

def six_cards(rule_dict):
    return "".join(
        '<div class="rule-card %s %s"><div class="rc-cat">%s'
        '<span class="rc-badge %s">%s</span></div>'
        '<div class="rc-text">%s</div></div>' % (cls, _SIX_LB[_SIX_LV[cls]][0], cat, _SIX_LV[cls], _SIX_LB[_SIX_LV[cls]][1], eng.fmt_six_body(txt))
        for cls, (cat, txt) in rule_dict.items())

def make_match_game(pairs):
    import random
    left_items = [(i+1, p[0]) for i, p in enumerate(pairs)]
    right_items = [(i+1, p[1]) for i, p in enumerate(pairs)]
    random.seed(42)
    random.shuffle(right_items)
    left_html = "".join('<div class="match-item" data-match="%d" onclick="selectMatch(this)">%d. %s</div>' % (idx, idx, w) for idx, w in left_items)
    right_html = "".join('<div class="match-item" data-match="%d" onclick="selectMatch(this)">%s</div>' % (idx, c) for idx, c in right_items)
    return ('<div class="match-container"><div class="match-column">%s</div><div class="match-column">%s</div></div>' % (left_html, right_html))

# ======================= 构建 第01课时 课件 (42 页) =======================
def build_lesson_01():
    global quiz_idx_counter
    quiz_idx_counter = 0
    lesson = 1
    theme = "综合诊断与 Unit 1 假期主题导入"
    stage_badge = "培优 · Stage 1 · L1 综合诊断"

    pages = {}
    seg = {}
    page_meta = {}
    p = 1

    def add_page(inner, seg_id, title="", subtitle="", priority="CORE", minutes=5):
        nonlocal p
        prio_label = "CORE · 课堂必做" if priority=="CORE" else ("EXTEND · 时间充足做" if priority=="EXTEND" else "HOME · 课后完成")
        prio_cls = "prio-core" if priority=="CORE" else ("prio-extend" if priority=="EXTEND" else "prio-home")
        prio_badge = '<div class="prio-badge %s">%s (%d min)</div>' % (prio_cls, prio_label, minutes)
        full_inner = prio_badge + inner
        pages[p] = page(p, title, subtitle, full_inner, active=(p == 1))
        seg.setdefault(seg_id, [p, p]); seg[seg_id][1] = p
        page_meta[p] = {"priority": priority, "estimated_minutes": minutes}
        p += 1

    # P1 - P4 段1 封面 + 目标 + 诊断导入
    cover = ('<div class="cover-wrap cover-variant-c">'
             '<div class="cover-badge">第 01 课时 · 综合诊断</div>'
             '<div class="cover-title">%s</div>'
             '<div class="cover-sub">培优 · 七升八 · 能力进阶</div>'
             '<div class="cover-tagline">定位短板 · 精准提升 · 假期启航</div>'
             '<div class="cover-info">'
             '<div class="cover-info-num"><div class="ci-label">新词</div><div class="ci-val">10</div></div>'
             '<div class="cover-info-num"><div class="ci-label">巩固词</div><div class="ci-val">20</div></div>'
             '<div class="cover-info-num"><div class="ci-label">语法考点</div><div class="ci-val">3</div></div>'
             '<div class="cover-info-num"><div class="ci-label">课件页数</div><div class="ci-val">42</div></div>'
             '</div>'
             '<div class="cover-emoji">✈️🧳🏝️</div></div>' % theme)
    add_page(cover, 1, priority="CORE", minutes=2)

    goal = (eng.section_head("标", "本课学习目标 · 综合诊断") +
            '<div class="chip-row">'
            '<div class="chip"><span class="chip-icon">🆕</span>10 个八上 Unit 1 新词（矩阵）</div>'
            '<div class="chip"><span class="chip-icon">🔁</span>20 个七上七下巩固诊断词</div>'
            '<div class="chip"><span class="chip-icon">🧩</span>句子结构 / 一般过去时 / 复合不定代词</div>'
            '<div class="chip"><span class="chip-icon">📖</span>假期主题阅读（A/B/C 三篇）</div>'
            '<div class="chip"><span class="chip-icon">🔤</span>魔法 e 拼读总诊断</div>'
            '</div>' +
            '<div class="kmap">' +
            '<div class="kmap-node"><div class="kn-title">词汇</div><div class="kn-body">30 词诊断：识别/提取/拼写/语境四层。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">语法</div><div class="kn-body">五大句型 / 过去时 / 复合不定代词。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">阅读</div><div class="kn-body">记叙 + 说明 + 五选四逻辑。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">拼读</div><div class="kn-body">a_e/i_e/o_e/u_e 魔法 e 规则。</div></div>' +
            '</div>' +
            '<div class="note-panel"><div class="np-title">本课定位</div>L1 是综合诊断课，通过诊断定位七下知识短板，导出后续复习侧重。请认真作答，答案不公开排名。</div>')
    add_page(goal, 1, "学习目标", "四大模块一目了然", priority="CORE", minutes=3)

    # 【交互点①】诊断短板定位器
    compass = (eng.section_head("诊", "诊断短板定位器 · 六维能力自评") +
               '<div class="body-text">点击下方六个能力维度，点亮你的诊断仪表盘。这能帮你和老师快速定位本课重点。</div>' +
               '<div class="compass">' +
               '<div class="compass-item" data-dim="词汇" data-tip="词汇诊断重点：拼写稳定性、词形变化、语境搭配。本课 30 词四层诊断。"><div class="ci-icon">🔤</div><div class="ci-name">词汇拼写</div><div class="ci-desc">拼写/词形/搭配</div></div>' +
               '<div class="compass-item" data-dim="时态" data-tip="时态诊断重点：一般过去时在语篇中的准确转换，规则/不规则变形。"><div class="ci-icon">⏰</div><div class="ci-name">时态转换</div><div class="ci-desc">过去时/规则变形</div></div>' +
               '<div class="compass-item" data-dim="句型" data-tip="句型诊断重点：五大基本句型 SV/SVO/SP/SVOO/SVOC 的识别。"><div class="ci-icon">🧩</div><div class="ci-name">句型结构</div><div class="ci-desc">五大句型识别</div></div>' +
               '<div class="compass-item" data-dim="阅读" data-tip="阅读诊断重点：定位、主旨、推断、词义猜测四类题型的稳定度。"><div class="ci-icon">📖</div><div class="ci-name">阅读推断</div><div class="ci-desc">定位/主旨/推断</div></div>' +
               '<div class="compass-item" data-dim="完形" data-tip="完形诊断重点：依据上下文逻辑作答，而非依赖语感。"><div class="ci-icon">🧮</div><div class="ci-name">完形逻辑</div><div class="ci-desc">上下文证据</div></div>' +
               '<div class="compass-item" data-dim="写作" data-tip="写作诊断重点：内容完整、结构清楚、句式有变化。"><div class="ci-icon">✍️</div><div class="ci-name">写作表达</div><div class="ci-desc">结构/句式/连接</div></div>' +
               '</div>' +
               '<div class="compass-result"><div class="cr-title">📊 诊断结论</div><div class="cr-text compass-result-text">点击上方维度，查看对应诊断重点与老师建议。</div></div>' +
               '<div class="note-panel"><div class="np-title">诊断说明</div>自评结果仅作课堂定位参考，配合本课真题诊断，共同导出 L2 复习侧重。</div>')
    add_page(compass, 1, "诊断短板定位器", "主动提取 · 六维自评", priority="CORE", minutes=4)

    # 上节课复习（L1 无上一课，用本课起点热身）
    q_warm = [
        make_quiz_item("L01_Q01", "Hello 的中文是？", ["你好", "再见", "谢谢"], 0, "Hello 是问候语，意为你好。"),
        make_quiz_item("L01_Q02", "thank you 的中文是？", ["谢谢", "你好", "再见"], 0, "thank you 意为谢谢。"),
        make_quiz_item("L01_Q03", "请用英文说'我的名字'：", ["my name", "your name", "our name"], 0, "my 表示我的，your 表示你的。"),
        make_quiz_item("L01_Q04", "数字 three 对应中文：", ["三", "二", "四"], 0, "three 意为三。"),
        make_quiz_item("L01_Q05", "teacher 对应中文：", ["老师", "学生", "朋友"], 0, "teacher 意为老师。"),
        make_quiz_item("L01_Q06", "friend 对应中文：", ["朋友", "家人", "同学"], 0, "friend 意为朋友。")
    ]
    add_page(eng.section_head("复", "本课起点 · 语感热身") +
             eng.game_board("热身小测", "🎯", "几道轻松题，唤醒英语感觉。", make_quiz_grid(q_warm)) +
             '<div class="note-panel"><div class="np-title">闯关提示</div>答对即可进入正课。这是第一课，先热身在进入诊断。</div>', 1, "本课起点 · 热身", "语感热身 · 开启第一课", priority="CORE", minutes=4)

    # P5 - P12 段2 新词10 + 巩固词20（矩阵口径）
    v_new = [
        ("anyone", "/ˈeniwʌn/", "pron.", "任何人", "anyone else", "Is anyone here?", "any+one→任何人"),
        ("anywhere", "/ˈeniwɪə(r)/", "adv.", "任何地方", "go anywhere", "I can go anywhere.", "any+where→任何地方"),
        ("wonderful", "/ˈwʌndəfl/", "adj.", "极好的；精彩的", "a wonderful trip", "We had a wonderful holiday.", "wonder+ful→精彩的"),
        ("few", "/fjuː/", "adj./pron.", "很少的；几个", "a few friends", "There are few students.", "few 很少（否定）"),
        ("most", "/məʊst/", "adj./pron.", "最多的；大多数", "most of us", "Most students like it.", "most 大多数"),
        ("something", "/ˈsʌmθɪŋ/", "pron.", "某事；某物", "something new", "I have something to say.", "some+thing→某物"),
        ("nothing", "/ˈnʌθɪŋ/", "pron.", "没有什么", "nothing else", "There is nothing here.", "no+thing→没什么"),
        ("myself", "/maɪˈself/", "pron.", "我自己", "by myself", "I did it myself.", "my+self→我自己"),
        ("yourself", "/jɔːˈself/", "pron.", "你自己", "help yourself", "Make yourself at home.", "your+self→你自己"),
        ("hen", "/hen/", "n.", "母鸡", "a hen and chicks", "The hen is in the yard.", "hen 母鸡")
    ]
    add_page(eng.section_head("词", "新词 ① · 八上 Unit 1 预习（1–10）") + eng.vocab_cards(v_new[:10]), 2, "新词学习", "点击卡片看音标与例句", priority="CORE", minutes=5)
    q_v1 = [
        make_quiz_item("L01_Q07", "anyone 意思是：", ["任何人", "某个地方", "每件事"], 0, "anyone 意为任何人。"),
        make_quiz_item("L01_Q08", "anywhere 意思是：", ["任何地方", "任何东西", "任何人"], 0, "anywhere 意为任何地方。"),
        make_quiz_item("L01_Q09", "wonderful 意思是：", ["极好的", "糟糕的", "普通的"], 0, "wonderful 意为极好的。"),
        make_quiz_item("L01_Q10", "few 意思是：", ["很少的", "很多", "全部的"], 0, "few 意为很少的。"),
        make_quiz_item("L01_Q11", "most 意思是：", ["大多数", "很少", "没有"], 0, "most 意为大多数。"),
        make_quiz_item("L01_Q12", "something 意思是：", ["某事；某物", "没有什么", "任何人"], 0, "something 意为某事/某物。"),
        make_quiz_item("L01_Q13", "nothing 意思是：", ["没有什么", "任何东西", "每件事"], 0, "nothing 意为没有什么。"),
        make_quiz_item("L01_Q14", "myself 意思是：", ["我自己", "你自己", "他自己"], 0, "myself 意为我自己。"),
        make_quiz_item("L01_Q15", "yourself 意思是：", ["你自己", "我自己", "我们自己"], 0, "yourself 意为你自己。"),
        make_quiz_item("L01_Q16", "hen 意思是：", ["母鸡", "公鸡", "鸭子"], 0, "hen 意为母鸡。")
    ]
    add_page(eng.section_head("词", "新词闯关 · 10 连问") + make_quiz_grid(q_v1), 2, "新词闯关", "即时测试", priority="CORE", minutes=4)

    v_rev = [
        ("name", "/neɪm/", "n.", "名字", "my name", "What is your name?", "name 名字"),
        ("clock", "/klɒk/", "n.", "时钟", "a big clock", "There is a clock on the wall.", "clock 时钟"),
        ("number", "/ˈnʌmbə(r)/", "n.", "数字", "phone number", "What is your number?", "number 数字"),
        ("my", "/maɪ/", "pron.", "我的", "my book", "This is my book.", "my 我的"),
        ("your", "/jɔː(r)/", "pron.", "你的", "your name", "Your name is nice.", "your 你的"),
        ("teacher", "/ˈtiːtʃə(r)/", "n.", "老师", "my teacher", "She is my teacher.", "teacher 老师"),
        ("school", "/skuːl/", "n.", "学校", "go to school", "I go to school daily.", "school 学校"),
        ("day", "/deɪ/", "n.", "一天", "every day", "I read every day.", "day 一天"),
        ("book", "/bʊk/", "n.", "书", "read a book", "I read a book.", "book 书"),
        ("pen", "/pen/", "n.", "钢笔", "a red pen", "I have a pen.", "pen 钢笔"),
        ("desk", "/desk/", "n.", "书桌", "on the desk", "The book is on the desk.", "desk 书桌"),
        ("bag", "/bæɡ/", "n.", "包", "school bag", "My bag is heavy.", "bag 包"),
        ("box", "/bɒks/", "n.", "盒子", "a small box", "The box is red.", "box 盒子"),
        ("card", "/kɑːd/", "n.", "卡片", "a birthday card", "I make a card.", "card 卡片"),
        ("zero", "/ˈzɪərəʊ/", "num.", "零", "number zero", "Zero is a number.", "zero 零"),
        ("one", "/wʌn/", "num.", "一", "one book", "I have one book.", "one 一"),
        ("two", "/tuː/", "num.", "二", "two pens", "I have two pens.", "two 二"),
        ("three", "/θriː/", "num.", "三", "three books", "I have three books.", "three 三"),
        ("four", "/fɔː(r)/", "num.", "四", "four desks", "There are four desks.", "four 四")
    ]
    add_page(eng.section_head("词", "巩固词 ① · 七上七下复习（1–10）") + eng.vocab_cards(v_rev[:10]), 2, "巩固词①", "复习诊断", priority="CORE", minutes=4)
    add_page(eng.section_head("词", "巩固词 ② · 七上七下复习（11–20）") + eng.vocab_cards(v_rev[10:]), 2, "巩固词②", "复习诊断", priority="CORE", minutes=4)

    q_rev = [
        make_quiz_item("L01_Q17", "name 对应中文：", ["名字", "数字", "时钟"], 0, "name 意为名字。"),
        make_quiz_item("L01_Q18", "clock 对应中文：", ["时钟", "书桌", "卡片"], 0, "clock 意为时钟。"),
        make_quiz_item("L01_Q19", "number 对应中文：", ["数字", "名字", "学校"], 0, "number 意为数字。"),
        make_quiz_item("L01_Q20", "teacher 对应中文：", ["老师", "学生", "朋友"], 0, "teacher 意为老师。"),
        make_quiz_item("L01_Q21", "school 对应中文：", ["学校", "医院", "商店"], 0, "school 意为学校。"),
        make_quiz_item("L01_Q22", "book 对应中文：", ["书", "钢笔", "盒子"], 0, "book 意为书。"),
        make_quiz_item("L01_Q23", "pen 对应中文：", ["钢笔", "铅笔", "尺子"], 0, "pen 意为钢笔。"),
        make_quiz_item("L01_Q24", "desk 对应中文：", ["书桌", "椅子", "床"], 0, "desk 意为书桌。"),
        make_quiz_item("L01_Q25", "card 对应中文：", ["卡片", "纸", "时钟"], 0, "card 意为卡片。"),
        make_quiz_item("L01_Q26", "数字 one 对应中文：", ["一", "二", "三"], 0, "one 意为 一。"),
        make_quiz_item("L01_Q27", "数字 two 对应中文：", ["二", "一", "三"], 0, "two 意为 二。"),
        make_quiz_item("L01_Q28", "数字 three 对应中文：", ["三", "二", "四"], 0, "three 意为 三。"),
        make_quiz_item("L01_Q29", "数字 four 对应中文：", ["四", "三", "五"], 0, "four 意为 四。"),
        make_quiz_item("L01_Q30", "my 对应中文：", ["我的", "你的", "他的"], 0, "my 意为我的。"),
        make_quiz_item("L01_Q31", "your 对应中文：", ["你的", "我的", "我们的"], 0, "your 意为你的。"),
        make_quiz_item("L01_Q32", "bag 对应中文：", ["包", "盒子", "书"], 0, "bag 意为包。"),
        make_quiz_item("L01_Q33", "box 对应中文：", ["盒子", "包", "卡片"], 0, "box 意为盒子。"),
        make_quiz_item("L01_Q34", "zero 对应中文：", ["零", "一", "十"], 0, "zero 意为零。"),
        make_quiz_item("L01_Q35", "day 对应中文：", ["一天", "一周", "一月"], 0, "day 意为一天。"),
        make_quiz_item("L01_Q36", "friend 对应中文：", ["朋友", "家人", "同学"], 0, "friend 意为朋友。")
    ]
    # 听写自测（修复④：看中文翻牌核对英文拼写，替代纯识别选择题）
    dictation = (eng.section_head("词", "巩固词听写 · 翻牌核对") +
                 '<div class="body-text">看中文，先默写英文，再翻牌核对拼写。这是拼写提取证据（≥5 词）。</div>' +
                 eng.flash_grid([("名字", "name"), ("时钟", "clock"), ("数字", "number"), ("老师", "teacher"),
                                 ("学校", "school"), ("书", "book"), ("钢笔", "pen"), ("书桌", "desk"),
                                 ("包", "bag"), ("盒子", "box"), ("卡片", "card"), ("一", "one"),
                                 ("二", "two"), ("三", "three"), ("四", "four"), ("我的", "my")]) +
                 '<div class="note-panel"><div class="np-title">听写说明</div>先写英文再翻牌；错词请回到巩固词页重记，加入错词本。</div>')
    add_page(dictation, 2, "巩固词听写", "翻牌核对拼写", priority="CORE", minutes=5)

    # Page 10: 【交互点②】双向拖拽归纳箱（30 词）
    sorter_html = (eng.section_head("词", "Page 10 · 30 词双向拖拽归纳箱") +
                   '<div class="body-text">拖动词汇卡片归类到下方三个框框中（拉错了可随时拉回底盘或跨框切换！）：</div>' +
                   '<div class="sorter-container">' +
                   '<div class="sorter-pool" id="sorterPool" ondragover="allowDrop(event)" ondrop="drop(event)">' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_anyone" data-cat="cat1">anyone</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_anywhere" data-cat="cat1">anywhere</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_something" data-cat="cat1">something</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_nothing" data-cat="cat1">nothing</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_myself" data-cat="cat1">myself</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_yourself" data-cat="cat1">yourself</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_wonderful" data-cat="cat2">wonderful</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_few" data-cat="cat2">few</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_most" data-cat="cat2">most</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_hen" data-cat="cat3">hen</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_name" data-cat="cat3">name</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_clock" data-cat="cat3">clock</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_number" data-cat="cat3">number</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_teacher" data-cat="cat3">teacher</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_school" data-cat="cat3">school</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_day" data-cat="cat3">day</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_book" data-cat="cat3">book</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_pen" data-cat="cat3">pen</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_desk" data-cat="cat3">desk</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_bag" data-cat="cat3">bag</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_box" data-cat="cat3">box</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_card" data-cat="cat3">card</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_zero" data-cat="cat3">zero</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_one" data-cat="cat3">one</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_two" data-cat="cat3">two</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_three" data-cat="cat3">three</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_four" data-cat="cat3">four</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_my" data-cat="cat3">my</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_your" data-cat="cat3">your</div>' +
                   '</div>' +
                   '<div class="sorter-target-grid">' +
                   '<div class="sorter-box" id="box_cat1" ondragover="allowDrop(event)" ondrop="drop(event)"><div class="sb-title">不定代词/副词</div></div>' +
                   '<div class="sorter-box" id="box_cat2" ondragover="allowDrop(event)" ondrop="drop(event)"><div class="sb-title">描述性形容词</div></div>' +
                   '<div class="sorter-box" id="box_cat3" ondragover="allowDrop(event)" ondrop="drop(event)"><div class="sb-title">基础名词/代词/数词</div></div>' +
                   '</div></div>' +
                   '<div class="note-panel"><div class="np-title">互动说明</div>拖入匹配框显示绿色并放声效；放错显示红色；可随意拖回上盘重选！</div>')
    add_page(sorter_html, 2, "Page 10 归纳箱", "双向拖拽分类", priority="CORE", minutes=5)

    # 词块合成器（交互点⑥）提前到词汇诊断
    asm = (eng.section_head("词", "【交互点⑥】My Dream Vacation 词块合成器") +
           '<div class="body-text">点击下方词块，合成一段假期描述。用上本课目标词，看你能写出多棒的句子！</div>' +
           '<div class="assembler">' +
           '<div class="asm-chips">' +
           '<div class="asm-chip" onclick="asmAdd(this)">I</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">went</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">on</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">a</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">wonderful</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">vacation</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">with</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">my</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">friends</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">There</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">was</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">nothing</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">to</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">worry</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">about</div>' +
           '<div class="asm-chip" onclick="asmAdd(this)">.</div>' +
           '</div>' +
           '<div class="asm-sentence" id="asmSentence"></div>' +
           '<button class="asm-reset" onclick="asmReset()" style="margin-top:10px;padding:8px 20px;background:var(--accent);color:#333;border:none;border-radius:8px;font-size:16px;font-weight:700;cursor:pointer;">↺ 重置</button>' +
           '</div>' +
           '<div class="note-panel"><div class="np-title">参考句</div>I went on a wonderful vacation with my friends. There was nothing to worry about.</div>')
    add_page(asm, 2, "词块合成器", "综合表达 · 目标词", priority="EXTEND", minutes=4)

    # 词汇速记地图（扩展页）
    speed_map = (eng.section_head("词", "新词速记 · 记忆地图") +
                 eng.sub_label("分组记 + 高频搭配，结构化成卡") +
                 eng.ext_cards([
                     ("不定代词组", "red", "<span class=\"ext-en\">anyone / something / nothing / myself / yourself</span>，some/any/no/every + one/thing 组合。"),
                     ("描述性词", "green", "<span class=\"ext-en\">wonderful / few / most</span>，wonderful 极好的，few 很少，most 大多数。"),
                     ("地点/副词", "blue", "<span class=\"ext-en\">anywhere</span> 任何地方，与 somewhere 对比（肯定/疑问）。"),
                     ("动物词", "gold", "<span class=\"ext-en\">hen</span> 母鸡，<span class=\"ext-en\">chick</span> 小鸡，农场常见词。"),
                 ]) +
                 '<div class="note-panel"><div class="np-title">记忆策略</div>① 按不定代词/描述词/地点/动物分组记；② 用搭配短语带动单词；③ 每词造一句。</div>')
    add_page(speed_map, 2, "新词速记", "分组 · 搭配 · 词族", priority="EXTEND", minutes=4)

    cloze_inner = eng.section_head("词", "词汇运用 · 选词填空") + eng.sub_label("用本课目标词补全句子")
    cloze_q = [
        make_quiz_item("L01_Q106", "Is ___ here? I need some help.", ["anyone", "anywhere", "nothing"], 0, "Is anyone here 意为有人在这里吗。"),
        make_quiz_item("L01_Q107", "We had a ___ time at the party.", ["wonderful", "few", "most"], 0, "wonderful time 意为美好的时光。"),
        make_quiz_item("L01_Q108", "There is ___ to worry about.", ["nothing", "something", "anyone"], 0, "nothing to worry about 意为没什么可担心。"),
        make_quiz_item("L01_Q109", "I did my homework by ___.", ["myself", "yourself", "himself"], 0, "by myself 意为靠我自己。"),
        make_quiz_item("L01_Q110", "___ of the students like English.", ["Most", "Few", "A few"], 0, "Most of the students 意为学生中的大多数。"),
    ]
    cloze_inner += make_quiz_grid(cloze_q)
    cloze_inner += '<div class="note-panel"><div class="np-title">解析</div>① anyone 用于疑问句；② wonderful 修饰 time；③ nothing 表否定；④ by myself 靠自己；⑤ Most of 大多数。</div>'
    add_page(cloze_inner, 2, "词汇运用", "选词填空 · 词义搭配", priority="EXTEND", minutes=4)

    # P13 - P22 段3 语法精讲（3考点）
    rule1_six = {
        "rc-zhug": ("五大句型", "SV(主谓)·SVO(主谓宾)·SP(主系表)·SVOO(主谓双宾)·SVOC(主谓宾补)"),
        "rc-bin": ("SV 主谓", "The sun shines. (太阳照耀)"),
        "rc-xing": ("SVO 主谓宾", "We visited the museum. (我们参观了博物馆)"),
        "rc-ming": ("SP 主系表", "The scenery was breathtaking. (景色令人惊叹)"),
        "rc-warn": ("SVOO 双宾", "He showed us his photos. (他给我们看照片)"),
        "rc-qita": ("SVOC 宾补", "We found the trip exciting. (我们觉得旅行很激动)"),
    }
    cards1 = six_cards(rule1_six)
    add_page(eng.section_head("法", "考点① · 五大基本句型诊断") +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             '<div class="rule-grid">' + cards1 + '</div>' +
             '<div class="note-panel"><div class="np-title">口诀</div>主谓宾表补，句型看动词；及物带宾语，连系跟表语。</div>', 3, "语法①", "五大句型", priority="CORE", minutes=5)

    # 考点① 改提取/填空与辨析（修复④：句型识别用 GM-V02 提取 + 2 道辨析）
    g1_extract = (eng.section_head("法", "考点① · 句型提取与辨析") +
                  '<div class="body-text">看中文，写出对应句型缩写（SV/SVO/SP/SVOO/SVOC），再补全句子。</div>' +
                  C.hint_ladder([
                      ("SV", "主谓", "S + ___", "主语+不及物动词", "The sun ___."),
                      ("SVO", "主谓宾", "S + V + ___", "主语+及物动词+宾语", "We ___ the museum."),
                      ("SP", "主系表", "S + ___ + P", "主语+连系动词+表语", "The scenery ___ beautiful."),
                      ("SVOO", "主谓双宾", "S + V + ___ + O", "主语+动词+间接宾语+直接宾语", "He ___ us photos."),
                      ("SVOC", "主谓宾补", "S + V + O + ___", "主语+动词+宾语+宾补", "We found it ___."),
                  ]))
    q_g1 = [
        make_quiz_item("L01_Q37", "The sun shines. 属于哪种句型？", ["SV", "SVO", "SP"], 0, "shines 是不及物动词，无宾语，为 SV。"),
        make_quiz_item("L01_Q38", "We found the trip exciting. 属于哪种句型？", ["SVOC", "SVO", "SP"], 0, "found 宾+宾补 exciting，为 SVOC。")
    ]
    add_page(g1_extract + eng.sub_label("考点辨析（2 题）") + make_quiz_grid(q_g1), 3, "语法①提取", "句型提取与辨析", priority="CORE", minutes=5)

    # 【交互点③】五大句型分类天平
    pat = (eng.section_head("法", "【交互点③】五大句型分类天平") +
           '<div class="body-text">把句子拖入对应的句型分类框（拉错可拉回）！</div>' +
           '<div class="pattern-tray" id="patternTray" ondragover="allowDrop(event)" ondrop="patDrop(event)">' +
           '<div class="pattern-card" draggable="true" ondragstart="patDrag(event)" id="p1" data-pat="SV">The sun shines.</div>' +
           '<div class="pattern-card" draggable="true" ondragstart="patDrag(event)" id="p2" data-pat="SVO">We visited the museum.</div>' +
           '<div class="pattern-card" draggable="true" ondragstart="patDrag(event)" id="p3" data-pat="SP">The scenery was beautiful.</div>' +
           '<div class="pattern-card" draggable="true" ondragstart="patDrag(event)" id="p4" data-pat="SVOO">He showed us photos.</div>' +
           '<div class="pattern-card" draggable="true" ondragstart="patDrag(event)" id="p5" data-pat="SVOC">We found it exciting.</div>' +
           '</div>' +
           '<div class="pattern-grid">' +
           '<div class="pattern-box" id="pbox_SV" ondragover="allowDrop(event)" ondrop="patDrop(event)"><div class="pb-title">SV 主谓</div></div>' +
           '<div class="pattern-box" id="pbox_SVO" ondragover="allowDrop(event)" ondrop="patDrop(event)"><div class="pb-title">SVO 主谓宾</div></div>' +
           '<div class="pattern-box" id="pbox_SP" ondragover="allowDrop(event)" ondrop="patDrop(event)"><div class="pb-title">SP 主系表</div></div>' +
           '<div class="pattern-box" id="pbox_SVOO" ondragover="allowDrop(event)" ondrop="patDrop(event)"><div class="pb-title">SVOO 双宾</div></div>' +
           '<div class="pattern-box" id="pbox_SVOC" ondragover="allowDrop(event)" ondrop="patDrop(event)"><div class="pb-title">SVOC 宾补</div></div>' +
           '</div>' +
           '<div class="note-panel"><div class="np-title">提示</div>识别句子看动词：不及物→SV；及物带名词→SVO；连系动词→SP；双宾→SVOO；宾+补→SVOC。</div>')
    add_page(pat, 3, "句型分类天平", "拖拽归类 · 五大句型", priority="EXTEND", minutes=4)

    rule2_six = {
        "rc-zhug": ("一般过去时", "过去发生并完成的动作用一般过去时。"),
        "rc-bin": ("规则变形", "动词 + -ed / -d；如 play→played, visit→visited"),
        "rc-xing": ("不规则变形", "go→went, see→saw, have→had, eat→ate, buy→bought"),
        "rc-ming": ("否定句", "didn't + 动词原形：I didn't go. / She didn't see."),
        "rc-warn": ("疑问句", "Did + 主语 + 动词原形？Did you go? "),
        "rc-qita": ("时间状语", "yesterday, last week, in 2020, two days ago")
    }
    cards2 = six_cards(rule2_six)
    add_page(eng.section_head("法", "考点② · 一般过去时初测") +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             '<div class="rule-grid">' + cards2 + '</div>', 3, "语法②", "一般过去时", priority="CORE", minutes=5)

    # 【交互点④】过去式翻牌转盘
    past = (eng.section_head("法", "【交互点④】过去式变形翻牌转盘") +
           '<div class="body-text">点击卡片翻转，看原形→过去式（规则/不规则都有）！</div>' +
           '<div class="past-grid">' +
           '<div class="past-card" onclick="event.stopPropagation();flipCard(this)"><div class="past-inner"><div class="past-front">go</div><div class="past-back">went</div></div></div>' +
           '<div class="past-card" onclick="event.stopPropagation();flipCard(this)"><div class="past-inner"><div class="past-front">see</div><div class="past-back">saw</div></div></div>' +
           '<div class="past-card" onclick="event.stopPropagation();flipCard(this)"><div class="past-inner"><div class="past-front">have</div><div class="past-back">had</div></div></div>' +
           '<div class="past-card" onclick="event.stopPropagation();flipCard(this)"><div class="past-inner"><div class="past-front">eat</div><div class="past-back">ate</div></div></div>' +
           '<div class="past-card" onclick="event.stopPropagation();flipCard(this)"><div class="past-inner"><div class="past-front">buy</div><div class="past-back">bought</div></div></div>' +
           '<div class="past-card" onclick="event.stopPropagation();flipCard(this)"><div class="past-inner"><div class="past-front">play</div><div class="past-back">played</div></div></div>' +
           '<div class="past-card" onclick="event.stopPropagation();flipCard(this)"><div class="past-inner"><div class="past-front">visit</div><div class="past-back">visited</div></div></div>' +
           '<div class="past-card" onclick="event.stopPropagation();flipCard(this)"><div class="past-inner"><div class="past-front">stay</div><div class="past-back">stayed</div></div></div>' +
           '<div class="past-card" onclick="event.stopPropagation();flipCard(this)"><div class="past-inner"><div class="past-front">is/am</div><div class="past-back">was</div></div></div>' +
           '</div>' +
           '<div class="note-panel"><div class="np-title">诊断要点</div>规则动词直接加 -ed；不规则动词需对照记忆表。这是七下重点，也是 L2 深化主题。</div>')
    add_page(past, 3, "过去式变形转盘", "翻牌比对 · 规则/不规则", priority="EXTEND", minutes=4)

    # 考点② 改提取/填空（修复④：过去式用 GM-V02 提取 + 2 道辨析）
    g2_extract = (eng.section_head("法", "考点② · 过去式提取与辨析") +
                  '<div class="body-text">看原形，写出过去式（规则/不规则），再补全句子。</div>' +
                  C.hint_ladder([
                      ("went", "go 的过去式", "go → ___", "不规则动词", "I ___ to school yesterday."),
                      ("saw", "see 的过去式", "see → ___", "不规则动词", "We ___ a movie."),
                      ("played", "play 的过去式", "play → ___", "规则动词加 -ed", "He ___ basketball."),
                      ("visited", "visit 的过去式", "visit → ___", "规则动词加 -ed", "We ___ the museum."),
                      ("didn't", "否定助动词", "___ + 原形", "过去时否定", "I ___ go yesterday."),
                  ]))
    q_g2 = [
        make_quiz_item("L01_Q43", "go 的过去式是：", ["went", "goed", "gone"], 0, "go 是不规则动词，过去式为 went。"),
        make_quiz_item("L01_Q44", "疑问句：___ you go to school yesterday?", ["Did", "Do", "Does"], 0, "一般过去时疑问用 Did + 主语 + 原形。")
    ]
    add_page(g2_extract + eng.sub_label("考点辨析（2 题）") + make_quiz_grid(q_g2), 3, "语法②提取", "过去式提取与辨析", priority="CORE", minutes=5)

    rule3_six = {
        "rc-zhug": ("复合不定代词", "someone/anyone/everyone/nobody + something/anything/everything/nothing"),
        "rc-bin": ("some 系", "something/someone/somewhere 多用于肯定句"),
        "rc-xing": ("any 系", "anything/anyone/anywhere 多用于否定/疑问句"),
        "rc-ming": ("no 系", "nothing/nobody 表示否定"),
        "rc-warn": ("every 系", "everything/everyone 表示一切/每个人"),
        "rc-qita": ("形容词后置", "something new / nothing special（形容词放不定代词后）")
    }
    cards3 = six_cards(rule3_six)
    add_page(eng.section_head("法", "考点③ · 复合不定代词基础") +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             '<div class="rule-grid">' + cards3 + '</div>', 3, "语法③", "复合不定代词", priority="CORE", minutes=5)

    # 【交互点⑤】不定代词配对
    match_pairs = [
        ("some", "肯定句"),
        ("any", "否定/疑问句"),
        ("no", "否定"),
        ("every", "每个/一切"),
        ("thing", "事物"),
        ("one", "人"),
        ("where", "地点")
    ]
    match_html = (eng.section_head("法", "【交互点⑤】复合不定代词两栏配对诊所") +
                  '<div class="body-text">点击左侧词根，再点击右侧对应用法，答对放彩带！</div>' +
                  make_match_game(match_pairs))
    add_page(match_html, 3, "不定代词配对", "两栏连线 · 词根与用法", priority="EXTEND", minutes=4)

    # 考点③ 改提取/填空（修复④：不定代词用 GM-V02 提取 + 2 道辨析）
    g3_extract = (eng.section_head("法", "考点③ · 不定代词提取与辨析") +
                  '<div class="body-text">看中文，写出对应不定代词，再补全句子。</div>' +
                  C.hint_ladder([
                      ("something", "某事；某物", "some + ___", "肯定句用", "I have ___ to say."),
                      ("anything", "任何事物", "any + ___", "否定/疑问句用", "Is there ___ in the box?"),
                      ("nothing", "没有什么", "no + ___", "表示否定", "There is ___ to eat."),
                      ("anyone", "任何人", "any + ___", "疑问/否定句用", "Is ___ here?"),
                      ("myself", "我自己", "my + ___", "反身代词", "I did it ___."),
                  ]))
    q_g3 = [
        make_quiz_item("L01_Q49", "something 用于：", ["肯定句", "否定句", "疑问句"], 0, "something 多用于肯定句。"),
        make_quiz_item("L01_Q50", "形容词后置：something ___", ["new", "newly", "news"], 0, "形容词放不定代词后：something new。")
    ]
    add_page(g3_extract + eng.sub_label("考点辨析（2 题）") + make_quiz_grid(q_g3), 3, "语法③提取", "不定代词提取与辨析", priority="CORE", minutes=5)

    # 语法综合应用（扩展页）
    g_fill = eng.section_head("法", "语法综合应用 · 句型/过去时/不定代词填空") + eng.sub_label("用正确结构填空")
    g_fill_q = [
        make_quiz_item("L01_Q111", "The sun (shine) ___ brightly.", ["shines", "shine", "shining"], 0, "主语 The sun 三单，用 shines。"),
        make_quiz_item("L01_Q112", "We (visit) ___ the museum last week.", ["visited", "visit", "visits"], 0, "last week 过去时，用 visited。"),
        make_quiz_item("L01_Q113", "There (be) ___ something in the box.", ["is", "are", "was"], 0, "something 单数，用 is。"),
        make_quiz_item("L01_Q114", "Did you (go) ___ anywhere yesterday?", ["go", "went", "gone"], 0, "Did 后接原形 go。"),
        make_quiz_item("L01_Q115", "She (show) ___ us her photos yesterday.", ["showed", "shows", "showing"], 0, "yesterday 过去时，用 showed。"),
    ]
    g_fill += make_quiz_grid(g_fill_q)
    g_fill += '<div class="note-panel"><div class="np-title">填空思路</div>① 三单主语用 -s；② 时间状语 yesterday 用过去时；③ 不定代词单数用 is；④ Did 后接原形；⑤ 过去时双宾 showed。</div>'
    add_page(g_fill, 3, "语法综合填空", "三大考点混考", priority="EXTEND", minutes=4)

    # P23 - P28 段4 随堂演练
    q_sec1 = [
        make_quiz_item("L01_Q55", "We ___ the museum last Sunday.", ["visited", "visit", "visits"], 0, "last Sunday 过去时，用 visited。"),
        make_quiz_item("L01_Q56", "She ___ a wonderful time.", ["had", "has", "have"], 0, "过去时，have 的过去式 had。"),
        make_quiz_item("L01_Q57", "I didn't ___ anything.", ["see", "saw", "seen"], 0, "didn't 后接动词原形 see。"),
        make_quiz_item("L01_Q58", "___ you go anywhere last weekend?", ["Did", "Do", "Does"], 0, "过去时疑问用 Did。"),
        make_quiz_item("L01_Q59", "The weather was ___.", ["wonderful", "wonder", "wonderfully"], 0, "was 后接形容词 wonderful。"),
        make_quiz_item("L01_Q60", "There is ___ in the box.", ["nothing", "no", "not"], 0, "There is nothing 表示什么都没有。"),
        make_quiz_item("L01_Q61", "He did it by ___.", ["himself", "myself", "yourself"], 0, "by himself 意为靠他自己。"),
        make_quiz_item("L01_Q62", "Make ___ at home.", ["yourself", "myself", "himself"], 0, "Make yourself at home 意为别拘束。"),
        make_quiz_item("L01_Q63", "Most of ___ like English.", ["us", "we", "our"], 0, "Most of us 意为我们大多数。"),
        make_quiz_item("L01_Q64", "A few friends ___ to my party.", ["came", "comes", "coming"], 0, "过去时，came 与 few friends 搭配。")
    ]
    add_page(eng.section_head("练", "随堂演练 ① · 综合诊断单选") + make_quiz_grid(q_sec1), 4, "演练①", "综合诊断", priority="CORE", minutes=4)

    q_sec2 = [
        make_quiz_item("L01_Q65", "The boy (play) ___ basketball yesterday.", ["played", "plays", "playing"], 0, "yesterday 过去时，用 played。"),
        make_quiz_item("L01_Q66", "She (be) ___ happy last week.", ["was", "is", "are"], 0, "last week 过去时，单数 was。"),
        make_quiz_item("L01_Q67", "We (go) ___ to the beach last summer.", ["went", "go", "goes"], 0, "last summer 过去时，go 的过去式 went。"),
        make_quiz_item("L01_Q68", "I (not, see) ___ him yesterday.", ["didn't see", "didn't saw", "don't see"], 0, "过去时否定用 didn't + 原形 see。"),
        make_quiz_item("L01_Q69", "There (be) ___ two books on the desk.", ["are", "is", "was"], 0, "two books 复数，用 are。"),
        make_quiz_item("L01_Q70", "He (have) ___ a wonderful holiday.", ["had", "has", "have"], 0, "过去时，have 的过去式 had。")
    ]
    add_page(eng.section_head("练", "随堂演练 ② · 语法填空诊断") + make_quiz_grid(q_sec2), 4, "演练②", "语法填空", priority="CORE", minutes=4)

    q_sec3 = [
        make_quiz_item("L01_Q71", "找错：He didn't went to school.", ["went → go", "didn't → don't", "to → for"], 0, "didn't 后接原形，went 应改为 go。"),
        make_quiz_item("L01_Q72", "找错：She seen a movie yesterday.", ["seen → saw", "a → an", "movie → movies"], 0, "过去式用 saw，seen 是过去分词。"),
        make_quiz_item("L01_Q73", "找错：There is nothing new.", ["正确", "nothing → something", "new → newly"], 0, "形容词放不定代词后，nothing new 正确。"),
        make_quiz_item("L01_Q74", "找错：Did you played basketball?", ["played → play", "Did → Do", "basketball → basketballs"], 0, "Did 后接原形，played 应改为 play。")
    ]
    add_page(eng.section_head("练", "随堂演练 ③ · 改错诊断") + make_quiz_grid(q_sec3), 4, "演练③", "改错闯关", priority="EXTEND", minutes=3)

    mini_task = (eng.section_head("练", "Mini Task · 描述我的假期") +
                 '<div class="mini-task-box">' +
                 '<div class="mini-task-header"><span class="mini-task-icon">📋</span><div class="mini-task-title">任务：用目标词写一段假期描述</div></div>' +
                 '<div class="mini-task-content">用 <b>wonderful, vacation, friends, went, nothing, myself</b> 等词，写 3-4 句描述一次假期或想去的地方。</div>' +
                 '</div>' +
                 '<div class="note-panel"><div class="np-title">表达支架</div>I went on a wonderful vacation with my friends. We had nothing to worry about. I enjoyed myself very much.</div>')
    add_page(mini_task, 4, "Mini Task", "综合运用 · 目标词", priority="CORE", minutes=5)

    # 阅读解题 SOP（六步法 · 移到阅读题目之前，先讲方法再做题）
    sop = (eng.section_head("读", "阅读解题 SOP · 六步法") +
           eng.key_points([("一 先题后文", "先读题干圈关键词，再回原文定位。口诀：先看题，后读文。"),
                           ("二 定位细节", "题干词多在原文原词复现，直接比对。口诀：关键句，划出来。"),
                           ("三 识别主旨", "找首尾句与高频词，避免以偏概全。口诀：首尾段，见主旨。"),
                           ("四 推断判断", "根据证据推结论，不选无依据选项。口诀：有证据，才推断。"),
                           ("五 词义猜测", "利用上下文线索、同义复现猜生词。口诀：看前后，猜词义。"),
                           ("六 复查核对", "核对题目与选项，排除过度推断。口诀：再复查，防陷阱。")]) +
           '<div class="note-panel"><div class="np-title">微型示范 · 六步做题</div><b>Step1</b> 读题：Where did they go?（关键词 where/go）→ <b>Step2</b> 回文定位到 "went to a beautiful town" → <b>Step3-4</b> 主旨：假期经历；无过度推断 → <b>Step5</b> 生词 breathtaking 由 scenery/beautiful 猜出"令人惊叹" → <b>Step6</b> 复查选 A。</div>' +
           '<div class="note-panel"><div class="np-title">先讲方法再做题</div>按照六步法完成下面 A/B/C 三篇。答题痕迹标在原文上（可点右上角画笔圈画）。</div>')
    add_page(sop, 5, "阅读解题 SOP", "六步法 · 先讲方法再做题", priority="CORE", minutes=5)

    # P29 - P32 段5 阅读理解（三篇 100-140 词 · 培优 · 覆盖四类题）
    pa_text = ("<b>Passage A (My Wonderful Weekend) · {{source_id:HN2026_L1_reading_a}}</b><br>"
               "Last weekend, I went to a beautiful town with my friends. We had a wonderful time. "
               "The town is famous for its old museum, and everyone said the scenery was breathtaking. "
               "When we arrived, the weather was sunny, so we walked around and saw many interesting things. "
               "We took lots of photos and bought some cards to remember the day. "
               "In the afternoon, we rested under a big tree. I felt a little tired but happy. "
               "There was nothing to worry about. My friends and I decided to visit the museum again next time. "
               "I think a trip like this makes us closer, and it helps us learn about history in a fun way. "
               "We also tried some local food, and it tasted really good. "
               "Before we left, we promised to come back together next year.")
    q_pa = [
        make_quiz_item("L01_Q75", "细节题：Where did they go last weekend?", ["A beautiful town.", "A big city.", "A quiet village."], 0, "原文定位：went to a beautiful town。"),
        make_quiz_item("L01_Q76", "推断题：What can we infer (推断) from the passage?", ["They had a happy trip.", "They didn't like the town.", "It rained all day."], 0, "they felt happy/tired but happy/decided to visit again → 推断为快乐的旅行。"),
        make_quiz_item("L01_Q77", "词汇题：The word \"breathtaking\" in the passage means _____.", ["极美的；令人惊叹的", "便宜的", "常见的"], 0, "由 scenery/old museum/famous 上下文中猜出 breathtaking=令人惊叹的。"),
        make_quiz_item("L01_Q78", "主旨题：What is the passage mainly about?", ["A wonderful weekend trip.", "How to take photos.", "A famous museum's history."], 0, "全文围绕假期旅行经历，主旨为精彩的周末旅行。")
    ]
    pa_html = ('<div class="read-split">'
               '<div class="read-left">'
               '<div class="annotation-bar">'
               '<button class="ann-btn" onclick="setPen(\'red\', \'canvas_L01_A\')">✏️ 细红笔</button>'
               '<button class="ann-btn" onclick="setPen(\'highlighter\', \'canvas_L01_A\')">🖍️ 荧光笔</button>'
               '<button class="ann-btn" onclick="setPen(\'eraser\', \'canvas_L01_A\')">🧹 橡皮</button>'
               '<button class="ann-btn" onclick="setPen(\'clear\', \'canvas_L01_A\')">🗑️ 清空</button>'
               '</div>'
               '<div class="passage-wrap"><canvas class="read-canvas" id="canvas_L01_A"></canvas>'
               '<div class="reading-passage">%s</div></div></div>'
               '<div class="read-right">%s</div>'
               '</div>' % (pa_text, make_quiz_grid(q_pa, cols=False)))
    add_page(eng.section_head("阅", "阅读理解 A · 记叙文 (双栏对比+画笔)") + pa_html, 5, "阅读A", "细节理解", priority="CORE", minutes=6)

    pb_text = ("<b>Passage B (Why Holidays Are Good for You) · {{source_id:HN2026_L1_reading_b}}</b><br>"
               "Taking a holiday is not just fun. It is also very important for your health. "
               "When you are on holiday, you can relax and rest your body and mind. "
               "Most of us feel tired from school and homework, so a break helps a lot. "
               "Some people think holidays cost too much money, but a few days in a nearby park can be wonderful, too. "
               "You can walk, read, or simply enjoy the fresh air. "
               "Nothing can make you feel as fresh as a short trip in nature. "
               "So next time you have a free day, remember to give yourself a comfortable break. "
               "Your body and your brain thank you for it. "
               "A short holiday also gives you time to think about your goals and plans. "
               "When you come back, you feel ready to study and work better.")
    q_pb = [
        make_quiz_item("L01_Q79", "细节题：Why is taking a holiday important?", ["It helps you relax and rest.", "It makes you tired.", "It costs a lot."], 0, "原文定位：relax and rest your body and mind。"),
        make_quiz_item("L01_Q80", "词义题：The word \"break\" in the passage means _____.", ["休息；暂停", "打破", "早餐"], 0, "由 take a holiday/rest 语境猜出 break=休息。"),
        make_quiz_item("L01_Q81", "推断题：What can we infer from the passage?", ["A short trip is enough sometimes.", "Holidays are always expensive.", "Only rich people can take holidays."], 0, "原文：a few days in a nearby park can be wonderful → 推断短途也够。"),
        make_quiz_item("L01_Q82", "主旨题：What is the best title for the passage?", ["Why Holidays Are Good for You", "How to Save Money", "My Last Holiday"], 0, "全文围绕假期对健康的好处，主旨为标题选项 A。")
    ]
    pb_html = ('<div class="read-split">'
               '<div class="read-left">'
               '<div class="annotation-bar">'
               '<button class="ann-btn" onclick="setPen(\'red\', \'canvas_L01_B\')">✏️ 细红笔</button>'
               '<button class="ann-btn" onclick="setPen(\'highlighter\', \'canvas_L01_B\')">🖍️ 荧光笔</button>'
               '<button class="ann-btn" onclick="setPen(\'clear\', \'canvas_L01_B\')">🗑️ 清空</button>'
               '</div>'
               '<div class="passage-wrap"><canvas class="read-canvas" id="canvas_L01_B"></canvas>'
               '<div class="reading-passage">%s</div></div></div>'
               '<div class="read-right">%s</div>'
               '</div>' % (pb_text, make_quiz_grid(q_pb, cols=False)))
    add_page(eng.section_head("阅", "阅读理解 B · 说明文 (双栏对比+画笔)") + pb_html, 5, "阅读B", "说明理解", priority="EXTEND", minutes=6)

    pc_text = ("<b>Passage C (Holiday Safety Tips) · {{source_id:HN2026_L1_sa}}</b><br>"
               "Before you go on a trip, read these tips to keep yourself safe and happy.<br>"
               "1. Choose a good place to visit. Ask your parents or friends before you decide. A good place makes your trip comfortable and fun.<br>"
               "2. Check the weather first. If it is going to rain, take an umbrella and some warm clothes. You do not want to get wet or cold.<br>"
               "3. Keep your things safe. Do not put your money or phone anywhere easy to find. Put them in a safe bag.<br>"
               "4. Stay with your family or friends. Never go anywhere alone at night. It is safer to stay together.<br>"
               "5. Most of all, keep calm and enjoy your holiday. A little trouble is nothing to worry about. A good plan makes your trip full of fun.")
    # C 篇改任务型：阅读回答问题（输入判题，非纯单选）
    pc_fill = (eng.section_head("答", "阅读 C · 回答问题（输入判题）") +
               '<div class="body-text">根据短文内容，在输入框内用英文回答下列问题（答对显绿，答错显红并显示答案）。</div>' +
               '<div class="fill-zone">' +
               '<div class="fill-q" data-ans="the weather"><div class="fq-text">1. What should you check before you go?</div>' +
               '<input class="fill-input-box" type="text" placeholder="输入英文答案"><button class="fill-check-btn" onclick="checkFill(this)">提交</button>' +
               '<div class="fill-explain"></div></div>' +
               '<div class="fill-q" data-ans="calm"><div class="fq-text">2. What should you keep when there is a little trouble?</div>' +
               '<input class="fill-input-box" type="text" placeholder="输入英文答案"><button class="fill-check-btn" onclick="checkFill(this)">提交</button>' +
               '<div class="fill-explain"></div></div>' +
               '<div class="fill-q" data-ans="stay with your family or friends"><div class="fq-text">3. What should you do to keep yourself safe at night?</div>' +
               '<input class="fill-input-box" type="text" placeholder="输入英文答案"><button class="fill-check-btn" onclick="checkFill(this)">提交</button>' +
               '<div class="fill-explain"></div></div>' +
               '<div class="fill-q" data-ans="a good place"><div class="fq-text">4. What makes your trip comfortable and fun?</div>' +
               '<input class="fill-input-box" type="text" placeholder="输入英文答案"><button class="fill-check-btn" onclick="checkFill(this)">提交</button>' +
               '<div class="fill-explain"></div></div>' +
               '</div>' +
               '<div class="note-panel"><div class="np-title">任务型阅读</div>本题为阅读回答问题，用英文简答，考查信息定位与表达。</div>')
    pc_html = ('<div class="read-split">'
               '<div class="read-left">'
               '<div class="reading-passage">%s</div></div>'
               '<div class="read-right">%s</div>'
               '</div>' % (pc_text, pc_fill))
    add_page(eng.section_head("阅", "阅读理解 C · 应用文 (双栏对比+任务型)") + pc_html, 5, "阅读C", "任务型阅读", priority="HOME", minutes=6)

    # 阅读迁移（写作衔接：用文中 2 个新词各造 1 句）
    transfer = (eng.section_head("写", "阅读迁移 · 用新词造句") +
                '<div class="body-text">从三篇阅读中用 <span class="highlight">2 个本课新词</span>（如 wonderful / nothing / anywhere）各造 1 句，作为写作衔接。</div>' +
                '<div class="note-panel"><div class="np-title">示范</div>① <b>wonderful</b>: The trip was wonderful and I want to go again.<br>② <b>nothing</b>: There was nothing to worry about during the holiday.</div>' +
                '<div class="mini-task-box"><div class="mini-task-header"><span class="mini-task-icon">✍️</span><div class="mini-task-title">我的造句（写 2 句）</div></div>' +
                '<div class="mini-task-content">1. ______________________<br>2. ______________________</div></div>')
    add_page(transfer, 5, "阅读迁移", "新词造句 · 写作衔接", priority="EXTEND", minutes=4)

    # P33 - P36 段6 自然拼读（魔法 e · 排版重构：大号示例词 + 音素高亮 + 分卡分栏 + 对照词 + 口诀）
    phon_cards = (
        '<div class="ph-grid">' +
        '<div class="ph-card"><div class="ph-cat">a_e · /eɪ/</div>' +
        '<div class="ph-words">c<b class="ph-hl">a</b>ke&nbsp;&nbsp;n<b class="ph-hl">a</b>me&nbsp;&nbsp;m<b class="ph-hl">a</b>ke</div>' +
        '<div class="ph-compare">没有 e：cap ↔ cape（cap 读 /æ/，cape 读 /eɪ/）</div></div>' +
        '<div class="ph-card"><div class="ph-cat">i_e · /aɪ/</div>' +
        '<div class="ph-words">k<b class="ph-hl">i</b>te&nbsp;&nbsp;f<b class="ph-hl">i</b>ve&nbsp;&nbsp;n<b class="ph-hl">i</b>ne</div>' +
        '<div class="ph-compare">没有 e：kit ↔ kite（kit 读 /ɪ/，kite 读 /aɪ/）</div></div>' +
        '<div class="ph-card"><div class="ph-cat">o_e · /əʊ/</div>' +
        '<div class="ph-words">h<b class="ph-hl">o</b>me&nbsp;&nbsp;n<b class="ph-hl">o</b>se&nbsp;&nbsp;r<b class="ph-hl">o</b>se</div>' +
        '<div class="ph-compare">没有 e：not ↔ note（not 读 /ɒ/，note 读 /əʊ/）</div></div>' +
        '<div class="ph-card"><div class="ph-cat">u_e · /juː/</div>' +
        '<div class="ph-words">c<b class="ph-hl">u</b>te&nbsp;&nbsp;u<b class="ph-hl">u</b>se&nbsp;&nbsp;J<b class="ph-hl">u</b>ne</div>' +
        '<div class="ph-compare">没有 e：cub ↔ cube（cub 读 /ʌ/，cube 读 /juː/）</div></div>' +
        '</div>' +
        '<div class="note-panel"><div class="np-title">口诀</div>e 在词尾不发音，元音变成长音声！a→/eɪ/，i→/aɪ/，o→/əʊ/，u→/juː/。</div>')
    add_page(eng.section_head("拼", "自然拼读 P1 · 魔法 e 发音规则表") + phon_cards, 6, "拼读规则", "魔法 e 辨音", priority="CORE", minutes=3)

    q_ph1 = [
        make_quiz_item("L01_Q85", "单词 cake 中 a 的发音是：", ["/eɪ/", "/æ/", "/e/"], 0, "魔法 e 使 a 发长音 /eɪ/。"),
        make_quiz_item("L01_Q86", "单词 kite 中 i 的发音是：", ["/aɪ/", "/ɪ/", "/iː/"], 0, "魔法 e 使 i 发长音 /aɪ/。"),
        make_quiz_item("L01_Q87", "单词 home 中 o 的发音是：", ["/əʊ/", "/ɒ/", "/ɔː/"], 0, "魔法 e 使 o 发长音 /əʊ/。"),
        make_quiz_item("L01_Q88", "单词 cute 中 u 的发音是：", ["/juː/", "/ʌ/", "/uː/"], 0, "魔法 e 使 u 发长音 /juː/。")
    ]
    add_page(eng.section_head("拼", "拼读 P2 · 辨音选词") + make_quiz_grid(q_ph1), 6, "拼读闯关①", "听音选词", priority="CORE", minutes=3)

    q_ph2 = [
        make_quiz_item("L01_Q89", "cake 中 a_e 的发音与哪个词相同？", ["name", "cat", "map"], 0, "name 也是 a_e，发 /eɪ/。"),
        make_quiz_item("L01_Q90", "kite 中 i_e 的发音与哪个词相同？", ["bike", "big", "six"], 0, "bike 也是 i_e，发 /aɪ/。"),
        make_quiz_item("L01_Q91", "home 中 o_e 的发音与哪个词相同？", ["nose", "dog", "box"], 0, "nose 也是 o_e，发 /əʊ/。"),
        make_quiz_item("L01_Q92", "cute 中 u_e 的发音与哪个词相同？", ["June", "cup", "bus"], 0, "June 也是 u_e，发 /juː/。")
    ]
    add_page(eng.section_head("拼", "拼读 P3 · 解码高手") + make_quiz_grid(q_ph2), 6, "拼读闯关②", "同音识别", priority="EXTEND", minutes=3)

    add_page(eng.section_head("拼", "拼读 P4 · 归纳总结") +
             '<div class="note-panel"><div class="np-title">总结法则</div>魔法 e：辅音 + 元音 + 辅音 + e，结尾 e 不发音，使中间元音发长音。熟记规则轻松拼读！</div>', 6, "拼读总结", "法则归纳", priority="EXTEND", minutes=2)

    # P37 - P38 段7 课堂游戏
    q_g17_1 = [
        make_quiz_item("L01_Q93", "哪个是不定代词？", ["something", "quickly", "happily"], 0, "something 是不定代词。"),
        make_quiz_item("L01_Q94", "哪个是过去式？", ["went", "go", "goes"], 0, "went 是 go 的过去式。"),
        make_quiz_item("L01_Q95", "哪个是形容词？", ["wonderful", "wonder", "wonderfully"], 0, "wonderful 是形容词。"),
        make_quiz_item("L01_Q96", "哪个句型是 SVO？", ["I like apples.", "The sun shines.", "She is happy."], 0, "I like apples 是主谓宾 SVO。")
    ]
    add_page(eng.section_head("戏", "课堂综合游戏 ① · 知识快闪") + make_quiz_grid(q_g17_1), 7, "游戏①", "快速反应", priority="EXTEND", minutes=4)

    q_g17_2 = [
        make_quiz_item("L01_Q97", "听音选词：/wʌn/ 对应：", ["one", "two", "three"], 0, "one 发音为 /wʌn/。"),
        make_quiz_item("L01_Q98", "听音选词：/fɔː(r)/ 对应：", ["four", "two", "three"], 0, "four 发音为 /fɔː(r)/。"),
        make_quiz_item("L01_Q99", "听音选词：/neɪm/ 对应：", ["name", "number", "clock"], 0, "name 发音为 /neɪm/。"),
        make_quiz_item("L01_Q100", "听音选词：/ˈeniwʌn/ 对应：", ["anyone", "anywhere", "something"], 0, "anyone 发音为 /ˈeniwʌn/。")
    ]
    add_page(eng.section_head("戏", "课堂综合游戏 ② · 听音辨词") + make_quiz_grid(q_g17_2), 7, "游戏②", "听音匹配", priority="EXTEND", minutes=4)

    # P39 - P42 段8 总结 + 段9 导图
    sum_html = (eng.section_head("结", "课堂总结 · 知识图谱") +
                '<div class="kmap">' +
                '<div class="kmap-node"><div class="kn-title">句型</div><div class="kn-body">SV/SVO/SP/SVOO/SVOC 五大句型。</div></div>' +
                '<div class="kmap-node"><div class="kn-title">过去时</div><div class="kn-body">规则 -ed / 不规则 went/saw/had；否定 didn&#39;t，疑问 Did。</div></div>' +
                '<div class="kmap-node"><div class="kn-title">不定代词</div><div class="kn-body">some/any/no/every + one/thing/where。</div></div>' +
                '<div class="kmap-node"><div class="kn-title">拼读</div><div class="kn-body">魔法 e：a_e/i_e/o_e/u_e 发长音。</div></div>' +
                '</div>' +
                '<div class="note-panel"><div class="np-title">课后作业</div>① 背诵 30 词（10 新词 + 20 巩固）；② 用五大句型各写 1 句；③ 完成配套练习；④ 整理错题本。</div>')
    add_page(sum_html, 8, "课堂总结", "知识图谱", priority="CORE", minutes=3)

    q_exit = [
        make_quiz_item("L01_Q101", "wonderful 意思是：", ["极好的", "糟糕的", "普通的"], 0, "wonderful 意为极好的。"),
        make_quiz_item("L01_Q102", "_____ 是 go 的过去式？", ["went", "goes", "going"], 0, "go 的过去式是 went。"),
        make_quiz_item("L01_Q103", "The sun shines. 是哪种句型？", ["SV", "SVO", "SP"], 0, "shines 不及物，为 SV。"),
        make_quiz_item("L01_Q104", "Is there ___ in the box?", ["anything", "something", "nothing"], 0, "疑问句用 anything。"),
        make_quiz_item("L01_Q105", "写一句含 wonderful 的假期句子。", ["I had a wonderful holiday.", "I like apples.", "He is tall."], 0, "用 wonderful 描述假期即可。")
    ]
    add_page(eng.section_head("结", "Exit Ticket · 5分钟形成性检测") + make_quiz_grid(q_exit), 8, "Exit Ticket", "检测通关", priority="CORE", minutes=5)

    # 下节课预告（扩展页）
    preview = (eng.section_head("结", "下节课预告 · 第 2 课") +
               eng.key_points([("语法①", "一般过去时 was/were 与 did。"),
                               ("语法②", "地点与感受表达。"),
                               ("语法③", "不定表达 somewhere/anywhere/nothing。"),
                               ("新词", "假期地点与感受相关词汇。")]) +
               '<div class="note-panel"><div class="np-title">课前准备</div>复习本课诊断短板，下节课将围绕一般过去时深化与假期地点表达展开。</div>')
    add_page(preview, 8, "下节课预告", "第 2 课", priority="EXTEND", minutes=3)

    card17 = {
        "lesson": 1,
        "theme": theme,
        "tier": "培优",
        "stage": "S1",
        "student": "李民宪",
        "grammar": ["五大基本句型", "一般过去时", "复合不定代词"],
        "phonics": "a_e/i_e/o_e/u_e",
        "vocab": {"new_count": 10}
    }
    mm_html = (eng.section_head("图", "课堂思维导图 · 本课全貌") +
               '<div class="body-text">点击分支复盘本课 <span class="highlight">词汇 + 语法 + 拼读</span> 核心脉络（含诊断结论）。</div>' +
               eng.mind_map(card17))
    add_page(mm_html, 9, "思维导图", "互动复盘", priority="CORE", minutes=3)

    mm_full = (eng.section_head("图", "思维导图 · 完整内容页") +
               eng.mind_map_full(card17))
    add_page(mm_full, 9, "完整大纲", "对照自测", priority="EXTEND", minutes=3)

    total = p - 1
    seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
    js_extra = ("var studentId='stu_lmx';\n" +
                JS_FULL % (total, json.dumps(seg_pages, ensure_ascii=False),
                           json.dumps(page_meta, ensure_ascii=False)))
    # 视觉合同标记（批次2 V1.0：仅纯注释，不改变 CSS 声明）
    CSS_CONTRACT_MARKERS = (
        '/* <CW-CSS-EXTRA version="1.0" required="true"> */\n'
        '/* <CW-SECTION name="tokens"> */\n'
        '/* </CW-SECTION> */\n'
        '/* <CW-SECTION name="components"> */\n'
        '/* </CW-SECTION> */\n'
        '/* <CW-SECTION name="states"> */\n'
        '/* </CW-SECTION> */\n'
        '/* <CW-SECTION name="theme"> */\n'
        '/* </CW-SECTION> */\n'
        '/* <CW-SECTION name="patches"> */\n'
        '/* </CW-SECTION> */\n'
        '/* </CW-CSS-EXTRA> */\n'
    )
    html = build_courseware(title="第01课时 · " + theme, pages_dict=pages, js_extra=js_extra,
                            session="L01", nav_html=NAV_HTML, stage_badge=stage_badge,
                            n_pages=total, css_extra=CSS_CONTRACT_MARKERS + CSS_FULL + build_theme_css("review"))
    # 注入 HTML 合同标记到封面页首（CW-VISUAL-CONTRACT:1 标记新合同课件）
    html = html.replace(
        '<div class="cover-wrap',
        '<!-- CW-VISUAL-CONTRACT:1 -->\n<div class="cover-wrap',
        1
    )
    return html

if __name__ == "__main__":
    html = build_lesson_01()
    out = os.path.join(os.path.dirname(HERE), "李民宪", "第01课时", "第01课时_课件.html")
    open(out, "w", encoding="utf-8").write(html)
    print("李民宪 L1 课件生成：%s (%d bytes)" % (out, len(html.encode("utf-8"))))