from langchain_core.output_parsers import XMLOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import os
# pip install defusexml

model = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    temperature=0
)

action_query = "生成周星驰的简化电影作品列表,按照最新的顺序降序"
parser = XMLOutputParser()
prompt = PromptTemplate(
    template="回答用户的查询.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
chain = prompt | model
response = chain.invoke({"query": action_query})
xml_output = parser.parse(response.content)
print(response.content)

# 输出
"""
```xml
<movie_list>
    <movie>
        <title>美人鱼</title>
        <year>2016</year>
    </movie>
    <movie>
        <title>西游降魔篇</title>
        <year>2013</year>
    </movie>
    <movie>
        <title>长江七号</title>
        <year>2008</year>
    </movie>
    <movie>
        <title>功夫</title>
        <year>2004</year>
    </movie>
    <movie>
        <title>少林足球</title>
        <year>2001</year>
    </movie>
</movie_list>
```
"""