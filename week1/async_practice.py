from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dataclasses import dataclass
from langchain.tools import tool
import asyncio

System_prompt = """
你是一个工具测试者，根据用户传入的任务id，调用工具返回结果"""

@tool
async def test_tool(id: int):
    """调用此工具"""
    print(f"{id}任务正在执行")
    if id % 2 == 0:
        raise ValueError(f"{id}任务失败")
    await asyncio.sleep(1)
    print(f"{id}任务执行结束")
    return f"{id}任务成功执行"

@dataclass
class Context:
    """运行上下文信息"""
    user_id: str

agent = create_agent(
    model = ChatOpenAI(
        model = "deepseek-chat",
        base_url="https://api.deepseek.com/v1",
        api_key="sk-eacd3a82b8e3491d888df3ef213e442e",
    ),
    tools = [test_tool],
    context_schema = Context,
    system_prompt = System_prompt
)


async def task_handler(question: str):
    try:
        result = await asyncio.wait_for(
            agent.ainvoke({"messages":[{"role":"user", "content":question}]}, ), 
            timeout = 5
        )
        return result
    except asyncio.TimeoutError:
        return "执行失败"


async def main():
    questions = [f"任务id{id}" for id in range(1, 6)]
    semaphore = asyncio.Semaphore(3)
    async with semaphore:
        result = await asyncio.gather(*[task_handler(question) for question in questions], return_exceptions=True)
        for i in range(len(result)):
            if isinstance(result[i], Exception) or isinstance(result[i], str):
                print(f"执行失败: ")
            else:
                print(result[i]["messages"][-1].content)

asyncio.run(main())