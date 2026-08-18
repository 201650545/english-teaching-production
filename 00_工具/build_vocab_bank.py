# -*- coding: utf-8 -*-
"""M2 词汇库构建：L1-L4已用词(从生成器提取) + 主题候选池 → vocab_bank.json + used_vocab.json"""
import json
DATA_DIR = "D:/英语教学/01_数据"

import gen_l1_l13_v2 as g

def tuples_to_words(tuples_, lesson, theme):
    out = []
    for t in tuples_:
        en, phon, pos, cn, coll, ex, hook = t
        out.append({"en": en, "phonetic": phon, "pos": pos, "cn": cn,
                    "collocation": coll, "example": ex, "hook": hook,
                    "theme": theme, "used_by_lesson": lesson, "frequency": "high"})
    return out

# L1-L4 已用词（保持与已交付课件一致）
bank = []
bank += tuples_to_words(g.VOCAB_L1, 1, "school")
bank += tuples_to_words(g.VOCAB_L2, 2, "family")
bank += tuples_to_words(g.VOCAB_L3, 3, "school_things")
bank += tuples_to_words(g.VOCAB_L4, 4, "room")

# ---- 主题候选池（未被任何课使用） ----
FOOD = [
    ("food","/fuːd/","n.","食物","a lot of food","I like Chinese food.","oo 长音/uː/"),
    ("drink","/drɪŋk/","v./n.","喝；饮料","drink water","I drink milk every day.","dr 连缀"),
    ("rice","/raɪs/","n.","米饭","a bowl of rice","Rice is nice.","i 发/aɪ/"),
    ("noodle","/ˈnuːdl/","n.","面条","a bowl of noodles","I eat noodles for lunch.","常用复数 noodles"),
    ("egg","/eɡ/","n.","鸡蛋","an egg","I have an egg for breakfast.","e 短音/e/"),
    ("milk","/mɪlk/","n.","牛奶","a glass of milk","Milk is white.","i 短音/ɪ/"),
    ("bread","/bred/","n.","面包","a piece of bread","The bread is soft.","ea 发/e/"),
    ("apple","/ˈæpl/","n.","苹果","an apple a day","An apple a day is good.","a 发/æ/"),
    ("banana","/bəˈnɑːnə/","n.","香蕉","a yellow banana","The banana is sweet.","三个 a 发音不同"),
    ("orange","/ˈɒrɪndʒ/","n.","橙子","an orange","The orange is juicy.","o 短音/ɒ/"),
    ("water","/ˈwɔːtə/","n.","水","drink water","Water is important.","a 发/ɔː/"),
    ("juice","/dʒuːs/","n.","果汁","orange juice","I like apple juice.","ui 发/uː/"),
    ("vegetable","/ˈvedʒtəbl/","n.","蔬菜","eat vegetables","Vegetables are healthy.","veg+etable"),
    ("fruit","/fruːt/","n.","水果","fresh fruit","Fruit is sweet.","ui 发/uː/"),
    ("meat","/miːt/","n.","肉","eat meat","I don't eat much meat.","ea 长音/iː/"),
    ("fish","/fɪʃ/","n.","鱼","eat fish","Fish is good for you.","sh 发/ʃ/"),
    ("chicken","/ˈtʃɪkɪn/","n.","鸡肉","some chicken","The chicken is nice.","ch 发/tʃ/"),
    ("breakfast","/ˈbrekfəst/","n.","早餐","have breakfast","I have breakfast at 7.","break+fast"),
    ("lunch","/lʌntʃ/","n.","午餐","have lunch","Lunch is at twelve.","u 发/ʌ/"),
    ("dinner","/ˈdɪnə/","n.","晚餐","have dinner","We have dinner together.","din+ner"),
    ("hungry","/ˈhʌŋɡri/","adj.","饥饿的","be hungry","I am hungry now.","hung+ry"),
    ("thirsty","/ˈθɜːsti/","adj.","口渴的","be thirsty","She is thirsty.","th 咬舌"),
    ("eat","/iːt/","v.","吃","eat well","Eat breakfast every day.","ea 长音/iː/"),
    ("tea","/tiː/","n.","茶","a cup of tea","My grandpa likes tea.","ea 长音/iː/"),
    ("cake","/keɪk/","n.","蛋糕","a birthday cake","The cake is sweet.","a_e 魔法e"),
    ("soup","/suːp/","n.","汤","hot soup","The soup is hot.","ou 发/uː/"),
    ("salad","/ˈsæləd/","n.","沙拉","fruit salad","I like fruit salad.","a 发/æ/"),
    ("hamburger","/ˈhæmbɜːɡə/","n.","汉堡包","a hamburger","The hamburger is big.","ham+burger"),
    ("dessert","/dɪˈzɜːt/","n.","甜点","for dessert","Ice cream is a dessert.","双写 s"),
]
MEALS = [
    ("porridge","/ˈpɒrɪdʒ/","n.","粥","a bowl of porridge","I have porridge for breakfast.","por+ridge"),
    ("dumpling","/ˈdʌmplɪŋ/","n.","饺子","eat dumplings","We eat dumplings at festivals.","dump+ling"),
    ("pancake","/ˈpænkeɪk/","n.","薄饼","make pancakes","Mom makes pancakes.","pan+cake"),
    ("sandwich","/ˈsænwɪtʃ/","n.","三明治","a sandwich","I have a sandwich for lunch.","sand+wich"),
    ("cookie","/ˈkʊki/","n.","曲奇","a cookie","The cookie is sweet.","ook 短音/ʊ/"),
    ("candy","/ˈkændi/","n.","糖果","some candy","Don't eat too much candy.","can+dy"),
    ("chocolate","/ˈtʃɒklət/","n.","巧克力","like chocolate","She likes chocolate.","choco+late"),
    ("cheese","/tʃiːz/","n.","奶酪","some cheese","Cheese is yellow.","ee 长音/iː/"),
    ("butter","/ˈbʌtə/","n.","黄油","bread and butter","Butter is on the bread.","but+ter"),
    ("sugar","/ˈʃʊɡə/","n.","糖","some sugar","Don't add too much sugar.","s 发/ʃ/"),
    ("salt","/sɔːlt/","n.","盐","a little salt","The soup needs salt.","al 发/ɔː/"),
    ("pepper","/ˈpepə/","n.","胡椒","salt and pepper","Pepper is hot.","pp 双写"),
    ("oil","/ɔɪl/","n.","油","cooking oil","Mom cooks with oil.","oi 发/ɔɪ/"),
    ("flour","/ˈflaʊə/","n.","面粉","some flour","We make bread with flour.","fl 连缀"),
    ("honey","/ˈhʌni/","n.","蜂蜜","sweet honey","Honey is sweet.","hon+ey"),
    ("jam","/dʒæm/","n.","果酱","strawberry jam","I like jam on bread.","j 发/dʒ/"),
    ("sausage","/ˈsɒsɪdʒ/","n.","香肠","a sausage","The sausage is hot.","sau+sage"),
    ("bean","/biːn/","n.","豆","green beans","Beans are healthy.","ea 长音/iː/"),
    ("potato","/pəˈteɪtə/","n.","土豆","a potato","Potatoes are nice.","复数 potatoes"),
    ("tomato","/təˈmɑːtəʊ/","n.","西红柿","a tomato","The tomato is red.","复数 tomatoes"),
]
ACTIONS = [
    ("want","/wɒnt/","v.","想要","want to eat","I want some rice.","a 发/ɒ/"),
    ("need","/niːd/","v.","需要","need water","Plants need water.","ee 长音/iː/"),
    ("help","/help/","v.","帮助","help mom","I help mom cook.","e 短音/e/"),
    ("give","/ɡɪv/","v.","给","give me","Give me some water.","i 短音/ɪ/"),
    ("take","/teɪk/","v.","拿；带走","take away","Take an apple with you.","a_e 魔法e"),
    ("make","/meɪk/","v.","制作","make food","Mom makes dinner.","a_e 魔法e"),
    ("cook","/kʊk/","v./n.","烹饪；厨师","cook dinner","Dad cooks well.","oo 短音/ʊ/"),
    ("taste","/teɪst/","v./n.","尝；味道","taste good","The soup tastes good.","a_e 魔法e"),
    ("smell","/smel/","v./n.","闻；气味","smell nice","The bread smells nice.","e 短音/e/"),
    ("share","/ʃeə/","v.","分享","share food","We share the cake.","sh 发/ʃ/"),
    ("order","/ˈɔːdə/","v./n.","点餐；命令","order food","We order noodles.","or 发/ɔː/"),
    ("serve","/sɜːv/","v.","上菜；服务","serve dinner","They serve lunch at 12.","er 发/ɜː/"),
    ("wash","/wɒʃ/","v.","洗","wash hands","Wash hands before meals.","sh 发/ʃ/"),
    ("cut","/kʌt/","v.","切","cut the cake","Cut the apple, please.","u 发/ʌ/"),
    ("put","/pʊt/","v.","放","put on the table","Put the eggs here.","u 短音/ʊ/"),
    ("keep","/kiːp/","v.","保持","keep fresh","Keep the milk cold.","ee 长音/iː/"),
    ("grow","/ɡrəʊ/","v.","种植；生长","grow vegetables","We grow tomatoes.","ow 发/əʊ/"),
    ("pick","/pɪk/","v.","摘；捡","pick apples","We pick apples in autumn.","i 短音/ɪ/"),
    ("sell","/sel/","v.","卖","sell fruit","They sell oranges.","e 短音/e/"),
    ("buy","/baɪ/","v.","买","buy food","Mom buys vegetables.","uy 发/aɪ/"),
]

POOLS = {"food": FOOD, "meals": MEALS, "actions": ACTIONS}
for theme, pool in POOLS.items():
    bank += tuples_to_words(pool, None, theme)

json.dump({"words": bank}, open(os.path.join(DATA_DIR, "banks", "vocab_bank.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

used = {}
for n in (1, 2, 3, 4):
    used[str(n)] = [t[0] for t in getattr(g, "VOCAB_L%d" % n)]
all_used = [w for lst in used.values() for w in lst]
json.dump({"used": used, "all": all_used}, open(os.path.join(DATA_DIR, "content", "used_vocab.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=1)

# 防呆：候选池与已用词零重叠校验
pool_words = [t[0] for pool in POOLS.values() for t in pool]
overlap = set(pool_words) & set(all_used)
print("bank total:", len(bank), "| used:", len(all_used), "| pool:", len(pool_words), "| overlap:", overlap or "无")
