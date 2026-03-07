# 知识总结
1. python异步同步
   1. 同步，sync，阻塞式io，直到任务结束才能继续执行
   2. 异步，async，非阻塞式io，任务不会立刻执行，而是返回协程对象，等待调用
      1. 协程对象：一般通过async类型的函数实例化，不会立刻执行，调用方式：
         1. await：在另一个async函数中调用，会阻塞，直到产生结果
         2. asyncio.run:最高层调用，一般是主函数或者测试函数调用
      2. 错误控制：通过自定义检查方法，抛出异常，并在上层函数中捕获，例如`raise ValueError("Invalid input")` 
      3. 超时控制：通过`asyncio.wait_for(task, timeout)`，一般任务task指的是协程对象的执行，超时则抛出`asyncio.TimeoutError`
      4. 并发限制：通过`asyncio.semaphore(num)`，num作为并发数量，多余的必须等待前面任务的完成才能开始执行
2. 错误管理
   1. 在`asyncio.gather`中传入参数`return_exceptions=true`，能够捕获到异常，并针对异常进行处理，同时gather必须传入可变参数，不能是列表，对于任务列表，通过*进行解包
3. agent异步调用
   1. 同步调用使用agent.invoke()，异步调用则使用ainvoke()，能够被python异步调用