# demo分析

1. 执行流程
   1. 用户传入message、config、context
      1. message包含role和content：role和content的结构约定俗成
         1. role：user\assistant\system\tool
         2. content是对话消息
      2. config代表各种参数，可以通过线程id恢复对话，可以设置agent对话次数等，线程id和当前终端运行保持一致，终端结束，线程也随之结束
      3. context是传入的上下文信息
      4. LLM的可见范围是messages:[{"role":"", "context":""}]，对于context，只能由工具看到
   2. 提示词组合，将输入信息、工具的相关信息、message历史全部组合成一个完整的prompt发送给LLM，LLM来决定下一步直接回复还是调用工具，调用工具后会返回调用记录，然后再次发送给LLM，最后根据回复模板回复
   3. 
