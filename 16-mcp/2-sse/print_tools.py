import asyncio
from fastmcp import Client

# 配置 SSE 协议服务器（已弃用）
config_sse = {
    "mcpServers": {
        "my_legacy_server": {
            "url": "http://0.0.0.0:12322/sse",  # 服务器的 SSE 端点，通常是 /sse 路径
            "transport": "sse"  # 明确指定使用 sse 协议
        }
    }
}

async def main_sse():
    client = Client(config_sse)
    async with client:
        tools = await client.list_tools()
        print("使用 SSE 协议找到的工具:")
        for tool in tools:
            print(f"- {tool.name}")

if __name__ == "__main__":
    # 请根据情况选择运行 main 还是 main_sse
    asyncio.run(main_sse())