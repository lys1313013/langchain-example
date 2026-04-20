# 引入langchain聊天专用提示词模板
from langchain_core.prompts import ChatPromptTemplate

# 引入langchain openai sdk
from langchain_openai import ChatOpenAI

# 如果是官方URL,使用以下即可
llm = ChatOpenAI()

# 根据message 定义提示词模板
# 这里以对话模型的消息格式为例子，不熟悉openai对话模型的话，可以参考官方文档
# 下面消息模板，定义两条消息，system消息告诉模型扮演什么角色，user消息代表用户输入的问题
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是世界级的技术专家"),
    ("user", "{input}")
])

# 通过langchain的链式调用，生成一个chain
# 基于LCEL表达式构建LLM链，lcel语法类似linux的pipeline语法，从左到右顺序执行
# 下面编排了一个简单的工作流，首先执行prompt完成提示词模板（prompt template）格式化处理，然后将格式化后的结果传递给llm模型
chain = prompt | llm

result = chain.invoke({"input": "帮我写一篇关于AI的技术文章，100字"})
print(result)
