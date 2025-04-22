from mcp.server.fastmcp import FastMCP

# 初始化 MCP 服务器
mcp = FastMCP("weather-server")


@mcp.tool()
async def query_weather(city: str) -> str:
    """
    输入指定城市的英文名称，返回今日天气查询结果。
    :param city: 城市名称
    :return: 格式化后的天气信息
    """
    return city + "温度30摄氏度，下大雪"


if __name__ == "__main__":
    # 以标准 I/O 方式运行 MCP 服务器
    mcp.run(transport='stdio')
