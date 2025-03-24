from langchain_core.tools import StructuredTool
import asyncio

def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

async def main():
    # func 参数：指定一个同步函数。当你在同步上下文中调用工具时，它会使用这个同步函数来执行操作。
    # oroutine 参数：指定一个异步函数。当你在异步上下文中调用工具时，它会使用这个异步函数来执行操作。
    calculator = StructuredTool.from_function(func=multiply, coroutine=amultiply)
    # invoke是同步调用
    print(calculator.invoke({"a": 2, "b": 3}))
    # ainvoke是异步调用
    print(await calculator.ainvoke({"a": 2, "b": 5}))

asyncio.run(main())