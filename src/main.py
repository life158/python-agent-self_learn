from src.rag_service import build_context,answer_question
from src.retrieve import retrieve
from src.logger_handler import get_logger
import math
import time
from src.rerank import get_reranker
from src.vector_store import get_collection

logger = get_logger(__name__)
#检索结果数量不代表检索质量，必须判断检索内容是否具有足够的相关性
def is_relevant(
        results:list[dict],
        threshold:float = 0.5
)-> bool:
    # 1.检查输入的合法性
    # 1.1 检查results是否为列表
    if not isinstance(results,list) :
        raise ValueError("results must be  not_empty list")
    if not results:
        return False
    # 1.2 检查threshold是否为有效数值
    if not isinstance(threshold,(int,float)) or isinstance(threshold,bool) or not math.isfinite(threshold):
        raise ValueError("threshold must be a finite number")
    # 1.3 检查每个result的数据是否合法
    for result in results:
        if not isinstance(result,dict) :
            raise ValueError("results must be  not_empty dict")
        if "score" not in result:
            raise ValueError("result must contain 'score' key")
        score = result["score"]
        #判断score的合法性
        if not isinstance(score,(int,float)) or isinstance(score,bool) or not math.isfinite(score):
            raise ValueError("score must be a finite number")

    # 2.获取最高的cross_Encoder 分数
    max_score = max(result["score"] for result in results)
    # 3.判断最高分是否达到阈值
    return max_score >= threshold
#day15:创建统一RAG返回结果
def create_rag_result(question:str) ->dict:
    '''
    接收用户问题,创建一个统一的RAG结果字典,为后续各个模块提供统一的数据存储位置
    :param question: 用户的问题
    :return: 统一的结果字典
    '''
    # 1.检查question是否为非空字符串
    if not isinstance(question,str) or not question.strip():
        raise ValueError("question must be not_empty string")
    # 2.创建统一的结果字典
    result = {
        #用户问题
        "question":question,
        #最终检索结果
        "results":[],

        #向量检索耗时
        "retrieval_time":0.0,

        #重排序耗时
        #模型初始化时间
        "rerank_init_time":0.0,
        #推理时间
        "rerank_inference_time":0.0,
        #总耗时
        "rerank_time":0.0,
        #是否通过相关性判断
        "is_relevant":False,
        #检索上下文
        "context":"",

        #大模型问答
        "answer":"",
        #当前执行状态
        "status":"pending",
        #异常信息
        "error":None
    }
    return result


def main():

    # 1. 获取用户问题
    question = input("请输入您想提问的问题:").strip()

    # 2. 判断问题合法性
    if not question:
        raise ValueError("question must not be empty")

    # 3. 创建统一结果字典
    result = create_rag_result(question)

    try:
        # 4. 执行向量检索，并记录耗时
        start_time = time.perf_counter()
        collection = get_collection()
        reference = retrieve(question, collection, k=10)

        result["retrieval_time"] = time.perf_counter() - start_time

        # 5. 保存主要检索结果
        result["results"] = reference["primary_results"]

        # 6. 判断是否有候选结果
        if not reference["primary_results"]:
            result["is_relevant"] = False
            result["status"] = "success"
            result["answer"] = "当前知识库没有检索到相关资料。"
            return result
        primary_results = reference["primary_results"]
        print("检索候选文本数量：", len(primary_results))
        # 8. 执行重排序，分别记录初始化和推理耗时
        #记录整个重排序阶段开始时间
        start_time = time.perf_counter()
        # 1.获取或初始化Reranker
        init_time = time.perf_counter()
        reranker = get_reranker()
        result["rerank_init_time"] = time.perf_counter() - init_time
        # 2.推理耗时
        inference_start = time.perf_counter()
        ranked_results = reranker.rerank(
            question=question,
            results=reference["primary_results"],
            top_k=3
        )
        result["rerank_inference_time"] = time.perf_counter() - inference_start
        result["rerank_time"] = time.perf_counter() - start_time
        # 9. 更新重排序结果
        result["results"] = ranked_results

        # 10. 执行相关性判断
        relevant = is_relevant(
            ranked_results,
            threshold=0.5
        )

        result["is_relevant"] = relevant

        # 11. 如果相关性不足，拒绝生成回答
        if not relevant:
            result["answer"] = "当前知识库缺少足够相关的资料，无法依据知识库回答。"
            result["status"] = "success"
            return result

        # 12. 构建上下文
        context = build_context(ranked_results)
        result["context"] = context

        # 13. 调用千问生成回答
        answer = answer_question(question, context)

        result["answer"] = answer

        # 14. 更新执行状态
        result["status"] = "success"

        return result

    except Exception as e:

        # 15. 记录异常日志
        logger.exception("RAG主流程执行失败")

        # 16. 更新异常状态
        result["status"] = "failed"
        result["error"] = str(e)

        return result

if __name__ == "__main__":
    result = main()
    print("执行状态：", result["status"])
    print("相关性判断：", result["is_relevant"])
    print("检索耗时：", result["retrieval_time"])
    print("Reranker初始化耗时：", result["rerank_init_time"])
    print("Reranker推理耗时：", result["rerank_inference_time"])
    print("Reranker总耗时：", result["rerank_time"])
    print("模型回答", result["answer"])
    print("模型错误:", result["error"])
