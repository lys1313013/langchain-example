
# 消息持久化到redis
import os
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory

chat = ChatOpenAI(base_url="https://api.xty.app/v1")
temp_chat_history = ChatMessageHistory()
temp_chat_history.add_user_message("Hello!")
temp_chat_history.add_ai_message("Hi there!")
temp_chat_history.add_user_message("What is your name?")
temp_chat_history.add_ai_message("I am a bot.")
temp_chat_history.messages

prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant who's good at {ability}. Respond in 20 words or fewer"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

model = ChatOpenAI(
    api_key= os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    temperature=0,
)
runnable = prompt | model

store = {}

REDIS_URL = "redis://localhost:6379/0"
def get_session_history(session_id: str) -> RedisChatMessageHistory:
    return RedisChatMessageHistory(session_id, url=REDIS_URL)


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
