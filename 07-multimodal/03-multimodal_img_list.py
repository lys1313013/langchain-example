# 传入多个图片url并比较图片
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

image_url1 = "https://avatars.githubusercontent.com/u/64422807?v=4"
image_url2 = "https://i-avatar.csdnimg.cn/a565ae7306de49babdb4ac8d52f50c19_weixin_43811294.jpg!1"
model = ChatOpenAI(model="gpt-4o")
message = HumanMessage(
    content=[
        {"type": "text", "text": "这两张图片有啥区别"},
        {"type": "image_url", "image_url": {"url": image_url1}},
        {"type": "image_url", "image_url": {"url": image_url2}}
    ],
)

response = model.invoke([message])
print(response.content)

