question = "Embedding在RAG中有什么作用？"
documents = [
    "Chroma负责保存和管理向量数据。",
    "Embedding将文本转换成向量，用于语义检索。",
    "Python是一种广泛使用的编程语言。"
]

pairs = [
    [question,document]
    for document in documents
]

for pair in pairs:
    print("="*20)
    print(pair)
    print("="*20)