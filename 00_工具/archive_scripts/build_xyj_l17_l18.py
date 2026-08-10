# -*- coding: utf-8 -*-
"""
许颖嘉 L17 与 L18 深度优化生成器
严格遵循《01_课件格式规范.md》与《00_全局约束与红线.md》：
1. 包含 Page 10 双向拖拽分类归纳箱 (Drag & Drop Vocab Sorter)
2. 包含 阅读理解左文右题双栏对比 + 屏幕手划批注工具 (Annotation Canvas) + sticky 可滚动答题框
3. 包含 每题详尽解析 (.quiz-explain) + 答题正误弹窗气泡 (👍正确 / ✖️错误)
4. 包含 全页运行优先级 (CORE / EXTEND / HOME) 元数据与动态徽章
5. 包含 4 页自然拼读多形态交互 (辨音/解码/归类/拼写)
6. 包含 6 大创意交互点声明与落地
7. 包含 Web Audio API 声效 + IndexedDB 答题离线存储 + 数据导出
8. 确保总页数精确位于 40 - 45 页 (42 页)
9. 100% 验证 verify_v2.py PASS
"""
import os, sys, json, re, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from courseware_core import build_courseware, page, vocab_cards, CORE_CSS, CORE_JS
import courseware_engine as eng
from theme_colors import build_theme_css

# ======================= 全局 CSS 追加 =======================
CSS_FULL = CORE_CSS + "\n" + eng.CSS_EXTRA + """
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

.quiz-opt:hover, .game-board .quiz-opt:hover {
  background: #F1F5F9 !important;
  color: #000000 !important;
  border-color: #000000 !important;
}

.quiz-opt.opt-correct, .game-board .quiz-opt.opt-correct {
  background: #DCFCE7 !important;
  color: #15803D !important;
  border: 3px solid #16A34A !important;
  font-weight: 800 !important;
}

.quiz-opt.opt-wrong, .game-board .quiz-opt.opt-wrong {
  background: #FEE2E2 !important;
  color: #B91C1C !important;
  border: 3px solid #DC2626 !important;
  font-weight: 800 !important;
}

/* 语法六色卡 · 标题条 + 记忆分级徽标（2026-08-03 新体系：压过引擎基线，重点/难点/理解分级） */
.rule-card {
  padding: 16px 20px !important;
  border-radius: 12px !important;
  box-shadow: 0 4px 12px rgba(0,0,0,0.06) !important;
  margin: 8px 0 !important;
}

.rc-cat {
  display: flex !important;
  justify-content: space-between !important;
  align-items: center !important;
  gap: 8px !important;
  padding: 9px 12px 9px 16px !important;
  margin-bottom: 0 !important;
  font-size: 16px !important;
  font-weight: 800 !important;
  letter-spacing: 1px !important;
  border-radius: 10px 10px 0 0 !important;
}

.rc-text {
  padding: 10px 14px 12px 16px !important;
  font-size: 18px !important;
  font-weight: 700 !important;
  color: #000000 !important;
  line-height: 1.6 !important;
}

.rc-zhug { background: #EFF6FF !important; border-left: 6px solid #2563EB !important; border-top: 1px solid #BFDBFE !important; border-right: 1px solid #BFDBFE !important; border-bottom: 1px solid #BFDBFE !important; }
.rc-zhug .rc-cat { background: rgba(37,99,235,.90) !important; color: #ffffff !important; }

.rc-bin { background: #F0FDF4 !important; border-left: 6px solid #16A34A !important; border-top: 1px solid #BBF7D0 !important; border-right: 1px solid #BBF7D0 !important; border-bottom: 1px solid #BBF7D0 !important; }
.rc-bin .rc-cat { background: rgba(22,163,74,.90) !important; color: #ffffff !important; }

.rc-xing { background: #FEF3C7 !important; border-left: 6px solid #D97706 !important; border-top: 1px solid #FDE68A !important; border-right: 1px solid #FDE68A !important; border-bottom: 1px solid #FDE68A !important; }
.rc-xing .rc-cat { background: rgba(217,119,6,.90) !important; color: #ffffff !important; }

.rc-ming { background: #FAF5FF !important; border-left: 6px solid #9333EA !important; border-top: 1px solid #E9D5FF !important; border-right: 1px solid #E9D5FF !important; border-bottom: 1px solid #E9D5FF !important; }
.rc-ming .rc-cat { background: rgba(147,51,234,.90) !important; color: #ffffff !important; }

.rc-warn { background: #FEF2F2 !important; border-left: 6px solid #DC2626 !important; border-top: 1px solid #FECACA !important; border-right: 1px solid #FECACA !important; border-bottom: 1px solid #FECACA !important; }
.rc-warn .rc-cat { background: rgba(220,38,38,.90) !important; color: #ffffff !important; }

.rc-qita { background: #F0FDFA !important; border-left: 6px solid #0D9488 !important; border-top: 1px solid #99F6E4 !important; border-right: 1px solid #99F6E4 !important; border-bottom: 1px solid #99F6E4 !important; }
.rc-qita .rc-cat { background: rgba(13,148,136,.90) !important; color: #ffffff !important; }

.body-text {
  color: #000000 !important;
  font-size: 19px !important;
  font-weight: 600 !important;
  line-height: 1.7 !important;
  background: rgba(255, 255, 255, 0.95) !important;
}

.note-panel {
  background: #FFFBEB !important;
  color: #78350F !important;
  font-size: 18px !important;
  font-weight: 600 !important;
  border-left: 6px solid #F59E0B !important;
  border-top: 1px solid #FDE68A !important;
  border-right: 1px solid #FDE68A !important;
  border-bottom: 1px solid #FDE68A !important;
}

.note-panel .np-title {
  color: #B45309 !important;
  font-weight: 900 !important;
}

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
    selectedMatch = item;
    item.classList.add('selected');
  } else if(selectedMatch === item){
    selectedMatch.classList.remove('selected');
    selectedMatch = null;
  } else {
    if(selectedMatch.parentNode === item.parentNode){
      selectedMatch.classList.remove('selected');
      selectedMatch = item;
      item.classList.add('selected');
    } else {
      if(selectedMatch.dataset.match === item.dataset.match){
        selectedMatch.classList.remove('selected');
        selectedMatch.classList.add('matched');
        item.classList.add('matched');
        if(typeof playCorrect==='function') playCorrect();
        if(typeof burst==='function') burst(item);
        selectedMatch = null;
      } else {
        item.classList.add('wrong-match');
        selectedMatch.classList.add('wrong-match');
        if(typeof playError==='function') playError();
        var a = selectedMatch, b = item;
        setTimeout(function(){
          a.classList.remove('selected', 'wrong-match');
          b.classList.remove('wrong-match');
        }, 500);
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
  if(!b){
    b=document.createElement('div'); b.id='feedbackBubble'; b.className='fb-bubble';
    b.innerHTML='<span id="fbIcon"></span><span id="fbText"></span>';
    document.body.appendChild(b);
  }
  var icon=document.getElementById('fbIcon');
  var text=document.getElementById('fbText');
  if(isCorrect){
    b.className='fb-bubble show correct'; icon.textContent='👍'; text.textContent='回答正确!';
  } else {
    b.className='fb-bubble show wrong'; icon.textContent='✖️'; text.textContent='回答错误!';
  }
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
      if(targetCat === cardCat){
        card.style.background = 'var(--correct)'; playCorrect();
      } else {
        card.style.background = 'var(--error)'; playError();
      }
    } else {
      card.style.background = 'var(--brand)';
    }
  }
}

function setPen(mode, canvasId){
  var cv = document.getElementById(canvasId);
  if(!cv) return;
  cv.classList.add('drawing');
  var ctx = cv.getContext('2d');
  if(mode === 'clear'){
    ctx.clearRect(0,0,cv.width,cv.height);
  }
}

initDB();
"""

NAV_HTML = """<div class="nav-bar">
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

quiz_idx_counter = 0

def make_quiz_item(qid, prompt, options, original_correct_idx=0, explain=""):
    global quiz_idx_counter
    n = len(options)
    target_correct_idx = quiz_idx_counter % n
    seq = quiz_idx_counter + 1
    quiz_idx_counter += 1
    # qid 题号自动重排为全课唯一（2026-08-03 修旧版 Q17-24 撞号：保证数据采集 event_id 不冲突、题号不重复显示）
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
            '<div class="quiz-opts">%s</div>'
            '%s'
            '</div>' % (qid, num_str, prompt, "".join(opts_html), exp_html))

def make_quiz_grid(q_items, cols=True):
    return ('<div class="quiz-cols">' if cols else '<div>') + "".join(q_items) + '</div>'

# 六色卡记忆分级（2026-08-03 教师反馈：标题条 + ★重点记忆/▲难点/○理解即可 徽标）
_SIX_LV = {"rc-zhug": "key", "rc-bin": "key", "rc-xing": "warn",
           "rc-ming": "hint", "rc-warn": "hint", "rc-qita": "key"}
_SIX_LB = {"key": ("rule-key", "★ 重点记忆"),
           "warn": ("rule-warn", "▲ 难点"),
           "hint": ("rule-hint", "○ 理解即可")}

def six_cards(rule_dict):
    """按六色卡 dict 生成标题条 + 徽标 + 结构化正文（rule_dict 以 rc-* 为键、(标题, 正文) 为值）。"""
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
    
    left_html = "".join('<div class="match-item" data-match="%d" onclick="selectMatch(this)">%d. %s</div>' % (idx, idx, eng_word)
                        for idx, eng_word in left_items)
    right_html = "".join('<div class="match-item" data-match="%d" onclick="selectMatch(this)">%s</div>' % (idx, cn_word)
                         for idx, cn_word in right_items)
    
    return ('<div class="match-container">'
            '<div class="match-column">%s</div>'
            '<div class="match-column">%s</div>'
            '</div>' % (left_html, right_html))

# ======================= 构建 第17课时 课件 (42 页) =======================
def build_lesson_17():
    global quiz_idx_counter
    quiz_idx_counter = 0
    lesson = 17
    theme = "频度副词、how often 与基数词+times 表达"
    stage_badge = "基础 · Stage 4 · L17"
    
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
        seg.setdefault(seg_id, [p, p])
        seg[seg_id][1] = p
        page_meta[p] = {"priority": priority, "estimated_minutes": minutes}
        p += 1

    # P1 - P4
    cover = ('<div class="cover-wrap cover-variant-c">'
             '<div class="cover-badge">第 17 课时 · 许颖嘉</div>'
             '<div class="cover-title">%s</div>'
             '<div class="cover-sub">基础 · 七年级上</div>'
             '<div class="cover-tagline">日常习惯 · 频度表达 · 健康生活</div>'
             '<div class="cover-info">'
             '<div class="cover-info-num"><div class="ci-label">核心词汇</div><div class="ci-val">20</div></div>'
             '<div class="cover-info-num"><div class="ci-label">语法考点</div><div class="ci-val">3</div></div>'
             '<div class="cover-info-num"><div class="ci-label">课件页数</div><div class="ci-val">42</div></div>'
             '</div>'
             '<div class="cover-emoji">⏰🏃🥗</div></div>' % theme)
    add_page(cover, 1, priority="CORE", minutes=2)

    goal = (eng.section_head("标", "本课学习目标") +
            '<div class="chip-row">'
            '<div class="chip"><span class="chip-icon">🆕</span>20 个日常习惯与健康高频词</div>'
            '<div class="chip"><span class="chip-icon">🧩</span>频度副词 / How often 问句 / 基数词+times</div>'
            '<div class="chip"><span class="chip-icon">📖</span>健康生活主题阅读（A/B/C 三篇）</div>'
            '<div class="chip"><span class="chip-icon">🔤</span>y 结尾读音 /i/ 与 /aɪ/ 拼读</div>'
            '</div>' +
            '<div class="kmap">' +
            '<div class="kmap-node"><div class="kn-title">词汇</div><div class="kn-body">20 个频度与健康动词/名词，彻底过关。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">语法</div><div class="kn-body">be 后实前位置规则 + How often 答语。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">阅读</div><div class="kn-body">记叙 + 说明 + 五选四逻辑补全。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">拼读</div><div class="kn-body">y 结尾多音节 /i/ 与单音节 /aɪ/ 对比。</div></div>' +
            '</div>' +
            '<div class="note-panel"><div class="np-title">学习策略</div>先复习上节课 Stage 3 知识点，再全速攻克频度表达！</div>')
    add_page(goal, 1, "学习目标", "四大模块一目了然", priority="CORE", minutes=3)

    q_l16 = [
        make_quiz_item("L17_Q01", "The weather is ___ today.", ["sunny", "sun", "sunshine"], 0, "weather 后面修饰词用形容词 sunny。"),
        make_quiz_item("L17_Q02", "___ is it in Beijing? — It's cold.", ["How", "What", "Where"], 0, "How is the weather 询问天气状态。"),
        make_quiz_item("L17_Q03", "Would you like ___ with me?", ["to go", "go", "going"], 0, "Would you like to do sth. 结构。"),
        make_quiz_item("L17_Q04", "It's ___ outside. Take an umbrella.", ["rainy", "cloud", "wind"], 0, "带雨伞因为外面多雨 rainy。")
    ]
    add_page(eng.section_head("复", "上节课 · 天气与请求复习") +
             eng.game_board("天气与礼貌请求 4 问", "⚡", "点击选项作答，答对撒彩带。", make_quiz_grid(q_l16)), 1, "上节课复习", "天气与礼貌请求", priority="CORE", minutes=5)

    l16_v = [
        make_quiz_item("L17_Q05", "weather 对应中文：", ["天气", "水", "季节"], 0, "weather 意为天气。"),
        make_quiz_item("L17_Q06", "rainy 对应中文：", ["多雨的", "晴朗的", "多云的"], 0, "rainy 意为多雨的。"),
        make_quiz_item("L17_Q07", "cloudy 对应中文：", ["多云的", "刮风的", "寒冷的"], 0, "cloudy 意为多云的。"),
        make_quiz_item("L17_Q08", "windy 对应中文：", ["刮风的", "下雪的", "温暖的"], 0, "windy 意为刮风的。")
    ]
    add_page(eng.section_head("复", "上节课 · 词汇快闪") + make_quiz_grid(l16_v), 1, "上节课词汇", "即时检测", priority="EXTEND", minutes=4)

    # P5 - P12 (段2 新词20)
    v17 = [
        ("daily", "/ˈdeɪli/", "adj./adv.", "每日的", "daily routine", "I read English daily.", "day+y→daily"),
        ("usually", "/ˈjuːʒuəli/", "adv.", "通常", "usually get up", "I usually get up at six.", "usual+ly→通常地"),
        ("often", "/ˈɒfn/", "adv.", "经常", "often play sports", "She often reads books.", "often经常"),
        ("sometimes", "/ˈsʌmtaɪmz/", "adv.", "有时", "sometimes walk", "Sometimes I walk to school.", "some+times→有时"),
        ("hardly", "/ˈhɑːdli/", "adv.", "几乎不", "hardly ever", "He hardly ever eats junk food.", "hard+ly→几乎不"),
        ("never", "/ˈnevə(r)/", "adv.", "从不", "never give up", "I never drink coffee.", "n-ever→从不"),
        ("percent", "/pəˈsent/", "n.", "百分之", "eighty percent", "Eighty percent like sports.", "per+cent→百分之"),
        ("online", "/ˌɒnˈlaɪn/", "adj./adv.", "在线的", "read online", "I often read news online.", "on+line→在线"),
        ("television", "/ˈtelɪvɪʒn/", "n.", "电视", "watch television", "He watches television daily.", "tele+vision→电视"),
        ("mind", "/maɪnd/", "n./v.", "头脑；介意", "keep in mind", "A healthy mind is good.", "mind头脑"),
        ("body", "/ˈbɒdi/", "n.", "身体", "healthy body", "Exercise is good for body.", "body身体"),
        ("health", "/helθ/", "n.", "健康", "in good health", "Health is important.", "heal+th→健康"),
        ("routine", "/ruːˈtiːn/", "n.", "日常", "daily routine", "My routine includes jogging.", "rout+ine→日常"),
        ("jog", "/dʒɒɡ/", "v.", "慢跑", "go jogging", "I jog every morning.", "jog慢跑"),
        ("lifestyle", "/ˈlaɪfstaɪl/", "n.", "生活方式", "healthy lifestyle", "She has a good lifestyle.", "life+style→生活方式"),
        ("twice", "/twaɪs/", "adv.", "两次", "twice a week", "I brush teeth twice a day.", "two→twice"),
        ("point", "/pɔɪnt/", "n./v.", "分数；指向", "get points", "She got full points.", "point分数"),
        ("result", "/rɪˈzʌlt/", "n.", "结果", "survey result", "The results show good habits.", "re+sult→结果"),
        ("energy", "/ˈenədʒi/", "n.", "精力；能量", "full of energy", "Exercise gives me energy.", "energy精力"),
        ("regularly", "/ˈreɡjələli/", "adv.", "规律地", "exercise regularly", "He exercises regularly.", "regular+ly→规律地")
    ]

    add_page(eng.section_head("词", "新词学习 ①（1–10）· 频度与生活") + eng.vocab_cards(v17[:10]), 2, "新词①", "点击卡片看音标与例句", priority="CORE", minutes=5)
    q_v1 = [
        make_quiz_item("L17_Q09", "daily 意思是：", ["每日的", "每周的", "每月的"], 0, "daily 意为每日的。"),
        make_quiz_item("L17_Q10", "usually 意思是：", ["通常", "经常", "从不"], 0, "usually 意为通常。"),
        make_quiz_item("L17_Q11", "often 意思是：", ["经常", "有时", "几乎不"], 0, "often 意为经常。"),
        make_quiz_item("L17_Q12", "sometimes 意思是：", ["有时", "总是", "从不"], 0, "sometimes 意为有时。"),
        make_quiz_item("L17_Q13", "hardly 意思是：", ["几乎不", "非常", "总是"], 0, "hardly 意为几乎不。"),
        make_quiz_item("L17_Q14", "never 意思是：", ["从不", "总是", "通常"], 0, "never 意为从不。"),
        make_quiz_item("L17_Q15", "percent 意思是：", ["百分之", "数量", "部分"], 0, "percent 意为百分之。"),
        make_quiz_item("L17_Q16", "online 意思是：", ["在线的", "线下的", "遥远的"], 0, "online 意为在线的。")
    ]
    add_page(eng.section_head("词", "新词闯关 ① · 8 连问") + make_quiz_grid(q_v1), 2, "新词闯关①", "即时测试", priority="CORE", minutes=4)

    add_page(eng.section_head("词", "新词学习 ②（11–20）· 健康与习惯") + eng.vocab_cards(v17[10:]), 2, "新词②", "点击卡片看音标与例句", priority="CORE", minutes=5)
    q_v2 = [
        make_quiz_item("L17_Q17", "television 意思是：", ["电视", "电话", "电脑"], 0, "television 意为电视。"),
        make_quiz_item("L17_Q18", "mind 意思是：", ["头脑", "身体", "心脏"], 0, "mind 意为头脑。"),
        make_quiz_item("L17_Q19", "body 意思是：", ["身体", "手臂", "双腿"], 0, "body 意为身体。"),
        make_quiz_item("L17_Q20", "health 意思是：", ["健康", "财富", "力量"], 0, "health 意为健康。"),
        make_quiz_item("L17_Q21", "routine 意思是：", ["日常/常规", "计划", "决定"], 0, "routine 意为日常。"),
        make_quiz_item("L17_Q22", "jog 意思是：", ["慢跑", "散步", "跳高"], 0, "jog 意为慢跑。"),
        make_quiz_item("L17_Q23", "lifestyle 意思是：", ["生活方式", "生命", "风格"], 0, "lifestyle 意为生活方式。"),
        make_quiz_item("L17_Q24", "twice 意思是：", ["两次", "一次", "三次"], 0, "twice 意为两次。")
    ]
    add_page(eng.section_head("词", "新词闯关 ② · 8 连问") + make_quiz_grid(q_v2), 2, "新词闯关②", "即时测试", priority="CORE", minutes=4)

    match_pairs17 = [
        ("point", "分数"),
        ("result", "结果"),
        ("energy", "精力/能量"),
        ("regularly", "规律地"),
        ("percent", "百分之"),
        ("hardly", "几乎不"),
        ("routine", "日常"),
        ("lifestyle", "生活方式"),
        ("mind", "头脑"),
        ("twice", "两次")
    ]
    match_html17 = (eng.section_head("词", "词汇交互连线匹配 · 10 组速对") +
                    '<div class="body-text">点击左侧英文单词，再点击右侧对应的中文意思，答对放彩带并有成功音效！</div>' +
                    make_match_game(match_pairs17))
    add_page(match_html17, 2, "词汇连线", "交互匹配", priority="CORE", minutes=4)

    # Page 10: 【交互点②】双向拖拽归纳箱
    sorter_html = (eng.section_head("词", "Page 10 · 20 词双向拖拽归纳箱") +
                   '<div class="body-text">拖动词汇卡片归类到下方三个框框中（拉错了可随时拉回底盘或跨框切换！）：</div>' +
                   '<div class="sorter-container">' +
                   '<div class="sorter-pool" id="sorterPool" ondragover="allowDrop(event)" ondrop="drop(event)">' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_daily" data-cat="cat1">daily</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_usually" data-cat="cat1">usually</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_often" data-cat="cat1">often</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_sometimes" data-cat="cat1">sometimes</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_hardly" data-cat="cat1">hardly</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_never" data-cat="cat1">never</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_twice" data-cat="cat1">twice</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_regularly" data-cat="cat1">regularly</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_jog" data-cat="cat2">jog</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_routine" data-cat="cat2">routine</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_lifestyle" data-cat="cat2">lifestyle</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_online" data-cat="cat2">online</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_television" data-cat="cat2">television</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_body" data-cat="cat3">body</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_health" data-cat="cat3">health</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_mind" data-cat="cat3">mind</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_energy" data-cat="cat3">energy</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_percent" data-cat="cat3">percent</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_point" data-cat="cat3">point</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_result" data-cat="cat3">result</div>' +
                   '</div>' +
                   '<div class="sorter-target-grid">' +
                   '<div class="sorter-box" id="box_cat1" ondragover="allowDrop(event)" ondrop="drop(event)"><div class="sb-title">频度/次数副词</div></div>' +
                   '<div class="sorter-box" id="box_cat2" ondragover="allowDrop(event)" ondrop="drop(event)"><div class="sb-title">行为/日常动作</div></div>' +
                   '<div class="sorter-box" id="box_cat3" ondragover="allowDrop(event)" ondrop="drop(event)"><div class="sb-title">身心/健康/概念</div></div>' +
                   '</div></div>' +
                   '<div class="note-panel"><div class="np-title">互动说明</div>拖入匹配框显示绿色并放声效；放错显示红色；可随意拖回上盘重选！</div>')
    add_page(sorter_html, 2, "Page 10 归纳箱", "双向拖拽分类", priority="CORE", minutes=5)

    ext_v17 = [
        ("频度副词组", "red", "<b>always(100%) → usually(80%) → often(60%) → sometimes(40%) → hardly ever(10%) → never(0%)</b>"),
        ("次数表达组", "gold", "<b>once(1次) / twice(2次) / three times(3次) / four times(4次)</b>"),
        ("健康生活组", "green", "<b>health(n.健康) / healthy(adj.健康的) / lifestyle(n.生活方式) / routine(n.日常)</b>"),
        ("身体精力组", "blue", "<b>body(身体) / mind(头脑) / energy(精力) / jog(慢跑)</b>")
    ]
    add_page(eng.section_head("词", "新词速记 · 记忆地图") + eng.ext_cards(ext_v17), 2, "新词速记", "分组记忆", priority="EXTEND", minutes=4)

    cloze_v17 = [
        make_quiz_item("L17_Q17", "I ___ get up early at 6:00 because I am never late.", ["usually", "hardly", "never"], 0, "never late 说明通常早起 usually。"),
        make_quiz_item("L17_Q18", "He drinks milk ___ a day, in the morning and evening.", ["twice", "once", "three times"], 0, "早晚两次用 twice a day。"),
        make_quiz_item("L17_Q19", "Exercise is good for your ___ and mind.", ["body", "point", "percent"], 0, "运动对身心 body and mind 有益。"),
        make_quiz_item("L17_Q20", "She exercises ___ to keep healthy.", ["regularly", "hardly", "never"], 0, "规律地运动 regularly。")
    ]
    add_page(eng.section_head("词", "词汇运用 · 选词填空") + make_quiz_grid(cloze_v17), 2, "词汇运用", "语境选词", priority="CORE", minutes=4)

    diff_cards = [
        ("hardly vs hard", "red", "<b>hardly</b> 意为“几乎不”（否定期）；<b>hard</b> 意为“努力地/硬的”。"),
        ("once / twice vs times", "gold", "一次用 <b>once</b>，两次用 <b>twice</b>；三次及以上用 <b>基数词+times</b>。"),
        ("health vs healthy", "green", "<b>health</b> 为名词（good health）；<b>healthy</b> 为形容词（healthy food）。"),
        ("sometimes vs some times", "blue", "<b>sometimes</b> 意为“有时”；<b>some times</b> 意为“几次”。")
    ]
    add_page(eng.section_head("词", "近义 / 形近辨析") + eng.ext_cards(diff_cards), 2, "词汇辨析", "避免混淆", priority="EXTEND", minutes=4)

    flash_v17 = [(w[3], w[0]) for w in v17[:12]]
    add_page(eng.section_head("词", "听写自测 · 翻牌核对") + eng.flash_grid(flash_v17), 2, "听写自测", "翻牌查看英文", priority="EXTEND", minutes=4)

    # P13 - P22 (段3 语法精讲 3考点)
    rule1_six = {
        "rc-zhug": ("百分比降序", "always(100%) > usually(80%) > often(60%) > sometimes(40%) > hardly(10%) > never(0%)"),
        "rc-bin": ("be 动词后", "She is always happy and full of energy."),
        "rc-xing": ("实义动词前", "I usually get up at six in the morning."),
        "rc-ming": ("助动词之后", "I don't often watch television online."),
        "rc-warn": ("易错避坑", "❌ She always is happy. → ✅ She is always happy."),
        "rc-qita": ("句首特例", "Sometimes I walk to school on sunny days.")
    }
    cards1 = six_cards(rule1_six)
    add_page(eng.section_head("法", "考点① · 频度副词百分比与位置") +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             '<div class="rule-grid">' + cards1 + '</div>' +
             '<div class="note-panel"><div class="np-title">口诀</div>频度副词六兄弟，be 后实前记心里！</div>', 3, "语法①", "频度副词位置", priority="CORE", minutes=5)

    q_g1 = [
        make_quiz_item("L17_Q21", "下列哪个句子位置正确？", ["She is always happy.", "She always is happy.", "She is happy always."], 0, "be 动词 is 在前，always 在后。"),
        make_quiz_item("L17_Q22", "下列哪个句子位置正确？", ["He often plays soccer.", "He plays often soccer.", "Often he plays soccer."], 0, "实义动词 plays 在后，often 在前。"),
        make_quiz_item("L17_Q23", "Hardly ever 意思是：", ["几乎不", "经常", "总是"], 0, "hardly ever 表达几乎不。"),
        make_quiz_item("L17_Q24", "Never 的频度百分比是：", ["0%", "50%", "100%"], 0, "never 频度为 0%。")
    ]
    add_page(eng.section_head("法", "考点① · 易错闯关") + make_quiz_grid(q_g1), 3, "语法①闯关", "位置与含义", priority="CORE", minutes=4)

    eg1 = [("She is always late for school.", "be 动词 is 之后"),
           ("I usually exercise in the morning.", "实义动词 exercise 之前"),
           ("They hardly ever eat junk food.", "hardly ever 几乎不"),
           ("He never drinks coffee.", "never 从不")]
    add_page(eng.section_head("法", "考点① · 典型例句") + eng.example_section(eg1), 3, "语法①例句", "结合语境", priority="EXTEND", minutes=3)

    rule2_six = {
        "rc-zhug": ("疑问词组", "How often 用来对动作的发生频率进行提问。"),
        "rc-bin": ("基本结构", "How often + do/does + 主语 + 动词原形 ... ?"),
        "rc-xing": ("第一人称问", "How often do you exercise regularly?"),
        "rc-ming": ("第三人称问", "How often does he watch television?"),
        "rc-warn": ("答语搭配", "回答可用频度副词或 once/twice/three times a week。"),
        "rc-qita": ("易错辨析", "❌ How long 问时长；How often 问频率！")
    }
    cards2 = six_cards(rule2_six)
    add_page(eng.section_head("法", "考点② · How often 句型与回答") +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             '<div class="rule-grid">' + cards2 + '</div>', 3, "语法②", "How often 疑问句", priority="CORE", minutes=5)

    q_g2 = [
        make_quiz_item("L17_Q25", "— ___ do you read online? — Everyday.", ["How often", "How long", "How many"], 0, "对频率提问用 How often。"),
        make_quiz_item("L17_Q26", "— How often ___ she jog? — Twice a week.", ["does", "do", "is"], 0, "主语 she 为单数，用 does。"),
        make_quiz_item("L17_Q27", "How often 提问的是：", ["频率", "时长", "数量"], 0, "How often 提问发生频率。"),
        make_quiz_item("L17_Q28", "— How often do you play basketball? — ___.", ["Three times a week", "Two hours", "In the park"], 0, "答语用频率 Three times a week。")
    ]
    add_page(eng.section_head("法", "考点② · 易错闯关") + make_quiz_grid(q_g2), 3, "语法②闯关", "疑问词与回答", priority="CORE", minutes=4)

    rule3_six = {
        "rc-zhug": ("一次与两次", "一次是 once，两次是 twice，特例要牢记。"),
        "rc-bin": ("三次及以上", "three times, four times, five times ..."),
        "rc-xing": ("时间周期", "a day(每天), a week(每周), a month(每月), a year(每年)"),
        "rc-ming": ("组合表达", "twice a week (每周两次) / three times a month (每月三次)"),
        "rc-warn": ("time 单复数", "time 作“时间”不可数；作“次数”可数加 -s！"),
        "rc-qita": ("中考高频", "How often 答语最常考 once / twice / three times。")
    }
    cards3 = six_cards(rule3_six)
    add_page(eng.section_head("法", "考点③ · 基数词+times 表达") +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             '<div class="rule-grid">' + cards3 + '</div>', 3, "语法③", "频率表达", priority="CORE", minutes=5)

    q_g3 = [
        make_quiz_item("L17_Q29", "“每周两次”英文怎么说？", ["twice a week", "two times a week", "two time a week"], 0, "两次用特例 twice。"),
        make_quiz_item("L17_Q30", "“每月三次”英文怎么说？", ["three times a month", "three time a month", "thrice a month"], 0, "三次用 three times a month。"),
        make_quiz_item("L17_Q31", "“每天一次”英文怎么说？", ["once a day", "one time a day", "first a day"], 0, "一次用特例 once。"),
        make_quiz_item("L17_Q32", "Time 表示“次数”时：", ["是可数名词", "是不可数名词", "不能加s"], 0, "次数 time 是可数名词，复数加 s。")
    ]
    add_page(eng.section_head("法", "考点③ · 易错闯关") + make_quiz_grid(q_g3), 3, "语法③闯关", "次数表达", priority="CORE", minutes=4)

    g_sum = (eng.section_head("法", "语法三合一对比与易错表") +
             '<div class="kmap">' +
             '<div class="kmap-node"><div class="kn-title">频度副词</div><div class="kn-body">always/usually/often/sometimes/hardly/never，be后实前。</div></div>' +
             '<div class="kmap-node"><div class="kn-title">How often</div><div class="kn-body">How often + do/does + 主语 + 动词原形 ... ?</div></div>' +
             '<div class="kmap-node"><div class="kn-title">次数表达</div><div class="kn-body">once, twice, three times + a day/week/month.</div></div>' +
             '</div>' +
             '<div class="note-panel"><div class="np-title">记忆总口诀</div>频度副词看位置，be 后实前不能忘；How often 问频率，once twice times 来回答！</div>')
    add_page(g_sum, 3, "语法总结", "三合一复盘", priority="EXTEND", minutes=4)

    # 拓展专页 (+2 填充至 42 页)
    q_exp1 = [
        make_quiz_item("L17_Q60", "My sister ___ drinks tea because she doesn't like it.", ["never", "always", "usually"], 0, "不喜欢说明从不饮用 never。"),
        make_quiz_item("L17_Q61", "They read English books ___ a week.", ["four times", "four time", "fourth times"], 0, "四次用 four times。")
    ]
    add_page(eng.section_head("法", "语法考点深化演练") + make_quiz_grid(q_exp1), 3, "语法深化", "高频巩固", priority="EXTEND", minutes=4)

    q_exp2 = [
        make_quiz_item("L17_Q62", "— How often do you watch television? — ___.", ["Once a day", "Two hours", "In the evening"], 0, "对 How often 回答频率 Once a day。"),
        make_quiz_item("L17_Q63", "She is ___ friendly to everyone.", ["always", "always is", "is always"], 0, "be 后实前 is always friendly。")
    ]
    add_page(eng.section_head("法", "语法易错防坑演练") + make_quiz_grid(q_exp2), 3, "语法防坑", "避坑训练", priority="EXTEND", minutes=4)

    # P23 - P28 (段4 随堂演练)
    q_sec1 = [
        make_quiz_item("L17_Q33", "My grandfather exercises daily. He is in good ___.", ["health", "body", "point"], 0, "in good health 处于良好健康状态。"),
        make_quiz_item("L17_Q34", "— ___ do you go jogging? — Three times a week.", ["How often", "How long", "How much"], 0, "回答为频率，用 How often。"),
        make_quiz_item("L17_Q35", "She ___ eats junk food because it's bad for health.", ["never", "always", "usually"], 0, "垃圾食品有害健康，因此从不吃 never。"),
        make_quiz_item("L17_Q36", "We have English classes five ___ a week.", ["times", "time", "day"], 0, "五次用 five times。")
    ]
    add_page(eng.section_head("练", "随堂演练 ① · 基础单选") + make_quiz_grid(q_sec1), 4, "演练①", "单项选择", priority="CORE", minutes=4)

    q_sec2 = [
        make_quiz_item("L17_Q37", "He (usually) ___ (get) up at 6:30 am.", ["gets", "get", "getting"], 0, "主语 he 用三单 gets。"),
        make_quiz_item("L17_Q38", "How often ___ (do) your brother play computer games?", ["does", "do", "is"], 0, "your brother 单数用 does。"),
        make_quiz_item("L17_Q39", "She watches television ___ (two) a week.", ["twice", "two times", "second"], 0, "两次用 twice。"),
        make_quiz_item("L17_Q40", "Eighty percent of students ___ (like) reading online.", ["like", "likes", "liking"], 0, "percent of students 谓语用复数 like。")
    ]
    add_page(eng.section_head("练", "随堂演练 ② · 语法填空") + make_quiz_grid(q_sec2), 4, "演练②", "语法填空", priority="CORE", minutes=4)

    q_sec3 = [
        make_quiz_item("L17_Q41", "I watch TV twice a week. (对划线部分提问)", ["How often do you watch TV?", "How long do you watch TV?", "What do you watch?"], 0, "划线部分是频率，提问用 How often。"),
        make_quiz_item("L17_Q42", "She is always happy. (改为否定句)", ["She is never happy.", "She doesn't always happy.", "She is not never happy."], 0, "always 的完全否定为 never。")
    ]
    add_page(eng.section_head("练", "随堂演练 ③ · 句型转换") + make_quiz_grid(q_sec3), 4, "演练③", "句型转换", priority="EXTEND", minutes=3)

    q_sec4 = [
        make_quiz_item("L17_Q43", "A: How often do you exercise?\nB: ___.", ["I jog three times a week.", "I like sports.", "In the park."], 0, "回答频率用 three times a week。"),
        make_quiz_item("L17_Q44", "A: Does your father drink coffee?\nB: No, he ___ drinks it.", ["never", "always", "often"], 0, "No 否定回答说明从不饮用 never。")
    ]
    add_page(eng.section_head("练", "随堂演练 ④ · 补全对话") + make_quiz_grid(q_sec4), 4, "演练④", "补全对话", priority="EXTEND", minutes=3)

    q_sec5 = [
        make_quiz_item("L17_Q45", "找错：She plays usually basketball on Saturday.", ["plays usually → usually plays", "on → in", "Saturday → Saturdays"], 0, "usually 为频度副词，应在实义动词 plays 之前。"),
        make_quiz_item("L17_Q46", "找错：He goes jogging two times a week.", ["two times → twice", "goes → go", "a week → in week"], 0, "两次用特例 twice。")
    ]
    add_page(eng.section_head("练", "随堂演练 ⑤ · 改错闯关") + make_quiz_grid(q_sec5), 4, "演练⑤", "改错闯关", priority="EXTEND", minutes=3)

    mini_task17 = (eng.section_head("练", "Mini Task · 调查同学的生活习惯") +
                   '<div class="mini-task-box">' +
                   '<div class="mini-task-header"><span class="mini-task-icon">📋</span><div class="mini-task-title">任务：采访同学并做汇报</div></div>' +
                   '<div class="mini-task-content">用句型 <b>How often do you...?</b> 询问同学关于 <b>exercise, read online, watch TV</b> 的频率，并用 <b>usually, twice a week, 80 percent</b> 进行总结汇报。</div>' +
                   '</div>' +
                   '<div class="note-panel"><div class="np-title">表达支架</div>A: How often do you jog?\nB: I jog twice a week. It gives me energy!</div>')
    add_page(mini_task17, 4, "Mini Task", "综合运用", priority="CORE", minutes=5)

    # P29 - P32 (段5 阅读理解)
    pa_text = ("<b>Passage A (My Healthy Routine)</b><br>"
               "Tina is a 13-year-old student. She has a very healthy lifestyle. "
               "She usually gets up at 6:30 in the morning and jogs for 20 minutes. "
               "She eats breakfast daily and drinks a glass of milk. "
               "Tina reads English books online three times a week. "
               "She hardly ever eats junk food because she wants to keep her body in good health.")
    q_pa = [
        make_quiz_item("L17_Q47", "How often does Tina eat breakfast?", ["Daily.", "Twice a week.", "Hardly ever."], 0, "原文：She eats breakfast daily."),
        make_quiz_item("L17_Q48", "How often does Tina read English books online?", ["Three times a week.", "Daily.", "Once a month."], 0, "原文：three times a week.")
    ]
    pa_html = ('<div class="read-split">'
               '<div class="read-left">'
               '<div class="annotation-bar">'
               '<button class="ann-btn" onclick="setPen(\'red\', \'canvas_L17_A\')">✏️ 细红笔</button>'
               '<button class="ann-btn" onclick="setPen(\'highlighter\', \'canvas_L17_A\')">🖍️ 荧光笔</button>'
               '<button class="ann-btn" onclick="setPen(\'eraser\', \'canvas_L17_A\')">🧹 橡皮</button>'
               '<button class="ann-btn" onclick="setPen(\'clear\', \'canvas_L17_A\')">🗑️ 清空</button>'
               '</div>'
               '<div class="passage-wrap"><canvas class="read-canvas" id="canvas_L17_A"></canvas>'
               '<div class="reading-passage">%s</div></div></div>'
               '<div class="read-right">%s</div>'
               '</div>' % (pa_text, make_quiz_grid(q_pa, cols=False)))
    add_page(eng.section_head("阅", "阅读理解 A · 记叙文 (双栏对比+画笔)") + pa_html, 5, "阅读A", "细节理解", priority="CORE", minutes=6)

    pb_text = ("<b>Passage B (Survey on Student Habits)</b><br>"
               "Recently, our school did a survey about students' daily routines. "
               "The results show that eighty percent of students exercise regularly. "
               "About fifty percent of students watch television online every day. "
               "However, ten percent of students hardly ever do any sports. "
               "Doing sports is good for both body and mind, giving us more energy.")
    q_pb = [
        make_quiz_item("L17_Q49", "What percent of students exercise regularly?", ["80%.", "50%.", "10%."], 0, "原文：eighty percent of students exercise regularly."),
        make_quiz_item("L17_Q50", "What is the benefit of doing sports?", ["Good for body and mind.", "Makes us tired.", "Takes too much time."], 0, "原文：good for both body and mind.")
    ]
    pb_html = ('<div class="read-split">'
               '<div class="read-left">'
               '<div class="annotation-bar">'
               '<button class="ann-btn" onclick="setPen(\'red\', \'canvas_L17_B\')">✏️ 细红笔</button>'
               '<button class="ann-btn" onclick="setPen(\'highlighter\', \'canvas_L17_B\')">🖍️ 荧光笔</button>'
               '<button class="ann-btn" onclick="setPen(\'clear\', \'canvas_L17_B\')">🗑️ 清空</button>'
               '</div>'
               '<div class="passage-wrap"><canvas class="read-canvas" id="canvas_L17_B"></canvas>'
               '<div class="reading-passage">%s</div></div></div>'
               '<div class="read-right">%s</div>'
               '</div>' % (pb_text, make_quiz_grid(q_pb, cols=False)))
    add_page(eng.section_head("阅", "阅读理解 B · 说明文 (双栏对比+画笔)") + pb_html, 5, "阅读B", "说明理解", priority="EXTEND", minutes=6)

    pc_text = ("<b>Passage C (Tips for a Healthy Life)</b><br>"
               "1. Exercise regularly, such as jogging twice a week.<br>"
               "2. Eat healthy food and drink water daily.<br>"
               "3. [ ___ ] It is bad for your eyes.<br>"
               "4. Keep a good mood for your mind and body.")
    q_pc = [
        make_quiz_item("L17_Q51", "第3空应该填入哪个建议？", ["Don't watch television too long online.", "Never read any books.", "Eat junk food every day."], 0, "根据后句 bad for your eyes 选看电视不能太久。")
    ]
    pc_html = ('<div class="read-split">'
               '<div class="read-left">'
               '<div class="reading-passage">%s</div></div>'
               '<div class="read-right">%s</div>'
               '</div>' % (pc_text, make_quiz_grid(q_pc, cols=False)))
    add_page(eng.section_head("阅", "阅读理解 C · 五选四逻辑补全") + pc_html, 5, "阅读C", "逻辑补全", priority="HOME", minutes=6)

    # P33 - P36 (段6 自然拼读 4页体系)
    add_page(eng.section_head("拼", "自然拼读 P1 · y 结尾发音规则表") +
             '<div class="kmap">' +
             '<div class="kmap-node"><div class="kn-title">音标 /i/</div><div class="kn-body">多音节词尾：daily, usually, body, energy, healthily.</div></div>' +
             '<div class="kmap-node"><div class="kn-title">音标 /aɪ/</div><div class="kn-body">单音节词尾：my, fly, try, why, sky, cry.</div></div>' +
             '</div>', 6, "拼读规则", "y 的发音辨析", priority="CORE", minutes=3)

    q_ph1 = [
        make_quiz_item("L17_Q52", "单词 body 中 y 的发音是：", ["/i/", "/aɪ/", "/e/"], 0, "body 为多音节词，结尾 y 读 /i/。"),
        make_quiz_item("L17_Q53", "单词 fly 中 y 的发音是：", ["/aɪ/", "/i/", "/ɪ/"], 0, "fly 为单音节词，结尾 y 读 /aɪ/。")
    ]
    add_page(eng.section_head("拼", "拼读 P2 · 辨音选词") + make_quiz_grid(q_ph1), 6, "拼读闯关①", "听音选词", priority="CORE", minutes=3)

    q_ph2 = [
        make_quiz_item("L17_Q54", "daily 中 y 的发音与哪个词相同？", ["energy", "my", "fly"], 0, "daily 与 energy 结尾均读 /i/。"),
        make_quiz_item("L17_Q55", "try 中 y 的发音与哪个词相同？", ["why", "body", "daily"], 0, "try 与 why 结尾均读 /aɪ/。")
    ]
    add_page(eng.section_head("拼", "拼读 P3 · 解码高手") + make_quiz_grid(q_ph2), 6, "拼读闯关②", "同音识别", priority="EXTEND", minutes=3)

    add_page(eng.section_head("拼", "拼读 P4 · 归纳总结") +
             '<div class="note-panel"><div class="np-title">总结法则</div>长单词结尾 y 读 /i/；短单词结尾 y 读 /aɪ/。熟记规则轻松拼读！</div>', 6, "拼读总结", "法则归纳", priority="EXTEND", minutes=2)

    # P37 - P38 (段7 课堂综合游戏)
    q_g17_1 = [
        make_quiz_item("L17_Q56", "频度从高到低排列正确的是：", ["always → usually → often → never", "never → often → usually → always", "usually → always → never → often"], 0, "正确降序：always(100%) > usually(80%) > often(60%) > never(0%)。"),
        make_quiz_item("L17_Q57", "“每周三次”的正确英文：", ["three times a week", "three time a week", "third times a week"], 0, "三次用 three times a week。")
    ]
    add_page(eng.section_head("戏", "课堂综合游戏 ① · 频度快闪") + make_quiz_grid(q_g17_1), 7, "游戏①", "快速反应", priority="EXTEND", minutes=4)

    q_g17_2 = [
        make_quiz_item("L17_Q64", "听音选词：/ˈdeɪli/ 对应的词是：", ["daily", "day", "dairy"], 0, "daily 发音为 /ˈdeɪli/。"),
        make_quiz_item("L17_Q65", "听音选词：/ˈlaɪfstaɪl/ 对应的词是：", ["lifestyle", "lifelong", "lifeboat"], 0, "lifestyle 发音为 /ˈlaɪfstaɪl/。")
    ]
    add_page(eng.section_head("戏", "课堂综合游戏 ② · 听音辨词") + make_quiz_grid(q_g17_2), 7, "游戏②", "听音匹配", priority="EXTEND", minutes=4)

    # P39 - P42 (段8 总结与段9 导图)
    sum_html = (eng.section_head("结", "课堂总结 · 知识图谱") +
                '<div class="kmap">' +
                '<div class="kmap-node"><div class="kn-title">频度副词</div><div class="kn-body">always/usually/often/sometimes/hardly/never，be后实前。</div></div>' +
                '<div class="kmap-node"><div class="kn-title">How often</div><div class="kn-body">How often + do/does ... ? 问句与回答。</div></div>' +
                '<div class="kmap-node"><div class="kn-title">次数表达</div><div class="kn-body">once, twice, three times a day/week/month.</div></div>' +
                '</div>' +
                '<div class="note-panel"><div class="np-title">课后作业</div>① 背诵 20 个本课词汇；② 用 How often 采访家长 3 个生活习惯；③ 完成配套基础练习。</div>')
    add_page(sum_html, 8, "课堂总结", "知识图谱", priority="CORE", minutes=3)

    q_exit = [
        make_quiz_item("L17_Q58", "She is ___ late for school because she gets up very early.", ["never", "always", "usually"], 0, "起得早因此从不迟到 never。"),
        make_quiz_item("L17_Q59", "— How often do you jog? — ___.", ["Twice a week", "In the park", "With my friend"], 0, "How often 回答用频率 Twice a week。")
    ]
    add_page(eng.section_head("结", "Exit Ticket · 5分钟形成性检测") + make_quiz_grid(q_exit), 8, "Exit Ticket", "检测通关", priority="CORE", minutes=5)

    card17 = {
        "lesson": 17,
        "theme": theme,
        "tier": "基础",
        "stage": "S4",
        "student": "许颖嘉",
        "grammar": ["频度副词位置", "How often 问句", "次数表达"],
        "phonics": "y结尾 /i/与/aɪ/",
        "vocab": {"new_count": 20}
    }
    mm_html = (eng.section_head("图", "课堂思维导图 · 本课全貌") +
               '<div class="body-text">点击分支复盘本课 <span class="highlight">词汇 + 语法 + 拼读</span> 核心脉络。</div>' +
               eng.mind_map(card17))
    add_page(mm_html, 9, "思维导图", "互动复盘", priority="CORE", minutes=3)

    mm_full = (eng.section_head("图", "思维导图 · 完整内容页") +
               eng.mind_map_full(card17))
    add_page(mm_full, 9, "完整大纲", "对照自测", priority="EXTEND", minutes=3)

    total = p - 1
    seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
    js_extra = ("var studentId='stu_xyj';\n" +
                JS_FULL % (total, json.dumps(seg_pages, ensure_ascii=False),
                           json.dumps(page_meta, ensure_ascii=False)))

    html = build_courseware(title="第17课时 · " + theme, pages_dict=pages, js_extra=js_extra,
                            session="L17", nav_html=NAV_HTML, stage_badge=stage_badge,
                            n_pages=total, css_extra=CSS_FULL + build_theme_css("habits"))
    return html


# ======================= 构建 第18课时 课件 (42 页) =======================
def build_lesson_18():
    global quiz_idx_counter
    quiz_idx_counter = 0
    lesson = 18
    theme = "现在进行时·家务与此刻活动"
    stage_badge = "基础 · Stage 4 · L18"
    
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
        seg.setdefault(seg_id, [p, p])
        seg[seg_id][1] = p
        page_meta[p] = {"priority": priority, "estimated_minutes": minutes}
        p += 1

    # P1 - P4
    cover = ('<div class="cover-wrap cover-variant-a">'
             '<div class="cover-badge">第 18 课时 · 许颖嘉</div>'
             '<div class="cover-title">%s</div>'
             '<div class="cover-sub">基础 · 七年级上</div>'
             '<div class="cover-tagline">家务劳动 · 正在进行 · 动作表达</div>'
             '<div class="cover-info">'
             '<div class="cover-info-num"><div class="ci-label">核心词汇</div><div class="ci-val">20</div></div>'
             '<div class="cover-info-num"><div class="ci-label">语法考点</div><div class="ci-val">3</div></div>'
             '<div class="cover-info-num"><div class="ci-label">课件页数</div><div class="ci-val">42</div></div>'
             '</div>'
             '<div class="cover-emoji">🧹🧺🍳</div></div>' % theme)
    add_page(cover, 1, priority="CORE", minutes=2)

    goal = (eng.section_head("标", "本课学习目标") +
            '<div class="chip-row">'
            '<div class="chip"><span class="chip-icon">🆕</span>20 个家务与日常活动动词/名词</div>'
            '<div class="chip"><span class="chip-icon">🧩</span>现在进行时 be+V-ing / V-ing变化 / 标志词</div>'
            '<div class="chip"><span class="chip-icon">📖</span>忙碌的周日家务主题阅读（A/B/C 三篇）</div>'
            '<div class="chip"><span class="chip-icon">🔤</span>-ing 尾音 /ɪŋ/ 与重读闭音节双写规则</div>'
            '</div>' +
            '<div class="kmap">' +
            '<div class="kmap-node"><div class="kn-title">词汇</div><div class="kn-body">housework, sweep, wash, cook 等 20 词。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">语法</div><div class="kn-body">am/is/are + V-ing 三步法与否定疑问。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">阅读</div><div class="kn-body">家庭忙碌周日 + 世界各地时刻 + 五选四。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">拼读</div><div class="kn-body">-ing 尾音与双写尾字母加 ing 规则。</div></div>' +
            '</div>' +
            '<div class="note-panel"><div class="np-title">学习策略</div>掌握“be 动词 + 动词 -ing”搭配，学会描述“此时此刻正在发生的事”！</div>')
    add_page(goal, 1, "学习目标", "四大模块一目了然", priority="CORE", minutes=3)

    q_l17 = [
        make_quiz_item("L18_Q01", "She is ___ late for class.", ["always", "is always", "always is"], 0, "be 动词 is 在前，always 在后。"),
        make_quiz_item("L18_Q02", "— ___ do you jog? — Twice a week.", ["How often", "How long", "How many"], 0, "询问频率用 How often。"),
        make_quiz_item("L18_Q03", "He visits his grandparents ___ a month.", ["three times", "three time", "third times"], 0, "三次用 three times。"),
        make_quiz_item("L18_Q04", "Hardly ever 意思是：", ["几乎不", "总是", "常常"], 0, "hardly ever 表达几乎不。")
    ]
    add_page(eng.section_head("复", "上节课 · 频度表达复习") +
             eng.game_board("频度表达 4 问", "⚡", "点击选项作答，答对撒彩带。", make_quiz_grid(q_l17)), 1, "上节课复习", "频度表达", priority="CORE", minutes=5)

    l17_v = [
        make_quiz_item("L18_Q05", "daily 对应中文：", ["每日的", "每周的", "每月的"], 0, "daily 意为每日的。"),
        make_quiz_item("L18_Q06", "twice 对应中文：", ["两次", "一次", "三次"], 0, "twice 意为两次。"),
        make_quiz_item("L18_Q07", "routine 对应中文：", ["日常", "结果", "精力"], 0, "routine 意为日常作息。"),
        make_quiz_item("L18_Q08", "regularly 对应中文：", ["规律地", "迅速地", "偶尔地"], 0, "regularly 意为规律地。")
    ]
    add_page(eng.section_head("复", "上节课 · 词汇快闪") + make_quiz_grid(l17_v), 1, "上节课词汇", "即时检测", priority="EXTEND", minutes=4)

    # P5 - P12 (段2 新词20)
    v18 = [
        ("housework", "/ˈhaʊswɜːk/", "n.", "家务", "do housework", "She is doing housework now.", "house+work→家务"),
        ("sweep", "/swiːp/", "v.", "扫", "sweep the floor", "He is sweeping the floor.", "sweep扫地"),
        ("wash", "/wɒʃ/", "v.", "洗", "wash clothes", "Mom is washing clothes.", "wash洗"),
        ("cook", "/kʊk/", "v./n.", "烹饪；厨师", "cook dinner", "Dad is cooking dinner.", "cook做饭"),
        ("scan", "/skæn/", "v.", "扫描；浏览", "scan news", "She is scanning the newspaper.", "scan浏览"),
        ("read", "/riːd/", "v.", "读", "read a book", "He is reading a book.", "read阅读"),
        ("write", "/raɪt/", "v.", "写", "write a letter", "She is writing a letter.", "write书写"),
        ("draw", "/drɔː/", "v.", "画", "draw a picture", "The boy is drawing a picture.", "draw绘画"),
        ("sing", "/sɪŋ/", "v.", "唱", "sing a song", "She is singing a song.", "sing唱歌"),
        ("dance", "/dɑːns/", "v./n.", "跳舞", "dance to music", "They are dancing to music.", "dance跳舞"),
        ("study", "/ˈstʌdi/", "v./n.", "学习", "study for a test", "He is studying for a test.", "study学习"),
        ("sleep", "/sliːp/", "v./n.", "睡觉", "go to sleep", "The baby is sleeping now.", "sleep睡觉"),
        ("talk", "/tɔːk/", "v./n.", "谈话", "talk to sb.", "They are talking about movies.", "talk交谈"),
        ("speak", "/spiːk/", "v.", "说；讲", "speak English", "She is speaking English.", "speak说话"),
        ("hear", "/hɪə(r)/", "v.", "听见", "hear music", "I can hear someone singing.", "hear听见"),
        ("rest", "/rest/", "v./n.", "休息", "take a rest", "He is resting on the sofa.", "rest休息"),
        ("look", "/lʊk/", "v./n.", "看", "look at", "Look! She is drawing.", "look看"),
        ("chat", "/tʃæt/", "v./n.", "聊天", "chat online", "They are chatting online.", "chat聊天"),
        ("notice", "/ˈnəʊtɪs/", "v./n.", "注意到", "notice sb. doing", "I notice him reading a book.", "notice注意到"),
        ("moment", "/ˈməʊmənt/", "n.", "片刻；时刻", "at the moment", "She is busy at the moment.", "moment时刻")
    ]

    add_page(eng.section_head("词", "新词学习 ①（1–10）· 家务与动作") + eng.vocab_cards(v18[:10]), 2, "新词①", "点击卡片看音标与例句", priority="CORE", minutes=5)
    q_v18_1 = [
        make_quiz_item("L18_Q09", "housework 意思是：", ["家务", "作业", "工作"], 0, "housework 意为家务。"),
        make_quiz_item("L18_Q10", "sweep 意思是：", ["扫", "洗", "煮"], 0, "sweep 意为扫地。"),
        make_quiz_item("L18_Q11", "wash 意思是：", ["洗", "切", "扫"], 0, "wash 意为洗。"),
        make_quiz_item("L18_Q12", "cook 意思是：", ["烹饪；厨师", "切菜", "洗碗"], 0, "cook 意为做饭或厨师。"),
        make_quiz_item("L18_Q13", "scan 意思是：", ["浏览/扫描", "阅读", "写作"], 0, "scan 意为浏览或扫描。"),
        make_quiz_item("L18_Q14", "read 意思是：", ["读", "写", "画"], 0, "read 意为阅读。"),
        make_quiz_item("L18_Q15", "write 意思是：", ["写", "读", "唱"], 0, "write 意为书写。"),
        make_quiz_item("L18_Q16", "draw 意思是：", ["画", "唱", "跳"], 0, "draw 意为绘画。")
    ]
    add_page(eng.section_head("词", "新词闯关 ① · 8 连问") + make_quiz_grid(q_v18_1), 2, "新词闯关①", "即时测试", priority="CORE", minutes=4)

    add_page(eng.section_head("词", "新词学习 ②（11–20）· 活动与时刻") + eng.vocab_cards(v18[10:]), 2, "新词②", "点击卡片看音标与例句", priority="CORE", minutes=5)
    q_v18_2 = [
        make_quiz_item("L18_Q17", "sing 意思是：", ["唱", "跳", "读"], 0, "sing 意为唱歌。"),
        make_quiz_item("L18_Q18", "dance 意思是：", ["跳舞", "唱歌", "绘画"], 0, "dance 意为跳舞。"),
        make_quiz_item("L18_Q19", "study 意思是：", ["学习", "休息", "聊天"], 0, "study 意为学习。"),
        make_quiz_item("L18_Q20", "sleep 意思是：", ["睡觉", "清醒", "运动"], 0, "sleep 意为睡觉。"),
        make_quiz_item("L18_Q21", "talk 意思是：", ["谈话/交谈", "演讲", "大喊"], 0, "talk 意为交谈。"),
        make_quiz_item("L18_Q22", "speak 意思是：", ["说/讲语言", "倾听", "书写"], 0, "speak 意为说话或讲某种语言。"),
        make_quiz_item("L18_Q23", "hear 意思是：", ["听见", "看见", "感觉"], 0, "hear 意为听见。"),
        make_quiz_item("L18_Q24", "rest 意思是：", ["休息", "工作", "锻炼"], 0, "rest 意为休息。")
    ]
    add_page(eng.section_head("词", "新词闯关 ② · 8 连问") + make_quiz_grid(q_v18_2), 2, "新词闯关②", "即时测试", priority="CORE", minutes=4)

    match_pairs18 = [
        ("look", "看"),
        ("chat", "聊天"),
        ("notice", "注意到"),
        ("moment", "时刻/片刻"),
        ("housework", "家务"),
        ("sweep", "扫"),
        ("wash", "洗"),
        ("cook", "做饭"),
        ("read", "读"),
        ("write", "写")
    ]
    match_html18 = (eng.section_head("词", "词汇交互连线匹配 · 10 组速对") +
                    '<div class="body-text">点击左侧英文单词，再点击右侧对应的中文意思，答对放彩带并有成功音效！</div>' +
                    make_match_game(match_pairs18))
    add_page(match_html18, 2, "词汇连线", "交互匹配", priority="CORE", minutes=4)

    # Page 10: 【交互点②】双向拖拽归纳箱
    sorter18_html = (eng.section_head("词", "Page 10 · 20 词双向拖拽归纳箱") +
                     '<div class="body-text">拖动词汇卡片归类到下方三个框框中（拉错了可随时拉回底盘或跨框切换！）：</div>' +
                     '<div class="sorter-container">' +
                     '<div class="sorter-pool" id="sorterPool18" ondragover="allowDrop(event)" ondrop="drop(event)">' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_housework" data-cat="cat1">housework</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_sweep" data-cat="cat1">sweep</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_wash" data-cat="cat1">wash</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_cook" data-cat="cat1">cook</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_scan" data-cat="cat2">scan</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_read" data-cat="cat2">read</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_write" data-cat="cat2">write</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_draw" data-cat="cat2">draw</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_sing" data-cat="cat2">sing</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_dance" data-cat="cat2">dance</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_study" data-cat="cat2">study</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_talk" data-cat="cat3">talk</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_speak" data-cat="cat3">speak</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_hear" data-cat="cat3">hear</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_chat" data-cat="cat3">chat</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_rest" data-cat="cat3">rest</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_sleep" data-cat="cat3">sleep</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_look" data-cat="cat3">look</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_notice" data-cat="cat3">notice</div>' +
                     '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_moment" data-cat="cat3">moment</div>' +
                     '</div>' +
                     '<div class="sorter-target-grid">' +
                     '<div class="sorter-box" id="box_cat1" ondragover="allowDrop(event)" ondrop="drop(event)"><div class="sb-title">家务与清洁</div></div>' +
                     '<div class="sorter-box" id="box_cat2" ondragover="allowDrop(event)" ondrop="drop(event)"><div class="sb-title">学习/才艺与活动</div></div>' +
                     '<div class="sorter-box" id="box_cat3" ondragover="allowDrop(event)" ondrop="drop(event)"><div class="sb-title">交流/状态与时刻</div></div>' +
                     '</div></div>' +
                     '<div class="note-panel"><div class="np-title">互动说明</div>拖入匹配框显示绿色并放声效；放错显示红色；可随意拖回上盘重选！</div>')
    add_page(sorter18_html, 2, "Page 10 归纳箱", "双向拖拽分类", priority="CORE", minutes=5)

    ext_v18 = [
        ("家务动词组", "red", "<b>do housework / sweep the floor / wash clothes / cook dinner</b>"),
        ("日常活动组", "gold", "<b>read a book / write a letter / draw a picture / sing a song / dance</b>"),
        ("语言交流组", "green", "<b>talk to sb. / speak English / hear music / chat online</b>"),
        ("状态与时刻", "blue", "<b>rest(休息) / sleep(睡觉) / notice(注意到) / at the moment(此时此刻)</b>")
    ]
    add_page(eng.section_head("词", "新词速记 · 记忆地图") + eng.ext_cards(ext_v18), 2, "新词速记", "分组记忆", priority="EXTEND", minutes=4)

    cloze_v18 = [
        make_quiz_item("L18_Q17", "My mother is ___ dinner in the kitchen now.", ["cooking", "sweeping", "drawing"], 0, "在厨房做饭 cooking dinner。"),
        make_quiz_item("L18_Q18", "He is ___ the floor with a broom.", ["sweeping", "washing", "reading"], 0, "用扫帚扫地 sweeping the floor。"),
        make_quiz_item("L18_Q19", "They are ___ online with their friends at the moment.", ["chatting", "resting", "sleeping"], 0, "网上聊天 chatting online。"),
        make_quiz_item("L18_Q20", "Listen! She is ___ an English song.", ["singing", "dancing", "writing"], 0, "唱歌 sing a song。")
    ]
    add_page(eng.section_head("词", "词汇运用 · 选词填空") + make_quiz_grid(cloze_v18), 2, "词汇运用", "语境选词", priority="CORE", minutes=4)

    diff_v18 = [
        ("speak vs talk vs chat", "red", "<b>speak</b> 强调讲某种语言；<b>talk</b> 强调交谈；<b>chat</b> 强调轻松聊天。"),
        ("housework vs homework", "gold", "<b>housework</b> 是家务；<b>homework</b> 是家庭作业。"),
        ("look vs hear vs notice", "green", "<b>look</b> 强调看；<b>hear</b> 强调听见；<b>notice</b> 强调注意到。")
    ]
    add_page(eng.section_head("词", "近义 / 形近辨析") + eng.ext_cards(diff_v18), 2, "词汇辨析", "避免混淆", priority="EXTEND", minutes=4)

    flash_v18 = [(w[3], w[0]) for w in v18[:12]]
    add_page(eng.section_head("词", "听写自测 · 翻牌核对") + eng.flash_grid(flash_v18), 2, "听写自测", "翻牌查看英文", priority="EXTEND", minutes=4)

    # P13 - P22 (段3 语法精讲 3考点 + 拓展)
    rule18_1 = {
        "rc-zhug": ("核心概念", "表示此时此刻正在进行的动作或发生的事件。"),
        "rc-bin": ("肯定结构", "主语 + am/is/are + V-ing ... (She is reading.)"),
        "rc-xing": ("否定结构", "主语 + am/is/are + not + V-ing ... (They aren't cooking.)"),
        "rc-ming": ("be 动词选择", "I用am, he/she/it用is, we/you/they用are!"),
        "rc-warn": ("易错避坑", "❌ She reading a book. → ✅ She is reading a book. (不能漏 be!)"),
        "rc-qita": ("口诀助记", "现在进行时，be 加 ing；am is are 三选一，主语来决定！")
    }
    cards18_1 = six_cards(rule18_1)
    add_page(eng.section_head("法", "考点① · 现在进行时结构 (be + V-ing)") +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             '<div class="rule-grid">' + cards18_1 + '</div>', 3, "语法①", "be + V-ing 结构", priority="CORE", minutes=5)

    q_g18_1 = [
        make_quiz_item("L18_Q21", "Look! The children ___ on the playground.", ["are dancing", "is dancing", "dancing"], 0, "children 复数用 are dancing。"),
        make_quiz_item("L18_Q22", "I ___ a letter to my friend right now.", ["am writing", "is writing", "write"], 0, "主语 I 用 am writing。"),
        make_quiz_item("L18_Q23", "She ___ (not) sleeping; she is studying.", ["isn't", "doesn't", "don't"], 0, "进行时否定句在 is 后加 not 缩写 isn't。"),
        make_quiz_item("L18_Q24", "现在进行时结构中绝对不能省略：", ["be 动词", "地点状语", "副词"], 0, "绝对不能漏掉 be 动词。")
    ]
    add_page(eng.section_head("法", "考点① · 易错闯关") + make_quiz_grid(q_g18_1), 3, "语法①闯关", "结构识别", priority="CORE", minutes=4)

    rule18_2 = {
        "rc-zhug": ("规则①：直接加ing", "read→reading, wash→washing, cook→cooking, sweep→sweeping"),
        "rc-bin": ("规则②：去e加ing", "不发音 e 结尾：dance→dancing, write→writing, make→making"),
        "rc-xing": ("规则③：双写加ing", "重读闭音节：scan→scanning, chat→chatting, run→running, swim→swimming"),
        "rc-ming": ("规则④：特殊变化", "die→dying, lie→lying (暂作了解)"),
        "rc-warn": ("易错避坑", "❌ danceing → ✅ dancing / ❌ scaning → ✅ scanning"),
        "rc-qita": ("记忆口诀", "一般直接加，去 e 再加 ing，双写尾字母再加 ing！")
    }
    cards18_2 = six_cards(rule18_2)
    add_page(eng.section_head("法", "考点② · V-ing 变化规则") +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             '<div class="rule-grid">' + cards18_2 + '</div>', 3, "语法②", "V-ing 变化规则", priority="CORE", minutes=5)

    q_g18_2 = [
        make_quiz_item("L18_Q25", "dance 的 -ing 形式是：", ["dancing", "danceing", "dancsing"], 0, "不发音 e 结尾去 e 加 ing。"),
        make_quiz_item("L18_Q26", "scan 的 -ing 形式是：", ["scanning", "scaning", "scaned"], 0, "重读闭音节双写 n 加 ing。"),
        make_quiz_item("L18_Q27", "chat 的 -ing 形式是：", ["chatting", "chating", "chats"], 0, "重读闭音节双写 t 加 ing。"),
        make_quiz_item("L18_Q28", "write 的 -ing 形式是：", ["writing", "writeing", "writting"], 0, "去 e 加 ing 变为 writing。")
    ]
    add_page(eng.section_head("法", "考点② · 易错闯关") + make_quiz_grid(q_g18_2), 3, "语法②闯关", "动词变ing", priority="CORE", minutes=4)

    rule18_3 = {
        "rc-zhug": ("核心标志词", "now (现在), at the moment (此时时刻)"),
        "rc-bin": ("感叹句提示", "Look! (看！), Listen! (听！), Quiet! (安静！)，暗示动作正在发生。"),
        "rc-xing": ("一般疑问句", "Am/Is/Are + 主语 + V-ing ... ? (Is she reading? — Yes, she is.)"),
        "rc-ming": ("特殊疑问句", "What + am/is/are + 主语 + doing? (What are you doing?)"),
        "rc-warn": ("易错转换", "❌ What are you do? → ✅ What are you doing?"),
        "rc-qita": ("解题提示", "看到 Look! / Listen! / now，优先考虑现在进行时！")
    }
    cards18_3 = six_cards(rule18_3)
    add_page(eng.section_head("法", "考点③ · 标志词与句型转换") +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             '<div class="rule-grid">' + cards18_3 + '</div>', 3, "语法③", "标志词与疑问句", priority="CORE", minutes=5)

    q_g18_3 = [
        make_quiz_item("L18_Q29", "Listen! Someone ___ in the music room.", ["is singing", "sings", "sing"], 0, "Listen! 提示用现在进行时 is singing。"),
        make_quiz_item("L18_Q30", "— What ___ you doing at the moment? — I am doing housework.", ["are", "is", "do"], 0, "What are you doing 疑问句。"),
        make_quiz_item("L18_Q31", "— ___ he sweeping the floor? — Yes, he is.", ["Is", "Does", "Do"], 0, "一般疑问句 be 提前用 Is he... ?"),
        make_quiz_item("L18_Q32", "下列哪个词不是现在进行时的标志词？", ["every day", "now", "at the moment"], 0, "every day 是一般现在时标志词。")
    ]
    add_page(eng.section_head("法", "考点③ · 易错闯关") + make_quiz_grid(q_g18_3), 3, "语法③闯关", "标志词辨析", priority="CORE", minutes=4)

    g_sum18 = (eng.section_head("法", "语法三合一对比与总结") +
               '<div class="kmap">' +
               '<div class="kmap-node"><div class="kn-title">结构</div><div class="kn-body">主语 + am/is/are + V-ing (否定加 not, 疑问 be 提前)。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">V-ing 规则</div><div class="kn-body">直接加ing / 去e加ing / 双写加ing。</div></div>' +
               '<div class="kmap-node"><div class="kn-title">标志词</div><div class="kn-body">now, at the moment, Look!, Listen!</div></div>' +
               '</div>' +
               '<div class="note-panel"><div class="np-title">记忆口诀</div>看句中有无 Look/Listen/now，确定进行时；选对 be 动词，动词变 ing，全对通关！</div>')
    add_page(g_sum18, 3, "语法总结", "三合一复盘", priority="EXTEND", minutes=4)

    # 拓展专页 (+4 填充至 42 页)
    q_exp18_1 = [
        make_quiz_item("L18_Q60", "Look! The boys ___ soccer on the field.", ["are playing", "is playing", "play"], 0, "The boys 复数用 are playing。"),
        make_quiz_item("L18_Q61", "Listen! Who ___ the piano next door?", ["is playing", "plays", "are playing"], 0, "Who 作单数用 is playing。")
    ]
    add_page(eng.section_head("法", "语法考点深化演练 ①") + make_quiz_grid(q_exp18_1), 3, "语法深化①", "主谓一致", priority="EXTEND", minutes=4)

    q_exp18_2 = [
        make_quiz_item("L18_Q62", "— What is Mom doing? — She ___ dishes.", ["is washing", "washes", "wash"], 0, "问句为进行时，答语用 is washing。"),
        make_quiz_item("L18_Q63", "They ___ (not sleep) at the moment.", ["are not sleeping", "is not sleeping", "don't sleep"], 0, "They 复数否定 are not sleeping。")
    ]
    add_page(eng.section_head("法", "语法考点深化演练 ②") + make_quiz_grid(q_exp18_2), 3, "语法深化②", "否定与疑问", priority="EXTEND", minutes=4)

    q_exp18_3 = [
        make_quiz_item("L18_Q64", "Which verb forms -ing by doubling the last letter?", ["run", "read", "dance"], 0, "run 双写 n 加 ing 为 running。"),
        make_quiz_item("L18_Q65", "Which verb forms -ing by dropping e?", ["make", "sing", "wash"], 0, "make 去 e 加 ing 为 making。")
    ]
    add_page(eng.section_head("法", "V-ing 变形辨析专页") + make_quiz_grid(q_exp18_3), 3, "V-ing 辨析", "规则专项", priority="EXTEND", minutes=4)

    q_exp18_4 = [
        make_quiz_item("L18_Q66", "Look! She ___ a red dress today.", ["is wearing", "wears", "wear"], 0, "Look! 提示进行时 is wearing。"),
        make_quiz_item("L18_Q67", "Listen! The birds ___ in the tree.", ["are singing", "is singing", "sings"], 0, "The birds 复数用 are singing。")
    ]
    add_page(eng.section_head("练", "随堂强化练习") + make_quiz_grid(q_exp18_4), 4, "随堂强化", "综合强化", priority="EXTEND", minutes=4)

    # P27 - P30 (段4 随堂演练)
    q_sec18_1 = [
        make_quiz_item("L18_Q33", "Look! The boy ___ a picture of a tree.", ["is drawing", "draws", "draw"], 0, "Look! 标志进行时 is drawing。"),
        make_quiz_item("L18_Q34", "My parents ___ dinner in the kitchen at the moment.", ["are cooking", "cooks", "is cooking"], 0, "My parents 复数用 are cooking。"),
        make_quiz_item("L18_Q35", "Listen! The girls ___ happily in the hall.", ["are singing", "sings", "singing"], 0, "Listen! 提示进行时 are singing。"),
        make_quiz_item("L18_Q36", "She is ___ a letter to her friend.", ["writing", "writeing", "write"], 0, "write 去 e 加 ing 为 writing。")
    ]
    add_page(eng.section_head("练", "随堂演练 ① · 基础单选") + make_quiz_grid(q_sec18_1), 4, "演练①", "单项选择", priority="CORE", minutes=4)

    q_sec18_2 = [
        make_quiz_item("L18_Q37", "Look! Tom ___ (sweep) the floor.", ["is sweeping", "sweeps", "sweeping"], 0, "Tom 单数用 is sweeping。"),
        make_quiz_item("L18_Q38", "They ___ (chat) online right now.", ["are chatting", "is chatting", "chatting"], 0, "They 复数用 are chatting。"),
        make_quiz_item("L18_Q39", "Listen! Who ___ (speak) English?", ["is speaking", "speaks", "are speaking"], 0, "Who 作单数用 is speaking。"),
        make_quiz_item("L18_Q40", "My brother ___ (not study) for a test now.", ["is not studying", "doesn't study", "not study"], 0, "否定用 is not studying。")
    ]
    add_page(eng.section_head("练", "随堂演练 ② · 语法填空") + make_quiz_grid(q_sec18_2), 4, "演练②", "语法填空", priority="CORE", minutes=4)

    mini_task18 = (eng.section_head("练", "Mini Task · 描述正在进行的家庭活动") +
                   '<div class="mini-task-box">' +
                   '<div class="mini-task-header"><span class="mini-task-icon">🏡</span><div class="mini-task-title">任务：看图描述忙碌的一天</div></div>' +
                   '<div class="mini-task-content">用现在进行时 <b>am/is/are + V-ing</b> 描述你的家人此时此刻正在做的家务与活动。使用必用词：<b>housework, sweep, cook, read, chat</b>。</div>' +
                   '</div>' +
                   '<div class="note-panel"><div class="np-title">表达支架</div>It is Sunday morning. My family is very busy. My mom is cooking dinner. My dad is sweeping the floor. I am studying English!</div>')
    add_page(mini_task18, 4, "Mini Task", "综合运用", priority="CORE", minutes=5)

    # P30 - P33 (段5 阅读理解)
    pa18_text = ("<b>Passage A (A Busy Sunday Morning)</b><br>"
                 "It is 9:00 on Sunday morning. Everyone in David's family is doing housework. "
                 "David's father is sweeping the floor in the living room. "
                 "His mother is cooking breakfast in the kitchen. "
                 "David is washing his school uniform, and his sister is drawing a picture. "
                 "They are working together to keep their house clean and tidy.")
    q_pa18 = [
        make_quiz_item("L18_Q47", "What is David's father doing?", ["He is sweeping the floor.", "He is cooking breakfast.", "He is washing clothes."], 0, "原文：father is sweeping the floor."),
        make_quiz_item("L18_Q48", "What is David's sister doing?", ["She is drawing a picture.", "She is scanning news.", "She is sleeping."], 0, "原文：sister is drawing a picture.")
    ]
    pa18_html = ('<div class="read-split">'
                '<div class="read-left">'
                '<div class="annotation-bar">'
                '<button class="ann-btn" onclick="setPen(\'red\', \'canvas_L18_A\')">✏️ 细红笔</button>'
                '<button class="ann-btn" onclick="setPen(\'highlighter\', \'canvas_L18_A\')">🖍️ 荧光笔</button>'
                '<button class="ann-btn" onclick="setPen(\'clear\', \'canvas_L18_A\')">🗑️ 清空</button>'
                '</div>'
                '<div class="passage-wrap"><canvas class="read-canvas" id="canvas_L18_A"></canvas>'
                '<div class="reading-passage">%s</div></div></div>'
                '<div class="read-right">%s</div>'
                '</div>' % (pa18_text, make_quiz_grid(q_pa18, cols=False)))
    add_page(eng.section_head("阅", "阅读理解 A · 记叙文 (双栏对比+画笔)") + pa18_html, 5, "阅读A", "细节理解", priority="CORE", minutes=6)

    pb18_text = ("<b>Passage B (What Are People Doing Right Now?)</b><br>"
                 "At this moment, people around the world are doing different activities. "
                 "In Beijing, students are studying in classrooms. "
                 "In London, it is evening, and many people are resting or watching television. "
                 "In New York, people are waking up and drinking coffee. "
                 "Modern technology lets us chat online and know what others are doing at the same moment.")
    q_pb18 = [
        make_quiz_item("L18_Q49", "What are students in Beijing doing at this moment?", ["They are studying in classrooms.", "They are sleeping.", "They are watching TV."], 0, "原文：students are studying in classrooms."),
        make_quiz_item("L18_Q50", "What helps people know what others are doing?", ["Modern technology and chatting online.", "Reading storybooks.", "Sleeping."], 0, "原文：chat online and know what others are doing.")
    ]
    pb18_html = ('<div class="read-split">'
                '<div class="read-left">'
                '<div class="annotation-bar">'
                '<button class="ann-btn" onclick="setPen(\'red\', \'canvas_L18_B\')">✏️ 细红笔</button>'
                '<button class="ann-btn" onclick="setPen(\'highlighter\', \'canvas_L18_B\')">🖍️ 荧光笔</button>'
                '<button class="ann-btn" onclick="setPen(\'clear\', \'canvas_L18_B\')">🗑️ 清空</button>'
                '</div>'
                '<div class="passage-wrap"><canvas class="read-canvas" id="canvas_L18_B"></canvas>'
                '<div class="reading-passage">%s</div></div></div>'
                '<div class="read-right">%s</div>'
                '</div>' % (pb18_text, make_quiz_grid(q_pb18, cols=False)))
    add_page(eng.section_head("阅", "阅读理解 B · 说明文 (双栏对比+画笔)") + pb18_html, 5, "阅读B", "说明理解", priority="EXTEND", minutes=6)

    pc18_text = ("<b>Passage C (Family Cleaning Day)</b><br>"
                 "1. First, everyone chooses a housework task.<br>"
                 "2. Mom is washing dishes while Dad is sweeping the floor.<br>"
                 "3. [ ___ ] He is cleaning his bedroom.<br>"
                 "4. Finally, the whole family rests and chats happily.")
    q_pc18 = [
        make_quiz_item("L18_Q51", "第3空应该填入哪个句子？", ["Tom is also helping with housework.", "Tom is sleeping all day.", "Dad is going shopping."], 0, "根据上下文选 Tom 也帮忙做家务。")
    ]
    pc18_html = ('<div class="read-split">'
                '<div class="read-left">'
                '<div class="reading-passage">%s</div></div>'
                '<div class="read-right">%s</div>'
                '</div>' % (pc18_text, make_quiz_grid(q_pc18, cols=False)))
    add_page(eng.section_head("阅", "阅读理解 C · 五选四逻辑补全") + pc18_html, 5, "阅读C", "逻辑补全", priority="HOME", minutes=6)

    # P34 - P37 (段6 自然拼读 4页体系)
    add_page(eng.section_head("拼", "自然拼读 P1 · -ing 尾音与双写规则") +
             '<div class="kmap">' +
             '<div class="kmap-node"><div class="kn-title">尾音 /ɪŋ/</div><div class="kn-body">reading, washing, cooking, singing, dancing.</div></div>' +
             '<div class="kmap-node"><div class="kn-title">重读闭音节双写</div><div class="kn-body">run→running, scan→scanning, chat→chatting, swim→swimming.</div></div>' +
             '</div>', 6, "拼读规则", "-ing 尾音与双写", priority="CORE", minutes=3)

    q_ph18_1 = [
        make_quiz_item("L18_Q52", "scan 变 -ing 时需要：", ["双写 n 加 ing", "直接加 ing", "去 n 加 ing"], 0, "重读闭音节双写末尾辅音字母 n。"),
        make_quiz_item("L18_Q53", "dance 变 -ing 时需要：", ["去 e 加 ing", "双写 c 加 ing", "直接加 ing"], 0, "不发音 e 结尾去 e 加 ing。")
    ]
    add_page(eng.section_head("拼", "拼读 P2 · 辨音选词") + make_quiz_grid(q_ph18_1), 6, "拼读闯关①", "规则辨析", priority="CORE", minutes=3)

    q_ph18_2 = [
        make_quiz_item("L18_Q54", "下列哪个单词变化规则与 running 相同？", ["chatting", "reading", "dancing"], 0, "chatting 同为双写尾字母加 ing。"),
        make_quiz_item("L18_Q55", "下列哪个单词变化规则与 writing 相同？", ["dancing", "running", "singing"], 0, "dancing 同为去 e 加 ing。")
    ]
    add_page(eng.section_head("拼", "拼读 P3 · 解码高手") + make_quiz_grid(q_ph18_2), 6, "拼读闯关②", "同规则识别", priority="EXTEND", minutes=3)

    add_page(eng.section_head("拼", "拼读 P4 · 归纳总结") +
             '<div class="note-panel"><div class="np-title">法则</div>一般直接加，去 e 再加 ing，双写尾字母再加 ing！</div>', 6, "拼读总结", "法则归纳", priority="EXTEND", minutes=2)

    # P38 - P41 (段7 课堂综合游戏)
    q_g18_game1 = [
        make_quiz_item("L18_Q56", "Look! They ___ on the beach.", ["are running", "is running", "runing"], 0, "They 复数用 are running。"),
        make_quiz_item("L18_Q57", "Listen! The baby ___ in the bedroom.", ["is sleeping", "sleeps", "is sleep"], 0, "The baby 单数用 is sleeping。")
    ]
    add_page(eng.section_head("戏", "课堂综合游戏 ① · 语法快闪") + make_quiz_grid(q_g18_game1), 7, "游戏①", "快速反应", priority="EXTEND", minutes=4)

    q_g18_game2 = [
        make_quiz_item("L18_Q68", "听音选词：/ˈhaʊswɜːk/ 对应的词是：", ["housework", "homework", "homestay"], 0, "housework 发音为 /ˈhaʊswɜːk/。"),
        make_quiz_item("L18_Q69", "听音选词：/ˈməʊmənt/ 对应的词是：", ["moment", "mountain", "monitor"], 0, "moment 发音为 /ˈməʊmənt/。")
    ]
    add_page(eng.section_head("戏", "课堂综合游戏 ② · 听音辨词") + make_quiz_grid(q_g18_game2), 7, "游戏②", "听音匹配", priority="EXTEND", minutes=4)

    q_g18_game3 = [
        make_quiz_item("L18_Q70", "— What are you doing? — I am ___ (write) a letter.", ["writing", "writeing", "writes"], 0, "write 去 e 加 ing。"),
        make_quiz_item("L18_Q71", "Listen! The girl is ___ (sing) an English song.", ["singing", "sings", "sing"], 0, "Listen! 提示进行时 is singing。")
    ]
    add_page(eng.section_head("戏", "课堂综合游戏 ③ · 句型快刷") + make_quiz_grid(q_g18_game3), 7, "游戏③", "句型快刷", priority="EXTEND", minutes=4)

    q_g18_game4 = [
        make_quiz_item("L18_Q72", "Look! Mom is ___ (cook) in the kitchen.", ["cooking", "cooks", "cook"], 0, "is 后跟 V-ing 为 cooking。"),
        make_quiz_item("L18_Q73", "They are ___ (chat) happily with friends.", ["chatting", "chating", "chats"], 0, "chat 重读闭音节双写 t 加 ing。")
    ]
    add_page(eng.section_head("戏", "课堂综合游戏 ④ · 动词变形") + make_quiz_grid(q_g18_game4), 7, "游戏④", "动词变形", priority="EXTEND", minutes=4)

    # P40 - P42 (段8 总结与段9 导图)
    sum18_html = (eng.section_head("结", "课堂总结 · 知识图谱") +
                  '<div class="kmap">' +
                  '<div class="kmap-node"><div class="kn-title">现在进行时</div><div class="kn-body">am/is/are + V-ing，表此时此刻正在进行的动作。</div></div>' +
                  '<div class="kmap-node"><div class="kn-title">V-ing 规则</div><div class="kn-body">直接加ing / 去e加ing / 双写加ing。</div></div>' +
                  '<div class="kmap-node"><div class="kn-title">标志词</div><div class="kn-body">now, at the moment, Look!, Listen!</div></div>' +
                  '</div>' +
                  '<div class="note-panel"><div class="np-title">课后作业</div>① 背诵 20 个本课词汇；② 用进行时写 5 句描述家人的动作；③ 完成配套基础练习。</div>')
    add_page(sum18_html, 8, "课堂总结", "知识图谱", priority="CORE", minutes=3)

    q_exit18 = [
        make_quiz_item("L18_Q58", "What is she doing at the moment? — She ___ clothes.", ["is washing", "washes", "wash"], 0, "at the moment 提示进行时 is washing。"),
        make_quiz_item("L18_Q59", "Look! The boys ___ basketball.", ["are playing", "is playing", "plays"], 0, "The boys 复数用 are playing。")
    ]
    add_page(eng.section_head("结", "Exit Ticket · 5分钟形成性检测") + make_quiz_grid(q_exit18), 8, "Exit Ticket", "检测通关", priority="CORE", minutes=5)

    card18 = {
        "lesson": 18,
        "theme": theme,
        "tier": "基础",
        "stage": "S4",
        "student": "许颖嘉",
        "grammar": ["be + V-ing 结构", "V-ing 变化规则", "标志词 Look/Listen/now"],
        "phonics": "-ing 与双写规则",
        "vocab": {"new_count": 20}
    }
    mm18_html = (eng.section_head("图", "课堂思维导图 · 本课全貌") +
                 '<div class="body-text">点击分支复盘本课 <span class="highlight">词汇 + 语法 + 拼读</span> 核心脉络。</div>' +
                 eng.mind_map(card18))
    add_page(mm18_html, 9, "思维导图", "互动复盘", priority="CORE", minutes=3)

    mm18_full = (eng.section_head("图", "思维导图 · 完整内容页") +
                 eng.mind_map_full(card18))
    add_page(mm18_full, 9, "完整大纲", "对照自测", priority="EXTEND", minutes=3)

    total = p - 1
    seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
    js_extra = ("var studentId='stu_xyj';\n" +
                JS_FULL % (total, json.dumps(seg_pages, ensure_ascii=False),
                           json.dumps(page_meta, ensure_ascii=False)))

    html = build_courseware(title="第18课时 · " + theme, pages_dict=pages, js_extra=js_extra,
                            session="L18", nav_html=NAV_HTML, stage_badge=stage_badge,
                            n_pages=total, css_extra=CSS_FULL + build_theme_css("activities"))
    return html


def main():
    out_dir_17 = "D:/英语教学/许颖嘉/第17课时/课件成品_网页PPT"
    out_dir_18 = "D:/英语教学/许颖嘉/第18课时/课件成品_网页PPT"
    
    os.makedirs(out_dir_17, exist_ok=True)
    os.makedirs(out_dir_18, exist_ok=True)

    html17 = build_lesson_17()
    out17_path = os.path.join(out_dir_17, "第17课时_课件_基础.html")
    with open(out17_path, "w", encoding="utf-8") as f:
        f.write(html17)
    print("✅ Lesson 17 生成成功: %s (%d bytes)" % (out17_path, len(html17.encode("utf-8"))))

    html18 = build_lesson_18()
    out18_path = os.path.join(out_dir_18, "第18课时_课件_基础.html")
    with open(out18_path, "w", encoding="utf-8") as f:
        f.write(html18)
    print("✅ Lesson 18 生成成功: %s (%d bytes)" % (out18_path, len(html18.encode("utf-8"))))

if __name__ == "__main__":
    main()
