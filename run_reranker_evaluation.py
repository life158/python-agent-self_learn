from src.vector_store import get_collection
from src.evaluation import evaluate_reranker

collection = get_collection()

result = evaluate_reranker(
    question="Embedding在RAG中有什么作用？",
    collection=collection,
    relevant_doc_ids=[
        "chunk_2",
        "chunk_6"
    ],
    k=3,
    candidate_k=7
)

print("检索评价结果：")
print(result)