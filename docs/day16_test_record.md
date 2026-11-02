# Day 16：Agent / RAG 自动化测试学习记录

## 1. 今日学习目标

本次学习围绕 Agent / RAG 项目的自动化测试展开，主要目标如下：

- 使用 `pytest` 编写和运行测试。
- 测试 `create_rag_result` 的正常输入与非法输入。
- 使用 `Mock` 和 `patch` 隔离真实的 OpenAI API 调用。
- 使用 `return_value` 模拟 API 正常返回。
- 使用 `side_effect` 模拟 API 调用异常。
- 使用 `pytest.raises` 检查异常是否继续向上抛出。
- 使用 `caplog` 检查 `logger.exception` 是否记录错误日志。
- 理解导入路径、补丁目标和补丁作用域对测试结果的影响。

## 2. pytest 环境与常用命令

安装 pytest：

```bash
pip install pytest
```

运行全部测试：

```bash
pytest
```

显示更详细的测试信息：

```bash
pytest -v
```

运行指定测试文件：

```bash
pytest -v tests/test_rag_service.py
```

运行指定测试函数：

```bash
pytest -v tests/test_rag_service.py::test_answer_question
```

如果需要在测试时显示程序输出，可以使用：

```bash
pytest -v -s
```

## 3. `create_rag_result` 测试

### 3.1 `create_rag_result` 测试目的

`create_rag_result` 的测试既要验证正常输入能够生成预期结果，也要验证非法输入不会被当成正常数据处理。

主要检查内容包括：

- 正常输入时，函数返回值是否正确。
- 返回结果的结构和字段是否符合预期。
- 空值、错误类型或不符合要求的参数是否触发预期异常。
- 边界输入是否得到正确处理。

### 3.2 正常输入测试思路

正常测试遵循 Arrange、Act、Assert 三个步骤：

```python
def test_create_rag_result_with_valid_input():
    # Arrange：准备合法输入
    question = "什么是 RAG？"
    answer = "RAG 是检索增强生成。"

    # Act：调用被测试函数
    result = create_rag_result(question, answer)

    # Assert：检查实际字段，以下仅表示测试结构
    assert result is not None
```

实际断言应以项目中 `create_rag_result` 的真实返回结构和业务规则为准。

### 3.3 非法输入测试思路

当函数约定非法输入应抛出异常时，可以使用 `pytest.raises`：

```python
def test_create_rag_result_with_invalid_input():
    with pytest.raises((TypeError, ValueError)):
        create_rag_result(None, None)
```

异常类型应与项目当前实现保持一致，不应为了让测试通过而随意扩大捕获范围。

### 3.4 `create_rag_result` 已确认结果

`create_rag_result` 相关测试已经得到以下结果：

```text
4 passed
```

这说明当时编写的 4 个相关测试均已通过。

## 4. `answer_question` 的外部 API 隔离测试

### 4.1 为什么需要 Mock

`answer_question` 会调用 OpenAI 客户端。单元测试不应依赖真实网络和真实 API，因为真实调用可能受到以下因素影响：

- 网络状态。
- API Key 是否有效。
- 调用额度和费用。
- 第三方服务是否稳定。
- 模型返回内容是否具有不确定性。

因此，测试中使用 `Mock` 和 `patch` 替换真实客户端，只验证当前模块自身的业务逻辑。

## 5. patch 本地创建的 OpenAI 客户端

### 5.1 patch 的核心原则

补丁应加在“被测试代码查找对象的位置”，而不一定是该对象最初定义的位置。

本项目的 OpenAI 客户端是在 `src.rag_service.answer_question` 内部创建的，因此测试应针对 `answer_question` 实际使用的名称或构造位置进行 patch。

如果函数内部通过类似下面的方式创建客户端：

```python
client = OpenAI(...)
```

测试通常需要 patch `answer_question` 所在模块中的 `Codex汉化增强版`，而不是直接 patch OpenAI SDK 的原始定义。例如：

```python
with patch("src.rag_service.answer_question.OpenAI") as mock_openai:
    ...
```

具体路径仍应以项目当前的模块结构和导入方式为准。如果 `answer_question` 是函数名而不是模块名，则需要 patch 该函数实际所属模块中的 `Codex汉化增强版` 名称。

### 5.2 `return_value` 模拟正常响应

`return_value` 用于指定 Mock 被调用后返回的内容。测试可以构造与真实 SDK 响应结构相似的对象：

```python
from unittest.mock import Mock, patch


def test_answer_question_success():
    mock_response = Mock()
    mock_response.choices[0].message.content = "模拟回答"

    with patch("src.rag_service.answer_question.OpenAI") as mock_openai:
        mock_client = mock_openai.return_value
        mock_client.chat.completions.create.return_value = mock_response

        result = answer_question("测试问题")

    assert result == "模拟回答"
```

以上代码展示的是本次学习使用的 Mock 链路；调用参数和返回断言应与项目的真实函数签名保持一致。

### 5.3 正常场景已确认结果

`answer_question` 的正常场景测试已经通过。

## 6. `side_effect` 模拟 API 异常

### 6.1 API 异常测试目的

异常测试需要确认两件不同的事情：

1. API 失败后，异常会继续抛给上层调用者。
2. 程序会记录错误日志，便于定位问题和查看完整堆栈。

`side_effect` 可以让 Mock 在被调用时主动抛出异常：

```python
mock_client.chat.completions.create.side_effect = RuntimeError("API 调用失败")
```

### 6.2 使用 `pytest.raises` 检查异常

```python
with pytest.raises(RuntimeError, match="API 调用失败"):
    answer_question("测试问题")
```

`pytest.raises` 验证异常没有被静默吞掉。上层调用者收到异常后，才能决定重试、降级或终止流程。

### 6.3 使用 `caplog` 检查 `logger.exception`

如果业务代码的异常处理类似：

```python
except Exception:
    logger.exception("调用API生成问答失败")
    raise
```

测试可以同时检查异常和日志：

```python
import logging


def test_answer_question_api_error(caplog):
    with patch("src.rag_service.answer_question.OpenAI") as mock_openai:
        mock_client = mock_openai.return_value
        mock_client.chat.completions.create.side_effect = RuntimeError("API 调用失败")

        with caplog.at_level(logging.ERROR):
            with pytest.raises(RuntimeError, match="API 调用失败"):
                answer_question("测试问题")

    assert "调用API生成问答失败" in caplog.text
```

相比直接 Mock `logger.exception`，`caplog` 更贴近程序的真实日志行为，并且可以直接检查日志文本。

### 6.4 为什么异常和日志都要检查

异常抛出和日志记录承担不同职责：

- `raise`：把失败传递给上层，避免上层误以为任务成功，并允许上层决定重试、降级或终止。
- `logger.exception`：记录错误信息和异常堆栈，帮助开发者追溯错误原因和发生位置。

因此，同时检查两项可以验证错误处理链路是否完整，而不只是确认“程序报错了”。

### 6.5 异常场景已确认结果

异常场景测试中遇到的日志捕获问题已经通过 `caplog` 成功解决。

目前已有信息没有明确给出该测试与其他测试一起运行时的最终汇总数字，因此本记录不写成“全部测试均已通过”，也不虚构最终的 `pytest` 汇总输出。

## 7. 本次问题与经验总结

### 7.1 导入路径问题

测试能否导入目标函数，取决于项目目录、包结构和运行位置。遇到 `ModuleNotFoundError` 或导入失败时，应依次检查：

- 是否从项目根目录运行 `pytest`。
- `src` 目录和模块路径是否与 import 语句一致。
- 包目录是否需要 `__init__.py`。
- 测试中导入的是模块还是模块内的函数。
- 项目的 pytest 或 Python 路径配置是否正确。

本次学习的重要经验是：优先修正项目的导入方式和测试运行位置，不要依赖临时、难以维护的路径修改。

### 7.2 patch 路径问题

patch 目标应是被测试模块运行时实际查找的名称。即使对象来自 OpenAI SDK，也可能需要 patch：

```text
src.rag_service.answer_question.OpenAI
```

而不是 SDK 的原始路径。判断 patch 是否正确，可以检查：

- 被测试文件使用了 `import openai`，还是 `from openai import OpenAI`。
- 客户端是在模块加载时创建，还是在函数内部创建。
- patch 路径指向的是模块属性，还是误把函数当成模块。

### 7.3 patch 上下文管理器的作用域

`with patch(...):` 只在其代码块内部生效。离开代码块后，原对象会自动恢复。

因此，被测试函数的调用必须发生在 patch 的作用域内：

```python
with patch("正确路径") as mocked:
    # 配置 Mock
    result = answer_question("问题")

# 此处 patch 已失效
```

如果在 `with` 代码块结束后才调用 `answer_question`，程序可能重新创建真实客户端并发起真实 API 请求，导致测试失败或产生额外费用。

## 8. 今日掌握的能力

- 使用 pytest 组织并执行自动化测试。
- 使用断言验证函数返回值。
- 为正常输入、非法输入和边界输入设计测试。
- 使用 Mock 隔离外部 API。
- 使用 patch 替换函数内部创建的 OpenAI 客户端。
- 使用 `return_value` 模拟正常 API 返回。
- 使用 `side_effect` 模拟 API 异常。
- 使用 `pytest.raises` 验证异常向上抛出。
- 使用 `caplog` 验证错误日志。
- 理解异常负责传递失败、日志负责追踪故障。
- 理解正确导入路径、patch 目标和 patch 作用域的重要性。

## 9. 测试结果记录

截至本记录整理时，已确认的信息如下：

| 测试内容 | 已确认结果 |
| --- | --- |
| `create_rag_result` 相关测试 | `4 passed` |
| `answer_question` 正常场景 | 测试通过 |
| `answer_question` API 异常场景 | `caplog` 日志捕获问题已解决，测试成功完成 |
| 所有测试的最终合并运行结果 | 尚未提供明确汇总数字 |

## 10. 下一步计划

1. 从项目根目录运行完整测试套件，记录最终的 pytest 汇总结果。
2. 检查正常场景和异常场景是否都完全隔离真实 API。
3. 为关键 Mock 增加调用参数断言，例如 `assert_called_once_with`。
4. 补充空字符串、缺失上下文、响应结构异常等边界场景。
5. 统一测试文件命名、fixture 和重复的 Mock 数据。
6. 学习依赖注入，降低 RAG 模块与 OpenAI 客户端之间的耦合度。
7. 在确认文件和测试结果无误后，再自行完成 Git 提交。

> 说明：本记录仅整理当前已经确认的学习和测试情况，未声明 Git 提交已经完成。
