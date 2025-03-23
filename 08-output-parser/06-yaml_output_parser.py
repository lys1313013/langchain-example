from langchain.output_parsers import YamlOutputParser
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import os

class Joke(BaseModel):
    setup: str = Field(description="设置笑话的问题")
    punchline: str = Field(description="解决笑话的答案")


model = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    temperature=0
)

joke_query = "告诉我一个笑话."
# 设置一个解析器 + 将指令注入到提示模板中.
parser = YamlOutputParser(pydantic_object=Joke)
prompt = PromptTemplate(
    template="回答用户的查询.\n{format_instructions}\n{query}\n",
    input_variables=["query"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)
chain = prompt | model
print(parser.get_format_instructions())
response = chain.invoke({"query": joke_query})
print(response.content)

# 输出示例
"""
The output should be formatted as a YAML instance that conforms to the given JSON schema below.

# Examples
## Schema
```
{"title": "Players", "description": "A list of players", "type": "array", "items": {"$ref": "#/definitions/Player"}, "definitions": {"Player": {"title": "Player", "type": "object", "properties": {"name": {"title": "Name", "description": "Player name", "type": "string"}, "avg": {"title": "Avg", "description": "Batting average", "type": "number"}}, "required": ["name", "avg"]}}}
```
## Well formatted instance
```
- name: John Doe
  avg: 0.3
- name: Jane Maxfield
  avg: 1.4
```

## Schema
```
{"properties": {"habit": { "description": "A common daily habit", "type": "string" }, "sustainable_alternative": { "description": "An environmentally friendly alternative to the habit", "type": "string"}}, "required": ["habit", "sustainable_alternative"]}
```
## Well formatted instance
```
habit: Using disposable water bottles for daily hydration.
sustainable_alternative: Switch to a reusable water bottle to reduce plastic waste and decrease your environmental footprint.
``` 

Please follow the standard YAML formatting conventions with an indent of 2 spaces and make sure that the data types adhere strictly to the following JSON schema: 
```
{"properties": {"setup": {"description": "\u8bbe\u7f6e\u7b11\u8bdd\u7684\u95ee\u9898", "title": "Setup", "type": "string"}, "punchline": {"description": "\u89e3\u51b3\u7b11\u8bdd\u7684\u7b54\u6848", "title": "Punchline", "type": "string"}}, "required": ["setup", "punchline"]}
```

Make sure to always enclose the YAML output in triple backticks (```). Please do not add anything other than valid YAML output!
```
setup: 为什么电脑去医院？
punchline: 它需要检查一下“病毒”。
```
"""