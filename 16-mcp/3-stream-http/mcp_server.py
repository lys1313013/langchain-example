from mcp.server.fastmcp import FastMCP


mcp = FastMCP("weather", host="0.0.0.0", port=12321)

@mcp.tool()
def get_weather(city: str) -> str:
    """根据城市名称获取天气信息"""
    return '气温 30 度，天气晴'

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
