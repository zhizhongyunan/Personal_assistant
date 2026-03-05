from langchain.agents import create_agent, AgentState
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from dataclasses import dataclass
from langchain.agents.structured_output import ToolStrategy

@tool
def add_tools(a: int, b: int) -> int:
    """计算器"""
    return a + b

model = ChatOpenAI(
    model = 'deepseek-chat',
    base_url = 'https://api.deepseek.com/v1',
    api_key = 'sk-eacd3a82b8e3491d888df3ef213e442e'
)
@dataclass
class ResponseFormat:
    """
    这里是输出格式, result放数值，description放计算公式
    """
    result: int
    description: str


agent = create_agent(
    tools = [add_tools],
    model = model,
    response_format = ToolStrategy(ResponseFormat)
)

response = agent.invoke(
    {"messages":
    [{"role": "user", "content": "计算123 + 456"}]},
)

print(response['structured_response'])