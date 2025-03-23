from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os

model = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    temperature=0
)

joke_query = "告诉我一个笑话."
parser = JsonOutputParser()
prompt = PromptTemplate(
    template="回答用户的查询.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
chain = prompt | model | parser
response = chain.invoke({"query": joke_query})
for s in chain.stream({"query": joke_query}):
    print(s)

# 输出
"""
{}
{'joke': '为什么'}
{'joke': '为什么电脑去医院？因为它'}
{'joke': '为什么电脑去医院？因为它需要检查一下‘'}
{'joke': '为什么电脑去医院？因为它需要检查一下‘病毒’！'}
"""