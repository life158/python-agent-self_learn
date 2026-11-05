from data.evaluation_dataset import evaluation_dataset

for item in evaluation_dataset:
    print("问题：", item["question"])
    print("相关文档：", item["relevant_doc_ids"])
    print("相关文档数量：", len(item["relevant_doc_ids"]))
    print("-" * 40)