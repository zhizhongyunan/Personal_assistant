# LangChain 1.0 学习计划更新总结（2026-03-09）

## 📋 本次更新概览

基于对 LangChain 官方文档、DEV Community 和招聘市场的最新调研，已完成学习计划的全面更新。

---

## 🔍 调研来源

1. **LangChain 官方文档**: https://docs.langchain.com/
2. **LangChain 1.0 Release**: https://blog.langchain.com/langchain-langgraph-1dot0/
3. **What's new in LangChain v1**: https://docs.langchain.com/oss/python/releases/langchain-v1
4. **DEV Community - AI Agents 2026**: Skills Required for Building AI Agents in 2026
5. **MCP 文档**: https://modelcontextprotocol.io/

---

## ⚠️ 关键技术更新（必须掌握）

### 1. LangChain 1.0 核心变化

| 变化项 | 旧版本 (0.x) | 新版本 (1.0+) | 影响 |
|--------|--------------|---------------|------|
| Agent 创建 | `create_react_agent` | `create_agent` | ⭐⭐⭐⭐⭐ |
| 结构化输出 | `PydanticOutputParser` | `with_structured_output` | ⭐⭐⭐⭐⭐ |
| Response Format | 无 | `ToolStrategy`/`ProviderStrategy` | ⭐⭐⭐⭐⭐ |
| Middleware | 无 | 6 个钩子函数 | ⭐⭐⭐⭐⭐ |
| Context Schema | Pydantic | 仅 TypedDict | ⭐⭐⭐⭐ |
| Content Blocks | 无 | `content_blocks` 属性 | ⭐⭐⭐⭐ |
| 包结构 | 统一包 | 拆分 + langchain-classic | ⭐⭐⭐ |
| Python 版本 | 3.9+ | 3.10+ | ⭐⭐ |

### 2. 2026 年技能优先级变化

**新晋热门技能**：
- **Context Engineering** ⭐⭐⭐⭐⭐ (上下文设计)
- **MCP (Model Context Protocol)** ⭐⭐⭐⭐⭐ (模型上下文协议)
- **Human-in-the-loop** ⭐⭐⭐⭐ (人机回环)
- **多 Agent 编排** ⭐⭐⭐⭐ (并行/串行/Coordinator)

**重要性下降**：
- 手写 LangGraph StateGraph ⭐⭐⭐ (仅高级场景使用)
- 深度学习框架 ⭐⭐ (了解即可)

### 3. 五大核心软技能（DEV Community 2026 调研）

1. **Problem Shaping** - 将模糊需求分解为可执行任务
2. **Context Design** - 设计高质量的信息注入
3. **Aesthetic Judgment** - 判断什么值得构建
4. **Agent Orchestration** - 知道何时用单 Agent/多 Agent/并行/串行
5. **Knowing When NOT to Use Agent** - 知道何时不用 Agent

---

## 📁 更新的文件

| 文件 | 更新内容 |
|------|----------|
| `CLAUDE.md` | 完整更新学习计划、技能要求、LangChain 1.0 特性 |
| `week2/interview/answers.md` | 新增 Q10-Q18 详细答案（LangChain 1.0 核心考点） |

---

## 📅 更新后的学习计划

### 第一阶段：LangChain 1.0 核心（第 1-3 周）
- ✅ 第 1 周：异步编程 + `create_agent`
- ✅ 第 2 周：Prompt + Content Blocks + Structured Output
- ⏳ 第 3 周：**Middleware 专题**（重点）

### 第二阶段：RAG 核心（第 4-7 周）
- 第 4 周：向量数据库 + Embedding
- 第 5 周：Retriever + Hybrid Search
- 第 6 周：高级 RAG（Rerank、多路召回）
- 第 7 周：RAG 项目实战

### 第三阶段：Agent 进阶（第 8-11 周）
- 第 8 周：自定义 Tool + 动态 Tool 注册
- 第 9 周：**Context Engineering**
- 第 10 周：**多 Agent 编排**
- 第 11 周：规划型 Agent + Reflection

### 第四阶段：MCP 与工程化（第 12-15 周）
- 第 12 周：**MCP 协议基础**
- 第 13 周：FastAPI + Agent 服务化
- 第 14 周：LangGraph StateGraph（高级场景）
- 第 15 周：综合项目

### 第五阶段：求职准备（第 16-17 周）
- 第 16 周：简历 + GitHub
- 第 17 周：面试刷题 + Mock Interview

---

## 🎯 面试必考点（Q10-Q18 答案已更新）

| 题号 | 考点 | 核心答案 |
|------|------|----------|
| Q10 | `with_structured_output` vs `PydanticOutputParser` | API 硬约束 vs Prompt 软约束 |
| Q11 | `ToolStrategy` 是什么 | 通过 Tool 调用生成结构化输出 |
| Q12 | Middleware 位置和应用 | 6 个钩子函数，敏感词过滤/重试/日志 |
| Q13 | `context_schema` vs State | 业务上下文 vs 对话状态，TypedDict |
| Q14 | OutputParserException 处理 | `ToolStrategy` 内置自动重试 |
| Q15 | Human-in-the-loop 实现 | `HumanInTheLoopMiddleware` |
| Q16 | 动态 Few-Shot | VectorStore 检索相似示例注入 |
| Q17 | 降级策略 | `function_calling` 模式 |
| Q18 | MCP 作用 | 解决 N×M 集成问题，标准化工具定义 |

---

## 💡 关键洞察

### 1. LangChain 1.0 的设计哲学
- **精简核心**：将 Legacy 功能移入 `langchain-classic`
- **Middleware 优先**：提供细粒度控制能力
- **Provider 原生支持**：优先使用模型提供商的原生 API

### 2. 2026 年 AI Agent 开发趋势
- **Context Engineering** 成为核心竞争力
- **MCP 协议** 正在成为事实标准
- **Human-in-the-loop** 成为企业级应用标配
- **多 Agent 编排** 是复杂场景的必然选择

### 3. 学习建议
- **优先掌握**：`create_agent` + Middleware + Context Schema
- **了解即可**：手写 StateGraph（仅高级场景）
- **必须实践**：至少 3 个完整项目（RAG、Agent、MCP）

---

## 📚 推荐学习资源

### 必读官方文档
1. [LangChain 1.0 Release Notes](https://docs.langchain.com/oss/python/releases/langchain-v1)
2. [Middleware Guide](https://docs.langchain.com/oss/python/langchain/middleware)
3. [Agents Documentation](https://docs.langchain.com/oss/python/langchain/agents)
4. [MCP Documentation](https://modelcontextprotocol.io/)

### 技术博客
1. [LangChain Blog](https://blog.langchain.com/)
2. [DEV Community - AI Agents](https://dev.to/t/aiagents)

---

## ✅ 下一步行动

### 本周任务（第 3 周 - Middleware 专题）
- [ ] 理解 Middleware 6 个钩子函数
- [ ] 实现 `HumanInTheLoopMiddleware`
- [ ] 实现 `SummarizationMiddleware`
- [ ] 实现自定义 Middleware（敏感词过滤）
- [ ] 整理 Middleware 笔记

### 本月目标
- [ ] 完成 LangChain 1.0 核心特性学习
- [ ] 实现一个带 Middleware 的 Agent Demo
- [ ] 开始 RAG 核心技术学习

---

*创建时间：2026-03-09*
*版本：2026 最新版*
*下次更新：2026-03-16（周一更新进度）*
