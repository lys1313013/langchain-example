# 异步调用
from langchain_openai import ChatOpenAI
import asyncio


async def task1():
    llm = ChatOpenAI()
    chunks = []
    async for chunk in llm.astream("天空是什么颜色？"):
        chunks.append(chunk)
        if len(chunks) == 2:
            print(chunks[1])
        # 实时打印响应块的内容，并以'|'分隔
        print(chunk.content, end="|", flush=True)


async def task2():
    llm = ChatOpenAI()
    chunks = []
    async for chunk in llm.astream("讲个笑话？"):
        chunks.append(chunk)
        if len(chunks) == 2:
            print(chunks[1])
        # 实时打印响应块的内容，并以'|'分隔
        print(chunk.content, end="|", flush=True)


async def main():
    # 同步调用
    await task1()
    await task2()

    # 异步调用
    # await asyncio.gather(task1(), task2())


asyncio.run(main())
