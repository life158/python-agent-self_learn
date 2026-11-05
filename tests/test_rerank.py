import copy
import subprocess
import sys
from unittest.mock import patch,Mock

import numpy as np
import pytest
from networkx.convert import to_dict_of_lists

from src.rerank import Reranker

def test_rerank_lazy_import():

    code = """
import sys
import src.rerank

assert "sentence_transformers" not in sys.modules
"""

    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0

@ pytest.mark.parametrize(
    "batch_size",
    [0,-1,True,1.5]
)
def test_computer_scores_invalid_batch_size(batch_size):
    # 1. 创建 Rerank 测试对象
    #创建 不执行__init__的测试对象
    reranker = Reranker.__new__(Reranker)
    # 2. Mock.self.model.predict
    reranker.model = Mock()
    # 3.使用pytest.raises 捕获ValueError
    with pytest.raises(ValueError):
        reranker.compute_scores(
            question="什么是RAG？",
            documents=["RAG是一种检索增强技术"],
            batch_size=batch_size
        )
    # 4.验证predict 没有被调用
    reranker.model.predict.assert_not_called()

def test_computer_scores_valid_batch_size():
    # 1.创建Rerank测试对象
    reranker = Reranker.__new__(Reranker)
    # 2.Mock.self.model.predict
    reranker.model = Mock()
    reranker.model.predict.return_value = Mock(
        tolist = lambda:[0.85]
    )
    result = reranker.compute_scores(
        question="什么是RAG？",
        documents=["RAG是一种检索增强技术"],
        batch_size=16
    )
    #验证返回结果
    assert result ==[0.85]
    #验证predict是否被调用一次
    reranker.model.predict.assert_called_once_with(
        [["什么是RAG？","RAG是一种检索增强技术"]],
        batch_size=16,
        show_progress_bar=False
    )

def test_rerank_batch_size_consistency():

    reranker = Reranker.__new__(Reranker)

    #Mock模型，模拟固定评分
    reranker.model = Mock()
    reranker.model.predict.side_effect = [
        np.array([0.85,0.60,0.95,0.30]),
        np.array([0.85,0.60,0.95,0.30])
    ]
    results = [
        {"document":"RAG是一种检索增强生成技术"},
        {"document":"Agent是一种能够自主执行任务的智能体"},
        {"document":"Embedding用于将文本转换成向量"},
        {"document":"python是一种编程语言"}
    ]
    result_1 = reranker.rerank(
        question="什么是RAG？",
        results=copy.deepcopy(results),
        top_k=4,
        batch_size=1
    )

    result_4 = reranker.rerank(
        question="什么是RAG？",
        results=copy.deepcopy(results),
        top_k=4,
        batch_size=4
    )

    #验证最终排序一致
    assert [item["document"] for item in result_1] == [item["document"] for item in result_4]