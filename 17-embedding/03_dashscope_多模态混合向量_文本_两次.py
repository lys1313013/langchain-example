import dashscope
import json
import os

import numpy as np

MODEL = "qwen3-vl-embedding"
API_KEY = os.getenv("DASHSCOPE_API_KEY")


def get_embedding(text):
    # 使用 qwen3-vl-embedding 生成向量
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
    return resp.output['embeddings'][0]['embedding']


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# qwen3_vl_embedding 同样的计算结果，每次计算结果会有一定的差别
a_embedding = get_embedding("1")
b_embedding = get_embedding("1")
print(a_embedding)
print(b_embedding)
print(cosine_similarity(a_embedding, b_embedding))
