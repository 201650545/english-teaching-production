# -*- coding: utf-8 -*-
"""M12 创意组件库：10 个可复用组件 + 白话映射表
每个组件独立函数，返回 HTML 片段；可复用、不跨课重样。
组件数 = 当课新知识点数（L5 需 6 个）。
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------- 组件 1：翻牌记忆 ----------
def flip_cards(words, title="翻牌记忆"):
    """翻牌：点击翻转查看词义。words=[(en, cn), ...]"""
    cards = "".join(
        f'<div class="flip-card" onclick="event.stopPropagation();this.classList.toggle(\'flipped\')">'
        f'<div class="flip-inner"><div class="flip-front">{en}</div><div class="flip-back">{cn}</div></div></div>'
        for en, cn in words
    )
    return f'<div class="component flip-memory"><h3>{title}</h3><div class="flip-grid">{cards}</div></div>'

# ---------- 组件 2：快速选择 ----------
def quick_select(q, options, correct, title="快速选择"):
    """快选：点击选项即时反馈。options=[(label, is_correct), ...]"""
    opts = "".join(
        f'<button class="quiz-opt" data-correct="{1 if is_c else 0}" onclick="checkOpt(this)">{label}</button>'
        for label, is_c in options
    )
    return f'<div class="component quick-select"><h3>{title}</h3><div class="q-stem">{q}</div><div class="q-opts">{opts}</div></div>'

# ---------- 组件 3：打地鼠 ----------
def whack_a_mole(words, title="打地鼠"):
    """打地鼠：目标词随机出现，点击得分。words=[en, ...]"""
    moles = "".join(f'<div class="mole" data-word="{w}" onclick="whack(event)">{w}</div>' for w in words)
    return f'<div class="component whack"><h3>{title}</h3><div class="mole-grid">{moles}</div><div class="mole-score">得分：<span id="moleScore">0</span></div></div>'

# ---------- 组件 4：投篮分类 ----------
def basket_sort(words, categories, title="投篮分类"):
    """投篮分类：把词拖入正确分类框。words=[(word, cat), ...], categories=[cat,...]"""
    baskets = "".join(f'<div class="basket" data-cat="{c}" ondrop="dropBasket(event)" ondragover="allowDrop(event)">{c}</div>' for c in categories)
    balls = "".join(f'<div class="ball" draggable="true" data-cat="{c}" ondragstart="dragBall(event)">{w}</div>' for w, c in words)
    return f'<div class="component basket-sort"><h3>{title}</h3><div class="basket-row">{baskets}</div><div class="ball-row">{balls}</div></div>'

# ---------- 组件 5：转盘 ----------
def wheel_spin(items, title="幸运转盘"):
    """转盘：点击旋转，随机停在一个词上。items=[label, ...]"""
    segs = "".join(f'<div class="wheel-seg">{it}</div>' for it in items)
    return f'<div class="component wheel"><h3>{title}</h3><div class="wheel-circle" onclick="spinWheel(event)">{segs}</div><div class="wheel-result" id="wheelResult"></div></div>'

# ---------- 组件 6：消消乐 ----------
def match_eliminate(pairs, title="消消乐"):
    """消消乐：中英配对消除。pairs=[(en, cn), ...]"""
    items = []
    for en, cn in pairs:
        items.append(f'<div class="match-item" data-pair="{en}" onclick="matchClick(event)">{en}</div>')
        items.append(f'<div class="match-item" data-pair="{en}" onclick="matchClick(event)">{cn}</div>')
    return f'<div class="component match-elim"><h3>{title}</h3><div class="match-grid">{"".join(items)}</div></div>'

# ---------- 组件 7：投票 ----------
def vote(question, options, title="投票表决"):
    """投票：选择并显示统计。options=[label, ...]"""
    opts = "".join(f'<button class="vote-opt" onclick="voteClick(event)">{o}</button>' for o in options)
    return f'<div class="component vote"><h3>{title}</h3><div class="q-stem">{question}</div><div class="vote-row">{opts}</div></div>'

# ---------- 组件 8：连线 ----------
def connect_lines(left, right, title="连线配对"):
    """连线：左列与右列配对。left=[label,...], right=[label,...]"""
    l = "".join(f'<div class="conn-left" data-idx="{i}" onclick="connClick(event)">{x}</div>' for i, x in enumerate(left))
    r = "".join(f'<div class="conn-right" data-idx="{i}" onclick="connClick(event)">{x}</div>' for i, x in enumerate(right))
    return f'<div class="component connect"><h3>{title}</h3><div class="conn-col">{l}</div><div class="conn-col">{r}</div></div>'

# ---------- 组件 9：闯关 ----------
def level_quest(levels, title="闯关挑战"):
    """闯关：逐关答题。levels=[{q, options, correct}, ...]"""
    lv = "".join(
        f'<div class="level" data-level="{i+1}"><div class="q-stem">{l["q"]}</div>'
        + "".join(f'<button class="quiz-opt" data-correct="{1 if o==l["correct"] else 0}" onclick="checkOpt(this)">{o}</button>' for o in l["options"])
        + '</div>'
        for i, l in enumerate(levels)
    )
    return f'<div class="component level-quest"><h3>{title}</h3>{lv}</div>'

# ---------- 组件 10：听音 ----------
def listen_choose(word, options, title="听音选词"):
    """听音：播放发音，选正确词。word=正确词, options=[干扰词,...]"""
    opts = "".join(f'<button class="quiz-opt" data-correct="{1 if o==word else 0}" onclick="checkOpt(this)">{o}</button>' for o in [word]+options)
    return f'<div class="component listen"><h3>{title}</h3><button class="listen-btn" onclick="playWord(event)">🔊 播放</button><div class="q-opts">{opts}</div></div>'

# ============================================================
# C3 决议第 5 条 · 第一批 3 个组件（GM-V02 / GM-G03 / GM-R06）
# 交付要求：独立 HTML/CSS/JS、离线、触屏替代、IndexedDB 事件、重置、无动画降级、引擎调用示例
# 交互 JS/CSS 集中在 COMPONENT3_JS / COMPONENT3_CSS，由 courseware_engine 统一注入；
# 本库只出 HTML 片段（各组件函数），demo 构建器提供引擎调用示例与离线验证。
# ============================================================

# ---------- C3 组件 1：GM-V02 主动提取提示梯 ----------
def hint_ladder(words, title="主动提取提示梯"):
    """GM-V02（扩展 07 T1-G/T1-H）：看中文，主动提取英文词。
    实现 08 规范 §13.3 正式版：无提示首次提取 → 三级提示 → 显示答案 → 遮盖再提取 → 迁移题。
    并区分 independent_correct / hinted_correct / revealed_then_correct（提示后答对不直接升级）。
    words 每项支持：
      (en, cn)                      基本
      (en, cn, chunk)               三级提示词块（含 ___ 占位，如 "some + ___"）
      (en, cn, chunk, semantic)     一级提示语义（如 "表示'某个不确定的地点'，常用于肯定句"）
      (en, cn, chunk, semantic, transfer)  迁移题句子（含 ___ 占位，如 "I need ___ you."）
    """
    def _esc(s):
        return str(s).replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;").replace("\n", " ")
    units = []
    for item in words:
        en, cn = item[0], item[1]
        chunk = item[2] if len(item) >= 3 else ""
        semantic = item[3] if len(item) >= 4 else ""
        transfer = item[4] if len(item) >= 5 else ""
        transfer_view = transfer.replace("___", "________") if transfer else "请用该词填空"
        units.append(
            '<div class="hl-word" data-en="%s" data-chunk="%s" data-semantic="%s" data-transfer="%s" '
            'data-hint="0" data-revealed="0" data-state="initial">'
            '<div class="hl-cn">%s</div>'
            '<div class="hl-box">______</div>'
            '<div class="hl-input-row">'
            '<input class="hl-input" type="text" placeholder="输入英文" autocomplete="off" '
            'onfocus="var u=this.closest(\'.hl-word\');if(!u._startTime)u._startTime=Date.now();" '
            'onkeydown="if(event.key===\'Enter\'){event.preventDefault();hlCheck(this);}">'
            '<button class="hl-check" onclick="event.stopPropagation();hlCheck(this)">提交</button>'
            '</div>'
            '<div class="hl-btns">'
            '<button onclick="event.stopPropagation();hlHint(this)">① 提示</button>'
            '<button onclick="event.stopPropagation();hlReveal(this)">查看答案</button>'
            '</div>'
            '<div class="hl-note"></div>'
            '<div class="hl-retry" style="display:none">'
            '<div class="hl-retry-msg">答案已隐藏，请凭记忆重新拼写：</div>'
            '<div class="hl-input-row">'
            '<input class="hl-input hl-retry-input" type="text" placeholder="重新输入" autocomplete="off" '
            'onkeydown="if(event.key===\'Enter\'){event.preventDefault();hlRetryCheck(this);}">'
            '<button class="hl-check" onclick="event.stopPropagation();hlRetryCheck(this)">确认</button>'
            '</div>'
            '</div>'
            '<div class="hl-transfer" style="display:none">'
            '<div class="hl-transfer-sent">迁移句：%s</div>'
            '<div class="hl-input-row">'
            '<input class="hl-input hl-transfer-input" type="text" placeholder="填入单词" autocomplete="off" '
            'onkeydown="if(event.key===\'Enter\'){event.preventDefault();hlTransferCheck(this);}">'
            '<button class="hl-check" onclick="event.stopPropagation();hlTransferCheck(this)">确认迁移</button>'
            '</div>'
            '</div>'
            '<button class="hl-reset" onclick="event.stopPropagation();hlReset(this)">重置</button>'
            '</div>' % (_esc(en), _esc(chunk), _esc(semantic), _esc(transfer), _esc(cn), _esc(transfer_view))
        )
    return ('<div class="component hint-ladder"><h3>%s</h3><div class="hl-grid">%s</div>'
            '<div class="hl-tip">先想中文对应的英文并输入；错再逐级提示，尽量少用提示。'
            '答案显示后会遮盖，请凭记忆再拼一次。</div>'
            '<div class="hl-log" style="display:none"></div></div>'
            % (title, "".join(units)))

# ---------- C3 组件 2：GM-G03 错句医生 ----------
def sentence_doctor(sentences, title="错句医生"):
    """GM-G03（完全重叠 07 T2-H）：点出句中错词（点错位），再选正确改法（修复）。
    sentences=[(错句, 正确词), ...]；错句里带错误的词用 <w>包裹，如 "He <w>don't</w> like apples."。"""
    units = []
    for i, (sent, fix) in enumerate(sentences):
        parts = sent.split("<w>")
        if len(parts) == 1:
            html = sent  # 无标记则整句作为可点目标
        else:
            head, tail = parts[0], parts[1]
            bad, rest = tail.split("</w>", 1)
            html = (head + '<span class="sd-w" data-w="%s" onclick="event.stopPropagation();sdPick(this)">%s</span>' % (bad, bad)) + rest
        units.append(
            '<div class="sd-unit" data-ans="%s">'
            '<div class="sd-sentence">%s</div>'
            '<div class="sd-fix">'
            '<div class="sd-q">错误的词该改成？</div>'
            '<button class="sd-opt" data-correct="1" onclick="event.stopPropagation();sdFix(this)">%s</button>'
            '<button class="sd-opt" data-correct="0" onclick="event.stopPropagation();sdFix(this)">%s</button>'
            '<button class="sd-opt" data-correct="0" onclick="event.stopPropagation();sdFix(this)">%s</button>'
            '</div>'
            '<button class="hl-reset" onclick="event.stopPropagation();sdReset(this)">重置</button>'
            '</div>' % (fix, html, fix, _bad_fix(bad, fix), _bad_fix(bad, fix, 2))
        )
    return ('<div class="component sentence-doctor"><h3>%s</h3><div class="sd-list">%s</div>'
            '<div class="hl-tip">先点出错词（点错位），再从改法里选正确项。</div></div>'
            % (title, "".join(units)))

def _bad_fix(bad, fix, variant=1):
    """为错句医生生成 2 个干扰改法（不同于正确答案与错词本身）。"""
    cands = [bad, "not", "is", "are", "does", "do", "am", "was", "to " + fix, fix + "s", fix + "ed"]
    for c in cands:
        if c != fix and c != bad and c.strip():
            if variant == 1:
                return c
            variant -= 1
    return "don't" if fix != "don't" else "doesn't"

# ---------- C3 组件 3：GM-R06 证据连线 ----------
def evidence_connect(pairs, title="证据连线"):
    """GM-R06（新增）：题目↔原文证据句连线；触屏改点击两点（先点题目再点证据）。"""
    left = "".join(
        '<div class="ec-q" data-ev="E%d" onclick="event.stopPropagation();ecClick(this)">%s</div>' % (i + 1, q)
        for i, (q, ev) in enumerate(pairs)
    )
    right = "".join(
        '<div class="ec-ev" data-id="E%d" onclick="event.stopPropagation();ecClick(this)">%s</div>' % (i + 1, ev)
        for i, (q, ev) in enumerate(pairs)
    )
    return ('<div class="component evidence-connect"><h3>%s</h3>'
            '<div class="ec-grid"><div class="ec-left">%s</div><div class="ec-right">%s</div></div>'
            '<div class="ec-status"></div>'
            '<button class="hl-reset" onclick="event.stopPropagation();ecReset(this)">重置</button></div>'
            % (title, left, right))

# ---------- 三组件 JS（courseware_engine 注入，离线可用；无动画依赖，降级安全） ----------
COMPONENT3_JS = r"""
/* ===== GM-V02 主动提取提示梯（08 规范 §13.3 正式版） =====
 * 状态机：initial(无提示首次提取) → hint0 → hint1/2/3(三级提示) → revealed(显示答案)
 *         → 遮盖后再次提取(hl-retry) → 迁移题(hl-transfer) → done
 * 判定：independent_correct(无提示独立) vs hinted_correct(提示后) vs revealed_then_correct(显示答案后遮盖重拼)
 * 提示后答对不直接升级；显示答案后答对只算即时修正，不算跨日掌握。 */
function hlNorm(s){ return (s||'').trim().toLowerCase().replace(/[^a-z]/g,''); }
function hlOk(input, target){ return hlNorm(input)===hlNorm(target); }
function hlElapsed(unit){ return unit._startTime ? (Date.now()-unit._startTime) : 0; }

function hlHint(btn){
  var unit=btn.closest('.hl-word'), state=unit.getAttribute('data-state');
  if(state==='done'||state==='initial') return;
  var h=parseInt(unit.getAttribute('data-hint'),10), box=unit.querySelector('.hl-box');
  var en=unit.getAttribute('data-en'), note=unit.querySelector('.hl-note');
  if(h<1){ // 一级：语义/语境（不直接给字母）
    unit.setAttribute('data-hint','1'); unit.setAttribute('data-state','hint1');
    var sem=unit.getAttribute('data-semantic');
    box.textContent='提示1：'+(sem||'想想它的语义和常用搭配。');
    note.textContent='提示1（语义）——方向对了吗？现在再回忆完整单词。';
  } else if(h<2){ // 二级：首字母+长度
    unit.setAttribute('data-hint','2'); unit.setAttribute('data-state','hint2');
    box.textContent='提示2：首字母 '+en.charAt(0)+'，共 '+en.length+' 个字母。';
    note.textContent='提示2（首字母+长度）——已经有首字母线索，请尽量自己完成。';
  } else if(h<3){ // 三级：词块/部分形式
    unit.setAttribute('data-hint','3'); unit.setAttribute('data-state','hint3');
    var chunk=unit.getAttribute('data-chunk');
    box.textContent='提示3：'+(chunk||(en.charAt(0)+en.charAt(1)+'___'));
    note.textContent='提示3（词块/部分形式）已用。请尽量自己完成。';
  }
}
function hlCheck(btn){
  var unit=btn.closest('.hl-word'), input=unit.querySelector('.hl-input');
  var en=unit.getAttribute('data-en'), val=input.value, state=unit.getAttribute('data-state');
  if(!val.trim()){ unit.querySelector('.hl-note').textContent='请先输入英文。'; return; }
  if(state==='hint0'){ unit.querySelector('.hl-note').textContent='先点①提示获得线索，再输入。'; return; }
  if(state==='initial'){
    unit._firstAnswer=val; unit._firstCorrect=hlOk(val,en); unit._attempt=1;
    if(unit._firstCorrect){
      unit._independent=true; unit.setAttribute('data-state','done');
      input.classList.add('correct');
      unit.querySelector('.hl-box').textContent=en; unit.querySelector('.hl-box').classList.add('hl-done');
      unit.querySelector('.hl-note').textContent='提取正确！把它放进新句子试一次。';
      if(typeof playCorrect==='function') playCorrect();
      hlShowTransfer(unit);
    } else {
      unit._independent=false; input.classList.add('wrong');
      unit.querySelector('.hl-note').textContent='还没提取出来。看一个提示，再试一次。';
      if(typeof playError==='function') playError();
      unit.setAttribute('data-state','hint0');
    }
    hlLogEvent(unit); return;
  }
  if(state==='hint1'||state==='hint2'||state==='hint3'){
    unit._finalAnswer=val; unit._finalCorrect=hlOk(val,en);
    if(unit._finalCorrect){
      unit.setAttribute('data-state','done'); input.classList.add('correct');
      unit.querySelector('.hl-box').textContent=en; unit.querySelector('.hl-box').classList.add('hl-done');
      unit.querySelector('.hl-note').textContent=(state==='hint1')
        ? '方向对了吗？现在再回忆完整单词。'
        : '这次已经修正。它会在后面再次出现，确认是否真正记住。';
      if(typeof playCorrect==='function') playCorrect();
      hlShowTransfer(unit);
    } else {
      unit._finalCorrect=false;
      unit.querySelector('.hl-note').textContent='还没有。再走一步提示，或直接看答案。';
      if(typeof playError==='function') playError();
      var h=parseInt(unit.getAttribute('data-hint'),10);
      if(h>=3){ hlRevealFromHint(unit); }
      else { unit.setAttribute('data-state','hint'+(h+1)); }
    }
    hlLogEvent(unit);
  }
}
function hlReveal(btn){
  var unit=btn.closest('.hl-word'); hlRevealFromHint(unit);
}
function hlRevealFromHint(unit){
  if(unit.getAttribute('data-revealed')==='1') return;
  unit.setAttribute('data-revealed','1'); unit.setAttribute('data-state','revealed');
  var en=unit.getAttribute('data-en'), box=unit.querySelector('.hl-box');
  box.textContent=en+'  '+(unit.getAttribute('data-chunk')||'');
  box.classList.add('hl-done');
  unit.querySelector('.hl-note').textContent='先看清词形。稍后答案会隐藏，你需要重新拼写。';
  unit._revealed=true;
  setTimeout(function(){ // 3.5 秒后遮盖，进入遮盖再提取
    box.textContent='______'; box.classList.remove('hl-done');
    var retry=unit.querySelector('.hl-retry');
    if(retry){ retry.style.display='block'; unit.querySelector('.hl-note').textContent='答案已隐藏，请凭记忆重新拼写。'; }
    var ri=unit.querySelector('.hl-retry-input'); if(ri) ri.focus();
  }, 3500);
  hlLogEvent(unit);
}
function hlRetryCheck(btn){
  var unit=btn.closest('.hl-word'), en=unit.getAttribute('data-en');
  var val=unit.querySelector('.hl-retry-input').value;
  if(!val.trim()) return;
  if(hlOk(val,en)){
    unit._postRetrieval='correct';
    unit.querySelector('.hl-note').textContent='这次已经修正。它会在后面再次出现，确认是否真正记住。';
    if(typeof playCorrect==='function') playCorrect();
    unit.querySelector('.hl-retry').style.display='none';
    hlShowTransfer(unit);
  } else {
    unit._postRetrieval='wrong';
    unit.querySelector('.hl-note').textContent='遮盖后仍没拼对。这个词已加入复习池，稍后重点复习。';
    if(typeof playError==='function') playError();
    unit.querySelector('.hl-box').textContent=en; unit.querySelector('.hl-box').classList.add('hl-done');
  }
  hlLogEvent(unit);
}
function hlShowTransfer(unit){
  var tr=unit.querySelector('.hl-transfer');
  if(!tr) return;
  unit.setAttribute('data-state','transfer');
  tr.style.display='block';
  var ti=unit.querySelector('.hl-transfer-input'); if(ti) ti.focus();
}
function hlTransferCheck(btn){
  var unit=btn.closest('.hl-word'), en=unit.getAttribute('data-en');
  var val=unit.querySelector('.hl-transfer-input').value;
  if(!val.trim()) return;
  unit.setAttribute('data-state','done');
  if(hlOk(val,en)){
    unit._transfer='correct';
    unit.querySelector('.hl-note').textContent='迁移正确！这个词已掌握。';
    if(typeof playCorrect==='function') playCorrect();
  } else {
    unit._transfer='wrong';
    unit.querySelector('.hl-note').textContent='词形记住了，但新语境还不稳定。已加入复习池。';
    if(typeof playError==='function') playError();
  }
  hlLogEvent(unit);
}
function hlReset(btn){
  var unit=btn.closest('.hl-word');
  unit.setAttribute('data-state','initial'); unit.setAttribute('data-hint','0'); unit.setAttribute('data-revealed','0');
  delete unit._firstAnswer; delete unit._firstCorrect; delete unit._finalAnswer; delete unit._finalCorrect;
  delete unit._independent; delete unit._revealed; delete unit._postRetrieval; delete unit._transfer; delete unit._attempt; delete unit._startTime;
  var box=unit.querySelector('.hl-box'); box.textContent='______'; box.classList.remove('hl-done');
  var note=unit.querySelector('.hl-note'); if(note) note.textContent='';
  var inputs=unit.querySelectorAll('.hl-input'); for(var i=0;i<inputs.length;i++){ inputs[i].value=''; inputs[i].classList.remove('correct','wrong'); }
  var retry=unit.querySelector('.hl-retry'); if(retry) retry.style.display='none';
  var tr=unit.querySelector('.hl-transfer'); if(tr) tr.style.display='none';
}
/* GM-V02 事件记录：完整事件统一写入 EnglishCoursewareDB/answerRecords（P0-2 取消 GMEventsDB），同时调用底座 saveAnswer 存基础记录 */
/* P0-2 统一存储：完整事件写入底座库 answerRecords，不再另建互不导出的 GMEventsDB。
   若底座 db 尚未就绪，则自行打开同一库（结构定义与底座一致）兜底写入。 */
function writeFullEvent(ev){
  if(!window.indexedDB) return;
  if(window.db && db.objectStoreNames.contains(STORE_NAME)){
    var tx=db.transaction([STORE_NAME],'readwrite'); tx.objectStore(STORE_NAME).put(ev);
    return;
  }
  var req=indexedDB.open(DB_NAME, DB_VERSION);
  req.onupgradeneeded=function(e){ var d=e.target.result; if(!d.objectStoreNames.contains(STORE_NAME)){ var st=d.createObjectStore(STORE_NAME,{keyPath:'event_id'}); st.createIndex('student_id','student_id',{unique:false}); st.createIndex('question_id','question_id',{unique:false}); st.createIndex('session_id','session_id',{unique:false}); } };
  req.onsuccess=function(e){ var d=e.target.result; var tx=d.transaction([STORE_NAME],'readwrite'); tx.objectStore(STORE_NAME).put(ev); };
}
function hlLogEvent(unit){
  var en=unit.getAttribute('data-en');
  var sid=(typeof studentId!=='undefined')?studentId:'stu';
  var sess=(typeof sessionId!=='undefined')?sessionId:'SESSION';
  var ev={
    event_id: sid+'_'+sess+'_CMP_V02_'+en+'_'+(unit._attempt||1),
    student_id: sid, session_id: sess, question_id: 'CMP_V02_'+en, knowledge_id: 'VOC_'+en,
    first_answer: unit._firstAnswer||'', final_answer: unit._finalAnswer||unit._firstAnswer||'',
    is_first_correct: !!unit._firstCorrect, is_final_correct: !!unit._finalCorrect,
    independent_correct: !!unit._independent, attempt_no: unit._attempt||1,
    hint_used: (parseInt(unit.getAttribute('data-hint'),10)||0)>0,
    max_hint_level: parseInt(unit.getAttribute('data-hint'),10)||0,
    answer_revealed: unit.getAttribute('data-revealed')==='1',
    post_reveal_retrieval: unit._postRetrieval||'', response_time_ms: hlElapsed(unit),
    transfer_correct: unit._transfer||'', sync_status:'pending', timestamp:new Date().toISOString()
  };
  writeFullEvent(ev);
  if(typeof saveAnswer==='function'){
    saveAnswer(ev.question_id, ev.final_answer||ev.first_answer, en,
               ev.is_final_correct||ev.is_first_correct, ev.attempt_no, 0, ev.hint_used);
  }
  var log=document.querySelector('.hl-log');
  if(log){ log.style.display='block'; log.textContent=JSON.stringify(ev); }
}
/* ===== GM-G03 错句医生 ===== */
function sdPick(span){
  var unit=span.closest('.sd-unit'); if(unit.getAttribute('data-picked')) return;
  unit.setAttribute('data-picked', span.getAttribute('data-w')||span.textContent.trim());
  span.classList.add('sd-picked');
  var fix=unit.querySelector('.sd-fix'); if(fix) fix.style.display='block';
}
function sdFix(btn){
  var unit=btn.closest('.sd-unit'); if(unit.getAttribute('data-fixed')) return;
  unit.setAttribute('data-fixed','1');
  var ok=btn.getAttribute('data-correct')==='1';
  var opts=unit.querySelectorAll('.sd-opt');
  for(var i=0;i<opts.length;i++){ opts[i].disabled=true; }
  if(ok){ btn.classList.add('sd-ok'); if(typeof playCorrect==='function') playCorrect(); }
  else{
    btn.classList.add('sd-no'); if(typeof playError==='function') playError();
    for(var i=0;i<opts.length;i++){ if(opts[i].getAttribute('data-correct')==='1') opts[i].classList.add('sd-ok'); }
  }
  if(typeof saveAnswer==='function') saveAnswer('CMP_G03_'+unit.getAttribute('data-picked'),
    btn.textContent.trim(), unit.getAttribute('data-ans'), ok, 1, 0, false);
}
function sdReset(btn){
  var unit=btn.closest('.sd-unit');
  unit.removeAttribute('data-picked'); unit.removeAttribute('data-fixed');
  var w=unit.querySelectorAll('.sd-w'); for(var i=0;i<w.length;i++) w[i].classList.remove('sd-picked');
  var o=unit.querySelectorAll('.sd-opt'); for(var i=0;i<o.length;i++){ o[i].disabled=false; o[i].classList.remove('sd-ok','sd-no'); }
  var f=unit.querySelector('.sd-fix'); if(f) f.style.display='none';
}
/* ===== GM-R06 证据连线 ===== */
var ecSel=null;
function ecClick(el){
  var box=el.closest('.evidence-connect'); if(box.getAttribute('data-done')) return;
  if(el.classList.contains('ec-q')){
    if(ecSel) ecSel.classList.remove('ec-sel');
    ecSel=el; el.classList.add('ec-sel');
  } else if(el.classList.contains('ec-ev')){
    if(!ecSel){ el.classList.add('ec-warn'); setTimeout(function(){ el.classList.remove('ec-warn'); },500); return; }
    var q=ecSel; ecSel=null; q.classList.remove('ec-sel');
    var evId=el.getAttribute('data-id');
    if(q.getAttribute('data-ev')===evId){
      q.classList.add('ec-ok'); el.classList.add('ec-ok');
      if(typeof playCorrect==='function') playCorrect();
      var label=q.textContent.replace(/\s+/g,' ').trim().slice(0,18);
      if(typeof saveAnswer==='function') saveAnswer('CMP_R06_'+label, evId, evId, true, 1, 0, false);
    } else {
      q.classList.add('ec-no'); el.classList.add('ec-no');
      setTimeout(function(){ q.classList.remove('ec-no'); el.classList.remove('ec-no'); }, 600);
      if(typeof playError==='function') playError();
    }
    var qs=box.querySelectorAll('.ec-q'), done=true;
    for(var i=0;i<qs.length;i++){ if(!qs[i].classList.contains('ec-ok')) done=false; }
    if(done){ box.setAttribute('data-done','1'); var st=box.querySelector('.ec-status'); if(st) st.textContent='全部连线正确 ✓'; }
  }
}
function ecReset(btn){
  var box=btn.closest('.evidence-connect');
  var qs=box.querySelectorAll('.ec-q'), evs=box.querySelectorAll('.ec-ev');
  for(var i=0;i<qs.length;i++){ qs[i].classList.remove('ec-ok','ec-no','ec-sel'); }
  for(var i=0;i<evs.length;i++){ evs[i].classList.remove('ec-ok','ec-no'); }
  box.removeAttribute('data-done'); ecSel=null;
  var st=box.querySelector('.ec-status'); if(st) st.textContent='';
}
"""

# ---------- 三组件 CSS（courseware_engine 注入；触屏友好大按钮） ----------
COMPONENT3_CSS = """
.component.hint-ladder .hl-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;}
.hl-word{background:#fff;border:1px solid rgba(230,57,70,.18);border-radius:12px;padding:12px;text-align:center;display:flex;flex-direction:column;gap:8px;}
.hl-cn{font-size:22px;font-weight:700;color:var(--brand);}
.hl-box{font-size:18px;letter-spacing:1px;color:var(--text-primary);min-height:30px;line-height:1.5;}
.hl-box.hl-done{color:var(--correct);font-weight:700;}
.hl-input-row{display:flex;gap:6px;justify-content:center;align-items:center;}
.hl-input{flex:1;min-width:0;padding:8px 10px;border:2px solid #ddd;border-radius:8px;font-size:16px;text-align:center;}
.hl-input:focus{border-color:var(--brand);}
.hl-input.correct{border-color:var(--correct);background:var(--correct-row-bg);}
.hl-input.wrong{border-color:var(--error);background:var(--error-row-bg);}
.hl-check{padding:8px 14px;background:var(--accent);color:#333;border:none;border-radius:8px;font-size:15px;font-weight:600;white-space:nowrap;}
.hl-check:hover{background:var(--accent-light);}
.hl-btns{display:flex;gap:8px;justify-content:center;flex-wrap:wrap;}
.hl-btns button{background:#FFF3E0;color:#8B5E3C;border:1px solid #F5C6AA;border-radius:8px;padding:6px 12px;font-size:14px;}
.hl-btns button:hover{background:#FFE0B2;}
.hl-note{font-size:13px;color:var(--text-secondary);min-height:18px;line-height:1.4;}
.hl-retry{background:#FFF8F0;border:1px dashed #E0B08A;border-radius:8px;padding:8px;}
.hl-retry-msg{font-size:13px;color:#8B5E3C;margin-bottom:6px;}
.hl-transfer{background:rgba(59,130,246,.06);border:1px dashed #93C5FD;border-radius:8px;padding:8px;}
.hl-transfer-sent{font-size:14px;color:var(--sop-blue);margin-bottom:6px;line-height:1.5;}
.hl-reset{font-size:13px;color:#9C1F1F;background:none;border:1px dashed #D98B8B;border-radius:8px;padding:4px 12px;cursor:pointer;align-self:center;}
.hl-tip{font-size:13px;color:var(--text-secondary);margin-top:10px;}
.hl-log{font-size:11px;color:var(--text-secondary);background:#f5f5f5;border-radius:6px;padding:6px;margin-top:8px;word-break:break-all;max-height:80px;overflow:auto;}
.component.sentence-doctor .sd-list{display:flex;flex-direction:column;gap:16px;}
.sd-unit{background:#fff;border:1px solid rgba(230,57,70,.18);border-radius:12px;padding:14px;}
.sd-sentence{font-size:20px;line-height:1.7;margin-bottom:6px;}
.sd-w{display:inline-block;padding:0 2px;border-radius:4px;cursor:pointer;}
.sd-w.sd-picked{background:#FFE0B2;box-shadow:0 0 0 2px #FF9800;}
.sd-fix{display:none;background:#FFF8F0;border:1px dashed #E0B08A;border-radius:8px;padding:10px;margin:8px 0;}
.sd-q{font-size:15px;color:#8B5E3C;margin-bottom:6px;}
.sd-opt{display:inline-block;margin:4px 6px 0 0;background:#FFF3E0;color:#7B4A2B;border:1px solid #F5C6AA;border-radius:8px;padding:8px 14px;font-size:16px;}
.sd-opt.sd-ok{background:rgba(16,185,129,.18);border-color:#34D399;color:#0B7A5A;}
.sd-opt.sd-no{background:rgba(239,68,68,.15);border-color:#F87171;color:#C0392B;}
.component.evidence-connect .ec-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px;}
.ec-left,.ec-right{display:flex;flex-direction:column;gap:10px;}
.ec-q,.ec-ev{background:#fff;border:1px solid rgba(230,57,70,.18);border-radius:10px;padding:10px 12px;font-size:16px;cursor:pointer;}
.ec-q:hover,.ec-ev:hover{border-color:#FF9800;}
.ec-q.ec-sel{background:#FFF3E0;box-shadow:0 0 0 2px #FF9800;}
.ec-q.ec-ok,.ec-ev.ec-ok{background:rgba(16,185,129,.15);border-color:#34D399;color:#0B7A5A;}
.ec-q.ec-no,.ec-ev.ec-no{background:rgba(239,68,68,.15);border-color:#F87171;}
.ec-ev.ec-warn{background:#FFE0B2;border-color:#FF9800;}
.ec-status{font-size:16px;font-weight:700;color:var(--correct);margin-top:12px;min-height:22px;}
@media(max-width:768px){.component.evidence-connect .ec-grid{grid-template-columns:1fr;}}
"""

# ---------- 三组件引擎调用示例（build_lesson 内使用方式） ----------
def build_component_demo(out=None):
    """引擎调用示例 + 离线验证：用 courseware_core.build_courseware 组装 3 组件演示课件。
    正式课件在 build_lesson 里直接调用 hint_ladder()/sentence_doctor()/evidence_connect()
    即可（JS/CSS 已由 courseware_engine 注入），本 demo 供浏览器/离线人工测试。
    注意：demo 仅 3 页，不满足 verify_v2 的 40-45 页生产规则；组件本身以 node --check + 浏览器交互验收。"""
    import importlib.util
    core_path = os.path.join(HERE, "courseware_core.py")
    spec = importlib.util.spec_from_file_location("core", core_path)
    core = importlib.util.module_from_spec(spec); spec.loader.exec_module(core)
    pages = {}
    pages[1] = core.page(1, "GM-V02 · 主动提取提示梯", "输入提取 · 三级提示 · 遮盖重拼 · 迁移",
                         hint_ladder([("somewhere", "某个不确定的地点", "some + ___",
                                       "表示'某个不确定的地点'，常用于肯定句", "I need ___ you."),
                                      ("drink", "喝；饮料", "a glass of ___",
                                       "与'水'搭配，动词表示'喝'", "We ___ water every day."),
                                      ("apple", "苹果", "an ___ a day",
                                       "一种水果，常与'一天一个'搭配", "She eats an ___ every morning.")]))
    pages[2] = core.page(2, "GM-G03 · 错句医生", "点错位 · 选改法",
                         sentence_doctor([("He <w>don't</w> like apples.", "doesn't"),
                                          ("She <w>am</w> a teacher.", "is")]))
    pages[3] = core.page(3, "GM-R06 · 证据连线", "题目 ↔ 原文证据",
                         evidence_connect([("谁吃了蛋糕？", "Tom ate the cake."),
                                           ("谁在打篮球？", "Mike plays basketball."),
                                           ("几点吃早餐？", "We have breakfast at seven.")]))
    js = ("var totalPages=3; "
          "var segmentPages={1:[1,1],2:[2,2],3:[3,3],4:[1,3],5:[1,3],6:[1,3],7:[1,3],8:[1,3],9:[1,3]};\n"
          "initDB();\n" + COMPONENT3_JS)
    html = core.build_courseware(title="组件演示 · C3 第一批 3 组件", pages_dict=pages,
                                 js_extra=js, session="DEMO", n_pages=3,
                                 css_extra=COMPONENT3_CSS)
    out = out or os.path.join(HERE, "test_components.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(html)
    return out

# ---------- 白话映射表 ----------
NL_MAP = {
    "翻牌": "flip_cards",
    "翻牌记忆": "flip_cards",
    "快选": "quick_select",
    "快速选择": "quick_select",
    "打地鼠": "whack_a_mole",
    "投篮": "basket_sort",
    "投篮分类": "basket_sort",
    "转盘": "wheel_spin",
    "幸运转盘": "wheel_spin",
    "消消乐": "match_eliminate",
    "配对消除": "match_eliminate",
    "投票": "vote",
    "投票表决": "vote",
    "连线": "connect_lines",
    "连线配对": "connect_lines",
    "闯关": "level_quest",
    "闯关挑战": "level_quest",
    "听音": "listen_choose",
    "听音选词": "listen_choose",
    "提示梯": "hint_ladder",
    "主动提取": "hint_ladder",
    "错句医生": "sentence_doctor",
    "证据连线": "evidence_connect",
    "连线证据": "evidence_connect",
}

COMPONENTS = {
    "flip_cards": flip_cards,
    "quick_select": quick_select,
    "whack_a_mole": whack_a_mole,
    "basket_sort": basket_sort,
    "wheel_spin": wheel_spin,
    "match_eliminate": match_eliminate,
    "vote": vote,
    "connect_lines": connect_lines,
    "level_quest": level_quest,
    "listen_choose": listen_choose,
    "hint_ladder": hint_ladder,
    "sentence_doctor": sentence_doctor,
    "evidence_connect": evidence_connect,
}

def resolve(nl_desc):
    """白话描述 → 组件函数名"""
    for k, v in NL_MAP.items():
        if k in nl_desc:
            return v
    return None

if __name__ == "__main__":
    # 验收：10 组件 + 白话映射
    print(f"组件数：{len(COMPONENTS)}")
    print(f"白话映射条数：{len(NL_MAP)}")
    # 测试 resolve
    for desc in ["翻牌记忆", "投篮分类", "幸运转盘", "听音选词"]:
        print(f"  '{desc}' → {resolve(desc)}")
    # 保存 nl_map.json
    with open(os.path.join(HERE, "nl_map.json"), "w", encoding="utf-8") as f:
        json.dump(NL_MAP, f, ensure_ascii=False, indent=2)
    print("nl_map.json 已保存")
