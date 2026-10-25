# Day 02：路径与文本读取

## 1. 今日目标

- 使用 `pathlib.Path` 处理文件路径。
- 实现 `read_text(path, encoding="utf-8")`。
- 正确读取普通文本、中文文本和空文件。
- 对文件不存在和路径不是文件的情况抛出明确异常。

## 2. 开发环境

- 操作系统：Windows
- Python：3.14.5
- 内容根目录：`D:\work_data\PythonProject\agent\self_learn`
- 源代码：`src/file_handler.py`
- 测试数据：`data/`

## 3. 本次更新

原来的路径计算会向上返回过多目录，导致程序错误地在 `agent/data` 中查找文件。本次将内容根目录改为根据当前源文件定位：

```python
file_root = Path(__file__).resolve().parent.parent
file_path = file_root.joinpath(path).resolve()
```

路径关系如下：

```text
self_learn/                 # 内容根目录
├── data/
│   ├── chinese.txt
│   ├── empty.txt
│   └── normal.txt
└── src/
    └── file_handler.py     # __file__
```

`Path(__file__).resolve()` 得到 `file_handler.py` 的绝对路径；第一个 `.parent` 得到 `src`，第二个 `.parent` 得到内容根目录 `self_learn`。因此，即使程序从其他目录启动，也可以正确找到 `data` 中的文件。

同时，将“路径存在但不是文件”的异常修改为 `IsADirectoryError`：

```python
if not file_path.is_file():
    raise IsADirectoryError(f"File not file: {file_path}")
```

## 4. 当前函数

```python
def read_text(path: str | Path, encoding="utf-8") -> str:
    file_root = Path(__file__).resolve().parent.parent
    file_path = file_root.joinpath(path).resolve()
    print(file_path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if not file_path.is_file():
        raise IsADirectoryError(f"File not file: {file_path}")

    return file_path.read_text(encoding=encoding)
```

## 5. 测试数据

| 输入 | 测试目的 |
|---|---|
| `data/chinese.txt` | 验证 UTF-8 中文读取 |
| `data/empty.txt` | 验证空文件处理 |
| `data/normal.txt` | 验证普通英文文本读取 |
| `data/test.txt` | 验证文件不存在时的异常 |
| `data` | 验证路径是目录时的异常 |

其中 `data/test.txt` 故意不创建，用来测试 `FileNotFoundError`。

## 6. 实际测试结果

| 测试场景 | 预期结果 | 实际结果 | 状态 |
|---|---|---|---|
| 读取中文文件 | 返回完整中文内容，无乱码 | 成功返回 71 个字符，内容以“你好”开头 | 通过 |
| 读取空文件 | 返回空字符串 `""` | 返回 `""` | 通过 |
| 读取普通英文文件 | 返回三行英文文本 | 成功返回完整内容 | 通过 |
| 读取不存在的文件 | 抛出 `FileNotFoundError` | 正确抛出 `FileNotFoundError` | 通过 |
| 读取目录 | 抛出 `IsADirectoryError` | 正确抛出 `IsADirectoryError` | 通过 |

所有场景均使用当前的 `read_text()` 独立执行并验证，测试结果符合预期。

## 7. 主程序执行顺序说明

当前 `__main__` 中的测试顺序是：中文文件、空文件、不存在的文件、普通文件。

程序执行到 `data/test.txt` 时会按预期抛出 `FileNotFoundError`，因此后面的 `normal.txt` 不会继续执行。这不代表普通文件读取失败；独立测试已经确认它能够正常读取。

如果希望一次运行完所有测试，可以分别使用 `try/except` 捕获每个测试的异常，或者把不存在文件的测试放到最后。

## 8. 今日收获

- 学会通过 `__file__` 定位当前 Python 文件。
- 学会从 `src/file_handler.py` 推导项目内容根目录。
- 理解相对路径和绝对路径的区别。
- 理解空文件、文件不存在和路径是目录属于三种不同情况。
- 学会使用 `FileNotFoundError` 和 `IsADirectoryError` 表达不同错误。
- 确认异常不能被静默吞掉，调用方应该能清楚看到失败原因。

## 9. 后续改进

- 删除或替换函数中的临时调试语句 `print(file_path)`。
- 为 `read_text()` 添加 docstring。
- 把手工测试迁移到 `tests/test_file_handler.py`，使用 `pytest` 自动验证。
- 为绝对路径输入和错误编码增加测试。

## 10. 完成情况

Day 02 的核心任务已经完成：函数可以从项目内容根目录读取文本，并且五种测试场景均有明确、符合预期的结果。
