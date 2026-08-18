# 任务三：`passage_bank.json`安全合并说明

## 一、文件

- 源数据：`任务三_w5五选四题目补全_2026-08-04.json`
- 合并脚本：`safe_merge_passage_bank.py`
- 校验报告：`任务三_入库前严格校验报告_2026-08-04.md`

脚本只使用Python标准库，不依赖npm、pip或第三方库。

## 二、支持的目标结构

脚本只接受以下两种`passage_bank.json`结构：

### 结构A：根数组

```json
[
  {"id": "..."}
]
```

### 结构B：对象中的`passages`数组

```json
{
  "passages": [
    {"id": "..."}
  ]
}
```

遇到其他结构时会停止，不写入。

## 三、先做JSON语法检查

Windows PowerShell或终端：

```bash
python -m json.tool "任务三_w5五选四题目补全_2026-08-04.json" > NUL
```

macOS/Linux：

```bash
python -m json.tool "任务三_w5五选四题目补全_2026-08-04.json" > /dev/null
```

## 四、默认只演练

在项目根目录执行：

```bash
python safe_merge_passage_bank.py ^
  --source "任务三_w5五选四题目补全_2026-08-04.json" ^
  --target "00_工具\passage_bank.json"
```

PowerShell也可写成一行：

```powershell
python .\safe_merge_passage_bank.py --source ".\任务三_w5五选四题目补全_2026-08-04.json" --target ".\00_工具\passage_bank.json"
```

没有`--apply`时，脚本：

- 解析并校验源JSON；
- 校验三个固定ID；
- 检查目标根结构；
- 检查目标库重复ID；
- 输出拟增加、替换或跳过数量；
- 不修改目标文件。

## 五、实际写入

确认演练通过后：

```powershell
python .\safe_merge_passage_bank.py --source ".\任务三_w5五选四题目补全_2026-08-04.json" --target ".\00_工具\passage_bank.json" --apply
```

默认重复策略是`abort`。目标库已存在任何一个相同ID时，脚本会停止。

人工确认需要覆盖后，才可使用：

```powershell
python .\safe_merge_passage_bank.py --source ".\任务三_w5五选四题目补全_2026-08-04.json" --target ".\00_工具\passage_bank.json" --on-duplicate replace --apply
```

不建议在未逐字比对时使用`replace`。

## 六、安全措施

实际写入前，脚本会：

1. 计算目标SHA-256；
2. 生成带时间戳的`.bak_YYYYMMDD_HHMMSS`备份；
3. 检查备份哈希；
4. 写入同目录临时文件；
5. 重新解析临时JSON；
6. 使用`os.replace()`替换目标文件；
7. 重新读取目标文件；
8. 确认三个目标ID全部存在。

## 七、本地Agent必须补做的逐字检查

由于当前会话环境无法再次解压最初任务包，执行方在正式合并前应：

```text
原任务包三篇源文
↕ 逐字diff
任务三JSON中的passage_with_blanks
```

允许差异只应包括任务包明确授权的空位规范化，以及L1移除原空15占位符。发现其他正文、标点或单词差异时，停止合并并报告。
