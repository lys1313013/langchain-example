# 导入工具装饰器库
from langchain_core.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

# 打印工具的属性
print(multiply.name)
print(multiply.description)
print(multiply.args)