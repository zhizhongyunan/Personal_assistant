# 第二周面试复习清单 - ChatPromptTemplate + FewShot + Output Parser

## 📅 复习时间安排

| 时间 | 内容 | 目标 |
|------|------|------|
| 第 1 天 | ChatPromptTemplate 基础 | 理解概念，能口述 |
| 第 2 天 | FewShotPromptTemplate | 能手写代码 |
| 第 3 天 | Output Parser 详解 | 理解原理，能延伸讨论 |
| 第 4 天 | 综合练习 | 30 分钟内完成综合任务 |

---

## ✅ 复习清单

### 基础题（必须掌握）

- [ ] Q1: ChatPromptTemplate 和 PromptTemplate 的区别
- [ ] Q2: MessagesPlaceholder 的作用是什么
- [ ] Q3: 如何在 ChatPromptTemplate 中添加变量
- [ ] Q4: format_messages() 和 format() 的区别
- [ ] Q5: FewShot 示例的核心价值是什么
- [ ] Q6: example_prompt 和 examples 的关系
- [ ] Q7: Output Parser 的作用是什么
- [ ] Q8: StrOutputParser 和 PydanticOutputParser 的区别
- [ ] Q9: 如何在 Prompt 中添加输出格式指引
- [ ] Q10: 什么时候需要使用 FewShot

**检查标准**：能盖住答案口述，能在 IDE 中手写

---

### 中阶题（拉开差距）

- [ ] Q11: ChatPromptTemplate 组合多个子 Prompt 的方法
- [ ] Q12: FewShotChatMessagePromptTemplate 的完整使用流程
- [ ] Q13: 如何自定义 Output Parser
- [ ] Q14: PydanticOutputParser 的 format_instructions() 如何使用
- [ ] Q15: 如何处理 OutputParserException 异常
- [ ] Q16: OutputFixingParser 的工作原理
- [ ] Q17: with_structured_output() 和 PydanticOutputParser 的区别
- [ ] Q18: 如何确保 LLM 输出正确的 JSON 格式
- [ ] Q19: 流式输出如何处理
- [ ] Q20: FewShot + Output Parser 组合使用的场景

**检查标准**：能不看书写出完整代码

---

### 高阶题（加分项）

- [ ] Q21: Output Parser 的底层 Runnable 实现原理
- [ ] Q22: 如何处理复杂嵌套结构的解析
- [ ] Q23: Pydantic v2 和 v1 在 Output Parser 中的区别
- [ ] Q24: 多步骤输出解析的设计思路
- [ ] Q25: 从网页内容提取结构化信息的完整流程

**检查标准**：能说出核心思路，能延伸讨论

---

## 🎯 代码手写练习

### 练习 1：基础 ChatPromptTemplate（10 分钟）

```python
# 任务：创建一个带历史记忆的对话 prompt
# 要求：system + 历史消息 + 用户问题
# 变量：topic(专业领域), history(对话历史), question(用户问题)

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 你的代码写在这里


```

---

### 练习 2：FewShotChatMessagePromptTemplate（15 分钟）

```python
# 任务：创建一个 FewShot 对话 prompt
# 要求：至少 2 个示例，示例包含 user 和 ai 对话

from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate

examples = [...]  # 定义示例

example_prompt = ...  # 定义示例模板

fewshot = ...  # 创建 FewShot prompt

# 组合使用
final_prompt = ...

```

---

### 练习 3：综合任务 - 带 FewShot 的专业问答助手（30 分钟）

```python
# 任务：创建一个医疗问答助手
# 要求：
# 1. System 消息：定义角色为医疗专家
# 2. FewShot 示例：3 个医疗问答示例
# 3. MessagesPlaceholder：支持对话历史
# 4. Output Parser：使用 PydanticOutputParser 输出结构化数据
# 5. 输出结构：answer(答案), confidence(置信度 0-1), references(参考文献列表)

from langchain_core.prompts import (
    ChatPromptTemplate,
    MessagesPlaceholder,
    FewShotChatMessagePromptTemplate
)
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

# 定义输出结构
class MedicalAnswer(BaseModel):
    answer: str = Field(description="医疗建议")
    confidence: float = Field(description="置信度，0-1 之间")
    references: list[str] = Field(description="参考文献或来源")

# 1. 定义 FewShot 示例（3 个医疗问答）
examples = [...]


# 2. 定义示例模板
example_prompt = ...


# 3. 创建 FewShot prompt
fewshot = ...


# 4. 创建 Output Parser
parser = ...


# 5. 创建最终 prompt（包含 system + fewshot + history + user）
final_prompt = ...


# 6. 测试调用
messages = final_prompt.format_messages(
    history=[...],
    question="..."
)

```

---

### 练习 4：自定义 Output Parser（20 分钟）

```python
# 任务：自定义一个提取第一个句子的 Output Parser
# 要求：继承 StrOutputParser，重写 parse() 方法

from langchain_core.output_parsers import StrOutputParser

class FirstSentenceParser(StrOutputParser):
    # 你的代码写在这里
    pass


# 测试你的 parser
# chain = prompt | model | FirstSentenceParser()
# result = await chain.ainvoke({"question": "什么是 Python？"})

```

---

### 练习 5：JSON 格式输出（15 分钟）

```python
# 任务：使用 JsonOutputParser 解析 LLM 输出
# 要求：输出为 dict 格式，包含 name, age, hobby 三个字段

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate

parser = ...

prompt = ...

chain = ...

# result = await chain.ainvoke({...})
# 验证：assert isinstance(result, dict)
# 验证：assert "name" in result

```

---

## 📊 自测评分表

| 模块 | 满分 | 你的得分 | 达标线 |
|------|------|----------|--------|
| 基础题（Q1-Q10） | 25 分 | | 20 分 |
| 中阶题（Q11-Q20） | 35 分 | | 25 分 |
| 高阶题（Q21-Q25） | 25 分 | | 15 分 |
| 代码手写（5 题） | 15 分 | | 10 分 |
| **总计** | **100 分** | | **70 分** |

---

## 🔗 相关资源

| 文件 | 说明 |
|------|------|
| `questions.md` | 本文件 - 只有题目 |
| `README.md` | 完整题库 + 答案 |
| `code_examples.py` | 可运行代码示例 |
| `week2/prompt_practice.py` | 你自己的实践代码 |

---

*最后更新：2026-03-08*
