import json
import uuid
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/api/v1/rerank', methods=['POST'])
def rerank():
    """
    模拟 Cohere 接口响应格式
    """
    data = request.json
    print(f"接口调用参数:\n{json.dumps(data, ensure_ascii=False, indent=2)}", flush=True)
    docs = data.get("documents", [])
    total = len(docs)

    # 采用倒序的方式：将最后面的文档赋予最高分并优先返回，同时保留其在原列表中的真实 index
    results = [
        {
            "index": total - 1 - i,
            "relevance_score": 0.99 - (0.01 * i),
            "document": {"text": doc if isinstance(doc, str) else doc.get("text", "")}
        }
        for i, doc in enumerate(reversed(docs))
    ]

    return jsonify({
        "id": str(uuid.uuid4()),
        "results": results,
        "meta": None
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)