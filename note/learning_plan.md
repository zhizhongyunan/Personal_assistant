# AI Agent 开发 4 个月学习计划 (LangChain 1.0+ 版本)

> 目标：2026 年 7 月找到 AI Agent 开发实习
> 当前：2026 年 3 月 8 日，研一下学期
> **重要更新**：本计划已适配 LangChain 1.0+ 版本

---

## 📊 已学习内容（Week 1-2）

### Week 1: 异步编程 + Agent 基础 ✅
- [x] async/await 异步编程
- [x] `create_agent` (✅ LangChain 1.0 新 API)
- [x] `@tool` 装饰器定义工具
- [x] `ToolRuntime` 运行时上下文
- [x] `context_schema` 上下文类型定义
- [x] `InMemorySaver` 状态持久化
- [x] 信号量控制并发

### Week 2: Prompt + Output Parser ✅
- [x] `ChatPromptTemplate` 聊天提示词
- [x] `MessagesPlaceholder` 动态历史消息
- [x] `FewShotChatMessagePromptTemplate` 示例提示
- [x] `StrOutputParser` 字符串输出
- [x] `JsonOutputParser` JSON 输出
- [x] `PydanticOutputParser` Pydantic 模型输出 (⚠️ 1.0 推荐用 `with_structured_output`)

---

## ⚠️ LangChain 1.0 重要变化（必须知道）

### 包结构变化
```python
# 旧版本 (0.x)
from langchain.chains import LLMChain
from langchain.agents import initialize_agent

# 新版本 (1.0) - 核心
from langchain.agents import create_agent  # 主推方式
from langchain.agents.structured_output import ToolStrategy, ProviderStrategy

# 旧代码移到 langchain-classic
from langchain_classic.chains import LLMChain  # 向后兼容
```

### Agent 创建变化
```python
# 旧版本 (0.2-0.3)
from langgraph.prebuilt import create_react_agent

# 新版本 (1.0+) ✅ 推荐
from langchain.agents import create_agent
```

### 结构化输出变化
```python
# 旧版本 - 使用 PydanticOutputParser
from langchain_core.output_parsers import PydanticOutputParser
parser = PydanticOutputParser(pydantic_object=Person)
format_instructions = parser.get_format_instructions()  # ⚠️ 已废弃

# 新版本 (1.0+) ✅ 推荐
from pydantic import BaseModel
class Person(BaseModel):
    name: str
    
# 方式1: with_structured_output (推荐)
model = ChatOpenAI(model="gpt-4")
structured_model = model.with_structured_output(Person)
result = structured_model.invoke("创建一个人")

# 方式2: create_agent 中的 response_format
from langchain.agents.structured_output import ToolStrategy
agent = create_agent(
    model=model,
    tools=tools,
    response_format=ToolStrategy(Person)  # 强制结构化输出
)
```

### 新增核心概念
1. **Middleware (中间件)**：可插拔的定制化扩展
2. **Content Blocks**：统一的内容类型表示
3. **Model Profiles**：模型能力描述
4. **Python 3.10+**：不再支持 3.9

---

## 🗓️ 详细周计划（更新版）

### 第 1 周（3.5 - 3.11）：Python 异步与 LangChain 基础 ✅ 已完成

**检查点**：✅ 已使用 LangChain 1.0 的 `create_agent`

---

### 第 2 周（3.12 - 3.18）：Prompt 与 Memory ⚠️ 部分过时需更新

**更新内容**：
- [ ] Output Parser 部分更新为 `with_structured_output`
- [ ] 添加 ProviderStrategy/ToolStrategy 讲解

---

### 第 3 周（3.19 - 3.25）：RAG 基础 - 向量数据库

**学习目标**：
- 理解 Embedding 原理
- 掌握 Chroma/LangChain 1.0 向量存储
- 实现文档向量化存储

**每日任务**：

| 日期 | 任务 | 预计耗时 | 完成打勾 |
|------|------|----------|----------|
| 周一 | Embedding 原理学习 | 2h | [ ] |
| 周二 | Chroma 1.0 安装与基础使用 | 2h | [ ] |
| 周三 | 文本分块策略（Chunking） | 2h | [ ] |
| 周四 | 文档加载与分块实践 | 2h | [ ] |
| 周五 | 向量化存储完整流程 | 3h | [ ] |
| 周六 | 实践：个人笔记知识库 | 4h | [ ] |
| 周日 | 整理笔记 + 复盘 | 2h | [ ] |

**代码练习（LangChain 1.0）**：
```python
# 1.0 版本向量存储
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

# 加载文档
loader = TextLoader("docs.txt")
docs = loader.load()

# 分块
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = splitter.split_documents(docs)

# 向量化存储
embeddings = OpenAIEmbeddings()
vectorstore = Chroma.from_documents(documents=splits, embedding=embeddings)

# 检索
retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
```

**检查点**：
- [ ] 理解余弦相似度计算
- [ ] 能完成文档向量化入库 (Chroma 1.0)
- [ ] 实现基础向量检索

---

### 第 4 周（3.26 - 4.1）：RAG 进阶 - 检索优化

**学习目标**：
- 掌握 Retriever 配置
- 理解多路召回
- 实现 Rerank 重排序

**每日任务**：

| 日期 | 任务 | 预计耗时 | 完成打勾 |
|------|------|----------|----------|
| 周一 | VectorStoreRetriever | 2h | [ ] |
| 周二 | BM25 关键词检索 | 2h | [ ] |
| 周三 | 多路召回（向量+BM25） | 3h | [ ] |
| 周四 | Rerank 模型使用 | 2h | [ ] |
| 周五 | RAG 完整流程整合 | 3h | [ ] |
| 周六 | 实践：文档问答系统 | 4h | [ ] |
| 周日 | 整理笔记 + 复盘 | 2h | [ ] |

**检查点**：
- [ ] 理解检索召回率概念
- [ ] 能配置多路召回
- [ ] 检索准确率>80%

---

### 第 5 周（4.2 - 4.8）：RAG 项目实战

**目标**：完成一个完整的 RAG 项目，可作为面试作品

**项目选题**（三选一）：
- [ ] 个人笔记知识库问答
- [ ] PDF 论文问答系统
- [ ] 技术文档智能助手

---

### 第 6 周（4.9 - 4.15）：自定义 Tool 开发 (LangChain 1.0)

**学习目标**：
- 深入理解 Tool 定义（1.0 新API）
- 能封装任意函数为 Tool
- 掌握 Tool 注册与发现

**每日任务**：

| 日期 | 任务 | 预计耗时 | 完成打勾 |
|------|------|----------|----------|
| 周一 | @tool 装饰器基础 | 2h | [ ] |
| 周二 | Tool 注解与描述 | 2h | [ ] |
| 周三 | 复杂参数 Tool 定义 | 2h | [ ] |
| 周四 | Tool 注册机制 | 2h | [ ] |
| 周五 | 实践：5 个实用工具 | 3h | [ ] |
| 周六 | Tool 库整合 | 3h | [ ] |
| 周日 | 整理笔记 + 复盘 | 2h | [ ] |

**1.0 新增 Tool 概念**：
```python
# LangChain 1.0 Tool 定义
from langchain.tools import tool

@tool
def calculate(a: int, b: int, operation: str = "add") -> int:
    """执行数学计算
    
    Args:
        a: 第一个数字
        b: 第二个数字
        operation: 操作类型，add/subtract/multiply/divide
    """
    operations = {"add": a + b, "subtract": a - b, "multiply": a * b, "divide": a / b}
    return operations.get(operation, a + b)
```

**工具实践清单**：
- [ ] 天气查询工具
- [ ] 计算器工具
- [ ] 数据库查询工具
- [ ] 文件处理工具
- [ ] API 调用工具

---

### 第 7 周（4.16 - 4.22）：LangGraph 状态图

**学习目标**：
- 理解 StateGraph 核心概念
- 掌握节点与边定义
- 实现条件路由

**每日任务**：

| 日期 | 任务 | 预计耗时 | 完成打勾 |
|------|------|----------|----------|
| 周一 | StateGraph 基础 | 2h | [ ] |
| 周二 | 节点定义与执行 | 2h | [ ] |
| 周三 | 边与条件路由 | 2h | [ ] |
| 周四 | 状态管理深入 | 2h | [ ] |
| 周五 | 多节点工作流 | 3h | [ ] |
| 周六 | 实践：多步骤任务流 | 4h | [ ] |
| 周日 | 整理笔记 + 复盘 | 2h | [ ] |

---

### 第 8 周（4.23 - 4.29）：Agent 规划能力

**学习目标**：
- 理解 ReAct 模式
- 掌握 Plan-and-Execute
- 实现 Reflection 机制

---

### 第 9 周（4.30 - 5.6）：Agent 项目实战

**目标**：完成一个完整的 Agent 项目

---

### 第 10 周（5.7 - 5.13）：FastAPI 与 Agent 服务化

**学习目标**：
- 掌握 FastAPI 基础
- 实现 Agent API 封装
- 理解异步并发处理

---

### 第 11 周（5.14 - 5.20）：多 Agent 协作

**学习目标**：
- 理解多 Agent 协作模式
- 掌握 CrewAI 框架
- 实现 Agent 通信

---

### 第 12 周（5.21 - 5.27）：MCP 协议与工具集成

**学习目标**：
- 理解 MCP 协议
- 实现 MCP 兼容工具
- 掌握 OpenAPI 规范

---

### 第 13-16 周：项目实战 + 求职准备

---

## 📈 进度追踪

### 总体进度

| 阶段 | 时间 | 状态 |
|------|------|------|
| 第一阶段：基础巩固 | 第 1-2 周 | ✅ 第 1 周已完成，第 2 周需更新 |
| 第二阶段：RAG 核心 | 第 3-6 周 | ⏳ 待开始 |
| 第三阶段：Agent 进阶 | 第 7-10 周 | ⏳ 待开始 |
| 第四阶段：工程化 | 第 11-14 周 | ⏳ 待开始 |
| 第五阶段：求职准备 | 第 15-16 周 | ⏳ 待开始 |

### 本周任务（第 2 周）- 更新

- [x] ChatPromptTemplate 基础
- [x] FewShotChatMessagePromptTemplate
- [ ] Output Parser 更新到 1.0 推荐方式
- [ ] 添加 ToolStrategy 实战
- [ ] 整理 LangChain 1.0 笔记

---

## ⚡ LangChain 1.0 面试必考点

| 知识点 | 旧版本 (0.x) | 新版本 (1.0+) | 重要程度 |
|--------|--------------|---------------|----------|
| Agent 创建 | `create_react_agent` | `create_agent` | ⭐⭐⭐⭐⭐ |
| 结构化输出 | `PydanticOutputParser` | `with_structured_output` | ⭐⭐⭐⭐⭐ |
| Middleware | 无 | 新功能 | ⭐⭐⭐⭐ |
| 包结构 | 统一包 | 拆分 + langchain-classic | ⭐⭐⭐ |
| Python 版本 | 3.9+ | 3.10+ | ⭐⭐ |

---

*更新于：2026-03-08*
*版本：LangChain 1.0+ 适配版*