# 基于运行内存存储记忆,使用session_id字段
import os
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain_core.chat_history import BaseChatMessageHistory

# 创建一个聊天提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system",
     "You are a helpful assistant who's good at {ability}. Respond in 20 words or fewer"),
    # 历史消息占位符
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}"),
])

# 这里使用阿里百炼的api,用官网的或者其他第三方网站也可以
llm = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    temperature=0,
)

runnable = prompt | llm

store = {}

# 定义获取会话历史的函数,入参是session_id, 返回是会话历史记录
def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


# 创建一个带历史记录的Runnable
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

# 输出示例
"""
content='余弦是三角函数之一，表示一个角的邻边与斜边的比值，在直角三角形中定义。' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 27, 'prompt_tokens': 37, 'total_tokens': 64, 'completion_tokens_details': None, 'prompt_tokens_details': None}, 'model_name': 'qwen-turbo', 'system_fingerprint': None, 'id': 'chatcmpl-cb4f0420-558c-9434-8683-8a2774c7388d', 'finish_reason': 'stop', 'logprobs': None} id='run-71960f82-e3a8-4a72-8985-7867f4238b56-0' usage_metadata={'input_tokens': 37, 'output_tokens': 27, 'total_tokens': 64, 'input_token_details': {}, 'output_token_details': {}}
content='余弦是三角函数，表示角的邻边与斜边之比，用于描述角度与边长关系。' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 25, 'prompt_tokens': 76, 'total_tokens': 101, 'completion_tokens_details': None, 'prompt_tokens_details': None}, 'model_name': 'qwen-turbo', 'system_fingerprint': None, 'id': 'chatcmpl-0bd7e899-ab8b-94b6-b9be-5cc5bbbabc26', 'finish_reason': 'stop', 'logprobs': None} id='run-173def05-79ef-4704-8a2a-c2a98f63c39b-0' usage_metadata={'input_tokens': 76, 'output_tokens': 25, 'total_tokens': 101, 'input_token_details': {}, 'output_token_details': {}}
content='抱歉，我没听清楚您的问题。请再说一遍或具体描述您想了解的内容。' additional_kwargs={'refusal': None} response_metadata={'token_usage': {'completion_tokens': 19, 'prompt_tokens': 34, 'total_tokens': 53, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_name': 'qwen-turbo', 'system_fingerprint': None, 'id': 'chatcmpl-b81b81f2-7d16-9116-870c-6617478fed7a', 'finish_reason': 'stop', 'logprobs': None} id='run-a9aed86f-80f9-43d9-b7c0-9ea7ab6f566a-0' usage_metadata={'input_tokens': 34, 'output_tokens': 19, 'total_tokens': 53, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}
"""
# 第二句话和第一句话用了同样的session_id，所以第二句话获取到了第一句话的记录传给了大模型，所以第二句话接上了第一句话
# 第三局话用了不同的session_id，所以第三句话没有获取到历史记录传给大模型，所以大模型不知道是啥意思。