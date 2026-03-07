"""
第一周面试代码练习题

包含所有高频面试题的代码实现，可直接运行验证
"""
import asyncio
from datetime import datetime


# ============================================
# 基础题练习
# ============================================

# Q1: async vs sync 调用区别
async def async_func():
    return "hello async"

def sync_func():
    return "hello sync"

# 测试
# result1 = sync_func()                    # ✅ 直接调用
# result2 = await async_func()             # ✅ 在 async 中 await
# result3 = asyncio.run(async_func())      # ✅ 顶层调用


# Q4: asyncio.run() vs await
async def fetch():
    await asyncio.sleep(0.1)
    return "done"

# asyncio.run(fetch())  # ✅ 顶层
# async def main():
#     result = await fetch()  # ✅ async 内部


# ============================================
# 中阶题练习
# ============================================

# Q6: asyncio.gather 用法
async def gather_example():
    async def task(i):
        await asyncio.sleep(0.1)
        return f"result {i}"

    # 方式 1: 直接传入
    results = await asyncio.gather(task(1), task(2), task(3))

    # 方式 2: 列表解包
    tasks = [task(i) for i in range(3)]
    results = await asyncio.gather(*tasks)

    # 方式 3: 异常不中断
    results = await asyncio.gather(
        task(1),
        asyncio.sleep(-1),  # 会抛出异常
        return_exceptions=True
    )
    return results


# Q8: Semaphore 限制并发
async def semaphore_example():
    semaphore = asyncio.Semaphore(3)  # 最多 3 个并发

    async def limited_task(i):
        async with semaphore:
            print(f"任务{i}开始，时间：{datetime.now().strftime('%H:%M:%S')}")
            await asyncio.sleep(1)
            print(f"任务{i}结束")
            return f"result {i}"

    # 10 个任务，但最多 3 个并发
    results = await asyncio.gather(*[limited_task(i) for i in range(10)])
    return results


# Q9: 超时控制
async def timeout_example():
    async def slow_task():
        await asyncio.sleep(10)
        return "done"

    try:
        result = await asyncio.wait_for(slow_task(), timeout=2)
        return result
    except asyncio.TimeoutError:
        return "超时了！"


# Q10: 异常处理
async def exception_example():
    async def may_fail(i):
        if i == 2:
            raise ValueError(f"任务{i}失败了")
        return f"任务{i}成功"

    # 方式 1: try-except
    async def safe_task(i):
        try:
            return await may_fail(i)
        except Exception as e:
            return f"捕获异常：{e}"

    results = await asyncio.gather(
        safe_task(1),
        safe_task(2),
        safe_task(3)
    )

    # 方式 2: return_exceptions
    results = await asyncio.gather(
        may_fail(1),
        may_fail(2),
        may_fail(3),
        return_exceptions=True
    )

    # 处理结果
    for i, r in enumerate(results):
        if isinstance(r, Exception):
            print(f"任务{i}异常：{r}")
        else:
            print(f"任务{i}成功：{r}")


# Q11: LangChain invoke vs ainvoke
# 同步版本 - 串行
# for q in questions:
#     result = agent.invoke({"messages": [...]})

# 异步版本 - 并发
# tasks = [agent.ainvoke({"messages": [...]}) for q in questions]
# results = await asyncio.gather(*tasks)


# Q12: 综合手写题 - 限流 + 超时 + 异常处理
async def interview_standard_solution():
    """
    面试标准答案：
    并发调用 5 个 API，限制并发为 3，超时 5 秒，异常不中断
    """
    semaphore = asyncio.Semaphore(3)

    async def api_call(i):
        """模拟 API 调用"""
        await asyncio.sleep(0.5)
        if i == 3:
            raise ValueError("API 错误")
        return f"API 结果 {i}"

    async def fetch_with_limit(semaphore, i):
        async with semaphore:
            try:
                result = await asyncio.wait_for(
                    api_call(i),
                    timeout=5
                )
                return result
            except asyncio.TimeoutError:
                return f"任务{i}超时"
            except Exception as e:
                return f"任务{i}异常：{e}"

    tasks = [fetch_with_limit(semaphore, i) for i in range(5)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, r in enumerate(results):
        print(f"任务{i}: {r}")

    return results


# ============================================
# 高阶题练习
# ============================================

# Q15: 状态隔离 - 独立的 thread_id
async def state_isolation_example():
    """Agent 并发时状态隔离"""
    # ❌ 错误：共享 thread_id
    shared_config = {"configurable": {"thread_id": 1}}

    # ✅ 正确：独立 thread_id
    tasks = [
        # agent.ainvoke(
        #     {"messages": [...]},
        #     config={"configurable": {"thread_id": i}}
        # )
        asyncio.sleep(0.1)  # 占位
        for i in range(5)
    ]
    await asyncio.gather(*tasks)


# Q15: 异步锁保护
async def lock_example():
    """使用 asyncio.Lock 保护共享资源"""
    lock = asyncio.Lock()
    shared_counter = 0

    async def increment():
        nonlocal shared_counter
        async with lock:  # 临界区
            temp = shared_counter
            await asyncio.sleep(0.01)
            shared_counter = temp + 1

    await asyncio.gather(*[increment() for _ in range(10)])
    print(f"最终计数：{shared_counter}")  # 应该是 10


# ============================================
# 运行所有练习
# ============================================

async def main():
    print("=== Q6: gather 示例 ===")
    print(await gather_example())

    print("\n=== Q8: Semaphore 示例 ===")
    await semaphore_example()

    print("\n=== Q9: 超时示例 ===")
    print(await timeout_example())

    print("\n=== Q10: 异常处理示例 ===")
    await exception_example()

    print("\n=== Q12: 标准面试答案 ===")
    await interview_standard_solution()

    print("\n=== Q15: 锁示例 ===")
    await lock_example()


if __name__ == "__main__":
    asyncio.run(main())
