# -*- coding: utf-8 -*-
"""M7 拼读库生成器：从 lesson_map.json 的 phonics 字段生成 phonics_bank.json
结构：{"组合":"bl","发音":"/bl/","词族":[...],"儿歌":"...","lesson":5}
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = "D:/英语教学/01_数据"

lm = json.load(open(os.path.join(DATA_DIR, "schemas", "lesson_map.json"), encoding="utf-8"))

# 常见拼读组合 → 发音 + 词族（种子数据，后续可扩充）
PHONICS_SEED = {
    "短元音 a/e/i/o/u": {"发音": "/æ/ /e/ /ɪ/ /ɒ/ /ʌ/", "词族": ["cat", "bed", "pig", "dog", "bus"]},
    "th/sh/ch/wh/ph": {"发音": "/θ/ /ʃ/ /tʃ/ /w/ /f/", "词族": ["think", "ship", "chair", "what", "photo"]},
    "th/wh/ph/ng/nk": {"发音": "/θ/ /w/ /f/ /ŋ/ /ŋk/", "词族": ["three", "white", "phone", "sing", "bank"]},
    "br/cr/dr/fr/tr/gr": {"发音": "/br/ /kr/ /dr/ /fr/ /tr/ /gr/", "词族": ["bread", "cry", "dress", "friend", "tree", "green"]},
    "bl/cl/fl/gl/pl/sl": {"发音": "/bl/ /kl/ /fl/ /gl/ /pl/ /sl/", "词族": ["blue", "clock", "flag", "glass", "play", "slow"]},
    "ar/or/ir/er/ur": {"发音": "/ɑː/ /ɔː/ /ɜː/ /ə/ /ɜː/", "词族": ["car", "for", "bird", "teacher", "nurse"]},
    "-ed 发音 /t//d//ɪd/": {"发音": "/t/ /d/ /ɪd/", "词族": ["worked", "played", "visited"]},
    "wh-问词家族": {"发音": "/w/ /h/", "词族": ["what", "where", "when", "why", "who", "how"]},
    "三单-s/-es发音 /s//z//ɪz/": {"发音": "/s/ /z/ /ɪz/", "词族": ["likes", "goes", "watches"]},
    "魔法e a_e/i_e/o_e/u_e": {"发音": "/eɪ/ /aɪ/ /əʊ/ /juː/", "词族": ["cake", "kite", "home", "cute"]},
    "ai/ay/ea/ee": {"发音": "/eɪ/ /eɪ/ /iː/ /iː/", "词族": ["rain", "day", "eat", "see"]},
    "oa/ow/oo": {"发音": "/əʊ/ /aʊ/ /uː/", "词族": ["boat", "cow", "moon"]},
    "er/or 后缀": {"发音": "/ə/ /ə/", "词族": ["teacher", "doctor"]},
    "ow/ou/oi/oy": {"发音": "/aʊ/ /aʊ/ /ɔɪ/ /ɔɪ/", "词族": ["cow", "house", "coin", "boy"]},
    "y结尾 /i/与/aɪ/": {"发音": "/i/ /aɪ/", "词族": ["happy", "my"]},
    "-ing 与双写规则": {"发音": "/ɪŋ/", "词族": ["running", "swimming", "eating"]},
    "复合词重音": {"发音": "重音在前", "词族": ["blackboard", "classroom"]},
    "综合复习": {"发音": "综合", "词族": []},
}

bank = {}
for key in sorted(lm["lessons"].keys(), key=int):
    m = lm["lessons"][key]
    ph = m["phonics"]
    seed = PHONICS_SEED.get(ph, {"发音": "待补充", "词族": []})
    bank[ph] = {
        "组合": ph,
        "发音": seed["发音"],
        "词族": seed["词族"],
        "儿歌": f"{ph} 拼读儿歌（待补充）",
        "lesson": int(key)
    }

out = os.path.join(DATA_DIR, "banks", "phonics_bank.json")
with open(out, "w", encoding="utf-8") as f:
    json.dump(bank, f, ensure_ascii=False, indent=2)
print(f"phonics_bank.json 生成完成：{len(bank)} 个拼读组合")
# 验收：L5 拼读组合齐全
print("L5 拼读组合:", lm["lessons"]["5"]["phonics"], "→", "OK" if lm["lessons"]["5"]["phonics"] in bank else "缺失")
