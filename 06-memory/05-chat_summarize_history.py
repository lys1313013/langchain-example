# 过往聊天记录总结
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
        ("user", "{input}"),
    ]
)

chat = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    temperature=0,
)

chain = prompt | chat
chain_with_messgaes_history = RunnableWithMessageHistory (
    chain,
    lambda session_id: temp_chat_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)

def summarize_messages(chain_input):
    stored_messages = temp_chat_history.messages
    if len(stored_messages) == 0:
        return False
    summarization_prompt = ChatPromptTemplate.from_messages(
        [
            MessagesPlaceholder(variable_name="chat_history"),
            (
                "user",
                "将上述聊天消息浓缩成一条摘要消息.尽可能包含多个具体细节",
            ),
        ]
    )
    summarization_chain = summarization_prompt | chat
    summary_messages = summarization_chain.invoke({"chat_history": stored_messages})
    temp_chat_history.clear()
    temp_chat_history.add_message(summary_messages)
    return True

chain_with_summarization = (
    RunnablePassthrough.assign(messages_summarized=summarize_messages)
    | chain_with_messgaes_history
)

response = chain_with_summarization.invoke(
    {"input": "名字,下午在干嘛,心情"},
    {"configurable": {"session_id": "unused"}},
)
print(response.content)
print(temp_chat_history.messages)

# 输出示例
"""
名字是张三，下午在打篮球，心情很好。
[AIMessage(content='张三下午打篮球，提问关于自己下午的活动。', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 13, 'prompt_tokens': 70, 'total_tokens': 83, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_name': 'qwen-turbo', 'system_fingerprint': None, 'id': 'chatcmpl-9683a078-e696-954a-a692-073a25bff5c9', 'finish_reason': 'stop', 'logprobs': None}, id='run-588c8cca-33a0-4d71-b665-54d15c82b830-0', usage_metadata={'input_tokens': 70, 'output_tokens': 13, 'total_tokens': 83, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}}), HumanMessage(content='名字,下午在干嘛,心情', additional_kwargs={}, response_metadata={}), AIMessage(content='名字是张三，下午在打篮球，心情很好。', additional_kwargs={'refusal': None}, response_metadata={'token_usage': {'completion_tokens': 13, 'prompt_tokens': 66, 'total_tokens': 79, 'completion_tokens_details': None, 'prompt_tokens_details': {'audio_tokens': None, 'cached_tokens': 0}}, 'model_name': 'qwen-turbo', 'system_fingerprint': None, 'id': 'chatcmpl-0c5e55a9-4689-9a8f-8699-5473e59247b6', 'finish_reason': 'stop', 'logprobs': None}, id='run-b7505feb-d382-48e5-9d67-0f01e6d31a5b-0', usage_metadata={'input_tokens': 66, 'output_tokens': 13, 'total_tokens': 79, 'input_token_details': {'cache_read': 0}, 'output_token_details': {}})]
"""