import os

from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.tools import TavilySearchResults
from langchain_community.vectorstores import FAISS
from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.tools import create_retriever_tool
from langchain_openai import ChatOpenAI
from langchain_text_splitters import RecursiveCharacterTextSplitter

loader = WebBaseLoader("https://zh.wikipedia.org/wiki/%E7%8C%AB")
docs = loader.load()
documents = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200
).split_documents(docs)

# 将网页文本转换为向量并存储
embeddings = DashScopeEmbeddings(model="text-embedding-v3")
vector = FAISS.from_documents(documents, embeddings)
retriever = vector.as_retriever()

retriever_tool = create_retriever_tool(
    retriever,
    "wiki_search",
    "搜索维基百科"
)

model = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",
)

search = TavilySearchResults(max_results=1)

tools = [search, retriever_tool]

from langchain import hub
# 获取要使用的提示
prompt = hub.pull("hwchase17/openai-functions-agent")
print(prompt.messages)

from langchain.agents import create_tool_calling_agent
agent = create_tool_calling_agent(model, tools, prompt)

from langchain.agents import AgentExecutor
agent_executor = AgentExecutor(agent=agent, tools=tools)

response = agent_executor.invoke(
    {
        "chat_history": [
            HumanMessage(content="你好，我的名字叫小四"),
            AIMessage(content="你好，小四，请问有什么可以帮到你的吗？"),
        ],
        "input": "我的名字是什么？",
    }
)
print(response)