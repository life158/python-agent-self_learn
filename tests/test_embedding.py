import pytest


def test_embedding_lazy_import():
    import subprocess
    import sys

    code = """
import sys
import src.embedding

assert "openai" not in sys.modules
"""

    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, result.stderr

from unittest.mock import patch
from src import embedding

def test_embedding_client_cache():
    #清除之前的缓存
    embedding.get_embedding_client.cache_clear()
    #模拟OpenAI客户端
    with patch("openai.OpenAI") as openai_mock:
        #第一次调用
        client1 = embedding.get_embedding_client()
        #第二次调用
        client2 = embedding.get_embedding_client()
        #验证两个对象是否相同
        assert client1 == client2
        #验证客户端只创建一次
        openai_mock.assert_called_once()
    #清除缓存，避免影响其他测试
    embedding.get_embedding_client.cache_clear()


def test_documents_success():
    # 1.导入需要的模块
    from unittest.mock import Mock,patch
    from src import embedding
    # 2.创建模拟AOI返回对象
    mock_response = Mock()
    # 3.创建两条模拟向量数据
    mock_item1 = Mock()
    mock_item1.index = 1
    mock_item1.embedding = [0.2,0.3]

    mock_item2 = Mock()
    mock_item2.index = 0
    mock_item2.embedding = [0.5,0.6]

    # 4.设置API返回的数据
    mock_response.data = [mock_item1, mock_item2]

    # 5.替换客户端获取函数
    with patch("src.embedding.get_embedding_client") as mock_get_client:
        # 6.替换客户端获取函数
        mock_client = mock_get_client.return_value
        # 7.设置模拟API返回值
        mock_client.embeddings.create.return_value = mock_response
        # 8.调用真正的业务函数
        result = embedding.embed_documents(["什么是RAG","什么是Agent"])
        # 9.验证返回向量顺序
        assert result ==[[0.5,0.6],[0.2,0.3]]

        #10.验证API调用次数
        mock_client.embeddings.create.assert_called_once()
        #11.验证客户端获取次数
        mock_get_client.assert_called_once()

def test_embed_documents_invalid_type():

    with patch("src.embedding.get_embedding_client") as mock_client:
        with pytest.raises(ValueError):
            embedding.embed_documents("什么是RAG")

    #验证非法输入没有触发客户端初始化
    mock_client.assert_not_called()

def test_embed_documents_empty():

    with patch("src.embedding.get_embedding_client") as mock_client:
        with pytest.raises(ValueError):
            embedding.embed_documents([])

    #验证非法输入没有触发客户端初始化
    mock_client.assert_not_called()

def test_embed_documents_too_many():
    with patch("src.embedding.get_embedding_client") as mock_client:
        with pytest.raises(ValueError):
            texts = ["测试文本"] * 11
            embedding.embed_documents(texts)
    #验证非法输入没有触发客户端初始化
    mock_client.assert_not_called()

def test_embed_documents_invalid_text():
    #创建包含空字符串的列表
    texts=["","     ","agent是什么？"]
    with patch("src.embedding.get_embedding_client") as mock_client:
        with pytest.raises(ValueError):
            embedding.embed_documents(texts)
    #验证非法输入没有触发客户端初始化
    mock_client.assert_not_called()

