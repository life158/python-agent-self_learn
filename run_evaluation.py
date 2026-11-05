from src.vector_store import get_collection
from src.evaluation import evaluate_question

collection = get_collection()

result = evaluate_question(
    question="Embedding在RAG中有什么作用？",
    collection=collection,
    relevant_doc_ids=[
        "chunk_2",
        "chunk_6"
    ],
    k=3
)

print("检索评价结果：")
print(result)