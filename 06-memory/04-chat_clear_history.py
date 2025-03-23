# 保留两条记录测试不同的问题是否能回答
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnablePassthrough
import os

temp_chat_history = ChatMessageHistory()
temp_chat_history.add_user_message("我叫张三，你好")
temp_chat_history.add_ai_message("你好")
temp_chat_history.add_user_message("我今天心情挺开心")
temp_chat_history.add_ai_message("你今天心情怎么样")
temp_chat_history.add_user_message("我下午在打篮球")
temp_chat_history.add_user_message("你下午在做什么")
temp_chat_history.messages

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "你是一个乐于助人的助手。尽力回答所有问题。提供的聊天历史包括与您交谈的用户试试"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)

chat = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    temperature=0,
)

chain = prompt | chat

# 只取最新的两条记录
def trim_messages(chain_input):
    stored_messages = temp_chat_history.messages
    if len(stored_messages) <= 6:
        return False
    temp_chat_history.clear()
    for message in stored_messages[-6:]:
        temp_chat_history.add_message(message)
    return True


chain_with_message_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: temp_chat_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)
chain_with_trimming = (
        RunnablePassthrough.assign(messages_trimmed=trim_messages)
        | chain_with_message_history
)

# 对话
response = chain_with_trimming.invoke(
    # {"input": "我下午在干啥"},  # 能回答
    {"input": "我是谁"},  # 不能回答
    {"configurable": {"session_id": "unused"}},
)

print(response.content)
print(temp_chat_history.messages)
