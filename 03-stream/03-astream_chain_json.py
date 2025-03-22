import asyncio

from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4")
chain = (
        llm | JsonOutputParser()
) # 由于较旧版本的 Langchain 中存在的 bug，JsonOutputParser 未从某些模型中流式传输结果


async def async_stream():
    async for text in chain.astream(
            "以json格式输出法国、西班牙和日本的国家及其人口列表。"
            '使用一个带有"countries"外部键的字典，其中包含国家列表。'
            "每个国家都应该有键`name`和`population`"
    ):
        print(text, flush=True)

# 使用 asyncio.run() 运行异步函数
asyncio.run(async_stream())
