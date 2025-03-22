# 获取事件信息，方便排查问题
from langchain_openai import ChatOpenAI
import asyncio

llm = ChatOpenAI()


async def async_stream():
    events = []
    async for event in llm.astream_events("hello", version="v2"):
        events.append(event)
    print(events)


asyncio.run(async_stream())
