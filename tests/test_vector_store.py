def test_import_vector_store():
    import src.vector_store
    assert src.vector_store.get_chroma_client.cache_info().currsize == 0
    assert src.vector_store.get_collection.cache_info().currsize == 0
