"""
LangChain 1.0 综合练习：覆盖 Structured Output + Middleware + Context Schema
覆盖知识点:
1. Structured Output (ToolStrategy)
2. Middleware (wrap_tool_call, before_model, after_model)
3. Context Schema (TypedDict - 1.0 仅支持这个)
4. 工具定义 (@tool)
5. 日志记录 + 重试 + 上下文管理
"""

from langchain.agents import create_agent
from langchain.agents.middleware import AgentMiddleware, wrap_tool_call
from langchain.agents.structured_output import ToolStrategy
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
from pydantic import BaseModel, Field
from typing import TypedDict, List
import os

# ==================== 1. 定义 Context Schema (TypedDict - 1.0 仅支持这个) ====================

class UserContext(TypedDict):
    """用户上下文 - 存储用户信息"""
    username: str
    user_preference: dict


# ==================== 2. 定义 Structured Output (Pydantic) ====================

class TaskResult(BaseModel):
    """任务结果 - 结构化输出"""
    task: str = Field(description="任务名称")
    status: str = Field(description="状态：pending/in_progress/completed")
    description: str = Field(description="任务描述")
    priority: int = Field(description="优先级：1-5", ge=1, le=5)


class PlanResult(BaseModel):
    """学习计划 - 包含多个任务"""
    user: str
    tasks: List[TaskResult]
    total_hours: int


# ==================== 3. 定义工具 ====================

@tool
def get_user_status(username: str) -> str:
    """获取用户当前状态（学习时间、精力等）"""
    return f"{username} 现在精力充沛，适合学习 2 小时"


@tool
def send_notification(message: str) -> str:
    """发送通知给用户"""
    print(f"📬 通知：{message}")
    return "通知已发送"


@tool
def save_plan(plan: str) -> str:
    """保存学习计划"""
    print(f"💾 已保存计划：{plan}")
    return "计划已保存"


# ==================== 4. 自定义 Middleware ====================

class RetryMiddleware(AgentMiddleware):
    """工具调用重试中间件"""

    def __init__(self, max_attempts: int = 3, timeout: int = 10):
        self.max_attempts = max_attempts
        self.timeout = timeout

    @wrap_tool_call
    def retry_on_failure(self, request, handler):
        """工具调用失败时自动重试"""
        tool_name = request.tool_call["name"]

        for attempt in range(self.max_attempts):
            try:
                result = handler(request)
                return result
            except Exception as e:
                if attempt == self.max_attempts - 1:
                    return ToolMessage(
                        content=f"工具 {tool_name} 调用失败：{str(e)}",
                        tool_call_id=request.tool_call["id"]
                    )
                print(f"工具 {tool_name} 调用失败，重试 {attempt + 1}/{self.max_attempts}")

        return None


class ContextLengthMiddleware(AgentMiddleware):
    """上下文长度管理中间件"""

    def __init__(self, max_messages: int = 20):
        self.max_messages = max_messages

    def before_model(self, state, runtime):
        """在调用模型前检查上下文长度"""
        messages = state.get("messages", [])

        if len(messages) > self.max_messages:
            keep_first = messages[0]
            keep_last = messages[-self.max_messages + 1:]
            state["messages"] = [keep_first] + keep_last
            print(f"⚠️  上下文过长，已裁剪至 {self.max_messages} 条消息")


class LoggingMiddleware(AgentMiddleware):
    """日志记录中间件"""

    def before_model(self, state, runtime):
        print(f"📝 [Before Model] 当前消息数：{len(state.get('messages', []))}")

    def after_model(self, response, runtime):
        print(f"📝 [After Model] 模型响应：{response.message.content[:50]}...")

    @wrap_tool_call
    def log_tool_calls(self, request, handler):
        tool_name = request.tool_call["name"]
        print(f"🔧 [Tool Call] 调用工具：{tool_name}")
        result = handler(request)
        print(f"✅ [Tool Done] 工具 {tool_name} 完成")
        return result


# ==================== 5. 创建 Agent ====================

# ⚠️ API Key 应该用环境变量，不要硬编码
model = ChatOpenAI(
    model="deepseek-chat",
    base_url="https://api.deepseek.com/v1",
    api_key=os.environ.get("DEEPSEEK_API_KEY", "sk-eacd3a82b8e3491d888df3ef213e442e"),
)

system_prompt = """你是一个智能学习助手。
你的任务是根据用户的当前状态和偏好，制定合理的学习计划。
请以结构化的方式输出计划，包含任务名称、状态、描述和优先级。
"""

agent = create_agent(
    model=model,
    system_prompt=system_prompt,
    tools=[
        get_user_status,
        send_notification,
        save_plan,
    ],
    response_format=ToolStrategy(PlanResult),  # 结构化输出
    middleware=[
        RetryMiddleware(max_attempts=3),
        ContextLengthMiddleware(max_messages=20),
        LoggingMiddleware(),
    ],
    context_schema=UserContext,  # Context Schema
)


# ==================== 6. 调用 Agent ====================

if __name__ == "__main__":
    print("=" * 50)
    print("🎯 LangChain 1.0 综合练习")
    print("=" * 50)

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "我现在是研一学生，每天有 3 小时空闲时间，想学习 Python 和 AI。请帮我制定一个学习计划。"
                }
            ]
        },
        context={
            "username": "张三",
            "user_preference": {
                "学习目标": "Python 和 AI",
                "每天时间": "3 小时",
                "当前水平": "入门"
            }
        },
    )

    print("\n" + "=" * 50)
    print("📋 生成的学习计划:")
    print("=" * 50)

    if "structured_response" in result:
        plan = result["structured_response"]
        print(f"用户：{plan.user}")
        print(f"任务数量：{len(plan.tasks)}")
        print(f"总学习时长：{plan.total_hours} 小时")
        print("\n任务详情:")
        for i, task in enumerate(plan.tasks, 1):
            print(f"  {i}. [{task.priority}⭐] {task.task}")
            print(f"     状态：{task.status}")
            print(f"     描述：{task.description}")
    else:
        print("未生成结构化响应，查看原始消息:")
        print(result["messages"][-1].content)

    print("\n" + "=" * 50)
    print("✅ 练习完成!")
    print("=" * 50)
