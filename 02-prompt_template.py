from langchain.prompts import PromptTemplate

# 定义一个提示词模板，包含adjective 和 content两个模板变量，模板变量使用{}包括起来
prompt_template = PromptTemplate.from_template(
    "给我讲一个关于{content}的{adjective}笑话。"
)

# 通过提示词模板参数格式化提示模板
prompt = prompt_template.format(content="猴子", adjective="冷")
print(prompt)
