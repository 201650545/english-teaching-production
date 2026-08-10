# -*- coding: utf-8 -*-
"""M2b 基础已知词表生成器（2026-08-02 教师授权扩充 M2 词库）
用途：基础/中等学生「课前已掌握」的功能词与高频初等词，独立成 base_vocab.json。
- 只用于生词率计算（缺口 F），不计入新词选择（vocab_selector 只读 vocab_bank.json 的目标主题）；
- 已存在于目标词库（vocab_bank.json）的词自动剔除，避免重复；
- 70% 熟词 / 30% 生词的目标由此可得准确测量。
结构：{"words":[{en, cn, pos, theme:"base"}, ...]}
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = "D:/英语教学/01_数据"

target = set(w["en"].lower() for w in json.load(open(os.path.join(DATA_DIR, "banks", "vocab_bank.json"), encoding="utf-8"))["words"])

# 功能词 + 高频初等词（词性 n./v./adj./adv./prep./pron./conj./num./art./aux.）
BASE = [
    # 冠词/代词/be/助动词
    ("a", "一个", "art."), ("an", "一个", "art."), ("the", "这；那", "art."),
    ("I", "我", "pron."), ("you", "你；你们", "pron."), ("he", "他", "pron."), ("she", "她", "pron."),
    ("it", "它", "pron."), ("we", "我们", "pron."), ("they", "他们", "pron."),
    ("me", "我(宾)", "pron."), ("him", "他(宾)", "pron."), ("her", "她(宾)", "pron."),
    ("us", "我们(宾)", "pron."), ("them", "他们(宾)", "pron."),
    ("my", "我的", "pron."), ("your", "你的", "pron."), ("his", "他的", "pron."),
    ("its", "它的", "pron."), ("our", "我们的", "pron."), ("their", "他们的", "pron."),
    ("this", "这个", "pron."), ("that", "那个", "pron."), ("these", "这些", "pron."), ("those", "那些", "pron."),
    ("am", "是(第一人称)", "aux."), ("is", "是(单数)", "aux."), ("are", "是(复数)", "aux."),
    ("was", "是(过去)", "aux."), ("were", "是(过去复数)", "aux."),
    ("do", "做；助动词", "v."), ("does", "做(三单)", "v."), ("did", "做(过去)", "v."),
    ("have", "有；吃", "v."), ("has", "有(三单)", "v."), ("had", "有(过去)", "v."),
    ("can", "能；会", "aux."), ("could", "可以(过去)", "aux."), ("may", "可以", "aux."),
    ("must", "必须", "aux."), ("will", "将要", "aux."), ("would", "愿意", "aux."),
    ("shall", "将要", "aux."), ("should", "应该", "aux."),
    # 连词/介词
    ("and", "和", "conj."), ("or", "或", "conj."), ("but", "但是", "conj."), ("so", "所以", "conj."),
    ("because", "因为", "conj."), ("if", "如果", "conj."), ("when", "当…时", "conj."),
    ("of", "…的", "prep."), ("to", "到；向", "prep."), ("for", "为了；给", "prep."),
    ("with", "和…一起", "prep."), ("from", "从；来自", "prep."), ("at", "在(时间/地点)", "prep."),
    ("in", "在…里", "prep."), ("on", "在…上", "prep."), ("under", "在…下", "prep."),
    ("by", "通过；乘", "prep."), ("near", "在…附近", "prep."), ("about", "关于；大约", "prep."),
    ("after", "在…之后", "prep."), ("before", "在…之前", "prep."), ("between", "在…之间", "prep."),
    ("behind", "在…后面", "prep."), ("above", "在…上方", "prep."), ("into", "进入", "prep."),
    ("out", "外出", "adv."), ("up", "向上", "adv."), ("down", "向下", "adv."), ("left", "左边", "adj./n."),
    ("right", "右边；正确", "adj./n."),
    # 疑问词/副词
    ("what", "什么", "pron."), ("where", "哪里", "adv."), ("who", "谁", "pron."),
    ("which", "哪一个", "pron."), ("how", "怎样", "adv."), ("why", "为什么", "adv."),
    ("not", "不", "adv."), ("yes", "是", "adv."), ("no", "不；没有", "adv."),
    ("very", "非常", "adv."), ("too", "也；太", "adv."), ("also", "也", "adv."), ("again", "再次", "adv."),
    ("now", "现在", "adv."), ("then", "然后", "adv."), ("always", "总是", "adv."),
    ("usually", "通常", "adv."), ("often", "经常", "adv."), ("sometimes", "有时", "adv."),
    ("never", "从不", "adv."), ("please", "请", "adv."), ("well", "好地；健康的", "adv."),
    ("here", "这里", "adv."), ("there", "那里", "adv."), ("today", "今天", "adv."),
    ("tomorrow", "明天", "adv."), ("yesterday", "昨天", "adv."), ("together", "一起", "adv."),
    # 数词
    ("one", "一", "num."), ("two", "二", "num."), ("three", "三", "num."), ("four", "四", "num."),
    ("five", "五", "num."), ("six", "六", "num."), ("seven", "七", "num."), ("eight", "八", "num."),
    ("nine", "九", "num."), ("ten", "十", "num."), ("eleven", "十一", "num."), ("twelve", "十二", "num."),
    ("thirteen", "十三", "num."), ("twenty", "二十", "num."), ("thirty", "三十", "num."),
    ("hundred", "百", "num."),
    # 时间
    ("morning", "早上", "n."), ("afternoon", "下午", "n."), ("evening", "晚上", "n."),
    ("night", "夜晚", "n."), ("day", "天", "n."), ("week", "周", "n."), ("month", "月", "n."),
    ("year", "年", "n."), ("hour", "小时", "n."), ("minute", "分钟", "n."), ("time", "时间", "n."),
    ("weekend", "周末", "n."), ("o'clock", "…点钟", "n."),
    # 颜色
    ("red", "红色", "adj."), ("yellow", "黄色", "adj."), ("blue", "蓝色", "adj."), ("green", "绿色", "adj."),
    ("black", "黑色", "adj."), ("white", "白色", "adj."), ("brown", "棕色", "adj."), ("pink", "粉色", "adj."),
    ("purple", "紫色", "adj."), ("grey", "灰色", "adj."),
    # 身体
    ("head", "头", "n."), ("eye", "眼睛", "n."), ("ear", "耳朵", "n."), ("nose", "鼻子", "n."),
    ("mouth", "嘴", "n."), ("face", "脸", "n."), ("hair", "头发", "n."), ("hand", "手", "n."),
    ("arm", "手臂", "n."), ("leg", "腿", "n."), ("foot", "脚", "n."), ("tooth", "牙齿", "n."),
    ("finger", "手指", "n."),
    # 常见人物/地点/基础名词
    ("man", "男人", "n."), ("woman", "女人", "n."), ("boy", "男孩", "n."), ("girl", "女孩", "n."),
    ("child", "孩子", "n."), ("people", "人们", "n."), ("friend", "朋友", "n."),
    ("father", "父亲", "n."), ("mother", "母亲", "n."), ("brother", "兄弟", "n."),
    ("sister", "姐妹", "n."), ("parent", "父母", "n."), ("home", "家", "n."), ("house", "房子", "n."),
    ("street", "街道", "n."), ("road", "路", "n."), ("shop", "商店", "n."), ("garden", "花园", "n."),
    ("door", "门", "n."), ("window", "窗户", "n."), ("wall", "墙", "n."), ("floor", "地板", "n."),
    ("table", "桌子", "n."), ("chair", "椅子", "n."), ("bed", "床", "n."),
    # 常见形容词
    ("big", "大的", "adj."), ("small", "小的", "adj."), ("tall", "高的", "adj."), ("short", "矮的；短的", "adj."),
    ("long", "长的", "adj."), ("new", "新的", "adj."), ("old", "老的；旧的", "adj."), ("good", "好的", "adj."),
    ("bad", "坏的", "adj."), ("nice", "好的；令人愉快的", "adj."), ("fine", "好的", "adj."),
    ("happy", "高兴的", "adj."), ("sad", "难过的", "adj."), ("angry", "生气的", "adj."),
    ("tired", "疲惫的", "adj."), ("hot", "热的", "adj."), ("cold", "冷的", "adj."), ("warm", "温暖的", "adj."),
    ("cool", "凉爽的；酷的", "adj."), ("clean", "干净的", "adj."), ("dirty", "脏的", "adj."),
    ("easy", "容易的", "adj."), ("hard", "困难的；努力地", "adj."), ("fast", "快的", "adj."),
    ("slow", "慢的", "adj."), ("early", "早的", "adj."), ("late", "迟的", "adj."), ("high", "高的", "adj."),
    ("low", "低的", "adj."), ("busy", "忙碌的", "adj."), ("free", "空闲的；免费的", "adj."),
    ("kind", "友善的", "adj."), ("quiet", "安静的", "adj."), ("loud", "大声的", "adj."),
    ("strong", "强壮的", "adj."), ("weak", "虚弱的", "adj."), ("healthy", "健康的", "adj."),
    ("full", "饱的；满的", "adj."), ("empty", "空的", "adj."), ("sweet", "甜的", "adj."),
    ("fresh", "新鲜的", "adj."), ("important", "重要的", "adj."), ("interesting", "有趣的", "adj."),
    ("different", "不同的", "adj."), ("same", "相同的", "adj."), ("favorite", "最喜欢的", "adj."),
    ("delicious", "美味的", "adj."), ("funny", "滑稽的", "adj."), ("careful", "小心的", "adj."),
    ("beautiful", "美丽的", "adj."),
    # 常见动词（基础高频）
    ("be", "是", "v."), ("go", "去", "v."), ("come", "来", "v."), ("get", "得到；到达", "v."),
    ("make", "制作；使得", "v."), ("give", "给", "v."), ("take", "拿；乘坐", "v."), ("put", "放", "v."),
    ("find", "找到", "v."), ("feel", "感觉", "v."), ("help", "帮助", "v."), ("work", "工作", "v."),
    ("play", "玩；打", "v."), ("run", "跑", "v."), ("walk", "走", "v."), ("sit", "坐", "v."),
    ("stand", "站", "v."), ("eat", "吃", "v."), ("drink", "喝", "v."), ("read", "读", "v."),
    ("write", "写", "v."), ("speak", "说", "v."), ("talk", "交谈", "v."), ("listen", "听", "v."),
    ("sleep", "睡觉", "v."), ("open", "打开", "v."), ("close", "关闭", "v."), ("wash", "洗", "v."),
    ("brush", "刷", "v."), ("ride", "骑", "v."), ("wear", "穿", "v."), ("buy", "买", "v."),
    ("cook", "烹饪", "v."), ("draw", "画", "v."), ("sing", "唱", "v."), ("meet", "遇见", "v."),
    ("wait", "等待", "v."), ("stop", "停止", "v."), ("start", "开始", "v."), ("finish", "完成", "v."),
    ("try", "尝试", "v."), ("learn", "学习", "v."), ("study", "学习；书房", "v."), ("teach", "教", "v."),
    ("show", "展示", "v."), ("use", "使用", "v."), ("keep", "保持", "v."), ("leave", "离开", "v."),
    ("turn", "转弯；翻转", "v."), ("begin", "开始", "v."), ("forget", "忘记", "v."),
    ("remember", "记得", "v."), ("bring", "带来", "v."), ("carry", "搬运", "v."), ("clean", "打扫", "v."),
    ("cut", "切", "v."), ("dance", "跳舞", "v."), ("drive", "驾驶", "v."), ("fly", "飞", "v."),
    ("grow", "生长", "v."), ("hear", "听见", "v."), ("hold", "握住", "v."), ("hope", "希望", "v."),
    ("jump", "跳", "v."), ("laugh", "笑", "v."), ("pick", "摘；挑选", "v."), ("smile", "微笑", "v."),
    ("swim", "游泳", "v."), ("visit", "参观；拜访", "v."), ("watch", "观看", "v."),
    ("welcome", "欢迎", "v."), ("win", "赢", "v."), ("wish", "祝愿", "v."), ("ask", "问；请求", "v."),
    ("answer", "回答", "v."), ("say", "说", "v."), ("tell", "告诉", "v."), ("look", "看", "v."),
    ("see", "看见", "v."), ("think", "想；认为", "v."), ("know", "知道", "v."), ("want", "想要", "v."),
    ("like", "喜欢", "v."), ("love", "爱", "v."), ("need", "需要", "v."),
]

def main():
    words = []
    seen = set()
    for en, cn, pos in BASE:
        key = en.lower()
        if key in target:
            continue  # 已在目标词库，剔除
        if key in seen:
            continue
        seen.add(key)
        words.append({"en": en, "phonetic": "", "pos": pos, "cn": cn,
                      "collocation": "", "example": "", "hook": "",
                      "theme": "base", "used_by_lesson": 0, "frequency": "high"})
    out = os.path.join(DATA_DIR, "banks", "base_vocab.json")
    json.dump({"words": words}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("基础已知词表生成：%s（%d 词，剔除目标词库重复 %d）" %
          (out, len(words), len(BASE) - len(words)))

if __name__ == "__main__":
    main()
