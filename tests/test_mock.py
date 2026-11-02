from unittest.mock import Mock
def create_mock():
    # 1. 模拟 API 返回对象
    mock_response = Mock()
    # 2. 创建模拟 message 对象
    mock_message = Mock()
    mock_message.content = "RAG是一种检索增强生成技术。"
    # 3. 创建模拟 choice 对象
    mock_choice = Mock()
    mock_choice.message = mock_message
    # 4. 将 choice 放入列表
    mock_response.choices = [mock_choice]
    # 模拟API客户端
    mock_client = Mock()
    mock_client.chat.completions.create.return_value = mock_response
    # 模拟调用
    response = mock_client.chat.completions.create(
        model="test-model",
        messages=[]
    )
    answer = response.choices[0].message.content
    return answer,mock_client

def test_create_mock():
    answer,mock_client = create_mock()
    assert answer=="RAG是一种检索增强生成技术。"
    #验证API恰好调用一次
    mock_client.chat.completions.create.assert_called_once()
    #验证API调用参数
    mock_client.chat.completions.create.assert_called_once_with(
        model="test-model",
        messages=[]
    )

