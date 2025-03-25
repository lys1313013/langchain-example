# 更前面的记忆demo有点重复了
import os

from langchain_community.tools import TavilySearchResults
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from langchain import hub

model = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
)

search = TavilySearchResults(max_results=1)

tools = [search]

# 获取要使用的提示
prompt = hub.pull("hwchase17/openai-functions-agent")
print(prompt.messages)

from langchain.agents import create_tool_calling_agent

agent = create_tool_calling_agent(llm=model, tools=tools, prompt=prompt)

from langchain.agents import AgentExecutor

agent_executor = AgentExecutor(agent=agent, tools=tools)

response = agent_executor.invoke(
    {
        "chat_history": [
            HumanMessage(content="你好，我的名字叫小四"),
            AIMessage(content="你好，小四，请问有什么可以帮到你的吗？"),
        ],
        "input": "我的名字是什么？",
    }
)
print(response)

store = {}


def get_session_history(session_id: str) -> BaseChatMessageHistory:
    if session_id not in store:
        store[session_id] = ChatMessageHistory()
    return store[session_id]


agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    get_session_history,
    input_messages_key="input",
    history_messages_key="chat_history"
)

response = agent_with_chat_history.invoke(
    {"input": "你好 我的名字是小四"},
    config={"configurable": {"session_id": "123"}}
)
print(response)

response = agent_with_chat_history.invoke(
    {"input": "我的名字是什么？"},
    config={"configurable": {"session_id": "123"}}
)
print(response)

response = agent_with_chat_history.invoke(
    {"input": "我的名字是什么？"},
    config={"configurable": {"session_id": "256"}}
)
print(response)
