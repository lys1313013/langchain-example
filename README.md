

需配置系统环境变量
```bash
OPENAI_API_KEY
OPENAI_API_BASE (可选项)
```

OPENAI_API_BASE 如果不是用官网api接口，需要配置这个变量

如果不使用官网的api key，可以使用以下地址注册：[https://api.xty.app/register?aff=U22j](https://api.xty.app/register?aff=U22j) 



安装依赖
```bash
pip install langchain
pip install langchain-openai
pip install langchain_community
```

使用阿里百炼的模型
将
```python
llm = ChatOpenAI()
```
替换以下代码即可为
```python
chatLLM = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",  
)
```