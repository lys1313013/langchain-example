from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount

mcp = FastMCP("calculate-bmi")

@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    result = weight_kg / (height_m ** 2)
    print(f"身高: {height_m} 体重：{weight_kg}kg 计算结果：{result}")
    # 打印日志
    return result

# 挂载SSE服务器到ASGI服务器上
app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)