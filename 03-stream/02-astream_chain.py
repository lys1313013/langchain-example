from langchain_openai import ChatOpenAI
# 为了支持异步调用
import asyncio
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

prompt = ChatPromptTemplate.from_template("给我讲一个关于{topic}的笑话")
llm = ChatOpenAI()
parser = StrOutputParser()
chain = prompt | llm | parser


async def async_stream():
    async for chunk in chain.astream({"topic": "老虎"}):
        print(chunk, end="", flush=True)


# 运行异步流处理
asyncio.run(async_stream())
