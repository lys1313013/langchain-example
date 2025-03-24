from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

api_wrapper = WikipediaAPIWrapper(top_k_result=1, doc_content_chars_max=100)
tool = WikipediaQueryRun(api_wrapper=api_wrapper)
print(tool.invoke({"query": "langchain"}))

print(f"Name: {tool.name}")
print(f"Description: {tool.description}")
print(f"args schema: {tool.args}")
print(f"returns directly?: {tool.return_direct}")
