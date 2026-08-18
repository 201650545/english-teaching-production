#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build L19 courseware HTML - Pages 10-20."""

import os

target = r'D:\英语教学\邓兴华\第19课时\课件成品_网页PPT\第19课时_课件_中等.html'

pages_10_20 = r'''<!-- ===================== PAGE 10: 词汇矩阵 + 复合不定代词预览 ===================== -->
<div class="page" id="page10">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🗂️</span> 词汇矩阵 · 20词分类总览 + 复合不定代词预览</div>
<div class="data-table">
<tr><th>分类</th><th>单词</th><th>词性</th><th>核心释义</th></tr>
<tr><td rowspan="4">复合不定代词·指人</td><td>someone</td><td>pron.</td><td>某人</td></tr>
<tr><td>anyone</td><td>pron.</td><td>任何人</td></tr>
<tr><td>no one</td><td>pron.</td><td>没有人</td></tr>
<tr><td>everyone</td><td>pron.</td><td>每个人</td></tr>
<tr><td rowspan="4">复合不定代词·指物</td><td>something</td><td>pron.</td><td>某事/某物</td></tr>
<tr><td>anything</td><td>pron.</td><td>任何事物</td></tr>
<tr><td>nothing</td><td>pron.</td><td>没有什么</td></tr>
<tr><td>everything</td><td>pron.</td><td>一切</td></tr>
<tr><td rowspan="3">复合不定代词·指地点</td><td>somewhere</td><td>adv.</td><td>某个地方</td></tr>
<tr><td>anywhere</td><td>adv.</td><td>任何地方</td></tr>
<tr><td>nowhere</td><td>adv.</td><td>无处</td></tr>
<tr><td rowspan="5">周末活动与情感</td><td>abroad</td><td>adv.</td><td>在国外</td></tr>
<tr><td>event</td><td>n.</td><td>事件；活动</td></tr>
<tr><td>plan</td><td>n./v.</td><td>计划</td></tr>
<tr><td>explore</td><td>v.</td><td>探索</td></tr>
<tr><td>wonder</td><td>v.</td><td>想知道</td></tr>
<tr><td rowspan="4">情感与描述</td><td>seem</td><td>v.</td><td>似乎</td></tr>
<tr><td>bored</td><td>adj.</td><td>无聊的</td></tr>
<tr><td>diary</td><td>n.</td><td>日记</td></tr>
<tr><td>enjoyable</td><td>adj.</td><td>令人愉快的</td></tr>
</table>
<div class="rule-card rc-zhug"><div class="rc-cat">预览 <span class="rc-badge key">★ 重点记忆</span></div><div class="rc-text">
<strong>复合不定代词四大家族：</strong><br>
<span class="rc-chip">some-</span>（肯定） + <span class="rc-chip">any-</span>（否定/疑问） + <span class="rc-chip">no-</span>（全否定） + <span class="rc-chip">every-</span>（全包含）
</div></div>
</div>

<!-- ===================== PAGE 11: 词汇搭配连线 ===================== -->
<div class="page" id="page11">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🔗</span> 词汇搭配连线 · 英汉配对</div>
<div class="section-header"><span class="sh-icon">🎯</span><span class="sh-text">点击左边的词，再点击右边对应的释义，完成连线！</span></div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_11_0" data-knowledge-id="g49" data-section="core" data-template-id="G-LINK-RELATION" data-interaction-type="link" data-action-type="link" data-cognitive-level="retrieval" data-scorable="true">
<div class="link-container">
<div class="ec-grid">
<div class="ec-left link-left">
<div class="link-item" data-pair="1" onclick="linkClick(this)">someone</div>
<div class="link-item" data-pair="2" onclick="linkClick(this)">nothing</div>
<div class="link-item" data-pair="3" onclick="linkClick(this)">explore</div>
<div class="link-item" data-pair="4" onclick="linkClick(this)">enjoyable</div>
<div class="link-item" data-pair="5" onclick="linkClick(this)">diary</div>
</div>
<div class="ec-right link-right">
<div class="link-item" data-pair="1" onclick="linkClick(this)">某人</div>
<div class="link-item" data-pair="3" onclick="linkClick(this)">探索</div>
<div class="link-item" data-pair="5" onclick="linkClick(this)">日记</div>
<div class="link-item" data-pair="2" onclick="linkClick(this)">没有什么</div>
<div class="link-item" data-pair="4" onclick="linkClick(this)">令人愉快的</div>
</div>
</div>
</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_11_1" data-knowledge-id="g49" data-section="core" data-template-id="G-LINK-RELATION" data-interaction-type="link" data-action-type="link" data-cognitive-level="retrieval" data-scorable="true">
<div class="link-container">
<div class="ec-grid">
<div class="ec-left link-left">
<div class="link-item" data-pair="1" onclick="linkClick(this)">abroad</div>
<div class="link-item" data-pair="2" onclick="linkClick(this)">wonder</div>
<div class="link-item" data-pair="3" onclick="linkClick(this)">seem</div>
<div class="link-item" data-pair="4" onclick="linkClick(this)">bored</div>
<div class="link-item" data-pair="5" onclick="linkClick(this)">plan</div>
</div>
<div class="ec-right link-right">
<div class="link-item" data-pair="3" onclick="linkClick(this)">似乎</div>
<div class="link-item" data-pair="1" onclick="linkClick(this)">在国外</div>
<div class="link-item" data-pair="5" onclick="linkClick(this)">计划</div>
<div class="link-item" data-pair="4" onclick="linkClick(this)">无聊的</div>
<div class="link-item" data-pair="2" onclick="linkClick(this)">想知道</div>
</div>
</div>
</div>
</div>
</div>

<!-- ===================== PAGE 12: 拼写补全 ===================== -->
<div class="page" id="page12">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">📝</span> 拼写补全 · 根据释义填入缺失字母</div>
<div class="section-header"><span class="sh-icon">🎯</span><span class="sh-text">输入缺失的字母，拼出正确的单词！</span></div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_12_0" data-knowledge-id="g49" data-section="core" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="retrieval" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">1. some___ → 某人（填缺失部分）</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="one" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_12_1" data-knowledge-id="g49" data-section="core" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="retrieval" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">2. every____ → 一切（填缺失部分）</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="thing" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_12_2" data-knowledge-id="g49" data-section="core" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="retrieval" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">3. any____ → 任何地方（填缺失部分）</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="where" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_12_3" data-knowledge-id="g49" data-section="core" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="retrieval" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">4. no____ → 无处（填缺失部分）</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="where" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_12_4" data-knowledge-id="g49" data-section="core" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="retrieval" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">5. en___able → 令人愉快的（填缺失部分）</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="joy" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
</div>

<!-- ===================== PAGE 13: G49 P1 - 复合不定代词分类表 ===================== -->
<div class="page" id="page13">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🧩</span> G49 · 复合不定代词分类表（1/3）</div>
<div class="rule-card rc-qita"><div class="rc-cat">口诀 <span class="rc-badge key">★ 重点记忆</span></div><div class="rc-text">
"some 开头用于肯定，any 开头用于否定疑问；no 开头表示全否定，every 开头表示全都含"
</div></div>
<div class="data-table">
<tr><th>类别</th><th>指人</th><th>指物</th><th>指地点</th></tr>
<tr><td><strong>some-</strong>（肯定）</td><td>someone</td><td>something</td><td>somewhere</td></tr>
<tr><td><strong>any-</strong>（否定/疑问）</td><td>anyone</td><td>anything</td><td>anywhere</td></tr>
<tr><td><strong>no-</strong>（全否定）</td><td>no one</td><td>nothing</td><td>nowhere</td></tr>
<tr><td><strong>every-</strong>（全包含）</td><td>everyone</td><td>everything</td><td>everywhere</td></tr>
</table>
<div class="formula-box">
<div class="formula-title">核心规则</div>
<div class="formula-content">
some- → 肯定句 ✅<br>
any- → 否定句 ❌ / 疑问句 ❓<br>
no- → 全否定（= not any）<br>
every- → 全包含（= all）
</div>
</div>
<div class="example-sent"><span class="sent-label">some-</span> <strong>Someone</strong> is exploring the park.（肯定句，指人）</div>
<div class="example-sent"><span class="sent-label">any-</span> Is <strong>anyone</strong> planning to go abroad?（疑问句，指人）</div>
<div class="example-sent"><span class="sent-label">no-</span> <strong>No one</strong> is bored at the event.（全否定，指人）</div>
<div class="example-sent"><span class="sent-label">every-</span> <strong>Everyone</strong> seems happy today.（全包含，指人）</div>
<div class="rule-card rc-bin"><div class="rc-cat">螺旋关系 <span class="rc-badge key">★ 重点记忆</span></div><div class="rc-text">
<span class="rc-chip">G33 some/any</span><span class="rc-arw">→</span><span class="rc-chip">G49 复合不定代词</span><br>
<strong>some/any 规则升级：</strong>some+one/thing/where → someone/something/somewhere<br>
any+one/thing/where → anyone/anything/anywhere
</div></div>
</div>

<!-- ===================== PAGE 14: G49 P2 - 语义矩阵 ===================== -->
<div class="page" id="page14">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">📊</span> G49 · 复合不定代词语义辨析矩阵（2/3）</div>
<div class="data-table">
<tr><th>不定代词</th><th>语义</th><th>用法</th><th>示例</th></tr>
<tr><td>someone</td><td>某人</td><td>肯定句中用</td><td>Someone is calling you.</td></tr>
<tr><td>anyone</td><td>任何人</td><td>否定句/疑问句</td><td>Is anyone here? / I don't know anyone.</td></tr>
<tr><td>no one</td><td>没有人</td><td>全否定（= nobody）</td><td>No one knows the answer.</td></tr>
<tr><td>everyone</td><td>每个人</td><td>全包含（= everybody）</td><td>Everyone is happy.</td></tr>
<tr><td>something</td><td>某事</td><td>肯定句中用</td><td>I want something to drink.</td></tr>
<tr><td>anything</td><td>任何事</td><td>否定句/疑问句</td><td>Do you need anything?</td></tr>
<tr><td>nothing</td><td>没有什么</td><td>全否定（= not anything）</td><td>Nothing is impossible.</td></tr>
<tr><td>everything</td><td>一切</td><td>全包含（= all things）</td><td>Everything is fine.</td></tr>
</table>
<div class="tip-box"><div class="tip-title">💡 some- 也可用于疑问句</div><div class="tip-content">表示请求/邀请时，用 some- 而非 any-（螺旋自 G33）<br>Would you like <strong>something</strong> to drink?（请求，用 something ✅）<br>Can <strong>someone</strong> help me?（请求，用 someone ✅）</div></div>
<div class="rule-card rc-xing"><div class="rc-cat">易错 <span class="rc-badge warn">▲ 难点</span></div><div class="rc-text">
<div class="rc-err-row">❌ I don't know someone.</div><div class="rc-fix-row">✅ I don't know anyone.（否定句用 anyone）</div>
<div class="rc-err-row">❌ No one are here.</div><div class="rc-fix-row">✅ No one is here.（复合不定代词谓语用单数）</div>
<div class="rc-err-row">❌ Everyone have a plan.</div><div class="rc-fix-row">✅ Everyone has a plan.（谓语用单数）</div>
</div></div>
<div class="highlight-box">
<div class="hb-title">🔒 防越级约束</div>
<div class="hb-content">仅限基础复合不定代词（someone/anyone/no one/everyone/something/anything/nothing/everything/somewhere/anywhere/nowhere），不引入 everywhere（留至后续课复现）</div>
</div>
</div>

<!-- ===================== PAGE 15: G49 P3 - 不定代词探险器交互组件 ===================== -->
<div class="page" id="page15">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🧭</span> G49 · 不定代词探险器（3/3）</div>
<div class="section-header"><span class="sh-icon">🗺️</span><span class="sh-text">点击单元格，探索不同句型中的复合不定代词！</span></div>
<div class="explorer-grid">
<div class="explorer-cell" onclick="exHighlight(this)"><div class="ex-label">肯定句</div><div class="ex-word">someone</div><div class="ex-type">指人</div></div>
<div class="explorer-cell" onclick="exHighlight(this)"><div class="ex-label">肯定句</div><div class="ex-word">something</div><div class="ex-type">指物</div></div>
<div class="explorer-cell" onclick="exHighlight(this)"><div class="ex-label">肯定句</div><div class="ex-word">somewhere</div><div class="ex-type">指地点</div></div>
<div class="explorer-cell" onclick="exHighlight(this)"><div class="ex-label">肯定句</div><div class="ex-word">everything</div><div class="ex-type">全包含</div></div>
<div class="explorer-cell" onclick="exHighlight(this)"><div class="ex-label">疑问句</div><div class="ex-word">anyone</div><div class="ex-type">指人</div></div>
<div class="explorer-cell" onclick="exHighlight(this)"><div class="ex-label">疑问句</div><div class="ex-word">anything</div><div class="ex-type">指物</div></div>
<div class="explorer-cell" onclick="exHighlight(this)"><div class="ex-label">疑问句</div><div class="ex-word">anywhere</div><div class="ex-type">指地点</div></div>
<div class="explorer-cell" onclick="exHighlight(this)"><div class="ex-label">请求/邀请</div><div class="ex-word">someone</div><div class="ex-type">some- 特殊</div></div>
<div class="explorer-cell" onclick="exHighlight(this)"><div class="ex-label">否定句</div><div class="ex-word">no one</div><div class="ex-type">指人</div></div>
<div class="explorer-cell" onclick="exHighlight(this)"><div class="ex-label">否定句</div><div class="ex-word">nothing</div><div class="ex-type">指物</div></div>
<div class="explorer-cell" onclick="exHighlight(this)"><div class="ex-label">否定句</div><div class="ex-word">nowhere</div><div class="ex-type">指地点</div></div>
<div class="explorer-cell" onclick="exHighlight(this)"><div class="ex-label">全包含</div><div class="ex-word">everyone</div><div class="ex-type">指人</div></div>
</div>
<div class="quiz-container">
<div class="quiz-question">检测：I can't find my diary ____.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> somewhere</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> anywhere</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> everything</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>否定句（can't）→ 用 anywhere。G49 考点。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container">
<div class="quiz-question">检测：____ is impossible if you try hard.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> Anything</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> Nothing</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Something</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>"没有什么是不可能的" → Nothing is impossible. 全否定用 nothing。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
</div>

<!-- ===================== PAGE 16: G49 错句定位 ===================== -->
<div class="page" id="page16">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🔍</span> G49 · 错句定位 · 找出并改正错误</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_16_0" data-knowledge-id="g49" data-section="core" data-template-id="C-POINT-ERROR" data-interaction-type="single_choice" data-action-type="point" data-cognitive-level="retrieval" data-scorable="true">
<div class="quiz-question">1. 找出错误并改正：I don't know someone here.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">A</span> I don't know anyone here.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">B</span> I don't know everyone here.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> I don't know no one here.</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>否定句用 anyone，不用 someone。G49 考点。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_16_1" data-knowledge-id="g49" data-section="core" data-template-id="C-POINT-ERROR" data-interaction-type="single_choice" data-action-type="point" data-cognitive-level="retrieval" data-scorable="true">
<div class="quiz-question">2. 找出错误并改正：Do you need something for the trip?</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> Do you need someone for the trip?</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> Do you need anything for the trip?</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Do you need everything for the trip?</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>一般疑问句用 anything（非请求/邀请语境）。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_16_2" data-knowledge-id="g49" data-section="core" data-template-id="C-POINT-ERROR" data-interaction-type="single_choice" data-action-type="point" data-cognitive-level="retrieval" data-scorable="true">
<div class="quiz-question">3. 找出错误并改正：Everyone are planning something enjoyable.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> Everyone were planning something enjoyable.</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> Everyone is planning something enjoyable.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Everyone be planning something enjoyable.</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>复合不定代词作主语 → 谓语用单数 is，不是 are。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_16_3" data-knowledge-id="g49" data-section="core" data-template-id="C-POINT-ERROR" data-interaction-type="single_choice" data-action-type="point" data-cognitive-level="application" data-scorable="true">
<div class="quiz-question">4. 找出错误并改正：No one know the answer.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">A</span> No one knows the answer.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">B</span> No one knowing the answer.</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> No one is know the answer.</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>No one → 三单谓语 knows，不是 know。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
</div>

<!-- ===================== PAGE 17: G49 some/any 复合形式转换 P1 ===================== -->
<div class="page" id="page17">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🔄</span> G49 · some/any 复合形式转换（1/2）</div>
<div class="rule-card rc-zhug"><div class="rc-cat">同义转换 <span class="rc-badge key">★ 重点记忆</span></div><div class="rc-text">
<strong>no one = not anyone</strong>：No one knows. = I don't know anyone.<br>
<strong>nothing = not anything</strong>：I know nothing. = I don't know anything.
</div></div>
<div class="example-sent"><span class="sent-label">转换</span> <strong>No one</strong> is bored. = <strong>Nobody is</strong> bored. = I don't know <strong>anyone</strong> who is bored.</div>
<div class="example-sent"><span class="sent-label">转换</span> <strong>Nothing</strong> seems fun. = <strong>Not anything</strong> seems fun.</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_17_0" data-knowledge-id="g49" data-section="core" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="application" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">1. 同义转换：I know nothing. = I don't know ____.</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="anything" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_17_1" data-knowledge-id="g49" data-section="core" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="application" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">2. 同义转换：No one knows the answer. = I don't know ____ who knows the answer.</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="anyone" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
<div class="quiz-container">
<div class="quiz-question">3. 同义转换：There is nothing in the box. = There isn't ____ in the box.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> something</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> anything</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> everything</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>nothing = not anything，否定句用 anything。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
</div>

<!-- ===================== PAGE 18: G49 some/any 复合形式转换 P2 ===================== -->
<div class="page" id="page18">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">🔄</span> G49 · some/any 复合形式转换练习（2/2）</div>
<div class="quiz-container">
<div class="quiz-question">1. 将肯定句改为疑问句：Someone is calling you. → Is ____ calling you?</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> someone</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> anyone</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> everyone</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>肯定句 someone → 疑问句 anyone。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container">
<div class="quiz-question">2. 改为否定句：I want something to eat. → I don't want ____ to eat.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> something</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> anything</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> nothing</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>否定句用 anything，不用 something。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container" data-interaction-item="1" data-question-id="Q19_18_0" data-knowledge-id="g49" data-section="core" data-template-id="G-WRITE-FORM" data-interaction-type="fill_in" data-action-type="write" data-cognitive-level="application" data-scorable="true">
<div class="qq-text" style="margin-bottom:8px">3. 用 some- 填空（请求语境）：Would you like ____ to drink?</div>
<div class="fill-input-wrap">
<input class="fill-input" type="text" data-correct="something" placeholder="输入答案" autocomplete="off" onkeydown="if(event.key==='Enter'){event.preventDefault();checkFill(this);}">
<button class="fill-check-btn" onclick="checkFill(this)">确认</button>
</div>
</div>
<div class="quiz-container">
<div class="quiz-question">4. 选择：Can ____ help me?（请求语境）</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">A</span> someone</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">B</span> anyone</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> no one</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>请求/邀请语境用 some-，即使是疑问句也用 someone。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
</div>

<!-- ===================== PAGE 19: G49 选择练习 ===================== -->
<div class="page" id="page19">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">✏️</span> G49 · 复合不定代词选择练习</div>
<div class="quiz-container">
<div class="quiz-question">1. I want ____ interesting to read this weekend.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">A</span> something</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">B</span> anything</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> nothing</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>肯定句 → something。G49 考点。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container">
<div class="quiz-question">2. Is there ____ in the room?</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> someone</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> anyone</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> everyone</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>疑问句 → anyone。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container">
<div class="quiz-question">3. Let's go ____ fun this weekend!</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">A</span> somewhere</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">B</span> anywhere</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> nowhere</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>肯定句 → somewhere。指地点。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container">
<div class="quiz-question">4. ____ is ready for the event. We can start now.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> Something</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> Everything</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> Nothing</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>"一切准备好了" → Everything。全包含。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container">
<div class="quiz-question">5. I can't find my diary ____!</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> somewhere</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> anywhere</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> nothing</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>否定句 can't → anywhere。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
<div class="quiz-container">
<div class="quiz-question">6. She seems ____ today. She is smiling.</div>
<div class="quiz-options">
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">A</span> bored</button>
<button class="quiz-opt" data-correct="1" onclick="checkOpt(this)"><span class="opt-label">B</span> happy</button>
<button class="quiz-opt" data-correct="0" onclick="checkOpt(this)"><span class="opt-label">C</span> tired</button>
</div>
<div class="quiz-feedback"><span class="feedback-label">解析：</span>smiling → happy。seem + 形容词。</div>
<div class="undo-hint">答错后双击可撤销回答</div>
</div>
</div>

<!-- ===================== PAGE 20: 综合对比表 ===================== -->
<div class="page" id="page20">
<div style="display:flex;align-items:center;gap:8px;margin-bottom:8px"><span class="priority-badge core">CORE · 课堂必做</span></div>
<div class="page-title"><span class="title-icon">📊</span> 综合对比表 · some/any vs 复合不定代词</div>
<div class="data-table">
<tr><th>对比项</th><th>some/any 基础（G33）</th><th>复合不定代词（G49）</th><th>关系</th></tr>
<tr><td>肯定句</td><td>some water</td><td>someone / something / somewhere</td><td>some + one/thing/where</td></tr>
<tr><td>否定句</td><td>any water</td><td>anyone / anything / anywhere</td><td>any + one/thing/where</td></tr>
<tr><td>疑问句</td><td>any water</td><td>anyone / anything / anywhere</td><td>同上</td></tr>
<tr><td>请求/邀请</td><td>some water?</td><td>something / someone?</td><td>疑问句也用 some-</td></tr>
<tr><td>全否定</td><td>no water</td><td>no one / nothing / nowhere</td><td>no + one/thing/where</td></tr>
<tr><td>全包含</td><td>all water</td><td>everyone / everything</td><td>every + one/thing</td></tr>
</table>
<div class="rule-card rc-bin"><div class="rc-cat">核心规律 <span class="rc-badge key">★ 重点记忆</span></div><div class="rc-text">
<strong>some/any 规则不变，只是后面加了 one/thing/where：</strong><br>
✅ some → someone, something, somewhere（肯定句 / 请求疑问句）<br>
✅ any → anyone, anything, anywhere（否定句 / 疑问句）<br>
✅ no → no one, nothing, nowhere（全否定）<br>
✅ every → everyone, everything（全包含）
</div></div>
<div class="example-sent"><span class="sent-label">对比</span> I have <strong>some</strong> water. → I have <strong>something</strong> to drink.</div>
<div class="example-sent"><span class="sent-label">对比</span> Do you have <strong>any</strong> water? → Do you have <strong>anything</strong> to drink?</div>
<div class="example-sent"><span class="sent-label">对比</span> I have <strong>no</strong> water. → I have <strong>nothing</strong> to drink.</div>
</div>
'''

with open(target, 'a', encoding='utf-8') as f:
    f.write(pages_10_20)

print(f"Pages 10-20 appended. Current size: {os.path.getsize(target)} bytes")
