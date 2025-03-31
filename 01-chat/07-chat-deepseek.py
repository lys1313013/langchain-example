from langchain_openai import ChatOpenAI
import os

# 调用deepseek官网API
# 文档地址：https://api-docs.deepseek.com/zh-cn/

chatLLM = ChatOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
    model="deepseek-reasoner" # deepseek-chat, deepseek-reasoner
)

# 流式输出
for chunk in chatLLM.stream("什么是langchain?"):
    print(chunk.content, end="", flush=True)