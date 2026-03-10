"""
Embedding 向量文件相似度计算工具

支持的文件格式：
- JSONL: 每行一个 JSON 对象，embedding 向量在指定字段中
- JSON: 包含 embedding 向量的 JSON 文件
- NPY: NumPy 数组文件

使用示例：
    python embedding_similarity.py file1.jsonl file2.jsonl --field embedding --index 0
"""

import json

import numpy as np
from pathlib import Path
from typing import Union, List, Optional


def load_embedding_from_jsonl(file_path: str, field: str = "embedding", index: int = 0) -> np.ndarray:
    """
    从 JSONL 文件加载 embedding 向量
    
    Args:
        file_path: JSONL 文件路径
        field: embedding 向量所在的字段名
        index: 要读取的行索引（从 0 开始）
    
    Returns:
        embedding 向量（numpy 数组）
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i == index:
                data = json.loads(line.strip())
                if field not in data:
                    raise KeyError(f"字段 '{field}' 在第 {index} 行不存在，可用字段: {list(data.keys())}")
                return np.array(data[field])
    raise IndexError(f"索引 {index} 超出文件行数范围")


def load_embedding_from_json(file_path: str, field: Optional[str] = None) -> np.ndarray:
    """
    从 JSON 文件加载 embedding 向量
    
    Args:
        file_path: JSON 文件路径
        field: embedding 向量所在的字段名（如果为 None，则假设整个文件就是向量）
    
    Returns:
        embedding 向量（numpy 数组）
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 如果数据直接就是列表（向量数组），直接返回
    if isinstance(data, list):
        return np.array(data)
    
    # 如果是字典，尝试从指定字段获取
    if isinstance(data, dict):
        if field is not None and field in data:
            return np.array(data[field])
        elif 'embedding' in data:
            return np.array(data['embedding'])
        else:
            raise ValueError(f"无法自动识别 embedding 字段，可用字段: {list(data.keys())}")
    
    raise ValueError("不支持的 JSON 数据格式")


def load_embedding_from_npy(file_path: str) -> np.ndarray:
    """
    从 NPY 文件加载 embedding 向量
    
    Args:
        file_path: NPY 文件路径
    
    Returns:
        embedding 向量（numpy 数组）
    """
    return np.load(file_path)


def load_embedding(file_path: str, field: str = "embedding", index: int = 0) -> np.ndarray:
    """
    自动检测文件格式并加载 embedding 向量
    
    Args:
        file_path: 文件路径
        field: embedding 向量所在的字段名（用于 JSON/JSONL）
        index: 要读取的行索引（用于 JSONL，从 0 开始）
    
    Returns:
        embedding 向量（numpy 数组）
    """
    path = Path(file_path)
    suffix = path.suffix.lower()
    
    if suffix == '.jsonl':
        return load_embedding_from_jsonl(file_path, field, index)
    elif suffix == '.json':
        return load_embedding_from_json(file_path, field)
    elif suffix == '.npy':
        return load_embedding_from_npy(file_path)
    else:
        # 尝试按 JSONL 格式读取
        try:
            return load_embedding_from_jsonl(file_path, field, index)
        except:
            raise ValueError(f"不支持的文件格式: {suffix}，支持的格式: .jsonl, .json, .npy")


def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    计算两个向量的余弦相似度
    
    Args:
        vec1: 第一个向量
        vec2: 第二个向量
    
    Returns:
        余弦相似度值（范围 [-1, 1]）
    """
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    
    if norm1 == 0 or norm2 == 0:
        raise ValueError("向量的模不能为 0")
    
    return np.dot(vec1, vec2) / (norm1 * norm2)


def euclidean_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    计算两个向量的欧氏距离
    
    Args:
        vec1: 第一个向量
        vec2: 第二个向量
    
    Returns:
        欧氏距离值
    """
    return np.linalg.norm(vec1 - vec2)


def dot_product(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    计算两个向量的点积
    
    Args:
        vec1: 第一个向量
        vec2: 第二个向量
    
    Returns:
        点积值
    """
    return np.dot(vec1, vec2)


def manhattan_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
    """
    计算两个向量的曼哈顿距离
    
    Args:
        vec1: 第一个向量
        vec2: 第二个向量
    
    Returns:
        曼哈顿距离值
    """
    return np.sum(np.abs(vec1 - vec2))


def calculate_all_metrics(vec1: np.ndarray, vec2: np.ndarray) -> dict:
    """
    计算两个向量之间的所有相似度/距离指标
    
    Args:
        vec1: 第一个向量
        vec2: 第二个向量
    
    Returns:
        包含所有指标的字典
    """
    return {
        "cosine_similarity": cosine_similarity(vec1, vec2),
        "euclidean_distance": euclidean_distance(vec1, vec2),
        "dot_product": dot_product(vec1, vec2),
        "manhattan_distance": manhattan_distance(vec1, vec2)
    }


def main():
    # ============ 配置参数 ============
    file1 = "embedding1.json"       # 第一个 embedding 文件路径
    file2 = "embedding2.json"       # 第二个 embedding 文件路径
    field = "embedding"        # embedding 向量所在的字段名
    index1 = 0                 # 第一个文件要读取的行索引
    index2 = 0                 # 第二个文件要读取的行索引
    metric = "all"             # 相似度指标: all, cosine, euclidean, dot, manhattan
    # =================================
    
    # 加载 embedding 向量
    print(f"加载文件 1: {file1} (索引: {index1})")
    vec1 = load_embedding(file1, field, index1)
    print(f"  向量维度: {vec1.shape[0]}")
    
    print(f"加载文件 2: {file2} (索引: {index2})")
    vec2 = load_embedding(file2, field, index2)
    print(f"  向量维度: {vec2.shape[0]}")
    
    # 检查维度是否匹配
    if vec1.shape != vec2.shape:
        print(f"\n警告: 两个向量的维度不匹配！({vec1.shape[0]} vs {vec2.shape[0]})")
        return
    
    print(f"\n{'='*50}")
    print("相似度/距离计算结果:")
    print(f"{'='*50}")
    
    # 计算并输出结果
    if metric == "all":
        metrics = calculate_all_metrics(vec1, vec2)
        print(f"  余弦相似度 (Cosine Similarity):     {metrics['cosine_similarity']:.6f}")
        print(f"  欧氏距离 (Euclidean Distance):      {metrics['euclidean_distance']:.6f}")
        print(f"  点积 (Dot Product):                 {metrics['dot_product']:.6f}")
        print(f"  曼哈顿距离 (Manhattan Distance):    {metrics['manhattan_distance']:.6f}")
    elif metric == "cosine":
        result = cosine_similarity(vec1, vec2)
        print(f"  余弦相似度 (Cosine Similarity):     {result:.6f}")
    elif metric == "euclidean":
        result = euclidean_distance(vec1, vec2)
        print(f"  欧氏距离 (Euclidean Distance):      {result:.6f}")
    elif metric == "dot":
        result = dot_product(vec1, vec2)
        print(f"  点积 (Dot Product):                 {result:.6f}")
    elif metric == "manhattan":
        result = manhattan_distance(vec1, vec2)
        print(f"  曼哈顿距离 (Manhattan Distance):    {result:.6f}")


if __name__ == "__main__":
    main()
