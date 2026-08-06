# -*- coding: utf-8 -*-
"""M6b 补充语篇库生成器（原创·教师授权 2026-08-02）
用途：填补 passage_bank.json 缺失课时（L4/L5/L7/L9-L12）的阅读语料。
红线（本库例外条款）：原 passage_bank 仅真题母本改编、禁编造；本补充库由教师 2026-08-02
显式授权「自行采集优质文本或根据时事/科学原创开发高质量语库」，故 source_type = original，
provenance 必填溯源说明。制作练习符合本课规范（示例 70% 熟词 / 30% 生词，脚本按 vocab_bank 实测）。
结构：{id, lesson, student, tier, source_type, provenance, genre, difficulty,
       word_count, vocab_rate, theme, grammar_focus, text, questions[{num,q,opts,answer}]}
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
vocab_bank = json.load(open(os.path.join(HERE, "vocab_bank.json"), encoding="utf-8"))["words"]
V = set(w["en"].lower() for w in vocab_bank)
# M2b 基础已知词表（功能词+高频初等词）：计入生词率的"熟词"
try:
    base_vocab = json.load(open(os.path.join(HERE, "base_vocab.json"), encoding="utf-8"))["words"]
    V |= set(w["en"].lower() for w in base_vocab)
except FileNotFoundError:
    pass


def stem(w):
    w = re.sub(r"[^a-zA-Z']", "", w).lower()
    if w in V:
        return w
    for suf in ("'s", "es", "s", "ed", "ing"):
        if w.endswith(suf) and w[:-len(suf)] in V:
            return w[:-len(suf)]
    return w


def word_count(text):
    return len(re.findall(r"[A-Za-z]+", text))


def vocab_rate(text):
    words = re.findall(r"[A-Za-z]+", text)
    known = sum(1 for w in words if stem(w) in V)
    return "%.0f%%" % (100.0 * known / len(words))


def Q(n, q, opts, answer):
    """opts: [(letter, text)...], answer: 选项字母（大写）"""
    return {"num": n, "q": q, "opts": [[l, t] for l, t in opts], "answer": answer}


def P(lesson, ptype, theme, genre, gfocus, prov, text, questions):
    return {
        "id": "XYJ2026_L%02d_%s" % (lesson, ptype),
        "lesson": lesson, "student": "许颖嘉", "tier": "基础",
        "source_type": "original", "provenance": prov,
        "genre": genre, "difficulty": "易",
        "word_count": word_count(text), "vocab_rate": vocab_rate(text),
        "vocab_rate_note": "生词率按目标词库 vocab_bank + 基础已知词表 base_vocab（M2b，2026-08-02 扩充）实测；"
                           "语篇难度为七下基础常用词，目标 70% 熟词 / 30% 生词。",
        "theme": theme, "grammar_focus": gfocus, "text": text,
        "questions": questions,
    }


PROV = "原创语篇 · AI 编写（教师 2026-08-02 授权自行开发高质量语库）；主题/语法对齐人教版七下对应单元；非真题改编，生词率按 M2 词汇库实测"

BANK = []
BANK.append(P(4, "reading_a", "房间与方位", "记叙文", ["名词复数", "方位介词", "tidy"],
    PROV,
    "Hello! My name is Lucy. I have a small but tidy room. There is a bed, a desk and a chair in it. "
    "On the wall, there are two maps and three photos. Under the desk, there is a big box. "
    "My books are in the box. Some are on the shelf, and some are on the desk. "
    "My clothes are in the wardrobe. My schoolbag is on the chair. "
    "Look at the table! There are some cups, two glasses and a plant on it. "
    "Between the bed and the desk, there is a lamp. Behind the door, there is a ball. "
    "My room is small, but it is clean and tidy. I like my room very much.",
    [Q(1, "How many photos are on the wall?", [("A", "two"), ("B", "three"), ("C", "five")], "B"),
     Q(2, "Where is the big box?", [("A", "on the desk"), ("B", "under the desk"), ("C", "on the shelf")], "B"),
     Q(3, "What is between the bed and the desk?", [("A", "a plant"), ("B", "a ball"), ("C", "a lamp")], "C"),
     Q(4, "Where is the ball?", [("A", "behind the door"), ("B", "in the wardrobe"), ("C", "under the chair")], "A"),
     Q(5, "Which word is the plural of 'box'?", [("A", "boxs"), ("B", "boxes"), ("C", "boxies")], "B")]))

BANK.append(P(4, "reading_b", "房间与方位", "记叙文", ["方位介词", "Where 问句"],
    PROV,
    "It is Sunday morning. Mike wants to play football, but he cannot find his ball. "
    "\"Where is my ball?\" he asks. \"Is it under your bed?\" his mother asks. "
    "Mike looks under the bed. No ball there. \"Is it behind the door?\" his father asks. "
    "Mike looks behind the door. No ball there. \"Is it in the box?\" his sister asks. "
    "Mike looks in the box. No ball there. He is sad. "
    "Then his little brother comes in. \"Look, Mike! Your ball is on the table, between two cups,\" he says. "
    "Mike runs to the table and finds his ball. \"Thank you, little brother!\" Mike is happy again. "
    "They go to the park and play football together.",
    [Q(1, "When does the story happen?", [("A", "Sunday morning"), ("B", "Friday night"), ("C", "Monday morning")], "A"),
     Q(2, "What does Mike want to do?", [("A", "play football"), ("B", "read a book"), ("C", "play basketball")], "A"),
     Q(3, "Where is the ball at last?", [("A", "under the bed"), ("B", "on the table"), ("C", "behind the door")], "B"),
     Q(4, "Who helps Mike find the ball?", [("A", "his father"), ("B", "his mother"), ("C", "his brother")], "C"),
     Q(5, "How does Mike feel at the end?", [("A", "sad"), ("B", "happy"), ("C", "angry")], "B")]))

BANK.append(P(5, "reading_a", "食物与日常", "记叙文", ["祈使句", "What 问句", "like"],
    PROV,
    "Lily is a student. She has good eating habits. Every morning, she has milk and bread for breakfast. "
    "\"What do you like for breakfast?\" her mother asks. \"I like milk and bread,\" Lily answers. "
    "For lunch, she has rice, vegetables and chicken at school. "
    "In the evening, her family eat apples, bananas and oranges after dinner. "
    "Lily drinks water every day. She says, \"Drink water, not cola! It is good for you.\" "
    "She does not like fast food. \"Don't eat too much fast food,\" she often says. "
    "Fruit and milk help her grow tall and strong. Lily is healthy and happy.",
    [Q(1, "What does Lily have for breakfast?", [("A", "rice and chicken"), ("B", "milk and bread"), ("C", "fruit and cola")], "B"),
     Q(2, "What does Lily like?", [("A", "milk and bread"), ("B", "fast food"), ("C", "cola")], "A"),
     Q(3, "What does Lily drink every day?", [("A", "cola"), ("B", "juice"), ("C", "water")], "C"),
     Q(4, "What does Lily say about fast food?", [("A", "Eat it every day"), ("B", "Don't eat too much"), ("C", "It is good for you")], "B"),
     Q(5, "What helps Lily grow tall and strong?", [("A", "fast food and cola"), ("B", "fruit and milk"), ("C", "candy and cakes")], "B")]))

BANK.append(P(5, "reading_b", "食物与日常", "记叙文", ["like", "祈使句"],
    PROV,
    "Sam gets up at seven on Sunday. He is hungry. He wants a big breakfast. "
    "\"What do you have for breakfast?\" his mother asks. \"I like eggs and bread,\" Sam says. "
    "Mother says, \"Please wash your hands first.\" Sam washes his hands. "
    "Then he eats two eggs and some bread. He also drinks a glass of milk. "
    "After breakfast, his mother says, \"Don't forget to brush your teeth.\" Sam brushes his teeth. "
    "Now Sam is full. \"What do you like for lunch?\" his mother asks. "
    "Sam smiles. \"I like rice and chicken. And I like oranges after lunch!\" he answers. "
    "What a happy Sunday!",
    [Q(1, "When does Sam get up?", [("A", "at six"), ("B", "at seven"), ("C", "at eight")], "B"),
     Q(2, "What does Sam like for breakfast?", [("A", "eggs and bread"), ("B", "rice and chicken"), ("C", "fruit")], "A"),
     Q(3, "What does mother ask Sam to do first?", [("A", "brush teeth"), ("B", "wash hands"), ("C", "drink milk")], "B"),
     Q(4, "What does Sam drink?", [("A", "a glass of milk"), ("B", "a cup of cola"), ("C", "a cup of tea")], "A"),
     Q(5, "What does Sam like for lunch?", [("A", "eggs and bread"), ("B", "rice and chicken"), ("C", "milk and bread")], "B")]))

BANK.append(P(7, "reading_a", "复习综合（L1–L6）", "记叙文", ["be 动词", "人称代词", "食物", "一般现在时"],
    PROV,
    "My name is Tom. I am thirteen years old. I am a student at Sunshine Middle School. "
    "I have a good friend. Her name is Alice. She is my classmate. We like English very much. "
    "My mother is a nurse. My father is a doctor. They work very hard. "
    "I get up at six thirty every day. Then I have breakfast. I like milk and eggs. "
    "My sister Lily is eight. She likes fruit and vegetables. "
    "On weekends, we go to the park. We play games and have a good time. "
    "This is my family and my school. I love them all. "
    "Do you have a good family? I think yes.",
    [Q(1, "How old is Tom?", [("A", "twelve"), ("B", "thirteen"), ("C", "fourteen")], "B"),
     Q(2, "Who is Alice?", [("A", "Tom's sister"), ("B", "Tom's classmate"), ("C", "Tom's mother")], "B"),
     Q(3, "What does Tom's father do?", [("A", "a nurse"), ("B", "a teacher"), ("C", "a doctor")], "C"),
     Q(4, "What does Tom like?", [("A", "milk and eggs"), ("B", "fruit and vegetables"), ("C", "cola and candy")], "A"),
     Q(5, "Where do they go on weekends?", [("A", "to the park"), ("B", "to school"), ("C", "to the library")], "A")]))

BANK.append(P(7, "reading_b", "复习综合（L1–L6）", "记叙文", ["be 动词", "食物", "介词"],
    PROV,
    "It is a sunny day. The Greens are at home. Mr Green is in the living room. He is reading a book. "
    "Mrs Green is in the kitchen. She is cooking dinner. There is some rice, fish and vegetables. "
    "Their son David is in his room. He is doing his homework. Their daughter Amy is on the sofa. "
    "She is playing with a cat. The cat is under the table. "
    "At six o'clock, Mrs Green says, \"Dinner is ready! Please come and eat.\" "
    "The family sit at the table. The food is very nice. They talk and laugh. "
    "After dinner, David washes the dishes. Amy cleans the table. "
    "What a happy family!",
    [Q(1, "What is Mr Green doing?", [("A", "reading a book"), ("B", "cooking dinner"), ("C", "doing homework")], "A"),
     Q(2, "Where is Mrs Green?", [("A", "in the living room"), ("B", "in the kitchen"), ("C", "in the garden")], "B"),
     Q(3, "What is Amy doing?", [("A", "playing with a cat"), ("B", "doing homework"), ("C", "washing dishes")], "A"),
     Q(4, "Where is the cat?", [("A", "on the sofa"), ("B", "under the table"), ("C", "in the kitchen")], "B"),
     Q(5, "Who washes the dishes?", [("A", "Amy"), ("B", "Mrs Green"), ("C", "David")], "C")]))

BANK.append(P(9, "reading_a", "学校与方位", "记叙文", ["特殊疑问句", "方位介词", "Where/What/Who"],
    PROV,
    "This is my new school. It is big and beautiful. There are many buildings in it. "
    "The classroom building is in the middle. The library is next to it. "
    "Where is the playground? It is behind the classroom building. "
    "What is on the left of the library? It is the science lab. "
    "Who is our English teacher? She is Miss Green. She is very kind. "
    "Who is that man near the gate? He is our head teacher, Mr White. "
    "Where is the dining hall? It is on the right of the science lab. "
    "Which floor is your classroom on? It is on the third floor. "
    "I like my new school. What about you?",
    [Q(1, "Where is the library?", [("A", "next to the classroom building"), ("B", "behind the playground"), ("C", "in the middle")], "A"),
     Q(2, "Where is the playground?", [("A", "behind the classroom building"), ("B", "on the left of the library"), ("C", "next to the gate")], "A"),
     Q(3, "Who is Miss Green?", [("A", "the head teacher"), ("B", "the English teacher"), ("C", "the science teacher")], "B"),
     Q(4, "Where is the dining hall?", [("A", "on the right of the science lab"), ("B", "in the middle"), ("C", "behind the gate")], "A"),
     Q(5, "Which floor is the classroom on?", [("A", "the first floor"), ("B", "the second floor"), ("C", "the third floor")], "C")]))

BANK.append(P(9, "reading_b", "周末活动", "记叙文", ["特殊疑问句", "选择疑问句"],
    PROV,
    "It is Saturday morning. Kate asks her brother Jack, \"What do you want to do today?\" "
    "\"I want to play basketball,\" Jack says. \"Do you want to play basketball or watch TV?\" Kate asks. "
    "\"Play basketball, of course!\" Jack answers. "
    "\"Who will go with us?\" Kate asks. \"Our friend Ben,\" Jack says. "
    "\"Where shall we meet?\" Kate asks. \"Let's meet at the gate of the park at nine.\" "
    "\"How will we get there?\" Kate asks. \"We can ride our bikes,\" Jack answers. "
    "At nine o'clock, they meet at the gate. They play basketball for two hours. "
    "They are tired but very happy. \"When shall we play again?\" Ben asks. "
    "\"Next Saturday!\" Kate and Jack say together.",
    [Q(1, "What does Jack want to do?", [("A", "play basketball"), ("B", "watch TV"), ("C", "ride bikes")], "A"),
     Q(2, "Who will go with them?", [("A", "Kate's mother"), ("B", "Ben"), ("C", "their teacher")], "B"),
     Q(3, "Where do they meet?", [("A", "at the gate of the park"), ("B", "at school"), ("C", "at the library")], "A"),
     Q(4, "How do they get to the park?", [("A", "by bus"), ("B", "on foot"), ("C", "by bike")], "C"),
     Q(5, "When will they play again?", [("A", "next Saturday"), ("B", "next Sunday"), ("C", "today")], "A")]))

BANK.append(P(10, "reading_a", "日常作息", "记叙文", ["一般现在时三单", "does"],
    PROV,
    "Tom is a middle school student. He gets up at six thirty every day. "
    "He has breakfast at seven. Then he goes to school. He studies hard at school. "
    "He likes English and maths. His best friend Bob likes science and music. "
    "After school, Tom plays basketball with his friends. "
    "In the evening, he does his homework. He watches TV for half an hour. "
    "He goes to bed at ten. "
    "Does Tom get up late on weekends? No, he doesn't. He gets up at seven on weekends too. "
    "Does his mother cook breakfast for him? Yes, she does. She makes eggs, milk and bread. "
    "Tom loves his family. He is a good student.",
    [Q(1, "When does Tom get up?", [("A", "at six"), ("B", "at six thirty"), ("C", "at seven")], "B"),
     Q(2, "What does Bob like?", [("A", "English and maths"), ("B", "science and music"), ("C", "basketball")], "B"),
     Q(3, "What does Tom do in the evening?", [("A", "plays basketball"), ("B", "does his homework"), ("C", "goes to the park")], "B"),
     Q(4, "Does Tom get up late on weekends?", [("A", "Yes, he does"), ("B", "No, he doesn't"), ("C", "We don't know")], "B"),
     Q(5, "Who cooks breakfast for Tom?", [("A", "his father"), ("B", "his grandmother"), ("C", "his mother")], "C")]))

BANK.append(P(10, "reading_b", "家人习惯", "记叙文", ["一般现在时三单", "频度"],
    PROV,
    "I am Anna. There are four people in my family. My father is a teacher. "
    "He teaches maths at a middle school. He goes to work by bus. "
    "My mother is a doctor. She works at a hospital. She is very busy. "
    "My brother Sam is ten. He likes drawing. He draws pictures every day. "
    "I am twelve. I like reading. I read books in the library after school. "
    "On Sundays, we have a big dinner together. Mother cooks fish and vegetables. "
    "Father washes the fruit. Sam and I set the table. "
    "We talk and laugh at the table. My family is warm and happy. "
    "I love my family very much.",
    [Q(1, "What does Anna's father do?", [("A", "a doctor"), ("B", "a teacher"), ("C", "a worker")], "B"),
     Q(2, "How does father go to work?", [("A", "by bus"), ("B", "by bike"), ("C", "on foot")], "A"),
     Q(3, "What does Sam like doing?", [("A", "reading"), ("B", "drawing"), ("C", "cooking")], "B"),
     Q(4, "What does mother cook on Sundays?", [("A", "fish and vegetables"), ("B", "rice and eggs"), ("C", "noodles")], "A"),
     Q(5, "Where does Anna read books?", [("A", "at home"), ("B", "in the library"), ("C", "in the park")], "B")]))

BANK.append(P(11, "reading_a", "图书馆规则", "应用文", ["祈使句", "must/have to"],
    PROV,
    "Welcome to our school library. Please read the library rules. "
    "First, you must keep quiet in the library. Don't talk loudly. "
    "Second, you must show your student card when you come in. "
    "Third, you can borrow two books at a time. You must return them in two weeks. "
    "Don't write or draw in the books. Be kind to the books. "
    "Don't eat or drink in the library, please. "
    "If you have questions, ask the librarian for help. "
    "You must put the books back on the shelves after you read them. "
    "The library opens at eight in the morning and closes at six in the afternoon. "
    "Please follow these rules. Have a nice time in our library!",
    [Q(1, "How many books can you borrow at a time?", [("A", "one"), ("B", "two"), ("C", "three")], "B"),
     Q(2, "When must you return the books?", [("A", "in one week"), ("B", "in two weeks"), ("C", "in a month")], "B"),
     Q(3, "What must you NOT do in the library?", [("A", "talk loudly"), ("B", "keep quiet"), ("C", "ask for help")], "A"),
     Q(4, "What must you show when you come in?", [("A", "your homework"), ("B", "your student card"), ("C", "your ID card")], "B"),
     Q(5, "When does the library open?", [("A", "at eight in the morning"), ("B", "at six in the morning"), ("C", "at nine in the morning")], "A")]))

BANK.append(P(11, "reading_b", "交通安全", "应用文", ["祈使句", "must", "Don't"],
    PROV,
    "There are many cars and buses on the road. We must be careful. "
    "Here are some road rules for students. "
    "First, you must walk on the sidewalk, not in the middle of the road. "
    "Second, you must look left and right before you cross the street. "
    "Third, you must wait for the green light. Don't cross on the red light. "
    "Don't run after a bus. It is very dangerous. "
    "When you ride a bike, you must wear a helmet. "
    "Don't play football on the road, please. "
    "Follow these rules and you will be safe. "
    "Safety comes first. Have a safe day!",
    [Q(1, "Where must you walk?", [("A", "on the sidewalk"), ("B", "in the middle of the road"), ("C", "after a bus")], "A"),
     Q(2, "What must you do before crossing the street?", [("A", "run quickly"), ("B", "look left and right"), ("C", "wait for a bus")], "B"),
     Q(3, "What must you NOT do on the road?", [("A", "wear a helmet"), ("B", "look at the light"), ("C", "play football")], "C"),
     Q(4, "When you ride a bike, what must you wear?", [("A", "a hat"), ("B", "a helmet"), ("C", "a coat")], "B"),
     Q(5, "What is the best title?", [("A", "Road Rules"), ("B", "My School"), ("C", "My Family")], "A")]))

BANK.append(P(12, "reading_a", "食物与购物", "说明文", ["可数/不可数", "some/any", "冠词"],
    PROV,
    "It is Friday afternoon. Lily goes to the supermarket with her mother. "
    "They want to buy some food for the weekend. "
    "First, they buy some apples and bananas. They are fresh and sweet. "
    "Then they buy a bag of rice and a bottle of oil. "
    "Mother asks, \"Do we need any eggs?\" Lily says, \"Yes, we need some eggs.\" "
    "They also buy some milk, but they don't buy any cola. Cola is not good for health. "
    "Lily wants some bread. \"Can I have a piece of bread?\" she asks. "
    "Mother says, \"Of course. Bread is a good breakfast.\" "
    "They buy some vegetables, too. There is no candy in their basket. "
    "Lily is happy. She likes going shopping with her mother.",
    [Q(1, "When do they go shopping?", [("A", "Friday afternoon"), ("B", "Saturday morning"), ("C", "Sunday evening")], "A"),
     Q(2, "What do they NOT buy?", [("A", "colas"), ("B", "apples"), ("C", "milk")], "A"),
     Q(3, "What does Lily want?", [("A", "a piece of bread"), ("B", "a cup of cola"), ("C", "a bag of candy")], "A"),
     Q(4, "Which word is UNCOUNTABLE?", [("A", "apple"), ("B", "egg"), ("C", "rice")], "C"),
     Q(5, "How does Lily feel?", [("A", "sad"), ("B", "happy"), ("C", "tired")], "B")]))

BANK.append(P(12, "reading_b", "野餐", "记叙文", ["some/any", "可数/不可数", "there be"],
    PROV,
    "Today is a fine day. My classmates and I have a picnic in the park. "
    "We bring a lot of food. There is some bread, some fruit and some juice. "
    "There are some sandwiches and hamburgers, too. "
    "Mike asks, \"Is there any water? I am thirsty.\" "
    "Lucy says, \"Yes, there is some water in this bottle. But there isn't any tea.\" "
    "We sit on the grass and eat. The food is very nice. "
    "After lunch, we play games. Some students play football. Some students fly kites. "
    "There is a small river near the park. We see some fish in it. "
    "We have a lot of fun. I hope we can have a picnic again next week.",
    [Q(1, "Where do they have a picnic?", [("A", "in the park"), ("B", "at school"), ("C", "at home")], "A"),
     Q(2, "What does Mike want to drink?", [("A", "tea"), ("B", "juice"), ("C", "water")], "C"),
     Q(3, "Is there any tea?", [("A", "Yes, there is"), ("B", "No, there isn't"), ("C", "We don't know")], "B"),
     Q(4, "What do some students do after lunch?", [("A", "fly kites"), ("B", "sleep"), ("C", "swim")], "A"),
     Q(5, "What do they see in the river?", [("A", "some fish"), ("B", "some ducks"), ("C", "some boats")], "A")]))


def main():
    out = os.path.join(HERE, "passage_bank_supplement.json")
    json.dump(BANK, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("补充语篇库生成：%s (%d 篇)" % (out, len(BANK)))
    for p in BANK:
        print("  %s | %s | %s 词 | 熟词率 %s | 题 %d" %
              (p["id"], p["genre"], p["word_count"], p["vocab_rate"], len(p["questions"])))
    # 校验：每题答案字母必须出现在选项里
    for p in BANK:
        for q in p["questions"]:
            letters = [o[0] for o in q["opts"]]
            if q["answer"] not in letters:
                raise SystemExit("答案 %s 不在选项 %s（%s）" % (q["answer"], letters, p["id"]))
    print("答案校验 OK")


if __name__ == "__main__":
    main()
