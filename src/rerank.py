# def extract_words(question:str,candidate_keywords:list[str])->list[str]:
#     keywords = []
#     for candidate in candidate_keywords:
#         if candidate.lower() in question.lower():
#             keywords.append(candidate)
#     return keywords
#
#
# def calculate_score(text:str,keywords:list[str])->float:
#     if not isinstance(text,str) or  not text.strip():
#         raise ValueError("问题必须是非空字符串!")
#     if not isinstance(keywords,list) or not keywords:
#         raise ValueError("keywords必须是非空列表")
#     # 统计匹配的关键词数量
#     matched_count = sum(1 for keyword in keywords if keyword.lower() in text.lower())
#     score = matched_count / len(keywords) *100
#     return score
#
# def rerank(question:str,results:list[dict],candidate_keywords:list[str])->list[dict]:
#     #1检查输入的合法性
#     #1.1检查question
#     if not isinstance(question,str) or not question.strip():
#         raise ValueError("question必须为非空字符串")
#     #检查 candidate_keywords:
#     if not isinstance(candidate_keywords,list) or not candidate_keywords:
#         raise ValueError("candidate_keywords必须为非空列表")
#     # 2.遍历results
#     for result in results:
#     # 3.获取每个chunk的document
#         document = result["document"]
#     # 4.调用calculate_score()计算得分
#         score = calculate_score(document,candidate_keywords)
#     # 5.将得分保存到对应的结果中
#         result["score"] = score
#     # 6.按照score从高到低排序
#     sorted_results = sorted(results,key=lambda x:x["score"],reverse=True)
#     # 7.返回排序结果
#     return sorted_results
#
# if __name__ == "__main__":
#     question = input("请输入你的问题:").strip()
#     candidate_keywords = ["Embedding","RAG","向量","语义","检索","作用","数据库","文本"]
#     keywords = extract_words(question,candidate_keywords)
#     result = calculate_score(question,candidate_keywords)
#     print("该问题的评分为:", result)
#     print("该问题提取出来的关键词为:", keywords)
from functools import lru_cache
from src.logger_handler import get_logger
logger = get_logger(__name__)
class Reranker:
    def __init__(self,model_name:str):
        # 1.检查模型名称
        if not isinstance(model_name,str) or not model_name.strip():
            raise ValueError("model_name must be not_empty string")
        # 2.加载 CrossEncoder模型
        # 延迟导入 CrossEncoder
        from sentence_transformers import CrossEncoder
        self.model = CrossEncoder(model_name)

    def compute_scores(self,question:str,documents:list[str])-> list[float]:
        # 1.检查输入的合法性
        # 1.1检查question是否为非空字符串
        if not isinstance(question,str) or not question.strip():
            raise ValueError("question must be not_empty string")
        # 1.2检查documents是否为非空列表
        if not isinstance(documents,list) or not documents:
            raise ValueError("documents must be not_empty list")
        # 1.3检查documents 中的元素是否都是字符串
        for document in documents:
            if not isinstance(document,str) or not document.strip():
                raise ValueError("document must be not_empty string")
        # 2.将question和documents配对
        pairs =[[question,document] for document in documents]
        # 3.调用CrossEncoder模型预测
        scores = self.model.predict(pairs)
       # 4.返回评分结果
        return scores.tolist()

    def rerank(self,
               question:str,
               results:list[dict],
               top_k:int = 3)->list[dict]:
        # 1.检查输入的合法性
        if not isinstance(question,str) or not question.strip():
            raise ValueError("question must be not_empty string")
        # 1.1 检查results是否为非空列表
        if not isinstance(results,list) or not results:
            raise ValueError("results must be not_empty list")
        # 1.2 检查top_k是否为正整数，不能为bool
        if not isinstance(top_k,int) or isinstance(top_k,bool)or top_k<=0:
            raise ValueError("top_k must be not_negative integer")
        # 2.提取所有Chunk的document
        documents = [result["document"] for result in results]
        # 3.调用compute_scores()计算相关性分数
        scores = self.compute_scores(question,documents)
        # 4.将分数保存到对应的result中
        for item,score in zip(results,scores):
            item["score"] = float(score)
        # 5.按照score从高到低排序
        sorted_results = sorted(results,key = lambda x:x["score"],reverse=True)
        # 6.返回前top_k个结果
        return sorted_results[:top_k]


@lru_cache(maxsize=1)
def get_reranker(
        model_name: str = "BAAI/bge-reranker-base"
) -> Reranker:
    """按需创建并复用重排序器，避免模块导入时下载或加载模型。"""
    return Reranker(model_name)

#检索结果数量不代表检索质量，必须判断检索内容是否具有足够的相关性
# def is_relevant(
#         results:list[dict],
#         threshold:float = 0.5
# )-> bool:
#     # 1.检查输入的合法性
#     # 1.1 检查results是否为列表
#     if not isinstance(results,list) :
#         raise ValueError("results must be  not_empty list")
#     if not results:
#         return False
#     # 1.2 检查threshold是否为有效数值
#     if not isinstance(threshold,(int,float)) or isinstance(threshold,bool) or not math.isfinite(threshold):
#         raise ValueError("threshold must be a finite number")
#     # 1.3 检查每个result的数据是否合法
#     for result in results:
#         if not isinstance(result,dict) :
#             raise ValueError("results must be  not_empty dict")
#         if "score" not in result:
#             raise ValueError("result must contain 'score' key")
#         score = result["score"]
#         #判断score的合法性
#         if not isinstance(score,(int,float)) or isinstance(score,bool) or not math.isfinite(score):
#             raise ValueError("score must be a finite number")
#
#     # 2.获取最高的cross_Encoder 分数
#     max_score = max(result["score"] for result in results)
#     # 3.判断最高分是否达到阈值
#     return max_score >= threshold

# #day15:创建统一RAG返回结果
# def create_rag_result(question:str) ->dict:
#     '''
#     接收用户问题,创建一个统一的RAG结果字典,为后续各个模块提供统一的数据存储位置
#     :param question: 用户的问题
#     :return: 统一的结果字典
#     '''
#     # 1.检查question是否为非空字符串
#     if not isinstance(question,str) or not question.strip():
#         raise ValueError("question must be not_empty string")
#     # 2.创建统一的结果字典
#     result = {
#         #用户问题
#         "question":question,
#         #最终检索结果
#         "results":[],
#
#         #向量检索耗时
#         "retrieval_time":0.0,
#
#         #重排序耗时
#         "rerank_time":0.0,
#         #是否通过相关性判断
#         "is_relevant":False,
#         #检索上下文
#         "context":"",
#
#         #大模型问答
#         "answer":"",
#         #当前执行状态
#         "status":"pending",
#         #异常信息
#         "error":None
#     }
#     return result
# # def main1():
# #     question = input("请输入你想问答问题:")
# #     # 1. 执行向量检索
# #     reference = retrieve(question, collection, k=10)
# #
# #     # 2. 合并主要结果和备用结果
# #     candidate_results = (
# #             reference["primary_results"]
# #             + reference["fallback_results"]
# #     )
# #     # 3. 检查是否存在候选文本
# #     if not candidate_results:
# #         print("知识库没有检索到相关资料")
# #         return
# #     reranker = Reranker("BAAI/bge-reranker-base")
# #     # 4. 使用 Cross-Encoder 重新排序
# #     ranked_results = reranker.rerank(
# #         question=question,
# #         results=candidate_results,
# #         top_k=3
# #     )
# #     #为了更清晰地观察Cross-Encoder的运行结果
# #     print("\n=============重排序结果=================")
# #     for item in ranked_results:
# #         print("相关性分数",item["score"])
# #         print("文本",item["document"])
# #         print("-" * 50)
# #     # 5.判断检索结果是否足够相关
# #     if not is_relevant(ranked_results,threshold=0.5):
# #         print("当前知识库缺少足够相关的资料，无法依据知识库回答。")
# #         return
# #     # 6.构建上下文
# #     context =  build_context(ranked_results)
# #     try:
# #         # 7. 交给大语言模型生成回答
# #         answer = answer_question(question, context)
# #         print("大模型的回答：", answer)
# #     except Exception:
# #         logger.exception("RAG主流程生成问答失败。")
# #         print("模型暂时无法回答，请稍后重试。")
# #
# # import time
# #
# # def main():
# #
# #     # 1. 获取用户问题
# #     question = input("请输入您想提问的问题:").strip()
# #
# #     # 2. 判断问题合法性
# #     if not question:
# #         raise ValueError("question must not be empty")
# #
# #     # 3. 创建统一结果字典
# #     result = create_rag_result(question)
# #
# #     try:
# #         # 4. 执行向量检索，并记录耗时
# #         start_time = time.perf_counter()
# #
# #         reference = retrieve(question, collection, k=10)
# #
# #         result["retrieval_time"] = time.perf_counter() - start_time
# #
#         # 5. 保存主要检索结果
#         result["results"] = reference["primary_results"]
#
#         # 6. 判断是否有候选结果
#         if not reference["primary_results"]:
#             result["is_relevant"] = False
#             result["status"] = "success"
#             result["answer"] = "当前知识库没有检索到相关资料。"
#             return result
#
#         # 7. 创建 Cross-Encoder 重排序器
#         reranker = Reranker("BAAI/bge-reranker-base")
#
#         # 8. 执行重排序，并记录耗时
#         start_time = time.perf_counter()
#
#         ranked_results = reranker.rerank(
#             question=question,
#             results=reference["primary_results"],
#             top_k=3
#         )
#
#         result["rerank_time"] = time.perf_counter() - start_time
#
#         # 9. 更新重排序结果
#         result["results"] = ranked_results
#
#         # 10. 执行相关性判断
#         relevant = is_relevant(
#             ranked_results,
#             threshold=0.5
#         )
#
#         result["is_relevant"] = relevant
#
#         # 11. 如果相关性不足，拒绝生成回答
#         if not relevant:
#             result["answer"] = "当前知识库缺少足够相关的资料，无法依据知识库回答。"
#             result["status"] = "success"
#             return result
#
#         # 12. 构建上下文
#         context = build_context(ranked_results)
#         result["context"] = context
#
#         # 13. 调用千问生成回答
#         answer = answer_question(question, context)
#
#         result["answer"] = answer
#
#         # 14. 更新执行状态
#         result["status"] = "success"
#
#         return result
#
#     except Exception as e:
#
#         # 15. 记录异常日志
#         logger.exception("RAG主流程执行失败")
#
#         # 16. 更新异常状态
#         result["status"] = "failed"
#         result["error"] = str(e)
#
#         return result
#
#
#
#
#
#
#
#
#
#
