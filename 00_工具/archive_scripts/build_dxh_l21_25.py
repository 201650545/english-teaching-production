# -*- coding: utf-8 -*-
"""邓兴华 L21-L25 课件构建共享模块。
在 courseware_core.build_courseware 基础上，提供：
  1. 共享交互 JS（checkOpt/fillCheck/drag/order/link/flip/undo + IndexedDB 落库）
  2. 共享 CSS（六色卡/翻牌卡/思维导图/拖拽/排序/连线/随堂演练）
  3. 页面构建 helpers（section_head/vocab/quiz/fill/drag/order/link/flip/mind_map/rule_cards）
  4. per-lesson 页面装配 + 写出 HTML
双契约标记：CW-VISUAL-CONTRACT:1 + CW-INTERACTION-CONTRACT:1
"""
import os, json, re, sys, html as _html
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from courseware_core import build_courseware, page as _pg

# ---------------------------------------------------------------
# 共享交互 JS（追加在 CORE_JS 之后；含答案落 IndexedDB + 双击撤销）
# ---------------------------------------------------------------
def js_extra(total, seg_pages, page_meta):
    return JS_EXTRA % (total, json.dumps(seg_pages, ensure_ascii=False),
                       json.dumps(page_meta, ensure_ascii=False))

JS_EXTRA = r"""
/* ==================== 交互增强（L21-25 新建线） ==================== */
var totalPages = %d;
var segmentPages = %s;
var PAGE_META = %s;

/* 初始化 IndexedDB（页面加载即建立连接，答题实时落库） */
if(typeof initDB === 'function'){ initDB(); }

function flipCard(el){
  el.classList.toggle('flipped');
}

/* 彩带动画 */
function burst(el){
  var r=el.getBoundingClientRect(), cx=r.left+r.width/2, cy=r.top+r.height/2;
  for(var i=0;i<12;i++){
    var p=document.createElement('div'); p.className='burst-p';
    var a=Math.random()*6.283, d=40+Math.random()*60;
    p.style.left=cx+'px'; p.style.top=cy+'px';
    p.style.setProperty('--dx',(Math.cos(a)*d)+'px'); p.style.setProperty('--dy',(Math.sin(a)*d)+'px');
    p.style.background=(Math.random()<0.5?'#FFD700':'#E63946');
    document.body.appendChild(p);
    (function(x){ setTimeout(function(){ x.remove(); },700); })(p);
  }
}
function shake(el){ if(!el) return; el.style.animation='none'; void el.offsetWidth; el.style.animation='shake .4s'; }

/* 值域：单选（checkOpt 已在 CORE_JS 之外由本模块提供？不，CORE_JS 无 checkOpt，故在此定义） */
var _LAST_KEY = null;
function checkOpt(btn){
  if(btn && btn.currentTarget && btn.currentTarget.classList && btn.currentTarget.classList.contains('quiz-opt')){
    btn = btn.currentTarget;
  }
  if(!btn || !btn.classList) return;
  var q=btn.parentNode; if(!q) return;
  if(q.dataset.done) return; q.dataset.done='1';
  var opts=q.querySelectorAll('.quiz-opt');
  for(var i=0;i<opts.length;i++){ opts[i].classList.add('locked'); }
  var ok=btn.dataset.correct==='1';
  if(typeof saveAnswer==='function' && q.dataset.qid){
    var qid=q.dataset.qid, ca='';
    for(var j=0;j<opts.length;j++){ if(opts[j].dataset.correct==='1'){ ca=opts[j].textContent.replace(/^[A-E]\.?\s*/,'').trim(); } }
    saveAnswer(qid, btn.textContent.replace(/^[A-E]\.?\s*/,'').trim(), ca, ok);
  }
  if(ok){ btn.classList.add('opt-correct'); playCorrect(); burst(btn); }
  else{
    btn.classList.add('opt-wrong'); playError();
    for(var k=0;k<opts.length;k++){
      if(opts[k].dataset.correct==='1'){ opts[k].classList.add('opt-correct'); }
    }
    var h=q.querySelector('.et-undo-hint');
    if(!h){ h=document.createElement('div'); h.className='et-undo-hint';
            h.onclick=function(ev){ ev.stopPropagation(); }; q.appendChild(h); }
  }
  var fb=q.querySelector('.quiz-feedback');
  if(fb) fb.classList.add('show');
}

/* 双击撤销（答错后可撤回重答） */
function undoQuiz(q){
  if(!q) return;
  q.dataset.done='0';
  var opts=q.querySelectorAll('.quiz-opt');
  for(var i=0;i<opts.length;i++){ opts[i].classList.remove('opt-correct','opt-wrong','locked'); }
  var fb=q.querySelector('.quiz-feedback'); if(fb) fb.classList.remove('show');
  var h=q.querySelector('.et-undo-hint'); if(h) h.remove();
  playPageTurn();
}
document.addEventListener('dblclick', function(e){
  var q=e.target.closest ? e.target.closest('.quiz-q,.quiz-question,.fill-q,.drag-q') : null;
  if(q && q.dataset.done==='1'){ undoQuiz(q); }
});
document.addEventListener('touchstart', function(e){
  var q=e.target.closest ? e.target.closest('.quiz-q,.quiz-question') : null;
  if(q && q.dataset.done==='1'){ undoQuiz(q); }
});

/* 填空判题 */
function fillCheck(btn){
  var q=btn.parentNode; if(!q) return; if(q.dataset.done) return; q.dataset.done='1';
  var inp=q.querySelector('.fill-input'); if(!inp){ q.dataset.done='0'; return; }
  var ans=inp.getAttribute('data-answer')||'';
  var val=inp.value.replace(/^\s+|\s+$/g,'');
  var ok=(val.toLowerCase()===ans.toLowerCase());
  if(typeof saveAnswer==='function' && q.dataset.qid){ saveAnswer(q.dataset.qid, val, ans, ok); }
  if(ok){ inp.classList.add('correct'); playCorrect(); burst(inp); }
  else{ inp.classList.add('wrong'); playError(); q.querySelector('.fill-answer').classList.add('show'); }
}

/* 拖拽填空 */
function pickWord(word){
  var w=word.target||word.currentTarget||word;
  if(w.classList.contains('fill-check-btn')) return;
  if(w.classList.contains('drag-word')){
    if(w.classList.contains('used')) return;
    var slots=document.querySelectorAll('.drag-slot');
    for(var i=0;i<slots.length;i++){
      if(!slots[i].getAttribute('data-filled')){
        slots[i].textContent=w.textContent;
        slots[i].setAttribute('data-filled','1');
        slots[i].setAttribute('data-word',w.textContent);
        w.classList.add('used');
        return;
      }
    }
  }
}
function dragSubmit(btn){
  var cont=btn.getAttribute('data-target')?document.getElementById(btn.getAttribute('data-target')):btn.parentNode;
  if(!cont) cont=btn.parentNode;
  var slots=cont.querySelectorAll('.drag-slot');
  var ok=true;
  var all=true;
  slots.forEach(function(s){
    s.classList.remove('correct','wrong');
    if(!s.getAttribute('data-filled')){ all=false; return; }
    var expect=s.getAttribute('data-expect');
    var got=s.getAttribute('data-word');
    if(expect && got && got.trim().toLowerCase()===expect.trim().toLowerCase()){ s.classList.add('correct'); }
    else{ s.classList.add('wrong'); ok=false; }
  });
  if(!all){ alert('请先把所有空格填满'); return; }
  if(typeof saveAnswer==='function' && cont.getAttribute('data-qid')){ saveAnswer(cont.getAttribute('data-qid'), ok?'全部正确':'有误','全部正确',ok); }
  if(ok){ playCorrect(); burst(btn); cont.classList.add('solved'); }
  else{ playError(); shake(cont); }
}

/* 排序判题 */
function moveUp(btn){
  var li=btn.parentNode.parentNode; var ul=li.parentNode;
  if(li.previousElementSibling) ul.insertBefore(li, li.previousElementSibling);
}
function moveDown(btn){
  var li=btn.parentNode.parentNode; var ul=li.parentNode;
  if(li.nextElementSibling) ul.insertBefore(li, li.nextElementSibling);
}
function orderCheck(btn){
  var cont=btn.parentNode.parentNode;
  var items=cont.querySelectorAll('.order-item');
  var key=cont.getAttribute('data-key')||'';
  var seq=[]; items.forEach(function(it){ seq.push(it.getAttribute('data-val')); });
  var ok=(seq.join('|')===key);
  if(typeof saveAnswer==='function' && cont.getAttribute('data-qid')){ saveAnswer(cont.getAttribute('data-qid'), seq.join(','), key.replace(/\|/g,','), ok); }
  if(ok){ playCorrect(); burst(btn); cont.classList.add('solved');
    items.forEach(function(it){ it.classList.add('ok'); });
  } else { playError(); shake(cont); cont.classList.add('show-ans'); }
}

/* 连线题：点击左右列配对 */
function matchPick(btn){
  var m=btn.getAttribute('data-match'); if(!m) return;
  var col=btn.parentNode;
  var sel=col.querySelector('.selected');
  if(sel){ sel.classList.remove('selected'); if(sel===btn){ return; } }
  btn.classList.add('selected');
  var cont=btn.parentNode.parentNode;
  var left=cont.querySelector('.mcol-l'), right=cont.querySelector('.mcol-r');
  var lsel=left.querySelector('.selected'), rsel=right.querySelector('.selected');
  if(lsel && rsel){
    var ok=(lsel.getAttribute('data-match')===rsel.getAttribute('data-match'));
    if(typeof saveAnswer==='function' && cont.getAttribute('data-qid')){
      saveAnswer(cont.getAttribute('data-qid'), lsel.textContent+'→'+rsel.textContent, lsel.getAttribute('data-match'), ok);
    }
    if(ok){ lsel.classList.add('matched'); rsel.classList.add('matched'); lsel.classList.remove('selected'); rsel.classList.remove('selected');
            playCorrect(); burst(lsel); }
    else{ lsel.classList.remove('selected'); rsel.classList.remove('selected'); playError(); shake(lsel); }
  }
}

/* 翻牌卡（词汇自检） */
function flipCard2(el){ el.classList.toggle('flipped'); }

/* 思维导图分支展开 */
document.addEventListener('click', function(e){
  var mm=e.target.closest ? e.target.closest('.mm-branch') : null;
  if(mm){ mm.classList.toggle('open'); }
});

/* 音效按钮（无音频文件，用 Web Audio 提示音） */
function playHint(){ playPageTurn(); }
"""

# ---------------------------------------------------------------
# 共享 CSS（含六色卡 6/6）
# ---------------------------------------------------------------
CSS_EXTRA = """
/* <CW-CSS-EXTRA */
/* <CW-SECTION name="components"> */
/* THEME: dengxinghua-L21-25 teaching (red-gold · warm cream) */
/* ==================== 新建线设计层（L21-25） ==================== */
/* 六色卡约束：rule-card rc-zhug / rc-bin / rc-xing / rc-ming / rc-warn / rc-qita */
.rule-card{padding:14px 18px;border-radius:12px;margin:10px 0;box-shadow:0 2px 10px rgba(0,0,0,.06);}
.rule-card.rc-zhug{background:#E8F0FE;border-left:5px solid #1A73E8;}
.rule-card.rc-bin{background:#E6F4EA;border-left:5px solid #188038;}
.rule-card.rc-xing{background:#FEF7E0;border-left:5px solid #F9AB00;}
.rule-card.rc-ming{background:#FCE8E6;border-left:5px solid #E5252B;}
.rule-card.rc-warn{background:#F3E8FD;border-left:5px solid #9334E6;}
.rule-card.rc-qita{background:#E0F7FA;border-left:5px solid #12B2B8;}
.rule-card .rc-title{font-size:20px;font-weight:700;margin-bottom:6px;}
.rule-card .rc-body{font-size:18px;line-height:1.7;}

.section-head{display:flex;align-items:center;gap:10px;margin:6px 0 14px;}
.section-head .sh-icon{width:40px;height:40px;border-radius:10px;background:#E63946;color:#fff;display:flex;align-items:center;justify-content:center;font-size:20px;}
.section-head .sh-num{font-size:15px;font-weight:700;color:#E63946;background:rgba(230,57,70,.08);border:1px solid #E63946;border-radius:8px;padding:1px 8px;}
.section-head .sh-title{font-size:28px;font-weight:700;color:#1A1A2E;}
.section-head .sh-tag{font-size:14px;background:#FFD700;color:#333;padding:2px 10px;border-radius:10px;}

.sub-label{font-size:15px;color:#666;margin:6px 0 10px;}

/* 正文段落 / 高亮 / 笔记面板 / 双列选择 */
.body-text{font-size:18px;line-height:1.8;color:#333;background:#FFF8F0;border-left:4px solid #E63946;padding:12px 16px;border-radius:8px;margin:10px 0;}
.highlight{background:#FFF3CD;color:#856404;padding:2px 8px;border-radius:6px;font-weight:600;}
.note-panel{background:#FFF8E1;border-left:5px solid #F9AB00;border-radius:10px;padding:14px 18px;margin:10px 0;box-shadow:0 2px 10px rgba(0,0,0,.06);}
.note-panel .np-title{font-size:19px;font-weight:700;color:#B8860B;margin-bottom:6px;}
.note-panel .np-body{font-size:17px;line-height:1.7;color:#555;}
.quiz-cols{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.flash-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:10px 0;}

/* 随堂演练 / 选择 */
.quiz-q{background:#fff;border-radius:10px;padding:14px 18px;margin:10px 0;box-shadow:0 2px 10px rgba(0,0,0,.06);}
.qq-text{font-size:19px;font-weight:600;margin-bottom:8px;}
.quiz-opt{display:block;width:100%;text-align:left;padding:9px 14px;border:2px solid #ddd;border-radius:8px;font-size:17px;margin:5px 0;cursor:pointer;background:#fff;transition:all .2s;}
.quiz-opt:hover{border-color:#E63946;background:rgba(230,57,70,.04);}
.quiz-opt.locked{pointer-events:none;}
.quiz-opt.opt-correct{border-color:#06A77D;background:#E8F5E9;color:#06A77D;font-weight:700;}
.quiz-opt.opt-wrong{border-color:#E63946;background:#FFEBEE;color:#E63946;}
.quiz-feedback{display:none;margin-top:8px;padding:8px 12px;background:#FFF8E1;border-radius:6px;font-size:15px;color:#B8860B;}
.quiz-feedback.show{display:block;}
.et-undo-hint{font-size:11px;color:#8B7D6B;opacity:.75;margin:4px 0;cursor:pointer;text-align:right;}

/* 填空 */
.fill-q{background:#fff;border-radius:10px;padding:14px 18px;margin:10px 0;box-shadow:0 2px 10px rgba(0,0,0,.06);}
.fill-input{width:160px;padding:6px 12px;border:2px solid #ddd;border-radius:6px;font-size:18px;margin:0 6px;}
.fill-input:focus{border-color:#E63946;}
.fill-input.correct{border-color:#06A77D;background:#E8F5E9;}
.fill-input.wrong{border-color:#E63946;background:#FFEBEE;}
.fill-check-btn{padding:6px 16px;background:#FFD700;color:#333;border:none;border-radius:6px;font-size:16px;font-weight:700;cursor:pointer;margin-left:6px;}
.fill-answer{display:none;font-size:16px;color:#06A77D;font-weight:600;margin-top:4px;}
.fill-answer.show{display:block;}

/* 拖拽填空 */
.drag-container{background:#fff;border-radius:10px;padding:14px;margin:10px 0;box-shadow:0 2px 10px rgba(0,0,0,.06);}
.drag-words{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:10px;min-height:44px;padding:8px;background:#FFF8E1;border-radius:8px;}
.drag-word{padding:8px 16px;background:#E63946;color:#fff;border-radius:8px;font-size:16px;cursor:pointer;user-select:none;transition:all .15s;}
.drag-word:hover{background:#FF6B6B;}
.drag-word.used{opacity:.35;cursor:default;pointer-events:none;}
.drag-slot{display:inline-block;min-width:80px;height:36px;border:2px dashed #ccc;border-radius:6px;margin:0 4px;vertical-align:middle;text-align:center;line-height:32px;font-size:16px;}
.drag-slot.correct{border-color:#06A77D;border-style:solid;background:rgba(76,175,80,.1);}
.drag-slot.wrong{border-color:#E63946;border-style:solid;background:rgba(244,67,54,.1);}
.drag-submit{padding:8px 20px;background:#FFD700;color:#333;border:none;border-radius:8px;font-size:17px;font-weight:700;cursor:pointer;margin-top:8px;}
.drag-submit:hover{background:#FFE66D;}

/* 排序 */
.order-container{background:#fff;border-radius:10px;padding:14px;margin:10px 0;box-shadow:0 2px 10px rgba(0,0,0,.06);}
.order-list{list-style:none;padding:0;}
.order-item{display:flex;align-items:center;gap:8px;background:#FFF8E1;border:2px solid #f0e0d0;border-radius:8px;padding:8px 12px;margin:6px 0;}
.order-item .o-text{flex:1;font-size:17px;}
.order-item.ok{border-color:#06A77D;background:#E8F5E9;}
.order-item button{padding:4px 10px;background:#E63946;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:14px;}
.order-check{padding:8px 20px;background:#FFD700;color:#333;border:none;border-radius:8px;font-size:17px;font-weight:700;cursor:pointer;margin-top:8px;}
.order-ans{display:none;font-size:16px;color:#06A77D;font-weight:600;margin-top:6px;}
.order-container.show-ans .order-ans{display:block;}

/* 连线 */
.match-container{background:#fff;border-radius:10px;padding:14px;margin:10px 0;box-shadow:0 2px 10px rgba(0,0,0,.06);display:flex;gap:30px;justify-content:center;}
.match-column{display:flex;flex-direction:column;gap:10px;min-width:240px;}
.match-item{padding:10px 16px;background:#fff;border:2px solid #ddd;border-radius:8px;font-size:16px;cursor:pointer;transition:all .2s;text-align:center;}
.match-item:hover{border-color:#E63946;}
.match-item.selected{border-color:#FFD700;background:rgba(255,215,0,.15);}
.match-item.matched{border-color:#06A77D;background:#E8F5E9;pointer-events:none;}

/* 翻牌卡 */
.flip-card{perspective:1000px;height:120px;cursor:pointer;}
.flip-card-inner{position:relative;width:100%;height:100%;transition:transform .6s;transform-style:preserve-3d;}
.flip-card.flipped .flip-card-inner{transform:rotateY(180deg);}
.flip-card-front,.flip-card-back{position:absolute;width:100%;height:100%;backface-visibility:hidden;border-radius:10px;padding:12px;display:flex;flex-direction:column;justify-content:center;align-items:center;box-shadow:0 2px 10px rgba(0,0,0,.08);}
.flip-card-front{background:#fff;border-left:5px solid #E63946;font-size:20px;font-weight:700;}
.flip-card-back{background:#E8F5E9;border-left:5px solid #06A77D;transform:rotateY(180deg);font-size:18px;text-align:center;}
.flip-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:10px 0;}

/* 词汇卡片 */
.vocab-grid{display:grid;grid-template-columns:repeat(2,1fr);gap:10px;margin:10px 0;}
.vocab-card{background:#fff;border-radius:10px;padding:12px 16px;box-shadow:0 2px 10px rgba(0,0,0,.06);border-left:4px solid #E63946;}
.vocab-card:nth-child(even){border-left-color:#FFD700;}
.vocab-head{display:flex;align-items:center;gap:8px;margin-bottom:4px;}
.vocab-word{font-size:22px;font-weight:700;color:#E63946;}
.vocab-phonetic{font-size:15px;color:#666;font-style:italic;}
.vocab-pos{font-size:13px;background:#E63946;color:#fff;padding:1px 8px;border-radius:8px;}
.vocab-cn{font-size:18px;font-weight:600;margin-bottom:2px;}
.vocab-collocation{font-size:14px;color:#666;}
.vocab-example{font-size:14px;color:#333;font-style:italic;}

/* 思维导图 */
.mm-wrap{background:#fff;border-radius:14px;padding:18px;margin:10px 0;box-shadow:0 2px 10px rgba(0,0,0,.06);}
.mm-head{font-size:24px;font-weight:700;color:#E63946;text-align:center;margin-bottom:14px;}
.mm-branches{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;}
.mm-branch{border-radius:10px;padding:12px;cursor:pointer;border-top:4px solid #E63946;background:#FFF8F0;}
.mm-branch:nth-child(2){border-top-color:#1A73E8;}
.mm-branch:nth-child(3){border-top-color:#188038;}
.mm-branch:nth-child(4){border-top-color:#F9AB00;}
.mm-branch:nth-child(5){border-top-color:#9334E6;}
.mm-branch:nth-child(6){border-top-color:#12B2B8;}
.mm-branch-title{font-size:18px;font-weight:700;margin-bottom:6px;}
.mm-branch .mm-items{font-size:15px;color:#555;line-height:1.6;}

/* 关键词地图 kmap（考点关键词分级） */
.kmap{background:#fff;border-radius:14px;padding:18px;margin:10px 0;box-shadow:0 2px 10px rgba(0,0,0,.06);border-top:5px solid #1A73E8;}
.kmap .kmap-title{font-size:20px;font-weight:700;color:#1A73E8;margin-bottom:12px;text-align:center;}
.kmap-nodes{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;}
.kmap-node{border-radius:10px;padding:12px;text-align:center;border-top:4px solid #E63946;background:#FFF8F0;}
.kmap-node:nth-child(2){border-top-color:#188038;}
.kmap-node:nth-child(3){border-top-color:#F9AB00;}
.kmap-node .kn-title{font-size:18px;font-weight:700;margin-bottom:6px;}
.kmap-node .kn-body{font-size:15px;color:#555;line-height:1.5;}

/* 拓展卡 ext-card */
.ext-card{background:#fff;border-radius:12px;padding:14px 18px;margin:10px 0;box-shadow:0 2px 10px rgba(0,0,0,.06);border-left:5px solid #12B2B8;}
.ext-card .ext-cat{display:inline-block;background:#12B2B8;color:#fff;padding:2px 12px;border-radius:12px;font-size:14px;font-weight:700;margin-bottom:6px;}
.ext-card .ext-body{font-size:17px;color:#333;line-height:1.7;}

/* 游戏面板 */
.game-board{background:#fff;border-radius:14px;padding:16px;margin:10px 0;box-shadow:0 2px 10px rgba(0,0,0,.06);}
.game-title{font-size:20px;font-weight:700;color:#E63946;margin-bottom:6px;}
.game-rule{font-size:15px;color:#666;margin-bottom:10px;}

/* 随堂演练 / 结果 */
.stats-panel{display:flex;gap:12px;justify-content:center;margin:12px 0;}
.stats-card{background:#fff;border-radius:10px;padding:10px 20px;text-align:center;box-shadow:0 2px 10px rgba(0,0,0,.06);min-width:110px;}
.stats-card .stats-num{font-size:32px;font-weight:700;color:#E63946;}
.stats-card .stats-label{font-size:14px;color:#666;margin-top:2px;}

/* 表 */
.content-table{width:100%;border-collapse:collapse;margin:12px 0;font-size:17px;}
.content-table thead{background:#E63946;color:#fff;}
.content-table th,.content-table td{padding:8px 10px;border-bottom:1px solid #f0e0d0;text-align:center;}

/* 遮罩/进度 */
.modal-overlay{display:none;position:fixed;inset:0;background:rgba(0,0,0,.4);z-index:2000;}
.modal-overlay.show{display:flex;align-items:center;justify-content:center;}
.modal-content{background:#fff;border-radius:12px;padding:20px;max-width:600px;width:90%;}
.page-counter{position:fixed;bottom:12px;right:20px;z-index:1001;background:rgba(255,255,255,.9);padding:6px 14px;border-radius:12px;font-size:14px;font-weight:600;box-shadow:0 2px 8px rgba(0,0,0,.1);}
.export-btn{position:fixed;bottom:12px;left:20px;z-index:1001;background:#E63946;color:#fff;padding:6px 14px;border-radius:12px;font-size:14px;font-weight:600;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.2);}

/* 动画 */
.opt-correct,.opt-wrong{animation:none;}
.burst-p{position:fixed;width:10px;height:10px;border-radius:50%;pointer-events:none;z-index:3000;animation:burstFly .7s ease-out forwards;}
@keyframes burstFly{0%{transform:translate(0,0) scale(1);opacity:1;}100%{transform:translate(var(--dx),var(--dy)) scale(.3);opacity:0;}}
@keyframes shake{0%,100%{transform:translateX(0);}25%{transform:translateX(-6px);}75%{transform:translateX(6px);}}

/* 防越级/无翻页过渡动画（翻页用淡入，无滑动偏移） */
.page.active{animation:pageFade .35s ease-out;}
@keyframes pageFade{from{opacity:0;}to{opacity:1;}}

/* 封面（L21 讲评课） */
.cover-wrap{text-align:center;padding:20px 0;}
.cover-badge{display:inline-block;background:#E63946;color:#fff;padding:6px 20px;border-radius:20px;font-size:16px;font-weight:700;letter-spacing:1px;margin-bottom:18px;}
.cover-title{font-size:44px;font-weight:700;color:#E63946;margin-bottom:10px;}
.cover-sub{font-size:20px;color:#555;margin-bottom:20px;}
.cover-tagline{display:inline-block;background:#FFD700;color:#333;padding:4px 18px;border-radius:16px;font-size:15px;font-weight:700;margin-bottom:18px;}
.cover-info{display:flex;gap:16px;justify-content:center;margin-bottom:20px;flex-wrap:wrap;}
.cover-info-num{background:#fff;padding:12px 26px;border-radius:12px;box-shadow:0 2px 10px rgba(0,0,0,.08);border-top:3px solid #FFD700;text-align:center;}
.ci-label{font-size:13px;color:#666;}
.ci-val{font-size:30px;font-weight:700;color:#E63946;}
.cover-emoji{font-size:48px;margin-top:10px;}

/* <CW-SECTION name="theme"> */
/* 主题变量（红金暖色系 · 亮色） */
/* </CW-CSS-EXTRA> */

@media (prefers-reduced-motion: reduce){
  *{animation:none !important;transition:none !important;}
}
"""

# ---------------------------------------------------------------
# 页面 helpers
# ---------------------------------------------------------------
def esc(t):
    return _html.escape(str(t))

_SECSEQ = [0]
def section_head(icon, title, tag="", num=""):
    tag_html = '<span class="sh-tag">%s</span>' % esc(tag) if tag else ""
    num_html = '<span class="sh-num">%s</span>' % esc(num) if num else ""
    return ('<div class="section-head"><div class="sh-icon">%s</div>%s<div class="sh-title">%s</div>%s</div>'
            % (esc(icon), num_html, esc(title), tag_html))

def sub_label(t):
    return '<div class="sub-label">%s</div>' % esc(t)

def body_text(t):
    return '<div class="body-text">%s</div>' % t

def hl(t):
    return '<span class="highlight">%s</span>' % esc(t)

def note_panel(title, body):
    return ('<div class="note-panel"><div class="np-title">%s</div><div class="np-body">%s</div></div>'
            % (esc(title), body))

def kmap_block(title, nodes):
    """nodes: list of (kn_title, kn_body)"""
    html = '<div class="kmap"><div class="kmap-title">%s</div><div class="kmap-nodes">' % esc(title)
    for t, b in nodes:
        html += ('<div class="kmap-node"><div class="kn-title">%s</div><div class="kn-body">%s</div></div>'
                 % (esc(t), b))
    html += '</div></div>'
    return html

def ext_card(cat, body):
    return ('<div class="ext-card"><span class="ext-cat">%s</span><div class="ext-body">%s</div></div>'
            % (esc(cat), body))

def vocab_cards(words):
    """words: list of (en, ph, pos, cn, coll, ex)"""
    out = []
    for en, ph, pos, cn, coll, ex in words:
        out.append('<div class="vocab-card"><div class="vocab-head"><span class="vocab-word">%s</span>'
                   '<span class="vocab-phonetic">%s</span><span class="vocab-pos">%s</span></div>'
                   '<div class="vocab-cn">%s</div><div class="vocab-collocation">搭配：%s</div>'
                   '<div class="vocab-example">%s</div></div>' %
                   (esc(en), esc(ph), esc(pos), esc(cn), esc(coll), esc(ex)))
    return '<div class="vocab-grid">' + "\n".join(out) + '</div>'

_QSEQ = [0]
def quiz_html(questions):
    """questions: list of (stem, correct_text, list_of_distractors)"""
    letters = ["A","B","C","D"]
    out = []
    for stem, correct, distractors in questions:
        _QSEQ[0] += 1
        n = len(distractors) + 1
        opts = distractors[:]
        # 正确项按全局题序号循环摆放，保证整卷答案分布均衡（任一项占比≤40%）
        pos = (_QSEQ[0] - 1) % (len(opts) + 1)
        opts.insert(pos, correct)
        qid = "Q%03d" % _QSEQ[0]
        out.append('<div class="quiz-q" data-qid="%s"><div class="qq-text">%s</div>' % (qid, stem))
        for letter, text in zip(letters, opts):
            cor = "1" if text == correct else "0"
            out.append('<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, esc(text)))
        out.append('</div>')
    return "\n".join(out)

def fill_q(question, answer, qid=None):
    """混合选择填空：question 含 ___，answer 为正确词，但此处用输入的 fill 结构"""
    if not qid:
        _QSEQ[0] += 1; qid = "Q%03d" % _QSEQ[0]
    return ('<div class="fill-q quiz-q" data-qid="%s"><div class="qq-text">%s <input class="fill-input" data-answer="%s">'
            '<button class="fill-check-btn" onclick="fillCheck(this)">检查</button></div>'
            '<div class="fill-answer">答案：%s</div></div>') % (qid, question, esc(answer), esc(answer))

def drag_q(sentence_slots, words, qid=None):
    """sentence_slots: [(pre, expect, post)], words: list of options"""
    if not qid:
        _QSEQ[0] += 1; qid = "Q%03d" % _QSEQ[0]
    html = '<div class="drag-container quiz-q" data-qid="%s"><div class="drag-words">' % (qid)
    for w in words:
        html += '<span class="drag-word" onclick="pickWord(this)">%s</span>' % esc(w)
    html += '</div><div class="qq-text">'
    for pre, expect, post in sentence_slots:
        html += esc(pre) + ' <span class="drag-slot" data-expect="%s"></span> ' % esc(expect) + esc(post)
    html += '</div>'
    html += '<button class="drag-submit" onclick="dragSubmit(this)">提交</button>'
    html += '<div class="sub-label">（先点上方词块填入，再点提交）</div></div>'
    return html

def order_q(title, items, key, qid=None):
    """items: list of (val,text)"""
    if not qid:
        _QSEQ[0] += 1; qid = "Q%03d" % _QSEQ[0]
    html = '<div class="order-container" data-qid="%s" data-key="%s"><div class="qq-text">%s</div>' % (qid, esc(key), esc(title))
    html += '<ul class="order-list">'
    for val, text in items:
        html += ('<li class="order-item" data-val="%s"><button onclick="moveUp(this)">▲</button>'
                 '<button onclick="moveDown(this)">▼</button>'
                 '<span class="o-text">%s</span></li>') % (esc(val), esc(text))
    html += '</ul><button class="order-check" onclick="orderCheck(this)">检查顺序</button>'
    html += '<div class="order-ans">正确顺序：%s</div></div>' % esc(key.replace("|"," → "))
    return html

def match_q(left, right, qid=None):
    """left/right: list of (match, text)"""
    if not qid:
        _QSEQ[0] += 1; qid = "Q%03d" % _QSEQ[0]
    html = '<div class="match-container" data-qid="%s"><div class="match-column mcol-l">' % (qid)
    for m, t in left:
        html += '<div class="match-item" data-match="%s" onclick="matchPick(this)">%s</div>' % (esc(m), esc(t))
    html += '</div><div class="match-column mcol-r">'
    for m, t in right:
        html += '<div class="match-item" data-match="%s" onclick="matchPick(this)">%s</div>' % (esc(m), esc(t))
    html += '</div></div>'
    return html

def flip_grid(words):
    """words: list of (front, back)"""
    html = '<div class="flip-grid">'
    for f, b in words:
        html += ('<div class="flip-card" onclick="flipCard(this)"><div class="flip-card-inner">'
                 '<div class="flip-card-front">%s</div><div class="flip-card-back">%s</div></div></div>') % (esc(f), esc(b))
    html += '</div>'
    return html

def rule_cards(cards):
    """cards: list of (cls6, title, body) 其中 cls6 ∈ zhug/bin/xing/ming/warn/qita"""
    out = []
    order = ["zhug","bin","xing","ming","warn","qita"]
    for cls6, title, body in cards:
        out.append('<div class="rule-card rc-%s"><div class="rc-title">%s</div><div class="rc-body">%s</div></div>' %
                   (cls6, esc(title), body))
    return "\n".join(out)

def mind_map(lesson, theme, branches):
    """branches: list of (title, items_html)"""
    html = '<div class="mm-wrap"><div class="mm-head">L%d · %s · 思维导图</div><div class="mm-branches">' % (lesson, esc(theme))
    for title, items in branches:
        html += '<div class="mm-branch"><div class="mm-branch-title">%s</div><div class="mm-items">%s</div></div>' % (esc(title), items)
    html += '</div></div>'
    return html

def game_board(title, icon, rule, inner):
    return ('<div class="game-board"><div class="game-title">%s %s</div><div class="game-rule">%s</div>%s</div>'
            % (esc(icon), esc(title), esc(rule), inner))

def stats_panel(items):
    html = '<div class="stats-panel">'
    for num, label in items:
        html += '<div class="stats-card"><div class="stats-num">%s</div><div class="stats-label">%s</div></div>' % (esc(num), esc(label))
    html += '</div>'
    return html

# ---------------------------------------------------------------
# 写出
# ---------------------------------------------------------------
def write_courseware(lesson, title, pages, nav, stage_badge, css_extra, js_extra, out_path, session=None):
    if session is None:
        session = "L%02d" % lesson
    html = build_courseware(title=title, pages_dict=pages, js_extra=js_extra,
                            session=session, nav_html=nav,
                            stage_badge=stage_badge, n_pages=max(pages.keys()),
                            css_extra=css_extra)
    # 双契约标记
    html = html.replace('<div class="cover-wrap', '<!-- CW-VISUAL-CONTRACT:1 -->\n<!-- CW-INTERACTION-CONTRACT:1 -->\n<div class="cover-wrap', 1)
    if '<!-- CW-INTERACTION-CONTRACT:1 -->' not in html:
        html = html.replace('<!-- CW-VISUAL-CONTRACT:1 -->', '<!-- CW-VISUAL-CONTRACT:1 -->\n<!-- CW-INTERACTION-CONTRACT:1 -->', 1)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    open(out_path, "w", encoding="utf-8").write(html)
    return len(html.encode("utf-8"))