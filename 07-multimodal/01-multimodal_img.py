# 根据url识别图片
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

image_url = "https://avatars.githubusercontent.com/u/64422807?v=4"
model = ChatOpenAI(model="gpt-4o")
message = HumanMessage(
    content=[
        {"type": "text", "text": "用中文描述描述这张图片"},
        {"type": "image_url", "image_url": {"url": image_url}}
    ],
)

response = model.invoke([message])
print(response.content)

# 这张图片的背景是简单的灰色，给人一种简洁和宁静的感觉。画面中人物的头发呈深色卷发，线条柔和，增添了些许艺术感。发间融入了一些灰色的花瓣图案，仿佛花瓣从头发中生长出来，让整体效果显得富有创意和美感。人物穿着一件白色上衣，与整个色调的搭配和谐，看起来干净而柔和。整个图像呈现出一种朦胧且充满梦幻的风格。