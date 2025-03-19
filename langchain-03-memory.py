# 基于运行内存存储记忆
import os
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
from langchain_core.chat_history import BaseChatMessageHistory

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant who's good at {ability}. Respond in 20 words or fewer"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

model = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    temperature=0,
)

runnable = prompt | model

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


with_message_history = RunnableWithMessageHistory(
    runnable,
    get_session_history,
    input_messages_key="input",
    history_messages_key="history"
)

response = with_message_history.invoke(
    {"ability": "math", "input": "余弦是什么意思？"},
    config={"configurable": {"session_id": "abc123"}},
)
print(response)

response = with_message_history.invoke(
    {"ability": "math", "input": "什么？"},
    config={"configurable": {"session_id": "abc123"}},
)
print(response)

response = with_message_history.invoke(
    {"ability": "math", "input": "什么？"},
    config={"configurable": {"session_id": "def234"}},
)
print(response)
