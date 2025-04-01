
# 代码内容
LangChain框架练习包含内容：

1. 对话（包含ChatGPT、ollama、deepseek官网api、阿里百炼）
2. 提示词模板
3. 流式输出
4. 还有问题
5. LangSmit、verbose、debug
6. 记忆（内存、Redis）
7. 多模态
8. 输出格式（JSON、XML、YAML）
9. 工具调用
10. agent demo
11. 基于streamlit实现文档上传解析于对话
12. LangGraph例子
13. 未搞定
14. huggingface模型下载与使用
15. browser-use使用

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

第三方网站：[https://api.xty.app/register?aff=U22j](https://api.xty.app/register?aff=U22j) （会送一点免费额度）

对应的配置为`OPENAI_API_BASE=https://api.xty.app/v1`



阿里百炼的平台，api key获取地址

https://bailian.console.aliyun.com/?apiKey=1#/api-key （每个模型送了一部分的额度）

需要配置的环境变量为

```
DASHSCOPE_API_KEY
```

如果使用阿里百炼的地址，将

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