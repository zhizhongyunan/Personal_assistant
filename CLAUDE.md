# CLAUDE.md - AI Agent 开发学习与求职计划 (LangChain 1.0+ 版本)

## 👤 个人画像

| 项目 | 信息 |
|------|------|
| 学校 | 山西大学（本硕） |
| 专业 | 计算机科学与技术 |
| 年级 | 研一在读 |
| 目标 | 4 个月后（2026 年 7 月）找到 AI Agent 开发实习 |
| 当前进度 | 已完成 Week 1-2 学习，正在适配 LangChain 1.0 |

---

## 📁 项目目录介绍

```
E:\agent
├── demo_agent.py          # LangChain 1.0 Agent Demo（已适配1.0）
├── demo2.py               # 结构化输出 Demo（已适配1.0）
├── week1/
│   ├── async_practice.py  # 异步Agent练习（已适配1.0）
│   └── async_sync.py      # 异步同步练习
├── week2/
│   ├── prompt_practice.py # Prompt练习
│   ├── output_practice.py # Output Parser练习
│   └── interview/
│       ├── questions.md   # 面试题库（1.0版本）
│       └── code_examples.py # 代码示例
└── note/
    └── learning_plan.md   # 学习计划（1.0版本）
```

---

## ⚠️ LangChain 1.0 重要变化（面试必考）

### 包结构
```python
# 1.0 核心包
from langchain.agents import create_agent           # ✅ 推荐
from langchain.agents.structured_output import ToolStrategy, ProviderStrategy

# 旧代码兼容
from langchain_classic.chains import LLMChain        # 向后兼容
```

### Agent 创建
```python
# 旧版本 (0.2-0.3) ❌
from langgraph.prebuilt import create_react_agent

# 新版本 (1.0+) ✅
from langchain.agents import create_agent
```

### 结构化输出
```python
# 旧版本 ❌ (仍可用，但不推荐)
from langchain_core.output_parsers import PydanticOutputParser

# 新版本 ✅ 推荐
from pydantic import BaseModel
from langchain_openai import ChatOpenAI

class Person(BaseModel):
    name: str

model = ChatOpenAI(model="gpt-4")
structured_model = model.with_structured_output(Person)
result = structured_model.invoke("创建一个人")
```

---

## 🎯 求职目标岗位分析

### 目标岗位：AI Agent 开发实习生

| 公司类型 | 代表企业 | 技能匹配度 |
|----------|----------|------------|
| 大厂 | 京东、字节、腾讯 | LangChain 1.0 + RAG + Tool Calling |
| AI 初创 | MiniMax、月之暗面 | Agent 架构 + 多 Agent 协作 |
| 传统企业数字化 | 各类转型企业 | 工具集成 + API 对接 |

### 核心技能要求（从招聘 JD 提取）

| 技能类别 | 具体要求 | 优先级 | 当前状态 |
|----------|----------|--------|----------|
| Python 编程 | 扎实基础 + 异步编程 | ⭐⭐⭐⭐⭐ | 已入门 |
| LangChain/LangGraph | Agent 开发框架 | ⭐⭐⭐⭐⭐ | 已入门 (1.0) |
| RAG 技术 | 向量检索 + 知识库 | ⭐⭐⭐⭐⭐ | 未学习 |
| Tool Calling | 工具定义与调用 | ⭐⭐⭐⭐⭐ | 已入门 |
| Context Engineering | 上下文管理 | ⭐⭐⭐⭐ | 已入门 |
| 向量数据库 | Chroma | ⭐⭐⭐⭐ | 未学习 |
| API 集成 | OpenAPI/MCP | ⭐⭐⭐⭐ | 未学习 |
| 深度学习框架 | PyTorch 基础 | ⭐⭐⭐ | 了解即可 |

---

## 📅 4 个月详细学习计划（2026.03 - 2026.07）

### 第一阶段：基础巩固（第 1-2 周）⚠️ 需更新

**目标**：夯实 Python 基础和 LangChain 核心概念

| 周次 | 学习内容 | 产出物 | 检查点 |
|------|----------|--------|--------|
| 第 1 周 | - Python 异步编程（async/await）<br>- LangChain 1.0 create_agent<br>- ChatModel 深入理解 | 完成 3 个异步调用 Demo | ✅ 已完成 |
| 第 2 周 | - Prompt Template 高级用法<br>- **with_structured_output** (1.0)<br>- 基础 Memory 实现 | 实现带记忆的对话机器人 | ⚠️ 更新中 |

---

### 第二阶段：RAG 核心技术（第 3-6 周）⭐⭐⭐⭐⭐

**目标**：掌握 RAG 全流程，能独立搭建知识库问答系统

| 周次 | 学习内容 | 产出物 | 检查点 |
|------|----------|--------|--------|
| 第 3 周 | - 向量数据库基础（Chroma 1.0）<br>- 文本分块策略<br>- Embedding 原理 | 搭建本地 Chroma 知识库 | ⏳ 待开始 |
| 第 4 周 | - Retriever 配置与优化<br>- 向量检索 + 关键词检索<br>- RAG 基本流程 | 实现文档问答 Demo | ⏳ 待开始 |
| 第 5 周 | - 高级 RAG 技巧（多路召回、重排序）<br>- Rerank 模型使用 | 优化检索准确率 | ⏳ 待开始 |
| 第 6 周 | - RAG 项目实战：个人知识库问答 | 完整 RAG 项目 | ⏳ 待开始 |

---

### 第三阶段：Agent 进阶（第 7-10 周）⭐⭐⭐⭐⭐

**目标**：深入理解 Agent 架构，掌握复杂 Agent 开发

| 周次 | 学习内容 | 产出物 | 检查点 |
|------|----------|--------|--------|
| 第 7 周 | - 自定义 Tool 开发（1.0 @tool）<br>- 工具注册与发现<br>- Tool Calling 深入 | 实现 5+ 个自定义工具 | ⏳ 待开始 |
| 第 8 周 | - LangGraph 状态图<br>- 多节点 Agent 设计<br>- 条件路由 | 实现多步骤工作流 | ⏳ 待开始 |
| 第 9 周 | - Agent 规划能力（ReAct/Plan-and-Execute）<br>- Reflection 机制 | 实现规划型 Agent | ⏳ 待开始 |
| 第 10 周 | - Agent 项目实战：智能助手 | 完整 Agent 项目 | ⏳ 待开始 |

---

### 第四阶段：工程化与多 Agent（第 11-14 周）

**目标**：掌握工程化部署和多 Agent 协作

| 周次 | 学习内容 | 产出物 | 检查点 |
|------|----------|--------|--------|
| 第 11 周 | - FastAPI 后端框架<br>- Agent API 封装<br>- 异步并发处理 | Agent 服务化 Demo | ⏳ 待开始 |
| 第 12 周 | - 多 Agent 协作模式<br>- CrewAI 框架<br>- Agent 通信机制 | 多 Agent 协作 Demo | ⏳ 待开始 |
| 第 13 周 | - MCP 协议基础<br>- 工具集成标准化<br>- OpenAPI 规范 | 实现 MCP 兼容工具 | ⏳ 待开始 |
| 第 14 周 | - 综合项目设计与开发 | 完整工程项目 | ⏳ 待开始 |

---

### 第五阶段：求职准备（第 15-16 周）

**目标**：完善简历、准备面试、投递实习

| 周次 | 学习内容 | 产出物 | 检查点 |
|------|----------|--------|--------|
| 第 15 周 | - 简历优化<br>- 项目文档完善<br>- GitHub 整理 | 简历终稿 + GitHub 主页 | ⏳ 待开始 |
| 第 16 周 | - 面试题刷题（算法 + 八股）<br>- Mock Interview<br>- 开始投递 | 面试题库 + 投递记录 | ⏳ 待开始 |

---

## 🏆 核心项目清单（面试用）

| 项目 | 技术栈 | 难度 | 优先级 | 状态 |
|------|--------|------|--------|------|
| RAG 知识库问答 | Chroma + LangChain 1.0 + Embedding | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 待开发 |
| 智能数据分析 Agent | LangGraph + Pandas | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 待开发 |
| 多 Agent 协作系统 | CrewAI/LangGraph | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 待开发 |
| MCP 工具集 | MCP 协议 + FastAPI | ⭐⭐⭐ | ⭐⭐⭐ | 待开发 |

---

## 📚 学习资源汇总

### 文档与教程
| 资源 | 链接 | 说明 |
|------|------|------|
| LangChain 1.0 官方文档 | https://docs.langchain.com/ | **使用此链接** |
| LangGraph 文档 | https://langchain-ai.github.io/langgraph/ | 必学 |
| CrewAI 文档 | https://docs.crewai.com/ | 多 Agent 框架 |
| Chroma 文档 | https://docs.trychroma.com/ | 向量数据库 |

### 视频课程
| 资源 | 平台 | 说明 |
|------|------|------|
| LangChain 中文教程 | B 站 | 中文入门首选 |
| 大模型 Agent 开发实战 | B 站/慕课 | 项目导向 |

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
| 第一阶段：基础巩固 | 第 1-2 周 | ⚠️ 第 1 周已完成，第 2 周更新中 |
| 第二阶段：RAG 核心 | 第 3-6 周 | ⏳ 待开始 |
| 第三阶段：Agent 进阶 | 第 7-10 周 | ⏳ 待开始 |
| 第四阶段：工程化 | 第 11-14 周 | ⏳ 待开始 |
| 第五阶段：求职准备 | 第 15-16 周 | ⏳ 待开始 |

### 本周任务（第 2 周）- 更新

- [x] ChatPromptTemplate 基础
- [x] FewShotChatMessagePromptTemplate
- [x] Output Parser 更新到 1.0 推荐方式
- [x] 添加 ToolStrategy 实战
- [ ] 整理 LangChain 1.0 笔记

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
*下次更新：每周一更新进度追踪*