# LangChain 1.0 掌握程度自测表（2026 最新版）

> **使用说明**：每学完一个知识点，对照下表自测。能独立写出✅标记的代码才算真正掌握。

---

## 📊 掌握程度分级

| 等级 | 标准 | 自测方法 | 面试要求 |
|------|------|----------|----------|
| **了解** | 能说出概念和用途 | 看文档能看懂 | 大厂八股文 |
| **会用** | 能照着文档写代码 | 离开文档能写出 50% | 大厂笔试 |
| **掌握** | 知道何时用、如何组合 | 能独立设计项目 | 面试 + 实战 |

---

## 1️⃣ Context Schema (TypedDict)

### 自测题目
- [ ] **了解**: 能说出 `context_schema` 和 `State` 的区别
- [ ] **会用**: 能定义一个 TypedDict 作为 context_schema
- [ ] **掌握**: 知道何时用它而不是直接传 state

### 代码自测（不看文档写出以下代码）
```python
# ✅ 任务：定义一个用户上下文，包含 user_id 和 preferences
from typing import TypedDict

class UserContext(TypedDict):
    user_id: str
    preferences: dict

# ✅ 任务：在 create_agent 中使用 context_schema
agent = create_agent(
    model=model,
    tools=tools,
    context_schema=UserContext,  # ← 能写出这行
)

# ✅ 任务：在 invoke 时传入 context
result = agent.invoke(
    {"messages": [...]},
    context={"user_id": "123", "preferences": {"lang": "zh"}}  # ← 能写出这行
)
```

### 掌握度评分
| 题目 | 了解 | 会用 | 掌握 |
|------|------|------|------|
| 定义 TypedDict | ⬜ | ⬜ | ⬜ |
| 在 agent 中使用 | ⬜ | ⬜ | ⬜ |
| 在 invoke 中传入 | ⬜ | ⬜ | ⬜ |

---

## 2️⃣ Structured Output (ToolStrategy / with_structured_output)

### 自测题目
- [ ] **了解**: 能说出 `with_structured_output` 和 `PydanticOutputParser` 的区别
- [ ] **会用**: 能定义 Pydantic 模型并绑定到 agent
- [ ] **掌握**: 知道何时用 `ToolStrategy` 何时用 `ProviderStrategy`

### 代码自测
```python
from pydantic import BaseModel, Field
from langchain.agents.structured_output import ToolStrategy

# ✅ 任务：定义一个结构化输出模型
class TaskResult(BaseModel):
    task: str = Field(description="任务名称")
    status: str
    priority: int = Field(ge=1, le=5)

# ✅ 任务：在 create_agent 中使用 ToolStrategy
agent = create_agent(
    model=model,
    tools=tools,
    response_format=ToolStrategy(TaskResult),  # ← 能写出这行
)

# ✅ 任务：从结果中提取 structured_response
result = agent.invoke({"messages": [...]})
plan = result["structured_response"]  # ← 能写出这行
print(plan.task)  # 访问字段
```

### 掌握度评分
| 题目 | 了解 | 会用 | 掌握 |
|------|------|------|------|
| 定义 Pydantic 模型 | ⬜ | ⬜ | ⬜ |
| 使用 ToolStrategy | ⬜ | ⬜ | ⬜ |
| 提取 structured_response | ⬜ | ⬜ | ⬜ |

---

## 3️⃣ Middleware (中间件)

### 自测题目
- [ ] **了解**: 能说出 6 个钩子函数的触发时机
- [ ] **会用**: 能写一个简单的 Middleware（如日志记录）
- [ ] **掌握**: 能设计解决具体问题的 Middleware（如重试、权限检查）

### 代码自测
```python
from langchain.agents.middleware import AgentMiddleware, wrap_tool_call

# ✅ 任务：定义一个 Middleware 类
class LoggingMiddleware(AgentMiddleware):

    # ✅ before_model 钩子
    def before_model(self, state, runtime):
        print(f"消息数：{len(state['messages'])}")

    # ✅ after_model 钩子
    def after_model(self, response, runtime):
        print(f"响应：{response.message.content[:50]}")

    # ✅ wrap_tool_call 钩子（用装饰器）
    @wrap_tool_call
    def log_tools(self, request, handler):
        print(f"调用工具：{request.tool_call['name']}")
        return handler(request)  # ← 能写出这行

# ✅ 任务：在 create_agent 中使用 middleware
agent = create_agent(
    model=model,
    tools=tools,
    middleware=[LoggingMiddleware()],  # ← 能写出这行
)
```

### 掌握度评分
| 题目 | 了解 | 会用 | 掌握 |
|------|------|------|------|
| 知道 6 个钩子时机 | ⬜ | ⬜ | ⬜ |
| 写出 before_model | ⬜ | ⬜ | ⬜ |
| 写出 after_model | ⬜ | ⬜ | ⬜ |
| 写出 wrap_tool_call | ⬜ | ⬜ | ⬜ |
| 在 agent 中使用 | ⬜ | ⬜ | ⬜ |

---

## 4️⃣ 工具定义 (@tool)

### 自测题目
- [ ] **了解**: 知道 `@tool` 装饰器的作用
- [ ] **会用**: 能定义一个简单的工具函数
- [ ] **掌握**: 知道如何写 docstring 让模型理解工具用途

### 代码自测
```python
from langchain.tools import tool

# ✅ 任务：定义一个带 docstring 的工具
@tool
def get_weather(city: str) -> str:
    """获取城市的天气信息

    Args:
        city: 城市名称

    Returns:
        天气信息字符串
    """
    return f"{city} 今天晴朗，25°C"

# ✅ 任务：在 create_agent 中注册工具
agent = create_agent(
    model=model,
    tools=[get_weather],  # ← 能写出这行
)
```

### 掌握度评分
| 题目 | 了解 | 会用 | 掌握 |
|------|------|------|------|
| 使用 @tool 装饰器 | ⬜ | ⬜ | ⬜ |
| 写出带 docstring 的工具 | ⬜ | ⬜ | ⬜ |
| 在 agent 中注册 | ⬜ | ⬜ | ⬜ |

---

## 5️⃣ create_agent 完整使用

### 自测题目
- [ ] **了解**: 知道 `create_agent` 的最小必要参数
- [ ] **会用**: 能独立创建一个能跑的 agent
- [ ] **掌握**: 知道如何组合 middleware、tools、response_format

### 代码自测（不看文档写出完整代码）
```python
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from pydantic import BaseModel
from langchain.agents.structured_output import ToolStrategy
from typing import TypedDict

# 1. 定义工具
@tool
def search(query: str) -> str:
    """搜索信息"""
    return f"搜索结果：{query}"

# 2. 定义结构化输出
class SearchResult(BaseModel):
    query: str
    results: list

# 3. 定义 context schema
class Context(TypedDict):
    user_id: str

# 4. 创建 agent
agent = create_agent(
    model=ChatOpenAI(model="gpt-4"),
    tools=[search],
    response_format=ToolStrategy(SearchResult),
    context_schema=Context,
)

# 5. 调用
result = agent.invoke(
    {"messages": [{"role": "user", "content": "搜索 AI 新闻"}]},
    context={"user_id": "123"}
)
```

### 掌握度评分
| 题目 | 了解 | 会用 | 掌握 |
|------|------|------|------|
| 定义工具 | ⬜ | ⬜ | ⬜ |
| 定义 Pydantic 模型 | ⬜ | ⬜ | ⬜ |
| 定义 TypedDict | ⬜ | ⬜ | ⬜ |
| 创建 agent | ⬜ | ⬜ | ⬜ |
| 调用 agent | ⬜ | ⬜ | ⬜ |

---

## 📈 总体掌握度评估

### 评分标准
- **了解**: 3 个以下 ⬜ → 需要复习概念
- **会用**: 3-5 个 ⬜ → 可以做简单项目
- **掌握**: 全部 ⬜ → 可以应对面试

### 你的当前状态（完成 output_practice.py 后）

| 知识点 | 当前状态 |
|--------|----------|
| Context Schema | ⬜ 了解 ⬜ 会用 ⬜ 掌握 |
| Structured Output | ⬜ 了解 ⬜ 会用 ⬜ 掌握 |
| Middleware | ⬜ 了解 ⬜ 会用 ⬜ 掌握 |
| 工具定义 | ⬜ 了解 ⬜ 会用 ⬜ 掌握 |
| create_agent | ⬜ 了解 ⬜ 会用 ⬜ 掌握 |

---

## 🎯 下一步建议

### 如果大部分是「了解」
→ 做一遍 `output_practice.py`，照着代码敲一遍

### 如果大部分是「会用」
→ 尝试独立写一个完整项目（不参照文档）

### 如果大部分是「掌握」
→ 开始 RAG 核心技术学习（第 4 周内容）

---

## 📝 面试代码题模拟

### 题目 1：写一个带重试的 Middleware（字节面试题）
```python
# 要求：工具调用失败时自动重试 3 次
from langchain.agents.middleware import AgentMiddleware, wrap_tool_call
from langchain_core.messages import ToolMessage

class RetryMiddleware(AgentMiddleware):
    @wrap_tool_call
    def retry(self, request, handler):
        # 写出实现代码
        pass
```

### 题目 2：用 Structured Output 返回结构化数据（腾讯面试题）
```python
# 要求：定义一个 Pydantic 模型，返回包含 title、author、summary 的结构
from pydantic import BaseModel, Field

# 写出模型定义
class ArticleSummary(BaseModel):
    pass
```

---

*更新于：2026-03-09*
*使用方法：每学完一个知识点，对照此表自测*
