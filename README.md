

# 安装依赖

```
pip install langchain
pip install langchain-openai
pip install langchain_community
```

这三个是比较基础的，在运行的过程中，还需要增加一些其他的依赖

# 配置系统环境变量

```bash
OPENAI_API_KEY
OPENAI_API_BASE (可选)
```

如果是用官网的api，就不需要配置`OPENAI_API_BASE`，如果是用第三方的api接口中转，需要配置。

例如使用以下网站：

[https://api.xty.app/register?aff=U22j](https://api.xty.app/register?aff=U22j) （会送一点免费额度）

对应的配置为`OPENAI_API_BASE=https://api.xty.app/v1`

也可以使用阿里百炼的平台，api key获取地址

https://bailian.console.aliyun.com/?apiKey=1#/api-key （每个模型送了一部分的额度）

需要配置的环境变量为

```
DASHSCOPE_API_KEY
```

如果使用阿里百炼的模型，则有些代码需要做以下修改：
将

```python
llm = ChatOpenAI()
```
替换为
```python
chatLLM = ChatOpenAI(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    model="qwen-turbo",  
)
```