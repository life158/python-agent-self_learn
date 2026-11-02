import pytest
from src.main import create_rag_result
#正常输入
def test_rag_result():
    question = "什么是RAG？"
    results = create_rag_result(question=question)
    assert isinstance(results, dict)
    assert results["question"] == question
    assert results["results"] == []
    assert results["status"]=="pending"
    assert results["error"] is None

#非法输入
#测试空字符串
def test_empty_question():
    with pytest.raises(ValueError):
        create_rag_result(question="")

#测试纯空格
def test_whitespace_question():
    with pytest.raises(ValueError):
        create_rag_result("   ")

# 测试整数
def test_invalid_type():
    with pytest.raises(ValueError):
        create_rag_result(123)

