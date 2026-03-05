import dashscope
import json
import os

MODEL = "qwen3-vl-embedding"
API_KEY = os.getenv("DASHSCOPE_API_KEY")
text = "这是一段测试文本"

input_data = [
    {
        "text": text
    }
]

resp = dashscope.MultiModalEmbedding.call(
    api_key=API_KEY,
    model=MODEL,
    input=input_data,
    dimension=1024
)

print(json.dumps(resp.output['embeddings'][0]['embedding'], indent=4))