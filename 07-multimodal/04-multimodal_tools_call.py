# 图片识别+工具调用
from typing import Literal
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool


@tool
def color_tool(color: Literal["黑色的", "白色的", "绿色的", "灰色的", "蓝色的"]) -> None:
    """Describe the color"""
    pass


model = ChatOpenAI(model="gpt-4o")
model_with_tool = model.bind_tools([color_tool])
image_url1 = "https://avatars.githubusercontent.com/u/64422807?v=4"
image_url2 = "https://i-avatar.csdnimg.cn/a565ae7306de49babdb4ac8d52f50c19_weixin_43811294.jpg!1"
message = HumanMessage(
    content=[
        {"type": "text", "text": "用中文描述这两张图片的主题颜色"},
        {"type": "image_url", "image_url": {"url": image_url1}},
        {"type": "image_url", "image_url": {"url": image_url2}}
    ],
)

response = model_with_tool.invoke([message])
print(response.tool_calls)

# 输出
"""
[{'name': 'color_tool', 'args': {'color': '灰色的'}, 'id': 'call_kovBTsMEYBp0nJhiGeunGvO2', 'type': 'tool_call'}, {'name': 'color_tool', 'args': {'color': '蓝色的'}, 'id': 'call_1tNCe6TPAbvjts9bmhc3STvT', 'type': 'tool_call'}]
"""
