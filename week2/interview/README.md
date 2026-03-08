# 第二周面试题整理 - Prompt Template + Output Parser

## 📌 说明

本文件夹整理第二周的面试高频问题，包含：
- **第一部分**：ChatPromptTemplate + FewShot（基础）
- **第二部分**：Output Parser 详解（核心）
- **第三部分**：综合应用（高阶）

---

## 🔹 第一部分：ChatPromptTemplate + FewShot（基础必会）

### Q1: ChatPromptTemplate 和 PromptTemplate 的区别？

**参考答案：**

| 对比项 | `ChatPromptTemplate` | `PromptTemplate` |
|--------|---------------------|------------------|
| 用途 | 对话场景（多消息） | 单文本模板 |
| 消息类型 | system/user/ai 多种角色 | 单一文本模板 |
| 输出 | `PromptValue`（可转消息列表） | 字符串 |

**代码对比：**
```python
# PromptTemplate - 单文本模板
prompt = PromptTemplate.from_template("你好，{name}!")
result = prompt.format(name="张三")  # 返回字符串

# ChatPromptTemplate - 对话模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是助手"),
    ("user", "{question}")
])
result = prompt.format_messages(question="你好")  # 返回消息列表
```

---

### Q2: MessagesPlaceholder 的作用是什么？

**参考答案：**

`MessagesPlaceholder` 用于**动态插入消息列表**，常用于对话历史。

**代码示例：**
```python
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是助手"),
    MessagesPlaceholder(variable_name="history"),  # 动态插入历史消息
    ("user", "{question}")
])

messages = prompt.format_messages(
    history=[("user", "你好"), ("ai", "你好！")],
    question="1+1=?"
)
```

---

### Q3: FewShot 的核心价值是什么？

**参考答案：**

FewShot 通过**提供示例**让 LLM 输出格式更一致，适用于：
1. 需要固定输出格式的场景
2. 复杂任务示范
3. 少样本学习

**代码示例：**
```python
from langchain_core.prompts import FewShotChatMessagePromptTemplate

examples = [
    {"input": "1+1 等于？", "output": "1+1 等于 2"},
    {"input": "2+3 等于？", "output": "2+3 等于 5"},
]

example_prompt = ChatPromptTemplate.from_messages([
    ("user", "{input}"),
    ("ai", "{output}")
])

fewshot = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)
```

---

### Q4: 如何组合 ChatPromptTemplate + FewShot + MessagesPlaceholder？

**参考答案：**

**完整示例：**
```python
from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    FewShotChatMessagePromptTemplate
)

# 1. 定义 FewShot
examples = [...]
example_prompt = ChatPromptTemplate.from_messages([...])
fewshot = FewShotChatMessagePromptTemplate(...)

# 2. 组合最终 prompt
final_prompt = ChatPromptTemplate.from_messages([
    ("system", "你是{topic}专家"),
    fewshot,
    MessagesPlaceholder(variable_name="history"),
    ("user", "{question}")
])

# 3. 调用
messages = final_prompt.format_messages(
    topic="数学",
    history=[...],
    question="..."
)
```

---

## 🔹 第二部分：Output Parser（核心重点）

### Q5: Output Parser 的作用是什么？

**参考答案：**

Output Parser 用于**解析 LLM 的输出**，将其从原始文本转换为结构化格式。

```
LLM 原始输出 → 文本字符串（不易程序处理）
    ↓ Output Parser
结构化数据 → dict/list/Pydantic 模型（易于程序处理）
```

**常见 Output Parser 类型：**
| Parser | 用途 |
|--------|------|
| `StrOutputParser` | 简单字符串输出 |
| `PydanticOutputParser` | Pydantic 模型结构化输出 |
| `JsonOutputParser` | JSON 格式解析 |
| `CommaSeparatedListOutputParser` | 逗号分隔列表解析 |

---

### Q6: StrOutputParser 和 PydanticOutputParser 有什么区别？

**参考答案：**

| 对比项 | `StrOutputParser` | `PydanticOutputParser` |
|--------|------------------|------------------------|
| 输出类型 | `str` | Pydantic 模型实例 |
| 复杂度 | 最简单 | 较复杂 |
| 格式约束 | 无 | 严格（Pydantic 验证） |
| 适用场景 | 对话、文本生成 | 结构化数据提取 |

---

### Q7: 如何在 Prompt 中添加输出格式指引？

**参考答案：**

使用 `format_instructions()` 方法获取格式指引，并添加到 Prompt 中。

**代码示例：**
```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

class Answer(BaseModel):
    question: str = Field(description="问题")
    answer: str = Field(description="答案")

parser = PydanticOutputParser(pydantic_object=Answer)

# 获取格式指引
format_instructions = parser.get_format_instructions()

# 添加到 Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "请严格按照格式输出：{format_instructions}"),
    ("user", "{question}")
]).partial(format_instructions=format_instructions)
```

---

### Q8: OutputParserException 是什么？如何处理？

**参考答案：**

`OutputParserException` 是当 LLM 输出**无法被正确解析**时抛出的异常。

**处理方式：**
```python
from langchain_core.exceptions import OutputParserException
from langchain_core.output_parsers import OutputFixingParser

# 方式 1: try-except
try:
    result = await chain.ainvoke({...})
except OutputParserException as e:
    print(f"解析失败：{e}")

# 方式 2: OutputFixingParser
fix_parser = OutputFixingParser.from_llm(
    parser=base_parser,
    llm=model
)
```

---

### Q9: with_structured_output() 和 PydanticOutputParser 有什么区别？

**参考答案：**

| 对比项 | `with_structured_output()` | `PydanticOutputParser` |
|--------|---------------------------|------------------------|
| 所属 | ChatModel 方法 | 独立 Output Parser |
| 实现方式 | API 原生 structured output | prompt + 解析 |
| 准确率 | 更高（模型原生支持） | 较依赖 prompt |

**推荐使用顺序：**
1. 优先使用 `with_structured_output()`（如果模型支持）
2. 否则使用 `PydanticOutputParser`

---

### Q10: 如何自定义 Output Parser？

**参考答案：**

继承 `StrOutputParser`，重写 `parse()` 方法。

**代码示例：**
```python
from langchain_core.output_parsers import StrOutputParser

class FirstSentenceParser(StrOutputParser):
    """只提取第一个句子的解析器"""

    def parse(self, text: str) -> str:
        first_sentence = text.split('.')[0].strip()
        return first_sentence
```

---

### Q11: 如何确保 LLM 输出正确的 JSON 格式？

**参考答案：**

**方法 1：JsonOutputParser**
```python
parser = JsonOutputParser()
prompt = ChatPromptTemplate.from_messages([
    ("system", "{format_instructions}"),
    ("user", "{question}")
]).partial(format_instructions=parser.get_format_instructions())
```

**方法 2：FewShot 示例**
```python
examples = [
    {"input": "问题 1", "output": '{"key": "value1"}'},
]
```

**方法 3：OutputFixingParser**
```python
fix_parser = OutputFixingParser.from_llm(
    parser=JsonOutputParser(),
    llm=model
)
```

---

## 🔹 第三部分：综合应用（高阶加分）

### Q12: Output Parser 的底层实现原理是什么？

**参考答案：**

Output Parser 是 `Runnable` 接口实现，支持链式调用。

**链式调用流程：**
```python
chain = prompt | model | parser

# 等价于
chain = RunnableSequence(prompt, model, parser)

# 执行流程
result = chain.invoke({...})
# 1. prompt.format() → PromptValue
# 2. model.invoke(PromptValue) → LLM 输出
# 3. parser.parse(LLM 输出) → 最终结果
```

---

### Q13: 如何处理流式输出（Streaming）？

**参考答案：**

**StrOutputParser 流式处理：**
```python
chain = prompt | model | StrOutputParser()

async for chunk in chain.astream({"question": "什么是 AI？"}):
    print(chunk, end="", flush=True)
```

---

### Q14: 如何处理复杂嵌套结构的解析？

**参考答案：**

**使用嵌套 Pydantic 模型：**
```python
from pydantic import BaseModel, Field

class Author(BaseModel):
    name: str
    affiliation: str

class Article(BaseModel):
    title: str
    abstract: str
    authors: list[Author]
    keywords: list[str]

parser = PydanticOutputParser(pydantic_object=Article)
```

---

### Q15: 综合场景：从网页内容提取结构化信息

**参考答案：**

**完整流程：**
```python
from pydantic import BaseModel, Field
from langchain_core.output_parsers import PydanticOutputParser

# 1. 定义数据结构
class ExtractedInfo(BaseModel):
    title: str
    summary: str
    entities: list[str]
    category: str

# 2. 创建解析器
parser = PydanticOutputParser(pydantic_object=ExtractedInfo)

# 3. 构建 Prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "请提取信息：{format_instructions}"),
    ("user", "内容：{content}")
]).partial(format_instructions=parser.get_format_instructions())

# 4. 链式调用
chain = prompt | model | parser
result = await chain.ainvoke({"content": webpage_content})
```

---

## 📚 手写代码练习（30 分钟完成）

### 练习 1：基础 ChatPromptTemplate（10 分钟）

```python
# 任务：创建一个带历史记忆的对话 prompt
# 要求：system + 历史消息 + 用户问题

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 你的代码写在这里


```

---

### 练习 2：FewShot + Output Parser 组合（20 分钟）

```python
# 任务：创建一个医疗问答助手
# 要求：
# 1. System 消息：定义角色为医疗专家
# 2. FewShot 示例：3 个医疗问答示例
# 3. MessagesPlaceholder：支持对话历史
# 4. PydanticOutputParser：输出结构化数据

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    FewShotChatMessagePromptTemplate
)
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

class MedicalAnswer(BaseModel):
    answer: str = Field(description="医疗建议")
    confidence: float = Field(description="置信度，0-1 之间")
    references: list[str] = Field(description="参考文献列表")

# 你的代码写在这里


```

---

## 🎯 面试准备建议

| 优先级 | 内容 | 建议 |
|--------|------|------|
| ⭐⭐⭐⭐⭐ | 基础题 Q1-Q5 | 必须熟练 |
| ⭐⭐⭐⭐⭐ | 中阶题 Q6-Q11 | 能手写代码 |
| ⭐⭐⭐ | 高阶题 Q12-Q15 | 理解思路 |

**复习方法：**
1. 盖住答案，自己口述
2. 在 IDE 中手写代码验证
3. 结合实践代码理解

---

*整理时间：2026-03-08*
*适用范围：AI Agent 开发实习岗*
