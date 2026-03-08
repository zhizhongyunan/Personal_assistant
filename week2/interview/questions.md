#### 🟢 基础题 (必须掌握 - 核心概念)
> **检查标准**: 能口述核心区别，能手写最简代码。

- [ ] **Q1**: `ChatPromptTemplate` 和 `PromptTemplate` 的本质区别是什么？(消息列表 vs 纯字符串)
- [ ] **Q2**: `MessagesPlaceholder` 在多轮对话中起什么作用？为什么不能直接用 `{history}` 变量？
- [ ] **Q3**: 在 LangChain 1.0 中，如何定义一个**结构化输出**的 Pydantic 模型并绑定到 Model？(`with_structured_output`)
- [ ] **Q4**: `format_messages()` 和 `format()` 返回类型的区别？(List[BaseMessage] vs str)
- [ ] **Q5**: Few-Shot Prompting 的核心价值是什么？它主要解决模型的什么问题？
- [ ] **Q6**: Output Parser 的核心职责是什么？(LLM 输出 -> 程序可用对象)
- [ ] **Q7**: 什么时候应该使用 `StrOutputParser`，什么时候必须用 `with_structured_output`？
- [ ] **Q8**: (新) LangChain 1.0 中，`create_agent` 的最小必要参数有哪些？
- [ ] **Q9**: (新) 什么是 **Content Blocks**？它在流式输出中比纯文本流好在哪里？

#### 🟡 中阶题 (拉开差距 - 实战与原理)
> **检查标准**: 能不看书写出完整代码片段，解释清楚执行流程。

- [ ] **Q10**: **核心考点**: `with_structured_output()` 和 `PydanticOutputParser` 的底层实现区别？(API 硬约束 vs Prompt 软约束)
- [ ] **Q11**: (新) `create_agent` 中的 `response_format=ToolStrategy(...)` 是什么意思？它与直接返回 JSON 有什么区别？
- [ ] **Q12**: (新) **Middleware (中间件)** 在 Agent 执行链路中的位置？请举例说明它的三个应用场景 (如：敏感词过滤、自动重试、日志记录)。
- [ ] **Q13**: (新) `context_schema` 和传统的 Graph `State` 有什么区别？为什么要将业务上下文分离？
- [ ] **Q14**: 如何处理 `OutputParserException`？在 1.0 中是否有更好的自动修复机制？
- [ ] **Q15**: 如何在 `create_agent` 中实现 **Human-in-the-loop (人机回环)**？(例如：在执行转账工具前暂停等待人工确认)
- [ ] **Q16**: (更新) 如何实现**动态 Few-Shot**？(结合 VectorStore 检索相似示例注入 Prompt，而非硬编码)
- [ ] **Q17**: 当模型不支持 `json_schema` (如 DeepSeek 旧版) 时，`with_structured_output` 会自动降级为什么模式？(`function_calling`)
- [ ] **Q18**: (新) 简述 **MCP (Model Context Protocol)** 在 LangChain 1.0 中的作用。它解决了什么痛点？

#### 🔴 高阶题 (加分项 - 架构与设计)
> **检查标准**: 能设计解决方案，理解源码级逻辑。

- [ ] **Q19**: (新) 设计一个**自定义 Middleware**：要求在所有工具调用前，自动检查用户权限；在所有 LLM 响应后，自动脱敏手机号。写出伪代码。
- [ ] **Q20**: (新) `create_agent` 内部是如何编排 LangGraph 的？它默认使用了哪种 Graph 结构？(ReAct? Plan-and-Execute?)
- [ ] **Q21**: 如何处理**复杂嵌套结构**的结构化输出？(例如：List[Dict[str, List[int]]])，Pydantic 模型该如何定义？
- [ ] **Q22**: (新) 在多线程/异步环境下，`context_schema` 如何保证不同会话之间的数据隔离？
- [ ] **Q23**: 如果 `with_structured_output` 失败了，底层的 **Fallback Strategy** 是如何工作的？
- [ ] **Q24**: (新) 对比 **LangChain 1.0 (`create_agent`)** 和 **LangGraph (手写 StateGraph)** 的适用边界。什么时候必须下沉到手写 LangGraph？
- [ ] **Q25**: (新) 如何利用 **Checkpointer** 实现 Agent 的“时间旅行” (回溯到某一步骤重新执行)？

---
