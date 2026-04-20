import anthropic
import os

# 通过 Anthropic SDK 调用阿里百炼
# 代码参考于：https://help.aliyun.com/zh/model-studio/anthropic-api-messages

client = anthropic.Anthropic(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/apps/anthropic",
)

# 流式输出
print("=== 流式输出 ===")
stream = client.messages.create(
    model="qwen-plus",
    max_tokens=1024,
    stream=True,
    messages=[
        {
            "role": "user",
            "content": "什么是langchain?",
        }
    ],
)

for chunk in stream:
    if chunk.type == "content_block_delta":
        if hasattr(chunk.delta, "text"):
            print(chunk.delta.text, end="", flush=True)

# 非流式输出
print("\n\n=== 非流式输出 ===")
message = client.messages.create(
    model="qwen-plus",
    max_tokens=1024,
    system="You are a helpful assistant.",
    messages=[
        {
            "role": "user",
            "content": "你是谁？",
        }
    ],
)

for block in message.content:
    if hasattr(block, "text"):
        print(block.text)
