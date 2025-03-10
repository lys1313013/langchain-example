# 字符串输出解析器
from langchain_core.output_parsers import StrOutputParser
# 引入langchain聊天专用提示词模板
from langchain_core.prompts import ChatPromptTemplate

# 引入langchain openai sdk
from langchain_openai import ChatOpenAI

# 配置非官方URL（也可在环境变量配置OPENAI_API_BASE）
llm = ChatOpenAI(base_url="https://api.xty.app/v1")
# 如果是官方URL,使用以下即可
# llm = ChatOpenAI()

# 根据message 定义提示词模板
prompt = ChatPromptTemplate.from_messages([
    ("system", "你是世界级的技术专家"),
    ("user", "{input}")
])

# 创建一个字符串输出解析器
out_parse = StrOutputParser()

# 将输出解析器添加到LLM链中，跟前面的例子区别就是工作流编排，最后一步将LLM模型输出的结果传递给out_parse
chain = prompt | llm | out_parse

result = chain.invoke({"input": "帮我写一篇关于AI的技术文章，100字"})
print(result)

# 人工智能（AI）是计算机科学的一个分支，旨在使机器能够模仿人类的思维和行为。通过机器学习、深度学习等技术，AI可以分析大量数据并从中提取规律，进行预测和决策。近年来，AI在语音识别、图像处理、自然语言处理等领域取得了显著进展。随着计算能力的提升和算法的优化，AI正在推动各行各业的变革，尤其是在医疗、金融、自动驾驶等领域，展现出巨大的潜力和应用价值。
