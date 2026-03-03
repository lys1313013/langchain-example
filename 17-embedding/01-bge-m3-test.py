import os
from openai import OpenAI
import numpy as np

SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
MODEL = "BAAI/bge-m3"

client = OpenAI(
    api_key=SILICONFLOW_API_KEY,
    base_url="https://api.siliconflow.cn/v1"
)


def get_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model=MODEL,
        input=text
    )
    return response.data[0].embedding


def cosine_similarity(a: list[float], b: list[float]) -> float:
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def calculate_similarity(text1: str, text2: str) -> float:
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    return cosine_similarity(emb1, emb2)


if __name__ == "__main__":
    t1 = "今天天气真好"
    t2 = "天气很不错，阳光明媚"
    similarity = calculate_similarity(t1, t2)
    print(f"文本1: {t1}")
    print(f"文本2: {t2}")
    print(f"相似度: {similarity:.4f}")
