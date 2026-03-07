# 第一周面试题整理

## 📌 说明

本文件夹整理第一周（Python 异步编程 + LangChain 基础）的面试高频问题，包含：
- 基础题（必会）
- 中阶题（区分度）
- 高阶题（大厂/初创）

---

## 🔹 一、基础题（必会）

### Q1: `async` 函数和普通函数有什么本质区别？

**代码示例：**
```python
async def async_func():
    return "hello"

def sync_func():
    return "hello"

# 调用方式有何不同？
```

**参考答案：**

| 对比项 | `async` 函数 | 普通函数 |
|--------|-------------|----------|
| 调用返回值 | 协程对象（不立即执行） | 直接返回结果 |
| 执行方式 | 需 `await` 或 `asyncio.run()` | 直接调用 |
| 内部可用 | `await`、`async for`、`async with` | 普通语法 |

**常见错误：**
```python
async_func()  # ❌ RuntimeWarning: coroutine was never awaited
await async_func()  # ✅ 在 async 函数中
asyncio.run(async_func())  # ✅ 在顶层调用
```

---

### Q2: 解释什么是协程（Coroutine）？

**参考答案：**

协程是**用户态的轻量级线程**，特点：
1. **协作式调度**：协程主动让出控制权（`await`），而非被操作系统抢占
2. **单线程并发**：多个协程在单线程内交替执行
3. **状态保持**：暂停后恢复时，局部变量状态保留

**类比理解：**
```
同步函数 = 做饭时一直等水烧开（阻塞）
协程     = 烧水时去切菜，水开了再回来（非阻塞）
```

---

### Q3: `await` 关键字的作用是什么？

**参考答案：**

`await` 的作用：
1. **暂停当前协程**，等待可等待对象（Awaitable）完成
2. **让出控制权**给事件循环，允许执行其他任务
3. **恢复执行**当等待的对象完成后

**可等待的对象：**
- `asyncio.sleep()`
- 异步 I/O 操作（`aiohttp`、`asyncpg` 等）
- 其他 `async` 函数的调用结果
- `asyncio.gather()`、`asyncio.wait()` 等

**错误示例：**
```python
def sync_func():
    await asyncio.sleep(1)  # ❌ SyntaxError: await outside async function

async def async_func():
    asyncio.sleep(1)  # ❌ RuntimeWarning: coroutine was never awaited
    await asyncio.sleep(1)  # ✅
```

---

### Q4: `asyncio.run()` 和 `await` 有什么区别？

**参考答案：**

| 对比项 | `asyncio.run()` | `await` |
|--------|-----------------|---------|
| 使用位置 | 顶层（主函数） | `async` 函数内部 |
| 作用 | 启动事件循环 | 等待可等待对象 |
| 调用次数 | 程序一般只调用一次 | 可多次调用 |

**示例：**
```python
async def fetch():
    await asyncio.sleep(1)
    return "done"

# ✅ 正确
asyncio.run(fetch())

# ✅ 正确
async def main():
    result = await fetch()

# ❌ 错误
await fetch()  # SyntaxError: await outside async function
```

---

### Q5: 下面代码有什么问题？如何修复？

```python
async def main():
    async def fetch():
        await asyncio.sleep(1)
        return "done"

    fetch()  # 问题在哪？
```

**参考答案：**

**问题**：协程未 `await`，不会执行，会触发 `RuntimeWarning`

**修复：**
```python
async def main():
    async def fetch():
        await asyncio.sleep(1)
        return "done"

    result = await fetch()  # ✅
    print(result)
```

---

## 🔹 二、中阶题（区分度）

### Q6: `asyncio.gather` 的作用是什么？如何使用？

**参考答案：**

`asyncio.gather` 用于**并发运行多个协程**，等待所有完成。

**基本用法：**
```python
async def fetch(i):
    await asyncio.sleep(1)
    return f"result {i}"

async def main():
    # 方式 1：直接传入多个协程
    results = await asyncio.gather(
        fetch(1),
        fetch(2),
        fetch(3)
    )
    print(results)  # ['result 1', 'result 2', 'result 3']

    # 方式 2：传入列表（解包）
    tasks = [fetch(i) for i in range(5)]
    results = await asyncio.gather(*tasks)
```

**关键参数 `return_exceptions`：**
```python
# 默认：遇到异常立即抛出
await asyncio.gather(fetch(1), fetch(2))  # ❌ 一个失败全部失败

# 设置后：异常作为结果返回
results = await asyncio.gather(
    fetch(1),
    fetch(2),
    return_exceptions=True
)
# results 可能包含 Exception 对象
```

---

### Q7: `asyncio.create_task` 和 `asyncio.gather` 有什么区别？

**参考答案：**

| 对比项 | `create_task` | `gather` |
|--------|---------------|----------|
| 用途 | 创建后台任务 | 等待多个任务完成 |
| 返回值 | `Task` 对象 | 结果列表 |
| 执行时机 | 立即调度执行 | 等待 `await` 时才并发 |
| 典型场景 | 后台任务、定时任务 | 批量请求、并发处理 |

**示例对比：**
```python
# create_task - 后台任务
async def background():
    task = asyncio.create_task(fetch())
    # 可以继续做其他事
    await do_something_else()
    result = await task  # 需要时再等待

# gather - 批量等待
results = await asyncio.gather(fetch1(), fetch2(), fetch3())
```

---

### Q8: 如何限制并发数量？为什么需要？

**参考答案：**

使用 `asyncio.Semaphore` 限制并发数量。

**为什么需要：**
1. 避免远程服务限流（如 API 速率限制）
2. 防止内存占用过高
3. 避免数据库连接池耗尽

**代码示例：**
```python
semaphore = asyncio.Semaphore(5)  # 最多 5 个并发

async def limited_fetch(i):
    async with semaphore:  # 获取信号量
        await asyncio.sleep(1)
        return f"result {i}"

async def main():
    tasks = [limited_fetch(i) for i in range(100)]
    results = await asyncio.gather(*tasks)
```

**信号量工作原理：**
```
初始：5 个可用
任务 1-5: 获取信号量，执行
任务 6  : 等待（没有可用信号量）
任务 1 完成：释放信号量 → 任务 6 开始执行
```

---

### Q9: 什么是超时控制？如何实现？

**参考答案：**

超时控制用于**防止任务长时间挂起**，使用 `asyncio.wait_for`。

**代码示例：**
```python
async def fetch():
    await asyncio.sleep(10)  # 假设很慢
    return "done"

async def main():
    try:
        result = await asyncio.wait_for(fetch(), timeout=5)
        print(result)
    except asyncio.TimeoutError:
        print("超时了！")
```

**常见应用场景：**
- API 请求超时
- 数据库查询超时
- 用户操作等待超时

---

### Q10: 异步中如何正确处理异常？

**参考答案：**

**方式 1：`try-except` 包裹 `await`**
```python
async def safe_fetch():
    try:
        result = await fetch()
        return result
    except Exception as e:
        print(f"错误：{e}")
        return None
```

**方式 2：`gather` 的 `return_exceptions=True`**
```python
results = await asyncio.gather(
    fetch(1),
    fetch(2),
    return_exceptions=True
)
for i, r in enumerate(results):
    if isinstance(r, Exception):
        print(f"任务{i}失败：{r}")
    else:
        print(f"任务{i}成功：{r}")
```

**方式 3：Task 级别异常处理**
```python
task = asyncio.create_task(fetch())
task.add_done_callback(lambda t: print(t.exception()))
```

---

### Q11: LangChain 中 `invoke` 和 `ainvoke` 有什么区别？

**参考答案：**

| 对比项 | `invoke` | `ainvoke` |
|--------|----------|-----------|
| 类型 | 同步调用 | 异步调用 |
| 阻塞 | 是 | 否 |
| 返回 | 直接结果 | 协程对象 |
| 并发 | 串行 | 可并发 |

**性能对比：**
```python
# 同步 - 串行执行，总时间 = 3 × 单次时间
for q in questions:
    result = agent.invoke({"messages": [...]})

# 异步 - 并发执行，总时间 ≈ 单次时间
tasks = [agent.ainvoke({"messages": [...]}) for q in questions]
results = await asyncio.gather(*tasks)
```

**底层实现：**
- `invoke` 使用 `httpx.Client`（阻塞）
- `ainvoke` 使用 `httpx.AsyncClient`（非阻塞）

---

### Q12: 手写代码：并发调用 5 个 API，限制并发为 3，超时 5 秒，异常不中断

**参考答案：**
```python
import asyncio

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

async def main():
    semaphore = asyncio.Semaphore(3)
    tasks = [fetch_with_limit(semaphore, i) for i in range(5)]
    results = await asyncio.gather(*tasks, return_exceptions=True)

    for i, r in enumerate(results):
        print(f"任务{i}: {r}")

asyncio.run(main())
```

---

## 🔹 三、高阶题（大厂/初创）

### Q13: 事件循环（Event Loop）的工作原理是什么？

**参考答案：**

事件循环是异步编程的**核心调度器**，工作流程：

```
1. 就绪队列：待执行的任务
2. 等待队列：等待 I/O 完成的任务
3. 循环过程：
   - 执行就绪队列中的任务
   - 遇到 await I/O → 挂起，放入等待队列
   - I/O 完成 → 移回就绪队列
   - 重复循环
```

**简化模型：**
```python
# 伪代码理解事件循环
class EventLoop:
    def __init__(self):
        self.ready_queue = []
        self.waiting_tasks = {}

    def run_until_complete(self, main):
        task = create_task(main)
        self.ready_queue.append(task)

        while self.ready_queue or self.waiting_tasks:
            # 执行就绪任务
            while self.ready_queue:
                task = self.ready_queue.pop(0)
                self._step_task(task)

            # 等待 I/O
            self._wait_for_io()
```

**关键理解：**
- 单线程、协作式调度
- I/O 多路复用（`select`/`epoll`/`kqueue`）
- 任务切换在 `await` 点发生

---

### Q14: 什么是 I/O 多路复用？和异步的关系？

**参考答案：**

**I/O 多路复用**：单个线程监控多个 I/O 连接，哪个就绪就处理哪个。

**技术实现：**
| 系统 | 机制 |
|------|------|
| Linux | `epoll` |
| macOS | `kqueue` |
| Windows | `IOCP` |
| 跨平台 | `select`/`poll` |

**和异步的关系：**
```
事件循环 (asyncio)
    ↓
I/O 多路复用 (epoll/kqueue)
    ↓
操作系统内核
    ↓
网络/磁盘 I/O
```

**通俗理解：**
```
传统阻塞 I/O = 每个请求一个线程，等响应
I/O 多路复用  = 一个线程盯着所有请求，谁好了处理谁
```

---

### Q15: 如果 Agent 并发调用时出现状态混乱，可能是什么原因？如何解决？

**参考答案：**

**可能原因：**
1. **共享 `thread_id`**：多个请求使用同一个配置
2. **全局变量竞争**：异步修改全局状态
3. **Memory 未隔离**：对话历史串了

**解决方案：**

**1. 独立配置：**
```python
# ❌ 错误：共享 thread_id
config = {"configurable": {"thread_id": 1}}
results = await asyncio.gather(
    agent.ainvoke(..., config=config),
    agent.ainvoke(..., config=config)
)

# ✅ 正确：独立 thread_id
tasks = [
    agent.ainvoke(
        ...,
        config={"configurable": {"thread_id": i}}
    )
    for i in range(5)
]
```

**2. 异步锁保护：**
```python
lock = asyncio.Lock()

async def safe_operation():
    async with lock:
        # 临界区代码
        pass
```

**3. 无状态设计：**
- 避免全局变量
- 每次请求传入完整上下文

---

### Q16: 如何封装一个异步工具函数供 LangChain Agent 使用？

**参考答案：**

**完整示例：**
```python
from langchain.tools import tool
import httpx

@tool
async def search_web(query: str) -> str:
    """搜索网络信息"""
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.example.com/search",
            params={"q": query},
            timeout=10
        )
    return response.json()["result"]

# 在 Agent 中使用
agent = create_agent(
    model=llm,
    tools=[search_web],  # 异步工具会被自动识别
)
```

**关键点：**
1. 工具函数用 `async def` 定义
2. 使用异步 HTTP 客户端（`httpx.AsyncClient`）
3. Agent 的 `ainvoke` 会自动调用异步工具

---

### Q17: 协程和线程有什么区别？各自适用场景？

**参考答案：**

| 对比项 | 协程 | 线程 |
|--------|------|------|
| 调度方式 | 用户态、协作式 | 内核态、抢占式 |
| 切换开销 | 极小（微秒级） | 较大（毫秒级） |
| 并发数量 | 数万 + | 数百（受系统限制） |
| 数据共享 | 同线程内，无需锁 | 需同步锁 |
| 适用场景 | I/O 密集型 | CPU 密集型 |

**场景选择：**
```
I/O 密集型（网络请求、文件读写）→ 协程
CPU 密集型（计算、图像处理）   → 多进程/线程池
混合场景 → 协程 + 线程池执行 CPU 任务
```

---

## 📚 附加：手写代码练习

### 练习 1：基础异步函数
```python
# 任务：编写异步函数，sleep 1 秒后返回"done"
async def task1():
    await asyncio.sleep(1)
    return "done"
```

### 练习 2：并发执行
```python
# 任务：并发执行 5 个任务，收集结果
async def task2():
    async def work(i):
        await asyncio.sleep(0.5)
        return f"task {i}"

    results = await asyncio.gather(*[work(i) for i in range(5)])
    return results
```

### 练习 3：带限流和超时
```python
# 任务：并发 10 个任务，限制 3 并发，超时 2 秒
async def task3():
    semaphore = asyncio.Semaphore(3)

    async def work(i):
        async with semaphore:
            return await asyncio.wait_for(
                asyncio.sleep(1),
                timeout=2
            )

    results = await asyncio.gather(
        *[work(i) for i in range(10)],
        return_exceptions=True
    )
    return results
```

---

## 🎯 面试准备建议

| 优先级 | 内容 | 建议 |
|--------|------|------|
| ⭐⭐⭐⭐⭐ | 基础题 Q1-Q5 | 必须熟练 |
| ⭐⭐⭐⭐⭐ | 中阶题 Q6-Q12 | 能手写代码 |
| ⭐⭐⭐ | 高阶题 Q13-Q17 | 理解思路 |

**复习方法：**
1. 盖住答案，自己口述
2. 在 IDE 中手写代码验证
3. 结合自己的 `async_practice.py` 理解

---

*整理时间：2026-03-06*
*适用范围：AI Agent 开发实习岗*
