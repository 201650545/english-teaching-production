# 任务包三：w5 五选四语篇库题目补全（给 Traework）

**执行方**：Traework（综合能力/实时信息强）
**发起方**：郭老师（人工中继）｜上下文打包：Claude
**日期**：2026-08-04
**性质**：纯题目生成任务，语篇已存在、一个词不改。目标是把 `passage_bank.json` 里 3 篇 w5 母本的 `"questions": []`（当前标"题目待生成"）补成标准**五选四**题目组。所有输入都在本文档内，你不需访问任何文件。

---

## 0. 背景（30 秒读懂）

初中英语课件生产项目（人教版衔接）。`passage_bank.json` 是**真题母本语篇库**：每篇语篇来自真实中考试卷素材（溯源 ID 必填），红线是**语篇仅真题母本改编，禁编造**。其中 3 篇 `w5`（五选四）母本正文已经齐全，只差题目（4 个空位 + 5 个选项句 + 答案 + 解析）。你的任务就是把这 3 篇的题目补全，输出可直接合并入库的 JSON。**语篇正文本身你不许动一个字**——你只处理"空位选在哪、选项句、答案、解析"。

**卷面规格**：阅读 C · 五选四 = 4 个空，从 A–E 五个句子中选最佳句填入（其中 1 句是多余项）。

---

## 1. 目标：3 篇待补题目

| 库 ID | 文体 | 难度 | 词数 | 生词率 | 现状 |
|---|---|---|---|---|---|
| `HN2026_L1_w5` | 记叙文 | 中 | 87 | 15% | 正文已嵌 **5 个空**（`___11___`—`___15___`，五选五遗留格式） |
| `HN2026_L6_w5` | 说明文 | 中 | 107 | 19% | 正文已嵌 **4 个空**（裸 `___`），一组可用题目已存在（见 §4 范例） |
| `HN2026_L8_w5` | 记叙文 | 中 | 132 | 26% | 正文已嵌 **4 个空**（裸 `___`） |

---

## 2. 硬规则（红线，违反即废）

1. **语篇正文一字不改**：只确定空位/给空编号，不增删改正文单词、标点、句子。
2. 每篇产出一组**标准五选四**：**恰好 4 个空** + **5 个选项句（A–E）** + **答案映射** + **1 个多余项** + **逐空解析**。
3. **选项句必须来自语篇内的真实句子**：可直接用原句，或对原句做最小改写（改人称/时态/同义替换）使其贴合一空。**多余项**可仿语篇主题编写（语义通顺、"好像对但其实放哪都不成立"），但**不得引入语篇没有的新知识点**。
4. **空位必须落在逻辑衔接点**：前后句代词指代（It/They/He/This）、连接词（because/so/but/then/also）、总分或总结过渡。每空测试**一个明确衔接关系**。
5. 逐空解析必写：一句话说明呼应依据（如"11→A：fruit 与 vitamins 呼应"）。
6. **L1 特殊**：源正文嵌了 5 个空（五选五遗留），五选四只需 4 个——你要**明确说明删/并了哪一空及理由**（建议删信息量最低的空；正文本身仍不改字）。
7. 选项顺序要**打乱**，避免正确答案连续同字母；正确项与多余项要有区分度。
8. 难度控制在易—中，生词不超出该篇标注生词率水平。

---

## 3. 输入：3 篇语篇正文（逐字，禁止改动）

### 3.1 HN2026_L1_w5（记叙文 · 5 个现成空）

> Hello, everyone! My name is David. I am a new student at No. 1 Middle School. ___11___ I am in Class Two, Grade Seven. My English teacher is Mr. Zhang. ___12___ He is very nice to us. He helps us with English. I have some good friends here. ___13___ Their names are Mike and Tom. We often play together after class. I like playing basketball with them. ___14___ It is my favorite sport. ___15___ I am happy to be here. I like my school, my teachers and my classmates. Welcome to my school!

（空位位置说明：11 在"school."后，12 在"Mr. Zhang."后，13 在"friends here."后，14 在"with them."后，15 在句首"___15___ I am happy to be here."。五选四请保留其中 4 个、说明删/并哪个。）

### 3.2 HN2026_L6_w5（说明文 · 4 个裸空）

> Eating healthy food is important for every student at school. Good food is the fuel for your body and your brain. A good breakfast helps you listen and learn in class with a clear mind. ___ We should eat fruit every day after our three meals because fruit gives us vitamins. ___ Fresh vegetables help our body grow tall and stay strong, so eat them often. ___ Drink milk for strong bones and white teeth every morning before school. ___ A good diet keeps us happy and full of energy for the whole day. Eat well, drink water often and move every day for a healthy life that you will love!

### 3.3 HN2026_L8_w5（记叙文 · 4 个裸空）

> We went on a school trip last month and it was a lot of fun for the whole class. A good plan before the day helps a lot to make the trip easy. ___ We visited the science museum and saw old and strange exhibits there with our eyes for the first time. ___ Our guide told us funny stories about small robots and stars in the sky. ___ We took many photos by the big door together to remember the day with joy. ___ Everyone enjoyed the trip and we went home happy and tired at night. The bus was yellow and clean, and the weather was fine and bright. We learned new things and made new friends on the way all together. Next time we want to go there again with the same smile!

---

## 4. 范例：L6 已存在的一组五选四（邓兴华 L06 课件在用，以此为标准质量与格式）

**正文嵌空方式**：`A good breakfast helps you listen and learn in class with a clear mind. __(11)__ We should eat fruit ... __(12)__ Fresh vegetables ... __(13)__ Drink milk ... __(14)__ A good diet keeps us happy and full of energy for the whole day.`

**选项**：
- A. Fruit gives us vitamins.
- B. We also need water every day.
- C. Candy is bad for our teeth.
- D. Exercise is good for us, too.
- E. Cola is a good drink for health.

**答案**：11→A，12→B，13→D，14→C；**多余项 E**。

**解析**：11→A（fruit 与 vitamins 呼应）；12→B（water 与 drink 呼应）；13→D（exercise 与 body 呼应）；14→C（candy 与 teeth 呼应）；E 为多余项，五选四。

> 质量要点：A、B、D、C 均来自语篇原句或近义改写（Fruit gives us vitamins / drink water often / move every day / white teeth）；E 仿主题写、语法通顺但语义放任何一空都不成立；每空解析一句话说清呼应词。

---

## 5. 五选四出题 SOP（按此操作）

1. **通读语篇**，标出所有可作为空位的逻辑衔接点（指代衔接 / 连接词衔接 / 总分衔接），每篇至少备选 5 处，从中选 4 个。
2. **空位错开**：4 个空分散全文，不要挤在开头；每空衔接类型尽量不重复。
3. **确定正确句**：每个空位的正确句 = 语篇内原句或其最小改写。
4. **写多余项**：仿语篇主题编一句"语义可能但放哪都不成立"的句子；或把语篇某句改写使其与上下文冲突。
5. **打乱选项顺序**，检查无连续同字母正确答案。
6. **写解析**：每空一句话，点出呼应词/指代对象/连接关系。

---

## 6. 输出格式（每篇一个 JSON 块，可直接合并入库）

```json
{
  "id": "HN2026_L6_w5",
  "passage_with_blanks": "正文全文，空位统一标为 __(11)__ ～ __(14)__，其余一字不动",
  "options": [["A", "选项句"], ["B", "选项句"], ["C", "选项句"], ["D", "选项句"], ["E", "选项句"]],
  "answers": {"11": "A", "12": "B", "13": "D", "14": "C"},
  "extra": "E",
  "rationale": {"11": "fruit 与 vitamins 呼应", "12": "water 与 drink 呼应", "13": "exercise 与 body 呼应", "14": "candy 与 teeth 呼应"},
  "note": "L1：删除/合并了空 X（理由…）；L6/L8：沿用原空位。"
}
```

**硬要求**：
- 3 篇各出一块，共 3 块；`passage_with_blanks` 字段必须能与 §3 原正文逐字核对（只许把空位从裸 `___` 或 `___11___` 规整为 `__(11)__` 编号，不许动任何单词）。
- `answers` 的每个键必须与 `passage_with_blanks` 里的空编号一一对应。
- `extra` 必须与 `answers` 的任何值都不重复。
- 每篇给 1 句"自检说明"：确认正文未改动、4 空衔接类型各是什么。

---

## 7. 通用规则

1. 每条结论给依据：解析必写呼应词；查不到/拿不准的标"待确认"，不编造。
2. 不引入语篇外新知识点；不把语篇正文当成自己可以改写的东西。
3. 输出纯 JSON（无多余散文），能被发起方直接合并进 `passage_bank.json` 并重新生成课件。
