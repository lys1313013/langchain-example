from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage

prompt_template = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant"),
    # 可以传入一组消息
    MessagesPlaceholder("msgs")

])
result = prompt_template.invoke({"msgs": [HumanMessage(content="hi!"), HumanMessage(content="hello")]})
print(result)

# 输出
# messages=[SystemMessage(content='You are a helpful assistant', additional_kwargs={}, response_metadata={}), HumanMessage(content='hi!', additional_kwargs={}, response_metadata={}), HumanMessage(content='hello', additional_kwargs={}, response_metadata={})]