import dashscope
import json
import os

# 多模态融合向量：将文本、图片、视频融合成一个融合向量
# 适用于跨模态检索、图搜等场景
text = "这是一段测试文本，用于生成多模态融合向量"
image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"
video = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"

# 输入包含文本、图片、视频，模型会将它们融合成一个融合向量
input_data = [
    {
        "text": text,
        "image": image,
        "video": video
    }
]

# 使用 qwen3-vl-embedding 生成融合向量
resp = dashscope.MultiModalEmbedding.call(
    api_key=os.getenv("DASHSCOPE_API_KEY"),
    model="qwen3-vl-embedding",
    input=input_data,
    dimension=1024
)

print(json.dumps(resp.output, indent=4))