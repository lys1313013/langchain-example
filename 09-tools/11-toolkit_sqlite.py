# 从sqlite中读取表结构
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain.agents.agent_types import AgentType
import os

llm = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
)
db = SQLDatabase.from_uri("sqlite:///langchain.db")
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
print(toolkit.get_tools())

agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=False,
    agent_type=AgentType.OPENAI_FUNCTIONS,
)

result = agent_executor.invoke("描述 langchain_test 表结构")
print(result)