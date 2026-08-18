#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build L19 courseware HTML - Pages 21-31."""

import os

target = r'D:\英语教学\邓兴华\第19课时\课件成品_网页PPT\第19课时_课件_中等.html'

pages_21_31 = r'''<!-- ===================== PAGE 21: 句块排序 ===================== -->
<div class="page" id="page21">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🔢</span> 句块排序 · 周末活动叙述</div>
<div class="section-header"><span class="sh-icon">🎯</span><span class="sh-text">点击词块排列成正确的句子顺序，然后提交！</span></div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_21_0" data-knowledge-id="g49" data-section="core" data-template-id="G-ORDER-SENTENCE" data-interaction-type="order" data-action-type="order" data-cognitive-level="application" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">1. 排列成正确句子：</div>
<div class="order-container" data-order='["Someone","is","exploring","the","park"]'>
<div class="order-chunks">
<span class="order-chunk" onclick="orderClick(this)">the</span>
<span class="order-chunk" onclick="orderClick(this)">is</span>
<span class="order-chunk" onclick="orderClick(this)">Someone</span>
<span class="order-chunk" onclick="orderClick(this)">park</span>
<span class="order-chunk" onclick="orderClick(this)">exploring</span>
</div>
<button class="fill-check-btn" onclick="orderSubmit(this)">提交排序</button>
</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_21_1" data-knowledge-id="g49" data-section="core" data-template-id="G-ORDER-SENTENCE" data-interaction-type="order" data-action-type="order" data-cognitive-level="application" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">2. 排列成正确句子：</div>
<div class="order-container" data-order='["Everyone","is","planning","something","enjoyable"]'>
<div class="order-chunks">
<span class="order-chunk" onclick="orderClick(this)">something</span>
<span class="order-chunk" onclick="orderClick(this)">Everyone</span>
<span class="order-chunk" onclick="orderClick(this)">enjoyable</span>
<span class="order-chunk" onclick="orderClick(this)">planning</span>
<span class="order-chunk" onclick="orderClick(this)">is</span>
</div>
<button class="fill-check-btn" onclick="orderSubmit(this)">提交排序</button>
</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_21_2" data-knowledge-id="g49" data-section="core" data-template-id="G-ORDER-SENTENCE" data-interaction-type="order" data-action-type="order" data-cognitive-level="application" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">3. 排列成正确句子：</div>
<div class="order-container" data-order='["Nothing","seems","boring","when","you","have","a","good","diary"]'>
<div class="order-chunks">
<span class="order-chunk" onclick="orderClick(this)">boring</span>
<span class="order-chunk" onclick="orderClick(this)">diary</span>
<span class="order-chunk" onclick="orderClick(this)">good</span>
<span class="order-chunk" onclick="orderClick(this)">Nothing</span>
<span class="order-chunk" onclick="orderClick(this)">a</span>
<span class="order-chunk" onclick="orderClick(this)">have</span>
<span class="order-chunk" onclick="orderClick(this)">when</span>
<span class="order-chunk" onclick="orderClick(this)">seems</span>
<span class="order-chunk" onclick="orderClick(this)">you</span>
</div>
<button class="fill-check-btn" onclick="orderSubmit(this)">提交排序</button>
</div>
</div>
</div>

<!-- ===================== PAGE 22: 填空演练 ===================== -->
<div class="page" id="page22">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">✍️</span> 填空演练 · 复合不定代词填空</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_22_0" data-knowledge-id="g49" data-section="core" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="application" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">1. I want ____ to eat. I am hungry.（填 something/anything/nothing）</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="something" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_22_1" data-knowledge-id="g49" data-section="core" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="application" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">2. Do you need ____ for the weekend?（填 something/anything）</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="anything" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_22_2" data-knowledge-id="g49" data-section="core" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="application" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">3. ____ is impossible if you try hard.（填 Nothing/Anything）</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="Nothing" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_22_3" data-knowledge-id="g49" data-section="core" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="application" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">4. Let's go ____ fun this weekend.（填 somewhere/anywhere）</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="somewhere" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_22_4" data-knowledge-id="g49" data-section="core" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="application" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">5. ____ is ready for the trip. We can start now.（填 Everything/Anything）</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="Everything" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
</div>

<!-- ===================== PAGE 23: 阅读 A篇 ===================== -->
<div class="page" id="page23">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">📖</span> 阅读 A 篇 · Weekend Event Notice</div>
<div class="reading-layout">
<div class="rl-left">
<div class="reading-passage">
<div class="passage-title">Weekend Event Notice</div>
<div class="word-count">161 words · 应用文</div>
<p>Welcome to our weekend event! Everyone is invited to join the fun. We have something special for you this Saturday.</p>
<p>First, we are planning an outdoor event in the park. You can explore new places and try new activities. Someone from our club is going to show you around. If you are bored at home, this is your chance to do something enjoyable!</p>
<p>We also have a plan for those who want to go abroad. Our teacher is going to talk about study abroad programs. You can learn about different cultures and meet new friends. Everything is free for students.</p>
<p>If you wonder about anything, please ask. We want everyone to have a wonderful weekend. Nowhere else can you find such a great event! Write in your diary about your experience.</p>
<p>The event starts at 9:00 a.m. and ends at 5:00 p.m. We look forward to seeing you there!</p>
</div>
</div>
<div class="rl-right">
<div class="read-right">
<h4>📝 阅读理解 A 篇</h4>
<div class="rl-reel" data-name="A">
<div class="rl-reel-viewport">
<div class="rl-reel-track">
<div class="rl-reel-card"><div class="quiz-q">
<div class="quiz-question">1. Who is invited to the weekend event?</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> Only teachers</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> Everyone</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Only club members</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>第一段 "Everyone is invited to join the fun."。</div>
</div></div>
<div class="rl-reel-card"><div class="quiz-q">
<div class="quiz-question">2. What can you do in the park?</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> Only rest</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> Explore new places and try new activities</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Only play sports</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>第二段 "explore new places and try new activities"。</div>
</div></div>
<div class="rl-reel-card"><div class="quiz-q">
<div class="quiz-question">3. What does the teacher talk about?</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> Sports events</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> Study abroad programs</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Weekend homework</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>第三段 "talk about study abroad programs"。</div>
</div></div>
<div class="rl-reel-card"><div class="quiz-q">
<div class="quiz-question">4. What does the writer suggest at the end?</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> Go home early</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> Write in your diary about your experience</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Buy a ticket</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>第四段 "Write in your diary about your experience."。</div>
</div></div>
<div class="rl-reel-card"><div class="quiz-q">
<div class="quiz-question">5. What is the passage mainly about?</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> A school exam</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> A weekend event notice</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> A travel guide</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>主旨题。全文是周末活动通知。</div>
</div></div>
</div>
</div>
<div class="rl-reel-nav">
<button class="rl-prev" onclick="rlStep(this,-1)" title="上一题">‹</button>
<span class="rl-reel-dots"><i class="on"></i><i></i><i></i><i></i><i></i></span>
<span class="rl-reel-count">1 / 5</span>
<button class="rl-next" onclick="rlStep(this,1)" title="下一题">›</button>
</div>
</div>
</div>
</div>
</div>

<!-- ===================== PAGE 24: 阅读 A篇题目解析 ===================== -->
<div class="page" id="page24">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🔍</span> 阅读 A 篇 · 题目解析与考点回顾</div>
<div class="rule-card rc-zhug"><div class="rc-cat">考点分析 <span class="rc-badge key">★ 重点记忆</span></div><div class="rc-text">
<strong>A篇考点覆盖：</strong><br>
<span class="rc-chip">G49</span> everyone, someone, something, anything, everything, nothing, nowhere 复合不定代词<br>
<span class="rc-chip">词汇</span> explore, bored, enjoyable, abroad, wonder, diary, event, plan<br>
<span class="rc-chip">题型</span> 细节题 3 + 推断题 1 + 主旨题 1
</div></div>
<div class="ok-box"><div class="ok-title">✅ 正确答案与解析</div>
<div class="ok-content">
1. <strong>B</strong> Everyone — 第一段原文 "Everyone is invited"<br>
2. <strong>B</strong> Explore new places — 第二段原文<br>
3. <strong>B</strong> Study abroad programs — 第三段原文<br>
4. <strong>B</strong> Write in your diary — 第四段原文<br>
5. <strong>B</strong> A weekend event notice — 主旨归纳
</div></div>
<div class="tip-box"><div class="tip-title">💡 阅读技巧</div><div class="tip-content">应用文抓"活动信息"：时间、地点、参与者、活动内容。注意复合不定代词的使用语境。</div></div>
</div>

<!-- ===================== PAGE 25: 阅读 B篇 ===================== -->
<div class="page" id="page25">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge extend">EXTEND · 时间充足时做</span></div>
<div class="page-title"><span class="title-icon">📖</span> 阅读 B 篇 · A Weekend to Remember</div>
<div class="reading-layout">
<div class="rl-left">
<div class="reading-passage">
<div class="passage-title">A Weekend to Remember</div>
<div class="word-count">183 words · 记叙文</div>
<p>Last weekend is one that I will always remember. It seems like everything was perfect.</p>
<p>On Saturday morning, my friend Lily and I are planning to explore a new place. We want to go somewhere we have never been before. Lily suggests that we visit an old town near our city. No one in our class has been there, so we are very excited.</p>
<p>When we arrive, everything looks wonderful. The streets are clean and quiet. Someone is playing music in the square. We walk around and find a small diary shop. Lily buys a beautiful diary to write about our trip.</p>
<p>We also visit a small museum. There are many old things to see. We wonder about the stories behind them. The guide tells us everything about the town's history. It is so interesting that no one feels bored.</p>
<p>In the evening, we sit by the river. I write in my diary: "Today is the most enjoyable day." We plan to explore more places next weekend. There is nothing better than a good adventure with a good friend!</p>
</div>
</div>
<div class="rl-right">
<div class="read-right">
<h4>📝 阅读理解 B 篇</h4>
<div class="rl-reel" data-name="B">
<div class="rl-reel-viewport">
<div class="rl-reel-track">
<div class="rl-reel-card"><div class="quiz-q">
<div class="quiz-question">1. Where do they go on Saturday?</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> A big city</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> An old town</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> A beach</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>第二段 "visit an old town near our city"。</div>
</div></div>
<div class="rl-reel-card"><div class="quiz-q">
<div class="quiz-question">2. What does Lily buy?</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> A ticket</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> A diary</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> A map</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>第三段 "Lily buys a beautiful diary"。</div>
</div></div>
<div class="rl-reel-card"><div class="quiz-q">
<div class="quiz-question">3. The underlined word "bored" in Paragraph 4 means ____.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> excited</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> not interested</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> happy</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>词义题。bored = 无聊的 = not interested。语境：so interesting that no one feels bored。</div>
</div></div>
<div class="rl-reel-card"><div class="quiz-q">
<div class="quiz-question">4. What can we infer from the last paragraph?</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> The writer doesn't like the trip</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> The writer wants to explore more places</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> The writer is bored</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>推断题。"We plan to explore more places next weekend" → 想继续探索。</div>
</div></div>
<div class="rl-reel-card"><div class="quiz-q">
<div class="quiz-question">5. What is the best title for the passage?</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> A Boring Weekend</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> A Weekend to Remember</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> A Diary Shop</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>主旨题。全文讲述一个值得记住的周末经历。</div>
</div></div>
</div>
</div>
<div class="rl-reel-nav">
<button class="rl-prev" onclick="rlStep(this,-1)" title="上一题">‹</button>
<span class="rl-reel-dots"><i class="on"></i><i></i><i></i><i></i><i></i></span>
<span class="rl-reel-count">1 / 5</span>
<button class="rl-next" onclick="rlStep(this,1)" title="下一题">›</button>
</div>
</div>
</div>
</div>
</div>

<!-- ===================== PAGE 26: 阅读 B篇题目解析 ===================== -->
<div class="page" id="page26">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge extend">EXTEND · 时间充足时做</span></div>
<div class="page-title"><span class="title-icon">🔍</span> 阅读 B 篇 · 题目解析与考点回顾</div>
<div class="rule-card rc-zhug"><div class="rc-cat">考点分析 <span class="rc-badge key">★ 重点记忆</span></div><div class="rc-text">
<strong>B篇考点覆盖：</strong><br>
<span class="rc-chip">G49</span> someone, something, anything, nothing, everything, somewhere, nowhere<br>
<span class="rc-chip">词汇</span> explore, wonder, seem, bored, diary, enjoyable, plan, abroad, event<br>
<span class="rc-chip">题型</span> 细节题 3 + 词义题 1 + 推断题 1
</div></div>
<div class="ok-box"><div class="ok-title">✅ 正确答案与解析</div>
<div class="ok-content">
1. <strong>B</strong> An old town — 第二段原文<br>
2. <strong>B</strong> A diary — 第三段原文<br>
3. <strong>B</strong> not interested — bored 词义辨析<br>
4. <strong>B</strong> Wants to explore more — 推断<br>
5. <strong>B</strong> A Weekend to Remember — 主旨
</div></div>
<div class="tip-box"><div class="tip-title">💡 记叙文阅读技巧</div><div class="tip-content">抓时间线：Saturday morning → arrive → museum → evening。注意人物情感变化和复合不定代词用法。</div></div>
</div>

<!-- ===================== PAGE 27: 五选四 ===================== -->
<div class="page" id="page27">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge extend">EXTEND · 时间充足时做</span></div>
<div class="page-title"><span class="title-icon">📋</span> 阅读五选四 · Planning Our Weekend</div>
<div class="reading-passage b5-passage">
<div class="passage-title">Planning Our Weekend</div>
<div class="word-count">161 words · 对话/短文</div>
<p>Two friends, Tom and Lucy, are talking about their weekend plan.</p>
<p>Tom: I am bored with nothing to do this weekend. <span class="b5-hole" data-interaction-item="1" data-question-id="Q19_27_0" data-knowledge-id="g49" data-section="extend" data-template-id="G-BLANK-PICK" data-interaction-type="blank_pick" data-action-type="point" data-cognitive-level="retrieval" data-scorable="true" data-blank="1" data-correct="B" data-answer="Do you want to go somewhere fun?"><button class="b5-blank" onclick="b5ToggleBlank(this)">· 点击 ·</button></span></p>
<p>Lucy: Sure! I am planning to explore the new park. <span class="b5-hole" data-interaction-item="1" data-question-id="Q19_27_1" data-knowledge-id="g49" data-section="extend" data-template-id="G-BLANK-PICK" data-interaction-type="blank_pick" data-action-type="point" data-cognitive-level="retrieval" data-scorable="true" data-blank="2" data-correct="D" data-answer="Everyone says it is very enjoyable."><button class="b5-blank" onclick="b5ToggleBlank(this)">· 点击 ·</button></span></p>
<p>Tom: That sounds great! Is there anything special to see?</p>
<p>Lucy: Yes! Someone told me there is a big event on Saturday. <span class="b5-hole" data-interaction-item="1" data-question-id="Q19_27_2" data-knowledge-id="g49" data-section="extend" data-template-id="G-BLANK-PICK" data-interaction-type="blank_pick" data-action-type="point" data-cognitive-level="retrieval" data-scorable="true" data-blank="3" data-correct="A" data-answer="We can explore the gardens and try new activities."><button class="b5-blank" onclick="b5ToggleBlank(this)">· 点击 ·</button></span></p>
<p>Tom: I wonder if we need to bring anything.</p>
<p>Lucy: Just bring your diary! <span class="b5-hole" data-interaction-item="1" data-question-id="Q19_27_3" data-knowledge-id="g49" data-section="extend" data-template-id="G-BLANK-PICK" data-interaction-type="blank_pick" data-action-type="point" data-cognitive-level="application" data-scorable="true" data-blank="4" data-correct="C" data-answer="Nothing is better than a good weekend with friends."><button class="b5-blank" onclick="b5ToggleBlank(this)">· 点击 ·</button></span></p>
<p>Tom: Let's go then!</p>
</div>
<div style="margin:10px 0 4px;font-size:14px;color:var(--accent-dark)">👆 先读短文，点击文中任意一个虚线空，再从下方选项中选择合适的句子填入。</div>
<div class="b5-opts" id="b5-panel">
<div class="b5-opts-head">👇 请在下方 5 个选项中，点击一个字母作为答案</div>
<div class="b5-opt-row" data-letter="A"><button class="b5-opt" data-letter="A" onclick="b5Pick(this)">A</button><span class="b5-opt-text">We can explore the gardens and try new activities.</span></div>
<div class="b5-opt-row" data-letter="B"><button class="b5-opt" data-letter="B" onclick="b5Pick(this)">B</button><span class="b5-opt-text">Do you want to go somewhere fun?</span></div>
<div class="b5-opt-row" data-letter="C"><button class="b5-opt" data-letter="C" onclick="b5Pick(this)">C</button><span class="b5-opt-text">Nothing is better than a good weekend with friends.</span></div>
<div class="b5-opt-row" data-letter="D"><button class="b5-opt" data-letter="D" onclick="b5Pick(this)">D</button><span class="b5-opt-text">Everyone says it is very enjoyable.</span></div>
<div class="b5-opt-row" data-letter="E"><button class="b5-opt" data-letter="E" onclick="b5Pick(this)">E</button><span class="b5-opt-text">We are planning to go abroad next year.</span></div>
</div>
</div>

<!-- ===================== PAGE 28: 汉译英练习 ===================== -->
<div class="page" id="page28">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🌐</span> 汉译英练习 · 复合不定代词</div>
<div class="quiz-container">
<div class="quiz-question">1. 有人正在公园里探索。</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> Anyone is exploring the park.</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> Someone is exploring the park.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Nothing is exploring the park.</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>"有人" → 肯定句 → someone。G49 考点。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container">
<div class="quiz-question">2. 你需要什么吗？</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> Do you need something?</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> Do you need anything?</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Do you need nothing?</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>疑问句 → anything。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container">
<div class="quiz-question">3. 一切都准备好了。</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> Something is ready.</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> Everything is ready.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Nothing is ready.</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>"一切" → everything。全包含。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container">
<div class="quiz-question">4. 我哪里都找不到我的日记。</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> I can't find my diary somewhere.</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> I can't find my diary anywhere.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> I can't find my diary nowhere.</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>否定句 can't → anywhere。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
</div>

<!-- ===================== PAGE 29: 造句练习 ===================== -->
<div class="page" id="page29">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">✏️</span> 造句练习 · 用复合不定代词造句</div>
<div class="quiz-container">
<div class="quiz-question">1. 用 "someone" 造一个肯定句（指人）：</div>
<div style="padding:10px;background:#F8FAFC;border-radius:8px;font-size:15px;color:var(--text-secondary)">💬 示范：Someone is planning a weekend trip.</div>
<div class="quiz-feedback"><span class="feedback-label">造句任务：</span>学生口头或书面造句。核心：someone + 单数谓语。</div>
</div>
<div class="quiz-container">
<div class="quiz-question">2. 用 "nothing" 造一个全否定句：</div>
<div style="padding:10px;background:#F8FAFC;border-radius:8px;font-size:15px;color:var(--text-secondary)">💬 示范：Nothing is more fun than a good weekend.</div>
<div class="quiz-feedback"><span class="feedback-label">造句任务：</span>学生口头或书面造句。核心：nothing + 单数谓语（全否定）。</div>
</div>
<div class="quiz-container">
<div class="quiz-question">3. 用 "anywhere" 造一个否定句：</div>
<div style="padding:10px;background:#F8FAFC;border-radius:8px;font-size:15px;color:var(--text-secondary)">💬 示范：I can't find my diary anywhere.</div>
<div class="quiz-feedback"><span class="feedback-label">造句任务：</span>学生口头或书面造句。核心：否定句 + anywhere。</div>
</div>
<div class="quiz-container">
<div class="quiz-question">4. 用 "everything" 造一个全包含句：</div>
<div style="padding:10px;background:#F8FAFC;border-radius:8px;font-size:15px;color:var(--text-secondary)">💬 示范：Everything is ready for the event.</div>
<div class="quiz-feedback"><span class="feedback-label">造句任务：</span>学生口头或书面造句。核心：everything + 单数谓语。</div>
</div>
</div>

<!-- ===================== PAGE 30: 改错填空 ===================== -->
<div class="page" id="page30">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🔧</span> 改错填空 · 找出并改正错误</div>
<div class="quiz-container">
<div class="quiz-question">1. 找出错误：Everyone are happy today.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">A</span> Everyone is happy today.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">B</span> Everyone were happy today.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Everyone be happy today.</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>复合不定代词作主语 → 谓语用单数 is。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container">
<div class="quiz-question">2. 找出错误：I don't know someone here.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">A</span> I don't know anyone here.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">B</span> I don't know no one here.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> I don't know everyone here.</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>否定句用 anyone，不用 someone。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container">
<div class="quiz-question">3. 找出错误：Nothing are wrong.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">A</span> Nothing is wrong.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">B</span> Nothing were wrong.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Nothing be wrong.</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>Nothing → 单数谓语 is。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container">
<div class="quiz-question">4. 找出错误：Someone have a plan.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">A</span> Someone has a plan.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">B</span> Someone are having a plan.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Someone have has a plan.</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>Someone → 三单谓语 has。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
</div>

<!-- ===================== PAGE 31: 进阶翻译 ===================== -->
<div class="page" id="page31">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge extend">EXTEND · 时间充足时做</span></div>
<div class="page-title"><span class="title-icon">🌟</span> 进阶翻译 · 综合运用</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_31_0" data-knowledge-id="g49" data-section="extend" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="application" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">1. 每个人似乎都很开心。→ ____ seems happy.</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="Everyone" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_31_1" data-knowledge-id="g49" data-section="extend" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="application" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">2. 我在哪儿都找不到它。→ I can't find it ____.</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="anywhere" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_31_2" data-knowledge-id="g49" data-section="extend" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="application" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">3. 没有人知道答案。→ ____ knows the answer.</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="No one" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
<div class="quiz-container">
<div class="quiz-question">4. 你想要点什么喝的吗？（请求语境）→ Would you like ____ to drink?</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">A</span> something</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">B</span> anything</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> nothing</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>请求/邀请语境用 something，虽然是疑问句。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container">
<div class="quiz-question">5. 一切都为旅行准备好了。→ ____ is ready for the trip.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> Something</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> Everything</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Anything</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>"一切" → everything。全包含。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
</div>
'''

with open(target, 'a', encoding='utf-8') as f:
    f.write(pages_21_31)

print(f"Pages 21-31 appended. Current size: {os.path.getsize(target)} bytes")
