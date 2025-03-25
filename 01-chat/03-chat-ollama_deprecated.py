from langchain_community.llms import Ollama
# 不被推荐的方式

# 初始化 Ollama 连接
llm = Ollama(
    base_url="http://127.0.0.1:11434",  # Ollama 默认端口
    model="deepseek-r1:1.5b",
    temperature=0.3,  # 控制创造性（0-1）
    num_ctx=4096  # 上下文长度
)

# 流式输出（适合长文本）
for chunk in llm.stream("LLM 是什么？"):
    print(chunk, end="", flush=True)

print("===========================================================")

# 单次对话
response = llm.invoke("LLM 如何学习？")
print("回答：", response)
