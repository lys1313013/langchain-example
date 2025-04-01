# browser_use 使用demo
# 项目地址：browser_use
import os

from langchain_openai import ChatOpenAI
from browser_use import Agent
import asyncio
from dotenv import load_dotenv

load_dotenv()


async def main():
    agent = Agent(
        task="github 本年度最热门的项目 请打印访问地址",
        llm=ChatOpenAI(api_key=os.getenv("DASHSCOPE_API_KEY"),
                       base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
                       model="qwen-turbo"),  # 这里一定要配置对，否则它会卡在第一步
    )
    await agent.run()


asyncio.run(main())
