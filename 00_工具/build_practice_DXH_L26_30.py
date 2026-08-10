# -*- coding: utf-8 -*-
"""邓兴华 L26-L30 配套练习批量生成（真实题目版 · exam_spec v2026.3）
- L26-30 = 授课课配套练习（阅读30/语言25/综合25/语法诊断20，不含听力）
- L26 三时态（G16一般现在/G43频度副词/G46现在进行）
- L27 现在完成时首次（G64 基本结构+标志词）
- L28 现在完成时进阶（G64 since/for+been三态）
- L29 被动语态首次（G65 be+过去分词）
- L30 被动语态进阶（G65 情态被动+主动表被动）
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

# ─────────────────────────── L26 内容（三时态：一般现在/现在进行/一般过去） ───────────────────────────
L26 = {
 "reading_a": {"id":"DXH2026_L26_reading_a","genre":"应用文/记叙","difficulty":"中","word_count":194,
   "绑定":"G16一般现在 / G46现在进行 / 学校生活",
   "paragraphs":[
    "My Busy School Day",
    "I get up at six thirty every day. I usually have eggs and milk for breakfast. Then I go to school by bus. My first class begins at eight o'clock.",
    "I often have English and math in the morning. Miss Li teaches English very well. Now I am listening to her carefully. She is explaining the new words to us.",
    "We have a short rest at noon. I sometimes play basketball with my friends in the playground. In the afternoon, I have a music lesson. I am learning to play the piano now.",
    "After school, I go home and do my homework. I usually finish it before dinner. Yesterday I watched a funny movie with my parents. We enjoyed it very much.",
    "I am busy every day, but I am happy. I like my busy school life."],
   "questions":[
    {"num":1,"q":"What time does the writer get up every day?","opts":[["A","At six thirty."],["B","At eight o'clock."],["C","At noon."]],"answer":"A"},
    {"num":2,"q":"What is Miss Li doing now?","opts":[["A","Explaining new words."],["B","Playing the piano."],["C","Having breakfast."]],"answer":"A"},
    {"num":3,"q":"What did the writer do yesterday?","opts":[["A","Watched a movie."],["B","Played basketball."],["C","Went to town."]],"answer":"A"}]},
 "reading_b": {"id":"DXH2026_L26_reading_b","genre":"记叙文","difficulty":"中","word_count":215,
   "绑定":"G43频度副词 / G46现在进行 / 一天生活",
   "paragraphs":[
    "A Day in My Life",
    "Every morning, I get up early and make my bed. I always wash my face and brush my teeth after I get up.",
    "My mother cooks breakfast for us. Right now, she is cooking rice in the kitchen. I can smell it from my room. It smells so good.",
    "I usually walk to school with my best friend. On the way, we often talk about our lessons. Sometimes we even sing songs together.",
    "At school, I rarely feel bored. I like all my subjects. My teacher is always kind to us. This week, we are learning about space.",
    "I never stay up late. I go to bed at ten o'clock. I sometimes read a book before I sleep.",
    "Every day is the same for me, but I never feel tired of it. I think my life is full of fun."],
   "questions":[
    {"num":1,"q":"What is the writer's mother doing now?","opts":[["A","Cooking rice."],["B","Washing clothes."],["C","Reading a book."]],"answer":"A"},
    {"num":2,"q":"How does the writer go to school?","opts":[["A","By bus."],["B","On foot."],["C","By bike."]],"answer":"A"},
    {"num":3,"q":"What are they learning this week?","opts":[["A","About space."],["B","About animals."],["C","About food."]],"answer":"A"},
    {"num":4,"q":"What does the underlined word \"rarely\" mean?","opts":[["A","很少"],["B","经常"],["C","总是"]],"answer":"A"}]},
 "reading_c": {"id":"DXH2026_L26_reading_c","genre":"说明文","difficulty":"中","word_count":215,
   "绑定":"G16/G43/G46 时态与频度副词",
   "paragraphs":[
    "Routines Make Us Healthy",
    "Having good routines is important for our health. People who keep good habits usually feel happy and strong.",
    "We often get up at the same time every day. We always eat three meals on time. We sometimes exercise in the morning. These small habits help our bodies stay well.",
    "Now smart students are learning to manage their time. They are making plans for study and play. They are using their time wisely every day.",
    "Yesterday I started a new routine. I got up early and ran for half an hour. I felt great after the run. I am going to keep doing it.",
    "Good routines are not hard to build. We just need to do small things again and again. Remember, a healthy body comes from good habits."],
   "questions":[
    {"num":1,"q":"Why are good routines important?","opts":[["A","They help us stay healthy."],["B","They make us tired."],["C","They waste time."]],"answer":"A"},
    {"num":2,"q":"What are smart students doing now?","opts":[["A","Making plans for study and play."],["B","Sleeping all day."],["C","Eating too much."]],"answer":"A"},
    {"num":3,"q":"What did the writer do yesterday?","opts":[["A","Ran for half an hour."],["B","Played games."],["C","Watched TV."]],"answer":"A"},
    {"num":4,"q":"What is the main idea of the passage?","opts":[["A","Good routines help us be healthy."],["B","Routines are boring."],["C","We should sleep more."]],"answer":"A"}]},
 "w5": {"id":"DXH2026_L26_w5","title":"根据短文内容，从方框中选出最佳句子填入文中空白处（有一项多余）",
   "绑定":"G16/G43/G46 时态与频度",
   "paragraphs":[
    "My Daily Habits",
    "Hello! I want to tell you about my daily habits.",
    "I usually get up at six and have breakfast. ___1___ I always brush my teeth after breakfast.",
    "I often walk to school. ___2___ On the way, I sometimes sing songs.",
    "Right now, I am writing a letter to my friend. ___3___ She is my best friend.",
    "Yesterday I cleaned my room. ___4___ I will keep my room clean every day."],
   "candidates":[["A","She is writing back to me now."],["B","I like talking to her on the way."],["C","I am telling her about my school."],["D","I like to keep my teeth clean."],["E","I am very proud of my work."]],
   "answers":{"1":"D","2":"B","3":"C","4":"E"}},
 "cloze": {"id":"DXH2026_L26_cloze","title":"完形填空",
   "绑定":"G16/G43/G46",
   "paragraphs":[
    "My friend Tom ___1___ up early every day. He ___2___ always happy in the morning.",
    "He ___3___ breakfast at seven o'clock. He usually ___4___ some milk and bread.",
    "Right now, Tom ___5___ his homework. He ___6___ carefully at his book.",
    "Yesterday he ___7___ a kite in the park. He ___8___ very happy that day.",
    "Tom ___9___ games after school. He never ___10___ time."],
   "items":[
    {"num":1,"opts":[["A","gets"],["B","get"],["C","got"]],"answer":"A"},
    {"num":2,"opts":[["A","is"],["B","are"],["C","was"]],"answer":"A"},
    {"num":3,"opts":[["A","has"],["B","have"],["C","had"]],"answer":"A"},
    {"num":4,"opts":[["A","eats"],["B","eat"],["C","ate"]],"answer":"A"},
    {"num":5,"opts":[["A","is doing"],["B","do"],["C","does"]],"answer":"A"},
    {"num":6,"opts":[["A","is looking"],["B","look"],["C","looks"]],"answer":"A"},
    {"num":7,"opts":[["A","flew"],["B","flies"],["C","fly"]],"answer":"A"},
    {"num":8,"opts":[["A","was"],["B","is"],["C","are"]],"answer":"A"},
    {"num":9,"opts":[["A","plays"],["B","play"],["C","played"]],"answer":"A"},
    {"num":10,"opts":[["A","wastes"],["B","waste"],["C","wasted"]],"answer":"A"}]},
 "grammar_fill": {"id":"DXH2026_L26_grammar_fill","title":"从方框内选择适当的词并用其正确形式填空（每空限填一词）",
   "绑定":"G16/G43/G46",
   "word_bank":["always","usually","often","sometimes","never","get","have","look","play","watch","extra","extra"],
   "paragraphs":[
    "I ___1___ drink milk in the morning because it is good for me.",
    "He ___2___ up at seven o'clock every day.",
    "We ___3___ breakfast together at home.",
    "She ___4___ at the blackboard in class now.",
    "They ___5___ football after school on Friday.",
    "___6___ , I go to the library on weekends.",
    "My father ___7___ TV after dinner in the evening.",
    "I ___8___ eat too much candy before bed.",
    "Tom ___9___ to school by bus every day.",
    "We ___10___ our favorite show last night."],
   "answers":["usually","gets","have","is looking","play","Sometimes","watches","never","goes","watched"]},
 "sa": {"id":"DXH2026_L26_sa","title":"阅读表达",
   "passage_title":"My Weekend",
   "绑定":"G16/G43/G46",
   "paragraphs":[
    "I usually have a busy but happy weekend. On Saturday morning, I get up at eight and do my homework.",
    "In the afternoon, I often play basketball with my friends. Right now, they are playing in the park.",
    "On Sunday, I sometimes visit my grandparents. My grandmother cooks delicious food for us.",
    "Yesterday I helped my mother clean the garden. We were both very happy."],
   "questions":[
    {"num":1,"q":"What does the writer do on Saturday morning?","answer":"He does his homework.","type":"简答"},
    {"num":2,"q":"What are the writer's friends doing now?","answer":"They are playing in the park.","type":"简答"},
    {"num":3,"q":"Who cooks delicious food for the family?","answer":"The writer's grandmother.","type":"简答"},
    {"num":4,"q":"请把文中画线句子翻译成汉语（Yesterday I helped my mother clean the garden.）","answer":"昨天我帮妈妈打扫了花园。","type":"翻译"},
    {"num":5,"q":"Was the writer happy yesterday? How do you know?","answer":"Yes. He says 'We were both very happy.'","type":"简答"}]},
 "writing": {"id":"DXH2026_L26_writing","title":"书面表达",
   "prompt":"假如你是李华，请用英语写一篇80词左右的短文，介绍你一天的学习和生活（可用一般现在时、现在进行时或一般过去时），并说明你最喜欢的活动。",
   "sample":[
    "My School Day",
    "I am Li Hua. I am a student of Grade Eight. I get up at six thirty every day.",
    "I usually have breakfast and go to school by bus. My favorite subject is English. Right now, I am learning English with my classmates.",
    "Yesterday I played basketball with my friends after school. We had a great time. I like playing basketball because it makes me strong.",
    "I am busy every day, but I am very happy."],
   "requirements":"1. 词数约80词；2. 用一般现在时/现在进行时/一般过去时；3. 语句通顺，语法正确；4. 可适当发挥。",
   "绑定":"三时态/频度副词"}}

# ─────────────────────────── L27 内容（现在完成时首次：have/has+过去分词+标志词） ───────────────────────────
L27 = {
 "reading_a": {"id":"DXH2026_L27_reading_a","genre":"记叙文/书信","difficulty":"中","word_count":194,
   "绑定":"G64现在完成时 / 交换生",
   "paragraphs":[
    "My Experience as an Exchange Student",
    "Dear Mom, I have just arrived in London. The trip was long, but I am now safe here.",
    "I have already seen the famous Big Ben. I have also visited the London Eye. I have taken many photos for you.",
    "I haven't eaten English food yet. My host family has cooked some noodles for me. I have felt very welcome here.",
    "I have ever dreamed of studying abroad. Now my dream has come true. I have learned many new words this week.",
    "I have made some new friends before, but these friends are the kindest. I hope you can come and visit me one day."],
   "questions":[
    {"num":1,"q":"Where has the writer just arrived?","opts":[["A","In London."],["B","In Paris."],["C","In Beijing."]],"answer":"A"},
    {"num":2,"q":"What has the writer already seen?","opts":[["A","Big Ben."],["B","The Eiffel Tower."],["C","The Great Wall."]],"answer":"A"},
    {"num":3,"q":"Has the writer eaten English food yet?","opts":[["A","No, not yet."],["B","Yes, already."],["C","We don't know."]],"answer":"A"}]},
 "reading_b": {"id":"DXH2026_L27_reading_b","genre":"记叙文","difficulty":"中","word_count":215,
   "绑定":"G64现在完成时标志词 already/yet/just/ever/before/once",
   "paragraphs":[
    "A Letter about My Exchange Life",
    "Dear Dad, I have just finished my first week here. I have already got used to the new school.",
    "In the morning, we have English classes. I have never spoken so much English before. I have already made three good friends here.",
    "My host family has been very kind. They have cooked local food for me. I have eaten fish and chips once. It was delicious.",
    "I haven't visited the museum yet, but I plan to go there next week. I have ever wanted to see the old paintings. Now I can.",
    "I have had a wonderful time so far. I have learned about the British culture before from books, but now I see it with my own eyes.",
    "I miss you all, but I am happy here. I will write to you again soon. Love, Tom"],
   "questions":[
    {"num":1,"q":"What has the writer just finished?","opts":[["A","His first week here."],["B","His homework."],["C","A big test."]],"answer":"A"},
    {"num":2,"q":"How many friends has the writer made?","opts":[["A","Three."],["B","Five."],["C","None."]],"answer":"A"},
    {"num":3,"q":"What has the writer eaten once?","opts":[["A","Fish and chips."],["B","Rice and noodles."],["C","Bread and milk."]],"answer":"A"},
    {"num":4,"q":"What does the underlined word \"local\" mean?","opts":[["A","当地的"],["B","国外的"],["C","昂贵的"]],"answer":"A"}]},
 "reading_c": {"id":"DXH2026_L27_reading_c","genre":"说明文","difficulty":"中","word_count":215,
   "绑定":"G64现在完成时 / 交换学习的意义",
   "paragraphs":[
    "The Value of Studying Abroad",
    "Studying abroad has become popular in recent years. Many students have chosen to study in foreign countries.",
    "I have ever talked with an exchange student. He has been to the USA twice. He has learned a lot about the American culture.",
    "He has already improved his English. Before that, he had trouble speaking. Now he can talk with foreigners easily.",
    "He has also made friends from different countries. He has visited many famous places. He has taken lots of photos.",
    "But studying abroad is not always easy. He has sometimes felt homesick. He has missed his family and friends.",
    "All in all, studying abroad has given him a new view of the world. I think it has been a valuable experience."],
   "questions":[
    {"num":1,"q":"How many times has the exchange student been to the USA?","opts":[["A","Twice."],["B","Once."],["C","Three times."]],"answer":"A"},
    {"num":2,"q":"What has the exchange student already improved?","opts":[["A","His English."],["B","His cooking."],["C","His driving."]],"answer":"A"},
    {"num":3,"q":"What has he has sometimes felt?","opts":[["A","Homesick."],["B","Hungry."],["C","Tired of travel."]],"answer":"A"},
    {"num":4,"q":"What is the main idea of the passage?","opts":[["A","Studying abroad is a valuable experience."],["B","Studying abroad is easy."],["C","We should never leave home."]],"answer":"A"}]},
 "w5": {"id":"DXH2026_L27_w5","title":"根据短文内容，从方框中选出最佳句子填入文中空白处（有一项多余）",
   "绑定":"G64现在完成时标志词",
   "paragraphs":[
    "My Trip to Beijing",
    "I have just come back from Beijing.",
    "I have already visited the Great Wall. ___1___ It is very long and amazing.",
    "I have also seen the Forbidden City. ___2___ I have taken many photos there.",
    "I haven't been to the Summer Palace yet. ___3___ I plan to go there next time.",
    "Beijing is a wonderful city. ___4___ I hope to visit it again one day."],
   "candidates":[["A","I have heard of its long history."],["B","I have had a great time there."],["C","I have never seen such a wall."],["D","I have walked on it for hours."],["E","I have ever been to the museum."]],
   "answers":{"1":"D","2":"A","3":"C","4":"B"}},
 "cloze": {"id":"DXH2026_L27_cloze","title":"完形填空",
   "绑定":"G64现在完成时",
   "paragraphs":[
    "I ___1___ just finished my homework. I am very happy now.",
    "My sister ___2___ already gone to school. She ___3___ left ten minutes ago.",
    "___4___ you ever been to the museum? Yes, I have. I ___5___ there once.",
    "He hasn't told me the news ___6___ . I want to know it.",
    "I have ___7___ seen such a beautiful park. It is really nice.",
    "They have ___8___ the report before. They know it well.",
    "We ___9___ known each other for a long time. We are good friends.",
    "She has ___10___ her keys. She can't find them anywhere."],
   "items":[
    {"num":1,"opts":[["A","have"],["B","has"],["C","had"]],"answer":"A"},
    {"num":2,"opts":[["A","have"],["B","has"],["C","is"]],"answer":"B"},
    {"num":3,"opts":[["A","has"],["B","have"],["C","is"]],"answer":"A"},
    {"num":4,"opts":[["A","Have"],["B","Has"],["C","Do"]],"answer":"A"},
    {"num":5,"opts":[["A","have been"],["B","has been"],["C","am"]],"answer":"A"},
    {"num":6,"opts":[["A","yet"],["B","already"],["C","ever"]],"answer":"A"},
    {"num":7,"opts":[["A","never"],["B","before"],["C","yet"]],"answer":"A"},
    {"num":8,"opts":[["A","read"],["B","reads"],["C","reading"]],"answer":"A"},
    {"num":9,"opts":[["A","have"],["B","has"],["C","are"]],"answer":"A"},
    {"num":10,"opts":[["A","lost"],["B","lose"],["C","losing"]],"answer":"A"}]},
 "grammar_fill": {"id":"DXH2026_L27_grammar_fill","title":"从方框内选择适当的词并用其正确形式填空（每空限填一词）",
   "绑定":"G64现在完成时",
   "word_bank":["already","yet","just","ever","before","once","finish","visit","see","go","extra","extra"],
   "paragraphs":[
    "I have ___1___ finished my breakfast.",
    "He hasn't cleaned his room ___2___.",
    "She has ___3___ arrived at school.",
    "___4___ you ever tried this food?",
    "I have been to the park ___5___ this year.",
    "We have ___6___ eaten dinner.",
    "They have ___7___ their homework already.",
    "I have ___8___ the museum twice.",
    "Have you ___9___ this movie before?",
    "She has ___10___ to Shanghai twice."],
   "answers":["just","yet","already","Have","once","already","finished","visited","seen","gone"]},
 "sa": {"id":"DXH2026_L27_sa","title":"阅读表达",
   "passage_title":"My Exchange Experience",
   "绑定":"G64现在完成时",
   "paragraphs":[
    "I have just returned from my exchange trip. I have been to Australia for a month.",
    "I have already visited the Sydney Opera House. It is very famous and beautiful.",
    "I haven't tried the local food yet, but I have seen many restaurants.",
    "I have made some good friends during my stay. They have taught me a lot about their culture."],
   "questions":[
    {"num":1,"q":"How long has the writer been to Australia?","answer":"For a month.","type":"简答"},
    {"num":2,"q":"What has the writer already visited?","answer":"The Sydney Opera House.","type":"简答"},
    {"num":3,"q":"Has the writer tried the local food yet?","answer":"No, not yet.","type":"简答"},
    {"num":4,"q":"请把文中画线句子翻译成汉语（I have already visited the Sydney Opera House.）","answer":"我已经参观了悉尼歌剧院。","type":"翻译"},
    {"num":5,"q":"What have the friends taught the writer?","answer":"They have taught him a lot about their culture.","type":"简答"}]},
 "writing": {"id":"DXH2026_L27_writing","title":"书面表达",
   "prompt":"假如你是李华，你刚参加了一次交换生活动。请用英语写一篇80词左右的短文，介绍你这次经历中已经做过的事情（可用现在完成时），并表达你的感受。",
   "sample":[
    "My Exchange Experience",
    "I have just finished my exchange trip. I have been to a foreign country for two weeks.",
    "I have already visited many famous places. I have also made some new friends there.",
    "I haven't tried all the local food yet, but I have enjoyed most of it. I have learned many new words.",
    "I have had a wonderful time. I think this experience has helped me a lot. I will never forget it."],
   "requirements":"1. 词数约80词；2. 用现在完成时描述经历；3. 语句通顺，语法正确；4. 可适当发挥。",
   "绑定":"现在完成时"}}

# ─────────────────────────── L28 内容（现在完成时进阶：since/for + been三态） ───────────────────────────
L28 = {
 "reading_a": {"id":"DXH2026_L28_reading_a","genre":"说明文/记叙","difficulty":"中","word_count":194,
   "绑定":"G64进阶 since/for / 家乡变化",
   "paragraphs":[
    "The Changes in My Hometown",
    "My hometown has changed a lot in recent years. I have lived here since I was born.",
    "The streets have become wider since 2010. Tall buildings have been built in the city. Many new shops have opened for years.",
    "The environment has improved. We have planted more trees since last year. The river has been cleaner for a long time.",
    "Transportation has developed greatly. I have used the new subway since it opened. It has made the travel much easier.",
    "I am proud of my hometown. It has grown into a modern city."],
   "questions":[
    {"num":1,"q":"How long has the writer lived in his hometown?","opts":[["A","Since he was born."],["B","For two years."],["C","Since last month."]],"answer":"A"},
    {"num":2,"q":"When have tall buildings been built?","opts":[["A","Since 2010."],["B","Last year."],["C","Yesterday."]],"answer":"A"},
    {"num":3,"q":"Since when have they planted more trees?","opts":[["A","Since last year."],["B","Since 2010."],["C","For a long time."]],"answer":"A"}]},
 "reading_b": {"id":"DXH2026_L28_reading_b","genre":"记叙文","difficulty":"中","word_count":215,
   "绑定":"G64 since+时间点/for+时间段 / 家乡变化",
   "paragraphs":[
    "A New Look of My Hometown",
    "My hometown is not what it used to be. It has changed a lot since I was a child.",
    "The old houses have been replaced by tall buildings. I have lived in the new area since 2018. The streets have been clean for years.",
    "The park has become a popular place. I have walked there every morning for a long time. Green trees have been planted all around.",
    "The school has improved a lot. I have studied here since last year. The teachers have been very helpful for my study.",
    "People's life has become better. They have eaten healthier food since the new market opened. They have enjoyed the good life for a long time.",
    "I love my hometown. I believe it will become even better in the future."],
   "questions":[
    {"num":1,"q":"How long has the writer lived in the new area?","opts":[["A","Since 2018."],["B","For many years."],["C","Since last week."]],"answer":"A"},
    {"num":2,"q":"How long have the streets been clean?","opts":[["A","For years."],["B","Since today."],["C","Not long."]],"answer":"A"},
    {"num":3,"q":"How long has the writer studied at the school?","opts":[["A","Since last year."],["B","Since 2018."],["C","Since he was a child."]],"answer":"A"},
    {"num":4,"q":"What does the underlined word \"replaced\" mean?","opts":[["A","被取代"],["B","被隐藏"],["C","被忘记"]],"answer":"A"}]},
 "reading_c": {"id":"DXH2026_L28_reading_c","genre":"说明文","difficulty":"中","word_count":215,
   "绑定":"G64 中考考法（vs 一般过去时）",
   "paragraphs":[
    "How to Use the Present Perfect Tense",
    "The present perfect tense is very useful in English. We use it to talk about things that happened in the past but are still true now.",
    "We use it with since and for. We use since with a point of time, like since Monday. We use for with a period of time, like for two days.",
    "We also use have been to and have gone to. Have been to means someone went and came back. Have gone to means someone went and is not here now.",
    "For example, I have been to Beijing twice. But my brother has gone to Beijing. He is still there now.",
    "We can use the present perfect with ever, never, already, yet, just, before and once. We cannot use it with a past time like yesterday.",
    "Remember, if there is a past time, we use the simple past tense. The two tenses are different, and we must choose carefully."],
   "questions":[
    {"num":1,"q":"What do we use since with?","opts":[["A","A point of time."],["B","A period of time."],["C","A past action."]],"answer":"A"},
    {"num":2,"q":"What does have been to mean?","opts":[["A","Went and came back."],["B","Went and is not here."],["C","Is going now."]],"answer":"A"},
    {"num":3,"q":"Which word do we NOT use with the present perfect?","opts":[["A","Yesterday."],["B","Already."],["C","Just."]],"answer":"A"},
    {"num":4,"q":"What is the main idea of the passage?","opts":[["A","How to use the present perfect tense."],["B","How to write a letter."],["C","How to travel."]],"answer":"A"}]},
 "w5": {"id":"DXH2026_L28_w5","title":"根据短文内容，从方框中选出最佳句子填入文中空白处（有一项多余）",
   "绑定":"G64 since/for + been三态",
   "paragraphs":[
    "My Best Friend",
    "I have known my best friend for six years.",
    "We have studied together since primary school. ___1___ We help each other a lot.",
    "He has been to Beijing many times. ___2___ He has brought back many gifts for me.",
    "I haven't been to Beijing yet. ___3___ I plan to go there with him next year.",
    "Our friendship has lasted for a long time. ___4___ I am glad to have him as my friend."],
   "candidates":[["A","He has visited many famous places."],["B","I have learned a lot from him."],["C","He has gone to Shanghai."],["D","I have never been there before."],["E","We have shared many happy memories."]],
   "answers":{"1":"B","2":"A","3":"D","4":"E"}},
 "cloze": {"id":"DXH2026_L28_cloze","title":"完形填空",
   "绑定":"G64 since/for + been三态",
   "paragraphs":[
    "I have worked here ___1___ 2019. I have lived in this city for ___2___ years.",
    "My friend has ___3___ to Beijing. He is still there now.",
    "I have ___4___ to Shanghai three times. I like it very much.",
    "We have studied English ___5___ last year. We have learned many words.",
    "She has stayed here ___6___ three days. She will leave tomorrow.",
    "The city ___7___ changed a lot since 2010.",
    "___8___ you ever been to the museum? Yes, I have.",
    "He has not come here ___9___ . We are waiting for him.",
    "I have known him ___10___ a long time."],
   "items":[
    {"num":1,"opts":[["A","since"],["B","for"],["C","in"]],"answer":"A"},
    {"num":2,"opts":[["A","two"],["B","since"],["C","in"]],"answer":"A"},
    {"num":3,"opts":[["A","gone"],["B","been"],["C","go"]],"answer":"A"},
    {"num":4,"opts":[["A","been"],["B","gone"],["C","go"]],"answer":"A"},
    {"num":5,"opts":[["A","since"],["B","for"],["C","in"]],"answer":"A"},
    {"num":6,"opts":[["A","for"],["B","since"],["C","in"]],"answer":"A"},
    {"num":7,"opts":[["A","has"],["B","have"],["C","is"]],"answer":"A"},
    {"num":8,"opts":[["A","Have"],["B","Has"],["C","Do"]],"answer":"A"},
    {"num":9,"opts":[["A","yet"],["B","already"],["C","ever"]],"answer":"A"},
    {"num":10,"opts":[["A","for"],["B","since"],["C","in"]],"answer":"A"}]},
 "grammar_fill": {"id":"DXH2026_L28_grammar_fill","title":"从方框内选择适当的词并用其正确形式填空（每空限填一词）",
   "绑定":"G64 since/for + been三态",
   "word_bank":["since","for","been","gone","change","know","live","work","visit","build","extra","extra"],
   "paragraphs":[
    "I have lived here ___1___ 2015.",
    "He has stayed with us ___2___ two weeks.",
    "Have you ever ___3___ to the Great Wall?",
    "My father has ___4___ to Shanghai. He is there now.",
    "The city has ___5___ a lot since 2010.",
    "I have ___6___ him for many years.",
    "She has ___7___ in Beijing since 2018.",
    "They have ___8___ here for five years.",
    "New buildings have been ___9___ in the city.",
    "I have ___10___ the museum twice this year."],
   "answers":["since","for","been","gone","changed","known","lived","worked","built","visited"]},
 "sa": {"id":"DXH2026_L28_sa","title":"阅读表达",
   "passage_title":"My Hometown",
   "绑定":"G64 since/for",
   "paragraphs":[
    "My hometown has changed a lot since I was a child.",
    "The roads have become wider since 2015. Many new buildings have been built for years.",
    "I have lived here since I was born. I have seen many changes.",
    "The park has been my favorite place for a long time. I have walked there every morning."],
   "questions":[
    {"num":1,"q":"When did the roads become wider?","answer":"Since 2015.","type":"简答"},
    {"num":2,"q":"How long has the writer lived in his hometown?","answer":"Since he was born.","type":"简答"},
    {"num":3,"q":"What is the writer's favorite place?","answer":"The park.","type":"简答"},
    {"num":4,"q":"请把文中画线句子翻译成汉语（My hometown has changed a lot since I was a child.）","answer":"自从我小时候起，我的家乡已经改变了很多。","type":"翻译"},
    {"num":5,"q":"How long has the park been the writer's favorite place?","answer":"For a long time.","type":"简答"}]},
 "writing": {"id":"DXH2026_L28_writing","title":"书面表达",
   "prompt":"假如你是李华，请用英语写一篇80词左右的短文，介绍你的家乡近年来的变化（可用现在完成时与 since/for），并表达你对家乡的感受。",
   "sample":[
    "Changes in My Hometown",
    "My hometown has changed a lot in recent years.",
    "The environment has improved since last year. Many trees have been planted. The river has been clean for a long time.",
    "Transportation has become better. I have used the new subway since it opened. It has made my travel easier.",
    "I have lived here since I was born. I love my hometown. I think it will become more beautiful in the future."],
   "requirements":"1. 词数约80词；2. 用现在完成时与 since/for；3. 语句通顺，语法正确；4. 可适当发挥。",
   "绑定":"现在完成时进阶"}}

# ─────────────────────────── L29 内容（被动语态首次：be+过去分词） ───────────────────────────
L29 = {
 "reading_a": {"id":"DXH2026_L29_reading_a","genre":"说明文","difficulty":"中","word_count":194,
   "绑定":"G65被动 be+过去分词 / 茶文化",
   "paragraphs":[
    "How Is Tea Made?",
    "Do you know how tea is made? Tea is grown in many parts of China. It is picked by farmers in the spring.",
    "First, the fresh leaves are collected from the trees. Then the leaves are dried in the sun. After that, they are processed in a factory.",
    "The tea leaves are packed into boxes. They are sent to many cities. The tea is drunk by people all over the world.",
    "Tea is made in different ways in different places. Some tea is made by machine, and some is made by hand. Hand-made tea is often more expensive.",
    "Tea is a very popular drink in China. It is served to guests at home. I hope you can enjoy it too."],
   "questions":[
    {"num":1,"q":"Where is tea grown?","opts":[["A","In many parts of China."],["B","Only in the north."],["C","In the desert."]],"answer":"A"},
    {"num":2,"q":"Who pick the tea leaves?","opts":[["A","Farmers."],["B","Workers."],["C","Students."]],"answer":"A"},
    {"num":3,"q":"How is hand-made tea often?","opts":[["A","More expensive."],["B","Cheaper."],["C","The same."]],"answer":"A"}]},
 "reading_b": {"id":"DXH2026_L29_reading_b","genre":"说明文","difficulty":"中","word_count":215,
   "绑定":"G65被动 / 制作过程",
   "paragraphs":[
    "How Is Chocolate Made?",
    "Chocolate is loved by people all over the world. But do you know how it is made?",
    "Chocolate is made from cocoa beans. The beans are grown on cocoa trees in hot countries. They are picked when they are ripe.",
    "First, the beans are dried in the sun. Then they are roasted in a big machine. After that, the beans are crushed into a thick paste.",
    "The paste is mixed with sugar and milk. The mixture is heated and stirred. Finally, it is shaped into bars and cooled.",
    "The chocolate bars are wrapped in colorful paper. They are sent to shops and supermarkets. They are sold to hungry customers.",
    "Making chocolate is a long process. But the result is very sweet. Now you know how your favorite treat is made."],
   "questions":[
    {"num":1,"q":"What is chocolate made from?","opts":[["A","Cocoa beans."],["B","Wheat."],["C","Rice."]],"answer":"A"},
    {"num":2,"q":"Where are the beans grown?","opts":[["A","On cocoa trees in hot countries."],["B","In the cold north."],["C","In the sea."]],"answer":"A"},
    {"num":3,"q":"What is the paste mixed with?","opts":[["A","Sugar and milk."],["B","Salt and oil."],["C","Water and flour."]],"answer":"A"},
    {"num":4,"q":"What does the underlined word \"ripe\" mean?","opts":[["A","成熟的"],["B","绿色的"],["C","苦的"]],"answer":"A"}]},
 "reading_c": {"id":"DXH2026_L29_reading_c","genre":"说明文","difficulty":"中","word_count":215,
   "绑定":"G65被动 / 主动改被动三步",
   "paragraphs":[
    "How Things Are Made",
    "Many things around us are made by machines or by hand. Let me tell you how some of them are made.",
    "Paper is made from wood. The wood is cut into small pieces. Then the pieces are boiled and made into pulp. The pulp is pressed into sheets and dried.",
    "Glass is made from sand. The sand is heated at a very high temperature. Then it is blown or shaped into bottles. The bottles are used for many things.",
    "To change an active sentence into a passive one, we follow three steps. First, the object is moved to the front. Second, the verb is changed to be plus the past participle. Third, we add the word by.",
    "For example, Farmers grow tea. The object tea is moved first. The verb is changed to is grown. Finally we say, Tea is grown by farmers.",
    "Now you know how things are made and how we make passive sentences."],
   "questions":[
    {"num":1,"q":"What is paper made from?","opts":[["A","Wood."],["B","Sand."],["C","Glass."]],"answer":"A"},
    {"num":2,"q":"What is glass made from?","opts":[["A","Sand."],["B","Wood."],["C","Paper."]],"answer":"A"},
    {"num":3,"q":"How many steps do we follow to make a passive sentence?","opts":[["A","Three."],["B","Two."],["C","Five."]],"answer":"A"},
    {"num":4,"q":"What is the main idea of the passage?","opts":[["A","How things are made and how passives are formed."],["B","How to cook."],["C","How to travel."]],"answer":"A"}]},
 "w5": {"id":"DXH2026_L29_w5","title":"根据短文内容，从方框中选出最佳句子填入文中空白处（有一项多余）",
   "绑定":"G65被动语态",
   "paragraphs":[
    "How Bread Is Made",
    "Bread is a popular food all over the world.",
    "First, the flour is mixed with water. ___1___ Then the dough is kneaded.",
    "The dough is left to rise for some time. ___2___ It becomes bigger and softer.",
    "Then the dough is shaped into loaves. ___3___ They are put into the oven.",
    "Finally, the bread is baked and taken out. ___4___ It smells and tastes so good."],
   "candidates":[["A","It is left to rise for an hour."],["B","The loaves are placed in a hot oven."],["C","The dough is made from flour and water."],["D","The bread is served at breakfast."],["E","It is cut into pieces before being served."]],
   "answers":{"1":"C","2":"A","3":"B","4":"D"}},
 "cloze": {"id":"DXH2026_L29_cloze","title":"完形填空",
   "绑定":"G65被动语态",
   "paragraphs":[
    "Tea ___1___ grown in many parts of China.",
    "The leaves ___2___ picked by farmers in spring.",
    "The tea ___3___ packed into boxes every day.",
    "These books ___4___ written by a famous writer.",
    "The window ___5___ broken by the boy yesterday.",
    "The room ___6___ cleaned by Lucy every morning.",
    "This song ___7___ sung by many students.",
    "The bridge ___8___ built in 2010.",
    "The flowers ___9___ watered by my mother.",
    "The work ___10___ finished by the workers now."],
   "items":[
    {"num":1,"opts":[["A","is"],["B","are"],["C","was"]],"answer":"A"},
    {"num":2,"opts":[["A","are"],["B","is"],["C","were"]],"answer":"A"},
    {"num":3,"opts":[["A","is"],["B","are"],["C","was"]],"answer":"A"},
    {"num":4,"opts":[["A","were"],["B","are"],["C","is"]],"answer":"A"},
    {"num":5,"opts":[["A","was"],["B","is"],["C","are"]],"answer":"A"},
    {"num":6,"opts":[["A","is"],["B","are"],["C","was"]],"answer":"A"},
    {"num":7,"opts":[["A","is"],["B","are"],["C","were"]],"answer":"A"},
    {"num":8,"opts":[["A","was"],["B","is"],["C","are"]],"answer":"A"},
    {"num":9,"opts":[["A","is"],["B","are"],["C","were"]],"answer":"A"},
    {"num":10,"opts":[["A","is"],["B","are"],["C","was"]],"answer":"A"}]},
 "grammar_fill": {"id":"DXH2026_L29_grammar_fill","title":"从方框内选择适当的词并用其正确形式填空（每空限填一词）",
   "绑定":"G65被动语态",
   "word_bank":["make","grow","build","write","break","clean","sing","water","pick","paint","extra","extra"],
   "paragraphs":[
    "Tea is ___1___ in China.",
    "The house was ___2___ in 2010.",
    "This book was ___3___ by a famous writer.",
    "The window was ___4___ by the boy.",
    "The floor is ___5___ every morning.",
    "The song is ___6___ by many students.",
    "The flowers are ___7___ by my mother.",
    "The leaves are ___8___ in spring.",
    "The chair was ___9___ by the worker.",
    "The cake is ___10___ by my grandmother."],
   "answers":["grown","built","written","broken","cleaned","sung","watered","picked","painted","made"]},
 "sa": {"id":"DXH2026_L29_sa","title":"阅读表达",
   "passage_title":"How Kites Are Made",
   "绑定":"G65被动语态",
   "paragraphs":[
    "Kites are loved by children all over the world. Do you know how kites are made?",
    "First, thin pieces of wood are cut into a frame. Then the frame is covered with paper.",
    "The paper is painted with beautiful colors. A long string is tied to the kite.",
    "Finally, the kite is tested in the open air. It is flown high in the sky."],
   "questions":[
    {"num":1,"q":"What is the frame covered with?","answer":"It is covered with paper.","type":"简答"},
    {"num":2,"q":"What is painted on the paper?","answer":"Beautiful colors.","type":"简答"},
    {"num":3,"q":"What is tied to the kite?","answer":"A long string.","type":"简答"},
    {"num":4,"q":"请把文中画线句子翻译成汉语（Kites are loved by children all over the world.）","answer":"风筝被全世界的孩子们喜爱。","type":"翻译"},
    {"num":5,"q":"Where is the kite tested?","answer":"In the open air.","type":"简答"}]},
 "writing": {"id":"DXH2026_L29_writing","title":"书面表达",
   "prompt":"假如你是李华，请用英语写一篇80词左右的短文，介绍一样东西（如茶、风筝、面包等）是如何被制作出来的（用被动语态），并说明它的用途。",
   "sample":[
    "How Kites Are Made",
    "Kites are very popular in China. They are loved by many people.",
    "Kites are made by hand. First, thin wood is cut into a light frame. Then the frame is covered with paper. The paper is painted with bright colors.",
    "A long string is tied to the kite. Finally, the kite is flown in the open air. It is a great way to enjoy the sky.",
    "I think making a kite is interesting and fun."],
   "requirements":"1. 词数约80词；2. 用被动语态描述制作过程；3. 语句通顺，语法正确；4. 可适当发挥。",
   "绑定":"被动语态"}}

# ─────────────────────────── L30 内容（被动进阶：情态被动+主动表被动） ───────────────────────────
L30 = {
 "reading_a": {"id":"DXH2026_L30_reading_a","genre":"应用文/说明","difficulty":"中","word_count":194,
   "绑定":"G65进阶 情态被动 / 校规",
   "paragraphs":[
    "Rules in Our School",
    "Every school has its own rules. Following them makes our school a safe and happy place.",
    "Students must be on time for class. Noise should be avoided in the library. Mobile phones are not allowed in class.",
    "Homework must be finished on time. Smoking is forbidden on the campus. Parking is prohibited near the gate.",
    "School uniforms are required every day. Photos are permitted in the art room. Students are expected to be polite to others.",
    "These rules are made to protect us. They are respected by everyone. I think good rules help us grow well."],
   "questions":[
    {"num":1,"q":"What must students be for class?","opts":[["A","On time."],["B","Late."],["C","Quiet."]],"answer":"A"},
    {"num":2,"q":"Are mobile phones allowed in class?","opts":[["A","No, they aren't."],["B","Yes, they are."],["C","We don't know."]],"answer":"A"},
    {"num":3,"q":"Where is smoking forbidden?","opts":[["A","On the campus."],["B","In the art room."],["C","At the gate only."]],"answer":"A"}]},
 "reading_b": {"id":"DXH2026_L30_reading_b","genre":"说明文","difficulty":"中","word_count":215,
   "绑定":"G65进阶 主动表被动 / 物品使用",
   "paragraphs":[
    "How Things Are Used",
    "Many things in our daily life are used in different ways. Let me introduce some of them.",
    "This tool can be used to cut wood. The scissors are used for cutting paper. These books are read by many students.",
    "The new machine sells well in the market. This story reads well and is loved by children. The cloth washes easily and stays clean.",
    "Water is used for drinking and cooking. The chairs are used by older people. The rules should be followed by everyone.",
    "The products are supplied to many cities. They are expected to be of good quality. Things can be used in many different ways.",
    "We should use things wisely. In this way, we can make our life better and better."],
   "questions":[
    {"num":1,"q":"What can this tool be used to do?","opts":[["A","Cut wood."],["B","Cook food."],["C","Draw pictures."]],"answer":"A"},
    {"num":2,"q":"How does the new machine sell?","opts":[["A","Well."],["B","Badly."],["C","Slowly."]],"answer":"A"},
    {"num":3,"q":"What does 'sells well' mean here?","opts":[["A","卖得好"],["B","被卖得好"],["C","正在卖"]],"answer":"A"},
    {"num":4,"q":"What are the products expected to be?","opts":[["A","Of good quality."],["B","Very cheap."],["C","Very big."]],"answer":"A"}]},
 "reading_c": {"id":"DXH2026_L30_reading_c","genre":"应用文","difficulty":"中","word_count":215,
   "绑定":"G65进阶 被动识别 / 通知",
   "paragraphs":[
    "A School Notice",
    "Notice to all students. Please read the following rules carefully.",
    "The library will be closed on Friday. Books must be returned before the end of the week. The laboratory is not allowed to be used without a teacher.",
    "The new sports equipment has been installed. All students are expected to join the sports meeting next month.",
    "Rules are advised to be followed carefully. The school is known for its good tradition. It is said that a new museum will be built next year.",
    "The notice is written to keep everyone informed. Please be on time for all activities. Thank you for your attention.",
    "Remember, a good school is built by all of us. Let us follow the rules together."],
   "questions":[
    {"num":1,"q":"When will the library be closed?","opts":[["A","On Friday."],["B","On Monday."],["C","On Sunday."]],"answer":"A"},
    {"num":2,"q":"When must the books be returned?","opts":[["A","Before the end of the week."],["B","At the end of the month."],["C","Next year."]],"answer":"A"},
    {"num":3,"q":"What is the school known for?","opts":[["A","Its good tradition."],["B","Its big playground."],["C","Its long history."]],"answer":"A"},
    {"num":4,"q":"What is the purpose of the notice?","opts":[["A","To keep everyone informed."],["B","To sell books."],["C","To close the school."]],"answer":"A"}]},
 "w5": {"id":"DXH2026_L30_w5","title":"根据短文内容，从方框中选出最佳句子填入文中空白处（有一项多余）",
   "绑定":"G65进阶 情态被动",
   "paragraphs":[
    "Classroom Rules",
    "Our classroom has some important rules.",
    "Students must be quiet in the library. ___1___ Noise should be avoided there.",
    "Homework must be finished on time. ___2___ It should be checked carefully.",
    "Mobile phones are not allowed in class. ___3___ They should be turned off.",
    "Everyone is expected to be kind to others. ___4___ Good manners are valued here."],
   "candidates":[["A","They should be kept in the bag."],["B","Kind words should be spoken often."],["C","The tables should be kept clean."],["D","Late work is not accepted."],["E","The room should be kept quiet."]],
   "answers":{"1":"E","2":"D","3":"A","4":"B"}},
 "cloze": {"id":"DXH2026_L30_cloze","title":"完形填空",
   "绑定":"G65进阶 情态被动+主动表被动",
   "paragraphs":[
    "The work can ___1___ done today.",
    "This book ___2___ well in the market.",
    "Homework must ___3___ finished on time.",
    "The rules should ___4___ followed by everyone.",
    "This cloth ___5___ easily.",
    "The story ___6___ well and is loved by children.",
    "Smoking is ___7___ on the campus.",
    "Students are ___8___ to be polite to others.",
    "The products are ___9___ to many cities.",
    "Photos are ___10___ in the art room."],
   "items":[
    {"num":1,"opts":[["A","be"],["B","is"],["C","was"]],"answer":"A"},
    {"num":2,"opts":[["A","sells"],["B","is sold"],["C","sell"]],"answer":"A"},
    {"num":3,"opts":[["A","be"],["B","is"],["C","was"]],"answer":"A"},
    {"num":4,"opts":[["A","be"],["B","is"],["C","was"]],"answer":"A"},
    {"num":5,"opts":[["A","washes"],["B","is washed"],["C","wash"]],"answer":"A"},
    {"num":6,"opts":[["A","reads"],["B","is read"],["C","read"]],"answer":"A"},
    {"num":7,"opts":[["A","forbidden"],["B","allow"],["C","forbid"]],"answer":"A"},
    {"num":8,"opts":[["A","expected"],["B","expect"],["C","expecting"]],"answer":"A"},
    {"num":9,"opts":[["A","supplied"],["B","supply"],["C","supplying"]],"answer":"A"},
    {"num":10,"opts":[["A","permitted"],["B","permit"],["C","permitting"]],"answer":"A"}]},
 "grammar_fill": {"id":"DXH2026_L30_grammar_fill","title":"从方框内选择适当的词并用其正确形式填空（每空限填一词）",
   "绑定":"G65进阶 情态被动+主动表被动",
   "word_bank":["can","must","should","sell","wash","read","forbid","allow","expect","supply","extra","extra"],
   "paragraphs":[
    "The work ___1___ be done today.",
    "This book ___2___ well in the market.",
    "Homework ___3___ be finished on time.",
    "The rules ___4___ be followed by everyone.",
    "This cloth ___5___ easily.",
    "The story ___6___ well.",
    "Smoking is ___7___ on the campus.",
    "Photos are ___8___ in the art room.",
    "Students are ___9___ to be polite.",
    "The products are ___10___ to many cities."],
   "answers":["can","sells","must","should","washes","reads","forbidden","allowed","expected","supplied"]},
 "sa": {"id":"DXH2026_L30_sa","title":"阅读表达",
   "passage_title":"Library Rules",
   "绑定":"G65进阶 情态被动",
   "paragraphs":[
    "The library has many rules. They should be followed by every student.",
    "Noise must be avoided in the reading room. Books should be returned on time.",
    "Mobile phones are not allowed in the library. They should be turned off.",
    "Students are expected to keep the room clean. Photos are permitted in the hall."],
   "questions":[
    {"num":1,"q":"What must be avoided in the reading room?","answer":"Noise.","type":"简答"},
    {"num":2,"q":"When should the books be returned?","answer":"On time.","type":"简答"},
    {"num":3,"q":"Are mobile phones allowed in the library?","answer":"No, they are not allowed.","type":"简答"},
    {"num":4,"q":"请把文中画线句子翻译成汉语（They should be followed by every student.）","answer":"它们应该被每个学生遵守。","type":"翻译"},
    {"num":5,"q":"Where are photos permitted?","answer":"In the hall.","type":"简答"}]},
 "writing": {"id":"DXH2026_L30_writing","title":"书面表达",
   "prompt":"假如你是李华，请用英语写一篇80词左右的短文，介绍你学校或班级的规则（用被动语态与情态动词，如 must/should/can be done），并说明遵守规则的好处。",
   "sample":[
    "Rules in Our School",
    "Every school has rules, and ours is no different.",
    "Students must be on time for class. Noise should be avoided in the library. Mobile phones are not allowed in class.",
    "Homework must be finished on time. These rules are made to keep us safe. They should be followed by everyone.",
    "I think good rules help us study better. Following them makes our school a happy place."],
   "requirements":"1. 词数约80词；2. 用被动语态与情态动词；3. 语句通顺，语法正确；4. 可适当发挥。",
   "绑定":"被动语态进阶"}}

# 语法诊断（20 分：mc5 + fill5）
def _diag(lesson, gram, mc, fill):
    return {"id":"DXH2026_L%d_grammar_diag"%lesson,"title":"语法诊断","mc":mc,"fill":fill}

L26["grammar_diag"] = _diag(26,"G16/G43/G46",
 [{"num":1,"q":"He ____ to school every day.","opts":[["A","goes"],["B","go"],["C","going"]],"answer":"A","绑定":"G16"},
  {"num":2,"q":"She is ____ her homework now.","opts":[["A","doing"],["B","does"],["C","do"]],"answer":"A","绑定":"G46"},
  {"num":3,"q":"I ____ my homework yesterday.","opts":[["A","finished"],["B","finish"],["C","finishing"]],"answer":"A","绑定":"G16"},
  {"num":4,"q":"He ____ drinks milk in the morning.","opts":[["A","usually"],["B","yesterday"],["C","now"]],"answer":"A","绑定":"G43"},
  {"num":5,"q":"Look! They ____ football in the park.","opts":[["A","are playing"],["B","play"],["C","played"]],"answer":"A","绑定":"G46"}],
 [{"num":1,"q":"She ____ (watch) TV now.","answer":"is watching","绑定":"G46"},
  {"num":2,"q":"We ____ (go) to school by bike every day.","answer":"go","绑定":"G16"},
  {"num":3,"q":"I ____ (visit) my grandparents last week.","answer":"visited","绑定":"G16"},
  {"num":4,"q":"He ____ (often) plays basketball after school.","answer":"often","绑定":"G43"},
  {"num":5,"q":"They ____ (have) a music lesson at the moment.","answer":"are having","绑定":"G46"}])

L27["grammar_diag"] = _diag(27,"G64 现在完成时",
 [{"num":1,"q":"I have ____ finished my homework.","opts":[["A","just"],["B","yesterday"],["C","tomorrow"]],"answer":"A","绑定":"G64"},
  {"num":2,"q":"She has ____ to school.","opts":[["A","gone"],["B","go"],["C","going"]],"answer":"A","绑定":"G64"},
  {"num":3,"q":"Have you ____ been to Beijing?","opts":[["A","ever"],["B","yet"],["C","for"]],"answer":"A","绑定":"G64"},
  {"num":4,"q":"He hasn't finished the work ____.","opts":[["A","yet"],["B","already"],["C","just"]],"answer":"A","绑定":"G64"},
  {"num":5,"q":"I have been to the museum ____.","opts":[["A","once"],["B","yesterday"],["C","last week"]],"answer":"A","绑定":"G64"}],
 [{"num":1,"q":"I have ____ (see) this movie before.","answer":"seen","绑定":"G64"},
  {"num":2,"q":"She has ____ (finish) her homework.","answer":"finished","绑定":"G64"},
  {"num":3,"q":"We ____ (be) to Shanghai twice.","answer":"have been","绑定":"G64"},
  {"num":4,"q":"He has never ____ (eat) such food.","answer":"eaten","绑定":"G64"},
  {"num":5,"q":"They have already ____ (visit) the museum.","answer":"visited","绑定":"G64"}])

L28["grammar_diag"] = _diag(28,"G64 since/for",
 [{"num":1,"q":"I have lived here ____ 2015.","opts":[["A","since"],["B","for"],["C","in"]],"answer":"A","绑定":"G64"},
  {"num":2,"q":"He has worked here ____ two years.","opts":[["A","for"],["B","since"],["C","in"]],"answer":"A","绑定":"G64"},
  {"num":3,"q":"My brother has ____ to Shanghai. He is there now.","opts":[["A","gone"],["B","been"],["C","go"]],"answer":"A","绑定":"G64"},
  {"num":4,"q":"I have ____ to the Great Wall twice.","opts":[["A","been"],["B","gone"],["C","go"]],"answer":"A","绑定":"G64"},
  {"num":5,"q":"The city has changed a lot ____ 2010.","opts":[["A","since"],["B","for"],["C","in"]],"answer":"A","绑定":"G64"}],
 [{"num":1,"q":"I have known him ____ (很) a long time.","answer":"for","绑定":"G64"},
  {"num":2,"q":"We have studied here ____ (自从) last year.","answer":"since","绑定":"G64"},
  {"num":3,"q":"She has ____ (go) to Beijing. She isn't here.","answer":"gone","绑定":"G64"},
  {"num":4,"q":"Have you ever ____ (be) to the museum?","answer":"been","绑定":"G64"},
  {"num":5,"q":"The school has ____ (change) a lot.","answer":"changed","绑定":"G64"}])

L29["grammar_diag"] = _diag(29,"G65 被动语态",
 [{"num":1,"q":"Tea ____ grown in China.","opts":[["A","is"],["B","are"],["C","be"]],"answer":"A","绑定":"G65"},
  {"num":2,"q":"The window ____ broken yesterday.","opts":[["A","was"],["B","is"],["C","be"]],"answer":"A","绑定":"G65"},
  {"num":3,"q":"The room ____ cleaned every morning.","opts":[["A","is"],["B","are"],["C","be"]],"answer":"A","绑定":"G65"},
  {"num":4,"q":"The bridge ____ built in 2010.","opts":[["A","was"],["B","is"],["C","be"]],"answer":"A","绑定":"G65"},
  {"num":5,"q":"These books ____ written by a famous writer.","opts":[["A","were"],["B","was"],["C","be"]],"answer":"A","绑定":"G65"}],
 [{"num":1,"q":"The cake is ____ (make) by my mother.","answer":"made","绑定":"G65"},
  {"num":2,"q":"The house was ____ (build) in 2010.","answer":"built","绑定":"G65"},
  {"num":3,"q":"The flowers are ____ (water) every day.","answer":"watered","绑定":"G65"},
  {"num":4,"q":"The song is ____ (sing) by many students.","answer":"sung","绑定":"G65"},
  {"num":5,"q":"The work was ____ (finish) yesterday.","answer":"finished","绑定":"G65"}])

L30["grammar_diag"] = _diag(30,"G65 情态被动+主动表被动",
 [{"num":1,"q":"The work can ____ done today.","opts":[["A","be"],["B","is"],["C","was"]],"answer":"A","绑定":"G65"},
  {"num":2,"q":"This book ____ well in the market.","opts":[["A","sells"],["B","is sold"],["C","sell"]],"answer":"A","绑定":"G65"},
  {"num":3,"q":"Rules must ____ be followed.","opts":[["A","be"],["B","is"],["C","was"]],"answer":"A","绑定":"G65"},
  {"num":4,"q":"This cloth ____ easily.","opts":[["A","washes"],["B","is washed"],["C","wash"]],"answer":"A","绑定":"G65"},
  {"num":5,"q":"Smoking is ____ on the campus.","opts":[["A","forbidden"],["B","allow"],["C","forbid"]],"answer":"A","绑定":"G65"}],
 [{"num":1,"q":"The work must be ____ (do) today.","answer":"done","绑定":"G65"},
  {"num":2,"q":"This story ____ (read) well.","answer":"reads","绑定":"G65"},
  {"num":3,"q":"The rules should be ____ (follow).","answer":"followed","绑定":"G65"},
  {"num":4,"q":"Photos are ____ (allow) in the hall.","answer":"allowed","绑定":"G65"},
  {"num":5,"q":"The products are ____ (supply) to many cities.","answer":"supplied","绑定":"G65"}])

LESSONS = {26:L26, 27:L27, 28:L28, 29:L29, 30:L30}

# 结构：授课课渲染参数（阅读30/语言25/综合25/语法诊断20，不含听力）
def render_paper(lesson, content, test=False):
    card = {"lesson":lesson,"student":"邓兴华","tier":"中等","stage":"Stage 6",
            "type":"授课课练习","theme":"","listening":False}
    doc = bpp.Document()
    for s in doc.sections:
        s.top_margin=bpp.Cm(1.5); s.bottom_margin=bpp.Cm(1.5)
        s.left_margin=bpp.Cm(1.5); s.right_margin=bpp.Cm(1.5)
    _heading(doc, "第 %02d 课时配套练习" % lesson)
    _para(doc, "学生：邓兴华    层级：中等    结构对齐 2026 湖南中考（不含听力）    满分：100 分",
          align=bpp.WD_ALIGN_PARAGRAPH.CENTER, size=10.5)
    _para(doc, "姓名：____________    得分：____________    用时：____________",
          align=bpp.WD_ALIGN_PARAGRAPH.CENTER, size=10.5)
    qnum = 1
    ans1_rd, ans1_w5 = [], []
    ans2_cl, ans2_gf = [], []
    ans3_sa, ans3_wr = [], []
    ans4 = []

    # 第一部分 阅读理解（22+8=30）
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

    # 第二部分 语言运用（15+10=25）
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

    # 第三部分 综合技能（阅读表达5×2=10 + 写作15=25）
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

    # 第四部分 语法诊断（20 分）
    gd = content["grammar_diag"]
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
    for lesson in (26,27,28,29,30):
        p, total = render_paper(lesson, LESSONS[lesson], test=False)
        print("L%d 练习生成：%s（%d 题, %d bytes）" % (lesson, p, total, os.path.getsize(p)))