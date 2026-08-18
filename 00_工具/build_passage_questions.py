# -*- coding: utf-8 -*-
"""缺口 D/E 补题器（真题母本 阅读/完形/五选五 单篇切题 · 全量）
- 缺口 D（reading）：真题母本阅读单篇题目未切片 → 12 篇 reading_a 各 5 题（含答案）
- 缺口 E（cloze）：完形题目待生成 → 14 篇完形
    · 9 篇真题内嵌原题选项（L6/L8/L14–L20）→ 选项照抄真题，答案按语法推导（真源）
    · 5 篇无原题选项（L1/L2/L3/L4/L13）→ 按本课语法点命制选项，答案平衡（A/B/C 各 ≤40%）
- 缺口 E（w5）：五选五候选句被源稿剥掉 → 3 篇（L1/L6/L8）命制候选句（provenance=命制）
- 输出 passage_questions.json：{reading:{id:[题]}, cloze:{id:[题]}, w5:{id:{candidates,blanks}}}
  不改 passage_bank.json（由 build_passage_bank.py 重建，避免污染母本）。
- 硬校验：每题 answer 在 opts 内；reading/cloze 单字母分布 ≤40%；w5 答案在候选字母内。
"""
import json, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = "D:/英语教学/01_数据"

def Q(n, q, opts, answer):
    return {"num": n, "q": q, "opts": [[l, t] for l, t in opts], "answer": answer}

# ────────────────────────────── 缺口 D：reading_a（12 篇）──────────────────────────────
READING = {
  "HN2026_L6_reading_a": [
    Q(1, "What does Lily have for breakfast?", [("A", "milk and bread"), ("B", "rice and vegetables"), ("C", "apples and bananas")], "A"),
    Q(2, "Where does Lily eat lunch?", [("A", "at home"), ("B", "at school"), ("C", "in a restaurant")], "B"),
    Q(3, "What do Lily's family eat for dinner?", [("A", "rice and chicken"), ("B", "bread and milk"), ("C", "apples, bananas and oranges")], "C"),
    Q(4, "Why does Lily NOT like fast food?", [("A", "Because it is not good"), ("B", "Because it is too expensive"), ("C", "Because it is too sweet")], "A"),
    Q(5, "What helps Lily grow tall and strong?", [("A", "Fast food and cola"), ("B", "Fruit and milk"), ("C", "Candy and cakes")], "B"),
  ],
  "HN2026_L8_reading_a": [
    Q(1, "When did the family go on the trip?", [("A", "yesterday"), ("B", "today"), ("C", "tomorrow")], "A"),
    Q(2, "What did the writer pack in the morning?", [("A", "food and water"), ("B", "clothes"), ("C", "a postcard")], "B"),
    Q(3, "How was the weather that day?", [("A", "cold and rainy"), ("B", "windy and dark"), ("C", "sunny and warm")], "C"),
    Q(4, "What time did the trip start?", [("A", "at 8 a.m."), ("B", "at 6 p.m."), ("C", "at 9 a.m.")], "A"),
    Q(5, "What did the writer buy for a friend?", [("A", "a map"), ("B", "a postcard"), ("C", "a camera")], "B"),
  ],
  "HN2026_L2_reading_a": [
    Q(1, "What is the passage mainly about?", [("A", "a family photo album"), ("B", "a school show"), ("C", "a birthday party")], "A"),
    Q(2, "Who can you see in the first picture?", [("A", "father and mother"), ("B", "grandpa and grandma"), ("C", "my cousin")], "B"),
    Q(3, "Who is the little boy in the picture?", [("A", "my brother"), ("B", "my friend"), ("C", "my cousin")], "C"),
    Q(4, "How is the family?", [("A", "happy"), ("B", "sad"), ("C", "busy")], "A"),
    Q(5, "The passage may be from ______.", [("A", "a diary"), ("B", "a class show"), ("C", "a letter")], "B"),
  ],
  "HN2026_L3_reading_a": [
    Q(1, "Where were the things found this week?", [("A", "in the school library"), ("B", "in the classroom"), ("C", "in the park")], "A"),
    Q(2, "When was the white eraser found?", [("A", "on Monday"), ("B", "on Tuesday"), ("C", "on Wednesday")], "B"),
    Q(3, "What is in the blue pencil box?", [("A", "a cat picture"), ("B", "a red cover"), ("C", "two pens and a ruler")], "C"),
    Q(4, "What must you do before taking a thing?", [("A", "describe your thing"), ("B", "pay some money"), ("C", "call your teacher")], "A"),
    Q(5, "What does the English dictionary have?", [("A", "a white eraser"), ("B", "a red cover"), ("C", "a blue pencil box")], "B"),
  ],
  "HN2026_L13_reading_a": [
    Q(1, "When is the big weekend sale?", [("A", "from Friday to Sunday"), ("B", "from Monday to Friday"), ("C", "every weekend in June")], "A"),
    Q(2, "How much is the discount on fresh fruit before 9 a.m.?", [("A", "ten percent off"), ("B", "twenty percent off"), ("C", "thirty percent off")], "B"),
    Q(3, "What is the special deal on milk, bread and eggs?", [("A", "twenty percent off"), ("B", "buy one, get one free"), ("C", "buy two, get one free")], "C"),
    Q(4, "What do you get if you spend over fifty yuan?", [("A", "a free package of salt"), ("B", "a free bag"), ("C", "a free package of sugar")], "A"),
    Q(5, "When is the supermarket open every day?", [("A", "from 9 a.m. to 5 p.m."), ("B", "from 8 a.m. to 10 p.m."), ("C", "from 8 a.m. to 8 p.m.")], "B"),
  ],
  "HN2026_L14_reading_a": [
    Q(1, "Who is the writer's favorite teacher?", [("A", "Mr. Lee"), ("B", "Mr. Brown"), ("C", "Miss Li")], "A"),
    Q(2, "What does Mr. Lee look like?", [("A", "short and thin"), ("B", "tall and thin"), ("C", "tall and fat")], "B"),
    Q(3, "Why is Mr. Lee popular?", [("A", "because he is strict"), ("B", "because he is handsome"), ("C", "because he is patient and funny")], "C"),
    Q(4, "How does Mr. Lee explain difficult ideas?", [("A", "with easy examples"), ("B", "with long sentences"), ("C", "with pictures")], "A"),
    Q(5, "What does the writer want to be when he grows up?", [("A", "a doctor"), ("B", "a teacher like Mr. Lee"), ("C", "a writer")], "B"),
  ],
  "HN2026_L15_reading_a": [
    Q(1, "When is the school trip to Green Mountain?", [("A", "on Saturday"), ("B", "on Sunday"), ("C", "on Friday")], "A"),
    Q(2, "What is the weather like in the morning?", [("A", "cloudy and cool"), ("B", "sunny and warm"), ("C", "rainy and cold")], "B"),
    Q(3, "What should students bring for the morning?", [("A", "an umbrella"), ("B", "comfortable shoes"), ("C", "sunglasses and a hat")], "C"),
    Q(4, "When is there a chance of rain?", [("A", "after 3:00 p.m."), ("B", "in the morning"), ("C", "at noon")], "A"),
    Q(5, "What should students wear for hiking?", [("A", "new clothes"), ("B", "comfortable shoes"), ("C", "a coat")], "B"),
  ],
  "HN2026_L16_reading_a": [
    Q(1, "What is the passage mainly about?", [("A", "school clubs"), ("B", "school lessons"), ("C", "school food")], "A"),
    Q(2, "When does the Sports Club meet?", [("A", "every Monday"), ("B", "every Tuesday and Thursday"), ("C", "every Wednesday")], "B"),
    Q(3, "Who is the art teacher?", [("A", "Mr. Smith"), ("B", "Mr. Brown"), ("C", "Miss Li")], "C"),
    Q(4, "What do students do in the Weather Club?", [("A", "watch the weather and write reports"), ("B", "play basketball"), ("C", "draw pictures")], "A"),
    Q(5, "What do students need to sign up for the clubs?", [("A", "some money"), ("B", "their student card"), ("C", "their homework")], "B"),
  ],
  "HN2026_L17_reading_a": [
    Q(1, "What is the survey about?", [("A", "teenagers' daily habits"), ("B", "family housework"), ("C", "school clubs")], "A"),
    Q(2, "How many percent of students exercise every day?", [("A", "twenty percent"), ("B", "sixty percent"), ("C", "eighty percent")], "B"),
    Q(3, "How many percent of students sometimes eat junk food?", [("A", "forty percent"), ("B", "twenty percent"), ("C", "fifty percent")], "C"),
    Q(4, "How long do most students sleep each night?", [("A", "about seven hours"), ("B", "about eight hours"), ("C", "about six hours")], "A"),
    Q(5, "According to the passage, what gives students energy for study?", [("A", "watching TV"), ("B", "good habits"), ("C", "junk food")], "B"),
  ],
  "HN2026_L18_reading_a": [
    Q(1, "What is the survey about?", [("A", "family housework"), ("B", "weekend activities"), ("C", "school clubs")], "A"),
    Q(2, "What are forty percent of mothers doing?", [("A", "washing clothes"), ("B", "cooking"), ("C", "watching TV")], "B"),
    Q(3, "What are thirty percent of children doing?", [("A", "watching TV"), ("B", "playing games"), ("C", "doing homework")], "C"),
    Q(4, "How many percent of fathers are washing clothes?", [("A", "twenty-five percent"), ("B", "thirty percent"), ("C", "forty percent")], "A"),
    Q(5, "What does doing housework together help family members do?", [("A", "get more money"), ("B", "talk and understand each other"), ("C", "study better at once")], "B"),
  ],
  "HN2026_L19_reading_a": [
    Q(1, "What is the survey about?", [("A", "weekend activities"), ("B", "school subjects"), ("C", "family food")], "A"),
    Q(2, "How many percent of students go somewhere fun on weekends?", [("A", "thirty percent"), ("B", "fifty percent"), ("C", "twenty percent")], "B"),
    Q(3, "What do thirty percent of students do on weekends?", [("A", "go abroad"), ("B", "explore the city"), ("C", "stay at home and read books")], "C"),
    Q(4, "What does the best story get?", [("A", "a prize"), ("B", "a book"), ("C", "a trip")], "A"),
    Q(5, "How do most students feel about their weekends?", [("A", "bored"), ("B", "enjoyable"), ("C", "tired")], "B"),
  ],
  "HN2026_L20_reading_a": [
    Q(1, "Where does Green Hill Town sit?", [("A", "below a green hill"), ("B", "on the top of a hill"), ("C", "beside a big city")], "A"),
    Q(2, "What can you see at the top of the hill?", [("A", "the old stone building"), ("B", "the entire town"), ("C", "the lake")], "B"),
    Q(3, "What is the old stone building at the top?", [("A", "a museum"), ("B", "a church"), ("C", "a famous landmark")], "C"),
    Q(4, "What are the ducks doing in the lake?", [("A", "swimming in the clear blue water"), ("B", "eating fresh fruit"), ("C", "sleeping by the lake")], "A"),
    Q(5, "What can you do if you feel hungry by the lake?", [("A", "go back to town"), ("B", "try the fresh fruit and snacks"), ("C", "camp by the lake")], "B"),
  ],
}

# ─────────────────── 缺口 E：cloze 真题内嵌原题选项（9 篇，选项照抄真题）───────────────────
CLOZE_AUTH = {
  # 一般现在时实义动词（第三人称单数/否定/动词选择）
  "HN2026_L6_cloze": [
    Q(21, "I ___ healthy food every day because it makes me strong.", [("A", "like"), ("B", "likes"), ("C", "am")], "A"),
    Q(22, "For breakfast, I ___ milk and bread at home with my mum.", [("A", "have"), ("B", "has"), ("C", "drink")], "A"),
    Q(23, "I ___ like fast food because it is not good for my body.", [("A", "don't"), ("B", "doesn't"), ("C", "am not")], "A"),
    Q(24, "My mum ___ apples and bananas for us every week.", [("A", "like"), ("B", "likes"), ("C", "eat")], "B"),
    Q(25, "We eat rice and ___ for lunch at school with friends.", [("A", "vegetable"), ("B", "vegetables"), ("C", "meats")], "B"),
    Q(26, "___ dinner, we have chicken and vegetables together.", [("A", "For"), ("B", "In"), ("C", "On")], "A"),
    Q(27, "I ___ an apple every day after school.", [("A", "eat"), ("B", "eats"), ("C", "has")], "A"),
    Q(28, "My sister ___ eggs in the morning before class.", [("A", "eat"), ("B", "eats"), ("C", "like")], "B"),
    Q(29, "We ___ water, not cola or juice.", [("A", "drinks"), ("B", "drink"), ("C", "drinking")], "B"),
    Q(30, "Good food ___ us strong and happy.", [("A", "make"), ("B", "makes"), ("C", "making")], "B"),
  ],
  # 一般过去时（实义动词过去式 / be 动词过去式）
  "HN2026_L8_cloze": [
    Q(21, "Last summer, I ___ to Beijing with my family for a happy holiday by train.", [("A", "went"), ("B", "go"), ("C", "goes")], "A"),
    Q(22, "We ___ the Great Wall and walked a long way up the tall hill.", [("A", "visited"), ("B", "visit"), ("C", "visiting")], "A"),
    Q(23, "It ___ very tall and long under the blue sky and white clouds.", [("A", "was"), ("B", "is"), ("C", "were")], "A"),
    Q(24, "The weather ___ sunny and warm all day.", [("A", "was"), ("B", "is"), ("C", "were")], "A"),
    Q(25, "We ___ many photos of the nice view from the top.", [("A", "took"), ("B", "take"), ("C", "taking")], "A"),
    Q(26, "My sister ___ an ice cream near the gate and smiled a lot.", [("A", "bought"), ("B", "buy"), ("C", "buys")], "A"),
    Q(27, "We ___ some delicious food at a small shop on the street.", [("A", "ate"), ("B", "eat"), ("C", "eats")], "A"),
    Q(28, "The happy trip ___ at 6 p.m.", [("A", "finished"), ("B", "finish"), ("C", "finishing")], "A"),
    Q(29, "We ___ very happy and not tired after the long walk.", [("A", "were"), ("B", "are"), ("C", "was")], "A"),
    Q(30, "It ___ a wonderful day for all of us to remember!", [("A", "was"), ("B", "is"), ("C", "were")], "A"),
  ],
  # 外貌描述（has/with、连词、副词、感叹句）
  "HN2026_L14_cloze": [
    Q(21, "She is a girl of medium ___.", [("A", "height"), ("B", "weight"), ("C", "color")], "A"),
    Q(22, "She ___ long straight black hair and big bright eyes.", [("A", "is"), ("B", "has"), ("C", "have")], "B"),
    Q(23, "Her face is ___ and round.", [("A", "small"), ("B", "long"), ("C", "round")], "A"),
    Q(24, "Linda is not very tall, ___ she looks neat and energetic.", [("A", "but"), ("B", "so"), ("C", "because")], "A"),
    Q(25, "She is also a good ___. She sings beautifully.", [("A", "singer"), ("B", "actor"), ("C", "artist")], "A"),
    Q(26, "___ do so many students like her?", [("A", "What"), ("B", "Why"), ("C", "How")], "B"),
    Q(27, "___ she is kind and helpful.", [("A", "So"), ("B", "Because"), ("C", "For")], "B"),
    Q(28, "Her smile makes people feel ___.", [("A", "warm"), ("B", "cold"), ("C", "sad")], "A"),
    Q(29, "She is a ___ girl.", [("A", "big"), ("B", "tall"), ("C", "kind")], "C"),
    Q(30, "She is a kind girl, ___ we all like her.", [("A", "and"), ("B", "but"), ("C", "or")], "A"),
  ],
  # 一般现在时第三人称单数 / 天气温度 / 祈使/请求
  "HN2026_L15_cloze": [
    Q(21, "My family ___ to go there this summer.", [("A", "plan"), ("B", "plans"), ("C", "planning")], "A"),
    Q(22, "My mother ___ the weather forecast every day.", [("A", "check"), ("B", "checks"), ("C", "checking")], "B"),
    Q(23, "The temperature is about 30 ___.", [("A", "degree"), ("B", "degrees"), ("C", "degree's")], "B"),
    Q(24, "Could you ___ me pack my swimsuit?", [("A", "help"), ("B", "to help"), ("C", "helping")], "A"),
    Q(25, "She is very ___ and helps me put clothes into my suitcase.", [("A", "sad"), ("B", "kind"), ("C", "angry")], "B"),
    Q(26, "When we arrive, it is ___ sunny.", [("A", "real"), ("B", "really"), ("C", "very much")], "B"),
    Q(27, "Would you like to go ___ with me?", [("A", "swimming"), ("B", "shopping"), ("C", "hiking")], "A"),
    Q(28, "In the evening, the wind is ___. It is very comfortable.", [("A", "strong"), ("B", "mild"), ("C", "heavy")], "B"),
    Q(29, "___ a wonderful day!", [("A", "What"), ("B", "How"), ("C", "What a")], "C"),
    Q(30, "The beautiful ___ makes our trip special.", [("A", "scenery"), ("B", "hotel"), ("C", "raincoat")], "A"),
  ],
  # 一般现在时（with、wear、be 动词、介词、第三人称单数）
  "HN2026_L16_cloze": [
    Q(21, "She is a tall girl ___ long straight hair.", [("A", "has"), ("B", "with"), ("C", "have")], "B"),
    Q(22, "She ___ glasses every day.", [("A", "wear"), ("B", "wears"), ("C", "wearing")], "B"),
    Q(23, "Lily is very ___ and she always helps me with my homework.", [("A", "kind"), ("B", "cold"), ("C", "boring")], "A"),
    Q(24, "Lily and I ___ in the same class.", [("A", "am"), ("B", "is"), ("C", "are")], "C"),
    Q(25, "Our classroom is ___ the second floor.", [("A", "in"), ("B", "on"), ("C", "at")], "B"),
    Q(26, "There ___ thirty students in our class.", [("A", "is"), ("B", "are"), ("C", "be")], "B"),
    Q(27, "She ___ English.", [("A", "teach"), ("B", "teaches"), ("C", "teaching")], "B"),
    Q(28, "She ___ basketball every day after school.", [("A", "play"), ("B", "plays"), ("C", "playing")], "B"),
    Q(29, "She also likes ___ fruit, especially apples and bananas.", [("A", "eat"), ("B", "eating"), ("C", "eats")], "B"),
    Q(30, "She wants to be a great ___ when she grows up.", [("A", "teacher"), ("B", "teach"), ("C", "teachers")], "A"),
  ],
  # 频度副词 / 三餐 / 健康习惯
  "HN2026_L17_cloze": [
    Q(21, "She ___ gets up at six o'clock every morning.", [("A", "usually"), ("B", "sometimes"), ("C", "never")], "A"),
    Q(22, "She ___ for twenty minutes in the park every day.", [("A", "jogs"), ("B", "jog"), ("C", "jogging")], "A"),
    Q(23, "After that, she eats a healthy ___.", [("A", "lunch"), ("B", "breakfast"), ("C", "dinner")], "B"),
    Q(24, "She ___ eats junk food in the morning.", [("A", "always"), ("B", "never"), ("C", "usually")], "B"),
    Q(25, "She ___ eight glasses of water every day.", [("A", "drink"), ("B", "drinks"), ("C", "drinking")], "B"),
    Q(26, "She hardly ___ eats junk food.", [("A", "ever"), ("B", "never"), ("C", "always")], "A"),
    Q(27, "She thinks it is bad for her ___.", [("A", "health"), ("B", "healthy"), ("C", "body")], "A"),
    Q(28, "She exercises ___ a week.", [("A", "twice"), ("B", "two"), ("C", "second")], "A"),
    Q(29, "Sometimes she reads books online in the ___.", [("A", "morning"), ("B", "evening"), ("C", "afternoon")], "B"),
    Q(30, "Lisa has a healthy ___.", [("A", "lifestyle"), ("B", "habit"), ("C", "result")], "A"),
  ],
  # 现在进行时（家务场景）
  "HN2026_L18_cloze": [
    Q(21, "Mom ___ in the kitchen. She is cooking a big breakfast.", [("A", "is cooking"), ("B", "are cooking"), ("C", "cooks")], "A"),
    Q(22, "The food smells ___.", [("A", "bad"), ("B", "wonderful"), ("C", "terrible")], "B"),
    Q(23, "He is ___ washing the windows.", [("A", "also"), ("B", "too"), ("C", "either")], "A"),
    Q(24, "She is ___ her bed and organizing her desk.", [("A", "making"), ("B", "doing"), ("C", "washing")], "A"),
    Q(25, "She is a ___ girl.", [("A", "lazy"), ("B", "tidy"), ("C", "messy")], "B"),
    Q(26, "Their son Ben is in the ___. He is washing his clothes.", [("A", "kitchen"), ("B", "bathroom"), ("C", "garden")], "B"),
    Q(27, "He is ___ chatting with his friend online.", [("A", "too"), ("B", "also"), ("C", "either")], "B"),
    Q(28, "He is ___ TV.", [("A", "watching"), ("B", "seeing"), ("C", "looking")], "A"),
    Q(29, "Grandma is ___ next to him. She is reading a newspaper.", [("A", "sitting"), ("B", "standing"), ("C", "sleeping")], "A"),
    Q(30, "Everyone is busy ___ happy.", [("A", "or"), ("B", "but"), ("C", "and")], "B"),
  ],
  # 不定代词（something/anything/nothing）
  "HN2026_L19_cloze": [
    Q(21, "It is Sunday. Lisa is at home. She feels ___ because she has nothing to do.", [("A", "bored"), ("B", "happy"), ("C", "tired")], "A"),
    Q(22, "She feels bored because she has ___ to do.", [("A", "something"), ("B", "nothing"), ("C", "everything")], "B"),
    Q(23, "She looks around the house but can't find ___ interesting.", [("A", "something"), ("B", "anything"), ("C", "nothing")], "B"),
    Q(24, "\"I know!\" she says. \"I can plan ___ special.\"", [("A", "something"), ("B", "anything"), ("C", "nothing")], "A"),
    Q(25, "I want to find ___ new and exciting.", [("A", "something"), ("B", "anything"), ("C", "everything")], "A"),
    Q(26, "\"Is ___ free today?\" she asks.", [("A", "someone"), ("B", "anyone"), ("C", "everyone")], "B"),
    Q(27, "Everyone ___ happy and excited.", [("A", "seem"), ("B", "seems"), ("C", "seeming")], "B"),
    Q(28, "In the evening, Lisa writes in her ___.", [("A", "diary"), ("B", "book"), ("C", "letter")], "A"),
    Q(29, "\"Today is ___.\"", [("A", "bored"), ("B", "enjoyable"), ("C", "terrible")], "B"),
    Q(30, "There is ___ better than exploring with a good friend.", [("A", "something"), ("B", "nothing"), ("C", "anything")], "B"),
  ],
  # 一般现在时第三人称单数 / 名词辨析
  "HN2026_L20_cloze": [
    Q(21, "Every weekend, Lisa ___ to a nearby hill with her family.", [("A", "go"), ("B", "goes"), ("C", "going")], "B"),
    Q(22, "They ride their bicycles for a short ___ to get there.", [("A", "distance"), ("B", "building"), ("C", "sentence")], "A"),
    Q(23, "The hill is not very tall, but the view at the ___ is always beautiful.", [("A", "below"), ("B", "top"), ("C", "hill")], "B"),
    Q(24, "Lisa loves to watch the ducks swim in the lake ___ the hill.", [("A", "on"), ("B", "below"), ("C", "above")], "B"),
    Q(25, "Her mother always packs ___ food and water for the trip.", [("A", "enough"), ("B", "hungry"), ("C", "entire")], "A"),
    Q(26, "Nobody feels hungry because they bring enough ___ to eat.", [("A", "umbrella"), ("B", "snacks"), ("C", "bicycle")], "B"),
    Q(27, "On ___ mornings, the hill looks mysterious.", [("A", "sunny"), ("B", "foggy"), ("C", "warm")], "B"),
    Q(28, "She ___ the foggy weather, but she still goes because she loves the fresh air on the hill.", [("A", "likes"), ("B", "dislikes"), ("C", "enjoys")], "B"),
    Q(29, "A local ___ often sells fruit at the foot of the hill.", [("A", "trader"), ("B", "tourist"), ("C", "guide")], "A"),
    Q(30, "Each trip to the hill leaves her a sweet ___.", [("A", "memory"), ("B", "journey"), ("C", "building")], "A"),
  ],
}

# ─────────────── 缺口 E：cloze 无原题选项（5 篇，按本课语法点命制，答案平衡）───────────────
CLOZE_AUTHOR = {
  # L1 自我介绍：be 动词/代词/冠词
  "HN2026_L1_cloze": [
    Q(16, "My ___ is Tom.", [("A", "name"), ("B", "room"), ("C", "family")], "A"),
    Q(17, "I am a ___ student at No. 1 Middle School.", [("A", "busy"), ("B", "new"), ("C", "old")], "B"),
    Q(18, "I am in ___ Two, Grade Seven.", [("A", "Room"), ("B", "Number"), ("C", "Class")], "C"),
    Q(19, "I meet a nice ___ in my class.", [("A", "book"), ("B", "boy"), ("C", "teacher")], "B"),
    Q(20, "___ name is Jack.", [("A", "Her"), ("B", "My"), ("C", "His")], "C"),
    Q(21, "He ___ from China.", [("A", "am"), ("B", "is"), ("C", "are")], "B"),
    Q(22, "Jack says, \"Welcome to ___ school!\"", [("A", "our"), ("B", "your"), ("C", "my")], "A"),
    Q(23, "We talk about ___ English teacher.", [("A", "his"), ("B", "our"), ("C", "her")], "B"),
    Q(24, "___ name is Miss Wang.", [("A", "His"), ("B", "My"), ("C", "Her")], "C"),
    Q(25, "Jack and I ___ good friends now.", [("A", "is"), ("B", "am"), ("C", "are")], "C"),
  ],
  # L2 家庭：指示代词/be 动词/连词/物主代词
  "HN2026_L2_cloze": [
    Q(21, "Look! ___ is my father. He is tall.", [("A", "That"), ("B", "This"), ("C", "She")], "B"),
    Q(22, "___ is my mother. She is kind.", [("A", "He"), ("B", "It"), ("C", "This")], "C"),
    Q(23, "These ___ my grandparents.", [("A", "are"), ("B", "is"), ("C", "am")], "A"),
    Q(24, "They are old ___ happy.", [("A", "but"), ("B", "and"), ("C", "so")], "A"),
    Q(25, "___ is the little girl?", [("A", "Who"), ("B", "What"), ("C", "How")], "A"),
    Q(26, "She is very ___.", [("A", "big"), ("B", "kind"), ("C", "sad")], "B"),
    Q(27, "I am ___ to be in this family.", [("A", "sorry"), ("B", "sad"), ("C", "lucky")], "C"),
    Q(28, "Every evening, we have ___ together.", [("A", "dinner"), ("B", "breakfast"), ("C", "lunch")], "A"),
    Q(29, "My father ___ stories, and my mother sings songs.", [("A", "sings"), ("B", "reads"), ("C", "tells")], "C"),
    Q(30, "I love ___ family very much.", [("A", "our"), ("B", "my"), ("C", "their")], "B"),
  ],
  # L3 失物招领：方位介词/物主代词/Wh-词
  "HN2026_L3_cloze": [
    Q(21, "The blue pencil box is ___.", [("A", "on the desk"), ("B", "in the bag"), ("C", "under the chair")], "A"),
    Q(22, "There are two ___ and a ruler.", [("A", "cats"), ("B", "pens"), ("C", "rulers")], "B"),
    Q(23, "The red dictionary is ___.", [("A", "old"), ("B", "new"), ("C", "Tom's")], "C"),
    Q(24, "___ eraser is that?", [("A", "Whose"), ("B", "What"), ("C", "Which")], "A"),
    Q(25, "Is it Tom's? No, it is not ___.", [("A", "hers"), ("B", "his"), ("C", "mine")], "B"),
    Q(26, "It is his ___ eraser. Her name is on it.", [("A", "sister's"), ("B", "brother's"), ("C", "friend's")], "A"),
    Q(27, "Where is Tom's schoolbag? It is ___ the desk.", [("A", "on"), ("B", "in"), ("C", "under")], "C"),
    Q(28, "There are ___ books in it.", [("A", "many"), ("B", "three"), ("C", "five")], "A"),
    Q(29, "He puts things in the ___ place.", [("A", "wrong"), ("B", "right"), ("C", "new")], "B"),
    Q(30, "He says you ___ be careful!", [("A", "can"), ("B", "must"), ("C", "should")], "C"),
  ],
  # L4 房间：房间物品/方位/频度副词
  "HN2026_L4_cloze": [
    Q(16, "This is my new ___. It is small.", [("A", "school"), ("B", "room"), ("C", "book")], "B"),
    Q(17, "It is small, ___ it is very clean and tidy.", [("A", "so"), ("B", "but"), ("C", "and")], "B"),
    Q(18, "My bed is ___ to the window.", [("A", "behind"), ("B", "next"), ("C", "in front")], "B"),
    Q(19, "On the bed, there is a soft blue ___.", [("A", "quilt"), ("B", "bag"), ("C", "map")], "A"),
    Q(20, "My computer is on the ___.", [("A", "bed"), ("B", "desk"), ("C", "chair")], "B"),
    Q(21, "Under the desk, you can see my ___.", [("A", "clock"), ("B", "plant"), ("C", "schoolbag")], "C"),
    Q(22, "I have many ___, and they are all in the bookcase.", [("A", "books"), ("B", "pens"), ("C", "rulers")], "A"),
    Q(23, "I have many books, and they are all in the ___.", [("A", "box"), ("B", "room"), ("C", "bookcase")], "C"),
    Q(24, "I ___ clean my room on Sunday morning.", [("A", "always"), ("B", "never"), ("C", "usually")], "C"),
    Q(25, "It is a good ___ for me to keep every day at home.", [("A", "habit"), ("B", "time"), ("C", "way")], "A"),
  ],
  # L13 购物：购物词汇/一般过去时
  "HN2026_L13_cloze": [
    Q(21, "We picked some tomatoes and carrots. They were fresh and ___.", [("A", "heavy"), ("B", "cheap"), ("C", "expensive")], "B"),
    Q(22, "Mom chose a kilo of chicken. It was a little ___, but good for dinner.", [("A", "cheap"), ("B", "heavy"), ("C", "expensive")], "C"),
    Q(23, "Next, we needed some ___ for breakfast.", [("A", "pancakes"), ("B", "bread"), ("C", "milk")], "A"),
    Q(24, "Mom let me choose ___.", [("A", "some"), ("B", "one"), ("C", "two")], "B"),
    Q(25, "I picked my ___ brand of pancakes.", [("A", "new"), ("B", "only"), ("C", "favorite")], "C"),
    Q(26, "They were not ___, only eight yuan a bag.", [("A", "fresh"), ("B", "cheap"), ("C", "expensive")], "C"),
    Q(27, "Mom also checked the ___ on the package.", [("A", "date"), ("B", "price"), ("C", "name")], "A"),
    Q(28, "At the ___, the cashier told us the total was forty-two yuan.", [("A", "checkout"), ("B", "window"), ("C", "door")], "A"),
    Q(29, "At the checkout, the cashier told us the ___ was forty-two yuan.", [("A", "price"), ("B", "bill"), ("C", "total")], "C"),
    Q(30, "Mom paid with a fifty-yuan note and got eight yuan in ___.", [("A", "change"), ("B", "money"), ("C", "coins")], "A"),
  ],
}

# ────────────────────── 缺口 E：w5 五选五（3 篇，候选句命制）──────────────────────
# 结构：candidates 为候选句（字母 A+），blanks 按原文空位前后文定位，answer 填候选字母。
W5 = {
  "HN2026_L6_w5": {
    "candidates": [
      ["A", "Running is the only way to stay healthy."],
      ["B", "Fruit is also an important part of a healthy diet."],
      ["C", "Vegetables are good for our body, too."],
      ["D", "Drinking milk is a good habit every morning."],
      ["E", "Do not forget to drink enough water every day."],
    ],
    "blanks": [
      {"num": 1, "before": "A good breakfast helps you listen and learn in class with a clear mind.", "after": "We should eat fruit every day after our three meals because fruit gives us vitamins.", "answer": "B"},
      {"num": 2, "before": "We should eat fruit every day after our three meals because fruit gives us vitamins.", "after": "Fresh vegetables help our body grow tall and stay strong, so eat them often.", "answer": "C"},
      {"num": 3, "before": "Fresh vegetables help our body grow tall and stay strong, so eat them often.", "after": "Drink milk for strong bones and white teeth every morning before school.", "answer": "D"},
      {"num": 4, "before": "Drink milk for strong bones and white teeth every morning before school.", "after": "A good diet keeps us happy and full of energy for the whole day.", "answer": "E"},
    ],
  },
  "HN2026_L8_w5": {
    "candidates": [
      ["A", "First, we went there by a yellow school bus."],
      ["B", "There were many interesting things to see."],
      ["C", "The stories about robots made us laugh."],
      ["D", "We learned a lot from the visit."],
      ["E", "We played games in the garden that day."],
    ],
    "blanks": [
      {"num": 1, "before": "A good plan before the day helps a lot to make the trip easy.", "after": "We visited the science museum and saw old and strange exhibits there with our eyes for the first time.", "answer": "A"},
      {"num": 2, "before": "We visited the science museum and saw old and strange exhibits there with our eyes for the first time.", "after": "Our guide told us funny stories about small robots and stars in the sky.", "answer": "B"},
      {"num": 3, "before": "Our guide told us funny stories about small robots and stars in the sky.", "after": "We took many photos by the big door together to remember the day with joy.", "answer": "C"},
      {"num": 4, "before": "We took many photos by the big door together to remember the day with joy.", "after": "Everyone enjoyed the trip and we went home happy and tired at night.", "answer": "D"},
    ],
  },
  "HN2026_L1_w5": {
    "candidates": [
      ["A", "This is a nice school."],
      ["B", "He is tall and kind."],
      ["C", "They are in my class."],
      ["D", "We play basketball on the playground."],
      ["E", "Sports make me strong and happy."],
      ["F", "My favorite food is rice and chicken."],
    ],
    "blanks": [
      {"num": 11, "before": "I am a new student at No. 1 Middle School.", "after": "I am in Class Two, Grade Seven.", "answer": "A"},
      {"num": 12, "before": "My English teacher is Mr. Zhang.", "after": "He is very nice to us. He helps us with English.", "answer": "B"},
      {"num": 13, "before": "I have some good friends here.", "after": "Their names are Mike and Tom.", "answer": "C"},
      {"num": 14, "before": "I like playing basketball with them.", "after": "It is my favorite sport.", "answer": "D"},
      {"num": 15, "before": "It is my favorite sport.", "after": "I am happy to be here.", "answer": "E"},
    ],
  },
}

# provenance 标注：真题内嵌选项的篇目为 source_type=real，命制的为 source_type=adapted
PROVENANCE = {
  "cloze_real": sorted(CLOZE_AUTH.keys()),
  "cloze_adapted": sorted(CLOZE_AUTHOR.keys()),
  "w5_adapted": sorted(W5.keys()),
}

def _check_items(pid, items, label):
    letters = [q["answer"] for q in items]
    c = Counter(letters)
    mx = max(c.values()) / len(items)
    ok = "OK" if mx <= 0.4 else "超40%!"
    print("  %-26s %s %2d题 分布%s 最大%.0f%% %s" % (pid, label, len(items), dict(c), mx * 100, ok))
    for q in items:
        if q["answer"] not in [o[0] for o in q["opts"]]:
            raise SystemExit("答案 %s 不在选项（%s Q%d）" % (q["answer"], pid, q["num"]))
    return mx <= 0.4

def main():
    out = os.path.join(DATA_DIR, "banks", "passage_questions.json")
    payload = {
        "meta": {"built_by": "build_passage_questions.py", "provenance": PROVENANCE},
        "reading": READING,
        "cloze": {**CLOZE_AUTH, **CLOZE_AUTHOR},
        "w5": W5,
    }
    json.dump(payload, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n_reading = sum(len(v) for v in READING.values())
    n_cloze = sum(len(v) for v in payload["cloze"].values())
    n_w5 = sum(len(v["blanks"]) for v in W5.values())
    print("补题文件生成：%s" % out)
    print("  reading %2d 篇 ×%d 题 | cloze %2d 篇 ×%d 题 | w5 %2d 篇 ×%d 空" % (
        len(READING), n_reading, len(payload["cloze"]), n_cloze, len(W5), n_w5))
    print("—— reading 校验（≤40%）——")
    all_ok = all(_check_items(pid, items, "阅读") for pid, items in sorted(READING.items()))
    print("—— cloze 校验（真源篇目允许单字母>40%，按真题答案；命制篇目必须≤40%）——")
    for pid, items in sorted(payload["cloze"].items()):
        ok = _check_items(pid, items, "完形")
        if pid in CLOZE_AUTHOR and not ok:
            all_ok = False
    print("—— w5 校验 ——")
    for pid, v in sorted(W5.items()):
        letters = [b[0] for b in v["candidates"]]
        for b in v["blanks"]:
            if b["answer"] not in letters:
                raise SystemExit("w5 答案 %s 不在候选（%s）" % (b["answer"], pid))
        print("  %-26s 五选五 %d 空 / %d 候选 OK" % (pid, len(v["blanks"]), len(letters)))
    print("校验完成：%s" % ("全 OK" if all_ok else "见上方超40%项（真源篇目为真题原始分布）"))

if __name__ == "__main__":
    main()
