# CLAUDE.md - AI Agent 开发学习与求职计划 (LangChain 1.0+ 版本 - 2026 最新)

## 👤 个人画像

| 项目 | 信息 |
|------|------|
| 学校 | 山西大学（本硕） |
| 专业 | 计算机科学与技术 |
| 年级 | 研一在读 |
| 目标 | 4 个月后（2026 年 7 月）找到 AI Agent 开发实习 |
| 当前进度 | 已完成 Week 1-2 学习，LangChain 1.0 核心特性已掌握 |

---

## 📁 项目目录介绍

```
E:\agent
├── demo_agent.py          # LangChain 1.0 Agent Demo（已适配 1.0）
├── demo2.py               # 结构化输出 Demo（已适配 1.0）
├── week1/
│   ├── async_practice.py  # 异步 Agent 练习（已适配 1.0）
│   └── async_sync.py      # 异步同步练习
├── week2/
│   ├── prompt_practice.py # Prompt 练习
│   ├── output_practice.py # Output Parser 练习
│   └── interview/
│       ├── questions.md   # 面试题库（1.0 版本）
│       └── code_examples.py # 代码示例
└── note/
    └── learning_plan.md   # 学习计划（1.0 版本）
```

---

## ⚠️ LangChain 1.0 重要变化（面试必考 - 2026 最新）

### 包结构
```python
# 1.0 核心包
from langchain.agents import create_agent           # ✅ 推荐
from langchain.agents.structured_output import ToolStrategy, ProviderStrategy
from langchain.agents.middleware import (
    AgentMiddleware,
    HumanInTheLoopMiddleware,
    SummarizationMiddleware,
    PIIMiddleware
)

# 旧代码兼容（移入 langchain-classic）
from langchain_classic.chains import LLMChain
from langchain_classic.output_parsers import PydanticOutputParser
```

### Agent 创建
```python
# 旧版本 (0.2-0.3) ❌ 已弃用
from langgraph.prebuilt import create_react_agent

# 新版本 (1.0+) ✅
from langchain.agents import create_agent
```

### 结构化输出
```python
# 旧版本 ❌ (仍可用，但不推荐 - 软约束/Prompt 注入)
from langchain_core.output_parsers import PydanticOutputParser

# 新版本 ✅ 推荐 - API 硬约束/Provider 原生支持
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

class Person(BaseModel):
    name: str

model = ChatOpenAI(model="gpt-4")
structured_model = model.with_structured_output(Person)
result = structured_model.invoke("创建一个人")
```

### Middleware（1.0 核心特性）
```python
from langchain.agents import create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    SummarizationMiddleware,
    PIIMiddleware
)

agent = create_agent(
    model="gpt-4.1",
    tools=[search, send_email],
    middleware=[
        PIIMiddleware(strategy="redact"),
        HumanInTheLoopMiddleware(interrupt_on={"send_email": {}})
    ],
    context_schema=Context  # TypedDict，不再支持 Pydantic
)
```

### Context Schema（新 - 仅支持 TypedDict）
```python
from typing import TypedDict  # ✅ 仅支持 TypedDict

class Context(TypedDict):
    user_id: str
    session_id: str

# ❌ Pydantic 不再支持作为 state_schema
```

### Standard Content Blocks（新）
```python
# 统一访问不同提供商的内容类型（reasoning、citation、tool_call 等）
response = model.invoke("What's the capital of France?")
for block in response.content_blocks:
    if block["type"] == "reasoning":
        print(f"Model reasoning: {block['reasoning']}")
    elif block["type"] == "text":
        print(f"Response: {block['text']}")
    elif block["type"] == "tool_call":
        print(f"Tool call: {block['name']}({block['args']})")
```

---

## 🎯 求职目标岗位分析（2026 最新调研）

### 目标岗位：AI Agent 开发实习生

| 公司类型 | 代表企业 | 技术栈要求 |
|----------|----------|------------|
| 大厂 | 京东、字节、腾讯 | LangChain 1.0 + RAG + MCP + 多 Agent 编排 |
| AI 初创 | MiniMax、月之暗面、零一万物 | Agent 架构 + Context Engineering + Human-in-the-loop |
| 传统企业数字化 | 各类转型企业 | MCP 工具集成 + FastAPI + 标准化 API |

### 核心技能要求（2026 年最新 - 从招聘 JD 和 DEV Community 调研）

| 技能类别 | 具体要求 | 优先级 | 当前状态 | 变化 |
|----------|----------|--------|----------|------|
| **Context Engineering** | 上下文设计、状态管理、Prompt 工程 | ⭐⭐⭐⭐⭐ | 已入门 | ↑↑ |
| **LangChain 1.0** | `create_agent` + Middleware | ⭐⭐⭐⭐⭐ | 已入门 | ↑ |
| **MCP (Model Context Protocol)** | 工具标准化集成 | ⭐⭐⭐⭐⭐ | 未学习 | ↑↑ |
| **RAG 技术** | 向量检索 + 知识库 + Rerank | ⭐⭐⭐⭐⭐ | 未学习 | - |
| **Human-in-the-loop** | 人机回环、审批流程 | ⭐⭐⭐⭐ | 未学习 | ↑↑ |
| **Tool Calling** | 工具定义与调用、@tool 装饰器 | ⭐⭐⭐⭐⭐ | 已入门 | - |
| **多 Agent 编排** | 并行/串行/Coordinator 模式 | ⭐⭐⭐⭐ | 未学习 | ↑↑ |
| **向量数据库** | Chroma/pgvector | ⭐⭐⭐⭐ | 未学习 | - |
| **Python 异步** | async/await、并发控制 | ⭐⭐⭐⭐ | 已入门 | - |
| **LangGraph** | StateGraph（高级场景） | ⭐⭐⭐ | 未学习 | ↓ |
| 深度学习框架 | PyTorch 基础 | ⭐⭐ | 了解即可 | ↓ |

### 2026 年五大核心软技能（DEV Community 调研）

1. **Problem Shaping（问题塑形）** - 将模糊需求分解为可执行任务
2. **Context Design（上下文设计）** - 设计高质量的信息注入
3. **Aesthetic Judgment（审美判断）** - 判断什么值得构建
4. **Agent Orchestration（Agent 编排）** - 知道何时用单 Agent/多 Agent/并行/串行
5. **Knowing When NOT to Use Agent** - 知道何时不用 Agent

---

## 📅 4 个月详细学习计划（2026.03 - 2026.07）- 2026 最新版

### 第一阶段：LangChain 1.0 核心（第 1-3 周）⭐⭐⭐⭐⭐

**目标**：掌握 LangChain 1.0 核心特性，理解 Middleware 和 Context Engineering

| 周次 | 学习内容 | 产出物 | 检查点 |
|------|----------|--------|--------|
| 第 1 周 | - Python 异步编程（async/await）<br>- LangChain 1.0 `create_agent`<br>- ChatModel 与 `with_structured_output` | 完成 3 个异步 Agent Demo | ✅ 已完成 |
| 第 2 周 | - Prompt Template 高级用法<br>- Standard Content Blocks<br>- ToolStrategy vs ProviderStrategy | 实现结构化输出 Demo | ✅ 已完成 |
| 第 3 周 | - **Middleware 核心概念**（1.0 重点）<br>- `HumanInTheLoopMiddleware`<br>- `SummarizationMiddleware`、`PIIMiddleware`<br>- 自定义 Middleware 开发 | 实现带中间件的 Agent | ⏳ 进行中 |

**关键理解**：
- `with_structured_output()` = API 硬约束（Provider 原生支持）
- `PydanticOutputParser` = Prompt 软约束（注入 prompt，易出错）
- Middleware 钩子：`before_agent`、`before_model`、`wrap_model_call`、`wrap_tool_call`、`after_model`、`after_agent`

---

### 第二阶段：RAG 核心技术（第 4-7 周）⭐⭐⭐⭐⭐

**目标**：掌握 RAG 全流程，能独立搭建知识库问答系统

| 周次 | 学习内容 | 产出物 | 检查点 |
|------|----------|--------|--------|
| 第 4 周 | - 向量数据库基础（Chroma 1.0/pgvector）<br>- Embedding 原理与选型<br>- 文本分块策略（Chunking） | 搭建本地 Chroma 知识库 | ⏳ 待开始 |
| 第 5 周 | - Retriever 配置与优化<br>- 向量检索 + 关键词检索（Hybrid Search）<br>- RAG 基本流程 | 实现文档问答 Demo | ⏳ 待开始 |
| 第 6 周 | - 高级 RAG 技巧（多路召回、Rerank）<br>- Contextual Compression<br>- Parent Document Retriever | 优化检索准确率 | ⏳ 待开始 |
| 第 7 周 | - RAG 项目实战：个人知识库问答<br>- 结合 LangChain 1.0 Middleware | 完整 RAG 项目 | ⏳ 待开始 |

**关键技术**：
- 使用 `langchain_classic.retrievers`（RAG 相关已移入 classic）
- Chroma 1.0 支持 serverless 和本地持久化

---

### 第三阶段：Agent 进阶与 Context Engineering（第 8-11 周）⭐⭐⭐⭐⭐

**目标**：深入理解 Agent 架构，掌握 Context Engineering 和多 Agent 编排

| 周次 | 学习内容 | 产出物 | 检查点 |
|------|----------|--------|--------|
| 第 8 周 | - 自定义 Tool 开发（1.0 `@tool`）<br>- 动态 Tool 注册与发现<br>- Tool Calling 深入 | 实现 5+ 个自定义工具 | ⏳ 待开始 |
| 第 9 周 | - **Context Engineering**<br>- `context_schema`设计<br>- State vs Context 分离 | 实现上下文管理模块 | ⏳ 待开始 |
| 第 10 周 | - **多 Agent 编排模式**<br>- Sequential Pipeline<br>- Coordinator + Specialist<br>- Parallel Execution + Merge | 多 Agent 协作 Demo | ⏳ 待开始 |
| 第 11 周 | - Agent 规划能力（ReAct/Plan-and-Execute）<br>- Reflection 机制<br>- Critic Node 设计 | 实现规划型 Agent | ⏳ 待开始 |

---

### 第四阶段：MCP 与工程化（第 12-15 周）⭐⭐⭐⭐⭐

**目标**：掌握 MCP 协议和工程化部署

| 周次 | 学习内容 | 产出物 | 检查点 |
|------|----------|--------|--------|
| 第 12 周 | - **MCP (Model Context Protocol)** 基础<br>- MCP Server 搭建<br>- LangChain + MCP 集成 | 实现 MCP 兼容工具 | ⏳ 待开始 |
| 第 13 周 | - FastAPI 后端框架<br>- Agent API 封装<br>- 异步并发处理 | Agent 服务化 Demo | ⏳ 待开始 |
| 第 14 周 | - LangGraph StateGraph（高级场景）<br>- Checkpointer 与 Time Travel<br>- 持久化与断点续跑 | LangGraph 高级项目 | ⏳ 待开始 |
| 第 15 周 | - 综合项目设计与开发<br>- 结合 RAG + MCP + Middleware | 完整工程项目 | ⏳ 待开始 |

**MCP 重点理解**：
- 解决 N×M 集成问题（标准化协议）
- LangChain 通过 Adapter 集成 MCP Server
- 2026 年成为 AI Agent 标准协议

---

### 第五阶段：求职准备（第 16-17 周）⭐⭐⭐⭐⭐

**目标**：完善简历、准备面试、投递实习

| 周次 | 学习内容 | 产出物 | 检查点 |
|------|----------|--------|--------|
| 第 16 周 | - 简历优化<br>- 项目文档完善<br>- GitHub 整理 | 简历终稿 + GitHub 主页 | ⏳ 待开始 |
| 第 17 周 | - 面试题刷题（算法 + 八股）<br>- Mock Interview<br>- 开始投递 | 面试题库 + 投递记录 | ⏳ 待开始 |

---

## 🏆 核心项目清单（面试用 - 2026 最新版）

| 项目 | 技术栈 | 难度 | 优先级 | 状态 |
|------|--------|------|--------|------|
| **RAG 知识库问答** | Chroma + LangChain 1.0 + Embedding | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 待开发 |
| **带 Middleware 的智能助手** | `create_agent` + Middleware + HITL | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 待开发 |
| **MCP 工具集成平台** | MCP Protocol + FastAPI | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 待开发 |
| **多 Agent 协作系统** | Coordinator Pattern + Parallel | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 待开发 |
| **Context Engineering Demo** | context_schema + State 管理 | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 待开发 |

---

## 📚 学习资源汇总（2026 最新）

### 官方文档
| 资源 | 链接 | 说明 |
|------|------|------|
| LangChain 1.0 官方文档 | https://docs.langchain.com/ | **首选学习资源** |
| LangChain 1.0 Release Notes | https://docs.langchain.com/oss/python/releases/langchain-v1 | 必读 |
| LangGraph 文档 | https://docs.langchain.com/oss/python/langgraph/overview | 高级场景使用 |
| MCP 官方文档 | https://modelcontextprotocol.io/ | 2026 年重点 |
| Chroma 文档 | https://docs.trychroma.com/ | 向量数据库 |

### 技术博客
| 资源 | 链接 | 说明 |
|------|------|------|
| LangChain Blog | https://blog.langchain.com/ | 官方公告 |
| DEV Community - AI Agents | https://dev.to/t/aiagents | 社区讨论 |

### 视频课程
| 资源 | 平台 | 说明 |
|------|------|------|
| LangChain 中文教程 | B 站 | 中文入门首选 |
| LangChain Academy | 官方 | 系统性学习 |

---

## ✅ 每日学习习惯

| 时间 | 任务 | 时长 |
|------|------|------|
| 早上 | 阅读 AI 技术文章/论文 | 30min |
| 下午 | 编码实践 | 2-3h |
| 晚上 | 整理笔记/复盘 | 30min |
| 周末 | 项目攻坚/总结 | 4-6h |

---

## 📈 进度追踪

### 总体进度

| 阶段 | 时间 | 状态 |
|------|------|------|
| 第一阶段：LangChain 1.0 核心 | 第 1-3 周 | ⚠️ 第 1-2 周已完成，第 3 周进行中 |
| 第二阶段：RAG 核心 | 第 4-7 周 | ⏳ 待开始 |
| 第三阶段：Agent 进阶 | 第 8-11 周 | ⏳ 待开始 |
| 第四阶段：MCP 与工程化 | 第 12-15 周 | ⏳ 待开始 |
| 第五阶段：求职准备 | 第 16-17 周 | ⏳ 待开始 |

### 本周任务（第 3 周）- Middleware 专题

- [ ] 理解 Middleware 6 个钩子函数
- [ ] 实现 `HumanInTheLoopMiddleware`
- [ ] 实现 `SummarizationMiddleware`
- [ ] 实现自定义 Middleware（敏感词过滤）
- [ ] 整理 Middleware 笔记

---

## 🔖 回复格式要求

**重要**：每次回复结尾必须包含以下内容（不需要保存到文件）：

### 当前问题分析

| 分析项 | 内容 |
|--------|------|
| 重要程度 | ⭐⭐⭐⭐⭐ / ⭐⭐⭐⭐ / ⭐⭐⭐ / ⭐⭐ / ⭐ |
| 难度级别 | 基础 / 中阶 / 高阶 |
| 是否必须掌握 | ✅ 需要 / 了解即可 |
| 相关概念 | 关联的知识点 |

---

## ⚡ LangChain 1.0 面试必考点（2026 最新）

### 核心概念题

| 知识点 | 旧版本 (0.x) | 新版本 (1.0+) | 重要程度 | 底层原理 |
|--------|--------------|---------------|----------|----------|
| Agent 创建 | `create_react_agent` | `create_agent` | ⭐⭐⭐⭐⭐ | 基于 LangGraph |
| 结构化输出 | `PydanticOutputParser` | `with_structured_output` | ⭐⭐⭐⭐⭐ | API 硬约束 vs Prompt 软约束 |
| Response Format | 无 | `ToolStrategy`/`ProviderStrategy` | ⭐⭐⭐⭐⭐ | Tool 调用 vs Provider 原生 |
| Middleware | 无 | 新功能 | ⭐⭐⭐⭐⭐ | 6 个钩子函数 |
| Context Schema | Pydantic | 仅 TypedDict | ⭐⭐⭐⭐ | 类型限制 |
| Content Blocks | 无 | `content_blocks` 属性 | ⭐⭐⭐⭐ | 跨提供商统一 |
| 包结构 | 统一包 | 拆分 + langchain-classic | ⭐⭐⭐ | 核心精简 |
| Python 版本 | 3.9+ | 3.10+ | ⭐⭐ | 语法特性 |

### 面试题库（Q1-Q25）

详见 `week2/interview/questions.md`，已更新到 1.0 版本。

---

*更新于：2026-03-09*
*版本：LangChain 1.0+ 适配版 - 2026 最新*
*下次更新：每周一更新进度追踪*
