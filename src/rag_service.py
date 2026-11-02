import os
from dotenv import load_dotenv
from openai import OpenAI
from src.retrieve import retrieve
from src.vector_store import collection
from src.logger_handler import get_logger

logger = get_logger(__name__)
load_dotenv()
MODEL_API_KEY = os.getenv("MODEL_API_KEY")
# MODEL_API_KEY = "sk-ws-H.PEPMIXR.a5jz.MEQCIAn9XLiS5e-g1fgF1IHUIAN2T13Wp3Z-yVNFfDpbJvYsAiB3bYQ0X6oRV5KhNEH90pTecMpp90WVqSFbgTlhGhA4Hk"
MODEL_BASE_URL = os.getenv("MODEL_BASE_URL")
MODEL_ID = os.getenv("MODEL_ID")
def build_context(primary_results:list[dict])->str:
    # 1.创建一个空列表，用于保存文本片段
    results_list = []
    # 2.遍历primary_results
    # 3.提取每个结果中的document
    for result in primary_results:
        results_list.append(result["document"])
    # 4.将多个文本片段合并成一个字符串
    return "\n\n ".join(results_list)

def answer_question(question:str,context:str)->str:
    '''
    该函数负责将用户问题和检索到的上下文发送给千问大语言模型，让模型根据上下文生成问答。
    :param question:
    :param context:
    :return:
    '''
    try:
        messages = [
            {
                "role": "system",
                "content": "你是一个严谨的助手，请优先根据提供的上下文回答问题。"
            },
            {
                "role": "user",
                "content": f"参考资料：\n{context}\n\n问题:{question}"
            }
        ]
        # 创建客户端
        client = OpenAI(api_key=MODEL_API_KEY, base_url=MODEL_BASE_URL)
        response = client.chat.completions.create(model=MODEL_ID, messages=messages)
        answer = response.choices[0].message.content
        return answer
    except Exception :
        # 6.记录异常日记
        logger.exception("调用API生成问答失败")
        # 7.抛出异常
        raise

def main():
    question = input("请输入你想问的问题:").strip()
    if not question:
        raise ValueError("问题不能为空字符串!")
    reference = retrieve(question,collection,k=3)
    print("\n========== 检索结果分析 ==========")
    for item in (
            reference["primary_results"]
            + reference["fallback_results"]
    ):
        print("距离：", item["distance"])
        print("来源：", item["metadata"].get("source"))
        print("文本：", item["document"][:200])
        print("-" * 40)
    if not reference["primary_results"]:
        print("当前知识库没有检索到足够相关的资料，无法依据知识库回答。")
        return
    context = build_context(reference["primary_results"])
    try:
        answer = answer_question(question, context)
        print("大模型的回答为:", answer)
    except Exception :
        print("模型暂时无法回答，请稍后重试。")


if __name__=="__main__":
    main()

