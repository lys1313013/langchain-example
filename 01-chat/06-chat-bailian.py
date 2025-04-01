from langchain_openai import ChatOpenAI
import os

# 调用阿里百炼
# 代码参考于： https://help.aliyun.com/zh/model-studio/developer-reference/use-bailian-in-langchain

chatLLM = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",  # 可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
)

# 流式输出
for chunk in chatLLM.stream("什么是langchain?"):
    print(chunk.content, end="", flush=True)

# 非流式输出
print()
print("非流式输出")
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁？"}]
response = chatLLM.invoke(messages)
print(response.content)