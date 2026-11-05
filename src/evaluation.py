from torchgen.gen_functionalization_type import return_from_mutable_noop_redispatch
from src.rerank import get_reranker, Reranker
from src.vector_store import get_collection
from src.retrieve import retrieve
def precision_at_k(results:list,k:int)->float:
    #检查输入的合法性
    # 1.检查results是否为非空列表。
    if not isinstance(results,list) or not results:
        raise ValueError("results must be a non_empty list")

    for result in results:
        if (not isinstance(result,int) or isinstance(result,bool) or result not in (0,1)):
            raise ValueError("results的元素必须是0或者1")

    if not isinstance(k,int) or isinstance(k,bool) or k<=0:
        raise ValueError("k must be a positive integer")
    #计算相关文档数量
    selected_results = results[:k]
    return sum(selected_results) / len(selected_results)



def recall_at_k(
        results:list,
        total_relevant:int,
        k:int
)->float:
    #检查输入的合法性
    # 1.检查results是否为非空列表。
    if not isinstance(results, list) or not results:
        raise ValueError("results must be a non_empty list")

    for result in results:
        if (not isinstance(result, int) or isinstance(result, bool) or result not in (0, 1)):
            raise ValueError("results的元素必须是0或者1")

    if not isinstance(total_relevant,int) or isinstance(total_relevant,bool) or total_relevant<=0:
        raise ValueError("total_relevant must be a positive integer")

    if not isinstance(k, int) or isinstance(k, bool) or k <= 0:
        raise ValueError("k must be a positive integer")

    selected_results = results[:k]
    if sum(selected_results) > total_relevant:
        raise ValueError("截取的相关文档的数量不能大于总相关文档数量")
    return sum(selected_results) / total_relevant



def reciprocal_rank(results:list[int])->float:
    #检查输入的合法性
    if not isinstance(results, list) or not results:
        raise ValueError("results must be a non_empty list")
    for result in results:
        if (not isinstance(result, int) or isinstance(result, bool) or result not in (0, 1)):
            raise ValueError("列表元素只能是整数0/1")
    for index,result in enumerate(results):
        if result == 1:
            return 1/(index+1)

    return 0.0
def mean_reciprocal_rank(queries_results:list[list[int]])->float:
    #检查输入合法性
    if not isinstance(queries_results, list) or not queries_results:
        raise ValueError("queries_results must be a non_empty list")
    total_rr = 0.0
    for results in queries_results:
        result  = reciprocal_rank(results)
        total_rr += result
    average = total_rr / len(queries_results)
    return average
#以上是底层函数负责输入校验，上层函数负责编排
def evaluate_retrieval(results:list[int],total_relevant:int,k:int)->dict:
    precision_result = precision_at_k(results,k)
    recall_result = recall_at_k(results,total_relevant,k)
    reciprocal_result = reciprocal_rank(results[:k])
    return {
        "precision_at_k":precision_result,
        "recall_at_k":recall_result,
        "reciprocal_rank":reciprocal_result,
    }

def convert_to_relevance(retrieved_doc_ids:list[str], relevant_doc_ids:list[str])->list[int]:
    #检查输入合法性
    if not isinstance(retrieved_doc_ids, list) or not retrieved_doc_ids:
        raise ValueError("retrieved_doc_ids must be a non_empty list")
    if not isinstance(relevant_doc_ids,list) or not relevant_doc_ids:
        raise ValueError("relevant_doc_ids must be a non_empty list")
    result = []
    for doc_id in retrieved_doc_ids:
        if doc_id in relevant_doc_ids:
            #将这个位置变成1
            result.append(1)
        else:
            result.append(0)

    return result

def evaluate_question(question:str,collection,relevant_doc_ids:list[str],k:int=3)->dict:
    retrieved_result = retrieve(question,collection,k=k)
    #提取实际检索到的文档ID
    ids=[result["id"] for result in retrieved_result["all_results"]]
    #转换相关性标签
    convert_ids = convert_to_relevance(ids,relevant_doc_ids)
    #计算评价指标
    result_dict = evaluate_retrieval(convert_ids,total_relevant=len(relevant_doc_ids),k=k)
    return result_dict


def evaluate_reranker(
        question:str,
        collection,
        relevant_doc_ids:list[str],
        k:int=3,
        candidate_k: int = 7)->dict:
    retrieved_result = retrieve(question,collection,k=candidate_k)
    ids=[result["id"] for result in retrieved_result["primary_results"][:k]]
    base_convert_ids = convert_to_relevance(ids,relevant_doc_ids)
    #计算原始向量的检索指标
    baseline_metrics = evaluate_retrieval(base_convert_ids,total_relevant=len(relevant_doc_ids),k=k)
    #调用 Reranker
    reranker = get_reranker("BAAI/bge-reranker-base")
    #执行重排序
    rerank_result = reranker.rerank(
        question=question,
        results=[
            item.copy() for item in retrieved_result["primary_results"]
        ],
        top_k=k
    )
    reranker_id = [result["id"] for result in rerank_result]
    reranker_convert_ids = convert_to_relevance(reranker_id,relevant_doc_ids)
    reranker_metrics = evaluate_retrieval(reranker_convert_ids,total_relevant=len(relevant_doc_ids),k=k)

    return {
        "question":question,
        "baseline_metrics":baseline_metrics,
        "reranker_metrics":reranker_metrics,
    }








if __name__=="__main__":
    results = [1,0,0]
    print("预期结果为:",reciprocal_rank(results))
    results = [0,1,0]
    print("预期结果为:",reciprocal_rank(results))
    results = [0,0,0]
    print("预期结果为:",reciprocal_rank(results))

