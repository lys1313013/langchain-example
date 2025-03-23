from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_tool_calling_agent

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate
from langchain.globals import set_verbose

llm = ChatOpenAI()
tools = [TavilySearchResults(max_results=1)]
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system", "你是一位得力的助手",
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)
# 构建工具代理
agent = create_tool_calling_agent(llm, tools, prompt)
# 打印详细日志
set_verbose(True)
# 通过传入代理和工具来创建代理执行器
agent_executor = AgentExecutor(agent=agent, tools=tools)
response = agent_executor.invoke(
    {"input": "谁指导了2023年的电影《奥本海默》，他多少岁了？"}
)
print(response)
