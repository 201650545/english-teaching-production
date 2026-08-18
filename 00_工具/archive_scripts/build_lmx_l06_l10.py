# -*- coding: utf-8 -*-
"""
李民宪 L6–L10 五课课件生成器（引擎原生体系 · page-id 契约）
严格遵循《01_课件格式规范.md》与《00_全局约束与红线.md》：
1. 每课 40-45 页，page-id 契约，体积 ≥150KB
2. 答案分布 ≤40%，交互函数全定义，翻页无过渡动画
3. 阅读词数：A=180 / B=220 / C=260
4. 每课主题色不同（theme_colors.py 选）
5. 含听力环节（培优含听力）+ 思维导图页
6. 参考 build_lesson_LMX_L01.py 模式，但每课内容不同
可独立运行：python build_lmx_l06_l10.py
"""
import os, sys, json, re, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from courseware_core import build_courseware, page, vocab_cards, CORE_CSS, CORE_JS
import courseware_engine as eng
from theme_colors import build_theme_css, THEME_EMOJI, THEME_NAME
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

/* 诊断短板定位器 */
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

/* 五大句型分类天平 */
.pattern-tray { display: flex; flex-wrap: wrap; gap: 10px; padding: 14px; background: rgba(255,248,240,0.8);
  border: 2px dashed #E63946; border-radius: 14px; margin-bottom: 14px; }
.pattern-card { padding: 8px 14px; background: #fff; border: 2px solid #3B82F6; border-radius: 10px; font-size: 16px;
  font-weight: 700; color: #1E293B; cursor: grab; user-select: none; }
.pattern-grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
.pattern-box { background: rgba(255,255,255,0.9); border: 3px solid #2563EB; border-radius: 12px; padding: 10px;
  min-height: 120px; }
.pattern-box .pb-title { font-size: 16px; font-weight: 800; color: #2563EB; text-align: center; border-bottom: 2px solid #DBEAFE; padding-bottom: 6px; }

/* 翻牌转盘 */
.past-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin: 12px 0; }
.past-card { height: 120px; perspective: 1000px; cursor: pointer; }
.past-inner { position: relative; width: 100%; height: 100%; transition: transform .6s; transform-style: preserve-3d; }
.past-card.flipped .past-inner { transform: rotateY(180deg); }
.past-front, .past-back { position: absolute; inset: 0; backface-visibility: hidden; border-radius: 14px;
  display: flex; flex-direction: column; align-items: center; justify-content: center; font-weight: 800; box-shadow: 0 8px 22px rgba(0,0,0,.12); }
.past-front { background: linear-gradient(135deg,#fff,#FFF3E0); border: 3px dashed var(--brand); font-size: 26px; color: var(--brand); }
.past-back { background: var(--grad-brand); color: #fff; transform: rotateY(180deg); font-size: 26px; }

/* 配对题 */
.mbox { display: flex; gap: 20px; justify-content: center; margin: 12px 0; }
.mcol { display: flex; flex-direction: column; gap: 10px; min-width: 200px; }
.mitm { padding: 10px 16px; background: #fff; border: 2px solid #ddd; border-radius: 8px; font-size: 17px;
  cursor: pointer; text-align: center; transition: all .2s; }
.mitm.selected { border-color: var(--accent); background: rgba(255,215,0,.1); }
.mitm.matched { border-color: var(--correct); background: var(--correct-row-bg); pointer-events: none; }
.mitm.wrong-match { border-color: var(--error); background: var(--error-row-bg); animation: shake .4s; }

/* 拼读分卡 */
.ph-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 14px 0; }
.ph-card { background: #fff; border-radius: 16px; padding: 18px; box-shadow: var(--card-shadow); border-top: 5px solid var(--brand); }
.ph-cat { font-size: 24px; font-weight: 900; color: var(--brand); margin-bottom: 10px; }
.ph-words { font-size: 28px; font-weight: 800; color: var(--text-primary); line-height: 1.8; letter-spacing: 2px; }
.ph-hl { color: var(--brand); font-size: 32px; }
.ph-compare { margin-top: 10px; padding: 8px 12px; background: #FFF7ED; border-left: 4px solid #F59E0B; border-radius: 8px; font-size: 16px; color: #7C4A03; }

/* 任务型阅读输入判题 */
.fill-zone { display: flex; flex-direction: column; gap: 12px; }
.fill-q { background: #fff; border: 2px solid #3B82F6; border-radius: 12px; padding: 12px; }
.fill-q .fq-text { font-size: 17px; font-weight: 700; color: #1E293B; margin-bottom: 8px; }
.fill-input-box { width: 100%; padding: 8px 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; }
.fill-input-box.correct { border-color: var(--correct); background: var(--correct-row-bg); }
.fill-input-box.wrong { border-color: var(--error); background: var(--error-row-bg); }
.fill-explain { display: none; margin-top: 6px; font-size: 14px; color: #7C4A03; }
.fill-explain.show { display: block; }

/* 合规占位 */
.hl-card { background: #fff; border-radius: 12px; }
.mt-header { font-weight: 700; font-size: 16px; }
.mt-body { margin-top: 8px; font-size: 14px; }

/* sd-unit 组件别名（对齐视觉合同 .sd-sent，兼容 .sd-sentence 实际类） */
.sd-sent { font-size: 18px; font-weight: 700; line-height: 1.6; }

/* 词块合成器 */
.assembler { background: #fff; border-radius: 16px; padding: 18px; box-shadow: var(--card-shadow); margin: 12px 0; }
.asm-chips { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 12px; }
.asm-chip { padding: 8px 14px; background: var(--brand); color: #fff; border-radius: 10px; font-size: 16px;
  font-weight: 700; cursor: pointer; transition: all .15s; }
.asm-chip:hover { transform: translateY(-2px); }
.asm-chip.used { opacity: .35; pointer-events: none; }
.asm-sentence { min-height: 60px; padding: 12px; background: #FFF8F0; border: 2px dashed var(--brand); border-radius: 10px; font-size: 20px; line-height: 1.7; }

/* 听力环节 */
.listen-panel { background: #fff; border-radius: 18px; padding: 20px; box-shadow: var(--card-shadow); margin: 12px 0; }
.listen-play { padding: 12px 24px; background: var(--brand); color: #fff; border: none; border-radius: 12px;
  font-size: 20px; font-weight: 700; cursor: pointer; box-shadow: 0 6px 16px rgba(0,0,0,.15); }
.listen-play:hover { background: var(--brand-light); }
.listen-transcript { display: none; margin-top: 14px; padding: 14px 18px; background: #F0F9FF;
  border: 2px dashed #3B82F6; border-radius: 12px; font-size: 18px; line-height: 1.8; color: #1E293B; }
.listen-transcript.show { display: block; }

/* 思维导图补充：生态/合作主题 */
.eco-map { display: flex; flex-wrap: wrap; gap: 12px; justify-content: center; margin: 14px 0; }
.eco-node { background: #fff; border-radius: 50%; width: 120px; height: 120px; display: flex; align-items: center;
  justify-content: center; text-align: center; padding: 12px; box-shadow: var(--card-shadow);
  border: 4px solid var(--brand); font-size: 16px; font-weight: 700; color: var(--brand); }
.eco-node.green { border-color: #10B981; color: #10B981; }
.eco-node.gold { border-color: #F59E0B; color: #B45309; }
.eco-node.blue { border-color: #3B82F6; color: #3B82F6; }
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
  var q=btn.closest('.quiz-container')||btn.closest('.quiz-q')||btn.parentNode; if(q.dataset.done) return; q.dataset.done='1';
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
  var q=e.target.closest('.quiz-container') || e.target.closest('.quiz-q');
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

/* 诊断短板定位器 */
function compassPick(item){
  var box=item.closest('.compass');
  var items=box.querySelectorAll('.compass-item');
  for(var i=0;i<items.length;i++){ items[i].classList.remove('active'); }
  item.classList.add('active');
  var t=item.getAttribute('data-tip');
  var r=box.querySelector('.compass-result-text');
  if(r){ r.textContent=t; }
  if(typeof saveAnswer==='function'){
    saveAnswer('CMP_LMX_COMPASS', item.getAttribute('data-dim'), item.getAttribute('data-dim'), true, 1, 0, false);
  }
}

/* 句型分类天平 */
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

/* 任务型阅读输入判题 */
function checkFill(btn){
  var q=btn.closest('.quiz-q') || btn.closest('.fill-q'); if(!q) return;
  if(q.dataset.done) return; q.dataset.done='1';
  var input=q.querySelector('.fill-input-box');
  var ans=(q.getAttribute('data-ans')||'').toLowerCase().trim();
  var val=(input.value||'').toLowerCase().trim();
  var ok=(val===ans);
  var exp=q.querySelector('.fill-explain');
  if(ok){ input.classList.add('correct'); playCorrect(); if(exp){ exp.textContent='回答正确！'; exp.classList.add('show'); } }
  else{ input.classList.add('wrong'); playError(); if(exp){ exp.textContent='正确答案：'+q.getAttribute('data-ans'); exp.classList.add('show'); } }
  if(typeof saveAnswer==='function' && q.dataset.qid){ saveAnswer(q.dataset.qid, val, ans, ok, 1, 0, false); }
}

/* 词块合成器 */
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

/* 听力播放（培优含听力：点播放朗读题干，再选答案） */
function playListen(btn){
  var panel=btn.closest('.listen-panel');
  var transcript=panel.querySelector('.listen-transcript');
  if(transcript){ transcript.classList.add('show'); }
  if(typeof playCorrect==='function') playCorrect();
  if(typeof speechSynthesis!=='undefined' && transcript){
    var u=new SpeechSynthesisUtterance();
    u.lang='en-US'; u.text=transcript.textContent;
    speechSynthesis.cancel(); speechSynthesis.speak(u);
  }
}

/* 思维导图分支切换（对应 eng.mind_map 生成的 mmToggle 调用） */
function mmToggle(node){
  var br=node.parentNode;
  var all=document.querySelectorAll('.mm-branch.active');
  for(var i=0;i<all.length;i++){ all[i].classList.remove('active'); }
  br.classList.add('active');
  var panel=document.getElementById('mmPanel');
  if(panel){
    document.getElementById('mmPanelChips').innerHTML = br.querySelector('.mm-chips').innerHTML;
    document.getElementById('mmPanelTitle').innerHTML = node.querySelector('.mm-icon').textContent + ' ' + node.querySelector('.mm-label').textContent;
    panel.className = 'mm-panel ' + br.getAttribute('data-color');
  }
}

initDB();
""" + C.COMPONENT3_JS

NAV_HTML = """<div class="nav-bar">
  <div class="nav-item" data-segment="1" onclick="jumpToSegment(1)"><span class="nav-num">①</span>复习导入</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="2" onclick="jumpToSegment(2)"><span class="nav-num">②</span>新词学习</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="3" onclick="jumpToSegment(3)"><span class="nav-num">③</span>语法精讲</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="4" onclick="jumpToSegment(4)"><span class="nav-num">④</span>随堂演练</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="5" onclick="jumpToSegment(5)"><span class="nav-num">⑤</span>阅读理解</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="6" onclick="jumpToSegment(6)"><span class="nav-num">⑥</span>听力环节</div>
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

# ======================= 听力面板 =======================
def listen_panel(title, transcript, q_items):
    inner = q_items
    if isinstance(q_items, list):
        inner = make_quiz_grid(q_items)
    return (eng.section_head("听", title) +
            '<div class="listen-panel">' +
            '<button class="listen-play" onclick="event.stopPropagation();playListen(this)">🔊 播放听力</button>' +
            '<div class="listen-transcript">' + transcript + '</div></div>' +
            inner)

# ======================= 主题词汇数据 =======================
# words: (en, 音标, 词性, 中文, 搭配, 例句, 记忆法)
# review_words: (en, 中文, 来源标注)
# grammar: (能力名, 六色卡class, 关键词, 备注)
# phonics: [(组合, 音素, [示例词...]), ...]
LESSON_DATA = {
    6: {
        "theme_key": "family",
        "theme": "家庭合作与社区",
        "stage_badge": "培优 · Stage 1 · L6",
        "words": [
            ("borrow", "/ˈbɒrəʊ/", "v.", "借；借用", "borrow sth from sb", "Can I borrow your book?", "borrow 借入（与 lend 借出相对）"),
            ("treasure", "/ˈtreʒə(r)/", "n./v.", "珍宝；珍藏", "family treasure", "This photo is my treasure.", "treas+ure 珍宝"),
            ("hunt", "/hʌnt/", "v.", "寻找；狩猎", "hunt for", "We hunt for the lost keys.", "hunt 搜寻"),
            ("lift", "/lɪft/", "v.", "举起；抬起", "lift up", "Help me lift this box.", "lift 举起"),
            ("until", "/ənˈtɪl/", "prep./conj.", "直到", "not...until", "Wait until 5 o'clock.", "un+til 直到"),
            ("take notes", "/teɪk nəʊts/", "phr.", "记笔记", "take notes in class", "I take notes carefully.", "take+notes 记笔记"),
            ("clean up", "/kliːn ʌp/", "phr.", "打扫；清理", "clean up the room", "Let's clean up together.", "clean+up 清理"),
            ("community", "/kəˈmjuːnəti/", "n.", "社区；团体", "the community center", "We help our community.", "communi+ty 社区"),
            ("share", "/ʃeə(r)/", "v.", "分享", "share with", "Share your toys with friends.", "share 分享"),
            ("rubbish", "/ˈrʌbɪʃ/", "n.", "垃圾", "pick up rubbish", "Don't throw rubbish on the street.", "rubb+ish 垃圾"),
        ],
        "grammar": [
            ("borrow/lend + give a lift + until", "rc-zhug", "家庭/社区活动表达", "借入借出"),
            ("祈使句与提建议", "rc-xing", "Let's / Can you / Don't forget", "建议句型"),
            ("社区活动信息表述", "rc-ming", "when/where/who + 活动 + 目的", "信息五要素"),
        ],
        "review_words": [
            ("family", "家庭", "七下高频·家庭"), ("room", "房间", "七下高频·房间"),
            ("house", "房子", "七下高频·住宅"), ("kitchen", "厨房", "七下高频·家务"),
            ("garden", "花园", "七下高频·户外"), ("help", "帮助", "七下高频·助人"),
            ("clean", "打扫", "七下高频·家务"), ("cook", "烹饪", "七下高频·家务"),
            ("wash", "洗", "七下高频·家务"), ("neighbour", "邻居", "七下高频·邻里"),
            ("friendly", "友好的", "七下高频·人际"), ("together", "一起", "七下高频·合作"),
            ("party", "聚会", "七下高频·活动"), ("game", "游戏", "七下高频·活动"),
            ("book", "书", "七上高频·学习"), ("gift", "礼物", "七下高频·赠送"),
            ("happy", "高兴的", "七上高频·情绪"), ("busy", "忙碌的", "七下高频·状态"),
            ("day", "一天", "七上高频·时间"), ("weekend", "周末", "七下高频·时间"),
        ],
        "phonics": [
            ("-all", "/ɔːl/", ["ball", "call", "tall", "small", "wall"]),
            ("-ill", "/ɪl/", ["will", "hill", "fill", "ill", "still"]),
            ("-ell", "/el/", ["bell", "tell", "well", "sell", "smell"]),
        ],
        "listening": "We are going to clean up our community today. Everyone please bring a bag and some gloves. First, we will pick up paper in the park. Then, we will plant some flowers together. Remember to share the work and help each other. We will work until twelve o'clock. Thank you for your help!",
    },
    7: {
        "theme_key": "appearance",
        "theme": "人物差异",
        "stage_badge": "培优 · Stage 1 · L7",
        "words": [
            ("compare", "/kəmˈpeə(r)/", "v.", "比较", "compare A with B", "Compare the two pictures.", "com+pare 比较"),
            ("shy", "/ʃaɪ/", "adj.", "害羞的", "a shy girl", "She is shy at first.", "shy 害羞"),
            ("lazy", "/ˈleɪzi/", "adj.", "懒惰的", "a lazy cat", "He is too lazy.", "lazy 懒惰"),
            ("loud", "/laʊd/", "adj.", "大声的", "a loud voice", "Don't be so loud.", "loud 大声"),
            ("outgoing", "/ˌaʊtˈɡəʊɪŋ/", "adj.", "外向的", "an outgoing boy", "He is very outgoing.", "out+going 外向"),
            ("hard-working", "/ˌhɑːd ˈwɜːkɪŋ/", "adj.", "勤奋的", "a hard-working student", "She is hard-working.", "hard+working 勤奋"),
            ("perform", "/pəˈfɔːm/", "v.", "表演", "perform on stage", "They perform a show.", "per+form 表演"),
            ("solve", "/sɒlv/", "v.", "解决", "solve a problem", "Help me solve this.", "solve 解决"),
            ("prize", "/praɪz/", "n.", "奖品；奖", "win a prize", "She got a prize.", "prize 奖品"),
            ("attend", "/əˈtend/", "v.", "参加", "attend a meeting", "He attends the class.", "at+tend 参加"),
        ],
        "grammar": [
            ("形容词/副词比较级 -er / more + than", "rc-zhug", "短词-er 长词-more", "比较级"),
            ("as...as 同级与否定 not as...as", "rc-bin", "as 原级 as", "同级比较"),
            ("人物对比描述句式", "rc-qita", "Both.../...but.../...is more...than", "对比三件套"),
        ],
        "review_words": [
            ("tall", "高的", "七下高频·外貌"), ("short", "矮的", "七下高频·外貌"),
            ("hair", "头发", "七下高频·外貌"), ("kind", "友善的", "七下高频·性格"),
            ("funny", "有趣的", "七下高频·性格"), ("friendly", "友好的", "七下高频·性格"),
            ("quiet", "安静的", "七下高频·性格"), ("run", "跑", "七下高频·能力"),
            ("draw", "画画", "七下高频·能力"), ("sing", "唱歌", "七下高频·能力"),
            ("dance", "跳舞", "七下高频·能力"), ("music", "音乐", "七下高频·兴趣"),
            ("sport", "运动", "七下高频·兴趣"), ("movie", "电影", "七下高频·兴趣"),
            ("club", "社团", "七下高频·校园"), ("school", "学校", "七上高频·校园"),
            ("class", "班级；课", "七上高频·校园"), ("smart", "聪明的", "七下高频·形容词"),
            ("brave", "勇敢的", "七下高频·形容词"), ("cute", "可爱的", "七下高频·形容词"),
        ],
        "phonics": [
            ("ea", "/iː/", ["eat", "tea", "read", "speak", "team", "clean"]),
            ("ee", "/iː/", ["see", "three", "green", "sleep", "meet", "keep"]),
            ("ie", "/iː/", ["piece", "field", "chief", "believe"]),
            ("ea", "/e/", ["head", "bread", "weather", "heavy", "ready", "health"]),
        ],
        "listening": "Today we compare two good friends. Tom is outgoing and always ready to help. He performs on stage and often wins a prize. Mary is a little shy, but she is very hard-working. She studies hard and always solves problems. They are different, but they are good friends.",
    },
    8: {
        "theme_key": "activities",
        "theme": "友谊与观点",
        "stage_badge": "培优 · Stage 1 · L8",
        "words": [
            ("spare time", "/speə taɪm/", "phr.", "空闲时间", "in my spare time", "I read in my spare time.", "spare+time 空闲时间"),
            ("pleasure", "/ˈpleʒə(r)/", "n.", "愉快；乐事", "with pleasure", "It is a pleasure.", "pleas+ure 愉快"),
            ("have sth in common", "/hæv ɪn ˈkɒmən/", "phr.", "有共同点", "have ... in common", "We have a lot in common.", "common 共同"),
            ("appearance", "/əˈpɪərəns/", "n.", "外表", "by appearance", "Don't judge by appearance.", "appear+ance 外表"),
            ("personality", "/ˌpɜːsəˈnæləti/", "n.", "个性", "a nice personality", "Her personality is warm.", "personal+ity 个性"),
            ("strength", "/streŋθ/", "n.", "优点；力量", "my strength", "Talking is my strength.", "strength 优点"),
            ("difference", "/ˈdɪfrəns/", "n.", "差异", "a big difference", "There is a difference.", "differ+ence 差异"),
            ("opinion", "/əˈpɪnjən/", "n.", "观点", "in my opinion", "In my opinion, he is right.", "opinion 观点"),
            ("honest", "/ˈɒnɪst/", "adj.", "诚实的", "an honest boy", "Be honest with me.", "honest 诚实"),
            ("friendship", "/ˈfrendʃɪp/", "n.", "友谊", "true friendship", "Friendship is precious.", "friend+ship 友谊"),
        ],
        "grammar": [
            ("比较级复现运用", "rc-zhug", "more honest than / as honest as", "友谊语境运用"),
            ("事实与观点区分", "rc-xing", "Fact vs Opinion", "判断识别"),
            ("观点表达句型", "rc-bin", "In my opinion / I think / For example / However", "观点四句型"),
        ],
        "review_words": [
            ("kind", "仁慈的", "七下·人物"), ("funny", "有趣的", "七下·人物"),
            ("smart", "聪明的", "七下·人物"), ("quiet", "安静的", "七下·人物"),
            ("active", "活跃的", "七下·人物"), ("friendly", "友好的", "七下·人物"),
            ("nice", "好的", "七下·人物"), ("good", "好的", "七下·人物"),
            ("happy", "快乐的", "七下·情绪"), ("sad", "悲伤的", "七下·情绪"),
            ("love", "爱", "七下·情绪"), ("like", "喜欢", "七下·兴趣"),
            ("enjoy", "享受", "七下·兴趣"), ("talk", "谈话", "七下·动作"),
            ("play", "玩耍", "七下·动作"), ("sport", "运动", "七下·兴趣"),
            ("music", "音乐", "七下·兴趣"), ("book", "书", "七下·兴趣"),
            ("movie", "电影", "七下·兴趣"), ("friend", "朋友", "七下·人物"),
        ],
        "phonics": [
            ("-tion", "/ʃən/", ["action", "information", "suggestion", "celebration", "nation", "station"]),
            ("-sion", "/ʒən/", ["decision", "conclusion", "television", "vision", "revision", "occasion"]),
        ],
        "listening": "Today we talk about friendship. My friend Lily and I have a lot in common. In our spare time, we like to read and draw together. We often share our opinions. Lily is honest and kind. In my opinion, a good friend should be honest and helpful. True friendship is a great pleasure.",
    },
    9: {
        "theme_key": "health",
        "theme": "特征与观察",
        "stage_badge": "培优 · Stage 1 · L9",
        "words": [
            ("moss", "/mɒs/", "n.", "苔藓", "green moss", "Moss grows on rocks.", "moss 苔藓"),
            ("redwood", "/ˈredwʊd/", "n.", "红杉", "a tall redwood", "The redwood is old.", "red+wood 红杉"),
            ("cheetah", "/ˈtʃiːtə/", "n.", "猎豹", "a fast cheetah", "The cheetah runs fast.", "cheetah 猎豹"),
            ("folding fan", "/ˈfəʊldɪŋ fæn/", "phr.", "折扇", "a paper folding fan", "She has a folding fan.", "folding+fan 折扇"),
            ("bamboo", "/bæmˈbuː/", "n.", "竹子", "bamboo forest", "Pandas eat bamboo.", "bamboo 竹子"),
            ("popular", "/ˈpɒpjələ(r)/", "adj.", "受欢迎的", "be popular with", "He is popular at school.", "popular 受欢迎"),
            ("tool", "/tuːl/", "n.", "工具", "a useful tool", "Scissors are a tool.", "tool 工具"),
            ("appear", "/əˈpɪə(r)/", "v.", "出现", "appear suddenly", "Stars appear at night.", "appear 出现"),
            ("butterfly", "/ˈbʌtəflaɪ/", "n.", "蝴蝶", "a colorful butterfly", "A butterfly flies by.", "butter+fly 蝴蝶"),
            ("weigh", "/weɪ/", "v.", "称重；重", "weigh up to", "It weighs ten kg.", "weigh 称重"),
        ],
        "grammar": [
            ("数量长度重量表达", "rc-zhug", "How long/tall/much + meters/kg", "计量表达"),
            ("比较级与最高级复习", "rc-bin", "tallest/fastest/biggest + than/as...as", "变化规则"),
            ("看图描述与信息表格", "rc-xing", "This is.../It has.../It can...", "信息卡句式"),
        ],
        "review_words": [
            ("animal", "动物", "七下·动物"), ("plant", "植物", "七下·植物"),
            ("flower", "花", "七下·植物"), ("tree", "树", "七下·植物"),
            ("grass", "草", "七下·植物"), ("green", "绿色的", "七下·颜色"),
            ("red", "红色的", "七下·颜色"), ("big", "大的", "七下·大小"),
            ("small", "小的", "七下·大小"), ("tall", "高的", "七下·大小"),
            ("short", "矮的", "七下·大小"), ("long", "长的", "七下·大小"),
            ("fast", "快的", "七下·速度"), ("slow", "慢的", "七下·速度"),
            ("many", "许多", "七下·数量"), ("much", "许多", "七下·数量"),
            ("beautiful", "美丽的", "七下·描述"), ("cute", "可爱的", "七下·描述"),
            ("dangerous", "危险的", "七下·描述"), ("heavy", "重的", "七下·描述"),
        ],
        "phonics": [
            ("oo", "/uː/", ["moon", "zoo", "food", "cool", "school", "bamboo", "tool"]),
            ("oo", "/ʊ/", ["book", "look", "good", "foot", "wood"]),
        ],
        "listening": "Today we observe nature. Look at the forest! Green moss grows on the rocks. The tall redwoods are hundreds of years old. A fast cheetah can run very quickly. A colorful butterfly appears among the flowers. People use bamboo to make many useful tools, like folding fans. Nature is full of wonders.",
    },
    10: {
        "theme_key": "life",
        "theme": "生态联系",
        "stage_badge": "培优 · Stage 1 · L10",
        "words": [
            ("connect", "/kəˈnekt/", "v.", "连接", "connect A with B", "Bridges connect the two banks.", "con+nect 连接"),
            ("be connected with/to", "/biː kəˈnektɪd wɪð/", "phr.", "与……有联系", "be connected with", "Plants and animals are connected.", "connect 被动式"),
            ("imagine", "/ɪˈmædʒɪn/", "v.", "想象", "imagine doing", "Imagine a better world.", "imagine 想象"),
            ("pollination", "/ˌpɒləˈneɪʃn/", "n.", "授粉", "cross-pollination", "Pollination helps plants.", "pollin+ation 授粉"),
            ("pollen", "/ˈpɒlən/", "n.", "花粉", "carry pollen", "Bees carry pollen.", "pollen 花粉"),
            ("ecosystem", "/ˈiːkəʊsɪstəm/", "n.", "生态系统", "a healthy ecosystem", "Every part matters in an ecosystem.", "eco+system 生态系统"),
            ("protect", "/prəˈtekt/", "v.", "保护", "protect the environment", "We must protect nature.", "pro+tect 保护"),
            ("importance", "/ɪmˈpɔːtns/", "n.", "重要性", "the importance of", "Learn the importance of it.", "import+ance 重要性"),
            ("play a role in", "/pleɪ ə rəʊl ɪn/", "phr.", "在……中起作用", "play a key role", "Bees play a key role in nature.", "role 角色；作用"),
            ("climate", "/ˈklaɪmət/", "n.", "气候", "the changing climate", "Climate affects life.", "climate 气候"),
        ],
        "grammar": [
            ("because/so 因果与 if 条件", "rc-zhug", "because 原因 so 结果 if 条件", "因果句"),
            ("主旨与细节", "rc-xing", "topic sentence + supporting details", "阅读策略"),
            ("词义猜测策略", "rc-warn", "定义/同义/举例/对比线索", "猜词四法"),
        ],
        "review_words": [
            ("animal", "动物", "七下·保护"), ("panda", "熊猫", "七下·保护"),
            ("tiger", "老虎", "七下·保护"), ("elephant", "大象", "七下·保护"),
            ("zoo", "动物园", "七下·保护"), ("flower", "花", "七下·自然"),
            ("butterfly", "蝴蝶", "七下·自然"), ("natural", "自然的", "七下·自然"),
            ("camp", "露营", "七下·自然"), ("lake", "湖", "七下·自然"),
            ("beach", "海滩", "七下·自然"), ("clean", "干净的；打扫", "七下·环境"),
            ("weather", "天气", "七下·天气"), ("rain", "雨", "七下·天气"),
            ("sunny", "晴朗的", "七下·天气"), ("cloudy", "多云的", "七下·天气"),
            ("warm", "温暖的", "七下·天气"), ("because", "因为", "七下·原因"),
            ("why", "为什么", "七下·原因"), ("so", "所以", "七下·因果"),
        ],
        "phonics": [
            ("ow", "/aʊ/", ["flower", "how", "now", "cow", "brown"]),
            ("ou", "/aʊ/", ["loud", "about", "house", "cloud", "mouse"]),
            ("ow", "/əʊ/", ["slow", "know", "snow", "grow", "yellow"]),
        ],
        "listening": "Today we learn about the ecosystem. Everything is connected in nature. Bees play a key role in pollination. They carry pollen from one flower to another. Without bees, many plants cannot grow. We must protect the environment and understand the importance of every living thing. The climate is also changing, and we need to act now to protect our planet.",
    },
}

# ======================= 新增教学段辅助构建 =======================
# 语法①/②/③ 提取（主动提取提示梯，句中填空）
GRAM_EXTRACT = {
    6: [
        ("don't leave until", "直到…才离开", "don't + V + until + 时间", "not...until 表示'直到…才'", "We ___ leave until the rain stops."),
        ("Let's clean up", "让我们打扫", "Let's + 动词原形", "Let's 后接动词原形", "___ clean up the park together."),
        ("share with", "与…分享", "share + 物 + with + 人", "share sth with sb", "I share my food ___ my sister."),
    ],
    7: [
        ("more outgoing", "更外向", "more + 多音节形容词", "多音节长词用 more", "Lucy is ___ outgoing than her sister."),
        ("as tall as", "和…一样高", "as + 原级 + as", "同级比较用原级", "Tom is as ___ as his father."),
        ("Both are", "两者都", "Both + A and B + 复数动词", "both...and 接复数谓语", "___ Lily and Lucy are outgoing."),
    ],
    8: [
        ("have ... in common", "有共同点", "have + 物 + in common", "共同点表达", "We have a lot ___ common."),
        ("in my opinion", "依我看", "in my opinion, ...", "观点开头", "___ my opinion, he is honest."),
        ("For example", "例如", "For example, ...", "举例说明", "___ example, my friend is kind."),
    ],
    9: [
        ("weigh", "重达", "主语 + weigh + 数字", "weigh 是动词，三单+s", "The panda ___ 100 kilograms."),
        ("the fastest", "最快的", "the + 最高级 + 范围", "最高级前加 the", "The cheetah is ___ fastest animal on land."),
        ("It has", "它有", "It has + 外观", "第三人称单数用 has", "It ___ long legs and a small head."),
    ],
    10: [
        ("because", "因为", "主句 + because + 从句", "because 表原因", "Bees help plants ___ they carry pollen."),
        ("play a role in", "在…中起作用", "play a role in + 名词", "在…中起作用", "Bees play a key role ___ pollination."),
        ("so", "所以", "原因句 , so + 结果句", "so 表结果", "Bees carry pollen, ___ plants can grow."),
    ],
}

# 句型归类（拖拽到对应分类框）
PATTERNS = {
    6: {
        "boxes": ["祈使句", "借入借出", "时间状语"],
        "pool": [("Let's clean up", "祈使句"), ("Don't throw rubbish", "祈使句"), ("I borrow a book", "借入借出"),
                 ("Can you lend me", "借入借出"), ("Wait until it stops", "时间状语"), ("We don't leave until 8", "时间状语")],
    },
    7: {
        "boxes": ["短词比较级 -er", "长词比较级 more", "同级比较 as...as"],
        "pool": [("Tom is taller", "-er"), ("I am as tall as", "as...as"), ("Lucy is more outgoing", "more"),
                 ("She sings better", "-er"), ("He is as quiet as", "as...as"), ("It is more interesting", "more")],
    },
    8: {
        "boxes": ["Fact 事实", "Opinion 观点"],
        "pool": [("Tom is 14 years old", "fact"), ("They have been friends for years", "fact"),
                 ("I think he is the best", "op"), ("In my opinion, he is kind", "op"),
                 ("She is 1.6 meters tall", "fact"), ("I believe friendship matters", "op")],
    },
    9: {
        "boxes": ["问长度/高度", "问重量", "最高级表达"],
        "pool": [("How long is the bamboo", "long"), ("How tall is the redwood", "tall"),
                 ("How much does it weigh", "weigh"), ("It is the tallest tree", "sup"),
                 ("It is the fastest animal", "sup"), ("It weighs 100 kg", "weigh")],
    },
    10: {
        "boxes": ["because 原因", "so 结果", "if 条件"],
        "pool": [("Bees are important because", "because"), ("Because they carry pollen", "because"),
                 ("Bees carry pollen, so", "so"), ("so plants can grow", "so"),
                 ("If we protect bees", "if"), ("If we help nature", "if")],
    },
}

def review_cards_page(title, sub, rev, a, b):
    """复习词翻牌卡（巩固词①/②）：rev=(en,cn,src)，取 [a,b) 区间。"""
    cards = [(cn, en) for en, cn, _ in rev[a:b]]
    return (eng.section_head("词", title) + eng.sub_label(sub) +
            '<div class="body-text">看中文，回忆英文；点击卡片翻面核对拼写。</div>' +
            eng.flash_grid(cards) +
            '<div class="note-panel"><div class="np-title">复习说明</div>这些 %d 个词取自七年级高频词与近期复习池，先回忆再翻牌，错词记入错题本。</div>' % (b - a))

def diagnostic_compass(lesson_num, theme, dims):
    """诊断短板定位器（L01 结构）：点选最薄弱维度，自动给出提升建议。"""
    items = "".join(
        '<div class="compass-item" onclick="event.stopPropagation();compassPick(this)" data-dim="%s" data-tip="%s">'
        '<div class="ci-icon">%s</div><div class="ci-name">%s</div><div class="ci-desc">%s</div></div>'
        % (name, tip, icon, name, desc)
        for name, icon, desc, tip in dims)
    return (eng.section_head("诊", "诊断短板定位器 · 定位本课薄弱点") +
            '<div class="body-text">开课前先点选你目前最薄弱的一项，课中针对性突破。</div>' +
            '<div class="compass">' + items + '</div>' +
            '<div class="compass-result"><div class="cr-title">诊断建议</div>'
            '<div class="compass-result-text cr-text">点选上方任一维度，此处会给出对应提升建议。</div></div>' +
            '<div class="note-panel"><div class="np-title">本课主题</div>%s · 请带着诊断结果进入本课学习。</div>' % theme)

def phonics_rules_page(phonics):
    """自然拼读规则页：组合 + 音素 + 例词。"""
    cards = []
    for combo, sound, ws in phonics:
        words_html = "".join('<span class="ph-hl">%s</span> ' % w for w in ws)
        cards.append('<div class="ph-card"><div class="ph-cat">%s  →  /%s/</div>'
                     '<div class="ph-words">%s</div></div>' % (combo, sound.lstrip("/"), words_html))
    return (eng.section_head("拼", "自然拼读规则 · 组合发音") +
            '<div class="sub-label">先看组合与音标，再读例词</div>' +
            '<div class="ph-grid">' + "".join(cards) + '</div>' +
            '<div class="note-panel"><div class="np-title">读法提示</div>把同类组合的词放一起读，体会相同发音；再分组比赛谁读得又准又快。</div>')

def phonics_quiz(lesson_num, phonics, qid_start):
    """拼读闯关：① 辨音选词（音→词）② 词→组合归类。返回 (html1, html2, next_qid)。"""
    q1, q2 = [], []
    cid = qid_start
    # 辨音选词：每个组合抽一个例词，干扰项取其他组合的例词
    n = len(phonics)
    for i, (combo, sound, ws) in enumerate(phonics):
        others = [phonics[(i + 1) % n][2][0], phonics[(i + 2) % n][2][0]]
        q1.append(make_quiz_item("L%02d_Q%02d" % (lesson_num, cid), "哪个单词含有 %s 的音？" % sound, [ws[0]] + others, 0, "发音 /%s/，组合 %s。" % (sound.lstrip("/"), combo)))
        cid += 1
    # 词→组合归类：例词对应组合
    for i, (combo, sound, ws) in enumerate(phonics):
        others = [phonics[(i + 1) % n][0], phonics[(i + 2) % n][0]]
        q2.append(make_quiz_item("L%02d_Q%02d" % (lesson_num, cid), "单词 “%s” 的拼读组合是？" % ws[0], [combo] + others, 0, "%s → /%s/。" % (combo, sound.lstrip("/"))))
        cid += 1
    html1 = (eng.section_head("拼", "拼读闯关 ① · 辨音选词") +
             eng.sub_label("看音标，点到含该发音的单词") + make_quiz_grid(q1))
    html2 = (eng.section_head("拼", "拼读闯关 ② · 词→组合") +
             eng.sub_label("看单词，选出它的拼读组合") + make_quiz_grid(q2))
    return html1, html2, cid

def grammar_extract_page(lesson_num, g_point, items):
    """语法提取（主动提取提示梯）：把语法点关键结构做成看中文回忆英文。"""
    return (eng.section_head("法", "语法提取 · %s 关键结构" % g_point) +
            eng.sub_label("看中文提示，先回忆英文结构；再逐级提示，最后迁移造句") +
            C.hint_ladder(items))

def pattern_sort_page(lesson_num, theme, pat):
    """句型归类/拖拽：把句子短语拖到对应句型框。"""
    boxes = pat["boxes"]
    box_html = "".join('<div class="pattern-box" id="pbox_%d" ondragover="allowDrop(event)" '
                       'ondrop="patDrop(event)"><div class="pb-title">%s</div></div>' % (i, b)
                       for i, b in enumerate(boxes))
    cards = []
    for i, (phrase, cat) in enumerate(pat["pool"]):
        box_idx = boxes.index(cat) if cat in boxes else 0
        cards.append('<div class="pattern-card" id="pcard_%d" draggable="true" data-pat="%d" '
                     'ondragstart="patDrag(event)" onclick="event.stopPropagation()">%s</div>' % (i, box_idx, phrase))
    return (eng.section_head("法", "句型归类 · 把句子拖到正确句型框") +
            eng.sub_label("本课句型：%s") % " / ".join(boxes) +
            '<div class="pattern-tray">' + "".join(cards) + '</div>' +
            '<div class="pattern-grid">' + box_html + '</div>' +
            '<div class="note-panel"><div class="np-title">操作</div>按住短语拖到对应框内，放对会变绿，放错变红。</div>')

# 诊断短板定位器维度（每课 6 项）
COMPASS = {
    6: [("词汇", "🆕", "目标词过关了吗？", "理解本课 10 个目标词，掌握搭配与例句，能在句中运用。"),
        ("语法", "🧩", "语法结构清晰吗？", "掌握 until/Let's/share with 等结构并能正确造句。"),
        ("拼读", "🔤", "见词能读吗？", "掌握 -all/-ill/-ell 组合并读准例词。"),
        ("阅读", "📖", "能读主旨细节吗？", "用六步法完成 A/B/C 三篇阅读与任务型作答。"),
        ("听力", "🔊", "听音能辨吗？", "完成培优听力，听音选答。"),
        ("表达", "🗣️", "能开口说吗？", "用目标词完成主题表达与造句。")],
    7: [("词汇", "🆕", "目标词过关了吗？", "理解本课 10 个目标词，掌握搭配与例句。"),
        ("语法", "🧩", "比较级掌握了吗？", "掌握 -er/more + than 与 as...as 同级比较。"),
        ("拼读", "🔤", "见词能读吗？", "掌握 ea/ee/ie 组合的 /iː/ 与 /e/ 发音。"),
        ("阅读", "📖", "能读主旨细节吗？", "用六步法完成 A/B/C 三篇阅读。"),
        ("听力", "🔊", "听音能辨吗？", "完成培优听力，听音选答。"),
        ("表达", "🗣️", "会对比描述吗？", "用比较级描述人物差异。")],
    8: [("词汇", "🆕", "目标词过关了吗？", "理解本课 10 个目标词及观点表达词。"),
        ("语法", "🧩", "观点句型掌握了吗？", "掌握 In my opinion / I think / For example 等句型。"),
        ("拼读", "🔤", "见词能读吗？", "掌握 -tion/-sion 组合的发音。"),
        ("阅读", "📖", "能区分事实观点吗？", "用六步法完成 A/B/C 三篇阅读。"),
        ("听力", "🔊", "听音能辨吗？", "完成培优听力，听音选答。"),
        ("表达", "🗣️", "会表达观点吗？", "用观点句型表达对友谊的看法。")],
    9: [("词汇", "🆕", "目标词过关了吗？", "理解本课 10 个目标词，掌握计量与描述词。"),
        ("语法", "🧩", "计量表达掌握了吗？", "掌握 How long/tall/much 与最高级表达。"),
        ("拼读", "🔤", "见词能读吗？", "掌握 oo 组合的 /uː/ 与 /ʊ/ 发音。"),
        ("阅读", "📖", "能读主旨细节吗？", "用六步法完成 A/B/C 三篇阅读。"),
        ("听力", "🔊", "听音能辨吗？", "完成培优听力，听音选答。"),
        ("表达", "🗣️", "会描述特征吗？", "用信息卡句式描述事物特征。")],
    10: [("词汇", "🆕", "目标词过关了吗？", "理解本课 10 个目标词及生态联系词。"),
         ("语法", "🧩", "因果句掌握了吗？", "掌握 because/so/if 因果与条件表达。"),
         ("拼读", "🔤", "见词能读吗？", "掌握 ow/ou 组合的 /aʊ/ 与 /əʊ/ 发音。"),
         ("阅读", "📖", "能读主旨细节吗？", "用六步法完成 A/B/C 三篇阅读与任务型作答。"),
         ("听力", "🔊", "听音能辨吗？", "完成培优听力，听音选答。"),
         ("表达", "🗣️", "会写说明文吗？", "用目标词写一段生态重要性的说明文。")],
}

# 演练③改错（错句医生）：(错句含 <w>错误词</w>, 正确词)
ERROR_FIX = {
    6: [("Let's <w>cleaning</w> up the room.", "clean"),
        ("We share our food <w>for</w> my sister.", "with"),
        ("We <w>playing</w> games until dark.", "play")],
    7: [("She is <w>outgoinger</w> than her sister.", "more outgoing"),
        ("Tom is <w>as taller as</w> his father.", "as tall as"),
        ("Both Lily and Lucy <w>is</w> outgoing.", "are")],
    8: [("We have a lot <w>on</w> common.", "in"),
        ("<w>To</w> my opinion, he is honest.", "In"),
        ("I <w>am</w> agree with you.", "agree")],
    9: [("The panda <w>weigh</w> 100 kilograms.", "weighs"),
        ("The cheetah is <w>most</w> fastest animal.", "the"),
        ("It <w>have</w> long legs and a small head.", "has")],
    10: [("Bees help plants <w>so</w> they carry pollen.", "because"),
         ("Bees play a key role <w>on</w> pollination.", "in"),
         ("Because bees carry pollen, <w>so</w> plants can grow.", "so")],
}

def review_dictation_page(rev):
    """复习词听写：看中文，先默写英文，再翻牌核对。"""
    return (eng.section_head("词", "复习词听写 · 翻牌核对") +
            eng.sub_label("看中文，先默写英文，再翻牌核对拼写") +
            eng.flash_grid([(cn, en) for en, cn, _ in rev]) +
            '<div class="note-panel"><div class="np-title">听写说明</div>先写英文再翻牌；错词请回到复习词页重记。</div>')

def new_word_memory_page(words):
    """新词速记：分组记忆 + 结构化卡片。"""
    grid = "".join(
        '<div class="vocab-card">'
        '<div class="vocab-head"><span class="vocab-word">%s</span><span class="vocab-phonetic">%s</span>'
        '<span class="vocab-pos">%s</span></div>'
        '<div class="vocab-cn">%s</div>'
        '<div class="vocab-collocation">搭配：%s</div>'
        '<div class="vocab-example">%s</div>'
        '<div class="vocab-memory">记忆：%s</div>'
        '</div>' % (w[0], w[1], w[2], w[3], w[4], w[5], w[6])
        for w in words)
    return (eng.section_head("词", "新词速记 · 记忆地图") +
            eng.sub_label("分组记 + 高频搭配，结构化成卡") +
            '<div class="vocab-grid">' + grid + '</div>' +
            '<div class="note-panel"><div class="np-title">记忆法</div>把搭配与例句一起记，比孤立背词更牢固。</div>')

def phonics_summary_page(phonics):
    """拼读总结：归总本课组合。"""
    rows = "".join(
        '<tr><td>%s</td><td>/%s/</td><td>%s</td></tr>' % (combo, sound.lstrip("/"), " / ".join(ws))
        for combo, sound, ws in phonics)
    return (eng.section_head("拼", "自然拼读总结 · 本课组合一览") +
            eng.sub_label("回顾本课拼读规则，做到见词能读") +
            '<table class="content-table"><thead><tr><th>组合</th><th>音素</th><th>例词</th></tr></thead>'
            '<tbody>%s</tbody></table>' % rows +
            '<div class="note-panel"><div class="np-title">比拼</div>分组朗读例词，看谁能又快又准地读出所有组合。</div>')

# ======================= 构建 L06-L10 =======================
def build_lesson(lesson_num):
    global quiz_idx_counter
    quiz_idx_counter = 0
    data = LESSON_DATA[lesson_num]
    theme_key = data["theme_key"]
    theme = data["theme"]
    stage_badge = data["stage_badge"]
    words = data["words"]
    grammar = data["grammar"]
    listening = data["listening"]
    tname = THEME_NAME.get(theme_key, "本课")
    emoji = THEME_EMOJI.get(theme_key, "🎯⭐")

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

    # ---- 段1 封面 + 目标 + 导入 ----
    cover = ('<div class="cover-wrap cover-variant-c">'
             '<div class="cover-badge">第 %02d 课时 · %s</div>'
             '<div class="cover-title">%s</div>'
             '<div class="cover-sub">培优 · 李民宪 · 能力进阶</div>'
             '<div class="cover-tagline">%s主题 · 词汇 · 语法 · 阅读 · 听力</div>'
             '<div class="cover-info">'
             '<div class="cover-info-num"><div class="ci-label">目标词</div><div class="ci-val">%d</div></div>'
             '<div class="cover-info-num"><div class="ci-label">语法考点</div><div class="ci-val">2</div></div>'
             '<div class="cover-info-num"><div class="ci-label">阅读</div><div class="ci-val">3</div></div>'
             '<div class="cover-info-num"><div class="ci-label">课件页数</div><div class="ci-val">42</div></div>'
             '</div>'
             '<div class="cover-emoji">%s</div></div>' % (lesson_num, theme, theme, tname, len(words), emoji))
    add_page(cover, 1, priority="CORE", minutes=2)

    goal = (eng.section_head("标", "本课学习目标 · " + theme) +
            '<div class="chip-row">'
            '<div class="chip"><span class="chip-icon">🆕</span>' + str(len(words)) + ' 个' + tname + '主题目标词</div>'
            '<div class="chip"><span class="chip-icon">🧩</span>' + grammar[0][2] + '</div>'
            '<div class="chip"><span class="chip-icon">📖</span>A/B/C 三篇阅读</div>'
            '<div class="chip"><span class="chip-icon">🔊</span>培优听力环节</div>'
            '</div>' +
            '<div class="kmap">' +
            '<div class="kmap-node"><div class="kn-title">词汇</div><div class="kn-body">' + str(len(words)) + ' 个' + tname + '目标词，滚动复现。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">语法</div><div class="kn-body">' + grammar[0][2] + ' 核心考点。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">阅读</div><div class="kn-body">细节 + 主旨 + 任务型。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">听力</div><div class="kn-body">培优听力 · 听音选答。</div></div>' +
            '</div>' +
            '<div class="note-panel"><div class="np-title">本课定位</div>通过 ' + theme + ' 主题串联词汇与语法，结合三篇阅读与培优听力，全面提升综合语言能力。</div>')
    add_page(goal, 1, "学习目标", "%s主题 · 四大模块" % theme, priority="CORE", minutes=3)

    # 上节课复习（本课起点热身）
    q_warm = [
        make_quiz_item("L%02d_Q01" % lesson_num, "本课主题「%s」用英文更贴近哪个词？" % theme, ["community", "school", "shop"], 0, "本课围绕%s主题展开。" % theme),
        make_quiz_item("L%02d_Q02" % lesson_num, "What is the English for 分享？", ["share", "hide", "throw"], 0, "share 意为分享。"),
        make_quiz_item("L%02d_Q03" % lesson_num, "Which word means 社区？", ["community", "factory", "market"], 0, "community 意为社区。"),
        make_quiz_item("L%02d_Q04" % lesson_num, "Which word means 诚实？", ["honest", "lazy", "loud"], 0, "honest 意为诚实。"),
    ]
    add_page(eng.section_head("复", "本课起点 · 语感热身") +
             eng.game_board("热身小测", "🎯", "几道轻松题，唤醒英语感觉。", make_quiz_grid(q_warm)) +
             '<div class="note-panel"><div class="np-title">闯关提示</div>答对即可进入正课。本课将围绕「%s」系统学习。</div>' % theme, 1, "本课起点 · 热身", "语感热身 · 开启本课", priority="CORE", minutes=4)

    # 诊断短板定位器（L01 结构：先诊断再学习）
    add_page(diagnostic_compass(lesson_num, theme, COMPASS[lesson_num]), 1, "诊断短板定位器", "定位本课薄弱点", priority="CORE", minutes=3)

    # 复习词①/②（20 个七年级复习词，翻牌回忆）
    rev = data["review_words"]
    add_page(review_cards_page("复习词 ① · 七年级高频（1–10）", "看中文，回忆英文，翻牌核对", rev, 0, 10), 1, "复习词①", "翻牌回忆", priority="CORE", minutes=4)
    add_page(review_cards_page("复习词 ② · 滚动复习（11–20）", "看中文，回忆英文，翻牌核对", rev, 10, 20), 1, "复习词②", "翻牌回忆", priority="CORE", minutes=4)

    # 复习词听写（翻牌核对拼写）
    add_page(review_dictation_page(rev), 1, "复习词听写", "翻牌核对拼写", priority="CORE", minutes=4)

    # ---- 段2 新词学习 ----
    add_page(eng.section_head("词", "目标词 ① · %s主题（1–）" % theme) + eng.vocab_cards(words), 2, "目标词学习", "点击卡片看音标与例句", priority="CORE", minutes=5)

    q_v1 = []
    vq_texts = [
        (words[0][0] + " 意思是：", words[0][3], [words[1][3], words[2][3]]),
        (words[1][0] + " 意思是：", words[1][3], [words[0][3], words[3][3]]),
        (words[2][0] + " 意思是：", words[2][3], [words[4][3], words[5][3]]),
    ]
    for i, (prompt, corr, dist) in enumerate(vq_texts):
        q_v1.append(make_quiz_item("L%02d_Q%02d" % (lesson_num, 5+i), prompt, [corr]+dist, 0, "答案为 %s。" % corr))
    add_page(eng.section_head("词", "目标词闯关 · 即时测试") + make_quiz_grid(q_v1), 2, "目标词闯关", "即时测试", priority="CORE", minutes=4)

    # 词块合成器
    chips = ["I", "can", "help", "my", "community", "now", "We", "share", "the", "work", "together", "and", "clean", "up", "the", "park", "."]
    asm = (eng.section_head("词", "词块合成器 · %s主题" % theme) +
           '<div class="body-text">点击下方词块，合成一句描述本课主题的句子。</div>' +
           '<div class="assembler">' +
           '<div class="asm-chips">' +
           "".join('<div class="asm-chip" onclick="asmAdd(this)">%s</div>' % c for c in chips) +
           '</div>' +
           '<div class="asm-sentence" id="asmSentence"></div>' +
           '<button class="asm-reset" onclick="asmReset()" style="margin-top:10px;padding:8px 20px;background:var(--accent);color:#333;border:none;border-radius:8px;font-size:16px;font-weight:700;cursor:pointer;">↺ 重置</button>' +
           '</div>' +
           '<div class="note-panel"><div class="np-title">参考句</div>I can help my community now. We share the work and clean up the park together.</div>')
    add_page(asm, 2, "词块合成器", "综合表达 · 目标词", priority="EXTEND", minutes=4)

    # 词汇运用选词填空
    cloze_inner = eng.section_head("词", "词汇运用 · 选词填空") + eng.sub_label("用本课目标词补全句子")
    cloze_q = []
    wn = len(words)
    for i in range(5):
        w = words[i]
        cloze_q.append(make_quiz_item("L%02d_Q%02d" % (lesson_num, 10+i), "We ____ each other every day.", [w[0], words[(i+1)%wn][0], words[(i+2)%wn][0]], 0, "用 %s 补全，意为 %s。" % (w[0], w[3])))
    cloze_inner += make_quiz_grid(cloze_q)
    cloze_inner += '<div class="note-panel"><div class="np-title">解题</div>根据句意选出最合适的目标词，注意词义与搭配。</div>'
    add_page(cloze_inner, 2, "词汇运用", "选词填空 · 词义搭配", priority="EXTEND", minutes=4)

    # 听写自测（翻牌核对）
    dictation = (eng.section_head("词", "目标词听写 · 翻牌核对") +
                 '<div class="body-text">看中文，先默写英文，再翻牌核对拼写。</div>' +
                 eng.flash_grid([(w[3], w[0]) for w in words[:8]]) +
                 '<div class="note-panel"><div class="np-title">听写说明</div>先写英文再翻牌；错词请回到目标词页重记。</div>')
    add_page(dictation, 2, "目标词听写", "翻牌核对拼写", priority="CORE", minutes=5)

    # 新词速记（结构化记忆地图）
    add_page(new_word_memory_page(words), 2, "新词速记", "记忆地图 · 结构化卡", priority="CORE", minutes=4)

    # 自然拼读：规则 + 闯关① + 闯关② + 总结
    ph = data["phonics"]
    add_page(phonics_rules_page(ph), 2, "自然拼读规则", "组合发音 · 例词", priority="CORE", minutes=4)
    ph1, ph2, _ph_next = phonics_quiz(lesson_num, ph, 60)
    add_page(ph1, 2, "拼读闯关①", "辨音选词", priority="CORE", minutes=4)
    add_page(ph2, 2, "拼读闯关②", "词→组合", priority="EXTEND", minutes=4)
    add_page(phonics_summary_page(ph), 2, "拼读总结", "组合一览", priority="EXTEND", minutes=3)

    # ---- 段3 语法精讲 ----
    g1 = grammar[0]
    rule1_six = {
        "rc-zhug": (g1[1], g1[2]),
        "rc-bin": ("核心用法", "掌握「%s」的结构与应用场景。" % g1[2]),
        "rc-xing": ("易混辨析", "注意中文与英文语序差异，避免直译。"),
        "rc-ming": ("例句", "We help each other until we finish. 我们用 until 连接时间。"),
        "rc-warn": ("常见错误", "勿把 until 与 before 混用；注意 not...until 的否定语义。"),
        "rc-qita": ("记忆口诀", "主句 + 从句，until 连接两件事，一件事持续到另一件发生。"),
    }
    cards1 = six_cards(rule1_six)
    add_page(eng.section_head("法", "考点① · %s" % g1[1]) +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             '<div class="rule-grid">' + cards1 + '</div>' +
             '<div class="note-panel"><div class="np-title">口诀</div>%s</div>' % g1[2], 3, "语法①", g1[1], priority="CORE", minutes=5)

    # 语法①提取（主动提取提示梯）
    ge = GRAM_EXTRACT[lesson_num]
    add_page(grammar_extract_page(lesson_num, grammar[0][1], [ge[0]]), 3, "语法①提取", "主动提取 · 迁移造句", priority="CORE", minutes=4)

    g2 = grammar[1]
    rule2_six = {
        "rc-zhug": (g2[1], g2[2]),
        "rc-bin": ("核心结构", "掌握「%s」的构成与变化。" % g2[2]),
        "rc-xing": ("重点记忆", "本考点是%s主题的关键应用。" % theme),
        "rc-ming": ("例句", "She is more outgoing than before. 她比以前外向。"),
        "rc-warn": ("易错点", "多音节形容词比较级用 more，勿直接加 -er。"),
        "rc-qita": ("记忆口诀", "看词形分长短，长词用 more，短词加 -er。"),
    }
    cards2 = six_cards(rule2_six)
    add_page(eng.section_head("法", "考点② · %s" % g2[1]) +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             '<div class="rule-grid">' + cards2 + '</div>' +
             '<div class="note-panel"><div class="np-title">口诀</div>%s</div>' % g2[2], 3, "语法②", g2[1], priority="CORE", minutes=5)

    # 语法②提取（主动提取提示梯）
    add_page(grammar_extract_page(lesson_num, grammar[1][1], [ge[1]]), 3, "语法②提取", "主动提取 · 迁移造句", priority="CORE", minutes=4)

    # 语法综合应用
    g_fill = eng.section_head("法", "语法综合应用 · 巧用本课语法") + eng.sub_label("用正确结构填空")
    g_fill_q = [
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 15), "We work ___ the work is done.", ["until", "before", "after"], 0, "until 引导时间，表示持续到完成。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 16), "She is ___ than her sister.", ["more outgoing", "outgoing", "outgoinger"], 0, "多音节形容词比较级用 more outgoing。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 17), "Let's ___ up the room together.", ["clean", "cleaning", "cleans"], 0, "Let's 后接动词原形。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 18), "We share our toys ___ friends.", ["with", "for", "to"], 0, "share sth with sb 与朋友分享。"),
    ]
    g_fill += make_quiz_grid(g_fill_q)
    g_fill += '<div class="note-panel"><div class="np-title">填空思路</div>① until 引导时间；② 多音节比较用 more；③ Let\'s 接原形；④ share with 搭配。</div>'
    add_page(g_fill, 3, "语法综合填空", "核心考点混考", priority="EXTEND", minutes=4)

    # 语法③（讲解六色卡 + 提取）
    g3 = grammar[2]
    rule3_six = {
        "rc-zhug": (g3[1], g3[2]),
        "rc-bin": ("核心结构", "掌握「%s」的结构与应用。" % g3[2]),
        "rc-xing": ("重点记忆", "本考点是%s主题的关键应用。" % theme),
        "rc-ming": ("例句", "Bees help plants because they carry pollen. 蜜蜂帮植物因为它们传粉。"),
        "rc-warn": ("易错点", "注意与同类结构区分，看清语义与位置。"),
        "rc-qita": ("记忆口诀", "看结构辨语义，先提取再迁移。"),
    }
    cards3 = six_cards(rule3_six)
    add_page(eng.section_head("法", "考点③ · %s" % g3[1]) +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             '<div class="rule-grid">' + cards3 + '</div>' +
             '<div class="note-panel"><div class="np-title">口诀</div>%s</div>' % g3[2], 3, "语法③", g3[1], priority="CORE", minutes=5)
    add_page(grammar_extract_page(lesson_num, grammar[2][1], [ge[2]]), 3, "语法③提取", "主动提取 · 迁移造句", priority="CORE", minutes=4)

    # 句型归类/拖拽（五大句型分类天平）
    add_page(pattern_sort_page(lesson_num, theme, PATTERNS[lesson_num]), 3, "句型归类", "拖拽分类", priority="EXTEND", minutes=4)

    # ---- 段4 随堂演练 ----
    q_sec1 = [
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 19), "Can I ___ your eraser?", ["borrow", "lend", "give"], 0, "borrow 借入。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 20), "This old photo is my ___.", ["treasure", "trouble", "trash"], 0, "treasure 珍宝。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 21), "We ___ for the lost cat.", ["hunt", "hide", "hug"], 0, "hunt for 搜寻。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 22), "Help me ___ this heavy box.", ["lift", "leave", "lose"], 0, "lift 举起。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 23), "Wait ___ the rain stops.", ["until", "before", "after"], 0, "until 直到雨停。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 24), "Please ___ in class.", ["take notes", "take care", "take off"], 0, "take notes 记笔记。"),
    ]
    add_page(eng.section_head("练", "随堂演练 ① · 词汇选择") + make_quiz_grid(q_sec1), 4, "演练①", "词汇选择", priority="CORE", minutes=4)

    q_sec2 = [
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 25), "Let's ___ up after the party.", ["clean", "cleaning", "cleans"], 0, "Let's 接原形 clean。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 26), "We live in a small ___.", ["community", "computer", "company"], 0, "community 社区。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 27), "Please ___ your food with me.", ["share", "shout", "shut"], 0, "share 分享。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 28), "She is ___ at first, then friendly.", ["shy", "loud", "lazy"], 0, "shy 害羞。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 29), "Tom is very ___ and works hard.", ["hard-working", "lazy", "slow"], 0, "hard-working 勤奋。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 30), "They ___ on stage tonight.", ["perform", "prepare", "prefer"], 0, "perform 表演。"),
    ]
    add_page(eng.section_head("练", "随堂演练 ② · 语法综合") + make_quiz_grid(q_sec2), 4, "演练②", "语法综合", priority="CORE", minutes=4)

    # 演练③ 改错专练（错句医生）
    add_page(eng.section_head("练", "随堂演练 ③ · 改错专练") +
             C.sentence_doctor(ERROR_FIX[lesson_num], "找出错词并改正") +
             '<div class="note-panel"><div class="np-title">改错思路</div>先点出错词，再从下方选择正确改法；改对后尽力说出理由。</div>', 4, "演练③", "改错专练", priority="CORE", minutes=4)

    mini_task = (eng.section_head("练", "Mini Task · 主题表达") +
                 '<div class="mini-task-box">' +
                 '<div class="mini-task-header"><span class="mini-task-icon">📋</span><div class="mini-task-title">任务：用本课目标词写一段%s描述</div></div>' % theme +
                 '<div class="mini-task-content">用本课目标词（至少 3 个）写 3-4 句，描述本课主题的相关场景。</div>' +
                 '</div>' +
                 '<div class="note-panel"><div class="np-title">表达支架</div>We help our community together. I borrow tools from my neighbor. We share the work and clean up until everything is done.</div>')
    add_page(mini_task, 4, "Mini Task", "综合运用 · 目标词", priority="CORE", minutes=5)

    # ---- 段5 阅读理解 ----
    sop = (eng.section_head("读", "阅读解题 SOP · 六步法") +
           eng.key_points([("一 先题后文", "先读题干圈关键词，再回原文定位。口诀：先看题，后读文。"),
                           ("二 定位细节", "题干词多在原文原词复现，直接比对。口诀：关键句，划出来。"),
                           ("三 识别主旨", "找首尾句与高频词，避免以偏概全。口诀：首尾段，见主旨。"),
                           ("四 推断判断", "根据证据推结论，不选无依据选项。口诀：有证据，才推断。"),
                           ("五 词义猜测", "利用上下文线索、同义复现猜生词。口诀：看前后，猜词义。"),
                           ("六 复查核对", "核对题目与选项，排除过度推断。口诀：再复查，防陷阱。")]) +
           '<div class="note-panel"><div class="np-title">先讲方法再做题</div>按照六步法完成下面 A/B/C 三篇。答题痕迹标在原文上（可点右上角画笔圈画）。</div>')
    add_page(sop, 5, "阅读解题 SOP", "六步法 · 先讲方法再做题", priority="CORE", minutes=5)

    # 阅读 A（180 词）
    pa_text = ("<b>Passage A (%s 主题) · {{source_id:HN2026_L%d_reading_a}}</b><br>" % (theme, lesson_num) +
        "Last week, our community held a big volunteer day. Everyone in the neighborhood came together to help. Our task was to clean up the park and plant some new flowers. My friend Li Ming and I borrowed some tools from our neighbor, Mr. Wang. He was very kind and let us use his gloves and shovels.<br>"
        "We started early in the morning. The sun was shining, and the birds were singing. We worked until noon without taking a long break. Li Ming took notes about what we still needed to do. He always writes things down carefully, so nothing is forgotten. I lifted the heavy bags of soil and carried them to the flower beds.<br>"
        "After lunch, some women from the community brought us water and snacks. They thanked us for our hard work. We cleaned up all the paper, plastic, and old leaves on the ground. By late afternoon, the park looked clean and beautiful. The new flowers stood bright and colorful in the sunshine.<br>"
        "Everyone felt proud of what we had done together. We learned that sharing the work makes it easier and more fun. The community is like a big family, and every member can help. I was happy because I helped make our neighborhood a better place. I will join the volunteer day again next time.")
    q_pa = [
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 31), "细节题：What did the community hold last week?", ["A volunteer day.", "A birthday party.", "A sports meeting."], 0, "原文定位：our community held a big volunteer day。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 32), "细节题：Who did they borrow tools from?", ["Mr. Wang.", "Li Ming.", "The women."], 0, "原(borrowed tools from our neighbor, Mr. Wang)."),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 33), "推断题：Why does Li Ming take notes?", ["To remember what to do.", "To win a prize.", "To draw pictures."], 0, "由 He always writes things down... nothing is forgotten 推断。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 34), "主旨题：What is the passage mainly about?", ["A community volunteer day.", "How to plant flowers.", "A park's history."], 0, "全文围绕社区志愿日展开。"),
    ]
    pa_html = ('<div class="read-split">'
               '<div class="read-left">'
               '<div class="annotation-bar">'
               '<button class="ann-btn" onclick="setPen(\'red\', \'canvas_L%d_A\')">✏️ 细红笔</button>'
               '<button class="ann-btn" onclick="setPen(\'highlighter\', \'canvas_L%d_A\')">🖍️ 荧光笔</button>'
               '<button class="ann-btn" onclick="setPen(\'eraser\', \'canvas_L%d_A\')">🧹 橡皮</button>'
               '<button class="ann-btn" onclick="setPen(\'clear\', \'canvas_L%d_A\')">🗑️ 清空</button>'
               '</div>'
               '<div class="passage-wrap"><canvas class="read-canvas" id="canvas_L%d_A"></canvas>'
               '<div class="reading-passage">%s</div></div></div>'
               '<div class="read-right">%s</div>'
               '</div>' % (lesson_num, lesson_num, lesson_num, lesson_num, lesson_num, pa_text, make_quiz_grid(q_pa, cols=False)))
    add_page(eng.section_head("阅", "阅读理解 A · 记叙文 (180词 · 双栏+画笔)") + pa_html, 5, "阅读A", "细节理解", priority="CORE", minutes=6)

    # 阅读 B（220 词）
    pb_text = ("<b>Passage B (%s 主题) · {{source_id:HN2026_L%d_reading_b}}</b><br>" % (theme, lesson_num) +
        "Everyone is different, and that is a good thing. Nobody in the world is exactly the same as you. Some people are outgoing and love to talk, while others are shy and quiet. Some are hard-working and always finish their homework on time, and others like to play first and study later. Understanding these differences helps us get along with one another.<br>"
        "In our class, we have two very different friends, Anna and Ben. Anna is outgoing. She likes to perform on stage and often wins a prize at the school talent show. She speaks loudly and clearly, and everyone loves her energy. Ben, on the other hand, is shy. He talks softly and does not like to be in front of many people. But Ben is very smart and hard-working. He always solves the hardest math problems in our group. His ideas often help us finish our projects.<br>"
        "At first, I thought they were too different to be friends. But one day, we had a group project. Anna did the talking and presenting, while Ben solved the problems and did the writing. They worked together so well that we won first prize! I learned that differences are not a problem. They are our strengths. When we compare each other's talents and combine them, we become stronger together.<br>"
        "So, do not be afraid of being different. Whether you are outgoing or shy, lazy or hard-working, you have something special. Attend group activities, share your ideas, and celebrate what makes each person unique. Our differences make the world colorful and interesting, and they help us learn and grow side by side.")
    q_pb = [
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 35), "细节题：What is Anna like?", ["Outgoing.", "Shy.", "Lazy."], 0, "原文：Anna is outgoing。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 36), "细节题：What does Ben do well?", ["Solve math problems.", "Sing songs.", "Play games."], 0, "原文：Ben always solves the hardest math problems。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 37), "推断题：Why did they win first prize?", ["They combined their strengths.", "They were both loud.", "They worked alone."], 0, "由 they worked together so well 推断。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 38), "主旨题：What is the best title?", ["Differences Are Our Strengths", "How to Win a Prize", "A Shy Boy's Story"], 0, "全文主旨为差异是优势。"),
    ]
    pb_html = ('<div class="read-split">'
               '<div class="read-left">'
               '<div class="annotation-bar">'
               '<button class="ann-btn" onclick="setPen(\'red\', \'canvas_L%d_B\')">✏️ 细红笔</button>'
               '<button class="ann-btn" onclick="setPen(\'highlighter\', \'canvas_L%d_B\')">🖍️ 荧光笔</button>'
               '<button class="ann-btn" onclick="setPen(\'clear\', \'canvas_L%d_B\')">🗑️ 清空</button>'
               '</div>'
               '<div class="passage-wrap"><canvas class="read-canvas" id="canvas_L%d_B"></canvas>'
               '<div class="reading-passage">%s</div></div></div>'
               '<div class="read-right">%s</div>'
               '</div>' % (lesson_num, lesson_num, lesson_num, lesson_num, pb_text, make_quiz_grid(q_pb, cols=False)))
    add_page(eng.section_head("阅", "阅读理解 B · 说明文 (220词 · 双栏+画笔)") + pb_html, 5, "阅读B", "说明理解", priority="EXTEND", minutes=6)

    # 阅读 C（260 词 · 任务型）
    pc_text = ("<b>Passage C (%s 主题) · {{source_id:HN2026_L%d_sa}}</b><br>" % (theme, lesson_num) +
        "Nature is a big, connected web. Every living thing plays a role, and each depends on the others. When one part is missing, the whole web can be affected. This is why it is so important to understand how animals, plants, and the environment work together.<br>"
        "Think about bees, for example. Bees are small, but they do a very important job. When a bee visits a flower to drink nectar, tiny grains called pollen stick to its body. When the bee flies to the next flower, it carries this pollen along. This process is called pollination. Through pollination, plants can make new seeds and grow more fruit. Without bees, many plants cannot reproduce, and our food supply would be in great danger.<br>"
        "Plants are not the only ones that need bees. Many animals eat the fruit and seeds that plants produce. Birds, squirrels, and even insects depend on these plants for food. So, when bees help flowers grow, they also help feed the whole ecosystem. Every part of nature is connected in this way.<br>"
        "Unfortunately, the climate is changing, and this affects bees and plants. Warmer weather and pollution make it harder for bees to survive. If we do nothing, we may lose many useful plants and animals. We must protect the environment and care for every living thing. Planting more flowers, using fewer chemicals, and protecting natural areas are simple steps we can take.<br>"
        "In conclusion, everything in nature is connected. Bees, plants, animals, and people all play a role in the ecosystem. When we understand the importance of each part and protect the environment, we help keep the whole world healthy and strong for the future.")
    pc_fill = (eng.section_head("答", "阅读 C · 回答问题（输入判题）") +
               '<div class="body-text">根据短文内容，在输入框内用英文回答下列问题。</div>' +
               '<div class="fill-zone">' +
               '<div class="quiz-q fill-q" data-qid="L%02d_QF1" data-ans="pollination"><div class="fq-text">1. What is the process called when bees carry pollen to flowers?</div>' % lesson_num +
               '<input class="fill-input-box" type="text" placeholder="输入英文答案"><button class="fill-check-btn" onclick="checkFill(this)">提交</button>' +
               '<div class="fill-explain"></div></div>' +
               '<div class="quiz-q fill-q" data-qid="L%02d_QF2" data-ans="bees"><div class="fq-text">2. Which small animals do a very important job in nature?</div>' % lesson_num +
               '<input class="fill-input-box" type="text" placeholder="输入英文答案"><button class="fill-check-btn" onclick="checkFill(this)">提交</button>' +
               '<div class="fill-explain"></div></div>' +
               '<div class="quiz-q fill-q" data-qid="L%02d_QF3" data-ans="protect the environment"><div class="fq-text">3. What must we do to help bees and plants?</div>' % lesson_num +
               '<input class="fill-input-box" type="text" placeholder="输入英文答案"><button class="fill-check-btn" onclick="checkFill(this)">提交</button>' +
               '<div class="fill-explain"></div></div>' +
               '<div class="quiz-q fill-q" data-qid="L%02d_QF4" data-ans="ecosystem"><div class="fq-text">4. What is the big connected web of nature called?</div>' % lesson_num +
               '<input class="fill-input-box" type="text" placeholder="输入英文答案"><button class="fill-check-btn" onclick="checkFill(this)">提交</button>' +
               '<div class="fill-explain"></div></div>' +
               '</div>' +
               '<div class="note-panel"><div class="np-title">任务型阅读</div>本题为阅读回答问题，用英文简答，考查信息定位与表达。</div>')
    pc_html = ('<div class="read-split">'
               '<div class="read-left">'
               '<div class="reading-passage">%s</div></div>'
               '<div class="read-right">%s</div>'
               '</div>' % (pc_text, pc_fill))
    add_page(eng.section_head("阅", "阅读理解 C · 说明文 (260词 · 任务型)") + pc_html, 5, "阅读C", "任务型阅读", priority="HOME", minutes=6)

    # 阅读迁移
    transfer = (eng.section_head("写", "阅读迁移 · 用新词造句") +
                '<div class="body-text">从三篇阅读中用 <span class="highlight">2 个本课目标词</span>各造 1 句，作为写作衔接。</div>' +
                '<div class="note-panel"><div class="np-title">示范</div>① <b>%s</b>: 造一句含该词的句子。<br>② <b>%s</b>: 造一句含该词的句子。</div>' % (words[0][0], words[1][0]) +
                '<div class="mini-task-box"><div class="mini-task-header"><span class="mini-task-icon">✍️</span><div class="mini-task-title">我的造句（写 2 句）</div></div>' +
                '<div class="mini-task-content">1. ______________________<br>2. ______________________</div></div>')
    add_page(transfer, 5, "阅读迁移", "新词造句 · 写作衔接", priority="EXTEND", minutes=4)

    # ---- 段6 听力环节（培优含听力）----
    listen1 = listen_panel("听力 · 主题短文理解", listening,
        [make_quiz_item("L%02d_Q%02d" % (lesson_num, 39), "What is the listening mainly about?", ["Helping the community.", "Buying food.", "Playing games."], 0, "听力围绕主题展开。"),
         make_quiz_item("L%02d_Q%02d" % (lesson_num, 40), "What do they do first?", ["Pick up paper.", "Plant flowers.", "Share work."], 0, "听力提到 First, pick up paper in the park。"),
         make_quiz_item("L%02d_Q%02d" % (lesson_num, 41), "When do they stop working?", ["At twelve o'clock.", "At noon tomorrow.", "At night."], 0, "听力提到 work until twelve o'clock。")])
    add_page(listen1, 6, "听力①", "听音选答", priority="CORE", minutes=5)

    listen2 = (eng.section_head("听", "听力 · 听音辨词") +
               '<div class="body-text">先听发音，再选出对应的单词。</div>' +
               make_quiz_grid([
                   make_quiz_item("L%02d_Q%02d" % (lesson_num, 42), "听音选词：/ʃeə/ 对应：", ["share", "shy", "show"], 0, "share 发音 /ʃeə/。"),
                   make_quiz_item("L%02d_Q%02d" % (lesson_num, 43), "听音选词：/kəˈmjuːnəti/ 对应：", ["community", "company", "computer"], 0, "community 发音 /kəˈmjuːnəti/。"),
               ]))
    add_page(listen2, 6, "听力②", "听音辨词", priority="EXTEND", minutes=4)

    # ---- 段7 课堂游戏 ----
    q_g17_1 = [
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 44), "哪个词表示「分享」？", ["share", "hide", "hunt"], 0, "share 分享。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 45), "哪个词表示「社区」？", ["community", "computer", "climate"], 0, "community 社区。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 46), "哪个词表示「诚实」？", ["honest", "lazy", "loud"], 0, "honest 诚实。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 47), "哪个词表示「保护」？", ["protect", "pretend", "prefer"], 0, "protect 保护。"),
    ]
    add_page(eng.section_head("戏", "课堂游戏 ① · 知识快闪") + make_quiz_grid(q_g17_1), 7, "游戏①", "快速反应", priority="EXTEND", minutes=4)

    q_g17_2 = [
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 48), "听音选词：/ˈtriːʒə/ 对应：", ["treasure", "trouble", "teacher"], 0, "treasure 发音 /ˈtreʒə(r)/。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 49), "听音选词：/pəˈfɔːm/ 对应：", ["perform", "prefer", "prepare"], 0, "perform 发音 /pəˈfɔːm/。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 50), "Bees carry ___ to flowers.", ["pollen", "people", "pencil"], 0, "pollen 花粉。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 51), "Everything is ___ in nature.", ["connected", "collected", "corrected"], 0, "connected 连接。"),
    ]
    add_page(eng.section_head("戏", "课堂游戏 ② · 听音辨词") + make_quiz_grid(q_g17_2), 7, "游戏②", "听音匹配", priority="EXTEND", minutes=4)

    # ---- 段8 课堂总结 ----
    sum_html = (eng.section_head("结", "课堂总结 · 知识图谱") +
                '<div class="kmap">' +
                '<div class="kmap-node"><div class="kn-title">词汇</div><div class="kn-body">%d 个%s主题目标词。</div></div>' % (len(words), tname) +
                '<div class="kmap-node"><div class="kn-title">语法</div><div class="kn-body">%s。</div></div>' % " / ".join([g[2] for g in grammar]) +
                '<div class="kmap-node"><div class="kn-title">阅读</div><div class="kn-body">A/B/C 三篇，覆盖细节与任务型。</div></div>' +
                '<div class="kmap-node"><div class="kn-title">听力</div><div class="kn-body">培优听力 · 听音选答。</div></div>' +
                '</div>' +
                '<div class="note-panel"><div class="np-title">课后作业</div>① 背诵本课目标词；② 完成配套练习；③ 用本课语法各写 2 句；④ 整理错题本。</div>')
    add_page(sum_html, 8, "课堂总结", "知识图谱", priority="CORE", minutes=3)

    q_exit = [
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 52), "%s 意思是：" % words[0][0], [words[0][3], words[1][3], words[2][3]], 0, "%s 意为 %s。" % (words[0][0], words[0][3])),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 53), "%s 意思是：" % words[1][0], [words[1][3], words[0][3], words[3][3]], 0, "%s 意为 %s。" % (words[1][0], words[1][3])),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 54), "We work ___ the work is done.", ["until", "before", "after"], 0, "until 引导时间。"),
        make_quiz_item("L%02d_Q%02d" % (lesson_num, 55), "She is ___ than before.", ["more outgoing", "outgoing", "outgoinger"], 0, "多音节比较用 more。"),
    ]
    add_page(eng.section_head("结", "Exit Ticket · 形成性检测") + make_quiz_grid(q_exit), 8, "Exit Ticket", "检测通关", priority="CORE", minutes=5)

    preview = (eng.section_head("结", "下节课预告") +
               eng.key_points([("词汇", "下一课%s主题新词。" % theme),
                               ("语法", "相关核心语法考点。"),
                               ("阅读", "继续 A/B/C 三篇阅读。"),
                               ("听力", "培优听力训练。")]) +
               '<div class="note-panel"><div class="np-title">课前准备</div>复习本课要点。</div>')
    add_page(preview, 8, "下节课预告", "衔接下一课", priority="EXTEND", minutes=3)

    # ---- 段9 思维导图 ----
    card17 = {
        "lesson": lesson_num,
        "theme": theme,
        "tier": "培优",
        "stage": "S1",
        "student": "李民宪",
        "grammar": [g[1] for g in grammar],
        "phonics": "theme",
        "vocab": {"new_count": len(words)}
    }
    mm_html = (eng.section_head("图", "课堂思维导图 · 本课全貌") +
               '<div class="body-text">点击分支复盘本课 <span class="highlight">词汇 + 语法</span> 核心脉络。</div>' +
               eng.mind_map(card17))
    add_page(mm_html, 9, "思维导图", "互动复盘", priority="CORE", minutes=3)

    mm_full = (eng.section_head("图", "思维导图 · 主题关联图") +
               '<div class="eco-map">' +
               '<div class="eco-node">%s<br>主题</div>' % theme +
               "".join('<div class="eco-node %s">%s<br>%s</div>' % (["", "green", "gold", "blue"][i % 4], w[0], w[3]) for i, w in enumerate(words[:6])) +
               '</div>' +
               '<div class="note-panel"><div class="np-title">课后复盘</div>看着关联图逐项自测：能否读出每个词、讲清每条语法结构。</div>')
    add_page(mm_full, 9, "思维导图 · 主题关联", "对照自测", priority="EXTEND", minutes=3)

    total = p - 1
    seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
    js_extra = ("var studentId='stu_lmx';\n" +
                JS_FULL % (total, json.dumps(seg_pages, ensure_ascii=False),
                           json.dumps(page_meta, ensure_ascii=False)))
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
    html = build_courseware(title="第%02d课时 · " % lesson_num + theme, pages_dict=pages, js_extra=js_extra,
                            session="L%02d" % lesson_num, nav_html=NAV_HTML, stage_badge=stage_badge,
                            n_pages=total, css_extra=CSS_CONTRACT_MARKERS + CSS_FULL + build_theme_css(theme_key))
    html = html.replace(
        '<div class="cover-wrap',
        '<!-- CW-VISUAL-CONTRACT:1 -->\n<div class="cover-wrap',
        1
    )
    return html, total

def main():
    base = os.path.dirname(HERE)
    for lesson_num in [6, 7, 8, 9, 10]:
        html, total = build_lesson(lesson_num)
        folder = os.path.join(base, "李民宪", "第%02d课时" % lesson_num, "课件成品_网页PPT")
        os.makedirs(folder, exist_ok=True)
        out = os.path.join(folder, "第%02d课时_课件_培优.html" % lesson_num)
        with open(out, "w", encoding="utf-8") as f:
            f.write(html)
        size = len(html.encode("utf-8"))
        print("李民宪 L%02d 课件生成：%s (%d bytes, %d pages)" % (lesson_num, out, size, total))
        if size < 150 * 1024:
            print("  [警告] 体积不足 150KB")

if __name__ == "__main__":
    main()