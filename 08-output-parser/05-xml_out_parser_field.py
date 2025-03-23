# 指定字段名称
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

joke_query = "生成周星驰的简化电影作品列表,按照最新的顺序降序"
parser = XMLOutputParser(tags=["movies", "actor", "film", "name", "genre"])
prompt = PromptTemplate(
    template="回答用户的查询.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
chain = prompt | model
response = chain.invoke({"query": joke_query})
xml_output = parser.parse(response.content)
print(response.content)

# 输出
"""
```xml
<movies>
    <actor>
        <name>周星驰</name>
        <film>
            <name>美人鱼</name>
            <genre>喜剧</genre>
        </film>
        <film>
            <name>西游降魔篇</name>
            <genre>奇幻, 喜剧</genre>
        </film>
        <film>
            <name>功夫</name>
            <genre>动作, 喜剧</genre>
        </film>
        <film>
            <name>少林足球</name>
            <genre>喜剧, 动作</genre>
        </film>
    </actor>
</movies>
```
"""