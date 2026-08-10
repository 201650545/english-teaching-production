# archive_scripts — 归档的一次性课时脚本

> 归档日期：2026-08-10（P1-1 脚本收口）

## 为什么归档

`00_工具/` 曾积累 30+ 个"一生一课一脚本"（`build_lesson_*`、`build_practice_*`、
`build_xyj_*`、`build_lmx_*`、`gen_contracts_*` 等），每个脚本内嵌读 JSON、课时
专属转换、拼装逻辑，与既有引擎（`courseware_engine.py` / `docx_engine.py` /
`build_practice_paper.py` / `components.py`）的引擎化目标矛盾，且持续增殖。

P1-1 起：**禁止新增按学生/课时命名的一次性构建脚本**（见
`00_格式规范/00_全局约束与红线.md` 红线条款）。新课时只允许：

1. 产出已拼装的内容 JSON（引擎契约形态：`{card, content}`）；
2. 调用统一入口 `00_工具/build/build_practice.py`（练习）渲染输出。

## 归档内容（31 个）

课时专属的课件/练习/契约生成器与旧 `.py` 内容文件，代码完整保留、不删除。
存量课时如需重出，优先用统一入口 + 已拼装 JSON；确需复用旧脚本逻辑时，从本
目录恢复运行即可。

> 说明：`gen_l1_l13_v2.py` 原在归档清单内，因被 `engine/courseware_engine.py`
> 依赖（L4 复习数据源）而移回 `00_工具/engine/`，不属于归档。

## 可运行性说明

归档脚本原按 `HERE = 脚本自身目录` 解析共享模块/数据（引擎、题库 JSON 均位于
`00_工具/` 顶层）。移入本目录后，直接运行会找不到位于上一级目录的依赖。
如需运行，二选一：

- 将脚本临时拷回 `00_工具/` 顶层运行（依赖与数据路径即刻可用）；
- 或把脚本内的 `HERE = os.path.dirname(os.path.abspath(__file__))`
  改为 `HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))`
  （解析到上一级 `00_工具/`）。

前向路径是统一入口，归档脚本不再维护。
