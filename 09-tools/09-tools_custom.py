# 使用维基百科
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper
from pydantic import BaseModel, Field

api_wrapper = WikipediaAPIWrapper(top_k_result=1, doc_content_chars_max=100)

class WikiInputs(BaseModel):
    """维基百科工具的输入"""
    query: str = Field(
        description="query to look up in Wikipedia， should be 3 or less words"
    )

tool = WikipediaQueryRun(
    name="wiki-tool",
    description="look ip things in wikipedia",
    args_schema=WikiInputs,
    api_wrapper=api_wrapper,
    return_direct=True,
)

print(tool.run("langchain"))