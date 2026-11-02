from unittest.mock import patch

from src.rerank import get_reranker


def test_get_reranker_loads_model_lazily_and_reuses_instance():
    get_reranker.cache_clear()

    with patch("src.rerank.CrossEncoder") as mock_cross_encoder:
        first = get_reranker("test-model")
        second = get_reranker("test-model")

    mock_cross_encoder.assert_called_once_with("test-model")
    assert first is second

    get_reranker.cache_clear()
