"""
第三周 RAG 实战代码 - 向量数据库基础

包含所有核心代码示例，可直接运行
"""
import asyncio
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter


# ============================================
# 练习 1：搭建本地 Chroma 知识库
# ============================================

async def chroma_basic_example():
    """
    Chroma 基础用法
    """
    # 1. 初始化 Embedding
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key="sk-xxx"  # 替换为你的 API Key
    )

    # 2. 创建向量数据库
    db = Chroma(
        collection_name="my_docs",
        persist_directory="./chroma_db",  # 持久化路径
        embedding_function=embeddings
    )

    # 3. 添加文档
    docs = [
        "LangChain 是一个 AI 开发框架",
        "Python 是一门编程语言",
        "RAG 是检索增强生成技术",
        "向量数据库用于语义搜索",
        "Embedding 将文本转为向量"
    ]
    db.add_texts(docs)

    # 4. 检索
    results = db.similarity_search("AI 框架", k=2)

    print("=== 检索结果 ===")
    for i, r in enumerate(results):
        print(f"{i+1}. {r.page_content}")

    return results


# ============================================
# 练习 2：文本分块实战
# ============================================

async def text_splitting_example():
    """
    文本分块示例
    """
    # 1. 创建分块器
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,        # 每块 300 字符
        chunk_overlap=30,      # 重叠 30 字符
        separators=["\n\n", "\n", "。", ".", " "]
    )

    # 2. 测试文章
    article = """
    LangChain 是一个用于开发 AI 应用的框架，
    它提供了丰富的组件和工具，
    帮助开发者快速构建基于大语言模型的应用。

    RAG（检索增强生成）是 LangChain 的核心功能之一。
    它通过检索外部知识库，
    增强 LLM 的回答能力，
    解决知识截止和幻觉问题。

    向量数据库是 RAG 系统的基础组件。
    它将文本转为向量存储，
    支持语义相似度检索，
    比传统关键词搜索更智能。
    """

    # 3. 分块
    chunks = splitter.split_text(article)

    print(f"\n=== 分块结果：共 {len(chunks)} 块 ===")
    for i, chunk in enumerate(chunks):
        print(f"\n--- 块 {i+1} ---")
        print(f"字符数：{len(chunk)}")
        print(chunk[:100] + "..." if len(chunk) > 100 else chunk)

    return chunks


# ============================================
# 练习 3：完整的 RAG 流程
# ============================================

async def full_rag_example():
    """
    完整 RAG 流程演示
    """
    print("\n=== 完整 RAG 流程 ===\n")

    # 1. 准备数据
    article = """
    LangChain 2026 年发布了 1.0 版本，
    带来了全新的 create_agent API 和 Middleware 系统。
    1.0 版本使用 with_structured_output 进行结构化输出，
    支持 ToolStrategy 和 ProviderStrategy 两种方式。

    RAG 技术是企业级 AI 应用的核心，
    能够解决 LLM 知识截止、私有数据接入、幻觉等问题。
    Chroma 是流行的向量数据库，
    支持本地持久化和云端部署。
    """

    # 2. 文本分块
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=150,
        chunk_overlap=20
    )
    chunks = splitter.split_text(article)

    print(f"1. 分块完成：{len(chunks)} 块")

    # 3. 存入向量数据库
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small",
        api_key="sk-xxx"
    )

    db = Chroma.from_texts(
        chunks,
        embedding=embeddings,
        persist_directory="./chroma_rag_demo"
    )

    print("2. 向量数据库创建完成")

    # 4. 检索测试
    queries = [
        "LangChain 1.0 有什么新功能？",
        "RAG 解决什么问题？",
        "Chroma 是什么？"
    ]

    print("\n3. 检索测试：")
    for q in queries:
        results = db.similarity_search(q, k=1)
        print(f"\nQ: {q}")
        print(f"A: {results[0].page_content}")

    return db


# ============================================
# 练习 4：Embedding 模型对比
# ============================================

async def embeddings_comparison():
    """
    对比不同 Embedding 模型
    """
    print("\n=== Embedding 模型对比 ===\n")

    # 模型列表
    models = [
        ("text-embedding-3-small", 1536),
        ("text-embedding-3-large", 3072),
    ]

    test_text = "测试文本，用于比较不同 Embedding 模型"

    for model_name, dims in models:
        print(f"模型：{model_name}")
        print(f"维度：{dims}")

        embeddings = OpenAIEmbeddings(
            model=model_name,
            api_key="sk-xxx"
        )

        vector = embeddings.embed_query(test_text)
        print(f"实际维度：{len(vector)}")
        print(f"向量前 5 个值：{vector[:5]}")
        print("-" * 40)


# ============================================
# 运行所有练习
# ============================================

async def main():
    print("=== 第三周 RAG 实战代码 ===\n")

    # 练习 1：Chroma 基础
    # await chroma_basic_example()

    # 练习 2：文本分块
    # await text_splitting_example()

    # 练习 3：完整 RAG 流程
    # await full_rag_example()

    # 练习 4：Embedding 对比
    # await embeddings_comparison()

    print("\n=== 完成！取消注释运行练习 ===")


if __name__ == "__main__":
    asyncio.run(main())
