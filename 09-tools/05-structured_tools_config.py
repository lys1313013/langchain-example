from langchain_core.tools import StructuredTool
import asyncio
from pydantic import BaseModel, Field


class CalculatorInput(BaseModel):
    a: int = Field(description="first number")
    b: int = Field(description="second number")

def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

async def amultiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

async def main():
    calculator = StructuredTool.from_function(
        func=multiply,
        name="calculator",
        description="multiply numbers",
        args_schema=CalculatorInput,
        return_direct=True,
    )
    print(calculator.invoke({"a": 2, "b": 3}))
    print(calculator.name)
    print(calculator.description)
    print(calculator.args)

asyncio.run(main())