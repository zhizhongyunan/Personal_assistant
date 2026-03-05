from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
from langchain.agents.structured_output import ToolStrategy

System_prompt = """
    你是一个计划规划师，能够根据不同用户规划各自的计划

    你有两个工具可以使用
    1. 计划制作：根据指定的要求，制作计划
    2. 用户信息查询：根据用户id查询

    当不明确用户时，调用用户id查询工具获取用户信息，明确用户后调用计划制作工具制作计划
    """


@dataclass
class Context:
    """
    这是运行时上下文模式
    """
    user_id: str
    past: str


@tool
def get_plan(user: str) -> str:
    """
    这是计划制作工具
    """
    return f"{user}的计划制作完成"


@tool
def get_user_info(runtime: ToolRuntime[Context]) -> str:
    """
    这是用户信息查询工具
    """
    user_id = runtime.context.user_id
    past = runtime.context.past
    print(f"正在查看用户信息{past}")
    return "zhangsan" if user_id == "1" else "lisi"

@dataclass
class Response_format:
    """
    这是响应格式化函数
    
    """
    punny: str
    punny_response: str | None = None

model = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com/v1",
    api_key="sk-eacd3a82b8e3491d888df3ef213e442e"
)

checkpointer = InMemorySaver()

agents = create_agent(
    model = model,
    system_prompt = System_prompt,
    context_schema = Context,
    tools = [get_plan, get_user_info],
    response_format = ToolStrategy(Response_format),
    checkpointer = checkpointer,
)

config = {"configurable": {"thread_id": "1"}}


response = agents.invoke(
    {"messages": [{"role": "user", "content": "我之前跟你说过什么"}]},
    config=config,
    context=Context(user_id="2", past="用户之前制定过计划"),
)

print(response['structured_response'])