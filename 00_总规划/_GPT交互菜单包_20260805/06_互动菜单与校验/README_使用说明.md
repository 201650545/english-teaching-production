# 交互形式菜单与选择题转化｜使用说明

## 文件

- `交互形式菜单与选择题转化_研究答复_2026-08-05.md`
- `interaction_menu_v1.json`
- `interaction_rotation_v1.py`
- `verify_interaction_v1.py`
- `conversion_examples_v1.json`
- `rotation_request_example.json`
- `rotation_output_example.json`
- `test_verify_interaction_v1.py`
- `TEST_RESULTS.txt`
- `MANIFEST_SHA256.txt`

## 轮换示例

```bash
python interaction_rotation_v1.py   --menu interaction_menu_v1.json   --request rotation_request_example.json
```

## 校验示例

```bash
python verify_interaction_v1.py 第10课时_课件.html --level medium
```

## 测试

```bash
python -m unittest test_verify_interaction_v1.py
```

## 边界

参考脚本不能直接覆盖本地最新`courseware_engine.py`或`verify_v2.py`。正式入库前必须按真实HTML结构、类名和CLI适配。比例按题目容器计数，不按选项按钮计数。
