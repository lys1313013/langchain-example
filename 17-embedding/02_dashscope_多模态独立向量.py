import dashscope
import json
import os
from http import HTTPStatus

# 输入可以是视频
# video = "https://help-static-aliyun-doc.aliyuncs.com/file-manage-files/zh-CN/20250107/lbcemt/new+video.mp4"
# input = [{'video': video}]
# 或图片
image = "https://dashscope.oss-cn-beijing.aliyuncs.com/images/256_1.png"
# 支持独立 embedding
input = [{'image': image}, {'image': image}]
resp = dashscope.MultiModalEmbedding.call(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv('DASHSCOPE_API_KEY'),
    model="tongyi-embedding-vision-plus",
    input=input
)

print(json.dumps(resp.output, indent=4))