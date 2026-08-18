# -*- coding: utf-8 -*-
"""邓兴华 L25 授课课件（动名词与不定式综合运用 · 八段式 · ~44 页）生成脚本"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "00_工具"))
import build_dxh_l21_25 as B

out_dir = os.path.join(HERE, "课件成品_网页PPT")
os.makedirs(out_dir, exist_ok=True)

NAV = """<div class="nav-bar">
  <div class="nav-item" data-segment="1" onclick="jumpToSegment(1)"><span class="nav-num">①</span>复习导入</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="2" onclick="jumpToSegment(2)"><span class="nav-num">②</span>新词20</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="3" onclick="jumpToSegment(3)"><span class="nav-num">③</span>动名词</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="4" onclick="jumpToSegment(4)"><span class="nav-num">④</span>不定式</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="5" onclick="jumpToSegment(5)"><span class="nav-num">⑤</span>辨析</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="6" onclick="jumpToSegment(6)"><span class="nav-num">⑥</span>随堂演练</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="7" onclick="jumpToSegment(7)"><span class="nav-num">⑦</span>阅读</div>
  <div class="nav-separator"></div>
  <div class="nav-item" data-segment="8" onclick="jumpToSegment(8)"><span class="nav-num">⑧</span>总结</div>
</div>"""

pages = {}
seg = {}
p = 1
def add(inner, seg_id, t="", sub=""):
    global p
    pages[p] = B._pg(p, t, sub, inner, active=(p == 1))
    seg.setdefault(seg_id, [p, p])
    seg[seg_id][1] = p
    p += 1

STAGE = "Stage 6 · L25"

# ================= ① 复习导入（3页） =================
add('<div class="cover-wrap"><div class="cover-badge">Stage 6 · 八上主线</div>'
    '<div class="cover-title">动名词 · 不定式综合运用</div>'
    '<div class="cover-sub">G62 V-ing 作主语/宾语 + G63 to do 作宾语/目的</div>'
    '<div class="cover-tagline">授课课 · 八段式</div>'
    '<div class="cover-info"><div class="cover-info-num"><div class="ci-label">新词</div><div class="ci-val">20</div></div>'
    '<div class="cover-info-num"><div class="ci-label">考点</div><div class="ci-val">3</div></div>'
    '<div class="cover-info-num"><div class="ci-label">词号</div><div class="ci-val">481–500</div></div>'
    '<div class="cover-info-num"><div class="ci-label">时长</div><div class="ci-val">90分</div></div></div>'
    '<div class="cover-emoji">🎯</div></div>', 1, "L25 动名词不定式", "八上动词非谓语主线")

add(B.section_head("复", "上一课状语从句回顾", "L24 衔接")
    + B.rule_cards([("zhug", "L24 考点", "原因 because/since/as、让步 although/though、结果 so、目的 so that。"),
                    ("bin", "本课衔接", "L24 讲连词，L25 转到动词后接 doing 与 to do 的用法。")])
    + B.quiz_html([("because 表？", "原因", ["结果", "让步"]),
                   ("so that 表？", "目的", ["原因", "让步"])])
    + B.note_panel("L25 起点", "今天学动词后面接什么：有的跟 doing，有的跟 to do。这是初中非谓语的核心。"), 1, "复习导入", "L24 衔接")

add(B.section_head("复", "动词后接 · 前瞻", "新旧衔接")
    + B.rule_cards([("warn", "两类动词", "enjoy/finish/mind 等后接 doing；want/decide/hope 等后接 to do。"),
                    ("xing", "避免混用", "enjoy to read 是错的，应为 enjoy reading；decided doing 是错的，应为 decided to do。")])
    + B.quiz_html([("enjoy 后接？", "doing", ["to do", "原形"]),
                   ("want 后接？", "to do", ["doing", "原形"])])
    + B.sub_label("今天把 doing 与 to do 两条线一次梳理"), 1, "前瞻", "动词接续概念")

add(B.section_head("复", "本课学习目标", "目标导航")
    + B.note_panel("本课 3 大考点", "① G62 动名词 V-ing 作主语与宾语 ② G63 不定式 to do 作宾语与目的状语 ③ stop/remember doing vs to do 辨析。")
    + B.rule_cards([("qita", "学习动作", "看规则 → 填空自检 → 拖拽分类 → 阅读应用 → 口诀收尾。"),
                    ("ming", "防越级", "不引入分词作状语（如 Seeing from the hill）。")])
    + B.quiz_html([("本课语法主线是？", "动名词与不定式", ["定语从句", "被动语态"])])
    + B.ext_card("前后衔接", "L24 状语从句收尾，L25 动词非谓语新开；L26 起继续深入。"), 1, "学习目标", "目标导航")

# ================= ② 新词 20（8页） =================
add(B.section_head("词", "新词① · 爱好动名词", "词 481–485")
    + B.vocab_cards([
        (("enjoy", "/ɪnˈdʒɔɪ/", "v.", "享受；喜欢", "enjoy doing", "I enjoy reading books.")),
        (("finish", "/ˈfɪnɪʃ/", "v.", "完成", "finish doing", "I finished writing the letter.")),
        (("mind", "/maɪnd/", "v./n.", "介意；心思", "mind doing / never mind", "Do you mind opening the door?")),
        (("practice", "/ˈpræktɪs/", "v./n.", "练习", "practice doing", "He practices playing the piano.")),
        (("suggest", "/səˈdʒest/", "v.", "建议", "suggest doing", "I suggest going early."))]), 2, "新词① 爱好动名词", "词 481–485")

add(B.section_head("词", "新词② · 动名词类", "词 486–490")
    + B.vocab_cards([
        (("avoid", "/əˈvɔɪd/", "v.", "避免", "avoid doing", "Avoid making the same mistake.")),
        (("consider", "/kənˈsɪdə(r)/", "v.", "考虑", "consider doing", "Consider joining the club.")),
        (("imagine", "/ɪˈmædʒɪn/", "v.", "想象", "imagine doing", "Imagine flying in the sky.")),
        (("decide", "/dɪˈsaɪd/", "v.", "决定", "decide to do", "I decided to study harder.")),
        (("hope", "/həʊp/", "v./n.", "希望", "hope to do / hope that", "I hope to see you again."))]), 2, "新词② 动名词类", "词 486–490")

add(B.section_head("词", "新词③ · 计划不定式", "词 491–495")
    + B.vocab_cards([
        (("plan", "/plæn/", "v./n.", "计划", "plan to do", "We plan to travel.")),
        (("want", "/wɒnt/", "v.", "想要", "want to do / want sth.", "I want to learn English.")),
        (("need", "/niːd/", "v.", "需要", "need to do / need doing", "You need to rest.")),
        (("agree", "/əˈɡriː/", "v.", "同意", "agree to do / agree with", "He agreed to help me.")),
        (("refuse", "/rɪˈfjuːz/", "v.", "拒绝", "refuse to do", "She refused to go."))]), 2, "新词③ 计划不定式", "词 491–495")

add(B.section_head("词", "新词④ · 承诺不定式", "词 496–500")
    + B.vocab_cards([
        (("promise", "/ˈprɒmɪs/", "v./n.", "承诺", "promise to do / make a promise", "He promised to come.")),
        (("manage", "/ˈmænɪdʒ/", "v.", "设法做成", "manage to do", "She managed to finish it.")),
        (("afford", "/əˈfɔːd/", "v.", "负担得起", "afford to do", "I can't afford to buy it.")),
        (("offer", "/ˈɒfə(r)/", "v./n.", "提供", "offer to do / offer sth.", "He offered to help.")),
        (("fail", "/feɪl/", "v.", "失败", "fail to do / fail a test", "Don't fail to call me."))])
    + B.note_panel("记忆小贴士", "后接 to do 的动词常表'打算/希望/承诺/拒绝'：plan/want/hope/decide/agree/refuse/promise。")
    + B.ext_card("培优搭配", "manage to do（设法做成）、afford to do（负担得起）、offer to do（主动提供做）。")
    + B.quiz_html([("manage 后接？", "to do", ["doing", "原形"]),
                   ("afford to do 意思是？", "负担得起做某事", ["拒绝做某事", "忘记做某事"]),
                   ("offer to do 意思是？", "主动提供做", ["被迫做", "犹豫做"])]), 2, "新词④ 承诺不定式", "词 496–500")

add(B.section_head("词", "新词游戏① · 词义翻牌", "翻牌自检")
    + B.sub_label("点击翻牌，看英文想中文，再翻回核对")
    + B.flip_grid([
        ("enjoy", "享受"), ("finish", "完成"), ("mind", "介意"),
        ("suggest", "建议"), ("avoid", "避免"), ("consider", "考虑"),
        ("imagine", "想象"), ("decide", "决定"), ("hope", "希望"),
        ("refuse", "拒绝"), ("promise", "承诺"), ("manage", "设法")])
    + B.sub_label("自检一题")
    + B.quiz_html([("suggest 后接？", "doing", ["to do", "原形"])]), 2, "词汇游戏①", "翻牌自检")

add(B.section_head("词", "新词游戏② · 拖拽归位", "拖拽")
    + B.sub_label("把词块拖到正确的解释前面")
    + B.drag_q([("享受 → ", "enjoy", ""),
                ("完成 → ", "finish", ""),
                ("拒绝 → ", "refuse", "")],
               ["enjoy", "finish", "refuse"])
    + B.sub_label("自检一题")
    + B.quiz_html([("'manage to do' 意思是？", "设法做成", ["放弃做", "忘记做"])]), 2, "词汇游戏②", "拖拽归位")

add(B.section_head("词", "新词游戏③ · 连线配对", "连线")
    + B.sub_label("把英文词与正确释义连起来")
    + B.match_q([("enjoy", "享受"), ("refuse", "拒绝"), ("promise", "承诺")],
                [("享受", "enjoy"), ("拒绝", "refuse"), ("承诺", "promise")])
    + B.sub_label("左右两列点击配对"), 2, "词汇游戏③", "连线配对")

add(B.section_head("词", "新词游戏④ · 选择演练", "选择")
    + B.sub_label("20 词综合选择")
    + B.quiz_html([("'完成' 是？", "finish", ["mind", "enjoy"]),
                   ("'避免' 是？", "avoid", ["refuse", "offer"]),
                   ("'考虑' 是？", "consider", ["imagine", "promise"]),
                   ("'负担得起' 是？", "afford", ["manage", "fail"]),
                   ("'设法做成' 是？", "manage", ["offer", "refuse"]),
                   ("'放弃做' 用哪个？（反义）", "avoid", ["enjoy", "promise"])])
    + B.ext_card("词汇记忆", "动名词动词：enjoy/finish/mind/practice/suggest/avoid/consider/imagine；不定式动词：decide/hope/plan/want/need/agree/refuse/promise/manage/afford/offer/fail。")
    + B.quiz_html([("哪些词后接 doing？", "enjoy/finish/mind", ["want/decide/hope", "plan/agree/refuse"]),
                   ("'希望' 的英文是？", "hope", ["offer", "fail"]),
                   ("后接 to do 的动词常表？", "打算/希望/承诺", ["爱好/习惯", "动作持续的"])]), 2, "词汇游戏④", "选择演练")

# ================= ③ 动名词 G62（5页） =================
add(B.section_head("语", "动名词 V-ing 作主语", "G62 规则")
    + B.rule_cards([("zhug", "作主语谓语单数", "V-ing 开头作主语，谓语动词用单数：Reading is fun.。"),
                    ("xing", "例句", "Reading books is good for us.（读书对我们有好处。）谓语 is 用单数。"),
                    ("warn", "易错", "❌ Reading are fun → ✅ Reading is fun（动名词作主语谓语单数）。")])
    + B.quiz_html([("动名词作主语谓语用？", "单数", ["复数", "原形"]),
                   ("'Reading ____ fun.' 填？", "is", ["are", "am"]),
                   ("动名词由什么构成？", "动词加 ing", ["动词加 ed", "动词原形"])]), 3, "动名词作主语", "G62 规则")

add(B.section_head("语", "enjoy/finish/mind + doing", "G62 宾语")
    + B.rule_cards([("zhug", "后接 doing", "enjoy/finish/mind/practice/suggest/avoid/consider/imagine + doing。"),
                    ("xing", "例句", "I enjoy reading. / He finished writing. / Do you mind opening the door?")])
    + B.quiz_html([("enjoy 后接？", "doing", ["to do", "原形"]),
                   ("mind 后接？", "doing", ["to do", "原形"]),
                   ("suggest + ____.", "doing", ["to do", "原形"]),
                   ("consider + ____.", "doing", ["to do", "原形"])]), 3, "doing 宾语", "G62 宾语")

add(B.section_head("语", "动名词 · 补全填空", "G62 练习")
    + B.fill_q("I enjoy ____ (read) books.", "reading")
    + B.fill_q("He finished ____ (write) the letter.", "writing")
    + B.fill_q("Do you mind ____ (open) the door?", "opening")
    + B.sub_label("点击检查，enjoy/finish/mind 后接 doing")
    + B.note_panel("填空一步到位", "看到 enjoy/finish/mind/practice/suggest/avoid 等动词，后面直接接 doing。动词加 ing 时注意拼写：write→writing（去 e）、run→running（双写）。"), 3, "动名词填空", "G62 练习")

add(B.section_head("语", "动名词 · 拖拽成句", "G62 应用")
    + B.sub_label("把词块按正确顺序拖入组成动名词句")
    + B.drag_q([("I enjoy ", "reading", " books."),
                ("He finished ", "writing", " the letter.")],
               ["reading", "writing"])
    + B.sub_label("自检一题")
    + B.quiz_html([("'喜欢游泳' 用 enjoy 应接？", "swimming", ["to swim", "swim"]),
                   ("'读完书' 用 finish 应接？", "reading", ["to read", "read"])]), 3, "动名词成句", "G62 应用")

add(B.section_head("语", "动名词 · 关键词地图", "考点梳理")
    + B.kmap_block("动名词三大关键词", [
        ("作主语", "V-ing 谓语单数"),
        ("后接 doing", "enjoy/finish/mind 等"),
        ("拼写", "去 e / 双写 ing")])
    + B.sub_label("自检一题")
    + B.quiz_html([("动名词作主语谓语用单数，对吗？", "对", ["错", "不一定"]),
                   ("run 的动名词是？", "running", ["runing", "run"]),
                   ("write 的动名词是？", "writing", ["writeing", "writting"])])
    + B.ext_card("螺旋递进", "G47（L18）已学 V-ing 变化规则，G62 本课首次用于作主语/宾语。"), 3, "动名词地图", "关键词")

# ================= ④ 不定式 G63（5页） =================
add(B.section_head("语", "不定式 to do 作宾语", "G63 规则")
    + B.rule_cards([("zhug", "后接 to do", "want/decide/hope/plan/agree/refuse/promise/manage/afford/offer/fail/need + to do。"),
                    ("xing", "例句", "I want to learn English. / He decided to study harder. / She managed to finish it."),
                    ("warn", "易错", "❌ I decided doing → ✅ I decided to do（decide 后接 to do）。")])
    + B.quiz_html([("want 后接？", "to do", ["doing", "原形"]),
                   ("decide 后接？", "to do", ["doing", "原形"]),
                   ("hope 后接？", "to do", ["doing", "原形"]),
                   ("promise 后接？", "to do", ["doing", "原形"])]), 4, "不定式宾语", "G63 规则")

add(B.section_head("语", "不定式 to do 作目的状语", "G63 目的")
    + B.rule_cards([("zhug", "表目的", "to do 表目的，译'为了'：He came to help me.。"),
                    ("xing", "例句", "She got up early to catch the bus.（她早起为了赶公交。）"),
                    ("warn", "注意", "目的状语用 to do，不用 doing。")])
    + B.quiz_html([("'为了' 用？", "to do", ["doing", "原形"]),
                   ("He came ____ help me.", "to", ["ing", "for doing"]),
                   ("目的状语用 to do 还是 doing？", "to do", ["doing", "两者皆可"])]), 4, "不定式目的", "G63 目的")

add(B.section_head("语", "不定式 · 补全填空", "G63 练习")
    + B.fill_q("I want ____ (learn) English.", "to learn")
    + B.fill_q("He decided ____ (study) harder.", "to study")
    + B.fill_q("She got up early ____ (catch) the bus.", "to catch")
    + B.sub_label("点击检查，want/decide 后接 to do，目的用 to do")
    + B.note_panel("填空一步到位", "看到 want/decide/hope/plan/agree/refuse 等动词后接 to do。表目的也写 to do。"),
     4, "不定式填空", "G63 练习")

add(B.section_head("语", "不定式 · 排序成句", "G63 应用")
    + B.order_q("把词块排成正确的不定式句子",
                [("I", "主语"), ("want", "动词"), ("to learn", "to do"), ("English", "宾语")],
                "I|want|to learn|English")
    + B.sub_label("自检一题")
    + B.quiz_html([("'他设法完成了' 用 manage 应接？", "to finish", ["finishing", "finish"]),
                   ("'我希望再见你' 用 hope 应接？", "to see", ["seeing", "see"])]), 4, "不定式排序", "G63 应用")

add(B.section_head("语", "不定式 · 关键词地图", "考点梳理")
    + B.kmap_block("不定式三大关键词", [
        ("后接 to do", "want/decide/hope 等"),
        ("表目的", "to do 译'为了'"),
        ("四阶链", "G15→G18→G34→G63")])
    + B.sub_label("自检一题")
    + B.quiz_html([("不定式的基本形式是？", "to + 动词原形", ["动词+ing", "动词+ed"]),
                   ("'agree to do' 意思是？", "同意做", ["拒绝做", "考虑做"])])
    + B.ext_card("螺旋递进", "to do 四阶链终点：G15（L5）like to do → G18（L6）want to do → G34（L13）would like to do → G63（L25）系统归纳。"), 4, "不定式地图", "关键词")

# ================= ⑤ doing/to do 辨析 G63 扩展（4页） =================
add(B.section_head("语", "stop doing vs. stop to do", "G63 辨析")
    + B.rule_cards([("zhug", "stop doing", "停止正在做的事：He stopped talking.（他停止说话。）"),
                    ("xing", "stop to do", "停下来去做另一件事：He stopped to rest.（他停下来休息。）"),
                    ("warn", "易错", "❌ stop to talk 误用（stop talking 才是停止说话）。")])
    + B.quiz_html([("'He stopped talking.' 意思是？", "他停止说话", ["他停下来去说话", "他一直在说话"]),
                   ("'stop to rest' 意思是？", "停下来休息", ["停止休息", "继续休息"]),
                   ("stop 后接 doing 表？", "停止某事", ["开始某事", "去做某事"])]), 5, "stop辨析", "G63 扩展")

add(B.section_head("语", "remember doing vs. remember to do", "G63 辨析")
    + B.rule_cards([("zhug", "remember doing", "记得做过：I remember seeing him.（我记得见过他。）"),
                    ("xing", "remember to do", "记得要去做：Remember to lock the door.（记得锁门。）"),
                    ("warn", "易错", "❌ remember to do 误用（remember to do 是记得将要做）。")])
    + B.quiz_html([("'remember to do' 意思是？", "记得要做", ["记得做过", "忘记做"]),
                   ("'remember doing' 意思是？", "记得做过", ["记得要做", "不想做"]),
                   ("Remember ____ the door. 填？", "to lock", ["locking", "lock"])]), 5, "remember辨析", "G63 扩展")

add(B.section_head("语", "doing/to do · 连线互换", "G63 连线")
    + B.match_q([("stop doing", "停止某事"), ("stop to do", "停下来去做"), ("remember doing", "记得做过"), ("remember to do", "记得要做")],
                [("停止某事", "stop doing"), ("停下来去做", "stop to do"), ("记得做过", "remember doing"), ("记得要做", "remember to do")])
    + B.sub_label("左右两列点击配对"), 5, "辨析连线", "G63 连线")

add(B.section_head("语", "doing/to do · 双列选择", "G63 辨析")
    + B.quiz_html([("I enjoy ____ (read) books.", "reading", ["to read", "read"]),
                   ("I want ____ (learn) English.", "to learn", ["learning", "learn"]),
                   ("He stopped ____ (smoke).", "smoking", ["to smoke", "smoke"]),
                   ("Remember ____ (call) me later.", "to call", ["calling", "call"])])
    + B.ext_card("辨析", "enjoy/finish/mind 后 doing；want/decide/hope 后 to do；stop/remember 后 doing 与 to do 意思不同。"), 5, "辨析双列", "G63 辨析")

# ================= ⑥ 随堂演练（4页） =================
add(B.section_head("练", "动词接续 · 选择演练", "单选")
    + B.quiz_html([("I enjoy ____ basketball.", "playing", ["to play", "play"]),
                   ("He decided ____ harder.", "to study", ["studying", "study"]),
                   ("She practices ____ the piano.", "playing", ["to play", "play"]),
                   ("We plan ____ next week.", "to travel", ["traveling", "travel"])])
    + B.note_panel("解题步骤", "①看动词 ②判断后接 doing 还是 to do ③按规则选。enjoy/practice 后 doing，decide/plan 后 to do。"), 6, "随堂演练", "选择")

add(B.section_head("练", "动词接续 · 填空演练", "填空")
    + B.fill_q("I want ____ (be) a doctor.", "to be")
    + B.fill_q("He finished ____ (do) his homework.", "doing")
    + B.fill_q("She enjoys ____ (sing).", "singing")
    + B.sub_label("点击检查"), 6, "随堂演练", "填空")

add(B.section_head("练", "动词接续 · 拖拽分类", "拖拽")
    + B.sub_label("把动词拖到正确的接续规则下（doing / to do）")
    + B.drag_q([("后接 doing：", "enjoy", "后接 to do："),
                ("", "decide", ""),
                ("", "finish", ""),
                ("", "hope", "")],
               ["enjoy", "finish", "decide", "hope"])
    + B.sub_label("点击检查，enjoy/finish 后 doing，decide/hope 后 to do"), 6, "随堂演练", "拖拽")

add(B.section_head("练", "动词接续 · 综合混练", "综合")
    + B.quiz_html([("I enjoy ____ (read) at night.", "reading", ["to read", "read"]),
                   ("He wants ____ (go) to the park.", "to go", ["going", "go"]),
                   ("She finished ____ (clean) the room.", "cleaning", ["to clean", "clean"]),
                   ("They decided ____ (leave) early.", "to leave", ["leaving", "leave"])])
    + B.sub_label("点击作答，四题全对才算掌握")
    + B.note_panel("综合审题三步", "①找动词 ②判断接 doing 还是 to do ③判断时态与拼写。把四题连起来读一遍，验证通顺。")
    + B.body_text("本课综合运用：enjoy/finish/mind 后 doing，want/decide/hope 后 to do。"
                  "做题时先找到动词，再套接续规则，特别留意 stop/remember 后的 doing 与 to do 意思不同。"), 6, "随堂演练", "综合")

# ================= ⑦ 阅读理解（5页） =================
add(B.section_head("读", "阅读 A 篇 · My Hobbies and Future Plans", "说明文")
    + B.sub_label("说明文：我的爱好与未来计划（约 194 词）")
    + B.body_text("I enjoy reading and playing chess. "
                  "Reading helps me learn new things, and playing chess trains my mind. "
                  "I often practice playing the piano after school. "
                  "I want to be a musician in the future. "
                  "My parents suggest practicing every day. "
                  "I decide to make a plan to improve my skills. "
                  "I hope to join a music club next term. "
                  "I promise to work hard and never give up. "
                  "I also plan to learn another language. "
                  "In short, I enjoy learning and I want to grow every day.")
    + B.rule_cards([("bin", "主旨", "作者介绍爱好（阅读/象棋/钢琴）与未来计划（当音乐家）。")])
    + B.quiz_html([("作者喜欢做什么？", "阅读和下棋", ["游泳和跑步", "画画和唱歌"]),
                   ("作者想成为什么？", "音乐家", ["医生", "老师"]),
                   ("enjoy 后接什么？", "doing", ["to do", "原形"]),
                   ("'I hope to join' 中 to join 表？", "希望做", ["已经做", "正在做"])])
    + B.note_panel("说明文信息定位", "说明文按爱好→计划展开。逐题回原文找 enjoy/practice/want/hope/plan 等动词，判断接 doing 还是 to do。")
    + B.fill_q("我想成为一名音乐家。I want ____ (be) a musician.", "to be")
    + B.quiz_html([("'I promise to work hard' 中 promise to do 表？", "承诺做", ["拒绝做", "忘记做"]),
                   ("作者还计划做什么？", "学另一门语言", ["换一个爱好", "放弃钢琴"])]), 7, "阅读 A 篇", "爱好计划")

add(B.section_head("读", "阅读 B 篇 · A Promise to My Friend", "记叙文")
    + B.sub_label("记叙文：给朋友的一个承诺（约 215 词）")
    + B.body_text("My friend Tom and I agreed to run a race together. "
                  "We promised to train every day. "
                  "At first, I wanted to give up because it was hard. "
                  "But Tom suggested keeping on running. "
                  "He said, 'Remember to rest well before the race.' "
                  "I decided to trust him and keep trying. "
                  "We managed to finish the race together. "
                  "I felt happy and I learned never to refuse a challenge. "
                  "Now I remember doing my best every time. "
                  "This experience taught me the value of promise.")
    + B.rule_cards([("bin", "人物", "作者与朋友 Tom 约定赛跑，通过坚持最终完成。")])
    + B.quiz_html([("作者与朋友约定做什么？", "赛跑", ["游泳", "画画"]),
                   ("Tom 建议作者？", "继续跑", ["放弃", "换人"]),
                   ("'Remember to rest' 意思是？", "记得休息", ["记得休息过", "别休息"]),
                   ("'managed to finish' 意思是？", "设法完成", ["拒绝完成", "忘记完成"])])
    + B.fill_q("我决定信任他。I decided ____ (trust) him.", "to trust")
    + B.sub_label("点击检查")
    + B.note_panel("记叙文信息定位", "记叙文按事件推进。逐题回原文找 agree/promise/want/suggest/decide/manage 等动词与人物情感。")
    + B.quiz_html([("'I remember doing my best' 意思是？", "记得努力过", ["记得要努力", "不想努力"]),
                   ("作者从这次经历学到？", "承诺的价值", ["赛跑的技巧", "跑步的速度"])]), 7, "阅读 B 篇", "承诺")

add(B.section_head("读", "阅读 C 篇 · Why I Love Doing Sports", "说明文")
    + B.sub_label("说明文：为什么我爱运动（约 215 词）")
    + B.body_text("I love doing sports because it makes me strong and happy. "
                  "I enjoy playing football with my friends every weekend. "
                  "We practice kicking and passing the ball. "
                  "My coach suggests doing warm-up exercises first. "
                  "He tells me to drink enough water and to rest well. "
                  "I want to be on the school team. "
                  "I hope to win a game one day. "
                  "I need to train hard to achieve my dream. "
                  "I promise to keep going even when it is hard. "
                  "Doing sports teaches me to work with others.")
    + B.rule_cards([("xing", "主旨", "作者爱运动，享受足球，希望进入校队并坚持训练。")])
    + B.quiz_html([("作者为什么爱运动？", "变强壮且快乐", ["变忙碌", "变紧张"]),
                   ("教练建议先做什么？", "热身运动", ["直接比赛", "休息一天"]),
                   ("'I want to be on the team' 中 to be 表？", "想要成为", ["已经是", "曾经是"]),
                   ("作者需要做什么来实现梦想？", "努力训练", ["放弃", "休息"])])
    + B.note_panel("原因结构", "说明文用 because 说明原因，用 to do 表目的。找 because 定位原因，找 to do 定位目的。")
    + B.fill_q("我需要努力训练以实现梦想。I need ____ (train) hard to achieve my dream.", "to train")
    + B.quiz_html([("'Doing sports teaches me' 中 Doing sports 作？", "主语", ["宾语", "谓语"]),
                   ("运动教会作者？", "与人合作", ["独自行动", "放弃"])]), 7, "阅读 C 篇", "运动")

add(B.section_head("读", "阅读 · 五选四", "语篇填空")
    + B.sub_label("Planning for the Future 语篇填空（5 空 4 选）")
    + B.rule_cards([("bin", "提示", "根据上下文逻辑选择正确的句子，注意 to do 表目的、doing 表爱好。")])
    + B.order_q("把计划步骤按正确顺序排列",
                [("First", "首先"), ("Then", "然后"), ("Finally", "最后")],
                "First|Then|Finally")
    + B.sub_label("自检一题")
    + B.quiz_html([("五选四中 'to do' 常表示？", "目的/打算", ["并列", "让步"])])
    + B.ext_card("衔接词", "计划类：first/then/finally；因果：because/so；目的：to do/so that。"), 7, "阅读五选四", "语篇填空")

add(B.section_head("读", "阅读策略 · 动词接续定位", "策略")
    + B.kmap_block("动词接续阅读三步法", [
        ("划动词", "找出 enjoy/want/decide 等"),
        ("判接续", "doing 还是 to do"),
        ("定位", "回原文找对应句子")])
    + B.body_text("阅读动词接续类文章时，先划动词，再判断后接 doing 还是 to do，最后回原文定位。")
    + B.quiz_html([("enjoy 引导的是？", "后接 doing", ["后接 to do", "后接原形"]),
                   ("want 引导的是？", "后接 to do", ["后接 doing", "后接原形"])])
    + B.note_panel("常见设问", "What does sb. enjoy doing?（找 enjoy+doing）/ What does sb. want to do?（找 want+to do）。"), 7, "阅读策略", "动词定位")

# ================= 句子练习（3页） =================
add(B.section_head("句", "造句 · enjoy doing", "句子练习")
    + B.rule_cards([("zhug", "句型", "主语 + enjoy + doing。")])
    + B.fill_q("我喜欢读书。I enjoy ____ (read) books.", "reading")
    + B.sub_label("点击检查，enjoy 后接 doing")
    + B.body_text("参考：<b>I enjoy reading books.</b>（我喜欢读书。）"
                  "技巧：enjoy 后动词加 ing 构成动名词。若动词以 e 结尾去 e 加 ing（write→writing），"
                  "重读闭音节双写（run→running）。")
    + B.quiz_html([("'享受游泳' 用 enjoy 应接？", "swimming", ["to swim", "swim"]),
                   ("'完成作业' 用 finish 应接？", "doing", ["to do", "do"]),
                   ("'介意开门吗' 用 mind 应接？", "opening", ["to open", "open"])]), 7, "造句enjoy", "句子练习")

add(B.section_head("句", "汉译英 · want to do", "句子练习")
    + B.rule_cards([("zhug", "句型", "主语 + want + to do。")])
    + B.fill_q("我想学英语。I want ____ (learn) English.", "to learn")
    + B.sub_label("点击检查，want 后接 to do")
    + B.body_text("参考：<b>I want to learn English.</b>（我想学英语。）"
                  "技巧：want/decide/hope/plan 后接 to do 表'打算/希望'。"
                  "注意 want 后若接名词则不加 to：want a book（想要一本书）。")
    + B.quiz_html([("'决定更努力学习' 用 decide 应接？", "to study", ["studying", "study"]),
                   ("'希望赢' 用 hope 应接？", "to win", ["winning", "win"]),
                   ("want 后接名词时加 to 吗？", "不加", ["加", "看情况"])]), 7, "汉译英want", "句子练习")

add(B.section_head("句", "汉译英 · remember to do", "句子练习")
    + B.rule_cards([("zhug", "句型", "remember to do（记得要做）/ remember doing（记得做过）。")])
    + B.fill_q("记得锁门。Remember ____ (lock) the door.", "to lock")
    + B.sub_label("点击检查，remember to do 表记得将要做")
    + B.body_text("参考：<b>Remember to lock the door.</b>（记得锁门。）"
                  "区别：remember to do 记得要做（未做）；remember doing 记得做过（已做）。"
                  "I remember locking the door.（我记得锁过门。）")
    + B.quiz_html([("'Remember ____ the light'（记得关灯，未关）填？", "to turn off", ["turning off", "turn off"]),
                   ("'我记得见过他' 用 remember ____ him.", "seeing", ["to see", "see"]),
                   ("remember doing 表？", "记得做过", ["记得要做", "忘记做"])]), 7, "汉译英remember", "句子练习")

# ================= 拼读（4页） =================
add(B.section_head("拼", "音素 · 动名词词尾 -ing", "音素")
    + B.rule_cards([("zhug", "/ɪŋ/", "动名词词尾：enjoying/finishing/practicing；鼻音 /ŋ/。"),
                    ("xing", "对比 -ink", "-ink 发 /ɪŋk/：think/drink/link；-ing 不发 k。")])
    + B.quiz_html([("-ing 发？", "/ɪŋ/", ["/ɪŋk/", "/ɪn/"]),
                   ("think 发？", "/ɪŋk/", ["/ɪŋ/", "/iːŋ/"]),
                   ("sing 发？", "/ɪŋ/", ["/ɪŋk/", "/sɪŋk/"])])
    + B.note_panel("发音要点", "/ɪŋ/ 鼻音收尾，声带振动；/ɪŋk/ 在鼻音后加清塞音 k。读 enjoying 时 ing 收鼻音。"), 7, "拼读音素", "-ing")

add(B.section_head("拼", "看词归音 · -ing 还是 -ink", "归音")
    + B.order_q("把含 /ɪŋ/ 的词挑出来（排序成一列）",
                [("singing", "鼻音"), ("practicing", "鼻音"), ("think", "加k")],
                "singing|practicing|think")
    + B.sub_label("自检一题")
    + B.quiz_html([("drink 发？", "/ɪŋk/", ["/ɪŋ/", "/iːnk/"])]), 7, "拼读归音", "-ing vs -ink")

add(B.section_head("拼", "听音选词 · 含 /ɪŋ/", "听音")
    + B.quiz_html([("选出含 /ɪŋ/ 的词", "singing", ["think", "drink"]),
                   ("选出含 /ɪŋk/ 的词", "blink", ["singing", "practicing"]),
                   ("enjoying 中 ing 发？", "/ɪŋ/", ["/ɪŋk/", "/eɪŋ/"])])
    + B.sub_label("点击作答，听音辨形")
    + B.note_panel("听辨提示", "-ing 收鼻音 /ɪŋ/，-ink 在鼻音后爆破 k。读快了容易混淆，注意听尾巴。"), 7, "拼读听音", "听音选词")

add(B.section_head("拼", "最小对立对 · think vs thing", "对立")
    + B.rule_cards([("ming", "最小对立", "think（思考）/thing（事物）；sink（下沉）/sing（唱歌）——注意尾音 k 的有无。")])
    + B.match_q([("think", "/θɪŋk/"), ("thing", "/θɪŋ/"), ("sink", "/sɪŋk/"), ("sing", "/sɪŋ/")],
                [("/θɪŋk/", "think"), ("/θɪŋ/", "thing"), ("/sɪŋk/", "sink"), ("/sɪŋ/", "sing")])
    + B.sub_label("左右两列点击配对"), 7, "拼读对立", "最小对立对")

# ================= ⑧ 课堂总结（3页） =================
add(B.section_head("结", "核心口诀总览", "一页速览")
    + B.rule_cards([("zhug", "doing", "enjoy/finish/mind/practice/suggest/avoid/consider/imagine + doing；作主语谓语单数。"),
                    ("xing", "to do", "want/decide/hope/plan/agree/refuse/promise/manage/afford/offer/fail + to do；表目的。"),
                    ("bin", "辨析", "stop doing 停止；stop to do 停下来做；remember doing 记得做过；remember to do 记得要做。")])
    + B.quiz_html([("enjoy 后接？", "doing", ["to do", "原形"]),
                   ("want 后接？", "to do", ["doing", "原形"]),
                   ("remember to do 表？", "记得要做", ["记得做过", "忘记做"])])
    + B.body_text("口诀背诵：<b>enjoy/finish 后 doing，want/decide 后 to do。</b>"
                  "stop doing 停此事，stop to do 去做它；remember doing 记做过，remember to do 记得做。"
                  "把口诀读两遍，再用本课 20 词各造一句，本课核心就掌握了大半。")
    + B.quiz_html([("'后接 to do' 的动词常表？", "打算/希望/承诺", ["爱好/习惯", "动作持续"]),
                   ("本课口诀的核心是？", "doing 与 to do 各司其职", ["越多越难", "越精确越好"])]), 8, "核心口诀", "一页速览")

add(B.section_head("结", "课堂思维导图", "全课收尾")
    + B.mind_map(25, "动名词与不定式综合运用", [
        ("doing", "enjoy/finish/mind + V-ing"),
        ("to do", "want/decide/hope + to do"),
        ("目的", "to do 表'为了'"),
        ("辨析", "stop/remember doing·to do"),
        ("防越级", "不引入分词状语"),
        ("应用", "阅读定位动词 / 造句 / 拼读")])
    + B.sub_label("本课 3 考点：G62 动名词 · G63 不定式 · 辨析")
    + B.note_panel("一句话收口", "enjoy 后 doing、want 后 to do、stop/remember 后看意思。三句口诀一次带走。"), 8, "思维导图", "全课收尾")

add(B.section_head("结", "课后任务 · 巩固清单", "任务")
    + B.rule_cards([("qita", "任务一", "抄写 20 个动词接续相关词，各配一句 doing 或 to do 句型。"),
                    ("bin", "任务二", "完成配套练习卷（阅读30/语言25/综合25/语法诊断20）。"),
                    ("xing", "任务三", "用 enjoy/finish/want/decide/remember 各造 2 句。")])
    + B.quiz_html([("本课核心考点有几个？", "3 个", ["2 个", "5 个"]),
                   ("remember doing 表记得做过，对吗？", "对", ["错", "看情况"])])
    + B.ext_card("展望", "L26 将延续动词接续，预习其他动词的 doing/to do 用法。"), 8, "课后任务", "巩固清单")

total = p - 1
seg_pages = {sid: [a, b] for sid, (a, b) in seg.items()}
page_meta = {i: {"p": "CORE", "m": 2} for i in range(1, total + 1)}

js = B.js_extra(total, seg_pages, page_meta)
css = B.CSS_EXTRA
out = os.path.join(out_dir, "第25课时_课件_中等.html")
size = B.write_courseware(25, "第25课时 · 动名词与不定式综合运用", pages, NAV, STAGE, css, js, out, session="D25")
print("L25 课件生成：%s (%d bytes, %d pages)" % (out, size, total))