from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, FewShotChatMessagePromptTemplate



history = [("user","langchain是什么"), ("ai","langchain是一个为大模型开发提供的框架")]


examples = [{"user":"langchain是什么","ai":"燕政奇你好，langchain是一个为LLM开发的框架"}]

examples_prompt = ChatPromptTemplate.from_messages(
    [("user", "{user}"),("ai", "{ai}")]
)

shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt = examples_prompt,
    examples = examples,
    input_variables=["user", "ai"]
)

prompt = ChatPromptTemplate.from_messages(
    [(
        "system", "你是{topic}领域的专家"
    ),
    shot_prompt,
    MessagesPlaceholder(variable_name="history"),
    ("user", "{question}")]
)

messages = prompt.format_messages(topic = "编程", history = history ,question = "1+1等于多少")

for i, msg in enumerate(messages):
    print(f"i:{i}, msg:{msg.content}, type:{msg.type}")
