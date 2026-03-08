# 提示词总结
1. 主要使用ChatPromptTemplate来进行信息交互
   1. `ChatPromptTemplate([("system", "你是一个系统助手"),("user","今天天气怎么样")], fewshottemplate, MessagesPlaceholder(variable_name="name"), )`