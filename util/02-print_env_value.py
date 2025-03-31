import os

# 打印经常使用的一些环境变量值

print(f"OPENAI_API_KEY: {os.getenv('OPENAI_API_KEY')}")
print(f"OPENAI_API_BASE: {os.getenv('OPENAI_API_BASE')}")

print(f"LANGCHAIN_TRACING_V2: {os.getenv('LANGCHAIN_TRACING_V2')}")
print(f"LANGCHAIN_API_KEY: {os.getenv('LANGCHAIN_API_KEY')}")

# Tavily api key
print(f"TAVILY_API_KEY: {os.getenv('TAVILY_API_KEY')}")

# DeepSeek api key
print(f"DEEPSEEK_API_KEY", os.getenv("DEEPSEEK_API_KEY"))
# 阿里百炼 api key
print(f"DASHSCOPE_API_KEY: {os.getenv('DASHSCOPE_API_KEY')}")