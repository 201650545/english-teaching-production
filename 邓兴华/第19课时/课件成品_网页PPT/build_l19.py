#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build L19 courseware HTML by appending page content to the CSS header."""

import os

target = r'D:\英语教学\邓兴华\第19课时\课件成品_网页PPT\第19课时_课件_中等.html'

# Pages 1-5
pages_1_5 = r'''<!-- ===================== PAGE 1: Cover ===================== -->
<div class="page cover-page cover-poster" id="page1">
<div class="cover-topbar">
<div class="cover-badge">🧭 STAGE 5 · L19 · WEEKEND EXPLORER</div>
<div class="cover-floor">Entry No.19</div>
</div>
<div class="cover-title">第19课 · 周末探索之旅</div>
<div class="cover-subtitle">复合不定代词（someone/anything…）分类与语义</div>
<div class="cover-route">
<div class="route-stop"><span>📦</span><b>新词20</b><em>词汇</em></div>
<div class="route-stop"><span>🧩</span><b>G49</b><em>语法</em></div>
<div class="route-stop"><span>📖</span><b>3篇阅读</b><em>阅读</em></div>
<div class="route-stop"><span>🗺️</span><b>五选四</b><em>题型</em></div>
<div class="route-stop"><span>🔊</span><b>ture /tʃə/</b><em>拼读</em></div>
</div>
<div class="cover-objectives">
<div class="obj-card"><div class="obj-icon">🔤</div><div class="obj-text">20新词：复合不定代词·周末活动</div></div>
<div class="obj-card"><div class="obj-icon">📐</div><div class="obj-text">G49 复合不定代词分类与语义（螺旋自G33 some/any）</div></div>
<div class="obj-card"><div class="obj-icon">📖</div><div class="obj-text">A篇应用文 + B篇记叙文 + 五选四说明文</div></div>
<div class="obj-card"><div class="obj-icon">🔊</div><div class="obj-text">拼读 ture /tʃə/ + tion /ʃə/ 对比</div></div>
</div>
<div class="cover-meta">
<span class="meta-chip">时长 · <strong>90分钟</strong></span>
<span class="meta-chip">词汇 · <strong>20词</strong></span>
<span class="meta-chip">语法 · <strong>G49</strong></span>
<span class="meta-chip">页数 · <strong>42页</strong></span>
</div>
</div>

<!-- ===================== PAGE 2: 复习导入 P1 - L18语法回顾 ===================== -->
<div class="page" id="page2">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🔄</span> L18 语法回顾 · 现在进行时三剑客</div>
<div class="section-header"><span class="sh-icon">📚</span><span class="sh-text">上节课我们学了什么？</span></div>
<div class="rule-card rc-qita"><div class="rc-cat">口诀回顾 <span class="rc-badge key">★ 重点记忆</span></div><div class="rc-text">
<div class="rc-chip">G46 现在进行时</div><span class="rc-arw">→</span><span class="rc-chip">be + V-ing</span><br>
<div class="rc-chip">G47 V-ing 变化</div><span class="rc-arw">→</span><span class="rc-chip">直接+ing / 去e+ing / 双写+ing</span><br>
<div class="rc-chip">G48 标志词</div><span class="rc-arw">→</span><span class="rc-chip">now / look / listen</span>
</div></div>
<div class="formula-box">
<div class="formula-title">G46 · 现在进行时结构公式</div>
<div class="formula-content">I + <strong>am</strong> + V-ing<br>He/She/It + <strong>is</strong> + V-ing<br>We/You/They + <strong>are</strong> + V-ing</div>
</div>
<div class="formula-box">
<div class="formula-title">G47 · V-ing 变化规则</div>
<div class="formula-content">直接+ing: read→reading · play→playing<br>去e+ing: write→writing · make→making<br>双写+ing: run→running · swim→swimming</div>
</div>
<div class="tip-box"><div class="tip-title">💡 G48 现在进行时标志词</div><div class="tip-content">now · look! · listen! · at the moment · right now</div></div>
<div class="example-sent"><span class="sent-label">G46</span> She <strong>is cooking</strong> dinner <em>now</em>.</div>
<div class="example-sent"><span class="sent-label">G46</span> Look! He <strong>is drawing</strong> a picture.</div>
<div class="example-sent"><span class="sent-label">G46</span> They <strong>are playing</strong> basketball <em>right now</em>.</div>
<div class="quiz-container">
<div class="quiz-question">复习检测：Look! The children ____ games in the park.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> play</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> are playing</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> plays</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>标志词 Look! → 现在进行时 be + V-ing。G46 考点。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
</div>

<!-- ===================== PAGE 3: 复习导入 P2 - L18词汇快闪 ===================== -->
<div class="page" id="page3">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">⚡</span> L18 词汇快闪 · 家务与感官20词</div>
<div class="section-header"><span class="sh-icon">🃏</span><span class="sh-text">看词说义，看义说词！</span></div>
<div class="mini-flash-grid">
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">clean</div><div class="mf-cn">打扫</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">wash</div><div class="mf-cn">洗</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">cook</div><div class="mf-cn">做饭</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">sweep</div><div class="mf-cn">扫</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">tidy</div><div class="mf-cn">整理</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">smell</div><div class="mf-cn">闻</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">taste</div><div class="mf-cn">尝</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">sound</div><div class="mf-cn">听起来</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">feel</div><div class="mf-cn">感觉</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">look</div><div class="mf-cn">看起来</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">listen</div><div class="mf-cn">听</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">watch</div><div class="mf-cn">观看</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">touch</div><div class="mf-cn">触摸</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">hear</div><div class="mf-cn">听见</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">dirty</div><div class="mf-cn">脏的</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">neat</div><div class="mf-cn">整洁的</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">quiet</div><div class="mf-cn">安静的</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">loud</div><div class="mf-cn">大声的</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">soft</div><div class="mf-cn">柔软的</div></div>
<div class="mini-flash-item" onclick="flipCard(this)"><div class="mf-word">fresh</div><div class="mf-cn">新鲜的</div></div>
</div>
<div class="vocab-game">
<div class="game-prompt">🎮 跨课词汇复习 · 用 L18 词汇完成句子</div>
<div class="context-box">1. The food ____ delicious! I love it.</div>
<div style="display:flex;gap:8px;flex-wrap:wrap">
<button class="game-option" data-correct="1" onclick="gameCheck(this)">tastes</button>
<button class="game-option" data-correct="0" onclick="gameCheck(this)">smells</button>
<button class="game-option" data-correct="0" onclick="gameCheck(this)">sounds</button>
</div>
<div class="game-feedback"><span class="feedback-label">解析：</span>food + delicious → tastes（尝起来）。感官动词。</div>
<div class="context-box" style="margin-top:10px">2. Please ____ your room. It is very ____.</div>
<div style="display:flex;gap:8px;flex-wrap:wrap">
<button class="game-option" data-correct="1" onclick="gameCheck(this)">tidy; dirty</button>
<button class="game-option" data-correct="0" onclick="gameCheck(this)">wash; neat</button>
<button class="game-option" data-correct="0" onclick="gameCheck(this)">cook; loud</button>
</div>
<div class="game-feedback"><span class="feedback-label">解析：</span>tidy your room = 整理房间，dirty = 脏的。</div>
</div>
</div>

<!-- ===================== PAGE 4: 复习导入 P3 - L18错题回顾 + 本课导入 ===================== -->
<div class="page" id="page4">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🧭</span> L18 错题回顾 + 本课导入 · 周末探索</div>
<div class="err-box"><div class="err-title">❌ L18 高频错题</div>
<div class="err-item"><span class="err-wrong">She are cooking now.</span><span class="err-right">→ She is cooking now.</span>（she → is）</div>
<div class="err-item"><span class="err-wrong">He is runing.</span><span class="err-right">→ He is running.</span>（run → 双写+ing）</div>
<div class="err-item"><span class="err-wrong">Look! They plays football.</span><span class="err-right">→ Look! They are playing football.</span>（Look! → 现在进行时）</div>
</div>
<div class="highlight-box">
<div class="hb-title">🤔 思考一下</div>
<div class="hb-content">周末你想去哪里探索？<br>你有没有什么有趣的计划？<br>你身边有没有人在做有趣的事？<br>→ 这些句子用英语怎么说？</div>
</div>
<div class="rule-card rc-zhug"><div class="rc-cat">本课核心 <span class="rc-badge key">★ 重点记忆</span></div><div class="rc-text">
<strong>本课核心语法：</strong><br>
<div class="rc-chip">G49 复合不定代词分类与语义</div><br>
<strong>螺旋自：</strong><span class="rc-chip">G33 some/any 基础辨析</span> → 升级为复合不定代词
</div></div>
<div class="example-sent"><span class="sent-label">导入</span> <strong>Someone</strong> is exploring the park.</div>
<div class="example-sent"><span class="sent-label">导入</span> Is <strong>anyone</strong> planning to go <strong>abroad</strong>?</div>
<div class="example-sent"><span class="sent-label">导入</span> I want <strong>something</strong> enjoyable to do.</div>
<div class="quiz-container">
<div class="quiz-question">导入检测：I want ____ to eat.（我想要点东西吃）</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> someone</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> something</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> anywhere</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>to eat → 指物 → something。G49 考点预热。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
</div>

<!-- ===================== PAGE 5: 跨课词汇游戏 ===================== -->
<div class="page" id="page5">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🎮</span> 跨课词汇游戏 · 周末活动 vs 学校活动</div>
<div class="vocab-game">
<div class="game-prompt">🎯 玩法：点击词汇卡片，将其归入"周末活动"或"学校活动"分类箱！</div>
<div style="display:flex;gap:10px;flex-wrap:wrap;margin-bottom:16px">
<div style="flex:1;min-width:180px;background:rgba(255,255,255,0.6);border-radius:var(--radius);padding:10px">
<h4 style="color:var(--brand-dark);font-size:14px">📥 词卡池</h4>
<div id="dd-pool2" style="min-height:80px">
<span class="dd-card" data-cat="weekend" onclick="sortCard2(this,'weekend')">explore</span>
<span class="dd-card" data-cat="school" onclick="sortCard2(this,'school')">meeting</span>
<span class="dd-card" data-cat="weekend" onclick="sortCard2(this,'weekend')">diary</span>
<span class="dd-card" data-cat="school" onclick="sortCard2(this,'school')">club</span>
<span class="dd-card" data-cat="weekend" onclick="sortCard2(this,'weekend')">abroad</span>
<span class="dd-card" data-cat="school" onclick="sortCard2(this,'school')">volunteer</span>
<span class="dd-card" data-cat="weekend" onclick="sortCard2(this,'weekend')">enjoyable</span>
<span class="dd-card" data-cat="school" onclick="sortCard2(this,'school')">outdoor</span>
<span class="dd-card" data-cat="weekend" onclick="sortCard2(this,'weekend')">event</span>
<span class="dd-card" data-cat="school" onclick="sortCard2(this,'school')">station</span>
</div>
</div>
</div>
<div style="display:flex;gap:10px;flex-wrap:wrap">
<div class="dd-bin bin-1" style="flex:1;min-width:160px" id="bin-weekend">
<h4>🗺️ 周末活动</h4>
</div>
<div class="dd-bin bin-2" style="flex:1;min-width:160px" id="bin-school">
<h4>🏫 学校活动</h4>
</div>
</div>
<div class="game-feedback" id="dd-feedback2"><span class="feedback-label">提示：</span>点击词卡后选择正确的分类箱！</div>
</div>
</div>
'''

with open(target, 'a', encoding='utf-8') as f:
    f.write(pages_1_5)

print(f"Pages 1-5 appended. Current size: {os.path.getsize(target)} bytes")
