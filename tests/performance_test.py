import time
from src.rerank import get_reranker

def benchmark_reranker(question,documents):

    reranker = get_reranker()
    batch_sizes = [1,2,4,8]

    for batch_size in batch_sizes:

        #  预热两次
        for _ in range(2):
            reranker.compute_scores(
                question,
                documents,
                batch_size=batch_size
            )
        times = []
        #正式测试5次
        for _ in range(10):
            start = time.perf_counter()
            reranker.compute_scores(
                question,
                documents,
                batch_size=batch_size
            )
            elapsed = time.perf_counter() - start
            times.append(elapsed)

        avg_time = sum(times) / len(times)

        print(f"batch_size = {batch_size}, "
              f"times={times},"
              f"avg_time = {avg_time:.4f}s")



if __name__ == '__main__':
    question = input("Question: ")
    documents = [
        "这里放第一条真实的候选文本",
        "这里放第二条真实的候选文本",
        "这里放第三条真实的候选文本",
        "这里放第四条真实的候选文本"
    ]
    benchmark_reranker(question,documents)


