from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

def split_documents(documents: list[Document],chunk_size: int = 500,chunk_overlap: int = 50) -> list[Document]:
    #判断chunk_size和chunk_overlap的合法性
    if chunk_size <= 0 or chunk_overlap < 0:
        raise ValueError("chunk_size and chunk_overlap must be non-negative")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be less than chunk_size")
    if not isinstance(chunk_size,int) or not isinstance(chunk_overlap,int):
        raise ValueError("chunk_size and chunk_overlap must be int")
    #1.创建RecursiveCharacterTextSplitter
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = splitter.split_documents(documents)
    return chunks

if __name__ == "__main__":
    document = Document(
        page_content="""
    RAG，全称 Retrieval-Augmented Generation，即检索增强生成，是一种将外部知识检索与大语言模型生成能力结合起来的技术。在传统的大语言模型应用中，模型主要依赖训练阶段学习到的知识回答用户问题。但是模型训练完成之后，其内部知识通常不会自动更新，因此当用户询问最新信息、企业内部资料或者某个专业知识库中的内容时，仅依赖模型自身参数可能无法得到准确答案。RAG 的核心思想是在大语言模型生成答案之前，先从外部知识库中检索与用户问题相关的信息，然后将这些信息作为上下文提供给大语言模型，使模型能够基于检索结果生成更加准确的回答。

    一个典型的 RAG 系统通常包含文件加载、文本解析、文本切分、向量化、向量存储、信息检索以及大语言模型生成等多个阶段。首先，系统需要读取 PDF、TXT、Markdown 等不同类型的知识文件，并将文件内容转换为统一的 Document 对象。Document 通常不仅包含 page_content，也就是实际的文本内容，同时还包含 metadata，用于记录文件来源、页码、文件路径等补充信息。这些 metadata 在后续的知识检索、来源追踪和结果过滤过程中具有重要作用。

    由于一个完整文件可能包含大量文本，因此通常不会直接将整个文件作为一个检索单位。RAG 系统会使用 Text Splitter 将较长的 Document 切分成多个较小的 Chunk。每个 Chunk 保存原始文档中的一部分内容，同时通常继续保留原始 Document 的 metadata。通过这种方式，即使一个文件被切分成几十甚至几百个 Chunk，系统仍然能够知道每个 Chunk 来源于哪个原始文件。

    文本切分过程中有两个重要参数，分别是 chunk_size 和 chunk_overlap。chunk_size 用于控制每个文本块的目标大小，而 chunk_overlap 用于控制相邻文本块之间保留多少重复内容。如果 chunk_size 设置得过大，一个 Chunk 中可能同时包含多个不同主题，从而降低检索的精确程度；如果 chunk_size 设置得过小，又可能导致完整语义被切散，使检索到的文本缺乏足够上下文。因此在实际 RAG 项目中，需要根据文档特点、Embedding 模型以及具体业务需求选择合适的文本切分策略。

    文本完成切分之后，每一个 Chunk 会通过 Embedding 模型转换为向量。Embedding 的作用是将文本的语义信息表示为一组数值，使计算机可以通过向量之间的距离或相似度判断不同文本之间的语义关系。生成的向量通常会存储到专门的向量数据库中。当用户提出问题时，系统同样会将用户问题转换为向量，并在向量数据库中搜索与问题最相似的若干文本块。

    检索得到相关 Chunk 后，RAG 系统会将这些文本内容与用户原始问题一起构造成 Prompt，并发送给大语言模型。大语言模型不再只依赖自身训练参数回答问题，而是可以参考从知识库中检索出来的内容。因此，RAG 能够在不重新训练大语言模型的情况下，为模型提供特定领域、企业内部或者持续更新的外部知识。对于实际的 Agent 系统来说，RAG 还可以作为 Agent 获取外部知识的一种重要工具，与其他工具调用、任务规划和状态管理模块共同组成更加完整的智能应用。
    """,
        metadata={
            "source": "data/rag_test.txt",
            "file_type": ".txt",
            "topic": "RAG"
        }
    )

    chunks = split_documents([document])
    print(f"总共切除{len(chunks)}个chunk")
    i = 1
    for chunk in chunks:
        print(f"chunk {i}的内容为:{chunk.page_content}")
        i += 1

