# 获取图片后base64发送给大模型
import base64
import os

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
# 用httpx,获取图片的base64编码
import httpx

image_url = "https://img0.baidu.com/it/u=4036329736,2858248034&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=1200"
# 将图片二进制数据转换为base64编码
image_data = base64.b64encode(httpx.get(image_url).content).decode("utf-8")
chatLLM = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen3-vl-plus",  # 可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
)
message = HumanMessage(
    content=[
        {"type": "text", "text": "用中文描述描述这张图片"},
        {
            "type": "image_url",
            "image_url": {"url": f"data:image/png;base64,{image_data}"},
        }
    ],
)

response = chatLLM.invoke([message])
print(response.content)

