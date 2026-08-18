# -*- coding: utf-8 -*-
"""M8 装配器（L5 基线版 · 通用化大部分完成）—— 2026-08-03 状态声明
输入课程卡 -> 45 页 HTML -> verify_v2 全过。

【当前状态（如实声明，2026-08-03）】
本模块以 L5（食物主题 · 祈使句/What/like）为基线，通用化已在阶段A/B/C 完成：
  1. 主题：主题词库、学习目标、配色、新词/拓展、随堂演练、一览表 -> 由 card 语法/词汇/主题字段驱动
  2. 语法：考点可视化（结构图/一览表/汇总卡/思维导图分支）-> grammar_bank 六色卡驱动
  3. 复习/预告：上节课复习 与 下节课预告 -> lesson_map 读前/后课卡驱动，「上一课/下一课」契约
  4. 阅读 A/B：语篇与题目 -> passage_bank 按课号选择（无匹配回退 L5 基线篇）
  5. 封面信息卡：由 card 主题字段驱动
【仍为基线/待办（如实声明）】
  1. 阅读 C 五选四：语篇库 w5 条目题目为空（选项「待生成」），暂沿用 L5 基线五选四，待语篇库补选项后交付
  2. 上节课复习语法题：由上一课卡语法名 + grammar_bank 易错题生成，语料缺失时回退 L4 基线数据
  3. 阶段D 跨主题回归：school / family 两非食物主题已通过（见 check_b4_regression.py）

仅调用 courseware_core.py（不改底座）；复用 gen_l1_l13_v2.py 的 L4 复习数据。
"""
import json, os, re, importlib.util, html
HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = "D:/英语教学/01_数据"

spec = importlib.util.spec_from_file_location("g", os.path.join(HERE, "gen_l1_l13_v2.py"))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
# C3 第一批 3 组件（GM-V02/G03/R06）：HTML 在 components.py，JS/CSS 由本引擎统一注入
specc = importlib.util.spec_from_file_location("components", os.path.join(HERE, "components.py"))
C = importlib.util.module_from_spec(specc); specc.loader.exec_module(C)
CSS_EXTRA = g.CSS_EXTRA  # 基线（section-head/kp-grid 等），下面追加设计层
# 交互 JS：checkOpt 增强（答对彩带 + 答错晃动 + 高亮正确）+ 翻牌
JS_EXTRA_TPL = r"""
var totalPages = %d;
var segmentPages = %s;
var PAGE_META = %s;
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
function checkOpt(btn){
  // 兼容旧调用：若传入的事件对象（checkOpt(event)），用 currentTarget 取回绑定的按钮元素
  if(btn && btn.currentTarget && btn.currentTarget.classList && btn.currentTarget.classList.contains('quiz-opt')){
    btn = btn.currentTarget;
  }
  var q=btn.parentNode; if(q.dataset.done) return; q.dataset.done='1';
  var opts=q.querySelectorAll('.quiz-opt');
  // 不再 disabled（disabled 会吞掉 dblclick 事件），改用 locked 视觉锁定 + dataset 防重答
  for(var i=0;i<opts.length;i++){ opts[i].classList.add('locked'); }
  var ok=btn.dataset.correct==='1';
  // 先保存再反馈（08 规范：先入库后反馈）；缺 qid 的旧结构题（如五选四 .w5-opts）跳过
  if(typeof saveAnswer==='function' && q.dataset.qid){
    var qid=q.dataset.qid, ca='';
    for(var j=0;j<opts.length;j++){ if(opts[j].dataset.correct==='1'){ ca=opts[j].textContent.replace(/^[A-E]\.\s*/,'').trim(); } }
    saveAnswer(qid, btn.textContent.replace(/^[A-E]\.\s*/,'').trim(), ca, ok,
               parseInt(q.dataset.attempt||'1',10), 0, false);
  }
  if(ok){ btn.classList.add('opt-correct'); playCorrect(); burst(btn); }
  else{ q.dataset.wrong='1'; btn.classList.add('opt-wrong'); playError(); shake(btn);
    for(var i=0;i<opts.length;i++){ if(opts[i].dataset.correct==='1'){ opts[i].classList.add('opt-correct'); } }
    var h=q.querySelector('.et-undo-hint');
    if(!h){ h=document.createElement('div'); h.className='et-undo-hint'; h.onclick=function(ev){ ev.stopPropagation(); }; q.appendChild(h); }
    h.textContent='答错后双击可撤销回答';
  }
}
function undoQuiz(q){
  var opts=q.querySelectorAll('.quiz-opt');
  for(var i=0;i<opts.length;i++){ opts[i].classList.remove('opt-correct','opt-wrong','locked'); }
  delete q.dataset.done; delete q.dataset.wrong;
  q.dataset.attempt=String(parseInt(q.dataset.attempt||'1',10)+1); // 重答新增尝试，首次答案不覆盖（§3.8）
  var h=q.querySelector('.et-undo-hint');
  if(h){ h.textContent='已撤销，请重答'; setTimeout(function(){ if(h.parentNode) h.parentNode.removeChild(h); }, 3000); }
}
// §3.8.2 答错后双击撤销（容错交互）：双击错题选项（或小字提示）立即复原重答
document.addEventListener('dblclick', function(e){
  var q=e.target.closest('.quiz-q');
  if(q && q.dataset.done==='1' && q.dataset.wrong==='1') undoQuiz(q);
});
function mmToggle(node){
  var br=node.parentNode;
  var all=document.querySelectorAll('.mm-branch.active');
  for(var i=0;i<all.length;i++){ all[i].classList.remove('active'); }
  br.classList.add('active');
  var panel=document.getElementById('mmPanel');
  document.getElementById('mmPanelChips').innerHTML = br.querySelector('.mm-chips').innerHTML;
  document.getElementById('mmPanelTitle').innerHTML = node.querySelector('.mm-icon').textContent + ' ' + node.querySelector('.mm-label').textContent;
  panel.className = 'mm-panel ' + br.getAttribute('data-color');
}
// 启动 IndexedDB（§3.8 数据采集）；脚本在 body 末尾，DOM 已就绪，initDB 由 CORE_JS 定义
initDB();
"""
# C3 第一批 3 组件交互 JS（GM-V02/G03/R06，见 components.py）
JS_EXTRA_TPL = JS_EXTRA_TPL + C.COMPONENT3_JS
# X26 落地（A类报告 2026-08-04）：切页后暂停离屏页动画（显示优先级为 .active，非 active 页 CSS 动画随 display:none 自然停，
# 此逻辑作保险并拦截可能的页面级动画残留）。注意本模板经 % 格式化，勿在字符串内使用裸 %。
JS_EXTRA_TPL = JS_EXTRA_TPL + r"""
(function(){
  function x26PauseHidden(){
    var pages=document.querySelectorAll('.page,.slide');
    for(var i=0;i<pages.length;i++){
      var p=pages[i];
      if(p.classList.contains('active')){ continue; }
      if(!p.getAnimations){ continue; }
      var run=p.getAnimations({subtree:true}).filter(function(a){ return a.playState==='running'; });
      for(var j=0;j<run.length;j++){ run[j].pause(); }
    }
  }
  var c=document.getElementById('pagesContainer');
  if(c && 'MutationObserver' in window){
    new MutationObserver(function(){ x26PauseHidden(); })
      .observe(c,{subtree:true,attributes:true,attributeFilter:['class']});
  }
})();
"""
# P0-2 数据同步字段统一（2026-08-03）：sync_status 为唯一规范字段。
# 不修改 CORE_JS；通过 js_extra 包装 saveAnswer 补写规范字段，并重写 CSV 导出纳入 sync_status。
# 注意：本模板经 % 格式化，字符串内不得出现裸 %。
JS_EXTRA_TPL = JS_EXTRA_TPL + r"""
/* ===== P0-2 数据同步字段统一（2026-08-03）=====
   规范字段：sync_status（唯一真源）；旧字段 synced（CORE_JS 写入）仅作向后兼容，不删除。
   实现：不修改 CORE_JS，通过 js_extra 包装 saveAnswer 补写 sync_status，并重写 CSV 导出纳入该列。
*/
(function(){
  if(typeof saveAnswer!=='function') return;
  var _origSave = saveAnswer;
  window.saveAnswer = function(questionId, studentAnswer, correctAnswer, isCorrect, attemptNo, timeUsed, hintUsed){
    var before = answerRecords.length;
    _origSave(questionId, studentAnswer, correctAnswer, isCorrect, attemptNo, timeUsed, hintUsed);
    if(answerRecords.length <= before) return; /* db 未就绪未写入，跳过 */
    var rec = answerRecords[answerRecords.length-1];
    if(rec){
      rec.sync_status = rec.synced || 'pending';
      if(window.db && rec.event_id){
        var tx = db.transaction([STORE_NAME], 'readwrite');
        tx.objectStore(STORE_NAME).put(rec);
      }
    }
  };
  /* CSV 导出纳入 sync_status 规范列（旧字段 synced 兜底） */
  window.convertToCSV = function(records){
    var headers = ['event_id','student_id','session_id','question_id','attempt_no','student_answer','correct_answer','is_correct','time_used','hint_used','sync_status','timestamp'];
    var csv = headers.join(',') + '\n';
    records.forEach(function(r){
      var row = headers.map(function(h){
        var val = (h==='sync_status') ? (r.sync_status || r.synced || 'pending') : (r[h]!==undefined ? String(r[h]) : '');
        if(val.indexOf(',')!==-1 || val.indexOf('"')!==-1){ val = '"' + val.replace(/"/g,'""') + '"'; }
        return val;
      });
      csv += row.join(',') + '\n';
    });
    return csv;
  };
})();
"""
NAV = """<div class="nav-bar">
  <div class="nav-item" data-segment="1" onclick="jumpToSegment(1)"><span class="nav-num">①</span>复习导入</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="2" onclick="jumpToSegment(2)"><span class="nav-num">②</span>新词20</div>
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
section_head = g.section_head; sub_label = g.sub_label; key_points = g.key_points
example_section = g.example_section; error_callout = g.error_callout; recall_grid = g.recall_grid
spec2 = importlib.util.spec_from_file_location("courseware_core", os.path.join(HERE, "courseware_core.py"))
core = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(core)
page = core.page; vocab_cards = core.vocab_cards; build_courseware = core.build_courseware
vocab = json.load(open(os.path.join(DATA_DIR, "banks", "vocab_bank.json"), encoding="utf-8"))["words"]
grammar = json.load(open(os.path.join(DATA_DIR, "banks", "grammar_bank.json"), encoding="utf-8"))
passages = json.load(open(os.path.join(DATA_DIR, "banks", "passage_bank.json"), encoding="utf-8"))
try:
    # M6b 补充语篇库（原创·教师授权）：优先按课时取本课语料
    passages += json.load(open(os.path.join(DATA_DIR, "banks", "passage_bank_supplement.json"), encoding="utf-8"))
except FileNotFoundError:
    pass
phonics = json.load(open(os.path.join(DATA_DIR, "banks", "phonics_bank.json"), encoding="utf-8"))
# 40 课教学大纲（阶段B 通用化：上/下节课复习与预告由 lesson_map 读前/后课卡驱动，替代硬编码 L4/L6）
# 每课含 stage/type/grammar/theme/vocab_theme/phonics；复习课(type=test)无独立语法考点。
try:
    _lessons_map = json.load(open(os.path.join(DATA_DIR, "schemas", "lesson_map.json"), encoding="utf-8"))["lessons"]
except (FileNotFoundError, KeyError, json.JSONDecodeError):
    _lessons_map = {}
# L4 复习数据（兼容回退：仅当 lesson_map 缺失或上一课无数据时使用，避免通用化前退化）
QUIZ_L4 = g.QUIZ_L4; QUIZ_EXTRA_L4 = g.QUIZ_EXTRA_L4
VOCAB_L4 = g.VOCAB_L4; VDICT_L4 = g.VDICT_L4
GRAMMAR_L4 = g.GRAMMAR_L4
# 主题中文名（阶段B/阶段A 通用化文案驱动；模块级导入，供上述 helper 使用）
from theme_colors import THEME_NAME

# ============================================================
# 设计系统层（追加到基线 CSS 之上，含层级覆写）
# ============================================================
CSS_EXTRA += r"""
/* ================= 设计系统 v2（字号 1.2x + 玻璃 + 动效） ================= */
:root{
  --fs-h1:44px; --fs-h2:24px; --fs-body:20px; --fs-card:21px; --fs-note:20px;
  --grad-brand:linear-gradient(135deg,#E63946,#FF7A45);
  --grad-gold:linear-gradient(135deg,#FFD700,#FF9F1C);
  --glass:rgba(255,255,255,.62); --glass-line:rgba(255,255,255,.75);
}
html,body{font-size:19px;}
.page{background:
  radial-gradient(1200px 600px at 85% -10%,rgba(255,215,0,.20),transparent 60%),
  radial-gradient(900px 500px at -10% 110%,rgba(230,57,70,.14),transparent 55%),
  linear-gradient(135deg,#FFF4E6 0%,#FFE8D6 45%,#FFD9E8 100%);
  padding:24px 40px 48px;}
.page-title:empty,.page-subtitle:empty{display:none;}
/* ---- 主/副/正文三级层级 ---- */
.page-title{font-size:var(--fs-h1);font-weight:900;background:var(--grad-brand);
  -webkit-background-clip:text;background-clip:text;color:transparent;letter-spacing:2px;
  margin-bottom:10px;text-shadow:none;}
.page-subtitle{font-size:var(--fs-h2);color:#6b5b3e;font-weight:600;margin-bottom:16px;
  background:rgba(255,255,255,.5);display:inline-block;padding:5px 18px;border-radius:30px;}
.section-head .sh-num{width:40px;height:40px;font-size:22px;}
.section-head .sh-title{font-size:28px;}
.sub-label{font-size:20px;padding:8px 20px;border-radius:30px;}
/* ---- 正文与卡片 ---- */
.body-text{font-size:var(--fs-body);padding:16px 22px;background:var(--glass);
  backdrop-filter:blur(8px);border:2px solid var(--glass-line);border-left:6px solid var(--accent);
  border-radius:16px;line-height:1.7;}
.note-panel{font-size:var(--fs-note);padding:14px 20px;background:var(--glass);
  backdrop-filter:blur(8px);border:2px solid var(--glass-line);border-radius:18px;line-height:1.7;}
.note-panel .np-title{font-size:var(--fs-note);}
.kp-item{border-left:6px solid var(--brand);padding:14px 18px;border-radius:14px;}
.kp-key{font-size:20px;} .kp-desc{font-size:20px;line-height:1.55;}
.eg-en{font-size:22px;} .eg-note{font-size:17px;padding:3px 12px;}
.rule-card{position:relative;border-radius:14px;overflow:hidden;box-shadow:0 4px 12px rgba(0,0,0,.16);}
.rule-card::before{content:'';position:absolute;left:0;top:0;bottom:0;width:6px;background:rgba(255,255,255,.32);}
.rule-key::before{width:8px;background:#FFD700;}
.rc-cat{display:flex;justify-content:space-between;align-items:center;gap:8px;padding:8px 12px 8px 16px;
  font-size:16px;font-weight:800;letter-spacing:1px;background:rgba(0,0,0,.20);}
.rc-badge{flex-shrink:0;font-size:12px;font-weight:800;padding:2px 9px;border-radius:10px;letter-spacing:0;white-space:nowrap;}
.rc-badge.key{background:#FFD700;color:#7a5b00;}
.rc-badge.warn{background:#fff;color:#C62828;}
.rc-badge.hint{background:rgba(255,255,255,.30);color:#fff;}
.rc-text{padding:10px 14px 12px 16px;font-size:18px;font-weight:500;line-height:1.5;}
/* 六色卡正文结构化（2026-08-03 教师反馈：正文突出重点，不再逐行平铺） */
.rc-text .rc-err-row{display:flex;align-items:flex-start;gap:8px;margin:4px 0;padding:6px 10px;
  background:rgba(220,38,38,.08);border-left:3px solid #DC2626;border-radius:8px;color:#7F1D1D;}
.rc-text .rc-err-mark{flex:0 0 auto;width:20px;height:20px;border-radius:50%;background:#DC2626;color:#fff;
  display:inline-flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;margin-top:2px;}
.rc-text .rc-fix-row{display:flex;align-items:flex-start;gap:8px;margin:4px 0;padding:6px 10px;
  background:rgba(22,163,74,.10);border-left:3px solid #16A34A;border-radius:8px;color:#14532D;}
.rc-text .rc-fix-mark{flex:0 0 auto;width:20px;height:20px;border-radius:50%;background:#16A34A;color:#fff;
  display:inline-flex;align-items:center;justify-content:center;font-size:12px;font-weight:800;margin-top:2px;}
.rc-text .rc-seq{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0;}
.rc-text .rc-chip{padding:3px 11px;border-radius:20px;background:rgba(0,0,0,.06);border:1px solid rgba(0,0,0,.12);
  font-size:15px;font-weight:700;color:#1F2937;}
.rc-text .rc-chip .rc-arw{color:var(--brand);font-weight:900;padding:0 1px;}
.rc-text .rc-example{display:block;padding:6px 12px;margin:2px 0;background:rgba(0,0,0,.04);
  border-left:3px solid var(--brand);border-radius:8px;font-style:italic;color:#111827;}
.rc-text .rc-note{display:block;padding:2px 0;color:#475569;}
.rc-text .rc-kw{color:var(--brand);font-weight:800;}
.error-card{padding:13px 15px;border-radius:14px;}
.err-wrong{font-size:20px;} .err-arrow{font-size:17px;} .err-right{font-size:20px;}
/* ---- 词汇卡 ---- */
.vocab-card{padding:16px 20px;border-radius:16px;border-left:6px solid var(--brand);
  box-shadow:0 6px 18px rgba(0,0,0,.08);}
.vocab-word{font-size:27px;} .vocab-phonetic{font-size:18px;} .vocab-pos{font-size:16px;}
.vocab-cn{font-size:22px;} .vocab-collocation,.vocab-example{font-size:17px;}
.vocab-memory{font-size:16px;}
/* ---- 选择题：题目两列流（第1题左/第2题右，往下第3题左/第4题右）---- */
.quiz-cols{display:grid;grid-template-columns:1fr 1fr;gap:12px 16px;align-items:start;margin:8px 0;}
.quiz-q{padding:12px 14px;border-radius:12px;box-shadow:0 4px 12px rgba(230,57,70,.08);}
.quiz-q .qq-text{font-size:20px;margin-bottom:8px;}
.quiz-opt{font-size:19px;padding:9px 13px;border-radius:10px;margin:6px 0;}
/* ---- 表格 ---- */
.content-table,.pm-table{font-size:22px;}
.content-table th{font-size:22px;padding:12px;} .content-table td{font-size:20px;padding:10px;}
.pm-table th,.pm-table td{font-size:20px;padding:10px;}
/* ---- 阅读 ---- */
.reading-passage{font-size:22px;line-height:1.85;padding:18px 24px;}
/* ---- 拼读 ---- */
.phonics-card{border-radius:16px;padding:14px 10px;}
.phonics-card .pc-letter{font-size:36px;} .phonics-card .pc-word{font-size:20px;}
.phonics-card .pc-cn{font-size:17px;}
/* ---- 知识图谱 ---- */
.kmap-node{border-radius:16px;padding:13px 15px;}
.kmap-node .kn-title{font-size:20px;} .kmap-node .kn-body{font-size:18px;}
/* ---- 封面（玻璃渐变 + 光斑 + 徽章） ---- */
.cover-wrap{position:relative;display:flex;flex-direction:column;align-items:center;justify-content:center;
  height:100%;text-align:center;overflow:hidden;border-radius:30px;padding:20px;}
/* 封面布局 v2026-08-05 教师偏好：信息标签置顶、底部留白（仅 flex 版，非 grid 变体；grid 变体由 grid-template-areas 重排） */
.cover-wrap:not([class*="variant"]){justify-content:flex-start;padding-top:6vh;padding-bottom:3vh;}
.cover-wrap .cover-badge{order:-3;}
.cover-wrap .cover-info{order:-2;}
.cover-wrap .cover-title,.cover-wrap .cover-sub,.cover-wrap .cover-tagline{order:0;}
.cover-wrap .cover-emoji{order:10;margin-top:auto;padding-bottom:2vh;}
.cover-wrap::before,.cover-wrap::after{content:'';position:absolute;border-radius:50%;filter:blur(70px);opacity:.55;z-index:0;}
.cover-wrap::before{width:460px;height:460px;background:radial-gradient(circle,#FFD700,#FF7A45);top:-130px;right:-50px;
  animation:coverFloat 6s ease-in-out infinite;}
.cover-wrap::after{width:420px;height:420px;background:radial-gradient(circle,#E63946,#FF7A45);bottom:-150px;left:-40px;
  animation:coverFloat 7s ease-in-out infinite reverse;}
@keyframes coverFloat{0%,100%{transform:translateY(0) scale(1);}50%{transform:translateY(-18px) scale(1.06);}}
.cover-badge{position:relative;z-index:2;font-size:22px;font-weight:800;color:#fff;background:var(--grad-brand);
  padding:9px 28px;border-radius:50px;box-shadow:0 8px 22px rgba(230,57,70,.4);letter-spacing:2px;}
.cover-title{position:relative;z-index:2;font-size:64px;font-weight:900;background:var(--grad-brand);
  -webkit-background-clip:text;background-clip:text;color:transparent;margin-top:20px;letter-spacing:4px;}
.cover-sub{position:relative;z-index:2;font-size:30px;color:#5d4f33;margin-top:14px;font-weight:600;}
.cover-tagline{position:relative;z-index:2;font-size:20px;color:#8a7a58;margin-top:8px;}
.cover-info{position:relative;z-index:2;display:flex;gap:18px;margin-top:26px;flex-wrap:wrap;justify-content:center;}
.cover-info-num{background:var(--glass);backdrop-filter:blur(10px);border:2px solid var(--glass-line);
  border-radius:20px;padding:14px 28px;box-shadow:0 10px 26px rgba(0,0,0,.12);}
.cover-info-num .ci-label{font-size:18px;color:#7a6a4a;}
.cover-info-num .ci-val{font-size:42px;font-weight:900;background:var(--grad-brand);
  -webkit-background-clip:text;background-clip:text;color:transparent;}
.cover-emoji{position:relative;z-index:2;font-size:50px;margin-top:20px;animation:coverBounce 2.4s ease-in-out infinite;}
@keyframes coverBounce{0%,100%{transform:translateY(0);}50%{transform:translateY(-10px);}}
/* 封面模板库（2026-08-03 教师反馈：封面形式去同质化，按 lesson%3 轮换 A/B/C）*/
.cover-variant-a{display:grid;grid-template-areas:"badge" "info" "title" "sub" "tag" "emoji";
  justify-items:center;align-content:center;gap:6px;height:100%;text-align:center;}
.cover-variant-a .cover-title,.cover-variant-a .cover-sub,.cover-variant-a .cover-tagline,
.cover-variant-a .cover-info,.cover-variant-a .cover-emoji,.cover-variant-a .cover-badge{margin-top:0;}
.cover-variant-b{display:grid;grid-template-columns:1.2fr .8fr;
  grid-template-areas:"badge info" "title info" "sub info" "tag info" "emoji info";
  align-items:center;justify-items:center;gap:8px 24px;height:100%;text-align:center;padding:0 6%;}
.cover-variant-b .cover-title,.cover-variant-b .cover-sub,.cover-variant-b .cover-tagline,
.cover-variant-b .cover-info,.cover-variant-b .cover-emoji,.cover-variant-b .cover-badge{margin-top:0;}
.cover-variant-b .cover-title{font-size:54px;}
.cover-variant-b .cover-info{flex-direction:column;gap:14px;}
.cover-variant-b::before,.cover-variant-b::after{animation:none;}
.cover-variant-c{display:grid;grid-template-areas:"badge badge" "info info" "title title" "sub sub" "tag tag" "emoji emoji";
  justify-items:center;align-content:center;gap:6px 28px;height:100%;text-align:center;}
.cover-variant-c .cover-title,.cover-variant-c .cover-sub,.cover-variant-c .cover-tagline,
.cover-variant-c .cover-info,.cover-variant-c .cover-emoji,.cover-variant-c .cover-badge{margin-top:0;}
.cover-variant-c .cover-title{font-size:52px;letter-spacing:8px;}
.cover-variant-c .cover-info{flex-direction:column;gap:12px;}
.cover-variant-c::before{animation:coverSweep 9s ease-in-out infinite;}
.cover-variant-c::after{animation:coverFloat 8s ease-in-out infinite reverse;}
@keyframes coverSweep{0%,100%{transform:translate(0,0) scale(1);}50%{transform:translate(-28px,18px) scale(1.08);}}
/* 翻牌卡形式轮换（同课统一变体，build_lesson 按 lesson%3 设置 _RECALL_VARIANT）*/
.recall-variant-b .recall-grid{grid-template-columns:repeat(2,1fr);gap:16px;}
.recall-variant-b .flash-card{height:210px;}
.recall-variant-c .recall-grid{grid-template-columns:repeat(2,1fr);gap:18px;}
.recall-variant-c .flash-card{height:190px;}
.recall-variant-c .recall-grid .flash-card:nth-child(odd){transform:translateY(16px);}
/* 词汇卡形式轮换（build_lesson 按 lesson%3 设置 vocab-variant-*）*/
.vocab-variant-a .vocab-card{border-left:6px solid var(--brand);}
.vocab-variant-b .vocab-card{border-left:none;border-top:5px solid var(--brand);
  padding-top:18px;}
.vocab-variant-b .vocab-head{flex-wrap:wrap;}
.vocab-variant-c .vocab-card{border-left:none;border:1px solid rgba(23,34,53,.10);
  background:var(--card-bg);box-shadow:none;}
.vocab-variant-c .vocab-head{border-bottom:1px dashed rgba(23,34,53,.12);
  padding-bottom:8px;margin-bottom:8px;}
/* ---- 大号翻牌卡 ---- */
.recall-grid{grid-template-columns:repeat(3,1fr);gap:16px;}
.flash-card{height:180px;perspective:1000px;cursor:pointer;}
.flash-inner{position:relative;width:100%;height:100%;transition:transform .6s;transform-style:preserve-3d;}
.flash-card.flipped .flash-inner{transform:rotateY(180deg);}
.flash-front,.flash-back{position:absolute;inset:0;backface-visibility:hidden;border-radius:18px;
  display:flex;flex-direction:column;align-items:center;justify-content:center;padding:14px;text-align:center;
  box-shadow:0 8px 22px rgba(0,0,0,.12);}
.flash-front{background:linear-gradient(135deg,#fff,#FFF3E0);border:3px dashed var(--brand);}
.flash-back{background:var(--grad-brand);color:#fff;transform:rotateY(180deg);}
.flash-q{font-size:30px;font-weight:800;color:var(--brand);line-height:1.35;}
.flash-back .flash-a{font-size:30px;font-weight:800;line-height:1.35;}
.flash-hint{font-size:18px;color:var(--text-secondary);margin-top:8px;}
/* ---- 游戏面板（深色闯关） ---- */
.game-board{background:linear-gradient(140deg,#3A0D2C,#6B1533);border-radius:22px;padding:22px;color:#fff;
  box-shadow:0 12px 34px rgba(58,13,44,.45);margin:12px 0;}
.game-top{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px;gap:12px;}
.game-title{font-size:26px;font-weight:800;display:flex;align-items:center;gap:10px;}
.game-title .gt-icon{font-size:30px;}
.game-tag{font-size:18px;background:rgba(255,255,255,.16);padding:5px 16px;border-radius:30px;color:#FFE9A8;}
.game-rule{font-size:20px;color:#FFD9D9;margin-bottom:12px;line-height:1.5;}
.game-board .quiz-q{background:transparent;border:none;box-shadow:none;padding:0;}
.game-board .quiz-opt{background:#FFFFFF !important;color:#000000 !important;border:2px solid #1E293B !important;
  font-size:20px;padding:10px 14px;font-weight:700 !important;}
.game-board .quiz-opt:hover{background:#F1F5F9 !important;color:#000000 !important;border-color:#000000 !important;}
.game-board .quiz-opt.opt-correct{background:#DCFCE7 !important;border-color:#16A34A !important;color:#15803D !important;font-weight:800 !important;}
.game-board .quiz-opt.opt-wrong{background:#FEE2E2 !important;border-color:#DC2626 !important;color:#B91C1C !important;font-weight:800 !important;}
/* ---- 拓展知识卡 ---- */
.ext-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin:12px 0;}
.ext-card{position:relative;background:#fff;border-radius:18px;padding:16px 20px;
  box-shadow:0 6px 20px rgba(0,0,0,.09);overflow:hidden;transition:transform .2s;}
.ext-card:hover{transform:translateY(-4px);}
.ext-card::before{content:'';position:absolute;top:0;left:0;width:100%;height:8px;background:var(--grad-brand);}
.ext-card.blue::before{background:linear-gradient(135deg,#3B82F6,#60A5FA);}
.ext-card.green::before{background:linear-gradient(135deg,#10B981,#34D399);}
.ext-card.gold::before{background:var(--grad-gold);}
.ext-card.purple::before{background:linear-gradient(135deg,#8B5CF6,#A78BFA);}
.ext-cat{font-size:23px;font-weight:800;color:var(--brand);display:flex;align-items:center;gap:10px;margin-bottom:8px;}
.ext-card.blue .ext-cat{color:var(--sop-blue);}
.ext-card.green .ext-cat{color:var(--sop-green);}
.ext-card.gold .ext-cat{color:#B8860B;}
.ext-card.purple .ext-cat{color:var(--sop-purple);}
.ext-body{font-size:24px;color:var(--text-primary);line-height:1.6;}
.ext-body b,.ext-high{color:var(--brand);background:rgba(230,57,70,.10);border-radius:8px;padding:1px 8px;font-weight:800;}
.ext-card.gold .ext-body b,.ext-card.gold .ext-high{color:#B8860B;background:rgba(255,215,0,.18);}
.ext-body .ext-key{color:var(--sop-blue);font-weight:800;}
.ext-body .ext-en{color:var(--brand);font-weight:800;}
/* ---- 语法流程图（祈使句） ---- */
.grammar-flow{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:14px;margin:16px 0;}
.gf-step{background:#fff;border-radius:18px;padding:14px 18px;text-align:center;
  box-shadow:0 6px 20px rgba(0,0,0,.12);border-top:6px solid var(--brand);min-width:190px;}
.gf-step:nth-child(3){border-top-color:var(--accent);}
.gf-step:nth-child(5){border-top-color:var(--sop-green);}
.gf-label{font-size:20px;color:var(--text-secondary);font-weight:700;}
.gf-main{font-size:30px;font-weight:900;color:var(--brand);margin-top:6px;}
.gf-ex{font-size:23px;color:var(--text-primary);margin-top:6px;line-height:1.4;}
.gf-arrow{font-size:32px;color:var(--accent);font-weight:900;}
/* ---- 结构公式框（What 问句） ---- */
.formula-box{background:linear-gradient(140deg,#0F2A43,#1E4976);border-radius:20px;padding:22px;color:#fff;
  box-shadow:0 10px 28px rgba(30,73,118,.4);margin:14px 0;text-align:center;}
.formula-label{font-size:20px;color:#BFDBFE;font-weight:700;margin-bottom:8px;}
.formula-main{font-size:32px;font-weight:900;color:#93C5FD;line-height:1.5;}
.formula-ex{font-size:24px;color:#fff;margin-top:12px;line-height:1.5;}
/* ---- like 结构图 ---- */
.like-diagram{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;margin:14px 0;}
.ld-item{background:#fff;border-radius:18px;padding:16px;text-align:center;box-shadow:0 6px 20px rgba(0,0,0,.1);border-top:6px solid;}
.ld-item:nth-child(1){border-top-color:var(--brand);}
.ld-item:nth-child(2){border-top-color:var(--sop-blue);}
.ld-item:nth-child(3){border-top-color:var(--sop-green);}
.ld-f{font-size:26px;font-weight:900;color:var(--brand);}
.ld-item:nth-child(2) .ld-f{color:var(--sop-blue);}
.ld-item:nth-child(3) .ld-f{color:var(--sop-green);}
.ld-e{font-size:22px;color:var(--text-primary);margin-top:8px;line-height:1.4;}
/* ---- 通用语法结构卡（阶段A 通用化：grammar_bank 六色卡驱动，替代祈使句/What/like 专属分支） ---- */
.gram-card-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin:16px 0;}
.gram-card{background:#fff;border-radius:18px;padding:16px 18px;box-shadow:0 6px 20px rgba(0,0,0,.10);border-top:6px solid;text-align:left;}
.gram-card.gc-red{border-top-color:var(--brand);}
.gram-card.gc-blue{border-top-color:var(--sop-blue);}
.gram-card.gc-gold{border-top-color:var(--accent);}
.gram-card.gc-green{border-top-color:var(--sop-green);}
.gram-card.gc-purple{border-top-color:#8B5CF6;}
.gram-card .gc-t{font-size:20px;font-weight:800;color:var(--text-secondary);}
.gram-card .gc-b{font-size:24px;line-height:1.5;color:var(--text-primary);margin-top:6px;font-weight:600;}
.gram-card .gc-b b{color:var(--brand);}
/* ---- 交互改错 ---- */
.err-zone{background:#fff;border:3px solid var(--brand);border-radius:18px;padding:16px;
  box-shadow:0 6px 20px rgba(230,57,70,.1);margin:12px 0;}
.err-zone-title{font-size:23px;font-weight:800;color:var(--brand);margin-bottom:6px;display:flex;gap:10px;align-items:center;}
.err-zone .body-text{font-size:21px;padding:12px 16px;}
/* ---- 一览表 ---- */
.glance-table{border-collapse:separate;border-spacing:0;width:100%;font-size:22px;margin:12px 0;overflow:hidden;border-radius:16px;}
.glance-table th{background:var(--grad-brand);color:#fff;font-size:22px;padding:13px;font-weight:800;}
.glance-table td{padding:13px;border-bottom:1px solid #f3e0d0;background:rgba(255,255,255,.75);text-align:center;font-size:21px;}
.glance-table tr:nth-child(even) td{background:rgba(255,248,225,.7);}
.glance-table .gt-key{font-weight:900;color:var(--brand);font-size:24px;}
.glance-table .gt-en{color:var(--sop-blue);font-weight:700;}
/* ---- 动画：彩带粒子 / 晃动 ---- */
.burst-p{position:fixed;width:14px;height:14px;border-radius:50%;z-index:4000;pointer-events:none;
  animation:burstFly .6s ease-out forwards;}
@keyframes burstFly{from{transform:translate(0,0) scale(1);opacity:1;}
  to{transform:translate(var(--dx),var(--dy)) scale(.2);opacity:0;}}
@keyframes shake{0%,100%{transform:translateX(0);}20%{transform:translateX(-10px);}40%{transform:translateX(10px);}
  60%{transform:translateX(-6px);}80%{transform:translateX(6px);}}
/* ---- 游戏目标 chips ---- */
.chip-row{display:flex;gap:12px;flex-wrap:wrap;justify-content:center;margin:12px 0;}
.chip{background:#fff;border:3px solid var(--brand);border-radius:40px;padding:9px 20px;font-size:22px;
  font-weight:700;color:var(--brand);box-shadow:0 5px 14px rgba(230,57,70,.12);display:flex;align-items:center;gap:8px;}
.chip .chip-icon{font-size:26px;}
/* ---- 思维导图（中心辐射式 + 底部交互面板） ---- */
.mm-wrap{position:relative;height:520px;margin:8px 0;}
.mm-center{position:absolute;left:50%;top:38%;transform:translate(-50%,-50%);z-index:3;
  width:160px;height:160px;border-radius:50%;background:linear-gradient(140deg,#E63946,#FF7A45);
  color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;
  box-shadow:0 14px 36px rgba(230,57,70,.45);border:6px solid #fff;text-align:center;}
.mm-c-emoji{font-size:28px;margin-bottom:2px;}
.mm-c-en{font-size:30px;font-weight:900;letter-spacing:1px;}
.mm-c-cn{font-size:20px;margin-top:4px;opacity:.95;}
.mm-lines{position:absolute;left:0;top:0;width:100%;height:100%;z-index:1;}
.mm-lines line{stroke:rgba(230,57,70,.4);stroke-width:.6;stroke-dasharray:1.2 1;fill:none;}
.mm-branch{position:absolute;transform:translate(-50%,-50%);z-index:2;}
.mm-b1{left:67%;top:26%;} .mm-b2{left:83%;top:38%;} .mm-b3{left:67%;top:52%;}
.mm-b4{left:33%;top:52%;} .mm-b5{left:17%;top:38%;} .mm-b6{left:33%;top:26%;}
.mm-node{display:flex;align-items:center;gap:8px;padding:9px 16px;border-radius:40px;color:#fff;
  font-size:23px;font-weight:800;cursor:pointer;box-shadow:0 8px 22px rgba(0,0,0,.18);
  border:3px solid #fff;transition:transform .15s,box-shadow .15s;white-space:nowrap;}
.mm-node:hover{transform:scale(1.08);}
.mm-icon{font-size:26px;}
.mm-red .mm-node{background:linear-gradient(140deg,#E63946,#FF7A45);}
.mm-blue .mm-node{background:linear-gradient(140deg,#3B82F6,#60A5FA);}
.mm-green .mm-node{background:linear-gradient(140deg,#10B981,#34D399);}
.mm-purple .mm-node{background:linear-gradient(140deg,#8B5CF6,#A78BFA);}
.mm-gold .mm-node{background:linear-gradient(140deg,#F59E0B,#FBBF24);}
.mm-teal .mm-node{background:linear-gradient(140deg,#14B8A6,#2DD4BF);}
.mm-branch.active .mm-node{transform:scale(1.14);box-shadow:0 0 0 6px rgba(255,255,255,.95),0 14px 32px rgba(0,0,0,.3);}
.mm-panel{position:absolute;left:50%;bottom:0;transform:translateX(-50%);width:88%;background:#fff;
  border-radius:18px;padding:14px 20px;box-shadow:0 10px 28px rgba(0,0,0,.16);border-top:6px solid #E63946;
  z-index:4;min-height:118px;transition:border-color .2s;}
.mm-panel.mm-red{border-top-color:#E63946;} .mm-panel.mm-blue{border-top-color:#3B82F6;}
.mm-panel.mm-green{border-top-color:#10B981;} .mm-panel.mm-purple{border-top-color:#8B5CF6;}
.mm-panel.mm-gold{border-top-color:#F59E0B;} .mm-panel.mm-teal{border-top-color:#14B8A6;}
.mm-panel-title{font-size:24px;font-weight:800;color:var(--brand);display:flex;gap:10px;align-items:center;margin-bottom:8px;}
.mm-panel-chips{display:flex;flex-wrap:wrap;gap:10px;}
.mm-chip{font-size:20px;padding:8px 14px;border-radius:12px;background:rgba(230,57,70,.06);
  border:1px solid rgba(230,57,70,.18);line-height:1.45;}
.mm-chip b{color:var(--brand);}
/* 思维导图变体：卡片簇 / 横向树状（形式按本课内容选择，非写死） */
.mm-head{text-align:center;font-size:36px;font-weight:900;background:var(--grad-brand);
  -webkit-background-clip:text;background-clip:text;color:transparent;margin:6px 0;letter-spacing:2px;}
.mm-cards{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin:12px 0;}
.mm-cards .ext-card{padding:13px 15px;}
.mm-cards .ext-cat{font-size:21px;margin-bottom:6px;}
.mm-cards .mm-chip{font-size:17px;padding:6px 10px;margin:4px 0;}
.ext-card.teal::before{background:linear-gradient(135deg,#14B8A6,#2DD4BF);}
.mm-tree{display:grid;grid-template-columns:auto 1fr;gap:14px 22px;align-items:start;margin:14px auto;max-width:1400px;}
.mm-tn{background:linear-gradient(140deg,#E63946,#FF7A45);color:#fff;padding:10px 18px;border-radius:40px;
  font-size:23px;font-weight:800;white-space:nowrap;box-shadow:0 6px 18px rgba(0,0,0,.15);border:3px solid #fff;}
.mm-tn.mm-blue{background:linear-gradient(140deg,#3B82F6,#60A5FA);}
.mm-tn.mm-green{background:linear-gradient(140deg,#10B981,#34D399);}
.mm-tn.mm-purple{background:linear-gradient(140deg,#8B5CF6,#A78BFA);}
.mm-tn.mm-gold{background:linear-gradient(140deg,#F59E0B,#FBBF24);}
.mm-tn.mm-teal{background:linear-gradient(140deg,#14B8A6,#2DD4BF);}
.mm-tchips{display:flex;flex-wrap:wrap;gap:8px;}
.mm-tchips .mm-chip{font-size:18px;padding:7px 12px;}
/* ---- 思维导图 · 完整内容组件（§3.9「必须呈现完整内容」） ---- */
.mm-panel{max-height:200px;overflow:auto;}
.mm-panel-chips{display:block;}
.mm-words{display:grid;grid-template-columns:repeat(5,1fr);gap:8px;}
.mm-w{background:#fff7f3;border:1px solid rgba(230,57,70,.16);border-radius:10px;padding:5px 8px;
  display:flex;align-items:center;justify-content:space-between;gap:6px;}
.mw-en{font-size:18px;font-weight:800;color:#2D2A32;}
.mw-cn{font-size:16px;color:#6B7280;}
.mm-gram{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;}
.mm-gram-card{border-radius:12px;padding:8px 10px;border:1px solid;font-size:15px;}
.mmg-red{background:#FFF1F0;border-color:#FFA39E;} .mmg-blue{background:#E6F4FF;border-color:#91CAFF;}
.mmg-green{background:#F0FFF4;border-color:#95DEAC;} .mmg-gold{background:#FFFBE6;border-color:#FFE58F;}
.mg-t{font-size:17px;font-weight:900;margin-bottom:4px;color:#2D2A32;}
.mg-f{line-height:1.5;color:#374151;}
.mg-f b{color:#E63946;}
.mg-e{margin-top:5px;font-size:14px;color:#6B7280;border-top:1px dashed rgba(0,0,0,.08);padding-top:4px;line-height:1.4;}
.mm-rd{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;}
.mm-rd-card{border-radius:12px;padding:8px 10px;background:#F0F9FF;border:1px solid #BAE6FD;font-size:15px;line-height:1.5;color:#374151;}
.mm-rd-card .mg-t{color:#0369A1;}
.mm-err{display:grid;grid-template-columns:1fr 1fr;gap:8px;}
.mm-err-line{display:flex;gap:8px;align-items:flex-start;font-size:16px;line-height:1.5;color:#374151;
  background:#FFFAF0;border:1px solid #FFD591;border-radius:10px;padding:6px 10px;}
.mm-err-line b{color:#E63946;}
.mm-room{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px;}
.mm-room-tile{font-size:15px;padding:4px 8px;border-radius:8px;background:rgba(245,158,11,.08);
  border:1px solid rgba(245,158,11,.25);color:#92400E;}
.mm-room-tile b{color:#B45309;}
/* 思维导图 · 完整内容页（词汇全表 / 语法全表 / 复习全表） */
.mm-full-words{display:grid;grid-template-columns:repeat(5,1fr);gap:10px;}
.mmf-w{border-radius:12px;background:#fff;border:1px solid rgba(230,57,70,.16);box-shadow:0 4px 12px rgba(0,0,0,.06);
  padding:8px 10px;display:flex;flex-direction:column;gap:2px;}
.mmf-en{font-size:19px;font-weight:900;color:#2D2A32;}
.mmf-ph{font-size:14px;color:#9CA3AF;}
.mmf-pos{font-size:13px;color:#E63946;font-weight:700;}
.mmf-cn{font-size:16px;color:#6B7280;}
.mm-full-gram{display:grid;grid-template-columns:1fr 1fr 1fr;gap:12px;margin:8px 0;}
.mm-full-gram .mm-gram-card{padding:12px 14px;}
.mm-full-gram .mg-t{font-size:20px;}
.mm-full-gram .mg-f{font-size:17px;}
.mm-full-gram .mg-e{font-size:15px;}
/* ---- 阅读理解 · 左文右题双栏（Split Screen：左侧原文 / 右侧题目框，题目框内可独立上下滚动） ---- */
.read-split{display:grid;grid-template-columns:55% 45%;gap:18px;align-items:start;}
.read-left{display:flex;flex-direction:column;gap:10px;min-width:0;}
.read-right{position:sticky;top:8px;align-self:start;display:flex;flex-direction:column;min-width:0;
  height:min(540px, calc(100vh - 150px));min-height:300px;
  border:3px solid rgba(230,57,70,.32);border-radius:16px;background:rgba(255,255,255,.74);
  box-shadow:0 10px 26px rgba(0,0,0,.12);overflow:hidden;}
.read-right-head{flex-shrink:0;padding:9px 14px;background:linear-gradient(135deg,#E63946,#FF7A45);color:#fff;
  font-size:19px;font-weight:800;letter-spacing:1px;display:flex;align-items:center;gap:6px;}
.read-qs-scroll{flex:1 1 auto;overflow-y:auto;padding:10px 14px;min-height:0;
  scrollbar-width:thin;scrollbar-color:#E63946 #FFE3D0;}
.read-qs-scroll::-webkit-scrollbar{width:8px;}
.read-qs-scroll::-webkit-scrollbar-thumb{background:#E63946;border-radius:4px;}
.read-qs-scroll::-webkit-scrollbar-track{background:#FFE3D0;}
.read-right .quiz-q{margin-bottom:12px;}
.read-right .quiz-q .qq-text{font-size:20px;line-height:1.4;}
.read-right .quiz-opt{font-size:17px;padding:7px 12px;margin:4px 0;}
.read-split .reading-passage{font-size:20px;line-height:1.75;}
.read-split .note-panel{padding:8px 12px;}
/* 五选四 · 右侧选项紧凑横排 */
.w5-opts{display:flex;flex-wrap:wrap;gap:6px;margin:4px 0 12px;}
.w5-opts .quiz-opt{flex:1 1 46%;min-width:0;margin:0;font-size:15px;padding:6px 9px;line-height:1.4;}
.read-qs-scroll .w5-qq{font-size:20px;font-weight:800;color:#2D2A32;margin:6px 0 2px;}
/* 阅读优先级徽标（CORE / EXTEND / HOME，仅标注不删篇） */
.pri-row{display:flex;gap:8px;align-items:center;margin-bottom:8px;}
.pri-badge{display:inline-block;padding:4px 14px;border-radius:20px;font-size:16px;font-weight:800;color:#fff;letter-spacing:1px;}
.pri-core{background:linear-gradient(135deg,#E63946,#FF7A45);box-shadow:0 4px 12px rgba(230,57,70,.3);}
.pri-extend{background:linear-gradient(135deg,#F59E0B,#FBBF24);box-shadow:0 4px 12px rgba(245,158,11,.3);}
.pri-home{background:linear-gradient(135deg,#10B981,#34D399);box-shadow:0 4px 12px rgba(16,185,129,.3);}
.pri-note{font-size:15px;color:#6B7280;font-weight:600;}
/* §3.8.2 答错双击撤销：已答锁定态 + 撤销提示小字 */
.quiz-opt.locked{opacity:.55;cursor:default;}
.quiz-opt.locked.opt-correct,.quiz-opt.locked.opt-wrong{opacity:1;cursor:pointer;}
.et-undo-hint{font-size:11px;color:#8B7D6B;opacity:.75;margin-top:4px;cursor:pointer;}
"""
# C3 第一批 3 组件样式（GM-V02/G03/R06，见 components.py）
CSS_EXTRA += C.COMPONENT3_CSS
# X26 视觉层（A类报告 2026-08-03 落地）：实体卡替代大面积玻璃 / 触屏按压态 / 键盘焦点 / 减弱动画
CSS_EXTRA += r"""
:root{
  --x26-bg:#f4f7fb; --x26-surface:rgba(255,255,255,.96); --x26-text:#172235; --x26-muted:#68758a;
  --x26-line:rgba(31,48,70,.12); --x26-primary:#356fd4; --x26-primary-soft:rgba(53,111,212,.10);
  --x26-radius-sm:10px; --x26-radius-md:16px; --x26-radius-lg:22px;
  --x26-shadow:0 1px 2px rgba(18,31,48,.04), 0 10px 28px rgba(18,31,48,.07);
  --x26-motion-fast:150ms; --x26-motion-base:220ms; --x26-ease:cubic-bezier(.2,0,0,1);
}
/* 1. 实体表面：正文/笔记/普通卡片由玻璃拟态改实体纸卡（A1: 明显边界回归） */
.body-text,.note-panel,.x26-card{
  background:var(--x26-surface);
  border:1px solid var(--x26-line);
  box-shadow:var(--x26-shadow);
  backdrop-filter:none;
  -webkit-backdrop-filter:none;
}
/* 2. 触屏按压态：按钮/选项统一按压反馈，touch 不触发延迟 */
button,.quiz-opt,.game-option,.fill-check-btn,.x26-button{
  transition:transform var(--x26-motion-fast) var(--x26-ease),
             background-color var(--x26-motion-fast) linear,
             border-color var(--x26-motion-fast) linear;
  touch-action:manipulation;
}
button:active,.quiz-opt:active,.game-option:active,.fill-check-btn:active,.x26-button:active{transform:scale(.98);}
/* 3. 数字等宽：进度/时间/分数不跳动 */
.x26-number,.progress-number,.timer,.score{font-variant-numeric:tabular-nums;letter-spacing:-.02em;}
/* 4. 键盘焦点可见（A3: 不能只靠颜色与hover） */
:where(button,input,select,textarea):focus-visible{outline:3px solid rgba(53,111,212,.35);outline-offset:3px;}
/* 5. 减弱动画（A2/A4: prefers-reduced-motion 全局降级） */
@media (prefers-reduced-motion: reduce){
  *,*::before,*::after{animation-duration:.01ms !important;animation-iteration-count:1 !important;transition-duration:.01ms !important;}
}
"""

# ============================================================
# 新渲染 helper（本地定义，不依赖 gen_l1_l13_v2 的旧样式语义）
# ============================================================
_RECALL_VARIANT = ""  # 翻牌卡形式变体（build_lesson 按课轮换设置）
def flash_grid(cards, variant=None):
    """大号翻牌卡：inline stopPropagation，组件点击不触发翻页。variant=recall-variant-* 形式变体。"""
    if variant is None:
        variant = _RECALL_VARIANT
    out = ['<div class="recall-grid%s">' % (" " + variant if variant else "")]
    for q, a in cards:
        out.append('<div class="flash-card" onclick="event.stopPropagation(); flipCard(this)"><div class="flash-inner">'
                   '<div class="flash-front"><div class="flash-q">%s</div><div class="flash-hint">点击翻面</div></div>'
                   '<div class="flash-back"><div class="flash-a">%s</div></div></div></div>' % (q, a))
    out.append('</div>')
    return "\n".join(out)

def ext_cards(items):
    """精美拓展知识卡：items = [(cat, color_class, body_html)]，重点用 <b> 包裹。"""
    out = ['<div class="ext-grid">']
    for cat, cls, body in items:
        out.append('<div class="ext-card %s"><div class="ext-cat">%s</div><div class="ext-body">%s</div></div>'
                   % (cls, cat, body))
    out.append('</div>')
    return "\n".join(out)

def game_board(title, icon, rule, inner):
    """深色闯关游戏面板，包裹选择题。"""
    return ('<div class="game-board"><div class="game-top"><span class="game-title">'
            '<span class="gt-icon">%s</span>%s</span><span class="game-tag">闯关</span></div>'
            '<div class="game-rule">%s</div>%s</div>') % (icon, title, rule, inner)

def grammar_structure(gname, entry):
    """把「构成与用法」从黑字升级为通用结构图（阶段A 通用化：grammar_bank 六色卡驱动，
    替代 祈使句/What/like 专属分支，适配任意语法考点）。"""
    intro = ('<div class="body-text"><span class="highlight">%s</span></div>' % entry.get("构成", ""))
    six = entry.get("六色卡", {})
    slots = [("用法", "gc-red"), ("构成", "gc-blue"), ("注意", "gc-gold"),
             ("易错", "gc-purple"), ("口诀", "gc-green"), ("例句", "gc-green")]
    cards = []
    for key, cls in slots:
        val = six.get(key)
        if not val:
            continue
        cards.append('<div class="gram-card %s"><div class="gc-t">%s</div><div class="gc-b">%s</div></div>'
                     % (cls, key, _fmt_err(val)))
    if not cards:
        # 六色卡缺失时回退到简介结构（仍未硬编码具体考点）
        cards = ['<div class="gram-card gc-red"><div class="gc-t">核心用法</div><div class="gc-b">%s</div></div>'
                 % entry.get("构成", "按考点结构理解")] if entry.get("构成") else []
    return intro + ('<div class="gram-card-grid">%s</div>' % "".join(cards))

def adapt_l4(ql4):
    """L4 选择题 (stem,[(letter,opt,cor)...]) → quiz_html (stem,correct,[distractors])。"""
    out = []
    for stem, opts in ql4:
        cor = [o[1] for o in opts if o[2] == "1"][0]
        dis = [o[1] for o in opts if o[2] == "0"]
        out.append((stem, cor, dis))
    return out

def vocab_en2cn(words):
    """新词「英文→中文」闯关：每词取后续两个词的中文作干扰项。"""
    out = []
    n = len(words)
    for i, w in enumerate(words):
        dis = [words[(i + 1) % n]["cn"], words[(i + 2) % n]["cn"]]
        out.append(("%s 是什么意思？" % w["en"], w["cn"], dis))
    return out

def vocab_cn2en(words, targets=None):
    """新词「中文→英文」闯关（主动提取方向）。
    words=干扰项池；targets=要考的词（默认取 words 前 2 个）；干扰项从池中排除自身选取，小样本不重复。"""
    if targets is None:
        targets = words[:2]
    out = []
    for t in targets:
        others = [w for w in words if w["en"] != t["en"]]
        dis = [others[0]["en"], others[1]["en"]] if len(others) >= 2 else [""]
        out.append(("%s 是哪个词？" % t["cn"], t["en"], dis))
    return out

def _collect_used_en_words(pages):
    """收集已生成页面上作为「正确答案」出现的英文词（Exit Ticket 词汇去重用）。
    中文→英文题的答案是英文（如课堂游戏「看中文选英文」）；英文→中文题的答案是中文，不会误收。
    语法题答案虽是英文但不在本课新词表内，不影响选词。"""
    used = set()
    en_re = re.compile(r"[A-Za-z][A-Za-z' -]{1,50}$")
    for pid, p in pages.items():
        for q in re.finditer(r'<div class="quiz-q[^"]*"[^>]*><div class="qq-text">(.*?)</div>(.*?)</div>', p, re.S):
            opts = q.group(2)
            m = re.search(r'data-correct="1"[^>]*>([^<]+)</button>', opts)
            if not m:
                continue
            txt = re.sub(r'^[A-E]\.\s*', '', m.group(1).strip()).strip()
            if en_re.match(txt):
                used.add(txt)
    return used

def _pick_mm_form(card):
    """思维导图形式按本课内容自动选择（对应格式规范 §3.9「形式选择制」，不写死）：
    - 生词量 ≥25（词汇密集课）→ 彩色卡片簇（D），信息密度与分类感最强
    - 语法点 ≤1（阅读/方法导向课）→ 左侧横向树状（B），主干-分支清晰
    - 其余（词汇/语法/阅读均衡课）→ 中心辐射式（A），六分支全景
    生成 Agent 可在 4_素材清单.md 中按内容改为其他形式或提出创新形式。"""
    ncount = card.get("vocab", {}).get("new_count", 20)
    gcount = len(card.get("grammar", []))
    if ncount >= 25:
        return "cards"
    if gcount <= 1:
        return "tree"
    return "radial"

def _mm_vocab_panel(fw):
    """词汇分支面板：全部新词逐词列出（en + cn），五列词格铺开（§3.9 完整内容）。"""
    tiles = "".join('<div class="mm-w"><div class="mw-en">%s</div><div class="mw-cn">%s</div></div>'
                    % (w["en"], w["cn"]) for w in fw)
    return '<div class="mm-words">%s</div>' % tiles

def _mm_grammar_panel(card=None):
    """语法分支面板：本课各考点结构构成 + 例句（阶段A 通用化：grammar_bank 驱动，替代硬编码三考点）。
    未传 card 时为旧签名兼容（回退默认三考点）。"""
    gnames = card.get("grammar", []) if card else ["祈使句基础", "What特殊疑问句", "like的用法"]
    colors = ["mmg-red", "mmg-blue", "mmg-green", "mmg-gold", "mmg-purple", "mmg-teal"]
    cards = []
    for i, gname in enumerate(gnames[:6]):
        entry = grammar.get(gname, {})
        six = entry.get("六色卡", {})
        cls = colors[i % len(colors)]
        f = six.get("构成") or six.get("用法") or entry.get("构成", "按考点结构理解")
        ex = six.get("例句") or (entry.get("例句6", [""])[0])
        cards.append('<div class="mm-gram-card %s"><div class="mg-t">%s</div>'
                     '<div class="mg-f">%s</div><div class="mg-e">%s</div></div>'
                     % (cls, gname, _fmt_err(f), _fmt_err(ex)))
    return '<div class="mm-gram">%s</div>' % "".join(cards)

def _mm_reading_panel():
    """阅读分支面板：各篇题型 + 解题策略。"""
    cards = [
        '<div class="mm-rd-card"><div class="mg-t">阅读A · 细节题</div>回原文定位关键词，答案多在原词复现。</div>',
        '<div class="mm-rd-card"><div class="mg-t">阅读B · 记叙文</div>抓三餐 / 食物 / 喜好，理解主旨。</div>',
        '<div class="mm-rd-card"><div class="mg-t">阅读C · 五选四</div>看空白前后句逻辑，排除重复 / 矛盾项。</div>',
    ]
    return '<div class="mm-rd">%s</div>' % "".join(cards)

def _mm_phonics_panel(ph_words, ph_items):
    """拼读分支面板：各组合 + 代表词 + 发音（§3.9 完整内容）。"""
    tiles = "".join('<div class="mm-room-tile"><b>%s</b> %s</div>' % (w[:2], w) for w in ph_words)
    sound = " · ".join("%s /%s/" % (x, x) for x in ph_items)
    return ('<div class="mm-room">%s</div>'
            '<div class="mg-e" style="margin-top:8px">辅音连缀要连读：%s，不要分开读。</div>') % (tiles, sound)

def _mm_review_panel(card):
    """复习分支面板（阶段B 通用化）：上节课语法结构 + 全部上一课主题词逐词列出（§3.9 完整内容）。
    由上一课卡驱动；无上一课（L1）时用本课起点提示。"""
    prev = _prev_card(card)
    if not prev:
        return ('<div class="mm-gram"><div class="mm-gram-card mmg-gold"><div class="mg-t">本课起点</div>'
                '<div class="mg-f">第一课 · 语感热身</div><div class="mg-e">欢迎进入本课学习。</div></div></div>'
                '<div class="sub-label">本课主题词预告</div>')
    pwords = _prev_vocab_words(prev)
    tiles = "".join('<div class="mm-room-tile"><b>%s</b> %s</div>' % (w["en"], w["cn"]) for w in pwords)
    gnames = [g for g in prev.get("grammar", []) if g][:3] or ["语法回顾"]
    colors = ["mmg-gold", "mmg-gold", "mmg-gold"]
    cards = []
    for i, gname in enumerate(gnames):
        entry = grammar.get(gname, {})
        six = entry.get("六色卡", {})
        cards.append('<div class="mm-gram-card %s"><div class="mg-t">%s</div>'
                     '<div class="mg-f">%s</div><div class="mg-e">%s</div></div>'
                     % (colors[i % len(colors)], gname,
                        _fmt_err(six.get("构成") or entry.get("构成", "按上节课结构理解")),
                        _fmt_err(six.get("例句") or (entry.get("例句6", [""])[0]))))
    return ('<div class="mm-gram">%s</div>' % "".join(cards) +
            '<div class="sub-label">上节课%s主题词（%d 个）</div>' % (THEME_NAME.get(prev.get("vocab_theme", "review"), "本课"), len(pwords)) +
            '<div class="mm-room">%s</div>' % tiles)

def _mm_err_panel():
    """易错分支面板：易错规则 + 正确写法（§3.9 完整内容）。"""
    lines = [
        ('<b>Don&#39;t</b> 后接原形，不接 to', 'Don&#39;t run. ✓　Don&#39;t to run. ✗'),
        ('<b>What</b> 后助动词随主语', 'What do you like? / What does he like?'),
        ('三单主语用 <b>likes</b>', 'She likes milk. ✓　She like milk. ✗'),
        ('爱好用 <b>like to do</b>', 'I like to play basketball.'),
    ]
    return '<div class="mm-err">%s</div>' % "".join(
        '<div class="mm-err-line"><span>%s</span><span>%s</span></div>' % (a, b) for a, b in lines)

def mind_map(card, form="auto"):
    """课堂收尾·思维导图（格式规范 §3.9）：本课主题居中/成题头，六根分支；每个分支面板
    呈现该模块<b>完整内容</b>（词汇逐词、语法逐条含例句、阅读策略、拼读示例、上节课复习
    全内容、易错规则），复习分支默认展开。form ∈ auto/radial/tree/cards：
    auto 按课程卡内容自动选择；生成 Agent 可在调用处显式指定（选择制，非写死）。"""
    lesson = card["lesson"]
    theme = card["theme"]
    ph = card["phonics"]
    ph_items = [w.strip() for w in ph.split("/") if w.strip()] if "/" in ph else ["bl", "cl", "fl", "gl", "pl", "sl"]
    fw = theme_words(card.get("vocab", {}).get("theme", "food"), card.get("vocab", {}).get("new_count", 20))
    ph_entry = phonics.get(ph, {})
    ph_words = ph_entry.get("词族", ["blue", "clock", "flag", "glass", "play", "slow"])
    branches = [
        ("词汇", "🍎", "mm-red", _mm_vocab_panel(fw)),
        ("语法", "🧩", "mm-blue", _mm_grammar_panel(card)),
        ("阅读", "📖", "mm-green", _mm_reading_panel()),
        ("拼读", "🔤", "mm-purple", _mm_phonics_panel(ph_words, ph_items)),
        ("复习·上一课", "🔁", "mm-gold", _mm_review_panel(card)),
        ("易错", "🧠", "mm-teal", _mm_err_panel()),
    ]
    if form == "auto":
        form = _pick_mm_form(card)
    head = '<div class="mm-head">L%d · %s · 思维导图</div>' % (lesson, theme)
    if form == "cards":
        # D 彩色卡片簇：每支分类为一张彩色顶条卡片，卡内呈现完整内容
        mm_to_ext = {"mm-red": "", "mm-blue": "blue", "mm-green": "green",
                     "mm-gold": "gold", "mm-purple": "purple", "mm-teal": "teal"}
        out = [head, '<div class="mm-cards">']
        for label, icon, color, content in branches:
            ext_cls = mm_to_ext[color]
            cls = ("ext-card " + ext_cls).strip()
            out.append('<div class="%s"><div class="ext-cat">%s %s</div>%s</div>'
                       % (cls, icon, label, content))
        out.append('</div>')
        return "\n".join(out)
    if form == "tree":
        # B 左侧横向树状：左侧彩色主干、右侧完整内容（阅读/方法导向课更清晰）
        out = [head, '<div class="mm-tree">']
        for label, icon, color, content in branches:
            out.append('<div class="mm-tn %s">%s %s</div><div class="mm-tchips">%s</div>'
                       % (color, icon, label, content))
        out.append('</div>')
        return "\n".join(out)
    # A 中心辐射式（默认）：主题在圆心，六根主枝，底部面板点击切换（复习默认展开）
    pos = ["mm-b1", "mm-b2", "mm-b3", "mm-b4", "mm-b5", "mm-b6"]
    out = ['<div class="mm-wrap">',
           '<svg class="mm-lines" viewBox="0 0 100 100" preserveAspectRatio="none">',
           '<line x1="50" y1="38" x2="67" y2="26"/><line x1="50" y1="38" x2="83" y2="38"/>',
           '<line x1="50" y1="38" x2="67" y2="52"/><line x1="50" y1="38" x2="33" y2="52"/>',
           '<line x1="50" y1="38" x2="17" y2="38"/><line x1="50" y1="38" x2="33" y2="26"/></svg>',
           '<div class="mm-center"><div class="mm-c-emoji">🍚</div><div class="mm-c-en">L%d</div>'
           '<div class="mm-c-cn">%s</div></div>' % (lesson, theme)]
    for i, (label, icon, color, content) in enumerate(branches):
        active = " active" if label.startswith("复习") else ""
        out.append('<div class="mm-branch %s %s%s" data-color="%s">'
                   '<div class="mm-node" onclick="event.stopPropagation(); mmToggle(this)">'
                   '<span class="mm-icon">%s</span><span class="mm-label">%s</span></div>'
                   '<div class="mm-chips" style="display:none">%s</div></div>'
                   % (color, pos[i], active, color, icon, label, content))
    out.append('<div class="mm-panel mm-gold" id="mmPanel">'
               '<div class="mm-panel-title" id="mmPanelTitle">🔁 复习·上一课</div>'
               '<div class="mm-panel-chips" id="mmPanelChips">%s</div></div>' % branches[4][3])
    out.append('</div>')
    return "\n".join(out)

def mind_map_full(card):
    """思维导图 · 完整内容页（格式规范 §3.9「必须呈现完整内容」）：本课词汇全表逐词
    （en/音标/词性/中文）+ 语法全表（结构+例句）+ 上节课复习全表（语法+全部房间词）。
    与总览页组合成 2 页思维导图收尾环节。"""
    lesson = card["lesson"]
    fw = theme_words(card.get("vocab", {}).get("theme", "food"), card.get("vocab", {}).get("new_count", 20))
    w_tiles = "".join(
        '<div class="mmf-w"><div class="mmf-en">%s</div><div class="mmf-ph">%s</div>'
        '<div class="mmf-pos">%s</div><div class="mmf-cn">%s</div></div>'
        % (w["en"], w.get("phonetic", ""), w.get("pos", ""), w.get("cn", "")) for w in fw)
    room = "".join('<div class="mm-room-tile"><b>%s</b> %s</div>' % (en, cn) for cn, en in VDICT_L4)
    review_gram = ('<div class="mm-gram">'
                   '<div class="mm-gram-card mmg-gold"><div class="mg-t">名词复数</div>'
                   '<div class="mg-f">s/x/sh/ch → <b>-es</b></div><div class="mg-f">辅音+y → <b>-ies</b></div>'
                   '<div class="mg-e">box→boxes · shelf→shelves · watch→watches</div></div>'
                   '<div class="mm-gram-card mmg-gold"><div class="mg-t">房间介词</div>'
                   '<div class="mg-f">on 上 / in 里 / under 下</div><div class="mg-f">behind 后 / between 之间</div>'
                   '<div class="mg-e">The ball is under the chair.</div></div>'
                   '<div class="mm-gram-card mmg-gold"><div class="mg-t">There be</div>'
                   '<div class="mg-f">就近原则</div><div class="mg-f">复数 / 不可数用 are / is</div>'
                   '<div class="mg-e">There is a book and two pens.</div></div>'
                   '</div>')
    out = [section_head("图", "思维导图 · 本课词汇全表（%d 词）" % len(fw)),
           '<div class="mm-full-words">%s</div>' % w_tiles,
           section_head("图", "思维导图 · 本课语法全表"),
           '<div class="mm-full-gram">%s</div>' % _mm_grammar_panel(card),
           section_head("图", "思维导图 · 上节课复习全表"),
           review_gram +
           '<div class="sub-label">上节课房间词（%d 个）</div>' % len(VDICT_L4) +
           '<div class="mm-room">%s</div>' % room]
    return "\n".join(out)

# 题目稳定唯一 ID（§3.8.3）：每道选择题一个 Q 序号，build_lesson 启动时归零，保证同课件版本内唯一
_QSEQ = 0
# 学生代码（覆盖 CORE_JS 底座硬编码的 stu_xyj；底座红线不改，由 JS_EXTRA 尾部 var 覆盖）
STUDENT_CODES = {"许颖嘉": "stu_xyj", "邓兴华": "stu_dxh", "李民宪": "stu_lmx"}

def quiz_html(questions, cols=True):
    """选择题：默认 .quiz-cols 两列流式（Q1 左 Q2 右）；cols=False 输出单列（用于右栏阅读题）。
    每题 .quiz-q 注入 data-qid（Q 序号），供 saveAnswer 数据采集用。"""
    global _QSEQ
    letters = ["A", "B", "C", "D"]
    out = []
    for i, (stem, correct, distractors) in enumerate(questions):
        n = len(distractors) + 1
        pos = i % n
        opts = []
        d = 0
        for p in range(n):
            if p == pos:
                opts.append((letters[p], correct, "1"))
            else:
                opts.append((letters[p], distractors[d], "0")); d += 1
        _QSEQ += 1
        out.append('<div class="quiz-q" data-qid="Q%03d"><div class="qq-text">%s</div>' % (_QSEQ, stem))
        for letter, text, cor in opts:
            out.append('<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text))
        out.append('</div>')
    body = "".join(out)
    return '<div class="quiz-cols">%s</div>' % body if cols else body

# ---- Exit Ticket 数据（C3 §17：2 词汇主动提取 + 2 核心语法 + 1 真题迁移） ----
# 核心语法题：语法名 -> (stem, correct, [distractors])，quiz_html 直接渲染、可判。
_EXIT_GRAMMAR = {
    "祈使句基础": ("___ the door, please.", "Open", ["Opening", "Opens"]),
    "What特殊疑问句": ("___ do you like for breakfast?", "What", ["How", "Where"]),
    "like的用法": ("I like ___ to school.", "to walk", ["walking", "walks"]),
}
# 真题迁移开放题：语法名 -> (开放题引导, 参考思路 HTML)。中考「Why or why not」/写作迁移风格。
_EXIT_REAL = {
    "祈使句基础": ("给你的同桌写一句祈使句建议（肯定或否定）。",
               "<b>参考</b>：Please have breakfast. ／ Don&#39;t be late for school."),
    "What特殊疑问句": ("用 What 造一个问句，问问同伴三餐爱吃什么。",
               "<b>参考</b>：What do you like for breakfast?"),
    "like的用法": ("用 like 写一句关于食物的句子。",
               "<b>参考</b>：I like to eat apples."),
}
_EXIT_GRAMMAR_FALLBACK = ("请选语法正确的一项。", "This ___ a book.", ["am", "are"])
_EXIT_REAL_FALLBACK = ("请用本课核心语法写一句正确的英文（口头或笔头自测）。",
                       "<b>参考</b>：用本课语法点写一句英文，能自查自答即可。")

def exit_ticket(card, fw, skip=None):
    """Exit Ticket · 5 题形成性检测（C3 §17；不计入正式练习卷，课堂自查不批改）。
    构成：2 词汇主动提取（看中文→选英文，避开本课已考过的词）
         + 2 核心语法（读 _EXIT_GRAMMAR 表，键=语法名）
         + 1 真题迁移开放题（读 _EXIT_REAL 表，中考「Why or why not」/写作迁移风格）
    落位：段8 课堂总结之后、下节课预告之前。
    skip=本课已作为正确答案出现过的英文词（build_lesson 用 _collect_used_en_words 传入），
          Exit Ticket 词汇题自动避开，避免与课堂游戏重复。
    新增语法课时：请在 _EXIT_GRAMMAR / _EXIT_REAL 补该语法条目，否则走通用回退题。"""
    gnames = card.get("grammar", [])
    # ① 2 词汇主动提取（中文→英文；跳过本课已考词，保底回补）
    if skip is None:
        skip = set()
    targets = [w for w in fw if w["en"] not in skip][:2]
    if len(targets) < 2:
        for w in fw:
            if len(targets) >= 2:
                break
            if all(w["en"] != t["en"] for t in targets):
                targets.append(w)
    qs = list(vocab_cn2en(fw, targets))
    # ② 2 核心语法（按语法名取题，不足则通用回退）
    for gname in gnames:
        if len(qs) >= 4:
            break
        qs.append(_EXIT_GRAMMAR.get(gname, _EXIT_GRAMMAR_FALLBACK))
    while len(qs) < 4:
        qs.append(_EXIT_GRAMMAR_FALLBACK)
    # ③ 1 真题迁移开放题
    prompt, ref = _EXIT_REAL.get(gnames[0] if gnames else "", _EXIT_REAL_FALLBACK)
    body = (section_head("检", "Exit Ticket · 退出检测") +
            '<div class="body-text"><span class="highlight">5 题形成性检测</span>：2 词汇主动提取 ＋ 2 核心语法 ＋ 1 真题迁移。<b>课堂自查，不计入正式练习卷</b>。</div>' +
            quiz_html(qs))
    body += ('<div class="quiz-q"><div class="qq-text">真题迁移 · 开放作答</div>' +
             '<div class="body-text" style="margin:6px 0">%s</div>' % prompt +
             '<details class="et-ref" onclick="event.stopPropagation()"><summary style="cursor:pointer;color:#8b1e1e;font-weight:700">点击查看参考思路</summary>' +
             '<div class="note-panel" style="margin-top:8px"><div class="np-title">参考思路（形成性自查 · 不批改）</div>%s</div>' % ref +
             '</details></div>')
    body += ('<div class="note-panel"><div class="np-title">Exit Ticket 说明</div>' +
             '本页 5 题仅用于课堂收尾自查：答错当场回看对应语法/词汇页，全部弄懂才算过关，成绩不计入正式练习卷。</div>')
    return body

def theme_words(theme, n=20):
    """按课程卡主题选取本课 n 个目标词（通用化，替代原 food 硬编码）。
    优先取该主题词库词；若不足，用其他主题词补齐，保证每课 20 词全覆盖。"""
    fw = [w for w in vocab if w.get("theme") == theme]
    if len(fw) < n:
        extra = [w for w in vocab if w.get("theme") != theme]
        fw = fw + extra[:n - len(fw)]
    return fw[:n]

def word_tuple(w):
    return (w["en"], w.get("phonetic", ""), w.get("pos", ""), w.get("cn", ""),
            w.get("collocation", ""), w.get("example", ""), w.get("hook", ""))

# ============================================================
# 阶段B 通用化：上/下节课复习与预告（lesson_map 驱动，替代硬编码 L4/L6）
# ============================================================
def _prev_card(card):
    """上一课课程卡（lesson_map 驱动）。返回 None 表示无上一课（L1 或数据缺失）。"""
    n = card.get("lesson")
    if not n:
        return None
    return _lessons_map.get(str(n - 1))

def _next_card(card):
    """下一课课程卡（lesson_map 驱动）。返回 None 表示无下一课。"""
    n = card.get("lesson")
    if not n:
        return None
    return _lessons_map.get(str(n + 1))

def _gram_q_from_err(gname, entry, limit=2):
    """从 grammar_bank 的「易错5」（'错误 → 正确' 对）生成"哪项正确"选择题。
    grammar_bank 缺失或解析失败时返回空表，由调用方回退兜底。"""
    out = []
    for e in entry.get("易错5", []):
        if len(out) >= limit:
            break
        mv = re.match(r'\s*(.+?)\s*→\s*(.+?)(?:\s*[（(].*)?$', e)
        if mv:
            wrong = mv.group(1).strip()
            right = mv.group(2).strip()
            if wrong and right and wrong != right:
                out.append(("%s · 下列哪项正确？" % gname, right, [wrong]))
    return out

def _prev_vocab_words(prev):
    """上一课词汇：按上一课 vocab_theme 从词库取 20 词（通用化，替代固定房间词）。"""
    theme = (prev or {}).get("vocab_theme", "review")
    return theme_words(theme, 20)

def _pick_reading(card, slot):
    """按 card 课号从 passage 库选阅读篇（阶段C 通用化：替代固定 L05 篇）。
    slot: 'a'/'b'（A/B 篇）。优先课号精确匹配 XYJ2026_L{lesson:02d}_reading_{slot}；
    仅当该篇完整（含 questions）才采用；无匹配或题目缺失时回退 L5 基线篇。"""
    lesson = (card or {}).get("lesson")
    if lesson:
        want = "XYJ2026_L%02d_reading_%s" % (lesson, slot)
        for p in passages:
            if p.get("id") == want and p.get("questions"):
                return p
    # L5 基线兜底（保证装配器始终可产出）
    for p in passages:
        if p["id"] == "XYJ2026_L05_reading_%s" % slot and p.get("questions"):
            return p
    return None

def _passage_quiz(p):
    """把 passage 库篇的 questions（含 opts+answer）转成 quiz_html 输入列表。
    返回 [(stem, correct, [distractors])...]；无完整题目返回 None。"""
    qs = p.get("questions") or []
    out = []
    for q in qs:
        opts = q.get("opts") or []
        ans = q.get("answer")
        if not opts or not ans:
            continue
        correct, dist = None, []
        for letter, text in opts:
            if letter == ans:
                correct = text
            else:
                dist.append(text)
        if correct is None:
            continue
        out.append((q.get("q"), correct, dist))
    return out or None

def _reading_ans_note(p, quiz):
    """由 passage 题目答案生成「答案解析」逐题定位说明（阶段C 通用化：基于真实答案，不捏造）。
    返回 HTML 字符串。"""
    qs = p.get("questions") or []
    parts = []
    for i, q in enumerate(qs):
        ans = q.get("answer")
        if not ans:
            continue
        parts.append("题%d（%s）定位原文核对" % (q.get("num", i + 1), ans))
    return "；".join(parts) if parts else "答案分布已校验，无主导字母，请回原文定位核对。"

def _prev_review_html(card, prev, fallback=""):
    """上一课复习（阶段B 通用化）：由上一课卡驱动生成「语法闯关 + 词汇闯关」两页内文。
    返回 (grammar_inner, vocab_inner)。
    - prev 存在（L2+）→ 由上一课卡驱动；
    - prev 缺失且 lesson_map 整体缺失（数据退化）→ 用 fallback 的 L4 基线兜底；
    - prev 缺失但 lesson_map 存在（L1 首课）→ 通用「本课起点」导学页，绝不回退到 L4 硬编码。"""
    if not prev:
        if not _lessons_map and fallback:
            return fallback
        vtheme = card.get("vocab", {}).get("theme", "review")
        pre_words = theme_words(vtheme, 8)
        g_inner = (section_head("复", "本课起点 · 一起来热身") +
                   '<div class="body-text"><span class="highlight">欢迎开启第一课</span>！先热身，再进入本课新词与语法。</div>' +
                   game_board("热身小测", "🎯", "几道轻松题，唤醒英语感觉。", quiz_html([("Hello 的中文是？", "你好", ["再见", "谢谢"]),
                       ("thank you 的中文是？", "谢谢", ["你好", "再见"])])) +
                   '<div class="note-panel"><div class="np-title">闯关提示</div>答对即可进入正课。</div>')
        v_inner = (section_head("复", "本课语感 · 词汇初探") +
                   '<div class="body-text">先认识本课主题词，新词页会系统学习。</div>' +
                   '<div class="sub-label">本课主题词预告</div>' +
                   flash_grid([(w["cn"], w["en"]) for w in pre_words]) +
                   '<div class="note-panel"><div class="np-title">闯关说明</div>翻牌预热，正式学习在下一段。</div>')
        return (g_inner, v_inner)
    gnames = [g for g in prev.get("grammar", []) if g][:3]
    pwords = _prev_vocab_words(prev)
    ptheme = THEME_NAME.get(prev.get("vocab_theme", "review"), "本课")
    # 语法闯关：从 grammar_bank 易错5 生成纠错题；不足用通用回退题
    pgram_qs = []
    for gname in gnames:
        pgram_qs += _gram_q_from_err(gname, grammar.get(gname, {}), limit=2)
    if not pgram_qs:
        pgram_qs = [("上节课语法：哪项正确？", "Please choose the right one.", ["Wrong one"])]
    g_inner = (section_head("复", "上节课 · 语法快闪闯关") +
               '<div class="body-text">还记得上节课的 <span class="highlight">%s</span> 吗？点击作答，答对有彩带动画！</div>' % " / ".join(gnames) +
               game_board("上节课 %s 个语法点" % len(gnames), "⚡", "从上节课语法点里各抽题，快速唤醒记忆。", quiz_html(pgram_qs)) +
               '<div class="note-panel"><div class="np-title">闯关提示</div>答错回看对应语法页，全对再进新词。</div>')
    # 词汇闯关：看中文选英文（8 问）+ 翻牌自检全部 20 词
    pvocab_qs = vocab_cn2en(pwords, pwords[:8])
    v_inner = (section_head("复", "上节课 · 词汇闯关") +
               '<div class="body-text">上节课 %d 个%s主题词还记得吗？先闯关再翻牌自检。</div>' % (len(pwords), ptheme) +
               game_board("%s主题词 8 连问" % ptheme, "🎮", "看中文，选英文，音形义一次叫醒。", quiz_html(pvocab_qs)) +
               '<div class="sub-label">翻牌自检 · 全部 %d 词</div>' % len(pwords) +
               flash_grid([(w["cn"], w["en"]) for w in pwords]) +
               '<div class="note-panel"><div class="np-title">闯关说明</div>翻牌看到英文对照；错一处回到上节课对应语法页重学，务必全对再进新词。</div>')
    return (g_inner, v_inner)

def _next_preview_html(card, nxt, fallback=""):
    """下节课预告（阶段B 通用化）：由下一课卡驱动生成预告页内文；无下一课时用 fallback 兜底。"""
    if not nxt:
        return fallback
    gnames = [g for g in nxt.get("grammar", []) if g][:3]
    tname = THEME_NAME.get(nxt.get("vocab_theme", "review"), "本课")
    pts = [("语法%d" % (i + 1), g or "相关表达") for i, g in enumerate(gnames)]
    pts.append(("新词", "%s主题核心词汇" % tname))
    return (section_head("结", "下节课预告 · 第 %d 课") % (nxt.get("lesson", card.get("lesson", 0) + 1)) +
            key_points(pts) +
            '<div class="note-panel"><div class="np-title">课前准备</div>复习本课要点，下节课将围绕「%s · %s」展开。</div>' % (tname, " / ".join(gnames)))

def _grammar_overview_table(card):
    """本课考点一览表（阶段A 通用化：grammar_bank 驱动，替代硬编码祈使句/What/like 表）。"""
    gnames = [g for g in card.get("grammar", []) if g][:3]
    rows = []
    for gname in gnames:
        entry = grammar.get(gname, {})
        six = entry.get("六色卡", {})
        struct = six.get("构成") or entry.get("构成", "按考点结构理解")
        ex = six.get("例句") or (entry.get("例句6", [""])[0])
        rows.append('<tr><td class="gt-key">%s</td><td>%s</td><td class="gt-en">%s</td></tr>'
                    % (gname, _fmt_err(struct), _fmt_err(ex)))
    return ('<div class="glance-table"><table>'
            '<tr><th>句型</th><th>结构</th><th>示例</th></tr>' + "".join(rows) + '</table></div>')

def _grammar_summary_cards(card):
    """本课考点综合梳理（阶段A 通用化：grammar_bank 六色卡驱动，替代硬编码综合梳理卡）。"""
    gnames = [g for g in card.get("grammar", []) if g][:3]
    colors = ["red", "blue", "green", "gold", "purple", "teal"]
    items = []
    for i, gname in enumerate(gnames):
        entry = grammar.get(gname, {})
        six = entry.get("六色卡", {})
        body = six.get("用法") or six.get("构成") or entry.get("构成", "按考点结构理解")
        items.append((gname, colors[i % len(colors)], _fmt_err(body)))
    exs, seen = [], set()
    for gname in gnames:
        for e in grammar.get(gname, {}).get("例句6", []):
            if e not in seen:
                seen.add(e); exs.append((e, gname))
    return ext_cards(items) + '<div class="sub-label">实战例句</div>' + example_section(exs[:3])

# ============================================================
# 自然拼读互动练习（多形态：辨音/解码/归类/补全）
# ============================================================
PHONICS_POOL = {
  # 辅音连缀
  "bl": ["blue", "black", "blow", "block", "blanket", "blind"],
  "cl": ["clock", "class", "clean", "clever", "climb", "close"],
  "fl": ["flag", "fly", "flower", "floor", "flat", "flip"],
  "gl": ["glass", "glad", "glow", "globe", "glove", "glue"],
  "pl": ["play", "please", "plate", "plane", "plant", "plus"],
  "sl": ["slow", "sleep", "slide", "slim", "slip", "slipper"],
  "br": ["bread", "brown", "brother", "bridge", "bring", "brush"],
  "cr": ["cry", "crab", "cross", "crown", "cream", "crocodile"],
  "dr": ["dress", "draw", "drink", "driver", "drop", "dream"],
  "fr": ["fruit", "frog", "friend", "front", "fresh", "from"],
  "tr": ["tree", "train", "truck", "trip", "try", "true"],
  "gr": ["grape", "green", "grass", "grandpa", "great", "grow"],
  # 元音组合
  "ar": ["car", "farm", "park", "star", "arm", "dark"],
  "or": ["for", "morning", "sport", "short", "horse", "corner"],
  "ir": ["bird", "girl", "first", "shirt", "skirt", "dirty"],
  "er": ["teacher", "father", "mother", "sister", "dinner", "water"],
  "ur": ["nurse", "turn", "purple", "hurt", "Thursday", "curtain"],
  "ai": ["rain", "wait", "train", "paint", "tail", "mail"],
  "ay": ["day", "play", "say", "way", "may", "stay"],
  "ea": ["eat", "sea", "teacher", "clean", "meat", "dream"],
  "ee": ["see", "three", "tree", "green", "sleep", "week"],
  "oa": ["boat", "coat", "goat", "road", "soap", "toast"],
  "ow": ["snow", "window", "yellow", "grow", "know", "bowl"],
  "oo": ["moon", "school", "food", "room", "book", "good"],
  "ou": ["house", "mouse", "cloud", "mouth", "about", "loud"],
  "oi": ["coin", "join", "point", "noise"],
  "oy": ["boy", "toy", "joy", "enjoy"],
  # 单辅音/字母组
  "th": ["think", "three", "thank", "thin", "thumb", "thunder"],
  "sh": ["ship", "shop", "shirt", "short", "shoe", "wash"],
  "ch": ["chair", "chicken", "China", "cheese", "child", "teach"],
  "wh": ["what", "where", "when", "why", "white", "wheel"],
  "ph": ["phone", "photo", "elephant", "dolphin", "alphabet", "physics"],
  "ng": ["sing", "thing", "morning", "king", "long", "swing"],
  "nk": ["pink", "drink", "thank", "think", "sink"],
  # 短元音
  "a": ["cat", "hat", "map", "bag", "hand", "apple"],
  "e": ["bed", "pen", "egg", "leg", "ten", "red"],
  "i": ["pig", "big", "sit", "six", "milk", "fish"],
  "o": ["dog", "box", "hot", "fox", "clock", "frog"],
  "u": ["cup", "bus", "sun", "jump", "run", "duck"],
  # 魔法e
  "a_e": ["cake", "name", "make", "late", "plane", "grape"],
  "i_e": ["kite", "five", "nine", "like", "bike", "ride"],
  "o_e": ["home", "nose", "rose", "note", "stone", "hope"],
  "u_e": ["cute", "use", "tube", "mule", "June", "cube"],
  # 后缀/r
  "y": ["happy", "sunny", "my", "fly", "cry", "why"],
  "ing": ["running", "swimming", "eating", "reading", "playing", "walking"],
}

def _ph_combos(combo_str):
    """'bl/cl/fl/gl/pl/sl' → ['bl','cl','fl','gl','pl','sl']；短元音 'a/e/i/o/u' 同理。"""
    return [p.strip() for p in re.split(r'[/\s]+', combo_str or "") if p.strip()]

def _ph_sounds(sound_str):
    """'/bl/ /kl/ /fl/' → ['bl','kl','fl']（去掉斜杠，保留 IPA 字符）。"""
    return re.findall(r'/([^/]+)/', sound_str or "")

def _ph_groups(combo_str, sound_str, rep_words):
    """把 组合/发音/词族 对齐成 [{combo,sound,words}]，词优先 PHONICS_POOL、缺则词族兜底。"""
    combos = _ph_combos(combo_str)
    sounds = _ph_sounds(sound_str)
    groups = []
    for i, c in enumerate(combos):
        s = sounds[i] if i < len(sounds) else (sounds[-1] if sounds else "")
        words = PHONICS_POOL.get(c)
        if not words and i < len(rep_words):
            words = [rep_words[i]]
        if words:
            groups.append({"combo": c, "sound": s, "words": list(words)})
    return groups

def _ph_diff_groups(groups, i):
    """与第 i 组发音不同的其他组（避免 ir/er/ur 同音造成歧义）。"""
    s = groups[i]["sound"]
    return [j for j, g in enumerate(groups) if j != i and g["sound"] != s and g["words"]]

def phonics_practice_pages(ph_entry):
    """自然拼读互动练习（多形态），返回 list[(标题, 副标题, inner_html)]。
    形态1 辨音选词（音→词）｜形态2 解码（词→组合）｜形态3 词族归类（找同类）｜形态4 拼写补全（缺组合）。
    全部走 quiz_html（checkOpt 正误反馈 + IndexedDB），离线可用；无同音歧义题。
    """
    groups = _ph_groups(ph_entry.get("组合", ""), ph_entry.get("发音", ""), ph_entry.get("词族", []))
    pages = []
    if len(groups) < 2:
        return pages
    # 形态1：辨音选词（音→词）
    q1 = []
    for i, g in enumerate(groups):
        dg = _ph_diff_groups(groups, i)
        if not dg:
            continue
        q1.append(("哪个单词含 %s 的音？" % ("/" + g["sound"] + "/"),
                   g["words"][0], [groups[j]["words"][0] for j in dg[:2]]))
    if q1:
        pages.append(("辨音选词 · 音→词", "看音标，点选含该发音的单词",
            section_head("拼", "拼读闯关 ① · 辨音选词") +
            sub_label("看音标，点选含有该发音的单词（答对响铃 + 彩带）") +
            '<div class="note-panel"><div class="np-title">玩法</div>读出左上的音标，再从三个词里选出含该音的单词。</div>' +
            quiz_html(q1)))
    # 形态2：解码（词→组合）
    q2 = []
    for i, g in enumerate(groups):
        others = [o["combo"] for j, o in enumerate(groups) if j != i][:3]
        if not others:
            continue
        q2.append(("“%s” 的拼读组合是？" % g["words"][0], g["combo"], others))
    if q2:
        pages.append(("解码高手 · 词→组合", "看单词，选出它的发音组合",
            section_head("拼", "拼读闯关 ② · 解码高手") +
            sub_label("看单词，点选它的发音组合（blue → bl）") +
            quiz_html(q2)))
    # 形态3：词族归类（找同类）
    q3 = []
    for i, g in enumerate(groups):
        if len(g["words"]) < 2:
            continue
        dg = _ph_diff_groups(groups, i)
        if not dg:
            continue
        q3.append(("哪个词和 “%s” 一样，也发 %s？" % (g["words"][0], "/" + g["sound"] + "/"),
                   g["words"][1], [groups[j]["words"][0] for j in dg[:2]]))
    if q3:
        pages.append(("词族归类 · 找同类", "按发音组合把单词归到一组",
            section_head("拼", "拼读闯关 ③ · 词族归类") +
            sub_label("每个组合都有同族词，找出和示例词同组合的词") +
            quiz_html(q3)))
    # 形态4：拼写补全（缺组合）
    q4 = []
    for i, g in enumerate(groups):
        others = [o["combo"] for j, o in enumerate(groups) if j != i][:3]
        if not others or g["combo"] not in g["words"][0]:
            continue
        q4.append(("补全单词 %s（缺的字母组合）" % g["words"][0].replace(g["combo"], "___", 1),
                   g["combo"], others))
    if q4:
        pages.append(("拼写补全 · 缺组合", "看残缺单词，补出字母组合",
            section_head("拼", "拼读闯关 ④ · 拼写补全") +
            sub_label("先读残缺单词，点选该补上的字母组合") +
            quiz_html(q4)))
    return pages

# ============================================================
# 主构建
# ============================================================
# ── 六色卡正文结构化（2026-08-03 教师反馈：正文逐行平铺无重点 → 易错行/序列块/例句引用/关键词高亮）──
_SIX_STOP = {"a", "an", "the", "and", "or", "of", "to", "in", "on", "at", "for", "with", "by",
             "is", "are", "am", "be", "it", "he", "she", "we", "you", "they", "not", "no", "so",
             "but", "from", "as", "this", "that", "do", "does", "if"}

def _esc(t):
    return html.escape(t, quote=False)

def _kw_hl(t):
    """中文说明中的英文关键词加粗（跳过高频功能词）。"""
    t = _esc(t)
    def repl(m):
        w = m.group(0)
        if w.lower() in _SIX_STOP:
            return w
        return '<b class="rc-kw">%s</b>' % w
    return re.sub(r"[A-Za-z][A-Za-z0-9'’\-/]*", repl, t)

def _is_english_sentence(t):
    alpha = [c for c in t if c.isalpha()]
    if not alpha:
        return False
    return sum(1 for c in alpha if ord(c) < 128) / len(alpha) > 0.8

def _fmt_err(text):
    """❌/✅ 易错对 → 红错行 / 绿对行。"""
    tokens = re.split(r"(❌|✅)", text)
    rows = []
    for i in range(1, len(tokens), 2):
        mark = tokens[i]
        seg = tokens[i + 1] if i + 1 < len(tokens) else ""
        seg = re.sub(r"→", "", seg).strip().strip("，；,;/:：").strip()
        if not seg:
            continue
        if mark == "❌":
            rows.append('<div class="rc-err-row"><span class="rc-err-mark">✕</span><span>%s</span></div>' % _esc(seg))
        else:
            rows.append('<div class="rc-fix-row"><span class="rc-fix-mark">✓</span><span>%s</span></div>' % _esc(seg))
    return "".join(rows)

def fmt_six_body(text):
    """六色卡正文按内容结构重排：❌/✅→红/绿行；> / → / + / / 序列→块；纯英例句→引用；其余→关键词高亮。"""
    if not text:
        return ""
    text = text.strip()
    if "❌" in text or "✅" in text:
        return _fmt_err(text)
    if ">" in text:
        parts = [p.strip() for p in text.split(">") if p.strip()]
        if len(parts) >= 2:
            return '<span class="rc-seq">' + "".join('<span class="rc-chip">%s</span>' % _esc(p) for p in parts) + '</span>'
    if "→" in text:
        segs = [s.strip() for s in re.split(r"[，,；;]", text) if s.strip()]
        arrow = [s for s in segs if "→" in s]
        other = [s for s in segs if "→" not in s]
        if arrow:
            body = '<span class="rc-seq">' + "".join(
                '<span class="rc-chip">%s</span>' % re.sub("→", '<b class="rc-arw">→</b>', _esc(s)) for s in arrow) + '</span>'
            if other:
                body = "".join('<span class="rc-note">%s</span>' % _esc(s) for s in other) + body
            return body
    if "+" in text:
        parts = [p.strip() for p in text.split("+") if p.strip()]
        if len(parts) >= 2:
            return '<span class="rc-seq">' + "".join('<span class="rc-chip">%s</span>' % _esc(p) for p in parts) + '</span>'
    if "/" in text:
        parts = [p.strip() for p in text.split("/") if p.strip()]
        if len(parts) >= 2 and all(re.search(r"[A-Za-z]", p) for p in parts):
            ratios = []
            for p in parts:
                alpha = [c for c in p if c.isalpha()]
                ratios.append(sum(1 for c in alpha if ord(c) < 128) / len(alpha) if alpha else 0.0)
            if all(r > 0.55 for r in ratios):
                return '<span class="rc-seq">' + "".join('<span class="rc-chip">%s</span>' % _esc(p) for p in parts) + '</span>'
    if _is_english_sentence(text):
        return '<span class="rc-example">%s</span>' % _esc(text)
    return _kw_hl(text)

def build_lesson(card):
    global _QSEQ
    _QSEQ = 0
    lesson = card["lesson"]
    theme = card["theme"]
    tier = card["tier"]
    # 形式轮换（2026-08-03 教师反馈：封面/翻牌卡形式去同质化）
    cover_variant = ["cover-variant-a", "cover-variant-b", "cover-variant-c"][lesson % 3]
    global _RECALL_VARIANT
    _RECALL_VARIANT = ["", "recall-variant-b", "recall-variant-c"][lesson % 3]
    # 主题化扩展：封面 emoji + 词汇卡形式变体
    vtheme = card.get("vocab", {}).get("theme", "review")
    from theme_colors import THEME_EMOJI, THEME_NAME
    cover_emoji = THEME_EMOJI.get(vtheme, "🎯⭐")
    tname = THEME_NAME.get(vtheme, "本课")  # 主题中文名（通用化文案）
    vocab_variant = ["vocab-variant-a", "vocab-variant-b", "vocab-variant-c"][lesson % 3]
    stage = card["stage"]
    gnames = card["grammar"]
    ph = card["phonics"]
    new_count = card["vocab"]["new_count"]
    title = "第%d课时 · %s" % (lesson, theme)
    stage_badge = "%s · Stage %s · L%d" % (tier, stage, lesson)
    pages = {}
    seg = {}
    page_meta = {}
    p = 1
    def add(inner, seg_id, t="", sub="", priority="CORE", minutes=5):
        nonlocal p
        pages[p] = page(p, t, sub, inner, active=(p == 1))
        seg.setdefault(seg_id, [p, p]); seg[seg_id][1] = p
        page_meta[p] = {"p": priority, "m": minutes}
        p += 1

    # ---- 段1 封面 + 复习导入（游戏化） ----
    cover = ('<div class="cover-wrap %s">' % cover_variant +
             '<div class="cover-badge">第 %d 课时</div>'
             '<div class="cover-title">%s</div>'
             '<div class="cover-sub">%s</div>'
             '<div class="cover-tagline">基础 · 七上</div>'
             '<div class="cover-info">'
             '<div class="cover-info-num"><div class="ci-label">新词</div><div class="ci-val">%d</div></div>'
             '<div class="cover-info-num"><div class="ci-label">语法考点</div><div class="ci-val">3</div></div>'
             '<div class="cover-info-num"><div class="ci-label">页数</div><div class="ci-val">45</div></div>'
             '</div>'
             '<div class="cover-emoji">%s</div></div>' % (lesson, theme, tier, new_count, cover_emoji))
    add(cover, 1)

    goal = (section_head("标", "本课学习目标") +
            '<div class="chip-row">'
            '<div class="chip"><span class="chip-icon">🆕</span>%d 个%s主题高频词</div>'
            '<div class="chip"><span class="chip-icon">🧩</span>祈使句 / What 问句 / like 用法</div>'
            '<div class="chip"><span class="chip-icon">📖</span>记叙 / 说明 / 应用阅读</div>'
            '<div class="chip"><span class="chip-icon">🔤</span>%s 拼读</div>'
            '</div>' +
            '<div class="kmap">' +
            '<div class="kmap-node"><div class="kn-title">词汇</div><div class="kn-body">%d 个%s主题高频词，滚动复现。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">语法</div><div class="kn-body">祈使句、What 问句、like 用法。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">阅读</div><div class="kn-body">A/B 细节 + C 五选四逻辑衔接。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">拼读</div><div class="kn-body">%s 连缀拼读。</div></div>' +
            '</div>' +
            '<div class="note-panel"><div class="np-title">闯关规则</div>先玩「上节课闯关」把旧知识叫醒，再进入本课新词与语法，全对即可通关。</div>') % (new_count, tname, ph, new_count, tname, ph)
    add(goal, 1, "第5课时 · 学习目标", "四个模块一目了然")

    # 上节课复习（阶段B 通用化：由上一课卡驱动，替代硬编码 L4；语料缺失回退 L4 基线）
    prev = _prev_card(card)
    _prev_fallback = (
        (section_head("复", "上节课 · 语法快闪闯关") +
         '<div class="body-text">还记得上节课的 <span class="highlight">名词复数 / 房间介词 / There be</span> 吗？点击作答，答对有彩带动画！</div>' +
         game_board("名词复数 / 介词 / There be", "⚡", "从上节课 3 个语法点里各抽几题，快速唤醒记忆。", quiz_html(adapt_l4(QUIZ_L4[:6] + QUIZ_EXTRA_L4[:4]))) +
         '<div class="note-panel"><div class="np-title">闯关提示</div>名词变复数看词尾（box→boxes / shelf→shelves）；介词看空间关系（on 上 / in 里 / under 下 / behind 后）；There be 看就近原则。</div>'),
        (section_head("复", "上节课 · 词汇闯关") +
         '<div class="body-text">上节课 20 个房间词还记得吗？先闯关再翻牌自检。</div>' +
         game_board("房间词 8 连问", "🎮", "看中文，选英文，音形义一次叫醒。", quiz_html([("椅子 是哪个词？", "chair", ["sofa", "lamp"]),
             ("整洁的 是哪个词？", "tidy", ["messy", "dirty"]),
             ("在…后面 是哪个词？", "behind", ["between", "above"]),
             ("球 是哪个词？", "ball", ["soccer", "habit"]),
             ("抽屉 是哪个词？", "drawer", ["wardrobe", "shelf"]),
             ("总是 是哪个词？", "always", ["never", "sometimes"]),
             ("干净的 是哪个词？", "clean", ["tidy", "dirty"]),
             ("在…之间 是哪个词？", "between", ["behind", "above"])])) +
         '<div class="sub-label">翻牌自检 · 全部 20 词</div>' +
         flash_grid(VDICT_L4) +
         '<div class="note-panel"><div class="np-title">闯关说明</div>翻牌看到英文对照；错一处回到上节课对应语法页重学，务必全对再进新词。</div>'))
    l4g, l4v = _prev_review_html(card, prev, _prev_fallback)
    if prev:
        prev_gnames = [g for g in prev.get("grammar", []) if g][:3] or ["语法回顾"]
        prev_tname = THEME_NAME.get(prev.get("vocab_theme", "review"), "本课")
        add(l4g, 1, "上节课 · 语法闯关", " / ".join(prev_gnames))
        add(l4v, 1, "上节课 · 词汇闯关", "上节课 %s 主题词 · 翻牌自检" % prev_tname)
    else:
        add(l4g, 1, "本课起点 · 热身", "语感热身 · 开启第一课")
        add(l4v, 1, "本课语感 · 词汇初探", "主题词预告 · 翻牌预热")

    # ---- 段2 新词20（卡片 + 每批趣味闯关 + 拓展卡） ----
    fw = theme_words(vtheme, new_count)
    add(section_head("词", "新词 ①（1–10）· 食物与日常") + sub_label("点击卡片 · 音标/搭配/例句") +
        '<div class="vocab-zone %s">%s</div>' % (vocab_variant, vocab_cards([word_tuple(w) for w in fw[:10]])),
        2, "新词学习 ①", "食物 · 三餐 · 动词")
    add(section_head("词", "新词 ① · 趣味闯关") +
        game_board("看英文，选中文", "🎯", "刚学的 10 个词，立刻闯关检验。", quiz_html(vocab_en2cn(fw[:10]))), 2, "新词闯关 ①", "即时巩固")
    add(section_head("词", "新词 ②（11–20）· 食物与日常") + sub_label("点击卡片 · 音标/搭配/例句") +
        '<div class="vocab-zone %s">%s</div>' % (vocab_variant, vocab_cards([word_tuple(w) for w in fw[10:20]])),
        2, "新词学习 ②", "水果 · 饮品 · 形容词")
    add(section_head("词", "新词 ② · 趣味闯关") +
        game_board("看英文，选中文", "🏆", "后 10 个词闯关，答对撒彩带。", quiz_html(vocab_en2cn(fw[10:20]))), 2, "新词闯关 ②", "即时巩固")
    add(section_head("词", "新词速记 · 记忆地图") +
        sub_label("分组记 + 高频搭配，结构化成卡") +
        ext_cards([
            ("三餐组", "red", "一日三餐 <span class=\"ext-en\">breakfast / lunch / dinner</span>，搭配动词 <b>have</b>：<b>have breakfast</b>。"),
            ("水果组", "green", "<span class=\"ext-en\">apple / banana / orange / fruit</span>，泛指水果用 <b>fruit</b>（不可数）。"),
            ("饮品组", "blue", "<span class=\"ext-en\">water / milk / juice</span>，量词搭配：<b>a glass of milk</b> / <b>a cup of tea</b>。"),
            ("主食组", "gold", "<span class=\"ext-en\">rice / bread / egg</span>，不可数用 <b>a piece of bread</b>；可数用 <b>two eggs</b>。"),
            ("状态词", "purple", "<b>hungry</b> 饿（想吃饭）／ <b>thirsty</b> 渴（想喝水），搭配 be：<b>I am hungry.</b>"),
            ("核心动词", "red", "<b>eat</b> 吃（固体）／ <b>drink</b> 喝（液体）／ <b>like</b> 喜欢，本课高频使用。"),
        ]) +
        '<div class="note-panel"><div class="np-title">记忆策略</div>① 按三餐/水果/饮品/主食分组记；② 用搭配短语带动单词；③ 每词造一句。</div>', 2, "新词速记", "分组 · 搭配 · 词族")
    cloze_inner = section_head("词", "词汇运用 · 选词填空") + sub_label("用本课新词补全句子")
    cloze_q = [("I have ___ at seven in the morning.", "breakfast", ["lunch", "dinner"]),
               ("I drink a glass of ___ every day.", "milk", ["rice", "egg"]),
               ("___ is good for your health.", "Vegetables", ["Candy", "Cola"]),
               ("I like ___ for lunch.", "noodles", ["desk", "book"]),
               ("She is ___ now. She wants to eat.", "hungry", ["thirsty", "tired"]),
               ("An ___ a day is good.", "apple", ["orange", "egg"]),
               ("We eat ___ for dinner.", "fish", ["pen", "bag"]),
               ("___ is a healthy drink.", "Water", ["Cola", "Juice"])]
    cloze_inner += quiz_html(cloze_q)
    cloze_inner += '<div class="note-panel"><div class="np-title">解析</div>① breakfast 与 have 搭配；② milk 与 a glass of 搭配；③ Vegetables 与 healthy 呼应；④ noodles 为午餐主食；⑤ hungry 表饥饿；⑥ apple 与 An 搭配；⑦ fish 为晚餐食物；⑧ Water 为健康饮品。</div>'
    add(cloze_inner, 2, "词汇运用", "选词填空 · 词义搭配")
    add(section_head("词", "近义词 / 形近词辨析") +
        ext_cards([
            ("food / fruit", "red", "<span class=\"ext-en\">food</span> 泛指<b>食物</b>；<span class=\"ext-en\">fruit</span> 特指<b>水果</b>。<b>healthy food</b> 健康食品。"),
            ("drink / eat", "blue", "<span class=\"ext-en\">drink</span> <b>喝（液体）</b>；<span class=\"ext-en\">eat</span> <b>吃（固体）</b>。<b>eat rice / drink water</b>。"),
            ("hungry / thirsty", "green", "<b>hungry</b> <b>饿</b>；<b>thirsty</b> <b>渴</b>。饿了想<b>eat</b>，渴了想<b>drink</b>。"),
            ("breakfast / lunch / dinner", "gold", "早/午/晚餐，都搭配 <b>have</b>：<b>have breakfast</b>。<b>for + 餐名</b> 表某一餐：<b>for breakfast</b>。"),
            ("rice / noodles", "purple", "<b>rice</b> 米饭（不可数）；<b>noodles</b> 面条（可数复数）。均为主食 staple food。"),
            ("water / juice", "blue", "<b>water</b> 水（最健康）；<b>juice</b> 果汁。<b>a glass of water / a cup of juice</b>。"),
        ]) +
        '<div class="note-panel"><div class="np-title">辨析口诀</div>形近看首尾字母，词义靠搭配；food/fruit、drink/eat 最易混，多写三遍。</div>' +
        '<div class="body-text">辨析不是死记，而是见词想搭档：<span class="highlight">breakfast→have</span>，<span class="highlight">milk→a glass of</span>，<span class="highlight">hungry→be hungry</span>。</div>', 2, "近义 / 形近辨析", "成对记忆 · 避免混淆")
    add(section_head("词", "听写自测 · 翻牌核对") + sub_label("看中文，翻牌核对英文拼写") +
        flash_grid([(w["cn"], w["en"]) for w in fw[:12]]) +
        '<div class="body-text">家长可对照此页听写；错词请回到新词页重记。</div>' +
        '<div class="note-panel"><div class="np-title">记忆提示</div>先记三餐/水果/饮料名词，再记 hungry/thirsty 形容词，分组记忆效率更高。</div>', 2, "听写自测", "翻牌核对拼写")

    # ---- 段3 语法精讲（构成用结构图 + 易错改选择 + 六色卡） ----
    err_mcqs = {
        "祈使句基础": [("哪个句子是正确的？", "Don't run in the classroom.",
                       ["Don't to run in the classroom.", "Don't running in the classroom."]),
                      ("哪个句子是正确的？", "Open the door, please.",
                       ["Opens the door, please.", "Please you open the door."]),
                      ("哪个句子是正确的？", "Don't watch TV too long.",
                       ["Don't to watch TV too long.", "Not watch TV too long."])],
        "What特殊疑问句": [("哪个句子是正确的？", "What do you like?",
                          ["What you like?", "What does you like?"]),
                         ("哪个句子是正确的？", "What is your name?",
                          ["What your name?", "What are your name?"]),
                         ("哪个句子是正确的？", "What sports do you like?",
                          ["What sport does you like?", "What sports you like?"])],
        "like的用法": [("哪个句子是正确的？", "I like to play basketball.",
                       ["I like play basketball.", "I like to playing basketball."]),
                      ("哪个句子是正确的？", "She likes milk.",
                       ["She like milk.", "She is like milk."]),
                      ("哪个句子是正确的？", "I like sports.",
                       ["I likes sports.", "I am like sports."])],
    }
    for gi, gname in enumerate(gnames, 1):
        entry = grammar.get(gname, {})
        six = entry.get("六色卡", {})
        # 六色卡记忆分级（2026-08-03 教师反馈）：用法/构成/口诀=重点记忆★，易错=难点▲，例句/注意=理解即可○
        _LV = {"rc-zhug": "key", "rc-bin": "key", "rc-xing": "warn", "rc-ming": "hint", "rc-warn": "hint", "rc-qita": "key"}
        _LB = {"key": ("rule-key", "★ 重点记忆"), "warn": ("rule-warn", "▲ 难点"), "hint": ("rule-hint", "○ 理解即可")}
        cards_html = "".join(
            '<div class="rule-card %s %s"><div class="rc-cat">%s<span class="rc-badge %s">%s</span></div>'
            '<div class="rc-text">%s</div></div>' % (cls, _LB[_LV[cls]][0], cat, _LV[cls], _LB[_LV[cls]][1], fmt_six_body(txt))
            for cls, (cat, txt) in zip(["rc-zhug", "rc-bin", "rc-xing", "rc-ming", "rc-warn", "rc-qita"], six.items()))
        pa = (section_head("法", "考点%d · %s" % (gi, gname)) +
              '<div class="sub-label">一 · 构成与用法</div>' +
              grammar_structure(gname, entry) +
              '<div class="sub-label">二 · 典型例句</div>' +
              example_section([(e, "例句%d" % i) for i, e in enumerate(entry.get("例句6", []), 1)]) +
              '<div class="sub-label">三 · 中考怎么考</div>' +
              '<div class="note-panel"><div class="np-title">考法预警</div>%s</div>' % entry.get("中考考法", ""))
        add(pa, 3, "语法① · 构成与用法" if gi == 1 else "语法%d · 构成与用法" % gi, gname)
        e5 = [tuple(e.split(" → ")) for e in entry.get("易错5", []) if " → " in e]
        pb = (section_head("法", "考点%d · 易错闯关 + 口诀 + 色卡" % gi) +
              '<div class="sub-label">三 · 高频易错 · 选一选</div>' +
              '<div class="body-text">与其硬背，不如自己选！找出<b>正确</b>的句子，答对得彩带。</div>' +
              game_board("易错点选一选", "🧠", "从三个句子中选出正确的那个。", quiz_html(err_mcqs.get(gname, []))) +
              '<div class="sub-label">四 · 记忆口诀</div>' +
              '<div class="note-panel"><div class="np-title">口诀</div>%s</div>' % entry.get("口诀", "") +
              '<div class="sub-label">五 · 语法要点色卡</div>' +
              '<div class="rule-grid">' + cards_html + '</div>')
        add(pb, 3, "语法%d · 易错与色卡" % gi, gname)
        if gname == "祈使句基础":
            qz = quiz_html([("___ the door, please.", "Open", ["Opening", "Opens"]),
                            ("___ run in the classroom.", "Don't", ["Not", "No"])])
        elif gname == "What特殊疑问句":
            qz = quiz_html([("___ do you like?", "What", ["How", "Where"]),
                            ("What ___ you like?", "do", ["does", "is"])])
        else:
            qz = quiz_html([("She ___ apples.", "likes", ["like", "liking"]),
                            ("I like ___ basketball.", "playing", ["play", "plays"])])
        add(section_head("法", "考点%d · 中考小测" % gi) + qz + '<div class="body-text">即时判定，答错自动回看对应讲解页。</div>', 3, "语法%d · 中考小测" % gi, gname)

    add(section_head("法", "三大考点一览表") + _grammar_overview_table(card) +
        '<div class="note-panel"><div class="np-title">对照记忆</div>对照本课结构，逐行复述，理解各考点之间的衔接与区别。</div>', 3, "三大考点一览表", "结构速查")

    gsum = (section_head("法", "三大考点综合梳理") +
            _grammar_summary_cards(card))
    add(gsum, 3, "三大考点综合梳理", "三条主线一张图")

    zhenti = (section_head("法", "中考真题体验 · 祈使句与 What 问句") +
              '<div class="reading-passage">' +
              '<p>___ (open) the door, please. ___ (not) run in the classroom.</p>' +
              '<p>What ___ (do) you like? I like ___ (play) basketball.</p></div>' +
              quiz_html([("1. 祈使句否定用哪个词？", "Don't", ["Not", "No"]),
                         ("2. What 后三单主语用哪个助动词？", "does", ["do", "is"])]) +
              '<div class="body-text">中考常把祈使句与特殊疑问句混在同一语篇中考查，务必看清结构。</div>' +
              '<div class="note-panel"><div class="np-title">真题解析</div>题1 祈使句否定用 Don&#39;t 加原形；题2 What 后接三单主语用 does。</div>')
    add(zhenti, 3, "中考真题体验", "省卷原题改编")

    pfill = section_head("法", "语法综合应用 · 祈使句/What/like 填空") + sub_label("用正确结构填空")
    pfill += quiz_html([("___ the window, please.", "Open", ["Opening", "Opens"]),
                        ("___ do you have for breakfast?", "What", ["How", "Where"]),
                        ("He ___ playing soccer.", "likes", ["like", "liking"]),
                        ("___ eat too much candy.", "Don't", ["Not", "No"])])
    pfill += '<div class="body-text">综合考查祈使句、What 问句与 like 用法，是中考语法填空微型演练。</div>'
    pfill += '<div class="note-panel"><div class="np-title">填空思路</div>① 句首动词原形→祈使句；② 对事物提问→What；③ 三单主语→likes；④ 否定命令→Don&#39;t。</div>'
    add(pfill, 3, "语法综合填空", "祈使句 / What / like 混考")

    # ---- 段4 随堂演练 ----
    quiz_all = [
        ("1. ___ the door, please.", "Open", ["Opening", "Opens", "Opened"]),
        ("2. ___ run in the classroom.", "Don't", ["Not", "No", "Doesn't"]),
        ("3. ___ do you like?", "What", ["How", "Where", "Who"]),
        ("4. She ___ apples.", "likes", ["like", "liking", "liked"]),
        ("5. I like ___ basketball.", "playing", ["play", "plays", "played"]),
        ("6. ___ go to school together.", "Let's", ["Let", "Lets", "Let us to"]),
        ("7. What ___ you like?", "do", ["does", "is", "are"]),
        ("8. He doesn't ___ fast food.", "like", ["likes", "liking", "liked"]),
        ("9. ___ quiet, please.", "Be", ["Is", "Are", "Am"]),
        ("10. What ___ your name?", "is", ["are", "am", "do"]),
        ("11. ___ eat too much candy.", "Don't", ["Not", "No", "Doesn't"]),
        ("12. What ___ he like?", "does", ["do", "is", "are"]),
        ("13. I like ___ milk.", "drinking", ["drink", "drinks", "drank"]),
        ("14. ___ the window, please.", "Open", ["Opening", "Opens", "Opened"]),
        ("15. What ___ they like?", "do", ["does", "is", "are"]),
        ("16. She ___ milk.", "likes", ["like", "liking", "liked"]),
        ("17. ___ play soccer after school.", "Let's", ["Let", "Lets", "Let us to"]),
        ("18. Don't ___ late.", "be", ["is", "are", "am"]),
        ("19. What ___ you have for breakfast?", "do", ["does", "is", "are"]),
        ("20. He likes ___ TV.", "watching", ["watch", "watches", "watched"]),
        ("21. ___ your book, please.", "Open", ["Opening", "Opens", "Opened"]),
        ("22. What ___ she like?", "does", ["do", "is", "are"]),
        ("23. I don't ___ fast food.", "like", ["likes", "liking", "liked"]),
        ("24. ___ be quiet.", "Please", ["Please to", "Pleaseing", "Pleaseed"]),
        ("25. What ___ this?", "is", ["are", "am", "do"]),
        ("26. She likes ___ fruit.", "eating", ["eat", "eats", "ate"]),
        ("27. ___ run in the hall.", "Don't", ["Not", "No", "Doesn't"]),
        ("28. What ___ you want?", "do", ["does", "is", "are"]),
        ("29. ___ the door, please.", "Open", ["Opening", "Opens", "Opened"]),
        ("30. What ___ she like?", "does", ["do", "is", "are"]),
        ("31. I like ___ fruit.", "eating", ["eat", "eats", "ate"]),
        ("32. ___ run in the hall.", "Don't", ["Not", "No", "Doesn't"]),
        ("33. What ___ you want?", "do", ["does", "is", "are"]),
        ("34. She ___ fruit.", "likes", ["like", "liking", "liked"]),
        ("35. ___ the window, please.", "Open", ["Opening", "Opens", "Opened"]),
        ("36. What ___ he like?", "does", ["do", "is", "are"]),
        ("37. ___ eat too much candy.", "Don't", ["Not", "No", "Doesn't"]),
        ("38. What ___ they like?", "do", ["does", "is", "are"]),
        ("39. I like ___ milk.", "drinking", ["drink", "drinks", "drank"]),
        ("40. ___ be quiet.", "Please", ["Please to", "Pleaseing", "Pleaseed"]),
    ]
    q1 = section_head("练", "随堂演练 ① · 语法选择（1–20）") + game_board("随堂演练 ①", "📝", "本课语法一次到位，每题答对有彩带。", quiz_html(quiz_all[:14]))
    q1 += '<div class="note-panel"><div class="np-title">解题锦囊</div>① 祈使句句首动词原形；② 否定用 Don&#39;t；③ What 后助动词随主语变（三单 does）；④ like 三单 likes，like to do 表爱好。</div>'
    add(q1, 4, "随堂演练 ①", "语法选择 1–20")
    q2 = section_head("练", "随堂演练 ② · 语法选择（21–40）") + game_board("随堂演练 ②", "🎲", "继续闯关，冲击全对。", quiz_html(quiz_all[14:]))
    q2 += '<div class="note-panel"><div class="np-title">解题锦囊</div>看清主语人称决定助动词（do/does）；祈使句否定一律 Don&#39;t 加原形；like 后接名词或 to do。</div>'
    add(q2, 4, "随堂演练 ②", "语法选择 21–40")

    drill = section_head("练", "句型操练 · 中译英（点击翻牌看答案）") + sub_label("用本课语法翻译下列句子")
    drill += flash_grid([("请开门。", "Open the door, please."),
                         ("不要在教室里跑。", "Don't run in the classroom."),
                         ("你喜欢什么？", "What do you like?"),
                         ("我喜欢苹果。", "I like apples."),
                         ("她喜欢牛奶。", "She likes milk."),
                         ("我们一起去上学吧。", "Let's go to school together."),
                         ("你喜欢打篮球吗？", "Do you like playing basketball?"),
                         ("他不喜欢快餐。", "He doesn't like fast food."),
                         ("请安静。", "Be quiet, please."),
                         ("你早餐吃什么？", "What do you have for breakfast?"),
                         ("我喜欢喝牛奶。", "I like drinking milk."),
                         ("不要迟到。", "Don't be late.")])
    drill += '<div class="body-text">先自己说/写英文，再翻牌核对；重点用对祈使句、What 问句与 like 表达。</div>'
    drill += '<div class="note-panel"><div class="np-title">翻译要点</div>祈使句句首动词原形；What 问句注意助动词；like 后接名词或 to do。</div>'
    add(drill, 4, "句型操练", "中译英 · 翻牌自检")

    err = section_head("练", "改错专练 · 选一选") + sub_label("找出正确句子")
    err += '<div class="body-text">五组易错句，选择<b>正确</b>版本，理解为什么错。</div>'
    err += quiz_html([("Don't to run. 的正确写法？", "Don't run.", ["Don't to run.", "Don't running."]),
                      ("Let's goes. 的正确写法？", "Let's go.", ["Let's goes.", "Let's going."]),
                      ("He like apples. 的正确写法？", "He likes apples.", ["He like apples.", "He is like apples."]),
                      ("What is you like? 的正确写法？", "What do you like?", ["What is you like?", "What you like?"]),
                      ("I like play basketball. 的正确写法？", "I like to play basketball.", ["I like play basketball.", "I like playing basketball."])])
    err += '<div class="note-panel"><div class="np-title">改错思路</div>① Don&#39;t 后接原形不接 to；② Let&#39;s 后接原形；③ 三单主语用 likes；④ What 后助动词随主语；⑤ like to do 表爱好。</div>'
    add(err, 4, "改错专练", "选出正确句子 · 理解错因")

    # ---- 段5 阅读理解（阶段C 通用化：A/B 篇由 passage 库按课号选择，替代固定 L05 篇） ----
    pa = _pick_reading(card, "a")
    if pa is None:
        pa = next((x for x in passages if x["id"] == "HN2026_L6_reading_a"), passages[0])
    paras_a = [s.strip() + "." for s in pa["text"].replace("A ", "").split(".") if s.strip()]
    a_quiz = _passage_quiz(pa) or [("What is the passage mainly about?", "reading passage", ["wrong answer"])]
    a_title = pa.get("title") or ("阅读 A · 篇章理解（左文右题）")
    ra_page = (section_head("读", a_title) +
               '<div class="pri-row"><span class="pri-badge pri-core">CORE · 课堂必做</span>'
               '<span class="pri-note">课堂精读 · 三篇都读，但只有 A 是课上必须完成</span></div>' +
               '<div class="read-split">' +
               '<div class="read-left">' +
               '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in paras_a) + '</div>' +
               '<div class="note-panel"><div class="np-title">阅读提示</div>先读题干圈关键词，再回原文定位；细节题答案多在原词复现。</div>' +
               '</div>' +
               '<div class="read-right">' +
               '<div class="read-right-head">📝 理解题 · 边读边选</div>' +
               '<div class="read-qs-scroll">' +
               quiz_html(a_quiz, cols=False) +
               '</div>' +
               '</div>' +
               '</div>' +
               '<div class="note-panel"><div class="np-title">答案解析</div>' + _reading_ans_note(pa, a_quiz) + '</div>')
    add(ra_page, 5, "阅读 A · 篇章＋理解题", "左文右题 · 边读边选", priority="CORE", minutes=8)

    pb = _pick_reading(card, "b")
    if pb is None:
        pb = next((x for x in passages if x["id"] == "HN2026_L6_reading_b"), pa)
    paras_b = [s.strip() + "." for s in pb["text"].replace("A ", "").split(".") if s.strip()]
    b_quiz = _passage_quiz(pb) or [("What is the passage mainly about?", "reading passage", ["wrong answer"])]
    b_title = pb.get("title") or ("阅读 B · 篇章理解（左文右题）")
    rb_page = (section_head("读", b_title) +
               '<div class="pri-row"><span class="pri-badge pri-extend">EXTEND · 时间充足时做</span>'
               '<span class="pri-note">时间不够可跳过，不影响核心闭环</span></div>' +
               '<div class="read-split">' +
               '<div class="read-left">' +
               '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in paras_b) + '</div>' +
               '<div class="note-panel"><div class="np-title">阅读提示</div>先读题干圈关键词，再回原文定位；细节题答案多在原词复现。</div>' +
               '</div>' +
               '<div class="read-right">' +
               '<div class="read-right-head">📝 理解题 · 边读边选</div>' +
               '<div class="read-qs-scroll">' +
               quiz_html(b_quiz, cols=False) +
               '</div>' +
               '</div>' +
               '</div>' +
               '<div class="note-panel"><div class="np-title">答案解析</div>' + _reading_ans_note(pb, b_quiz) + '</div>')
    add(rb_page, 5, "阅读 B · 篇章＋理解题", "左文右题 · 边读边选", priority="EXTEND", minutes=6)

    # 阅读 C 五选四：语篇库 w5 条目 questions 为空（选项「待生成」），数据不足时不得编造，
    # 故沿用 L5 基线五选四正文/选项（阶段C 通用化：A/B 已完成，w5 待语篇库补选项后交付）。
    w5text = "Eating healthy food is important for every student at school. Good food is the fuel for your body and your brain. A good breakfast helps you listen and learn in class with a clear mind. __(11)__ We should eat fruit every day after our three meals because fruit gives us vitamins. __(12)__ Fresh vegetables help our body grow tall and stay strong, so eat them often. __(13)__ Drink milk for strong bones and white teeth every morning before school. __(14)__ A good diet keeps us happy and full of energy for the whole day."
    w5paras = [s.strip() for s in w5text.split(".") if s.strip()]
    w5opts = [("A", "Fruit gives us vitamins."), ("B", "We also need water every day."),
              ("C", "Candy is bad for our teeth."), ("D", "Exercise is good for us, too."),
              ("E", "Cola is a good drink for health.")]
    w5ans = {11: "A", 12: "B", 13: "D", 14: "C"}
    rc_page = (section_head("读", "阅读 C · 五选四（左文右题）") +
               '<div class="pri-row"><span class="pri-badge pri-home">HOME · 课后完成</span>'
               '<span class="pri-note">培优课后做 · 逻辑衔接专练</span></div>' +
               '<div class="read-split">' +
               '<div class="read-left">' +
               '<div class="reading-passage">' + "".join("<p>%s</p>" % x for x in w5paras) + '</div>' +
               '<div class="note-panel"><div class="np-title">中文大意</div>健康饮食对学生很重要。好早餐帮助专心听讲；每天吃水果补充维生素；多吃蔬菜长得高；早餐前喝牛奶强健骨骼；健康饮食让人整天快乐有活力。</div>' +
               '</div>' +
               '<div class="read-right">' +
               '<div class="read-right-head">📝 五选四 · 逻辑衔接</div>' +
               '<div class="read-qs-scroll">' +
               '<div class="sub-label">从 A–E 中选最佳句填入空白（E 为多余项）</div>')
    for num in sorted(w5ans.keys()):
        ans = w5ans[num]
        rc_page += '<div class="w5-qq">__（%d）__ 应填：</div><div class="w5-opts">' % num
        for letter, text in w5opts:
            cor = '1' if letter == ans else '0'
            rc_page += '<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (cor, letter, text)
        rc_page += '</div>'
    rc_page += ('</div></div></div>' +
                '<div class="note-panel"><div class="np-title">答案解析</div>11→A（fruit 与 vitamins 呼应）；12→B（water 与 drink 呼应）；13→D（exercise 与 move 呼应）；14→C（candy 与 teeth 呼应）；E 为多余项，五选四。</div>')
    add(rc_page, 5, "阅读 C · 篇章＋五选四", "左文右题 · 逻辑衔接", priority="HOME", minutes=6)

    reading_tip = (section_head("读", "阅读解题 SOP") +
                   key_points([("先题后文", "先读题干圈关键词，再回原文定位。"),
                               ("细节题", "题干词多在原文原词复现，直接比对。"),
                               ("五选四", "看空白前后句逻辑，排除重复/矛盾项。"),
                               ("防陷阱", "注意人称与单复数一致。"),
                               ("猜词法", "利用上下文线索、同义复现猜测生词含义。"),
                               ("主旨题", "找首尾句与高频词，避免以偏概全。")]) +
                   '<div class="note-panel"><div class="np-title">本课的阅读</div>A/B 篇为细节题，C 篇为五选四逻辑衔接题，答案分布已校验无主导字母。</div>')
    add(reading_tip, 5, "阅读解题 SOP", "六步法")

    # （原「阅读实战」页已移除：与阅读A/B理解题重复，让位给思维导图完整内容页）
    # ---- 段6 自然拼读（展示 1 页 + 互动闯关 ≤4 页：辨音/解码/归类/补全）----
    ph_entry = phonics.get(ph, {})
    ph_sound = ph_entry.get("发音", "/bl/ /kl/ /fl/ /gl/ /pl/ /sl/")
    ph_combo = ph_entry.get("组合", "bl/cl/fl/gl/pl/sl")
    ph_groups = _ph_groups(ph_combo, ph_sound, ph_entry.get("词族", []))
    ph_cards = "".join('<div class="phonics-card"><div class="pc-letter">%s</div><div class="pc-word">%s</div><div class="pc-cn">%s</div></div>' % (g["combo"], g["words"][0], g["words"][0]) for g in ph_groups)
    ph_words_line = " · ".join("%s /%s/" % (g["combo"], g["sound"]) for g in ph_groups)
    ph_chant = "；<br>".join("%s %s %s" % (g["combo"], g["combo"], g["words"][0]) for g in ph_groups)
    ph_families = "｜".join("%s: %s" % (g["combo"], "、".join(g["words"][:4])) for g in ph_groups)
    add(section_head("拼", "自然拼读 · %s" % " / ".join(ph_combo.split("/"))) +
        sub_label("%s 的发音" % ph_words_line) +
        '<div class="phonics-grid">' + ph_cards + '</div>' +
        '<div class="note-panel"><div class="np-title">发音</div>%s</div>' % ph_sound +
        '<div class="note-panel"><div class="np-title">词族</div>%s</div>' % ph_families +
        '<div class="note-panel"><div class="np-title">拼读儿歌</div>%s；<br>连起来读，不要分开！</div>' % ph_chant,
        6, "自然拼读", "%s · 词族 · 儿歌" % ph_combo)
    for _i, (_t, _s, _inner) in enumerate(phonics_practice_pages(ph_entry)):
        add(_inner, 6, "拼读闯关", "闯关 %d · %s" % (_i + 1, _t))

    # ---- 段7 课堂游戏 ----
    cv1 = section_head("戏", "课堂游戏 · 跨课词汇快选 ①") + sub_label("看中文，选出正确英文")
    cv1 += '<div class="note-panel"><div class="np-title">玩法</div>点击与中文对应的英文词，答对响铃 + 彩带。</div>'
    cv1 += quiz_html([("食物 是哪个词？", "food", ["book", "desk"]),
                      ("牛奶 是哪个词？", "milk", ["rice", "egg"]),
                      ("苹果 是哪个词？", "apple", ["orange", "banana"]),
                      ("水 是哪个词？", "water", ["juice", "tea"]),
                      ("早餐 是哪个词？", "breakfast", ["lunch", "dinner"]),
                      ("饥饿的 是哪个词？", "hungry", ["thirsty", "tired"])])
    cv1 += '<div class="note-panel"><div class="np-title">提示</div>遇到形近词（food/fruit、drink/eat）先辨词义再选。</div>'
    add(cv1, 7, "课堂游戏 ①", "跨课词汇快选")
    listen = section_head("戏", "听音选词 · 词义匹配") + sub_label("下列英文，哪个意思是吃？")
    listen += quiz_html([("吃 对应：", "eat", ["drink", "run"]),
                         ("喝 对应：", "drink", ["eat", "play"]),
                         ("喜欢 对应：", "like", ["watch", "sound"]),
                         ("观看 对应：", "watch", ["like", "play"]),
                         ("玩 对应：", "play", ["eat", "drink"]),
                         ("听起来 对应：", "sound", ["watch", "like"])])
    listen += '<div class="body-text">巩固本课核心词义，为听力与完形打底。</div>'
    add(listen, 7, "课堂游戏 ②", "听音选词")

    # ---- 段8 课堂总结 ----
    summary = (section_head("结", "课堂总结 · 知识图谱") +
               '<div class="kmap">' +
               '<div class="kmap-node"><div class="kn-title">祈使句</div><div class="kn-body">动词原形开头；否定 Don&#39;t 加原形；提议 Let&#39;s 加原形。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">What 问句</div><div class="kn-body">What 加助动词加主语加原形加问号，对事物提问。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">like 用法</div><div class="kn-body">like 加名词 / to do；三单 likes；否定 doesn&#39;t。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">自然拼读</div><div class="kn-body">bl/cl/fl/gl/pl/sl 辅音连缀。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">学习建议</div><div class="kn-body">每天听写 5 词加造 2 句，周末回头复习，祈使句与 What 问句务必脱口而出。</div></div>' +
               '</div>' +
               '<div class="note-panel"><div class="np-title">课后作业</div>① 背诵本课 20 个新词（家长听写）；② 完成配套基础练习；③ 用祈使句、What 问句、like 各写 2 句；④ 整理错题本（本课易错 12 句）。</div>' +
               '<div class="note-panel"><div class="np-title">巩固建议</div>错题本按祈使句/What 问句/like 用法三类归档，每周回看一次，避免重复犯错。</div>')
    add(summary, 8, "课堂总结", "知识图谱")
    # Exit Ticket（C3 §17：⑧课堂总结后、⑨思维导图前；5 题形成性检测，不计入正式练习卷）
    # 词汇题自动避开本课已考过的词（课堂游戏/选词填空等），防重复
    add(exit_ticket(card, fw, skip=_collect_used_en_words(pages)), 8, "Exit Ticket", "5 题形成性检测", priority="CORE", minutes=3)
    preview = _next_preview_html(card, _next_card(card), fallback=(
        section_head("结", "下节课预告 · 第 6 课") +
        key_points([("语法①", "一般现在时实义动词。"),
                    ("语法②", "want/like 表达。"),
                    ("语法③", "食物可数与不可数。"),
                    ("新词", "三餐与饮食习惯相关词汇。")]) +
        '<div class="note-panel"><div class="np-title">课前准备</div>复习本课祈使句、What 问句与 like 用法，下节课用它们谈论三餐与饮食习惯。</div>' +
        '<div class="note-panel"><div class="np-title">课前任务</div>① 默写本课 20 词（家长签字）；② 用 like 各造 1 句；③ 预习一般现在时含义。</div>'))
    nxt = _next_card(card)
    nxt_lesson = (nxt or {}).get("lesson", lesson + 1)
    add(preview, 8, "下节课预告", "第 %d 课" % nxt_lesson)

    # ---- 段9 课堂思维导图（收尾复盘，含上节课复习） ----
    mm = (section_head("图", "课堂思维导图 · 本课全貌") +
          '<div class="body-text"><span class="highlight">本课知识 + 上节课复习</span> 一图收拢：点击彩色分支，面板展开该模块<b>完整内容</b>（词汇逐词、语法含例句）。</div>' +
          mind_map(card) +
          '<div class="note-panel"><div class="np-title">怎么用</div>课堂收尾用这张图把「上节课复习 + 本课新词/语法/阅读/拼读/易错」串成一张图，学生看着图复述一遍即完成复盘。</div>')
    add(mm, 9, "课堂思维导图", "本课全貌 · 含上节课复习")
    mm_full = (section_head("图", "思维导图 · 完整内容页") +
               '<div class="body-text"><span class="highlight">词汇全表 · 语法全表 · 上节课复习全表</span> 逐项铺开，对照自测。</div>' +
               mind_map_full(card) +
               '<div class="note-panel"><div class="np-title">课后复盘</div>看着全表逐项自测：能否读出每个词、讲清每条语法结构、说出上节课三个语法点？卡住处标记为下周复习重点。</div>')
    add(mm_full, 9, "思维导图 · 完整内容", "词汇全表 · 语法全表 · 复习全表")

    total = p - 1
    seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
    # 覆盖 CORE_JS 底座硬编码 studentId（底座红线不改），保证各学生答题记录归属正确
    scode = STUDENT_CODES.get(card.get("student", ""), "stu_xyj")
    js_extra = ("var studentId='" + scode + "';\n" +
                JS_EXTRA_TPL % (total, json.dumps(seg_pages, ensure_ascii=False),
                                json.dumps(page_meta, ensure_ascii=False)))
    # 主题化配色（2026-08-03 教师反馈：各课件配色不得同质化）——按本课 vocab_theme 注入独立主色系
    from theme_colors import build_theme_css
    theme_css = build_theme_css(card.get("vocab", {}).get("theme", "review"))
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
    html = build_courseware(title=title, pages_dict=pages, js_extra=js_extra,
                            session="L%02d" % lesson, nav_html=NAV,
                            stage_badge=stage_badge, n_pages=total,
                            css_extra=CSS_CONTRACT_MARKERS + CSS_EXTRA + theme_css)
    # 注入 HTML 合同标记到封面页首（CW-VISUAL-CONTRACT:1 标记新合同课件）
    html = html.replace(
        '<div class="cover-wrap',
        '<!-- CW-VISUAL-CONTRACT:1 -->\n<div class="cover-wrap',
        1
    )
    return html

if __name__ == "__main__":
    card = {
        "lesson": 5, "student": "许颖嘉", "tier": "基础", "stage": "S1", "type": "normal",
        "grammar": ["祈使句基础", "What特殊疑问句", "like的用法"], "theme": "食物与日常",
        "vocab": {"new_count": 20, "review_count": 0, "theme": "food"},
        "phonics": "bl/cl/fl/gl/pl/sl",
        "reading": {"genres": ["记叙文", "说明文", "应用文"], "w5": True, "vocab_rate": "15%"},
        "listening": False,
        "interactions": {"count_equals_new_knowledge_points": True},
        "output": ["html", "docx", "outline_courseware", "outline_practice"]
    }
    html = build_lesson(card)
    out = os.path.join(HERE, "test_L5_courseware.html")
    open(out, "w", encoding="utf-8").write(html)
    print("L5 课件生成：%s (%d bytes)" % (out, len(html.encode("utf-8"))))
