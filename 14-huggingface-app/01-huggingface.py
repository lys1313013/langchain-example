from humanfriendly.terminal import output
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from datasets import load_dataset
# pip install datasets

# 定义数据集名称和任务类型
dataset_name = "imdb"
task = "sentiment-analysis"

# 加载数据集
dataset = load_dataset(dataset_name)

# 打乱数据
dataset = dataset.shuffle()

# 初始化分词器和模型
model_name = "bert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# num_labels=2 意味着模型被设置为进行二分类任务，例如情感分析中的正面和负面分类。模型的输出层将有两个节点，每个节点
model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

# 获取前10条数据集数据
# https://huggingface.co/datasets/stanfordnlp/imdb/viewer?row=0
data = dataset["train"]["text"][:10]

inputs = tokenizer(data, padding=True, truncation=True, return_tensors="pt")

# 将编码后的张量输入模型进行预测
outputs = model(**inputs)

# 获取预测结果和标签
# outputs.logits是一个张量，其中包含模型对每个输入样本的每个类别的预测分数。
# argmax(dim=-1)会在最后一个维度找到最大值的索引，这个索引对应于预测的类别
predictions = outputs.logits.argmax(dim=-1)
labels = dataset["train"]["label"][:10]
# 标签0：在二分类情况分析任务中，0 通常表示“负面”情感
# 标签1：1 通常表示“正面”情感

# 遍历预测结果和真实标签，并打印每个样本的预测结果和真实标签
for i, (prediction, label, text) in enumerate(zip(predictions, labels, data)):
    prediction_label = "正面评论" if prediction == 1 else "负面评论"
    true_label = "正面评论" if label == 1 else "负面评论"
    is_correct = "正确" if prediction == label else "错误"
    print(f"Example {i+1}: Prediction: {prediction_label}, True label: {true_label}, Result: {is_correct}, Text: {text}")

