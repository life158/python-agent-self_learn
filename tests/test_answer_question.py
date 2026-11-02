from unittest.mock import Mock, patch
import pytest

from src import rag_service
from src.rag_service import answer_question
import logging

def test_answer_question_api_error(caplog):

    # 1. 模拟 OpenAI 客户端
    with patch("src.rag_service.OpenAI") as mock_openai:

        mock_client = mock_openai.return_value

        # 2. 模拟 API 调用失败
        mock_client.chat.completions.create.side_effect = RuntimeError(
            "模拟千问API调用失败"
        )

        # 3. 捕获日志
        with caplog.at_level(
            logging.ERROR,
            logger="src.rag_service"
        ):

            # 4. 验证异常是否重新抛出
            with pytest.raises(
                RuntimeError,
                match="模拟千问API调用失败"
            ):
                answer_question(
                    question="什么是RAG？",
                    context="RAG是一种检索增强生成技术。"
                )

        # 5. 验证 API 调用次数
        mock_client.chat.completions.create.assert_called_once()

        # 6. 验证客户端创建次数
        mock_openai.assert_called_once()

        # 7. 验证日志内容
        assert "调用API生成问答失败" in caplog.text
