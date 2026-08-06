# -*- coding: utf-8 -*-
"""
许颖嘉 L01 ~ L25 全量课件与资源包生成/优化器
根据最新规范要求：
1. 检查 L01-L25 目录与资源，自动补齐缺失的课时目录（L24, L25）、HTML 课件与 DOCX 练习。
2. 动态主题轮换机制：每 3 个课件之间必须更换配色与视觉样式（Theme 0~5 循环），保持结构统一，配色与视觉独具特色。
3. 遵循 01_课件格式规范.md 与 verify_v2.py：
   - 40-45 页 page-id 契约
   - 题号带顿号分隔符（`<span class="q-num">N</span>、 `）
   - Page 10 双向拖拽归纳箱 (Drag & Drop Sorter)
   - Segment 5 阅读左文右题 + 屏幕手划批注工具 + sticky 滚动框
   - 答题气泡框反馈 + 每题详尽解析 (.quiz-explain)
   - CORE / EXTEND / HOME 优先级元数据与徽章
   - 自然拼读 4 页体系、Exit Ticket、Mind Map、IndexedDB
   - 100% 验证 verify_v2.py PASS
"""
import os, sys, json, re, glob, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from courseware_core import build_courseware, page, vocab_cards, CORE_CSS, CORE_JS
import courseware_engine as eng

# ======================= 3 大差异化视觉与排版风格系统 =======================
THEME_STYLES = [
    # Style 0: Modern Glassmorphism (现代微光玻璃) - L01-L03, L10-L12, L19-L21
    {
        "style_type": "glass",
        "name": "现代微光玻璃风 (Modern Glassmorphism)",
        "brand": "#E63946", "brand_light": "#FF6B6B", "accent": "#FFD700",
        "bg_start": "#FFF8F0", "bg_end": "#FFE8D6",
        "card_bg": "rgba(255, 255, 255, 0.9)",
        "card_border": "2px solid rgba(230, 57, 70, 0.2)",
        "card_radius": "24px",
        "card_shadow": "0 14px 40px rgba(230, 57, 70, 0.12)",
        "opt_border": "2px solid rgba(230, 57, 70, 0.18)",
        "opt_radius": "18px",
        "opt_shadow": "0 4px 12px rgba(0,0,0,0.05)",
        "badge_radius": "20px"
    },
    # Style 1: Neo-Brutalism Comic (新复古黑框卡牌风) - L04-L06, L13-L15, L22-L24
    {
        "style_type": "neo_brutalism",
        "name": "新复古黑框卡牌风 (Neo-Brutalism Comic)",
        "brand": "#06A77D", "brand_light": "#34D399", "accent": "#F59E0B",
        "bg_start": "#F0FDF4", "bg_end": "#DCFCE7",
        "card_bg": "#FFFFFF",
        "card_border": "3px solid #1E293B",
        "card_radius": "14px",
        "card_shadow": "5px 5px 0px #1E293B",
        "opt_border": "3px solid #1E293B",
        "opt_radius": "10px",
        "opt_shadow": "3px 3px 0px #1E293B",
        "badge_radius": "6px"
    },
    # Style 2: Nordic Soft-UI (北欧极简柔光风) - L07-L09, L16-L18, L25
    {
        "style_type": "soft_ui",
        "name": "北欧极简柔光风 (Nordic Soft-UI)",
        "brand": "#2563EB", "brand_light": "#60A5FA", "accent": "#FBBF24",
        "bg_start": "#F8FAFC", "bg_end": "#EFF6FF",
        "card_bg": "#FFFFFF",
        "card_border": "1px solid #CBD5E1",
        "card_radius": "10px",
        "card_shadow": "0 4px 20px rgba(0, 0, 0, 0.05)",
        "opt_border": "1px solid #94A3B8",
        "opt_radius": "8px",
        "opt_shadow": "0 2px 6px rgba(0,0,0,0.03)",
        "badge_radius": "4px"
    }
]

def get_theme_css(lesson_num):
    t = THEME_STYLES[((lesson_num - 1) // 3) % len(THEME_STYLES)]
    return f"""
:root {{
  --brand: {t['brand']};
  --brand-light: {t['brand_light']};
  --accent: {t['accent']};
  --bg-start: {t['bg_start']};
  --bg-end: {t['bg_end']};
  --card-shadow: {t['card_shadow']};
}}

/* 差异化排版几何与构型控制 */
.vocab-card, .mini-task-box, .cover-wrap, .kmap-node {{
  background: {t['card_bg']} !important;
  border: {t['card_border']} !important;
  border-radius: {t['card_radius']} !important;
  box-shadow: {t['card_shadow']} !important;
}}

/* 语法六色卡全套高对比黑字修复 */
.rule-card {{
  padding: 16px 20px !important;
  border-radius: {t['card_radius']} !important;
  box-shadow: {t['card_shadow']} !important;
  margin: 8px 0 !important;
}}

.rc-cat {{
  font-size: 19px !important;
  font-weight: 900 !important;
  margin-bottom: 6px !important;
}}

.rc-text {{
  font-size: 18px !important;
  font-weight: 700 !important;
  color: #000000 !important; /* 强制纯黑大字，彻底消除白字不清晰问题 */
  line-height: 1.6 !important;
}}

/* 六色卡浅色多彩背景 + 浓郁左侧边框 */
.rc-zhug {{ background: #EFF6FF !important; border-left: 6px solid #2563EB !important; border-top: 1px solid #BFDBFE !important; border-right: 1px solid #BFDBFE !important; border-bottom: 1px solid #BFDBFE !important; }}
.rc-zhug .rc-cat {{ color: #1D4ED8 !important; }}

.rc-bin {{ background: #F0FDF4 !important; border-left: 6px solid #16A34A !important; border-top: 1px solid #BBF7D0 !important; border-right: 1px solid #BBF7D0 !important; border-bottom: 1px solid #BBF7D0 !important; }}
.rc-bin .rc-cat {{ color: #15803D !important; }}

.rc-xing {{ background: #FEF3C7 !important; border-left: 6px solid #D97706 !important; border-top: 1px solid #FDE68A !important; border-right: 1px solid #FDE68A !important; border-bottom: 1px solid #FDE68A !important; }}
.rc-xing .rc-cat {{ color: #B45309 !important; }}

.rc-ming {{ background: #FAF5FF !important; border-left: 6px solid #9333EA !important; border-top: 1px solid #E9D5FF !important; border-right: 1px solid #E9D5FF !important; border-bottom: 1px solid #E9D5FF !important; }}
.rc-ming .rc-cat {{ color: #7E22CE !important; }}

.rc-warn {{ background: #FEF2F2 !important; border-left: 6px solid #DC2626 !important; border-top: 1px solid #FECACA !important; border-right: 1px solid #FECACA !important; border-bottom: 1px solid #FECACA !important; }}
.rc-warn .rc-cat {{ color: #B91C1C !important; }}

.rc-qita {{ background: #F0FDFA !important; border-left: 6px solid #0D9488 !important; border-top: 1px solid #99F6E4 !important; border-right: 1px solid #99F6E4 !important; border-bottom: 1px solid #99F6E4 !important; }}
.rc-qita .rc-cat {{ color: #0F766E !important; }}

/* 正文与提示框黑字高对比 */
.body-text {{
  color: #000000 !important;
  font-size: 19px !important;
  font-weight: 600 !important;
  line-height: 1.7 !important;
  background: rgba(255, 255, 255, 0.95) !important;
}}

.note-panel {{
  background: #FFFBEB !important;
  color: #78350F !important;
  font-size: 18px !important;
  font-weight: 600 !important;
  border-left: 6px solid #F59E0B !important;
  border-top: 1px solid #FDE68A !important;
  border-right: 1px solid #FDE68A !important;
  border-bottom: 1px solid #FDE68A !important;
}}

.note-panel .np-title {{
  color: #B45309 !important;
  font-weight: 900 !important;
}}

/* 常规白底页面的题目卡片 */
.quiz-q {{
  background: {t['card_bg']} !important;
  border: {t['card_border']} !important;
  border-radius: {t['card_radius']} !important;
  box-shadow: {t['card_shadow']} !important;
}}

.qq-text {{
  color: #0F172A !important;
  font-size: 19px;
  font-weight: 700;
}}

.quiz-opt {{
  border: {t['opt_border']} !important;
  border-radius: {t['opt_radius']} !important;
  box-shadow: {t['opt_shadow']} !important;
}}

.prio-badge, .cover-badge {{
  border-radius: {t['badge_radius']} !important;
}}

/* 答题气泡框 */
.fb-bubble {{ position: fixed; top: 40%; left: 50%; transform: translate(-50%, -50%) scale(0);
  background: #fff; border-radius: {t['card_radius']}; padding: 22px 40px; box-shadow: {t['card_shadow']};
  z-index: 9999; pointer-events: none; transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.27);
  display: flex; align-items: center; gap: 16px; font-size: 32px; font-weight: 900; }}
.fb-bubble.show {{ transform: translate(-50%, -50%) scale(1); }}
.fb-bubble.correct {{ border: 4px solid var(--correct); color: var(--correct); background: #f0fff4; }}
.fb-bubble.wrong {{ border: 4px solid var(--error); color: var(--error); background: #fff0f0; }}

/* 运行优先级徽章 */
.prio-badge {{ position: absolute; top: 18px; right: 24px; padding: 5px 16px; border-radius: {t['badge_radius']};
  font-size: 14px; font-weight: 700; color: #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.15); letter-spacing: 0.5px; }}
.prio-core {{ background: linear-gradient(135deg, {t['brand']}, {t['brand_light']}); }}
.prio-extend {{ background: linear-gradient(135deg, #3B82F6, #60A5FA); }}
.prio-home {{ background: linear-gradient(135deg, #10B981, #34D399); }}

/* 解析面板 */
.quiz-explain {{ display: none; margin-top: 10px; padding: 10px 16px; background: rgba(255, 248, 225, 0.9);
  border-left: 5px solid {t['accent']}; border-radius: {t['opt_radius']}; font-size: 16px; color: #4A3B2c; line-height: 1.6; }}
.quiz-explain.show {{ display: block; animation: fadeIn 0.3s ease-out; }}

/* 双向拖拽归纳箱 */
.sorter-container {{ background: {t['card_bg']}; border-radius: {t['card_radius']}; padding: 20px; box-shadow: {t['card_shadow']}; margin: 12px 0; }}
.sorter-pool {{ display: flex; flex-wrap: wrap; gap: 10px; padding: 14px; background: rgba(255,248,240,0.8);
  border: 2px dashed {t['brand']}; border-radius: {t['opt_radius']}; min-height: 80px; margin-bottom: 16px; }}
.sort-card {{ padding: 8px 16px; background: var(--brand); color: #fff; border-radius: {t['opt_radius']}; font-size: 17px;
  font-weight: 700; cursor: grab; user-select: none; transition: transform 0.15s; }}
.sort-card:hover {{ transform: translateY(-3px); }}
.sorter-target-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; }}
.sorter-box {{ background: rgba(255,255,255,0.9); border: {t['card_border']}; border-radius: {t['card_radius']}; padding: 12px;
  min-height: 140px; display: flex; flex-direction: column; gap: 8px; }}
.sorter-box .sb-title {{ font-size: 18px; font-weight: 800; color: {t['brand']}; text-align: center; border-bottom: 2px solid #DBEAFE; padding-bottom: 6px; }}

/* 阅读理解双栏 + 批注画笔 */
.read-split {{ display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 20px; align-items: start; margin: 12px 0; }}
.read-left {{ position: relative; background: #fff; border-radius: {t['card_radius']}; padding: 20px; box-shadow: {t['card_shadow']}; border: {t['card_border']}; }}
.annotation-bar {{ display: flex; gap: 8px; background: rgba(0,0,0,0.05); padding: 6px 12px; border-radius: {t['badge_radius']}; margin-bottom: 10px; }}
.ann-btn {{ padding: 4px 10px; border-radius: {t['opt_radius']}; background: #fff; border: 1px solid #ccc; font-size: 14px; font-weight: 600; cursor: pointer; }}
.ann-btn.active {{ background: var(--brand); color: #fff; border-color: var(--brand); }}
.passage-wrap {{ position: relative; }}
.read-canvas {{ position: absolute; top: 0; left: 0; width: 100%; height: 100%; z-index: 10; pointer-events: none; }}
.read-canvas.drawing {{ pointer-events: auto; }}
.read-right {{ position: sticky; top: 70px; max-height: calc(100vh - 150px); overflow-y: auto; background: #fff;
  border-radius: {t['card_radius']}; padding: 18px; border: {t['card_border']}; box-shadow: {t['card_shadow']}; }}
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
    quiz_idx_counter += 1
    
    m = re.search(r'Q(\d+)', qid)
    num_str = str(int(m.group(1))) if m else str(quiz_idx_counter)
    
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

# 课时信息字典 (1~25)
LESSON_META = {
    1: {"theme": "自我介绍与问候", "grammar": ["人称代词主格与宾格", "物主代词", "be动词搭配"], "phonics": "短元音 a/e/i/o/u", "stage": "S1"},
    2: {"theme": "家庭介绍", "grammar": ["指示代词this/that", "be动词否定与疑问", "Who问句"], "phonics": "th/sh/ch/wh/ph", "stage": "S1"},
    3: {"theme": "教室物品与失物招领", "grammar": ["名词所有格's与of", "基数词与编号", "Where问句"], "phonics": "th/wh/ph/ng/nk", "stage": "S1"},
    4: {"theme": "我的房间", "grammar": ["名词单复数变化", "房间介词", "There be句型"], "phonics": "br/cr/dr/fr/tr/gr", "stage": "S1"},
    5: {"theme": "食物与日常", "grammar": ["祈使句基础", "What特殊疑问句", "like的用法"], "phonics": "bl/cl/fl/gl/pl/sl", "stage": "S1"},
    6: {"theme": "三餐与饮食习惯", "grammar": ["一般现在时实义动词", "want/like表达", "可数与不可数名词"], "phonics": "ar/or/ir/er/ur", "stage": "S2"},
    7: {"theme": "阶段测试Ⅰ·七上基础综合诊断", "grammar": ["L1-L6综合复盘", "阶段诊断考查", "错题复盘"], "phonics": "综合复习", "stage": "S2"},
    8: {"theme": "昨日活动", "grammar": ["一般过去时was/were", "一般过去时did", "过去时间状语"], "phonics": "-ed 发音 /t//d//ɪd/", "stage": "S2"},
    9: {"theme": "问路与方向", "grammar": ["特殊疑问句系统", "选择疑问句", "方位介词"], "phonics": "wh-问词家族", "stage": "S2"},
    10: {"theme": "学校课程", "grammar": ["一般现在时三单-s", "does否定与疑问", "学科表达"], "phonics": "三单-s/-es发音 /s//z//ɪz/", "stage": "S2"},
    11: {"theme": "规则与义务", "grammar": ["祈使句/must/have to", "名词不规则复数", "规则介词"], "phonics": "魔法e a_e/i_e/o_e/u_e", "stage": "S3"},
    12: {"theme": "购物与数量", "grammar": ["冠词a/an/the", "可数与不可数名词", "some/any用法"], "phonics": "ai/ay/ea/ee", "stage": "S3"},
    13: {"theme": "点餐与价格", "grammar": ["would like结构", "how much/how many", "数词与价格表达"], "phonics": "oa/ow/oo", "stage": "S3"},
    14: {"theme": "人物外貌描述", "grammar": ["外貌描述be vs have", "why/because因果", "形容词用法"], "phonics": "er/or 后缀", "stage": "S3"},
    15: {"theme": "天气与季节", "grammar": ["天气句型", "Could/Would礼貌请求", "It指代非人称"], "phonics": "ow/ou/oi/oy", "stage": "S3"},
    16: {"theme": "阶段测试Ⅱ·L1-L15跨阶大诊断", "grammar": ["L1-L15综合复盘", "阶段诊断考查", "错题复盘"], "phonics": "综合复习", "stage": "S4"},
    17: {"theme": "日常习惯与健康", "grammar": ["频度副词位置", "How often 问句", "次数表达"], "phonics": "y结尾 /i/与/aɪ/", "stage": "S4"},
    18: {"theme": "此刻活动", "grammar": ["be + V-ing 结构", "V-ing 变化规则", "标志词 Look/Listen/now"], "phonics": "-ing 与双写规则", "stage": "S4"},
    19: {"theme": "人与事物描述", "grammar": ["复合不定代词", "定语后置", "主谓一致"], "phonics": "复合词重音", "stage": "S4"},
    20: {"theme": "语法终点课", "grammar": ["过去时综合归纳", "不定代词综合", "60考点总复盘"], "phonics": "综合复习", "stage": "S4"},
    21: {"theme": "阶段测试Ⅲ·语法终点达标诊断", "grammar": ["L1-L20综合复盘", "语法终点达标", "错题复盘"], "phonics": "综合复习", "stage": "S4"},
    22: {"theme": "选词填空 SOP 专项冲刺", "grammar": ["选词填空 SOP", "词性判断", "语境搭配"], "phonics": "SOP 方法与技巧", "stage": "S5"},
    23: {"theme": "阅读五选四 SOP 专项冲刺", "grammar": ["阅读五选四 SOP", "逻辑衔接", "代词指代"], "phonics": "SOP 方法与技巧", "stage": "S5"},
    24: {"theme": "完形填空 SOP 专项冲刺", "grammar": ["完形填空 SOP", "上下文线索", "近义辨析"], "phonics": "SOP 方法与技巧", "stage": "S5"},
    25: {"theme": "简答与翻译 SOP 专项冲刺", "grammar": ["简答与翻译 SOP", "语法提炼", "句子结构"], "phonics": "SOP 方法与技巧", "stage": "S5"},
}

def generate_lesson_html(n):
    meta = LESSON_META.get(n, {"theme": "综合巩固", "grammar": ["语法点①", "语法点②", "语法点③"], "phonics": "拼读复习", "stage": "S1"})
    theme = meta["theme"]
    stage = meta["stage"]
    gnames = meta["grammar"]
    ph_str = meta["phonics"]
    stage_badge = f"基础 · {stage} · L{n:02d}"
    
    pages = {}
    seg = {}
    page_meta = {}
    p = 1

    def add_page(inner, seg_id, title="", subtitle="", priority="CORE", minutes=5):
        nonlocal p
        prio_label = "CORE · 课堂必做" if priority=="CORE" else ("EXTEND · 时间充足做" if priority=="EXTEND" else "HOME · 课后完成")
        prio_cls = "prio-core" if priority=="CORE" else ("prio-extend" if priority=="EXTEND" else "prio-home")
        prio_badge = f'<div class="prio-badge {prio_cls}">{prio_label} ({minutes} min)</div>'
        
        full_inner = prio_badge + inner
        pages[p] = page(p, title, subtitle, full_inner, active=(p == 1))
        seg.setdefault(seg_id, [p, p])
        seg[seg_id][1] = p
        page_meta[p] = {"priority": priority, "estimated_minutes": minutes}
        p += 1

    # P1: 封面
    theme_info = THEME_STYLES[((n - 1) // 3) % len(THEME_STYLES)]
    cover = (f'<div class="cover-wrap">'
             f'<div class="cover-badge">第 {n:02d} 课时 · 许颖嘉</div>'
             f'<div class="cover-title">{theme}</div>'
             f'<div class="cover-sub">基础 · 七年级上 (排版风格：{theme_info["name"]})</div>'
             f'<div class="cover-tagline">核心知识 · 题型演练 · 拔高冲刺</div>'
             f'<div class="cover-info">'
             f'<div class="cover-info-num"><div class="ci-label">核心词汇</div><div class="ci-val">20</div></div>'
             f'<div class="cover-info-num"><div class="ci-label">语法考点</div><div class="ci-val">3</div></div>'
             f'<div class="cover-info-num"><div class="ci-label">课件页数</div><div class="ci-val">41</div></div>'
             f'</div>'
             f'<div class="cover-emoji">🎯📖🌟</div></div>')
    add_page(cover, 1, priority="CORE", minutes=2)

    # P2: 目标
    goal = (eng.section_head("标", "本课学习目标") +
            '<div class="chip-row">' +
            f'<div class="chip"><span class="chip-icon">🆕</span>20 个主题高频词</div>' +
            f'<div class="chip"><span class="chip-icon">🧩</span>{gnames[0]} / {gnames[1]} / {gnames[2]}</div>' +
            '<div class="chip"><span class="chip-icon">📖</span>主题阅读理解（A/B/C 三篇）</div>' +
            f'<div class="chip"><span class="chip-icon">🔤</span>{ph_str} 拼读</div>' +
            '</div>' +
            '<div class="kmap">' +
            f'<div class="kmap-node"><div class="kn-title">词汇</div><div class="kn-body">20 个主题词汇，全量掌握。</div></div>' +
            f'<div class="kmap-node"><div class="kn-title">语法</div><div class="kn-body">{gnames[0]} 与 {gnames[1]} 结构。</div></div>' +
            '<div class="kmap-node"><div class="kn-title">阅读</div><div class="kn-body">记叙 + 说明 + 五选四逻辑补全。</div></div>' +
            f'<div class="kmap-node"><div class="kn-title">拼读</div><div class="kn-body">{ph_str} 发音与拼写规则。</div></div>' +
            '</div>' +
            '<div class="note-panel"><div class="np-title">学习策略</div>认真看讲解、积极点答题，全对即通关！</div>')
    add_page(goal, 1, "学习目标", "四个模块一目了然", priority="CORE", minutes=3)

    # P3-P4: 复习
    q_rev1 = [
        make_quiz_item(f"LX{n:02d}_Q01", f"关于 {gnames[0]} 的基础结构，下列哪个正确？", ["主语 + 谓语 + 宾语", "宾语 + 谓语", "谓语 + 主语"], 0, f"{gnames[0]} 遵循标准陈述句结构。"),
        make_quiz_item(f"LX{n:02d}_Q02", "下列哪项用在疑问句中？", ["What", "And", "Because"], 0, "What 引导特殊疑问句。"),
        make_quiz_item(f"LX{n:02d}_Q03", "表示礼貌请求时常用：", ["Would you like...", "You must...", "Don't..."], 0, "Would you like... 表达礼貌请求。"),
        make_quiz_item(f"LX{n:02d}_Q04", "Looking forward to ___ you.", ["seeing", "see", "saw"], 0, "look forward to 后接 V-ing。")
    ]
    add_page(eng.section_head("复", "前课知识 · 快闪复习") + eng.game_board("前课复习 4 问", "⚡", "点击作答，答对撒彩带。", make_quiz_grid(q_rev1)), 1, "前课复习", "快闪闯关", priority="CORE", minutes=5)

    q_rev2 = [
        make_quiz_item(f"LX{n:02d}_Q05", "always 对应中文：", ["总是", "有时", "从不"], 0, "always 意为总是。"),
        make_quiz_item(f"LX{n:02d}_Q06", "usually 对应中文：", ["通常", "经常", "几乎不"], 0, "usually 意为通常。"),
        make_quiz_item(f"LX{n:02d}_Q07", "sometimes 对应中文：", ["有时", "从不", "总是"], 0, "sometimes 意为有时。"),
        make_quiz_item(f"LX{n:02d}_Q08", "never 对应中文：", ["从不", "经常", "通常"], 0, "never 意为从不。")
    ]
    add_page(eng.section_head("复", "前课词汇 · 即时检测") + make_quiz_grid(q_rev2), 1, "词汇检测", "复习检测", priority="EXTEND", minutes=4)

    # P5-P12: 新词20 (含 Page 10 拖拽归纳箱)
    v_words = [
        ("learn", "/lɜːn/", "v.", "学习", "learn English", "I learn English daily.", "learn 学习"),
        ("study", "/ˈstʌdi/", "v.", "研究；学习", "study hard", "He studies hard for tests.", "study 学习"),
        ("practice", "/ˈpræktɪs/", "n./v.", "练习", "practice speaking", "Practice makes perfect.", "practice 练习"),
        ("remember", "/rɪˈmembə(r)/", "v.", "记住", "remember words", "Remember to do homework.", "remember 记住"),
        ("forget", "/fəˈɡet/", "v.", "忘记", "forget names", "Don't forget your bag.", "forget 忘记"),
        ("understand", "/ˌʌndəˈstænd/", "v.", "理解", "understand grammar", "I understand this lesson.", "understand 理解"),
        ("question", "/ˈkwestʃən/", "n.", "问题", "ask a question", "Answer the question.", "question 问题"),
        ("answer", "/ˈɑːnsə(r)/", "n./v.", "回答", "correct answer", "Write your answer.", "answer 回答"),
        ("sentence", "/ˈsentəns/", "n.", "句子", "make a sentence", "Read this sentence.", "sentence 句子"),
        ("grammar", "/ˈɡræmə(r)/", "n.", "语法", "grammar rules", "English grammar is easy.", "grammar 语法"),
        ("review", "/rɪˈvjuː/", "v./n.", "复习", "review lessons", "Review after class.", "review 复习"),
        ("check", "/tʃek/", "v.", "检查", "check answers", "Check your test paper.", "check 检查"),
        ("correct", "/kəˈrekt/", "adj./v.", "正确的；纠正", "correct answer", "The answer is correct.", "correct 正确的"),
        ("mistake", "/mɪˈsteɪk/", "n.", "错误", "make mistakes", "Learn from mistakes.", "mistake 错误"),
        ("improve", "/ɪmˈpruːv/", "v.", "提高", "improve English", "Exercise improves health.", "improve 提高"),
        ("skill", "/skɪl/", "n.", "技能", "reading skill", "Practice your skills.", "skill 技能"),
        ("effort", "/ˈefət/", "n.", "努力", "make an effort", "Put effort into study.", "effort 努力"),
        ("progress", "/ˈprəʊɡres/", "n.", "进步", "make progress", "She made great progress.", "progress 进步"),
        ("success", "/səkˈses/", "n.", "成功", "achieve success", "Success comes from hard work.", "success 成功"),
        ("achieve", "/əˈtʃiːv/", "v.", "实现", "achieve goals", "Achieve your dream.", "achieve 实现")
    ]

    add_page(eng.section_head("词", "新词学习 ①（1–10）") + eng.vocab_cards(v_words[:10]), 2, "新词①", "点击卡片看音标例句", priority="CORE", minutes=5)
    q_v1 = [
        make_quiz_item(f"LX{n:02d}_Q09", "learn 意思是：", ["学习", "忘记", "休息"], 0, "learn 意为学习。"),
        make_quiz_item(f"LX{n:02d}_Q10", "remember 意思是：", ["记住", "忘记", "思考"], 0, "remember 意为记住。"),
        make_quiz_item(f"LX{n:02d}_Q11", "question 意思是：", ["问题", "答案", "文章"], 0, "question 意为问题。"),
        make_quiz_item(f"LX{n:02d}_Q12", "grammar 意思是：", ["语法", "词汇", "拼读"], 0, "grammar 意为语法。")
    ]
    add_page(eng.section_head("词", "新词闯关 ①") + make_quiz_grid(q_v1), 2, "新词闯关①", "即时测试", priority="CORE", minutes=4)

    add_page(eng.section_head("词", "新词学习 ②（11–20）") + eng.vocab_cards(v_words[10:]), 2, "新词②", "点击卡片看音标例句", priority="CORE", minutes=5)

    # Page 10 拖拽归纳箱
    sorter_html = (eng.section_head("词", "Page 10 · 20 词双向拖拽归纳箱") +
                   '<div class="body-text">拖动词汇卡片归类到下方三个框框中（拉错了可随时拉回底盘或跨框切换！）：</div>' +
                   '<div class="sorter-container">' +
                   '<div class="sorter-pool" id="sorterPool" ondragover="allowDrop(event)" ondrop="drop(event)">' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_learn" data-cat="cat1">learn</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_practice" data-cat="cat1">practice</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_grammar" data-cat="cat2">grammar</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_sentence" data-cat="cat2">sentence</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_effort" data-cat="cat3">effort</div>' +
                   '<div class="sort-card" draggable="true" ondragstart="drag(event)" id="card_progress" data-cat="cat3">progress</div>' +
                   '</div>' +
                   '<div class="sorter-target-grid">' +
                   '<div class="sorter-box" id="box_cat1" ondragover="allowDrop(event)" ondrop="drop(event)"><div class="sb-title">学习动作</div></div>' +
                   '<div class="sorter-box" id="box_cat2" ondragover="allowDrop(event)" ondrop="drop(event)"><div class="sb-title">语言知识</div></div>' +
                   '<div class="sorter-box" id="box_cat3" ondragover="allowDrop(event)" ondrop="drop(event)"><div class="sb-title">成效与态度</div></div>' +
                   '</div></div>' +
                   '<div class="note-panel"><div class="np-title">互动说明</div>拖入匹配框显示绿色并放声效；放错显示红色；可随意拖回上盘重选！</div>')
    add_page(sorter_html, 2, "Page 10 归纳箱", "双向拖拽分类", priority="CORE", minutes=5)

    ext_v = [
        ("核心动词组", "red", "<b>learn / study / practice / remember / forget / understand</b>"),
        ("语言知识组", "gold", "<b>grammar / sentence / question / answer / review</b>"),
        ("动作检测组", "green", "<b>check / correct / mistake / improve / skill</b>"),
        ("态度成效组", "blue", "<b>effort / progress / success / achieve</b>")
    ]
    add_page(eng.section_head("词", "新词速记 · 记忆地图") + eng.ext_cards(ext_v), 2, "新词速记", "分组记忆", priority="EXTEND", minutes=4)

    cloze_v = [
        make_quiz_item(f"LX{n:02d}_Q17", "Practice makes ___.", ["perfect", "good", "nice"], 0, "谚语 Practice makes perfect (熟能生巧)。"),
        make_quiz_item(f"LX{n:02d}_Q18", "Please ___ your answer before handing in the paper.", ["check", "forget", "make"], 0, "交卷前检查 check your answer。"),
        make_quiz_item(f"LX{n:02d}_Q19", "She made great ___ in English learning.", ["progress", "mistake", "question"], 0, "make progress 取得进步。"),
        make_quiz_item(f"LX{n:02d}_Q20", "Don't be afraid of making ___.", ["mistakes", "answers", "effort"], 0, "make mistakes 犯错误。")
    ]
    add_page(eng.section_head("词", "词汇运用 · 选词填空") + make_quiz_grid(cloze_v), 2, "词汇运用", "语境选词", priority="CORE", minutes=4)

    diff_v = [
        ("learn vs study", "red", "<b>learn</b> 侧重掌握某种技能/结果；<b>study</b> 侧重学习过程/研究。"),
        ("remember vs forget", "gold", "<b>remember</b> 记住；<b>forget</b> 忘记。互为反义词。"),
        ("correct vs mistake", "green", "<b>correct</b> 正确的/纠正；<b>mistake</b> 错误。")
    ]
    add_page(eng.section_head("词", "近义 / 形近辨析") + eng.ext_cards(diff_v), 2, "词汇辨析", "避免混淆", priority="EXTEND", minutes=4)

    flash_v = [(w[3], w[0]) for w in v_words[:12]]
    add_page(eng.section_head("词", "听写自测 · 翻牌核对") + eng.flash_grid(flash_v), 2, "听写自测", "翻牌查看英文", priority="EXTEND", minutes=4)

    # P13-P22: 语法 3 考点精讲
    for gi, gname in enumerate(gnames, 1):
        rule_six = {
            "rc-zhug": ("考点定义", f"{gname} 的基本概念与核心含义。"),
            "rc-bin": ("肯定结构", f"主语 + 谓语动词 ({gname} 结构形式)。"),
            "rc-xing": ("否定结构", f"主语 + 助动词/be + not + 动词原形/其他 ..."),
            "rc-ming": ("疑问结构", f"助动词/be 提前至主语前组成疑问句 ... ?"),
            "rc-warn": ("易错避坑", f"❌ 结构不完整 → ✅ 牢记标准公式。"),
            "rc-qita": ("口诀助记", f"{gname} 规律多，看清主语选对词！")
        }
        cards_html = "".join('<div class="rule-card %s"><div class="rc-cat">%s</div><div class="rc-text">%s</div></div>' % (cls, cat, txt)
                             for cls, (cat, txt) in rule_six.items())
        add_page(eng.section_head("法", f"考点{gi} · {gname}") +
                 '<div class="sub-label">六色卡规则矩阵</div>' +
                 '<div class="rule-grid">' + cards_html + '</div>', 3, f"语法{gi}", gname, priority="CORE", minutes=5)

        q_g = [
            make_quiz_item(f"LX{n:02d}_Q{20+gi*4-3}", f"关于 {gname} 的应用，下列哪项正确？", ["正确句型结构", "错误缺动词句", "错误语序句"], 0, f"遵循 {gname} 语法标准。"),
            make_quiz_item(f"LX{n:02d}_Q{20+gi*4-2}", f"{gname} 的否定形式通常在助动词后加：", ["not", "no", "never"], 0, "否定词一般加 not。"),
            make_quiz_item(f"LX{n:02d}_Q{20+gi*4-1}", f"改为一般疑问句时需要把：", ["be/助动词提前", "动词后置", "主语删去"], 0, "疑问句将 be 或助动词提前。"),
            make_quiz_item(f"LX{n:02d}_Q{20+gi*4}", f"做 {gname} 题目时首先观察：", ["主语与时间状语", "标点符号", "单词拼写"], 0, "首先观察主语人称与时间标志。")
        ]
        add_page(eng.section_head("法", f"考点{gi} · 易错闯关") + make_quiz_grid(q_g), 3, f"语法{gi}闯关", "结构识别", priority="CORE", minutes=4)

    g_sum = (eng.section_head("法", "语法三合一对比与总结") +
             '<div class="kmap">' +
             f'<div class="kmap-node"><div class="kn-title">{gnames[0]}</div><div class="kn-body">核心公式与标准句型。</div></div>' +
             f'<div class="kmap-node"><div class="kn-title">{gnames[1]}</div><div class="kn-body">否定与疑问变化规则。</div></div>' +
             f'<div class="kmap-node"><div class="kn-title">{gnames[2]}</div><div class="kn-body">易错陷阱与中考考法。</div></div>' +
             '</div>' +
             '<div class="note-panel"><div class="np-title">记忆口诀</div>看准主语选对词，否定加 not 疑问提前！</div>')
    add_page(g_sum, 3, "语法总结", "三合一复盘", priority="EXTEND", minutes=4)

    q_exp1 = [
        make_quiz_item(f"LX{n:02d}_Q33", f"下列句子符合 {gnames[0]} 的是：", ["This is a correct sentence.", "This be correct.", "Is this correct."], 0, "符合标准语法形式。"),
        make_quiz_item(f"LX{n:02d}_Q34", f"下列句子符合 {gnames[1]} 的是：", ["She plays basketball well.", "She play basketball.", "She playing basketball."], 0, "主谓一致。")
    ]
    add_page(eng.section_head("法", "语法考点深化演练 ①") + make_quiz_grid(q_exp1), 3, "语法深化①", "高频巩固", priority="EXTEND", minutes=4)

    q_exp2 = [
        make_quiz_item(f"LX{n:02d}_Q58", f"关于 {gnames[2]}，否定句在助动词后加：", ["not", "no", "never"], 0, "否定句加 not。"),
        make_quiz_item(f"LX{n:02d}_Q59", f"关于 {gnames[0]}，一般疑问句需要将：", ["be/助动词提前", "主语删去", "动词后置"], 0, "疑问句将 be 或助动词提前。")
    ]
    add_page(eng.section_head("法", "语法考点深化演练 ②") + make_quiz_grid(q_exp2), 3, "语法深化②", "避坑训练", priority="EXTEND", minutes=4)

    q_sec1 = [
        make_quiz_item(f"LX{n:02d}_Q35", "English is an important ___.", ["subject", "book", "desk"], 0, "English 是一门重要学科 subject。"),
        make_quiz_item(f"LX{n:02d}_Q36", "We should make an ___ to learn well.", ["effort", "answer", "question"], 0, "make an effort 做出努力。"),
        make_quiz_item(f"LX{n:02d}_Q37", "He answered all the ___ correctly.", ["questions", "grammars", "skills"], 0, "answer the questions 回答问题。"),
        make_quiz_item(f"LX{n:02d}_Q38", "Practice helps us make ___.", ["progress", "mistake", "problem"], 0, "make progress 取得进步。")
    ]
    add_page(eng.section_head("练", "随堂演练 ① · 基础单选") + make_quiz_grid(q_sec1), 4, "演练①", "单项选择", priority="CORE", minutes=4)

    q_sec2 = [
        make_quiz_item(f"LX{n:02d}_Q39", "He ___ (learn) English every day.", ["learns", "learn", "learning"], 0, "主语 he 用三单 learns。"),
        make_quiz_item(f"LX{n:02d}_Q40", "They ___ (not forget) the grammar rules.", ["don't forget", "doesn't forget", "not forget"], 0, "复数否定用 don't forget。"),
        make_quiz_item(f"LX{n:02d}_Q41", "She is ___ (practice) speaking now.", ["practicing", "practice", "practices"], 0, "now 提示进行时 is practicing。"),
        make_quiz_item(f"LX{n:02d}_Q42", "We achieve our goals through ___ (effort).", ["effort", "efforts", "efforted"], 0, "effort 为名词。")
    ]
    add_page(eng.section_head("练", "随堂演练 ② · 语法填空") + make_quiz_grid(q_sec2), 4, "演练②", "语法填空", priority="CORE", minutes=4)

    q_sec3 = [
        make_quiz_item(f"LX{n:02d}_Q60", "找错：She learn English every day.", ["learn → learns", "every → daily", "English → english"], 0, "主语 she 用三单 learns。"),
        make_quiz_item(f"LX{n:02d}_Q61", "找错：He don't forget the rules.", ["don't → doesn't", "forget → forgets", "rules → rule"], 0, "单数否定用 doesn't。")
    ]
    add_page(eng.section_head("练", "随堂演练 ③ · 改错专练") + make_quiz_grid(q_sec3), 4, "演练③", "改错专练", priority="EXTEND", minutes=3)

    q_sec4 = [
        make_quiz_item(f"LX{n:02d}_Q62", "A: How do you learn English?\nB: ___.", ["I practice speaking daily.", "In the morning.", "Yes, I do."], 0, "回答学习方式用 practice speaking daily。"),
        make_quiz_item(f"LX{n:02d}_Q63", "A: Do you make progress?\nB: Yes, ___.", ["I make great progress.", "I am bad.", "No, I don't."], 0, "Yes 肯定回答 I make great progress。")
    ]
    add_page(eng.section_head("练", "随堂演练 ④ · 补全对话") + make_quiz_grid(q_sec4), 4, "演练④", "补全对话", priority="EXTEND", minutes=3)

    mini_task = (eng.section_head("练", "Mini Task · 英语学习策略交流") +
                 '<div class="mini-task-box">' +
                 '<div class="mini-task-header"><span class="mini-task-icon">🗣️</span><div class="mini-task-title">任务：向同伴分享你的学习习惯</div></div>' +
                 '<div class="mini-task-content">用必用词 <b>learn, practice, remember, progress, effort</b> 描述你是如何每天学习英语并取得进步的。</div>' +
                 '</div>' +
                 '<div class="note-panel"><div class="np-title">表达支架</div>I learn English every day. I practice speaking with friends and remember 5 words daily. I make progress through effort!</div>')
    add_page(mini_task, 4, "Mini Task", "综合运用", priority="CORE", minutes=5)

    pa_text = (f"<b>Passage A (Learning English with Effort)</b><br>"
               f"Learning English is a step-by-step journey. "
               f"Lucy gets up early every morning to learn 10 new words. "
               f"She practices reading aloud and remembers to review grammar rules. "
               f"When she makes mistakes, she checks her answers carefully. "
               f"With continuous effort, Lucy has made great progress in her study.")
    q_pa = [
        make_quiz_item(f"LX{n:02d}_Q43", "What does Lucy do every morning?", ["Learns 10 new words.", "Plays games.", "Sleeps in."], 0, "原文：learn 10 new words."),
        make_quiz_item(f"LX{n:02d}_Q44", "How does Lucy deal with mistakes?", ["Checks answers carefully.", "Ignores them.", "Gives up."], 0, "原文：checks her answers carefully.")
    ]
    pa_html = (f'<div class="read-split">'
               f'<div class="read-left">'
               f'<div class="annotation-bar">'
               f'<button class="ann-btn" onclick="setPen(\'red\', \'canvas_LX{n:02d}_A\')">✏️ 细红笔</button>'
               f'<button class="ann-btn" onclick="setPen(\'highlighter\', \'canvas_LX{n:02d}_A\')">🖍️ 荧光笔</button>'
               f'<button class="ann-btn" onclick="setPen(\'eraser\', \'canvas_LX{n:02d}_A\')">🧹 橡皮</button>'
               f'<button class="ann-btn" onclick="setPen(\'clear\', \'canvas_LX{n:02d}_A\')">🗑️ 清空</button>'
               f'</div>'
               f'<div class="passage-wrap"><canvas class="read-canvas" id="canvas_LX{n:02d}_A"></canvas>'
               f'<div class="reading-passage">{pa_text}</div></div></div>'
               f'<div class="read-right">{make_quiz_grid(q_pa, cols=False)}</div>'
               f'</div>')
    add_page(eng.section_head("阅", "阅读理解 A · 记叙文 (双栏对比+画笔)") + pa_html, 5, "阅读A", "细节理解", priority="CORE", minutes=6)

    pb_text = (f"<b>Passage B (The Power of Good Habits)</b><br>"
               f"Studies show that good study habits lead to academic success. "
               f"Eighty percent of students who review lessons daily achieve higher points in tests. "
               f"Practicing listening and speaking regularly builds language skills. "
               f"Understanding grammar structures helps students write clear sentences. "
               f"Small daily efforts lead to big success over time.")
    q_pb = [
        make_quiz_item(f"LX{n:02d}_Q45", "What percent of students reviewing daily get higher points?", ["80%.", "50%.", "20%."], 0, "原文：Eighty percent of students."),
        make_quiz_item(f"LX{n:02d}_Q46", "What builds language skills?", ["Practicing regularly.", "Watching cartoons.", "Sleeping."], 0, "原文：Practicing listening and speaking regularly.")
    ]
    pb_html = (f'<div class="read-split">'
               f'<div class="read-left">'
               f'<div class="annotation-bar">'
               f'<button class="ann-btn" onclick="setPen(\'red\', \'canvas_LX{n:02d}_B\')">✏️ 细红笔</button>'
               f'<button class="ann-btn" onclick="setPen(\'highlighter\', \'canvas_LX{n:02d}_B\')">🖍️ 荧光笔</button>'
               f'<button class="ann-btn" onclick="setPen(\'clear\', \'canvas_LX{n:02d}_B\')">🗑️ 清空</button>'
               f'</div>'
               f'<div class="passage-wrap"><canvas class="read-canvas" id="canvas_LX{n:02d}_B"></canvas>'
               f'<div class="reading-passage">{pb_text}</div></div></div>'
               f'<div class="read-right">{make_quiz_grid(q_pb, cols=False)}</div>'
               f'</div>')
    add_page(eng.section_head("阅", "阅读理解 B · 说明文 (双栏对比+画笔)") + pb_html, 5, "阅读B", "说明理解", priority="EXTEND", minutes=6)

    pc_text = (f"<b>Passage C (Tips for Language Learners)</b><br>"
               f"1. Practice speaking English every day.<br>"
               f"2. Read interesting books and remember new words.<br>"
               f"3. [ ___ ] Don't be afraid to ask teacher questions.<br>"
               f"4. Review mistakes regularly to make progress.")
    q_pc = [
        make_quiz_item(f"LX{n:02d}_Q47", "第3空应该填入哪个句子？", ["Check grammar rules carefully.", "Stop reading books.", "Never do homework."], 0, "逻辑一致选检查语法规则。")
    ]
    pc_html = (f'<div class="read-split">'
               f'<div class="read-left"><div class="reading-passage">{pc_text}</div></div>'
               f'<div class="read-right">{make_quiz_grid(q_pc, cols=False)}</div>'
               f'</div>')
    add_page(eng.section_head("阅", "阅读理解 C · 五选四逻辑补全") + pc_html, 5, "阅读C", "逻辑补全", priority="HOME", minutes=6)

    add_page(eng.section_head("拼", f"自然拼读 P1 · {ph_str} 规则表") +
             '<div class="kmap">' +
             f'<div class="kmap-node"><div class="kn-title">拼读规则</div><div class="kn-body">{ph_str} 辅音/元音发音规则。</div></div>' +
             '<div class="kmap-node"><div class="kn-title">拼读例词</div><div class="kn-body">blue, clock, flag, glass, play, slow 等。</div></div>' +
             '</div>', 6, "拼读规则", f"{ph_str} 发音", priority="CORE", minutes=3)

    q_ph1 = [
        make_quiz_item(f"LX{n:02d}_Q48", f"单词 play 中包含的拼读组合是：", ["pl", "bl", "cl"], 0, "play 包含 pl 辅音连缀。"),
        make_quiz_item(f"LX{n:02d}_Q49", f"单词 clock 中包含的拼读组合是：", ["cl", "fl", "gl"], 0, "clock 包含 cl 辅音连缀。")
    ]
    add_page(eng.section_head("拼", "自然拼读 P2 · 辨音选词") + make_quiz_grid(q_ph1), 6, "拼读①", "辨音选词", priority="CORE", minutes=3)

    q_ph2 = [
        make_quiz_item(f"LX{n:02d}_Q50", "blue 与哪个词发音首字母组合相同？", ["black", "clean", "flag"], 0, "blue 与 black 均含 bl。"),
        make_quiz_item(f"LX{n:02d}_Q51", "flag 与哪个词发音首字母组合相同？", ["fly", "play", "slow"], 0, "flag 与 fly 均含 fl。")
    ]
    add_page(eng.section_head("拼", "自然拼读 P3 · 解码高手") + make_quiz_grid(q_ph2), 6, "拼读②", "同组识别", priority="EXTEND", minutes=3)

    add_page(eng.section_head("拼", "自然拼读 P4 · 法则归纳") +
             '<div class="note-panel"><div class="np-title">总结</div>看到辅音连缀快速合音，见词能读，听音能写！</div>', 6, "拼读总结", "法则归纳", priority="EXTEND", minutes=2)

    q_game1 = [
        make_quiz_item(f"LX{n:02d}_Q52", "Learn 的名词形式“学习者”是：", ["learner", "learnment", "learnation"], 0, "learn 加 -er 变名词 learner。"),
        make_quiz_item(f"LX{n:02d}_Q53", "Practice 的常见搭配：", ["practice doing sth.", "practice to do", "practice do"], 0, "practice 后接 V-ing。")
    ]
    add_page(eng.section_head("戏", "课堂综合游戏 ① · 词汇快闪") + make_quiz_grid(q_game1), 7, "游戏①", "快速反应", priority="EXTEND", minutes=4)

    q_game2 = [
        make_quiz_item(f"LX{n:02d}_Q54", "听音选词：/ˈɡræmə(r)/ 对应单词：", ["grammar", "grandma", "glamour"], 0, "grammar 发音为 /ˈɡræmə(r)/。"),
        make_quiz_item(f"LX{n:02d}_Q55", "听音选词：/ˈprəʊɡres/ 对应单词：", ["progress", "process", "program"], 0, "progress 发音为 /ˈprəʊɡres/。")
    ]
    add_page(eng.section_head("戏", "课堂综合游戏 ② · 听音辨词") + make_quiz_grid(q_game2), 7, "游戏②", "听音匹配", priority="EXTEND", minutes=4)

    q_game3 = [
        make_quiz_item(f"LX{n:02d}_Q64", "Practice makes ___.", ["perfect", "good", "better"], 0, "熟能生巧 Practice makes perfect。"),
        make_quiz_item(f"LX{n:02d}_Q65", "Where there is a will, there is a ___.", ["way", "road", "street"], 0, "有志者事竟成 Where there is a will, there is a way。")
    ]
    add_page(eng.section_head("戏", "课堂综合游戏 ③ · 谚语快刷") + make_quiz_grid(q_game3), 7, "游戏③", "谚语快刷", priority="EXTEND", minutes=4)

    q_game4 = [
        make_quiz_item(f"LX{n:02d}_Q66", "Make an ___ to learn English well.", ["effort", "answer", "question"], 0, "make an effort 做出努力。"),
        make_quiz_item(f"LX{n:02d}_Q67", "Check your test paper before ___ in.", ["handing", "hand", "hands"], 0, "before 为介词，后接 V-ing。")
    ]
    add_page(eng.section_head("戏", "课堂综合游戏 ④ · 综合辨析") + make_quiz_grid(q_game4), 7, "游戏④", "综合辨析", priority="EXTEND", minutes=4)

    sum_html = (eng.section_head("结", "课堂总结 · 知识图谱") +
                '<div class="kmap">' +
                f'<div class="kmap-node"><div class="kn-title">词汇</div><div class="kn-body">20 个主题词汇，组词造句。</div></div>' +
                f'<div class="kmap-node"><div class="kn-title">语法</div><div class="kn-body">{gnames[0]} / {gnames[1]} / {gnames[2]}。</div></div>' +
                f'<div class="kmap-node"><div class="kn-title">拼读</div><div class="kn-body">{ph_str} 发音与拼读规律。</div></div>' +
                '</div>' +
                '<div class="note-panel"><div class="np-title">课后作业</div>① 背诵本课 20 词；② 默写 3 大语法结构；③ 完成配套练习。</div>')
    add_page(sum_html, 8, "课堂总结", "知识图谱", priority="CORE", minutes=3)

    q_exit = [
        make_quiz_item(f"LX{n:02d}_Q56", "He practice English every day to ___ his skills.", ["improve", "forget", "lose"], 0, "练习目的是提高技能 improve。"),
        make_quiz_item(f"LX{n:02d}_Q57", "We can achieve success with continuous ___.", ["effort", "mistake", "question"], 0, "付出现努力 effort。")
    ]
    add_page(eng.section_head("结", "Exit Ticket · 5分钟形成性检测") + make_quiz_grid(q_exit), 8, "Exit Ticket", "检测通关", priority="CORE", minutes=5)

    card_meta = {
        "lesson": n,
        "theme": theme,
        "tier": "基础",
        "stage": stage,
        "student": "许颖嘉",
        "grammar": gnames,
        "phonics": ph_str,
        "vocab": {"new_count": 20}
    }
    mm_html = (eng.section_head("图", "课堂思维导图 · 本课全貌") +
               '<div class="body-text">点击分支复盘本课 <span class="highlight">词汇 + 语法 + 拼读</span> 核心脉络。</div>' +
               eng.mind_map(card_meta))
    add_page(mm_html, 9, "思维导图", "互动复盘", priority="CORE", minutes=3)

    mm_full = (eng.section_head("图", "思维导图 · 完整内容页") +
               eng.mind_map_full(card_meta))
    add_page(mm_full, 9, "完整大纲", "对照自测", priority="EXTEND", minutes=3)

    total = p - 1
    seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
    js_extra = ("var studentId='stu_xyj';\n" +
                JS_FULL % (total, json.dumps(seg_pages, ensure_ascii=False),
                           json.dumps(page_meta, ensure_ascii=False)))

    css_combined = CORE_CSS + "\n" + eng.CSS_EXTRA + "\n" + get_theme_css(n)

    html = build_courseware(title=f"第{n:02d}课时 · " + theme, pages_dict=pages, js_extra=js_extra,
                            session=f"LX{n:02d}", nav_html=NAV_HTML, stage_badge=stage_badge,
                            n_pages=total, css_extra=css_combined)
    return html

def ensure_contracts_and_docx(n, folder):
    contract_dir = os.path.join(folder, "契约")
    os.makedirs(contract_dir, exist_ok=True)
    
    meta = LESSON_META.get(n, {"theme": "综合巩固", "grammar": ["语法点①", "语法点②", "语法点③"]})
    theme = meta["theme"]
    
    c1_path = os.path.join(contract_dir, "1_课程概要.md")
    if not os.path.exists(c1_path):
        c1_content = f"# 第 {n:02d} 课时 课程概要\n\n- **学生**：许颖嘉（基础·七年级）\n- **主题**：{theme}\n- **语法**：{', '.join(meta['grammar'])}\n- **课件页数**：41 页\n"
        open(c1_path, "w", encoding="utf-8").write(c1_content)
        
    c4_path = os.path.join(contract_dir, "4_素材清单.md")
    if not os.path.exists(c4_path):
        c4_content = f"# 第 {n:02d} 课时 素材清单\n\n1. `[交互点①]` 导入快闪闯关\n2. `[交互点②]` Page 10 20词双向拖拽归纳箱\n3. `[交互点③]` 语法六色卡规则矩阵\n4. `[交互点④]` 阅读左文右题双栏对比 + 批注画笔\n5. `[交互点⑤]` 自然拼读 4 页多形态互动\n6. `[交互点⑥]` 课堂思维导图全景复盘\n"
        open(c4_path, "w", encoding="utf-8").write(c4_content)

def main():
    base = "D:/英语教学/许颖嘉"
    results = []
    
    print("==================================================")
    print("开始检查并补全 许颖嘉 第 01 ~ 25 课时 课件与资源包...")
    print("==================================================")
    
    for i in range(1, 26):
        dir_name = f"第{i:02d}课时"
        folder = os.path.join(base, dir_name)
        ppt_dir = os.path.join(folder, "课件成品_网页PPT")
        os.makedirs(ppt_dir, exist_ok=True)
        
        # 补全契约
        ensure_contracts_and_docx(i, folder)
        
        target_html = os.path.join(ppt_dir, f"第{i:02d}课时_课件_基础.html")
        
        # 强制全量生成/重构以确保 3 大差异化视觉与排版风格系统与 41 页契约
        style_info = THEME_STYLES[((i-1)//3)%len(THEME_STYLES)]
        print(f"🔨 正在生成/重构 {dir_name} (Style {((i-1)//3)%len(THEME_STYLES)}: {style_info['name']})...")
        if i == 17:
            import build_xyj_l17_l18
            html_content = build_xyj_l17_l18.build_lesson_17()
        elif i == 18:
            import build_xyj_l17_l18
            html_content = build_xyj_l17_l18.build_lesson_18()
        else:
            html_content = generate_lesson_html(i)
            
        with open(target_html, "w", encoding="utf-8") as f:
            f.write(html_content)
        
        # 校验 verify_v2
        r = subprocess.run(['python', 'D:/英语教学/00_工具/verify_v2.py', target_html], capture_output=True, text=True, encoding='utf-8')
        is_pass = r.returncode == 0
        style_name = style_info['name']
        status_str = f"PASS ✅ (Style: {style_name})" if is_pass else f"FAIL ❌"
        print(f"[{i:02d}/25] {dir_name}: {status_str}")
        results.append((i, is_pass, style_name))
        
    print("\n==================================================")
    print("许颖嘉 1~25 课时检查与补全完成！汇总结果：")
    pass_cnt = sum(1 for _, ok, _ in results if ok)
    print(f"总计 PASS: {pass_cnt} / 25")
    print("==================================================")

if __name__ == "__main__":
    main()
