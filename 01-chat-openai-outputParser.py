# 字符串输出解析器 只输出回复
from langchain_core.output_parsers import StrOutputParser
# 引入langchain聊天专用提示词模板
from langchain_core.prompts import ChatPromptTemplate

# 引入langchain openai sdk
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

# 根据message 定义提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是世界级的技术专家"),
    ("user", "{input}")
])

# 创建一个字符串输出解析器
out_parse = StrOutputParser()

# 将输出解析器添加到LLM链中，跟前面的例子区别就是工作流编排，最后一步将LLM模型输出的结果传递给out_parse
chain = prompt | llm | out_parse

result = chain.invoke({"input": "帮我写一篇关于AI的技术文章，100字"})
print(result)