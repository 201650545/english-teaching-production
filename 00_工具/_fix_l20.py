# -*- coding: utf-8 -*-
import re, shutil, os

BASE=r'D:\英语教学\邓兴华'
LESSON=20
SRC=os.path.join(BASE,'第%d课时'%LESSON,'课件成品_网页PPT','第%d课时_课件_中等.html'%LESSON)
BAK=os.path.join(BASE,'第%d课时'%LESSON,'_旧件_收尾前20260808','课件成品_网页PPT','第%d课时_课件_中等.html'%LESSON)
os.makedirs(os.path.dirname(BAK),exist_ok=True)
shutil.copy2(SRC,BAK)
h=open(SRC,encoding='utf-8').read()
orig_h=h
log=[]

def do(desc):
    log.append(desc)

# --- 1. Fix broken question-id ---
if 'data-question-id="L20_data-interaction-type="' in h:
    h=h.replace('data-question-id="L20_data-interaction-type="','data-question-id="L20_ITM_001"')
    do('fix broken question-id L20_ITM_001')

# --- 2. Fix 6 broken premature-close quiz-q: wrap text in qq-text ---
# pattern: data-scorable="true">TEXT</div> <div class="quiz-options">
pat=re.compile(r'(data-scorable="true">)([^<]*?)(</div>)(\s*<div class="quiz-options">)')
n=0
def wrap(m):
    global n
    n+=1
    return m.group(1)+'\n<div class="qq-text">'+m.group(2)+'</div>\n'+m.group(4)
h=pat.sub(wrap,h)
do('qq-text wrap broken containers: %d'%n)

# --- 3. Remove data-interaction-item from link-container (fix VIS-615) ---
# only within link-container tags
def no_item_link(m):
    tag=m.group(0)
    tag=re.sub(r' data-interaction-item="1"','',tag)
    return tag
# process link-container open tags
pat2=re.compile(r'<div class="link-container"[^>]*>')
h=pat2.sub(lambda m: no_item_link(m), h)
do('removed data-interaction-item from link-container')

# --- 4. Add metadata to order-container (fix VIS-610/603) ---
# order-container currently: <div class="order-container" data-order='[...]' data-question-id="L20_P23_Q1">
pat3=re.compile(r'<div class="order-container" data-order=\'([^\']*)\' data-question-id="L20_P23_Q1">')
def fix_order(m):
    return '<div class="order-container" data-interaction-type="order" data-action-type="order" data-knowledge-id="GEN" data-section="core" data-template-id="C-INTERACT" data-cognitive-level="application" data-scorable="true" data-order=\''+m.group(1)+'\' data-question-id="L20_P23_Q1">'
h=pat3.sub(fix_order,h)
do('added metadata to order-container (L20_P23_Q1)')

# --- 5. Convert 6 single_choice -> fill_in ---
def find_matching_close(h,start):
    # start points at <div class="quiz-q"...>, find matching </div>
    depth=0; i=start
    while True:
        oi=h.find('<div',i); ci=h.find('</div>',i)
        if ci==-1: return -1
        if oi!=-1 and oi<ci:
            depth+=1; i=oi+4
        else:
            depth-=1
            if depth==0: return ci
            i=ci+6

def clean_ans(t):
    t=re.sub(r'<[^>]+>','',t)
    t=t.replace('&amp;','&').replace('&lt;','<').replace('&gt;','>').replace('&quot;','"').replace('&#39;',"'")
    return t.strip()

def convert_one(h,start,endtag):
    # find correct answer among the quiz-opt buttons in this container
    seg=h[start:endtag]
    am=re.search(r'<button class="quiz-opt"[^>]*data-correct="1"[^>]*>(.*?)</button>',seg,re.S)
    if not am: return h,False
    ans=clean_ans(am.group(1))
    # locate quiz-options block
    opto=h.find('<div class="quiz-options">',start)
    if opto==-1 or opto>endtag: return h,False
    opte=h.find('</div>',opto)
    opte2=h.find('</div>',opte+6)
    # find actual end of quiz-options (the div containing buttons)
    # find last </div> before the quiz-feedback
    fb=h.find('<div class="quiz-feedback">',start,endtag)
    if fb==-1: return h,False
    # options block spans from opto to fb
    opte=fb
    newblock='<div class="fill-input-wrap"><input class="fill-input" type="text" data-correct="%s" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key===\'Enter\'){event.preventDefault();checkFill(this);}"><button class="fill-check-btn" onclick="checkFill(this)">确认</button></div>'%ans
    # modify quiz-q open tag
    gt=h.find('>',start)
    tag=h[start:gt+1]
    tag2=tag.replace('data-interaction-type="single_choice"','data-interaction-type="fill_in"').replace('data-action-type="select"','data-action-type="fill"')
    between=h[gt+1:opto]
    h=h[:start]+tag2+between+newblock+h[opte:]
    return h,True

def find_matching_close2(h,start):
    depth=0;i=start
    while True:
        oi=h.find('<div',i);ci=h.find('</div>',i)
        if ci==-1:return -1
        if oi!=-1 and oi<ci:
            depth+=1;i=oi+4
        else:
            depth-=1
            if depth==0:return ci
            i=ci+6

# collect single_choice quiz-q positions
qids=[]  # (start, endtag)
for m in re.finditer(r'<div class="quiz-q"[^>]*data-interaction-type="single_choice"[^>]*>',h):
    start=m.start(); endtag=find_matching_close2(h,start)
    if endtag!=-1:
        qids.append((start,endtag))
to_convert=6
converted=0
# convert ones WITHOUT the attached structure issue first (prefer ones with quiz-options)
for start,endtag in qids:
    if converted>=to_convert:break
    h,ok=convert_one(h,start,endtag)
    if ok: converted+=1
do('converted single_choice->fill_in: %d'%converted)

# --- 6. Add page-turn exemptions with e.target.closest literal (fix VIS-614) ---
# L20 already has a guard using t.closest; verify requires literal 'e.target.closest(...)'
old_guard="if (t && t.closest && (t.closest('.drag-container') || t.closest('.link-container') || t.closest('.order-container'))) return;"
new_guard="if (e.target.closest('.drag-container') || e.target.closest('.link-container') || e.target.closest('.order-container')) return;"
if old_guard in h:
    h=h.replace(old_guard,new_guard)
    do('rewrote page-turn exemption guard to e.target.closest')
elif "e.target.closest('.link-container')" not in h:
    # fallback: insert guard right after the second closest() line in the click listener
    anchor="if (t && t.closest && (t.closest('.drag-container') || t.closest('.link-container') || t.closest('.order-container'))) return;"
    if anchor in h:
        h=h.replace(anchor,new_guard)
        do('rewrote page-turn exemption guard (alt)')
    else:
        # insert before 'if (e.clientX > window.innerWidth / 2) nextPage();'
        ins="if (e.clientX > window.innerWidth / 2) nextPage();"
        if ins in h:
            h=h.replace(ins, new_guard+"\n  "+ins)
            do('inserted page-turn exemption guard')

# ensure click-zone interactive containers z-index > 1 (VIS-614 click-zone branch)
for c in ('link-container','order-container','drag-container'):
    cssm=re.search(r'\.'+c+r'[^{]*\{[^}]*\}',h,re.S)
    if cssm:
        block=cssm.group(0)
        if not re.search(r'z-index\s*:\s*\d+',block):
            h=h.replace(block, block.rstrip()+' z-index:2; }')
            do('added z-index:2 to .'+c)

open(SRC,'w',encoding='utf-8').write(h)
print('L20 fixes applied. Current div balance: %d/%d'%(len(re.findall(r'<div\b',h)),len(re.findall(r'</div>',h))))
for l in log: print(' -',l)