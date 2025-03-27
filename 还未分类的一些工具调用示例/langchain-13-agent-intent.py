# 意图识别demo
from langchain_openai import ChatOpenAI
import os
from langchain.agents import Tool
import requests

def intent(agentName):
    print(f"获取到智能体名称：{agentName} ")
    if agentName == "BookHotel":
        print("正在执行定酒店操作...")
        return f"{agentName} 执行完成"
    elif agentName == "GetWeather":
        print("正在执行获取天气操作...")
        return f"{agentName} 执行完成"
    else:
        print("其他智能体")
        return f"其他智能体：{agentName}"
    # 转发到对应的智能体执行

# 创建一个工具
tools = [
    Tool(
        name="intent",
        func=intent,
        description="意图识别后转发，输入为智能体名称"
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
            "你是一个意图识别智能体。你需要根据用户的输出，识别出对应的意图。现有智能体配置，定酒店：BookHotel，获取天气：GetWeather，其他：other",
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
