# 流式输出
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

chunks = []
for chunk in llm.stream("天空为什么是蓝色的？"):
    chunks.append(chunk)
    print(chunk.content, end="|", flush=True)
# end="|" 改为 end=""中间就没有竖线了
