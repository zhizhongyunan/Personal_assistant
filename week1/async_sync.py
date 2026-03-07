# 不要给我补全代码了
import asyncio
from datetime import datetime
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from dataclasses import dataclass
from langchain.tools import tool, ToolRuntime
@tool
async def test_tool(id: int) -> str:
    """
    这是测试工具
    """
    if(id == 5):
        raise ValueError(f"测试工具{id}调用错误")
    await asyncio.sleep(1)
    return f"测试工具{id}调用成功"

@dataclass
class Context:
    """
    这是运行时上下文
    """
    user_id: int



agent = create_agent(
    model = ChatOpenAI(
        base_url="https://api.deepseek.com/v1",
        api_key="sk-eacd3a82b8e3491d888df3ef213e442e",
        model = "deepseek-chat"
    ),
    system_prompt = """你是一个测试助手。      
  当用户说"任务 X"时，你必须调用 test_tool   
  工具，传入参数 id=X。
  例如：用户说"任务 3"，你就调用
  test_tool(id=3)。
  不要直接回复，必须调用工具！并且把工具返回的结果输出""",
    tools = [
        test_tool
    ],
    context_schema = Context
)
questions = [f"任务{id}" for id in range(1, 6)]
config = {"configurable":{"thread_id":1}}

semaphore = asyncio.Semaphore(3)

async def ask_agent(question):
    """
    尝试异步调用agent
    """
    try:
        async with semaphore:
            result = await asyncio.wait_for(
            agent.ainvoke(
                {"messages":[{"role":"user", "content":question}]},
                config = config
            ),
            timeout = 10
            )
            return result
    except asyncio.TimeoutError:
        return f"问题'{question}'调用超时"

async def main():
    result = await asyncio.gather(*[ask_agent(question) for question in questions],
                                  return_exceptions=True)
    for i in range(len(result)):
        print(f"=== {questions[i]} ===")
        # 判断是否是异常
        if isinstance(result[i], str) or isinstance(result[i], Exception):
            print(f"异常：{result[i]}")
        else:
            # 正常结果，从 messages 中提取最后一条消息
            print(result[i]["messages"][-1].content)
asyncio.run(main())

# await只能在async函数中调用，而asyncio.run()只能在顶层函数调用
# async def failed_task(id: int):
#     if id == 5:
#         raise ValueError(f"{id}错误")

#     print(f"task{id} begin at {datetime.now()}")
#     await asyncio.sleep(id)
#     print(f"task{id} done at {datetime.now()}")
#     return f"{id} success"


# async def main():
#     #练习单独传入
#     result = asyncio.gather(
#         failed_task(1),
#         failed_task(2),
#         failed_task(3)
#     )
#     await result

#     # 练习列表
#     result2 = await asyncio.gather(
#         *[failed_task(i) for i in range(1, 6, 2)],
#         return_exceptions=True)
#     print(result2)

# asyncio.run(main())
