# 知识总结

## 开发规范

> **重要**：禁止使用 websearch 获取信息

1. **禁止使用 websearch**
   - 不依赖网络搜索获取信息
   - 优先查阅本地文档、代码和已有知识
   - 需要外部信息时，使用本地文件和 MCP 工具

## 核心技术

1. python 异步同步
   1. 同步，sync，阻塞式 io，直到任务结束才能继续执行
   2. 异步，async，非阻塞式 io，任务不会立刻执行，而是返回协程对象，等待调用
      1. 协程对象：一般通过 async 类型的函数实例化，不会立刻执行，调用方式：
         1. await：在另一个 async 函数中调用，会阻塞，直到产生结果
         2. asyncio.run:最高层调用，一般是主函数或者测试函数调用
      2. 错误控制：通过自定义检查方法，抛出异常，并在上层函数中捕获，例如 `raise ValueError("Invalid input")`
      3. 超时控制：通过 `asyncio.wait_for(task, timeout)`，一般任务 task 指的是协程对象的执行，超时则抛出 `asyncio.TimeoutError`
      4. 并发限制：通过 `asyncio.semaphore(num)`，num 作为并发数量，多余的必须等待前面任务的完成才能开始执行，在执行函数中传入 semaphore，然后通过 async with 语句进行信号量获取，在调用执行函数的函数中设置和传入信号量
2. 错误管理
   1. 在 `asyncio.gather`中传入参数`return_exceptions=true`，能够捕获到异常，并针对异常进行处理，同时 gather 必须传入可变参数，不能是列表，对于任务列表，通过*进行解包
3. agent 异步调用
   1. 同步调用使用 agent.invoke()，异步调用则使用 ainvoke()，能够被 python 异步调用
