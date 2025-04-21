from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount

mcp = FastMCP("calculate-bmi")

@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    print(f"身高: {weight_kg} 体重：{height_m}kg")
    # 打印日志
    return weight_kg / (height_m ** 2)


# 挂载SSE服务器到ASGI服务器上
app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)