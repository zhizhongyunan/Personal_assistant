# LangChain 1.0 面试题库（2026 最新版）

---

## 🟢 基础题 (必须掌握 - 核心概念)
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

---

## 🟡 中阶题 (拉开差距 - 实战与原理)
> **检查标准**: 能不看书写出完整代码片段，解释清楚执行流程。

### Q10: `with_structured_output()` 和 `PydanticOutputParser` 的底层实现区别？

**答案**：

| 对比维度 | `with_structured_output()` | `PydanticOutputParser` |
|----------|---------------------------|------------------------|
| **约束方式** | API 硬约束（Provider 原生支持） | Prompt 软约束（注入指令） |
| **实现位置** | 模型层（Model-level） | 输出解析层（Parser-level） |
| **可靠性** | 高（Provider 保证格式） | 中（依赖模型遵循指令） |
| **额外调用** | 无 | 无（但可能解析失败） |
| **兼容性** | 需 Provider 支持 | 通用（所有模型） |
| **LangChain 版本** | 1.0+ 推荐 | 已移入 `langchain-classic` |

**底层原理**：

```python
# with_structured_output() - API 硬约束
# 直接将 Pydantic Schema 转换为 Provider 的 structured output API
# OpenAI: response_format={"type": "json_schema", "json_schema": {...}}
# Anthropic: tool definition 注入
model = ChatOpenAI(model="gpt-4").with_structured_output(Person)
# Provider 在 API 层保证返回符合 schema 的 JSON

# PydanticOutputParser - Prompt 软约束
# 将 Pydantic Schema 转换为 Prompt 指令注入
parser = PydanticOutputParser(pydantic_object=Person)
prompt = ChatPromptTemplate.from_messages([
    ("user", "提取信息\n{format_instructions}"),
    ("user", "{input}")
]).partial(format_instructions=parser.get_format_instructions())
# 依赖模型遵循指令生成 JSON，可能格式错误
```

**何时使用**：
- ✅ `with_structured_output()`：Provider 支持时首选（OpenAI GPT-4+、Anthropic Claude）
- ✅ `PydanticOutputParser`：仅在不支持 structured output 的模型时使用（降级方案）

---

### Q11: `create_agent` 中的 `response_format=ToolStrategy(...)` 是什么意思？与直接返回 JSON 有什么区别？

**答案**：

**ToolStrategy**：通过人工定义的 Tool 调用来生成结构化输出，适用于所有支持 Tool Calling 的模型。

```python
from pydantic import BaseModel
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy

class Weather(BaseModel):
    temperature: float
    condition: str

def weather_tool(city: str) -> str:
    """Get weather for a city"""
    return f"Sunny, 25°C in {city}"

agent = create_agent(
    model="gpt-4.1-mini",
    tools=[weather_tool],
    response_format=ToolStrategy(Weather)
)

result = agent.invoke({
    "messages": [{"role": "user", "content": "What's the weather in SF?"}]
})
print(result["structured_response"])  # Weather(temperature=25.0, condition='Sunny')
```

**与直接返回 JSON 的区别**：

| 对比项 | `ToolStrategy` | 直接返回 JSON |
|--------|---------------|--------------|
| **实现方式** | 通过 Tool 定义注入 schema | Prompt 指令要求 JSON 格式 |
| **可靠性** | 高（Tool 调用强制约束） | 中（依赖模型遵循） |
| **适用模型** | 支持 Tool Calling 的模型 | 所有模型 |
| **额外调用** | 无（在主循环内完成） | 无 |
| **错误处理** | 自动重试（可配置） | 需手动处理 |

**ToolStrategy 工作流程**：
1. 将 Pydantic Schema 转换为 Tool 定义
2. 模型调用 Tool 时，参数自动符合 schema
3. 提取 Tool 调用参数作为结构化输出
4. 无需额外 LLM 调用（成本更低）

---

### Q12: **Middleware (中间件)** 在 Agent 执行链路中的位置？请举例说明三个应用场景。

**答案**：

**Middleware 位置**：

```
User Input
    ↓
[before_agent] ← Middleware Hook 1
    ↓
[before_model] ← Middleware Hook 2 (修改 Prompt、Trim 消息)
    ↓
[wrap_model_call] ← Middleware Hook 3 (拦截请求/响应)
    ↓
     Model
    ↓
[after_model] ← Middleware Hook 4 (验证输出、Guardrails)
    ↓
[wrap_tool_call] ← Middleware Hook 5 (拦截工具执行)
    ↓
     Tools
    ↓
[after_agent] ← Middleware Hook 6 (保存结果、清理)
    ↓
User Output
```

**六个钩子函数**：

| Hook | 触发时机 | 典型用途 |
|------|---------|---------|
| `before_agent` | Agent 执行前 | 加载 Memory、验证输入 |
| `before_model` | Model 调用前 | 修改 Prompt、Trim 消息 |
| `wrap_model_call` | 环绕 Model 调用 | 动态模型选择、日志记录 |
| `wrap_tool_call` | 环绕工具执行 | 权限检查、错误处理 |
| `after_model` | Model 响应后 | 内容过滤、格式验证 |
| `after_agent` | Agent 完成后 | 保存结果、清理资源 |

**三个应用场景示例**：

**1. 敏感词过滤（PII Redaction）**：
```python
from langchain.agents.middleware import PIIMiddleware

agent = create_agent(
    model="gpt-4.1",
    tools=[search],
    middleware=[
        PIIMiddleware(
            field="email",
            strategy="redact",  # redact | block | mask
            apply_to_input=True
        )
    ]
)
# 自动识别并脱敏邮箱、手机号、SSN 等
```

**2. 自动重试（Tool Retry）**：
```python
from langchain.agents.middleware import wrap_tool_call

@wrap_tool_call
def retry_middleware(request, handler):
    max_retries = 3
    for i in range(max_retries):
        try:
            return handler(request)
        except Exception as e:
            if i == max_retries - 1:
                raise
            continue
```

**3. 日志记录（Logging）**：
```python
from langchain.agents.middleware import AgentMiddleware
from langchain.agents.middleware.types import ModelRequest, ModelResponse

class LoggingMiddleware(AgentMiddleware):
    def before_model(self, state, runtime):
        logger.info(f"Model called with {len(state['messages'])} messages")

    def after_model(self, response: ModelResponse, runtime):
        logger.info(f"Model response: {response.message.content[:100]}...")
```

---

### Q13: `context_schema` 和传统的 Graph `State` 有什么区别？为什么要将业务上下文分离？

**答案**：

**区别对比**：

| 对比项 | `context_schema` | 传统 Graph `State` |
|--------|------------------|-------------------|
| **用途** | 业务上下文（用户信息、Session） | 对话状态（Messages、临时变量） |
| **生命周期** | 跨 Session 持久化 | 单次执行内有效 |
| **类型定义** | 仅 TypedDict（1.0） | TypedDict（1.0）/ Pydantic（旧版） |
| **访问方式** | `runtime.context` | `state["key"]` |
| **隔离性** | 按 Session 隔离 | 全局共享 |

**为什么要分离**：

1. **关注点分离**：State 关注对话流程，Context 关注业务数据
2. **类型安全**：Context Schema 提供编译时类型检查
3. **跨 Session 持久化**：Context 可在多次调用间保持
4. **权限控制**：Context 可基于用户身份动态注入

**代码示例**：
```python
from typing import TypedDict

# Context Schema - 业务上下文
class Context(TypedDict):
    user_id: str
    user_role: str  # admin | editor | viewer
    session_id: str

# State - 对话状态（由 AgentState 扩展）
class AgentState(TypedDict):
    messages: list

# 在 Middleware 中使用
from langchain.agents.middleware import wrap_tool_call

@wrap_tool_call
def check_permissions(request, handler):
    user_role = request.runtime.context["user_role"]
    if user_role != "admin" and request.tool_call["name"] == "delete_data":
        raise PermissionError("Only admins can delete")
    return handler(request)

agent = create_agent(
    model="gpt-4.1",
    tools=[read_data, write_data, delete_data],
    context_schema=Context
)
```

---

### Q14: 如何处理 `OutputParserException`？在 1.0 中是否有更好的自动修复机制？

**答案**：

**旧版本处理方式**：
```python
from langchain_core.exceptions import OutputParserException

try:
    result = parser.invoke(response)
except OutputParserException as e:
    # 手动重试或返回默认值
    result = default_value
```

**LangChain 1.0 自动修复机制**：

`ToolStrategy` 提供内置的错误处理和自动重试：

```python
from langchain.agents.structured_output import ToolStrategy

agent = create_agent(
    model="gpt-4.1",
    tools=[weather_tool],
    response_format=ToolStrategy(
        schema=Weather,
        handle_errors={
            "parsing_errors": "retry",  # retry | raise | default
            "multiple_tool_calls": "retry"  # 处理模型返回多个 Tool 调用
        }
    )
)
```

**自定义错误处理**：
```python
from langchain.agents.middleware import after_model

@after_model
def fix_parsing_errors(response, runtime):
    try:
        # 尝试解析
        return response
    except OutputParserException:
        # 自动添加修复指令
        runtime.state["messages"].append(
            AIMessage(content="请严格按照 JSON 格式输出")
        )
```

---

### Q15: 如何在 `create_agent` 中实现 **Human-in-the-loop (人机回环)**？

**答案**：

使用 `HumanInTheLoopMiddleware`：

```python
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware

agent = create_agent(
    model="gpt-4.1",
    tools=[read_email, send_email, transfer_money],
    middleware=[
        HumanInTheLoopMiddleware(
            interrupt_on={
                "send_email": {
                    "allowed_decisions": ["approve", "edit", "reject"]
                },
                "transfer_money": {
                    "allowed_decisions": ["approve", "reject"],
                    "condition": lambda state: state["amount"] > 1000  # 超过 1000 需要审批
                }
            }
        )
    ]
)
```

**工作流程**：
1. Agent 决定调用敏感工具（如 `send_email`）
2. Middleware 拦截并暂停执行
3. 等待用户审批（Approve/Edit/Reject）
4. 用户批准后继续执行

**手动实现（理解原理）**：
```python
from langchain.agents.middleware import wrap_tool_call

@wrap_tool_call
def human_approval(request, handler):
    sensitive_tools = {"send_email", "transfer_money"}
    if request.tool_call["name"] in sensitive_tools:
        # 暂停并等待用户输入
        print(f"Waiting for approval: {request.tool_call}")
        user_input = input("Approve? (y/n): ")
        if user_input.lower() != "y":
            raise PermissionError("Tool call rejected by user")
    return handler(request)
```

---

### Q16: 如何实现**动态 Few-Shot**？(结合 VectorStore 检索相似示例注入 Prompt)

**答案**：

**核心思路**：根据用户输入，从 VectorStore 检索最相似的 Few-Shot 示例动态注入。

```python
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.embeddings import FakeEmbeddings
from langchain.agents.middleware import before_model

# 准备 Few-Shot 示例
examples = [
    {"input": "你好", "output": "你好！有什么可以帮助你的？"},
    {"input": "再见", "output": "再见，祝你有美好的一天！"},
]

# 初始化 VectorStore
embeddings = FakeEmbeddings(size=10)
vectorstore = InMemoryVectorStore(embeddings)

# 添加示例到 VectorStore
for ex in examples:
    vectorstore.add_texts([ex["input"]], metadatas=[{"output": ex["output"]}])

# 创建动态 Few-Shot Middleware
class DynamicFewShotMiddleware:
    def __init__(self, vectorstore, k=2):
        self.vectorstore = vectorstore
        self.k = k

    def before_model(self, state, runtime):
        # 获取用户最后一条消息
        last_message = state["messages"][-1].content

        # 检索相似示例
        similar = self.vectorstore.similarity_search_with_score(
            last_message,
            k=self.k
        )

        # 构建 Few-Shot Prompt
        few_shot_text = "以下是几个示例：\n"
        for doc, score in similar:
            few_shot_text += f"输入：{doc.page_content}\n输出：{doc.metadata['output']}\n"

        # 注入到 System Prompt
        state["messages"][0].content += "\n\n" + few_shot_text

# 使用 Middleware
agent = create_agent(
    model="gpt-4.1",
    tools=[],
    middleware=[DynamicFewShotMiddleware(vectorstore, k=2)]
)
```

**优势**：
- 动态选择最相关的示例
- 避免硬编码 Few-Shot
- 支持大规模示例库

---

### Q17: 当模型不支持 `json_schema` (如 DeepSeek 旧版) 时，`with_structured_output` 会自动降级为什么模式？

**答案**：

**自动降级为 `function_calling` 模式**。

**降级策略**：
```python
# with_structured_output 内部逻辑
def with_structured_output(self, schema):
    if self.supports_json_schema():
        # 首选：Provider 原生 JSON Schema
        return self._bind_json_schema(schema)
    elif self.supports_function_calling():
        # 降级：Function Calling
        return self._bind_function_calling(schema)
    else:
        # 最后降级：PydanticOutputParser (Prompt 注入)
        return self._bind_pydantic_parser(schema)
```

**DeepSeek 旧版处理**：
```python
# DeepSeek 旧版不支持 json_schema，但支持 function_calling
model = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com"
).with_structured_output(Person)
# 自动降级为 function_calling 模式
```

**如何检查支持情况**：
```python
from langchain_openai import ChatOpenAI

model = ChatOpenAI(model="gpt-4")
print(model.profile.supports_structured_outputs)  # True/False
print(model.profile.supports_tool_calling)  # True/False
```

---

### Q18: 简述 **MCP (Model Context Protocol)** 在 LangChain 1.0 中的作用。它解决了什么痛点？

**答案**：

**MCP (Model Context Protocol)** 是 2025-2026 年新兴的开放协议，用于标准化 LLM 与外部工具/数据的连接方式。

**核心作用**：

1. **解决 N×M 集成问题**：
   - 传统方式：N 个模型 × M 个工具 = N×M 次集成
   - MCP 方式：N 个模型 + 1 个协议 + M 个工具 = N+M 次集成

2. **标准化工具定义**：
   ```python
   # MCP Server 定义工具（标准化）
   @mcp.tool()
   def search(query: str) -> str:
       """Search the web"""
       return search_result

   # LangChain 通过 MCP Adapter 连接
   from langchain_mcp import MCPToolkit

   mcp_toolkit = MCPToolkit(server_url="http://localhost:8000/sse")
   agent = create_agent(
       model="gpt-4.1",
       tools=mcp_toolkit.get_tools()  # 自动发现 MCP Server 的工具
   )
   ```

3. **解耦模型与工具**：
   - 工具开发者只需实现 MCP Server
   - 模型开发者只需实现 MCP Client
   - 双方通过协议通信

**LangChain 1.0 中的 MCP**：

```python
# LangChain 1.0 提供 MCP Adapter
from langchain_mcp import MCPAdapter

# 连接到 MCP Server
adapter = MCPAdapter("http://localhost:8000/sse")

# 获取工具
tools = adapter.get_tools()

# 创建 Agent
agent = create_agent(
    model="gpt-4.1",
    tools=tools,
    middleware=[
        # 可以使用 Middleware 增强 MCP 工具
    ]
)
```

**解决的痛点**：
| 痛点 | MCP 解决方案 |
|------|------------|
| 工具集成重复造轮子 | 标准化协议，一次实现多处使用 |
| 工具发现困难 | MCP Server 自动暴露工具列表 |
| 认证授权不统一 | MCP 协议内置 Auth 机制 |
| 工具调用格式不兼容 | 统一输入输出格式 |

**为什么重要（2026 趋势）**：
- MCP 正成为 AI Agent 工具集成的**事实标准**
- LangChain、LlamaIndex 等框架已支持 MCP
- 大厂（Microsoft、Google）正在采纳

---

## 🔴 高阶题 (加分项 - 架构与设计)
> **检查标准**: 能设计解决方案，理解源码级逻辑。

- [ ] **Q19**: (新) 设计一个**自定义 Middleware**：要求在所有工具调用前，自动检查用户权限；在所有 LLM 响应后，自动脱敏手机号。写出伪代码。
- [ ] **Q20**: (新) `create_agent` 内部是如何编排 LangGraph 的？它默认使用了哪种 Graph 结构？(ReAct? Plan-and-Execute?)
- [ ] **Q21**: 如何处理**复杂嵌套结构**的结构化输出？(例如：`List[Dict[str, List[int]]]`)，Pydantic 模型该如何定义？
- [ ] **Q22**: (新) 在多线程/异步环境下，`context_schema` 如何保证不同会话之间的数据隔离？
- [ ] **Q23**: 如果 `with_structured_output` 失败了，底层的 **Fallback Strategy** 是如何工作的？
- [ ] **Q24**: (新) 对比 **LangChain 1.0 (`create_agent`)** 和 **LangGraph (手写 StateGraph)** 的适用边界。什么时候必须下沉到手写 LangGraph？
- [ ] **Q25**: (新) 如何利用 **Checkpointer** 实现 Agent 的"时间旅行" (回溯到某一步骤重新执行)？

---

*更新于：2026-03-09*
*版本：LangChain 1.0+ 面试题库 - 2026 最新版*
