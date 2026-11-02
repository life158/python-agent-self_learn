# Day 03 多格式文件加载器测试记录

> 测试对象：`src/file_handler.py` 中的 `load_file()`  
> 测试日期：2026-10-25  
> Python 版本：3.14.5  
> 总体结论：Day 03 核心功能已完成。TXT、MD、JSON 三种正常读取场景已实际运行通过；异常场景仍需补充测试。

## 一、已完成内容

`load_file()` 当前支持 `.txt`、`.md`、`.json`，并完成路径构造、存在性检查、普通文件检查、后缀识别、格式分派和统一返回。

统一返回结构为：

```python
{
    "content": content,
    "path": str(file_path),
    "type": file_suffix,
}
```

TXT 和 Markdown 使用 `f.read()` 返回字符串；JSON 使用 `json.load()` 解析后，再通过 `json.dumps(..., ensure_ascii=False)` 转为字符串。

## 二、实际测试环境与执行

- 项目：`D:\work_data\PythonProject\agent\self_learn`
- Python：3.14.5
- 测试文件：`tests/test_file_handler.py`

虚拟环境中未安装 `pytest`，所以 `python -m pytest` 未能启动测试。这属于环境依赖缺失，不是业务代码测试失败。

随后从项目根目录执行：

```text
.venv\Scripts\python.exe -m tests.test_file_handler
```

进程退出码为 `0`，测试脚本中的 `test_txt()`、`test_md()`、`test_json()` 均执行通过。

## 三、测试结果

| 编号 | 测试项目 | 输入 | 结果 |
|---|---|---|---|
| TC-01 | TXT 文件读取 | `data/samples.txt` | ✅ 已通过 |
| TC-02 | Markdown 文件读取 | `data/example.md` | ✅ 已通过 |
| TC-03 | JSON 文件读取 | `data/example.json` | ✅ 已通过 |
| TC-04 | 不支持的文件格式 | `data/example.pdf` | ⚠️ 前置条件未满足 |
| TC-05 | 文件不存在 | 不存在的路径 | ⬜ 待补充自动化测试 |
| TC-06 | 路径是目录 | `data` | ⬜ 待补充自动化测试 |
| TC-07 | JSON 格式错误 | 错误 JSON 文件 | ⬜ 待补充自动化测试 |

统计：已运行通过 3 项，前置条件未满足 1 项，待补充自动化测试 3 项。

## 四、通过项详情

### TXT

- 返回值为字典；
- `content` 为 `str`；
- `type == ".txt"`。

### Markdown

- `content` 为 `str`；
- `type == ".md"`。

### JSON

- JSON 成功解析；
- 重新序列化后的 `content` 为 `str`；
- `type == ".json"`。

## 五、发现的问题

1. 虚拟环境尚未安装 `pytest`，暂时不能自动发现全部测试函数。
2. `data/example.pdf` 不存在，因此程序先抛出 `FileNotFoundError`，无法验证不支持格式分支。
3. 实现中不支持格式抛出 `TypeError`，而测试期待 `ValueError`。创建 PDF 测试文件后，该用例仍会因异常类型不一致而失败。建议统一为：

```python
raise ValueError(f'File not supported: {file_suffix}')
```

4. 直接运行 `tests/test_file_handler.py` 会因导入路径出现 `ModuleNotFoundError`；从项目根目录使用模块方式运行正常。

## 六、结论

Day 03 的多格式文件加载器核心功能已经完成，TXT、MD、JSON 三种主要正常场景均已实际运行验证。后续只需完善测试环境与异常测试：安装 `pytest`、准备真实的未支持格式文件、统一异常类型，并添加不存在文件、目录路径和错误 JSON 的用例。
