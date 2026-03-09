# 提示词总结
1. 主要使用ChatPromptTemplate来进行信息交互
   1. `ChatPromptTemplate([("system", "你是一个系统助手"),("user","今天天气怎么样")], fewshottemplate, MessagesPlaceholder(variable_name="name"), )`
   2. FewshotChatMessageTemplate用来构建fewshot提示词，首先用examples以及chatprmopt构建示例和示例与agent角色映射，随后通过在chat中放入shotprompt做到提示词注入
   3. 通过`"{variable}"`动态注入提示词内容
   4. messagesplaceholder(variable_name)进行动态提示词注入，一般可以存放对话历史或者，压缩过的上下文信息，传入[("ques1","ans1"), ("ques2", "ans2")]，好处就是不用写死内容，根据需求传入
2. 工具设置和调用：
   1. 通过装饰器tool定义自己所需要的工具，为工具添加描述，可以传入ToolRuntime(class)参数，让工具获取上下文信息或者关键信息，避免暴露给LLM
   2. 定义好的工具传入create_agent的tools列表参数，模型能够自主决定是否调用
3. model：
   1. 没什么好说的，通过ChatOpenAI设置base_url,api_key,model进行模型设置
4. context_schema：
   1. 暂时还不知道能用来干什么，应该是上下文关键信息的保存，能够在invoke执行的时候传入自定义上下文
5. 输出格式约束：
   1. 一般通过参数response_format进行定义，自定义的结果格式继承TypeDict，或者使用model.with_structured_output()绑定输出结果，在这之前通过parser，分别在提示词中注入，并在结果返回后解析，而现在的with或者response都是通过模型原生能力直接限制输出结果，或者自动降级为function_calling，通过模拟成工具调用，让model填入工具所需的参数，然后停止执行，直接取参数作为结果输出
   2. 过去常用的有stroutputparser(),pydanticoutputparser,jsonoutputparser，现在基本全用with和response参数
6. middleware：
   1. langchain新特性，中间件，通过钩子函数在不同阶段完成任务，主要目的是降低耦合，添加日志或者内容过滤拦截等操作，分别有六种，beforeagent\model, wrap_tool_call\wrap_model_call, afteragent\model根据各自运行状态可以添加操作，例如在beforemodel前进行提示词内容重写或者过滤，在wrap_tool_call中添加重试机制和超时限制，
   2. 一般通过继承agentmiddleware并重写方法，此时不需要添加装饰器，如果是单独的方法，则需要添加装饰器进行转换，在create_agent中传入初始化的类或者传入方法名称
7. 关于面试题回答：按照Qid排序
   1. ChatPromptTemplate核心特性是多角色，相比PromptTemplate只有单纯文本，丢失了角色信息，多角色意味着更好的提示词展示，模型能够更明显的看到要求和指令，前者返回的是List[BaseMessages]，是能够被model直接所理解的，后者虽然也能理解，但是效果要差很多
   2. MessagePlaceholder核心在于运行时绑定，可以根据需要调整占位以及内容，直接使用history被提前写死，不方便调试和更改
   3. 定义好class(TypeDict)，然后作为参数传到model.with_structured_output(dantic_object, method = "function_calling")，模型能够根据原生api能力或者模拟工具调用来进行参数提取
   4. format_messages返回的是List[BaseMessages]，不会丢失角色信息，而format返回的是字符串，不是LLM能直接接受的类型
   5. few-shot核心：提供回答风格和回答示例供ai参考，主要解决模型乱回答或者不会按照要求回答的问题
   6. parser的职责是让ai输出结构化信息，方便直接提取，而不是手动过滤结果
   7. 现在基本全部使用with_structured_output
   8. createa_agent最小参数是model，tools一般已经提前绑定或者不需要，但model必须
   9. content blocks，是流式输出中一种结果返回形式，以块的结构返回，每个块有自己的标识，能够通过判断块的类型进行数据的处理，或者选择某些内容作为最终回答，比纯文本流更加结构分明，不在模糊输出和工具调用结果的混合
   10. with是通过硬约束，比如api或者模拟调用提取参数，而parser实际上仍然是提示词工程，只是在最后再解析结果，但是也容易受模型输出影响，实际上并没有较明显的影响模型输出
   11. response_format=ToolStrategy()是模拟工具调用，让LLM收到调用工具的提醒，从而输出工具参数类型的结果，agent直接返回这些参数，实际调用次数还是一次，返回json是依赖模型能力的，模型不一定支持直接输出json
   12. 之前说的beforeagent\beforemodel \ wrap_model_call \ wrap_tool_call \ aftermodel \ afteragent，中间件可以用于输入过滤，输出过滤，日志记录，操作统计，调用情况查询
   13. context_schema能够定义关键信息，节省了上下文，传统的state依赖所有结果送入LLM，浪费token并且容易污染上下文，分离上下文能够节省token，保证模型对关键信息的认识，减少幻觉出现
   14. 一般通过返回ToolMessage或者其他类型的message告诉模型输出失败，在这之前先重新调用LLM，如果超过次数仍然失败，就给模型返回错误信息让模型决策下一步，现在agent已经自动包装了reterPolicy，或者其他修复机制，不需要手动设定这些内容
   15. 转账前保留当前状态，返回给系统让用户确认，然后得到结果后根据暂存的状态恢复上下文并执行后续人物
   16. 动态fewshot，通过message，在获取问题后，结合向量数据库，搜索相似语义，然后添加到examples中，作为messageplaceholder注入到提示ci
   17. 降级为function_calling，基本所有模型都支持
   18. MCP是model context protocol，是模型和外部工具交互的协议，基于这个协议，所有工具都可以被支持mcp的模型调用了，解决了模型只能提供建议而不能实际操作的痛点，真正意义上变成人工智能
   19. class Checkuser(AgentMiddlerware)，然后重写wrap_tool_call，检查权限，重写after_model，根据规则脱敏
   20. 如何编排？不知道，使用了React结构，思考，执行，观察再思考，还有其他例如planand execute，先做出计划然后完善计划随后执行
   21. 通过typeDict不停定义，在更深层的定义中利用List[myPydanticclass]这样嵌套定义，不要在一个数据体中尝试定义所有
   22. 通过thread_id来保证不同id内容的隔离，agent会在整个智能体中传递thread_id的信息，保证内容的隔离性
   23. 失败策略一般是携带错误信息补充到输出结果中，然后重写提示词，让LLM根据错误信息继续输出内容，一般设置了重写次数
   24. 必须要自己定义执行步骤或者工具如何调用时，必须手动写langgraph，或者节点交互必须高度自定义
   25. checkpoint一般会保存checkpoint_id和thread_id，后续根据这两个内容回溯信息