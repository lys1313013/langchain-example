from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM
# 推荐的使用方式

model = OllamaLLM(
    base_url="http://127.0.0.1:11434",  # Ollama 默认端口
    model="deepseek-r1:1.5b",
    temperature=0.3,  # 控制创造性（0-1）
    num_ctx=4096  # 上下文长度
)

# 流式输出
for chunk in model.stream("什么是 LangChain?"):
    print(chunk, end="", flush=True)

# 非流式输出
template = """问题: {question} 答案：让我们一步一步输出答案"""

prompt = ChatPromptTemplate.from_template(template)
chain = prompt | model
print(chain.invoke({"question": "什么是 LangChain?"}))