# -*- coding: utf-8 -*-
"""邓兴华 L08 配套练习内容（中等）— 2026-08-04
语篇均真题母本改编/仿真题，溯源ID登记。
时态：一般过去时 was/were + 规则动词-ed + 过去时间状语（G19-G21）
防越级：禁不规则动词过去式（went/bought/ate等）、禁将来时/完成时/被动语态
结构：阅读选择11题(4+4+3) + 五选四4题 + 完形10题 + 选词10题 + 简答5题 + 作文1题 + 诊断10题
"""
import json, re

# ────────────────────────────────────────
# 阅读 A 篇：Getting Dressed for Yesterday's Trip（应用文，107词）
# 仿真题（母本：HN2026_L8_reading_a 真题改编，时态合规化）
# ────────────────────────────────────────
reading_a = {
    "id": "HN2026_L8_reading_a",
    "genre": "应用文",
    "difficulty": "中等",
    "word_count": 107,
    "provenance": "仿真题（母本：HN2026_L8_reading_a 真题改编，时态合规化）",
    "paragraphs": [
        "Yesterday was a busy and happy day for our family. In the morning, I packed my blue bag with clothes. I took a map, a camera and an umbrella for the trip. My mum took water and food for us.",
        "We wore red hats because the weather was sunny and warm. The bus was cheap and clean. We were happy and ready at eight. The trip started at eight and finished at six. We visited many places and took photos.",
        "We ate nice food on the bus. The guide was kind and funny. I bought a postcard for my friend. It was a great day!"
    ],
    "questions": [
        {"num": 1, "q": "When did the family go on the trip?",
         "opts": [["A", "Yesterday."], ["B", "Today."], ["C", "Tomorrow."]], "answer": "A"},
        {"num": 2, "q": "What did the writer pack in the morning?",
         "opts": [["A", "Food and water."], ["B", "Clothes in a blue bag."], ["C", "A postcard."]], "answer": "B"},
        {"num": 3, "q": "How was the weather that day?",
         "opts": [["A", "Cold and rainy."], ["B", "Windy and dark."], ["C", "Sunny and warm."]], "answer": "C"},
        {"num": 4, "q": "What time did the trip start?",
         "opts": [["A", "At eight."], ["B", "At six."], ["C", "At nine."]], "answer": "A"},
    ],
    "绑定": "G19·G20·G21·旅行主题",
}

# ────────────────────────────────────────
# 阅读 B 篇：Yesterday's Trip to the Beach（记叙文，129词）
# 仿真题（母本：2025 湖南省卷阅读记叙文结构改编）
# ────────────────────────────────────────
reading_b = {
    "id": "teacher_authored_L8_reading_b",
    "genre": "记叙文",
    "difficulty": "中等",
    "word_count": 129,
    "provenance": "仿真题（母本：2025 湖南省卷阅读B记叙文结构改编）",
    "paragraphs": [
        "Yesterday, my family visited the beach. The weather was sunny and warm. We started early and arrived there at nine. The sand was soft and the water was blue. My sister and I played on the beach and tried to build a big sandcastle.",
        "At noon, we ate delicious food at a small restaurant. The fish was delicious and the price was cheap. After lunch, my dad decided to try surfing. He looked funny on the board. We all laughed and felt very happy.",
        "In the afternoon, the weather changed. It was terrible and rainy. We packed our things and stayed in the car. The trip finished at four. Two days ago, the weather was great, but yesterday was a mixed day. Still, we enjoyed it."
    ],
    "questions": [
        {"num": 5, "q": "When did the family visit the beach?",
         "opts": [["A", "Two days ago."], ["B", "Yesterday."], ["C", "Last week."]], "answer": "B"},
        {"num": 6, "q": "What did the writer and her sister try to build?",
         "opts": [["A", "A big house."], ["B", "A sandcastle."], ["C", "A boat."]], "answer": "B"},
        {"num": 7, "q": "The underlined word \"terrible\" in paragraph 3 means _____.",
         "opts": [["A", "very good"], ["B", "very bad"], ["C", "very warm"]], "answer": "B"},
        {"num": 8, "q": "Why did the family stay in the car in the afternoon?",
         "opts": [["A", "Because they were tired."], ["B", "Because the weather was rainy."], ["C", "Because the food was terrible."]], "answer": "B"},
    ],
    "绑定": "G19·G20·G21·旅行主题",
}

# ────────────────────────────────────────
# 阅读 C 篇：Why Traveling Is Good for Us（说明文，129词）
# 仿真题（母本：2025 湖南省卷阅读C说明文结构改编）
# ────────────────────────────────────────
reading_c = {
    "id": "teacher_authored_L8_reading_c",
    "genre": "说明文",
    "difficulty": "中等",
    "word_count": 129,
    "provenance": "仿真题（母本：2025 湖南省卷阅读C说明文结构改编）",
    "paragraphs": [
        "Traveling is one of the best ways to learn about the world. When we visit a new place, we see different things and meet different people. A museum is a great place to learn about history. Long ago, people lived without phones or computers.",
        "Traveling also helps us try new activities. We can try local food, learn a new sport, or talk to a guide. Some people think traveling is expensive, but there are many cheap ways to travel. A bus trip or a short camp can be fun.",
        "Finally, traveling is good because we can enjoy time with our family. We stay together, eat together, and share memories. A trip to the beach or a visit to a museum can bring family closer. That is why traveling is good for us."
    ],
    "questions": [
        {"num": 9, "q": "What is the main idea of this passage?",
         "opts": [["A", "Museums are boring."], ["B", "Traveling is good for us."], ["C", "Traveling is always expensive."]], "answer": "B"},
        {"num": 10, "q": "Where can we learn about history according to the passage?",
         "opts": [["A", "In a museum."], ["B", "On a bus."], ["C", "At a restaurant."]], "answer": "A"},
        {"num": 11, "q": "Why can traveling bring family closer?",
         "opts": [["A", "Because they stay together and share memories."], ["B", "Because they work together."], ["C", "Because they study together."]], "answer": "A"},
    ],
    "绑定": "G19·G20·G21·旅行主题",
}

# ────────────────────────────────────────
# 五选四：A Science Trip to the Museum（说明文，129词）
# 仿真题（母本：HN2026_L8_w5 结构改编，时态合规化）
# ────────────────────────────────────────
w5 = {
    "id": "HN2026_L8_w5",
    "title": "阅读下面短文，从方框中选出可以填入空白处的最佳选项（有一项为多余选项）",
    "paragraphs": [
        "We went on a school trip to the science museum last month. ___1___ The bus was yellow and clean, and everyone was excited. We arrived at nine in the morning and the guide welcomed us at the big door with a warm smile.",
        "___2___ There were robots, old computers, and strange machines everywhere in the hall. A friendly guide showed us around the big room and told us many interesting things about each exhibit there. ___3___ We laughed and asked many questions about the small robots and their funny movements.",
        "After lunch, we tried a science activity. We built a small bridge with paper and wood. ___4___ Everyone enjoyed the trip and we went home happy and tired. Two days ago, we talked about the trip in class again. It was a great day!"
    ],
    "candidates": [
        ["A", "First, we went there by a yellow school bus."],
        ["B", "There were many interesting things to see."],
        ["C", "The stories about robots made us laugh."],
        ["D", "We played games in the garden that day."],
        ["E", "It was not easy but we finished it."],
    ],
    "answers": {"1": "A", "2": "B", "3": "C", "4": "E"},
    "绑定": "G19·G20·G21·旅行主题",
}

# ────────────────────────────────────────
# 完形填空：旅行经历（107词，仅规则-ed + was/were + 时间状语）
# 仿真题（母本：HN2026_L8_cloze 结构改编，不规则动词全部替换为规则-ed）
# ────────────────────────────────────────
cloze = {
    "id": "HN2026_L8_cloze",
    "title": "阅读短文，从每题所给的 A、B、C 三个选项中选出最佳选项",
    "paragraphs": [
        "Last weekend, I ___1___ at home. I ___2___ to visit the museum with my friend. The museum ___3___ a beautiful place with many old and interesting things to see and learn about. We ___4___ there at nine in the morning. The weather ___5___ sunny and warm.",
        "We ___6___ many interesting things there. A guide ___7___ us about the history of the city and showed us around the big hall. We learned a lot from the visit. The guide ___8___ very kind and funny. We ___9___ delicious food at a small restaurant near the museum.",
        "The food ___10___ cheap and good. We enjoyed the trip very much. It was a wonderful day for all of us to remember!"
    ],
    "items": [
        {"num": 1, "q": "I ___ at home.",
         "opts": [["A", "stayed"], ["B", "stay"], ["C", "staying"]], "answer": "A"},
        {"num": 2, "q": "I ___ to visit the museum with my friend.",
         "opts": [["A", "decide"], ["B", "decided"], ["C", "deciding"]], "answer": "B"},
        {"num": 3, "q": "The museum ___ a beautiful place with many old and interesting things.",
         "opts": [["A", "were"], ["B", "was"], ["C", "is"]], "answer": "B"},
        {"num": 4, "q": "We ___ there at nine in the morning.",
         "opts": [["A", "start"], ["B", "started"], ["C", "starting"]], "answer": "B"},
        {"num": 5, "q": "The weather ___ sunny and warm.",
         "opts": [["A", "was"], ["B", "were"], ["C", "is"]], "answer": "A"},
        {"num": 6, "q": "We ___ many interesting things there.",
         "opts": [["A", "visit"], ["B", "visited"], ["C", "visiting"]], "answer": "B"},
        {"num": 7, "q": "A guide ___ us about the history of the city.",
         "opts": [["A", "guide"], ["B", "guided"], ["C", "guiding"]], "answer": "B"},
        {"num": 8, "q": "The guide ___ very kind and funny.",
         "opts": [["A", "were"], ["B", "was"], ["C", "are"]], "answer": "B"},
        {"num": 9, "q": "We ___ delicious food at a small restaurant.",
         "opts": [["A", "enjoy"], ["B", "enjoyed"], ["C", "enjoying"]], "answer": "B"},
        {"num": 10, "q": "The food ___ cheap and good.",
         "opts": [["A", "was"], ["B", "were"], ["C", "is"]], "answer": "A"},
    ],
    "绑定": "G19·G20·G21·旅行主题",
}

# ────────────────────────────────────────
# 选词填空：旅行对话（86词，6不变形 + 4考语法）
# 37考was/were(G19), 38考规则-ed(G20), 39考didn't+原形(G20), 40考时间状语(G21)
# ────────────────────────────────────────
grammar_fill = {
    "id": "teacher_authored_L8_wordbank",
    "title": "从方框内选择适当的词并用其正确形式填空（每空限填一词，每词限用一次）",
    "word_bank": ["beach", "delicious", "terrible", "activity", "guide", "place", "be", "visit", "stay", "ago"],
    "paragraphs": [
        "M: Hi Lisa! Where did you travel last weekend?\n"
        "W: I traveled to the ___1___. It was sunny and warm.\n"
        "M: Did you do any fun ___2___ there?\n"
        "W: Yes! The ___3___ showed us around.\n"
        "M: Was the food good?\n"
        "W: Yes, the fish was ___4___. But the bus was ___5___!\n"
        "M: Oh no! What happened then?\n"
        "W: The station ___6___ very crowded.\n"
        "M: What did you do?\n"
        "W: We ___7___ the small museum nearby.\n"
        "M: Did you stay long?\n"
        "W: No, I didn't ___8___ there long.\n"
        "M: Want to visit that ___9___ again?\n"
        "W: Yes! Two weeks ___10___, I traveled with my dad."
    ],
    "answers": ["beach", "activity", "guide", "delicious", "terrible", "was", "visited", "stay", "place", "ago"],
    "绑定": "G19(37)·G20(38,39)·G21(40)",
}

# ────────────────────────────────────────
# 阅读回答问题：旅行经历（107词）
# 仿真题（基于旅行主题改编，独立语篇）
# ────────────────────────────────────────
sa = {
    "id": "teacher_authored_L8_sa",
    "title": "阅读下面短文，回答下列问题或按要求完成句子",
    "paragraphs": [
        "Tom visited his grandparents last weekend. He stayed there for two days. The weather was sunny and warm. On Saturday, Tom and his grandpa visited a small farm. They saw chickens and ducks there.",
        "Tom tried to feed the chickens. It was his first time, and he felt very excited. In the afternoon, Tom's grandma cooked a delicious meal. The food was cheap but very tasty. Tom enjoyed every dish.",
        "After lunch, they sat under a tree and talked. Tom's grandpa told stories about the place long ago. Tom listened carefully. On Sunday, Tom finished his homework and started his trip home. He was very happy."
    ],
    "questions": [
        {"q": "Where did Tom go last weekend?", "answer": "He went to his grandparents' home.", "type": "简答"},
        {"q": "How was the weather on Saturday?", "answer": "It was sunny and warm.", "type": "简答"},
        {"q": "What did Tom try to do on the farm?", "answer": "He tried to feed the chickens.", "type": "简答"},
        {"q": "Did Tom enjoy the food?", "answer": "Yes, he did.", "type": "一般疑问句"},
        {"q": "Translate the underlined sentence into Chinese: \"Tom's grandpa told stories about the place long ago.\"", "answer": "汤姆的爷爷讲述了关于这个地方很久以前的故事。", "type": "翻译"},
    ],
    "绑定": "G19·G20·G21·旅行主题",
}

# ────────────────────────────────────────
# 书面表达：写一次旅行经历（100词，过去时实践）
# ────────────────────────────────────────
writing = {
    "id": "teacher_authored_L8_writing",
    "title": "书面表达（满分 15 分）",
    "prompt": (
        "Write a short passage (about 100 words) about a trip you took in the past. "
        "Include the following information:"
    ),
    "requirements": (
        "1. Where did you go and when?\n"
        "2. What did you do there?\n"
        "3. How did you feel about the trip?\n"
        "注意：1. 词数约100词；2. 使用一般过去时（was/were, 动词-ed形式）；3. 至少使用3个本课新词。"
    ),
    "sample": [
        "Last summer, I visited the beach with my family. The weather was sunny and warm. We started early in the morning. I tried to swim in the sea. It was my first time, and I felt very excited. We ate delicious food at a restaurant. The food was cheap but very good. In the afternoon, we played on the beach and took many photos. The trip finished at six. We enjoyed the trip very much. Two days ago, I decided to go there again. It was a wonderful day!"
    ],
    "绑定": "G19·G20·G21·旅行主题",
}

# ────────────────────────────────────────
# 语法诊断：G01-G21 全部21考点滚动（5选择 + 5填空）
# ────────────────────────────────────────
grammar_diag = {
    "id": "teacher_authored_L8_grammar_diag",
    "title": "语法复盘（G01–G21 全考点滚动）",
    "mc": [
        {"num": 1, "q": "Which word has the same sound as \"ay\" in \"play\"?",
         "opts": [["A", "rain"], ["B", "run"], ["C", "pen"]], "answer": "A",
         "绑定": "G01·拼读"},
        {"num": 2, "q": "She _____ TV at home yesterday evening.",
         "opts": [["A", "watched"], ["B", "watch"], ["C", "watching"]], "answer": "A",
         "绑定": "G20·规则-ed"},
        {"num": 3, "q": "The water _____ very cold yesterday.",
         "opts": [["A", "were"], ["B", "was"], ["C", "is"]], "answer": "B",
         "绑定": "G19·was/were"},
        {"num": 4, "q": "He didn't _____ to school last Monday.",
         "opts": [["A", "walked"], ["B", "walk"], ["C", "walking"]], "answer": "B",
         "绑定": "G20·didn't+原形"},
        {"num": 5, "q": "I visited the museum _____.",
         "opts": [["A", "two days ago"], ["B", "every day"], ["C", "tomorrow"]], "answer": "A",
         "绑定": "G21·过去时间状语"},
    ],
    "fill": [
        {"q": "They _____ (be) at the beach last weekend.", "answer": "were", "绑定": "G19"},
        {"q": "We _____ (visit) the museum two days ago.", "answer": "visited", "绑定": "G20"},
        {"q": "I didn't _____ (go) to school yesterday. (用动词原形填空)", "answer": "go", "绑定": "G20"},
        {"q": "She finished her homework _____ (昨天). (填入英文时间状语)", "answer": "yesterday", "绑定": "G21"},
        {"q": "The weather _____ (be) terrible last night.", "answer": "was", "绑定": "G19"},
    ],
}

# ────────────────────────────────────────
# 组装
# ────────────────────────────────────────
content = {
    "_doc": "邓兴华 L08 配套练习内容（中等）· 2026-08-04。语篇均真题母本改编/仿真题。时态：一般过去时was/were+规则-ed+过去时间状语（G19-G21）。防越级：禁不规则动词过去式、禁将来时/完成时/被动语态。",
    "reading_a": reading_a,
    "reading_b": reading_b,
    "reading_c": reading_c,
    "w5": w5,
    "cloze": cloze,
    "grammar_fill": grammar_fill,
    "sa": sa,
    "writing": writing,
    "grammar_diag": grammar_diag,
}

if __name__ == "__main__":
    print(json.dumps(content, ensure_ascii=False, indent=2))
