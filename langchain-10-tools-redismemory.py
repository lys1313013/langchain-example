from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain_community.chat_message_histories import RedisChatMessageHistory
import os


# 定义一个简单的获取天气的函数，这里只是模拟返回结果
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

# 初始化语言模型
llm = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
    temperature=0,
)


# 创建 Redis 记忆存储
def get_redis_memory(session_id):
    message_history = RedisChatMessageHistory(
        url="redis://localhost:6379/0",  # Redis 服务器地址
        ttl=600,  # 记忆存储时间（秒）
        session_id=session_id  # 唯一会话ID
    )

    return ConversationBufferMemory(
        memory_key="chat_history",
        chat_memory=message_history,
        return_messages=True
    )


# 持续对话循环
session_id = input("请输入会话ID（用于记忆存储）：")
memory = get_redis_memory(session_id)

# 初始化带记忆的代理
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,  # 使用支持对话的代理类型
    verbose=True,
    memory=memory,
    handle_parsing_errors=True  # 增加容错处理
)

while True:
    question = input("请输入你的问题（输入 '退出' 结束对话）：")
    if question.lower() == "退出":
        break
    response = agent.invoke({"input": question})
    print(f"助手：{response['output']}")
