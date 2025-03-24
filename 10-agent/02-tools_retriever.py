from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_core.tools import create_retriever_tool
from langchain_text_splitters import RecursiveCharacterTextSplitter

# 因为没有openai的额度了，我这里调用的是dashscope的embedding
from langchain_community.embeddings import DashScopeEmbeddings
# pip install faiss-cpu
# pip install dashscope
import os

loader = WebBaseLoader("https://zh.wikipedia.org/wiki/%E7%8C%AB")
docs = loader.load()
documents = RecursiveCharacterTextSplitter(
    # chunk_size 参数在 RecursiveCharacterTextSplitter 中用于指定每个文档块的最大字符数。它的作用主要有一下两个方面：
    # chunk_overlap 参数用于指定每个文档块之间的重叠字符数。这意味着，当文档被拆分成较小的块时，每个块的末尾部分会与下一个快的开发部分重叠。
    # 第一块包含字符1到1000, 第二个块包含字符801到1800，第三个块包含字符1601到2600。
    chunk_size=1000, chunk_overlap=200
).split_documents(docs)
# 将网页文本转换为向量并存储
embeddings = DashScopeEmbeddings(model="text-embedding-v3")
vector = FAISS.from_documents(documents, embeddings)
retriever = vector.as_retriever()

print(retriever.invoke("猫的特征")[0])

retriever_tool = create_retriever_tool(
    retriever,
    "wiki_search",
    "搜索维基百科"
)
