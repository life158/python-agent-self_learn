from pathlib import Path
import chromadb
from src.text_splitter import split_documents
from src.file_handler import load_file
from langchain_core.documents import Document
from src.embedding import embed_documents
#创建本地持久化客户端
path = "data/chroma_db"
file_root = Path(__file__).resolve().parent.parent
file_path = file_root.joinpath(path).resolve()
client = chromadb.PersistentClient(
    path=file_path
)
#获取或创建知识集合
collection = client.get_or_create_collection(name="knowledge_base")

print(collection.name)


def add_chunks(collection,chunks,embeddings):
    #1.检查chunks和embeddings数量是否一致
    if len(chunks) != len(embeddings):
        raise ValueError("chunks and embeddings must have the same length")
    if not chunks:
        return
    #2.生成每个chunk的固定ID
    ids = [f"chunk_{i}" for i in range(len(chunks))]
    #3.提取每个chunk的文本
    documents =[chunk.page_content for chunk in chunks]
    #4.提取每个chunk的metadata
    metadatas = [chunk.metadata for chunk in chunks]
    #5.使用collection.add()保存数据
    collection.add(ids=ids,documents=documents,metadatas=metadatas,embeddings=embeddings)

if __name__ == "__main__":
    # 创建本地持久化客户端
    path = "data/chroma_db"
    file_root = Path(__file__).resolve().parent.parent
    file_path = file_root.joinpath(path).resolve()
    client = chromadb.PersistentClient(
        path=file_path
    )
    # 获取或创建知识集合
    collection = client.get_or_create_collection(name="knowledge_base")
    result = load_file(path="data/chinese.txt")

    document = Document(
        page_content=result["content"],
        metadata={
            "source": result["path"],
            "file_type": result["type"],
            "topic": "RAG"
        }
    )

    chunks = split_documents([document])
    texts = [chunk.page_content for chunk in chunks]
    results = embed_documents(texts)

    print("Chunk 数量：", len(chunks))
    print("向量数量：", len(results))

    add_chunks(collection, chunks, results)

    print("数据库记录数量：", collection.count())