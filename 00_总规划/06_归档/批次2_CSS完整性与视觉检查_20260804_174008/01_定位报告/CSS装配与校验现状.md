# CSS 装配与校验现状（执行前定位报告）

> 生成日期：2026-08-04
> 用途：批次2 执行前审计，确认当前 CSS 装配路径、校验覆盖范围与事故边界

## 1. verify_v2.py 入口与返回码逻辑

- **入口**：`check_one(path)` 接收 HTML 路径，读取文件、解析契约、逐项检查。
- **返回码**：`all(hard)` 决定 PASS/FAIL；仅硬检查（体积/页数/div/残留/JS/答案可判/答案分布）参与 hard 列表；性能软检查、兼容检查、六色卡、防越级仅 WARN 不 FAIL。
- **CLI**：`python verify_v2.py <html_path> [...]`，汇总 `sum(results)/n`，`sys.exit(0 if all(results) else 1)`。

## 2. 现有硬校验函数与行号

| 检查 | 行号 | 类型 | 阈值 |
|------|------|------|------|
| 体积 | 127-135 | hard | page-id≥153600B |
| 页数 | 137-147 | hard | page-id 40-45 |
| div 平衡 | 148 | hard | opens==closes |
| 残留框架 | 149 | hard | 5 个已知残余词均为 0 |
| JS 语法 | 96-103 | hard | node --check 返回 0 |
| 答案可判 | 152-157 | hard | page-id 须有 quiz-opt 标签 |
| 答案分布 | 158 | hard | 最大占比≤40% |
| 六色卡 | 160-161 | soft | 仅统计，≥4 色 OK |
| 防越级 | 162 | soft | 扫描 FORBIDDEN 词 |
| 性能软检查 | 164-180 | soft | 无限动画/backdrop/will-change 等 |
| 兼容检查 | 181-188 | soft | checkOpt(event) 旧调用 |

## 3. CORE_CSS 进入最终 HTML 的路径

`courseware_core.py:64`——`<style>\n' + CORE_CSS + '\n' + (css_extra or "") + '\n</style>`
CORE_CSS 是 courseware_core.py 顶部的字符串常量，函数外定义，约 50KB。**不可修改**（红线）。

## 4. CSS_EXTRA 的定义、拼接与进入路径

**定义位置**（`courseware_engine.py`）：

| 行号 | 操作 | 内容 |
|------|------|------|
| 26 | `CSS_EXTRA = g.CSS_EXTRA` | 从 `gen_l1_l13_v2.py` 导入基线（~15KB，section-head/kp-grid/rule-card 等） |
| 209 | `CSS_EXTRA += r"""..."""` | 设计系统层 v2（字号/玻璃/动效，~11KB） |
| 595 | `CSS_EXTRA += C.COMPONENT3_CSS` | C3 组件样式（GM-V02/G03/R06，~2KB） |
| 597 | `CSS_EXTRA += r"""..."""` | X26 视觉层（实体卡/触屏态/减弱动画，~8KB） |

**最终拼接**（line 1913）：`css_extra=CSS_EXTRA + build_theme_css(...)`，传入 `build_courseware`。

## 5. 多主题 CSS 与组件 CSS

- `theme_css` = `build_theme_css(vocab_theme)` 来自 `theme_colors.py`（~0.5KB，`:root` 变量覆盖+`.page` 背景色）。
- `COMPONENT3_CSS` 来自 `components.py`（3 组件样式）。
- 整体 CSS 在 HTML 中合并为单个 `<style>` 块（CORE_CSS + CSS_EXTRA + theme_css）。

## 6. page-id 与 slide 契约识别

`detect_contract()` 判断逻辑：
- `id="pageN"` 且 `quiz-opt data-correct` 或 `checkOpt` → **page-id**
- `class="slide"` 且 `checkQuiz` 或 `data-correct` → **slide**
- 否则 → **unknown**

## 7. 当前课件视觉标记

**无**。`test_L5_courseware.html`（引擎生成测试件）和所有已交付课件均无 `CW-VISUAL-CONTRACT:1` 或 `<!-- CW-CSS-EXTRA -->` 标记。本批次新增。

## 8. 测试目录与样本生成命令

- 无独立测试目录。
- 引擎生成：`python courseware_engine.py` → `test_L5_courseware.html`。
- 回归样本：`verify_v2.py <html>` 直接运行。

## 9. `.rule-card` 重复选择器

`CSS_EXTRA` 中 `.rule-card` 定义位置：
- 基线（`gen_l1_l13_v2.py`）：一次定义（六色卡网格布局）。
- X26 视觉层（line 597+）：可能存在 `.rule-card` 的覆盖或补充声明。

## 10. 现有视觉检查函数

**无**。`check_one()` 内有性能软检查（无限动画/backdrop/will-change/prefers-reduced-motion/THEME），但无 CSS 完整性检查或视觉样式检查。

## 11. 事故边界

L26 重做版当前（2026-08-04 交付版本）视觉层完好：style 块 103KB、1467 选择器、六色卡 6/6。旧件（`_旧件_20260804重做`）同样完好。事故描述中的"视觉层被删"状态在当前交付件上未复现，可能事故已修复。本批次新增的 CSS 完整性检查通过**构造模拟样本**验证拦截能力。