# -*- coding: utf-8 -*-
"""
许颖嘉 L26 重做 · 书面表达 SOP 专项冲刺 课件生成器（重做版）
依据：许颖嘉L26课时包_重做命令_20260804.md（与开工说明冲突处以重做命令为准）
重做要点：
  - 删除拼读页（bl/cl/fl 等），拼读槽位改填"SOP 方法与技巧"（审题检查清单/书面格式规范）
  - 强化真动笔：句子仿写/段落扩写/脚手架全文填空 ≥2 篇/命题写作 ≥3 道，演练动笔 ≥14 页
  - 范文 ×1 书信 + 1 同体裁变式题，quiz 考"为什么/应用"，不考"时态/标题"常识
  - CSS 去重：.rule-card 只定义一次（主题层），无 !important 冲突
  - 总页数 42 页（不压 40 下限），无凑数页
  - 零新词（S5 冲刺专项），防越级 ≤八上 U2
  - 不产契约目录
"""
import os, sys, json, re, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from courseware_core import build_courseware, page, vocab_cards, CORE_CSS, CORE_JS
import courseware_engine as eng

# ======================= L26 独立主题（紫色·写作） =======================
def get_theme_css_l26():
    return r"""
/* THEME:writing_sop_redo */
:root {
  --brand: #8B5CF6;
  --brand-light: #A78BFA;
  --accent: #F59E0B;
  --bg-start: #F5F3FF;
  --bg-end: #EDE9FE;
  --card-shadow: 0 14px 40px rgba(139,92,246,0.12);
}
/* 主题覆盖基色（仅定义一次，不重复 .rule-card 定义） */
.vocab-card, .mini-task-box, .cover-wrap, .kmap-node {
  background: #FFFFFF;
  border: 2px solid rgba(139,92,246,0.25);
  border-radius: 18px;
  box-shadow: 0 8px 24px rgba(139,92,246,0.10);
}
.rule-card {
  position: relative;
  overflow: hidden;
  padding: 14px 18px;
  border-radius: 16px;
  box-shadow: 0 6px 18px rgba(139,92,246,0.10);
  margin: 8px 0;
}
.rule-card::before {
  content: '';
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 6px;
  background: rgba(255,255,255,0.32);
}
.rc-cat { font-size: 19px; font-weight: 900; margin-bottom: 6px; }
.rc-text { font-size: 18px; font-weight: 700; color: #1A1A2E; line-height: 1.6; }
.rc-zhug { background:#EFF6FF; border-left:6px solid #2563EB; border-top:1px solid #BFDBFE; border-right:1px solid #BFDBFE; border-bottom:1px solid #BFDBFE; }
.rc-zhug .rc-cat { color:#1D4ED8; }
.rc-bin { background:#F0FDF4; border-left:6px solid #16A34A; border-top:1px solid #BBF7D0; border-right:1px solid #BBF7D0; border-bottom:1px solid #BBF7D0; }
.rc-bin .rc-cat { color:#15803D; }
.rc-xing { background:#FEF3C7; border-left:6px solid #D97706; border-top:1px solid #FDE68A; border-right:1px solid #FDE68A; border-bottom:1px solid #FDE68A; }
.rc-xing .rc-cat { color:#B45309; }
.rc-ming { background:#FAF5FF; border-left:6px solid #9333EA; border-top:1px solid #E9D5FF; border-right:1px solid #E9D5FF; border-bottom:1px solid #E9D5FF; }
.rc-ming .rc-cat { color:#7E22CE; }
.rc-warn { background:#FEF2F2; border-left:6px solid #DC2626; border-top:1px solid #FECACA; border-right:1px solid #FECACA; border-bottom:1px solid #FECACA; }
.rc-warn .rc-cat { color:#B91C1C; }
.rc-qita { background:#F0FDFA; border-left:6px solid #0D9488; border-top:1px solid #99F6E4; border-right:1px solid #99F6E4; border-bottom:1px solid #99F6E4; }
.rc-qita .rc-cat { color:#0F766E; }
.body-text { color:#1A1A2E; font-size:19px; font-weight:600; line-height:1.7; background:rgba(255,255,255,0.96); }
.note-panel { background:#FFFBEB; color:#78350F; font-size:18px; font-weight:600; border-left:6px solid #F59E0B; border-top:1px solid #FDE68A; border-right:1px solid #FDE68A; border-bottom:1px solid #FDE68A; }
.note-panel .np-title { color:#B45309; font-weight:900; }
.quiz-q { background:#FFFFFF; border:2px solid rgba(139,92,246,0.25); border-radius:18px; box-shadow:0 8px 24px rgba(139,92,246,0.10); }
.qq-text { color:#1A1A2E; font-size:19px; font-weight:700; }
.quiz-opt { font-size:19px; padding:9px 13px; border-radius:12px; margin:6px 0; border:2px solid rgba(139,92,246,0.30); box-shadow:0 3px 8px rgba(0,0,0,0.05); }
.prio-badge, .cover-badge { border-radius:10px; }
.fb-bubble { position:fixed; top:40%; left:50%; transform:translate(-50%,-50%) scale(0); background:#fff; border-radius:18px; padding:22px 40px; box-shadow:0 14px 40px rgba(139,92,246,0.25); z-index:9999; pointer-events:none; transition:transform 0.3s cubic-bezier(0.175,0.885,0.32,1.27); display:flex; align-items:center; gap:16px; font-size:32px; font-weight:900; }
.fb-bubble.show { transform:translate(-50%,-50%) scale(1); }
.fb-bubble.correct { border:4px solid var(--correct); color:var(--correct); background:#f0fff4; }
.fb-bubble.wrong { border:4px solid var(--error); color:var(--error); background:#fff0f0; }
.prio-badge { position:absolute; top:18px; right:24px; padding:5px 16px; border-radius:10px; font-size:14px; font-weight:700; color:#fff; box-shadow:0 2px 8px rgba(0,0,0,0.15); letter-spacing:0.5px; }
.prio-core { background:linear-gradient(135deg,#8B5CF6,#A78BFA); }
.prio-extend { background:linear-gradient(135deg,#3B82F6,#60A5FA); }
.prio-home { background:linear-gradient(135deg,#10B981,#34D399); }
.quiz-explain { display:none; margin-top:10px; padding:10px 16px; background:rgba(245,243,255,0.9); border-left:5px solid #F59E0B; border-radius:12px; font-size:16px; color:#3b2f1a; line-height:1.6; }
.quiz-explain.show { display:block; animation:fadeIn 0.3s ease-out; }

/* 深色游戏面板内题干容器恢复白底（覆盖 eng.CSS_EXTRA .game-board .quiz-q 的透明背景，避免黑字压深紫底） */
.game-board .quiz-q { background:#FFFFFF; border:2px solid rgba(139,92,246,0.25); border-radius:18px; box-shadow:0 8px 24px rgba(139,92,246,0.10); padding:14px 16px; margin:10px 0; }
.game-board .qq-text { color:#1A1A2E; }
.game-board .quiz-explain { background:#F5F3FF; color:#3b2f1a; }

/* 写作练习专用样式 */
.mm-grid { display:flex; flex-wrap:wrap; gap:12px; justify-content:center; margin:12px 0; }
.mm-branch { flex:1 1 45%; min-width:200px; cursor:pointer; }
.writing-prompt { background:#FEF3C7; border:2px solid #F59E0B; border-radius:16px; padding:16px 20px; margin:10px 0; }
.wp-title { font-size:18px; font-weight:800; color:#92400E; margin-bottom:6px; }
.wp-body { font-size:17px; line-height:1.7; color:#78350F; }
.wp-hint { font-size:16px; color:#92400E; background:#FFFBEB; border-radius:10px; padding:10px 14px; margin:8px 0; border-left:4px solid #F59E0B; }
.wp-checklist { font-size:15px; line-height:1.6; color:#78350F; background:#FFF; border:1px solid #FDE68A; border-radius:10px; padding:10px 14px; margin:8px 0; }
.wp-checklist b { color:#DC2626; }
.scaffold-fill { background:#F5F3FF; border:2px dashed #8B5CF6; border-radius:14px; padding:14px 18px; font-size:18px; line-height:2.0; margin:10px 0; }
.scaffold-fill .blank { display:inline-block; min-width:80px; border-bottom:2px solid #8B5CF6; color:#7E22CE; font-weight:700; text-align:center; padding:0 4px; }
.sentence-tile { background:#FAF5FF; border:1px solid #E9D5FF; border-radius:12px; padding:12px 16px; margin:8px 0; font-size:18px; line-height:1.6; }
.sentence-tile .cn { color:#92400E; font-weight:600; }
.sentence-tile .en { color:#1D4ED8; font-weight:700; }
.to-cn { display:inline-block; background:#FEF3C7; padding:2px 10px; border-radius:6px; font-style:italic; color:#92400E; }
.fix-badge { display:inline-block; background:#FEF2F2; color:#B91C1C; border-radius:6px; padding:2px 8px; font-size:14px; margin-left:6px; cursor:pointer; transition:all 0.2s; }
.fix-badge:hover { background:#FEE2E2; }
.fix-badge.revealed { background:#DCFCE7; color:#15803D; }

/* 命题写作构思框架（三部分，绿色面板） */
.writing-structure { background:#F0FDF4; border:2px solid #22C55E; border-radius:16px; padding:14px 18px; margin:10px 0; }
.ws-title { font-size:18px; font-weight:800; color:#166534; margin-bottom:8px; display:flex; align-items:center; gap:8px; }
.ws-part { background:#FFF; border:1px solid #BBF7D0; border-radius:10px; padding:10px 14px; margin:6px 0; }
.ws-part .ws-pnum { font-weight:800; color:#15803D; font-size:16px; }
.ws-part .ws-pbody { margin-top:4px; font-size:16px; line-height:1.5; color:#374151; }
"""

JS_FULL = r"""
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
    p.style.background=(Math.random()<0.5?'#F59E0B':'#8B5CF6');
    document.body.appendChild(p);
    (function(x){ setTimeout(function(){ x.remove(); },700); })(p);
  }
}
function shake(el){ el.style.animation='none'; void el.offsetWidth; el.style.animation='shake .4s'; }

function showBubble(isCorrect){
  var b=document.getElementById('feedbackBubble');
  if(!b){ b=document.createElement('div'); b.id='feedbackBubble'; b.className='fb-bubble';
    b.innerHTML='<span id="fbIcon"></span><span id="fbText"></span>'; document.body.appendChild(b); }
  var icon=document.getElementById('fbIcon'); var text=document.getElementById('fbText');
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
  var exp=q.querySelector('.quiz-explain'); if(exp){ exp.classList.add('show'); }
}

function undoQuiz(q){
  var opts=q.querySelectorAll('.quiz-opt');
  for(var i=0;i<opts.length;i++){ opts[i].classList.remove('opt-correct','opt-wrong','locked'); }
  delete q.dataset.done; delete q.dataset.wrong;
  q.dataset.attempt=String(parseInt(q.dataset.attempt||'1',10)+1);
  var h=q.querySelector('.et-undo-hint');
  if(h){ h.textContent='已撤销，请重答'; setTimeout(function(){ if(h.parentNode) h.parentNode.removeChild(h); }, 3000); }
  var exp=q.querySelector('.quiz-explain'); if(exp){ exp.classList.remove('show'); }
}
document.addEventListener('dblclick', function(e){
  var q=e.target.closest('.quiz-q');
  if(q && q.dataset.done==='1' && q.dataset.wrong==='1') undoQuiz(q);
});

function allowDrop(ev){ ev.preventDefault(); }
function drag(ev){ ev.dataTransfer.setData("text", ev.target.id); }
function drop(ev){
  ev.preventDefault();
  var data=ev.dataTransfer.getData("text");
  var card=document.getElementById(data);
  var targetBox=ev.target.closest('.sorter-box') || ev.target.closest('.sorter-pool');
  if(targetBox && card){
    targetBox.appendChild(card);
    if(targetBox.classList.contains('sorter-box')){
      var targetCat=targetBox.id.replace('box_',''); var cardCat=card.dataset.cat;
      if(targetCat===cardCat){ card.style.background='var(--correct)'; playCorrect(); }
      else { card.style.background='var(--error)'; playError(); }
    } else { card.style.background='var(--brand)'; }
  }
}
function setPen(mode, canvasId){
  var cv=document.getElementById(canvasId); if(!cv) return;
  cv.classList.add('drawing'); var ctx=cv.getContext('2d');
  if(mode==='clear'){ ctx.clearRect(0,0,cv.width,cv.height); }
}
function mmToggle(el){
  var panel=document.getElementById('mmPanel'); if(!panel) return;
  var title=el.querySelector('.mm-label').textContent;
  var chips=el.querySelector('.mm-chips').innerHTML;
  document.getElementById('mmPanelTitle').textContent=el.querySelector('.mm-icon').textContent+' '+title;
  document.getElementById('mmPanelChips').innerHTML=chips;
  var branches=document.querySelectorAll('.mm-branch');
  branches.forEach(function(b){ b.classList.remove('active'); });
  el.classList.add('active');
}
function toggleFixBadge(el){
  var ans=el.getAttribute('data-answer');
  if(!el.classList.contains('revealed')){
    el.textContent=ans; el.classList.add('revealed');
  } else {
    el.textContent='点击查看答案'; el.classList.remove('revealed');
  }
}
initDB();
"""

NAV_HTML = """<div class="nav-bar">
  <div class="nav-item" data-segment="1" onclick="jumpToSegment(1)"><span class="nav-num">①</span>复习导入</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="2" onclick="jumpToSegment(2)"><span class="nav-num">②</span>写作语料</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="3" onclick="jumpToSegment(3)"><span class="nav-num">③</span>SOP五步</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="4" onclick="jumpToSegment(4)"><span class="nav-num">④</span>范文拆解</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="5" onclick="jumpToSegment(5)"><span class="nav-num">⑤</span>SOP方法</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="6" onclick="jumpToSegment(6)"><span class="nav-num">⑥</span>演练动笔</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="7" onclick="jumpToSegment(7)"><span class="nav-num">⑦</span>评分改错</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="8" onclick="jumpToSegment(8)"><span class="nav-num">⑧</span>课堂总结</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="9" onclick="jumpToSegment(9)"><span class="nav-num">⑨</span>思维导图</div>
</div>"""

_qc = [0]
def q(stem, opts, cor, explain=""):
    _qc[0] += 1
    n = len(opts)
    tgt = (_qc[0] - 1) % n
    o = list(opts)
    if cor != tgt:
        o[cor], o[tgt] = o[tgt], o[cor]
    letters = "ABC"
    html_opts = []
    for i, opt in enumerate(o):
        c = "1" if i == tgt else "0"
        html_opts.append('<button class="quiz-opt" data-correct="%s" onclick="checkOpt(this)">%s. %s</button>' % (c, letters[i], opt))
    exp = ('<div class="quiz-explain"><b>解析：</b>%s</div>' % explain) if explain else \
          ('<div class="quiz-explain"><b>解析：</b>正确答案为：%s。请牢记写作SOP要点。</div>' % o[tgt])
    return ('<div class="quiz-q" data-qid="L26_Q%03d"><div class="qq-text"><span class="q-num">%d</span>、 %s</div>'
            '<div class="quiz-opts">%s</div>%s</div>' % (_qc[0], _qc[0], stem, "".join(html_opts), exp))

def quiz_grid(items, cols=True):
    return ('<div class="quiz-cols">' if cols else '<div>') + "".join(items) + '</div>'

def six_cards(pairs):
    return '<div class="rule-grid">' + "".join(
        '<div class="rule-card %s"><div class="rc-cat">%s</div><div class="rc-text">%s</div></div>' % (c, cat, txt)
        for c, cat, txt in pairs) + '</div>'

def generate_lesson_26():
    n = 26
    stage_badge = "基础 · S5 · L26"
    pages = {}
    seg = {}
    page_meta = {}
    p = [1]
    def add_page(inner, seg_id, title="", subtitle="", priority="CORE", minutes=5):
        prio_label = "CORE · 课堂必做" if priority=="CORE" else ("EXTEND · 时间充足做" if priority=="EXTEND" else "HOME · 课后完成")
        prio_cls = "prio-core" if priority=="CORE" else ("prio-extend" if priority=="EXTEND" else "prio-home")
        prio_badge = '<div class="prio-badge %s">%s (%d min)</div>' % (prio_cls, prio_label, minutes)
        full_inner = prio_badge + inner
        pages[p[0]] = page(p[0], title, subtitle, full_inner, active=(p[0]==1))
        seg.setdefault(seg_id, [p[0], p[0]])
        seg[seg_id][1] = p[0]
        page_meta[p[0]] = {"priority": priority, "estimated_minutes": minutes}
        p[0] += 1

    # =============================================================
    # SEGMENT 1: 复习导入 (P1-P4, 4 pages)
    # =============================================================
    # ---- P1 封面 ----
    cover = ('<div class="cover-wrap">'
             '<div class="cover-badge">第 26 课时 · 许颖嘉</div>'
             '<div class="cover-title">书面表达 SOP 专项冲刺</div>'
             '<div class="cover-sub">基础 · 七年级 · S5 冲刺段（重做版 · 强化动笔）</div>'
             '<div class="cover-tagline">审题 → 列点 → 成句 → 连段 → 检查</div>'
             '<div class="cover-info">'
             '<div class="cover-info-num"><div class="ci-label">SOP 五步</div><div class="ci-val">5</div></div>'
             '<div class="cover-info-num"><div class="ci-label">范文共</div><div class="ci-val">2</div></div>'
             '<div class="cover-info-num"><div class="ci-label">动笔页</div><div class="ci-val">14</div></div>'
             '</div>'
             '<div class="cover-emoji">✍️📝🌟</div></div>')
    add_page(cover, 1, priority="CORE", minutes=2)

    # ---- P2 目标 ----
    goal = (eng.section_head("标", "本课学习目标") +
            '<div class="chip-row">'
            '<div class="chip"><span class="chip-icon">🧭</span>书面表达 SOP 五步法</div>'
            '<div class="chip"><span class="chip-icon">📑</span>范文拆解 + 变式题（书信）</div>'
            '<div class="chip"><span class="chip-icon">✍️</span>句子仿写 → 段落扩写 → 全文写作</div>'
            '<div class="chip"><span class="chip-icon">⭐</span>三维评分与自检</div>'
            '</div>'
            '<div class="kmap">'
            '<div class="kmap-node"><div class="kn-title">方法</div><div class="kn-body">SOP 五步法 + 审题检查清单</div></div>'
            '<div class="kmap-node"><div class="kn-title">范文</div><div class="kn-body">书信范文（含 SOP 落点标注）+ 同体裁变式题</div></div>'
            '<div class="kmap-node"><div class="kn-title">演练</div><div class="kn-body">句子→段落→全文→命题，层层练</div></div>'
            '<div class="kmap-node"><div class="kn-title">评分</div><div class="kn-body">内容完整/语言准确/结构连贯</div></div>'
            '</div>'
            '<div class="note-panel"><div class="np-title">学习策略</div>先学方法，再拆范文，从句子练到全文，最后按三维自评。</div>')
    add_page(goal, 1, "学习目标", "四个模块", priority="CORE", minutes=3)

    # ---- P3 前课复习快闪（交互①） ----
    q_rev = [
        q('简答题中"Why … ?"应当用哪个词回答？', ["Because …", "Yes, …", "No, …"], 0, "Why 问原因，必须用 Because 回答，这是阅卷扣分点。"),
        q('翻译题中，中文"他每天早上七点起床"最先定什么？', ["人称与动词时态", "句子标点", "单词拼写"], 0, "先定人称(He)+时态(一般现在时)，再写句子。"),
        q('简答"Yes/No"问句，答语开头的时态必须和什么一致？', ["问句的时态", "回答者的心情", "文章标题"], 0, "时态必须与问句一致，问句用 does 就用 does 答。"),
        q('L25 我们重点从"简答与翻译"中学到了什么核心方法？', ["先审人称时态再动笔", "先写答案再读题", "先检查再作答"], 0, "核心方法：审题→定人称时态→写答案→检查。"),
    ]
    add_page(eng.section_head("复", "前课知识 · 快闪复习（L25 简答与翻译）") +
             eng.game_board("前课复习 4 问", "⚡", "点击作答，答对撒彩带。", quiz_grid(q_rev)),
             1, "前课复习", "快闪闯关", priority="CORE", minutes=5)

    # ---- P4 跨课词汇复习（交互②） ----
    q_rev2 = [
        q('Please ___ my question in English. 为什么该填 answer？', ["因为 answer a question 是固定搭配", "因为 answer 是名词", "因为 ask 是过去式"], 0, "answer a question 是固定搭配，意为“回答问题”。"),
        q('"___ do you like the book? — Because it is fun." 为什么用 Why？', ["因为答语是 Because", "因为 What 问事物", "因为 How 问方式"], 0, "Because 开头的答语对应 Why 问原因。"),
        q('We should ___ the sentence into English. 为什么选 translate？', ["因为“翻译成英文”是 translate into", "因为 read 是阅读", "因为 write 是写作"], 0, "translate … into English 意为“把…翻译成英文”。"),
        q('Give me a ___ for being late. 为什么 reason 是正确选项？', ["因为“迟到的理由”用 reason", "因为 book 是书", "因为 pen 是笔"], 0, "reason for … 意为“…的理由”，是固定搭配。"),
    ]
    add_page(eng.section_head("复", "跨课词汇复习 · 配合检测（互动）") +
             '<div class="body-text">每道题不仅要选对，还要理解<span class="highlight">为什么</span>选这个答案。</div>' + quiz_grid(q_rev2),
             1, "词汇复习", "理解为什么", priority="EXTEND", minutes=4)

    # =============================================================
    # SEGMENT 2: 写作语料 (P5-P7, 3 pages)
    # =============================================================
    # ---- P5 衔接词 ----
    link_words = [
        ("first", "/fɜːst/", "adv.", "首先", "First of all", "First, I get up.", "First 用于开头列举。"),
        ("then", "/ðen/", "adv.", "然后", "and then", "Then I read.", "Then 表顺序。"),
        ("next", "/nekst/", "adv.", "接下来", "next to", "Next, I have class.", "Next 承接 Then。"),
        ("finally", "/ˈfaɪnəli/", "adv.", "最后", "at last", "Finally, I sleep.", "Finally 收尾。"),
        ("and", "/ænd/", "conj.", "和；并且", "and also", "I like apples and pears.", "and 并列。"),
        ("but", "/bʌt/", "conj.", "但是", "but also", "I like math but not P.E.", "but 转折。"),
        ("so", "/səʊ/", "conj.", "所以", "so that", "It rains, so we stay.", "so 因果（并列）。"),
        ("also", "/ˈɔːlsəʊ/", "adv.", "也", "not only…but also", "I also like music.", "also 补充。"),
        ("for example", "/fər ɪɡˈzɑːmpl/", "phr.", "例如", "such as", "I like sports, for example, soccer.", "for example 举例。"),
        ("in my opinion", "/ɪn maɪ əˈpɪnjən/", "phr.", "我认为", "I think", "In my opinion, English is fun.", "In my opinion 表观点。"),
    ]
    add_page(eng.section_head("料", "写作语料 ① · 衔接词（10 个）") + eng.vocab_cards(link_words),
             2, "衔接词", "点击卡片看例句", priority="CORE", minutes=5)

    # ---- P6 句型模板 ----
    ext_s = [
        ("开头句式", "gold", "<b>I am writing to …</b><br><b>Let me tell you about …</b>"),
        ("列举句式", "green", "<b>First … Then … Next … Finally …</b>"),
        ("观点句式", "blue", "<b>I think …</b><br><b>In my opinion …</b>"),
        ("建议句式", "red", "<b>We should …</b><br><b>You can …</b>"),
        ("结尾句式", "purple", "<b>I hope …</b><br><b>Best wishes,</b>"),
        ("衔接补充", "teal", "<b>and / but / so / also</b> 连句成段"),
    ]
    add_page(eng.section_head("料", "写作语料 ② · 常用句型模板") + eng.ext_cards(ext_s),
             2, "句型模板", "套用不出错", priority="CORE", minutes=5)

    # ---- P7 衔接词选择填空（交互③） ----
    q_link = [
        q('I get up. ___ I brush my teeth. 为什么用 Then？', ['因为“然后”表示时间顺序', '因为 But 表示转折', '因为 So 表示因果'], 0, "Then 表示“然后”，刷牙在起床之后，是时间顺序。"),
        q('He likes apples, ___ he doesn\'t like bananas. 为什么用 but？', ["因为前后意思相反（喜欢 vs 不喜欢）", "因为 and 并列", "因为 so 因果"], 0, "but 表转折：喜欢苹果，但不喜欢香蕉。"),
        q('It is raining, ___ we stay at home. 为什么用 so？', ["因为下雨是原因，待在家是结果", "因为 but 表转折", "因为 and 表并列"], 0, "so 表因果：下雨（原因），所以待在家（结果）。"),
        q('___, I want to say thanks to my teacher. 为什么用 Finally？', ['因为“最后”在句首总结', '因为 First 表开头', '因为 Next 表中间'], 0, "Finally 表示“最后”，用于总结全文。"),
    ]
    add_page(eng.section_head("料", "写作语料 ③ · 衔接词选择填空（交互）") + quiz_grid(q_link),
             2, "衔接词闯关", "即时测试", priority="CORE", minutes=4)

    # =============================================================
    # SEGMENT 3: SOP 五步 (P8-P13, 6 pages ≤6)
    # =============================================================
    # ---- P8 SOP① 审题 ----
    add_page(eng.section_head("法", "SOP ① · 审题（人称 / 时态 / 要点）") +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             six_cards([
                 ("rc-zhug", "要点", "读题圈出全部写作要点，不漏不增。"),
                 ("rc-bin", "人称", "确定第一/第三人称（I / He / She）。"),
                 ("rc-xing", "时态", "基础写作用一般现在时／一般过去时，不超八上U2。"),
                 ("rc-ming", "例句", "I am writing to tell you about my school day."),
                 ("rc-warn", "易错", "❌ 要点漏写 → ✅ 列点前先数清要点。"),
                 ("rc-qita", "口诀", "审人称、定时态、圈要点！"),
             ]), 3, "SOP①审题", "下笔前三问", priority="CORE", minutes=5)

    # ---- P9 SOP② 列点 ----
    add_page(eng.section_head("法", "SOP ② · 列点（覆盖全部要点）") +
             '<div class="body-text">把要点变成 <span class="highlight">1/2/3…</span> 小提纲，每段一个要点。</div>' +
             eng.ext_cards([
                 ("要点→段", "green", "一个要点＝一段，避免揉成一团。"),
                 ("顺序", "blue", "时间顺序：First → Then → Next → Finally。"),
                 ("不跑题", "red", "每个要点都回扣题目，不写无关内容。"),
             ]) +
             '<div class="note-panel"><div class="np-title">记忆口诀</div>先列点，再动笔；缺一点，扣一分。</div>',
             3, "SOP②列点", "提纲挈领", priority="CORE", minutes=4)

    # ---- P10 SOP③ 成句 ----
    add_page(eng.section_head("法", "SOP ③ · 成句（基础句式，不越级）") +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             six_cards([
                 ("rc-zhug", "句式", "主语 + 谓语 + 宾语，简单句最稳。"),
                 ("rc-bin", "肯定", "I like English. / She plays soccer."),
                 ("rc-xing", "三单", "❌ He like → ✅ He likes（三单加 -s）。"),
                 ("rc-ming", "例句", "My school is big and clean."),
                 ("rc-warn", "易错", "❌ 从句堆砌 → ✅ 用 and/but/so 连简单句。"),
                 ("rc-qita", "口诀", "写短句、写对句，胜过长难句！"),
             ]), 3, "SOP③成句", "基础句式", priority="CORE", minutes=5)

    # ---- P11 SOP④ 连段 ----
    add_page(eng.section_head("法", "SOP ④ · 连段（衔接词连句成篇）") +
             '<div class="body-text">用 <span class="highlight">衔接词</span> 把句子连成通顺段落。</div>' +
             eng.ext_cards([
                 ("时间链", "green", "First → Then → Next → Finally"),
                 ("并列/转折", "blue", "and（并列） / but（转折）"),
                 ("因果", "red", "so（因此，并列连词安全）"),
                 ("举例", "purple", "for example 引出例子"),
             ]), 3, "SOP④连段", "衔接成篇", priority="CORE", minutes=4)

    # ---- P12 SOP⑤ 检查 ----
    add_page(eng.section_head("法", "SOP ⑤ · 检查（拼写 / 三单 / 时态）") +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             six_cards([
                 ("rc-zhug", "拼写", "逐词检查拼写与大小写（English 大写 E）。"),
                 ("rc-bin", "三单", "he/she/it 作主语，动词加 -s。"),
                 ("rc-xing", "时态", "通篇时态一致，不混用现在/过去。"),
                 ("rc-ming", "例句", "She watches TV every evening."),
                 ("rc-warn", "易错", "❌ 写完不查 → ✅ 三查：拼写·三单·时态。"),
                 ("rc-qita", "口诀", "写完读三遍，错处自然现！"),
             ]), 3, "SOP⑤检查", "交卷前必做", priority="CORE", minutes=5)

    # ---- P13 SOP 五步闯关（交互④） ----
    q_sop = [
        q('写前第一步是审题，为什么不能直接动笔？', ["因为不审题会漏写要点/用错人称时态", "因为直接写更快", "因为审题浪费时间"], 0, "不审题就会漏要点、用错人称时态，扣分扣到不及格。"),
        q('列点的作用是什么？', ["确保覆盖所有写作要点，不跑题", "增加作文字数", "让作文看起来更复杂"], 0, "列点把题目要点变成提纲，确保不漏不跑。"),
        q('连段时为什么要用衔接词？', ["因为衔接词让句子之间有逻辑关系，读起来通顺", "因为衔接词好看", "因为衔接词可以凑字数"], 0, "衔接词连接前后句，使文章有逻辑、通顺。"),
        q('检查时重点看哪三样？为什么？', ["拼写、三单、时态——这三样最常扣分", "字数、颜色、字体", "标题、段落、标点"], 0, "拼写、三单、时态是阅卷老师最关注的扣分点。"),
    ]
    add_page(eng.section_head("法", "SOP 五步 · 闯关自检（交互）") +
             eng.game_board("SOP 步骤 4 问", "🧭", "点击作答，巩固五步法。", quiz_grid(q_sop)),
             3, "SOP闯关", "五步记忆", priority="CORE", minutes=4)

    # =============================================================
    # SEGMENT 4: 范文拆解 (P14-P17, 4 pages ≤4)
    # =============================================================
    # ---- P14 范文展示① 书信（标注 SOP 落点） ----
    model1 = ('<div class="body-text"><b>范文① · 书信（基础难度，约 70 词）</b></div>'
              '<div class="reading-passage" style="font-size:18px;line-height:1.9">'
              '<b>Dear Tom,</b><br>'
              '<span class="highlight">【审题】</span> I am writing to tell you about my school day. <span class="highlight">【列点·成句】</span> First, I get up at six. Then I read English. Next, I have four classes in the morning. I like math, <span class="highlight">【连段】</span> but I don\'t like P.E. Finally, I do my homework at night. I am happy every day.<br>'
              '<b>Best wishes,</b><br><b>Li Hua</b></div>'
              '<div class="note-panel"><div class="np-title">SOP 落点</div>审题I am writing…→列点First/Then/Next→成句简单句→连段but→检查时态一致。</div>')
    add_page(eng.section_head("范", "范文拆解 ① · 书信范文（标注 SOP 落点）") + model1,
             4, "范文①书信", "SOP 落点标注", priority="CORE", minutes=5)

    # ---- P15 范文① 审题落点分析（六色卡） ----
    add_page(eng.section_head("范", "范文拆解 ② · 审题落点分析（六色卡）") +
             '<div class="sub-label">对标范文①，逐项分析审题要点</div>' +
             six_cards([
                 ("rc-zhug", "人称", "第一人称 I（写信者 Li Hua 介绍自己）。"),
                 ("rc-bin", "时态", "一般现在时（daily routine 日常作息）。"),
                 ("rc-xing", "要点", "学校生活：起床/晨读/上课/爱好/作业/心情。"),
                 ("rc-ming", "例句", "I am writing to tell you about my school day."),
                 ("rc-warn", "易错", "❌ 人称跳变 → ✅ 全篇统一 I，不混 He/She。"),
                 ("rc-qita", "口诀", "人称时态先定好，要点不漏最重要！"),
             ]),
             4, "范文审题", "落点分析", priority="CORE", minutes=4)

    # ---- P16 范文① 结构拆解（书信三段式） ----
    add_page(eng.section_head("范", "范文拆解 ③ · 结构拆解（书信三段式）") +
             eng.ext_cards([
                 ("开头", "gold", "Dear Tom, + I am writing to tell you about my school day.<br>（问候+写信目的，一句话说清）"),
                 ("主体", "green", "First, I get up at six. → Then I read English. → Next, I have four classes.<br>（时间顺序：First/Then/Next，衔接流畅）"),
                 ("转折+结尾", "red", "I like math, but I don't like P.E. → Finally, I do my homework.<br>（but 表转折，Finally 收尾）"),
                 ("落款", "purple", "Best wishes, + Li Hua<br>（书信必备落款，不要漏）"),
             ]) +
             '<div class="note-panel"><div class="np-title">结构口诀</div>开头打招呼，主体按点写，but 表转折，Best wishes 收尾。</div>',
             4, "范文结构", "三段拆解", priority="CORE", minutes=4)

    # ---- P17 范文理解自测 + 同体裁变式题 ----
    q_model = [
        q('范文①为什么用一般现在时而不用过去时？', ["因为描述的是每天发生的日常作息", "因为写信只能用现在时", "因为过去时更复杂"], 0, "范文①写的是每天重复的校园生活，所以用一般现在时。"),
        q('如果范文①改成第三人称（He 代替 I），哪些动词要变？', ["get→gets, read→reads, have→has, don\'t→doesn\'t", "所有词都要变", "只有名词变"], 0, "he/she/it 第三人称单数主语，动词加 -s 或 -es（have→has, don\'t→doesn\'t）。"),
        q('范文①中"but"的作用是什么？', ["表示转折，连接喜欢和不喜欢的两件事", "表示并列", "表示因果"], 0, "but 表转折：I like math, but I don\'t like P.E. — 前后意思相反。"),
        q('【变式题】如果把范文①中"school day"改为"weekend"，要用什么时态？', ["还是一般现在时（周末活动也属日常）", "过去时（周末已过去）", "将来时（周末还没到）"], 0, "周末活动是每周重复的日常活动，仍用一般现在时。"),
    ]
    add_page(eng.section_head("范", "范文拆解 ④ · 理解自测 + 变式题（交互）") +
             '<div class="body-text">每题思考<span class="highlight">为什么</span>，不是考"是什么"。<span class="highlight">变式题</span>：把范文主题从"school day"换成"weekend"，其他不变，检验是否理解。</div>' +
             quiz_grid(q_model) +
             '<div class="note-panel"><div class="np-title">📝 变式思路</div>同一封书信体裁，把主题换成"my weekend"，要点变为：①起床时间 ②上午活动 ③下午活动 ④晚上活动。人称/时态/结构不变，只换内容！下节课将练习通知类写作。</div>',
             4, "范文自测", "考为什么+变式", priority="CORE", minutes=6)

    # =============================================================
    # SEGMENT 5: SOP 方法与技巧 (P18-P19, 2 pages — 替换拼读)
    # =============================================================
    # ---- P18 审题检查清单 ----
    checklist_html = ('<div class="body-text">写作前用这份清单逐项检查，养成习惯。</div>'
                      '<div class="kmap">'
                      '<div class="kmap-node"><div class="kn-title">☐ 人称定了吗？</div><div class="kn-body">I / He / She / We？全篇统一。</div></div>'
                      '<div class="kmap-node"><div class="kn-title">☐ 时态选对了吗？</div><div class="kn-body">一般现在时 / 一般过去时？不混用。</div></div>'
                      '<div class="kmap-node"><div class="kn-title">☐ 要点圈完没？</div><div class="kn-body">题目有几个要点，作文就写几段。</div></div>'
                      '<div class="kmap-node"><div class="kn-title">☐ 衔接词备了吗？</div><div class="kn-body">First/Then/Next/Finally/and/but/so。</div></div>'
                      '<div class="kmap-node"><div class="kn-title">☐ 检查环节有吗？</div><div class="kn-body">写完读三遍：拼写·三单·时态。</div></div>'
                      '</div><div class="note-panel"><div class="np-title">审题口诀</div>人称时态要点圈，列点成句连段查！</div>')
    add_page(eng.section_head("法", "SOP 方法 · 审题检查清单（写作前自查）") + checklist_html,
             5, "审题检查清单", "动笔前必看", priority="CORE", minutes=4)

    # ---- P19 书面格式规范 ----
    format_html = ('<div class="body-text">写作格式也是得分点，下面列出基础层最常扣分的格式规范。</div>'
                   '<div class="sub-label">六色卡记录规范</div>' +
                   six_cards([
                       ("rc-zhug", "书信格式", "开头 Dear + 名字 + 逗号；结尾 Best wishes, + 名字。"),
                       ("rc-bin", "段落首行", "每个段落开头空一格（不缩进也可，但段间空行）。"),
                       ("rc-xing", "标点符号", "句号用 . 不用 。；问号 ?；感叹号 !；不要中英文混用。"),
                       ("rc-ming", "大小写", "句首单词大写；English/Monday/China 专有词大写。"),
                       ("rc-warn", "易错", "❌ 不分段 → ✅ 一个要点一段；❌ 标点漏写 → ✅ 写完检查。"),
                       ("rc-qita", "易错", "❌ I 写小写 i → ✅ 第一人称 I 永远大写。"),
                   ]) +
                   '<div class="note-panel"><div class="np-title">格式口诀</div>书信格式要记牢，标点大小写别忘掉！</div>')
    add_page(eng.section_head("法", "SOP 方法 · 书面格式规范（书信/标点/大小写）") + format_html,
             5, "格式规范", "基础层注意", priority="CORE", minutes=4)

    # =============================================================
    # SEGMENT 6: 演练与动笔 (P20-P33, 14 pages ≥12)
    # =============================================================
    # === A. 句子层 (P20-P23, 4 pages) ===
    # ---- P20 句子仿写① 中文→英文（答案点击揭示） ----
    p20_html = ('<div class="body-text">根据中文写英文句子，注意<span class="highlight">人称·时态·三单</span>。点击下方<span class="highlight">[点击查看答案]</span>可核对。</div>'
                '<div class="sentence-tile"><span class="cn">① 我每天早上六点起床。</span><br>I ________ ________ at six every morning. <span class="fix-badge" onclick="toggleFixBadge(this)" data-answer="填：get up">点击查看答案</span></div>'
                '<div class="sentence-tile"><span class="cn">② 她喜欢读书。</span><br>She ________ ________ books. <span class="fix-badge" onclick="toggleFixBadge(this)" data-answer="填：likes reading">点击查看答案</span></div>'
                '<div class="sentence-tile"><span class="cn">③ 我们放学后打篮球。</span><br>We ________ ________ after school. <span class="fix-badge" onclick="toggleFixBadge(this)" data-answer="填：play basketball">点击查看答案</span></div>'
                '<div class="sentence-tile"><span class="cn">④ 他每天早上七点去上学。</span><br>He ________ ________ school at seven. <span class="fix-badge" onclick="toggleFixBadge(this)" data-answer="填：goes to">点击查看答案</span></div>'
                '<div class="sentence-tile"><span class="cn">⑤ 我妈妈做的饭很好吃。</span><br>My mother ________ good food. <span class="fix-badge" onclick="toggleFixBadge(this)" data-answer="填：cooks">点击查看答案</span></div>'
                '<div class="note-panel"><div class="np-title">检查</div>写完检查：① 主语是谁？② 动词加 -s 了吗？③ 单词拼写对吗？</div>')
    add_page(eng.section_head("练", "句子仿写 ① · 中文→英文（5 句基础句）") + p20_html,
             6, "句子仿写①", "中文→英文", priority="CORE", minutes=6)

    # ---- P21 句子仿写② 错句医生（交互⑥） ----
    q_doc = [
        q('改错："He like apples." 为什么错？应该怎么改？', ["like→likes（三单加 -s）", "He→Him", "apples→apple"], 0, "He 是第三人称单数，动词 like 要加 -s 变成 likes。"),
        q('改错："She go to school." 错误在哪？为什么？', ["go→goes（三单加 -es）", "She→Her", "school→schools"], 0, "She 是第三人称单数，go 要加 -es 变成 goes。"),
        q('改错："I is a student." 为什么 is 是错的？应该用什么？', ["is→am（I 配 am）", "I→He", "student→students"], 0, "I 是第一人称单数，be 动词用 am，不是 is。"),
        q('改错："They plays soccer." 为什么 plays 是错的？', ["plays→play（They 复数不加 -s）", "They→He", "soccer→soccers"], 0, "They 是复数主语，动词不用加 -s，用 play。"),
    ]
    add_page(eng.section_head("练", "句子仿写 ② · 错句医生（改错专练·交互）") +
             eng.game_board("错句医生 4 题", "🩺", "找出错误，说清为什么错。", quiz_grid(q_doc)),
             6, "错句医生", "改错+说原因", priority="CORE", minutes=5)

    # ---- P22 句子仿写③ 简单句合并（and/but/so） ----
    p22_html = ('<div class="body-text">用 and / but / so 把两个简单句合并成一句，注意<span class="highlight">逻辑关系</span>。</div>'
                '<div class="sentence-tile"><span class="cn">① I like math. I like English.</span><br>→ I like math ________ I like English. <span class="fix-badge">填：and（并列，都喜欢）</span></div>'
                '<div class="sentence-tile"><span class="cn">② I like soccer. I don\'t like basketball.</span><br>→ I like soccer ________ I don\'t like basketball. <span class="fix-badge">填：but（转折，喜欢 vs 不喜欢）</span></div>'
                '<div class="sentence-tile"><span class="cn">③ It is cold. I wear a coat.</span><br>→ It is cold, ________ I wear a coat. <span class="fix-badge">填：so（因果，冷→穿外套）</span></div>'
                '<div class="sentence-tile"><span class="cn">④ She gets up at six. She reads English.</span><br>→ She gets up at six ________ she reads English. <span class="fix-badge">填：and（并列，两件事先后）</span></div>'
                '<div class="note-panel"><div class="np-title">注意</div>and=并列/递进，but=转折(相反)，so=因果(因为→所以)。</div>')
    add_page(eng.section_head("练", "句子仿写 ③ · 简单句合并（and/but/so）") + p22_html,
             6, "句子合并", "and/but/so", priority="CORE", minutes=5)

    # ---- P23 句子仿写④ 用给定词汇写句 ----
    p23_html = ('<div class="body-text">用给出的词汇写完整句子，注意<span class="highlight">主语+谓语+宾语</span>结构。</div>'
                '<div class="sentence-tile"><span class="cn">① 用 first / get up / at six 写一句</span><br>→ ________, I ________ ________ ________ six. <span class="fix-badge">First, I get up at six.</span></div>'
                '<div class="sentence-tile"><span class="cn">② 用 she / like / reading 写一句</span><br>→ ________ ________ ________ ________. <span class="fix-badge">She likes reading.</span></div>'
                '<div class="sentence-tile"><span class="cn">③ 用 we / play basketball / after school 写一句</span><br>→ ________ ________ ________ ________ ________. <span class="fix-badge">We play basketball after school.</span></div>'
                '<div class="sentence-tile"><span class="cn">④ 用 he / go to school / by bike 写一句</span><br>→ ________ ________ ________ ________ ________ ________. <span class="fix-badge">He goes to school by bike.</span></div>'
                '<div class="note-panel"><div class="np-title">提示</div>写完检查：主语三单 → 动词 + -s。</div>')
    add_page(eng.section_head("练", "句子仿写 ④ · 用给定词汇造句") + p23_html,
             6, "造句练习", "词汇→句子", priority="CORE", minutes=5)

    # === B. 段落层 (P24-P26, 3 pages) ===
    # ---- P24 段落扩写① 介绍学校 ----
    p24_html = ('<div class="writing-prompt">'
                '<div class="wp-title">✏️ 段落扩写 · 介绍学校</div>'
                '<div class="wp-body">首句：<b>My school is big and beautiful.</b><br>'
                '中文要点：① 学校有 30 个教室 ② 有一个大操场 ③ 操场上有许多树和花<br>'
                '写 3-4 句英文，用 First/Then/Next/Finally 或 and/but/so 连接。</div>'
                '<div class="wp-hint"><b>高分提示：</b>There are 30 classrooms. / There is a big playground. / There are many trees and flowers.</div>'
                '</div>'
                '<div class="scaffold-fill">'
                'My school is big and beautiful. First, ________ ________ 30 classrooms. Then, ________ ________ a big playground. Next, ________ ________ many trees and flowers on the playground. I like my school!</div>'
                '<div class="note-panel"><div class="np-title">检查</div>① 写了几个要点？② there be 用对了吗？③ 有无衔接词？</div>')
    add_page(eng.section_head("练", "段落扩写 ① · 介绍学校（首句+要点）") + p24_html,
             6, "段落扩写①", "介绍学校", priority="CORE", minutes=6)

    # ---- P25 段落扩写② 书信段落（介绍家庭） ----
    p25_html = ('<div class="writing-prompt">'
                '<div class="wp-title">✏️ 段落扩写 · 书信段落（介绍家庭）</div>'
                '<div class="wp-body">这是书信正文的一段，首句：<b>There are four people in my family.</b><br>'
                '中文要点：① 爸爸是医生，妈妈是老师 ② 我 13 岁，是学生 ③ 妹妹 6 岁，上幼儿园<br>'
                '写 3-4 句英文，用衔接词连句，注意三单。</div>'
                '<div class="wp-hint"><b>高分提示：</b>My father is a doctor. / My mother is a teacher. / I am a student. / My little sister is 6 years old.</div>'
                '</div>'
                '<div class="scaffold-fill">'
                'There are four people in my family. My father ________ a doctor, and my mother ________ a teacher. I ________ 13 years old and I ________ a student. My little sister ________ 6 years old and she ________ to kindergarten. I love my family!</div>'
                '<div class="note-panel"><div class="np-title">检查</div>① 三单：he/she/it 后 be 动词用 is 吗？② 用了衔接词吗？③ 句子通顺吗？</div>')
    add_page(eng.section_head("练", "段落扩写 ② · 书信段落（介绍家庭）") + p25_html,
             6, "段落扩写②", "家庭", priority="CORE", minutes=6)

    # ---- P26 段落扩写③ 介绍周末活动 ----
    p26_html = ('<div class="writing-prompt">'
                '<div class="wp-title">✏️ 段落扩写 · 我的周末</div>'
                '<div class="wp-body">首句：<b>I have a happy weekend.</b><br>'
                '中文要点：① 周六早上写作业 ② 下午打篮球 ③ 周日和父母去公园<br>'
                '写 3-4 句英文，用 First/Then/Next/Finally 连接，时态用一般现在时。</div>'
                '<div class="wp-hint"><b>高分提示：</b>On Saturday morning, I do my homework. / In the afternoon, I play basketball. / On Sunday, I go to the park with my parents.</div>'
                '</div>'
                '<div class="scaffold-fill">'
                'I have a happy weekend. First, on Saturday morning, I ________ my homework. ________, in the afternoon, I ________ basketball. Next, on Sunday, I ________ to the park ________ my parents. I love my weekend!</div>'
                '<div class="note-panel"><div class="np-title">检查</div>① 时间顺序连贯吗？② 每个句子主语一致？③ 有无错别字？</div>')
    add_page(eng.section_head("练", "段落扩写 ③ · 我的周末（首句+要点）") + p26_html,
             6, "段落扩写③", "周末活动", priority="CORE", minutes=6)

    # === C. 全文层 (P27-P28, 2 pages ≥2) ===
    # ---- P27 脚手架填空① 书信范文 ----
    p27_html = ('<div class="body-text">用括号内动词的正确形式填空，完成这篇书信范文。</div>'
                '<div class="scaffold-fill">'
                'Dear Tom,<br>'
                'I am writing to tell you about my school day.<br>'
                'First, I ________ (get) up at six. Then I ________ (read) English. Next, I ________ (have) four classes. I like math, ________ I don\'t like P.E. (填衔接词)<br>'
                'Finally, I ________ (do) my homework. I ________ (be) happy every day.<br>'
                'Best wishes,<br>Li Hua</div>'
                '<div class="note-panel"><div class="np-title">答案·解析</div>get(原形，I 非三单) / read(原形) / have(原形) / but(转折) / do(原形) / am(I 配 am)</div>')
    add_page(eng.section_head("练", "全文填空 ① · 书信范文填空（动词三单/衔接词）") + p27_html,
             6, "书信填空", "动词三单+衔接词", priority="CORE", minutes=6)

    # ---- P28 脚手架填空② 书信变式（介绍家庭） ----
    p28_html = ('<div class="body-text">用括号内动词的正确形式填空，完成这封书信。</div>'
                '<div class="scaffold-fill">'
                'Dear Tom,<br>'
                'I am writing to tell you about my family.<br>'
                'There ________ (be) four people in my family. My father ________ (be) a doctor and my mother ________ (be) a teacher. My sister ________ (be) 6 years old. She ________ (go) to kindergarten. I ________ (like) my family very much.<br>'
                'Best wishes,<br>Li Hua</div>'
                '<div class="note-panel"><div class="np-title">答案·解析</div>are(复数There be) / is(三单) / is(三单) / is(三单) / goes(三单加-es) / like(I→原形)</div>')
    add_page(eng.section_head("练", "全文填空 ② · 书信变式填空（介绍家庭）") + p28_html,
             6, "书信填空②", "家庭主题", priority="CORE", minutes=5)

    # === D. 命题写作 (P29-P31, 3 pages ≥2) ===
    # ---- P29 命题写作① 书信（含构思框架） ----
    p29_html = ('<div class="writing-prompt">'
                '<div class="wp-title">✏️ 命题写作 · 书信（≥40 词）</div>'
                '<div class="wp-body"><b>题目：</b>假设你是李华，请给你的笔友 Peter 写一封信，介绍你的学校生活。要点：<br>'
                '① 早上几点起床  ② 上午上什么课  ③ 中午吃什么  ④ 下午放学后做什么</div>'
                '</div>'
                '<div class="writing-structure">'
                '<div class="ws-title">📐 构思框架（三部分）</div>'
                '<div class="ws-part"><span class="ws-pnum">① 开头（1–2 句）</span><div class="ws-pbody">Dear Peter, / I am writing to tell you about my school life. 点明写信目的。</div></div>'
                '<div class="ws-part"><span class="ws-pnum">② 正文（4–6 句）</span><div class="ws-pbody">First, I get up at six. Then I have classes in the morning. Next, I have lunch at school. Finally, I play basketball after school. 用衔接词串起要点。</div></div>'
                '<div class="ws-part"><span class="ws-pnum">③ 结尾（2–3 句）</span><div class="ws-pbody">I am happy every day. / Best wishes, / Li Hua 表达感受 + 署名。</div></div>'
                '</div>'
                '<div class="wp-hint"><b>高分句式提示：</b>I am writing to tell you about… / First… Then… Next… Finally… / I like… but I don\'t like… / Best wishes…</div>'
                '<div class="wp-checklist">'
                '<b>✏️ 写作检查清单：</b><br>'
                '☐ 人称=第一人称 I（全篇统一）<br>'
                '☐ 时态=一般现在时（全篇一致）<br>'
                '☐ 三单检查：I 开头动词不加 -s<br>'
                '☐ 衔接词：First…Then…Next…Finally…<br>'
                '☐ 拼写检查：English 大写 E，句首大写<br>'
                '☐ 字数：≥40 词</div>')
    add_page(eng.section_head("练", "命题写作 ① · 书信（给笔友介绍学校生活）") + p29_html,
             6, "命题写作①", "书信", priority="CORE", minutes=8)

    # ---- P30 命题写作② 书信变式（含构思框架） ----
    p30_html = ('<div class="writing-prompt">'
                '<div class="wp-title">✏️ 命题写作 · 书信变式（≥40 词）</div>'
                '<div class="wp-body"><b>题目：</b>假设你是李华，请给你的笔友 Peter 写一封信，介绍你的周末生活。要点：<br>'
                '① 周六上午做什么  ② 下午做什么  ③ 周日做什么  ④ 你的感受</div>'
                '</div>'
                '<div class="writing-structure">'
                '<div class="ws-title">📐 构思框架（三部分）</div>'
                '<div class="ws-part"><span class="ws-pnum">① 开头（1–2 句）</span><div class="ws-pbody">Dear Peter, / I am writing to tell you about my weekend. 点明写信目的（周末）。</div></div>'
                '<div class="ws-part"><span class="ws-pnum">② 正文（4–6 句）</span><div class="ws-pbody">On Saturday morning, I do my homework. In the afternoon, I play basketball. On Sunday, I go to the park. 用时间词写周六周日分别做什么。</div></div>'
                '<div class="ws-part"><span class="ws-pnum">③ 结尾（2–3 句）</span><div class="ws-pbody">I have a happy weekend. / Best wishes, / Li Hua 表达感受 + 署名。</div></div>'
                '</div>'
                '<div class="wp-hint"><b>高分句式提示：</b>I am writing to tell you about… / On Saturday morning, I… / In the afternoon, I… / On Sunday, I… / I feel… / Best wishes…</div>'
                '<div class="wp-checklist">'
                '<b>✏️ 写作检查清单：</b><br>'
                '☐ 格式=书信格式（Dear…/Best wishes）<br>'
                '☐ 人称=第一人称 I（全篇统一）<br>'
                '☐ 时态=一般现在时<br>'
                '☐ 三单：I 开头动词不加 -s<br>'
                '☐ 衔接词：On Saturday… In the afternoon… On Sunday…<br>'
                '☐ 拼写：English 大写 E，I 永远大写<br>'
                '☐ 字数：≥40 词</div>')
    add_page(eng.section_head("练", "命题写作 ② · 书信变式（给笔友介绍周末生活）") + p30_html,
             6, "命题写作②", "书信变式", priority="CORE", minutes=8)

    # ---- P31 命题写作③ 通知（含构思框架） ----
    p31_html = ('<div class="writing-prompt">'
                '<div class="wp-title">✏️ 命题写作 · 通知（≥40 词）</div>'
                '<div class="wp-body"><b>题目：</b>你是学生会主席，请写一则通知，通知同学们下周五下午 3 点在学校操场参加英语角活动。要点：<br>'
                '① 标题 NOTICE  ② 活动：英语角  ③ 时间：下周五下午 3 点  ④ 地点：学校操场  ⑤ 联系人：你（Li Hua）</div>'
                '</div>'
                '<div class="writing-structure">'
                '<div class="ws-title">📐 构思框架（三部分）</div>'
                '<div class="ws-part"><span class="ws-pnum">① 标题</span><div class="ws-pbody">NOTICE（居中，全部大写）。</div></div>'
                '<div class="ws-part"><span class="ws-pnum">② 正文（3–4 句）</span><div class="ws-pbody">We have an English Corner at 3:00 pm next Friday. Please come to the school playground. 写清活动+时间+地点。</div></div>'
                '<div class="ws-part"><span class="ws-pnum">③ 落款（1–2 句）</span><div class="ws-pbody">For more information, please call Li Hua. / The Student Union 写清联系人/组织。</div></div>'
                '</div>'
                '<div class="wp-hint"><b>高分句式提示：</b>NOTICE（标题居中） / We have an English Corner at 3:00 pm next Friday. / Please come to the school playground. / Time: 3:00 pm next Friday / Place: school playground / For more information, please call Li Hua.</div>'
                '<div class="wp-checklist">'
                '<b>✏️ 写作检查清单：</b><br>'
                '☐ 标题写 NOTICE（居中，全部大写）<br>'
                '☐ 时间·地点·活动三要素写全<br>'
                '☐ 人称用 We（我们）或 You（你们）<br>'
                '☐ 时态用一般现在时<br>'
                '☐ 拼写检查：NOTICE 大写，专有词大写</div>'
                '<div class="note-panel"><div class="np-title">注意</div>通知的要点：时间+地点+活动+联系人，缺一不可。</div>')
    add_page(eng.section_head("练", "命题写作 ③ · 通知（英语角活动通知）") + p31_html,
             6, "命题写作③", "通知", priority="CORE", minutes=7)

    # === E. 检查与自评 (P32-P33, 2 pages) ===
    # ---- P32 写作检查清单（交互⑦） ----
    q_check = [
        q('写完作文后，第一步应该检查什么？为什么？', ["拼写和大小写", "段落的空行", "字迹是否工整"], 0, "拼写和大小写是最基础的扣分点，English 大写 E、I 永远大写不能错。"),
        q('"She like playing soccer" 这句话错在哪？为什么？', ["like→likes（She 三单）", "playing→play", "soccer→soccers"], 0, "She 是第三人称单数，like 要加 -s 变成 likes。"),
        q('为什么作文中不能出现比较级（如 better）？', ["因为基础层还没学，老师可能会扣分", "因为比较级不常用", "因为比较级拼写复杂"], 0, "比较级不在基础层范围内，写错会被扣分，用简单句最安全。"),
        q('一篇文章里时态混用（现在时+过去时）会怎样？为什么？', ["会被扣分，因为时态不一致导致逻辑混乱", "没事，老师不仔细看", "时态混用表示水平高"], 0, "时态必须全篇一致，混用会让阅卷老师觉得逻辑混乱，严重扣分。"),
    ]
    add_page(eng.section_head("练", "写作检查清单 · 自测（交互）") +
             eng.game_board("写作检查 4 问", "✅", "做完作文后，用这些题检查一下自己的检查习惯。", quiz_grid(q_check)),
             6, "检查自测", "交互检查", priority="CORE", minutes=5)

    # ---- P33 评分自测（三维评分题，考"为什么/应用"） ----
    q_score = [
        q('一篇作文要点全写了但语法错误多，哪个维度扣分最多？', ["语言准确", "内容完整", "结构连贯"], 0, "语法错误多→语言准确维度扣分最多；内容完整看要点是否写全，结构连贯看衔接词。"),
        q('"First…Then…Next…Finally…" 可以提高哪个维度的分数？', ["结构连贯", "内容完整", "语言准确"], 0, "时间顺序衔接词让文章结构清晰，提高结构连贯维度分数。"),
        q('如果漏写了题目中的一个要点，哪个维度扣分？', ["内容完整（漏要点扣内容分）", "语言准确（不影响）", "结构连贯"], 0, "漏要点→内容完整维度扣分，所以审题时要圈全要点。"),
        q('"I am twelve years old. I am in Class 3." 这句话哪个维度做得最好？', ["语言准确（时态/语法/拼写都正确）", "内容完整", "结构连贯"], 0, "句子语法正确、拼写无误、I 大写→语言准确做得好。"),
    ]
    add_page(eng.section_head("练", "评分自测 · 三维评分题（交互）") +
             eng.game_board("评分自测 4 问", "⭐", "考“为什么”扣分，不考“是什么”。", quiz_grid(q_score)),
             6, "评分自测", "考为什么扣分", priority="CORE", minutes=5)

    # =============================================================
    # SEGMENT 7: 评分维度 (P34-P37, 4 pages ≥4)
    # =============================================================
    # ---- P34 评分维度总览 ----
    add_page(eng.section_head("评", "评分维度 ① · 总览（对齐 exam_spec 写作 15 分）") +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             six_cards([
                 ("rc-zhug", "内容完整", "覆盖全部要点，不漏不增。"),
                 ("rc-bin", "语言准确", "拼写/三单/时态正确，≤八上U2。"),
                 ("rc-xing", "结构连贯", "衔接词连段，段落清晰。"),
                 ("rc-ming", "例句", "First… Then… Next… Finally…"),
                 ("rc-warn", "易错", "❌ 要点漏写 → ✅ 先列点再写。"),
                 ("rc-qita", "口诀", "内容全、语言准、结构顺！"),
             ]), 7, "评分总览", "三维对齐", priority="CORE", minutes=5)

    # ---- P35 内容完整 ----
    add_page(eng.section_head("评", "评分维度 ② · 内容完整") +
             eng.ext_cards([
                 ("要点覆盖", "green", "题目几个要点，作文就写几个要点。"),
                 ("不跑题", "red", "每段回扣题目，不写无关句。"),
                 ("字数", "blue", "基础写作 60–80 词，≥40 词不扣分。"),
             ]), 7, "内容完整", "要点不漏", priority="CORE", minutes=4)

    # ---- P36 语言准确 ----
    add_page(eng.section_head("评", "评分维度 ③ · 语言准确（≤八上U2）") +
             '<div class="sub-label">六色卡规则矩阵</div>' +
             six_cards([
                 ("rc-zhug", "拼写", "English 大写，单词拼写准确。"),
                 ("rc-bin", "三单", "he/she/it + 动词 -s。"),
                 ("rc-xing", "时态", "通篇一致，不混现在/过去。"),
                 ("rc-ming", "例句", "She watches TV every evening."),
                 ("rc-warn", "易错", "❌ 比较级/从句 → ✅ 简单句安全。"),
                 ("rc-qita", "口诀", "拼写三单时态，三查保准确！"),
             ]), 7, "语言准确", "基础不越级", priority="CORE", minutes=5)

    # ---- P37 评分样例 ----
    add_page(eng.section_head("评", "评分维度 ④ · 好句 vs 差句对比") +
             eng.ext_cards([
                 ("好句", "green", "I get up at six. Then I read English. （简单句+衔接词，清晰连贯）"),
                 ("差句", "red", "I get up six. then read english. （漏介词 at、三单错、小写 English、无衔接）"),
                 ("提升", "blue", "加 First/Then，动词加 -s(E)，专有词大写 English。"),
             ]), 7, "评分样例", "对照提升", priority="EXTEND", minutes=3)

    # =============================================================
    # SEGMENT 8: 课堂总结 (P38-P40, 3 pages)
    # =============================================================
    # ---- P38 课堂总结 ----
    add_page(eng.section_head("结", "课堂总结 · 知识图谱") +
             '<div class="kmap">'
             '<div class="kmap-node"><div class="kn-title">方法</div><div class="kn-body">SOP 五步：审列成连查 + 审题检查清单 + 格式规范</div></div>'
             '<div class="kmap-node"><div class="kn-title">语料</div><div class="kn-body">衔接词 10 个 + 句型模板 6 组</div></div>'
             '<div class="kmap-node"><div class="kn-title">演练</div><div class="kn-body">句子→段落→全文→命题写作，层层递进</div></div>'
             '<div class="kmap-node"><div class="kn-title">评分</div><div class="kn-body">内容/语言/结构三维</div></div>'
             '</div><div class="note-panel"><div class="np-title">课后作业</div>① 背 10 个衔接词；② 用 SOP 写一篇书信（≥40 词）；③ 完成配套练习。</div>',
             8, "课堂总结", "知识图谱", priority="CORE", minutes=3)

    # ---- P39 Exit Ticket（交互⑧） ----
    q_exit = [
        q('"所以"用英文怎么表达？为什么？', ["so（因果）", "but（转折）", "and（并列）"], 0, "所以用 so，表示“因为……所以……”的因果关系。"),
        q('"First"在作文中起什么作用？', ["表示时间顺序的第一步", "表示转折", "表示总结"], 0, "First 表示“首先”，开始列举的第一项。"),
        q('She ________ to school every day. 该填什么？为什么？', ["goes（三单加 -es）", "go（原形）", "going（ing 形式）"], 0, "She 是第三人称单数，go 要加 -es 变成 goes。"),
        q('写前第一步应该是？为什么？', ["审题（定人称时态，圈要点）", "直接写（省时间）", "先检查（写完了再查）"], 0, "先审题才能确定人称时态和要点，不审题会漏要点。"),
    ]
    exit_html = (eng.section_head("检", "Exit Ticket · 5 分钟形成性检测") +
                 '<div class="body-text"><span class="highlight">5 题</span>：4 选择 + 1 开放。<b>课堂自查，不计入正式练习卷。</b></div>' +
                 quiz_grid(q_exit) +
                 '<div class="quiz-q"><div class="qq-text">开放题 · 用 SOP 写一句书信开头（不少于 2 个要点）</div>'
                 '<div class="body-text" style="margin:6px 0">例：Dear Tom, I am writing to tell you about my school. I get up at six and I have four classes.</div>'
                 '<div class="note-panel"><div class="np-title">参考思路</div>书信格式用 Dear…开头，主体用 I am writing to… / First…Then…，至少 2 个要点。</div></div>')
    add_page(exit_html, 8, "Exit Ticket", "检测通关", priority="CORE", minutes=5)

    # ---- P40 课后作业 ----
    add_page(eng.section_head("结", "课后作业 · 与下节课预告") +
             '<div class="kmap">'
             '<div class="kmap-node"><div class="kn-title">作业①</div><div class="kn-body">背 10 个衔接词并默写（first…in my opinion）。</div></div>'
             '<div class="kmap-node"><div class="kn-title">作业②</div><div class="kn-body">用 SOP 五步写一篇书信（≥40 词，写完后对照检查清单自查）。</div></div>'
             '<div class="kmap-node"><div class="kn-title">作业③</div><div class="kn-body">完成配套练习（听力按教师指令）。</div></div>'
             '<div class="kmap-node"><div class="kn-title">下节课</div><div class="kn-body">S5 冲刺段后续综合套卷演练。</div></div>'
             '</div>', 8, "课后作业", "预告下节", priority="CORE", minutes=2)

    # =============================================================
    # SEGMENT 9: 思维导图 (P41-P42, 2 pages)
    # =============================================================
    # ---- P41 思维导图·总览（交互⑨） ----
    mm_branches = [
        ("写作SOP五步", "🧭", "<b>①审题</b> 人称/时态/要点　<b>②列点</b> 要点提纲　<b>③成句</b> 简单句　<b>④连段</b> 衔接词　<b>⑤检查</b> 拼写三单时态"),
        ("范文×2", "📑", "书信范文：Dear…+主体(First/Then/Next)+Best wishes　书信变式：不同主题的书信（主题/时间/对象变化）"),
        ("衔接词全表", "🔗", "first/then/next/finally　and/but/so　also/for example/in my opinion"),
        ("评分三维", "⭐", "内容完整（要点不漏）　语言准确（拼写三单时态）　结构连贯（衔接词）"),
        ("SOP方法技巧", "📋", "审题检查清单（5 问）　格式规范（书信/标点/大小写）"),
        ("易错总结", "🧠", "三单 -s　拼写大写　时态一致　不写比较级/从句　I 永远大写"),
    ]
    mm_cards = "".join(
        '<div class="mm-branch ext-card" onclick="event.stopPropagation(); mmToggle(this)">'
        '<div class="ext-cat">%s %s</div><div class="mm-chips" style="display:none">%s</div></div>'
        % (icon, label, body) for label, icon, body in mm_branches)
    mm_html = (eng.section_head("图", "课堂思维导图 · 本课全貌（点击分支看详情）") +
               '<div class="body-text">点击分支复盘本课 <span class="highlight">SOP + 范文 + 衔接词 + 评分 + 方法与技巧 + 易错</span>。</div>' +
               '<div class="mm-grid">' + mm_cards + '</div>' +
               '<div class="note-panel" id="mmPanel" style="margin-top:12px"><div class="np-title" id="mmPanelTitle">🧭 写作SOP五步</div>'
               '<div id="mmPanelChips"><b>①审题</b> 人称/时态/要点　<b>②列点</b> 要点提纲　<b>③成句</b> 简单句　<b>④连段</b> 衔接词　<b>⑤检查</b> 拼写三单时态</div></div>')
    add_page(mm_html, 9, "思维导图", "互动复盘", priority="CORE", minutes=3)

    # ---- P42 思维导图·完整内容 ----
    add_page(eng.section_head("图", "思维导图 · 完整内容页") +
             '<div class="kmap">'
             '<div class="kmap-node"><div class="kn-title">SOP 五步</div><div class="kn-body">审题(人称/时态/要点)→列点(提纲)→成句(简单句)→连段(衔接词)→检查(拼写/三单/时态)</div></div>'
             '<div class="kmap-node"><div class="kn-title">衔接词全表</div><div class="kn-body">first/then/next/finally; and/but/so; also/for example/in my opinion</div></div>'
             '<div class="kmap-node"><div class="kn-title">评分三维</div><div class="kn-body">内容完整 / 语言准确(≤八上U2) / 结构连贯</div></div>'
             '<div class="kmap-node"><div class="kn-title">SOP 方法</div><div class="kn-body">审题检查清单 5 问 + 书面格式规范(书信/标点/大小写)</div></div>'
             '</div><div class="note-panel"><div class="np-title">易错</div>三单 -s；English 大写；时态一致；不写比较级/从句；I 永远大写。</div>',
             9, "完整大纲", "对照自测", priority="EXTEND", minutes=3)

    # ==================== 组装 ====================
    total = p[0] - 1
    seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
    js_extra = ("var studentId='stu_xyj';\n" +
                JS_FULL % (total, json.dumps(seg_pages, ensure_ascii=False),
                           json.dumps(page_meta, ensure_ascii=False)))
    # CSS: 恢复 eng.CSS_EXTRA 视觉层，但运行时剥离 .rule-card 和 .quiz-opt 基础定义（保留主题 CSS 中规范版）
    import re
    _css_extra = eng.CSS_EXTRA
    # 移除 .rule-card{...} 和 .rule-card::before{...}（保留主题 CSS 中唯一的规范版）
    _css_extra = re.sub(r'\.rule-card\{[^}]*\}', '', _css_extra)
    _css_extra = re.sub(r'\.rule-card::before\{[^}]*\}', '', _css_extra)
    # 移除 .quiz-opt{...} 基础定义（保留主题 CSS 中唯一的规范版；不删除 .game-board .quiz-opt 等复合选择器）
    _css_extra = re.sub(r'\.quiz-opt\{[^}]*\}', '', _css_extra)
    css_combined = CORE_CSS + "\n" + _css_extra + "\n" + get_theme_css_l26()
    html = build_courseware(title="第26课时 · 书面表达 SOP 专项冲刺（重做版）", pages_dict=pages,
                            js_extra=js_extra, session="L26", nav_html=NAV_HTML,
                            stage_badge=stage_badge, n_pages=total, css_extra=css_combined)
    return html

def main():
    base = "D:/英语教学/许颖嘉"
    folder = os.path.join(base, "第26课时")
    ppt_dir = os.path.join(folder, "课件成品_网页PPT")
    os.makedirs(ppt_dir, exist_ok=True)
    # 不再生成契约目录
    target = os.path.join(ppt_dir, "第26课时_课件_基础.html")
    print("🔨 生成 L26 重做版课件（书面表达 SOP 专项冲刺 · 42 页 · 强化动笔）…")
    html = generate_lesson_26()
    with open(target, "w", encoding="utf-8") as f:
        f.write(html)
    print("  写入 %d 字节" % len(html.encode("utf-8")))
    import sys as _sys
    r = subprocess.run([_sys.executable, 'D:/英语教学/00_工具/verify_v2.py', target],
                       capture_output=True, text=True, encoding='utf-8')
    print(r.stdout)
    if r.stderr:
        print("STDERR:", r.stderr)
    print("==> verify_v2 returncode:", r.returncode)

if __name__ == "__main__":
    main()