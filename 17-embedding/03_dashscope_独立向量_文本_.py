import dashscope
import json
import os

import numpy as np

MODEL = "qwen3-vl-embedding"
API_KEY = os.getenv("DASHSCOPE_API_KEY")


def get_mul_embedding(input_data):
    # 使用 qwen3-vl-embedding 生成向量
    resp = dashscope.MultiModalEmbedding.call(
        api_key=API_KEY,
        model=MODEL,
        input=input_data,
        dimension=1024
    )
    return resp.output['embeddings']


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

input_data1 = [
    {
        "text": "你好"
    },
    {
        "text": "测试一下是不是真的是独立的向量，如果真的是独立的向量，那么可以理解为，这是一个批量的接口"
    },
    {
        "text": "你好"
    },
]

input_data2 = [
    {
        "text": "你好"
    }
]


mul_embedding = get_mul_embedding(input_data1)
a_embedding1 = mul_embedding[0]['embedding']
a_embedding2 = mul_embedding[1]['embedding']
a_embedding3 = mul_embedding[2]['embedding']
b_embedding = get_mul_embedding(input_data2)[0]['embedding']
print(mul_embedding)
print(b_embedding)
print(cosine_similarity(a_embedding1, b_embedding))
print(cosine_similarity(a_embedding2, b_embedding))
print(cosine_similarity(a_embedding3, b_embedding))
