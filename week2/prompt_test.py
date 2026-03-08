"""

这里是自测
基础问题
1：ChatPromptTemplate能够传入更多参数，并且可以进行多轮对话，可以构建丰富的提示词，而prompt只能进行 单轮对话
2:MessagesPlaceholder能够在提示词模板中动态传入历史消息，核心是非固定性
3:使用{variable}设置参数名称，在后续的format_messages传入参数
4:format_messages返回的是chatprompt，是能够传入LLM的标准格式，而format只能返回一个字符串，并且会丢失角色信息
5:Fewshot核心是让不准确自然语言变成可视化的结构化格式，让LLM学会如何参考示例进行回答
6:example_prompt用于将examples的键对应到agent定义的user/ai/system等，映射输出
10:需要ai结构化输出或者学习要求的格式，fewshot提供示例，能更大概率获得需要的结果

中阶
11:按顺序填写即可，比如第一个放system的信息，随后填入fewshot，然后传入对话历史，最后放置用户问题即可
prompt = ChatPromptTemplate([("system","你是一个助手"), example_prompt, MessagesPlaceholder(variable_name=""), ("user","今天天气怎么样")])
12:完整使用：首先定义好examples = [{"answer1","你是谁"},{"answer2","我是燕政企的助手"}]
然后使用ChatPromptTemplate([("user", {answer1}),("ai",{answer2})])，保持和前面example的键一致
然后定义fewshotChatMessagestemplate(examples = examples, example_prompt = 上一步的映射,input_variable=["answer1","answer2"]可选)
随后传入ChatMessage即可


"""
# 练习1
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

history = [
    ("user", "你是谁"),
    ("ai", "我是大模型"),
    ("user", "什么是langchain"),
    ("ai", "langchain是一个为LLM开发的框架")
]

prompt = ChatPromptTemplate.from_messages([
    ("system", "你是一个专业的{topic}助手"), 
    MessagesPlaceholder(variable_name = "history"),
    ("user", "{question}")
    ]
)
end_prompt = prompt.format_messages(
    topic = "langchain",
    history = history,
    question = "提示词核心是什么"
)

# 练习2
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate

examples = ([
    {"user":"你是谁", "ai":"主人你好，我是大模型"},
    {"user":"你叫我什么", "ai":"主人，我叫你主人"}
])

example_prompt = ChatPromptTemplate([(
    "user", "{user}"),
    ("ai", "{ai}")
    ])

prompt2 = FewShotChatMessagePromptTemplate(
    examples = examples,
    example_prompt = example_prompt
)

end_prompt2 = ChatPromptTemplate.from_messages([
    ("system","你是个智能助手"),
    prompt2,
    MessagesPlaceholder(variable_name = "history"),
    ("user", "{question}")
])

# 调用
result = end_prompt2.format_messages(
    history = history,
    question = "提示词核心是什么"
)

# 补充 1：format() vs format_messages()
# format() 返回字符串，format_messages() 返回 BaseMessage 列表
print("=== format_messages() 返回类型 ===")
print(type(result))  # <class 'list'>
print(type(result[0]))  # <class 'langchain_core.messages.system.SystemMessage'>

# format() 返回字符串
text_result = end_prompt2.format(
    history=[{"role": "user", "content": "你好"}],  # format() 需要 dict 格式的历史
    question = "测试"
)
print("=== format() 返回类型 ===")
print(type(text_result))  # <class 'str'>
print(text_result)

# 补充 2：input_variables 什么时候需要？
# 当 FewShotChatMessagePromptTemplate 无法自动推断时，需要手动指定
prompt3 = FewShotChatMessagePromptTemplate(
    examples = examples,
    example_prompt = example_prompt,
    input_variables = ["history", "question"]  # 可选：当自动推断失败时添加
)

print("=== 完成！可以进入 Output Parser 了 ===")

