from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
# 兼容 openai api 接口
model = ChatOpenAI(
    base_url="http://127.0.0.1:11434",  # Ollama 默认端口
    model="deepseek-r1:1.5b",
    temperature=0.3,  # 控制创造性（0-1）
)

# 非流式输出
template = """问题: {question} 答案：让我们一步一步输出答案"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
print(chain.invoke({"question": "什么是 LangChain?"}))