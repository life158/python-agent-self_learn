from unittest import result

from src.embedding import embed_text
from src.logger_handler import get_logger
logger = get_logger(__name__)
def retrieve(question:str,collection,k:int=3)->dict:
    # 1.检查 question是否为非空字符串
    if not isinstance(question,str) or not question.strip() :
        raise ValueError("question必须是非空字符串！")

    # 2.检查k 是否为正整数，且不能为bool
    if not isinstance(k,int) or isinstance(k,bool) or k <= 0:
        raise ValueError("k必须为正整数")
    try:
        # 3.检查数据库是否有数据
        count = collection.count()
    except Exception:
        logger.exception("chroma数据库获取数据失败!")
        raise
    if count == 0:
        raise ValueError("数据库无数据!")
    # 4.将question转化成 Embedding向量
    query = embed_text(question)
    try:
        # 5.调用 collection.query()检索 Top-k
        result = collection.query(query_embeddings=[query], n_results=min(count, k),
                                  include=["documents", "metadatas", "distances"])
        ids = result["ids"][0]
        documents = result["documents"][0]
        metadatas = result["metadatas"][0]
        distances = result["distances"][0]
        primary_results = []
        fallback_results = []
        all_results = []
        threshold = 0.8
        for doc_id,document, metadata, distance in zip(ids,documents, metadatas, distances):
            item = {
                "id": doc_id,
                "document": document,
                "metadata": metadata,
                "distance": distance
            }
            if distance <= threshold:
                primary_results.append(item)
            else:
                fallback_results.append(item)
            all_results.append(item)

        # 6.返回检索结果
        return {
            "primary_results": primary_results,
            "fallback_results": fallback_results,
            "all_results": all_results
        }
    except Exception:
        logger.exception("chroma检索或结果处理失败!")
        raise



class FakeCollection:
    #模拟数据库中有10条数据
    def count(self):
        return 10

    #模拟数据库查询失败
    def query(self,**kwargs):
        raise RuntimeError("模拟chroma数据库查询失败")

if __name__ == "__main__":
    # # 测试一：与 RAG 知识库相关的问题
    # question_a = "Embedding在RAG中有什么作用？"
    #
    # # 测试二：与 RAG 知识库无关的问题
    # question_b = "今天天气很好，适合出去跑步吗？"
    #
    # # 执行检索
    # result_a = retrieve(question_a, collection, k=3)
    # result_b = retrieve(question_b, collection, k=3)
    #
    # # 输出测试结果
    # print("\n========== 测试 A：相关问题 ==========")
    # print("主要结果数量：", len(result_a["primary_results"]))
    # print("备用结果数量：", len(result_a["fallback_results"]))
    #
    # print("\n========== 测试 B：无关问题 ==========")
    # print("主要结果数量：", len(result_b["primary_results"]))
    # print("备用结果数量：", len(result_b["fallback_results"]))
    #
    # # 查看具体的检索结果
    # print("\n========== 测试 A 的主要结果 ==========")
    # for item in result_a["primary_results"]:
    #     print("文本：", item["document"][:100])
    #     print("距离：", item["distance"])
    #     print("来源：", item["metadata"].get("source"))
    #     print("-" * 30)
    #
    # print("\n========== 测试 B 的备用结果 ==========")
    # for item in result_b["fallback_results"]:
    #     print("文本：", item["document"][:100])
    #     print("距离：", item["distance"])
    #     print("来源：", item["metadata"].get("source"))
    #     print("-" * 30)
    # fake_collection = FakeCollection()
    # try:
    #     result = retrieve(
    #         "测试Chroma异常",
    #         fake_collection,
    #         k=3
    #     )
    #     print(result)
    # except Exception as e:
    #     print("捕获到异常",e)
    from src.vector_store import get_collection
    collection = get_collection()
    result = retrieve(question="什么是RAG?",collection=collection,k=3)
    print("============检索结果==================")
    for item in result["primary_results"]+result["fallback_results"]:
        print("ID",item["id"])
        print("文本",item["document"][:100])
        print("距离: ",item["distance"])
        print("来源: ",item["metadata"].get("source"))
        print("-" * 40)

    for item in result["all_results"]:
        print(item["id"],item["distance"])