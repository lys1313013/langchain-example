# 导入工具装饰器库
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")


@tool("multiplication-tool", args_schema=CalculatorInput, return_direct=True)
def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b


# 打印工具的属性
print(multiply.name)
print(multiply.description)
print(multiply.args)
print(multiply.return_direct)

print(multiply.invoke({"a": 2, "b": 3}))
