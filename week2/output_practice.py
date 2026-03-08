from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser, JsonOutputParser
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain.tools import tool, ToolRuntime
from dataclasses import dataclass
from langchain_core.prompts import ChatPromptTemplate
from langchain.agents.structured_output import ToolStrategy
from pydantic import BaseModel, Field

class Person(BaseModel):
    name: str = Field(description="这是人物 的姓名")
    age: int = Field(description="人物的年龄")
    hobby: str = Field(description="人物的爱好")

parser = PydanticOutputParser(pydantic_object=Person)

parser_information = parser.get_format_instructions()

prompt = ChatPromptTemplate.from_messages([
    ("system", "{format_instruction}"),
    ("user", "{question}")
]
).partial(format_instruction=parser_information)

model = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com/v1",
    api_key="sk-eacd3a82b8e3491d888df3ef213e442e",
)

agent = prompt | model | parser

result = agent.invoke({"question":"给我创建一个人物"})

print(result)

# System_output ="""
#     你是一个全能助手，给我总结文章后，请用json格式返回，字段有title，author，summary
# """

# parser = JsonOutputParser()

# prompt = ChatPromptTemplate([
#     ("system", System_output),
#     ("user", "{question}")
# ]
# )

# model = ChatOpenAI(
#     model="deepseek-chat",
#     base_url="https://api.deepseek.com/v1",
#     api_key="sk-eacd3a82b8e3491d888df3ef213e442e",
# )

# agent = prompt | model | parser
# result = agent.invoke(
#     {
#         "question": "美国知名科技商业媒体The Information近日报道称，阿里巴巴在AI办事领域的进展快于亚马逊和OpenAI。文章评价称，这将又是一个中国科技企业从美国科技公司接过接力棒并加速奔跑的例子，这种情况已多次发生，中国正将AI办事推向新的水平。在OpenAI、谷歌和亚马逊竞相进军AI购物领域之际，阿里巴巴正以更快的步伐展示人工智能体如何演变为个性化的购物助手。报道援引了摩根士丹利本周的一份报告数据：旗下AI助手千问发起的春节营销活动让APP日活从1700万激增至7350万，期间在千问上预订奶茶、电影票机票等各类商品的订单量达2亿。报道称，AI购物存在众多技术挑战，AI需要理解并使用复杂的电商数据，但卖家的产品线、商品库存、价格都在不断变化。近日，OpenAI受限于技术原因，调整了ChatGPT的电商战略，放弃在聊天界面里直接支付并完成交易。“相比亚马逊、谷歌和OpenAI等美国企业，阿里巴巴在应对上述挑战方面具有优势。阿里拥自研大模型、电商平台以及支付系统，旗下还拥有高德地图、在线旅游服务平台飞猪以及票务平台大麦网。如果阿里能打破内部壁垒，将千问与所有业务生态整合，未来将会发挥巨大潜力。”"
#     }
# )
# print(result)

# class Articlesummary(BaseModel):
#     title: str = Field(description="这里是文章的标题")
#     author: str = Field(description="作者")
#     summary: str = Field(description="100字左右的总结")

# parser = PydanticOutputParser(pydantic_object=Articlesummary)
# format_instructions = parser.get_format_instructions()

# System_prompt ="""
# 你是一个智能助手，能够根据用户要求的格式输出结果{format}
# """

# prompt = ChatPromptTemplate.from_messages(
#     [("system", System_prompt), ("user", "总结这篇文章{article}")]
# ).partial(format=format_instructions)

# model = ChatOpenAI(
#     model="deepseek-chat",
#     base_url="https://api.deepseek.com/v1",
#     api_key="sk-eacd3a82b8e3491d888df3ef213e442e",
# )


# agent = prompt | model | parser

# result = agent.invoke({"article": "美国知名科技商业媒体The Information近日报道称，阿里巴巴在AI办事领域的进展快于亚马逊和OpenAI。文章评价称，这将又是一个中国科技企业从美国科技公司接过接力棒并加速奔跑的例子，这种情况已多次发生，中国正将AI办事推向新的水平。在OpenAI、谷歌和亚马逊竞相进军AI购物领域之际，阿里巴巴正以更快的步伐展示人工智能体如何演变为个性化的购物助手。报道援引了摩根士丹利本周的一份报告数据：旗下AI助手千问发起的春节营销活动让APP日活从1700万激增至7350万，期间在千问上预订奶茶、电影票机票等各类商品的订单量达2亿。报道称，AI购物存在众多技术挑战，AI需要理解并使用复杂的电商数据，但卖家的产品线、商品库存、价格都在不断变化。近日，OpenAI受限于技术原因，调整了ChatGPT的电商战略，放弃在聊天界面里直接支付并完成交易。“相比亚马逊、谷歌和OpenAI等美国企业，阿里巴巴在应对上述挑战方面具有优势。阿里拥自研大模型、电商平台以及支付系统，旗下还拥有高德地图、在线旅游服务平台飞猪以及票务平台大麦网。如果阿里能打破内部壁垒，将千问与所有业务生态整合，未来将会发挥巨大潜力。”"})

# print(result.title)
# print(result)
# system_prompt = """
# 你是一个计划规划师，能够根据用户学习了的知识，检索并返回接下来的学习计划，调用工具获取用户已学习内容
# """

# prompt = ChatPromptTemplate.from_messages([
#     ("user", "{question}")
# ])
# @dataclass
# class Context:
#     """
#         running Context
#     """
#     user_id: str
#     memory: str

# @dataclass
# class Response_format:
#     """
#     response_format
#     """
#     result: str
#     resonging: str

# @tool
# def get_user_info(runtime: ToolRuntime[Context]):
#     """
#     获取用户的id和以学习内容"""
#     memory = runtime.context.memory
#     user_id = runtime.context.user_id
#     return f"{user_id}用户的已学习内容是{memory}"


# question = "langchain的输出解析器怎么学"

# agent = create_agent(
#     system_prompt=system_prompt,
#     model=ChatOpenAI(
#         model="deepseek-chat",
#         base_url="https://api.deepseek.com/v1",
#         api_key="sk-eacd3a82b8e3491d888df3ef213e442e",
#     ),
#     tools = [get_user_info],
#     context_schema = Context,
#     response_format = ToolStrategy(Response_format)
# )

# result = agent.invoke({"question":question},context = Context(user_id = "1", memory="用户已经学习了python的异步同步，还有ChatPromptTemplate和fewshot，现在正在学结构化输出Output_parser"))
# print(result["structured_response"])
