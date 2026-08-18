#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build L19 courseware HTML - Pages 6-20."""

import os

target = r'D:\英语教学\邓兴华\第19课时\课件成品_网页PPT\第19课时_课件_中等.html'

pages_6_9 = r'''<!-- ===================== PAGE 6: 新词 P1 (1-5) ===================== -->
<div class="page" id="page6">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">📖</span> 新词 1-5 · 复合不定代词·指人</div>
<div class="vocab-grid">
<div class="item-card"><span class="card-emoji">👤</span><span class="card-word">someone</span><span class="card-phonetic">/ˈsʌmwʌn/</span><div><span class="card-pos">pron.</span></div><div class="card-cn">某人</div><div class="card-mn">some(一些)+one(人)→某人</div><div class="card-example">Someone is singing in the room.</div></div>
<div class="item-card"><span class="card-emoji">🙋</span><span class="card-word">anyone</span><span class="card-phonetic">/ˈeniwʌn/</span><div><span class="card-pos">pron.</span></div><div class="card-cn">任何人</div><div class="card-mn">any(任何)+one(人)→任何人</div><div class="card-example">Is anyone there?</div></div>
<div class="item-card"><span class="card-emoji">🚫</span><span class="card-word">no one</span><span class="card-phonetic">/ˈnəʊwʌn/</span><div><span class="card-pos">pron.</span></div><div class="card-cn">没有人</div><div class="card-mn">no(无)+one(人)→没有人</div><div class="card-example">No one is in the room.</div></div>
<div class="item-card"><span class="card-emoji">👥</span><span class="card-word">everyone</span><span class="card-phonetic">/ˈevriwʌn/</span><div><span class="card-pos">pron.</span></div><div class="card-cn">每个人</div><div class="card-mn">every(每个)+one(人)→每个人</div><div class="card-example">Everyone is happy today.</div></div>
<div class="item-card"><span class="card-emoji">🎁</span><span class="card-word">something</span><span class="card-phonetic">/ˈsʌmθɪŋ/</span><div><span class="card-pos">pron.</span></div><div class="card-cn">某事/某物</div><div class="card-mn">some(一些)+thing(事物)→某物</div><div class="card-example">I want something to eat.</div></div>
</div>
<div class="quiz-container">
<div class="quiz-question">新词检测：Is ____ there? I need help.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> someone</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> anyone</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> everyone</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>疑问句用 anyone。G49 考点。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
</div>

<!-- ===================== PAGE 7: 新词 P2 (6-10) ===================== -->
<div class="page" id="page7">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">📖</span> 新词 6-10 · 复合不定代词·指物/地点</div>
<div class="vocab-grid">
<div class="item-card"><span class="card-emoji">❓</span><span class="card-word">anything</span><span class="card-phonetic">/ˈeniθɪŋ/</span><div><span class="card-pos">pron.</span></div><div class="card-cn">任何事物</div><div class="card-mn">any(任何)+thing(事物)→任何事物</div><div class="card-example">Do you need anything?</div></div>
<div class="item-card"><span class="card-emoji">⊘</span><span class="card-word">nothing</span><span class="card-phonetic">/ˈnʌθɪŋ/</span><div><span class="card-pos">pron.</span></div><div class="card-cn">没有什么</div><div class="card-mn">no+thing→什么都没有</div><div class="card-example">There is nothing in the box.</div></div>
<div class="item-card"><span class="card-emoji">🌟</span><span class="card-word">everything</span><span class="card-phonetic">/ˈevriθɪŋ/</span><div><span class="card-pos">pron.</span></div><div class="card-cn">一切</div><div class="card-mn">every(每个)+thing(事物)→一切</div><div class="card-example">Everything is ready.</div></div>
<div class="item-card"><span class="card-emoji">📍</span><span class="card-word">somewhere</span><span class="card-phonetic">/ˈsʌmweə(r)/</span><div><span class="card-pos">adv.</span></div><div class="card-cn">某个地方</div><div class="card-mn">some(一些)+where(地方)→某地</div><div class="card-example">Let's go somewhere fun.</div></div>
<div class="item-card"><span class="card-emoji">🗺️</span><span class="card-word">anywhere</span><span class="card-phonetic">/ˈeniweə(r)/</span><div><span class="card-pos">adv.</span></div><div class="card-cn">任何地方</div><div class="card-mn">any(任何)+where(地方)→任何地方</div><div class="card-example">I can't find it anywhere.</div></div>
</div>
<div class="quiz-container">
<div class="quiz-question">新词检测：Do you need ____ for the weekend?</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> something</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> anything</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> everything</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>疑问句用 anything。G49 考点。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
</div>

<!-- ===================== PAGE 8: 新词 P3 (11-15) ===================== -->
<div class="page" id="page8">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">📖</span> 新词 11-15 · 地点与活动类</div>
<div class="vocab-grid">
<div class="item-card"><span class="card-emoji">🚫📍</span><span class="card-word">nowhere</span><span class="card-phonetic">/ˈnəʊweə(r)/</span><div><span class="card-pos">adv.</span></div><div class="card-cn">无处</div><div class="card-mn">no(无)+where(地方)→无处</div><div class="card-example">The cat is nowhere to be found.</div></div>
<div class="item-card"><span class="card-emoji">✈️</span><span class="card-word">abroad</span><span class="card-phonetic">/əˈbrɔːd/</span><div><span class="card-pos">adv.</span></div><div class="card-cn">在国外；出国</div><div class="card-mn">a+broad(宽广)→走向宽广→出国</div><div class="card-example">She plans to go abroad next year.</div></div>
<div class="item-card"><span class="card-emoji">🎪</span><span class="card-word">event</span><span class="card-phonetic">/ɪˈvent/</span><div><span class="card-pos">n.</span></div><div class="card-cn">事件；活动</div><div class="card-mn">e(出)+vent(来)→出来的事→事件</div><div class="card-example">The school event is on Saturday.</div></div>
<div class="item-card"><span class="card-emoji">📋</span><span class="card-word">plan</span><span class="card-phonetic">/plæn/</span><div><span class="card-pos">n./v.</span></div><div class="card-cn">计划</div><div class="card-mn">音似"普蓝"→普蓝计划</div><div class="card-example">We are planning a weekend trip.</div></div>
<div class="item-card"><span class="card-emoji">🔍</span><span class="card-word">explore</span><span class="card-phonetic">/ɪkˈsplɔː(r)/</span><div><span class="card-pos">v.</span></div><div class="card-cn">探索</div><div class="card-mn">ex(出)+plore(呼喊)→向外呼喊→探索</div><div class="card-example">They love to explore new places.</div></div>
</div>
<div class="quiz-container">
<div class="quiz-question">新词检测：She plans to go ____ next year.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">A</span> abroad</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">B</span> event</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> nowhere</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>go abroad = 出国，next year 暗示计划出国。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
</div>

<!-- ===================== PAGE 9: 新词 P4 (16-20) ===================== -->
<div class="page" id="page9">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">📖</span> 新词 16-20 · 情感与描述类</div>
<div class="vocab-grid">
<div class="item-card"><span class="card-emoji">🤔</span><span class="card-word">wonder</span><span class="card-phonetic">/ˈwʌndə(r)/</span><div><span class="card-pos">v.</span></div><div class="card-cn">想知道；惊奇</div><div class="card-mn">音似"万的"→万得惊奇</div><div class="card-example">I wonder what he is doing.</div></div>
<div class="item-card"><span class="card-emoji">😶</span><span class="card-word">seem</span><span class="card-phonetic">/siːm/</span><div><span class="card-pos">v.</span></div><div class="card-cn">似乎；好像</div><div class="card-mn">音似"心"→看起来</div><div class="card-example">She seems happy today.</div></div>
<div class="item-card"><span class="card-emoji">😴</span><span class="card-word">bored</span><span class="card-phonetic">/bɔːd/</span><div><span class="card-pos">adj.</span></div><div class="card-cn">无聊的；厌烦的</div><div class="card-mn">bore(使厌烦)+d→无聊的</div><div class="card-example">He is bored with nothing to do.</div></div>
<div class="item-card"><span class="card-emoji">📔</span><span class="card-word">diary</span><span class="card-phonetic">/ˈdaɪəri/</span><div><span class="card-pos">n.</span></div><div class="card-cn">日记</div><div class="card-mn">di(日)+ary(表物)→日记</div><div class="card-example">She writes in her diary every day.</div></div>
<div class="item-card"><span class="card-emoji">😊</span><span class="card-word">enjoyable</span><span class="card-phonetic">/ɪnˈdʒɔɪəbl/</span><div><span class="card-pos">adj.</span></div><div class="card-cn">令人愉快的</div><div class="card-mn">enjoy(享受)+able(可以)→可享受的</div><div class="card-example">We have an enjoyable weekend.</div></div>
</div>
<div class="quiz-container">
<div class="quiz-question">新词检测：He is ____ with nothing to do.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> enjoyable</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> bored</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> wonder</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>nothing to do → 无聊 → bored。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
</div>
'''

with open(target, 'a', encoding='utf-8') as f:
    f.write(pages_6_9)

print(f"Pages 6-9 appended. Current size: {os.path.getsize(target)} bytes")
