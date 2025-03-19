from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain_openai import ChatOpenAI
import os

# 能调通，但是不稳定

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

# 初始化代理
agent = initialize_agent(tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# 提出问题
question = "北京的天气如何？"
# question = "帮我预定一个北京的酒店"
answer = agent.invoke(question)

print(answer)
