from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

embeddings = OpenAIEmbeddings(
    model="text-embedding-v4",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-50bcf3eb0ef649f19075cd6a016de5df",
    dimensions=1536,
    check_embedding_ctx_length=False,
)

text=["langchain是一个专业的agent开发框架", "rag是知识库检索系统", "燕政奇有点帅"]

db = Chroma(
    collection_name="my_docs",
    persist_directory="./chroma_db",  # 持久化路径
    embedding_function=embeddings,
)

db.add_texts(text)
print(db.similarity_search("what is langchain", k=5))

vectorstore = InMemoryVectorStore.from_texts(
    text, 
    embedding = embeddings,
)

retriever = vectorstore.as_retriever()
# print(retriever.invoke("what is langchain")[0])
