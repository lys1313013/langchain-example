import os

def print_env_value(env_name):
    """打印指定环境变量的值"""
    print(f"{env_name}: {os.getenv(env_name)}")

# 打印经常使用的一些环境变量值

# OPENAI
print_env_value("OPENAI_API_KEY")
print_env_value("OPENAI_API_BASE")

print_env_value("LANGCHAIN_TRACING_V2")
print_env_value("LANGCHAIN_API_KEY")

# Tavily api key
print_env_value("TAVILY_API_KEY")

# DeepSeek api key
print_env_value("DEEPSEEK_API_KEY")
# 阿里百炼 api key
print_env_value("DASHSCOPE_API_KEY")

# 查询天气api key 对应网站：https://openweathermap.org/api
print_env_value("OPENWEATHER_API_KEY")