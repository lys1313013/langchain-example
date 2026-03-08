import math
from collections import Counter

docs = [
    '资产管理系统跳转失败问题排查',
    '资产管理模块功能介绍',
    '系统登录跳转失败解决方案',
    '用户权限配置指南',
]

query = '资产管理 跳转 失败'

k1 = 1.5
b  = 0.75

# 改为字符级 ngram 分词（bigram）
def tokenize(text):
    text = text.replace(' ', '')
    return [text[i:i+2] for i in range(len(text)-1)]

doc_tokens = [tokenize(d) for d in docs]
query_tokens = tokenize(query.replace(' ', ''))
N = len(docs)
avgdl = sum(len(d) for d in doc_tokens) / N

def idf(term):
    df = sum(1 for d in doc_tokens if term in d)
    return math.log((N - df + 0.5) / (df + 0.5) + 1)

def bm25(doc_tks, query_tks):
    tf_map = Counter(doc_tks)
    dl = len(doc_tks)
    score = 0
    for term in query_tks:
        tf = tf_map.get(term, 0)
        idf_val = idf(term)
        tf_norm = (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avgdl))
        score += idf_val * tf_norm
    return score

print(f'Query: {query}')
print(f'Query tokens: {query_tokens}')
print()
results = [(docs[i], bm25(doc_tokens[i], query_tokens)) for i in range(N)]
results.sort(key=lambda x: x[1], reverse=True)
for doc, score in results:
    print(f'  [{score:.4f}]  {doc}')