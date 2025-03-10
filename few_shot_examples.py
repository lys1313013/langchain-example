from langchain.prompts.few_shot import FewShotPromptTemplate
from langchain.prompts.prompt import PromptTemplate

examples = [
    {
        "question": "谁的寿命更长，穆罕默德·阿里还是艾伦·图灵?",
        "answer":
            """
            这里需要跟进问题吗:是的。
            跟进:穆罕默德·阿里去世时多大?
            中间答案:穆罕默德·阿里去世时74岁。
            跟进:艾伦·图灵去世时多大?
            中间答案:艾伦·图灵去世时41岁。
            所以最终答案是:穆罕默德·阿里
            """
    }, {
        "question": "《大白鲨》和《皇家赌场》的导演都来自同一个国家吗？",
        "answer":
            """
            这里需要跟进问题吗:是的。
            跟进:《大白鲨》的导演是谁?
            中间答案：《大白鲨》的导演是Steven Spielberg
            跟进：Steven Spielberg来自哪里？
            中间答案:美国
            跟进:《皇家赌场》的导演是谁?
            中间答案：《皇家赌场》的导演是Martin Campbell。
            跟进：Martin Campbell来自哪里？
            中间答案: 新西兰。
            所以最终答案是:不是
            """
    }
]

example_prompt = PromptTemplate(input_variables=["question", "answer"], template="问题：{question}\\n{answer}")

prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    suffix="问题，{input}",
    input_variables=["input"]
)

print(prompt.format(input="乔治·华盛顿的父亲是谁"))
