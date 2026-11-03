#验证配置是否可靠
import pytest
from config.settings import  validate_model_settings,validate_embedding_settings
def test_validate_model_settings():
     validate_model_settings(
         model_api_key="test_key",
         model_base_url="https://example.com/v1",
         model_id="qwen-plus")
def test_model_api_key_error():
    with pytest.raises(ValueError):
        validate_model_settings(model_api_key="",
                                model_base_url="https://example.com/v1",
                                model_id="qwen-plus")
def test_model_api_base_url_error():
    with pytest.raises(ValueError):
        validate_model_settings(model_api_key="test_key",model_base_url="",model_id="qwen-plus")
def test_model_all_settings_missing():
    with pytest.raises(ValueError) as exc_info:
        validate_model_settings(model_api_key=None, model_base_url="",model_id="	")
    assert "MODEL_API_KEY" in str(exc_info.value)
    assert "MODEL_BASE_URL" in str(exc_info.value)
    assert "MODEL_ID" in str(exc_info.value)

#第二组:测试Embedding配置
def test_validate_embedding_settings():
    validate_embedding_settings(
        model_api_key="test_key",
        model_base_url="https://example.com/v1",
        embedding_model_id="text-embedding-v4"
    )

def test_embedding_model_missing():
    with pytest.raises(ValueError) as exc_info:
        validate_embedding_settings(model_api_key=None, model_base_url="", embedding_model_id="   ")
    assert "EMBEDDING_API_KEY" in str(exc_info.value)
    assert "EMBEDDING_BASE_URL" in str(exc_info.value)
    assert "EMBEDDING_MODEL_ID" in str(exc_info.value)


