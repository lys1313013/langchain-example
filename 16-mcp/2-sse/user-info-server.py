from mcp.server.fastmcp import FastMCP
from starlette.applications import Starlette
from starlette.routing import Mount

mcp = FastMCP("user-info")

@mcp.tool()
def get_user_info(user_id: str) -> str:
    """根据用户id查询用户信息"""
    print(f"传入参数：{user_id}")
    return user_id + "用户信息：lys"

# 挂载SSE服务器到ASGI服务器上
app = Starlette(
    routes=[
        Mount('/', app=mcp.sse_app()),
    ]
)