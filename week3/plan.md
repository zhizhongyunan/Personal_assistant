# 第三周：RAG 核心技术（一）- 向量数据库基础

## 📅 学习目标

掌握 RAG 全流程基础，能搭建本地知识库

---

## 🎯 核心内容

### 1. RAG 是什么？为什么重要？

```
RAG = Retrieval-Augmented Generation（检索增强生成）

传统 LLM 问题：
- 知识截止训练日期
- 无法访问私有数据
- 容易 hallucination（胡说八道）

RAG 解决方案：
1. 用户提问 →
2. 从知识库检索相关文档 →
3. 把文档 + 问题一起给 LLM →
4. LLM 基于文档回答
```

---

### 2. 向量数据库基础（Chroma）

#### 核心概念

```python
# 向量 = 把文字转成数字列表
"苹果" → [0.1, 0.9, -0.5, 0.3, ...]  # 768 维或 1536 维

# 语义相似的词，向量距离近
"苹果" 和 "香蕉" 的向量距离 < "苹果" 和 "汽车"
```

#### Chroma 安装与使用

```bash
pip install chromadb langchain-chroma
```

```python
from langchain_chroma import Chroma
from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

# 1. 初始化 Embedding 模型
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key="sk-xxx"
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
    "RAG 是检索增强生成技术"
]
db.add_texts(docs)

# 4. 检索相似文档
results = db.similarity_search("AI 框架", k=2)
print(results)  # 返回最相关的 2 个文档
```

---

### 3. 文本分块（Chunking）策略

**为什么需要分块？**
- LLM 有上下文长度限制
- 检索时需要精确匹配相关片段
- 太大：检索不精确；太小：丢失上下文

**常用分块方法：**

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 推荐：递归字符分块
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,        # 每块 500 字符
    chunk_overlap=50,      # 重叠 50 字符（保持上下文连贯）
    separators=["\n\n", "\n", "。", ".", " "]  # 按优先级分隔
)

text = "这是一篇长文章..."
chunks = splitter.split_text(text)
```

---

### 4. Embedding 原理与选型

#### 工作原理

```
文本 → Embedding 模型 → 向量（768/1536 维）

训练目标：语义相近的文本，向量距离近
```

#### 主流 Embedding 模型对比（2026 最新）

| 模型 | 维度 | 价格 | 适合场景 |
|------|------|------|----------|
| `text-embedding-3-small` | 1536 | $0.02/1M | 通用首选 |
| `text-embedding-3-large` | 3072 | $0.13/1M | 高精度场景 |
| `m3e-base` | 768 | 免费 | 中文离线 |
| `bge-large-zh` | 1024 | 免费 | 中文开源最佳 |

#### 使用示例

```python
from langchain_openai import OpenAIEmbeddings

# OpenAI
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    dimensions=1536  # 可指定维度
)

# 中文免费替代
# from langchain_community.embeddings import M3EEmbeddings
# embeddings = M3EEmbeddings()
```

---

## 💻 实战练习

### 练习 1：搭建本地 Chroma 知识库（30 分钟）

```python
# 任务：创建个人笔记知识库
# 要求：
# 1. 初始化 Chroma（持久化到本地）
# 2. 添加 5-10 条笔记
# 3. 测试检索功能

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# 1. 初始化
embeddings = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key="your-api-key"
)

db = Chroma(
    collection_name="notes",
    persist_directory="./chroma_notes",
    embedding_function=embeddings
)

# 2. 添加笔记
notes = [
    "LangChain 是 AI 开发框架，支持 Python 异步编程",
    "RAG 是检索增强生成，解决 LLM 知识截止问题",
    # ... 添加更多
]
db.add_texts(notes)

# 3. 检索
results = db.similarity_search("AI 开发框架", k=2)
for r in results:
    print(r.page_content)
```

---

### 练习 2：文本分块实战（20 分钟）

```python
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 任务：分割一篇长文章
splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=30
)

article = """
【这里放一篇长文章，500+ 字】
"""

chunks = splitter.split_text(article)
print(f"共分成 {len(chunks)} 块")
for i, chunk in enumerate(chunks):
    print(f"\n=== 块{i+1} ===")
    print(chunk)
```

---

## 📝 面试准备

### 基础题

- [ ] Q1: RAG 是什么？解决了什么问题？
- [ ] Q2: 向量数据库的作用是什么？
- [ ] Q3: 为什么需要文本分块？
- [ ] Q4: chunk_overlap 的作用是什么？
- [ ] Q5: Embedding 的工作原理？

### 中阶题

- [ ] Q6: Chroma 和传统数据库的区别？
- [ ] Q7: 如何选择合适的 Embedding 模型？
- [ ] Q8: 分块大小如何选择？太大/太小有什么问题？

---

## 🔗 相关资源

| 资源 | 链接 |
|------|------|
| Chroma 官方文档 | https://docs.trychroma.com/ |
| LangChain Chroma 集成 | https://docs.langchain.com/oss/python/integrations/vectorstores/chroma |
| Embedding 模型对比 | https://platform.openai.com/docs/guides/embeddings |

---

*创建时间：2026-03-09*
*下周预告：RAG 核心技术（二）- Retriever 与检索优化*
