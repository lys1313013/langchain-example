from mcp.server.fastmcp import FastMCP


mcp = FastMCP("Demo", host="0.0.0.0", port=12321)

@mcp.tool()
def get_user_info(user_id: str) -> str:
    """根据用户id查询用户信息"""
    print(f"传入参数：{user_id}")
    return user_id + "用户信息：lys"

@mcp.tool()
async def query_weather(city: str) -> str:
    """
    输入指定城市的名称，返回今日天气查询结果。
    :param city: 城市名称 （必传）
    :return: 格式化后的天气信息
    """
    return city + "温度30摄氏度，正在下冰雹"


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
