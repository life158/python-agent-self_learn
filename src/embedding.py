# def retrieve_top_k(chunks: list[str],
#                    similarities: list[float],
#                    k: int = 2) -> list[str]:
#     #检查输入
#     if len(chunks) != len(similarities):
#         raise ValueError('The number of chunks and similarities do not match.')
#     if not isinstance(k, int) or isinstance(k,bool) or k < 0:
#         raise ValueError('k must be a non-negative integer.')
#     # 1. 将 chunks 和 similarities 配对
#     pairs = list(zip(chunks, similarities))
#     # 2. 按相似度从高到低排序
#     ranks = sorted(pairs, key=lambda x: x[1], reverse=True)
#     # 3. 取出前 k 个结果
#     results = ranks[:k]
#     # 4. 只返回 Chunk 文本
#     return [item[0] for item in results]
#
# if __name__ == "__main__":
#     chunks = ["Chunk 1", "Chunk 2", "Chunk 3"]
#     similarities = [0.35, 0.92, 0.61]
#     print(retrieve_top_k(chunks, similarities, k=2))

import os
from dotenv import load_dotenv
from openai import OpenAI
from src.text_splitter import split_documents
from src.file_handler import load_file
from langchain_core.documents import Document
import math
from src.logger_handler import get_logger
load_dotenv()
logger = get_logger(__name__)

#从环境变量中读取API_key
MODEL_API_KEY = os.getenv("MODEL_API_KEY")
# MODEL_API_KEY = "sk-ws-H.PEPMIXR.a5jz.MEQCIAn9XLiS5e-g1fgF1IHUIAN2T13Wp3Z-yVNFfDpbJvYsAiB3bYQ0X6oRV5KhNEH90pTecMpp90WVqSFbgTlhGhA4Hk"
MODEL_BASE_URL = os.getenv("MODEL_BASE_URL")
client = OpenAI(api_key=MODEL_API_KEY, base_url=MODEL_BASE_URL)

def embed_text(text:str)->list[float]:
    #检查输入的合法性
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text must not be empty string")
    if not MODEL_API_KEY or not MODEL_BASE_URL:
        raise ValueError("API配置缺失，请检查环境变量")
    try:
        response = client.embeddings.create(input=text, model="text-embedding-v4")
        return response.data[0].embedding
    except Exception:
        logger.exception("Embedding API 调用失败")
        raise


#余弦相似度
def cosine_similarity(a: list[float], b: list[float]) -> float:
    # 1. 检查两个向量长度是否相同
    if len(a) != len(b):
        raise ValueError("vector length mismatch")
    dot_product = 0.0
    # 2. 计算两个向量对应元素的乘积之和
    for i in range(len(a)):
        dot_product += a[i] * b[i]
    # 3. 计算向量 a 的长度
    len_a = math.sqrt(sum(x * x for x in a))
    # 4. 计算向量 b 的长度
    len_b = math.sqrt(sum(x * x for x in b))
    if len_a == 0 or len_b == 0:
        raise ValueError("zero vector is not allowed")
    return dot_product / (len_b * len_a)

#处理多条文本
def embed_documents(texts: list[str]) -> list[list[float]]:
    #判断输入的变量是否合理
    if not isinstance(texts, list):
        raise ValueError("texts must be a list")
    if not texts:
        raise ValueError("texts must not be empty")
    if len(texts) > 10:
        raise ValueError("每次最多处理10条文本")
    if not all(isinstance(item, str) and item.strip() for item in texts):
        raise ValueError("每条文本都必须是非空字符串")
    #创建客户端
    response = client.embeddings.create(input=texts,model="text-embedding-v4")
    #为了确保返回向量与输入文本的顺序一致，可以根据 API 响应中的 index 排序
    items = sorted(response.data, key=lambda item:item.index)
    return [item.embedding for item in items]


if __name__ == "__main__":
    # #读取文本内容
    # result = load_file(path="data/chinese.txt")
    # #将文本转化成Decument
    # decument = Document(page_content=result["content"],metadata={
    #     "source": result["path"],
    #     "file_type": result["type"],
    #     "topic": "RAG"
    # })
    # chunks = split_documents([decument])
    # print(chunks)
    # texts =[chunk.page_content for chunk in chunks]
    # results = embed_documents(texts)
    # for result in results:
    #     print(result)
    #
    # print("Chunk 数量：", len(chunks))
    # print("向量数量：", len(results))
    #
    # for i, (chunk, vector) in enumerate(zip(chunks, results)):
    #     print("来源信息：", chunk.metadata)
    #     print("向量维度：", len(vector))
    #     print("向量前5个值：", vector[:5])
    # assert len(chunks) == len(results), "Chunk 数量与向量数量不一致"
    # assert all(len(vector) == 1024 for vector in results), "存在维度不正确的向量"
    # print("\n验证通过！")
    print(embed_text("测试Embedding异常处理"))