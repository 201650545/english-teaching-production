# -*- coding: utf-8 -*-
"""邓兴华 L07 阶段测试Ⅰ 配套练习（中等）内容定义
覆盖 L01-L06 全部 18 考点（G01-G18）+ 120 词
不含听力，笔试 100 分（含语法诊断附件 10 分不计入考试）
语篇来源：真题母本改编 + 教师授权原创
"""
import json, os, re, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))

def _load(name, fname):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, fname))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

bp = _load("bp", "build_practice_paper.py")

def split_paras(text, per=3):
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip())
             if s.strip() and s.strip() not in ("A", "A.")]
    return [" ".join(sents[i:i+per]) for i in range(0, len(sents), per)]

# ============================================================
# 阅读 A 篇：A Student Information Card（应用文，86词）
# 母本：2025 湖南省卷 阅读A 应用文（学生信息卡类）改编
# 考点：G06 Who提问、G08 基数词、G14 What提问、G07 所有格
# ============================================================
reading_a = {
    "id": "HN2025_L07_reading_a",
    "genre": "应用文",
    "difficulty": "中",
    "word_count": 86,
    "provenance": "母本：2025 湖南省卷 阅读A 应用文改编",
    "paragraphs": split_paras(
        "Hello! My name is Li Wei. I am a student at Sunshine Middle School. "
        "I am twelve years old. My birthday is in May. "
        "I am from China. I live in Changsha with my family. "
        "My father is a teacher and my mother is a doctor. I have a brother. "
        "His name is Li Ming. He is a student, too. "
        "My phone number is 138-4521-6790. My email is liwei2024@email.com. "
        "I like English and sports. My favorite subject is English. "
        "Welcome to my school! Let's be friends.",
        per=3
    ),
    "questions": [
        {"num": 1, "q": "Who is Li Wei?", "opts": [["A","a student"],["B","a teacher"],["C","a doctor"]], "answer": "A"},
        {"num": 2, "q": "How old is Li Wei?", "opts": [["A","twelve"],["B","eleven"],["C","thirteen"]], "answer": "A"},
        {"num": 3, "q": "What is Li Wei's phone number?", "opts": [["A","138-4521-6790"],["B","139-4521-6790"],["C","138-4512-6790"]], "answer": "A"},
        {"num": 4, "q": "What subject does Li Wei like?", "opts": [["A","math"],["B","Chinese"],["C","English"]], "answer": "C"},
        {"num": 5, "q": "What is the passage mainly about?", "opts": [["A","Li Wei's school"],["B","Li Wei's family only"],["C","Li Wei's information"]], "answer": "C"},
    ],
    "绑定": "G06·G08·G14·G07",
}

# ============================================================
# 阅读 B 篇：My Busy School Week（记叙文，107词）
# 母本：2025 长沙卷 阅读B 记叙文改编
# 考点：G11 形容词、G15 like+复数/to do、G16 一般现在时、G18 want to do
# ============================================================
reading_b = {
    "id": "HN2025_L07_reading_b",
    "genre": "记叙文",
    "difficulty": "中",
    "word_count": 109,
    "provenance": "母本：2025 长沙卷 阅读B 记叙文改编",
    "paragraphs": split_paras(
        "I am Tom. I have a busy week at school. On Monday, I have English and math. "
        "They are interesting but difficult. I like to read English books with my friends. "
        "On Tuesday and Thursday, I play basketball after class. It is fun and relaxing. "
        "My team is good. We have a match on Friday. I want to score for my team. "
        "On Wednesday, I clean my room. For breakfast, I eat bread and drink milk. "
        "For lunch, I have rice and chicken at school. "
        "My mother says, \"Don't eat too much fast food!\" I like fruit and vegetables. "
        "They are healthy. I want to be a strong player.",
        per=3
    ),
    "questions": [
        {"num": 1, "q": "What does Tom do on Tuesday and Thursday?", "opts": [["A","plays basketball"],["B","reads books"],["C","cleans his room"]], "answer": "A"},
        {"num": 2, "q": "What does Tom think of English and math?", "opts": [["A","easy and fun"],["B","interesting but difficult"],["C","boring"]], "answer": "B"},
        {"num": 3, "q": "What does the underlined word \"busy\" mean in Chinese?", "opts": [["A","忙碌的"],["B","轻松的"],["C","无聊的"]], "answer": "A"},
        {"num": 4, "q": "Why does Tom eat fruit and vegetables?", "opts": [["A","they are cheap"],["B","they are healthy"],["C","his mother cooks them"]], "answer": "B"},
        {"num": 5, "q": "What does Tom want to be?", "opts": [["A","a teacher"],["B","a strong player"],["C","a doctor"]], "answer": "B"},
    ],
    "绑定": "G11·G15·G16·G18",
}

# ============================================================
# 阅读 C 篇：A Healthy Eating Corner（说明文，106词）
# 母本：2025 湘西卷 阅读C 说明文改编
# 考点：G09 Where+There be、G12 方位介词、G17 可数/不可数
# ============================================================
reading_c = {
    "id": "HN2025_L07_reading_c",
    "genre": "说明文",
    "difficulty": "中",
    "word_count": 107,
    "provenance": "母本：2025 湘西卷 阅读C 说明文改编",
    "paragraphs": split_paras(
        "In our classroom, there is a Healthy Eating Corner. It is next to the window. "
        "On the table, there are apples, bananas and oranges. They are fruit. "
        "Under the table, there are tomatoes and potatoes. They are vegetables. "
        "Behind the table, there is milk and bread. Milk is a drink. We don't have any snack or sweet things. "
        "They are unhealthy. There is a shelf on the wall. "
        "On the shelf, you can see a picture of healthy food. "
        "Our teacher says, \"Eat well and keep healthy!\" We like this corner. "
        "It helps us learn about food. Do you want to have one in your classroom, too?",
        per=3
    ),
    "questions": [
        {"num": 1, "q": "Where is the Healthy Eating Corner?", "opts": [["A","next to the window"],["B","behind the door"],["C","under the desk"]], "answer": "A"},
        {"num": 2, "q": "What is under the table?", "opts": [["A","apples and bananas"],["B","tomatoes and potatoes"],["C","milk and bread"]], "answer": "B"},
        {"num": 3, "q": "What is on the shelf?", "opts": [["A","a picture of healthy food"],["B","some fruit"],["C","some milk"]], "answer": "A"},
        {"num": 4, "q": "Why don't they have snacks?", "opts": [["A","they are too expensive"],["B","they are unhealthy"],["C","they are not delicious"]], "answer": "B"},
        {"num": 5, "q": "What is the passage mainly about?", "opts": [["A","a healthy eating corner in the classroom"],["B","how to cook food"],["C","a school sports day"]], "answer": "A"},
    ],
    "绑定": "G09·G12·G17",
}

# ============================================================
# 五选四：My School Life（综合短文，106词）
# 母本：2025 湖南省卷 五选四改编
# 考点：G09 Where/There be、G12 方位介词、G11 形容词、G13 祈使、G15 like
# ============================================================
w5 = {
    "id": "HN2025_L07_w5",
    "title": "阅读下面短文，从方框中选出可以填入空白处的最佳选项（有一项为多余选项）",
    "paragraphs": split_paras(
        "I am Lily. I am a new student at this school. I am from a small city. "
        "___1___ My classroom is on the second floor. It is big and clean. "
        "There are forty desks and chairs in it. The walls are white and nice. "
        "___2___ She is nice and helpful. She helps me with my lessons. "
        "I like my new school life. After class, I play with my friends on the playground. "
        "___3___ It is fun and relaxing. We have a good time together. "
        "On weekends, I do my homework and read books at home. "
        "___4___ My room is always tidy. I think a clean room helps me study well.",
        per=2
    ),
    "candidates": [
        ["A", "I am happy to be here."],
        ["B", "My teacher is Miss Wang."],
        ["C", "We play basketball on the playground."],
        ["D", "I also clean my room."],
        ["E", "I don't like sports."],
    ],
    "answers": {"1": "A", "2": "B", "3": "C", "4": "D"},
}

# ============================================================
# 完形填空（86词，3选项，10空）
# 母本：2025 湖南省卷 完形填空改编
# 考点：G01 主格/宾格、G02 物主代词、G03 be搭配、G07 所有格、G10 复数
# ============================================================
cloze = {
    "id": "HN2025_L07_cloze",
    "title": "阅读短文，从每题所给的 A、B、C 三个选项中选出最佳选项",
    "paragraphs": split_paras(
        "Hello, everyone! Let ___1___ tell you about my friend. "
        "___2___ name is Jack. He ___3___ a student at No. 5 Middle School. "
        "Jack and I ___4___ in the same class. We are good friends. "
        "Our ___5___ teacher is Miss Li. She is very kind and nice. "
        "Jack has two ___6___ in his pencil box. They are new. "
        "This is ___7___ ruler. That ruler is ___8___. "
        "Jack's ___9___ is a doctor. He helps many people. "
        "They are ___10___ friends. We study and play together every day.",
        per=3
    ),
    "items": [
        {"num": 1, "opts": [["A","I"],["B","me"],["C","my"]], "answer": "B"},
        {"num": 2, "opts": [["A","He"],["B","His"],["C","Her"]], "answer": "B"},
        {"num": 3, "opts": [["A","am"],["B","is"],["C","are"]], "answer": "B"},
        {"num": 4, "opts": [["A","am"],["B","is"],["C","are"]], "answer": "C"},
        {"num": 5, "opts": [["A","English"],["B","Englishs"],["C","Englishes"]], "answer": "A"},
        {"num": 6, "opts": [["A","pen"],["B","pens"],["C","penses"]], "answer": "B"},
        {"num": 7, "opts": [["A","he"],["B","his"],["C","him"]], "answer": "B"},
        {"num": 8, "opts": [["A","my"],["B","me"],["C","mine"]], "answer": "C"},
        {"num": 9, "opts": [["A","father"],["B","fathers"],["C","father's"]], "answer": "C"},
        {"num": 10, "opts": [["A","good"],["B","well"],["C","best"]], "answer": "A"},
    ],
    "绑定": "G01·G02·G03·G07·G10",
}

# ============================================================
# 选词填空（64词，10空：6不变形+4考语法）
# 37考G05 be否定疑问、38考G10名词复数、39考G02物主变形、40考G16一般现在时
# 母本：2025 湖南省卷 语法填空改编
# ============================================================
grammar_fill = {
    "id": "HN2025_L07_wordbank",
    "title": "从方框内选择适当的词并用其正确形式填空（每空限填一词，每词限用一次）",
    "paragraphs": [
        "A: ___1___ you a new student here?\n"
        "B: Yes, I ___2___. My name is Mary.\n"
        "A: Is this your ___3___ day?\n"
        "B: Yes. I don't know the ___4___ here.\n"
        "A: Let me ___5___ you. That is our ___6___.\n"
        "B: ___7___ (be) the library next to it?\n"
        "A: Yes. There are many ___8___ (book) in it.\n"
        "B: Is that bag ___9___ (you)?\n"
        "A: No. I ___10___ (have) a blue bag."
    ],
    "word_bank": ["you", "am", "one", "student", "help", "library", "is", "book", "your", "have"],
    "answers": ["Are", "am", "first", "students", "help", "library", "Is", "books", "yours", "have"],
    "绑定": "G05·G10·G02·G16",
}

# ============================================================
# 简答与翻译（86词，5题：3简答+1一般疑问+1英译中）
# 考点：G06 Who、G09 Where/There be、G13/G14 What/祈使、G05 be疑问
# ============================================================
sa = {
    "id": "DXH2026_L07_sa",
    "title": "阅读短文，回答问题或按要求完成句子",
    "paragraphs": split_paras(
        "My name is Anna. I am from China. I am a student at No. 3 Middle School. "
        "My best friend is Lily. She is a kind girl. We study and play together. "
        "Our classroom is on the second floor. There is a big desk in the front. "
        "On the wall, there is a map of China. "
        "Our teacher says, \"Keep your desk clean!\" We all have good habits. "
        "I like my school. Do you want to visit our school? "
        "We can show you around. Welcome!",
        per=3
    ),
    "questions": [
        {"num": 1, "q": "Who is Anna's best friend?", "type": "简答", "answer": "Lily. (Her best friend is Lily.)"},
        {"num": 2, "q": "Where is Anna's classroom?", "type": "简答", "answer": "On the second floor."},
        {"num": 3, "q": "What does the teacher say?", "type": "简答", "answer": "\"Keep your desk clean!\""},
        {"num": 4, "q": "Is there a map of China on the wall? Why do you think so?", "type": "一般疑问", "answer": "Yes, there is. The passage says \"On the wall, there is a map of China.\""},
        {"num": 5, "q": "将文中划线句子 \"We can show you around.\" 译成中文。", "type": "翻译", "answer": "我们可以带你参观。"},
    ],
    "绑定": "G06·G09·G13·G14·G05",
}

# ============================================================
# 书面表达（15分，80词）
# 话题：自我介绍+家庭+兴趣+饮食综合
# ============================================================
writing = {
    "id": "DXH2026_L07_writing",
    "title": "书面表达（15 分）",
    "prompt": "请用英语写一篇短文，介绍你自己、你的家庭、你的兴趣爱好以及你的饮食习惯。",
    "requirements": "1. 综合运用 L1-L6 所学词汇与语法（be 动词、代词、所有格、一般现在时、like/want to do 等）；\n2. 80 词左右；\n3. 条理清楚，语句通顺，可适当发挥。",
    "sample": "Hello! My name is Tom. I am a student at Sunshine Middle School. I am twelve years old. "
              "There are four people in my family — my father, my mother, my brother and me. "
              "My father is a teacher. My mother is a doctor. I love my family. "
              "I like sports. I play basketball with my friends after class. It is fun and relaxing. "
              "I also like English. I want to read more English books. "
              "For breakfast, I eat bread and drink milk. For lunch, I have rice and chicken. "
              "I like fruit and vegetables. They are healthy. I don't want to eat fast food. "
              "I want to be strong and healthy.",
    "绑定": "G01-G18 综合",
}

# ============================================================
# 语法诊断（10题：5选择+5填空）
# 47-56 覆盖 G01-G18 全部18考点
# ============================================================
grammar_diag = {
    "id": "DXH2026_L07_grammar",
    "title": "语法复盘（G01-G18 全考点诊断）",
    "mc": [
        # 47: G01 主格/宾格
        {"num": 1, "q": "Please call ___ tomorrow.", "opts": [["A","I"],["B","me"],["C","my"]], "answer": "B"},
        # 48: G02 物主代词
        {"num": 2, "q": "This is my book. That book is ___.", "opts": [["A","your"],["B","you"],["C","yours"]], "answer": "C"},
        # 49: G03 be动词搭配
        {"num": 3, "q": "He ___ a student. They ___ teachers.", "opts": [["A","is; are"],["B","are; is"],["C","am; are"]], "answer": "A"},
        # 50: G04 指示代词
        {"num": 4, "q": "Look at ___ books on the desk. They are mine.", "opts": [["A","this"],["B","that"],["C","these"]], "answer": "C"},
        # 51: G05 be否定/疑问
        {"num": 5, "q": "— ___ she your English teacher? — No, she ___.", "opts": [["A","Is; isn't"],["B","Are; aren't"],["C","Is; isn't"]], "answer": "C"},
    ],
    "fill": [
        # 52: G06 Who疑问句
        {"q": "用适当的疑问词填空：— ___ is that boy? — He is my brother.", "answer": "Who"},
        # 53: G07 名词所有格
        {"q": "用所给词的所有格形式填空：This is ___ (Tom) desk.", "answer": "Tom's"},
        # 54: G08 基数词
        {"q": "用英语写出数字：28 → ___", "answer": "twenty-eight"},
        # 55: G09+G12 Where/方位
        {"q": "用适当的介词填空：The ball is ___ the table (在桌子下面).", "answer": "under"},
        # 56: G10-G18 综合
        {"q": "用所给词的正确形式填空：I ___ (like) apples, but I ___ (not like) bananas. (用一般现在时填空)", "answer": "like; don't like"},
    ],
}

# ============================================================
# 组装内容
# ============================================================
content = {
    "_doc": "邓兴华 L07 阶段测试Ⅰ配套练习（中等）· 覆盖 L01-L06 全部 18 考点 + 120 词。不含听力。",
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

card = {
    "lesson": 7,
    "student": "邓兴华",
    "tier": "中等",
    "stage": "S2",
    "type": "test",
    "grammar": ["G01-G18 全部18考点"],
    "theme": "阶段测试Ⅰ·七上基础综合诊断",
    "vocab": {"new_count": 0, "review_count": 120, "theme": "综合"},
    "phonics": "无（测试课）",
    "listening": False,
}

out = os.path.join(os.path.dirname(HERE), "邓兴华", "第07课时", "第07课时_配套练习.docx")
p = bp.build_practice(card, content, out)
print("阶段测试卷生成：%s (%d bytes)" % (p, os.path.getsize(p)))
