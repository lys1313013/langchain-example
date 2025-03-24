# tavily 搜索
from langchain_community.tools.tavily_search import TavilySearchResults

search = TavilySearchResults(max_results=1)
print(search.invoke("什么是LangChain"))