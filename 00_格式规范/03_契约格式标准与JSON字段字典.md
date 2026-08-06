# 英语黄金大师课程 · 契约规范标准与 JSON 字段字典 (02_CONTRACT_SPEC.md)

> **版本**：V7.0（2026-07-30 整合词汇教学与复习游戏综合规范：gameType扩展至29种、新增trainingObjective/promptLevel字段、vocabReviewPlan扩展miniTask/exitTicket/errorWordPool对象；2026-07-31 新增 dataCollectionPlan 数据采集配置对象）
> **归档位置**：`D:\workbuddy 工作空间\课件设计文档\02_契约规范标准与JSON字段字典.md`  
> **适用对象**：负责生成课件契约、HTML 网页 PPT 渲染及单元测试的所有 AI Agents。

---

## 第一章：单课契约 3 层架构标准

任何 Agent 在为某课时生成设计契约时，必须在其对应的 `第XX课/契约/` 目录下，生成以下 **6 份带序号的前缀标准文件**：

```
第XX课/
├── 契约/
│   ├── 1_课程概要.md        (教学元信息、语法公式、20去重新词表、阅读主题、防越级红线)
│   ├── 2_大纲脚本.md        (八段式流转：复习-新词-语法-演练-阅读-句子-拼读-总结 详细框架)
│   ├── 3_演讲意图.md        (逐页教师口语引导、视觉重音、互动指令与纠错提醒)
│   ├── 4_素材清单.md        (配色方案、组件需求、图标、音效与视觉卡片需求)
│   ├── 5_页面规划.json      (机器可读的 25~30 页 DOM 结构、组件类型、字号与布局字典)
│   └── 6_动效与素材.json    (机器可读的切换动效、高亮节点与音效槽位)
├── 课件成品_网页PPT/
│   └── 第XX课时_课件_档位.html
└── 第XX课时_配套练习_档位.docx
```

### 规约变更明细：
- ✓ 保留 `契约/` 子文件夹，与课件成品和练习卷物理隔离。
- ✕ 剔除 `交付清单.md` 与 `逐字稿.md`。
- ✓ 统一加上 `1_` 到 `6_` 序号前缀，物理顺序与逻辑顺序完美一致。

---

## 第二章：Markdown 契约规范标准

### 2.1 《1_课程概要.md》结构规范
包含 6 个必备板块：
1. **基础元数据**：课次、课名、学生、建议时长（90分钟）。
2. **语法硬契约**：必须明确给出“口诀 + 公式 + ≥3 例句”，并标注防越级校验结果。
3. **20 新词硬契约**：必须列出音标、中文、中考常考搭配，并标注与前课的去重校验。
4. **阅读指导硬契约**：篇章标题、词数、湖南中考源刊出处及“怎么指导”五步法。
5. **拼读/音标硬契约**：发音规则与典型例词。
6. **数据采集配置**：声明本课是否启用数据采集（IndexedDB）、同步方式（csv/local_tool/cloud_function）、题目 ID 前缀。详见 `08_学习数据闭环规范.md` 与下方 `dataCollectionPlan` Schema。

### 2.2 《2_大纲脚本.md》结构规范
严格按照 **"八段式"**（①复习/导入(从L2起2页：P1复习语法 + P2**跨课词汇复习游戏Tier2/3**) → ②新词20(5~6页：4页词卡教学 + **2页课内词汇复习游戏[1页Tier1词级 + 1页Tier2/3句篇级]**) → ③语法3考点(5~6页) → ④随堂演练(2页，P1须为**Mini Task综合表达任务**，P2常规练习) → ⑤阅读理解(2~3页) → ⑥句子练习(2~3页，插空造句与翻译) → ⑦自然拼读与拓展(3~4页：2页学习+1~2页练习，每页练习2~4题) → ⑧课堂总结(1页，须含**Exit Ticket退出检测**)）展开，课件总页数严格锁定在 **25 页 ~ 30 页之间**（彻底取消课后作业页），页面比例强制 21:9，逐页明确环节归属、展示内容与互动逻辑。高密度内容页可使用整页滚动机制（整个`.page`上下滚动，页码不变）。词汇复习游戏及词汇教学详细规范见 `07_词汇教学与复习游戏规范.md`，课件页面结构硬规则见 `01_课件格式规范.md` §3.7。


### 2.3 《3_演讲意图.md》结构规范
为渲染 Agent 或人类教师提供逐页的 `[视觉焦点]`、`[教师话术]` 与 `[学生可能错点与纠错]`，确保教学落地不空洞。

---

## 第三章：机器可读 JSON 字段字典规范

### 3.1 《5_页面规划.json》Schema 规范

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "LessonPagePlan",
  "type": "object",
  "required": ["lesson_id", "theme", "total_pages", "pages"],
  "properties": {
    "lesson_id": { "type": "string", "example": "第10课" },
    "theme": {
      "type": "object",
      "required": ["style", "primary_color", "accent_color", "font_size_base"],
      "properties": {
        "style": { "type": "string", "enum": ["Magazine Ink", "Classic Ink"] },
        "primary_color": { "type": "string", "example": "#2C3E50" },
        "accent_color": { "type": "string", "example": "#C0392B" },
        "font_size_base": { "type": "string", "example": "26pt" }
      }
    },
    "total_pages": { "type": "integer", "minimum": 25, "maximum": 30 },
    "pages": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["page_index", "section", "title", "layout_type", "components"],
        "properties": {
          "page_index": { "type": "integer", "minimum": 1, "maximum": 30 },
          "section": { "type": "string", "enum": ["复习导入", "新词20", "语法3考点", "随堂演练", "阅读理解", "句子练习", "自然拼读", "课堂总结"] },
          "title": { "type": "string" },
          "layout_type": { "type": "string", "enum": ["Cover", "Split-2", "Grid-4", "Formula-Card", "Reading-Passage", "Exercise-List", "Scrollable-List"] },
          "is_scrollable": { "type": "boolean", "default": true, "description": "整页滚动机制默认启用（V17.1）：整个.page支持上下滚动，无需单独标记" },
          "sub_content": {
            "type": "array",
            "description": "整页滚动内容块（V17.1：整页滚动机制下所有内容均在.page内顺序排列，此字段保留向后兼容）",
            "items": {
              "type": "object",
              "properties": {
                "sub_title": { "type": "string" },
                "components": { "type": "array" }
              }
            }
          },
          "components": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["type", "data"],
              "properties": {
                "type": { "type": "string", "enum": ["word-card", "formula-box", "example-line", "reading-passage", "exercise-item", "vocab-game"] },
                "data": { "type": "object" }
              }
            }
          },
          "vocabReviewTier": {
            "type": ["string", "null"],
            "enum": ["T1", "T2", "T3", null],
            "description": "词汇复习游戏层级：T1=词级, T2=句级, T3=篇章级。仅词汇复习游戏页填写，其他页为null"
          },
          "vocabReviewScope": {
            "type": ["string", "null"],
            "enum": ["in-lesson", "cross-lesson", null],
            "description": "复习范围：in-lesson=本课词汇, cross-lesson=上一课词汇。仅词汇复习游戏页填写"
          },
          "gameType": {
            "type": ["string", "null"],
            "enum": [
              "T1-A","T1-B","T1-C","T1-D","T1-E","T1-F","T1-G","T1-H","T1-I","T1-J",
              "T2-A","T2-B","T2-C","T2-D","T2-E","T2-F","T2-G","T2-H","T2-I",
              "T3-A","T3-B","T3-C","T3-D","T3-E","T3-F","T3-G","T3-H","T3-I","T3-J",
              null
            ],
            "description": "游戏类型编号，对应29种游戏（见07_词汇教学与复习游戏规范.md 第十三章）"
          },
          "trainingObjective": {
            "type": ["string", "null"],
            "enum": ["REC", "RET", "SPL", "COL", "CTX", "EXP", null],
            "description": "训练目标：REC=词义识别, RET=主动提取, SPL=拼写/词形, COL=词块搭配, CTX=语境应用, EXP=综合表达。仅游戏页填写"
          },
          "promptLevel": {
            "type": ["integer", "null"],
            "minimum": 1,
            "maximum": 8,
            "description": "提示梯度等级(1-8)：L1=图片+首字母+选项 ... L8=新情境中使用。仅游戏页填写"
          },
          "contextType": {
            "type": ["string", "null"],
            "enum": ["word", "sentence", "dialogue", "passage", "scenario", null],
            "description": "语境类型：word=孤词, sentence=句子, dialogue=对话, passage=语篇, scenario=情景"
          }
        }
      }
    },
    "vocabReviewPlan": {
      "type": "object",
      "description": "词汇复习游戏总体规划（见07_词汇教学与复习游戏规范.md）",
      "properties": {
        "inLessonGames": {
          "type": "array",
          "description": "课内词汇复习游戏（2个：1个Tier1词级 + 1个Tier2/3句篇级）",
          "items": {
            "type": "object",
            "properties": {
              "pageIndex": { "type": "integer" },
              "tier": { "type": "string", "enum": ["T1", "T2", "T3"] },
              "gameType": { "type": "string" },
              "trainingObjective": { "type": "string", "enum": ["REC", "RET", "SPL", "COL", "CTX", "EXP"] },
              "promptLevel": { "type": "integer", "minimum": 1, "maximum": 8 },
              "wordCount": { "type": "integer" }
            }
          }
        },
        "crossLessonGame": {
          "type": "object",
          "description": "跨课词汇复习游戏（1个，Tier2或Tier3，复习上一课词汇）",
          "properties": {
            "pageIndex": { "type": "integer" },
            "tier": { "type": "string", "enum": ["T2", "T3"] },
            "gameType": { "type": "string" },
            "trainingObjective": { "type": "string", "enum": ["CTX", "EXP"] },
            "promptLevel": { "type": "integer", "minimum": 1, "maximum": 8 },
            "reviewLessonId": { "type": "string" },
            "wordCount": { "type": "integer" }
          }
        },
        "miniTask": {
          "type": "object",
          "description": "Mini Task综合表达任务（落位④随堂演练P1，详见07_词汇教学与复习游戏规范.md 第十章）",
          "properties": {
            "pageIndex": { "type": "integer" },
            "taskContext": { "type": "string", "description": "任务情境" },
            "communicationGoal": { "type": "string", "description": "交际目标" },
            "requiredWords": { "type": "array", "items": { "type": "string" }, "description": "必用词清单" },
            "sentenceStarter": { "type": "string", "description": "句型支架" },
            "completionCriteria": { "type": "string", "description": "完成标准" }
          }
        },
        "exitTicket": {
          "type": "object",
          "description": "Exit Ticket退出检测（落位⑧课堂总结，详见07_词汇教学与复习游戏规范.md 第二十五章）",
          "properties": {
            "pageIndex": { "type": "integer" },
            "questionCount": { "type": "integer", "description": "题量：基础4/中等5/培优6" },
            "recQuestions": { "type": "integer", "description": "词义识别题数" },
            "retQuestions": { "type": "integer", "description": "主动提取题数" },
            "expQuestions": { "type": "integer", "description": "表达任务数" },
            "hasSelfAssessment": { "type": "boolean", "description": "是否含学生自评（培优级必含）" }
          }
        },
        "errorWordPool": {
          "type": "object",
          "description": "错词ABCD分类与滚动复习池（详见07_词汇教学与复习游戏规范.md 第十八、二十三章）",
          "properties": {
            "recentRatio": { "type": "integer", "description": "近期词比例%（基础60/中等50/培优40）" },
            "errorRatio": { "type": "integer", "description": "易错词比例%（基础30/中等30/培优35）" },
            "longTermRatio": { "type": "integer", "description": "长期词比例%（基础10/中等20/培优25）" },
            "classificationDepth": { "type": "string", "enum": ["AB-focus", "full-C-short", "full-D-page"], "description": "ABCD分类处理深度" }
          }
        }
      }
    },
    "dataCollectionPlan": {
      "type": "object",
      "description": "课件数据采集配置，详见08_学习数据闭环规范.md",
      "properties": {
        "enabled": { "type": "boolean", "description": "是否启用IndexedDB数据采集" },
        "syncMode": { "type": "string", "enum": ["csv", "local_tool", "cloud_function"], "description": "同步方式" },
        "exportFormats": { "type": "array", "items": { "type": "string", "enum": ["json", "csv"] } },
        "questionIdPrefix": { "type": "string", "description": "题目ID前缀，如L03_VOC" },
        "sessionIdRule": { "type": "string", "description": "会话ID生成规则" },
        "recordFirstAttemptOnly": { "type": "boolean", "description": "测试模式是否只记录首次答案" },
        "allowReview": { "type": "boolean", "description": "是否允许历史回看" }
      }
    }
  }
}
```

### 3.2 《6_动效与素材.json》Schema 规范

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "AnimationAndAssetPlan",
  "type": "object",
  "required": ["lesson_id", "animation_engine", "page_animations"],
  "properties": {
    "lesson_id": { "type": "string", "example": "第10课" },
    "animation_engine": { "type": "string", "enum": ["Motion One", "GSAP Core"] },
    "page_animations": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["page_index", "transition_in", "stagger_elements"],
        "properties": {
          "page_index": { "type": "integer" },
          "transition_in": { "type": "string", "example": "fade_slide_up 0.5s ease-out" },
          "stagger_elements": {
            "type": "array",
            "items": {
              "type": "object",
              "properties": {
                "selector": { "type": "string", "example": ".word-card" },
                "delay_ms": { "type": "integer", "example": 100 },
                "effect": { "type": "string", "example": "scale_up 0.3s" }
              }
            }
          }
        }
      }
    }
  }
}
```

---
*本规范文档归档于 `D:\workbuddy 工作空间\课件设计文档\02_契约规范标准与JSON字段字典.md`。*
