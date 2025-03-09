# 引入langchain聊天专用提示词模板
from langchain_core.prompts import ChatPromptTemplate

# 引入langchain openai sdk
from langchain_openai import ChatOpenAI

# 配置非官方URL（也可在环境变量配置OPENAI_API_BASE）
llm = ChatOpenAI(base_url="https://api.xty.app/v1")
# 如果是官方URL,使用以下即可
# llm = ChatOpenAI()

# 根据message 定义提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是世界级的技术专家"),
    ("user", "{input}")
])

# 通过langchain的链式调用，生成一个chain
chain = prompt | llm

result = chain.invoke({"input": "帮我写一篇关于AI的技术文章，100字"})
print(result)
