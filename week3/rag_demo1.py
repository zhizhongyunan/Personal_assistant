from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
embeddings = OpenAIEmbeddings(
    model="text-embedding-v4",
    dimensions=1536,
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-50bcf3eb0ef649f19075cd6a016de5df",
    check_embedding_ctx_length=False
)
text = ["Langchain is a framework for developing applications for LLM",
        "data is import for LLM"]

db = Chroma(
    collection_name="my_docs",
    persist_directory="./chroma_db",  # 持久化路径
    embedding_function=embeddings,
)

docs = [
    "LangChain 是一个 AI 开发框架",
    "Python 是一门编程语言",
    "RAG 是检索增强生成技术",
]
db.add_texts(docs)
print(db.similarity_search("what is langchain", k=1))

vectorstore = InMemoryVectorStore.from_texts(
    text, 
    embedding = embeddings,
    
)

retriever = vectorstore.as_retriever()
#print(retriever.invoke("what is langchain")[0])
