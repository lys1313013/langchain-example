import json
import random
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/rerank', methods=['POST'])
def rerank():
    """
    模拟 Rerank 接口响应格式
    请求参数示例: {"query":"What is Deep Learning?", "texts": ["Deep Learning is not...", "Deep learning is..."]}
    返回结果示例: [{"index":1,"score":0.9976404},{"index":0,"score":0.12421302}]
    """
    data = request.json
    print(f"接口调用参数:\n{json.dumps(data, ensure_ascii=False, indent=2)}", flush=True)
    
    texts = data.get("texts", [])
    total = len(texts)
    
    # 模拟打分：倒序分配分数，让最后面的文本分数最高
    results = []
    for i in range(total):
        index = total - 1 - i
        # 简单模拟分数，第一个返回最高分（原列表中最后一个），最后一个返回最低分
        score = 0.99 - (0.8 * i / max(1, total - 1)) + random.uniform(0, 0.009)
        results.append({
            "index": index,
            "score": round(score, 7)
        })
        
    return jsonify(results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9004)