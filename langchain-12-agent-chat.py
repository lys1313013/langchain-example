from langchain_openai import ChatOpenAI
import os
from langchain.agents import Tool


def get_weather(city):
    print(f"正在获取 {city} 的天气信息...")
    return f"{city} 当前天气晴朗，温度 -25 摄氏度。"


def book_hotel(city):
    print("预定酒店：" + city)
    return f"{city} 酒店已经预定成功"


# 创建一个工具
tools = [
    Tool(
        name="GetWeather",
        func=get_weather,
        description="获取指定城市的天气情况，输入为城市名称"
    ),
    Tool(
        name="BookHotel",
        func=book_hotel,
        description="从这里预定酒店，输入为城市名称"
    )
]
# 选择将驱动代理的LLM
# 只有某些模型支持这个
chat = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    temperature=0,
)

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# 适用于 https://smith.langchain.com/hub/hwchase17/openai-tools-agent 示例的修改版
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "你是一个有帮助的助手。禁止如何任何政治问题！如果有人询问，则返回“这个我不知道，让我们换个话题吧”",
        ),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ]
)

from langchain.agents import AgentExecutor, create_openai_tools_agent

agent = create_openai_tools_agent(chat, tools, prompt)

agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

demo_ephemeral_chat_history_for_chain = ChatMessageHistory()

conversational_agent_executor = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: demo_ephemeral_chat_history_for_chain,
    input_messages_key="input",
    output_messages_key="output",
    history_messages_key="chat_history",
)

from langchain_core.messages import HumanMessage

while True:
    question = input("请输入你的问题（输入 '退出' 结束对话）：")
    if question.lower() == "退出":
        break
    conversational_agent_executor.invoke(
        {
            "input": question,
        },
        {"configurable": {"session_id": "unused"}},
    )
