# 获取图片后base64发送给大模型
import base64
import os

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
import httpx


def get_image_data(image_path: str) -> str:
    """
    适配 远程图片和本地图片
    """
    if image_path.startswith("http://") or image_path.startswith("https://"):
        return base64.b64encode(httpx.get(image_path).content).decode("utf-8")
    else:
        return base64.b64encode(open(image_path, "rb").read()).decode("utf-8")


image_url = "/Users/hurry/Documents/coding/projects/llm_preojects/Qwen3-VL-Embedding/data/evaluation/mmeb_v2/image-tasks/MSCOCO_t2i/COCO_val2014_000000181859.jpg"
# 示例：HTTP URL 方式
# image_url = "https://img0.baidu.com/it/u=4036329736,2858248034&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=1200"

image_data = get_image_data(image_url)
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

