from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.chat_models import ChatOpenAI

# 能调通，但是不稳定
# 定义一个简单的获取天气的函数，这里只是模拟返回结果
def get_weather(city):
    return f"{city} 当前天气晴朗，温度 25 摄氏度。"


# 创建一个工具
tools = [
    Tool(
        name="GetWeather",
        func=get_weather,
        description="获取指定城市的天气情况，输入为城市名称"
    )
]

# 初始化语言模型
llm = ChatOpenAI(base_url="https://api.xty.app/v1", temperature=0)

# 初始化代理
agent = initialize_agent(tools, llm, agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

# 提出问题
question = "北京的天气如何？"
answer = agent.run(question)

print(answer)
