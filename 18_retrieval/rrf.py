"""
加权 RRF (Reciprocal Rank Fusion) 算法实现

RRF 是一种简单但有效的多路排序融合算法，用于将多个检索系统的结果合并为一个统一的排序列表。

公式：
RRF(d) = Σ (w_i / (k + rank_i(d)))

其中：
- d: 文档
- w_i: 第 i 个检索系统的权重
- k: 平滑参数，通常取 60
- rank_i(d): 文档 d 在第 i 个检索系统中的排名（从1开始）
"""

from typing import List, Dict, Any, Tuple, Optional
from collections import defaultdict


def weighted_rrf(
    ranked_lists: List[List[Tuple[str, float]]],
    weights: Optional[List[float]] = None,
    k: int = 60,
) -> List[Tuple[str, float]]:
    """
    加权 RRF 算法

    Args:
        ranked_lists: 多个排序列表，每个列表包含 (doc_id, score) 元组
                     列表顺序即为排序顺序（第一个元素排名最高）
        weights: 各个排序列表的权重，默认为等权重 [1.0, 1.0, ...]
        k: RRF 平滑参数，默认为 60

    Returns:
        融合后的排序列表，包含 (doc_id, rrf_score) 元组

    Example:
        >>> list1 = [("doc1", 0.9), ("doc2", 0.8), ("doc3", 0.7)]
        >>> list2 = [("doc2", 0.95), ("doc1", 0.85), ("doc4", 0.75)]
        >>> result = weighted_rrf([list1, list2], weights=[1.0, 2.0])
    """
    if not ranked_lists:
        return []

    # 默认等权重
    if weights is None:
        weights = [1.0] * len(ranked_lists)

    if len(weights) != len(ranked_lists):
        raise ValueError(f"权重数量({len(weights)})与排序列表数量({len(ranked_lists)})不匹配")

    # 存储每个文档的 RRF 分数
    doc_scores: Dict[str, float] = defaultdict(float)

    # 存储每个文档在各列表中的原始分数（可选，用于调试）
    doc_original_scores: Dict[str, List[Tuple[int, float, float]]] = defaultdict(list)

    for list_idx, (ranked_list, weight) in enumerate(zip(ranked_lists, weights)):
        for rank, (doc_id, score) in enumerate(ranked_list, start=1):
            # RRF 分数计算：weight / (k + rank)
            rrf_contribution = weight / (k + rank)
            doc_scores[doc_id] += rrf_contribution
            doc_original_scores[doc_id].append((list_idx, rank, score))

    # 按分数降序排序
    sorted_results = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)

    return sorted_results


def weighted_rrf_with_metadata(
    ranked_lists: List[List[Dict[str, Any]]],
    id_field: str = "id",
    score_field: str = "score",
    weights: Optional[List[float]] = None,
    k: int = 60,
) -> List[Dict[str, Any]]:
    """
    带元数据的加权 RRF 算法

    Args:
        ranked_lists: 多个排序列表，每个列表包含文档字典
        id_field: 文档ID字段名
        score_field: 分数字段名
        weights: 各个排序列表的权重
        k: RRF 平滑参数

    Returns:
        融合后的排序列表，包含文档字典，新增 rrf_score 字段
    """
    if not ranked_lists:
        return []

    if weights is None:
        weights = [1.0] * len(ranked_lists)

    if len(weights) != len(ranked_lists):
        raise ValueError(f"权重数量({len(weights)})与排序列表数量({len(ranked_lists)})不匹配")

    # 存储每个文档的 RRF 分数和元数据
    doc_scores: Dict[str, float] = defaultdict(float)
    doc_metadata: Dict[str, Dict[str, Any]] = {}

    for list_idx, (ranked_list, weight) in enumerate(zip(ranked_lists, weights)):
        for rank, doc in enumerate(ranked_list, start=1):
            doc_id = doc[id_field]
            rrf_contribution = weight / (k + rank)
            doc_scores[doc_id] += rrf_contribution

            # 保留第一次出现的文档元数据
            if doc_id not in doc_metadata:
                doc_metadata[doc_id] = doc.copy()

    # 构建结果
    results = []
    for doc_id, rrf_score in sorted(doc_scores.items(), key=lambda x: x[1], reverse=True):
        result = doc_metadata[doc_id].copy()
        result["rrf_score"] = rrf_score
        results.append(result)

    return results


def normalize_weights(weights: List[float]) -> List[float]:
    """
    归一化权重，使权重之和为 1

    Args:
        weights: 原始权重列表

    Returns:
        归一化后的权重列表
    """
    total = sum(weights)
    if total == 0:
        return [1.0 / len(weights)] * len(weights)
    return [w / total for w in weights]


# ============ 示例用法 ============

if __name__ == "__main__":
    # 示例：模拟 BM25 和 向量检索 两个系统的结果
    bm25_results = [
        ("doc1", 0.95),
        ("doc3", 0.85),
        ("doc5", 0.75),
        ("doc2", 0.65),
        ("doc7", 0.55),
    ]

    vector_results = [
        ("doc2", 0.92),
        ("doc4", 0.88),
        ("doc1", 0.82),
        ("doc6", 0.78),
        ("doc3", 0.72),
    ]

    print("=" * 60)
    print("RRF 算法示例")
    print("=" * 60)

    # 1. 等权重 RRF
    print("\n1. 等权重 RRF (k=60):")
    result = weighted_rrf([bm25_results, vector_results])
    for rank, (doc_id, score) in enumerate(result, start=1):
        print(f"  Rank {rank}: {doc_id} (RRF score: {score:.6f})")

    # 2. 加权 RRF（BM25 权重更高）
    print("\n2. 加权 RRF (BM25权重=2.0, 向量权重=1.0, k=60):")
    result = weighted_rrf([bm25_results, vector_results], weights=[2.0, 1.0])
    for rank, (doc_id, score) in enumerate(result, start=1):
        print(f"  Rank {rank}: {doc_id} (RRF score: {score:.6f})")

    # 3. 加权 RRF（向量检索权重更高）
    print("\n3. 加权 RRF (BM25权重=1.0, 向量权重=2.0, k=60):")
    result = weighted_rrf([bm25_results, vector_results], weights=[1.0, 2.0])
    for rank, (doc_id, score) in enumerate(result, start=1):
        print(f"  Rank {rank}: {doc_id} (RRF score: {score:.6f})")

    # 4. 不同 k 值的影响
    print("\n4. 不同 k 值的影响 (k=10):")
    result = weighted_rrf([bm25_results, vector_results], k=10)
    for rank, (doc_id, score) in enumerate(result, start=1):
        print(f"  Rank {rank}: {doc_id} (RRF score: {score:.6f})")

    # 5. 带元数据的 RRF
    print("\n5. 带元数据的加权 RRF:")
    bm25_with_meta = [
        {"id": "doc1", "score": 0.95, "title": "文档1", "source": "bm25"},
        {"id": "doc3", "score": 0.85, "title": "文档3", "source": "bm25"},
        {"id": "doc2", "score": 0.65, "title": "文档2", "source": "bm25"},
    ]
    vector_with_meta = [
        {"id": "doc2", "score": 0.92, "title": "文档2", "source": "vector"},
        {"id": "doc4", "score": 0.88, "title": "文档4", "source": "vector"},
        {"id": "doc1", "score": 0.82, "title": "文档1", "source": "vector"},
    ]
    result = weighted_rrf_with_metadata(
        [bm25_with_meta, vector_with_meta],
        weights=[1.0, 1.5],
    )
    for rank, doc in enumerate(result, start=1):
        print(f"  Rank {rank}: {doc['id']} - {doc['title']} (RRF: {doc['rrf_score']:.6f})")
