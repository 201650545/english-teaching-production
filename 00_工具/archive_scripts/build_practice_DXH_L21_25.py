# -*- coding: utf-8 -*-
"""邓兴华 L21-L25 配套练习批量生成（真实题目版 · exam_spec v2026.2）
- L21 = 阶段测试卷（100 分标准卷，蓝图 4.1：阅读40/语言20/综合30/语法诊断10，G01-G54 全覆盖）
- L22-25 = 授课课配套练习（阅读30/语言25/综合25/语法诊断20）
格式统一 L05 compact：Times New Roman；标题16pt粗居中；节题14pt / 小标题12pt粗左；正文/选项10.5pt。
"""
import os, json, sys, importlib.util

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = r"D:\英语教学\邓兴华"

# 复用 build_practice_paper 的渲染辅助函数
_spec = importlib.util.spec_from_file_location("bpp", os.path.join(HERE, "build_practice_paper.py"))
bpp = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(bpp)
_para = bpp._para; _heading = bpp._heading; _section = bpp._section; _sub = bpp._sub
_passage = bpp._passage; _options3 = bpp._options3; _question = bpp._question
_renumber = bpp._renumber; _ans_runs = bpp._ans_runs; _table = bpp._table
_set_font = bpp._set_font; _render_answer_card = bpp._render_answer_card

# ─────────────────────────── L22 内容 ───────────────────────────
L22 = {
 "reading_a": {"id":"DXH2026_L22_reading_a","genre":"应用文","difficulty":"中","word_count":192,
   "绑定":"G55比较级 / G56最高级 / 城市比较",
   "paragraphs":[
    "Comparing Two Cities",
    "Beijing and Guilin are two famous cities in China. Beijing is bigger than Guilin, and it has more people. The buildings in Beijing are taller than the ones in Guilin.",
    "However, Guilin is more beautiful than Beijing in some ways. The mountains and rivers there are more popular with tourists. The food in Guilin is cheaper than the food in big cities.",
    "Beijing is more expensive for visitors, but it has more museums and parks. Guilin is quieter and cleaner. Which city is better? It depends on what you like. Some people like the busy city, and some like the quiet one.",
    "In a word, both cities are great, but they are different. Comparing them helps us understand what each city is good at."],
   "questions":[
    {"num":1,"q":"Which city is bigger, Beijing or Guilin?","opts":[["A","Beijing."],["B","Guilin."],["C","They are the same."]],"answer":"A"},
    {"num":2,"q":"Why is Guilin more popular with tourists?","opts":[["A","Because of its mountains and rivers."],["B","Because it has more museums."],["C","Because it is bigger."]],"answer":"A"},
    {"num":3,"q":"What does the writer say about the food in Guilin?","opts":[["A","It is cheaper than food in big cities."],["B","It is more expensive."],["C","It is not good."]],"answer":"A"}]},
 "reading_b": {"id":"DXH2026_L22_reading_b","genre":"记叙文","difficulty":"中","word_count":215,
   "绑定":"G55比较级 / G56最高级 / 人物比较",
   "paragraphs":[
    "Two Friends",
    "I have two good friends, Tom and Mary. They are very different, and I love them both.",
    "Tom is more outgoing than Mary. He likes to talk and make jokes with everyone. He is also more humorous, so people around him feel happy. Tom is hard-working and often gets the highest score in our class.",
    "Mary is quieter than Tom, but she is more friendly. She is always ready to help others. She is talented in music and can play the piano very well. Mary is more creative than most of us when she draws pictures.",
    "Tom is taller and lazier than Mary. Sometimes he forgets to do his homework. On the other hand, Mary is the most careful student I know.",
    "Although they are different, they are both important to me. They teach me that everyone has his own advantages."],
   "questions":[
    {"num":1,"q":"Who is more outgoing, Tom or Mary?","opts":[["A","Tom."],["B","Mary."],["C","Both."]],"answer":"A"},
    {"num":2,"q":"What is Mary good at?","opts":[["A","Playing the piano and drawing."],["B","Making jokes."],["C","Running fast."]],"answer":"A"},
    {"num":3,"q":"What does the writer think of Mary?","opts":[["A","She is the most careful student he knows."],["B","She is lazy."],["C","She is not friendly."]],"answer":"A"},
    {"num":4,"q":"What does the underlined word \"humorous\" most probably mean?","opts":[["A","有趣的"],["B","严肃的"],["C","安静的"]],"answer":"A"}]},
 "reading_c": {"id":"DXH2026_L22_reading_c","genre":"说明文","difficulty":"中","word_count":215,
   "绑定":"G55比较级 / G56最高级 / 比较的意义",
   "paragraphs":[
    "Why Comparisons Help",
    "People often compare things with others. Comparing is not always a bad thing. It can help us improve ourselves.",
    "For example, when you compare your grades with a hard-working friend, you may want to study harder. When you see a faster runner, you practice more. In this way, you become better than before.",
    "But comparing can also make you unhappy if you only look at others' advantages. Everyone is different. Tom may be taller than you, but you may be smarter. Mary may be more popular, but you may be more creative.",
    "The best way is to compare yourself with yourself. Ask yourself: Am I better than I was last year? If the answer is yes, you are making progress.",
    "Remember, the most important competition is not with others, but with yourself."],
   "questions":[
    {"num":1,"q":"According to the passage, why can comparing be helpful?","opts":[["A","It helps us improve ourselves."],["B","It makes us sad."],["C","It is not important."]],"answer":"A"},
    {"num":2,"q":"What is the best way to compare according to the writer?","opts":[["A","Compare yourself with yourself."],["B","Compare with the tallest person."],["C","Compare with the fastest runner."]],"answer":"A"},
    {"num":3,"q":"What does the writer think is the most important competition?","opts":[["A","The competition with yourself."],["B","The competition with others."],["C","The competition in class."]],"answer":"A"},
    {"num":4,"q":"What is the main idea of the passage?","opts":[["A","Comparing can help us improve if we do it well."],["B","Comparing is always bad."],["C","We should never compare."]],"answer":"A"}]},
 "w5": {"id":"DXH2026_L22_w5","title":"根据短文内容，从方框中选出最佳句子填入文中空白处（有一项多余）",
   "绑定":"G55/G56/G57 同级比较",
   "paragraphs":[
    "My Best Friend",
    "I want to tell you about my best friend, Anna.",
    "Anna is as tall as me. ___1___ We often study together.",
    "She is smarter than most students, but she is never proud. ___2___ When I have problems, she always helps me.",
    "I am more outgoing than Anna, and I like to talk. ___3___ We are different, but we get on well.",
    "I think friendship is the most valuable thing in the world. ___4___"],
   "candidates":[["A","She is also very friendly and kind."],["B","I hope our friendship lasts forever."],["C","She likes to share funny stories with me."],["D","Both of us like reading books."],["E","Anna is the tallest girl in our school."]],
   "answers":{"1":"D","2":"A","3":"C","4":"B"}},
 "cloze": {"id":"DXH2026_L22_cloze","title":"完形填空",
   "绑定":"G55/G56/G57 比较最高级同级",
   "paragraphs":[
    "My school is very ___1___. There are many new ___2___ and a big playground.",
    "Our classroom is ___3___ than the old one. The desks are ___4___ and the chairs are comfortable.",
    "Among all the teachers, Miss Li is the ___5___ popular one. She teaches math ___6___ than other teachers.",
    "The library is ___7___ quiet place in the school. I like reading there every day.",
    "This year, our school is ___8___ beautiful than last year. We are all ___9___ in making it better.",
    "I think my school is the ___10___ school in our city."],
   "items":[
    {"num":1,"opts":[["A","big"],["B","bigger"],["C","biggest"]],"answer":"A"},
    {"num":2,"opts":[["A","building"],["B","buildings"],["C","building's"]],"answer":"B"},
    {"num":3,"opts":[["A","bright"],["B","brighter"],["C","brightest"]],"answer":"B"},
    {"num":4,"opts":[["A","new"],["B","newer"],["C","newest"]],"answer":"A"},
    {"num":5,"opts":[["A","much"],["B","more"],["C","most"]],"answer":"C"},
    {"num":6,"opts":[["A","good"],["B","well"],["C","better"]],"answer":"C"},
    {"num":7,"opts":[["A","a"],["B","an"],["C","the"]],"answer":"C"},
    {"num":8,"opts":[["A","very"],["B","more"],["C","most"]],"answer":"B"},
    {"num":9,"opts":[["A","interest"],["B","interested"],["C","interesting"]],"answer":"B"},
    {"num":10,"opts":[["A","good"],["B","better"],["C","best"]],"answer":"C"}]},
 "grammar_fill": {"id":"DXH2026_L22_grammar_fill","title":"从方框内选择适当的词并用其正确形式填空（每空限填一词）",
   "绑定":"G55/G56/G57",
   "word_bank":["tall","cheap","popular","fast","friendly","quiet","smart","lazy","big","expensive","extra","extra"],
   "paragraphs":[
    "Tom is ___1___ than his brother. He can reach the top shelf.",
    "This shop is ___2___ than that one, so I buy things here.",
    "Among all colors, blue is the ___3___ with my classmates.",
    "He runs ___4___ than me, so he always wins the race.",
    "Our new teacher is ___5___ than the old one; she always smiles.",
    "The library is the ___6___ place, so I can read there.",
    "Mary is ___7___ in our class; she answers every question.",
    "Don't be ___8___; work hard and you will succeed.",
    "Beijing is ___9___ in China.",
    "This watch is ___10___ than the one I bought last year."],
   "answers":["taller","cheaper","most popular","faster","friendlier","quietest","the smartest","lazy","the biggest","more expensive"]},
 "sa": {"id":"DXH2026_L22_sa","title":"阅读表达",
   "passage_title":"My Two Pets",
   "绑定":"G55/G56 比较",
   "paragraphs":[
    "I have two pets, a dog and a cat. The dog is bigger than the cat, and it runs faster.",
    "The dog is more active, but the cat is lazier and sleeps all day. The dog is friendlier and always welcomes me home.",
    "The cat is quieter and cleaner. It is also smarter because it can open the door by itself.",
    "I love both of them. They are the best pets in the world."],
   "questions":[
    {"num":1,"q":"Which pet is bigger, the dog or the cat?","answer":"The dog.","type":"简答"},
    {"num":2,"q":"Why does the writer say the cat is lazier?","answer":"Because it sleeps all day.","type":"简答"},
    {"num":3,"q":"What can the cat do by itself?","answer":"It can open the door by itself.","type":"简答"},
    {"num":4,"q":"请把文中画线句子翻译成汉语（They are the best pets in the world.）","answer":"它们是世界上最好的宠物。","type":"翻译"},
    {"num":5,"q":"Do the writer and his pets get on well? How do you know?","answer":"Yes. The writer says he loves both of them.","type":"简答"}]},
 "writing": {"id":"DXH2026_L22_writing","title":"书面表达",
   "prompt":"假如你是李华，请用英语写一篇80词左右的短文，比较你和你的好朋友（如身高、性格、爱好等），并说明你们为什么能成为好朋友。",
   "sample":[
    "My Good Friend",
    "I have a good friend named Wang Lei. We are both twelve years old.",
    "He is taller than me, and he runs faster than I do. But I am more outgoing than him, so I like to talk to new people.",
    "Wang Lei is harder-working and always gets good grades. He is also more humorous and makes me laugh. Although we are different, we both like playing basketball.",
    "I think we are good friends because we help each other and share the same hobbies. I am glad to have him as my best friend."],
   "requirements":"1. 词数约80词；2. 用比较级/最高级描写；3. 语句通顺，语法正确；4. 可适当发挥。",
   "绑定":"比较级/最高级"}}

# ─────────────────────────── L23 内容 ───────────────────────────
L23 = {
 "reading_a": {"id":"DXH2026_L23_reading_a","genre":"应用文/说明","difficulty":"中","word_count":194,
   "绑定":"G58 if条件句 / 志愿者主题",
   "paragraphs":[
    "If I Become a Volunteer",
    "Volunteering is a good way to help others. If I become a volunteer, I will feel happy every day.",
    "If I have free time on weekends, I will go to the old people's home. If the old people need help, I will read books to them or talk with them.",
    "If it is possible, I will also help clean the park. If many people join together, the city will be more beautiful.",
    "If you want to be a volunteer, you can start with small things. If you help a classmate with his homework, you are already a volunteer.",
    "Remember, if everyone gives a little love, the world will be a better place."],
   "questions":[
    {"num":1,"q":"What will the writer do if he becomes a volunteer?","opts":[["A","Help the old people."],["B","Play games all day."],["C","Stay at home."]],"answer":"A"},
    {"num":2,"q":"When will the writer go to the old people's home?","opts":[["A","If he has free time on weekends."],["B","If he is tired."],["C","If it rains."]],"answer":"A"},
    {"num":3,"q":"According to the passage, what is a small thing you can do?","opts":[["A","Help a classmate with his homework."],["B","Sleep more."],["C","Watch TV."]],"answer":"A"}]},
 "reading_b": {"id":"DXH2026_L23_reading_b","genre":"记叙文","difficulty":"中","word_count":215,
   "绑定":"G58 if / G59 unless / 选择主题",
   "paragraphs":[
    "A Big Decision",
    "Last year I had to make a big decision. I wanted to join the school basketball team, but my parents worried about my study.",
    "My father said, \"If you spend too much time on basketball, your grades will fall.\" My mother said, \"Unless you keep your study first, you cannot join the team.\"",
    "I thought about it carefully. I made a decision: I would study hard first, and then practice basketball after finishing my homework.",
    "I followed my plan. If I was tired, I took a short rest and then went on. Unless it was very late, I practiced every evening.",
    "At the end of the term, my grades were good and I played well in the team. I learned that a good plan and hard work can bring success."],
   "questions":[
    {"num":1,"q":"What did the writer want to do?","opts":[["A","Join the basketball team."],["B","Join the music club."],["C","Sleep more."]],"answer":"A"},
    {"num":2,"q":"What was the parents' worry?","opts":[["A","His grades would fall."],["B","He would be too tall."],["C","He would get hurt."]],"answer":"A"},
    {"num":3,"q":"When did the writer practice basketball?","opts":[["A","After finishing his homework."],["B","Before doing homework."],["C","All day long."]],"answer":"A"},
    {"num":4,"q":"What did the writer learn at last?","opts":[["A","A good plan and hard work bring success."],["B","Basketball is not fun."],["C","Parents are always wrong."]],"answer":"A"}]},
 "reading_c": {"id":"DXH2026_L23_reading_c","genre":"说明文","difficulty":"中","word_count":215,
   "绑定":"G58 if / G13 祈使句 and/or / 计划主题",
   "paragraphs":[
    "Plans for the Future",
    "Making plans for the future is important. If you have a clear goal, you will know what to do every day.",
    "First, set a goal. For example, if you want to be a doctor, you should study science hard now. If you want to be a teacher, work on your speaking and writing.",
    "Second, make a plan and follow it. If you plan your time well, you will have time for both study and fun. Work hard, and you will make progress. Be lazy, or you will fail.",
    "Third, don't be afraid of failure. If you make a mistake, learn from it. Unless you try new things, you will never know what you can do.",
    "In the future, your plan will lead you to success. So start planning today!"],
   "questions":[
    {"num":1,"q":"Why is making plans important?","opts":[["A","Because you will know what to do every day."],["B","Because it makes you tired."],["C","Because it is not necessary."]],"answer":"A"},
    {"num":2,"q":"What should you do if you want to be a doctor?","opts":[["A","Study science hard."],["B","Stop studying."],["C","Play all day."]],"answer":"A"},
    {"num":3,"q":"What does the writer say about failure?","opts":[["A","Learn from it."],["B","Be afraid of it."],["C","Never try again."]],"answer":"A"},
    {"num":4,"q":"What is the passage mainly about?","opts":[["A","How to make plans for the future."],["B","How to be a doctor."],["C","Why failure is bad."]],"answer":"A"}]},
 "w5": {"id":"DXH2026_L23_w5","title":"根据短文内容，从方框中选出最佳句子填入文中空白处（有一项多余）",
   "绑定":"G58 if / G59 unless",
   "paragraphs":[
    "A Clever Choice",
    "It was Friday afternoon, and I had to make a choice.",
    "My friends asked me to go to the movies. ___1___ But I also had a math test on Monday.",
    "If I went to the movies, I would have no time to review. ___2___ So I decided to stay at home and study.",
    "Unless I prepared well, I might fail the test. ___3___ After studying for two hours, I felt confident.",
    "The next day, I told my friends about my plan. ___4___ They all agreed to study with me."],
   "candidates":[["A","I knew I had to study first."],["B","They said I made a wise choice."],["C","I was very happy to go."],["D","I wanted to finish my homework first."],["E","The test was really difficult for me."]],
   "answers":{"1":"D","2":"A","3":"E","4":"B"}},
 "cloze": {"id":"DXH2026_L23_cloze","title":"完形填空",
   "绑定":"G58 if / G59 unless / G13 祈使句",
   "paragraphs":[
    "If you want to ___1___ in your study, you need a good plan.",
    "First, set a ___2___. If you have a clear goal, you will know what to do.",
    "Second, ___3___ your time well. If you waste time, you will ___4___ behind.",
    "Third, ask for ___5___ when you have problems. A good teacher can ___6___ you.",
    "Work hard, ___7___ you will make progress. Be lazy, ___8___ you will fail.",
    "Unless you ___9___ new things, you will not know your ability.",
    "Remember, if you ___10___ your plan every day, success will come."],
   "items":[
    {"num":1,"opts":[["A","succeed"],["B","fail"],["C","sleep"]],"answer":"A"},
    {"num":2,"opts":[["A","question"],["B","goal"],["C","mistake"]],"answer":"B"},
    {"num":3,"opts":[["A","waste"],["B","plan"],["C","forget"]],"answer":"B"},
    {"num":4,"opts":[["A","fall"],["B","jump"],["C","run"]],"answer":"A"},
    {"num":5,"opts":[["A","money"],["B","advice"],["C","food"]],"answer":"B"},
    {"num":6,"opts":[["A","stop"],["B","help"],["C","hurt"]],"answer":"B"},
    {"num":7,"opts":[["A","and"],["B","or"],["C","but"]],"answer":"A"},
    {"num":8,"opts":[["A","and"],["B","or"],["C","so"]],"answer":"B"},
    {"num":9,"opts":[["A","try"],["B","avoid"],["C","refuse"]],"answer":"A"},
    {"num":10,"opts":[["A","forget"],["B","follow"],["C","break"]],"answer":"B"}]},
 "grammar_fill": {"id":"DXH2026_L23_grammar_fill","title":"从方框内选择适当的词并用其正确形式填空（每空限填一词）",
   "绑定":"G58/G59/G13",
   "word_bank":["if","unless","succeed","fail","plan","advice","goal","choice","effort","progress","extra","extra"],
   "paragraphs":[
    "___1___ you study hard, you will pass the exam.",
    "You will ___2___ the test unless you review your notes.",
    "She made a wise ___3___ and joined the reading club.",
    "My ___4___ is to become a great scientist one day.",
    "He gave me some useful ___5___ about learning English.",
    "Work hard, ___6___ you will fail. (and/or)",
    "With great ___7___, he finally ___8___ in the competition.",
    "If you follow your ___9___, you will make ___10___ every week."],
   "answers":["If","fail","choice","goal","advice","or","effort","succeeded","plan","progress"]},
 "sa": {"id":"DXH2026_L23_sa","title":"阅读表达",
   "passage_title":"A Valuable Experience",
   "绑定":"G58 if / G59 unless",
   "paragraphs":[
    "Last summer, I joined a volunteer group. We helped children in the countryside.",
    "If it rained, we stayed inside and read stories to them. If the weather was fine, we played games outside.",
    "Unless we prepared well, we could not finish our tasks on time. So we always made a plan first.",
    "The children were very happy, and so were we. I learned that helping others brings joy."],
   "questions":[
    {"num":1,"q":"What did the volunteer group do for children?","answer":"They read stories and played games with them.","type":"简答"},
    {"num":2,"q":"What did they do if it rained?","answer":"They stayed inside and read stories.","type":"简答"},
    {"num":3,"q":"Why did they always make a plan first?","answer":"Because unless they prepared well, they could not finish tasks on time.","type":"简答"},
    {"num":4,"q":"请翻译画线句（helping others brings joy）","answer":"帮助他人带来快乐。","type":"翻译"},
    {"num":5,"q":"Where did the volunteers help the children?","answer":"In the countryside.","type":"简答"}]},
 "writing": {"id":"DXH2026_L23_writing","title":"书面表达",
   "prompt":"假如你是李华，请写一篇80词左右的短文，用 if / unless 说明你为实现梦想所做的计划，以及你如何坚持。",
   "sample":[
    "My Dream Plan",
    "Everyone has a dream, and so do I. My dream is to be a good doctor in the future.",
    "If I want to realize my dream, I must study science hard now. Unless I work hard every day, I will not be a good doctor.",
    "I make a plan every week. If I have free time, I read more books about medicine. If I meet problems, I ask my teachers for advice.",
    "Work hard, and my dream will come true. I will never give up."],
   "requirements":"1. 词数约80词；2. 用 if / unless 造句；3. 语句通顺；4. 可适当发挥。",
   "绑定":"G58/G59 条件句"}}

# ─────────────────────────── L24 内容 ───────────────────────────
L24 = {
 "reading_a": {"id":"DXH2026_L24_reading_a","genre":"说明文","difficulty":"中","word_count":194,
   "绑定":"G60 原因/让步 / 社交媒体主题",
   "paragraphs":[
    "Why Do Teenagers Love Social Media?",
    "Many teenagers love social media. Why do they like it so much?",
    "First, they can keep in touch with friends easily. Because they can send messages at any time, they feel closer to each other.",
    "Second, social media helps them learn new things. Since there is a lot of information, they can find what they need quickly.",
    "Although social media is fun, it also has problems. Because some people spend too much time on it, they may forget to study. Some false information can also cause trouble.",
    "So teenagers should use social media wisely. Though it is convenient, real friendship needs face-to-face time too."],
   "questions":[
    {"num":1,"q":"Why can teenagers keep in touch with friends easily?","opts":[["A","Because they can send messages at any time."],["B","Because they meet every day."],["C","Because they write letters."]],"answer":"A"},
    {"num":2,"q":"What problem does social media have?","opts":[["A","People may forget to study."],["B","It is too expensive."],["C","It is not fun."]],"answer":"A"},
    {"num":3,"q":"What is the writer's advice at last?","opts":[["A","Use social media wisely."],["B","Never use social media."],["C","Use it all the time."]],"answer":"A"}]},
 "reading_b": {"id":"DXH2026_L24_reading_b","genre":"记叙文","difficulty":"中","word_count":215,
   "绑定":"G60 原因 / G61 结果 / 善意主题",
   "paragraphs":[
    "Because of a Kind Word",
    "A kind word can change a person's life. I learned this from my friend Leo.",
    "Leo was not good at English, so he felt sad about it. Because he was afraid of making mistakes, he never spoke in class.",
    "His teacher noticed this. She said to him, \"You are smart, and you can do better.\" Because of this kind word, Leo decided to try harder.",
    "He studied every day so that he could improve. Although it was difficult at first, he kept going. Since he worked so hard, his grades rose quickly.",
    "Now Leo is confident in English. He often says that one kind word gave him hope. Therefore, we should be kind to others, because our words may become their power."],
   "questions":[
    {"num":1,"q":"Why did Leo never speak in class?","opts":[["A","Because he was afraid of making mistakes."],["B","Because he was too confident."],["C","Because he was lazy."]],"answer":"A"},
    {"num":2,"q":"What did the teacher say to Leo?","opts":[["A","You are smart, and you can do better."],["B","You are not good at English."],["C","You should give up."]],"answer":"A"},
    {"num":3,"q":"Why did Leo's grades rise quickly?","opts":[["A","Because he worked so hard."],["B","Because the test was easy."],["C","Because he stopped studying."]],"answer":"A"},
    {"num":4,"q":"What did Leo learn from his experience?","opts":[["A","A kind word can give hope."],["B","English is too hard."],["C","Teachers are not helpful."]],"answer":"A"}]},
 "reading_c": {"id":"DXH2026_L24_reading_c","genre":"说明文","difficulty":"中","word_count":215,
   "绑定":"G60 原因/让步 / G61 结果目的",
   "paragraphs":[
    "Causes and Effects",
    "Everything has a cause and an effect. Understanding them helps us solve problems.",
    "For example, because some students sleep too late, they feel tired in class. Because they are tired, they cannot focus on their study. As a result, their grades drop.",
    "The solution is simple: go to bed early so that you can get enough sleep. Although it is hard to change a habit, it is worth trying.",
    "Another example is about the environment. Because people throw away too much waste, rivers become dirty. Since the water is dirty, fish cannot live in it.",
    "So we must protect the environment. If everyone does a small thing, the effect will be great. Therefore, let's start from today."],
   "questions":[
    {"num":1,"q":"Why do some students feel tired in class?","opts":[["A","Because they sleep too late."],["B","Because they eat too much."],["C","Because they play too much."]],"answer":"A"},
    {"num":2,"q":"What is the solution to the sleeping problem?","opts":[["A","Go to bed early."],["B","Drink more coffee."],["C","Stay up later."]],"answer":"A"},
    {"num":3,"q":"Why cannot fish live in the dirty river?","opts":[["A","Because the water is dirty."],["B","Because there are too many fish."],["C","Because the water is cold."]],"answer":"A"},
    {"num":4,"q":"What is the passage mainly about?","opts":[["A","Causes and effects of some problems."],["B","How to sleep well."],["C","Why rivers are clean."]],"answer":"A"}]},
 "w5": {"id":"DXH2026_L24_w5","title":"根据短文内容，从方框中选出最佳句子填入文中空白处（有一项多余）",
   "绑定":"G60 原因 / G61 结果",
   "paragraphs":[
    "A Difficult Situation",
    "Last week I was in a difficult situation. My friend asked me to help him with a test, but I knew it was wrong.",
    "Because I wanted to be honest, I said no. ___1___ He was angry at first.",
    "Although he was unhappy, I explained my reason. ___2___ I told him that cheating is not good for anyone.",
    "Since he heard my words, he thought about it carefully. ___3___ He decided to study hard instead of cheating.",
    "Finally, we became better friends. ___4___ I learned that honesty is the best policy."],
   "candidates":[["A","He agreed with me at last."],["B","I helped him prepare for the test honestly."],["C","I was afraid he would be angry."],["D","He did not understand me at first."],["E","So I wanted to help him cheat."]],
   "answers":{"1":"D","2":"C","3":"A","4":"B"}},
 "cloze": {"id":"DXH2026_L24_cloze","title":"完形填空",
   "绑定":"G60 原因让步 / G61 结果目的",
   "paragraphs":[
    "I like my school ___1___ the teachers are kind.",
    "___2___ it is busy, I still enjoy my study here.",
    "Our school has a big library. We can find many books there, ___3___ we always have enough to read.",
    "The teachers help us ___4___ that we can learn well. They explain the lessons ___5___ clearly.",
    "___6___ I do not understand a question, I ask my teacher. ___7___ she is patient, I am not afraid.",
    "I study hard ___8___ I can get good grades. ___9___ I am happy at this school.",
    "I hope ___10___ students can have such a good learning place."],
   "items":[
    {"num":1,"opts":[["A","because"],["B","but"],["C","or"]],"answer":"A"},
    {"num":2,"opts":[["A","Although"],["B","So"],["C","And"]],"answer":"A"},
    {"num":3,"opts":[["A","so"],["B","because"],["C","but"]],"answer":"A"},
    {"num":4,"opts":[["A","so"],["B","because"],["C","although"]],"answer":"A"},
    {"num":5,"opts":[["A","very"],["B","so"],["C","such"]],"answer":"A"},
    {"num":6,"opts":[["A","If"],["B","Because"],["C","So"]],"answer":"A"},
    {"num":7,"opts":[["A","Since"],["B","But"],["C","Or"]],"answer":"A"},
    {"num":8,"opts":[["A","so that"],["B","or"],["C","but"]],"answer":"A"},
    {"num":9,"opts":[["A","Therefore"],["B","Although"],["C","Unless"]],"answer":"A"},
    {"num":10,"opts":[["A","other"],["B","another"],["C","others"]],"answer":"A"}]},
 "grammar_fill": {"id":"DXH2026_L24_grammar_fill","title":"从方框内选择适当的词并用其正确形式填空（每空限填一词）",
   "绑定":"G60/G61",
   "word_bank":["because","since","although","however","therefore","result","cause","reason","problem","solution","extra","extra"],
   "paragraphs":[
    "I stayed at home ___1___ it was raining heavily.",
    "___2___ you are here, let us start the meeting.",
    "___3___ he is young, he knows a lot.",
    "It was hard. ___4___, I did not give up.",
    "I was tired; ___5___, I went to bed early.",
    "As a ___6___ of the rain, the match was put off.",
    "What is the ___7___ of the problem?",
    "Please tell me the ___8___ why you were late.",
    "We need to solve the ___9___ at once.",
    "The best ___10___ is to ask for help."],
   "answers":["because","Since","Although","However","therefore","result","cause","reason","problem","solution"]},
 "sa": {"id":"DXH2026_L24_sa","title":"阅读表达",
   "passage_title":"A Helpful Experience",
   "绑定":"G60/G61 原因结果",
   "paragraphs":[
    "Last month I helped my younger brother with his homework. Because he was weak in math, he often felt sad.",
    "I explained every question clearly so that he could understand. Although it took time, he made progress.",
    "Since he improved, he became more confident. As a result, he began to like math.",
    "I was happy because I could help him. Helping others also makes me a better person."],
   "questions":[
    {"num":1,"q":"Why was the brother sad?","answer":"Because he was weak in math.","type":"简答"},
    {"num":2,"q":"How did the writer help his brother?","answer":"He explained every question clearly.","type":"简答"},
    {"num":3,"q":"What happened after the brother improved?","answer":"He became more confident and began to like math.","type":"简答"},
    {"num":4,"q":"请翻译画线句（Helping others also makes me a better person.）","answer":"帮助他人也使我自己变得更好。","type":"翻译"},
    {"num":5,"q":"What subject was the brother weak in?","answer":"Math.","type":"简答"}]},
 "writing": {"id":"DXH2026_L24_writing","title":"书面表达",
   "prompt":"假如你是李华，请写一篇80词左右的短文，说明你喜欢（或不喜欢）某个电子产品的原因，并用 because / although / so 等连接。",
   "sample":[
    "Why I Like Reading on a Tablet",
    "I like reading on a tablet because it is very convenient.",
    "Although the tablet is small, it can hold many books. Because I can carry it anywhere, I read at any time.",
    "However, I also know its problem. If I spend too long on it, my eyes may hurt. So I take a rest every hour.",
    "I think the tablet is a good helper, though I must use it wisely. Therefore, I enjoy my reading time."],
   "requirements":"1. 词数约80词；2. 用 because/although/so 造句；3. 语句通顺；4. 可适当发挥。",
   "绑定":"G60/G61"}}

# ─────────────────────────── L25 内容 ───────────────────────────
L25 = {
 "reading_a": {"id":"DXH2026_L25_reading_a","genre":"说明文/应用文","difficulty":"中","word_count":194,
   "绑定":"G62 动名词 / G63 不定式 / 爱好主题",
   "paragraphs":[
    "My Hobbies and Future Plans",
    "Everyone has hobbies, and hobbies can become our plans.",
    "I enjoy reading books very much. Reading makes me happy and helps me learn new things. I also like drawing. Drawing is relaxing, and I love doing it on weekends.",
    "Because of my hobbies, I plan to become a writer in the future. I want to write stories that make people smile. I hope to finish my first book one day.",
    "To make my dream come true, I need to practice every day. I decide to read more and write a little each week. I agree that hard work is important.",
    "My parents encourage me to keep going. They think doing what I love is the best way to grow."],
   "questions":[
    {"num":1,"q":"What does the writer enjoy doing?","opts":[["A","Reading and drawing."],["B","Playing games."],["C","Watching TV."]],"answer":"A"},
    {"num":2,"q":"What does the writer want to become?","opts":[["A","A writer."],["B","A doctor."],["C","A teacher."]],"answer":"A"},
    {"num":3,"q":"What does the writer decide to do every week?","opts":[["A","Write a little."],["B","Sleep more."],["C","Eat more."]],"answer":"A"}]},
 "reading_b": {"id":"DXH2026_L25_reading_b","genre":"记叙文","difficulty":"中","word_count":215,
   "绑定":"G62/G63 动名词不定式 / 承诺主题",
   "paragraphs":[
    "A Promise to My Friend",
    "Last term I made a promise to my friend Jack. I promised to help him improve his speaking.",
    "Jack wanted to speak English well, but he was afraid to speak in front of others. He refused to open his mouth in class.",
    "So I suggested practicing together every morning. We agreed to meet in the park and talk in English. At first, Jack found it hard to continue.",
    "However, we did not give up. We managed to practice for a month. I remember saying, \"Keep going, and you will succeed.\"",
    "After one term, Jack could speak English confidently. He no longer minds talking in public. He thanks me a lot, and I feel proud. We learn that keeping a promise is very important."],
   "questions":[
    {"num":1,"q":"What did the writer promise to help Jack do?","opts":[["A","Improve his speaking."],["B","Improve his writing."],["C","Improve his cooking."]],"answer":"A"},
    {"num":2,"q":"Why was Jack afraid to speak?","opts":[["A","He was afraid to speak in front of others."],["B","He did not like English."],["C","He was too busy."]],"answer":"A"},
    {"num":3,"q":"How did they practice?","opts":[["A","They met in the park and talked in English."],["B","They wrote letters every day."],["C","They watched movies."]],"answer":"A"},
    {"num":4,"q":"What did they learn at last?","opts":[["A","Keeping a promise is very important."],["B","Speaking is not useful."],["C","Giving up is easy."]],"answer":"A"}]},
 "reading_c": {"id":"DXH2026_L25_reading_c","genre":"说明文","difficulty":"中","word_count":215,
   "绑定":"G62 动名词 / G63 不定式 / 运动主题",
   "paragraphs":[
    "Why I Love Doing Sports",
    "I love doing sports. To me, sports are not only fun but also good for health.",
    "Playing basketball is my favorite. When I play it, I feel strong and happy. Swimming is also great, because it keeps my body healthy. I enjoy running in the morning before school.",
    "Doing sports has many advantages. It helps me relax after a long day of study. It also teaches me to work with others. I like playing with my teammates, and we learn to help each other.",
    "To get better, I need to practice regularly. I want to join the school team, so I train hard every day. My coach encourages me to keep trying.",
    "In a word, doing sports makes my life colorful. I hope everyone can find a sport they love."],
   "questions":[
    {"num":1,"q":"What is the writer's favorite sport?","opts":[["A","Playing basketball."],["B","Swimming."],["C","Running."]],"answer":"A"},
    {"num":2,"q":"Why does the writer like sports?","opts":[["A","Because they are fun and good for health."],["B","Because they are expensive."],["C","Because they are easy."]],"answer":"A"},
    {"num":3,"q":"What does doing sports teach the writer?","opts":[["A","To work with others."],["B","To give up easily."],["C","To stay at home."]],"answer":"A"},
    {"num":4,"q":"What is the passage mainly about?","opts":[["A","Why the writer loves doing sports."],["B","How to play basketball."],["C","Why swimming is hard."]],"answer":"A"}]},
 "w5": {"id":"DXH2026_L25_w5","title":"根据短文内容，从方框中选出最佳句子填入文中空白处（有一项多余）",
   "绑定":"G62/G63 动名词不定式",
   "paragraphs":[
    "Planning for the Future",
    "I often think about my future. I want to do something I love.",
    "First, I enjoy helping others. ___1___ Helping people makes me happy.",
    "Second, I plan to learn new skills. ___2___ Learning English and computer science is useful.",
    "To achieve my dream, I decide to work hard now. ___3___ I will not give up easily.",
    "Finally, I hope to have a healthy life. ___4___ Doing sports and eating well keep me strong."],
   "candidates":[["A","So I want to be a doctor or a teacher."],["B","I hope my dream can come true."],["C","These skills will help me in the future."],["D","I will make a clear plan for each year."],["E","I dislike learning anything new."]],
   "answers":{"1":"A","2":"C","3":"D","4":"B"}},
 "cloze": {"id":"DXH2026_L25_cloze","title":"完形填空",
   "绑定":"G62 动名词 / G63 不定式",
   "paragraphs":[
    "I enjoy ___1___ English very much. It is fun to learn new words.",
    "My teacher suggests ___2___ every day. ___3___ decided to practice speaking this term.",
    "I want ___4___ more about the world. Reading ___5___ me a lot.",
    "I agreed ___6___ my friend to study together. We plan ___7___ English movies on weekends.",
    "Although it is hard, I refuse ___8___ up. I hope ___9___ good English one day.",
    "Remember ___10___ your mistakes, and you will improve."],
   "items":[
    {"num":1,"opts":[["A","learn"],["B","learning"],["C","to learn"]],"answer":"B"},
    {"num":2,"opts":[["A","practice"],["B","practicing"],["C","to practice"]],"answer":"B"},
    {"num":3,"opts":[["A","I"],["B","having"],["C","to"]],"answer":"A"},
    {"num":4,"opts":[["A","know"],["B","knowing"],["C","to know"]],"answer":"C"},
    {"num":5,"opts":[["A","help"],["B","helps"],["C","helping"]],"answer":"B"},
    {"num":6,"opts":[["A","with"],["B","to"],["C","for"]],"answer":"A"},
    {"num":7,"opts":[["A","watch"],["B","watching"],["C","to watch"]],"answer":"C"},
    {"num":8,"opts":[["A","give"],["B","giving"],["C","to give"]],"answer":"C"},
    {"num":9,"opts":[["A","speak"],["B","speaking"],["C","to speak"]],"answer":"C"},
    {"num":10,"opts":[["A","correct"],["B","correcting"],["C","to correct"]],"answer":"C"}]},
 "grammar_fill": {"id":"DXH2026_L25_grammar_fill","title":"从方框内选择适当的词并用其正确形式填空（每空限填一词）",
   "绑定":"G62/G63",
   "word_bank":["enjoy","finish","decide","hope","agree","refuse","manage","offer","want","practice","extra","extra"],
   "paragraphs":[
    "I ___1___ reading books before going to bed.",
    "Please ___2___ your homework before dinner.",
    "She ___3___ to study abroad next year.",
    "We ___4___ to see you again soon.",
    "He ___5___ to help me with the heavy box.",
    "The boy ___6___ to follow his parents' advice.",
    "She ___7___ to finish the work on time.",
    "Tom ___8___ to clean the classroom after school.",
    "I ___9___ to be a singer in the future.",
    "You should ___10___ speaking English every day."],
   "answers":["enjoy","finish","decided","hope","agreed","refused","managed","offered","want","practice"]},
 "sa": {"id":"DXH2026_L25_sa","title":"阅读表达",
   "passage_title":"My Dream",
   "绑定":"G62/G63",
   "paragraphs":[
    "My dream is to become a musician. I enjoy playing the guitar and singing.",
    "I plan to practice for an hour every day so that I can improve. My parents want me to keep my dream.",
    "I hope to join a music club at school. I decide to take part in the school concert next term.",
    "To make my dream come true, I need to work hard and never give up."],
   "questions":[
    {"num":1,"q":"What is the writer's dream?","answer":"To become a musician.","type":"简答"},
    {"num":2,"q":"What does the writer enjoy doing?","answer":"Playing the guitar and singing.","type":"简答"},
    {"num":3,"q":"How long does the writer plan to practice every day?","answer":"For an hour.","type":"简答"},
    {"num":4,"q":"请翻译画线句（I need to work hard and never give up.）","answer":"我需要努力工作并且永不放弃。","type":"翻译"},
    {"num":5,"q":"What does the writer plan to do every day?","answer":"Practice for an hour.","type":"简答"}]},
 "writing": {"id":"DXH2026_L25_writing","title":"书面表达",
   "prompt":"假如你是李华，请写一篇80词左右的短文，介绍你的一个爱好和你未来的计划，用 enjoy/finish/want/hope 等动词。",
   "sample":[
    "My Hobby and My Plan",
    "I enjoy doing sports, especially playing football. Playing football makes me strong and happy.",
    "I practice playing football every week. My friends and I plan to win the school match this year.",
    "In the future, I want to be a football player. I hope to play in a big team one day.",
    "To achieve my dream, I need to keep practicing and never give up. I believe I can make it."],
   "requirements":"1. 词数约80词；2. 用动名词/不定式表达；3. 语句通顺；4. 可适当发挥。",
   "绑定":"G62/G63"}}

# ─────────────────────────── L21 测试卷内容 ───────────────────────────
# 蓝图 4.1：阅读40 / 语言20 / 综合30 / 语法诊断10；G01-G54 全覆盖
L21 = {
 "reading_a": {"id":"DXH2026_L21_reading_a","genre":"应用文","difficulty":"中","word_count":161,
   "绑定":"G08数词/G14What/G16现在时/G35how much how many",
   "paragraphs":[
    "Your Study Progress Guide",
    "Welcome to your study progress guide. This guide helps you review and improve your schoolwork.",
    "First, check your grades. Your score shows how well you understand each subject. If your score is low, do not worry.",
    "Second, make a plan. Write down your goals for this month. Review your notes every day and prepare for the next test.",
    "Third, practice your skills. Answer the questions in the workbook and check your marks. Correct your mistakes and remember them.",
    "Finally, be confident. Doubt is normal, but courage and practice bring progress. You can always improve with effort."],
   "questions":[
    {"num":1,"q":"What does the guide help you do?","opts":[["A","Review and improve your schoolwork."],["B","Play more games."],["C","Sleep more."]],"answer":"A"},
    {"num":2,"q":"What should you do if your score is low?","opts":[["A","Do not worry and make a plan."],["B","Give up."],["C","Forget about it."]],"answer":"A"},
    {"num":3,"q":"How often should you review your notes?","opts":[["A","Every day."],["B","Once a year."],["C","Never."]],"answer":"A"},
    {"num":4,"q":"What should you do with your mistakes?","opts":[["A","Correct and remember them."],["B","Hide them."],["C","Ignore them."]],"answer":"A"},
    {"num":5,"q":"What is the main idea of the guide?","opts":[["A","How to study with plan and practice."],["B","How to play sports."],["C","How to spend money."]],"answer":"A"}]},
 "reading_b": {"id":"DXH2026_L21_reading_b","genre":"记叙文","difficulty":"中","word_count":183,
   "绑定":"G19/G20过去时/G38why because/G52过去时综合",
   "paragraphs":[
    "A Better Grade",
    "Last term I got a poor score in math. I felt sad and thought I was not good at it.",
    "My teacher saw my mistake and gave me some advice. She said, \"You can improve if you practice every day.\"",
    "So I made a plan. Every evening I reviewed my notes and did more exercises. When I made an error, I wrote it down and corrected it.",
    "Before the next test, I prepared carefully. I remembered the key points and asked questions when I had doubt.",
    "At last, I got a much better grade. I was proud of myself. I learned that practice and courage make progress."],
   "questions":[
    {"num":1,"q":"Why did the writer feel sad?","opts":[["A","Because he got a poor score in math."],["B","Because he lost his book."],["C","Because it rained."]],"answer":"A"},
    {"num":2,"q":"What did the teacher advise?","opts":[["A","Practice every day."],["B","Stop studying."],["C","Play more."]],"answer":"A"},
    {"num":3,"q":"What did the writer do when he made an error?","opts":[["A","Wrote it down and corrected it."],["B","Hid it from others."],["C","Cried."]],"answer":"A"},
    {"num":4,"q":"What does the underlined word \"error\" mean?","opts":[["A","错误"],["B","分数"],["C","计划"]],"answer":"A"},
    {"num":5,"q":"What do practice and courage bring?","opts":[["A","Progress."],["B","Doubt."],["C","Tiredness."]],"answer":"A"}]},
 "reading_c": {"id":"DXH2026_L21_reading_c","genre":"说明文/科普","difficulty":"中","word_count":183,
   "绑定":"G13祈使句/G43频度副词/G55/G56比较级",
   "paragraphs":[
    "How to Make Progress",
    "Progress does not come easily. You need the right skills and a good plan.",
    "First, follow a study routine. Review your lessons every day, and you will remember them better. Practice more, and your skills will grow.",
    "Second, believe in yourself. Everyone has doubt sometimes, but confidence helps you go on. Never give up when things are hard.",
    "Third, set a clear goal. If you want to improve, compare yourself with yourself. You will find that today you are better than before.",
    "In short, progress comes from practice, confidence, and goals. Work hard, and success will follow."],
   "questions":[
    {"num":1,"q":"What is the first step to make progress?","opts":[["A","Follow a study routine."],["B","Sleep more."],["C","Watch TV."]],"answer":"A"},
    {"num":2,"q":"What should you do when you have doubt?","opts":[["A","Believe in yourself."],["B","Give up."],["C","Forget it."]],"answer":"A"},
    {"num":3,"q":"Who should you compare yourself with?","opts":[["A","Yourself."],["B","The tallest student."],["C","A teacher."]],"answer":"A"},
    {"num":4,"q":"What are the three keys to progress?","opts":[["A","Practice, confidence, and goals."],["B","Money, food, and sleep."],["C","Games, fun, and rest."]],"answer":"A"},
    {"num":5,"q":"What is the passage mainly about?","opts":[["A","How to make progress."],["B","How to play games."],["C","How to cook."]],"answer":"A"}]},
 "w5": {"id":"DXH2026_L21_w5","title":"根据短文内容，从方框中选出最佳句子填入文中空白处（有一项多余）",
   "绑定":"G18 want to do / G28 情态动词 / G34 would like / G46 进行时",
   "paragraphs":[
    "My Revision Plan",
    "The final exam is coming, so I made a revision plan.",
    "First, I review my notes every evening. ___1___ I want to remember all the key points.",
    "Second, I practice the exercises again. ___2___ I also correct my mistakes in a notebook.",
    "Third, I prepare for each subject. ___3___ I would like to do well in every test.",
    "On the weekend, I am reviewing the whole book. ___4___ I hope my plan can help me succeed."],
   "candidates":[["A","I am practicing the hard questions now."],["B","I will take a short rest after studying."],["C","I write down the important words."],["D","I can ask my teacher if I have doubt."],["E","I am reading them carefully."]],
   "answers":{"1":"E","2":"A","3":"D","4":"B"}},
 "cloze": {"id":"DXH2026_L21_cloze","title":"完形填空",
   "绑定":"G01-G54 滚动",
   "paragraphs":[
    "I want ___1___ a good student. I ___2___ my study very much.",
    "Every day I ___3___ my lessons and do my homework. My teacher is ___4___ and patient.",
    "Yesterday I ___5___ a math test. I felt a little nervous before it.",
    "___6___ I prepared well, I did not worry too much. I answered the questions ___7___.",
    "After the test, I checked my ___8___. I found I made a few mistakes.",
    "I will ___9___ these errors and try to do better next time. ___10___ I am confident in myself."],
   "items":[
    {"num":1,"opts":[["A","be"],["B","to be"],["C","being"]],"answer":"B"},
    {"num":2,"opts":[["A","enjoy"],["B","enjoys"],["C","enjoying"]],"answer":"A"},
    {"num":3,"opts":[["A","review"],["B","reviewed"],["C","reviewing"]],"answer":"A"},
    {"num":4,"opts":[["A","kind"],["B","kinder"],["C","kindest"]],"answer":"A"},
    {"num":5,"opts":[["A","take"],["B","took"],["C","takes"]],"answer":"B"},
    {"num":6,"opts":[["A","Because"],["B","So"],["C","But"]],"answer":"A"},
    {"num":7,"opts":[["A","careful"],["B","carefully"],["C","care"]],"answer":"B"},
    {"num":8,"opts":[["A","marks"],["B","mark"],["C","marking"]],"answer":"A"},
    {"num":9,"opts":[["A","correct"],["B","corrected"],["C","correcting"]],"answer":"A"},
    {"num":10,"opts":[["A","However"],["B","Therefore"],["C","Although"]],"answer":"B"}]},
 "grammar_fill": {"id":"DXH2026_L21_grammar_fill","title":"从方框内选择适当的词并用其正确形式填空（每空限填一词）",
   "绑定":"G01-G54 滚动",
   "word_bank":["grade","score","improve","review","prepare","practice","progress","result","subject","skill","extra","extra"],
   "paragraphs":[
    "She got a good ___1___ in the English test.",
    "My ___2___ in the competition was very high.",
    "Reading can ___3___ your vocabulary.",
    "I ___4___ my notes before the exam.",
    "We ___5___ for the final test last week.",
    "___6___ makes perfect.",
    "He made great ___7___ in math this term.",
    "The ___8___ of the test was excellent.",
    "Science is my favorite ___9___.",
    "Speaking is an important ___10___."],
   "answers":["grade","score","improve","review","prepared","Practice","progress","result","subject","skill"]},
 "sa": {"id":"DXH2026_L21_sa","title":"阅读表达",
   "passage_title":"An Experience of Improvement",
   "绑定":"G01-G54 滚动",
   "paragraphs":[
    "Last year I was weak in English. I wanted to improve, so I made a plan.",
    "Every morning I read English aloud for twenty minutes. In the evening I reviewed the new words and practiced speaking.",
    "When I made a mistake, I wrote it down and corrected it. I also asked my teacher for advice.",
    "After a few months, my English improved a lot. I became more confident and got better results. I learned that hard work brings progress."],
   "questions":[
    {"num":1,"q":"When did the writer read English aloud?","answer":"Every morning for twenty minutes.","type":"简答"},
    {"num":2,"q":"What did the writer do when he made a mistake?","answer":"He wrote it down and corrected it.","type":"简答"},
    {"num":3,"q":"Who did the writer ask for advice?","answer":"His teacher.","type":"简答"},
    {"num":4,"q":"请翻译画线句（I learned that hard work brings progress.）","answer":"我懂得了努力学习带来进步。","type":"翻译"},
    {"num":5,"q":"How long did the writer read English aloud every morning?","answer":"For twenty minutes.","type":"简答"}]},
 "writing": {"id":"DXH2026_L21_writing","title":"书面表达",
   "prompt":"假如你是李华，请写一篇100词左右的短文，写一次你提升某科成绩的经历（如数学、英语等）。内容包括做了什么、遇到什么困难、收获是什么。",
   "sample":[
    "My English Progress",
    "Last term my English was not good. I often got low scores, and I felt a little sad.",
    "So I made a plan. I decided to practice every day. Every morning I read English aloud, and every evening I reviewed the new words. When I made mistakes, I asked my teacher for advice and corrected them.",
    "At first it was hard, but I did not give up. I kept studying and practicing. Before the final exam, I prepared carefully and was confident.",
    "Finally, I got a much better grade. My teacher praised me. I learned that courage and practice bring progress, and I am proud of myself."],
   "requirements":"1. 词数约100词；2. 用一般过去时写经历；3. 语句通顺，语法正确；4. 可适当发挥。",
   "绑定":"过去时/学习经历"}}

# 语法诊断（L21: G01-G54 全覆盖，10 题；L22-25: 20 题 mc5+fill5）
L21["grammar_diag"] = {
 "id":"DXH2026_L21_grammar_diag","title":"语法诊断（G01-G54 全覆盖）",
 "mc":[
  {"num":1,"q":"This is ____ book. ____ is mine.","opts":[["A","my; That"],["B","mine; That"],["C","my; This"]],"answer":"A","绑定":"G01-G04"},
  {"num":2,"q":"There ____ many people in the park yesterday.","opts":[["A","were"],["B","was"],["C","are"]],"answer":"A","绑定":"G03/G05/G52"},
  {"num":3,"q":"____ you like swimming? — Yes, I do.","opts":[["A","Do"],["B","Does"],["C","Is"]],"answer":"A","绑定":"G09/G19"},
  {"num":4,"q":"I have two ____. They are very interesting.","opts":[["A","books"],["B","book"],["C","bookes"]],"answer":"A","绑定":"G10/G29"},
  {"num":5,"q":"She is ____ than her sister.","opts":[["A","taller"],["B","tall"],["C","tallest"]],"answer":"A","绑定":"G55"},
  {"num":6,"q":"____ careful! The floor is wet.","opts":[["A","Be"],["B","Do"],["C","Are"]],"answer":"A","绑定":"G13"},
  {"num":7,"q":"We ____ a movie now.","opts":[["A","are watching"],["B","watch"],["C","watched"]],"answer":"A","绑定":"G46"},
  {"num":8,"q":"I don't have ____ money.","opts":[["A","any"],["B","some"],["C","a"]],"answer":"A","绑定":"G31/G33"},
  {"num":9,"q":"How ____ is the coat? — 100 yuan.","opts":[["A","much"],["B","many"],["C","often"]],"answer":"A","绑定":"G34/G35"},
  {"num":10,"q":"Everyone ____ happy at the party yesterday.","opts":[["A","was"],["B","were"],["C","are"]],"answer":"A","绑定":"G49/G50/G51"}]}

# L22-25 语法诊断（20 分：mc5 + fill5）
def _diag(lesson, gram, mc, fill):
    return {"id":"DXH2026_L%d_grammar_diag"%lesson,"title":"语法诊断","mc":mc,"fill":fill}

L22["grammar_diag"] = _diag(22,"G55/G56/G57",
 [{"num":1,"q":"Tom is ____ than Jack.","opts":[["A","taller"],["B","tall"],["C","tallest"]],"answer":"A","绑定":"G55"},
  {"num":2,"q":"This is ____ book in the library.","opts":[["A","the most interesting"],["B","more interesting"],["C","interesting"]],"answer":"A","绑定":"G56"},
  {"num":3,"q":"She is ____ as her mother.","opts":[["A","as tall"],["B","taller"],["C","the tallest"]],"answer":"A","绑定":"G57"},
  {"num":4,"q":"He is not ____ as me.","opts":[["A","so smart"],["B","smarter"],["C","the smartest"]],"answer":"A","绑定":"G57"},
  {"num":5,"q":"Beijing is one of ____ cities in China.","opts":[["A","the biggest"],["B","bigger"],["C","big"]],"answer":"A","绑定":"G56"}],
 [{"num":1,"q":"This computer is ____ (cheap) than that one.","answer":"cheaper","绑定":"G55"},
  {"num":2,"q":"She runs ____ (fast) in our class.","answer":"the fastest","绑定":"G56"},
  {"num":3,"q":"My bag is ____ (heavy) than yours.","answer":"heavier","绑定":"G55"},
  {"num":4,"q":"He is ____ (hard-working) than before.","answer":"more hard-working","绑定":"G55"},
  {"num":5,"q":"This is ____ (good) movie I have seen.","answer":"the best","绑定":"G56"}])

L23["grammar_diag"] = _diag(23,"G58/G59/G13",
 [{"num":1,"q":"If it ____ tomorrow, we will stay home.","opts":[["A","rains"],["B","will rain"],["C","rained"]],"answer":"A","绑定":"G58"},
  {"num":2,"q":"You will fail ____ you work hard.","opts":[["A","unless"],["B","if"],["C","so"]],"answer":"A","绑定":"G59"},
  {"num":3,"q":"Work hard, ____ you will succeed.","opts":[["A","and"],["B","or"],["C","but"]],"answer":"A","绑定":"G13"},
  {"num":4,"q":"____ you hurry, you will be late.","opts":[["A","Unless"],["B","If"],["C","Because"]],"answer":"A","绑定":"G59"},
  {"num":5,"q":"If you ____ tired, take a rest.","opts":[["A","are"],["B","will be"],["C","were"]],"answer":"A","绑定":"G58"}],
 [{"num":1,"q":"If he ____ (come), we will start.","answer":"comes","绑定":"G58"},
  {"num":2,"q":"You can't pass ____ (unless) you study.","answer":"unless","绑定":"G59"},
  {"num":3,"q":"Hurry up, ____ you will miss the bus.","answer":"or","绑定":"G13"},
  {"num":4,"q":"If you ____ (want) to succeed, try hard.","answer":"want","绑定":"G58"},
  {"num":5,"q":"Be careful, ____ you will make mistakes.","answer":"or","绑定":"G13"}])

L24["grammar_diag"] = _diag(24,"G60/G61",
 [{"num":1,"q":"____ it rained, we went out.","opts":[["A","Although"],["B","So"],["C","Because"]],"answer":"A","绑定":"G60"},
  {"num":2,"q":"I stayed home ____ it was cold.","opts":[["A","because"],["B","but"],["C","or"]],"answer":"A","绑定":"G60"},
  {"num":3,"q":"He studied hard ____ he could pass.","opts":[["A","so that"],["B","because"],["C","although"]],"answer":"A","绑定":"G61"},
  {"num":4,"q":"I was tired, ____ I went to bed early.","opts":[["A","so"],["B","because"],["C","although"]],"answer":"A","绑定":"G61"},
  {"num":5,"q":"____ he is young, he knows a lot.","opts":[["A","Though"],["B","So"],["C","Unless"]],"answer":"A","绑定":"G60"}],
 [{"num":1,"q":"I like English ____ (因为) it is interesting.","answer":"because","绑定":"G60"},
  {"num":2,"q":"____ (虽然) it was late, we kept working.","answer":"Although","绑定":"G60"},
  {"num":3,"q":"She got up early so ____ she could catch the bus.","answer":"that","绑定":"G61"},
  {"num":4,"q":"It was difficult; ____ (然而), I did it.","answer":"however","绑定":"G60"},
  {"num":5,"q":"He was hungry, ____ he ate a sandwich.","answer":"so","绑定":"G61"}])

L25["grammar_diag"] = _diag(25,"G62/G63",
 [{"num":1,"q":"I enjoy ____ books.","opts":[["A","reading"],["B","to read"],["C","read"]],"answer":"A","绑定":"G62"},
  {"num":2,"q":"She wants ____ English well.","opts":[["A","to learn"],["B","learning"],["C","learn"]],"answer":"A","绑定":"G63"},
  {"num":3,"q":"He stopped ____ and had a rest.","opts":[["A","to work"],["B","working"],["C","work"]],"answer":"A","绑定":"G63"},
  {"num":4,"q":"Remember ____ the door when you leave.","opts":[["A","to lock"],["B","locking"],["C","lock"]],"answer":"A","绑定":"G63"},
  {"num":5,"q":"____ is good for our health.","opts":[["A","Swimming"],["B","Swim"],["C","To swimming"]],"answer":"A","绑定":"G62"}],
 [{"num":1,"q":"I finished ____ (write) the letter.","answer":"writing","绑定":"G62"},
  {"num":2,"q":"They decided ____ (go) by train.","answer":"to go","绑定":"G63"},
  {"num":3,"q":"He agreed ____ (help) me.","answer":"to help","绑定":"G63"},
  {"num":4,"q":"Avoid ____ (make) the same mistake.","answer":"making","绑定":"G62"},
  {"num":5,"q":"I hope ____ (see) you again.","answer":"to see","绑定":"G63"}])

LESSONS = {21:L21, 22:L22, 23:L23, 24:L24, 25:L25}

# 结构：test 卷（L21）与授课课（L22-25）渲染参数
def render_paper(lesson, content, test=False):
    card = {"lesson":lesson,"student":"邓兴华","tier":"中等","stage":("Stage 5" if test else "Stage 6"),
            "type":("测试卷" if test else "授课课练习"),"theme":"","listening":False}
    doc = bpp.Document()
    for s in doc.sections:
        s.top_margin=bpp.Cm(1.5); s.bottom_margin=bpp.Cm(1.5)
        s.left_margin=bpp.Cm(1.5); s.right_margin=bpp.Cm(1.5)
    _heading(doc, "第 %02d 课时%s" % (lesson, "测试卷" if test else "配套练习"))
    _para(doc, "学生：邓兴华    层级：中等    结构对齐 2026 湖南中考（不含听力）    满分：100 分",
          align=bpp.WD_ALIGN_PARAGRAPH.CENTER, size=10.5)
    _para(doc, "姓名：____________    得分：____________    用时：____________",
          align=bpp.WD_ALIGN_PARAGRAPH.CENTER, size=10.5)
    qnum = 1
    ans1_rd, ans1_w5 = [], []
    ans2_cl, ans2_gf = [], []
    ans3_sa, ans3_wr = [], []
    ans4 = []

    # 第一部分 阅读理解
    if test:
        rd_score, rd_sub = 30, "第一节（共 15 小题，每小题 2 分）"
        w5_score, w5_sub = 10, "第二节（共 5 小题，每小题 2 分，有一项多余）"
    else:
        rd_score, rd_sub = 22, "第一节（共 11 小题，每小题 2 分）"
        w5_score, w5_sub = 8, "第二节（共 4 小题，每小题 2 分，有一项多余）"
    _section(doc, "第一部分　阅读理解（共两节，满分 %d 分）" % (rd_score+w5_score))
    _sub(doc, rd_sub)
    for tag in ("a","b","c"):
        pg = content["reading_%s"%tag]
        _sub(doc, "Passage %s（%s · %d 词）" % (tag.upper(), pg.get("genre",""), pg.get("word_count","")))
        _passage(doc, pg["paragraphs"])
        for q in pg["questions"]:
            _question(doc, qnum, q["q"]); _options3(doc, q["opts"])
            ans1_rd.append((qnum, q["answer"])); qnum += 1
    _sub(doc, w5_sub)
    w = content["w5"]
    _passage(doc, _renumber(w["paragraphs"], qnum))
    _para(doc, "方框：", size=10.5, bold=True, space_after=1)
    for letter, s in w["candidates"]:
        _para(doc, "%s. %s" % (letter, s), size=10.5, left_indent=bpp.OPT, space_after=1)
    for k, v in sorted(w["answers"].items(), key=lambda x:int(x[0])):
        g = qnum + int(k) - 1
        ans1_w5.append((g, v))
    qnum += len(w["answers"])

    # 第二部分 语言运用
    if test:
        cl_score, cl_per, cl_sub = 10, 1, "第一节　完形填空（共 10 小题，每小题 1 分）"
        gf_score, gf_per, gf_sub = 10, 1, "第二节　选词填空（共 10 小题，每小题 1 分）"
    else:
        cl_score, cl_per, cl_sub = 15, 1.5, "第一节　完形填空（共 10 小题，每小题 1.5 分）"
        gf_score, gf_per, gf_sub = 10, 1, "第二节　选词填空（共 10 小题，每小题 1 分）"
    _section(doc, "第二部分　语言运用（共两节，满分 %d 分）" % (cl_score+gf_score))
    _sub(doc, cl_sub)
    c = content["cloze"]
    _passage(doc, _renumber(c["paragraphs"], qnum))
    for it in c["items"]:
        g = qnum + it["num"] - 1
        _options3(doc, it["opts"], num=g)
        ans2_cl.append((g, it["answer"]))
    qnum += len(c["items"])
    _sub(doc, gf_sub)
    wb = content["grammar_fill"]
    words = wb["word_bank"]; half=(len(words)+1)//2
    for i in range(0, len(words), half):
        _para(doc, "  ".join(words[i:i+half]), size=10.5, bold=True, space_after=1)
    _passage(doc, _renumber(wb["paragraphs"], qnum))
    for i, a in enumerate(wb["answers"]):
        ans2_gf.append((qnum+i, a))
    qnum += len(wb["answers"])

    # 第三部分 综合技能
    if test:
        sa_sub, sa_per, wr_score = "第一节　阅读表达（共 5 小题，每小题 1 分）", 1, 25
    else:
        sa_sub, sa_per, wr_score = "第一节　阅读表达（共 5 小题，每小题 2 分）", 2, 15
    _section(doc, "第三部分　综合技能（共两节，满分 %d 分）" % (sa_per*len(content["sa"]["questions"])+wr_score))
    _sub(doc, sa_sub)
    sa = content["sa"]
    _passage(doc, sa["paragraphs"])
    for i, q in enumerate(sa["questions"]):
        n = qnum + i
        _question(doc, n, q["q"])
        _para(doc, "    ____________________________________________________", size=10.5)
        ans3_sa.append((n, q["answer"]))
    qnum += len(sa["questions"])
    _sub(doc, "第二节　书面表达（满分 %d 分）" % wr_score)
    wr = content["writing"]
    _para(doc, "%d. %s" % (qnum, wr["prompt"]), size=10.5, left_indent=bpp.QI, space_after=2)
    _para(doc, wr["requirements"], size=10.5, left_indent=bpp.QI, space_after=4)
    for _ in range(6):
        _para(doc, "    ________________________________________________________", size=10.5, space_after=2)
    ans3_wr.append((qnum, "见参考答案范文"))
    qnum += 1

    # 第四部分 语法诊断
    gd = content["grammar_diag"]
    if test:
        di_sub = "语法诊断（共 %d 小题，每小题 1 分，G01-G54 覆盖）" % (len(gd["mc"])+len(gd.get("fill",[])))
        di_score = len(gd["mc"])+len(gd.get("fill",[]))
    else:
        di_sub = "语法诊断（共 10 小题，每小题 2 分）"
        di_score = len(gd["mc"])*2+len(gd.get("fill",[]))*2
    _section(doc, "第四部分　语法诊断（满分 %d 分）" % di_score)
    _sub(doc, di_sub)
    _sub(doc, "（一）单项选择")
    for q in gd["mc"]:
        _question(doc, qnum, q["q"]); _options3(doc, q["opts"])
        ans4.append((qnum, q["answer"])); qnum += 1
    if gd.get("fill"):
        _sub(doc, "（二）根据句意填空")
        for q in gd["fill"]:
            _question(doc, qnum, q["q"])
            ans4.append((qnum, q["answer"])); qnum += 1

    # 参考答案
    doc.add_page_break()
    _section(doc, "参考答案")
    _sub(doc, "第一部分　阅读理解")
    for ln in _ans_runs(ans1_rd): _para(doc, ln, size=10.5, space_after=1)
    for ln in _ans_runs(ans1_w5): _para(doc, ln, size=10.5, space_after=1)
    _sub(doc, "第二部分　语言运用")
    _sub(doc, "第一节　完形填空")
    for ln in _ans_runs(ans2_cl): _para(doc, ln, size=10.5, space_after=1)
    _sub(doc, "第二节　选词填空")
    for n, a in ans2_gf: _para(doc, "%d. %s" % (n, a), size=10.5, space_after=1)
    _sub(doc, "第三部分　综合技能")
    _sub(doc, "第一节　阅读表达")
    for n, a in ans3_sa: _para(doc, "%d. %s" % (n, a), size=10.5, space_after=1)
    _sub(doc, "第二节　书面表达")
    _passage(doc, wr["sample"])
    _sub(doc, "第四部分　语法诊断")
    for n, a in ans4: _para(doc, "%d. %s" % (n, a), size=10.5, space_after=1)

    path = os.path.join(ROOT, "第%02d课时" % lesson, "第%02d课时_配套练习_中等.docx" % lesson)
    doc.save(path)
    return path, qnum-1

if __name__ == "__main__":
    for lesson in (22,23,24,25):
        p, total = render_paper(lesson, LESSONS[lesson], test=False)
        print("L%d 练习生成：%s（%d 题, %d bytes）" % (lesson, p, total, os.path.getsize(p)))
    p, total = render_paper(21, LESSONS[21], test=True)
    print("L21 测试卷生成：%s（%d 题, %d bytes）" % (p, total, os.path.getsize(p)))
    print("全部生成完成")