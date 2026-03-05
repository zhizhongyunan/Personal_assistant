# 知识总结
1. 在python中，async执行通过执行权的交换来做到异步，async对象的创建会返回协程对象，该对象执行方式只有两种
   1. await function()调用，但是只允许在**另一个async函数**
   2. asyncio.run(function())执行，只允许在最顶层执行，其余情况只能用await
2. 批量调用采用async.gather()