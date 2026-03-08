"""
第二周面试代码练习题 - Output Parser 专题

包含所有高频面试题的代码实现，可直接运行验证
"""
import asyncio
from pydantic import BaseModel, Field
from langchain_core.output_parsers import (
    StrOutputParser,
    PydanticOutputParser,
    JsonOutputParser,
    CommaSeparatedListOutputParser,
    NumberedListOutputParser,
    DatetimeOutputParser,
)
from langchain_core.prompts import ChatPromptTemplate


# ============================================
# 基础题练习
# ============================================

# Q1-Q3: 基础 Output Parser 用法
async def basic_output_parser_example():
    """
    StrOutputParser - 最简单的输出解析器
    将 LLM 输出转换为字符串
    """
    # 定义简单 prompt
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个助手"),
        ("user", "{question}")
    ])

    # 链式调用
    # chain = prompt | model | StrOutputParser()
    # result = await chain.ainvoke({"question": "你是谁？"})

    print("StrOutputParser: 将 LLM 输出转换为字符串")


# Q5: with_structured_output 用法
async def structured_output_example():
    """
    使用 ChatModel 的 with_structured_output 方法
    这是 LangChain 1.x 推荐的结构化输出方式
    """

    # 定义输出结构
    class Answer(BaseModel):
        question: str = Field(description="原始问题")
        answer: str = Field(description="详细答案")
        confidence: float = Field(description="置信度 0-1")

    # 使用 with_structured_output
    # model = ChatOpenAI(...)
    # structured_model = model.with_structured_output(Answer)
    # result = await structured_model.ainvoke("Python 中什么是装饰器？")

    print("with_structured_output: 使用 Pydantic 模型定义输出结构")


# ============================================
# 中阶题练习
# ============================================

# Q6: 自定义 Output Parser
class CustomOutputParser(StrOutputParser):
    """
    自定义输出解析器
    示例：提取输出中的第一个句子
    """

    def parse(self, text):
        # 获取第一个句子
        first_sentence = text.split('.')[0].strip()
        return {
            "first_sentence": first_sentence,
            "full_text": text
        }


async def custom_parser_example():
    """使用自定义 Output Parser"""
    # parser = CustomOutputParser()
    # chain = prompt | model | parser
    # result = await chain.ainvoke({"question": "什么是 Python？"})
    print("自定义 Output Parser: 继承 StrOutputParser 并重写 parse 方法")


# Q7: JSON 格式输出
async def json_output_example():
    """JsonOutputParser 用法"""

    parser = JsonOutputParser()

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的助手。{format_instructions}"),
        ("user", "{question}")
    ]).partial(format_instructions=parser.get_format_instructions())

    # chain = prompt | model | parser
    # result = await chain.ainvoke({
    #     "question": "介绍三种 Python 数据类型"
    # })

    print("JsonOutputParser: 解析 JSON 格式输出，返回 dict 或 list")


# Q8: 修复格式错误的输出
async def robust_json_parsing_example():
    """
    处理 LLM 输出格式错误的情况
    使用 retry 或 fallback 机制
    """
    from langchain_core.output_parsers import OutputFixingParser

    # 基础解析器
    base_parser = PydanticOutputParser(pydantic_object=Answer)

    # 添加修复功能
    # from langchain_openai import ChatOpenAI
    # fix_parser = OutputFixingParser.from_llm(
    #     parser=base_parser,
    #     llm=ChatOpenAI()
    # )

    print("OutputFixingParser: 自动修复格式错误的输出")


# Q9: PydanticOutputParser 详解
class ArticleSummary(BaseModel):
    """文章摘要的数据模型"""
    title: str = Field(description="文章标题")
    summary: str = Field(description="文章摘要，100 字以内")
    keywords: list[str] = Field(description="关键词列表")
    reading_time_minutes: int = Field(description="预计阅读时间（分钟）")


async def pydantic_parser_example():
    """PydanticOutputParser 完整示例"""

    parser = PydanticOutputParser(pydantic_object=ArticleSummary)

    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的内容分析助手。{format_instructions}"),
        ("user", "请分析这篇文章：{article}")
    ]).partial(format_instructions=parser.get_format_instructions())

    # chain = prompt | model | parser
    # result = await chain.ainvoke({
    #     "article": "Python 是一种高级编程语言..."
    # })

    print("PydanticOutputParser: 使用 Pydantic 模型定义输出结构")
    print(f"  - 调用 pydantic_object.model_validate() 验证输出")
    print(f"  - 支持 Field 定义字段描述和验证规则")


# Q10: Output Parser + FewShot 组合
async def fewshot_with_parser_example():
    """
    FewShot 示例 + Output Parser 组合
    用于需要格式一致性的场景
    """
    from langchain_core.prompts import FewShotChatMessagePromptTemplate

    # FewShot 示例
    examples = [
        {
            "input": "Python 是什么？",
            "output": '{"type": "definition", "content": "Python 是一种编程语言"}'
        },
        {
            "input": "谁创建了 Python？",
            "output": '{"type": "fact", "content": "Guido van Rossum"}'
        }
    ]

    example_prompt = ChatPromptTemplate.from_messages([
        ("user", "{input}"),
        ("ai", "{output}")
    ])

    fewshot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=examples,
    )

    # 组合使用
    # final_prompt = ChatPromptTemplate.from_messages([
    #     ("system", "请按 JSON 格式回答"),
    #     fewshot_prompt,
    #     ("user", "{question}")
    # ])
    # chain = final_prompt | model | JsonOutputParser()

    print("FewShot + OutputParser: 通过示例让输出格式更稳定")


# ============================================
# 高阶题练习
# ============================================

# Q12: 处理流式输出
async def streaming_output_example():
    """
    流式输出解析
    适用于需要实时显示的场景
    """

    # chain = prompt | model | StrOutputParser()

    # 流式处理
    # async for chunk in chain.astream({"question": "什么是 AI？"}):
    #     print(chunk, end="", flush=True)

    print("流式输出：使用 astream() 方法逐块接收输出")


# Q13: 复杂嵌套结构解析
class NestedResult(BaseModel):
    """嵌套结构示例"""
    overview: str
    details: list[dict[str, str]]
    metadata: dict[str, str]


async def nested_structure_example():
    """处理复杂嵌套结构的 Output Parser"""

    parser = PydanticOutputParser(pydantic_object=NestedResult)

    # prompt 中明确说明格式要求
    prompt = ChatPromptTemplate.from_messages([
        ("system", "请严格按照以下格式输出：{format_instructions}"),
        ("user", "{question}")
    ]).partial(format_instructions=parser.get_format_instructions())

    # chain = prompt | model | parser
    print("嵌套结构：Pydantic 模型支持嵌套 dict、list 等复杂类型")


# Q15: 综合场景 - 多步骤输出解析
async def multi_step_parsing_example():
    """
    综合场景：
    1. 第一步：提取关键信息
    2. 第二步：验证和补充
    3. 第三步：格式化输出
    """

    # 第一步解析
    class ExtractedInfo(BaseModel):
        topic: str
        key_points: list[str]

    # 第二步验证
    class ValidatedResult(BaseModel):
        is_valid: bool
        feedback: str
        final_output: ExtractedInfo | None

    print("多步骤解析：链式调用多个 Output Parser")
    print("  1. 提取信息 → 2. 验证质量 → 3. 格式化输出")


# ============================================
# 运行所有练习
# ============================================

async def main():
    print("=== Output Parser 基础示例 ===")
    await basic_output_parser_example()

    print("\n=== 结构化输出示例 ===")
    await structured_output_example()

    print("\n=== 自定义 Parser 示例 ===")
    await custom_parser_example()

    print("\n=== JSON 输出示例 ===")
    await json_output_example()

    print("\n=== Pydantic Parser 示例 ===")
    await pydantic_parser_example()

    print("\n=== FewShot + Parser 示例 ===")
    await fewshot_with_parser_example()

    print("\n=== 流式输出示例 ===")
    await streaming_output_example()

    print("\n=== 嵌套结构示例 ===")
    await nested_structure_example()

    print("\n=== 多步骤解析示例 ===")
    await multi_step_parsing_example()


if __name__ == "__main__":
    asyncio.run(main())
